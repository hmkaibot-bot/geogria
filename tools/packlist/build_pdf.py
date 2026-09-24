# -*- coding: utf-8 -*-
"""Render 26-行李清單.md as a printable A4 PDF (26-行李清單.pdf at the repo root).

Every "- [ ] ..." line gets two empty tick boxes, A (Alex) and H (Hugo), for ticking
with a pen. Run: python3 tools/packlist/build_pdf.py
"""
import html, json, pathlib, re, subprocess
import markdown

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "26-行李清單.md"
OUT_HTML = HERE / "packlist_print.html"
OUT_PDF = ROOT / "26-行李清單.pdf"
IMG = ROOT / "tools" / "pdfbuild" / "img"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
COVER = "ge_gergeti"

credits = json.loads((IMG / "credits.json").read_text(encoding="utf-8"))
cov = credits.get(COVER, {})

MD = markdown.Markdown(extensions=["tables", "sane_lists"])
def render(s):
    MD.reset()
    return MD.convert(s)

def inline(s):
    return render(s).removeprefix("<p>").removesuffix("</p>")

TASK = re.compile(r"^(\s*)[-*] \[( |x|X)\] (.+)$")

def render_body(body):
    out, buf, tasks = [], [], []
    in_sub = False
    def flush_md():
        if buf:
            out.append(render("\n".join(buf))); buf.clear()
    def flush_tasks():
        if tasks:
            out.append('<ul class="ck">' + "".join(tasks) + "</ul>"); tasks.clear()
    for line in body.splitlines():
        m = TASK.match(line)
        if m:
            flush_md(); in_sub = False
            text = m.group(3).strip()
            owned = " own" if "✅已有" in text else ""
            tasks.append(f'<li class="it{owned}"><span class="bx">A</span><span class="bx">H</span>'
                         f'<span class="tx">{inline(text)}</span></li>')
            continue
        if (tasks or in_sub) and line.startswith(("  ", "\t")) and line.strip():
            flush_tasks(); in_sub = True; buf.append(line.strip()); continue
        in_sub = False
        flush_tasks()
        buf.append(line)
    flush_md(); flush_tasks()
    h = "\n".join(out)
    h = re.sub(r"(<ul class=\"ck\">.*?</ul>)\s*(<(ul|ol)>)", r'\1<\3 class="sub">', h, flags=re.S)
    return h

md_text = SRC.read_text(encoding="utf-8")
title = re.search(r"^# (.+)$", md_text, re.M).group(1).strip()
parts = re.split(r"^## ", md_text, flags=re.M)
intro = re.sub(r"^# .+$", "", parts[0], count=1, flags=re.M).strip()
sections = []
n_items = 0
for p in parts[1:]:
    head, _, body = p.partition("\n")
    body = body.strip().rstrip("-").strip()
    body = re.sub(r"\n---\s*$", "", body)
    b = render_body(body)
    n_items += b.count('class="it')
    cls = "sec"
    if head.strip().startswith("📚"):
        cls += " src"
    sections.append(f'<section class="{cls}"><h2>{html.escape(head.strip())}</h2>{b}</section>')

m = re.match(r"(\d+)\s*·\s*(.+?)（(.+)）$", title)
t_num, t_name, t_sub = (m.group(1), m.group(2), m.group(3)) if m else ("26", title, "")

