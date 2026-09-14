# -*- coding: utf-8 -*-
CSS = r"""
@page { size: A4; margin: 13mm 11mm 15mm 11mm; }
@page { @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Noto Sans CJK TC","Noto Sans CJK SC","Noto Sans",sans-serif;
  font-size: 8.8pt; line-height: 1.45; color: #22313a; margin: 0;
}
h1,h2,h3,h4 { margin: 0; font-weight: 700; }
a { color: #1c5668; text-decoration: none; }
b { color: #14323d; }

/* ---------------- cover ---------------- */
@page cover { size: A4; margin: 0; }
.cover { page: cover; position: relative; width: 210mm; height: 296mm; overflow: hidden;
  page-break-after: always; background: #14323d; color: #fff; }
.cover img.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 55%; }
.cover .scrim { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(12,38,48,.30) 0%, rgba(12,38,48,.12) 26%, rgba(12,38,48,.72) 62%, rgba(12,38,48,.96) 100%); }
.cover .in { position: absolute; left: 18mm; right: 18mm; bottom: 20mm; }
.cover .kicker { font-size: 9.5pt; letter-spacing: .34em; opacity: .82; text-transform: uppercase; color: #e8c17a; }
.cover h1 { font-size: 33pt; line-height: 1.16; margin: 5mm 0 3mm; text-shadow: 0 1px 8px rgba(0,0,0,.45); }
.cover .sub { font-size: 12.5pt; opacity: .93; font-weight: 300; }
.cover .rule { width: 32mm; height: 2.5px; background: #c8862b; margin: 7mm 0 6mm; }
.cover .grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 3.5mm 7mm; margin-top: 6mm; }
.cover .cell { background: rgba(255,255,255,.10); border-left: 2.5px solid #c8862b; padding: 2.6mm 4mm; border-radius: 2px; }
.cover .cell b { display: block; color: #e8c17a; font-size: 7pt; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 1mm; }
.cover .cell span { font-size: 10pt; }
.cover .foot { margin-top: 7mm; font-size: 7.4pt; opacity: .6; display: flex; justify-content: space-between; }

/* ---------------- section ---------------- */
.sec { page-break-before: always; }
.banner { position: relative; height: 30mm; border-radius: 3px; overflow: hidden; margin-bottom: 4.5mm; background: #1e3a44; }
.banner img { width: 100%; height: 100%; object-fit: cover; display: block; }
.banner .shade { position: absolute; inset: 0;
  background: linear-gradient(90deg, rgba(16,44,54,.92) 0%, rgba(16,44,54,.66) 46%, rgba(16,44,54,.08) 100%); }
.banner .t { position: absolute; left: 6mm; top: 50%; transform: translateY(-50%); color: #fff; }
.banner .t .n { font-size: 7.6pt; letter-spacing: .2em; color: #e8c17a; }
.banner .t h2 { font-size: 17pt; margin-top: .6mm; text-shadow: 0 1px 5px rgba(0,0,0,.4); }
.banner .t .s { font-size: 8.4pt; opacity: .9; margin-top: 1.2mm; }
.banner .cr { position: absolute; right: 2mm; bottom: 1.2mm; font-size: 5.6pt; color: rgba(255,255,255,.7); }

.block { margin-bottom: 4mm; page-break-inside: avoid; }
.bt { font-size: 9.4pt; font-weight: 700; color: #14323d; margin-bottom: 1.8mm;
  border-left: 3px solid #c8862b; padding-left: 2.2mm; }

/* ---------------- tables ---------------- */
table { width: 100%; border-collapse: collapse; font-size: 8pt; }
th { background: #eef3f4; color: #14323d; text-align: left; font-weight: 700;
  padding: 1.4mm 1.9mm; border: .5px solid #d3dee1; font-size: 7.6pt; }
td { padding: 1.4mm 1.9mm; border: .5px solid #e1e9eb; vertical-align: top; }
tr:nth-child(even) td { background: #fafcfc; }
td.t { white-space: nowrap; font-weight: 700; color: #1e3a44; width: 22mm; }
td.n { white-space: nowrap; text-align: right; width: 24mm; }

/* ---------------- pills ---------------- */
.pill { display: inline-block; padding: .35mm 1.5mm; border-radius: 2px; font-size: 6.8pt;
  font-weight: 700; letter-spacing: .03em; vertical-align: middle; white-space: nowrap; }
.p-yes  { background: #2f6b4f; color: #fff; }
.p-no   { background: #a33b2a; color: #fff; }
.p-maybe{ background: #c8862b; color: #fff; }
.p-free { background: #1c5668; color: #fff; }
.p-unv  { background: #eef3f4; color: #6b7f86; border: .5px solid #c3d2d6; }

/* ---------------- callouts ---------------- */
.warn { background: #fdf4ec; border-left: 3px solid #c8791f; padding: 2.2mm 2.8mm;
  font-size: 7.8pt; border-radius: 0 2px 2px 0; margin-top: 2mm; }
.warn b { color: #8a4d2e; }
.note { background: #eef4f5; border-left: 3px solid #1c5668; padding: 2.2mm 2.8mm;
  font-size: 7.8pt; border-radius: 0 2px 2px 0; margin-top: 2mm; }
.kill { background: #fbeeec; border-left: 3px solid #a33b2a; padding: 2.2mm 2.8mm;
  font-size: 7.8pt; border-radius: 0 2px 2px 0; margin-top: 2mm; }
.kill b { color: #a33b2a; }

/* ---------------- cards & photos ---------------- */
.cards { display: grid; grid-template-columns: repeat(3,1fr); gap: 3mm; }
.card { background: #f7fafa; border: 1px solid #dde7e9; border-radius: 3px; padding: 2.6mm 3mm; }
.card .h { font-size: 9pt; font-weight: 700; color: #14323d; }
.card .m { font-size: 7.6pt; color: #4b6068; margin-top: 1mm; }
.card .p { font-size: 11pt; font-weight: 700; color: #c8862b; margin-top: 1.4mm; }

.strip { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; gap: 2mm; margin: 3mm 0; }
.strip .s { position: relative; height: 26mm; border-radius: 2.5px; overflow: hidden; background: #eef3f4; }
.strip .s img { width: 100%; height: 100%; object-fit: cover; display: block; }
.strip .s .cap { position: absolute; left: 0; right: 0; bottom: 0; padding: 4mm 1.8mm 1.2mm; color: #fff;
  font-size: 6.6pt; line-height: 1.25;
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.74) 100%); }

.figure { float: right; width: 58mm; margin: 0 0 3mm 4mm; }
.figure img { width: 100%; height: 40mm; object-fit: cover; border-radius: 3px; display: block; }
.figure .cap { font-size: 6.6pt; color: #6b7f86; margin-top: 1mm; }

/* ---------------- timeline ---------------- */
.tl { width: 100%; border-collapse: collapse; font-size: 8pt; }
.tl td { border: none; border-bottom: .5px solid #e6eef0; padding: 1.6mm 2mm; }
.tl td.time { white-space: nowrap; font-weight: 700; color: #1c5668; width: 20mm; }
.tl tr.hi td { background: #fdf4ec; }
.tl tr.hi td.time { color: #8a4d2e; }

.small { font-size: 7.2pt; color: #6b7f86; }
.big { font-size: 12pt; font-weight: 700; color: #14323d; }
ul.tight { margin: 1mm 0 0; padding-left: 4.5mm; }
ul.tight li { margin-bottom: .8mm; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
.credits { display: grid; grid-template-columns: repeat(3,1fr); gap: 2.4mm; }
.credits .k { font-size: 6.6pt; line-height: 1.3; color: #4b6068; }
.credits .k img { width: 100%; height: 20mm; object-fit: cover; border-radius: 2px; display: block; margin-bottom: 1mm; }
.credits .k b { color: #14323d; display: block; }
.credits .k .u { color: #7d9099; word-break: break-all; font-size: 5.6pt; }
"""
