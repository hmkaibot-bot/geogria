# -*- coding: utf-8 -*-
import sys, csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from html import escape as e
from style import CSS
import render as R
import data_core as C
import data_days as DD
import images as IM

UPDATED = "2026-09-05"

PRI = {"must":("must","★ 必去"), "alt":("alt","○ 替代"),
       "bon":("bon","＋ 加碼"), "skip":("skip","✕ 可跳")}
TIER = {"平":"b","中":"m","貴":"s"}

parts = [R.cover(C.TRIP, IM, IM.COVER, UPDATED)]

# ========== 0. 行程一覽（相片） ==========
parts.append(R.section("行程一覽", "OVERVIEW · 17 日 · 相片全部為真實 CC 授權相，來源見最後一頁", R.overview(IM.OVERVIEW, IM) +
    R.note("<b>點用呢本 PDF：</b>每日一頁 — 時間表 → 行車段 → 酒店（訂單編號）→ 三餐（平／中／貴）→ 景點（座標）。"
           "座標可以直接 copy 入 Google Maps；全部點亦喺《座標總表》一次過列出。")))

# ========== 1. 訂單 + 航班 ==========
inner = []
f = C.FLIGHT_REF
inner.append(R.block("✈️ 機票 — Qatar Airways Holidays 套票",
    f'<div class="hotel"><span class="hn">訂單編號 {f["booking"]}　·　航空公司訂位編號 {f["airline"]}</span>'
    f'<div class="meta">{e(f["paid"])}　·　{e(f["promo"])}</div>'
    f'<div class="meta small">{e(f["contact"])}</div></div>' +
    R.tbl(["日期","航班","起飛","抵達","航段","備註"],
      [[e(a),f"<b>{e(b)}</b>",e(c),e(d),f"{e(g)} → {e(h)}",R.md(e(i))] for a,b,c,d,g,h,i in C.FLIGHTS],
      [None,None,"t","t",None,None]) +
    R.tbl(["旅客","出生日期","機票號碼"],
      [[e(n),e(dob),f'<span class="c">{e(tk)}</span>'] for n,dob,tk in f["tickets"]]) +
    R.warn("座位同餐飲偏好<b>未指定</b> — 上 qatarairways.com 用訂位編號 <b>8AWON6</b> 揀位")))

brows = []
for n,city,dates,nights,plat,ref,amt,ref2,st in C.BOOKINGS:
    badge = R.pill("已訂","ok") if st=="ok" else R.pill("要訂","no")
    brows.append([badge+" "+e(n), e(city), f"<b>{e(dates)}</b>", e(nights), e(plat),
                  f'<span class="c">{e(ref)}</span>', f"<b>{e(amt)}</b>", R.md(e(ref2))])
inner.append(R.block("🏨 住宿訂單（14 晚）",
    R.tbl(["酒店","城市","日期","晚","平台","訂單編號","金額","備註"], brows,
          [None,None,"t",None,None,None,None,None]) +
    R.note("🎉 <b>住宿全部訂晒 — 14/14 晚</b>。由 25/9 吉隆坡到 9/10 第比利斯，每一晚都有落腳點，冇 gap。"
           "淨返嘅只有 <b>7/10 GoTrip 包車</b> 同 <b>租車改期</b>。")))

r = C.RENTAL
inner.append(R.block("🏍 租車 — " + r["company"],
    R.tbl(["項目","詳情"], [[e(k), e(v) if k!="亞美尼亞" else f"<b>{e(v)}</b>"] for k,v in
      [("聯絡", r["contact"]),("車", r["bikes"]),("租期", r["period"]),("押金", r["deposit"]),
       ("保險", r["insurance"]),("牌照要求", r["licence"]),("亞美尼亞", r["armenia"]),("行李", r["luggage"])]],
      ["t",None])))
parts.append(R.section("訂單總覽", f"BOOKINGS · ✅ 14/14 晚已訂 · 最後更新 {UPDATED}", "".join(inner), IM, IM.SECTION_BANNER["訂單總覽"]))