CSS = r"""
@page { size: A4; margin: 13mm 12mm 14mm 12mm;
  @bottom-left { content: "26 · 行李清單 · Alex / Hugo"; font: 7pt "Noto Sans CJK TC"; color: #7C8F88; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 7pt "Noto Sans CJK TC"; color: #7C8F88; } }
@page :first { margin-top: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Noto Sans CJK TC","DejaVu Sans","Noto Color Emoji",sans-serif; font-size: 8.4pt; line-height: 1.5; color: #22332e; }
b, strong { color: #13302a; }
a { color: #1c5668; text-decoration: none; }
code { font-family: "DejaVu Sans Mono",monospace; font-size: .92em; background: #eef3f1; padding: 0 3px; border-radius: 2px; }

/* masthead */
.mast { position: relative; margin: 0 -12mm 5mm; height: 62mm; overflow: hidden; background: #1D3B34; color: #fff; }
.mast img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%; }
.mast .shade { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(18,40,35,.94) 0%, rgba(18,40,35,.78) 48%, rgba(18,40,35,.18) 100%); }
.mast .in { position: absolute; left: 14mm; right: 14mm; bottom: 9mm; }
.mast .kick { font-size: 7.4pt; letter-spacing: .28em; color: #F0CF93; text-transform: uppercase; }
.mast h1 { font-size: 27pt; line-height: 1.15; margin: 2mm 0 1.5mm; font-weight: 900; }
.mast h1 .n { color: #D59A3C; margin-right: 3mm; }
.mast .sub { font-size: 10pt; opacity: .92; }
.mast .route { margin-top: 4mm; font-family: "DejaVu Sans Mono",monospace; font-size: 8.4pt; letter-spacing: .06em; color: #F4E6C8; }
.mast .route i { font-style: normal; opacity: .55; padding: 0 1.2mm; }
.mast .cr { position: absolute; right: 3mm; bottom: 1.6mm; font-size: 5.4pt; color: rgba(255,255,255,.65); }
.stats { display: flex; gap: 3mm; margin: 0 0 4mm; }
.stats div { flex: 1; border: .6pt solid #d3ddd9; border-left: 2.4pt solid #D59A3C; padding: 1.8mm 3mm; border-radius: 1.5mm; }
.stats b { display: block; font-size: 13pt; line-height: 1.1; color: #1D3B34; }
.stats span { font-size: 7pt; color: #5d716a; }
.intro { background: #f4f7f5; border-radius: 1.5mm; padding: 2.4mm 3.2mm; margin-bottom: 4mm; font-size: 8pt; }
.intro blockquote { margin: 0; }
.intro p { margin: .6mm 0; }
.legend { display: flex; align-items: center; gap: 2mm; font-size: 7.6pt; color: #4d635c; margin: -1mm 0 4mm; }
.legend .bx { position: static; }

/* sections */
h2 { font-size: 13pt; line-height: 1.3; margin: 5.5mm 0 2mm; padding-bottom: 1.2mm; border-bottom: 1.4pt solid #1D3B34; color: #1D3B34; break-after: avoid; page-break-after: avoid; }
.sec:first-of-type h2 { margin-top: 0; }
h3 { font-size: 9.6pt; margin: 3.5mm 0 1.4mm; color: #8A5A17; break-after: avoid; page-break-after: avoid; }
h4 { font-size: 9pt; margin: 3mm 0 1mm; break-after: avoid; }
p { margin: 1.2mm 0; }
ul, ol { margin: 1mm 0 2mm; padding-left: 5mm; }
li { margin: .5mm 0; }
blockquote { margin: 2mm 0; padding: 1.6mm 3mm; border-left: 2.4pt solid #D59A3C; background: #fbf4e8; border-radius: 0 1.5mm 1.5mm 0; break-inside: avoid; }
blockquote p { margin: .6mm 0; }
hr { display: none; }

/* checklist rows: two pen boxes */
ul.ck { list-style: none; padding: 0; margin: 1.5mm 0 2mm; border-top: .5pt solid #e3eae7; }
ul.ck li.it { display: flex; gap: 1.6mm; align-items: flex-start; padding: 1.3mm 0 1.3mm .6mm; margin: 0; border-bottom: .5pt solid #e3eae7; break-inside: avoid; page-break-inside: avoid; }
.bx { flex: 0 0 3.6mm; width: 3.6mm; height: 3.6mm; margin-top: .45mm; border: .8pt solid #5d716a; border-radius: .6mm; font-size: 4.6pt; line-height: 3.4mm; text-align: center; color: #9aaba4; font-weight: 700; display: inline-block; }
li.own .bx { border-color: #2F6B4F; color: #2F6B4F; }
.tx { flex: 1; min-width: 0; padding-left: .8mm; }
ul.sub, ol.sub { margin: -1mm 0 2mm 9.6mm; padding: 1.4mm 2.6mm 1.4mm 6mm; background: #f6f8f7; border-radius: 0 0 1.5mm 1.5mm; font-size: 7.9pt; color: #3f544d; }

/* tables */
table { width: 100%; border-collapse: collapse; margin: 1.6mm 0 3mm; font-size: 7.5pt; line-height: 1.42; }
thead { display: table-header-group; }
th { background: #1D3B34; color: #fff; text-align: left; font-weight: 700; padding: 1.3mm 1.8mm; border: .5pt solid #1D3B34; }
td { padding: 1.2mm 1.8mm; border: .5pt solid #d8e1dd; vertical-align: top; }
tr { break-inside: avoid; page-break-inside: avoid; }
tbody tr:nth-child(even) td { background: #f7faf8; }

/* sources: compact two-column list */
.src { font-size: 6.6pt; line-height: 1.35; }
.src ul { columns: 2; column-gap: 6mm; padding-left: 3.5mm; }
.src li { break-inside: avoid; word-break: break-all; margin: .3mm 0; }
.src p { margin: 2mm 0 .6mm; font-size: 7.6pt; }
"""

codes = ["HKG", "KUL", "DOH", "TBS", "EVN", "TBS", "DOH", "KUL", "HKG"]
arrows = ["→", "→", "→", "⇢", "→", "→", "→", "→"]  # TBS⇢EVN is by car
route = codes[0] + "".join(f"<i>{a}</i>{c}" for a, c in zip(arrows, codes[1:]))

cover_credit = f'相片：{html.escape(cov.get("artist",""))} · {html.escape(cov.get("license",""))}（Flickr）'

page = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>
<div class="mast"><img src="file://{IMG / (COVER + '.jpg')}" alt=""><div class="shade"></div>
  <div class="in"><div class="kick">Packing list · Georgia × Armenia · 2026</div>
    <h1><span class="n">{t_num}</span>{html.escape(t_name)}</h1>
    <div class="sub">{html.escape(t_sub)}</div>
    <div class="route">{route}</div></div>
  <div class="cr">{cover_credit}</div></div>
<div class="stats">
  <div><b>2 人</b><span>Alex · Hugo</span></div>
  <div><b>17 日</b><span>25/9 – 11/10</span></div>
  <div><b>4 國</b><span>馬來西亞 · 卡塔爾 · 格魯吉亞 · 亞美尼亞</span></div>
  <div><b>{n_items} 項</b><span>逐項打剔</span></div>
</div>
<div class="legend"><span class="bx">A</span><span class="bx">H</span> 每項兩格：A ＝ Alex、H ＝ Hugo，執好就用筆剔自己嗰格。綠框 ＝ 你講過已經有嘅嘢。</div>
<div class="intro">{render(intro)}</div>
{''.join(sections)}
</body></html>"""

OUT_HTML.write_text(page, encoding="utf-8")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
                "--virtual-time-budget=15000", f"--print-to-pdf={OUT_PDF}", "--no-pdf-header-footer",
                f"file://{OUT_HTML}"], check=True, capture_output=True)
print(f"wrote {OUT_PDF} · {len(sections)} sections · {n_items} items")
