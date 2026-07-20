# Animal Fight 最新接手文件

> 更新：2026-07-20
> Branch：`feat/team-mission-props-prototype`
> 狀態：首批 16 張 V2 動物卡與團隊任務 v0.7 實體測試包皆已完成數位製作及畫面 QA；下一步只做實際黑白試印與真人實玩驗證

## 接手後先做什麼

先向使用者確認兩件事，不要直接擴充剩餘 116 張，也不要重新設計已定案版面：

1. 首批 16 張 V2 動物卡是否已用 A4 二分標籤、`100%`／「實際大小」、600 dpi 黑白列印。
2. 放大版 Poker 是否已到貨，以及是否已量到實際長寬。

若尚未列印或 Poker 尚未到貨，等待實物；可協助整理記錄表，但不要因數位畫面推測貼合結果。

## 這個 session 已完成

### 首批 16 張 V2 動物卡

- 最終 16 張：非洲獅、非洲象、獵豹、灣鱷、紅袋鼠、長頸鹿、海獺、皇帝企鵝、大熊貓、河豚、紅毛猩猩、黑豹、變色龍、蜂鳥、金剛鸚鵡、行軍蟻。
- 4 張 V2 定錨圖保留，12 張新圖完成；Prompt 與生成圖均經能力動作、物種解剖、構圖／黑白印刷／兒童適性三面向審核。
- 灣鱷重生後改為頭尾近水平、腹面朝觀者的死亡翻滾；紅袋鼠與變色龍移除速度線；金剛鸚鵡縮小置中以保留長尾。
- HTML：[`../../card/animal-cards-v2-first-16-half-label.html`](../../card/animal-cards-v2-first-16-half-label.html)
- Prompt／QA：[`../../card/img-prompt/animal-print-v2-first-16.md`](../../card/img-prompt/animal-print-v2-first-16.md)
- JSONL：[`../../card/img-prompt/animal-print-v2-first-16.jsonl`](../../card/img-prompt/animal-print-v2-first-16.jsonl)
- 正式 PDF：[`../../output/pdf/animal-fight-v2-first-16-half-label-a4.pdf`](../../output/pdf/animal-fight-v2-first-16-half-label-a4.pdf)
- 日期版詳細紀錄：[`2026-07-20-animal-v2-first-16.md`](2026-07-20-animal-v2-first-16.md)
- Dropbox：`/Users/linshuhuan/Library/CloudStorage/Dropbox/handoff/animal-fight/animal-fight-v2-first-16-half-label-a4.pdf`

PDF 為 8 頁 A4 橫式，每頁 2 張；卡面 `118.5×170mm`，置中於 A4 二分標籤。字型已嵌入、圖片與屬性圖約 300 ppi，8 頁 render QA 均無裁切、重疊、缺字或空白頁。

`card/images/` 內的 16 張原始 PNG 為 `1536×1024`，依既有 `.gitignore` 不進版控；同一 workspace 內仍保留，勿刪除。跨機器只有 Prompt、HTML 與已完成 PDF 會由 Git 提供。

### 團隊任務 v0.7 實體測試包

- 3 張寶物、2 張後援、待命／再挑戰／休息三區卡與 4 張大型揭露卡已完成。
- 狀態／區域 PDF：[`../../output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf`](../../output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf)
- 正式揭露卡 PDF：[`../../output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf`](../../output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf)
- DM 專注模式：[`../../game/dm/`](../../game/dm/)
- 日期版詳細紀錄：[`2026-07-19-team-mission-print-layout.md`](2026-07-19-team-mission-print-layout.md)

揭露卡的直向閱讀順序、單動物 `96mm` 屬性組與雙動物版面都已由使用者確認並遷移到正式 PDF。不要回頭使用 prototype 或早期 A／B 比較稿當正式列印檔。

## 已確認的注音決策

- 「骰子」正式卡面維持 `ㄊㄡˊ ˙ㄗ`。
- 這是[教育部《國語辭典簡編本》](https://dict.concised.moe.edu.tw/dictView.jsp?ID=10343&la=0&powerMode=0)的正式讀音；`ㄕㄞˇ ˙ㄗ` 是日常常見讀法，但本案不新增 override。
- 注音來源、IVS 與例外政策見 [`../../card/fonts/bopomofo/README.md`](../../card/fonts/bopomofo/README.md) 及 [`../../card/data/bopomofo-overrides.json`](../../card/data/bopomofo-overrides.json)。

## 下一輪實體驗證

### 動物卡

1. 量測裁切後是否為 `118.5×170mm`，再與 Poker 實物比較四周內縮。
2. 正常桌面距離檢查動物名、屬性、技能與注音是否清楚。
3. 優先觀察長頸鹿淺灰動態尾跡、灣鱷腹面翻滾、紅毛猩猩抓握足、行軍蟻群體語意。
4. 用 16 張跑一次完整淘汰賽，記錄孩子能否只看圖片說出動物與能力。
5. 只有實體結果顯示問題時才調整對比、構圖、字級或卡面內縮；使用者確認後再擴充剩餘 116 張。

### 團隊任務

1. 黑白列印 2 頁四分狀態／區域卡與 2 頁二分正式揭露卡。
2. 跑第一局真人測試，記錄寶物操作、Boss 原始骰池、後援前／後勝負、孩子理解度與 DM 負擔。
3. 沒有實體問題就不重新開版面設計，只依證據做小幅修正。

## 列印設定

- 黑白雷射、A4。
- 動物卡與揭露卡使用二分標籤；狀態／區域卡使用四分標籤。
- 縮放固定 `100%`／「實際大小」，不要選「符合頁面」。
- 建議 600 dpi；現有圖片有效解析度約 300 ppi，1200 dpi 不會增加圖片細節。

## Git 狀態與既有提交

- 工作 branch：`feat/team-mission-props-prototype`
- `00d9eaf feat(cards): finalize team mission reveal cards`
- `5394b65 feat(cards): define first 16 V2 animal artworks`
- `504fa34 feat(cards): build first 16 animal print sheets`
- 接手時先執行 `git status -sb`，確認 branch 已與 remote 同步且沒有使用者未提交修改。

## 常用指令

```bash
open output/pdf/animal-fight-v2-first-16-half-label-a4.pdf
open output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf
open output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf
git status -sb
```

本 session 已關閉 PDF 預覽用的本機 HTTP server，沒有需要接手的背景程序。
