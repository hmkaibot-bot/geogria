// Georgia + Armenia motorcycle trip — PowerPoint generator
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const SCRATCH = "/tmp/claude-0/-home-user-geogria/5ffd1c7e-856a-5a03-853a-f91f25484244/scratchpad";
const PDFDIR = path.join(__dirname, "..", "pdfbuild");
const IMG = path.join(PDFDIR, "img");
const QR = path.join(IMG, "qr");
const D = JSON.parse(fs.readFileSync(path.join(__dirname, "deck.json"), "utf8"));

// ---------- palette ----------
const INK = "1D3B34";        // deep forest — dominant
const INK2 = "2E4A43";
const AMBER = "D59A3C";      // accent
const PAPER = "FFFFFF";
const MIST = "EEF2F0";       // light green tint
const MIST2 = "F6F9F7";
const TEXT = "23302C";
const MUTED = "6B7A74";
const WARN = "8A4D2E";
const WARNBG = "FDF4EC";

const FONT = "Microsoft JhengHei";
const W = 13.333, H = 7.5;

function img(key) { return path.join(IMG, key + ".jpg"); }
function hasImg(key) { return key && fs.existsSync(img(key)); }
function qr(name) { const p = path.join(QR, name + ".png"); return fs.existsSync(p) ? p : null; }
function cap(key) { return D.captions[key] || ""; }
function credit(key) {
  const c = D.credits[key] || {};
  return [(c.artist || "").trim(), c.license || ""].filter(Boolean).join(" · ");
}

// --- crude but reliable text metrics for CJK+latin mix ---
function units(txt) {
  let u = 0;
  for (const ch of String(txt)) u += /[\x00-\xff]/.test(ch) ? 0.55 : 1;
  return u;
}
function estLines(txt, fs, wIn) {
  const perLine = Math.max(6, Math.floor((wIn * 72) / fs));
  let u = 0;                       // slightly heavier weights than clip(): boxes may grow, never clip
  for (const ch of String(txt)) u += /[\x00-\xff]/.test(ch) ? 0.58 : 1;
  return Math.max(1, Math.ceil((u * 1.12) / perLine));
}
function lineH(fs) { return (fs * 1.42) / 72; }
function clip(txt, maxUnits) {
  if (units(txt) <= maxUnits) return txt;
  let u = 0, out = "";
  for (const ch of String(txt)) {
    u += /[\x00-\xff]/.test(ch) ? 0.55 : 1;
    if (u > maxUnits - 1) break;
    out += ch;
  }
  return out.replace(/[·，、（(\s]+$/, "") + "…";
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "King Yip Lo";
pres.title = "格魯吉亞 · 亞美尼亞 電單車之旅 2026";

// ---------- reusable bits ----------
function pageTitle(s, title, kicker) {
  const fsize = units(title) > 14 ? 24 : units(title) > 9 ? 28 : 32;
  s.addText(title, { x: 0.6, y: 0.42, w: 8.6, h: 0.62, fontFace: FONT, fontSize: fsize, bold: true,
    color: INK, isTextBox: true, margin: 0, valign: "middle" });
  if (kicker) s.addText(kicker, { x: 0.6, y: 1.04, w: 9.6, h: 0.34, fontFace: FONT, fontSize: 12,
    color: MUTED, isTextBox: true, margin: 0, valign: "middle" });
}

function dayChip(s, text, x, y) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w: 1.18, h: 0.36, fill: { color: AMBER },
    rectRadius: 0.06, line: { color: AMBER } });
  s.addText(text, { x, y, w: 1.18, h: 0.36, fontFace: FONT, fontSize: 12, bold: true,
    color: PAPER, align: "center", valign: "middle", isTextBox: true, margin: 0 });
}

function photo(s, key, x, y, w, h, opts = {}) {
  if (!hasImg(key)) return;
  s.addImage({ path: img(key), x, y, w, h, sizing: { type: "cover", w, h },
    shadow: { type: "outer", blur: 10, offset: 2, angle: 90, color: "000000", opacity: 0.22 } });
  if (opts.caption !== false) {
    s.addText(cap(key), { x, y: y + h + 0.06, w, h: 0.24, fontFace: FONT, fontSize: 9,
      color: MUTED, isTextBox: true, margin: 0, valign: "top" });
  }
}

function creditLine(s, keys) {
  const txt = "📷 " + keys.filter(hasImg).map(k => cap(k) + "（" + credit(k) + "）").join("　·　");
  s.addText(txt, { x: 0.6, y: H - 0.42, w: W - 1.2, h: 0.26, fontFace: FONT, fontSize: 7,
    color: MUTED, isTextBox: true, margin: 0, valign: "middle" });
}

