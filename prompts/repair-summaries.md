# ซ่อมข่าวที่ย่อไม่สำเร็จ (Claude Haiku ทุกวัน ใช้โควต้า sub)

งานนี้คือ **ย่อข่าวอย่างเดียว** แทนโมเดลฟรีที่พลาด ห้ามใส่ความเห็นหรือวิเคราะห์ (กติกาข้อ 1 ใน `CLAUDE.md`)

**ในขั้นตอน GitHub Actions** (ต่อจากเก็บข่าว ใช้ token ของ sub) ทำแค่ข้อ 0–4 ห้ามรัน pytest/commit/push เพราะ workflow commit ให้เอง

ซ่อม 2 วัน: วันนี้ก่อน แล้วเมื่อวาน (เก็บตกถ้ารอบก่อนพลาดหรือข่าวเข้าช้า) ทำทีละวัน

## ขั้นตอน (ทำซ้ำสำหรับแต่ละวัน D = วันนี้, เมื่อวาน เวลาไทย: `TZ=Asia/Bangkok date -d "<today|yesterday>" +%F`)

0. `python -m pip install -q -r requirements.txt pytest` (ใช้ `python -m pip` เสมอ เพราะ `pip` เฉยๆ ในเครื่องนี้ลงคนละ python) ทำครั้งเดียว
1. `python scripts/collect.py --repair-pending /tmp/pending-D.json --date D`
   - ถ้าขึ้น `no data for ... yet` หรือ `0 items need a summary` → ข้ามวันนั้น
2. อ่าน `/tmp/pending-D.json` ทำตาม `rules` ในไฟล์ทุกข้อ (ใช้แค่ title/text ที่ให้มา ห้ามเปิดเว็บเติม ห้ามเดา)
3. เขียน `/tmp/summaries-D.json` รูปแบบ:
   `{"items":[{"id":"...","importance":0-3,"summary_th":"...","numbers":[],"tags":[],"entities":[]}]}`
   ใส่ทุก id ที่ได้มา id ละครั้ง
4. `python scripts/collect.py --repair-apply /tmp/summaries-D.json --date D` (สคริปต์กรองตัวเลขที่ไม่มีในต้นทางทิ้งเอง)

หลังครบทุกวัน ถ้ามีวันที่ซ่อม:
5. `python -m pytest -q tests` ต้องผ่าน
6. commit ข้อความ `news: YYYY-MM-DD repair` แล้ว push เข้า `main` (ชนให้ `git pull --rebase origin main` แล้ว push ใหม่)

ถ้าทั้งสองวันไม่มีอะไรซ่อม จบเลย ไม่ต้อง commit

## ห้าม

- ห้ามแก้ข่าวที่ย่อสำเร็จแล้ว ห้ามแก้ไฟล์อื่นนอกจากที่สคริปต์เขียน (`data/`, `news/`, `data/state/seen.json`)
- ห้ามเปิด PR
