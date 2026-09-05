# -*- coding: utf-8 -*-
"""HTML fragment builders for the itinerary PDF."""
import re as _re
from html import escape as e

def md(t):
    """Convert **bold** markdown to <b> tags. Input may already contain HTML."""
    if not isinstance(t, str): return t
    return _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

def tbl(headers, rows, classes=None):
    """classes: list of per-column css class or None"""
    h = "".join(f"<th>{e(str(x))}</th>" for x in headers)
    body = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            cls = (classes[i] if classes and i < len(classes) and classes[i] else "")
            cls = f' class="{cls}"' if cls else ""
            cells.append(f"<td{cls}>{c}</td>")   # NOTE: cells pre-escaped/marked-up by caller
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(body)}</tbody></table>"

def pill(text, kind):
    return f'<span class="pill p-{kind}">{e(text)}</span>'

def block(title, inner):
    return f'<div class="block"><div class="bt">{e(title)}</div>{inner}</div>'

def warn(html):  return f'<div class="warn">{html}</div>'
def note(html):  return f'<div class="note">{html}</div>'

def hotel_card(h):
    """h: dict(name, tag, addr, coord, ref, price, times, extra)"""
    bits = []
    if h.get("addr"):  bits.append(e(h["addr"]))
    if h.get("coord"): bits.append(f'<span class="c">{e(h["coord"])}</span>')
    line2 = []
    if h.get("ref"):   line2.append(f'訂單 <b>{e(h["ref"])}</b>')
    if h.get("price"): line2.append(f'<b>{e(h["price"])}</b>')
    if h.get("times"): line2.append(e(h["times"]))
    out = f'<div class="hotel"><span class="hn">{e(h["name"])}</span> {h.get("tag","")}'
    if bits:  out += f'<div class="meta">{" · ".join(bits)}</div>'
    if line2: out += f'<div class="meta">{" · ".join(line2)}</div>'
    if h.get("extra"): out += f'<div class="meta small">{h["extra"]}</div>'
    return out + "</div>"

def _photo_strip(keys, IM):
    keys = [k for k in keys if IM.has(k)]
    if not keys: return ""
    cells = "".join(
        f'<div class="s"><img src="{IM.thumb(k)}"><div class="cap">{e(IM.CAPTION.get(k,k))}</div></div>' for k in keys)
    return f'<div class="strip">{cells}</div>'

def day(dnum, date, weekday, route, stats, blocks, IM=None, hero=None, strip=()):
    right = "<br>".join(e(s) for s in stats)
    hd = f"""<div class="day-hd">
<div class="l"><span class="dnum">{e(dnum)}</span><span class="date">{e(date)}（{e(weekday)}）</span>
<span class="route">{e(route)}</span></div>
<div class="r">{right}</div></div>"""
    if IM and hero and IM.has(hero):
        top = (f'<div class="day-hero"><img class="bg" src="{IM.path(hero)}"><div class="shade"></div>'
               f'<div class="cr">📷 {e(IM.CAPTION.get(hero,""))} · {e(IM.credit(hero))}</div>{hd}</div>')
    else:
        inner = hd.split(">", 1)[1]  # drop the opening <div class="day-hd">
        top = f'<div class="day-hero" style="height:auto;position:relative"><div class="day-hd" style="position:static;background:#2e4a43">{inner}</div>'
    body = (_photo_strip(strip, IM) if IM else "") + "".join(blocks)
    return f'<div class="day">{top}<div class="day-body">{body}</div></div>'

def section(title, tag, inner, IM=None, banner=None):
    if IM and banner and IM.has(banner):
        head = (f'<div class="sec-banner"><img src="{IM.path(banner)}"><div class="shade"></div>'
                f'<div class="t"><h2>{e(title)}</h2><span class="tag">{e(tag)}</span></div>'
                f'<div class="cr">📷 {e(IM.CAPTION.get(banner,""))} · {e(IM.credit(banner))}</div></div>')
    else:
        head = f'<div class="sec-head"><h2>{e(title)}</h2><span class="tag">{e(tag)}</span></div>'
    return f'<div class="sec">{head}{inner}</div>'

def overview(items, IM):
    cells = []
    for d, date, place, key in items:
        if not IM.has(key): continue
        cells.append(f'<div class="c"><img src="{IM.path(key)}"><span class="d">{e(d)}</span>'
                     f'<div class="cap"><b>{e(place)}</b><span>{e(date)} · {e(IM.CAPTION.get(key,""))}</span></div></div>')
    return f'<div class="ov">{"".join(cells)}</div>'

def credits_page(IM):
    cells = []
    for k in sorted(IM.CREDITS):
        if not IM.has(k): continue
        c = IM.CREDITS[k]
        src = c.get("landing") or c.get("file") or ""
        cells.append(f'<div class="k"><img src="{IM.thumb(k)}"><b>{e(IM.CAPTION.get(k,k))}</b>'
                     f'{e(c.get("artist",""))} · {e(c.get("license",""))} · {e(str(c.get("src","")))}'
                     f'<div class="u">{e(src)}</div></div>')
    return f'<div class="credits">{"".join(cells)}</div>'

def cover(t, IM=None, photo=None, updated=""):
    cells = [("日期", t["dates"]), ("旅客", t["travellers"]),
             ("車", t["bikes"]), ("里程", t["distance"])]
    cg = "".join(f'<div class="cell"><b>{e(k)}</b><span>{e(v)}</span></div>' for k, v in cells)
    bg = ""
    cr = ""
    if IM and photo and IM.has(photo):
        bg = f'<img class="bg" src="{IM.path(photo)}"><div class="shade"></div>'
        cr = f'📷 {e(IM.CAPTION.get(photo,""))} · {e(IM.credit(photo))}'
    return f"""<div class="cover">{bg}<div class="in">
<div class="kicker">Itinerary · 完整行程表</div>
<h1>{e(t["title"])}</h1>
<div class="sub">{e(t["subtitle"])}</div>
<div class="rule"></div>
<div class="sub" style="font-size:9.5pt;opacity:.85;line-height:1.6">{e(t["route"])}</div>
<div class="grid">{cg}</div>
<div class="foot"><span>含座標 · 行車時間 · 酒店訂單 · 餐廳 · 景點　|　最後更新 {e(updated)}</span><span>{cr}</span></div>
</div></div>"""

def html_doc(css, body):
    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>格魯吉亞亞美尼亞行程</title><style>{css}</style></head><body>{body}</body></html>"""
