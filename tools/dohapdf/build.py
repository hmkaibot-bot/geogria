# -*- coding: utf-8 -*-
"""多哈 Local Tour 完整選項 — PDF 產生器（HTML → Chromium）。

資料來源：../../24-多哈local-tour選項.md（2026-09-13 查核）
相片：img/*.jpg，全部 Creative Commons，作者同授權見 img/credits.json
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from html import escape as e
from style import CSS

IMG = os.path.join(HERE, "img")
CRED = json.load(open(os.path.join(IMG, "credits.json"), encoding="utf-8"))

CAPTION = {
    "doha_skyline": "多哈 West Bay 天際線",
    "doha_corniche": "Doha Corniche 夜景",
    "doha_inlandsea": "Khor Al Adaid 內海",
    "doha_dunes": "Mesaieed／Sealine 沙丘",
    "doha_dhow": "傳統 dhow 木船 · 舊港",
    "doha_katara": "Katara 文化村圓形劇場",
    "doha_msheireb": "Msheireb Downtown",
    "doha_library": "卡塔爾國家圖書館（Rem Koolhaas）",
    "doha_zubarah": "Al Zubarah 堡壘（UNESCO）",
    "doha_zekreet": "Zekreet 蘑菇岩",
    "doha_falcon": "獵鷹 · Falcon Souq",
    "doha_camel": "駱駝 · Al Shahaniya",
    "doha_purple": "Al Khor 紅樹林 · Purple Island",
    "doha_pearl": "The Pearl · Porto Arabia",
    "doha_mia": "伊斯蘭藝術博物館 MIA",
    "doha_nmoq": "卡塔爾國家博物館「沙漠玫瑰」",
    "doha_souq": "Souq Waqif 老市集",
    "doha_wakra": "Al Wakra 海濱老市集",
}

def path(k): return "file://" + os.path.join(IMG, k + ".jpg")
def has(k): return k in CRED and os.path.exists(os.path.join(IMG, k + ".jpg"))
def cap(k): return CAPTION.get(k, k)
def credit(k):
    c = CRED.get(k, {})
    return " · ".join(x for x in [(c.get("artist") or "").strip(), c.get("license", "")] if x)

def md(t):
    """**bold** → <b>，[文字](url) → <a>"""
    if not isinstance(t, str): return t
    t = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

def tbl(headers, rows, classes=None):
    h = "".join(f"<th>{e(str(x))}</th>" for x in headers)
    body = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            cls = (classes[i] if classes and i < len(classes) and classes[i] else "")
            cls = f' class="{cls}"' if cls else ""
            cells.append(f"<td{cls}>{c}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(body)}</tbody></table>"

def pill(text, kind): return f'<span class="pill p-{kind}">{e(text)}</span>'
def block(title, inner): return f'<div class="block"><div class="bt">{e(title)}</div>{inner}</div>'
def warn(html): return f'<div class="warn">{html}</div>'
def note(html): return f'<div class="note">{html}</div>'
def kill(html): return f'<div class="kill">{html}</div>'

def banner(num, title, sub, key):
    img = ""
    if has(key):
        img = (f'<img src="{path(key)}"><div class="shade"></div>'
               f'<div class="cr">📷 {e(cap(key))} · {e(credit(key))}</div>')
    n = f'<div class="n">{e(num)}</div>' if num else ""
    return (f'<div class="banner">{img}<div class="t">{n}<h2>{e(title)}</h2>'
            f'<div class="s">{e(sub)}</div></div></div>')

def section(num, title, sub, key, inner):
    return f'<div class="sec">{banner(num, title, sub, key)}{inner}</div>'

def strip_imgs(keys):
    keys = [k for k in keys if has(k)]
    if not keys: return ""
    cells = "".join(f'<div class="s"><img src="{path(k)}"><div class="cap">{e(cap(k))}</div></div>' for k in keys)
    return f'<div class="strip">{cells}</div>'

def figure(key, h="40mm"):
    if not has(key): return ""
    return (f'<div class="figure"><img src="{path(key)}" style="height:{h}">'
            f'<div class="cap">📷 {e(cap(key))}<br>{e(credit(key))}</div></div>')

def timeline(rows):
    out = []
    for r in rows:
        hi = ' class="hi"' if len(r) > 2 and r[2] else ""
        out.append(f'<tr{hi}><td class="time">{e(r[0])}</td><td>{md(r[1])}</td></tr>')
    return f'<table class="tl"><tbody>{"".join(out)}</tbody></table>'

P = []   # pages

# =====================================================================
# COVER
# =====================================================================
P.append(f"""<div class="cover">
<img class="bg" src="{path('doha_dunes')}"><div class="scrim"></div>
<div class="in">
<div class="kicker">Doha Stopover · 27–28 Sep 2026</div>
<h1>多哈 Local Tour<br>完整選項</h1>
<div class="sub">兩日一夜中轉，邊啲團值得訂、邊啲剔走</div>
<div class="rule"></div>
<div class="sub" style="font-size:9.5pt;opacity:.85;line-height:1.65">
Alex · Hugo　|　住 Souq Al Wakra Hotel by Tivoli（Al Wakrah）<br>
27/9 有 13:00 Jiwan @ NMoQ 死約　·　28/9 15:30 QR253 飛第比利斯</div>
<div class="grid">
<div class="cell"><b>沙漠日出團</b><span>QAR 320 · 03:30–09:30</span></div>
<div class="cell"><b>Dhow 日落遊船</b><span>QAR 150 · 17:00–19:00</span></div>
<div class="cell"><b>內海保護區入場</b><span>免費 · 冇 permit 費</span></div>
<div class="cell"><b>最大風險</b><span>Al Wakrah 接送要確認</span></div>
</div>
<div class="foot"><span>資料查核 2026-09-13 · 價錢會變，落單前再對一次</span>
<span>📷 {e(cap('doha_dunes'))} · {e(credit('doha_dunes'))}</span></div>
</div></div>""")

# =====================================================================
# 快速結論
# =====================================================================
inner = []
inner.append(block("🎯 你哋嘅硬約束", tbl(["", "內容"], [
    ["<b>住邊</b>", md("Souq Al Wakra Hotel by Tivoli（Al Wakrah，25.1738 / 51.6104）。距多哈市中心約 **16 km**、機場約 **14 km**。")],
    ["<b>最關鍵</b>", md("**Al Wakrah 唔喺大部分 tour 寫嘅「Doha city limits」入面。** Discover Qatar 官網明寫接送範圍係 “major hotels within Doha city limits”。訂之前一定要問：*Do you pick up from Souq Al Wakra Hotel by Tivoli, Al Wakrah? Any surcharge?*")],
    ["<b>好消息</b>", md("你哋住嘅位置係去 Sealine / Mesaieed / Khor Al Adaid 嘅**順路方向**。市區酒店去沙漠入口要 45–60 分鐘，你哋由 Al Wakrah 出發更近 —— **沙漠團反而係你哋最抵玩嘅品類**。")],
    ["<b>27/9</b>", md("13:00 Jiwan @ NMoQ 係死約 → 09:00–12:00 幾乎唔夠做任何半日團（要預返酒店沖涼 + 出市區 20–25 分鐘）。")],
    ["<b>28/9</b>", md("得 08:00–11:30。12:00 退房、14:30 行李櫃枱閂。實際可用 **3 個鐘**，仲要計 Al Wakrah ↔ 市區來回 40–50 分鐘。")],
], ["t", None])))

inner.append(block("📌 三句總結", f"""<div class="cards">
<div class="card"><div class="h">1 · 沙漠日出團</div><div class="m">03:30–09:30 係 27/9 唯一放得落嘅沙漠選項 —— 4 小時內海團嘅兩個時段（09:00–13:00／14:00–18:00）都撞 Jiwan lunch。</div><div class="p">QAR 320</div></div>
<div class="card"><div class="h">2 · 28/9 唔好貪心</div><div class="m">最穩陣係 MIA 開門 09:00 入去嘆冷氣 90 分鐘，或者純粹行酒店門口嘅 Souq Al Wakra + Corniche。</div><div class="p">QAR 50 / 免費</div></div>
<div class="card"><div class="h">3 · 中轉團剔走</div><div class="m">Qatar Airways transit tour 同 +Qatar stopover 你哋基本上用唔到（已入境、自己訂咗酒店）。唔好白費時間研究。</div><div class="p">✕ 剔走</div></div>
</div>"""))

inner.append(strip_imgs(["doha_inlandsea", "doha_nmoq", "doha_wakra", "doha_dhow", "doha_souq"]))
inner.append(warn(md("**單一最大風險點：** 官網只寫 “within Doha city limits”。**先打 +974 4144 5150 問 Al Wakrah 接送，再落沙漠團單。** "
                     "如果 Discover Qatar 唔肯出 Al Wakrah，就轉 OTA（GetYourGuide／Viator checkout 時可以自己揀酒店 pickup point）"
                     "或者直接 WhatsApp 365 Adventures（+974 3339 3323）報私人價。")))
P.append(section("QUICK VERDICT", "快速結論", "兩日一夜真正做得到嘅事", "doha_skyline", "".join(inner)))

# =====================================================================
# 1 沙漠／內海 4x4
# =====================================================================
inner = []
inner.append(block("🏜 Discover Qatar（Qatar Airways 官方旅遊臂）— 一線選擇", tbl(
    ["產品", "時長", "時間", "價錢", "備註"],
    [[md("**Discover Sunrise in the Desert**（私人）"), "6 小時", md("**4–9月 03:30–09:30**"), md("**QAR 320**<br>≈US$88"),
      md("私人團、英語司機導遊、冷氣 4x4、30 分鐘 dune drive、日出影相位、**喺五星 Outpost Al Barari 沙漠營食早餐**、阿拉伯咖啡")],
     ["Discover the Desert and Inland Sea（私人）", "4 小時", "09:00–13:00 / 14:00–18:00 每日", md("**QAR 227 / 架車**<br>（最多 5 人）"),
      md("只包車＋持牌英語司機導遊，**唔包餐**。兩個人分＝每人 QAR 113，**全多哈最抵嘅私人 4x4 價** —— 可惜兩個時段都撞 Jiwan lunch")],
     ["Discover Dinner in the Desert", "5 小時", pill("未核實", "unv"), "由 QAR 295 起", "沙漠晚餐"]],
    [None, "t", None, "n", None])
    + note(md("官方訂購 discoverqatar.qa　·　電話 **+974 4144 5150**　·　"
              "⚠️ **取消政策官網冇寫**，訂之前要 email 問清楚。"))))

inner.append(block("🚙 其他本地 operator", tbl(["Operator", "聯絡", "備註"], [
    [md("**365 Adventures**"), md("**+974 3339 3323**（電話／WhatsApp）· 365adventures.me"),
     md("做 desert safari、city tour、kayaking、遊艇。卡塔爾第一間拎 Qatar Sustainability Certificate 嘅冒險公司。**網站冇公開價目，要 WhatsApp 報價**")],
    ["Inland Sea Tours", "inlandseatours.com", "專做內海 safari，有酒店接送。" + pill("價錢未核實", "unv")],
    ["Doha Magic Adventures", "dohamagicadventures.com", md("**有 Doha & Al Wakra Souq 組合團** — 見第 5 節")],
    ["Nomad Tourism Qatar", "nomadtourismqatar.com", "Al Khor + Purple Island kayak 6 小時"],
    ["Desert Track Tourism", "經 Expedia／TripAdvisor 上架", "Qatar West Tour 約 US$170 / 成人 " + pill("未核實", "unv")],
    ["Doha Adventure Tours · Golden Adventures", "各自官網", pill("未核實", "unv")],
], [None, None, None])
    + warn(md("**Arabian Adventures / Qatar Inbound Tours / Falcon Tours / Gulf Adventures：** 今次搵唔到 2025–26 年官方價目頁，"
              "**未核實**，唔亂寫價。要覆蓋就直接 Google「&lt;名&gt; Qatar contact」拎 WhatsApp 報價。"))))

inner.append(block("🛒 OTA 上架（GetYourGuide / Viator / Klook）", f"""
<ul class="tight">
<li>{md("價格區間（綜合搜尋結果，屬二手資料）：共乘 safari 約 **QAR 150 / 人**；私人車約 **QAR 600–650 / 架**。")}</li>
<li>{md("半日 4–5 小時＝dune bashing + 沙板 + 內海影相 20–30 分鐘；全日 7–8 小時＝加內海游水 60–90 分鐘 + 沙漠營 BBQ。")}</li>
<li>{md("**Inland Sea 保護區入場免費，冇 permit 費** —— 你畀嘅錢係畀架 4x4 同司機。")}</li>
<li>{md("**OTA 最大好處：GetYourGuide 同 Viator 大部分產品寫明 24 小時前免費取消**，而 Discover Qatar 官網冇公開取消條款。唔肯定頂唔頂到 40 度，行 OTA 買、留返免費取消權。")}</li>
<li>{md("Klook：今次冇 surface 到具體 Doha 沙漠團 listing，") + pill("未核實", "unv")}</li>
</ul>""" + note(md("**兩個人玩私人團性價比特別高**：好多產品係「per vehicle」計價，5 人同 2 人同價。"))))

inner.append(kill(md("**過夜沙漠營：剔走。** 27/9 夜你哋要返 Al Wakrah 酒店，28/9 朝要退房趕機。")))
P.append(section("SECTION 1", "沙漠／內海 4x4", "Khor Al Adaid · 你哋最抵玩嘅品類", "doha_inlandsea", "".join(inner)))

# =====================================================================
# 2 市內導覽團
# =====================================================================
inner = []
inner.append(figure("doha_corniche", "42mm"))
inner.append(block("🚌 Hop-on Hop-off 巴士（Doha Bus）", f"""
<ul class="tight">
<li>{md("**24 小時票約 US$55**，一經啟用 24 小時內無限次搭，車上多語言語音導覽，**送一次 1 小時夜遊**。")}</li>
<li>{md("站點包括 Souq Waqif、Katara、The Pearl、NMoQ、MIA、機場、Corniche、Falcon Souq、Inland Sea、Zekreet 等 20+ 站。")}</li>
<li>{md("班次頻率 ") + pill("未核實", "unv") + md("（官網 dohabus.com 抓唔到內容）。")}</li>
</ul>""" + kill(md("**❌ 唔建議。** 站點**冇一個喺 Al Wakrah**，要先花 25 分鐘車入市區先上到車；"
                   "27/9 你哋只得下午自由，24 小時票浪費一半。**Grab / Careem 點對點反而平又快**，"
                   "或者 Doha Metro 紅線由 Al Wakra 站直達 Souq Waqif／Msheireb。"))))

inner.append(block("🚐 私人／半日城市團", tbl(["產品", "細節"], [
    [md("**Discover Doha**（Discover Qatar 官方）"),
     md("3 小時，**QAR 115**。集合：Souq Waqif（Fanar Mosque 對面）或 Doha Sands Beach，提早 15 分鐘。"
        "**只限星期二、五、六出團 → 27/9 係星期日，做唔到。**")],
    ["Doha Guided City Tour with Hotel AND Airport Pickup（GetYourGuide）",
     md("有酒店＋機場接送版本 —— **呢個係少數可能覆蓋 Al Wakrah 嘅**")],
    ["Viator 私人 Doha City Tour + MIA", "私人導遊、可揀停點"],
    ["Doha Full or Half Day Tour with MIA（GYG）", "半日或全日，含 MIA"],
    ["MIA + Souq Waqif + Inland Sea 組合（GYG）", "一次過打包三個點"],
], [None, None])))

inner.append(block("🚶 步行團 · 📷 攝影團", f"""
<ul class="tight">
<li>{md("Half-Day Guided Souq Waqif Walking Tour（Viator，4 小時）；Msheireb Downtown 團一覽（GYG）。")}</li>
<li>{md("**實話：9 月尾中午 38–40 度行步行團係自虐。** Souq Waqif 建議夜晚 19:00 之後自己行 —— 你哋原定計劃啱。")}</li>
<li>{md("攝影團：今次冇 surface 到有官方價目嘅 Doha photography tour，") + pill("未核實", "unv")
      + md("。可 WhatsApp 365 Adventures 問有冇 photo-focused 私人行程。")}</li>
