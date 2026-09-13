# 行程簡報（PowerPoint）產生器

重新生成 `格魯吉亞亞美尼亞-行程簡報.pptx`：

```bash
cd tools/pdfbuild && python3 export_deck.py     # → deck.json（由 data_days / data_core / images / routes.json 匯出）
cd ../pptbuild && npm install pptxgenjs && node build_deck.js
```

`build_deck.js` 由 `deck.json` 砌出 27 頁：封面、行程一覽、重點數字、機票、住宿訂單、
租車、17 日逐日、預約清單、TO-DO、實用資料、相片來源。相片同 QR code 直接讀
`tools/pdfbuild/img/`，所以改 PDF 嗰邊嘅相就會一齊改。

`scrim.png` 係封面用嘅漸變遮罩（PowerPoint 唔支援 gradient fill，所以用圖）。

檢查：

```bash
python3 <skills>/pptx/scripts/office/validate.py 格魯吉亞亞美尼亞-行程簡報.pptx
soffice --headless --convert-to pdf 格魯吉亞亞美尼亞-行程簡報.pptx && pdftoppm -jpeg -r 100 ...
```
