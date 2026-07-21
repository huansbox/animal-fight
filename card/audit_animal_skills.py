#!/usr/bin/env python3
"""Audit animal skill copy for card and image-prompt production risks."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "game" / "digital" / "data" / "animals.json"

HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

FLAG_PATTERNS: dict[str, tuple[str, ...]] = {
    "multiple_actions": ("或", "還會", "又能", "又會", "同時", "然後"),
    "external_actor": (
        "敵人",
        "敵手",
        "對手",
        "攻擊者",
        "獵物",
        "掠食者",
        "同伴",
        "夥伴",
        "羊群",
        "魚群",
    ),
    "group_dependency": (
        "團隊",
        "同伴",
        "夥伴",
        "狼群",
        "一大群",
        "整群",
        "幾十萬",
        "幾百顆",
        "魚群",
        "羊群",
    ),
    "violent_visual": (
        "血",
        "顱",
        "頭骨",
        "致命",
        "必殺",
        "獵殺",
        "撲殺",
        "伏殺",
        "絞殺",
        "死鬥",
        "撕裂",
        "撕成碎片",
        "無法呼吸",
        "傷口",
        "吃光",
    ),
    "abstract_or_invisible": (
        "完全隱形",
        "看不見",
        "迷惑",
        "精神",
        "默契",
        "戰術",
        "智謀",
        "詭計",
        "什麼招數",
        "不怕",
        "找不到",
        "搞不清楚",
        "眼花撩亂",
    ),
    "absolute_or_hyperbolic": (
        "完全",
        "任何",
        "一切",
        "誰都",
        "什麼都",
        "絕不",
        "一擊必殺",
        "所向無敵",
        "一千倍",
        "比子彈還快",
        "幾秒",
        "全身麻痺",
    ),
}


@dataclass(frozen=True)
class AuditRow:
    id: str
    name: str
    skill_name: str
    skill_desc: str
    skill_name_chars: int
    skill_desc_chars: int
    comma_count: int
    bonus_total: int
    format_issues: tuple[str, ...]
    prompt_risk_flags: tuple[str, ...]
    matched_terms: dict[str, tuple[str, ...]]


def han_count(text: str) -> int:
    return len(HAN_RE.findall(text))


def matched_terms(text: str, terms: Iterable[str]) -> tuple[str, ...]:
    return tuple(term for term in terms if term in text)


def audit_animal(animal: dict) -> AuditRow:
    skill_name = animal.get("skillName", "")
    skill_desc = animal.get("skillDesc", "")
    name_chars = han_count(skill_name)
    desc_chars = han_count(skill_desc)
    comma_count = skill_desc.count("，")
    bonus_total = sum(item.get("val", 0) for item in animal.get("skillBonus", []))

    issues: list[str] = []
    if name_chars != 4:
        issues.append("skill_name_not_four_chars")
    if not 15 <= desc_chars <= 25:
        issues.append("skill_desc_length")
    if comma_count > 2:
        issues.append("too_many_commas")
    if bonus_total != 4:
        issues.append("skill_bonus_not_four")

    matches: dict[str, tuple[str, ...]] = {}
    for flag, terms in FLAG_PATTERNS.items():
        found = matched_terms(skill_desc, terms)
        if found:
            matches[flag] = found

    return AuditRow(
        id=animal.get("id", ""),
        name=animal.get("name", ""),
        skill_name=skill_name,
        skill_desc=skill_desc,
        skill_name_chars=name_chars,
        skill_desc_chars=desc_chars,
        comma_count=comma_count,
        bonus_total=bonus_total,
        format_issues=tuple(issues),
        prompt_risk_flags=tuple(matches),
        matched_terms=matches,
    )


def audit_all(animals: list[dict]) -> list[AuditRow]:
    rows = [audit_animal(animal) for animal in animals]

    skill_name_counts = Counter(row.skill_name for row in rows)
    duplicate_names = {name for name, count in skill_name_counts.items() if count > 1}
    if not duplicate_names:
        return rows

    adjusted: list[AuditRow] = []
    for row in rows:
        if row.skill_name not in duplicate_names:
            adjusted.append(row)
            continue
        data = asdict(row)
        data["format_issues"] = tuple((*row.format_issues, "duplicate_skill_name"))
        adjusted.append(AuditRow(**data))
    return adjusted


def summary(rows: list[AuditRow]) -> dict:
    format_counts = Counter(issue for row in rows for issue in row.format_issues)
    risk_counts = Counter(flag for row in rows for flag in row.prompt_risk_flags)
    return {
        "animals": len(rows),
        "format_issue_counts": dict(sorted(format_counts.items())),
        "prompt_risk_counts": dict(sorted(risk_counts.items())),
        "rows_with_format_issues": sum(bool(row.format_issues) for row in rows),
        "rows_with_prompt_risks": sum(bool(row.prompt_risk_flags) for row in rows),
    }


def render_text(rows: list[AuditRow]) -> str:
    report = summary(rows)
    lines = [
        f"Animals: {report['animals']}",
        f"Rows with format issues: {report['rows_with_format_issues']}",
        f"Rows with prompt-risk candidates: {report['rows_with_prompt_risks']}",
        "",
        "Format issues:",
    ]
    for issue, count in report["format_issue_counts"].items():
        lines.append(f"- {issue}: {count}")

    format_rows = [row for row in rows if row.format_issues]
    if format_rows:
        lines.extend(("", "[format_issues]"))
        for row in format_rows:
            issues = ", ".join(row.format_issues)
            lines.append(
                f"- {row.name}｜{row.skill_name}｜name={row.skill_name_chars}｜"
                f"desc={row.skill_desc_chars}｜{issues}"
            )

    lines.extend(("", "Prompt-risk candidates:"))
    for flag, count in report["prompt_risk_counts"].items():
        lines.append(f"- {flag}: {count}")

    grouped: dict[str, list[AuditRow]] = defaultdict(list)
    for row in rows:
        for flag in row.prompt_risk_flags:
            grouped[flag].append(row)

    for flag in FLAG_PATTERNS:
        candidates = grouped.get(flag, [])
        if not candidates:
            continue
        lines.extend(("", f"[{flag}]"))
        for row in candidates:
            terms = ", ".join(row.matched_terms[flag])
            lines.append(
                f"- {row.name}｜{row.skill_name}｜{row.skill_desc}｜matched: {terms}"
            )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    animals = json.loads(args.input.read_text(encoding="utf-8"))
    rows = audit_all(animals)
    if args.format == "json":
        payload = {"summary": summary(rows), "rows": [asdict(row) for row in rows]}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(rows), end="")


if __name__ == "__main__":
    main()
