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

def day(dnum, date, weekday, route, stats, blocks):
    right = "<br>".join(e(s) for s in stats)
    return f"""<div class="day"><div class="day-hd">
<div class="l"><span class="dnum">{e(dnum)}</span><span class="date">{e(date)}（{e(weekday)}）</span>
<span class="route">{e(route)}</span></div>
<div class="r">{right}</div></div>
<div class="day-body">{''.join(blocks)}</div></div>"""

def section(title, tag, inner):
    return f"""<div class="sec"><div class="sec-head"><h2>{e(title)}</h2>
<span class="tag">{e(tag)}</span></div>{inner}</div>"""

def cover(t):
    cells = [("日期", t["dates"]), ("旅客", t["travellers"]),
             ("車", t["bikes"]), ("里程", t["distance"])]
    cg = "".join(f'<div class="cell"><b>{e(k)}</b><span>{e(v)}</span></div>' for k, v in cells)
    return f"""<div class="cover">
<div class="kicker">Itinerary · 完整行程表</div>
<h1>{e(t["title"])}</h1>
<div class="sub">{e(t["subtitle"])}</div>
<div class="rule"></div>
<div class="sub" style="font-size:9.5pt;opacity:.8;line-height:1.6">{e(t["route"])}</div>
<div class="grid">{cg}</div>
<div class="foot">含座標 · 行車時間 · 酒店訂單 · 餐廳 · 景點　|　最後更新 2026-09-03</div>
</div>"""

def html_doc(css, body):
    return f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">
<title>格魯吉亞亞美尼亞行程</title><style>{css}</style></head><body>{body}</body></html>"""
