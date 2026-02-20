# Animal Guardians 動物守護者

兒童桌遊 - Print & Play 版本（132 張動物卡）

## 遊戲模式

### 合作闘關
- **玩家人數**：2-3 人（1 DM + 2 小玩家）
- **遊戲時間**：15-20 分鐘
- **規則書**：[`game/rulebook.md`](game/rulebook.md)

### 動物大對決
- **玩家人數**：2 人
- **遊戲時間**：5-15 分鐘
- **規則書**：[`game/battle-rules.md`](game/battle-rules.md)
- **數位版**：[`game/digital/`](game/digital/)（離線 Web App，瀏覽器即玩）

### 動物猜猜看
- **玩家人數**：1 人
- **遊戲時間**：5-10 分鐘
- **數位版**：[`game/quiz/`](game/quiz/)（離線 Web App，瀏覽器即玩）
- **玩法**：每題給 3 個提示，從 5 個選項猜動物，132 隻全收錄

**適合年齡**：6-12 歲

## 快速開始

### 實體版

**需要準備**
- 2 顆六面骰（2d6）
- 5 個愛心標記（硬幣、糖果皆可）
- 列印好的動物卡

**列印說明**
1. 開啟 [`card/final_cards.html`](card/final_cards.html)（128 張動物卡）
2. 使用瀏覽器列印功能
3. A4 紙列印，建議 160gsm 以上
4. 裁切成 63×88mm 卡片

### 數位版（對決 + 猜猜看）

從專案根目錄啟動 HTTP server：

```bash
cd animal-fight
python -m http.server 8080
# 動物大對決 http://localhost:8080/game/digital/
# 動物猜猜看 http://localhost:8080/game/quiz/
```

詳細說明見 [`game/digital/README.md`](game/digital/README.md)

## 圖片生成

圖片分兩套，分別供列印版和數位版使用：

| 目錄 | 用途 | 風格 | 生成方式 |
|------|------|------|---------|
| `card/images/` | 列印版（final_cards.html） | per-wave prompt 風格 | `generate_from_jsonl.py` 逐張生成 |
| `card/images-realistic/` | 數位版（game/digital/） | 寫實大頭照 | `batch_generate.py` Batch API 批次生成 |

**數位版圖片生成（寫實風格）：**

```bash
pip install openai python-dotenv
# 在 card/.env 填入 OPENAI_API_KEY

cd card
python3 batch_generate.py generate --skip-existing  # 產生 JSONL
python3 batch_generate.py submit                     # 提交 batch job
python3 batch_generate.py status --wait              # 等待完成
python3 batch_generate.py download                   # 下載至 images-realistic/
```

## 專案結構

```
animal-fight/
├── card/
│   ├── final_cards.html      # A4 列印版（128 張動物卡）
│   ├── batch_generate.py     # Batch API 批次生成寫實圖片
│   ├── generate_from_jsonl.py # 單張即時生成（舊版）
│   ├── data/                 # 結構化動物資料（per-wave JSON）
│   ├── images/               # 列印版圖片（per-wave prompt 風格）
│   └── images-realistic/     # 數位版圖片（寫實風格，Batch API 生成）
├── game/
│   ├── rulebook.md           # 合作闘關規則書
│   ├── battle-rules.md       # 動物大對決規則
│   ├── digital/              # 動物大對決數位版（離線 Web App）
│   └── quiz/                 # 動物猜猜看（離線 Web App）
├── docs/
│   ├── attributes.md         # 動物屬性數值表（v2.5）
│   └── design-versions/      # 設計迭代版本存檔
└── sim/
    ├── battle_sim_v5.py      # 對戰模擬器（64 隻，新版骰 6 規則）
    ├── battle_sim_v4.py      # 對戰模擬器（48 隻，3 強循環賽）
    └── battle_sim_v3.py      # 對戰模擬器（35 隻，原規則）
```

## 動物一覽（132 張）

### 第一波（16 張）
非洲獅、非洲象、大猩猩、灣鱷、蜜獾、蘇門答臘虎、海豚、科摩多龍、獵豹、北極狐、紅袋鼠、遊隼、黑斑羚、貓頭鷹、穿山甲、加拉巴哥象龜

### 第三波（19 張）
鬣狗、美洲野牛、山豬、犛牛、麋鹿、駱駝、非洲野犬、疣豬、水鹿、長臂猿、食蟻獸、豪豬、黃鼠狼、鴨嘴獸、大耳狐、狐獴、火雞、樹懶、藍鯨

### 第四波（13 張）
大白鯊、河馬、北極熊、犀牛、花豹、灰狼、狼獾、麝牛、長頸鹿、蟒蛇、人、鵜鶘、丹頂鶴

### 第五波（20 張）
虎鯨、鴕鳥、雪豹、白頭海鵰、電鰻、雪鴞、乳牛、擬態章魚、海獺、浣熊、蠍子、皇帝企鵝、犰狳、孔雀、箭毒蛙、蘭花螳螂、家豬、猞猁、雲豹、綠鬣蜥

### 第六波（16 張）
棕熊、美洲豹、海象、野馬、斑馬、大熊貓、牧羊犬、眼鏡蛇、螳螂蝦、兀鷲、羊駝、臭鼬、鈍尾毒蜥、巨嘴鳥、河豚、獨角仙

### 第七波（14 張，Creature Cases 系列）
象海豹、紅毛猩猩、鱷龜、郊狼、啄羊鸚鵡、水豚、安地斯神鷲、小貓熊、狼蛛、負鼠、針鼴、裸鼴鼠、喙頭蜥、糞金龜

### 第八波（8 張）
黑豹、日本獼猴、袋熊、喜馬拉雅塔爾羊、橡實啄木鳥、東部灰松鼠、公雞、鼷鹿

### 第九波（22 張）
長毛象、座頭鯨、黑猩猩、森蚺、眼鏡熊、大西洋劍魚、角鵰、短尾貓、食人魚、金剛鸚鵡、渡鴉、狐蝠、海龜、變色龍、刺蝟、北極兔、蜂鳥、水母、無尾熊、行軍蟻、竹節蟲、螢火蟲

### 第十波（4 張，上野動物園特區）
侏儒河馬、指猴、㺢㹢狓、鯨頭鸛

## 授權
個人使用，非商業用途
