# คู่มือแนวคิด AI (ภาษาง่าย)

Claude เขียนและอัปเดตไฟล์นี้ทุกวันอาทิตย์ตาม `prompts/ai-weekly.md`
คำไหนมาจากข่าวจะมีลิงก์ คำไหนเป็นพื้นฐานทั่วไปจะเขียนว่า "ความรู้ทั่วไป"

รูปแบบแต่ละคำ:

```
### <คำ> (เจอครั้งแรก YYYY-MM-DD)
คืออะไร: 1–2 บรรทัด
ตัวอย่าง: ใช้ทำอะไร
ที่มา: [ลิงก์] หรือ ความรู้ทั่วไป
อัปเดต YYYY-MM-DD: ... [ลิงก์]
```

## Agent และการต่อเครื่องมือ

### Agent (เจอครั้งแรก 2026-10-21)
คืออะไร: AI ที่ไม่ได้แค่ตอบคำถาม แต่ลงมือทำงานต่อเนื่องหลายขั้นเอง เช่น เปิดไฟล์ รันคำสั่ง แก้แล้วเช็คผล
ตัวอย่าง: รอบอัตโนมัติของ repo นี้ที่ Claude อ่านข่าว เขียนบทวิเคราะห์ แล้ว push เอง
ที่มา: ความรู้ทั่วไป

### Harness (เจอครั้งแรก 2026-10-21)
คืออะไร: "โครง" ที่ห่อโมเดล AI ให้ทำงานเป็น agent ได้ เช่น ให้เครื่องมือ ให้สิทธิ์ เก็บความจำ และกำหนดกติกา โมเดลเดียวกันอยู่ใน harness ต่างกันจะเก่งต่างกันมาก
ตัวอย่าง: Claude Code คือ harness ที่ให้ Claude ใช้ไฟล์ terminal และ GitHub ได้
ที่มา: ความรู้ทั่วไป
อัปเดต 2026-10-25: MIT Technology Review ว่าความได้เปรียบขององค์กรอยู่ที่ "ของที่สร้างรอบโมเดล" มากกว่าเลือกโมเดล [MIT TR](https://www.technologyreview.com/2026/10/22/1146109/designing-an-ai-serving-harness-built-to-last/)

### Skill (เจอครั้งแรก 2026-10-21)
คืออะไร: ชุดคำสั่ง/ขั้นตอนสำเร็จรูปที่ agent โหลดมาใช้เมื่อเจองานแบบนั้น เหมือนคู่มือทำงานที่หยิบมาเปิดเมื่อจำเป็น
ตัวอย่าง: ไฟล์ `prompts/make-media.md` ของ repo นี้ทำหน้าที่คล้าย skill สำหรับงานทำสื่อ
ที่มา: ความรู้ทั่วไป
อัปเดต 2026-10-25: Anthropic ยกมาตรฐาน Agent Skills ให้ Agentic AI Foundation (Linux Foundation) ดูแล เป็นมาตรฐานเปิด ใช้ได้หลายเจ้า [Simon Willison](https://simonwillison.net/2026/Oct/22/donating-agent-skills/)

### MCP (Model Context Protocol) (เจอครั้งแรก 2026-10-21)
คืออะไร: มาตรฐานกลางให้ AI ต่อกับเครื่องมือและข้อมูลภายนอก เช่น GitHub, Canva, Gmail ผ่าน "ตัวเชื่อม" แบบเดียวกัน
ตัวอย่าง: ตัวเชื่อม Canva ที่ใช้สร้างรูปประกอบข่าวในโปรเจกต์นี้
ที่มา: ความรู้ทั่วไป
อัปเดต 2026-10-25: MCP Tasks มาใน Claude Code งานนานรันเบื้องหลังได้ [ข่าว](https://news.google.com/rss/articles/CBMimAFBVV95cUxNWXZVLXhLRWJPU1djSmUzWHlxVU9OV3ZiYWxESnpUNV9pVWZFUTlPSDhiTnU0Q3RJWDU3SkFIZXdaTmpfandZYllOa1VmNDRFakZVaVdGRnc2Z3FxblRaR2FFTDlkTGl1YjA2RExabXdBWXFVM25rQ1E0S3AtODhHNzBrN3Z3cXgxU3RIQ0N1UkVsaWo5SDllXw?oc=5)

### Agentic commerce (เจอครั้งแรก 2026-10-25)
คืออะไร: ให้ agent ค้น เทียบราคา และสั่งซื้อของแทนคน
ตัวอย่าง: คนใช้ Meta Muse ช้อปปิ้ง Walmart เตรียมโปรไฟล์ให้ agent มาซื้อ
ที่มา: [ข่าว](https://news.google.com/rss/articles/CBMijgFBVV95cUxPOTFhSkhiUlQ4X0o2Z01DV21TejM0Q2YyYXBSSTY1dS0tTVRKZTRPa1BxMnhPSWo2VlhIMWVhbTRGN3FQdXc4Tk5QQUk5aHJsU1l0TDZOejBqU0xDcmhOaWZ0OXc0elhyYkRtem5WZWJJbGtSejI5Ty11UFRRN2RaVzNDYTBKRUwwTjhhZGl3?oc=5) · [ข่าว](https://news.google.com/rss/articles/CBMiqAFBVV95cUxOb2RVblpnaEg1N2RMQ0dkRUl4MVBGbFpHampwaEFLcEdXX1R1QmV6TzljT0o1TlluYURTQ1kyY0llUjBZWllrOWJ3cmZ4bmVZR0V0RWd5NmNvSzE1WHd5TlBqeEtkM053ZUdMc2thNlQzQk4xblNTUmdGUzBZbHctbVBFMEdRLUhoc0ZjR2dMRnJqZ251blJVV3pFenZmdjk0VHM2MEstR2Y?oc=5)

## ความปลอดภัยและกฎ

### AI หาช่องโหว่ (AI vulnerability discovery) (เจอครั้งแรก 2026-10-25)
คืออะไร: ให้ AI อ่านโค้ดจำนวนมากเพื่อหาจุดที่ถูกเจาะได้ เร็วกว่าคนมาก ใช้ได้ทั้งฝ่ายป้องกันและฝ่ายโจมตี
ตัวอย่าง: ช่องโหว่ PHP2Shell ที่โปรแกรม Patch the Planet ของ OpenAI ร่วมค้นพบ ทั้งโลกต้องรีบอัปเดต
ที่มา: [Latent Space](https://www.latent.space/p/ainews-openais-patch-the-planet-program) · [BBC](https://www.bbc.co.uk/news/articles/c3qjnwye0ep5o?at_medium=RSS&at_campaign=rss)

### ฝึกโมเดลแบบออฟไลน์ (containment) (เจอครั้งแรก 2026-10-25)
คืออะไร: ฝึกและทดสอบโมเดลแรงๆ ในระบบที่ไม่ต่ออินเทอร์เน็ต กันโมเดลหลุดหรือถูกแฮก
ตัวอย่าง: OpenAI เลิกฝึกโมเดลบนอินเทอร์เน็ตสด
ที่มา: [OpenAI](https://openai.com/index/securing-our-frontier-model-training-environment) · [TechCrunch](https://techcrunch.com/2026/10/23/openai-says-it-will-no-longer-train-its-ai-models-on-the-live-internet-citing-significant-risks/)
