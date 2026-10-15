# ธีมลงทุนที่เจอจากข่าว → หุ้นที่เกี่ยวข้อง

Claude เขียนไฟล์นี้จากข่าวที่เก็บมา (`news/`, `data/`) ไม่ใช่รายชื่อตั้งไว้ล่วงหน้า
ธีมไหนข่าวเงียบเกิน 3 สัปดาห์ ให้ย้ายลง "ธีมที่จบแล้ว" พร้อมเหตุผล
ไม่ใช่คำแนะนำการลงทุน หุ้นที่เจ้าของถือจริงอยู่ใน `memory/private.md` เท่านั้น

รูปแบบแต่ละธีม:

```
## <ชื่อธีม> (เริ่มเจอ YYYY-MM-DD · ล่าสุด YYYY-MM-DD)
ทำไม: <เหตุผล 1-2 บรรทัด>
หลักฐานจากข่าว: <หัวข่าวสั้น [ลิงก์]> (ใส่ 2-5 ข่าวล่าสุด)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
ที่มา: "ข่าว" = บริษัทนี้อยู่ในข่าวเอง (มีลิงก์ข้างบน) · "ความรู้ทั่วไป" = Claude เติมเองว่าอยู่ในกลุ่มเดียวกัน
ความเสี่ยงของธีม: ...
```

## ธีมที่กำลังเดิน

