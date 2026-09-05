# -*- coding: utf-8 -*-
"""Photo assets for the itinerary PDF.

All photos are real, Creative-Commons-licensed images sourced via Openverse
(Flickr) and Wikimedia Commons. Attribution for every image is listed on the
final "相片來源" page, generated from img/credits.json.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "img")
CREDITS = json.load(open(os.path.join(IMG_DIR, "credits.json"), encoding="utf-8"))

def path(key):
    return "file://" + os.path.join(IMG_DIR, key + ".jpg")

def thumb(key):
    return "file://" + os.path.join(IMG_DIR, "t", key + ".jpg")

def has(key):
    return key in CREDITS and os.path.exists(os.path.join(IMG_DIR, key + ".jpg"))

def credit(key):
    c = CREDITS.get(key, {})
    a = (c.get("artist") or "").strip()
    return f'{a} · {c.get("license","")}'.strip(" ·")

# Chinese caption for every photo key
CAPTION = {
    "kl_petronas": "雙子塔 Petronas Twin Towers · 吉隆坡",
    "kl_batu": "黑風洞 Batu Caves · 吉隆坡",
    "kl_iamm": "伊斯蘭藝術博物館 IAMM · 吉隆坡",
    "doha_mia": "伊斯蘭藝術博物館 MIA · 多哈",
    "doha_nmoq": "卡塔爾國家博物館「沙漠玫瑰」· 多哈",
    "doha_souq": "Souq Waqif 老市集 · 多哈",
    "doha_wakra": "Al Wakra 海濱老市集 · 多哈",
    "ge_tbilisi": "第比利斯老城 · Narikala 城堡望落去",
    "ge_abanotubani": "Abanotubani 硫磺浴區 · 第比利斯",
    "ge_fabrika": "Fabrika · 第比利斯 Chugureti",
    "ge_jvari": "Jvari 修道院 · Mtskheta",
    "ge_svetitskhoveli": "Svetitskhoveli 大教堂 · Mtskheta",
    "ge_ananuri": "Ananuri 城堡 · 軍事公路",
    "ge_gergeti": "Gergeti 三一教堂 + Kazbek 山",
    "ge_kazbek": "Kazbek 山（5,054m）",
    "ge_truso": "Truso 山谷",
    "ge_dariali": "Dariali 峽谷 · 近俄邊境",
    "ge_kakheti": "卡赫季 Kakheti 葡萄園",
    "ge_tsinandali": "Tsinandali 莊園 · 卡赫季",
    "ge_gori": "史太林博物館 · Gori",
    "ge_uplistsikhe": "Uplistsikhe 岩洞古城",
    "ge_bagrati": "Bagrati 大教堂 · 庫塔伊西",
    "ge_gelati": "Gelati 修道院（UNESCO）",
    "ge_katskhi": "Katskhi 石柱",
    "ge_chiatura": "Chiatura 蘇聯纜車",
    "ge_enguri": "Enguri 水壩（751m 拱壩）",
    "ge_mestia": "Mestia 斯凡塔樓",
    "ge_ushguli": "Ushguli · 歐洲最高常住村",
    "ge_shkhara": "Shkhara 山（5,193m）· 格魯吉亞最高峰",
    "ge_zagari": "Zagari 山口（2,620m）",
    "am_haghpat": "Haghpat 修道院（UNESCO）· Debed 峽谷",
    "am_sanahin": "Sanahin 修道院（UNESCO）",
    "am_republic": "共和國廣場 · 耶烈萬",
    "am_cascade": "Cascade 階梯 · 耶烈萬",
    "am_matenadaran": "Matenadaran 古手稿館 · 耶烈萬",
    "am_garni": "Garni 神殿",
    "am_geghard": "Geghard 岩鑿修道院（UNESCO）",
    "am_khorvirap": "Khor Virap + Ararat 山",
}

COVER = "ge_gergeti"

# Day number -> hero photo
DAY_HERO = {
    "DAY 01": "kl_petronas",
    "DAY 02": "kl_iamm",
    "DAY 03": "doha_mia",
    "DAY 04": "doha_wakra",
    "DAY 05": "ge_ananuri",
    "DAY 06": "ge_kazbek",
    "DAY 07": "ge_kakheti",
    "DAY 08": "ge_uplistsikhe",
    "DAY 09": "ge_mestia",
    "DAY 10": "ge_ushguli",
    "DAY 11": "ge_zagari",
    "DAY 12": "ge_katskhi",
    "DAY 13": "am_haghpat",
    "DAY 14": "am_geghard",
    "DAY 15": "ge_tbilisi",
    "DAY 16": "ge_abanotubani",
    "DAY 17": "doha_nmoq",
}

# Day number -> extra photos shown as a small strip under the hero (sights of that day)
DAY_STRIP = {
    "DAY 02": ["kl_petronas", "kl_batu"],
    "DAY 03": ["doha_nmoq", "doha_souq"],
    "DAY 05": ["ge_jvari", "ge_svetitskhoveli", "ge_gergeti"],
    "DAY 06": ["ge_truso", "ge_dariali", "ge_gergeti"],
    "DAY 07": ["ge_tsinandali"],
    "DAY 08": ["ge_gori", "ge_bagrati"],
    "DAY 09": ["ge_gelati", "ge_enguri"],
    "DAY 10": ["ge_shkhara"],
    "DAY 11": ["ge_shkhara", "ge_ushguli"],
    "DAY 12": ["ge_chiatura", "ge_fabrika"],
    "DAY 13": ["am_sanahin"],
    "DAY 14": ["am_garni", "am_khorvirap", "am_republic", "am_cascade", "am_matenadaran"],
    "DAY 15": ["ge_abanotubani"],
    "DAY 16": ["ge_tbilisi"],
}

# Section title -> slim banner photo
SECTION_BANNER = {
    "訂單總覽": "am_republic",
    "座標總表": "ge_svetitskhoveli",
    "出發前 TO-DO": "ge_enguri",
    "預約清單": "ge_tsinandali",
    "實用資料": "am_cascade",
}

# Overview grid after the cover: (day label, date, place, photo)
OVERVIEW = [
    ("D1–2", "25–26/9", "吉隆坡", "kl_petronas"),
    ("D3–4", "27–28/9", "多哈", "doha_mia"),
    ("D5", "29/9", "軍事公路 → Kazbegi", "ge_ananuri"),
    ("D6", "30/9", "Kazbegi · Truso", "ge_gergeti"),
    ("D7", "1/10", "Gombori → 卡赫季酒莊", "ge_kakheti"),
    ("D8", "2/10", "Uplistsikhe → Kutaisi", "ge_uplistsikhe"),
    ("D9", "3/10", "Gelati → Mestia", "ge_mestia"),
    ("D10", "4/10", "Ushguli · Shkhara", "ge_ushguli"),
    ("D11", "5/10", "Zagari 山口 → Kutaisi", "ge_zagari"),
    ("D12", "6/10", "Katskhi → 第比利斯", "ge_katskhi"),
    ("D13", "7/10", "Debed 峽谷 → 耶烈萬", "am_haghpat"),
    ("D14", "8/10", "Garni · Geghard", "am_geghard"),
    ("D15–16", "9–10/10", "第比利斯", "ge_tbilisi"),
    ("D17", "11/10", "多哈 → 吉隆坡 → 香港", "doha_nmoq"),
]
