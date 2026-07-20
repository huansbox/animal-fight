# Animal Fight - 動物守護者桌遊設計專案

## 專案概述
兒童桌遊，支援兩種遊戲模式：
- **合作闘關**：家長當 DM，2 位孩子合作闖關（RPG 風格）
- **動物大對決**：1v1 淘汰賽，快節奏對戰

適合 6-12 歲兒童。Print & Play 自製桌遊格式。

## 專案結構
```
animal-fight/
├── AGENTS.md                 # 專案架構與技術決策
├── README.md                 # 環境設置與快速開始
├── start-game.command        # 雙擊啟動遊戲（選單選擇對決/猜猜看）
├── archive/
│   ├── v1/                   # v1 數值封存（歷史備份）
│   └── docs/                 # 歷史設計文件
├── card/                     # 卡片相關檔案
│   ├── final_cards.html      # A4 全頁列印版（132 張動物卡，v2.5 數值）
│   ├── print-size-test-122x175.html # 放大版 Poker 尺寸測試（A4 橫式 2 張／頁）
│   ├── animal-card-final-prototype.html # 122×175mm 全卡注音版面原型
│   ├── bopomofo-coverage-qa.html # 132 張正式文字注音與缺字 QA
│   ├── team-mission-status-cards-quarter-label.html # 3 寶物＋2 後援＋3 區域卡，A4 四分標籤
│   ├── storm-forest-rescue-reveal-cards-half-label.html # 4 張大型揭露卡，A4 二分標籤
│   ├── reveal-card-stacked-layout-prototype.html # 最新揭露卡直向資訊層級候選，單／雙動物同頁測試
│   ├── reveal-card-requirement-ab-comparison.html # 揭露卡早期比例比較稿，僅保留紀錄
│   ├── build_bopomofo_fonts.py # 從官方來源重建正式 Bold／Medium WOFF2 subset
│   ├── generate_team_mission_print_kit.py # 產生 v0.6 控制板、揭露卡與 DM 指南 PDF
│   ├── batch_generate.py     # Batch API 批次生成寫實風格大頭照（4 子命令）
│   ├── generate_from_jsonl.py      # 單張圖片生成腳本（舊版）
│   ├── data/                 # 結構化動物資料（per-wave JSON）
│   │   └── animals-wave{7~10}.json # 第七～十波（較早波次見 docs/attributes.md）
│   ├── images/               # 列印版動物圖片
│   │   └── archive-cartoon/  # 封存的卡通風格測試圖片（10 張）
│   ├── images-realistic/     # 數位版動物圖片（寫實風格 132 張）
│   ├── mission-art/          # 團隊任務大型揭露卡黑白情境圖
│   ├── images-team-status/   # 寶物、後援與三區 V2 黑白插圖
│   ├── fonts/bopomofo/       # 正式卡片注音字型、corpus、授權與 build report
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
│   ├── handoffs/               # 跨 session 接手快照
│   └── design-versions/      # 設計迭代版本（6 個）
├── game/
│   ├── rulebook.md           # 合作闘關規則書
│   ├── battle-rules.md       # 動物大對決淘汰賽規則（v2.4 數值）
│   ├── dm/                   # 團隊任務 DM 專注模式（Cloudflare Pages 靜態 Web App）
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
├── output/pdf/
│   ├── animal-fight-card-size-test-122x175.pdf # 放大版 Poker 尺寸測試
│   ├── team-mission-status-zone-cards-quarter-label-a4.pdf # 8 張狀態／區域卡
│   ├── storm-forest-rescue-reveal-cards-half-label-a4.pdf # 4 張大型劇情揭露卡
│   ├── reveal-card-stacked-layout-prototype-a4.pdf # 最新揭露卡單／雙動物排版測試
│   ├── reveal-card-requirement-ab-comparison-a4.pdf # 揭露卡早期 A／B 比例比較
│   ├── team-mission-v06-control-board-a4.pdf # 團隊任務 A4 控制板
│   ├── storm-forest-rescue-reveal-cards-four-up-a4.pdf # 四分標籤揭露卡
│   ├── storm-forest-rescue-dm-guide-a4-duplex.pdf # A4 雙面 DM 指南
│   └── bopomofo-font-coverage-qa.pdf # 132 張正式文字注音覆蓋 QA
└── sim/                      # 對戰模擬器（v3~v5 + shared_dice）
    └── results/              # 模擬結果
```

## 技術決策

