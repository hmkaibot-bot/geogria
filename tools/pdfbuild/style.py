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

/* ---------- cover (full-bleed photo) ---------- */
@page cover { size: A4; margin: 0; }
.cover { page: cover; position: relative; width: 210mm; height: 296mm; overflow: hidden;
  display: flex; flex-direction: column; justify-content: flex-end; color: #fff;
  padding: 18mm 18mm 16mm; page-break-after: always; background: #1d3b34; }
.cover img.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 45%; }
.cover .shade { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(20,38,34,.18) 0%, rgba(20,38,34,.05) 30%, rgba(20,38,34,.62) 62%, rgba(20,38,34,.94) 100%); }
.cover .in { position: relative; }
.cover .kicker { font-size: 10pt; letter-spacing: .32em; opacity: .8; text-transform: uppercase; }
.cover h1 { font-size: 31pt; line-height: 1.14; margin: 4mm 0 2.5mm; text-shadow: 0 1px 6px rgba(0,0,0,.45); }
.cover .sub { font-size: 13pt; opacity: .92; font-weight: 300; }
.cover .rule { width: 34mm; height: 2.5px; background: #d59a3c; margin: 6mm 0; }
.cover .grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 3.5mm 7mm; margin-top: 6mm; }
.cover .cell { background: rgba(255,255,255,.10); border-left: 2.5px solid #d59a3c; padding: 2.6mm 4mm; border-radius: 2px;
  backdrop-filter: blur(2px); }
.cover .cell b { display: block; font-size: 7.2pt; letter-spacing: .12em; opacity: .72; text-transform: uppercase; margin-bottom: 1mm; }
.cover .cell span { font-size: 10.2pt; }
.cover .foot { margin-top: 7mm; font-size: 7.8pt; opacity: .62; display: flex; justify-content: space-between; }

/* ---------- overview photo grid ---------- */
.ov { display: grid; grid-template-columns: repeat(3,1fr); gap: 3mm; }
.ov .c { position: relative; height: 44mm; border-radius: 3px; overflow: hidden; background: #2e4a43; }
.ov .c img { width: 100%; height: 100%; object-fit: cover; display: block; }
.ov .c .cap { position: absolute; left: 0; right: 0; bottom: 0; padding: 6mm 2.6mm 2.2mm; color: #fff;
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.72) 100%); }
.ov .c .cap b { display: block; font-size: 9.6pt; }
.ov .c .cap span { font-size: 7.4pt; opacity: .9; }
.ov .c .d { position: absolute; top: 2mm; left: 2mm; background: #d59a3c; color: #fff; font-weight: 700;
  font-size: 7.6pt; padding: .6mm 1.8mm; border-radius: 2px; letter-spacing: .04em; }

/* ---------- section ---------- */
.sec { page-break-before: always; }
.sec-head { border-bottom: 2.2px solid #2e4a43; padding-bottom: 2mm; margin-bottom: 4mm;
  display: flex; align-items: baseline; justify-content: space-between; }
.sec-head h2 { font-size: 15pt; color: #1d3b34; }
.sec-head .tag { font-size: 8pt; color: #6b7a74; letter-spacing: .1em; }
.sec-banner { position: relative; height: 26mm; border-radius: 3px; overflow: hidden; margin-bottom: 4mm; background: #2e4a43; }
.sec-banner img { width: 100%; height: 100%; object-fit: cover; display: block; }
.sec-banner .shade { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(20,38,34,.88) 0%, rgba(20,38,34,.55) 45%, rgba(20,38,34,.05) 100%); }
.sec-banner .t { position: absolute; left: 5mm; top: 50%; transform: translateY(-50%); color: #fff; }
.sec-banner .t h2 { font-size: 16pt; text-shadow: 0 1px 4px rgba(0,0,0,.4); }
.sec-banner .t .tag { font-size: 8pt; opacity: .85; letter-spacing: .1em; display: block; margin-top: 1mm; }
.sec-banner .cr { position: absolute; right: 2mm; bottom: 1.2mm; font-size: 5.8pt; color: rgba(255,255,255,.75); }

/* ---------- day (photo hero) ---------- */
.day { page-break-before: always; }
.day-hero { position: relative; height: 44mm; border-radius: 3px 3px 0 0; overflow: hidden; background: #2e4a43; }
.day-hero img.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.day-hero .shade { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(20,38,34,.12) 0%, rgba(20,38,34,.10) 40%, rgba(20,38,34,.82) 100%); }
.day-hero .cr { position: absolute; right: 2mm; top: 1.4mm; font-size: 5.8pt; color: rgba(255,255,255,.8);
  background: rgba(0,0,0,.28); padding: .3mm 1.4mm; border-radius: 2px; }
.day-hd { position: absolute; left: 0; right: 0; bottom: 0; color: #fff; padding: 3mm 4mm;
  display: flex; align-items: flex-end; justify-content: space-between; }
.day-hd .l { display: flex; align-items: baseline; gap: 4mm; flex-wrap: wrap; }
.day-hd .dnum { font-size: 8pt; letter-spacing: .18em; opacity: .85; background: #d59a3c; padding: .5mm 1.8mm; border-radius: 2px; font-weight: 700; }
.day-hd .date { font-size: 15pt; font-weight: 700; text-shadow: 0 1px 4px rgba(0,0,0,.5); }
.day-hd .route { font-size: 10pt; opacity: .95; text-shadow: 0 1px 3px rgba(0,0,0,.5); }
.day-hd .r { text-align: right; font-size: 8pt; opacity: .92; line-height: 1.35; text-shadow: 0 1px 3px rgba(0,0,0,.5); white-space: nowrap; }
.strip { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; gap: 1.5mm; margin: 0 -3mm 3mm; padding: 0 3mm; }
.strip .s { position: relative; height: 22mm; border-radius: 2px; overflow: hidden; background: #eef2f0; }
.strip .s img { width: 100%; height: 100%; object-fit: cover; display: block; }
.strip .s .cap { position: absolute; left: 0; right: 0; bottom: 0; padding: 3mm 1.6mm 1mm; color: #fff; font-size: 6.6pt; line-height: 1.2;
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.7) 100%); }
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
.credits { display: grid; grid-template-columns: repeat(5,1fr); gap: 1.8mm; }
.credits .k { font-size: 6.2pt; line-height: 1.28; color: #4a5b55; }
.credits .k img { width: 100%; height: 13mm; object-fit: cover; border-radius: 2px; display: block; margin-bottom: .8mm; }
.credits .k b { color: #1d3b34; display: block; }
.credits .k .u { color: #6b7a74; word-break: break-all; font-size: 5.3pt; }
"""