</ul>"""))
P.append(section("SECTION 2", "市內導覽團", "巴士 · 私人團 · 步行團 · 攝影團", "doha_msheireb", "".join(inner)))

# =====================================================================
# 3 文化博物館
# =====================================================================
inner = []
inner.append(block("🕘 開放時間（qm.org.qa 官方，已核實）", tbl(
    ["博物館", "星期日 27/9", "星期一 28/9", "閉館日"],
    [[md("**National Museum of Qatar（NMoQ）**"), md("**09:00–19:00** ✅"), "09:00–19:00", md("**星期二**")],
     [md("**Museum of Islamic Art（MIA）**"), md("**09:00–19:00** ✅"), md("**09:00–19:00** ✅"), md("**星期三**")]],
    [None, None, None, "t"])
    + note(md("兩間 27/9（日）同 28/9（一）都開，冇伏。**Jiwan 就喺 NMoQ 入面**，13:00 lunch 完全喺開放時間內。"))))

inner.append(block("🎫 門票", tbl(["項目", "價錢", "備註"], [
    ["NMoQ", md("**QAR 25**"), md("因部分維修半價；GetYourGuide 約 €11 / 人。") + pill("未核實", "unv") + md(" 官網 qm.org.qa 要去 /tickets 買飛先見到價")],
    ["MIA", md("**QAR 50**"), md("非居民成人。有其他來源話 QAR 100，有出入。16 歲以下同持 QID 居民免費。") + pill("未核實", "unv")],
    ["Msheireb Museums", md("**免費**"), "4 幢歷史大宅，冷氣足"],
    ["Qatar Museums Pass / Discover One Pass", pill("未核實", "unv"), "價錢同涵蓋範圍未查到"],
], [None, "n", None])))

inner.append(strip_imgs(["doha_mia", "doha_nmoq", "doha_katara", "doha_library"]))

inner.append(block("🎧 官方導賞團 — 我嘅建議：唔使買", f"""
<ul class="tight">
<li>{md("Qatar Museums 官方 Plan Your Visit 頁**冇列出**導賞團時間或價錢（已核實：頁面確實冇）。MIA 有主題免費導賞團，但**時間表未核實**。")}</li>
<li>{md("Discover Qatar 有官方博物館產品（Discover the NMoQ / Discover the MIA）；第三方私人 MIA 導賞約 4 小時、包來回接送、門票自費、逢星期二除外。")}</li>
</ul>""" + note(md("**NMoQ 同 MIA 都唔需要買導賞團。** 兩間都有極好嘅館內標示同免費 audio guide app，"
                  "NMoQ 更加係 360 度沉浸影院為主，導賞員反而阻你節奏。**買門票入去自己行，慳返嚟食好啲。**"))))

inner.append(block("🏛 Katara / Qatar National Library", f"""
<ul class="tight">
<li>{md("**Katara Cultural Village：免費開放**，多數城市團都包。")}</li>
<li>{md("**Qatar National Library：免費入場。** 建築導賞官方 booking 頁搵唔到，") + pill("未核實", "unv")
      + md("；自己入去睇 Rem Koolhaas 嘅書架式建築就夠。")}</li>
