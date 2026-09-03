# -*- coding: utf-8 -*-
"""Confirmed bookings, flights, and the trip skeleton."""

TRIP = {
    "title": "格魯吉亞 · 亞美尼亞 電單車之旅",
    "subtitle": "Georgia & Armenia Motorcycle Trip 2026",
    "dates": "2026年9月25日 – 10月11日（17日）",
    "travellers": "King Yip Lo（Alex）· Wai Kit Chu（Hugo）",
    "bikes": "2 × KTM 690 · SLAVATOUR / KTM-Georgia",
    "route": "吉隆坡 → 多哈 → 第比利斯 → 卡茲別克 → 卡赫季 → 庫塔伊西 → 斯瓦涅季 → 耶烈萬 → 第比利斯",
    "distance": "電單車約 1,500 km · 包車約 400 km",
}

FLIGHTS = [
    ("26/9 六", "QR 855", "21:50", "23:55", "吉隆坡 KUL T1", "多哈 DOH", "經濟艙 · 25kg"),
    ("28/9 一", "QR 253", "15:30", "20:10", "多哈 DOH", "第比利斯 TBS", "經濟艙 · 25kg"),
    ("9/10 五", "3F 583", "11:00", "11:40", "耶烈萬 EVN", "第比利斯 TBS", "FlyOne A320 · ✅已訂"),
    ("10/10 六", "QR 256", "14:00", "16:15", "第比利斯 TBS", "多哈 DOH", "經濟艙 · 25kg"),
    ("11/10 日", "QR 852", "02:35", "15:10", "多哈 DOH", "吉隆坡 KUL T1", "經濟艙 · 25kg"),
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
 ("Gagma Chalets Kazbegi","卡茲別吉 Kazbegi","29/9–1/10","2","Booking.com","—","HK$1,359","免費取消 · 單臥室小木屋","ok"),
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
 ("騎行","日落 18:30 前埋站 · 牛／羊群隨時封路 · 盲彎有車爬頭 · 唔好夜騎"),
 ("酒駕","格魯吉亞 0.03%（≈一杯已中），罰 700 GEL 起 → 品酒只安排喺過夜點"),
]
