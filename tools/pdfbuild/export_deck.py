# -*- coding: utf-8 -*-
"""Export the itinerary data as deck.json for the PowerPoint generator."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data_days as DD, data_core as C, images as IM

OUT = os.path.join(os.path.dirname(HERE), "pptbuild", "deck.json")

def strip(t):
    if not isinstance(t, str): return t
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    return re.sub(r"<[^>]+>", "", t)

R = {r["day"]: r for r in json.load(open(os.path.join(HERE, "routes.json"), encoding="utf-8"))}
days = []
for d in DD.D:
    rt = R[d["num"]]
    ride = {x["time"]: x["ride"] for x in rt["timeline"]}
    h = d.get("hotel") or {}
    days.append(dict(
        num=d["num"], date=d["date"], wd=d["wd"], route=d["route"], stats=d["stats"],
        sched=[[t, strip(w), ride.get(t, "")] for t, w in d["sched"]],
        legs=[[strip(x) for x in l] for l in d.get("legs", [])],
        hotel={k: strip(v) for k, v in h.items() if k != "tag"},
        meals={k: [[a, strip(b), strip(c)] for a, b, c in v] for k, v in (d.get("meals") or {}).items()},
        sights=[[p, strip(n), co, strip(dt)] for p, n, co, dt in d.get("sights", [])],
        warns=[strip(w) for w in d.get("warns", [])], notes=[strip(n) for n in d.get("notes", [])],
        hero=IM.DAY_HERO.get(d["num"]), strip_imgs=IM.DAY_STRIP.get(d["num"], []),
        mode=rt["mode"], total_km=rt["total_km"], total_time=rt["total_ride_time"],
        maps=rt["maps_url"], caveat=rt["caveat"]))

out = dict(days=days, trip=C.TRIP, flights=C.FLIGHTS, flight_ref=C.FLIGHT_REF,
           bookings=[[strip(x) for x in b] for b in C.BOOKINGS], rental=C.RENTAL,
           todo=[[strip(x) for x in t] for t in C.TODO],
           practical=[[strip(x) for x in p] for p in C.PRACTICAL],
           book_now=[[strip(x) for x in b] for b in C.BOOK_NOW],
           book_later=[[strip(x) for x in b] for b in C.BOOK_LATER],
           traps=[[strip(x) for x in t] for t in C.TRAPS],
           overview=IM.OVERVIEW, captions=IM.CAPTION, credits=IM.CREDITS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(days), "days")
