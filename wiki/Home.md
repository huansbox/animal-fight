# Animal Fight（動物守護者）— 專案 Wiki

自製兒童桌遊：132 隻動物卡，一套五維數值同時支撐「實體 Print & Play」與「離線網頁小遊戲」。個人專案，做給自己家兩個小孩玩（搭飛機／火車打發時間），非商業用途。

目前 132 隻動物與三個數位小遊戲都已完成，專案停在兩個**需要人決定、AI 無法代決**的岔路上：玩法要不要從「一骰定勝負」改成類寶可夢的多回合制，以及實體卡片要做多大、怎麼做。

## 頂層約束

這些約束 gate 掉了後續所有設計決策，先看這裡再看細節：

- **實際玩家是 5 歲與 9 歲的兄弟**（README 寫的 6-12 歲是對外說法）。年齡差是硬約束：規則必須能分層，弟弟玩得動、哥哥不會膩。三方 review 的結論是「兩位數 HP 心算」直接踩線——小孩會變成在看爸爸算數，不是在玩。
- **純前端、零依賴、可離線**。三個 Web 小遊戲都是 Vanilla HTML/CSS/JS + ES Modules，沒有框架、沒有 build step、沒有後端。理由是要在飛機上沒網路時能玩。
- **單人維護**。優先簡單方案，不為假想的未來需求加抽象層。
- **Print & Play**。實體版必須能用家用印表機 + 文具店買得到的材料做出來。

## 系統組成

| 區塊 | 職責 | 位置 |
|---|---|---|
| 動物資料 | 132 隻的五維數值、技能、技能加成（唯一數值來源） | [`card/data/`](https://github.com/huansbox/animal-fight/tree/master/card/data)（分波）→ [`game/digital/data/animals.json`](https://github.com/huansbox/animal-fight/blob/master/game/digital/data/animals.json)（合併） |
| 數值規格 | 五維判斷原則、特殊能力設計、審核清單 | [`docs/attributes.md`](https://github.com/huansbox/animal-fight/blob/master/docs/attributes.md) |
| 卡片列印 | A4 全頁列印版（每張卡一頁） | [`card/final_cards.html`](https://github.com/huansbox/animal-fight/blob/master/card/final_cards.html) |
| 圖片生成 | OpenAI Batch API 批次生成寫實動物大頭照 | [`card/batch_generate.py`](https://github.com/huansbox/animal-fight/blob/master/card/batch_generate.py) + [`card/img-prompt/`](https://github.com/huansbox/animal-fight/tree/master/card/img-prompt) |
| 實體規則 | 合作闘關（DM 帶隊）／動物大對決（1v1 淘汰賽） | [`game/rulebook.md`](https://github.com/huansbox/animal-fight/blob/master/game/rulebook.md)、[`game/battle-rules.md`](https://github.com/huansbox/animal-fight/blob/master/game/battle-rules.md) |
| 數位版・動物大對決 | 選角 → 對戰 → 淘汰賽樹，含 AI 對手 | [`game/digital/`](https://github.com/huansbox/animal-fight/tree/master/game/digital) |
| 數位版・動物猜猜看 | 3 提示猜動物，含 132 題全制霸模式 | [`game/quiz/`](https://github.com/huansbox/animal-fight/tree/master/game/quiz) |
| 數位版・世界盃小遊戲 | 認國家 + 猜賽果（**只存在於 `claude/world-cup-travel-game-zlcnyd` 分支**，未合併回 master） | 見 [Tech-Debt](Tech-Debt) 的分支分歧項 |
| 平衡模擬器 | 大量對戰模擬驗證數值平衡 | [`sim/`](https://github.com/huansbox/animal-fight/tree/master/sim) |

架構細節與新增動物的 10 步 SOP 寫在 [`CLAUDE.md`](https://github.com/huansbox/animal-fight/blob/master/CLAUDE.md)，wiki 不重複。

## 專案階段

**已完成**：10 波共 132 隻動物（數值 → 技能 → 繪圖 prompt → JSON → HTML 全打通）、132 張寫實風格圖片、三個離線 Web 小遊戲、對戰模擬器 v3–v5。

**進行中**：玩法重設計的方向抉擇（類寶可夢草案已做完三方 review，收斂到「三回合淘汰 + 能量選招」，但 7 個細節待定）。詳見 [Plan](Plan)。

**卡住**：實體卡片尺寸與製作方式，文件裡有三種互相矛盾的說法，需要一次拍板。

## 線上試玩

<https://huansbox.github.io/animal-fight/>

**圖片是這個專案目前最大的坑，先讀再動手。** 所有卡片圖片都被 `.gitignore` 排除在版控外（240MB 的 PNG），造成兩件事：線上版的動物遊戲看不到任何圖片（世界盃小遊戲不吃圖，所以正常）；而列印版 `final_cards.html` 取圖的 `card/images/` 目錄目前是空的，**直接印會得到 132 張無圖卡片**。數位版用的 132 張寫實圖（`card/images-realistic/`）是完好的，只是沒進 git。成因與償還策略見 [Tech-Debt](Tech-Debt)。

## Wiki 頁面導覽

| 頁面 | 內容 |
|---|---|
| [Maintenance](Maintenance) | 維運手冊 — 怎麼跑、怎麼生圖、怎麼部署、踩過哪些坑 |
| [Roadmap](Roadmap) | 路線圖 — 走過的里程碑、現在的主軸、刻意不做的事 |
| [Plan](Plan) | 執行中計畫快照 — 現在卡在哪、下一步是什麼 |
| [Tech-Debt](Tech-Debt) | 技術債 — 依利息排序 + 償還紀錄 |

> **文件分工**：wiki 是導覽與快照，方便人快速上手；規格、待辦、決策的 source of truth 在 repo 內（`CLAUDE.md`、`docs/`、GitHub issues）。兩者衝突時**以 repo 為準**。
