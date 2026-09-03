# 行程 PDF 產生器

重新生成 `格魯吉亞亞美尼亞-完整行程.pdf`：

```bash
cd tools/pdfbuild
python3 build.py                     # → itinerary.html
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$CHROME --headless --disable-gpu --no-sandbox --virtual-time-budget=8000 \
        --print-to-pdf=itinerary.pdf --no-pdf-header-footer itinerary.html
```

需要 CJK 字體（`fonts-noto-cjk`）同 Chromium。

| 檔案 | 內容 |
|---|---|
| `data_core.py` | 航班、訂單、租車、TO-DO、實用資料 |
| `data_days.py` | 17 日逐日內容（時間表／行車段／住宿／三餐／景點） |
| `render.py` | HTML 片段產生器（表格、pill、酒店卡、`**粗體**` 轉換） |
| `style.py` | 列印用 CSS（A4、封面、日程版面） |
| `build.py` | 主程式：組裝全部 section |

座標總表由 `../../file13-pins.csv` 讀入，再加上新訂酒店。
