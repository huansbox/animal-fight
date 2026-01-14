# Animal Fight - 動物守護者桌遊設計專案

## 專案概述
兒童合作闖關 RPG 桌遊，適合 6-12 歲兒童與家長共玩。Print & Play 自製桌遊格式。

## 專案結構
```
animal-fight/
├── .gitignore
├── CLAUDE.md                 # 專案架構與技術決策
├── README.md                 # 環境設置與快速開始
├── card/                     # 卡片列印檔案
│   └── animal-cards-A4-bw.html
├── docs/
│   ├── prompt.txt            # 原始需求 prompt
│   ├── review-result.md      # 審查報告
│   └── design-versions/      # 設計迭代版本
│       ├── animal-cl.md      # Claude v1
│       ├── animal-ge.md      # Gemini v1
│       ├── animal-gpt.md     # GPT v1 (規格書)
│       ├── animal-cl-2.md    # Claude v2
│       ├── animal-cla-2.md   # Claude 整合優化版 (最佳)
│       └── animal-gpt-2.md   # GPT v2
└── game/
    └── rulebook.md           # 正式規則書 (採用 animal-cla-2)
```

## 技術決策

### 最終採用版本
**animal-cla-2.md** → `game/rulebook.md`
審查總分 132/150（第一名）

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
- [x] 專案結構整理
- [ ] 視覺設計（卡片美術）
- [ ] 印刷測試
- [ ] 實際遊玩測試

## 後續擴充（不納入 MVP）
- 裝備卡
- 狀態效果
- 更多動物系列
- Boss 專屬招式表
