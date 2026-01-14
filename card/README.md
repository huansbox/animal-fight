# 動物卡片生成

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `prompts.json` | 10 隻動物的 prompt 清單 |
| `generate_images.py` | 批次呼叫 OpenAI API 生成圖片 |
| `animal-cards-template.html` | 卡片模板（Emoji 版） |
| `images/` | 生成的圖片存放位置 |

## 使用方式

### 1. 安裝相依套件

```bash
pip install openai
```

### 2. 設定 API Key

```bash
# Windows CMD
set OPENAI_API_KEY=sk-xxxxxxxx

# Windows PowerShell
$env:OPENAI_API_KEY="sk-xxxxxxxx"

# Mac/Linux
export OPENAI_API_KEY=sk-xxxxxxxx
```

### 3. 執行腳本

```bash
cd D:\mywork\animal-fight\card
python generate_images.py
```

### 4. 輸出結果

圖片將儲存至 `card/images/` 資料夾：
```
images/
├── elephant.png
├── tortoise.png
├── cheetah.png
├── falcon.png
├── komodo.png
├── tiger.png
├── owl.png
├── dolphin.png
├── wolf.png
└── honeybadger.png
```

## 模型選擇

| 模型 | 品質 | 價格 | 速度 |
|------|------|------|------|
| `gpt-image-1` | 最高 | ~$0.04/張 | 慢 |
| `dall-e-3` | 高 | ~$0.04/張 | 中 |
| `dall-e-2` | 中 | ~$0.02/張 | 快 |

修改 `generate_images.py` 中的 `MODEL` 變數切換模型。

## 自訂 Prompt

編輯 `prompts.json`，每個 prompt 包含：
- `id`: 檔名（英文）
- `name`: 動物名稱（顯示用）
- `prompt`: 圖片生成指令

### Prompt 結構建議

```
[動物名稱], children's book illustration style,
simple flat design, soft pastel colors,
white background, centered composition,
cute and friendly expression,
[特徵1], [特徵2], [特徵3],
digital art, high quality
```

## 費用估算

10 張圖片（gpt-image-1, 1024x1024, medium）：
- 約 $0.40 USD
- 執行時間約 3-5 分鐘（含 rate limit 等待）

## 常見問題

### Rate Limit 錯誤
腳本預設每張圖片間隔 15 秒，若仍遇到 rate limit，可增加 `time.sleep()` 時間。

### 圖片風格不一致
確保所有 prompt 使用相同的風格關鍵字：
- `children's book illustration style`
- `simple flat design`
- `soft pastel colors`
