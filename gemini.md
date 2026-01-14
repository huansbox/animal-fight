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
- **平衡區間**：基礎 5 屬性總和落在 **23 - 28** 點。

## 📂 重要檔案路徑
- **設計總綱**：`game/rulebook.md` (包含完整動物清單與數值)。
- **對戰規則**：`game/battle-rules.md` (淘汰賽細則與加成表)。
- **列印檔案**：`card/final_cards.html` (整合所有 AI 圖卡的最終版)。
- **AI 繪圖指令**：
    - `animal-ai-prompts.md` (第一波 10 隻)。
    - `animal-ai-prompts2.md` (第二波 6 隻)。
    - `card/icon-ai-prompts.md` (屬性圖示)。

## 🛠️ 待辦事項 (Todo)
- [ ] 產出第二波 6 隻動物圖片 (`tortoise`, `impala`, `tiger`, `crocodile`, `fox`, `kangaroo`)。
- [ ] 更新 `card/final_cards.html` 以包含 16 隻動物。
- [ ] 測試「加成表」在實際擲骰時的平衡性。
- [ ] (選修) 設計 Boss 戰與場景劇本。

---
*上次更新日期：2026年1月14日*
