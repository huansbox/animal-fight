# Animal Fight - 動物守護者桌遊設計專案

## 專案概述
兒童桌遊，支援兩種遊戲模式：
- **合作闘關**：家長當 DM，2 位孩子合作闖關（RPG 風格）
- **動物大對決**：1v1 淘汰賽，快節奏對戰

適合 6-12 歲兒童。Print & Play 自製桌遊格式。

## 專案結構
```
animal-fight/
├── CLAUDE.md                 # 專案架構與技術決策
├── README.md                 # 環境設置與快速開始
├── start-game.command        # 雙擊啟動遊戲（選單選擇對決/猜猜看）
├── archive/
│   ├── v1/                   # v1 數值封存（歷史備份）
│   └── docs/                 # 歷史設計文件
├── card/                     # 卡片相關檔案
│   ├── final_cards.html      # A4 全頁列印版（132 張動物卡，v2.5 數值）
│   ├── batch_generate.py     # Batch API 批次生成寫實風格大頭照（4 子命令）
│   ├── generate_from_jsonl.py      # 單張圖片生成腳本（舊版）
│   ├── data/                 # 結構化動物資料（per-wave JSON）
│   │   └── animals-wave{7~10}.json # 第七～十波（較早波次見 docs/attributes.md）
│   ├── images/               # 列印版動物圖片
│   │   └── archive-cartoon/  # 封存的卡通風格測試圖片（10 張）
│   ├── images-realistic/     # 數位版動物圖片（寫實風格 132 張）
│   └── img-prompt/           # 圖片生成 prompt
│       ├── prompt-guidelines.md          # Prompt 撰寫指南與審核條件
│       ├── animal-ai-prompts{-N}.md      # 各波繪圖 prompt（1~10）
│       └── animal-prompts-api{-N}.jsonl  # 各波 JSONL（API 用）
├── docs/
│   ├── prompt.txt            # 原始需求 prompt
│   ├── review-result.md      # 審查報告
│   ├── attributes.md         # v2.5 完整屬性（數值+判斷原則+特殊能力設計）
│   ├── backlog.md            # 後續擴充動物清單（39 隻）
│   ├── 260118-animal-wave4.md  # 第四波設計文件
│   ├── 260209-animal-wave6.md  # 第六波設計文件
│   ├── 260210-animal-wave7.md  # 第七波設計文件
│   └── design-versions/      # 設計迭代版本（6 個）
├── game/
│   ├── rulebook.md           # 合作闘關規則書
│   ├── battle-rules.md       # 動物大對決淘汰賽規則（v2.4 數值）
│   ├── digital/              # 動物大對決數位版（離線 Web App）
│   │   ├── README.md         # 啟動方式、遊戲規則、維護指南
│   │   ├── index.html        # 進入點（單頁應用，5 個畫面）
│   │   ├── css/style.css     # 樣式 + 動畫
│   │   ├── js/               # app.js, battle.js, draft.js, ai.js, bracket.js, animations.js, utils.js, zones.js
│   │   ├── data/animals.json # 合併全部 wave 的 132 隻動物
│   │   └── (images/)         # 引用 ../../card/images-realistic/（不另存）
│   └── quiz/                 # 動物猜猜看（離線 Web App）
│       ├── index.html        # 進入點（4 個畫面）
│       ├── css/style.css     # 樣式
│       └── js/               # app.js（遊戲邏輯）, hints.js（132 隻提示 + 干擾分組）
└── sim/                      # 對戰模擬器（v3~v5 + shared_dice）
    └── results/              # 模擬結果
```

## 技術決策

### 卡片設計
- **5 屬性**：力量、速度、攻擊、防禦、智慧（骰子 1-5）
- **骰子 6**：特殊能力觸發，顯示加成 icon 和分數
- **特殊能力加成**：固定 +4 分，分配到 2-3 個屬性

### 數位版（game/digital/）
- **詳細文件**：[`game/digital/README.md`](game/digital/README.md)（啟動、規則、維護指南）
- **技術**：Vanilla HTML/CSS/JS（無框架），ES Modules，CSS Animations
- **架構**：單頁應用，5 畫面 CSS class 切換 + fade-in 過渡
- **對戰引擎**：從 `sim/battle_sim_v5.py` 移植，純邏輯無 DOM
- **動物資料**：`data/animals.json` 合併 132 隻，圖片引用 `../../card/images-realistic/`
- **動物園特區**：`js/zones.js` 定義特區（上野動物園 16 隻），選角畫面可篩選 + mini-card 徽章
- **AI 難度**：僅影響選角策略（骰子完全隨機）
- **對戰 UX**：隊伍色彩識別（藍/紅）、分開擲骰、互動重骰、分數公式拆解、全螢幕 bracket overlay（橫向左到右 + 連接線 + 比分）、跨輪次隊伍記憶（teamMap）
- **離線運行**：需從專案根目錄啟動 HTTP server（圖片路徑引用 `../../card/images-realistic/`），詳見 README
- **目標裝置**：MacBook Pro 14 吋，搭飛機/火車讓小孩玩

