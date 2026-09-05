# -*- coding: utf-8 -*-
"""Confirmed bookings, flights, and the trip skeleton."""

TRIP = {
    "title": "格魯吉亞 · 亞美尼亞 電單車之旅",
    "subtitle": "Georgia & Armenia Motorcycle Trip 2026",
    "dates": "2026年9月25日 – 10月11日（17日）· 香港出發",
    "travellers": "King Yip Lo（Alex）· Wai Kit Chu（Hugo）",
    "bikes": "2 × KTM 690 · SLAVATOUR / KTM-Georgia",
    "route": "香港 → 吉隆坡 → 多哈 → 第比利斯 → 卡茲別克 → 卡赫季 → 庫塔伊西 → 斯瓦涅季 → 耶烈萬 → 第比利斯",
    "distance": "電單車約 1,500 km · 包車約 400 km",
}

FLIGHTS = [
    ("25/9 五", "CX 733", "21:30", "01:30+1", "香港 HKG", "吉隆坡 KUL", "國泰 · 另一張機票"),
    ("26/9 六", "QR 855", "21:50", "23:55", "吉隆坡 KUL T1", "多哈 DOH", "經濟艙 · 25kg"),
    ("28/9 一", "QR 253", "15:30", "20:10", "多哈 DOH", "第比利斯 TBS", "經濟艙 · 25kg"),
    ("9/10 五", "3F 583", "11:00", "11:40", "耶烈萬 EVN", "第比利斯 TBS", "FlyOne A320 · ✅已訂"),
    ("10/10 六", "QR 256", "14:00", "16:15", "第比利斯 TBS", "多哈 DOH", "經濟艙 · 25kg"),
    ("11/10 日", "QR 852", "02:35", "15:10", "多哈 DOH", "吉隆坡 KUL T1", "經濟艙 · 25kg"),
    ("11/10 日", "CX 724", "17:40", "22:00", "吉隆坡 KUL", "香港 HKG", "⚠️只得 2h30 轉機 · 另一張票"),
]

FLIGHT_REF = {
    "booking": "Q878Z4FG", "airline": "8AWON6",
    "tickets": [("Mr King Yip Lo", "1985-04-09", "1572138506351"),
                ("Mr Wai Kit Chu", "1988-10-31", "1572138506352")],
    "paid": "USD 1,676（機票 819.22 + 稅 856.78）· 已付清",
    "promo": "目的地酒店 5% 折扣碼 QRHHOTEL",
    "contact": "Holidays@qatarairways.com.qa · +974 4144 5544（六–四 11:00–19:00，五休）",
}

# name, city, dates, nights, platform, ref, amount, refund, status
BOOKINGS = [
 ("Eaton Residence Unique Home KLCC","吉隆坡 Kuala Lumpur","25–26/9","1","Booking.com","—","HK$694","免費取消","ok"),
 ("Souq Al Wakra Hotel By Tivoli","多哈 Al Wakra","26–28/9","2","Qatar Holidays","Q878Z4FG","套票內","套票條款","ok"),
 ("Pura Vida Boutique Hotel Tbilisi","第比利斯 Tbilisi","28–29/9","1","Booking.com","—","HK$398","免費取消","ok"),
 ("Landscapes Hotel Kazbegi","卡茲別吉 Kazbegi","29/9–1/10","2","（待補）","（待補）","（待補）","鎮內 Marjanishvili St · 5 房小酒店 · 露台山景","ok"),
 ("Schuchmann Wines Chateau, Villas & SPA","卡赫季 Kisiskhevi","1–2/10","1","酒莊直接","RP8S","GEL 525","含品酒晚餐+SPA","ok"),
 ("AUTOGRAPH Kutaisi","庫塔伊西 Kutaisi","2–3/10","1","Booking.com","—","—","9.7 傑出 · 110a Gelati St","ok"),
 ("Guest House Keti Margiani","梅斯蒂亞 Mestia","3–4/10","1","Agoda","69553611","—","—","ok"),
 ("Mountain house","烏樹故里 Ushguli","4–5/10","1","Agoda","69553611","—","—","ok"),
 ("Newport Hotel Kutaisi","庫塔伊西 Kutaisi","5–6/10","1","Agoda","69553611","—","—","ok"),
 ("Fabrika Hostel & Suites","第比利斯 Tbilisi","6–7/10","1","Booking.com","—","HK$389","不可退款","ok"),
 ("R&R Hotel","耶烈萬 Yerevan","7–9/10","2","Trip.com","1359046727836962","HK$1,121.50","—","ok"),
 ("Fabrika Hostel & Suites","第比利斯 Tbilisi","9–10/10","1","Booking.com","—","HK$425","不可退款","ok"),
]

