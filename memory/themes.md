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

## ไฟฟ้าจาก AI: ไฟฟ้า นิวเคลียร์ ระบบไฟ (เริ่มเจอ 2026-10-06 · ล่าสุด 2026-10-15)
ทำไม: data center และ AI ใช้ไฟมากขึ้น ผู้ผลิตและผู้รับเหมาระบบไฟได้งาน
หลักฐานจากข่าว: นิวเคลียร์พุ่ง · MYR/Powell/Comfort Systems พุ่ง · GE Vernova ราคาวิ่ง · X-energy (ดู analysis/2026-10/2026-10-07-2day.md)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| GEV | US | เทอร์ไบน์ อุปกรณ์ไฟ | ข่าว |
| POWL, MYR, FIX | US | ผู้รับเหมา/อุปกรณ์ไฟ | ข่าว |
| CEG | US | ไฟนิวเคลียร์ เพิ่มกำลังผลิต | ข่าว (2026-10-15) |
| VST | US | ขายไฟให้ data center | ความรู้ทั่วไป |
| NEE | US | ร่วม Brookfield ทำ AI hub $100B | ข่าว (2026-10-15) |
| GULF.BK, GPSC.BK | TH | ผู้ผลิตไฟ (ทางอ้อม) | ความรู้ทั่วไป |
อัปเดต 2026-10-10: ไม่มีข่าวบริษัทใหม่ แต่ราคาแกว่งตามข่าวรายได้ OpenAI (8 ต.ค. CEG -4.85% VST -6.35% แล้ว 9 ต.ค. CEG +4.56% VST +3.42%) GEV นิ่งสุด (ดู analysis/2026-10/2026-10-10-2day.md) หลักฐาน: [ศูนย์ข้อมูลเป็นอสังหา ความเสี่ยงเพิ่ม](https://www.cnbc.com/2026/10/09/ai-data-centers-investing.html) · [AI ร่วงจากข่าวรายได้ OpenAI](https://www.cnbc.com/2026/10/08/open-ai-revenue-nvidia-oracle-coreweave.html)
อัปเดต 2026-10-11 (weekly): ทั้งสัปดาห์ GEV -2.4% POWL -6.2% FIX -5.6% CEG -0.8% VST +0.6% GPSC +4.6% GULF +1.3% ผู้รับเหมาคืนกำไรที่พุ่ง 6 ต.ค. หลักฐานใหม่: [เฟดชี้ data center ดันราคา](https://news.google.com/rss/articles/CBMisAFBVV95cUxOY1FrWkF5TURpdC1qQ3NITm9zVDhQVXJaaXM5aVVYZ0doMEhWaTNid1Q3b1Bfdzg5c01lVGVSOVhjZHhBQTZEUlhHR3diMG96NnBZR25RQWp5U1JuWGJYOHNIT0FJNEd6TVlubGNwQzRGRXA0bUZsTno3YjFmUVpJNVl0NFozV1F4T0Z2QUhkRVdNQW8xR1Nab1NIRWl0VlZaMVRic0F3ak50TzlYSW8wRA?oc=5) · [Google หยุดสร้าง data center ฟินแลนด์](https://www.cnbc.com/2026/10/07/google-finland-data-center-halt.html) · [รัฐหนุน VPP](https://oilprice.com/Energy/Energy-General/States-Bet-on-Virtual-Power-Plants-to-Cut-Grid-Costs.html)
MYR ชื่อย่อจริงคือ MYRG แก้ใน theme_stocks.yaml แล้ว
อัปเดต 2026-10-13: Uranium ETF ตก >20% ใน 12 เดือน แม้เทคซื้อไฟนิวเคลียร์ [OilPrice](https://oilprice.com/Alternative-Energy/Nuclear-Power/3-Stocks-To-Play-The-Nuclear-Energy-Boom.html) · Petra Power เซลล์เชื้อเพลิงให้ data center [TechCrunch](https://techcrunch.com/2026/10/10/petra-power-looks-to-modernize-energy-for-data-centers-and-defense-vehicles/) ราคายังเป็นของ 9 ต.ค. (ดู analysis/2026-10/2026-10-13-2day.md)
อัปเดต 2026-10-15: ไม่มีข่าวบริษัทใหม่ 2 วัน POWL -4.8% FIX -5.2% GEV -0.1% (ดู analysis/2026-10/2026-10-15-2day.md)
อัปเดต 2026-10-18 (weekly): ทั้งสัปดาห์ GEV -8.3% POWL -14.0% FIX -16.1% MYRG -10.1% CEG -9.0% VST -5.9% GULF +2.5% GPSC -0.5% ลงไปกับหุ้น AI ทั้งตลาด หลักฐาน: [Brookfield+NextEra AI hub $100B](https://oilprice.com/Energy/Energy-General/Brookfield-NextEra-to-Build-100-Billion-AI-Hub-on-Cold-War-Nuclear-Site.html) · [Constellation เพิ่มกำลังผลิต](https://www.technologyreview.com/2026/10/15/1146577/nuclear-power-upgrade/) · [สองพรรคต้าน data center](https://www.bbc.co.uk/news/articles/c0rezqpnekro?at_medium=RSS&at_campaign=rss) (ดู analysis/2026-10/2026-10-18-weekly.md)
อัปเดต 2026-10-19: ลงตามหุ้น AI (GEV -0.57% POWL -3.33% FIX -2.85% CEG -1.32% VST -1.39%) ไม่มีข่าวบริษัทใหม่ ดู [Nasdaq ร่วงเพราะน้ำมัน+ขายหุ้น AI](https://www.marketwatch.com/story/nowhere-to-hide-tech-selloff-hits-software-and-chip-stocks-alike-6d96773c) (analysis/2026-10/2026-10-19-2day.md)
อัปเดต 2026-10-21: ลงต่อ FIX -4.57% MYRG -3.56% GEV -1.99% CEG -1.65% VST +0.41% NEE +0.88% หลักฐานใหม่: [ไฟฟ้ายุโรปโตจาก data center](https://oilprice.com/Energy/Natural-Gas/Europes-Power-Demand-Returns-to-Growth.html)
ความเสี่ยงของธีม: ราคาอาจนำข่าวไปแล้ว ยีลด์สูง ผูกกับความเชื่อมั่น AI แรงต้าน data center จากทั้งสองพรรค

## LNG/ก๊าซนอกอ่าวเปอร์เซีย (เริ่มเจอ 2026-10-07 · ล่าสุด 2026-10-17)
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
อัปเดต 2026-10-18 (weekly): ทั้งกลุ่มขึ้นสวนตลาด LNG +4.0% KMI +5.3% PTTEP +5.4% PTT +2.5% หลักฐาน: [ไต้หวันซื้อ LNG อะแลสกา $70-80B](https://oilprice.com/Energy/Natural-Gas/Trump-Announces-80-Billion-Taiwan-LNG-Deal.html) · [LNG ขาดดันถ่านหิน](https://oilprice.com/Energy/Natural-Gas/Global-Coal-Demand-Rises-as-LNG-Shortage-Deepens.html) · [ยุโรปก๊าซสำรองต่ำก่อนหน้าหนาว](https://oilprice.com/Energy/Energy-General/Europe-Braces-for-a-Winter-Energy-Crisis-as-Gas-Reserves-Run-Low.html)
อัปเดต 2026-10-19: LNG +3.68% KMI +4.20% ขึ้นสวนตลาด เรือถูกโจมตีที่ฮอร์มุซ 12 ลำใน 1 สัปดาห์ [BBC](https://www.bbc.co.uk/news/articles/cmde8dpg8g0no?at_medium=RSS&at_campaign=rss)
อัปเดต 2026-10-21: LNG -1.13% KMI +0.54% PTTEP +1.92% ค่าระวางเรือน้ำมันทะลุ $1 ล้าน/วัน [OilPrice](https://oilprice.com/Energy/Energy-General/Petrobras-Deepwater-Push-Sets-Off-a-Race-for-Offshore-Vessels.html) แต่ WTI ลง 5% จากความหวังทางการทูต
ความเสี่ยงของธีม: หยุดยิง/ฮอร์มุซเปิด ราคาก๊าซร่วงเร็ว PTT อาจถูกคุมราคาในประเทศ

## ชิปหน่วยความจำ (เริ่มเจอ 2026-10-08 · ล่าสุด 2026-10-17)
ทำไม: AI ดูดหน่วยความจำ RAM ขาดและแพง ผู้ผลิตกำไรสถิติ
หลักฐานจากข่าว: [Samsung กำไรสถิติ](https://www.cnbc.com/2026/10/08/samsung-q3-earnings.html) · [Intel/AMD กลับไป DDR4 เพราะ RAM แพง](https://www.theverge.com/games/1009140/ram-shortage-intel-amd-ddr4-comeback) · [Micron ร่วงจากข่าว OpenAI](https://www.marketwatch.com/story/micron-nvidia-and-ai-chip-stocks-fall-as-report-on-openais-revenue-causes-undue-concern-2a2bcf53)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| 005930.KS (Samsung) | KR | หน่วยความจำ | ข่าว |
| MU | US | หน่วยความจำ | ข่าว |
| 000660.KS (SK Hynix) | KR | HBM | ความรู้ทั่วไป |
| HANA.BK | TH | ประกอบ/ทดสอบชิป ทางอ้อม | ความรู้ทั่วไป |
อัปเดต 2026-10-15: ร่วงแรง SK Hynix -11.1% Samsung -9.0% Micron -7.4% หลังรายงาน CXMT (จีน) คืบหน้าออกแบบชิป [CNBC](https://www.cnbc.com/2026/10/13/cxmt-memory-chip-stock-rout.html) · [Micron ลงต่อ จีนแข่งแรง](https://www.marketwatch.com/story/microns-stock-extends-declines-as-china-competition-heats-up-b8ec25f0) (ดู analysis/2026-10/2026-10-15-2day.md)
อัปเดต 2026-10-18 (weekly): SK Hynix -24.3% Samsung -17.8% (เทียบ 8 ต.ค.) MU -14.6% HANA -3.8% ยังไม่มีข่าวราคา RAM ลง [รมว.คลังเกาหลี: ชิปแข็งถึงปีหน้า](https://www.cnbc.com/2026/10/17/south-korea-semiconductor-outlook-lee-hyoung-il.html) · [SK Hynix ถูกค้านนำ Solidigm เข้า Nasdaq](https://news.google.com/rss/articles/CBMijgFBVV95cUxNc1lkMl9lTkxyUmhKRElVZGQtMy1PQ19PeGEtU1NHSzVuQWp3NUpES3RTNF9rSTNIeURkS2JRb3Q5NUQ0RE5oMW9) สถานะ: ธีมเสี่ยงสูง ยังไม่ตัด จบถ้าราคา RAM สัญญาเริ่มลง
อัปเดต 2026-10-19: MU -5.63% SMH -3.41% ยังไม่มีข่าวราคา RAM ลง [MarketWatch](https://www.marketwatch.com/story/nowhere-to-hide-tech-selloff-hits-software-and-chip-stocks-alike-6d96773c)
อัปเดต 2026-10-21: SK Hynix -4.23% Samsung -2.98% MU -0.98% ยังไม่มีข่าวราคา RAM ลง
ความเสี่ยงของธีม: วัฏจักรหน่วยความจำกลับลงเร็ว ผูกกับข่าวรายได้ AI จีนเริ่มตามทัน

## โรงกลั่น/ดีเซลขาด (เริ่มเจอ 2026-10-14 · ล่าสุด 2026-10-17)
ทำไม: ดีเซลตึงถึง 2027 ส่วนต่างราคาดีเซลกับน้ำมันดิบกว้าง รัฐเร่งกำลังกลั่น
หลักฐานจากข่าว: [IEA ดีเซลตึงถึง 2027](https://www.cnbc.com/2026/10/14/diesel-deal-oil-price-iea-report.html) · [รัฐใช้กฎหมายยุคสงครามเกาหลีเร่งโรงกลั่น Delek](https://oilprice.com/Energy/Crude-Oil/White-House-Turns-to-Korean-War-Era-Law-as-Diesel-Prices-Stay-Above-6.html) · [Rubio เยือนโรงกลั่น Reliance](https://www.cnbc.com/2026/10/16/marco-rubio-reliance-jamnagar-refinery.html)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| DK | US | โรงกลั่นที่รัฐเร่ง | ข่าว |
| VLO, MPC | US | โรงกลั่นใหญ่ | ความรู้ทั่วไป |
| TOP.BK | TH | โรงกลั่นไทย | ความรู้ทั่วไป |
อัปเดต 2026-10-19: สหรัฐปล่อย SPR อีก 17 ล้านบาร์เรล [OilPrice](https://oilprice.com/Latest-Energy-News/World-News/US-Offers-Another-17-Million-SPR-Barrels-as-Fuel-Crisis-Deepens.html) · ยกเลิกคว่ำบาตรรัสเซียส่วนใหญ่ อาจกดส่วนต่างกลั่นระยะกลาง
อัปเดต 2026-10-21: DK +3.40% VLO +0.03% MPC +0.28% TOP -1.06% น้ำมันดิบลงช่วยต้นทุนโรงกลั่น
ความเสี่ยงของธีม: รัฐห้ามส่งออก/คุมราคา (โดยเฉพาะไทย) ฮอร์มุซเปิด ส่วนต่างหดเร็ว

## ความปลอดภัยไซเบอร์ยุค AI agent (เริ่มเจอ 2026-10-12 · ล่าสุด 2026-10-17)
ทำไม: AI หาช่องโหว่ได้เร็ว agent ถูกใช้เจาะระบบ องค์กรต้องจ่ายเพิ่มเพื่ออุด
หลักฐานจากข่าว: [BofA จ้าง 1,000 คนแก้ช่องโหว่ที่ Mythos เจอ](https://www.cnbc.com/2026/10/14/anthropic-mythos-bank-of-america-hiring-cost.html) · [IonQ ซื้อ Elisity $1.3B](https://www.cnbc.com/2026/10/12/ionq-elisity-acquisition-cybersecurity.html) · [โมเดล OpenAI เจาะกระเป๋าคริปโต](https://arstechnica.com/security/2026/10/openai-models-hacked-a-crypto-wallet-and-breached-more-websites/) · [AI agent นอกลู่ในอินเดีย](https://techcrunch.com/2026/10/16/india-becomes-the-latest-country-to-report-rogue-ai-agent-activity/)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| IONQ | US | ซื้อบริษัทไซเบอร์ (ผันผวนสูง) | ข่าว |
| CRWD, PANW | US | ผู้นำความปลอดภัย | ความรู้ทั่วไป |
| BE8.BK | TH | บริการไอที/ไซเบอร์ ทางอ้อม | ความรู้ทั่วไป |
ความเสี่ยงของธีม: ถูกเทขายไปกับหุ้นซอฟต์แวร์ มูลค่าแพง

## ธีมที่จบแล้ว

(ยังไม่มี)
