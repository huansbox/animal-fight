"""
動物守護者 - 從 JSONL 批次生成圖片

此腳本以 OpenAI Python SDK 呼叫 Images API，支援：
- gpt-image-1.5（回傳 base64，直接存檔；可指定 output_format/background）
- dall-e-3（回傳圖片 URL，再下載存檔）

使用方式：
  1) pip install openai python-dotenv
  2) 在 `card/.env` 填入 OPENAI_API_KEY
  3) python generate_from_jsonl.py

輸入檔（JSONL）格式範例：
  {"id":"01","prompt":"..."}
"""

import base64
import json
import os
import re
import time
from pathlib import Path
from urllib.request import urlopen, Request

from dotenv import load_dotenv
from openai import OpenAI

# ============ 載入 .env ============
SCRIPT_DIR = Path(__file__).parent
load_dotenv(SCRIPT_DIR / ".env")

# ============ 設定區 ============
API_KEY = os.getenv("OPENAI_API_KEY")

# 模型設定
# - "gpt-image-1.5": 回傳 b64_json（建議用這個）
# - "dall-e-3": 回傳 URL（需再下載）
MODEL = "gpt-image-1.5"

# 影像輸出設定
SIZE = "1024x1024"  # 1024x1024 | 1792x1024 | 1024x1792
# 注意：quality 參數各模型支援的值不同
# - gpt-image-1.5：low | medium | high | auto
# - dall-e-3：standard | hd
GPT_IMAGE_QUALITY = "auto"
DALLE_QUALITY = "standard"
OUTPUT_FORMAT = "png"  # png | jpeg | webp（gpt-image-1.5 支援）
BACKGROUND = "auto"  # auto | transparent | opaque（依模型支援）

# 批次節流（避免 rate limit）
SLEEP_SECONDS = 5

# 檔案路徑
INPUT_FILE = SCRIPT_DIR / "animal-prompts-api.jsonl"
OUTPUT_DIR = SCRIPT_DIR / "images"


# ============ 工具函數 ============

def retryable_sleep(attempt: int) -> None:
    """指數退避等待"""
    time.sleep(min(2**attempt, 20))


def load_prompts(jsonl_path: Path) -> list[dict]:
    """從 JSONL 載入 prompt"""
    prompts: list[dict] = []
    with open(jsonl_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            # 移除 Midjourney 參數 --ar 1:1（避免污染 prompt）
            data["prompt"] = re.sub(r"\s*--ar\s+[\d:]+\s*$", "", data["prompt"])
            prompts.append(data)
    return prompts


def download_url(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "animal-guardians/1.0"})
    with urlopen(request, timeout=60) as resp:
        return resp.read()


def generate_image(client: OpenAI, prompt: str) -> bytes | None:
    """呼叫 API 生成圖片，含重試機制。成功回傳 bytes，失敗回傳 None。"""

    for attempt in range(6):
        try:
            if MODEL.startswith("gpt-image"):
                # gpt-image-1.5：回傳 base64（b64_json）
                response = client.images.generate(
                    model=MODEL,
                    prompt=prompt,
                    size=SIZE,
                    quality=GPT_IMAGE_QUALITY,
                    output_format=OUTPUT_FORMAT,
                    background=BACKGROUND,
                )

                b64_data = response.data[0].b64_json
                return base64.b64decode(b64_data)

            # dall-e-3：預設回傳 URL
            response = client.images.generate(
                model=MODEL,
                prompt=prompt,
                size=SIZE,
                quality=DALLE_QUALITY,
            )

            url = response.data[0].url
            return download_url(url)

        except Exception as exc:
            if attempt == 5:
                print(f"    錯誤: {exc}")
                return None

            print(f"    重試 {attempt + 1}/5...")
            retryable_sleep(attempt)

    return None


def effective_quality() -> str:
    return GPT_IMAGE_QUALITY if MODEL.startswith("gpt-image") else DALLE_QUALITY


def main() -> None:
    print("=" * 50)
    print("動物守護者 - 批次圖片生成")
    print("=" * 50)
    print(f"模型: {MODEL}")
    print(f"尺寸: {SIZE}")
    print(f"品質: {effective_quality()}")
    print(f"格式: {OUTPUT_FORMAT}")
    print(f"輸入: {INPUT_FILE.name}")
    print(f"輸出: {OUTPUT_DIR}")
    print("=" * 50)

    # 檢查 API Key
    if not API_KEY or "在這裡" in API_KEY:
        print("\n錯誤: 請在 .env 檔案設定 OPENAI_API_KEY")
        print(f"檔案位置: {SCRIPT_DIR / '.env'}")
        return

    print(f"API Key: {API_KEY[:12]}...{API_KEY[-4:]}")

    # 建立輸出資料夾
    OUTPUT_DIR.mkdir(exist_ok=True)

    # 初始化 client
    client = OpenAI(api_key=API_KEY)

    # 載入 prompts
    prompts = load_prompts(INPUT_FILE)
    total = len(prompts)
    print(f"\n載入 {total} 個 prompt\n")

    # 批次生成
    success = 0
    for index, item in enumerate(prompts, 1):
        animal_id = str(item.get("id", index)).strip()
        prompt = item.get("prompt", "").strip()

        if not prompt:
            print(f"[{index}/{total}] {animal_id}")
            print("    失敗：prompt 為空")
            continue

        output_path = OUTPUT_DIR / f"{animal_id}.{OUTPUT_FORMAT}"
        if output_path.exists():
            print(f"[{index}/{total}] {animal_id}")
            print(f"    跳過：已存在 {output_path.name}")
            continue

        print(f"[{index}/{total}] {animal_id}")
        print("    生成中...")

        image_bytes = generate_image(client, prompt)

        if image_bytes:
            output_path.write_bytes(image_bytes)
            file_size_kb = output_path.stat().st_size // 1024
            print(f"    完成: {output_path.name} ({file_size_kb} KB)")
            success += 1
        else:
            print("    失敗")

        if index < total and SLEEP_SECONDS > 0:
            print(f"    等待 {SLEEP_SECONDS} 秒...")
            time.sleep(SLEEP_SECONDS)

    print("\n" + "=" * 50)
    print(f"完成! 成功: {success}/{total}")
    print(f"圖片位置: {OUTPUT_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
