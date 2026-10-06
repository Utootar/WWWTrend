"""Free-model clients (Gemini primary, OpenRouter fallback).

Only public news text ever goes through here. Never pass portfolio or
company data to these providers: free tiers may train on inputs.
"""
import json
import os
import re
import time

import requests

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
KEY_ENV = {"gemini": "GEMINI_API_KEY", "openrouter": "OPENROUTER_API_KEY"}


class LLMError(Exception):
    pass


class RateLimited(LLMError):
    def __init__(self, msg, wait):
        super().__init__(msg)
        self.wait = wait


class ModelGone(LLMError):
    """Model name unknown or retired: skip it for the rest of the run."""


def _raise_for(resp, who):
    if resp.status_code == 429:
        wait = resp.headers.get("retry-after")
        raise RateLimited(f"{who} 429", float(wait) if wait and wait.isdigit() else 20.0)
    if resp.status_code == 404:
        raise ModelGone(f"{who} 404 {resp.text[:200]}")
    if resp.status_code >= 400:
        raise LLMError(f"{who} {resp.status_code} {resp.text[:300]}")


def call_gemini(model, system, prompt, key, timeout=120):
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"},
    }
    resp = requests.post(GEMINI_URL.format(model=model), json=body,
                         headers={"x-goog-api-key": key}, timeout=timeout)
    _raise_for(resp, f"gemini/{model}")
    data = resp.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError):
        raise LLMError(f"gemini/{model} empty response: {json.dumps(data)[:300]}")
    return "".join(p.get("text", "") for p in parts if not p.get("thought"))


def call_openrouter(model, system, prompt, key, timeout=180):
    body = {
        "model": model,
        "temperature": 0.2,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": prompt}],
    }
    headers = {"Authorization": f"Bearer {key}", "X-Title": "WWWTrend"}
    resp = requests.post(OPENROUTER_URL, json=body, headers=headers, timeout=timeout)
    _raise_for(resp, f"openrouter/{model}")
    data = resp.json()
    if "error" in data:
        raise LLMError(f"openrouter/{model} {str(data['error'])[:300]}")
    try:
        return data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError):
        raise LLMError(f"openrouter/{model} empty response: {json.dumps(data)[:300]}")


CALLERS = {"gemini": call_gemini, "openrouter": call_openrouter}


def parse_json(text):
    """Pull the JSON object out of a model reply (tolerates ``` fences and chatter)."""
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise LLMError(f"no JSON object in reply: {text[:200]}")
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as e:
        raise LLMError(f"bad JSON: {e}: {text[start:start + 200]}")


class Summarizer:
    """Tries each (provider, model) in config order until one returns valid JSON."""

    def __init__(self, cfg, env=os.environ, callers=CALLERS, sleep=time.sleep, log=print):
        self.min_interval = cfg.get("min_interval_sec", 0)
        self.sleep = sleep
        self.log = log
        self.callers = callers
        self.chain = []
        for p in cfg["providers"]:
            key = env.get(KEY_ENV[p["provider"]], "").strip()
            if not key:
                log(f"::warning::{KEY_ENV[p['provider']]} not set, skipping {p['provider']}")
                continue
            self.chain += [(p["provider"], m, key) for m in p["models"]]
        self.gone = set()
        self._last_call = 0.0

    @property
    def available(self):
        return bool(self.chain)

    def _throttle(self):
        wait = self._last_call + self.min_interval - time.monotonic()
        if wait > 0:
            self.sleep(wait)
        self._last_call = time.monotonic()

    def run(self, system, prompt):
        """Return (parsed_json, "provider/model"). Raises LLMError if every model failed."""
        errors = []
        for provider, model, key in self.chain:
            name = f"{provider}/{model}"
            if name in self.gone:
                continue
            for attempt in range(2):
                self._throttle()
                try:
                    return parse_json(self.callers[provider](model, system, prompt, key)), name
                except RateLimited as e:
                    errors.append(str(e))
                    if attempt == 0 and e.wait <= 60:
                        self.sleep(e.wait)
                        continue
                except ModelGone as e:
                    self.gone.add(name)
                    errors.append(str(e))
                except (LLMError, requests.RequestException) as e:
                    errors.append(f"{name}: {e}")
                break
        raise LLMError("all models failed: " + " | ".join(errors[-6:]))
