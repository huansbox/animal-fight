# Animal Fight 最新接手文件

> 更新：2026-07-21
> Branch：`feat/animal-ability-audit`
> 狀態：P0／P1／格式修訂已寫回 132 隻正式資料；注音字型、文字 QA 與首批 16 張 PDF 已重建並通過畫面檢查

## 接手後先做什麼

不要直接擴充剩餘 116 張，也不要覆蓋現有 16 張正式圖片。依序進行：

1. 先讀 [`../plans/2026-07-21-animal-skill-description-audit.md`](../plans/2026-07-21-animal-skill-description-audit.md)，沿用已定案的能力與 `artAction` 原則。
2. 重印一頁 `117×170mm`，確認新版文案與貼合容錯；等孩子有空再用現有 16 張 V2.0 跑完整淘汰賽。
3. 實體驗證沒有問題後，才逐波建立剩餘 116 張 V2.0 Prompt；圖片風格不再重開選型。

目前手邊沒有 Poker 可重新量測，先依標示尺寸 `122×175mm` 計算；日後有實物時仍需量 3–5 張並取最小長寬。

## 這個 session 已完成

### 132 隻特殊能力描述審核

- 新增 [`../../card/audit_animal_skills.py`](../../card/audit_animal_skills.py)，掃描四字技能名、15–25 字描述、複合動作、外部角色、群體依賴、暴力字詞、抽象效果與誇張語句。
- 修訂前 132 隻中有 10 隻格式問題、102 隻命中至少一項 Prompt 風險候選；正式寫回後四字技能名與 15–25 字描述問題均歸零，Prompt 風險候選降為 77 隻。
- P0 核心能力與 P1 兒童文案已由兒童文案、`artAction`／V2.0 相容性、臺灣用語／物種 plausibility 三個角度獨立 review，整併結果已同步至正式資料、卡面、規則表與相關 Prompt，詳見 [`../plans/2026-07-21-animal-skill-description-audit.md`](../plans/2026-07-21-animal-skill-description-audit.md)。
- 生圖 SOP 新增 `artAction`：`skillDesc` 不再直接餵給模型，先收斂為一個可見動作、單一瞬間與必要物件。
- 使用者確認原意是臺灣常見眼鏡蛇；正式資料已改為 `id=chinese_cobra`、英文 `Chinese Cobra`、中文維持「眼鏡蛇」。`Cobra` 是泛稱，`King Cobra` 則是不同物種「眼鏡王蛇」。本機被 `.gitignore` 排除的數位版圖片也已改名為 `card/images-realistic/chinese_cobra.png`；其他既有 workspace 若仍保留舊檔，需自行做相同 rename。
- 注音 corpus 與 Bold／Medium subset 已依新版文字重建；正式 QA 為 132 隻、83 個 IVS、6 個人工注音、23 頁、溢出 0。首批 16 張 PDF 維持 8 頁 A4 橫式，逐頁畫面抽查無裁切、重疊、缺字或空白頁。
- 對齊大對決逐骰天賦規則：相同最終骰面仍各算一次命中加成，多次骰到 6 再依觸發次數疊加。數位版已修正並有 regression test。

### 首批 16 張 V2 動物卡

- 最終 16 張：非洲獅、非洲象、獵豹、灣鱷、紅袋鼠、長頸鹿、海獺、皇帝企鵝、大熊貓、河豚、紅毛猩猩、黑豹、變色龍、蜂鳥、金剛鸚鵡、行軍蟻。
- 4 張 V2 定錨圖保留，12 張新圖完成；Prompt 與生成圖均經能力動作、物種解剖、構圖／黑白印刷／兒童適性三面向審核。
- 灣鱷重生後改為頭尾近水平、腹面朝觀者的死亡翻滾；紅袋鼠與變色龍移除速度線；金剛鸚鵡縮小置中以保留長尾。
- HTML：[`../../card/animal-cards-v2-first-16-half-label.html`](../../card/animal-cards-v2-first-16-half-label.html)
- Prompt／QA：[`../../card/img-prompt/animal-print-v2-first-16.md`](../../card/img-prompt/animal-print-v2-first-16.md)
- JSONL：[`../../card/img-prompt/animal-print-v2-first-16.jsonl`](../../card/img-prompt/animal-print-v2-first-16.jsonl)
- 正式 PDF：[`../../output/pdf/animal-fight-v2-first-16-half-label-a4.pdf`](../../output/pdf/animal-fight-v2-first-16-half-label-a4.pdf)
- 日期版詳細紀錄：[`2026-07-20-animal-v2-first-16.md`](2026-07-20-animal-v2-first-16.md)
- 動作比較 HTML：[`../../card/animal-action-v2-comparison.html`](../../card/animal-action-v2-comparison.html)
- 動作比較 Prompt／QA：[`../../card/img-prompt/animal-action-v2-comparison.md`](../../card/img-prompt/animal-action-v2-comparison.md)
- 動作比較 PDF：[`../../output/pdf/animal-action-v2-comparison-a4.pdf`](../../output/pdf/animal-action-v2-comparison-a4.pdf)

正式 PDF 為 8 頁 A4 橫式，每頁 2 張；卡面已由 `118.5×170mm` 縮為 `117×170mm`，置中於 A4 二分標籤。以名義 `122×175mm` Poker 計算，四邊各保留約 `2.5mm`。字型已嵌入、圖片與屬性圖約 300 ppi，更新後 8 頁 render QA 均無裁切、重疊、缺字或空白頁。

動作比較 PDF 為 4 頁 A4 橫式，每頁一隻動物；現有 V2 在上，V2.1／V2.2 在下，圖片框 `114×70mm`。8 張候選都是 `1536×1024`，存於 `card/images-action-test/`，不會覆蓋 `card/images/` 正式圖。

2026-07-21 比較結論：V2.1／V2.2 沒有顯著提升，正式圖片維持 V2.0「圖鑑平衡版」。候選圖與比較稿只保留為設計測試紀錄，不再往這條方向重生。

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

1. 重印新版一頁，量測裁切後是否為 `117×170mm`，確認貼歪時不再溢出 Poker。
2. 正常桌面距離再次確認動物名、屬性、技能與注音；首輪 `118.5×170mm` 黑白試印已確認清楚。
3. 用 16 張 V2.0 跑一次完整淘汰賽，記錄孩子能否只看圖片說出動物與能力。
4. 只有實體結果顯示問題時才調整對比、構圖、字級或卡面內縮；使用者確認後再擴充剩餘 116 張。

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

- 工作 branch：`feat/animal-ability-audit`
- `46c4176 fix(battle): count talent bonus per die`
- `54faf4a feat(cards): add skill description audit`
- `a6910da docs(cards): record three-way ability review`
- `e5544e6 feat(cards): apply reviewed animal abilities`
- `e41583a docs(prompts): align revised animal actions`
- 本接手快照、注音字型與 PDF 重建另由最後一個 `docs(project)` commit 收尾。
- 接手時先執行 `git status -sb`，預期 branch 已與 remote 同步且沒有未提交修改。

## 常用指令

```bash
open output/pdf/animal-fight-v2-first-16-half-label-a4.pdf
open output/pdf/animal-action-v2-comparison-a4.pdf
open output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf
open output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf
python3 card/audit_animal_skills.py --format text
git status -sb
```

本 session 已關閉 PDF 預覽用的本機 HTTP server，沒有需要接手的背景程序。