// =====================================================================
// 1. COVER
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addImage({ path: img(D.overview ? "ge_gergeti" : "ge_gergeti"), x: 0, y: 0, w: W, h: H,
    sizing: { type: "cover", w: W, h: H } });
  s.addImage({ path: path.join(__dirname, "scrim.png"), x: 0, y: 0, w: W, h: H });

  s.addText("I T I N E R A R Y　2 0 2 6", { x: 0.85, y: 4.26, w: 7, h: 0.3, fontFace: FONT,
    fontSize: 11, color: "D9E4DF", charSpacing: 3, isTextBox: true, margin: 0 });
  s.addText("格魯吉亞 · 亞美尼亞\n電單車之旅", { x: 0.85, y: 4.56, w: 8.4, h: 1.5, fontFace: FONT,
    fontSize: 40, bold: true, color: PAPER, lineSpacing: 46, isTextBox: true, margin: 0,
    shadow: { type: "outer", blur: 8, offset: 2, angle: 90, color: "000000", opacity: 0.5 } });
  s.addText("Georgia & Armenia Motorcycle Trip　·　2026年9月25日 – 10月11日（17日）", {
    x: 0.85, y: 6.06, w: 8.6, h: 0.3, fontFace: FONT, fontSize: 13, color: "E6EEEA", isTextBox: true, margin: 0 });

  const facts = [["旅客", "Alex · Hugo"], ["車", "2 × KTM 690"], ["電單車里程", "約 1,500 km"], ["住宿", "14 晚全部已訂"]];
  facts.forEach(([k, v], i) => {
    const x = 0.85 + i * 2.62;
    s.addText(k, { x, y: 6.52, w: 2.4, h: 0.2, fontFace: FONT, fontSize: 8.5, color: AMBER,
      charSpacing: 1.5, isTextBox: true, margin: 0 });
    s.addText(v, { x, y: 6.72, w: 2.4, h: 0.28, fontFace: FONT, fontSize: 12.5, bold: true,
      color: PAPER, isTextBox: true, margin: 0 });
  });
  s.addText("📷 " + cap("ge_gergeti") + "（" + credit("ge_gergeti") + "）", { x: W - 6.0, y: 7.13,
    w: 5.4, h: 0.24, fontFace: FONT, fontSize: 7.5, color: "9BAFA8", align: "right", isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("封面：Gergeti 三一教堂同 Kazbek 山，行程第 5 日會騎上去。");
}

// =====================================================================
// 2. 行程一覽（相片格）
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "行程一覽", "OVERVIEW · 17 日 · 香港 → 吉隆坡 → 多哈 → 格魯吉亞 → 亞美尼亞 → 香港");

  const items = D.overview.filter(o => hasImg(o[3]));
  const cols = 5, cw = 2.36, ch = 1.30, gx = 0.17, gy = 0.62;
  const x0 = 0.6, y0 = 1.62;
  items.forEach((o, i) => {
    const [lab, date, place, key] = o;
    const x = x0 + (i % cols) * (cw + gx);
    const y = y0 + Math.floor(i / cols) * (ch + gy);
    s.addImage({ path: img(key), x, y, w: cw, h: ch, sizing: { type: "cover", w: cw, h: ch },
      shadow: { type: "outer", blur: 8, offset: 2, angle: 90, color: "000000", opacity: 0.18 } });
    s.addShape(pres.ShapeType.roundRect, { x: x + 0.07, y: y + 0.07, w: 0.72, h: 0.26,
      fill: { color: AMBER }, rectRadius: 0.05, line: { color: AMBER } });
    s.addText(lab, { x: x + 0.07, y: y + 0.07, w: 0.72, h: 0.26, fontFace: FONT, fontSize: 9,
      bold: true, color: PAPER, align: "center", valign: "middle", isTextBox: true, margin: 0 });
    s.addText(place, { x, y: y + ch + 0.04, w: cw, h: 0.24, fontFace: FONT, fontSize: 10.5,
      bold: true, color: INK, isTextBox: true, margin: 0, valign: "top" });
    s.addText(date, { x, y: y + ch + 0.26, w: cw, h: 0.2, fontFace: FONT, fontSize: 8.5,
      color: MUTED, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addNotes("每格一個階段，相片全部係真實 Creative Commons 授權相，來源見最後一頁。");
}

// =====================================================================
// 3. 重點數字
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addText("一眼睇晒", { x: 0.6, y: 0.5, w: 6, h: 0.6, fontFace: FONT, fontSize: 32, bold: true,
    color: PAPER, isTextBox: true, margin: 0, valign: "middle" });
  s.addText("BY THE NUMBERS", { x: 0.6, y: 1.1, w: 6, h: 0.3, fontFace: FONT, fontSize: 11,
    color: AMBER, charSpacing: 2.5, isTextBox: true, margin: 0 });

  const stats = [
    ["17", "日", "香港出發、香港返"],
    ["8", "日電單車", "29/9 – 6/10 · 格魯吉亞"],
    ["1,500", "km", "電單車里程（另包車 400 km）"],
    ["2,623", "m", "最高點 Zagari 山口"],
    ["14", "晚", "住宿全部已訂"],
    ["72", "個座標", "可匯入 Google My Maps"],
  ];
  const cw = 3.86, ch = 2.06, gx = 0.3, gy = 0.3, x0 = 0.6, y0 = 1.76;
  stats.forEach(([n, unit, sub], i) => {
    const x = x0 + (i % 3) * (cw + gx);
    const y = y0 + Math.floor(i / 3) * (ch + gy);
    s.addShape(pres.ShapeType.roundRect, { x, y, w: cw, h: ch, fill: { color: INK2 },
      rectRadius: 0.08, line: { color: "3C5A4E" } });
    s.addText([{ text: n, options: { fontSize: 46, bold: true, color: PAPER } },
               { text: "  " + unit, options: { fontSize: 15, color: AMBER } }],
      { x: x + 0.34, y: y + 0.36, w: cw - 0.6, h: 0.92, fontFace: FONT, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(sub, { x: x + 0.34, y: y + 1.3, w: cw - 0.6, h: 0.5, fontFace: FONT, fontSize: 11.5,
      color: "C3D2CC", isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText("香港 → 吉隆坡 → 多哈 → 第比利斯 → 卡茲別吉 → 卡赫季 → 庫塔伊西 → 斯瓦涅季 → 耶烈萬 → 第比利斯", {
    x: 0.6, y: 6.66, w: W - 1.2, h: 0.34, fontFace: FONT, fontSize: 11, color: "9FB3AC", isTextBox: true, margin: 0, valign: "middle" });
}

// =====================================================================
// 4. 航班
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "機票", "FLIGHTS · Qatar Airways Holidays 套票 + 國泰香港段 + FlyOne");

  const rows = [[
    { text: "日期", options: { bold: true } }, { text: "航班", options: { bold: true } },
    { text: "起飛", options: { bold: true } }, { text: "抵達", options: { bold: true } },
    { text: "航段", options: { bold: true } }, { text: "備註", options: { bold: true } }]];
  D.flights.forEach(f => rows.push([f[0], { text: f[1], options: { bold: true, color: INK } },
    f[2], f[3], f[4] + " → " + f[5], f[6]]));
  s.addTable(rows, { x: 0.6, y: 1.62, w: 8.5, colW: [1.15, 1.05, 0.9, 1.0, 2.5, 1.9],
    fontFace: FONT, fontSize: 10.5, color: TEXT, border: { type: "solid", color: "DCE5E1", pt: 0.5 },
    fill: { color: PAPER }, rowH: 0.34, valign: "middle",
    autoPage: false });

  const f = D.flight_ref;
  const cardX = 9.4, cardW = 3.35;
  s.addShape(pres.ShapeType.roundRect, { x: cardX, y: 1.62, w: cardW, h: 2.5, fill: { color: MIST },
    rectRadius: 0.08, line: { color: "D6DED9" } });
  s.addText("訂位編號", { x: cardX + 0.28, y: 1.82, w: cardW - 0.56, h: 0.24, fontFace: FONT,
    fontSize: 9, color: MUTED, charSpacing: 1.2, isTextBox: true, margin: 0 });
  s.addText(f.booking, { x: cardX + 0.28, y: 2.04, w: cardW - 0.56, h: 0.36, fontFace: FONT,
    fontSize: 19, bold: true, color: INK, isTextBox: true, margin: 0 });
  s.addText("航空公司訂位編號　" + f.airline, { x: cardX + 0.28, y: 2.44, w: cardW - 0.56, h: 0.26,
    fontFace: FONT, fontSize: 11, color: TEXT, isTextBox: true, margin: 0 });
  s.addText(f.paid, { x: cardX + 0.28, y: 2.78, w: cardW - 0.56, h: 0.5, fontFace: FONT,
    fontSize: 10, color: TEXT, isTextBox: true, margin: 0, valign: "top" });
  s.addText("⚠️ 座位同餐飲偏好未指定 — 上 qatarairways.com 用 " + f.airline + " 揀位", {
    x: cardX + 0.28, y: 3.3, w: cardW - 0.56, h: 0.66, fontFace: FONT, fontSize: 9.5, color: WARN,
    isTextBox: true, margin: 0, valign: "top" });

  const trows = [[{ text: "旅客", options: { bold: true } }, { text: "出生日期", options: { bold: true } },
    { text: "機票號碼", options: { bold: true } }]];
  f.tickets.forEach(t => trows.push([t[0], t[1], t[2]]));
  s.addTable(trows, { x: cardX, y: 4.35, w: cardW, colW: [1.05, 1.05, 1.25], fontFace: FONT,
    fontSize: 8, color: TEXT, border: { type: "solid", color: "DCE5E1", pt: 0.5 }, rowH: 0.3, valign: "middle" });

  photo(s, "doha_mia", 0.6, 5.0, 4.1, 1.85, { caption: false });
  photo(s, "kl_petronas", 4.9, 5.0, 4.2, 1.85, { caption: false });
  creditLine(s, ["doha_mia", "kl_petronas"]);
}

// =====================================================================
// 5. 住宿訂單
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "住宿訂單", "BOOKINGS · 14 / 14 晚已訂 · 由 25/9 吉隆坡到 9/10 第比利斯，冇一晚 gap");

  const rows = [[
    { text: "日期", options: { bold: true } }, { text: "酒店", options: { bold: true } },
    { text: "城市", options: { bold: true } }, { text: "晚", options: { bold: true } },
    { text: "平台", options: { bold: true } }, { text: "金額", options: { bold: true } },
    { text: "備註", options: { bold: true } }]];
  D.bookings.forEach(b => {
    const [n, city, dates, nights, plat, ref, amt, note] = b;
    rows.push([{ text: dates, options: { bold: true, color: INK } }, n, city, nights, plat,
      { text: amt, options: { bold: true } }, note]);
  });
  s.addTable(rows, { x: 0.6, y: 1.6, w: W - 1.2, colW: [1.35, 3.15, 1.5, 0.42, 1.35, 1.35, 2.98],
    fontFace: FONT, fontSize: 9.5, color: TEXT, border: { type: "solid", color: "DCE5E1", pt: 0.5 },
    rowH: 0.3, valign: "middle", autoPage: false });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 6.5, w: W - 1.2, h: 0.62, fill: { color: MIST },
    rectRadius: 0.08, line: { color: "C9DACF" } });
  s.addText("仲欠：7/10 GoTrip 包車 · 租車改期 · Landscapes Hotel 訂單編號同金額待補　|　已知已付 ≈ HK$17,650（未計 Agoda 3 晚）", {
    x: 0.9, y: 6.5, w: W - 1.8, h: 0.62, fontFace: FONT, fontSize: 11, color: INK,
    isTextBox: true, margin: 0, valign: "middle" });
}

// =====================================================================
// 6. 租車
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "租車 · SLAVATOUR", "RENTAL · KTM-Georgia（基地就喺 Camp Hotel Pura Vida）· 2 × KTM 690 · 29 Sep – 6 Oct");

  const r = D.rental;
  const items = [["聯絡", r.contact], ["車", r.bikes], ["租期", r.period], ["押金", r.deposit],
    ["保險", r.insurance], ["牌照要求", r.licence], ["亞美尼亞", r.armenia], ["行李", r.luggage]];
  let y = 1.66;
  items.forEach(([k, v]) => {
    s.addText(k, { x: 0.6, y, w: 1.5, h: 0.42, fontFace: FONT, fontSize: 11, bold: true,
      color: INK, isTextBox: true, margin: 0, valign: "top" });
    s.addText(v, { x: 2.15, y, w: 5.5, h: 0.42, fontFace: FONT, fontSize: 10.5, color: TEXT,
      isTextBox: true, margin: 0, valign: "top" });
    y += 0.52;
  });

  photo(s, "ge_zagari", 8.2, 1.66, 4.5, 2.55);
  s.addShape(pres.ShapeType.roundRect, { x: 8.2, y: 4.62, w: 4.5, h: 2.2, fill: { color: WARNBG },
    rectRadius: 0.08, line: { color: "E8CDA9" } });
  s.addText("⚠️ 取車日要做嘅嘢", { x: 8.5, y: 4.78, w: 3.9, h: 0.3, fontFace: FONT, fontSize: 12,
    bold: true, color: WARN, isTextBox: true, margin: 0 });
  s.addText([
    { text: "逐格拍片記錄車身花痕", options: { bullet: true, breakLine: true } },
    { text: "簽約 · 畀 €850 × 2 押金", options: { bullet: true, breakLine: true } },
    { text: "裝軟袋、確認車牌同文件", options: { bullet: true, breakLine: true } },
    { text: "車行 09:00 先開 — 問可唔可以 08:00", options: { bullet: true } },
  ], { x: 8.5, y: 5.12, w: 3.9, h: 1.55, fontFace: FONT, fontSize: 10, color: TEXT,
    isTextBox: true, margin: 0, valign: "top", paraSpaceAfter: 5 });
  creditLine(s, ["ge_zagari"]);
}

