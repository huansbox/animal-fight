"""
動物守護者 - 從 JSONL 批次生成圖片

此腳本以 OpenAI Python SDK 呼叫 Images API，支援：
- gpt-image-1.5（回傳 base64，直接存檔；可指定 output_format/background）
- dall-e-3（回傳圖片 URL，再下載存檔）

使用方式：
  1) pip install openai python-dotenv
  2) 在 `card/.env` 填入 OPENAI_API_KEY
  3) python generate_from_jsonl.py

可選參數：
  - 指定輸入 JSONL：python generate_from_jsonl.py --input img-prompt/animal-prompts-api-3-2.jsonl
  - 指定輸出資料夾：python generate_from_jsonl.py --output-dir images
  - 每個 prompt 產多張：python generate_from_jsonl.py --num-images 2
  - 只跑前 N 筆：python generate_from_jsonl.py --limit 1
  - 覆寫既有檔案：python generate_from_jsonl.py --overwrite

輸入檔（JSONL）格式範例：
  {"id":"01","prompt":"..."}
"""

import argparse
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
PROMPT_DIR = SCRIPT_DIR / "img-prompt"
DEFAULT_INPUT_CANDIDATES = [
    PROMPT_DIR / "animal-prompts-api-3-2.jsonl",
    PROMPT_DIR / "animal-prompts-api-3.jsonl",
    PROMPT_DIR / "animal-prompts-api.jsonl",
    SCRIPT_DIR / "animal-prompts-api.jsonl",  # 向下相容舊位置
]
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "images" / "new"


# ============ 工具函數 ============

def pick_default_input_file() -> Path:
    for candidate in DEFAULT_INPUT_CANDIDATES:
        if candidate.exists():
            return candidate
    return DEFAULT_INPUT_CANDIDATES[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="從 JSONL 批次生成圖片（OpenAI Images API）")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=None,
        help="JSONL prompt 檔案路徑（預設會從 card/img-prompt/ 自動挑一個）",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="圖片輸出資料夾（預設：card/images/new/）",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="若輸出檔已存在則覆寫（預設：跳過）",
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=1,
        help="每個 prompt 生成幾張圖（預設：1；>1 時檔名會加 _1/_2... 後綴）",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="跳過前幾筆 prompt（預設：0）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="最多處理幾筆 prompt（0 表示不限制）",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=int,
        default=SLEEP_SECONDS,
        help="每張圖之間等待秒數（避免 rate limit）",
    )
    return parser.parse_args()


def item_num_images(item: dict, default_value: int) -> int:
    """支援在 JSONL 每筆資料覆寫張數：num_images / n / count"""
    for key in ("num_images", "n", "count"):
        if key in item:
            try:
                value = int(item[key])
            except Exception:
                return default_value
            return max(1, value)
    return max(1, default_value)


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
    args = parse_args()
    input_file: Path = args.input or pick_default_input_file()
    output_dir: Path = args.output_dir
    sleep_seconds: int = args.sleep_seconds
    default_num_images: int = max(1, int(args.num_images))
    overwrite: bool = bool(args.overwrite)
    offset: int = max(0, int(args.offset))
    limit: int = max(0, int(args.limit))

    print("=" * 50)
    print("動物守護者 - 批次圖片生成")
    print("=" * 50)
    print(f"模型: {MODEL}")
    print(f"尺寸: {SIZE}")
    print(f"品質: {effective_quality()}")
    print(f"格式: {OUTPUT_FORMAT}")
    print(f"輸入: {input_file}")
    print(f"輸出: {output_dir}")
    print("=" * 50)

    # 檢查 API Key
    if not API_KEY or "在這裡" in API_KEY:
        print("\n錯誤: 請在 .env 檔案設定 OPENAI_API_KEY")
        print(f"檔案位置: {SCRIPT_DIR / '.env'}")
        return

    print("API Key: 已載入")

    if not input_file.exists():
        print("\n錯誤: 找不到輸入 JSONL 檔案")
        print(f"指定路徑: {input_file}")
        if PROMPT_DIR.exists():
            jsonl_files = sorted(PROMPT_DIR.glob("*.jsonl"))
            if jsonl_files:
                print("\n可用的 JSONL（card/img-prompt/）：")
                for p in jsonl_files:
                    print(f"  - {p.name}")
        print("\n你可以用參數指定：")
        print("  python generate_from_jsonl.py --input img-prompt/animal-prompts-api-3-2.jsonl")
        return

    # 建立輸出資料夾
    output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化 client
    client = OpenAI(api_key=API_KEY)

    # 載入 prompts
    prompts = load_prompts(input_file)
    if offset:
        prompts = prompts[offset:]
    if limit:
        prompts = prompts[:limit]
    total = len(prompts)
    print(f"\n載入 {total} 個 prompt\n")

    # 批次生成
    success_images = 0
    for index, item in enumerate(prompts, 1):
        animal_id = str(item.get("id", index)).strip()
        prompt = item.get("prompt", "").strip()

        if not prompt:
            print(f"[{index}/{total}] {animal_id}")
            print("    失敗：prompt 為空")
            continue

        num_images = item_num_images(item, default_num_images)

        for variant_index in range(1, num_images + 1):
            suffix = "" if num_images == 1 else f"_{variant_index}"
            output_path = output_dir / f"{animal_id}{suffix}.{OUTPUT_FORMAT}"
            label = animal_id if num_images == 1 else f"{animal_id} ({variant_index}/{num_images})"

            if output_path.exists() and not overwrite:
                print(f"[{index}/{total}] {label}")
                print(f"    跳過：已存在 {output_path.name}")
                continue

            print(f"[{index}/{total}] {label}")
            print("    生成中...")

            image_bytes = generate_image(client, prompt)

            if image_bytes:
                output_path.write_bytes(image_bytes)
                file_size_kb = output_path.stat().st_size // 1024
                print(f"    完成: {output_path.name} ({file_size_kb} KB)")
                success_images += 1
            else:
                print("    失敗")

            if (index < total or variant_index < num_images) and sleep_seconds > 0:
                print(f"    等待 {sleep_seconds} 秒...")
                time.sleep(sleep_seconds)

    print("\n" + "=" * 50)
    print(f"完成! 新產生圖片: {success_images} 張（處理 prompt: {total} 筆）")
    print(f"圖片位置: {output_dir}")
    print("=" * 50)


if __name__ == "__main__":
    main()