RENTAL = {
    "company": "SLAVATOUR / KTM-Georgia（Camp Hotel Pura Vida 內）",
    "contact": "Slava Tavartkiladze · ktm-georgia.com",
    "bikes": "2 × KTM 690",
    "period": "29 Sep – 6 Oct 2026（8日）⚠️ 原 reserve 26 Sep–6 Oct，要改",
    "deposit": "€850 / 車 = €1,700（Visa／現金／轉賬）",
    "insurance": "Kasko 全保（條款待收；要問碎石路保唔保）",
    "licence": "A 牌 + 持牌滿 1 年（>500cc）",
    "armenia": "❌ 唔過境 → 唔使 250 GEL×2 授權書",
    "luggage": "建議軟袋（唔用硬箱）",
}

TODO = [
 ("🔴 即刻","覆 Slava 改租車期 29 Sep–6 Oct","email","—","講明唔過境，慳 250 GEL×2"),
 ("🔴 即刻","**訂 GoTrip 包車（7/10 Tbilisi→Yerevan）**","gotrip.ge","US$150–300","要停 Debed 三修道院 — 最後一項交通"),
 ("🟠 2週內","約 Schuchmann 酒浴 SPA 時段（1/10）","wine-spa 網上／+995 598 656 306","已含房價","11:00–20:00"),
 ("🔴 即刻","**Email 多哈酒店確認 01:00 夜到**","+974 4428 7888 · 引用 Q878Z4FG","—","核實 check-in 日期係 26/9 唔係 27/9"),
 ("🔴 即刻","**WhatsApp「Unique Home」約 01:30 夜間自助 check-in**","Booking 訊息","—","私人公寓冇前台，唔約好 03:00 入唔到"),
 ("🔴 即刻","**訂雙子塔 Skybridge 時段**（26/9 約 11:00）","eticket.petronastwintowers.com.my","RM98 ×2","週六位早清"),
 ("🟠 2週內","IDP ×2 + 電單車保險","運輸署／保險公司","HKD80 ×2","保險要明確保 >125cc"),
 ("🟡 3–4週","Barbarestan（9/10 告別晚餐）","電話／IG","100–150 GEL/人","全城最難訂"),
 ("🟡 3–4週","Jiwan @ NMoQ（27/9 多哈午餐）","jiwan.qa","QAR 100 set","米芝蓮必比登"),
 ("🟡 3–4週","Dolmama（8/10 Yerevan）","dolmamarestaurant.com","25–40k AMD","要庭院位"),
 ("🟢 1–2週","Maisi（29/9）· Palaty（2/10）· Lavash（7/10）","電話／rezto.ge","—","Maisi 逢三休"),
 ("🟢 1–2週","Chreli-Abano 硫磺浴（9/10）","booking.chreli-abano.ge","120–200 GEL/房/鐘","兩人分"),
 ("🔵 1週前","Cafe Laila（3/10 Mestia）+ 全面重confirm","+995 577 577 677","—","Laila 只收現金"),
 ("🔵 1週前","問 R&R Hotel 9/10 朝機場接送","Trip.com／酒店","—","09:30 到 EVN"),
]

PRACTICAL = [
 ("緊急電話","格魯吉亞 112（英語可）· 亞美尼亞 911／112 · 卡塔爾 999 · 馬來西亞 999"),
 ("貨幣","1 GEL≈HK$2.9 · 1 AMD≈HK$0.02 · QAR 1≈HK$2.1 · RM 1≈HK$1.8"),
 ("現金重點","Ushguli 全村冇 ATM、只收現金 → Mestia 撳定 400–600 GEL/人"),
 ("電壓插頭","格／亞：220V 歐式圓腳 C/F · 卡塔爾：240V 英式 G · 馬來西亞：240V G"),
 ("SIM","第比利斯機場 Magti 15 GEL/5GB · 亞美尼亞 Ucom／Team · 多哈用漫遊或 eSIM"),
 ("罰單","格魯吉亞天眼為主，唔會現場收現金 → video.police.ge 查同交"),
 ("🔴 導航","**Zagari 山口段 Google Maps 係壞嘅**：會俾 298–400km／8–10 小時，實際 73km／2 小時。用離線 GPX／Organic Maps"),
 ("道路 2025–26","Rikoti 高速（第比利斯–Kutaisi）2025年12月全線通車，51 條隧道 — 比舊資料快"),
 ("騎行","日落 18:30 前埋站 · 牛／羊群隨時封路 · 盲彎有車爬頭 · 唔好夜騎"),
 ("酒駕","格魯吉亞 0.03%（≈一杯已中），罰 700 GEL 起 → 品酒只安排喺過夜點"),
]