// =====================================================================
// 7..23  DAY SLIDES
// =====================================================================
D.days.forEach((d, idx) => {
  const s = pres.addSlide();
  s.background = { color: PAPER };
  const left = idx % 2 === 0;           // alternate photo side
  const colX = left ? 0.6 : 5.35;       // timeline column x
  const artX = left ? 8.45 : 0.6;       // art column x
  const colW = 7.4, artW = 4.28;
  const TOP = 1.06, BOT = H - 0.42;

  // --- header ---
  dayChip(s, d.num, 0.6, 0.4);
  s.addText(d.date + "（" + d.wd + "）", { x: 1.92, y: 0.33, w: 3.0, h: 0.5, fontFace: FONT,
    fontSize: 24, bold: true, color: INK, isTextBox: true, margin: 0, valign: "middle" });
  s.addText(d.route, { x: 4.95, y: 0.37, w: 5.4, h: 0.42, fontFace: FONT,
    fontSize: units(d.route) > 26 ? 11 : 13, color: INK2, isTextBox: true, margin: 0, valign: "middle" });
  s.addText(d.stats.join("　·　"), { x: W - 3.55, y: 0.37, w: 2.95, h: 0.42, fontFace: FONT,
    fontSize: 11, bold: true, color: AMBER, align: "right", isTextBox: true, margin: 0, valign: "middle" });

  // --- timeline table ---
  const rows = [[{ text: "時間", options: { bold: true, color: INK } },
                 { text: "行程", options: { bold: true, color: INK } },
                 { text: "行車", options: { bold: true, color: INK } }]];
  d.sched.forEach(([t, what, ride]) => rows.push([
    { text: t, options: { bold: true, color: INK2 } },
    { text: clip(what, 82), options: {} },
    { text: String(ride || "").replace(/（[^）]*）/g, "").trim(), options: { color: INK2, bold: true } }]));
  const n = d.sched.length;
  const fsz = n >= 14 ? 8.5 : n >= 12 ? 9 : 10;
  const rh = n >= 14 ? 0.29 : n >= 12 ? 0.32 : 0.36;
  s.addTable(rows, { x: colX, y: TOP, w: colW, colW: [0.78, colW - 2.48, 1.7], fontFace: FONT,
    fontSize: fsz, color: TEXT, border: { type: "solid", color: "DCE5E1", pt: 0.5 },
    rowH: rh, valign: "middle", autoPage: false });

  // --- art column, stacked top-down with measured heights ---
  let ay = TOP;
  const GAP = 0.14;
  if (hasImg(d.hero)) {
    const ph = 2.12;
    s.addImage({ path: img(d.hero), x: artX, y: ay, w: artW, h: ph,
      sizing: { type: "cover", w: artW, h: ph },
      shadow: { type: "outer", blur: 10, offset: 2, angle: 90, color: "000000", opacity: 0.22 } });
    s.addText(cap(d.hero), { x: artX, y: ay + ph + 0.03, w: artW, h: 0.22, fontFace: FONT,
      fontSize: 8, color: MUTED, isTextBox: true, margin: 0, valign: "top" });
    ay += ph + 0.28;
  }

  // hotel card — height from measured meta lines
  const ho = d.hotel || {};
  if (ho.name && ho.name !== "—" && ho.name.length > 1) {
    const innerW = artW - 0.44;
    const metaBits = [ho.addr, [ho.ref, ho.price, ho.times].filter(x => x && x !== "—").join(" · ")]
      .filter(Boolean);
    const metaFs = 8;
    let mLines = 0;
    metaBits.forEach(b => { mLines += estLines(b, metaFs, innerW); });
    const nameFs = units(ho.name) > 22 ? 10 : 11.5;
    const nLines = estLines("🏨 " + ho.name, nameFs, innerW);
    const nameH = nLines * lineH(nameFs);
    const hh = 0.16 + nameH + 0.04 + mLines * lineH(metaFs) + 0.12;
    s.addShape(pres.ShapeType.roundRect, { x: artX, y: ay, w: artW, h: hh, fill: { color: MIST },
      rectRadius: 0.08, line: { color: "D6DED9" } });
    s.addText("🏨 " + ho.name, { x: artX + 0.22, y: ay + 0.08, w: innerW, h: nameH + 0.04,
      fontFace: FONT, fontSize: nameFs, bold: true, color: INK, isTextBox: true, margin: 0, valign: "top" });
    s.addText(metaBits.join("\n"), { x: artX + 0.22, y: ay + 0.08 + nameH + 0.04,
      w: innerW, h: mLines * lineH(metaFs) + 0.06, fontFace: FONT, fontSize: metaFs, color: TEXT,
      isTextBox: true, margin: 0, valign: "top" });
    ay += hh + GAP;
  }

  // route QR
  const qrFile = qr(d.num.replace(" ", "")) || qr(d.num.replace(" ", "") + "_1");
  const qh = 0.92;
  if (qrFile && ay + qh <= BOT) {
    s.addShape(pres.ShapeType.roundRect, { x: artX, y: ay, w: artW, h: qh, fill: { color: MIST2 },
      rectRadius: 0.08, line: { color: "D6DED9" } });
    s.addImage({ path: qrFile, x: artX + 0.12, y: ay + 0.1, w: 0.72, h: 0.72 });
    s.addText("🗺 掃我開 Google Maps 路線", { x: artX + 0.96, y: ay + 0.1, w: artW - 1.14, h: 0.26,
      fontFace: FONT, fontSize: 9.5, bold: true, color: INK, isTextBox: true, margin: 0, valign: "middle" });
    const sub = clip([d.mode, d.total_km ? d.total_km + " km" : "", d.total_time].filter(Boolean).join(" · "), 46);
    s.addText(sub, { x: artX + 0.96, y: ay + 0.36, w: artW - 1.14, h: 0.46, fontFace: FONT,
      fontSize: 8, color: MUTED, isTextBox: true, margin: 0, valign: "top" });
    ay += qh + GAP;
  }

  // alerts — fill remaining space, trimmed to fit
  const avail = BOT - ay;
  const aFs = 8;
  if (avail >= 0.46) {
    const maxLines = Math.floor((avail - 0.2) / lineH(aFs));
    const candidates = [];
    d.warns.slice(0, 2).forEach(w => candidates.push("⚠️ " + w));
    if (!candidates.length && d.notes.length) candidates.push("💡 " + d.notes[0]);
    if (d.caveat) candidates.push("🗺 " + d.caveat);
    const picked = [];
    let used = 0;
    for (const c of candidates) {
      const room = maxLines - used;
      if (room <= 0) break;
      const perLine = Math.max(6, Math.floor((artW - 0.4) * 72 / aFs));
      const txt = clip(c, room * perLine);
      picked.push(txt);
      used += estLines(txt, aFs, artW - 0.4);
    }
    if (picked.length) {
      const hgt = Math.min(avail, 0.2 + used * lineH(aFs) + 0.06);
      s.addShape(pres.ShapeType.roundRect, { x: artX, y: ay, w: artW, h: hgt, fill: { color: WARNBG },
        rectRadius: 0.08, line: { color: "E8CDA9" } });
      s.addText(picked.join("\n"), { x: artX + 0.2, y: ay + 0.09, w: artW - 0.4, h: hgt - 0.18,
        fontFace: FONT, fontSize: aFs, color: WARN, isTextBox: true, margin: 0, valign: "top" });
    }
  }

  // speaker notes: full detail that didn't fit on the slide
  const notes = [];
  notes.push(d.sched.map(([t, what]) => t + "　" + what).join("\n"));
  Object.entries(d.meals || {}).forEach(([slot, opts]) => {
    notes.push(slot + "：" + opts.map(o => "[" + o[0] + "] " + o[1] + "（" + o[2] + "）").join("；"));
  });
  if (d.sights.length) notes.push("景點：" + d.sights.map(x => x[1] + "（" + x[2] + "）").join("；"));
  if (d.warns.length) notes.push("提醒：" + d.warns.join("　|　"));
  if (d.maps) notes.push("路線連結：" + d.maps);
  s.addNotes(notes.join("\n\n"));
});

