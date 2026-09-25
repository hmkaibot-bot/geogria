# -*- coding: utf-8 -*-
"""Fetch trip forecasts for every waypoint at the hour the itinerary passes it.

Sources: Open-Meteo (ECMWF IFS 0.25°, GFS, ICON, best_match; elevation-corrected),
Open-Meteo ECMWF ensemble (51 members, spread), MET Norway locationforecast.
Writes raw/*.json and summary.json next to this script.
Run: python3 tools/weather/fetch.py        (download + summarise)
     python3 tools/weather/fetch.py --offline  (re-summarise existing raw/ files)
"""
import calendar, json, pathlib, statistics, sys, time, urllib.parse, urllib.request
OFFLINE = "--offline" in sys.argv  # rebuild summary.json from raw/ without downloading

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw"; RAW.mkdir(exist_ok=True)
UA = {"User-Agent": "geogria-trip-planner/1.0 (personal trip weather)"}

# id, label, lat, lon, elevation m, moments [(YYYY-MM-DD, "HH", what)]
P = [
 ("hkg",   "香港機場 HKG",            22.308, 113.918,   10, [("2026-09-25","18","到機場 check-in"),("2026-09-25","21","CX733 起飛")]),
 ("kl",    "吉隆坡 KLCC",              3.158, 101.712,   60, [("2026-09-26","03","入住"),("2026-09-26","11","雙子塔"),("2026-09-26","15","IAMM／午後"),("2026-09-26","18","去 KLIA")]),
 ("dune",  "Sealine 沙丘",            24.913,  51.545,   20, [("2026-09-27","04","沙漠團出發"),("2026-09-27","05","日出 05:24"),("2026-09-27","08","離開沙漠")]),
 ("doha",  "多哈市區（MIA／Souq）",    25.295,  51.540,    5, [("2026-09-27","13","Jiwan 午餐"),("2026-09-27","17","Corniche 日落"),("2026-09-27","20","Souq Waqif"),("2026-09-28","09","Msheireb"),("2026-09-28","13","去機場")]),
 ("tbs",   "第比利斯機場 TBS",         41.669,  44.955,  480, [("2026-09-28","20","落機"),("2026-10-09","12","FlyOne 落機"),("2026-10-10","11","去機場")]),
 ("tbilisi","第比利斯市區",            41.700,  44.800,  450, [("2026-09-29","09","取車"),("2026-10-06","16","還車"),("2026-10-07","08","包車出發"),("2026-10-09","15","舊城／硫磺浴"),("2026-10-09","20","Barbarestan"),("2026-10-10","09","Dry Bridge")]),
 ("ananuri","Ananuri 城堡",            42.163,  44.703,  800, [("2026-09-29","11","Ananuri")]),
 ("gudauri","Gudauri",                 42.478,  44.478, 2190, [("2026-09-29","12","Gudauri 入油"),("2026-10-01","08","落山經過")]),
 ("jvari", "Jvari 山口",               42.515,  44.455, 2379, [("2026-09-29","13","過山口"),("2026-10-01","08","回程過山口")]),
 ("kazbegi","Stepantsminda（Kazbegi）",42.655,  44.648, 1740, [("2026-09-29","15","到酒店"),("2026-09-29","19","Maisi 晚餐"),("2026-09-30","19","晚餐"),("2026-10-01","07","出發")]),
 ("gergeti","Gergeti 聖三一教堂",       42.662,  44.620, 2170, [("2026-09-29","16","（可選）黃昏上 Gergeti"),("2026-09-30","07","黎明")]),
 ("truso", "Truso 山谷（Zakagori）",   42.612,  44.374, 2200, [("2026-09-30","11","Truso 碎石路"),("2026-09-30","13","Truso 折返")]),
 ("dariali","Dariali 峽谷",            42.735,  44.626, 1350, [("2026-09-30","15","Dariali")]),
 ("gombori","Gombori 山口",            41.864,  45.279, 1620, [("2026-10-01","12","過 Gombori"),("2026-10-02","08","回程過 Gombori")]),
 ("telavi","Kisiskhevi（Schuchmann）", 41.870,  45.520,  550, [("2026-10-01","14","check-in"),("2026-10-01","18","酒浴 SPA"),("2026-10-01","20","品酒晚餐")]),
 ("gori",  "Gori／Uplistsikhe",        41.975,  44.160,  600, [("2026-10-02","12","Gori／Uplistsikhe")]),
 ("kutaisi","Kutaisi",                 42.272,  42.707,  150, [("2026-10-02","18","到 Kutaisi"),("2026-10-02","19","Palaty"),("2026-10-03","09","Gelati"),("2026-10-05","16","到 Kutaisi"),("2026-10-06","08","出發")]),
 ("zugdidi","Zugdidi",                 42.509,  41.871,  110, [("2026-10-03","12","午餐＋入油")]),
 ("enguri","恩古里水壩",               42.763,  42.028,  520, [("2026-10-03","14","水壩")]),
 ("mestia","Mestia",                   43.045,  42.728, 1500, [("2026-10-03","17","到 Mestia"),("2026-10-03","21","夜晚"),("2026-10-04","09","出發")]),
 ("ushguli","Ushguli",                 42.915,  43.011, 2100, [("2026-10-04","13","到 Ushguli"),("2026-10-04","21","夜晚"),("2026-10-05","03","凌晨最凍"),("2026-10-05","08","出發前")]),
 ("shkhara","Shkhara 冰川路",          42.930,  43.040, 2250, [("2026-10-04","15","冰川谷")]),
 ("zagari","Zagari 山口",              42.860,  43.000, 2623, [("2026-10-05","06","清晨"),("2026-10-05","09","（建議）09:00 後"),("2026-10-05","10","過山口")]),
 ("lentekhi","Lentekhi",               42.789,  42.725,  750, [("2026-10-05","12","入油＋午餐")]),
 ("surami","Surami",                   42.025,  43.555,  750, [("2026-10-06","12","午餐")]),
 ("debed", "Debed 峽谷（Haghpat）",    41.092,  44.711, 1000, [("2026-10-07","12","修道院")]),
 ("yerevan","耶烈萬 Yerevan",          40.181,  44.515,  990, [("2026-10-07","19","到酒店"),("2026-10-08","19","Dolmama"),("2026-10-09","08","去機場")]),
 ("garni", "Garni／Geghard",           40.140,  44.780, 1500, [("2026-10-08","10","Geghard"),("2026-10-08","11","Garni")]),
]
HOURLY = ("temperature_2m,apparent_temperature,precipitation_probability,precipitation,rain,snowfall,"
          "weather_code,cloud_cover,wind_speed_10m,wind_gusts_10m,freezing_level_height,relative_humidity_2m")
