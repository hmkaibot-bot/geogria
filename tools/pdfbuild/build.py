# -*- coding: utf-8 -*-
import sys, csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from html import escape as e
from style import CSS
import render as R
import data_core as C
import data_days as DD

PRI = {"must":("must","★ 必去"), "alt":("alt","○ 替代"),
       "bon":("bon","＋ 加碼"), "skip":("skip","✕ 可跳")}
TIER = {"平":"b","中":"m","貴":"s"}

parts = [R.cover(C.TRIP)]

# ========== 1. 訂單 + 航班 ==========
inner = []
f = C.FLIGHT_REF
inner.append(R.block("✈️ 機票 — Qatar Airways Holidays 套票",
    f'<div class="hotel"><span class="hn">訂單編號 {f["booking"]}　·　航空公司訂位編號 {f["airline"]}</span>'
    f'<div class="meta">{e(f["paid"])}　·　{e(f["promo"])}</div>'
    f'<div class="meta small">{e(f["contact"])}</div></div>' +
    R.tbl(["日期","航班","起飛","抵達","航段","備註"],
      [[e(a),f"<b>{e(b)}</b>",e(c),e(d),f"{e(g)} → {e(h)}",e(i)] for a,b,c,d,g,h,i in C.FLIGHTS],
      [None,None,"t","t",None,None]) +
    R.tbl(["旅客","出生日期","機票號碼"],
      [[e(n),e(dob),f'<span class="c">{e(tk)}</span>'] for n,dob,tk in f["tickets"]]) +
    R.warn("座位同餐飲偏好<b>未指定</b> — 上 qatarairways.com 用訂位編號 <b>8AWON6</b> 揀位")))

brows = []
for n,city,dates,nights,plat,ref,amt,ref2,st in C.BOOKINGS:
    badge = R.pill("已訂","ok") if st=="ok" else R.pill("要訂","no")
    brows.append([badge+" "+e(n), e(city), f"<b>{e(dates)}</b>", e(nights), e(plat),
                  f'<span class="c">{e(ref)}</span>', f"<b>{e(amt)}</b>", e(ref2)])
inner.append(R.block("🏨 住宿訂單（14 晚）",
    R.tbl(["酒店","城市","日期","晚","平台","訂單編號","金額","備註"], brows,
          [None,None,"t",None,None,None,None,None]) +
    R.warn("<b>淨返 1 晚未訂：2/10（Kutaisi）</b> — 5/10 已經 Agoda 訂咗 Newport Hotel Kutaisi，"
           "<b>同一間加訂 2/10 最方便</b>，唔使搬。其餘 13 晚全部落實。")))

r = C.RENTAL
inner.append(R.block("🏍 租車 — " + r["company"],
    R.tbl(["項目","詳情"], [[e(k), e(v) if k!="亞美尼亞" else f"<b>{e(v)}</b>"] for k,v in
      [("聯絡", r["contact"]),("車", r["bikes"]),("租期", r["period"]),("押金", r["deposit"]),
       ("保險", r["insurance"]),("牌照要求", r["licence"]),("亞美尼亞", r["armenia"]),("行李", r["luggage"])]],
      ["t",None])))
parts.append(R.section("訂單總覽", "BOOKINGS · 13/14 晚已訂 · 最後更新 2026-09-03", "".join(inner)))

# ========== 2. 逐日 ==========
for d in DD.D:
    b = []
    if d["sched"]:
        b.append(R.block("⏱ 時間表", R.tbl(["時間","行程"],
            [[f'<b>{e(t)}</b>', R.md(w)] for t,w in d["sched"]], ["t",None])))
    if d.get("legs"):
        b.append(R.block("🛣 行車段", R.tbl(["由","到","距離","時間","路況／備註"],
            [[e(a),e(bb),f"<b>{e(km)}</b>",f"<b>{e(tm)}</b>",R.md(e(nt))] for a,bb,km,tm,nt in d["legs"]],
            [None,None,"km","km",None])))
    h = d.get("hotel")
    if h and h.get("name"):
        b.append(R.block("🏨 住宿", R.hotel_card({**h, "extra": R.md(h.get("extra",""))})))
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
    parts.append(R.day(d["num"], d["date"], d["wd"], d["route"], d["stats"], b))

