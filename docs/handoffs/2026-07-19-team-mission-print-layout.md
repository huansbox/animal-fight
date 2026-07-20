# 2026-07-19 團隊任務實體卡接手文件

## 接手結論

v0.7 寶物／後援／三區卡、DM 專注模式與正式 4 張揭露卡均已完成。單動物 `96mm` 屬性間距與雙動物版面已確認，直向資訊層級已遷移回正式兩頁 PDF 並通過逐頁畫面 QA。下一個 session 不要從規則或揭露卡版面重新討論；直接進行黑白試印與第一局真人測試。

目前 branch：`feat/team-mission-props-prototype`

目前正式進度已提交到此 branch；開始新工作前仍應先用 `git status` 核對工作目錄。

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

使用者已明確確認雙動物版與單動物 `96mm` 置中版「看起來 ok」。兩種版面均已遷移到正式 4 張揭露卡。

## 揭露卡檔案狀態

### 正式列印檔

- HTML：[`../../card/storm-forest-rescue-reveal-cards-half-label.html`](../../card/storm-forest-rescue-reveal-cards-half-label.html)
- PDF：[`../../output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf`](../../output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf)
- 內容：2 頁 A4、每頁 2 張，共 4 張正式揭露卡；卡面皆為實際 `170×118.5mm`。
- 狀態：已重建注音字型 subset，PDF 頁數／A4 尺寸與逐頁 render QA 均通過，等待黑白雷射試印。

### 版面測試紀錄

- HTML：[`../../card/reveal-card-stacked-layout-prototype.html`](../../card/reveal-card-stacked-layout-prototype.html)
- PDF：[`../../output/pdf/reveal-card-stacked-layout-prototype-a4.pdf`](../../output/pdf/reveal-card-stacked-layout-prototype-a4.pdf)
- 內容：1 頁 A4，上半張測單動物、下半張測雙動物；卡面皆為實際 `170×118.5mm`。
- Dropbox prototype：`/Users/linshuhuan/Library/CloudStorage/Dropbox/handoff/animal-fight/reveal-card-stacked-layout-prototype-a4.pdf`
- 此檔只保留版面測試紀錄，正式列印請使用上一節的完整兩頁 PDF。
- [`../../card/reveal-card-requirement-ab-comparison.html`](../../card/reveal-card-requirement-ab-comparison.html) 與對應 PDF 是早期比例比較稿，只保留為歷史參考。

## 下一個 session 的執行順序

1. 用黑白雷射、`100%`／「實際大小」列印 2 頁狀態／區域卡與 2 頁正式揭露卡。
2. 沿揭露卡虛線裁切，確認貼到放大版 Poker 後的安全邊界與實際閱讀距離。
3. 跑第一局真人測試，記錄寶物操作、Boss 骰池、後援前／後勝負、孩子理解度與 DM 負擔。
4. 依試印與實玩結果決定是否只做小幅字級／間距修正；沒有實體問題就不再重開版面。
5. 之後製作 16–24 隻 V2 安全牌動物首批。

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
