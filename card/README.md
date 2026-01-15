# 動物卡片（產圖與素材）

## 檔案說明

| 檔案/資料夾 | 用途 |
|---|---|
| `final_cards.html` | A4 全頁列印版（含動物圖與 icon） |
| `generate_from_jsonl.py` | 從 JSONL 批次呼叫 OpenAI Images API 產圖 |
| `img-prompt/` | 產圖用 prompts（`*.jsonl`/`*.md`） |
| `images/` | 產出的動物圖與 icon |
| `.env.example` / `.env` | API Key 範本 / 實際設定（勿提交） |

## 產圖使用方式

### 1) 安裝相依套件

```bash
pip install openai python-dotenv
```

### 2) 設定 API Key

把 `.env.example` 複製成 `.env`，並在 `card/.env` 內設定：
```text
OPENAI_API_KEY=sk-...
```

### 3) 執行批次產圖

```bash
cd D:\mywork\animal-fight\card
python generate_from_jsonl.py
```

指定 prompt 檔（例如 icon）：
```bash
python generate_from_jsonl.py --input img-prompt/icon-prompts-api.jsonl
```

同一個 prompt 產 2 張圖（檔名會變成 `id_1.png`、`id_2.png`）：
```bash
python generate_from_jsonl.py --num-images 2
```

調整每張圖的等待時間（避免 rate limit）：
```bash
python generate_from_jsonl.py --sleep-seconds 8
```

### 4) 輸出結果

圖檔會輸出到 `card/images/new/`（預設會跳過已存在的檔名）。