# ===== 預約清單（研究後） =====
# tier, name, date, how, price, why
BOOK_NOW = [
 ("🔴","雙子塔 Skybridge","26/9 六","eticket.petronastwintowers.com.my","RM80–98/人","全程唯一真正會賣完 · 限時入場+每日上限 · 週六最差 · 揀 10:00–12:00"),
 ("🔴","Maisi 晚餐","29/9 二","📧 reservations@mountaway.com · FB RestaurantMaisi · ☎+995 575 75 73 37","100–150 GEL/人","超細間 · 每晚只得 19:30／21:00 兩場 · 酒店喺鎮內 2km，坐的士去，兩場都得"),
 ("🔴","Toma's Wine Cellar","2/10 五","FB facebook.com/TomasWineCellar · 📧 tomaswinecellar@gmail.com","~50 GEL/人","冇餐牌，按確認人數煮 — 唔訂就冇得食 · ⚠️逢二休"),
 ("🔴","Schuchmann 酒浴 SPA 療程","1/10 四","schuchmann-wines.com/hotel/wine-spa/wine-spa-reservation/","355 GEL/90分","⚠️房價只包 SPA 入場，療程另計 · 得一間療程房"),
 ("🔴","Chreli-Abano 硫磺浴","9/10 五晚","booking.chreli-abano.ge · ☎+995 322 93 00 93","130 GEL/房/鐘","星期五最旺 · 呢個尺寸只得 3 間房 · 訂 17:00 或 18:00"),
 ("🔴","ARARAT 白蘭地英文團","8/10 四","araratbrandy.com/en/museum/ · ☎+374 10 51 01 49","4,500 AMD/人","每日淨得一場英文團(~11:30) · 直接訂平一半 · 同 Garni 撞"),
 ("🔴","Landscapes Hotel 問早餐＋泊車","29–30/9","訂房平台訊息 · ☎ +995 32 247 01 49","—","官網列有早餐但未必包喺房價 · 問兩架電單車泊邊、幾點 check-in"),
 ("🔴","Keti Margiani 訂餐","3–4/10","Booking 訊息 thread","晚餐 25–45 · 早餐 15 GEL","早餐唔包、晚餐要 on request · 仲要叫佢整 4/10 乾糧午餐"),
 ("🔴","Mountain house 訂餐","4–5/10","Agoda 訊息 thread","晚餐 30–50 GEL 現金","冇早餐冇 half-board · 5/10 朝要過 Zagari"),
]
BOOK_LATER = [
 ("🟡","Dolmama","8/10 Yerevan","dolmamarestaurant.com/en/online-reservation","20–30k AMD","葡萄藤庭院 3–11月開，要寫明"),
 ("🟡","In Vino 導賞品酒","7 或 8/10","GetYourGuide · ☎+374 10 521931","~US$21","導賞一定要預約（酒吧本身 walk-in OK）"),
 ("🟡","Jiwan @ NMoQ","27/9 多哈","WhatsApp +974 7102 7750 · jiwan.qa","set lunch QAR 100","米芝蓮必比登 · 逢二休 · 要露台位講明"),
 ("🟡","IDAM by Ducasse（可選）","27/9 多哈","idam.com · ☎+974 4422 4488","QAR 350/人","米芝蓮一星 · ⚠️只做日–四，12:30–14:00／19:00–21:00"),
 ("🟡","Gastro Yard Garni 打餅","8/10","叫 R&R 前台／司機 · WhatsApp +374 77 520710","~US$18/人","標明「需預約／團體」— 兩人 walk-in 未必燒爐"),
 ("🟡","Palaty","5/10 Kutaisi","rezto.ge/reservation/palaty","20–60 GEL","網上訂有 10% 折 · 現場鋼琴"),
 ("🟡","Craft Wine Restaurant","6/10 Tbilisi","craft-wine-bar-tbilisi.resos.com","70–110 GEL","⚠️星期二只做 18:00–24:00"),
 ("🟡","Li Yen @ Ritz-Carlton","26/9 KL","OpenTable（即時確認）","RM120–200","全 KL 唯一值得訂"),
 ("🟡","Cafe Laila","3/10 Mestia","☎+995 577 57 76 77 · FB Messenger","30–50 GEL","✅收信用卡（更正）· 到咗先訂"),
 ("🟡","Lilestan","2 或 5/10 Kutaisi","WhatsApp +995 577 90 15 90","30–50 GEL","英文 OK · 燈串庭院"),
]
BOOK_NEVER = """<b>格魯吉亞</b>　Rooms Kazbegi The Kitchen（⚠️非住客根本唔收訂位，18:30 早到）· Korbuda · Qondari · Stancia · Tiba ·
El Depo（24h，現金）· Baraqa · Bikentia's（12 GEL，現金）· Sapere · Old House（現金）· Lushnu Qor ·
<b>Ushguli 全部</b>（Koshki／Cafe Svaneti／Murkvam／Shumeri — 係有爐嘅村屋，唔係有 booking book 嘅餐廳）· FARM（Fabrika 內 08:00）· Ghebi（24h）· Amo Rame<br>
<b>亞美尼亞</b>　Tumanyan Khinkali · Tavern Yerevan · Sherep · Anteb · Old Garni · Harmonia Garden · Qefilyan（叫司機提前打 +374 55 210210 就夠）<br>
<b>景點門票</b>　IAMM RM20 · 黑風洞 免費 · Msheireb 免費 · Garni 1,500 AMD · Geghard 免費 · Cascade 免費 · Gelati 免費 ·
Uplistsikhe 15 GEL · 史太林博物館 15 GEL · 斯瓦涅季博物館 20 GEL · Narikala 纜車 2.5 GEL（⚠️要 Metromoney 卡，唔收現金）"""

