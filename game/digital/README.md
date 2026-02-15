# 動物大對決 — 數位版

離線單機版，瀏覽器開 `index.html` 即可遊玩。
目標裝置：MacBook Pro 14 吋（搭飛機/火車讓小孩玩）。

## 啟動

ES Modules 需要 HTTP server，不能直接雙擊 `index.html`。
**必須從專案根目錄啟動**（圖片路徑需要存取 `card/images/`）。

```bash
cd animal-fight          # 專案根目錄
python -m http.server 8080
# 瀏覽器開 http://localhost:8080/game/digital/
```

或用 Node.js：

```bash
npx serve .              # 從專案根目錄
# 瀏覽器開 http://localhost:3000/game/digital/
```

## 遊戲流程

```
主選單 → 賽制設定 → 選角 → 對戰（逐場） → 冠軍
```

### 主選單

- **VS 電腦**：選 AI 難度（簡單/普通/困難）後進設定
- **雙人對戰**：直接進設定

### 賽制設定

- **規模**：4 / 8 / 16 / 32 強
- **選角方式**：
  - **快速隨機** — 系統隨機分配，跳過選角直接開打
  - **選秀** — 系統抽 N 隻組成池，Snake Draft 輪選（A1 → B2 → A2 → B2 ...）
  - **自選** — 全部 128 隻為池，Snake Draft 輪選，有搜尋 + 排序

### 對戰

- 左右對稱佈局，卡片框線 / 骰子框 / 分數文字依隊伍著色（藍 vs 紅）
- 雙方分開擲骰：玩家按按鈕互動擲骰，電腦自動擲骰
- 骰到 6 → 天賦觸發閃光 + 計數器 → 玩家按「重骰！」（電腦自動重骰）
- 分數拆解逐步顯示：`力量 7 + 攻擊 8 = 15`，天賦加成內嵌 `+(2x1)`
- 卡片顯示技能加成明細（如 `力+2  攻+2`）
- 平手自動加賽
- 每場結束後彈出全螢幕淘汰賽表（橫向左到右，含連接線、比分與隊伍色圓點）
- 對戰中可隨時按「🏆 對戰表」查看晉級狀態
- 第二輪以後動物混戰時，仍保持原始隊伍識別

### 冠軍

- 顯示冠軍卡片、戰績
- 「再來一局」保留模式/難度設定，「回主選單」完全重置

## AI 難度

難度只影響選角策略，對戰骰子完全隨機。

| 難度 | 選角策略 |
|------|----------|
| 簡單 | 隨機挑選 |
| 普通 | 從總和前 50% 中隨機 |
| 困難 | 貪心選總和最高的 |

## 對戰規則

- 雙方各擲 2d6
- 骰面 1-5 對應五屬性（力量/速度/攻擊/防禦/智慧）
- 兩顆骰面相同 → 該屬性 x2
- 骰到 6 → 天賦觸發（重骰 + 條件加分），可連續觸發
- 天賦加分：觸發次數 x 最終骰面命中的技能加成屬性之和
- 分數高者勝，平手則加賽

## 檔案結構

```
game/digital/
├── index.html            # 進入點（單頁 5 畫面）
├── css/style.css         # 樣式 + 動畫
├── js/
│   ├── app.js            # 主流程、畫面切換、UI 事件
│   ├── battle.js         # 對戰引擎（純邏輯，無 DOM）
│   ├── draft.js          # 三種選角模式
│   ├── ai.js             # AI 選角策略
│   ├── bracket.js        # 淘汰賽樹邏輯 + 橫向 bracket 渲染
│   ├── animations.js     # 骰子滾動、天賦閃光、勝負特效
│   └── utils.js          # Fisher-Yates shuffle
└── data/animals.json     # 128 隻動物資料
```

## 維護筆記

### 圖片

圖片不在此目錄，引用路徑為 `../../card/images/{id}.png`。
因此 HTTP server **必須從專案根目錄啟動**，否則瀏覽器無法存取 `card/images/`。
缺圖的動物會顯示灰色 `?` placeholder（透過 `<img onerror>`）。

### 新增動物

1. 在 `data/animals.json` 加入新動物，格式：
   ```json
   {
     "id": "snake_id",
     "name": "中文名",
     "en": "English Name",
     "img": "snake_id.png",
     "stats": [力量, 速度, 攻擊, 防禦, 智慧],
     "skillName": "四字技能",
     "skillDesc": "15-25 字技能描述",
     "skillBonus": [{"attr": 0, "val": 2}, {"attr": 2, "val": 2}]
   }
   ```
   - `stats` index 0-4 = 力量/速度/攻擊/防禦/智慧
   - `skillBonus` 的 `attr` 對應 stats index，`val` 加總必須 = 4
2. 對應圖片放入 `card/images/`

### 修改對戰規則

只需改 `js/battle.js`，該檔案是純邏輯無 DOM 依賴。
對戰流程邏輯在 `js/app.js` 的 `playFullBattle()`。

### 設計文件

- 需求與畫面設計：`docs/plans/2026-02-14-digital-battle-design.md`
- 實作計畫（11 Task）：`docs/plans/2026-02-14-digital-battle-plan.md`