### 卡片設計
- **5 屬性**：力量、速度、攻擊、防禦、智慧（骰子 1-5）
- **骰子 6**：特殊能力觸發，顯示加成 icon 和分數
- **特殊能力加成**：固定 +4 分，分配到 2-3 個屬性
- **卡片用語**：實體兒童版將「智慧」顯示為「聰明」
- **全卡注音**：動物名、特殊能力與團隊任務實體卡使用源泉注音圓體 Bold／Medium；正式 subset 由 `card/build_bopomofo_fonts.py` 依 132 張動物文字及團隊任務卡文字重建
- **讀音校正**：89 個 IVS 多音字／輕聲校正，另有 7 個人工排注音實例；`一、不`維持字典本調
- **列管例外**：官方字型缺 `獴、㺢、㹢、狓`；`屁股`的「股」與`腦袋`的「袋」沒有本案採用的輕聲 IVS，統一由 `card/data/bopomofo-overrides.json` 處理

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
- **全制霸模式**：132 題不重複挑戰全部動物，localStorage 存檔接續（可中斷再繼續）
- **動物資料**：引用 `game/digital/data/animals.json`（132 隻），提示定義於 `js/hints.js`
- **干擾選項**：30 組語義分組（carnivore, primate, bird 等），優先選同組動物增加難度
- **離線運行**：同數位版，需從專案根目錄啟動 HTTP server

### 數值系統分歧
- 舊合作闘關（rulebook.md）：v1 數值系統（天賦為單一分數 8-12，總和 34-39）
- 團隊任務 v0.7：沿用 v2.5 卡面五維數值與 `skillBonus` 標記，但改用 1-3 顆骰的合作判定；不計卡面技能加分數字
- 動物大對決（battle-rules.md）：v2.5 數值系統（天賦為 +4 分配，總和 11-33）
- 三套規則獨立運作；團隊任務 v0.7 是目前合作玩法候選，等待真人實玩

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
| 整合 | 9 | **整合 HTML + 更新文件** → `final_cards.html` 加入新動物 + `AGENTS.md` 更新 |
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

> 後續擴充 39 隻待建，見 [`docs/backlog.md`](docs/backlog.md)

## 遊戲模式

### 合作闘關（rulebook.md）
- 判定：`2d6 + 屬性數值`
- 難度：DC 10（優勢）/ 12（標準）/ 14（劣勢）
- 生命：共享 5 愛心
- 勝利：累積 5 前進標記 → 終局
- **團隊任務模式 v0.2 草案**：[`docs/plans/2026-07-15-team-mission-simulation-review.md`](docs/plans/2026-07-15-team-mission-simulation-review.md)（完整文字模擬、三方 blind review、下一次實測規則）
- **團隊任務 v0.3 後援制**：[`docs/plans/2026-07-15-team-mission-v03-reserve-simulation-review.md`](docs/plans/2026-07-15-team-mission-v03-reserve-simulation-review.md)（8 隻配置、完整模擬、三方 blind review、v0.4 建議）
- **團隊任務 v0.4 歷史候選**：[`docs/plans/2026-07-15-team-mission-v04-rules-review.md`](docs/plans/2026-07-15-team-mission-v04-rules-review.md)（六格全公開、開局先排陣；保留為候選隊長策略模式）
- **團隊任務 v0.5 停止版本**：[`docs/plans/2026-07-17-team-mission-v05-rules.md`](docs/plans/2026-07-17-team-mission-v05-rules.md)（v0.4 文字修訂；回歸期間轉向逐關揭露）
- **團隊任務 v0.6 歷史基準**：[`docs/plans/2026-07-17-team-mission-v06-progressive-reveal-rules.md`](docs/plans/2026-07-17-team-mission-v06-progressive-reveal-rules.md)（Boss 先提示、前三關逐關揭露、待命／再挑戰／休息三區、兩次後援；6 局 Agent 模擬與短回歸通過；護盾部分已被 v0.7 取代）
- **v0.6 模擬整併**：[`docs/plans/2026-07-17-team-mission-v06-agent-simulation-review.md`](docs/plans/2026-07-17-team-mission-v06-agent-simulation-review.md)（5 歲、9 歲、兄弟模式各自然局＋邊界局；後援 A／B 難度比較）
- **v0.7 Boss 寶物規則**：[`docs/plans/2026-07-19-team-mission-v07-treasure-boss-design.md`](docs/plans/2026-07-19-team-mission-v07-treasure-boss-design.md)（三件寶物、固定 `2＋2`、結算順序、成功率與後援互動；取代 Boss 護盾）
- **v0.7 固定劇情模板**：[`docs/plans/2026-07-17-team-mission-story-template.md`](docs/plans/2026-07-17-team-mission-story-template.md)（批次產生欄位、區間理由、寶物銜接、失敗旁白與檢查清單）
- **v0.7 固定劇情原型**：[`docs/plans/scenarios/`](docs/plans/scenarios/)（災難救援／調查解謎／遠征運送各 1 套；三套皆已遷移為抽寶物與固定 `2＋2` Boss）
- **v0.6 舊實體測試包**：[`docs/plans/2026-07-18-team-mission-physical-production.md`](docs/plans/2026-07-18-team-mission-physical-production.md)（已被 7/19 原型取代，保留歷史）
- **v0.7 現行實體／DM 規格**：[`docs/plans/2026-07-19-team-mission-props-dm-web-design.md`](docs/plans/2026-07-19-team-mission-props-dm-web-design.md)（3 張寶物、2 張後援、3 張區域 Poker、4 張大型揭露卡、DM 專注模式 Web App；正式列印 PDF 均已完成畫面 QA）
- **目前接手快照**：[`docs/handoffs/2026-07-19-team-mission-print-layout.md`](docs/handoffs/2026-07-19-team-mission-print-layout.md)（v0.7 正式列印檔狀態、驗收重點與下一步真人試印／實玩）