# ========== 2. 逐日 ==========
for d in DD.D:
    b = []
    if d["sched"]:
        b.append(R.block("⏱ 時間表", R.tbl(["時間","行程"],
            [[f'<b>{e(t)}</b>', R.md(w)] for t,w in d["sched"]], ["t",None])))
    if d.get("legs"):
        b.append(R.block("🛣 行車段", R.tbl(["由","到","距離","時間","路況／備註"],
            [[e(a),e(bb),f"<b>{e(km)}</b>",R.md(e(tm)),R.md(e(nt))] for a,bb,km,tm,nt in d["legs"]],
            [None,None,"km","km",None])))
    h = d.get("hotel")
    if h and h.get("name"):
        b.append(R.block("🏨 住宿", R.hotel_card({**h, "extra": R.md(h.get("extra","")), "name": h.get("name","")})))
    if d.get("meals"):
        rows = []
        for slot, opts in d["meals"].items():
            for i,(tier,name,price) in enumerate(opts):
                rows.append([f"<b>{e(slot)}</b>" if i==0 else "",
                             R.pill(tier, TIER.get(tier,"b")), R.md(name), R.md(e(price))])
        b.append(R.block("🍽 三餐（平／中／貴）",
            R.tbl(["","檔次","餐廳","價錢"], rows, ["t",None,None,None])))
    if d.get("sights"):
        rows = []
        for pri,name,coord,detail in d["sights"]:
            k,lab = PRI.get(pri,("bon","＋"))
            rows.append([R.pill(lab,k), R.md(name), f'<span class="c">{e(coord)}</span>', R.md(detail)])
        b.append(R.block("🏛 景點（座標）", R.tbl(["","景點","座標","詳情／開放／門票"], rows,
            [None,None,"c",None])))
    for w in d.get("warns",[]):  b.append(R.warn("⚠️ " + R.md(w)))
    for n in d.get("notes",[]):  b.append(R.note("💡 " + R.md(n)))
    parts.append(R.day(d["num"], d["date"], d["wd"], d["route"], d["stats"], b,
                       IM, IM.DAY_HERO.get(d["num"]), IM.DAY_STRIP.get(d["num"], ())))

# ========== 3. 座標總表 ==========
rows = []
csvp = "/home/user/geogria/file13-pins.csv"
if os.path.exists(csvp):
    with open(csvp, encoding="utf-8") as fh:
        for r_ in csv.DictReader(fh):
            rows.append([e(r_["Name"]), f'<span class="c">{r_["Latitude"]}, {r_["Longitude"]}</span>',
                         e(r_["Day"]), e(r_["Category"]), e(r_["Notes"])])
extra = [
 ("Eaton Residence Unique Home KLCC","3.15153, 101.71996","D01","Lodging","26 Jalan Kia Peng · 私人公寓，冇前台"),
 ("Souq Al Wakra Hotel By Tivoli","25.173813, 51.610445","D03-04","Lodging","Al Wakra 老市集內 · +974 4428 7888"),
 ("Al Wakra 地鐵站（紅線總站）","25.19349, 51.59601","D03","Logistics","離酒店 4–5km，行唔到"),
 ("Museum of Islamic Art (MIA)","25.2952, 51.5397","D03","Sight","QAR 50 · 逢三休"),
 ("National Museum of Qatar","25.2867, 51.5514","D03","Sight","QAR 50 · 逢二休"),
 ("Souq Waqif","25.2870, 51.5333","D03","Sight","12:00–16:00 落閘"),
 ("Msheireb Museums","25.2870, 51.5250","D04","Sight","免費 · 逢日休"),
 ("Schuchmann Wines Chateau","41.8700, 45.5200","D07","Lodging","訂單 RP8S · Kisiskhevi"),
 ("Guest House Keti Margiani Mestia","43.048314, 42.730451","D09","Lodging","Lanchvali St 7 · Seti 廣場上面 8 分鐘"),
 ("Mountain house Ushguli","42.915166, 43.011476","D10","Lodging","⚠️座標待確認（有兩間同名）"),
 ("Newport Hotel Kutaisi","42.272838, 42.706514","D11","Lodging","Newport St 11/1 · 含早餐"),
 ("Pura Vida / Camp Hotel（SLAVATOUR）","41.7800, 44.7400","D04-05","Lodging","Digomi 西北郊 · 電單車基地"),
 ("AUTOGRAPH Kutaisi","42.2830, 42.7250","D08","Lodging","110a Gelati St · 9.7 傑出"),
 ("Fabrika Hostel & Suites","41.7028, 44.7995","D12/D15","Lodging","第比利斯 Chugureti"),
 ("R&R Hotel Yerevan","40.1815, 44.5145","D13-14","Lodging","17 Nalbandyan St · 1359046727836962"),
 ("Zvartnots Airport (EVN)","40.1473, 44.3959","D15","Logistics","FlyOne 3F583 11:00"),
 ("KLIA Terminal 1","2.7456, 101.7099","D02/D17","Logistics","Qatar 用 T1"),
 ("Hamad Intl Airport (DOH)","25.2609, 51.6138","D02-04","Logistics","轉機"),
]
rows.extend([[e(a), f'<span class="c">{b}</span>', e(c), e(dd), e(ee)] for a,b,c,dd,ee in extra])
parts.append(R.section("座標總表", f"COORDINATES · {len(rows)} 點 · 可匯入 Google My Maps", IM=IM, banner=IM.SECTION_BANNER["座標總表"], inner=
    R.tbl(["名稱","座標（緯度, 經度）","日","類別","備註"], rows, [None,"c","t",None,None]) +
    R.note("匯入方法：電腦開 <b>mymaps.google.com</b> → 建立新地圖 → 匯入 <b>file13-pins.csv</b> → "
           "位置欄揀 Latitude + Longitude、標題揀 Name → 用 Category 分色。手機 Google Maps → 已儲存 → 離線都睇到。")))

