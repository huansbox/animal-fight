# 2026-07-19 團隊任務實體卡接手文件

## 接手結論

本 session 已完成 v0.7 寶物／後援／三區卡、DM 專注模式與揭露卡新版面探索。下一個 session 不要從規則重新討論；先確認最新單動物揭露卡的屬性間距，再把已確認的直向資訊層級遷移回正式 4 張揭露卡。

目前 branch：`feat/team-mission-props-prototype`

目前 HEAD：`3182b34 feat(cards): finalize monochrome animal art style`

工作目錄有大量本 session 的已修改與未追蹤檔案，尚未 commit／push。這些都是專案進度，不可用 `git reset --hard`、`git checkout --` 或清理未追蹤檔案。

## 已完成且可延續

### v0.7 規則與劇情

- 三件 Boss 寶物、固定 `2＋2` 成功、後援互動與結算順序已記錄於 [`../plans/2026-07-19-team-mission-v07-treasure-boss-design.md`](../plans/2026-07-19-team-mission-v07-treasure-boss-design.md)。
- 三套固定劇情與共用模板已遷移到 v0.7。
- DM 專注模式 Web App 位於 [`../../game/dm/`](../../game/dm/)，可部署到 Cloudflare Pages。

### 寶物、後援與三區卡

- 正式來源：[`../../card/team-mission-status-cards-quarter-label.html`](../../card/team-mission-status-cards-quarter-label.html)
- 列印 PDF：[`../../output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf`](../../output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf)
- 共 2 頁 A4 四分標籤：3 寶物、2 後援、待命／再挑戰／休息。
- 三區卡統一保留四周 `5mm` 安全邊界；待命實線、再挑戰虛線、休息點線。
- 狀態卡與區域卡已完成畫面 QA，下一步是黑白雷射實際列印。

### 揭露卡情境圖

- 情境圖位於 [`../../card/mission-art/storm-forest-rescue/`](../../card/mission-art/storm-forest-rescue/)。
- 使用與動物圖片 V2 相容的五階灰階、中粗輪廓、適合黑白雷射列印風格。
- 屬性小圖使用 [`../../card/attribute-illustrations/`](../../card/attribute-illustrations/)，不是舊版 icon。

## 揭露卡最新對齊結果

固定閱讀順序：

1. 情境圖片。
2. 一句白話原因。
3. 需求數字。
4. 兩個可選屬性。

目前視覺決議：

- 不使用橫向分隔線。
- 不寫 `4-6` 或 `4 - 6`，直接列出 `4、5、6`；另外兩組同理為 `1、2、3`、`7、8、9`。
- 數字放在置中的淺灰圓角牌內。
- 兩個屬性不加個別外框，中間用小型黑底「或」表示選擇。
- 屬性圖片在上，屬性名稱與注音在正下方，與動物卡片一致。
- 單動物屬性整組置中、寬度限制為 `96mm`，避免左右距離過遠。
- 雙動物 2A／2B 各自保留工作名稱、原因、數字牌與兩個屬性。

使用者已明確表示雙動物版「看起來 ok」。單動物版先被指出屬性距離太遠，已改為 `96mm` 置中，但調整後尚未得到下一次明確確認。

## 揭露卡檔案狀態

### 最新候選

- HTML：[`../../card/reveal-card-stacked-layout-prototype.html`](../../card/reveal-card-stacked-layout-prototype.html)
- PDF：[`../../output/pdf/reveal-card-stacked-layout-prototype-a4.pdf`](../../output/pdf/reveal-card-stacked-layout-prototype-a4.pdf)
- 內容：1 頁 A4，上半張測單動物、下半張測雙動物；卡面皆為實際 `170×118.5mm`。
- Dropbox：`/Users/linshuhuan/Library/CloudStorage/Dropbox/handoff/animal-fight/reveal-card-stacked-layout-prototype-a4.pdf`

### 不要誤認為最新版

- [`../../card/storm-forest-rescue-reveal-cards-half-label.html`](../../card/storm-forest-rescue-reveal-cards-half-label.html) 與 [`../../output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf`](../../output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf) 仍是較早版面，尚未套用最新直向資訊層級。
- [`../../card/reveal-card-requirement-ab-comparison.html`](../../card/reveal-card-requirement-ab-comparison.html) 與對應 PDF 是早期比例比較稿，只保留為歷史參考。

## 下一個 session 的執行順序

1. 先讓使用者開啟最新 prototype，確認單動物 `96mm` 屬性間距。
2. 若確認，將 `reveal-card-stacked-layout-prototype.html` 的需求區結構與 CSS 遷移到 `storm-forest-rescue-reveal-cards-half-label.html`。
3. 套用到全部 4 張卡：任務簡報／Boss 預告、第一關單動物、第二關雙動物、第三關單動物。
4. Boss A／B 與 2A／2B 必須各自保留工作名稱和一句原因。
5. 重建注音字型 subset，因正式揭露卡文字 corpus 會變更。
6. 重新產生正式 2 頁 PDF，render 每頁 PNG，檢查裁切、注音、數字牌、屬性間距與雙工作密度。
7. 將正式 PDF 複製到 Dropbox handoff，再進行黑白雷射試印。
8. 揭露卡定案後，再做 16–24 隻 V2 安全牌動物首批。

## 常用指令

開啟最新 prototype：

```bash
open output/pdf/reveal-card-stacked-layout-prototype-a4.pdf
```

重建全卡注音 subset：

```bash
uv run --with-requirements card/requirements-fonts.txt python card/build_bopomofo_fonts.py --offline
```

從 HTML 產生 prototype PDF：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --disable-gpu \
  --allow-file-access-from-files \
  --no-pdf-header-footer \
  --print-to-pdf="output/pdf/reveal-card-stacked-layout-prototype-a4.pdf" \
  "file:///Users/linshuhuan/mywork/animal-fight/card/reveal-card-stacked-layout-prototype.html"
```

Render PDF 供畫面 QA：

```bash
mkdir -p tmp/pdfs/reveal-stacked-layout
pdftoppm -png -r 150 \
  output/pdf/reveal-card-stacked-layout-prototype-a4.pdf \
  tmp/pdfs/reveal-stacked-layout/page
```

DM App 如需本機預覽：

```bash
python -m http.server 8765
# http://localhost:8765/game/dm/
```

本 session 結束前已關閉 Port `8765` 與 `8931` 的背景預覽 server。

## 驗收重點

- 黑白雷射、A4、`100%`／「實際大小」。
- 卡面外框與虛線裁切框不能超出標籤安全範圍。
- 單動物的兩個屬性不能重新散到卡面左右兩端。
- 雙動物資訊密度不能壓縮到屬性名稱或注音被裁切。
- `1、2、3`／`4、5、6`／`7、8、9` 必須比說明文字更醒目。
- 圖片、文字、數字、屬性的閱讀順序不可改回左右雙欄。
