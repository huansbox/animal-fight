"""
動物守護者 - Batch API 批次生成寫實風格動物大頭照

使用 OpenAI Batch API（50% 折扣）批次生成 128 張動物圖片。
從 animals.json 讀取動物清單，依類別自動套用 prompt 模板。

子命令：
  generate  從 animals.json 生成 Batch API 格式 JSONL
  submit    上傳 JSONL + 建立 batch job
  status    查詢 batch job 進度
  download  下載結果、解碼 b64、存 PNG

使用方式：
  pip install openai python-dotenv
  在 card/.env 填入 OPENAI_API_KEY

  python3 batch_generate.py generate --skip-existing
  python3 batch_generate.py submit
  python3 batch_generate.py status --wait --interval 60
  python3 batch_generate.py download
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ANIMALS_JSON = SCRIPT_DIR.parent / "game" / "digital" / "data" / "animals.json"
BATCH_INPUT = SCRIPT_DIR / "batch_input.jsonl"
STATE_FILE = SCRIPT_DIR / ".batch_state.json"
IMAGES_DIR = SCRIPT_DIR / "images"

# ── 已完成的 10 張寫實圖片（不重複生成） ──
EXISTING_REALISTIC = {
    "tiger", "orca", "owl", "pangolin", "komodo",
    "mantis_shrimp", "gorilla", "hippopotamus", "bald_eagle", "pufferfish",
}

# ── Prompt 模板 ──
SUFFIX = (
    "facing slightly left, natural lighting, "
    "solid dark teal background, studio-quality, square format, "
    "no text, no watermark"
)

# ── 動物分類 ──
BIRDS = {
    "owl", "falcon", "bald_eagle", "snowy_owl", "ostrich", "peacock",
    "pelican", "red_crowned_crane", "emperor_penguin", "turkey",
    "griffon_vulture", "toco_toucan", "kea", "andean_condor",
    "acorn_woodpecker", "rooster", "harpy_eagle", "scarlet_macaw",
    "hummingbird", "raven",
}

REPTILES = {
    "komodo", "crocodile", "tortoise", "green_iguana", "king_cobra",
    "gila_monster", "tuatara", "chameleon", "python", "snapping_turtle",
    "sea_turtle",
}

FISH = {
    "great_white_shark", "electric_eel", "piranha", "swordfish", "pufferfish",
}

MARINE_MAMMALS = {
    "dolphin", "blue_whale", "orca", "walrus", "sea_otter",
    "elephant_seal", "humpback_whale",
}

AMPHIBIANS = {"poison_dart_frog"}

CEPHALOPODS = {"mimic_octopus"}

# macro 模板：昆蟲 / 節肢動物
MACRO = {
    "orchid_mantis", "rhino_beetle", "tarantula", "dung_beetle",
    "scorpion", "firefly", "army_ant", "walking_stick", "hedgehog",
}

# subject 覆寫
SUBJECT_OVERRIDES = {
    "black_panther": "melanistic Black Panther (leopard with all-black coat)",
    "woolly_mammoth": "Woolly Mammoth (prehistoric elephant)",
    "human": "young human child",
}


def get_template(animal_id: str) -> tuple[str, str]:
    """回傳 (prefix, features)"""
    if animal_id == "human":
        return "realistic portrait photograph", "facial features"
    if animal_id == "woolly_mammoth":
        return "realistic illustration portrait", "thick fur and curved tusks"
    if animal_id == "jellyfish":
        return "realistic macro portrait photograph", "translucent bell and trailing tentacles"
    if animal_id in MACRO:
        return "realistic macro portrait photograph", "exoskeleton and body texture"
    if animal_id in BIRDS:
        return "realistic wildlife portrait photograph", "plumage and beak"
    if animal_id in REPTILES:
        return "realistic wildlife portrait photograph", "scales and eyes"
    if animal_id in FISH:
        return "realistic wildlife portrait photograph", "scales and fins"
    if animal_id in MARINE_MAMMALS:
        return "realistic wildlife portrait photograph", "smooth skin and eyes"
    if animal_id in AMPHIBIANS:
        return "realistic wildlife portrait photograph", "vivid skin coloring"
    if animal_id in CEPHALOPODS:
        return "realistic wildlife portrait photograph", "tentacles and skin texture"
    # 預設：哺乳類
    return "realistic wildlife portrait photograph", "fur and eyes"


def build_prompt(animal_id: str, en_name: str) -> str:
    subject = SUBJECT_OVERRIDES.get(animal_id, en_name)
    prefix, features = get_template(animal_id)
    return f"{prefix} of a {subject}, showcasing {features}, {SUFFIX}"


def load_animals() -> list[dict]:
    with open(ANIMALS_JSON, encoding="utf-8") as f:
        return json.load(f)


# ── generate 子命令 ──

def cmd_generate(args: argparse.Namespace) -> None:
    animals = load_animals()
    skip_existing = args.skip_existing

    existing_files = set()
    if skip_existing and IMAGES_DIR.exists():
        existing_files = {p.stem for p in IMAGES_DIR.glob("*.png")}

    lines = []
    skipped = 0
    for animal in animals:
        aid = animal["id"]
        en = animal["en"]

        if skip_existing and aid in existing_files:
            skipped += 1
            continue

        prompt = build_prompt(aid, en)
        row = {
            "custom_id": aid,
            "method": "POST",
            "url": "/v1/images/generations",
            "body": {
                "model": "gpt-image-1.5",
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "medium",
                "output_format": "png",
            },
        }
        lines.append(json.dumps(row, ensure_ascii=False))

    BATCH_INPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已生成 {len(lines)} 行 → {BATCH_INPUT}")
    if skipped:
        print(f"跳過 {skipped} 隻（images/ 已有 PNG）")


# ── submit 子命令 ──

def cmd_submit(args: argparse.Namespace) -> None:
    _require_openai()
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv(SCRIPT_DIR / ".env")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not BATCH_INPUT.exists():
        print(f"找不到 {BATCH_INPUT}，請先執行 generate")
        sys.exit(1)

    # 上傳檔案
    print("上傳 JSONL...")
    with open(BATCH_INPUT, "rb") as f:
        file_obj = client.files.create(file=f, purpose="batch")
    print(f"檔案 ID: {file_obj.id}")

    # 建立 batch
    print("建立 batch job...")
    batch = client.batches.create(
        input_file_id=file_obj.id,
        endpoint="/v1/images/generations",
        completion_window="24h",
    )
    print(f"Batch ID: {batch.id}")
    print(f"狀態: {batch.status}")

    # 儲存狀態
    state = {
        "batch_id": batch.id,
        "input_file_id": file_obj.id,
        "created_at": batch.created_at,
    }
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(f"狀態已存至 {STATE_FILE}")


# ── status 子命令 ──

def cmd_status(args: argparse.Namespace) -> None:
    _require_openai()
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv(SCRIPT_DIR / ".env")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    state = _load_state()
    batch_id = state["batch_id"]
    wait = args.wait
    interval = args.interval

    while True:
        batch = client.batches.retrieve(batch_id)
        completed = batch.request_counts.completed if batch.request_counts else 0
        failed = batch.request_counts.failed if batch.request_counts else 0
        total = batch.request_counts.total if batch.request_counts else 0

        print(f"[{time.strftime('%H:%M:%S')}] 狀態: {batch.status}  "
              f"進度: {completed}/{total}  失敗: {failed}")

        if batch.status in ("completed", "failed", "expired", "cancelled"):
            if batch.output_file_id:
                state["output_file_id"] = batch.output_file_id
                STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
            if batch.error_file_id:
                state["error_file_id"] = batch.error_file_id
                STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
            break

        if not wait:
            break

        time.sleep(interval)


# ── download 子命令 ──

def cmd_download(args: argparse.Namespace) -> None:
    _require_openai()
    from openai import OpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv(SCRIPT_DIR / ".env")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    state = _load_state()

    # 若 state 沒有 output_file_id，先查一次
    if "output_file_id" not in state:
        batch = client.batches.retrieve(state["batch_id"])
        if batch.output_file_id:
            state["output_file_id"] = batch.output_file_id
            STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
        else:
            print(f"Batch 尚未完成（狀態: {batch.status}）")
            sys.exit(1)

    output_file_id = state["output_file_id"]
    print(f"下載結果檔 {output_file_id}...")
    content = client.files.content(output_file_id)
    raw_text = content.text

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    success = 0
    failed = 0
    for line in raw_text.strip().split("\n"):
        if not line.strip():
            continue
        result = json.loads(line)
        custom_id = result["custom_id"]
        response = result.get("response", {})
        status_code = response.get("status_code", 0)

        if status_code != 200:
            error = response.get("body", {}).get("error", {}).get("message", "unknown")
            print(f"  {custom_id}: 失敗 ({status_code}) - {error}")
            failed += 1
            continue

        body = response.get("body", {})
        data_list = body.get("data", [])
        if not data_list:
            print(f"  {custom_id}: 無圖片資料")
            failed += 1
            continue

        b64 = data_list[0].get("b64_json", "")
        if not b64:
            print(f"  {custom_id}: b64_json 為空")
            failed += 1
            continue

        img_bytes = base64.b64decode(b64)
        out_path = IMAGES_DIR / f"{custom_id}.png"
        out_path.write_bytes(img_bytes)
        size_kb = len(img_bytes) // 1024
        print(f"  {custom_id}: {size_kb} KB")
        success += 1

    # 下載錯誤檔（如果有）
    if state.get("error_file_id"):
        print(f"\n下載錯誤檔 {state['error_file_id']}...")
        err_content = client.files.content(state["error_file_id"])
        err_path = SCRIPT_DIR / "batch_errors.jsonl"
        err_path.write_text(err_content.text, encoding="utf-8")
        print(f"錯誤詳情已存至 {err_path}")

    print(f"\n完成: {success} 張成功, {failed} 張失敗")
    print(f"圖片位置: {IMAGES_DIR}")


# ── 工具函數 ──

def _require_openai() -> None:
    try:
        import openai  # noqa: F401
        import dotenv  # noqa: F401
    except ImportError:
        print("請先安裝依賴: pip install openai python-dotenv")
        sys.exit(1)


def _load_state() -> dict:
    if not STATE_FILE.exists():
        print(f"找不到 {STATE_FILE}，請先執行 submit")
        sys.exit(1)
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


# ── CLI ──

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch API 批次生成動物大頭照"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # generate
    gen_parser = sub.add_parser("generate", help="從 animals.json 生成 JSONL")
    gen_parser.add_argument(
        "--skip-existing", action="store_true",
        help="跳過 images/ 已有 PNG 的動物",
    )

    # submit
    sub.add_parser("submit", help="上傳 JSONL + 建立 batch job")

    # status
    st_parser = sub.add_parser("status", help="查詢 batch job 進度")
    st_parser.add_argument("--wait", action="store_true", help="持續等待直到完成")
    st_parser.add_argument("--interval", type=int, default=60, help="輪詢間隔秒數")

    # download
    sub.add_parser("download", help="下載結果並存 PNG")

    args = parser.parse_args()

    commands = {
        "generate": cmd_generate,
        "submit": cmd_submit,
        "status": cmd_status,
        "download": cmd_download,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
