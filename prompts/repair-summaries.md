# ซ่อมข่าวที่ย่อไม่สำเร็จ (Claude Sonnet ทุกเช้า)

งานนี้คือ **ย่อข่าวอย่างเดียว** แทนโมเดลฟรีที่พลาด ห้ามใส่ความเห็นหรือวิเคราะห์ (กติกาข้อ 1 ใน `CLAUDE.md`)

## ขั้นตอน

0. `python -m pip install -q -r requirements.txt pytest` (ใช้ `python -m pip` เสมอ เพราะ `pip` เฉยๆ ในเครื่องนี้ลงคนละ python)
1. `python scripts/collect.py --repair-pending /tmp/pending.json`
   - ถ้าขึ้น `no data for ... yet` (เก็บข่าว 06:00 ยังไม่เสร็จ) หรือ `0 items need a summary` → จบเลย ไม่ต้อง commit
2. อ่าน `/tmp/pending.json` ทำตาม `rules` ในไฟล์ทุกข้อ (ใช้แค่ title/text ที่ให้มา ห้ามเปิดเว็บเติม ห้ามเดา)
3. เขียน `/tmp/summaries.json` รูปแบบ:
   `{"items":[{"id":"...","importance":0-3,"summary_th":"...","numbers":[],"tags":[],"entities":[]}]}`
   ใส่ทุก id ที่ได้มา id ละครั้ง
4. `python scripts/collect.py --repair-apply /tmp/summaries.json` (สคริปต์กรองตัวเลขที่ไม่มีในต้นทางทิ้งเอง)
5. `python -m pytest -q tests` ต้องผ่าน
6. commit ข้อความ `news: YYYY-MM-DD repair` แล้ว push เข้า `main` (ชนให้ `git pull --rebase origin main` แล้ว push ใหม่)

## ห้าม

- ห้ามแก้ข่าวที่ย่อสำเร็จแล้ว ห้ามแก้ไฟล์อื่นนอกจากที่สคริปต์เขียน (`data/`, `news/`, `data/state/seen.json`)
- ห้ามเปิด PR