### 動物猜猜看（game/quiz/）
- **技術**：Vanilla HTML/CSS/JS（無框架），ES Modules
- **架構**：單頁應用，4 畫面（開始 → 題目 → 揭曉 → 結算）
- **玩法**：每題給 3 個文字提示，從 5 個選項猜動物；提示越少分數越高（3/2/1 分）
- **題數**：快速 10 題 / 標準 20 題 / 挑戰 30 題
- **動物資料**：引用 `game/digital/data/animals.json`（132 隻），提示定義於 `js/hints.js`
- **干擾選項**：30 組語義分組（carnivore, primate, bird 等），優先選同組動物增加難度
- **離線運行**：同數位版，需從專案根目錄啟動 HTTP server

### 數值系統分歧
- 合作闘關（rulebook.md）：v1 數值系統（天賦為單一分數 8-12，總和 34-39）
- 動物大對決（battle-rules.md）：v2.5 數值系統（天賦為 +4 分配，總和 11-33）
- 兩模式獨立運作，待實際遊玩測試後再決定是否統一

### 圖片生成策略（寫實風格 + Batch API）

- **風格**：寫實動物大頭照（realistic wildlife portrait photograph）
- **模型**：gpt-image-1.5，quality=medium，1024x1024
- **腳本**：`card/batch_generate.py`（4 子命令：generate / submit / status / download）
- **Prompt 模板**：依動物類別自動套用（wildlife / macro / extinct / human）
  - 鳥類 → `plumage and beak`
  - 爬行類 → `scales and eyes`
  - 魚類 → `scales and fins`
  - 海洋哺乳類 → `smooth skin and eyes`
  - 昆蟲/節肢 → macro 模板 + `exoskeleton and body texture`
  - 其餘哺乳類 → `fur and eyes`
- **共用後綴**：`facing slightly left, natural lighting, solid dark teal background, studio-quality, square format, no text, no watermark`
- **成本**：Batch API 50% 折扣，≈ $0.02/張（128 張實際總費用 $2.63）
- **輸出目錄**：`card/images-realistic/`（數位版專用，與列印版 `card/images/` 分開）
- **封存**：舊卡通風格測試圖片保留於 `card/images/archive-cartoon/`（10 張）

### 動物設計全流程 SOP（10 步）

觸發指令：「用 SOP 設計第 N 波新動物：[動物清單]」
AI 自動執行步驟 1-9（數值 + prompt + HTML + 文件更新），完成後只剩人工生圖。

| 階段 | 步驟 | 內容 |
|------|:----:|------|
| 數值 | 1 | **選定動物** → 由人決定，AI 不介入 |
| 數值 | 2 | **五維數值 + 特殊能力 + skillDesc** → `docs/attributes.md` §1-§5（數值）+ §7（技能設計 + +4 分配 + 命名）+「技能描述撰寫」（15-25 字） |
| 數值 | 3 | **五維重疊比對** → `docs/attributes.md` §9（差異分數 ≤3 必須調整） |
| 數值 | 3.5 | **自動化前置檢查** → `docs/attributes.md` §8（bonus 加總、skillName 撞名、加成模式重疊、差異分數） |
| 數值 | 4 | **3 Agent 數值審核** → `docs/attributes.md` §8（A=科學合理性 / B=特殊能力設計 / C=全局平衡與辨識度） |
| 數值 | 5 | **產出 JSON** → `card/data/animals-wave{N}.json`（7 欄位：id, name, en, img, stats, skillName, skillDesc, skillBonus）。img 格式固定為 `"images/{id}.png"` |
| Prompt | 5.5 | **物種特徵研究** → `prompt-guidelines.md` §0（每隻列出 2-3 個最高辨識度外觀特徵） |
| Prompt | 6 | **撰寫繪圖 Prompt** → `prompt-guidelines.md` §1-§6（模板 + 動作轉換 + 風格後綴），含 §7 黑化/特殊毛色處理 |
| Prompt | 7 | **3 Agent Prompt 審核** → `prompt-guidelines.md` §3 + §7-§12 + §13（12 項審核清單 + 審核分工） |
| Prompt | 8 | **產出 .md + .jsonl** → `prompt-guidelines.md` §14（JSONL 轉換規範） |
| 整合 | 9 | **整合 HTML + 更新文件** → `final_cards.html` 加入新動物 + `CLAUDE.md` 更新 |
| 人工 | 10 | **批次 API 生圖** → `card/batch_generate.py`（Batch API 生成寫實風格至 `card/images-realistic/`；列印版圖片另存 `card/images/`） |

