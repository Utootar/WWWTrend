# ซ่อมและตรวจข่าวย่อ (Claude Haiku ทุกวัน ใช้โควต้า sub)

งานนี้มี 2 อย่าง: **ย่อข่าว** ที่โมเดลฟรีพลาด และ **ตรวจแก้** ข่าวที่โมเดลฟรีย่อผิด ห้ามใส่ความเห็นหรือวิเคราะห์ (กติกาข้อ 1 ใน `CLAUDE.md`)

**ในขั้นตอน GitHub Actions** (ต่อจากเก็บข่าว ใช้ token ของ sub) ทำแค่ข้อ 0–8 ห้ามรัน pytest/commit/push เพราะ workflow commit ให้เอง

ข่าว AI (โฟลเดอร์ `ai/`) ใช้ขั้นตอนเดียวกัน แค่เติม `--config config/ai/sources.yaml --root ai` ทุกคำสั่ง `scripts/collect.py` (GitHub ทำให้ต่อจากเก็บข่าว AI)

ซ่อม 2 วัน: วันนี้ก่อน แล้วเมื่อวาน (เก็บตกถ้ารอบก่อนพลาดหรือข่าวเข้าช้า) ทำทีละวัน

## ขั้นตอน (ทำซ้ำสำหรับแต่ละวัน D = วันนี้, เมื่อวาน เวลาไทย: `TZ=Asia/Bangkok date -d "<today|yesterday>" +%F`)

0. `python -m pip install -q -r requirements.txt pytest` (ใช้ `python -m pip` เสมอ เพราะ `pip` เฉยๆ ในเครื่องนี้ลงคนละ python) ทำครั้งเดียว
1. `python scripts/collect.py --repair-pending /tmp/pending-D.json --date D`
   - ถ้าขึ้น `no data for ... yet` → ข้ามวันนั้นทั้งหมด
   - ถ้าขึ้น `0 items need a summary` → ไปข้อ 5 (ตรวจแก้)
2. อ่าน `/tmp/pending-D.json` ทำตาม `rules` ในไฟล์ทุกข้อ (ใช้แค่ title/text ที่ให้มา ห้ามเปิดเว็บเติม ห้ามเดา)
3. เขียน `/tmp/summaries-D.json` รูปแบบ:
   `{"items":[{"id":"...","importance":0-3,"summary_th":"...","numbers":[],"tags":[],"entities":[]}]}`
   ใส่ทุก id ที่ได้มา id ละครั้ง
4. `python scripts/collect.py --repair-apply /tmp/summaries-D.json --date D` (สคริปต์กรองตัวเลขที่ไม่มีในต้นทางทิ้งเอง)

ตรวจแก้ (ทำต่อในวันเดียวกัน):

5. `python scripts/collect.py --review-pending /tmp/review-D.json --date D`
   - ถ้าขึ้น `0 items to check` → ข้าม (ตรวจครบแล้ว)
6. อ่าน `/tmp/review-D.json` เทียบ `summary_th` กับ `title`/`text` ทีละข่าว ตาม `rules` ในไฟล์
   - แก้เฉพาะที่ผิดจริง: ตัวเลขผิด ทิศทางผิด (ขึ้น/ลง) ชื่อหรือวันผิด ใส่สิ่งที่ต้นทางไม่ได้พูด แปลหัวข่าวผิด หรือดาวผิดชัดๆ
   - ถูกแล้วไม่ต้องแตะ ไม่แก้เพราะสำนวน ตัวเลขในข่าวที่แก้ต้องเขียนแบบเดียวกับต้นทาง (สคริปต์ปัดตกถ้าเจอตัวเลขที่ต้นทางไม่มี)
7. เขียน `/tmp/fixes-D.json` รูปแบบ:
   `{"checked":["ทุก id ที่ได้มา"],"fixes":[{"id":"...","reason":"เหตุผลสั้นๆ","summary_th":"...","importance":0-3,"numbers":[]}]}`
   ใน `fixes` ใส่แค่ช่องที่เปลี่ยน (`id` กับ `reason` ต้องมี) ถ้าไม่มีอะไรผิด `fixes` เป็น `[]`
8. `python scripts/collect.py --review-apply /tmp/fixes-D.json --date D` ข่าวที่แก้จะมีป้าย "แก้โดย Claude" ในไฟล์ข่าว

หลังครบทุกวัน ถ้ามีวันที่ซ่อมหรือตรวจ:
9. `python -m pytest -q tests` ต้องผ่าน
10. commit ข้อความ `news: YYYY-MM-DD repair` แล้ว push เข้า `main` (ชนให้ `git pull --rebase origin main` แล้ว push ใหม่)

ถ้าทั้งสองวันไม่มีอะไรซ่อมและตรวจครบแล้ว จบเลย ไม่ต้อง commit

## ห้าม

- ห้ามแก้ไฟล์ข่าวเองด้วยมือ แก้ผ่านสคริปต์ข้อ 4 และ 8 เท่านั้น ห้ามแก้ไฟล์อื่นนอกจากที่สคริปต์เขียน (`data/`, `news/`, `data/state/seen.json`)
- ห้ามเปิด PR