## ไฟฟ้าจาก AI: ไฟฟ้า นิวเคลียร์ ระบบไฟ (เริ่มเจอ 2026-10-06 · ล่าสุด 2026-10-14)
ทำไม: data center และ AI ใช้ไฟมากขึ้น ผู้ผลิตและผู้รับเหมาระบบไฟได้งาน
หลักฐานจากข่าว: นิวเคลียร์พุ่ง · MYR/Powell/Comfort Systems พุ่ง · GE Vernova ราคาวิ่ง · X-energy (ดู analysis/2026-10/2026-10-07-2day.md)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| GEV | US | เทอร์ไบน์ อุปกรณ์ไฟ | ข่าว |
| POWL, MYR, FIX | US | ผู้รับเหมา/อุปกรณ์ไฟ | ข่าว |
| CEG, VST | US | ขายไฟนิวเคลียร์/ไฟให้ data center | ความรู้ทั่วไป |
| GULF.BK, GPSC.BK | TH | ผู้ผลิตไฟ (ทางอ้อม) | ความรู้ทั่วไป |
อัปเดต 2026-10-10: ไม่มีข่าวบริษัทใหม่ แต่ราคาแกว่งตามข่าวรายได้ OpenAI (8 ต.ค. CEG -4.85% VST -6.35% แล้ว 9 ต.ค. CEG +4.56% VST +3.42%) GEV นิ่งสุด (ดู analysis/2026-10/2026-10-10-2day.md) หลักฐาน: [ศูนย์ข้อมูลเป็นอสังหา ความเสี่ยงเพิ่ม](https://www.cnbc.com/2026/10/09/ai-data-centers-investing.html) · [AI ร่วงจากข่าวรายได้ OpenAI](https://www.cnbc.com/2026/10/08/open-ai-revenue-nvidia-oracle-coreweave.html)
อัปเดต 2026-10-11 (weekly): ทั้งสัปดาห์ GEV -2.4% POWL -6.2% FIX -5.6% CEG -0.8% VST +0.6% GPSC +4.6% GULF +1.3% ผู้รับเหมาคืนกำไรที่พุ่ง 6 ต.ค. หลักฐานใหม่: [เฟดชี้ data center ดันราคา](https://news.google.com/rss/articles/CBMisAFBVV95cUxOY1FrWkF5TURpdC1qQ3NITm9zVDhQVXJaaXM5aVVYZ0doMEhWaTNid1Q3b1Bfdzg5c01lVGVSOVhjZHhBQTZEUlhHR3diMG96NnBZR25RQWp5U1JuWGJYOHNIT0FJNEd6TVlubGNwQzRGRXA0bUZsTno3YjFmUVpJNVl0NFozV1F4T0Z2QUhkRVdNQW8xR1Nab1NIRWl0VlZaMVRic0F3ak50TzlYSW8wRA?oc=5) · [Google หยุดสร้าง data center ฟินแลนด์](https://www.cnbc.com/2026/10/07/google-finland-data-center-halt.html) · [รัฐหนุน VPP](https://oilprice.com/Energy/Energy-General/States-Bet-on-Virtual-Power-Plants-to-Cut-Grid-Costs.html)
MYR ชื่อย่อจริงคือ MYRG แก้ใน theme_stocks.yaml แล้ว
อัปเดต 2026-10-13: Uranium ETF ตก >20% ใน 12 เดือน แม้เทคซื้อไฟนิวเคลียร์ [OilPrice](https://oilprice.com/Alternative-Energy/Nuclear-Power/3-Stocks-To-Play-The-Nuclear-Energy-Boom.html) · Petra Power เซลล์เชื้อเพลิงให้ data center [TechCrunch](https://techcrunch.com/2026/10/10/petra-power-looks-to-modernize-energy-for-data-centers-and-defense-vehicles/) ราคายังเป็นของ 9 ต.ค. (ดู analysis/2026-10/2026-10-13-2day.md)
อัปเดต 2026-10-15: ไม่มีข่าวบริษัทใหม่ 2 วัน POWL -4.8% FIX -5.2% GEV -0.1% (ดู analysis/2026-10/2026-10-15-2day.md)
ความเสี่ยงของธีม: ราคาอาจนำข่าวไปแล้ว ยีลด์สูง ผูกกับความเชื่อมั่น AI แรงต้าน data center ในพื้นที่

## LNG/ก๊าซนอกอ่าวเปอร์เซีย (เริ่มเจอ 2026-10-07 · ล่าสุด 2026-10-14)
ทำไม: ฮอร์มุซไม่ปลอดภัย Qatar ขยายเหตุสุดวิสัย ผู้ส่งออก LNG/ก๊าซนอกอ่าวได้ออเดอร์
หลักฐานจากข่าว: [5 หุ้นก๊าซได้จากฮอร์มุซ (Cheniere)](https://oilprice.com/Energy/Natural-Gas/5-Natural-Gas-Stocks-Profiting-From-the-Strait-of-Hormuz-Standoff.html) · [Kinder Morgan ส่งก๊าซไปเม็กซิโกได้อีก](https://oilprice.com/Latest-Energy-News/World-News/Kinder-Morgan-Restores-US-Mexico-Gas-Flows-After-Pipeline-Outage.html) · [Alaska LNG กลับมา](https://oilprice.com/Energy/Natural-Gas/Who-Is-Going-to-Pay-for-Alaska-LNG.html)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| LNG | US | ส่งออก LNG | ข่าว |
| KMI | US | ท่อก๊าซ | ข่าว |
| PTTEP.BK | TH | ขายก๊าซ/น้ำมัน | ความรู้ทั่วไป |
| PTT.BK | TH | ก๊าซ+โรงกลั่น (ได้-เสียปน) | ความรู้ทั่วไป |
อัปเดต 2026-10-13: Brent ลง 103.21 หลังข่าวหยุดยิงพลังงานรัสเซีย-ยูเครน แต่ค่าขนส่งสถิติ คลังสำรองสหรัฐต่ำสุดตั้งแต่ 1982 [OilPrice](https://oilprice.com/Energy/Crude-Oil/How-Low-Can-the-Strategic-Petroleum-Reserve-Actually-Go.html)
อัปเดต 2026-10-15: LNG ตะวันออกกลางยังติดค้างหลังผ่านมา 7 เดือนครึ่ง [OilPrice](https://oilprice.com/Energy/Natural-Gas/Stranded-Middle-East-LNG-Supply-Upends-Gas-Markets.html) · Brent 106.86 อิหร่านโจมตีเรือในฮอร์มุซ
ความเสี่ยงของธีม: หยุดยิง/ฮอร์มุซเปิด ราคาก๊าซร่วงเร็ว PTT อาจถูกคุมราคาในประเทศ

## ชิปหน่วยความจำ (เริ่มเจอ 2026-10-08 · ล่าสุด 2026-10-15)
ทำไม: AI ดูดหน่วยความจำ RAM ขาดและแพง ผู้ผลิตกำไรสถิติ
หลักฐานจากข่าว: [Samsung กำไรสถิติ](https://www.cnbc.com/2026/10/08/samsung-q3-earnings.html) · [Intel/AMD กลับไป DDR4 เพราะ RAM แพง](https://www.theverge.com/games/1009140/ram-shortage-intel-amd-ddr4-comeback) · [Micron ร่วงจากข่าว OpenAI](https://www.marketwatch.com/story/micron-nvidia-and-ai-chip-stocks-fall-as-report-on-openais-revenue-causes-undue-concern-2a2bcf53)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| 005930.KS (Samsung) | KR | หน่วยความจำ | ข่าว |
| MU | US | หน่วยความจำ | ข่าว |
| 000660.KS (SK Hynix) | KR | HBM | ความรู้ทั่วไป |
| HANA.BK | TH | ประกอบ/ทดสอบชิป ทางอ้อม | ความรู้ทั่วไป |
อัปเดต 2026-10-15: ร่วงแรง SK Hynix -11.1% Samsung -9.0% Micron -7.4% หลังรายงาน CXMT (จีน) คืบหน้าออกแบบชิป [CNBC](https://www.cnbc.com/2026/10/13/cxmt-memory-chip-stock-rout.html) · [Micron ลงต่อ จีนแข่งแรง](https://www.marketwatch.com/story/microns-stock-extends-declines-as-china-competition-heats-up-b8ec25f0) (ดู analysis/2026-10/2026-10-15-2day.md)
ความเสี่ยงของธีม: วัฏจักรหน่วยความจำกลับลงเร็ว ผูกกับข่าวรายได้ AI จีนเริ่มตามทัน

## ธีมที่จบแล้ว

(ยังไม่มี)
