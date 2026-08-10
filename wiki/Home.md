# Animal Fight（動物守護者）— 專案 Wiki

自製兒童桌遊與離線網頁遊戲：132 隻動物卡支援「動物大對決」與 DM 帶領的「團隊任務」。個人非商業專案，主要玩家是 5 歲與 9 歲兄弟。

團隊任務目前是 v0.9 owner-approved prototype：DM Web、寶物卡、揭露卡與列印 PDF 已完成，但尚未取得 v0.9 的兒童操作證據，不能標示為 child-validated。

## 頂層約束

- **兒童可操作優先**：首局使用 tutorial-in-play，不一次講完整規則；5 歲孩子能否自行操作 3～4 顆骰取高 2 是後續觀察重點。
- **純前端、可離線**：三個 Web 工具均為 Vanilla HTML/CSS/JS，沒有 framework、build step 或後端。
- **單人維護**：只做目前需求需要的最簡方案。
- **Print & Play**：實體版以 A4 黑白雷射列印與文具店可取得的材料製作。

## 系統組成

| 區塊 | 職責 | 位置 |
|---|---|---|
| 動物資料 | 132 隻完整結構化資料正本 | [`game/digital/data/animals.json`](https://github.com/huansbox/animal-fight/blob/master/game/digital/data/animals.json) |
| 數值與設計規格 | 五維判斷、技能設計與人類可讀完整表 | [`docs/attributes.md`](https://github.com/huansbox/animal-fight/blob/master/docs/attributes.md) |
| 團隊任務 v0.9 | `2d6`、屬性額外骰、技能 `+1`、固定 DC 7／8 | [v0.9 設計正本](https://github.com/huansbox/animal-fight/blob/master/docs/plans/2026-08-07-team-mission-v09-2d6-design-review.md)、[`game/dm/`](https://github.com/huansbox/animal-fight/tree/master/game/dm) |
| 實體卡片 | 首批 16 張動物卡、寶物／區域卡與大型揭露卡 | [`card/`](https://github.com/huansbox/animal-fight/tree/master/card)、[`output/pdf/`](https://github.com/huansbox/animal-fight/tree/master/output/pdf) |
| 動物大對決 | 實體 1v1 淘汰賽與離線 Web App | [`game/battle-rules.md`](https://github.com/huansbox/animal-fight/blob/master/game/battle-rules.md)、[`game/digital/`](https://github.com/huansbox/animal-fight/tree/master/game/digital) |
| 動物猜猜看 | 132 題、三提示與全制霸存檔 | [`game/quiz/`](https://github.com/huansbox/animal-fight/tree/master/game/quiz) |
| 歷史證據 | v0.2～v0.8 規則、測試、handoff 與舊列印包 | [`archive/`](https://github.com/huansbox/animal-fight/tree/master/archive) |

架構、設計決策、新增動物 SOP 與當前狀態以 [`AGENTS.md`](https://github.com/huansbox/animal-fight/blob/master/AGENTS.md) 為準；本 session 狀態看 repo root [`HANDOFF.md`](https://github.com/huansbox/animal-fight/blob/master/HANDOFF.md)。

## 專案階段

**已完成**：132 隻動物與圖片、兩個離線小遊戲、動物大對決實體核心、首批 16 張 V2 動物卡、全卡注音資產，以及團隊任務 v0.9 Web／實體 prototype。

**進行中**：實玩 v0.9 prototype；量測放大版 Poker 並複核 `117×170mm` 卡面；重印至少一頁後跑 16 張淘汰賽；數位版仍待實際遊玩測試。詳見 [Plan](Plan)。

## Wiki 頁面導覽

| 頁面 | 內容 |
|---|---|
| [Maintenance](Maintenance) | 維運手冊 — 環境、執行、測試、列印與地雷 |
| [Roadmap](Roadmap) | 路線圖 — 里程碑、方向與非目標 |
| [Plan](Plan) | 執行中計畫快照 |
| [Tech-Debt](Tech-Debt) | 技術債 — 利息排序與償還紀錄 |

> wiki 是人類導覽快照；規格、待辦與決策正本在 `AGENTS.md`、`HANDOFF.md`、`docs/` 與 tracker。衝突時以 repo 為準。