# ========== 3. 座標總表 ==========
rows = []
csvp = "/home/user/geogria/file13-pins.csv"
if os.path.exists(csvp):
    with open(csvp, encoding="utf-8") as fh:
        for r_ in csv.DictReader(fh):
            rows.append([e(r_["Name"]), f'<span class="c">{r_["Latitude"]}, {r_["Longitude"]}</span>',
                         e(r_["Day"]), e(r_["Category"]), e(r_["Notes"])])
extra = [
 ("Eaton Residence Unique Home KLCC","3.1580, 101.7120","D01","Lodging","吉隆坡 KLCC"),
 ("Souq Al Wakra Hotel By Tivoli","25.1660, 51.6030","D03-04","Lodging","多哈 Al Wakra · Q878Z4FG"),
 ("Museum of Islamic Art (MIA)","25.2952, 51.5397","D03","Sight","QAR 50 · 逢三休"),
 ("National Museum of Qatar","25.2867, 51.5514","D03","Sight","QAR 50 · 逢二休"),
 ("Souq Waqif","25.2870, 51.5333","D03","Sight","12:00–16:00 落閘"),
 ("Msheireb Museums","25.2870, 51.5250","D04","Sight","免費 · 逢日休"),
 ("Schuchmann Wines Chateau","41.8700, 45.5200","D07","Lodging","訂單 RP8S · Kisiskhevi"),
 ("Fabrika Hostel & Suites","41.7028, 44.7995","D12/D15","Lodging","第比利斯 Chugureti"),
 ("R&R Hotel Yerevan","40.1815, 44.5145","D13-14","Lodging","17 Nalbandyan St · 1359046727836962"),
 ("Zvartnots Airport (EVN)","40.1473, 44.3959","D15","Logistics","FlyOne 3F583 11:00"),
 ("KLIA Terminal 1","2.7456, 101.7099","D02/D17","Logistics","Qatar 用 T1"),
 ("Hamad Intl Airport (DOH)","25.2609, 51.6138","D02-04","Logistics","轉機"),
]
rows.extend([[e(a), f'<span class="c">{b}</span>', e(c), e(dd), e(ee)] for a,b,c,dd,ee in extra])
parts.append(R.section("座標總表", f"COORDINATES · {len(rows)} 點 · 可匯入 Google My Maps",
    R.tbl(["名稱","座標（緯度, 經度）","日","類別","備註"], rows, [None,"c","t",None,None]) +
    R.note("匯入方法：電腦開 <b>mymaps.google.com</b> → 建立新地圖 → 匯入 <b>file13-pins.csv</b> → "
           "位置欄揀 Latitude + Longitude、標題揀 Name → 用 Category 分色。手機 Google Maps → 已儲存 → 離線都睇到。")))

# ========== 4. TODO ==========
parts.append(R.section("出發前 TO-DO", "ACTION LIST · 按死線排序",
    R.tbl(["死線","事項","點做","價","備註"],
      [[f"<b>{e(a)}</b>", R.md(b), e(c), e(dv), R.md(e(ev))] for a,b,c,dv,ev in C.TODO], ["t",None,None,None,None])))

# ========== 5. 實用 ==========
parts.append(R.section("實用資料", "PRACTICAL",
    R.tbl(["項目","詳情"], [[f"<b>{e(k)}</b>", e(v)] for k,v in C.PRACTICAL], ["t",None]) +
    R.warn("<b>只收現金：</b>Ushguli 全村 · Cafe Laila（Mestia）· Bikentia's（Kutaisi）· Nunu's（Lentekhi）· "
           "Zugdidi 巴刹 · Dry Bridge 市集 · Surami nazuki 攤 · Garni 小檔 · 多哈街邊 karak · KL 小販檔") +
    R.note("<b>每日出發前 check：</b>georoad.ge（格魯吉亞路況）· armroad.am（亞美尼亞）· 天氣（按山口高度睇，唔係市鎮）· 當日景點營業")))

open(os.path.join(HERE,"itinerary.html"),"w",encoding="utf-8").write(R.html_doc(CSS,"".join(parts)))
print("HTML written:", sum(len(p) for p in parts), "chars,", len(DD.D), "days,", len(rows), "coords")