</ul>"""))
P.append(section("SECTION 3", "文化博物館體驗", "NMoQ · MIA · Msheireb · Katara · QNL", "doha_library", "".join(inner)))

# =====================================================================
# 4 水上活動
# =====================================================================
inner = []
inner.append(block("⛵ Discover Dhow Sunset Cruise — 最啱你哋", tbl(["項目", "詳情"], [
    ["<b>時長</b>", "2 小時"],
    ["<b>時間</b>", md("**3–9 月 17:00–19:00**（10–2 月 16:00–18:00）→ **27/9 適用**")],
    ["<b>價錢</b>", md("約 **QAR 150**（5 歲以下免費）")],
    ["<b>集合點</b>", md("**Box Park / Old Doha Port 區 Marina Gate 3** dhow parking 嘅 National Cruise Office（綠色貨櫃），**提早 15 分鐘到**")],
    ["<b>必帶</b>", md("**QID 或護照正本**（有身份查核）")],
    ["<b>包</b>", "冷熱飲（樽裝水、咖啡、茶）"],
    ["<b>航線</b>", "Box Park → Corniche → Katara → The Pearl → 返 Box Park"],
], ["t", None])
    + warn(md("⚠️ **呢個係喺 Old Doha Port 上船，唔係 Corniche 中段。** 你哋原本寫「Corniche dhow」要改成 **Box Park 集合**。"
              "**冇酒店接送**，自己 Grab 過去。"))
    + note(md("其他 dhow：Viator 由 **US$23** 起；Dhow Cruise + Corniche Walk（2 小時）；含晚餐版本；"
              "Tiffan Tours 3 小時日落 dhow 含晚餐。最平係 Corniche 舊港自己上嘅基本 dhow 約 QAR 30 " ) + pill("未核實", "unv"))))

inner.append(figure("doha_dhow", "42mm"))
inner.append(block("🏝 Banana Island / Al Safliya", f"""
<ul class="tight">
<li>{md("**Banana Island Resort Doha by Anantara day pass：成人約 QAR 350–395**（12 歲以上）。**只能坐船去**，渡輪由 Corniche 上 Anantara 私人 Al Shyoukh Terminal 開出（近 MIA）。")}</li>
<li>{md("Al Safliya Island 快艇團：約 **US$118–175 / 成人** ") + pill("未核實", "unv")}</li>
</ul>""" + kill(md("**❌ 剔走。** Banana Island 係整日活動，27/9 撞 Jiwan lunch，28/9 冇時間。"))))

inner.append(block("🛶 Purple Island 紅樹林獨木舟（Al Khor）", f"""
<ul class="tight">
<li>{md("**AquaSports Mangrove Kayaking Camp：QAR 200 / 成人**（12 歲以下 QAR 100、7 歲以下 QAR 50），**現金到場付**。約 90 分鐘，**提早 30 分鐘到**，行 Al Khor Coastal Highway。")}</li>
<li>{md("GetYourGuide 2 小時由 **US$60** 起；Viator 4 小時私人 **US$149（減至 119）**；Nomad 6 小時 Al Khor + kayak。")}</li>
</ul>""" + kill(md("**❌❌ 完全唔得。** Al Khor 喺多哈**以北 50 km**，你哋喺**以南 16 km** —— 單程車程約 **1 小時 15 分**。"
                   "加上 9 月尾划艇曬到爆。剔走。"))))

inner.append(block("🤿 潛水／浮潛", note(md("今次冇 surface 到有官方 2025–26 價目嘅 Doha diving operator，") + pill("未核實", "unv")
    + md("。9 月尾水溫約 **33–34°C**，能見度一般，**唔值得為佢改行程**。"))))
P.append(section("SECTION 4", "水上活動", "Dhow 日落遊船 · 離島 · 紅樹林 · 潛水", "doha_pearl", "".join(inner)))

# =====================================================================
# 5 Al Wakrah 門口
# =====================================================================
inner = []
inner.append(block("🚶 你哋酒店門口就有嘢玩", tbl(["選項", "細節"], [
    [md("**Souq Al Wakra（步行）**"),
     md("**就喺你哋酒店隔離** —— Souq Al Wakra Hotel by Tivoli 本身就係建喺重建嘅 souq 入面。傳統攤檔、工藝、香料、布藝、街頭小食，"
        "加 Al Wakra Corniche 海邊散步。**免費、自己行就得。**")],
    ["Doha & Al Wakra Souq Tour（Doha Magic Adventures）",
     md("包 Al Wakra Souq、本地商店、街頭小食、Al Wakra Corniche，再加 MIA 或 Souq Waqif。**價錢／時長未核實。**")],
    [md("**Al Majles Resort – Sealine Day Pass**"),
     md("沙灘度假村，距 Sealine 沙漠入口 15 分鐘。日票包沙灘排球／足球、乒乓、沙板、sand slider、更衣室、室內 lounge 同餐廳。**價錢未核實。**")],
    ["Sealine / Al Wakrah 區 tour 一覽", "GetYourGuide 有 Al Wakrah、Sealine、Sealine Beach Resort 三個地區頁"],
    [md("沙漠 safari 含 **Souq Al Wakrah BBQ**"),
     md("Viator 有產品直接喺 Souq Al Wakrah 傳統市集食 BBQ —— **對住 Al Wakrah 嘅你哋特別順路**")],
], [None, None])))

inner.append(strip_imgs(["doha_wakra", "doha_dunes", "doha_falcon"]))
inner.append(warn(md("**酒店同 Al Wakrah 係禁酒區**（無酒精）—— 你哋都唔飲，唔構成問題。"
                     "但要注意：**Souq Al Wakra 一帶夜晚冇酒吧，夜生活全部要返市區。**")))
P.append(section("SECTION 5", "Al Wakrah 附近", "行出酒店門口就係景點", "doha_wakra", "".join(inner)))

# =====================================================================
# 6 Qatar Airways 中轉／Stopover
# =====================================================================
inner = []
inner.append(block("✈️ Qatar Stopover（+Qatar）", f"""
<ul class="tight">
<li>{md("**資格：卡塔爾航空／代碼共享／oneworld 確認機票持有人，多哈轉機最少 12 小時**，可停留 12–96 小時。")}</li>
<li>{md("價錢：Standard（4 星）由 **US$14** 起；Premium（5 星）由 **US$24** 起；Premium with Beach Access 由 **US$31** 起；Luxury 由 **US$83** 起。")}</li>
</ul>""" + kill(md("**❌ 你哋用唔到。** Stopover 係**同機票一齊或經 Qatar Airways Holidays 加購嘅酒店套票**，"
                   "而你哋已經自己訂咗 Souq Al Wakra Hotel；Stopover 酒店名單係指定嘅市區／The Pearl 酒店，唔會包你哋間。"))
    + note(md("**如果仲未出票**，理論上可以考慮改用 Stopover 套票（US$14 一晚 4 星真係平到離譜），"
              "但咁樣要放棄 Al Wakrah 呢間。**呢個係你哋自己決定嘅 trade-off，唔係 tour 問題。**"))))

inner.append(block("🎫 Transit Tours（Discover Qatar）— Transit Exclusive: Discover Doha", tbl(["項目", "詳情"], [
    ["<b>時長</b>", "3 小時"],
    ["<b>出發</b>", md("每日 **08:00 / 12:00 / 14:00 / 15:00 / 16:00 / 18:00 / 19:00 / 20:00**")],
    ["<b>價錢</b>", md("**QAR 115 / 人**（以一架車 5 人計）")],
    ["<b>最低轉機</b>", md("前後航班相距 **6 小時**")],
    ["<b>集合</b>", md("**Hamad International Airport Duty Free Plaza South** 嘅 Discover Qatar Transit Tour 櫃枱，出發前 90 分鐘到")],
    ["<b>規則</b>", md("轉機 6 小時以上 → 可參加 city tour 或內海沙漠團；3–6 小時 → 只有機場內按摩。"
                      "要預 90 分鐘過關 + 完團後 60 分鐘登機；必須喺下一班機起飛前 **2 小時** 送返機場。"
                      "唔符免簽嘅可喺櫃枱辦 **QAR 100** 過境簽。")],
], ["t", None])))

inner.append(kill(md("""<b>❌ 對你哋嘅判斷：用唔到。</b>
<ul class="tight">
<li>呢啲團<b>全部喺機場櫃枱集合</b>，設計上係畀「未離開機場、兩班機之間」嘅乘客。你哋 26/9 已經正式入境、住喺酒店。</li>
<li>28/9 航班 15:30。3 小時團最早 08:00 出發、11:00 完 —— 但你哋要 <b>07:00 前由 Al Wakrah 出發去機場</b>，然後 11:00 完團仲要返 Al Wakrah 12:00 退房再返機場。荒謬。</li>
<li>就算放棄退房、拖住行李去機場，<b>資格條款係按「layover」計，唔係按「今日有無時間」計</b> —— 你哋唔係 layover 乘客。</li>
<li>同樣嘅 3 小時城市團，Discover Qatar 普通市場版 “Discover Doha” 都係 <b>QAR 115</b>，冇平過，而且唔使去機場集合。</li>
</ul>
<b>簡單講：第 6 節呢一整類，剔走就得。慳返研究時間。</b>""")))
P.append(section("SECTION 6", "Qatar Airways 中轉／Stopover", "睇落吸引，但你哋唔符合資格", "doha_skyline", "".join(inner)))

# =====================================================================
# 7 特別體驗
# =====================================================================
inner = []
inner.append(block("⭐ 特別體驗逐個睇", tbl(["項目", "狀況", "判斷"], [
    [md("**駱駝賽 Al Shahaniya**"),
     md("2026–27 賽季 **9 月 7 日開鑼**，首階段 12 場晨賽**做到 9 月 18 日**；之後**要等 10 月至 2 月每逢星期五**先有正式賽事，Emir 主賽喺 3–4 月"),
     pill("❌ 剔走", "no") + md("<br>9 月 27–28 日正好喺兩段賽期**中間嘅空窗**。去到大機會得個訓練跑")],
    [md("**獵鷹 Falcon Souq + Falcon Hospital**"),
     md("Falcon Souq 平日 **09:00–13:00 及 16:00–20:00**，星期五只開晚市。Falcon Hospital 就喺隔離，**9 月至 1 月係旺季，每日醫治多達 150 隻鳥**，靜嘅時候有禮貌問，職員通常樂意帶你參觀"),
     pill("✅ 去", "yes") + md("<br>**免費、順路、啱晒。**27/9 夜去 Souq Waqif 食飯前 19:00–20:00 順手行埋")],
    [md("**Zekreet / Richard Serra 雕塑 / 蘑菇岩 / Film City**"),
     md("通常同 Al Shahaniya 賽道、Zekreet Beach 打包做西岸全日團。**Richard Serra 場地收 QAR 50 / 人**；Desert Track 嘅 Qatar West Tour 約 US$170 / 成人 ") + pill("未核實", "unv"),
     pill("❌ 剔走", "no") + md("<br>全日團 8–10 小時，西北岸單程 1.5 小時。27/9 撞 lunch，28/9 冇可能")],
    [md("**Al Zubarah Fort（UNESCO）**"),
     md("喺卡塔爾**西北角**，單程約 1.5–2 小時。搵唔到 2026 官方團價 ") + pill("未核實", "unv"),
     pill("❌ 剔走", "no") + md("<br>同上，做唔到")],
    [md("**直升機／熱氣球**"),
     md("有網站列出 Doha 直升機觀光，但**搵唔到具體 operator、出發時間同官方價錢 —— 全部未核實**"),
     pill("❌ 唔建議", "no") + md("<br>資料太薄，唔好喺陌生地方訂查唔到底細嘅飛行產品")],
    [md("**Lusail 賽道 / F1**"), md("2026 Qatar GP 係 **11 月 27–29 日**"),
     pill("❌ 唔關事", "no") + md("<br>9 月冇賽事")],
], [None, None, None])))
inner.append(strip_imgs(["doha_camel", "doha_falcon", "doha_zekreet", "doha_zubarah"]))
P.append(section("SECTION 7", "特別體驗", "駱駝賽 · 獵鷹 · 西岸 · 空中", "doha_zekreet", "".join(inner)))

# =====================================================================
# 8 唔使畀錢就得
# =====================================================================
inner = []
inner.append(block("🆓 呢啲喺 9 月尾買導賞團係倒錢落海", tbl(["地方", "點解自己去就夠"], [
    [md("**Souq Waqif**"), md("免費、24 小時開放式街區、夜晚最舒服。導賞團收你 4 個鐘錢去行一個你自己行得晒嘅市集。**Grab 過去，19:30 開始行。**")],
    [md("**Falcon Souq + Falcon Hospital**"), "免費，就喺 Souq Waqif 入面"],
    [md("**Souq Al Wakra + Al Wakra Corniche**"), md("**你哋酒店門口。** 零成本")],
    [md("**Msheireb Museums**"), md("**免費入場**，四幢歷史大宅，冷氣足")],
    [md("**Katara Cultural Village**"), "免費開放"],
    [md("**Qatar National Library**"), "免費入場，Rem Koolhaas 建築本身就係展品"],
    [md("**Doha Corniche 散步**"), md("免費。但 9 月尾**只有日落後行得**")],
    [md("**Khor Al Adaid 內海保護區入場**"), md("**免費、冇 permit 費**。你畀嘅錢係畀架 4x4 同司機，唔係門票")],
    [md("**NMoQ / MIA 館內導賞**"), md("館內標示同 app audio guide 都做得好好，NMoQ 主打沉浸式影院。**買門票入去自己行**")],
], [None, None])))
inner.append(note(md("**慳錢替代交通：** Grab / Careem / Uber 喺多哈都有；**Doha Metro 紅線由 Al Wakra 站直達市區**"
                     "（Souq Waqif 站、Msheireb 站），比 hop-on hop-off 巴士快又平好多。"
                     "（Metro 班次／票價 ") + pill("未核實", "unv") + md("，到埗用 Qatar Rail app 查。）")))
inner.append(strip_imgs(["doha_souq", "doha_msheireb", "doha_katara", "doha_corniche"]))
P.append(section("SECTION 8", "唔使畀錢就得", "免費、自己去更好嘅地方", "doha_souq", "".join(inner)))

# =====================================================================
# 27/9 方案
# =====================================================================
inner = []
inner.append(note(md("前提：**13:00 Jiwan @ NMoQ 係死約**。多哈 9 月尾日落約 17:40–17:50 ") + pill("未核實", "unv") + md("，到埗確認。")))
inner.append(block("方案 A（推薦）— 日出沙漠 + 午睡 + 博物館 + dhow", timeline([
    ("03:15", "酒店 lobby 等車 — 訂 **Discover Sunrise in the Desert**，QAR 320", 0),
    ("03:30–09:30", "**沙漠日出 6 小時私人團**，Outpost Al Barari 沙漠營早餐　⚠️訂之前必須確認 Al Wakrah 接送", 1),
    ("09:45–12:00", "返酒店，沖涼、瞓返覺 — 呢段係全日最熱嘅時候，留喺室內", 0),
    ("12:15", "出發去 NMoQ（約 20–25 分鐘車程，Grab）", 0),
    ("13:00–14:30", "**Jiwan lunch @ NMoQ** — 死約", 1),
    ("14:30–16:30", "**NMoQ 展館**（食完飯直接上去，唔使再搭車）· 開到 19:00", 0),
    ("16:40", "Grab 去 **Box Park / Old Doha Port Marina Gate 3**（NMoQ 去 Box Park 好近）", 0),
    ("16:45", "喺 **National Cruise Office**（綠色貨櫃）報到 — **提早 15 分鐘，帶護照正本**", 1),
    ("17:00–19:00", "**Discover Dhow Sunset Cruise**，約 QAR 150 · Corniche → Katara → The Pearl", 0),
    ("19:15", "Grab 去 Souq Waqif", 0),
    ("19:30–20:00", "**Falcon Souq**（開到 20:00）+ Falcon Hospital 望一望 — 免費", 0),
    ("20:00–21:30", "Souq Waqif 晚餐", 0),
    ("22:00", "返 Al Wakrah", 0),
]) + warn(md("**方案 A 剔走咗 MIA** —— 塞唔落，MIA 移去 28/9 朝。"
             "<br>**總開支（2 人）：** 沙漠 QAR 320 + dhow QAR 300 + NMoQ 門票 2×QAR 25 ≈ **QAR 670**（約 US$184），未計車費同餐飲。"))))

inner.append(block("方案 B — 唔想 03:15 起身", timeline([
    ("09:30", "出發", 0),
    ("10:00–12:30", "**MIA**（09:00 開門）", 0),
    ("13:00", "**Jiwan lunch @ NMoQ**", 1),
    ("14:30–16:30", "NMoQ 展館", 0),
    ("17:00–19:00", "Dhow 日落遊船", 0),
    ("19:30", "Souq Waqif", 0),
]) + note(md("**沙漠改喺 28/9 朝做** —— 但見下頁選項 3 嘅風險警告。"
             "<br>**老實講：03:15 起身玩 6 個鐘沙漠，跟住 40 度日頭再撐到夜晚 10 點，係好攞命嘅一日。**"
             "兩位如果唔係鐵人體質，我會推方案 B。"))))
P.append(section("27 SEP · SUNDAY", "27/9 建議行程", "方案 A vs 方案 B", "doha_dhow", "".join(inner)))

# =====================================================================
# 28/9 + 唔值得去 + 死線
# =====================================================================
inner = []
inner.append(note(md("可用窗口：**08:00–11:30**。12:00 退房，14:30 行李櫃枱閂。"
                     "Al Wakrah ↔ 市區單程 20–25 分鐘，Al Wakrah → 機場約 15–20 分鐘。")))
inner.append(block("選項 1（最穩陣，推薦）— MIA 早場", timeline([
    ("07:30", "酒店早餐，執好行李", 0),
    ("08:20", "Grab 出 MIA（約 20 分鐘）", 0),
    ("09:00–10:45", "**MIA 開門即入**（星期一 09:00–19:00，已核實）· 門票約 QAR 50 / 人", 1),
    ("11:00–11:30", "返酒店", 0),
    ("12:00", "退房", 0),
    ("12:30", "出發去機場", 0),
    ("13:00", "到 DOH，過關、食嘢", 0),
    ("14:30", "**行李櫃枱閂**", 1),
    ("15:30", "**QR253 → TBS**", 1),
]) + note(md("**風險低**，MIA 係全日最舒服嘅室內景點，早場冇人。"))))

inner.append(f"""<div class="two">
<div>{block("選項 2（零風險、零成本）— 酒店門口", f'''
<ul class="tight">
<li>{md("08:00–09:30 行 **Souq Al Wakra + Al Wakra Corniche**（就喺酒店外面），影相、食早餐咖啡")}</li>
<li>{md("09:30–11:30 返房間嘆冷氣 / 酒店泳池")}</li>
<li>{md("12:00 退房，從容去機場")}</li>
</ul>''' + warn(md("**Souq Al Wakra 大部分店舖朝早未必全開**（多數 souq 商戶 09–10 點先開）") + pill("未核實", "unv") + md("，可以問酒店 concierge。")))}</div>
<div>{block("選項 3（有 upside 但有風險）— 沙漠團塞喺 28/9", f'''
<ul class="tight">
<li>{md("03:30–09:30 沙漠日出團，09:30 返到酒店")}</li>
<li>{md("10:00–11:30 沖涼執嘢 → 12:00 退房 → 13:00 到機場")}</li>
<li>{md("緩衝：團完到行李櫃枱閂差 **5 個鐘**，理論上夠")}</li>
</ul>''' + kill(md("**⚠️ 但我唔會做。** 出發當日玩一個 6 小時、要出到 Mesaieed 沙漠、全程冇你控制權嘅活動 —— "
                   "一爆胎／一塞車就係災難。**沙漠團要玩就喺 27/9 玩。**")))}</div>