### 動物大對決（battle-rules.md）
- 賽制：淘汰賽，每輪 1 戰定勝負（進階：3 戰 2 勝）
- 擲骰：雙方各擲 2d6，比總和
- 骰到相同：該屬性 ×2
- 骰到 6：重骰＋觸發 1 次天賦加分（僅加骰面命中的屬性加成）
- 連續骰 6：每次都重骰＋再觸發 1 次（可累加）
- 平手：加賽

## 當前狀態

**已完成**：需求分析 → 多版本設計 → 審查選定 → 10 波 132 隻動物（數值 + 技能 + prompt + JSON + HTML） → 寫實風格圖片 132 張（Batch API） → 數位版 Web App（選角 + AI + 對戰 + 淘汰賽樹 + 動畫 + 動物園特區篩選） → 對戰模擬器 v3-v5 → 動物猜猜看小遊戲（132 隻 × 3 提示） → A4 黑白雷射列印實體原型與首輪親子遊玩測試 → 122×175mm 無圖卡面 PDF 尺寸試印（大小可接受） → 團隊任務 v0.6 逐關揭露規則、6 局 Agent 模擬、共用劇情模板與 3 套固定劇情 → 團隊任務第一套黑白雷射列印測試包（控制板、暴雨揭露卡、DM 雙面指南） → 實體動物卡文字版面與全卡注音規格定案 → 132 張正式文字字型 subset 與 QA PDF → 動物圖片 B+ 黑白印刷風格 3×4 試印套組 → 動物圖片正式採用 V2「圖鑑平衡版」 → 團隊任務舊護盾實體道具原型與 DM 專注模式 Web App → v0.7 三寶物 Boss 規則、結算順序與機率基準定案 → 三套劇情、DM App、寶物／後援／三區卡與兩頁列印 PDF 完成 v0.7 遷移 → 揭露卡單一路徑版面完成單／雙動物確認並遷移至正式 4 張揭露卡與 2 頁 PDF，逐頁畫面 QA 通過

**待完成**：
- [ ] 數位版實際遊玩測試
- [ ] 列印 v0.7 寶物／後援／三區卡與 4 張大型揭露卡，實際記錄寶物操作、Boss 骰池、後援前／後勝負與 DM 負擔
- [ ] 依黑白試印與親子實玩結果，定案 3 張寶物、2 張後援、3 張區域卡、4 張大型揭露卡與 DM 網頁
- [ ] 放大版 Poker 到貨後量測實際尺寸，微調 122×175mm 卡面與貼紙內縮量
- [ ] 先完成包含 4 張 V2 測試圖在內的 16–24 隻安全牌動物首批，用於實際遊玩與完整卡面試印
- [ ] 加入圖片並完成最終放大版 Poker 卡面

## 對戰模擬結果（64 隻淘汰賽 v5）⚠️ 尚未納入補充 4 隻

100,000 次模擬，新規則（骰 6 重骰＋條件加分），Top 6：虎鯨(33)→大白鯊(32)→北極熊(31)→非洲獅(30)→河馬(31)→大猩猩(30)

> 詳細數據見 `sim/results/v5_*.csv`

