# Animal Fight - 動物守護者桌遊設計專案

## 專案概述
兒童合作闖關 RPG 桌遊，適合 6-12 歲兒童與家長共玩。Print & Play 自製桌遊格式。

## 專案結構
```
animal-fight/
├── animal-fight-prompt.txt   # 原始需求 prompt
├── animal-cl.md              # Claude 第一版
├── animal-ge.md              # Gemini 版本
├── animal-gpt.md             # GPT 規格書版本
├── animal-cl-2.md            # Claude 第二版
├── animal-cla-2.md           # Claude 整合優化版 (最佳)
├── animal-gpt-2.md           # GPT 第二版
├── review-result.md          # 審查報告
├── CLAUDE.md                 # 本文件
└── README.md                 # 環境設置與說明
```

## 技術決策

### 最終採用版本
**animal-cla-2.md** - 審查總分 132/150（第一名）

### 核心機制
- 判定：`2d6 + 屬性數值`
- 難度：DC 10（優勢）/ 12（標準）/ 14（劣勢）
- 生命：共享 5 愛心
- 勝利：累積 5 前進標記 → 終局

### 數值平衡準則
- 動物卡總和：32-38
- 弱項：至少 1 個 ≤ 3
- 亮點：至少 1 個 ≥ 8 或天賦 ≥ 11
- 原型：坦克/速度/輸出/智慧/全能 各 2 張

## 當前狀態
- [x] 需求分析
- [x] 多版本設計
- [x] 審查評分
- [x] 選定最佳版本
- [ ] 視覺設計（卡片美術）
- [ ] 印刷測試
- [ ] 實際遊玩測試

## 後續擴充（不納入 MVP）
- 裝備卡
- 狀態效果
- 更多動物系列
- Boss 專屬招式表