// =====================================================================
// 24. 預約清單
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "仲要訂咩", "RESERVATIONS · 紅色＝真係會冇位，黃色＝到咗先訂都得");

  const now = D.book_now.filter(b => b[0] !== "✅");
  const done = D.book_now.filter(b => b[0] === "✅").concat(D.book_later.filter(b => b[0] === "✅"));

  // left: must book
  s.addText("🔴 而家就要訂", { x: 0.6, y: 1.6, w: 4, h: 0.32, fontFace: FONT, fontSize: 15,
    bold: true, color: "A33B2A", isTextBox: true, margin: 0 });
  let y = 2.0;
  now.slice(0, 8).forEach(b => {
    const [, name, date, how, price] = b;
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 7.4, h: 0.56, fill: { color: MIST2 },
      rectRadius: 0.06, line: { color: "E2E8E5" } });
    s.addText(clip(name, 30), { x: 0.8, y: y + 0.04, w: 4.3, h: 0.26, fontFace: FONT, fontSize: 10.5,
      bold: true, color: INK, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(clip(date, 30), { x: 0.8, y: y + 0.28, w: 4.3, h: 0.24, fontFace: FONT, fontSize: 8.5,
      color: MUTED, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(clip(price, 30), { x: 5.2, y: y + 0.02, w: 2.6, h: 0.52, fontFace: FONT, fontSize: 8.5, color: TEXT,
      align: "right", isTextBox: true, margin: 0, valign: "middle" });
    y += 0.62;
  });

  // right: already booked
  s.addText("✅ 已經訂好", { x: 8.35, y: 1.6, w: 4, h: 0.32, fontFace: FONT, fontSize: 15,
    bold: true, color: "2F6B4F", isTextBox: true, margin: 0 });
  let y2 = 2.0;
  done.slice(0, 6).forEach(b => {
    const [, name, date] = b;
    s.addShape(pres.ShapeType.roundRect, { x: 8.35, y: y2, w: 4.38, h: 0.56, fill: { color: MIST },
      rectRadius: 0.06, line: { color: "C9DACF" } });
    s.addText(clip(name, 28), { x: 8.55, y: y2 + 0.04, w: 4.0, h: 0.26, fontFace: FONT, fontSize: 10.5,
      bold: true, color: INK, isTextBox: true, margin: 0, valign: "middle" });
    s.addText(clip(date, 28), { x: 8.55, y: y2 + 0.28, w: 4.0, h: 0.24, fontFace: FONT, fontSize: 8.5,
      color: MUTED, isTextBox: true, margin: 0, valign: "middle" });
    y2 += 0.62;
  });
  s.addText("其餘餐廳 walk-in 就得 — 詳情見 PDF《預約清單》", { x: 8.35, y: y2 + 0.08, w: 4.38,
    h: 0.3, fontFace: FONT, fontSize: 9.5, color: MUTED, isTextBox: true, margin: 0 });
}

// =====================================================================
// 25. 出發前 TO-DO
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "出發前 TO-DO", "ACTION LIST · 按死線排序");

  const rows = [[{ text: "死線", options: { bold: true, color: INK } },
    { text: "事項", options: { bold: true, color: INK } },
    { text: "點做", options: { bold: true, color: INK } },
    { text: "價", options: { bold: true, color: INK } },
    { text: "備註", options: { bold: true, color: INK } }]];
  D.todo.forEach(t => rows.push([{ text: t[0], options: { bold: true } }, t[1], t[2], t[3], t[4]]));
  s.addTable(rows, { x: 0.6, y: 1.54, w: 8.3, colW: [1.0, 2.45, 1.7, 0.85, 2.3], fontFace: FONT,
    fontSize: 7.5, color: TEXT, border: { type: "solid", color: "DCE5E1", pt: 0.5 }, rowH: 0.24,
    valign: "middle", autoPage: false });

  s.addImage({ path: img("ge_enguri"), x: 9.1, y: 1.54, w: 3.63, h: 2.0,
    sizing: { type: "cover", w: 3.63, h: 2.0 },
    shadow: { type: "outer", blur: 10, offset: 2, angle: 90, color: "000000", opacity: 0.2 } });
  s.addText("📷 " + cap("ge_enguri") + "（" + credit("ge_enguri") + "）", { x: 9.1, y: 3.58,
    w: 3.63, h: 0.22, fontFace: FONT, fontSize: 7, color: MUTED, isTextBox: true, margin: 0, valign: "top" });
  s.addShape(pres.ShapeType.roundRect, { x: 9.1, y: 3.86, w: 3.63, h: 2.9, fill: { color: MIST },
    rectRadius: 0.08, line: { color: "C9DACF" } });
  s.addText("📄 證件 · 保險 · 現金", { x: 9.32, y: 4.02, w: 3.2, h: 0.3, fontFace: FONT,
    fontSize: 12, bold: true, color: INK, isTextBox: true, margin: 0 });
  s.addText([
    { text: "IDP 國際駕駛許可證 ×2（要有 A 類電單車）", options: { bullet: true, breakLine: true } },
    { text: "電單車旅遊保 ×2 — 必須保 >125cc", options: { bullet: true, breakLine: true } },
    { text: "護照有效期到 2027 年 4 月後", options: { bullet: true, breakLine: true } },
    { text: "€1,700 押金（€850 × 2）", options: { bullet: true, breakLine: true } },
    { text: "Mestia 撳定 400–600 GEL 現金（Ushguli 冇 ATM）", options: { bullet: true } },
  ], { x: 9.32, y: 4.4, w: 3.2, h: 2.2, fontFace: FONT, fontSize: 9.5, color: TEXT,
    isTextBox: true, margin: 0, valign: "top", paraSpaceAfter: 6 });
}

