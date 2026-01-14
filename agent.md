# Agent 指引（animal-fight）

本檔提供給在此專案工作的程式/內容助理（agent）使用：快速理解專案目的、檔案位置、常用流程（列印、產圖、改卡片），並避免踩雷（例如外洩 API key）。

## 專案目標
- 產出可列印（A4 Print & Play）的《動物守護者》兒童合作闖關桌遊。
- 同時包含合作闖關（RPG）與動物大對決（淘汰賽）兩種模式。

## 回應語言
- 預設以繁體中文溝通；專業術語可保留原文（例如 JSON、API、LLM）。

## 專案結構（最常用）
- `game/`
  - `game/rulebook.md`：合作闖關規則書
  - `game/battle-rules.md`：動物大對決規則
- `card/`
  - `card/final_cards.html`：A4 全頁列印版（含動物圖與 icon）
  - `card/animal-cards-A4-bw.html`：黑白列印版
  - `card/animal-cards-A4-emoji.html`：emoji 佔位的卡片模版（方便改版面/字級/格線）
  - `card/images/`：輸出的動物圖與 icon（**gitignore**；避免把大量圖檔提交）
  - `card/img-prompt/`：產圖用 prompts（JSONL/MD）
  - `card/generate_from_jsonl.py`：從 JSONL 批次產圖腳本
- `docs/`
  - `docs/prompt.txt`：原始需求
  - `docs/review-result.md`：多版本審查報告
  - `docs/design-versions/`：設計版本存檔
- `sim/`
  - `sim/battle_sim.py`：對戰模擬（用來看配對勝率/平衡）

## 列印流程（給人類/DM 的快速指引）
- 先看規則：`game/rulebook.md`
- 直接列印卡片：用瀏覽器開 `card/final_cards.html` 或 `card/animal-cards-A4-bw.html` → 列印（A4、建議 160–200gsm、100% 實際大小）→ 裁切。

## 產圖流程（OpenAI Images API）

### 重要檔案
- API key：`card/.env`（**不要**把 key 貼到對話/issue/commit；也不要在回覆中印出 `.env` 內容）
- prompts：`card/img-prompt/*.jsonl`
- 產出圖檔：`card/images/`（已在 `.gitignore` 排除）

### 一般操作
1. 確認 `card/.env` 有 `OPENAI_API_KEY=...`
2. 進入 `card/` 目錄後執行：`python generate_from_jsonl.py`
3. 成功後圖檔會出現在 `card/images/`

### 模型與 quality 注意事項
- `gpt-image-1.5`：`quality` 支援 `low | medium | high | auto`
- `dall-e-3`：`quality` 支援 `standard | hd`
- 若遇到 `403 PermissionDenied`，通常是 organization 權限/驗證尚未完成。

## 修改卡片/規則時的注意事項
- **一致性**：改了屬性、DC、或卡片欄位，需同步更新 `game/` 規則書與 `card/` 版面。
- **避免覆蓋素材**：
  - 批次產圖建議用「跳過已存在檔案」或「新檔名」策略，避免把原本可用的圖蓋掉。
- **避免外洩機密**：
  - 不要輸出/記錄/貼出 `OPENAI_API_KEY`。
  - 產圖與測試時若需要貼 log，先把 key 打碼。

## 常見任務指引
- 想快速調整卡片 UI（格線、字級、位置）：優先改 `card/animal-cards-A4-emoji.html`，確認排版 OK 後再套回有圖片的 `card/final_cards.html`。
- 想新增動物：
  1) 補數值/天賦（對齊規則與平衡）→ 2) 在 `card/img-prompt/` 新增 prompt → 3) 批次產圖到 `card/images/` → 4) 更新 `card/final_cards.html`。
