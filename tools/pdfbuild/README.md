# 行程 PDF 產生器

重新生成 `格魯吉亞亞美尼亞-完整行程.pdf`：

```bash
cd tools/pdfbuild
python3 build.py                     # → itinerary.html
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$CHROME --headless --disable-gpu --no-sandbox --allow-file-access-from-files \
        --virtual-time-budget=15000 --print-to-pdf=$PWD/itinerary.pdf \
        --no-pdf-header-footer file://$PWD/itinerary.html
```

需要 CJK 字體（`fonts-noto-cjk`）同 Chromium。

| 檔案 | 內容 |
|---|---|
| `data_core.py` | 航班、訂單、租車、TO-DO、實用資料 |
| `data_days.py` | 17 日逐日內容（時間表／行車段／住宿／三餐／景點） |
| `render.py` | HTML 片段產生器（表格、pill、酒店卡、`**粗體**` 轉換） |
| `style.py` | 列印用 CSS（A4、封面、日程版面） |
| `images.py` | 相片對應表：封面、行程一覽、每日 hero／小相、section banner、中文 caption |
| `img/*.jpg` | 38 張真實 CC 授權相片（1000px）；`img/t/` 係 480px 縮圖（小相／來源頁用） |
| `img/credits.json` | 每張相嘅作者、授權、來源連結 → 自動產生最後一頁「相片來源」 |
| `build.py` | 主程式：組裝全部 section |

座標總表由 `../../file13-pins.csv` 讀入，再加上新訂酒店。

## 相片

全部相片由 Openverse（Flickr CC BY／CC BY-SA）同 Wikimedia Commons 搵返嚟，冇 AI 生成。
換相：將新 JPG 放入 `img/`（寬 1000px）、`img/t/`（寬 480px），
喺 `credits.json` 加一條 `{artist, license, src, landing}`，再喺 `images.py` 加 caption 同對應日子。