TRAPS = [
 ("Kazbegi 酒店已改 Landscapes Hotel（鎮內）","Marjanishvili St，離廣場 600m／10 分鐘，Tiba 6 分、Rooms 7 分 — 之前 Gagma 離鎮 10km 嘅問題已經冇咗。Maisi 喺 Gergeti 村 2km，坐的士"),
 ("Rooms Kazbegi 非住客唔收訂位","30/9 想去就 18:30 早到 walk-in"),
 ("Cafe Laila 收信用卡","更正之前「只收現金」· Old House 先係只收現金"),
 ("NMoQ 而家半價 QAR 25","部分展廳維修到 2026/12/30 — 平咗但睇唔晒"),
 ("Cascade 室內畫廊只開五–日","你 7–8/10（三、四）入唔到，戶外階梯照行"),
 ("Zagari 通常開到 10月中","5/10 已近尾聲 — 出發前 24–48 小時問 SLAVATOUR 同 Ushguli 房東"),
 ("Mestia ATM 會抽乾","3/10 一到即撳 400–600 GEL，唔好等 4/10 朝"),
 ("AUTOGRAPH ≠ 萬豪 Autograph Collection","係前身 Green House Guest House 改名嘅民宿，唔好期望酒店餐廳"),
 ("KL Tower 加價","Sky Deck 而家 RM140（唔係 RM78）"),
 ("Gelati 長期維修中","2/10 晚叫 AUTOGRAPH 前台打電話確認 3/10 主教堂開唔開"),
]
ONARRIVAL = """格魯吉亞<b>冇 OpenTable／TheFork</b> — 唯一好用嘅網上系統係 <b>rezto.ge</b>（Palaty）同 <b>resOS</b>（Craft Wine）。<br>
最有效渠道係 <b>Facebook Messenger</b>，其次 WhatsApp／Viber，最後先係電話 — 山區餐廳好多冇人聽電話但會覆 Messenger。<br>
<b>叫酒店／民宿前台幫你打電話最快</b>，尤其 Kazbegi／Mestia／Ushguli。<br>
格魯吉亞人 <b>20:00–21:00</b> 先食晚飯，19:00 去多數有位 · 訂位一般唔使按金、唔會 no-show 收費 · 好多餐廳自動加 <b>10% service</b>，加咗就唔使再畀貼士。"""
