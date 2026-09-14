# 多哈 Local Tour PDF 產生器

重新生成 `多哈local-tour-完整選項.pdf`：

```bash
cd tools/dohapdf
python3 build.py                     # → doha.html
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
$CHROME --headless --disable-gpu --no-sandbox --allow-file-access-from-files \
        --virtual-time-budget=20000 --print-to-pdf=$PWD/doha.pdf \
        --no-pdf-header-footer file://$PWD/doha.html
cp doha.pdf ../../多哈local-tour-完整選項.pdf
```

需要 CJK 字體（`fonts-noto-cjk`）同 Chromium。

| 檔案 | 內容 |
|---|---|
| `build.py` | 全部內容 + 版面（15 頁：封面、快速結論、8 個分類、27/9 同 28/9 方案、唔值得去／死線、已核實／未核實、相片來源） |
| `style.py` | 列印用 CSS（A4、封面漸變、banner、卡片、pill、時間表） |
| `img/*.jpg` | 18 張真實 CC 授權相（Openverse／Flickr、Wikimedia Commons） |
| `img/credits.json` | 每張相嘅作者、授權、來源連結 → 自動產生最後一頁 |

內容來源：`../../24-多哈local-tour選項.md`（2026-09-13 查核）。
改內容就改 `build.py` 入面對應嘅 section；改完重新產生 PDF。

## 換相

放新 JPG 入 `img/`（寬 1000–1400px），喺 `credits.json` 加一條
`{artist, license, src, landing}`，再喺 `build.py` 嘅 `CAPTION` 加中文說明。