</div>""")

inner.append(kill(md("""<b>❌ 28/9 唔好諗嘅</b>
<ul class="tight">
<li>任何半日團（4 小時起跳，08:00 開 12:00 完，撞退房）</li>
<li>Transit tour（要去機場櫃枱集合，見第 6 節）</li>
<li>NMoQ（27/9 食完 lunch 就已經喺度）</li>
<li>Purple Island / Zekreet / Al Zubarah（單程都唔止 3 個鐘）</li>
</ul>""")))
P.append(section("28 SEP · MONDAY", "28/9 朝建議", "三個選項，只有 3 個鐘可用", "doha_mia", "".join(inner)))

# =====================================================================
# 唔值得去 + 訂位死線
# =====================================================================
inner = []
inner.append(block("🚫 唔值得去嘅（11 項）", tbl(["#", "項目", "點解剔走"], [
    ["1", md("**Hop-on Hop-off 巴士 24 小時票**（約 US$55）"), "冇一個站喺 Al Wakrah，27/9 只得半日自由，Metro 紅線 + Grab 快又平好多"],
    ["2", md("**Qatar Airways Transit Tour / Discover Relaxation**"), "已入境住酒店，唔係 layover 乘客；同樣 3 小時城市團市場版都係 QAR 115"],
    ["3", md("**Qatar Stopover 套票**"), "要最少 12 小時轉機 + 同機票一齊訂酒店，你哋已自己訂咗 Al Wakrah"],
    ["4", md("**Purple Island 紅樹林獨木舟**"), "方向完全相反（北 50 km vs 你哋南 16 km），單程 1 小時 15 分，加 9 月尾曬"],
    ["5", md("**Zekreet / Richard Serra / Al Zubarah 西岸全日團**"), "8–10 小時，兩日都塞唔落"],
    ["6", md("**駱駝賽**"), "9 月 27–28 日正好喺賽期空窗（首階段 9/18 完，下一輪 10 月先開）"],
    ["7", md("**Banana Island day pass**（QAR 350–395）"), "整日活動，撞 Jiwan lunch"],
    ["8", md("**Souq Waqif / Msheireb 付費步行團**"), "免費開放區域，自己夜晚行更舒服"],
    ["9", md("**NMoQ / MIA 私人導賞團**"), "館內導覽已經好完整"],
    ["10", md("**直升機／熱氣球**"), "查唔到可靠 operator 同價錢"],
    ["11", md("**潛水／浮潛**"), "9 月尾水溫 33°C+，能見度一般，唔值得改行程"],
], ["t", None, None])))

inner.append(block("⏰ 訂位死線", tbl(["項目", "幾時訂", "點解"], [
    [md("**沙漠日出團**（Discover Qatar 或 OTA）"), md("**出發前 2–3 星期**；最遲 **48 小時前**"),
     md("日出團私人車位少，9 月尾係旺季頭。**行 OTA 買多數有 24 小時前免費取消 —— 早訂零風險**")],
    [md("**Al Wakrah 接送確認**"), md("**落單同一日**"),
     md("email info@discoverqatar.qa 或打 **+974 4144 5150**。官網只寫 “within Doha city limits” —— **呢個係整個計劃最大嘅單一風險點**")],
    [md("**Discover Dhow Sunset Cruise**"), md("**2–5 日前**，最遲前一日"), "QAR 150 / 2 小時，17:00 場星期日會滿。要帶護照正本"],
    [md("**Jiwan @ NMoQ**"), pill("已訂 ✅", "yes"), "建議出發前 3 日再打去 reconfirm"],
    [md("**NMoQ / MIA 門票**"), "網上預先買或現場買", "qm.org.qa/tickets。NMoQ 半價 QAR 25、MIA 約 QAR 50"],
    [md("**私人城市團**（如果要）"), "3–5 日前", "OTA 24 小時免費取消"],
    [md("**Grab / Careem**"), "落機後即刻裝 app", "Al Wakrah 唔係市中心，夜晚等車可能要 10–15 分鐘"],
], [None, "t", None])))
inner.append(warn(md("**最重要嘅一句：先打 +974 4144 5150 問 Al Wakrah 接送，再落沙漠團單。**")))
P.append(section("DECISIONS", "唔值得去 · 訂位死線", "剔走咩、幾時落單", "doha_camel", "".join(inner)))

# =====================================================================
# 已核實／未核實
# =====================================================================
VERIFIED = [
    "NMoQ / MIA 開放時間（qm.org.qa 官方）：兩間 27/9 同 28/9 都開 09:00–19:00；NMoQ 逢二休、MIA 逢三休",
    "Discover Sunrise in the Desert：6 小時、4–9 月 03:30–09:30、QAR 320、私人 4x4、Outpost Al Barari 早餐",
    "Discover the Desert and Inland Sea（私人）：4 小時、09:00–13:00 / 14:00–18:00、QAR 227 每架車（最多 5 人）",
    "Discover Doha 市內團：3 小時、QAR 115、只限星期二五六 → 27/9 星期日做唔到",
    "Discover Dhow Sunset Cruise：2 小時、3–9 月 17:00–19:00、約 QAR 150、Box Park / Old Doha Port Marina Gate 3 集合、要護照正本",
    "Transit Exclusive – Discover Doha：3 小時、QAR 115/人、8 個出發時段、機場 Duty Free Plaza South 集合、需 6 小時轉機",
    "Qatar Stopover：需最少 12 小時轉機、Standard 由 US$14 起",
    "Khor Al Adaid 內海保護區入場免費、冇 permit 費",
    "Msheireb Museums 免費入場；Katara 同 Qatar National Library 免費",
    "駱駝賽 2026–27 賽季 9/7 開鑼、首階段做到 9/18、下一輪 10 月至 2 月逢星期五",
    "Falcon Souq 平日 09:00–13:00 及 16:00–20:00；Falcon Hospital 9 月至 1 月旺季",
    "Richard Serra 雕塑場地收 QAR 50 / 人",
    "AquaSports Purple Island kayak：QAR 200 / 成人、現金付、約 90 分鐘",
    "Banana Island day pass 成人約 QAR 350–395，只能坐船去",
    "2026 Qatar GP 係 11 月 27–29 日",
]
UNVERIFIED = [
    "Discover Qatar 全部產品嘅取消政策 — 官網根本冇公佈",
    "Discover Qatar 肯唔肯去 Al Wakrah 接客、加唔加錢（最大風險點）",
    "NMoQ 門票 QAR 25（維修半價）— 要去 qm.org.qa/tickets 先見到",
    "MIA 門票 QAR 50 — 有來源話 QAR 100，有出入",
    "Qatar Museums Pass / Discover One Pass 價錢同涵蓋範圍",
    "MIA 免費主題導賞團時間表",
    "Qatar National Library 建築導賞有冇官方 booking",
    "Doha Bus 班次頻率（官網抓唔到）",
    "365 Adventures、Inland Sea Tours、Doha Adventure Tours、Golden Adventures 嘅價目",
    "Arabian Adventures / Qatar Inbound Tours / Falcon Tours / Gulf Adventures 2025–26 官方價",
    "Klook 有冇 Doha 沙漠團 listing",
    "Doha 攝影團 operator 同價錢",
    "Corniche 舊港自己上嘅基本 dhow 約 QAR 30",
    "Al Safliya Island 快艇團 US$118–175",
    "Al Majles Resort Sealine day pass 價錢",
    "Doha Magic Adventures 嘅 Al Wakra Souq 團價錢／時長",
    "Desert Track Tourism Qatar West Tour US$170",
    "Al Zubarah 2026 官方團價",
    "直升機／熱氣球 operator、時間、價錢",
    "多哈 9 月尾日落時間 17:40–17:50",
    "Souq Al Wakra 商戶朝早幾點開",
    "Doha Metro 班次／票價",
]
inner = [f"""<div class="two">
<div>{block("✅ 已核實（有官方或一手來源）",
    '<ul class="tight">' + "".join(f"<li>{md(x)}</li>" for x in VERIFIED) + "</ul>")}</div>