// =====================================================================
// 26. 實用資料
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addText("實用資料", { x: 0.6, y: 0.42, w: 6, h: 0.6, fontFace: FONT, fontSize: 32, bold: true,
    color: PAPER, isTextBox: true, margin: 0, valign: "middle" });
  s.addText("PRACTICAL", { x: 0.6, y: 1.04, w: 6, h: 0.3, fontFace: FONT, fontSize: 11,
    color: AMBER, charSpacing: 2.5, isTextBox: true, margin: 0 });

  const rows = [];
  D.practical.forEach(p => rows.push([{ text: p[0], options: { bold: true, color: PAPER } },
    { text: p[1], options: { color: "D5E0DB" } }]));
  s.addTable(rows, { x: 0.6, y: 1.62, w: W - 1.2, colW: [1.9, W - 3.1], fontFace: FONT,
    fontSize: 9.5, border: { type: "solid", color: "3C5A4E", pt: 0.5 }, fill: { color: INK },
    rowH: 0.34, valign: "middle", autoPage: false });

  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 6.28, w: W - 1.2, h: 0.82, fill: { color: "5B3A1E" },
    rectRadius: 0.08, line: { color: "8A4D2E" } });
  s.addText("💵 只收現金：Ushguli 全村 · Cafe Laila（Mestia）· Bikentia's（Kutaisi）· Nunu's（Lentekhi）· Zugdidi 巴刹 · Dry Bridge 市集 · Garni 小檔 · 多哈街邊 karak · KL 小販檔", {
    x: 0.9, y: 6.28, w: W - 1.8, h: 0.82, fontFace: FONT, fontSize: 10, color: "F3E3D2",
    isTextBox: true, margin: 0, valign: "middle" });
}

