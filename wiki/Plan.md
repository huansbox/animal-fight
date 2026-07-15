# 執行中計畫

> 快照日期：2026-07-15。**Source of truth = repo 內的 [`AGENTS.md`](https://github.com/huansbox/animal-fight/blob/master/AGENTS.md)「當前狀態」段、[`docs/plans/`](https://github.com/huansbox/animal-fight/tree/master/docs/plans) 與 [GitHub issues](https://github.com/huansbox/animal-fight/issues)。** 本頁只是導覽快照，衝突時以 repo 為準。

## 主戰場一：團隊任務 v0.4 實玩

團隊任務已完成三輪文字模擬、三方 review 與 v0.4 規則收斂。核心流程：

1. 隨機抽 8 隻動物，6 隻前線、2 隻後援。
2. 前三關成功會打破 Boss 護盾，最後由兩隻動物合作挑戰 Boss。
3. 單向支援以多出的成功讓夥伴重擲失敗骰。
4. 只要提升 1 隻動物的結果就可能通關，即可派後援取代該位置並取較高結果；若必須同時救 2 隻則不能後援。
5. 故事描述增加參與感，但不改變骰子與勝負。

完整規則與 review：[`docs/plans/2026-07-15-team-mission-v04-rules-review.md`](https://github.com/huansbox/animal-fight/blob/master/docs/plans/2026-07-15-team-mission-v04-rules-review.md)。下一步是用實體卡進行第一次完整實玩，記錄排陣時間、支援／後援理解度與 Boss 難度。

## 主戰場二：放大版 Poker 卡片

- 暫定尺寸：122×175mm。
- 暫定工法：A4 黑白雷射專用標籤紙，每張 A4 橫式排 2 張，裁切後貼在放大版 Poker 上。
- 無圖測試：11pt 技能說明、長名稱與五屬性均可閱讀，已試印確認大小可接受。
- 測試檔：[`card/print-size-test-122x175.html`](https://github.com/huansbox/animal-fight/blob/master/card/print-size-test-122x175.html)／[PDF](https://github.com/huansbox/animal-fight/blob/master/output/pdf/animal-fight-card-size-test-122x175.pdf)。
- 下一步：等實體 Poker 到貨後量測，調整卡面與四周內縮，再加入圖片測一頁；目前不批量製作 132 張。

## 已通過：實體單淘汰核心玩法

實體版已用 A4 全頁、黑白雷射列印的臨時卡片開始遊玩，孩子喜歡目前版本。現行規則已清楚：

1. 採 4 強、8 強或 16 強單淘汰。
2. 兩位玩家各自為自己的動物擲骰，讓兩人都有參與。
3. 每場一戰定勝負，平手才重骰。
4. 不加 HP、能量、道具或三戰兩勝，除非實際遊玩出現明確問題。

核心玩法已通過多次實玩，中間停一陣子後孩子仍會重新拿出來玩。後續只需被動觀察：

- 4／8／16 強各自需要多少時間。
- 孩子是否會主動要求再玩一次。
- 是否有固定被排除、幾乎不會被選的弱動物。
- 骰到 6 的天賦重骰與加分，孩子是否能自己處理。
- 放大版 Poker 完成後，是否比 A4 全頁原型更方便收納與攜帶。

類寶可夢多回合草案已降為候選方案，保留在 [`docs/plans/2026-04-08-review-synthesis.md`](https://github.com/huansbox/animal-fight/blob/master/docs/plans/2026-04-08-review-synthesis.md)，不主動實作。

## 其他 active

| 項目 | 狀態 |
|---|---|
| 最終實體卡片尺寸 | 暫定放大版 Poker 122×175mm；無圖 PDF 試印大小可接受，等實物到貨後量測再定案 |
| 實體圖片資產可還原性 | 本機已有可玩原型，但圖片未進版控，新 clone 無法還原相同的列印環境，見 [Tech-Debt](Tech-Debt) |
| 數位版遊玩測試 | 尚未進行，與實體版分開追蹤 |

## 被動觀察（不需主動施工）

- **模擬結果過期**——`sim/results/` 的 v5 數據只跑了 64 隻，尚未涵蓋全部 132 隻。先看實際遊玩是否出現數值問題，不為了補齊數據而先跑模擬。
- **122×175mm 最終內縮量**——目前不猜市售底板的實際公差，等到貨後量測再改。

## 開工守則

- **動任何動物數值或新增動物之前**：讀 `CLAUDE.md` 的「動物設計全流程 SOP」，走 10 步流程。
- **動團隊任務規則之前**：先跑完一次 v0.4 實玩並留下具體觀察，不因文字模擬繼續加規則。
- **完工回寫**：每次實玩只記錄會影響下一個決定的觀察，不做過度記錄。