DAILY = ("temperature_2m_max,temperature_2m_min,apparent_temperature_min,apparent_temperature_max,precipitation_sum,"
         "precipitation_probability_max,snowfall_sum,wind_gusts_10m_max,uv_index_max,sunrise,sunset,weather_code")
MODELS = "best_match,ecmwf_ifs025,gfs_seamless,icon_seamless"

def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.load(r)
        except Exception as ex:
            if i == tries - 1: raise
            time.sleep(3 * (i + 1))

def om(pt):
    pid, _, lat, lon, el, _ = pt
    q = dict(latitude=lat, longitude=lon, elevation=el, hourly=HOURLY, daily=DAILY, models=MODELS,
             timezone="auto", forecast_days=16, wind_speed_unit="kmh")
    return get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(q))

def ens(pt):
    pid, _, lat, lon, el, _ = pt
    q = dict(latitude=lat, longitude=lon, elevation=el, hourly="temperature_2m,precipitation,snowfall",
             models="ecmwf_ifs025", timezone="auto", forecast_days=15)
    return get("https://ensemble-api.open-meteo.com/v1/ensemble?" + urllib.parse.urlencode(q))

def metno(pt):
    pid, _, lat, lon, el, _ = pt
    return get(f"https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={lat}&lon={lon}&altitude={el}")

WMO = {0:"晴",1:"大致晴",2:"部分多雲",3:"密雲",45:"霧",48:"霧凇",51:"微毛毛雨",53:"毛毛雨",55:"大毛毛雨",
       61:"微雨",63:"雨",65:"大雨",66:"凍雨",67:"大凍雨",71:"微雪",73:"雪",75:"大雪",77:"雪粒",
       80:"驟雨",81:"較大驟雨",82:"猛烈驟雨",85:"陣雪",86:"大陣雪",95:"雷暴",96:"雷暴冰雹",99:"強雷暴冰雹"}

def pick(h, key, idx):
    v = h.get(key)
    return None if v is None or idx is None or idx >= len(v) else v[idx]

