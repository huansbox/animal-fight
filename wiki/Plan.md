# 執行中計畫

> 快照日期：2026-07-14。**Source of truth = repo 內的 [`CLAUDE.md`](https://github.com/huansbox/animal-fight/blob/master/CLAUDE.md)「當前狀態」段、[`docs/plans/`](https://github.com/huansbox/animal-fight/tree/master/docs/plans) 與 [GitHub issues](https://github.com/huansbox/animal-fight/issues)。** 本頁只是導覽快照，衝突時以 repo 為準。

## 主戰場：玩法重設計，等一個人來拍板

設計工作已經做完了。三方 review 收斂到方向 B（三回合淘汰 + 能量選招），論證完整、數據齊全。**卡住的不是想不出方案，是沒人做決定。**

[`docs/plans/2026-04-08-review-synthesis.md`](https://github.com/huansbox/animal-fight/blob/master/docs/plans/2026-04-08-review-synthesis.md) 最後列了 7 個待討論事項，這是關鍵路徑上唯一的東西：

1. **方向選擇**：A（一骰定勝負 + 戰前策略）／ B（三回合淘汰，review 推薦）／ C（HP 刻度戰 + 全面修正），或混合？
2. **卡片尺寸確認**——這題和實體製作是同一題，見下方。
3. 是否需要新卡面設計（加棲地 icon、HP 等級星星）？
4. 道具卡的數量與種類（5 張夠嗎？要哪幾張？）
5. **132 隻動物的棲地分類**（陸／空／海逐一分配）——這是唯一一項純執行、可以外包給 AI 批次做掉的工作，但它得等方向確定才知道要不要做。
6. 合作模式規則（兄弟 vs 爸爸的 DM 規則怎麼設計）
7. 卡片製作方式（卡套法／護貝法／厚紙直印）

這七題全都是取捨題，不是實作題。AI 可以幫忙列選項、跑模擬、算平衡，但不能代替人決定「我希望我小孩玩到什麼」。

## 其他 active

| 項目 | 狀態 |
|---|---|
| 實體卡片尺寸拍板 | **卡住，且文件互相矛盾。** [`docs/plans/2026-02-10-card-size-production.md`](https://github.com/huansbox/animal-fight/blob/master/docs/plans/2026-02-10-card-size-production.md) 推 Tarot 70×120mm 並明說撲克牌「不推薦」（6-8 歲讀不了那麼密的資訊）；但 4 月的家長 review 反過來建議撲克牌 63×88mm（A5 太大，餐桌放不下 16 張）；README 又直接寫「裁切成 63×88mm」。三種說法，先解決矛盾再動版面 |
| 世界盃 5 個 enhancement（[#1](https://github.com/huansbox/animal-fight/issues/1)–[#5](https://github.com/huansbox/animal-fight/issues/5)） | 有時效性，賽事 7 月中後就結束了。**要做要現在做，否則建議直接關掉** — 見 [Roadmap](Roadmap) 收斂點 |
| 線上部署與 master 收斂 | Pages 部署自 `claude/world-cup-travel-game-zlcnyd` 分支，該分支比 master 多 4 個 commit（世界盃遊戲 + 合輯首頁）。master 目前沒有世界盃遊戲，也沒有那個首頁 → 見 [Tech-Debt](Tech-Debt) |
| 線上版動物圖片 404 | 圖片（240MB）不在版控裡。要修得先壓縮再進 git → 見 [Tech-Debt](Tech-Debt) 高利息第 1 項 |

## 被動觀察（不需主動施工）

- **實體版遊玩測試**、**印刷測試**、**數位版遊玩測試**——`CLAUDE.md` 的待完成清單裡掛了很久。這三項都不是「做」出來的，是要真的找小孩坐下來玩。玩法重設計拍板後，這些測試才有意義（現在測的是即將被改掉的規則）。
- **模擬結果過期**——`sim/results/` 的 v5 數據只跑了 64 隻，第十波的 4 隻沒納入。等玩法定案後要重跑，現在補跑白工。

## 開工守則

- **動任何動物數值或新增動物之前**：讀 `CLAUDE.md` 的「動物設計全流程 SOP」，走 10 步流程，不要繞過審核步驟。
- **動玩法規則之前**：先讀 `docs/plans/2026-04-08-review-synthesis.md`。裡面已經用模擬數據否決掉一批看起來很合理的設計（HP 制、先手不補償、能量定價），不要重蹈覆轍。
- **完工回寫**：決策寫回 `docs/plans/` 或開 issue；wiki 這幾頁是快照，過期了重跑 `/repo-wiki refresh` 就好，不要手動改網頁版。
