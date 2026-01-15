# 《動物守護者 (Animal Guardians)》專案備忘錄 (Gemini Context)

## 📌 專案概況
本專案旨在開發一套適合 6-12 歲兒童遊玩的 Print & Play (PnP) 合作/對戰 RPG 桌遊。
- **核心設計師**：家長 (DM) & Gemini
- **視覺風格**：黑白向量線稿 (適合雷射列印、可著色)、滿版 A4 卡片。

## 📖 核心規則 (淘汰賽版)
- **判定方式**：各自擲 2d6 + 屬性數值，比大。
- **同號 (Double)**：該數值 x 2。
- **單顆 6 (Joker)**：觸發「天賦加成」，總分固定 +4 (分配至特定屬性)。
- **雙顆 6 (Burst)**：重骰 2 顆，並固定套用一次 +4 加成。
- **平衡與真實性**：基礎 5 屬性總和原則上落在 **23 - 28** 點，特殊個體（如藍鯨 31、鬣狗 29）依真實性可微幅調整。

## 📂 重要檔案路徑
- **設計總綱**：`game/rulebook.md` (包含基礎動物清單與數值)。
- **對戰規則**：`game/battle-rules.md` (淘汰賽細則與加成表)。
- **最新設計定案**：`docs/260115-animal-final.md` (新增 19 隻動物之最終屬性與技能描述)。
- **列印檔案**：`card/final_cards.html` (整合 AI 圖卡的最終版)。
- **AI 繪圖指令**：
    - `card/img-prompt/animal-ai-prompts-3.md` (第三波 19 隻 Prompt 強調動態定案版)。
    - `card/img-prompt/animal-prompts-api-3.jsonl` (API 批次生成用指令)。
    - `card/img-prompt/animal-prompts-api-3-2.jsonl` (ID 結尾為 2 的變體版本)。
    - `card/img-prompt/animal-prompts-api-3-3.jsonl` (針對火雞、犛牛、大耳狐、食蟻獸的優化動作版本)。

## 🛠️ 待辦事項 (Todo)
- [ ] 產出第三波 19 隻動物圖片 (依據 `animal-prompts-api-3.jsonl` 或優化版 `3-3`)。
- [ ] 更新 `card/final_cards.html` 以包含全數 35 隻動物。
- [ ] 測試「加成表」在實際擲骰時的平衡性。
- [ ] (選修) 設計 Boss 戰與場景劇本。

---
*上次更新日期：2026年1月15日*