## 卡片實體製作
- **討論文件**：[`docs/plans/2026-02-10-card-size-production.md`](docs/plans/2026-02-10-card-size-production.md)
- **團隊任務現行原型**：[`docs/plans/2026-07-19-team-mission-props-dm-web-design.md`](docs/plans/2026-07-19-team-mission-props-dm-web-design.md)
- **目前原型**：A4 全頁、黑白雷射列印，已用於親子遊玩，孩子喜歡
- **暫定尺寸**：放大版 Poker 122×175mm；無圖測試 PDF 已試印，文字與數字大小可接受
- **動物卡工法**：A4 二分黑白雷射標籤紙，每張 A4 排 2 張，卡面暫定 170×118.5mm，裁切後貼在放大版 Poker 上
- **屬性視覺定案**：骰面 1-5 置於插圖正上方；五屬性採 B「簡化寫實鋼筆插畫」情境圖，不使用抽象 icon
- **屬性插圖**：[`card/attribute-illustrations/`](card/attribute-illustrations/)（力量搬石、速度奔跑、攻擊碎木、防禦擋石、聰明看地圖；卡面顯示高度 16mm）
- **動物圖片風格測試**：[`card/animal-image-style-3x4-comparison.html`](card/animal-image-style-3x4-comparison.html)（V1／V2／V3 × 非洲象、黑豹、河豚、行軍蟻，圖片框實際 114×70mm）；Prompt：[`card/img-prompt/animal-print-bplus-3x4.md`](card/img-prompt/animal-print-bplus-3x4.md)；PDF：[`output/pdf/animal-image-bplus-3x4-comparison.pdf`](output/pdf/animal-image-bplus-3x4-comparison.pdf)
- **動物圖片風格定案**：V2「圖鑑平衡版」（五階灰階、中粗外輪廓、只保留物種辨識所需紋理）；四種測試動物全部採用 V2，V1／V3 僅保留為比較紀錄
- **動物卡版面原型**：[`card/animal-card-final-prototype.html`](card/animal-card-final-prototype.html)（122×175mm、全卡注音、黑白雷射列印）
- **正式注音字型**：[`card/fonts/bopomofo/`](card/fonts/bopomofo/)（v1.500 固定來源、Bold／Medium subset、corpus、授權、build report）；QA：[`card/bopomofo-coverage-qa.html`](card/bopomofo-coverage-qa.html)、[`output/pdf/bopomofo-font-coverage-qa.pdf`](output/pdf/bopomofo-font-coverage-qa.pdf)
- **團隊任務工法**：萬用背包／探險手電筒／變化魔鏡各 1 張、後援 2 張、待命／再挑戰／休息各 1 張，共用 2 張 A4 四分標籤；4 張大型揭露卡使用 2 張 A4 二分標籤；全部貼在放大版 Poker 上
- **揭露卡正式版面**：情境圖片 → 白話原因 → 淺灰圓角數字牌 → 兩個屬性；直接列 `1、2、3`／`4、5、6`／`7、8、9`，不用區間符號或橫向分隔線；屬性圖片在上、名稱在下，中間以黑底「或」表示選擇。單動物屬性組置中限寬 `96mm`；單／雙動物版均已確認並遷移到正式 4 張揭露卡
- **DM 專注模式**：[`game/dm/`](game/dm/)；Vanilla HTML／CSS／JS、無 build、Cloudflare Pages-ready、逐關顯示、v0.7 Boss 寶物結算、`localStorage` 保存進度與最近 50 局摘要，可匯出 Markdown／JSON
- **測試檔**：[`card/print-size-test-122x175.html`](card/print-size-test-122x175.html)；可列印 PDF：[`output/pdf/animal-fight-card-size-test-122x175.pdf`](output/pdf/animal-fight-card-size-test-122x175.pdf)
- **團隊任務列印檔**：[`output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf`](output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf)（v0.7 三寶物版）、[`output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf`](output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf)
- **揭露卡正式檔狀態**：`storm-forest-rescue-reveal-cards-half-label.*` 已套用確認版直向資訊層級；正式 PDF 為 2 頁 A4 二分標籤、共 4 張揭露卡，逐頁畫面 QA 通過。`reveal-card-stacked-layout-prototype.*` 僅保留為版面測試紀錄
- **下一步**：黑白試印 v0.7 寶物／後援／三區／揭露卡並跑第一局真人測試；之後以 V2 規格製作包含現有 4 張測試圖在內的 16–24 隻安全牌首批；等實體 Poker 到貨後量測，再調整動物卡面尺寸與四周內縮

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