// =====================================================================
// 27. 相片來源
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  pageTitle(s, "相片來源", "PHOTO CREDITS · 全部真實 Creative Commons 授權相（Flickr 經 Openverse／Wikimedia Commons）");

  const keys = Object.keys(D.credits).sort();
  const col = 3, colw = 4.0, gx = 0.2;
  const per = Math.ceil(keys.length / col);
  keys.forEach((k, i) => {
    const c = D.credits[k] || {};
    const ci = Math.floor(i / per), ri = i % per;
    const x = 0.6 + ci * (colw + gx);
    const y = 1.66 + ri * 0.37;
    s.addText([{ text: (D.captions[k] || k) + "　", options: { bold: true, color: INK } },
               { text: [(c.artist || "").trim(), c.license || ""].filter(Boolean).join(" · "),
                 options: { color: MUTED } }],
      { x, y, w: colw, h: 0.34, fontFace: FONT, fontSize: 7.5, isTextBox: true, margin: 0, valign: "middle" });
  });
  s.addText("本簡報只作私人旅行用途。詳細行程、座標、餐廳同景點見同名 PDF。", {
    x: 0.6, y: H - 0.62, w: W - 1.2, h: 0.3, fontFace: FONT, fontSize: 9.5, color: MUTED,
    isTextBox: true, margin: 0, valign: "middle" });
}

const OUT = path.join(__dirname, "..", "..", "格魯吉亞亞美尼亞-行程簡報.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("written:", OUT));