### 動物總覽（132 隻，10 波完成）

完整數值見 `docs/attributes.md`，per-wave JSON 見 `card/data/`，合併資料見 `game/digital/data/animals.json`。

| 波次 | 張數 | 總和範圍 | 備註 |
|:----:|:----:|:--------:|------|
| 1 | 16 | 16–30 | 原始動物 |
| 3 | 19 | 13–31 | 設計過程見 `archive/docs/260115-animal-final.md` |
| 4 | 13 | 17–32 | 設計文件見 `docs/260118-animal-wave4.md` |
| 5 | 20 | 11–33 | 含 4 隻補充 |
| 6 | 16 | 14–31 | 設計文件見 `docs/260209-animal-wave6.md` |
| 7 | 14 | 11–25 | Creature Cases 系列，設計見 `docs/260210-animal-wave7.md` |
| 8 | 8 | 14–29 | 公雞 + 黑豹 + 6 隻 Creature Cases |
| 9 | 22 | 10–30 | 補至 128 張 |
| 10 | 4 | 17–21 | 上野動物園特區 |

> 後續擴充 35 隻待建，見 [`docs/backlog.md`](docs/backlog.md)

## 遊戲模式

### 合作闘關（rulebook.md）
- 判定：`2d6 + 屬性數值`
- 難度：DC 10（優勢）/ 12（標準）/ 14（劣勢）
- 生命：共享 5 愛心
- 勝利：累積 5 前進標記 → 終局

### 動物大對決（battle-rules.md）
- 賽制：淘汰賽，每輪 1 戰定勝負（進階：3 戰 2 勝）
- 擲骰：雙方各擲 2d6，比總和
- 骰到相同：該屬性 ×2
- 骰到 6：重骰＋觸發 1 次天賦加分（僅加骰面命中的屬性加成）
- 連續骰 6：每次都重骰＋再觸發 1 次（可累加）
- 平手：加賽

## 當前狀態

**已完成**：需求分析 → 多版本設計 → 審查選定 → 10 波 132 隻動物（數值 + 技能 + prompt + JSON + HTML） → 寫實風格圖片 132 張（Batch API） → 數位版 Web App（選角 + AI + 對戰 + 淘汰賽樹 + 動畫 + 動物園特區篩選） → 對戰模擬器 v3-v5 → 動物猜猜看小遊戲（132 隻 × 3 提示）

**待完成**：
- [ ] 數位版實際遊玩測試
- [ ] 印刷測試
- [ ] 實際遊玩測試（實體版）

## 對戰模擬結果（64 隻淘汰賽 v5）⚠️ 尚未納入補充 4 隻

100,000 次模擬，新規則（骰 6 重骰＋條件加分），Top 6：虎鯨(33)→大白鯊(32)→北極熊(31)→非洲獅(30)→河馬(31)→大猩猩(30)

> 詳細數據見 `sim/results/v5_*.csv`

## 卡片實體製作
- **討論文件**：[`docs/plans/2026-02-10-card-size-production.md`](docs/plans/2026-02-10-card-size-production.md)
- **狀態**：討論中，待決定尺寸與製作方式
- **初步方向**：Tarot 尺寸（70×120mm）+ 卡套法

## 技術債 / 待建工具

### 自動化前置檢查腳本（SOP 步驟 3.5 + Prompt 審核前）

目前由 AI 手動執行，待腳本化後可在 3 Agent 審核前自動攔截低級錯誤。

**數值階段**（輸入：`animals-wave{N}.json` + 歷史 wave JSON）

| 檢查項目 | 自動化方式 |
|----------|-----------|
| skillBonus 加總 = 4 | 加總所有 val 欄位 |
| skillName 四字 + 不撞名 | 計算字數 + 比對歷史 wave JSON |
| skillDesc 字數（15-25 字） | 計算中文字數（不含標點） |
| 加成模式不重疊 | 比對歷史 skillBonus attr+val 組合 |
| 五維差異分數 ≤ 3 | 批次計算新 vs 新 + 新 vs 舊 |

**Prompt 階段**（輸入：`animal-ai-prompts-{N}.md`）

| 檢查項目 | 自動化方式 |
|----------|-----------|
| 禁用詞掃描 | 正則比對 §7 禁用詞清單 |
| 風格後綴完整性 | 檢查結尾是否含固定後綴字串 |

## 後續擴充（不納入 MVP）
- 裝備卡
- 狀態效果
- 更多動物（39 隻待建，見 `docs/backlog.md`）
- Boss 專屬招式表
