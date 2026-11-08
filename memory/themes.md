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

## ไฟฟ้าจาก AI: ไฟฟ้า นิวเคลียร์ ระบบไฟ (เริ่มเจอ 2026-10-06 · ล่าสุด 2026-11-08)
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
อัปเดต 2026-10-23: เด้งสวนตลาดวันที่ Nasdaq -2.6% GEV +4.00% CEG +4.60% VST +3.87% POWL +3.26% FIX +0.30% ไม่มีข่าวบริษัทใหม่ แรงกดดันเงินทุนผู้สร้าง data center: [Meta FCF ติดลบ](https://www.cnbc.com/2026/10/22/meta-stock-q3-earnings-free-cash-flow.html) (analysis/2026-10/2026-10-23-2day.md)
อัปเดต 2026-10-25: แก้ตัวเลขรอบก่อน (+4% เป็นของวันที่ 21) วันที่ 22–23 ร่วงหนัก GEV -12.0% FIX -17.2% CEG -6.4% POWL ทรงตัว เหตุ: ความกังวลเครดิต/เงินทุน AI [CNBC](https://www.cnbc.com/2026/10/23/ai-turmoil-neoclouds-struggle-credit-risks-jump-solidigm-pulls-ipo.html) · [Nvidia ในฐานะผู้ให้เงิน AI](https://www.cnbc.com/2026/10/24/nvidias-role-as-ai-financier-faces-first-big-test-as-neoclouds-take-market-hit.html) (analysis/2026-10/2026-10-25-2day.md)
อัปเดต 2026-10-25 (weekly): ทั้งสัปดาห์ FIX -19.3% GEV -11.5% MYRG -9.2% POWL -8.6% VST -7.8% CEG -6.6% NEE +2.9% GULF -0.4% GPSC +1.0% เหตุ: เครดิต/เงินทุน AI ไม่ใช่ข่าวบริษัท หลักฐานใหม่: [Microsoft ถอนจาก data center ใหญ่สุดอังกฤษ](https://www.bbc.co.uk/news/articles/c9m26kl5y7epo?at_medium=RSS&at_campaign=rss) · [โรงนิวเคลียร์ขอเพิ่มกำลังผลิต](https://oilprice.com/Alternative-Energy/Nuclear-Power/The-Nuclear-Power-Shortcut-That-Could-Add-Gigawatts-to-the-US-Grid.html) · [TikTok หาไฟหลายกิกะวัตต์](https://www.cnbc.com/2026/10/23/tiktok-us-compute-capacity.html) · [ทรัมป์ไล่ยกเลิกโครงการลม $6.2B](https://oilprice.com/Alternative-Energy/Wind-Power/Trump-Targets-62-Billion-Offshore-Wind-Project-Nearing-Completion.html) น่าศึกษาก่อนเปลี่ยนเป็น NEE (analysis/2026-10/2026-10-25-weekly.md)
อัปเดต 2026-10-27: ราคาธีมสหรัฐในไฟล์ยังเป็นของ 23 ต.ค. (ไม่อัปเดต) Anthropic ยื่น IPO เปิดว่า data center พึ่งก๊าซมากขึ้น [The Verge](https://www.theverge.com/ai-artificial-intelligence/1018994/anthropic-ipo-ai-data-center-energy-climate-risk) · GPSC +0.98%
อัปเดต 2026-11-01: ร่วงตามเทค 28→30 ต.ค. FIX -8.4% POWL -7.0% GEV -2.3% VST -3.0% CEG +1.7% เหตุ: [Intel พัง กังวลงบ AI](https://www.cnbc.com/2026/10/30/amazon-intel-earnings-big-tech-ai-spending-concerns.html) · [S&P ลบมุมมอง Meta](https://www.cnbc.com/2026/10/30/meta-outlook-to-revised-to-negative-by-sp-after-cash-flow-negative.html) ดู analysis/2026-11/2026-11-01-2day.md
อัปเดต 2026-11-01 (weekly): ทั้งสัปดาห์ MYRG +11.1% FIX +6.2% GEV +5.3% CEG +3.5% POWL +3.5% NEE +2.0% VST -1.3% GULF -1.2% GPSC -3.4% เด้งแรงต้นสัปดาห์ (FIX ถึง 1,346) แล้วคืนวันศุกร์ หลักฐานใหม่: [GEV ซื้อ Trench อุปกรณ์ไฟแรงสูง](https://oilprice.com/Latest-Energy-News/World-News/GE-Vernova-Expands-in-High-Voltage-Grid-Gear-With-Trench-Deal.html) · ความเสี่ยงใหม่: [Arizona สองพรรคต้าน data center](https://www.techmeme.com/261031/p7)
อัปเดต 2026-11-05: เด้ง 4 พ.ย. GEV +6.5% FIX +7.1% POWL +6.1% MYRG +4.8% VST +3.7% CEG +2.4% NEE -0.8% ความเสี่ยงใหม่: ผู้ลงคะแนนปฏิเสธข้อเสนอ data center เกือบทั้งหมด [CNBC](https://www.cnbc.com/2026/11/04/data-center-ballot-measures-2026-midterm.html) · [Texas อาจไม่ใช่ศูนย์กลางอีก](https://www.technologyreview.com/2026/11/04/1148043/texas-was-the-new-epicenter-of-the-ai-data-center-buildout-that-might-be-kaput/) ฝั่งอุปสงค์ยังแรง [AMD](https://www.theverge.com/tech/1026148/amd-earnings-q3-2026-data-center-pc)
ความเสี่ยงของธีม: ราคาอาจนำข่าวไปแล้ว ยีลด์สูง ผูกกับความเชื่อมั่น AI แรงต้าน data center จากทั้งสองพรรค
อัปเดต 2026-11-03: 2 วันที่ผ่านมา CEG -0.8%/-2.0% VST -1.8%/-2.7% FIX -7.1%/-2.6% GEV -3.4%/+0.5% หลักฐานใหม่: OpenAI Grid Protectors ลดไฟ 1,000 MW ยามไฟตึง [Techmeme](https://www.techmeme.com/261102/p34) · Oracle ขอระดมทุน $20B [CNBC](https://www.cnbc.com/2026/11/02/oracle-files-to-sell-20-billion-in-new-stock-bonds-to-finance-ai-buildout.html)
อัปเดต 2026-11-08 (weekly): ทั้งสัปดาห์ FIX -17.5% POWL -14.8% VST -9.8% GEV -9.8% MYRG -7.0% CEG -4.7% แต่ NEE +3.9% GPSC +7.1% GULF +0.4% ผู้รับเหมาโครงการใหม่โดนหนักหลัง [ballot ต้าน data center](https://www.cnbc.com/2026/11/04/data-center-ballot-measures-2026-midterm.html) · NEE ได้จาก [เดโมแครตหนุนพลังงานหมุนเวียน](https://www.cnbc.com/2026/11/07/midterm-election-blue-wave-trump-renewable-energy.html) · ความเสี่ยงไทย: [ไทยชะลออนุมัติ data center 117 โครงการ](https://www.techmeme.com/261107/p15) · [นิวเคลียร์ติดปัญหาเชื้อเพลิง](https://oilprice.com/Alternative-Energy/Nuclear-Power/Americas-Nuclear-Revival-Is-Running-Into-a-Fuel-Supply-Wall.html) (analysis/2026-11/2026-11-08-weekly.md)

## LNG/ก๊าซนอกอ่าวเปอร์เซีย (เริ่มเจอ 2026-10-07 · ล่าสุด 2026-11-08)
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
อัปเดต 2026-10-23: Brent 113.23 สูงสุดตั้งแต่ พ.ค. LNG +0.31% KMI +1.19% PTTEP +3.16% PTT +1.84% หลักฐาน: [Brent เกิน $113](https://www.cnbc.com/2026/10/22/oil-prices-today-wti-brent-saudi-arabia.html)
อัปเดต 2026-10-25: Brent 116.72 LNG(Cheniere) +4.06% KMI +2.11% PTTEP +3.16% PTT +1.84% [กาตาร์ซื้อก๊าซสหรัฐ](https://www.cnbc.com/2026/10/23/cheniere-qatar-energy-lng-natural-gas-iran-war-strait-hormuz.html)
อัปเดต 2026-10-25 (weekly): ทั้งสัปดาห์ PTTEP +5.2% LNG +3.2% PTT +1.2% KMI +0.7% Brent +6.2% แต่มีพาดหัวว่าน้ำมันออกจากอ่าวมากกว่าก่อนสงคราม [WSJ](https://news.google.com/rss/articles/CBMiugFBVV95cUxOQ25MSXRodmt6X1ZwZFZ1b01nR01ZTE1PWDU0SGVaWTRKMXJLdl9FbXVHSnZTMGxiV1pMbGtOZTVUMjZER01kVHQ1TmtIczlGZ3Z3X2djQng0b0RrOEQtZkk4REEtYTE2U1JxVlpLMzAtUnNycVhiQXVqV3BET09SZDZLbWtfZGp3NFl6eDZPakRzeDk4N3VydmJucDB6SlgwNmNNWVlrVTVRdGQ2RTVVOUpqTXBJa3RWaXc?oc=5) = ความเสี่ยงราคาลงเร็วถ้าการโจมตีไม่เกิด
อัปเดต 2026-10-27: Brent ลง 109.88 (-5.86%) ข่าวเจรจาซาอุฯ–อิหร่าน [CNBC](https://www.cnbc.com/2026/10/26/oil-prices-today-wti-brent.html) · สงครามเพิ่มบิล LNG โลก $39B [OilPrice](https://oilprice.com/Energy/Natural-Gas/The-Iran-War-Just-Added-39-Billion-to-the-Worlds-LNG-Bill.html) · PTTEP -0.61% PTT +0.60%
อัปเดต 2026-11-01: LNG (Cheniere) +10.9% ใน 2 วัน (28→30 ต.ค.) หลักฐานใหม่: [แก๊สยุโรป >€101](https://oilprice.com/Latest-Energy-News/World-News/European-Gas-Tops-101-Euros-for-First-Time-Since-2022.html) · [ญี่ปุ่นแซงจีนนำเข้า LNG](https://oilprice.com/Latest-Energy-News/World-News/Japan-to-Overtake-China-As-Worlds-Top-LNG-Importer-This-Year.html)
อัปเดต 2026-11-01 (weekly): ทั้งสัปดาห์ LNG +10.6% PTTEP +1.2% PTT +1.2% KMI -1.6% Brent +0.8% (แกว่ง 109.9–117.6) แรงสุดของธีมทั้งหมด หลักฐาน: [แก๊สยุโรป >€101](https://oilprice.com/Latest-Energy-News/World-News/European-Gas-Tops-101-Euros-for-First-Time-Since-2022.html) · [ก๊าซสหรัฐผลิตสถิติ](https://oilprice.com/Energy/Natural-Gas/US-Natural-Gas-Production-Hits-New-Records-as-Demand-Surges.html)
ความเสี่ยงของธีม: หยุดยิง/ฮอร์มุซเปิด ราคาก๊าซร่วงเร็ว PTT อาจถูกคุมราคาในประเทศ
อัปเดต 2026-11-03: Brent -15.5% ใน 2 วันจากความหวังเจรจาอิหร่าน LNG -2.3% PTTEP -3.4% [CNBC](https://www.cnbc.com/2026/11/02/oil-prices-fall-as-iran-us-pursue-diplomacy.html)

อัปเดต 2026-11-05: Brent 93.96 (-9.3%) แต่หลักฐานฝั่งก๊าซยังแรง [แอฟริกา LNG +175%](https://oilprice.com/Energy/Natural-Gas/Africas-LNG-Exports-Set-to-Soar-175-as-Buyers-Flee-Hormuz.html) · [กาตาร์ซื้อ LNG สหรัฐมากสุด](https://oilprice.com/Energy/Natural-Gas/Qatar-Becomes-Largest-Buyer-of-US-LNG-Amid-Hormuz-Crisis.html) LNG -0.16% KMI +0.49% PTTEP -1.96% PTT -1.23%
อัปเดต 2026-11-08 (weekly): กลับทิศแรง LNG -15.9% PTTEP -13.6% KMI -11.5% PTT -8.9% Brent -13.3% (113.43→98.32) ตามความหวังสันติภาพหลังเลือกตั้ง [CNBC](https://www.cnbc.com/2026/11/04/oil-price-iran-war-us-election-strait-hormuz.html) · [แก๊สยุโรปลง](https://oilprice.com/Latest-Energy-News/World-News/European-Gas-Prices-Drop-on-Iran-Deal-Hopes-after-US-Midterms.html) พื้นฐานก๊าซยังตึง · 7 พ.ย. [สหรัฐโจมตีอิหร่านเล็กน้อย](https://www.cnbc.com/2026/11/07/trump-us-minor-strikes-iran-qeshm-island.html) ถ้าข่าวสงบอีก 2 สัปดาห์ พิจารณาย้ายลงธีมจบ

## ชิปหน่วยความจำ (เริ่มเจอ 2026-10-08 · ล่าสุด 2026-11-08)
ทำไม: AI ดูดหน่วยความจำ RAM ขาดและแพง ผู้ผลิตกำไรสถิติ
หลักฐานจากข่าว: [Samsung กำไรสถิติ](https://www.cnbc.com/2026/10/08/samsung-q3-earnings.html) · [Intel/AMD กลับไป DDR4 เพราะ RAM แพง](https://www.theverge.com/games/1009140/ram-shortage-intel-amd-ddr4-comeback) · [Micron ร่วงจากข่าว OpenAI](https://www.marketwatch.com/story/micron-nvidia-and-ai-chip-stocks-fall-as-report-on-openais-revenue-causes-undue-concern-2a2bcf53)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| 005930.KS (Samsung) | KR | หน่วยความจำ | ข่าว |
| MU | US | หน่วยความจำ | ข่าว |
| 000660.KS (SK Hynix) | KR | HBM | ความรู้ทั่วไป |
| HANA.BK | TH | ประกอบ/ทดสอบชิป ทางอ้อม | ความรู้ทั่วไป |
| SNDK | US | NAND/SSD รายได้เกือบ 5 เท่า | ข่าว (2026-10-30) |
อัปเดต 2026-10-15: ร่วงแรง SK Hynix -11.1% Samsung -9.0% Micron -7.4% หลังรายงาน CXMT (จีน) คืบหน้าออกแบบชิป [CNBC](https://www.cnbc.com/2026/10/13/cxmt-memory-chip-stock-rout.html) · [Micron ลงต่อ จีนแข่งแรง](https://www.marketwatch.com/story/microns-stock-extends-declines-as-china-competition-heats-up-b8ec25f0) (ดู analysis/2026-10/2026-10-15-2day.md)
อัปเดต 2026-10-18 (weekly): SK Hynix -24.3% Samsung -17.8% (เทียบ 8 ต.ค.) MU -14.6% HANA -3.8% ยังไม่มีข่าวราคา RAM ลง [รมว.คลังเกาหลี: ชิปแข็งถึงปีหน้า](https://www.cnbc.com/2026/10/17/south-korea-semiconductor-outlook-lee-hyoung-il.html) · [SK Hynix ถูกค้านนำ Solidigm เข้า Nasdaq](https://news.google.com/rss/articles/CBMijgFBVV95cUxNc1lkMl9lTkxyUmhKRElVZGQtMy1PQ19PeGEtU1NHSzVuQWp3NUpES3RTNF9rSTNIeURkS2JRb3Q5NUQ0RE5oMW9) สถานะ: ธีมเสี่ยงสูง ยังไม่ตัด จบถ้าราคา RAM สัญญาเริ่มลง
อัปเดต 2026-10-19: MU -5.63% SMH -3.41% ยังไม่มีข่าวราคา RAM ลง [MarketWatch](https://www.marketwatch.com/story/nowhere-to-hide-tech-selloff-hits-software-and-chip-stocks-alike-6d96773c)
อัปเดต 2026-10-21: SK Hynix -4.23% Samsung -2.98% MU -0.98% ยังไม่มีข่าวราคา RAM ลง
อัปเดต 2026-10-23: SK Hynix -5.49% Samsung -4.03% MU +1.96% ข่าวใหม่: [PC ส่งมอบลด >20% เพราะ RAM แพง](https://www.theverge.com/gadgets/1017144/global-pc-shipments-dropped-q3-2026-ram) เป็นสัญญาณอุปสงค์ปลายทางอ่อน
อัปเดต 2026-10-25: SK Hynix +4.42% Samsung +0.47% MU +2.46% เด้งสั้น ยังไม่มีข่าวราคา RAM ลง
อัปเดต 2026-10-25 (weekly): ทั้งสัปดาห์ทรงตัว MU -0.2% SK Hynix +0.4% Samsung 0% HANA -3.5% สัญญาณใหม่: อุปสงค์ปลายทางอ่อน [PC -20%](https://www.theverge.com/gadgets/1017144/global-pc-shipments-dropped-q3-2026-ram) ยังไม่มีข่าวราคา RAM ลง ยังไม่ตัด
อัปเดต 2026-10-27: เด้งตามหุ้น AI หลัง Anthropic ยื่น IPO SK Hynix +6.90% Samsung +4.58% Micron +2.46% Hana -2.06% KOSPI +3.46% [ข่าว](https://news.google.com/rss/articles/CBMijgFBVV95cUxNSlZDNHhSYkVHOW9iNENjRlUycDhVZXVrc29jSFBNY18wZFhSS2VNYi1lcHhpM1M5dUtMYlU3Nmg1cmdVMEt2ZmdlRlZYR1hlOFpjLXE5RXRyN1JXUlkxR1d2THVDQVFJdTZPdzBkZzZzaFZrYk1FbVBZeHRsa2IxZUl6Q0dKRlZFR0pTSERB?oc=5)
อัปเดต 2026-11-01: MU -10.0% SMH -7.96% (28→30 ต.ค.) ตามกลุ่มชิปหลัง [Intel/AMD](https://www.marketwatch.com/story/amds-stock-slides-after-intel-earnings-reveal-two-big-issues-d3afed91) ไม่มีข่าวหน่วยความจำเฉพาะ
อัปเดต 2026-11-01 (weekly): ทั้งสัปดาห์ SK Hynix +11.0% Samsung +4.4% MU +0.8% HANA -6.7% (MU พุ่งถึง 983 วันพุธแล้วกลับ) หลักฐาน: [SK Hynix กำไรเกินคาดมาก](https://www.cnbc.com/2026/10/28/sk-hynix-third-quarter-profit.html) · [Sandisk รายได้เกือบ 5 เท่า](https://www.marketwatch.com/story/sandisk-sees-revenue-nearly-quintuple-and-its-stock-is-heading-higher-b9318916) · [Intel ขาด RAM ขายชิปราคาถูกหมด](https://www.theverge.com/tech/1022911/intel-wildcat-lake-sold-out-ram-shortage) เพิ่ม SNDK (ข่าว)
ความเสี่ยงของธีม: วัฏจักรหน่วยความจำกลับลงเร็ว ผูกกับข่าวรายได้ AI จีนเริ่มตามทัน
อัปเดต 2026-11-03: 2 วัน MU -10.8% SNDK -19.1% SK Hynix -4.1% SMH -9.5% Apple ถูกกดจากหน่วยความจำขาด [MarketWatch](https://www.marketwatch.com/story/apples-iphone-business-is-booming-heres-why-the-stock-is-falling-anyway-07de9fff)
อัปเดต 2026-11-08 (weekly): แย่สุดของทุกธีม SNDK -27.4% MU -22.0% SK Hynix -20.2% HANA -17.1% Samsung -16.1% สัญญาณวัฏจักรกลับ: [Qualcomm โดน RAM แพงกดยอดมือถือ](https://www.cnbc.com/2026/11/04/qualcomm-qcom-earnings-report-q4-2026.html) · [TSMC พิจารณาผลิต 3D DRAM](https://www.techmeme.com/261106/p13) · ยังไม่มีข่าวราคา RAM ลดจริง

## โรงกลั่น/ดีเซลขาด (เริ่มเจอ 2026-10-14 · ล่าสุด 2026-11-08)
ทำไม: ดีเซลตึงถึง 2027 ส่วนต่างราคาดีเซลกับน้ำมันดิบกว้าง รัฐเร่งกำลังกลั่น
หลักฐานจากข่าว: [IEA ดีเซลตึงถึง 2027](https://www.cnbc.com/2026/10/14/diesel-deal-oil-price-iea-report.html) · [รัฐใช้กฎหมายยุคสงครามเกาหลีเร่งโรงกลั่น Delek](https://oilprice.com/Energy/Crude-Oil/White-House-Turns-to-Korean-War-Era-Law-as-Diesel-Prices-Stay-Above-6.html) · [Rubio เยือนโรงกลั่น Reliance](https://www.cnbc.com/2026/10/16/marco-rubio-reliance-jamnagar-refinery.html)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| DK | US | โรงกลั่นที่รัฐเร่ง | ข่าว |
| VLO, MPC | US | โรงกลั่นใหญ่ | ความรู้ทั่วไป |
| TOP.BK | TH | โรงกลั่นไทย | ความรู้ทั่วไป |
| XOM, CVX | US | กำไรโรงกลั่นพุ่ง ราคาหุ้นทำสถิติ | ข่าว (2026-10-30) |
อัปเดต 2026-10-19: สหรัฐปล่อย SPR อีก 17 ล้านบาร์เรล [OilPrice](https://oilprice.com/Latest-Energy-News/World-News/US-Offers-Another-17-Million-SPR-Barrels-as-Fuel-Crisis-Deepens.html) · ยกเลิกคว่ำบาตรรัสเซียส่วนใหญ่ อาจกดส่วนต่างกลั่นระยะกลาง
อัปเดต 2026-10-21: DK +3.40% VLO +0.03% MPC +0.28% TOP -1.06% น้ำมันดิบลงช่วยต้นทุนโรงกลั่น
อัปเดต 2026-10-23: DK +0.76% VLO +0.77% MPC -1.49% TOP +1.82% น้ำมันดิบกลับขึ้นอีก ดู [Brent เกิน $113](https://www.cnbc.com/2026/10/22/oil-prices-today-wti-brent-saudi-arabia.html)
อัปเดต 2026-10-25: DK -1.82% VLO -1.64% MPC -0.45% TOP +1.82% ยังไม่มีข่าวดีเซลใหม่ มีข้อยกเว้นขายดีเซลรัสเซีย 6 เดือน [OilPrice](https://oilprice.com/Energy/Energy-General/Trumps-Reverse-Nixon-Strategy-Bring-Russia-In-Shut-China-Out.html)
อัปเดต 2026-10-25 (weekly): ทั้งสัปดาห์ลง VLO -5.7% MPC -4.4% TOP -4.1% DK -2.9% แม้ดีเซลตึง [โดรนยูเครนตีโรงกลั่นรัสเซีย](https://www.cnbc.com/2026/10/21/ukraine-russia-drone-diesel-refinery-trump-putin-zelenskyy.html) · แรงกดดัน: ข้อยกเว้นดีเซลรัสเซีย + [ภาษีลาภลอย](https://oilprice.com/Energy/Energy-General/Big-Oil-Eyes-Record-Profits-but-Keeps-Spending-in-Check.html) มุมมองสัปดาห์ก่อน "โรงกลั่นได้ตรง" ผิดในสัปดาห์นี้
อัปเดต 2026-11-01: VLO +2.9% MPC +0.9% (28→30 ต.ค.) หลักฐานใหม่: [Exxon กำไร $15.4B](https://oilprice.com/Latest-Energy-News/World-News/ExxonMobil-Profits-Double-to-154-Billion.html) · [Chevron กำไรเกือบ 3 เท่า](https://oilprice.com/Latest-Energy-News/World-News/Chevron-Profits-Nearly-Triple-to-99-Billion.html) · [ยุโรปทบทวนการลดโรงกลั่น](https://oilprice.com/Energy/Crude-Oil/Europe-Is-Now-Seriously-Rethinking-Its-Oil-Refinery-Phase-Down.html) เพิ่ม XOM, CVX (ที่มา: ข่าว)
อัปเดต 2026-11-01 (weekly): โรงกลั่นล้วนลงต่อ TOP -10.8% VLO -4.7% MPC -2.7% DK -1.1% ขณะ [Chevron/Exxon ทำสถิติ](https://www.cnbc.com/2026/10/30/chevron-exxon-cvx-xom-earnings-q3-2026.html) · แรงกดดัน: [สหรัฐอาจปล่อยดีเซลรัสเซียเพิ่ม](https://www.cnbc.com/2026/10/27/trump-putin-zelenskyy-russia-ukraine-diesel.html) · [โรงกลั่นรัสเซียกลับมา +25%](https://news.google.com/rss/articles/CBMidkFVX3lxTE5TTGZmTjFVMEo0UW9Hckc2ajU4Y3M0R1ZpSEhlcWZrUV85SlBiMkNoU0w4c0Z3T0poek5fUGFiRU10WmotMkpaYWxNbTIzX2xfaXlPQnM3U2VMeTJSaURFbkxUWThYajFDNUQ5Z19kOThGT3p5UWc?oc=5) ไม่พบสาเหตุ TOP ร่วงในข่าว มุมมอง: ตลาดแยกบริษัทใหญ่ (บ่อ+โรงกลั่น) ออกจากโรงกลั่นล้วน
ความเสี่ยงของธีม: รัฐห้ามส่งออก/คุมราคา (โดยเฉพาะไทย) ฮอร์มุซเปิด ส่วนต่างหดเร็ว
อัปเดต 2026-11-03: 2 พ.ย. โรงกลั่น/ปิโตรเลียมลง 3-5% ตามน้ำมัน (VLO -4.6% XOM -4.1%) หลังเจรจา [OilPrice](https://oilprice.com/Latest-Energy-News/World-News/Oil-Prices-Plunge-7-as-US-and-Iran-Signal-Room-for-Diplomacy.html)
อัปเดต 2026-11-08 (weekly): ลงทั้งกลุ่มตามน้ำมัน MPC -16.2% VLO -13.3% DK -13.1% XOM -11.4% TOP -10.4% CVX -9.7% แม้ [ดีเซลจีนส่งออกดิ่ง](https://oilprice.com/Latest-Energy-News/World-News/Chinas-Diesel-Exports-Set-to-Plunge-as-Domestic-Inventories-Run-Low.html) · [ConocoPhillips กำไรเท่าตัว](https://oilprice.com/Latest-Energy-News/World-News/ConocoPhillips-Doubles-Profit-to-4-Billion-Raises-Dividend.html) · ความเสี่ยงใหม่: [เดโมแครตสอบดีลพลังงาน](https://www.cnbc.com/2026/11/05/trump-election-energy-venezuela-critical-mineral-renewable-iran.html)

## ความปลอดภัยไซเบอร์ยุค AI agent (เริ่มเจอ 2026-10-12 · ล่าสุด 2026-11-08)
ทำไม: AI หาช่องโหว่ได้เร็ว agent ถูกใช้เจาะระบบ องค์กรต้องจ่ายเพิ่มเพื่ออุด
หลักฐานจากข่าว: [BofA จ้าง 1,000 คนแก้ช่องโหว่ที่ Mythos เจอ](https://www.cnbc.com/2026/10/14/anthropic-mythos-bank-of-america-hiring-cost.html) · [IonQ ซื้อ Elisity $1.3B](https://www.cnbc.com/2026/10/12/ionq-elisity-acquisition-cybersecurity.html) · [โมเดล OpenAI เจาะกระเป๋าคริปโต](https://arstechnica.com/security/2026/10/openai-models-hacked-a-crypto-wallet-and-breached-more-websites/) · [AI agent นอกลู่ในอินเดีย](https://techcrunch.com/2026/10/16/india-becomes-the-latest-country-to-report-rogue-ai-agent-activity/)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| IONQ | US | ซื้อบริษัทไซเบอร์ (ผันผวนสูง) | ข่าว |
| CRWD, PANW | US | ผู้นำความปลอดภัย | ความรู้ทั่วไป |
| BE8.BK | TH | บริการไอที/ไซเบอร์ ทางอ้อม | ความรู้ทั่วไป |
อัปเดต 2026-10-25: CRWD +8.25% PANW +7.22% IONQ +0.35% (23 ต.ค.) ไม่พบสาเหตุในข่าว ข่าวเกี่ยวข้อง: [AI พบช่องโหว่ PHP ทั้งโลกต้องรีบอุด](https://www.bbc.co.uk/news/articles/c3qjnwye0ep5o?at_medium=RSS&at_campaign=rss)
อัปเดต 2026-10-25 (weekly): ทั้งสัปดาห์ CRWD +13.3% PANW +11.3% IONQ 0% BE8 -4.1% หลักฐาน: [AI เจอช่องโหว่ PHP](https://www.bbc.co.uk/news/articles/c3qjnwye0ep5o?at_medium=RSS&at_campaign=rss) · [FBI เตือน 70% ของเว็บ](https://news.google.com/rss/articles/CBMiVkFVX3lxTE5TSXJJNXZRcTdlbnlOOHFWTFIwV01hUlV2MjhieF82dmIwUzMtZ1BOOHBNZ0tRUEVCa0FvQTAxTGFrRndXekVqa1RMVkZpNnM1SlJ3anRB?oc=5) · [Microsoft: การโจมตีด้วย AI agent เชื่อมรัฐจีน](https://news.google.com/rss/articles/CBMiqwFBVV95cUxNRUxxWV9qVGlNR1BIcm1obUxtakoxb2dpTkl5R0FJU1VvakNmYU14MG43bVZMS1Rxa0l4RXNnbTlFMWxadUloOXNBVl9Mczk3UTZXSjlxdjZEVXN0UDhzMkp1UFAzSmZ6X1JuYzdGbzRWM3kyX21mRG5FMHBjcVEySGQ3ZFk3a2k0UmpQRG5fVzF1NWRtdG5BeTl4NVVLTzdYX0pGekdEWHdEcVU?oc=5)
อัปเดต 2026-11-01: CRWD -6.1% PANW -7.3% (28→30 ต.ค.) ลงตามเทค แม้ข่าวเสี่ยงเพิ่ม: [ส่วนขยาย Claude Code บน Cursor โดน backdoor](https://arstechnica.com/security/2026/10/anthropic-vs-code-extension-on-cursor-backdoored-for-nearly-12-hours/) · [Northflank โดนเจาะ](https://www.bleepingcomputer.com/news/security/northflank-security-breach-leads-to-abuse-of-customers-ai-api-keys/) · [Binance แฮก $6.3B](https://www.bbc.co.uk/news/articles/cwe8lp7zy07zo?at_medium=RSS&at_campaign=rss)
อัปเดต 2026-11-01 (weekly): ทั้งสัปดาห์ CRWD -2.8% PANW -3.9% IONQ -3.9% BE8 -8.1% ลงแม้ข่าวเจาะหนักสุด: [Binance $6.3B](https://www.bbc.co.uk/news/articles/cwe8lp7zy07zo?at_medium=RSS&at_campaign=rss) · [Chainalysis โดน agent เจาะ](https://www.bleepingcomputer.com/news/security/chainalysis-discloses-data-breach-from-offensive-agentic-techniques/) · [Fortinet ร่วงหลังงบ](https://www.marketwatch.com/story/fortinets-stock-is-taking-a-dive-after-earnings-heres-why-d407896e)
ความเสี่ยงของธีม: ถูกเทขายไปกับหุ้นซอฟต์แวร์ มูลค่าแพง
อัปเดต 2026-11-03: ตู้แช่ซูเปอร์มาร์เก็ต 7 ประเทศยุโรปถูกโจมตี [BBC](https://www.bbc.co.uk/news/articles/cq1kd1nee80eo?at_medium=RSS&at_campaign=rss) · Google ปราบบอตเน็ต XCPE [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-disrupts-million-device-xcpe-android-malware-botnet-bans-tv-box-maker/) · CRWD -3.4% PANW -3.9% (2 พ.ย.)
อัปเดต 2026-11-08 (weekly): CRWD -13.4% PANW -14.2% IONQ +8.6% BE8 +1.4% ข่าวเจาะหนักขึ้น: [AI agent หลุด sandbox เจาะ WorkOS](https://www.bleepingcomputer.com/news/security/runaway-ai-hacking-agent-behind-workos-breach-after-escaping-sandbox/) · [FBI/CISA เตือนระบบทำความเย็น](https://www.bleepingcomputer.com/news/security/fbi-cisa-warn-of-cyberattacks-targeting-refrigeration-systems/) · [ธนาคารฝรั่งเศส $133M](https://www.bleepingcomputer.com/news/security/hackers-pull-off-133-million-french-bank-heist-via-service-provider/) ความเสี่ยงใหม่ของหุ้น: เจ้าของโมเดลทำ AI หาช่องโหว่เอง [GPT-6 Cyber](https://www.bleepingcomputer.com/news/security/openais-new-gpt-6-cyber-ai-finds-81-firefox-flaws-948-linux-bugs/)

## สุขภาพ: ยาที่มีผลทดลองเด่น (เริ่มเจอ 2026-10-25 · ล่าสุด 2026-11-08)
ทำไม: เงินหมุนออกจาก AI เข้าหุ้นสุขภาพ (XLV สถิติ) ยาใหญ่มีผลทดลองระยะท้ายดีหลายตัวในสัปดาห์เดียว
หลักฐานจากข่าว: [หุ้นสุขภาพทำสถิติ](https://news.google.com/rss/articles/CBMi0wFBVV95cUxNOERPV24tN3hRdl9Ca1NtZHlzcndtUlp3TW1wSnc0emxOdy1nd1lDNXBtNTdBYmg1Qm0wVE9ERU01WkdGVUFOSzN4d3JJMkpKbGFjaFFvNnZwaV82akIwX0VIVHJ1NUJZQUlGSWMxemFQX2h3Y0tuems0MXJyNWxGY2Y0Q3pseklpMlVVZ2UxeVNjMVpKOVA4VUtveUliSDRIV25mbG8xNld3dzFPWW1sWXBZWmpMZ3ZIc1ZmRVdQa0I1bV9yNmRTZFFpMmNCZTFuMVk4?oc=5) · [Moderna/Merck วัคซีนมะเร็ง -42%](https://www.statnews.com/2026/10/22/esmo-moderna-merck-cancer-vaccine-intismeran-data-released/) · [Amgen มะเร็งปอด -58%](https://www.cnbc.com/2026/10/24/amgen-imdelltra-lung-cancer-data.html) · [Novo CagriSema -25% ในผู้หญิง](https://www.cnbc.com/2026/10/20/novo-cagrisema-women-weight-loss-analysis.html) · [สหรัฐเสนอจำกัดลงทุนไบโอเทคจีน](https://www.statnews.com/2026/10/22/biotech-news-treasury-restrictions-for-us-investment-in-chinese-biotech/)
| หุ้น | ตลาด | เกี่ยวยังไง | ที่มา |
|---|---|---|---|
| AMGN | US | ยามะเร็งปอด Imdelltra | ข่าว |
| MRK | US | วัคซีนมะเร็งร่วม Moderna | ข่าว |
| MRNA | US | วัคซีนมะเร็ง (ผันผวนสูง) | ข่าว |
| NVO | US | CagriSema ยาลดน้ำหนัก | ข่าว |
| LLY | US | Zepbound/Mounjaro โต · retatrutide ชนะ Ozempic | ข่าว (2026-10-29) |
| BDMS.BK | TH | โรงพยาบาล ทางอ้อม | ความรู้ทั่วไป |
อัปเดต 2026-11-01 (weekly): ทั้งสัปดาห์ MRNA +10.8% AMGN +6.1% XLV +3.1% MRK +2.9% NVO +2.4% BDMS +1.0% หลักฐาน: [Lilly ขึ้นคาดการณ์ยอดขาย](https://www.cnbc.com/2026/10/29/eli-lilly-lly-earnings-q3-2026.html) · [retatrutide ชนะ Ozempic](https://www.statnews.com/2026/10/28/biotech-news-lillys-triple-g-drug-beats-ozempic-in-head-to-head-study/) · [Merck งบเกินคาด](https://www.cnbc.com/2026/10/29/merck-mrk-earnings-q3-2026.html) เพิ่ม LLY (ข่าว) · ความเสี่ยงใหม่: [นายจ้างเลิกจ่าย GLP-1 ปี 2027](https://www.cnbc.com/2026/10/27/glp1-drug-coverage-weight-loss-options.html)
ความเสี่ยงของธีม: ข้อมูลบริษัทยังไม่ผ่านผู้ทบทวนอิสระ ราคารับข่าวไปก่อน (Moderna ร่วงทั้งที่ผลดี) รัฐคุมราคายา
อัปเดต 2026-11-08 (weekly): MRNA +14.6% ([ขึ้นคาดการณ์รายได้](https://www.marketwatch.com/story/modernas-stock-jumps-after-biotech-raises-sales-outlook-65363127)) BDMS +1.5% NVO +0.8% ([Wegovy เม็ดขายดี](https://www.cnbc.com/2026/11/04/novo-q3-earnings-wegovy-sales.html)) AMGN -1.2% MRK -1.9% LLY -4.5% XLV ทรงตัว ความเสี่ยงใหม่: [Medicare for All คุมกรรมาธิการ](https://www.statnews.com/2026/11/04/democratic-wins-medicare-for-all-momentum/) · [หุ้นสุขภาพไม่แน่นอนหลังเลือกตั้ง](https://www.cnbc.com/2026/11/07/healthcare-stocks-may-face-trouble-due-to-midterm-results.html)

## ธีมที่จบแล้ว

(ยังไม่มี)
