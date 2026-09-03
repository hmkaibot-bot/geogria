# -*- coding: utf-8 -*-
CSS = r"""
@page { size: A4; margin: 12mm 10mm 14mm 10mm; }
@page { @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Noto Sans CJK TC","Noto Sans CJK SC","Noto Sans",sans-serif;
  font-size: 8.6pt; line-height: 1.42; color: #23302c; margin: 0;
}
h1,h2,h3,h4 { margin: 0; font-weight: 700; }
a { color: #1f5f52; text-decoration: none; }

/* ---------- cover ---------- */
.cover { height: 268mm; display: flex; flex-direction: column; justify-content: center;
  background: linear-gradient(150deg,#1d3b34 0%,#2e4a43 55%,#3c5a4e 100%); color: #fff;
  padding: 20mm; page-break-after: always; }
.cover .kicker { font-size: 10pt; letter-spacing: .32em; opacity: .72; text-transform: uppercase; }
.cover h1 { font-size: 30pt; line-height: 1.14; margin: 5mm 0 3mm; }
.cover .sub { font-size: 13pt; opacity: .9; font-weight: 300; }
.cover .rule { width: 34mm; height: 2.5px; background: #d59a3c; margin: 7mm 0; }
.cover .grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 4mm 8mm; margin-top: 7mm; }
.cover .cell { background: rgba(255,255,255,.08); border-left: 2.5px solid #d59a3c; padding: 3mm 4mm; border-radius: 2px; }
.cover .cell b { display: block; font-size: 7.4pt; letter-spacing: .12em; opacity: .68; text-transform: uppercase; margin-bottom: 1.2mm; }
.cover .cell span { font-size: 10.5pt; }
.cover .foot { margin-top: auto; font-size: 8pt; opacity: .55; }

/* ---------- section ---------- */
.sec { page-break-before: always; }
.sec-head { border-bottom: 2.2px solid #2e4a43; padding-bottom: 2mm; margin-bottom: 4mm;
  display: flex; align-items: baseline; justify-content: space-between; }
.sec-head h2 { font-size: 15pt; color: #1d3b34; }
.sec-head .tag { font-size: 8pt; color: #6b7a74; letter-spacing: .1em; }

/* ---------- day ---------- */
.day { page-break-before: always; }
.day-hd { background: #2e4a43; color: #fff; padding: 3mm 4mm; border-radius: 3px 3px 0 0;
  display: flex; align-items: center; justify-content: space-between; }
.day-hd .l { display: flex; align-items: baseline; gap: 4mm; }
.day-hd .dnum { font-size: 8pt; letter-spacing: .18em; opacity: .7; }
.day-hd .date { font-size: 13.5pt; font-weight: 700; }
.day-hd .route { font-size: 9.6pt; opacity: .93; }
.day-hd .r { text-align: right; font-size: 8pt; opacity: .85; line-height: 1.35; }
.day-body { border: 1px solid #d6ded9; border-top: none; border-radius: 0 0 3px 3px; padding: 3mm; }

.block { margin-bottom: 3mm; }
.block:last-child { margin-bottom: 0; }
.bt { font-size: 8.4pt; font-weight: 700; color: #1d3b34; margin-bottom: 1.4mm;
  border-left: 3px solid #d59a3c; padding-left: 2mm; }

table { width: 100%; border-collapse: collapse; font-size: 8pt; }
th { background: #eef2f0; color: #1d3b34; text-align: left; font-weight: 700;
  padding: 1.3mm 1.8mm; border: .5px solid #d6ded9; font-size: 7.6pt; }
td { padding: 1.3mm 1.8mm; border: .5px solid #e2e8e5; vertical-align: top; }
tr:nth-child(even) td { background: #fafbfa; }
td.t { white-space: nowrap; font-weight: 700; color: #2e4a43; width: 15mm; }
td.km { white-space: nowrap; text-align: right; width: 17mm; }
td.c { font-family: ui-monospace,"DejaVu Sans Mono",monospace; font-size: 7.1pt; white-space: nowrap; color: #4a5b55; }

.pill { display: inline-block; padding: .3mm 1.4mm; border-radius: 2px; font-size: 6.9pt;
  font-weight: 700; letter-spacing: .03em; vertical-align: middle; }
.p-must { background: #1d3b34; color: #fff; }
.p-alt  { background: #6b7a74; color: #fff; }
.p-bon  { background: #d59a3c; color: #fff; }
.p-skip { background: #e2e8e5; color: #6b7a74; }
.p-b { background: #eef2f0; color: #2e4a43; border: .5px solid #c3cfc9; }
.p-m { background: #d59a3c; color: #fff; }
.p-s { background: #8a4d2e; color: #fff; }
.p-ok { background: #2f6b4f; color: #fff; }
.p-no { background: #a33b2a; color: #fff; }

.warn { background: #fdf4ec; border-left: 3px solid #c8791f; padding: 2mm 2.6mm;
  font-size: 7.7pt; border-radius: 0 2px 2px 0; margin-top: 1.6mm; }
.warn b { color: #8a4d2e; }
.note { background: #eef4f1; border-left: 3px solid #2f6b4f; padding: 2mm 2.6mm;
  font-size: 7.7pt; border-radius: 0 2px 2px 0; margin-top: 1.6mm; }
.hotel { background: #f4f7f5; border: 1px solid #d6ded9; border-radius: 2px; padding: 2.2mm 2.6mm; font-size: 7.9pt; }
.hotel .hn { font-weight: 700; font-size: 9pt; color: #1d3b34; }
.hotel .meta { color: #55655e; margin-top: .8mm; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.small { font-size: 7.3pt; color: #6b7a74; }
ul.tight { margin: .8mm 0 0; padding-left: 4mm; }
ul.tight li { margin-bottom: .5mm; }
.legend { font-size: 7.2pt; color: #6b7a74; margin-top: 2mm; }
"""