<div>{block("⚠️ 未核實（唔好當真，要自己再查）",
    '<ul class="tight">' + "".join(f"<li>{md(x)}</li>" for x in UNVERIFIED) + "</ul>")}</div>
</div>"""]
inner.append(warn(md("凡標 **未核實** 嘅價錢同時間，落單前一定要自己再 open 一次官方連結對一次 —— "
                     "原始 markdown（檔案 24）入面每一項都有 source link。")))
P.append(section("SOURCES", "已核實／未核實", "邊啲可以信、邊啲要自己再查", "doha_katara", "".join(inner)))

# =====================================================================
# 相片來源
# =====================================================================
cells = []
for k in sorted(CRED):
    if not has(k): continue
    c = CRED[k]
    src = c.get("landing") or c.get("file") or ""
    cells.append(f'<div class="k"><img src="{path(k)}"><b>{e(cap(k))}</b>'
                 f'{e(credit(k))}<div class="u">{e(src)}</div></div>')
inner = [note(md("所有相片均為 **Creative Commons** 授權嘅真實相片（Flickr 經 Openverse／Wikimedia Commons），"
                 "作者同授權條款如下；本 PDF 只作私人旅行用途。")),
         '<div style="height:3mm"></div>',
         f'<div class="credits">{"".join(cells)}</div>']
P.append(section("CREDITS", "相片來源", "Creative Commons · 18 張", "doha_pearl", "".join(inner)))

# =====================================================================
HTML = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>多哈 Local Tour 完整選項</title><style>{CSS}</style></head><body>{''.join(P)}</body></html>"""
out = os.path.join(HERE, "doha.html")
open(out, "w", encoding="utf-8").write(HTML)
print("HTML written:", out, len(HTML), "chars,", len(P), "pages")
