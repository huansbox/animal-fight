# 執行中計畫

> 快照日期：2026-08-10。**Source of truth = repo 的 [`AGENTS.md`](https://github.com/huansbox/animal-fight/blob/master/AGENTS.md)「當前狀態」、[`HANDOFF.md`](https://github.com/huansbox/animal-fight/blob/master/HANDOFF.md)、[`docs/plans/`](https://github.com/huansbox/animal-fight/tree/master/docs/plans) 與 [GitHub issues](https://github.com/huansbox/animal-fight/issues)。** 本頁只是導覽快照，衝突時以 repo 為準。

## 主戰場一：團隊任務 v0.9 實玩

v0.9 prototype 的 DM Web、寶物卡、孩子版揭露卡與兩份正式 PDF 已完成並通過自動測試、Browser smoke test 與 PDF 畫面 QA。owner 略過原訂最小兒童回歸，因此現在要收集的是後續實玩證據，不是補前置驗收。

實玩時優先觀察：

1. 5 歲孩子能否自行從 3～4 顆骰中選最大的 2 顆並相加。
2. 屬性符合多一顆骰，是否帶來可觀察的投入。
3. 屬性不符仍擲 `2d6`，且裁定後不能換卡或改方法，孩子是否能接受。
4. 若自然發生，記錄兩提示、後援、手電筒與魔鏡的操作；不為補表格強迫觸發。

規則正本：[v0.9 2d6 設計](https://github.com/huansbox/animal-fight/blob/master/docs/plans/2026-08-07-team-mission-v09-2d6-design-review.md)。v0.2～v0.8 文件已封存到 [`archive/docs/plans/`](https://github.com/huansbox/animal-fight/tree/master/archive/docs/plans)。

## 主戰場二：首批 16 張動物卡實體驗證

- 重新取得放大版 Poker 後，量測 3～5 張實物並取最小長寬。
- 重印 `117×170mm` 卡面至少一頁，確認貼歪時仍不溢出名義 `122×175mm` 底卡。
- 用 16 張 V2.0 圖片跑完整淘汰賽，觀察辨識度、閱讀距離與遊戲節奏。
- 只有實體結果顯示問題時才調整對比、構圖、字級或內縮；確認後才擴充剩餘 116 張。

## 其他 active

| 項目 | 狀態 |
|---|---|
| 數位版實際遊玩測試 | 尚未進行，與實體工作線分開 |
| 團隊任務黑白實際列印 | PDF 畫面 QA 已過，仍待紙本觀看距離與桌面方向驗證 |
| 剩餘 116 張 V2 動物卡 | 等首批 16 張完成尺寸、列印與淘汰賽驗證後再開始 |

## 被動觀察

- v5 對戰模擬仍只涵蓋 64 隻；除非實玩顯示平衡問題或準備重開模擬工作，暫不先施工。
- v0.9 尚無本版兒童證據是已知證據界線，不應在文件中改寫成已驗證。

## 開工守則

- 團隊任務修改前先讀 v0.9 設計正本與 `game/dm/rules.test.mjs`。
- 動物數值或新增動物前先讀 `AGENTS.md` 的 10 步 SOP 與 `docs/attributes.md`。
- 現行文件留在 `docs/`；被取代但具有追溯價值的規則、測試與 handoff 移到 `archive/`，不直接刪除。