summary = {"fetched_utc": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(min(f.stat().st_mtime for f in RAW.glob("*_om.json")))) if OFFLINE else time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), "points": {}}
for pt in P:
    pid, label, lat, lon, el, moments = pt
    rec = {"label": label, "lat": lat, "lon": lon, "elev": el, "moments": [], "daily": {}}
    if OFFLINE:
        d = json.loads((RAW / f"{pid}_om.json").read_text())
        fe, fm = RAW / f"{pid}_ens.json", RAW / f"{pid}_metno.json"
        e_ = json.loads(fe.read_text()) if fe.exists() else None
        m = json.loads(fm.read_text()) if fm.exists() else None
    else:
     try:
        d = om(pt); (RAW / f"{pid}_om.json").write_text(json.dumps(d))
     except Exception as ex:
        rec["error_om"] = str(ex); summary["points"][pid] = rec; print(pid, "OM FAIL", ex); continue
     try:
        e_ = ens(pt); (RAW / f"{pid}_ens.json").write_text(json.dumps(e_))
     except Exception as ex:
        e_ = None; rec["error_ens"] = str(ex)
     try:
        m = metno(pt); (RAW / f"{pid}_metno.json").write_text(json.dumps(m))
     except Exception as ex:
        m = None; rec["error_metno"] = str(ex)
    h, dd = d["hourly"], d["daily"]
    rec["tz"] = d.get("timezone"); rec["model_elev"] = d.get("elevation")
    times = h["time"]
    # met.no series: (utc epoch, values); matched to each moment by nearest step within 3 h
    mseries = []
    off = d.get("utc_offset_seconds", 0)
    if m:
        for st in m["properties"]["timeseries"]:
            ep = calendar.timegm(time.strptime(st["time"], "%Y-%m-%dT%H:%M:%SZ"))
            det = st["data"]["instant"]["details"]
            nxt = st["data"].get("next_1_hours") or st["data"].get("next_6_hours") or {}
            mseries.append((ep, {"t": det.get("air_temperature"), "wind_ms": det.get("wind_speed"), "gust_ms": det.get("wind_speed_of_gust"),
                            "sym": (nxt.get("summary") or {}).get("symbol_code"),
                            "pr": (nxt.get("details") or {}).get("precipitation_amount"),
                            "pp": (nxt.get("details") or {}).get("probability_of_precipitation"),
                            "local": time.strftime("%Y-%m-%d %H:%M", time.gmtime(ep + off)),
                            "step": "1h" if st["data"].get("next_1_hours") else "6h"}))
    for day, hh, what in moments:
        key = f"{day}T{hh}:00"
        idx = times.index(key) if key in times else None
        mm = {"date": day, "hour": hh, "what": what, "in_range": idx is not None}
        if idx is not None:
            for mdl in ("best_match", "ecmwf_ifs025", "gfs_seamless", "icon_seamless"):
                sfx = "" if mdl == "best_match" else "_" + mdl
                t = pick(h, "temperature_2m" + sfx, idx)
                if t is None and mdl == "best_match": t = pick(h, "temperature_2m_best_match", idx); sfx = "_best_match"
                mm[mdl] = {"t": t, "feels": pick(h, "apparent_temperature" + sfx, idx),
                           "pp": pick(h, "precipitation_probability" + sfx, idx), "pr": pick(h, "precipitation" + sfx, idx),
                           "snow": pick(h, "snowfall" + sfx, idx), "code": pick(h, "weather_code" + sfx, idx),
                           "wx": WMO.get(pick(h, "weather_code" + sfx, idx)), "wind": pick(h, "wind_speed_10m" + sfx, idx),
                           "gust": pick(h, "wind_gusts_10m" + sfx, idx), "fzl": pick(h, "freezing_level_height" + sfx, idx),
                           "cloud": pick(h, "cloud_cover" + sfx, idx), "rh": pick(h, "relative_humidity_2m" + sfx, idx)}
            if e_:
                eh = e_["hourly"]; et = eh["time"]
                if key in et:
                    j = et.index(key)
                    temps = [eh[k][j] for k in eh if k.startswith("temperature_2m") and eh[k][j] is not None]
                    prs = [eh[k][j] for k in eh if k.startswith("precipitation") and eh[k][j] is not None]
                    if temps:
                        st = sorted(temps)
                        mm["ens"] = {"n": len(st), "t_p10": round(st[int(.1*len(st))],1), "t_p50": round(statistics.median(st),1),
                                     "t_p90": round(st[int(.9*len(st))-1],1), "p_wet": round(100*sum(1 for p in prs if p >= .2)/len(prs)) if prs else None}
        if mseries:
            want = calendar.timegm(time.strptime(key, "%Y-%m-%dT%H:%M")) - off
            ep, v = min(mseries, key=lambda x: abs(x[0] - want))
            if abs(ep - want) <= 3 * 3600: mm["metno"] = v
        rec["moments"].append(mm)
    for i, day in enumerate(dd["time"]):
        row = {}
        for k, v in dd.items():
            if k == "time": continue
            row[k] = v[i] if i < len(v) else None
        rec["daily"][day] = row
    summary["points"][pid] = rec
    print(pid, "ok", len(rec["moments"]))
    if not OFFLINE: time.sleep(0.4)

(HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
print("wrote", HERE / "summary.json")
