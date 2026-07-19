#!/usr/bin/env python3
"""Build production Bopomofo WOFF2 subsets for animal and team-mission cards."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path

try:
    from fontTools import subset
    from fontTools.ttLib import TTFont
except ImportError as exc:  # pragma: no cover - dependency gate
    raise SystemExit(
        "缺少字型建置依賴。請執行：\n"
        "uv run --with-requirements card/requirements-fonts.txt "
        "python card/build_bopomofo_fonts.py"
    ) from exc


VERSION = "v1.500"
ZIP_URL = (
    "https://github.com/ButTaiwan/bpmfvs/releases/download/"
    f"{VERSION}/BpmfGenSenRounded.zip"
)
ZIP_SHA256 = "01548ac7216758bd2a2a46143ed41b26004198df2b07ab24b337c88505f8e558"
FONT_FILES = {
    "bold": "BpmfGenSenRounded-B.ttf",
    "medium": "BpmfGenSenRounded-M.ttf",
}
LICENSE_FILES = ("LICENSE-Gen.txt", "LICENSE-2.0.txt", "NOTICE.txt")
FIXED_BOLD_TEXT = "力量速度攻擊防禦聰明特殊能力"
ALLOWED_UNSUPPORTED = {
    "㺢": "㺢㹢狓",
    "㹢": "㺢㹢狓",
    "狓": "㺢㹢狓",
    "獴": "狐獴",
}
VARIATION_SELECTORS = tuple(range(0xE01E0, 0xE01E6))
PUNCTUATION = set("，。？！、：；（）「」『』—…")

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
ANIMALS_PATH = REPO_ROOT / "game" / "digital" / "data" / "animals.json"
OVERRIDES_PATH = SCRIPT_DIR / "data" / "bopomofo-overrides.json"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "fonts" / "bopomofo"
DEFAULT_CACHE_DIR = REPO_ROOT / "tmp" / "fonts" / "bpmfvs-v1.500-build"
TEAM_MISSION_CARD_PATHS = (
    SCRIPT_DIR / "team-mission-status-cards-quarter-label.html",
    SCRIPT_DIR / "storm-forest-rescue-reveal-cards-half-label.html",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_card_font_character(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or char in PUNCTUATION
    )


def card_codepoints(text: str) -> set[int]:
    return {ord(char) for char in text if is_card_font_character(char)}


def load_data() -> tuple[list[dict], dict]:
    animals = json.loads(ANIMALS_PATH.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    if len(animals) != 132:
        raise SystemExit(f"預期 132 隻動物，實際為 {len(animals)}")
    required = ("id", "name", "skillName", "skillDesc")
    for index, animal in enumerate(animals):
        missing = [key for key in required if not animal.get(key)]
        if missing:
            raise SystemExit(f"animals[{index}] 缺少欄位：{', '.join(missing)}")

    animals_by_id = {animal["id"]: animal for animal in animals}
    for section_name in ("fields", "manualRuby"):
        for key, entries in overrides.get(section_name, {}).items():
            animal_id, separator, field_name = key.partition(".")
            if not separator or animal_id not in animals_by_id:
                raise SystemExit(f"無效的讀音 override key：{key}")
            value = animals_by_id[animal_id].get(field_name)
            if value is None:
                raise SystemExit(f"讀音 override 欄位不存在：{key}")
            seen_indexes: set[int] = set()
            for entry in entries:
                entry_index = entry["index"]
                if entry_index in seen_indexes:
                    raise SystemExit(f"讀音 override 索引重複：{key}[{entry_index}]")
                seen_indexes.add(entry_index)
                actual = value[entry_index] if 0 <= entry_index < len(value) else None
                if actual != entry["char"]:
                    raise SystemExit(
                        f"讀音 override 索引不一致：{key}[{entry_index}] "
                        f"預期 {entry['char']}，實際 {actual or '超出範圍'}"
                    )
                if section_name == "fields" and entry.get("selector") not in range(6):
                    raise SystemExit(f"讀音 override selector 無效：{key}[{entry_index}]")
    return animals, overrides


def apply_ivs(text: str, entries: list[dict]) -> str:
    by_index = {entry["index"]: entry for entry in entries}
    output: list[str] = []
    for index, char in enumerate(text):
        output.append(char)
        entry = by_index.get(index)
        if entry:
            if entry["char"] != char:
                raise SystemExit(
                    f"讀音 override 索引不一致：預期 {entry['char']}，實際 {char}"
                )
            output.append(chr(0xE01E0 + entry["selector"]))
    return "".join(output)


def build_corpora(animals: list[dict], overrides: dict) -> dict[str, str]:
    fields = overrides.get("fields", {})
    missing_cards = [str(path) for path in TEAM_MISSION_CARD_PATHS if not path.exists()]
    if missing_cards:
        raise SystemExit(f"找不到團隊任務卡面：{', '.join(missing_cards)}")
    team_mission_text = "\n".join(
        path.read_text(encoding="utf-8") for path in TEAM_MISSION_CARD_PATHS
    )
    team_mission_characters = "".join(
        char for char in team_mission_text if is_card_font_character(char)
    )

    bold_parts = [FIXED_BOLD_TEXT, team_mission_characters]
    medium_parts: list[str] = [team_mission_characters]
    all_parts: list[str] = []

    for animal in animals:
        for field_name in ("name", "skillName"):
            value = animal[field_name]
            key = f"{animal['id']}.{field_name}"
            value = apply_ivs(value, fields.get(key, []))
            bold_parts.append(value)
            all_parts.append(value)

        description_key = f"{animal['id']}.skillDesc"
        description = apply_ivs(
            animal["skillDesc"], fields.get(description_key, [])
        )
        medium_parts.append(description)
        all_parts.append(description)

    all_parts.extend([FIXED_BOLD_TEXT, team_mission_characters])
    return {
        "bold": "\n".join(bold_parts),
        "medium": "\n".join(medium_parts),
        "all": "\n".join(all_parts),
    }


def ensure_source_fonts(cache_dir: Path, offline: bool) -> dict[str, Path]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    zip_path = cache_dir / "BpmfGenSenRounded-v1.500.zip"
    if not zip_path.exists():
        if offline:
            raise SystemExit(f"離線模式找不到來源 ZIP：{zip_path}")
        print(f"下載官方字型：{ZIP_URL}")
        with urllib.request.urlopen(ZIP_URL) as response, zip_path.open("wb") as target:
            shutil.copyfileobj(response, target)

    actual_sha = sha256(zip_path)
    if actual_sha != ZIP_SHA256:
        raise SystemExit(
            "官方字型 ZIP SHA-256 不符：\n"
            f"expected {ZIP_SHA256}\nactual   {actual_sha}"
        )

    required = tuple(FONT_FILES.values()) + LICENSE_FILES
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        missing = sorted(set(required) - names)
        if missing:
            raise SystemExit(f"官方 ZIP 缺少檔案：{', '.join(missing)}")
        for filename in required:
            destination = cache_dir / filename
            if not destination.exists():
                with archive.open(filename) as source, destination.open("wb") as target:
                    shutil.copyfileobj(source, target)

    return {weight: cache_dir / filename for weight, filename in FONT_FILES.items()}


def font_cmap(path: Path) -> set[int]:
    font = TTFont(path)
    return set(font.getBestCmap())


def validate_source_coverage(source_fonts: dict[str, Path], corpora: dict[str, str]) -> dict:
    allowed = {ord(char) for char in ALLOWED_UNSUPPORTED}
    result = {}
    for weight in ("bold", "medium"):
        requested = card_codepoints(corpora[weight])
        available = font_cmap(source_fonts[weight])
        missing = requested - available
        unexpected = missing - allowed
        if unexpected:
            formatted = " ".join(f"{chr(cp)}(U+{cp:04X})" for cp in sorted(unexpected))
            raise SystemExit(f"{weight} 原始字型出現未列管缺字：{formatted}")
        result[weight] = {
            "requestedCodepoints": len(requested),
            "supportedCodepoints": len(requested - missing),
            "allowedUnsupported": [chr(cp) for cp in sorted(missing)],
        }
    return result


def subset_font(source: Path, destination: Path, text: str) -> None:
    source_font = TTFont(source)
    available = set(source_font.getBestCmap())
    requested = card_codepoints(text)
    supported = requested & available
    unicodes = supported | set(VARIATION_SELECTORS)

    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    options.glyph_names = True
    options.notdef_glyph = True
    options.notdef_outline = True
    options.recommended_glyphs = True
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    options.name_languages = ["*"]
    options.hinting = True

    font = subset.load_font(str(source), options, lazy=False)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    subset.save_font(font, str(destination), options)


def variation_map(font: TTFont) -> dict[int, set[int]]:
    mapping: dict[int, set[int]] = {}
    for table in font["cmap"].tables:
        if table.format != 14:
            continue
        for selector, pairs in (table.uvsDict or {}).items():
            mapping[selector] = {base for base, _glyph in pairs}
    return mapping


def validate_output(
    path: Path, text: str, overrides: dict, field_suffixes: tuple[str, ...]
) -> dict:
    font = TTFont(path)
    cmap = set(font.getBestCmap())
    requested = card_codepoints(text) - {ord(char) for char in ALLOWED_UNSUPPORTED}
    missing = requested - cmap
    if missing:
        formatted = " ".join(f"{chr(cp)}(U+{cp:04X})" for cp in sorted(missing))
        raise SystemExit(f"輸出字型 {path.name} 缺字：{formatted}")

    features: list[str] = []
    if "GSUB" in font and font["GSUB"].table.FeatureList:
        features = [
            record.FeatureTag
            for record in font["GSUB"].table.FeatureList.FeatureRecord
        ]

    variants = variation_map(font)
    required_sequences = []
    for key, entries in overrides.get("fields", {}).items():
        if not key.endswith(field_suffixes):
            continue
        for entry in entries:
            selector = 0xE01E0 + entry["selector"]
            base = ord(entry["char"])
            required_sequences.append(f"U+{base:04X} U+{selector:05X}")
            if base not in variants.get(selector, set()):
                raise SystemExit(
                    f"輸出字型 {path.name} 未保留 IVS："
                    f"U+{base:04X} U+{selector:05X}"
                )

    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "cmapCodepoints": len(cmap),
        "gsubFeatures": sorted(set(features)),
        "requiredVariationSequences": required_sequences,
    }


def write_corpora(output_dir: Path, corpora: dict[str, str]) -> None:
    for name, text in corpora.items():
        (output_dir / f"corpus-{name}.txt").write_text(text + "\n", encoding="utf-8")


def build(args: argparse.Namespace) -> None:
    animals, overrides = load_data()
    corpora = build_corpora(animals, overrides)
    source_fonts = ensure_source_fonts(args.cache_dir, args.offline)
    source_report = validate_source_coverage(source_fonts, corpora)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_corpora(args.output_dir, corpora)

    outputs = {
        "bold": args.output_dir / "rounded-bold.woff2",
        "medium": args.output_dir / "rounded-medium.woff2",
    }
    subset_font(source_fonts["bold"], outputs["bold"], corpora["bold"])
    subset_font(source_fonts["medium"], outputs["medium"], corpora["medium"])

    for filename in LICENSE_FILES:
        shutil.copy2(args.cache_dir / filename, args.output_dir / filename)

    report = {
        "source": {
            "version": VERSION,
            "url": ZIP_URL,
            "zipSha256": ZIP_SHA256,
        },
        "animals": len(animals),
        "fixedBoldText": FIXED_BOLD_TEXT,
        "knownUnsupported": ALLOWED_UNSUPPORTED,
        "pronunciationOverrides": {
            "variationSequences": sum(
                len(entries) for entries in overrides.get("fields", {}).values()
            ),
            "manualRuby": sum(
                len(entries) for entries in overrides.get("manualRuby", {}).values()
            ),
        },
        "sourceCoverage": source_report,
        "outputs": {
            "bold": validate_output(
                outputs["bold"], corpora["bold"], overrides, (".name", ".skillName")
            ),
            "medium": validate_output(
                outputs["medium"], corpora["medium"], overrides, (".skillDesc",)
            ),
        },
    }
    (args.output_dir / "build-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"完成：{outputs['bold'].relative_to(REPO_ROOT)}")
    print(f"完成：{outputs['medium'].relative_to(REPO_ROOT)}")
    print(f"列管缺字：{', '.join(ALLOWED_UNSUPPORTED)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"輸出目錄（預設：{DEFAULT_OUTPUT_DIR.relative_to(REPO_ROOT)}）",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=DEFAULT_CACHE_DIR,
        help="官方 ZIP 與 TTF 快取目錄",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="禁止下載；快取不存在時直接失敗",
    )
    return parser.parse_args()


if __name__ == "__main__":
    build(parse_args())