# ========== 4. TODO ==========
parts.append(R.section("出發前 TO-DO", "ACTION LIST · 按死線排序", IM=IM, banner=IM.SECTION_BANNER["出發前 TO-DO"], inner=
    R.tbl(["死線","事項","點做","價","備註"],
      [[f"<b>{e(a)}</b>", R.md(b), e(c), e(dv), R.md(e(ev))] for a,b,c,dv,ev in C.TODO], ["t",None,None,None,None])))

# ========== 4b. 預約清單 ==========
bk = []
bk.append(R.block("🔴 而家喺香港訂（真係會冇位／得一場）",
    R.tbl(["","項目","日期","點訂","價","點解一定要訂"],
      [[R.pill("必訂","no"), f"<b>{e(n)}</b>", e(dt), R.md(e(hw)), e(pr), R.md(e(why))]
       for _,n,dt,hw,pr,why in C.BOOK_NOW], [None,None,"t",None,None,None])))
bk.append(R.block("🟡 到咗先訂 / 或 1–2 星期前（易訂，唔會冇位）",
    R.tbl(["","項目","日期","點訂","價","備註"],
      [[R.pill("建議","m"), f"<b>{e(n)}</b>", e(dt), R.md(e(hw)), e(pr), R.md(e(why))]
       for _,n,dt,hw,pr,why in C.BOOK_LATER], [None,None,"t",None,None,None])))
bk.append(R.block("⚪ 唔使訂（walk-in 就得，訂都冇用）", f'<div class="hotel small">{C.BOOK_NEVER}</div>'))
bk.append(R.block("⚠️ 研究揪出嚟嘅陷阱",
    R.tbl(["發現","影響"], [[f"<b>{e(k)}</b>", R.md(e(v))] for k,v in C.TRAPS], ["t",None])))
bk.append(R.block("📱 到咗當地點訂？", f'<div class="note">{C.ONARRIVAL}</div>'))
bk.append(R.note("<b>訂位範本：</b>「Hello! Could we book a table for 2 people on [DATE] at [TIME]? "
    "Name: Alex · Phone/WhatsApp: [NUMBER]. We are visiting from Hong Kong. Thank you!」<br>"
    "<b>問民宿餐食：</b>「Hello, we have a booking for [DATES] (2 people, motorcycles). "
    "1) Can you please provide DINNER on [DATE] around 19:30? 2) Can we have BREAKFAST on [DATE] at 07:30? "
    "3) Could you prepare a PACKED LUNCH for [DATE]? Please tell us the price per person. We will pay cash in GEL.」"))
parts.append(R.section("預約清單", "RESERVATIONS · 而家訂 / 到咗訂 / 唔使訂", "".join(bk), IM, IM.SECTION_BANNER["預約清單"]))

# ========== 5. 實用 ==========
parts.append(R.section("實用資料", "PRACTICAL", IM=IM, banner=IM.SECTION_BANNER["實用資料"], inner=
    R.tbl(["項目","詳情"], [[f"<b>{e(k)}</b>", R.md(e(v))] for k,v in C.PRACTICAL], ["t",None]) +
    R.warn("<b>只收現金：</b>Ushguli 全村 · Cafe Laila（Mestia）· Bikentia's（Kutaisi）· Nunu's（Lentekhi）· "
           "Zugdidi 巴刹 · Dry Bridge 市集 · Surami nazuki 攤 · Garni 小檔 · 多哈街邊 karak · KL 小販檔") +
    R.note("<b>每日出發前 check：</b>georoad.ge（格魯吉亞路況）· armroad.am（亞美尼亞）· 天氣（按山口高度睇，唔係市鎮）· 當日景點營業")))

# ========== 6. 相片來源 ==========
parts.append(R.section("相片來源", "PHOTO CREDITS · Creative Commons",
    R.note("所有相片均為 <b>Creative Commons</b> 授權嘅真實相片（Flickr 經 Openverse／Wikimedia Commons），作者同授權條款如下；本 PDF 只作私人旅行用途。") +
    '<div style="height:3mm"></div>' + R.credits_page(IM)))

open(os.path.join(HERE,"itinerary.html"),"w",encoding="utf-8").write(R.html_doc(CSS,"".join(parts)))
print("HTML written:", sum(len(p) for p in parts), "chars,", len(DD.D), "days,", len(rows), "coords")
