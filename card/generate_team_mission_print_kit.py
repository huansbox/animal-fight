#!/usr/bin/env python3
"""Generate the black-and-white team mission v0.6 print kit.

Outputs:
- A4 landscape player control board on plain paper.
- Four storm scenario reveal cards on one A4 four-up label sheet.
- Two-page A4 landscape duplex DM guide on plain paper.

All dimensions are physical sizes. Print the generated PDFs at 100% / Actual size.
"""

from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"

CONTROL_BOARD_PDF = OUTPUT_DIR / "team-mission-v06-control-board-a4.pdf"
REVEAL_CARDS_PDF = OUTPUT_DIR / "storm-forest-rescue-reveal-cards-four-up-a4.pdf"
DM_GUIDE_PDF = OUTPUT_DIR / "storm-forest-rescue-dm-guide-a4-duplex.pdf"

BLACK = colors.black
WHITE = colors.white
LIGHT = colors.Color(0.94, 0.94, 0.94)
VERY_LIGHT = colors.Color(0.975, 0.975, 0.975)


def find_font(candidates: list[str]) -> str:
    for candidate in candidates:
        expanded = os.path.expanduser(candidate)
        if os.path.exists(expanded):
            return expanded
    raise RuntimeError(
        "找不到可用的正體中文字型。請安裝 Noto Sans CJK TC，"
        "或在 generate_team_mission_print_kit.py 補上本機字型路徑。"
    )


def register_fonts() -> None:
    regular = find_font(
        [
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "C:/Windows/Fonts/msjh.ttc",
            "C:/Windows/Fonts/mingliu.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJKtc-Regular.otf",
        ]
    )
    bold = find_font(
        [
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "C:/Windows/Fonts/msjhbd.ttc",
            "C:/Windows/Fonts/msjh.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJKtc-Bold.otf",
        ]
    )
    pdfmetrics.registerFont(TTFont("CJK", regular, subfontIndex=0))
    pdfmetrics.registerFont(TTFont("CJKBold", bold, subfontIndex=0))
    pdfmetrics.registerFontFamily(
        "CJK",
        normal="CJK",
        bold="CJKBold",
        italic="CJK",
        boldItalic="CJKBold",
    )


register_fonts()


def style(
    name: str,
    size: float,
    leading: float | None = None,
    *,
    bold: bool = False,
    align: int = TA_LEFT,
    text_color=BLACK,
    space_after: float = 0,
) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName="CJKBold" if bold else "CJK",
        fontSize=size,
        leading=leading or size * 1.32,
        alignment=align,
        textColor=text_color,
        spaceAfter=space_after,
        allowWidows=0,
        allowOrphans=0,
    )


S = {
    "card_kicker": style("card_kicker", 9.5, 12, bold=True, align=TA_CENTER),
    "card_title": style("card_title", 17, 20, bold=True, align=TA_CENTER),
    "card_story": style("card_story", 9.3, 12.2, align=TA_LEFT),
    "card_job": style("card_job", 10.5, 13.2, bold=True, align=TA_CENTER),
    "card_range": style("card_range", 14, 17, bold=True, align=TA_CENTER),
    "card_attr": style("card_attr", 12.5, 16, bold=True, align=TA_CENTER),
    "card_note": style("card_note", 8.2, 10.5, align=TA_CENTER),
    "board_title": style("board_title", 20, 23, bold=True, align=TA_CENTER),
    "board_h": style("board_h", 12.5, 15, bold=True, align=TA_CENTER),
    "board_body": style("board_body", 9.2, 12),
    "board_small": style("board_small", 8.1, 10.3),
    "guide_title": style("guide_title", 17, 20, bold=True),
    "guide_subtitle": style("guide_subtitle", 9.2, 12),
    "guide_h": style("guide_h", 10.6, 13.2, bold=True),
    "guide_body": style("guide_body", 8.8, 11.4),
    "guide_small": style("guide_small", 8.8, 11.5),
    "guide_center": style("guide_center", 8.8, 11.4, align=TA_CENTER),
}


def draw_paragraph(
    c: canvas.Canvas,
    text: str,
    x: float,
    top: float,
    width: float,
    paragraph_style: ParagraphStyle,
    *,
    max_height: float = 1000 * mm,
) -> float:
    paragraph = Paragraph(text, paragraph_style)
    _, height = paragraph.wrap(width, max_height)
    paragraph.drawOn(c, x, top - height)
    return height


def draw_box(
    c: canvas.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    line_width: float = 1,
    dash: tuple[int, int] | None = None,
    fill=None,
    radius: float = 2.5 * mm,
) -> None:
    c.saveState()
    c.setStrokeColor(BLACK)
    c.setLineWidth(line_width)
    if dash:
        c.setDash(*dash)
    if fill is not None:
        c.setFillColor(fill)
        c.roundRect(x, y, width, height, radius, stroke=1, fill=1)
    else:
        c.roundRect(x, y, width, height, radius, stroke=1, fill=0)
    c.restoreState()


def draw_section_label(
    c: canvas.Canvas,
    text: str,
    x: float,
    top: float,
    width: float,
    *,
    height: float = 8 * mm,
) -> None:
    c.saveState()
    c.setFillColor(BLACK)
    c.roundRect(x, top - height, width, height, 2 * mm, stroke=0, fill=1)
    c.restoreState()
    label_style = style("section_white", 10.5, 13, bold=True, align=TA_CENTER, text_color=WHITE)
    draw_paragraph(c, text, x + 2 * mm, top - 1.4 * mm, width - 4 * mm, label_style)


def draw_checkbox(c: canvas.Canvas, x: float, y: float, size: float, label: str) -> None:
    c.setLineWidth(1.2)
    c.rect(x, y, size, size, stroke=1, fill=0)
    draw_paragraph(c, label, x + size + 2 * mm, y + size - 0.5 * mm, 36 * mm, S["board_body"])


def draw_shield(c: canvas.Canvas, cx: float, cy: float, size: float, number: int) -> None:
    points = [
        (cx - size * 0.55, cy + size * 0.5),
        (cx + size * 0.55, cy + size * 0.5),
        (cx + size * 0.48, cy - size * 0.1),
        (cx, cy - size * 0.62),
        (cx - size * 0.48, cy - size * 0.1),
    ]
    path = c.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    path.close()
    c.setLineWidth(2)
    c.drawPath(path, stroke=1, fill=0)
    c.setFont("CJKBold", size * 0.45)
    c.drawCentredString(cx, cy - size * 0.15, str(number))


def draw_control_board() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(str(CONTROL_BOARD_PDF), pagesize=(page_width, page_height))
    c.setTitle("團隊任務 v0.6 控制板")

    margin = 8 * mm
    gap = 4 * mm
    title_top = page_height - 7 * mm
    draw_paragraph(c, "團隊任務 v0.6 控制板", margin, title_top, page_width - 2 * margin, S["board_title"])
    draw_paragraph(
        c,
        "黑白雷射版｜抽 8 隻動物｜前三關逐關揭露｜故事方法不影響骰子",
        margin,
        title_top - 10 * mm,
        page_width - 2 * margin,
        style("board_tagline", 8.8, 11, align=TA_CENTER),
    )

    status_y = page_height - 63 * mm
    status_h = 35 * mm
    shield_w = 118 * mm
    reserve_w = 66 * mm
    progress_w = page_width - 2 * margin - shield_w - reserve_w - 2 * gap

    draw_box(c, margin, status_y, shield_w, status_h)
    draw_section_label(c, "洪水巨獸護盾", margin + 3 * mm, status_y + status_h - 3 * mm, 44 * mm, height=7 * mm)
    for index, x_offset in enumerate((63, 84, 105), start=1):
        draw_shield(c, margin + x_offset * mm, status_y + 16 * mm, 14 * mm, index)
    draw_paragraph(
        c,
        "一般任務成功：劃掉 1 面。<br/>到 Boss 才數還剩幾面。",
        margin + 4 * mm,
        status_y + 22 * mm,
        52 * mm,
        S["board_small"],
    )

    reserve_x = margin + shield_w + gap
    draw_box(c, reserve_x, status_y, reserve_w, status_h)
    draw_section_label(c, "全隊後援", reserve_x + 3 * mm, status_y + status_h - 3 * mm, 34 * mm, height=7 * mm)
    draw_checkbox(c, reserve_x + 8 * mm, status_y + 12 * mm, 8 * mm, "第 1 次")
    draw_checkbox(c, reserve_x + 36 * mm, status_y + 12 * mm, 8 * mm, "第 2 次")
    draw_paragraph(
        c,
        "每關最多 1 隻；整局最多 2 次。",
        reserve_x + 5 * mm,
        status_y + 9 * mm,
        reserve_w - 10 * mm,
        style("reserve_note", 7.7, 9.4, align=TA_CENTER),
    )

    progress_x = reserve_x + reserve_w + gap
    draw_box(c, progress_x, status_y, progress_w, status_h)
    draw_section_label(c, "關卡進度", progress_x + 3 * mm, status_y + status_h - 3 * mm, 33 * mm, height=7 * mm)
    progress_labels = ("1", "2A+B", "3", "Boss")
    start_x = progress_x + 7 * mm
    for index, label in enumerate(progress_labels):
        px = start_x + index * 20 * mm
        c.circle(px + 4 * mm, status_y + 15 * mm, 4 * mm, stroke=1, fill=0)
        c.setFont("CJKBold", 8.5)
        c.drawCentredString(px + 4 * mm, status_y + 12.5 * mm, label)

    lower_top = status_y - gap
    lower_y = 10 * mm
    lower_h = lower_top - lower_y
    zones_w = 172 * mm
    rules_x = margin + zones_w + gap
    rules_w = page_width - margin - rules_x

    draw_box(c, margin, lower_y, zones_w, lower_h)
    draw_section_label(c, "三個卡片區域", margin + 3 * mm, lower_top - 3 * mm, 38 * mm, height=7 * mm)
    draw_paragraph(
        c,
        "把動物卡分成三堆，放在控制板旁；卡片全程正面朝上。",
        margin + 45 * mm,
        lower_top - 4 * mm,
        zones_w - 49 * mm,
        style("zones_note", 8.2, 10.2, align=TA_CENTER),
    )

    zone_y = lower_y + 23 * mm
    zone_h = lower_h - 39 * mm
    zone_gap = 3 * mm
    zone_w = (zones_w - 8 * mm - 2 * zone_gap) / 3
    zone_specs = [
        (
            "待命區",
            "尚未出動",
            "可以第一次擔任主要動物，或在任務失敗後擔任後援。",
            None,
        ),
        (
            "再挑戰區",
            "第一次出動為 0 成功",
            "之後只能再出場 1 次，而且只能擔任後援。",
            (3, 2),
        ),
        (
            "休息區",
            "完成工作或用完機會",
            "本局不能再出動；卡片留在桌上，結局仍會說到牠。",
            (1, 2),
        ),
    ]
    for index, (title, subtitle, body, dash) in enumerate(zone_specs):
        zx = margin + 4 * mm + index * (zone_w + zone_gap)
        draw_box(c, zx, zone_y, zone_w, zone_h, line_width=1.3, dash=dash, fill=VERY_LIGHT)
        draw_paragraph(c, title, zx + 3 * mm, zone_y + zone_h - 4 * mm, zone_w - 6 * mm, S["board_h"])
        draw_paragraph(
            c,
            subtitle,
            zx + 3 * mm,
            zone_y + zone_h - 14 * mm,
            zone_w - 6 * mm,
            style(f"zone_sub_{index}", 8.3, 10.4, bold=True, align=TA_CENTER),
        )
        draw_paragraph(
            c,
            body,
            zx + 4 * mm,
            zone_y + zone_h - 27 * mm,
            zone_w - 8 * mm,
            style(f"zone_body_{index}", 8.1, 10.5, align=TA_CENTER),
        )

    draw_paragraph(
        c,
        "個別工作：至少 1 成功 → 休息區｜0 成功 → 再挑戰區",
        margin + 6 * mm,
        lower_y + 17 * mm,
        zones_w - 12 * mm,
        style("zone_footer", 9.1, 11.5, bold=True, align=TA_CENTER),
    )
    draw_paragraph(
        c,
        "別的動物後援成功，也不會取消原動物的再挑戰資格。",
        margin + 6 * mm,
        lower_y + 9 * mm,
        zones_w - 12 * mm,
        style("zone_footer2", 8, 10, align=TA_CENTER),
    )

    box_gap = 3 * mm
    dice_h = 39 * mm
    boss_h = 43 * mm
    helper_h = lower_h - dice_h - boss_h - 2 * box_gap

    dice_y = lower_top - dice_h
    draw_box(c, rules_x, dice_y, rules_w, dice_h)
    draw_section_label(c, "骰池", rules_x + 3 * mm, lower_top - 3 * mm, 24 * mm, height=7 * mm)
    draw_paragraph(
        c,
        "1. 屬性在指定區間：<b>2 顆</b>；不在：<b>1 顆</b><br/>"
        "2. 所選屬性有 skillBonus：<b>再加 1 顆</b><br/>"
        "3. 每隻最多 <b>3 顆</b>；骰出 <b>4、5、6 = 1 成功</b>",
        rules_x + 5 * mm,
        lower_top - 13 * mm,
        rules_w - 10 * mm,
        S["board_body"],
    )

    boss_y = dice_y - box_gap - boss_h
    draw_box(c, rules_x, boss_y, rules_w, boss_h)
    draw_section_label(c, "Boss 門檻", rules_x + 3 * mm, dice_y - box_gap - 3 * mm, 32 * mm, height=7 * mm)
    boss_rows = [
        ("0 盾", "1＋1"),
        ("1 盾", "合計 3，兩邊 > 0"),
        ("2 盾", "合計 4，兩邊 > 0"),
        ("3 盾", "2＋2"),
    ]
    row_top = dice_y - box_gap - 13 * mm
    for index, (shield, target) in enumerate(boss_rows):
        ry = row_top - index * 7 * mm
        c.setLineWidth(0.55)
        if index:
            c.line(rules_x + 5 * mm, ry + 2.2 * mm, rules_x + rules_w - 5 * mm, ry + 2.2 * mm)
        draw_paragraph(c, f"<b>{shield}</b>", rules_x + 6 * mm, ry, 22 * mm, S["board_small"])
        draw_paragraph(c, target, rules_x + 30 * mm, ry, rules_w - 36 * mm, S["board_small"])

    helper_y = lower_y
    draw_box(c, rules_x, helper_y, rules_w, helper_h)
    draw_section_label(c, "支援與後援", rules_x + 3 * mm, boss_y - box_gap - 3 * mm, 38 * mm, height=7 * mm)
    draw_paragraph(
        c,
        "<b>單向支援：</b>雙動物尚未通關時，成功較多的一邊，每個超過第 1 個的成功，可讓另一邊重擲 1 顆失敗骰；只做一個方向。<br/><br/>"
        "<b>後援 A：</b>整體仍失敗且只補一個位置就可能通關，才能呼叫。後援與原位置的成功數<b>取較高、不相加</b>。",
        rules_x + 5 * mm,
        boss_y - box_gap - 13 * mm,
        rules_w - 10 * mm,
        S["board_small"],
    )

    c.setFont("CJK", 6.8)
    c.drawRightString(page_width - margin, 4.5 * mm, "列印：A4 橫式｜普通紙｜黑白｜100% 實際大小")
    c.showPage()
    c.save()


def reveal_card_frame(c: canvas.Canvas, x: float, y: float, width: float, height: float, number: str) -> tuple[float, float, float, float]:
    inset = 5.5 * mm
    draw_box(c, x + inset, y + inset, width - 2 * inset, height - 2 * inset, line_width=1.4, radius=3.5 * mm)
    c.setFillColor(BLACK)
    c.circle(x + width - 13 * mm, y + height - 13 * mm, 6 * mm, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("CJKBold", 10)
    c.drawCentredString(x + width - 13 * mm, y + height - 16 * mm, number)
    c.setFillColor(BLACK)
    return x + inset + 5 * mm, y + inset + 5 * mm, width - 2 * inset - 10 * mm, height - 2 * inset - 10 * mm


def draw_attr_pills(c: canvas.Canvas, labels: list[str], x: float, y: float, width: float) -> None:
    gap = 3 * mm
    pill_w = (width - gap * (len(labels) - 1)) / len(labels)
    for index, label in enumerate(labels):
        px = x + index * (pill_w + gap)
        draw_box(c, px, y, pill_w, 12 * mm, line_width=1.1, radius=6 * mm)
        draw_paragraph(c, label, px + 2 * mm, y + 8.8 * mm, pill_w - 4 * mm, S["card_attr"])


def draw_reveal_cards() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    page_width, page_height = A4
    c = canvas.Canvas(str(REVEAL_CARDS_PDF), pagesize=A4)
    c.setTitle("暴雨森林救援隊：四張逐關揭露卡")

    cell_w = page_width / 2
    cell_h = page_height / 2
    cells = [
        (0, cell_h),
        (cell_w, cell_h),
        (0, 0),
        (cell_w, 0),
    ]

    # Card 0: mission briefing and Boss preview.
    x, y = cells[0]
    ix, iy, iw, ih = reveal_card_frame(c, x, y, cell_w, cell_h, "0")
    top = iy + ih
    draw_paragraph(c, "任務簡報＋Boss 提示", ix, top, iw, S["card_kicker"])
    top -= 10 * mm
    draw_paragraph(c, "暴雨森林救援隊", ix, top, iw, S["card_title"])
    top -= 13 * mm
    draw_paragraph(
        c,
        "洪水巨獸正朝動物村前進。沿途完成三次救援，打破牠的三面水盾。",
        ix,
        top,
        iw,
        S["card_story"],
    )
    top -= 25 * mm
    draw_box(c, ix, top - 28 * mm, iw, 28 * mm, fill=VERY_LIGHT)
    draw_paragraph(c, "Boss A｜突破水牆", ix + 3 * mm, top - 3 * mm, iw - 6 * mm, S["card_job"])
    draw_paragraph(c, "大格 7-9｜力量 或 攻擊", ix + 3 * mm, top - 13 * mm, iw - 6 * mm, S["card_attr"])
    top -= 33 * mm
    draw_box(c, ix, top - 28 * mm, iw, 28 * mm, dash=(4, 2))
    draw_paragraph(c, "Boss B｜穩住避難區", ix + 3 * mm, top - 3 * mm, iw - 6 * mm, S["card_job"])
    draw_paragraph(c, "剛好格 4-6｜防禦 或 智慧", ix + 3 * mm, top - 13 * mm, iw - 6 * mm, S["card_attr"])
    draw_paragraph(
        c,
        "現在只要記住最後可能需要的本領，不必先決定動物。Boss 到達時再由 DM 公布成功門檻。",
        ix,
        iy + 17 * mm,
        iw,
        S["card_note"],
    )

    # Card 1: first task.
    x, y = cells[1]
    ix, iy, iw, ih = reveal_card_frame(c, x, y, cell_w, cell_h, "1")
    top = iy + ih
    draw_paragraph(c, "第一關｜1 隻動物", ix, top, iw, S["card_kicker"])
    top -= 11 * mm
    draw_paragraph(c, "找出安全道路", ix, top, iw, S["card_title"])
    top -= 15 * mm
    draw_paragraph(
        c,
        "積水和倒木切斷道路，水還在上升。找出能讓整隊安全通過的連續路線。",
        ix,
        top,
        iw,
        S["card_story"],
    )
    top -= 31 * mm
    draw_paragraph(c, "剛好格 4-6", ix, top, iw, S["card_range"])
    draw_attr_pills(c, ["速度", "智慧"], ix, top - 20 * mm, iw)
    draw_paragraph(
        c,
        "這隻動物要怎麼用你選的能力，帶大家穿過積水和倒木？",
        ix,
        iy + 32 * mm,
        iw,
        S["card_note"],
    )

    # Card 2: double task.
    x, y = cells[2]
    ix, iy, iw, ih = reveal_card_frame(c, x, y, cell_w, cell_h, "2")
    top = iy + ih
    draw_paragraph(c, "第二關｜2 隻動物", ix, top, iw, S["card_kicker"])
    top -= 10 * mm
    draw_paragraph(c, "搖晃藤橋上的幼獸", ix, top, iw, S["card_title"])
    top -= 14 * mm
    draw_paragraph(
        c,
        "一隻固定藤橋，另一隻靠近並解開受驚的小鹿；兩邊都完成才通關。",
        ix,
        top,
        iw,
        S["card_story"],
    )
    top -= 26 * mm
    draw_box(c, ix, top - 31 * mm, iw, 31 * mm, fill=VERY_LIGHT)
    draw_paragraph(c, "2A｜固定藤橋", ix + 3 * mm, top - 3 * mm, iw - 6 * mm, S["card_job"])
    draw_paragraph(c, "大格 7-9", ix + 3 * mm, top - 13 * mm, iw - 6 * mm, S["card_range"])
    draw_paragraph(c, "力量 或 防禦", ix + 3 * mm, top - 24 * mm, iw - 6 * mm, S["card_attr"])
    top -= 36 * mm
    draw_box(c, ix, top - 31 * mm, iw, 31 * mm, dash=(4, 2))
    draw_paragraph(c, "2B｜解開幼獸", ix + 3 * mm, top - 3 * mm, iw - 6 * mm, S["card_job"])
    draw_paragraph(c, "小格 1-3", ix + 3 * mm, top - 13 * mm, iw - 6 * mm, S["card_range"])
    draw_paragraph(c, "速度 或 攻擊", ix + 3 * mm, top - 24 * mm, iw - 6 * mm, S["card_attr"])
    draw_paragraph(c, "各自說明動物怎麼完成自己的工作。", ix, iy + 10 * mm, iw, S["card_note"])

    # Card 3: third task.
    x, y = cells[3]
    ix, iy, iw, ih = reveal_card_frame(c, x, y, cell_w, cell_h, "3")
    top = iy + ih
    draw_paragraph(c, "第三關｜1 隻動物", ix, top, iw, S["card_kicker"])
    top -= 11 * mm
    draw_paragraph(c, "搬運易碎藥品", ix, top, iw, S["card_title"])
    top -= 15 * mm
    draw_paragraph(
        c,
        "玻璃藥瓶不能摔，也不能抱得太緊。把藥箱安全送過泥濘樹根。",
        ix,
        top,
        iw,
        S["card_story"],
    )
    top -= 31 * mm
    draw_paragraph(c, "小格 1-3", ix, top, iw, S["card_range"])
    draw_attr_pills(c, ["力量", "速度"], ix, top - 20 * mm, iw)
    draw_paragraph(
        c,
        "這隻動物要怎麼用你選的能力，輕輕把玻璃藥瓶送過樹根？",
        ix,
        iy + 32 * mm,
        iw,
        S["card_note"],
    )

    c.setFont("CJK", 5.8)
    c.drawCentredString(page_width / 2, 2.5 * mm, "A4 四分標籤紙｜單面｜黑白｜100% 實際大小｜每張標籤 105×148.5mm")
    c.showPage()
    c.save()


def draw_flow_box(
    c: canvas.Canvas,
    title: str,
    blocks: list[tuple[str, str]],
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    body_style: ParagraphStyle | None = None,
) -> float:
    draw_box(c, x, y, width, height, line_width=0.9)
    draw_section_label(c, title, x + 2.5 * mm, y + height - 2.5 * mm, width - 5 * mm, height=7 * mm)
    cursor = y + height - 12 * mm
    body_style = body_style or S["guide_body"]
    for kind, text in blocks:
        block_style = S["guide_h"] if kind == "h" else body_style
        used = draw_paragraph(c, text, x + 4 * mm, cursor, width - 8 * mm, block_style)
        cursor -= used + (1.3 * mm if kind == "h" else 1.7 * mm)
    if cursor < y + 3 * mm:
        raise RuntimeError(f"DM 指南區塊內容溢出：{title}")
    return cursor - y


def guide_header(c: canvas.Canvas, page_number: int, label: str) -> None:
    page_width, page_height = landscape(A4)
    draw_paragraph(c, "暴雨森林救援隊｜DM 雙面指南", 10 * mm, page_height - 7 * mm, 180 * mm, S["guide_title"])
    draw_paragraph(
        c,
        label,
        194 * mm,
        page_height - 8 * mm,
        93 * mm,
        style(f"guide_page_{page_number}", 9, 11, bold=True, align=TA_CENTER),
    )
    c.setLineWidth(1)
    c.line(10 * mm, page_height - 18 * mm, page_width - 10 * mm, page_height - 18 * mm)
    c.setFont("CJK", 6.5)
    c.drawRightString(page_width - 10 * mm, 5 * mm, f"v0.6｜第 {page_number}/2 頁")


def draw_dm_guide_page_one(c: canvas.Canvas) -> None:
    page_width, page_height = landscape(A4)
    guide_header(c, 1, "正面｜開場與前三關")

    top_y = page_height - 21 * mm
    intro_h = 34 * mm
    draw_box(c, 10 * mm, top_y - intro_h, page_width - 20 * mm, intro_h, line_width=0.9, fill=VERY_LIGHT)
    draw_paragraph(
        c,
        "<b>準備：</b>抽 8 隻動物面朝上；放 3 面水盾、2 次後援；先翻 0 號任務簡報卡。前三關卡片蓋住，依序翻開。<br/>"
        "<b>開場念：</b>昨晚暴雨讓河水、泥沙和漂流木聚成洪水巨獸。牠正朝動物村前進，你們要帶領救援隊沿途幫助受困動物，最後阻止牠。牠目前有三面水盾。<br/>"
        "<b>區間口訣：</b>小格是輕輕做，剛好格是控制得剛剛好，大格是把本領開大。故事方法不加骰，也沒有標準答案。",
        14 * mm,
        top_y - 4 * mm,
        page_width - 28 * mm,
        S["guide_body"],
    )

    columns_y = 11 * mm
    columns_top = top_y - intro_h - 4 * mm
    columns_h = columns_top - columns_y
    gap = 3.5 * mm
    col_w = (page_width - 20 * mm - 2 * gap) / 3

    task1 = [
        ("h", "翻卡後念"),
        ("b", "積水和倒木切斷道路，水還在上升。找出能讓整隊安全通過的連續路線。"),
        ("h", "位置 1｜剛好格 4-6｜速度／智慧"),
        ("b", "問：牠要怎麼用選好的能力，帶大家穿過積水和倒木？"),
        ("b", "速度卡住：一段一段試路；快速查看、到倒木前停穩。<br/>智慧卡住：看水流找淺處；比較倒木與高地並留下記號。"),
        ("h", "結果"),
        ("b", "成功：找到連續安全路線並留下標記；劃掉 1 面盾。<br/>0 成功：找到高地與危險區，但記號被樹枝蓋住；可問是否後援。<br/>後援成功：接著補完路線；劃盾。後援也失敗：繞遠路，記錄「道路繞遠」。"),
        ("h", "轉場"),
        ("b", "不論走近路或遠路，前方藤橋傳來幼獸叫聲。翻第 2 張卡。"),
    ]
    task2 = [
        ("h", "翻卡後念"),
        ("b", "洪水撞擊藤橋，小鹿被細藤纏住。兩隻動物分工：一隻固定橋，一隻靠近小鹿。"),
        ("h", "2A｜大格 7-9｜力量／防禦"),
        ("b", "問：怎麼讓藤橋不要再搖？<br/>力量：拉住粗藤；推回橋樁。<br/>防禦：擋開水和木頭；護住橋頭。"),
        ("h", "2B｜小格 1-3｜速度／攻擊"),
        ("b", "問：怎麼完成工作又不嚇到小鹿？<br/>速度：停一下走一步；橋穩時才移動。<br/>攻擊：只咬細藤鬆處；輕敲繩結。"),
        ("h", "結果"),
        ("b", "兩邊成功：橋穩、小鹿脫困；劃盾。<br/>只有一邊成功：成功者進休息，0 成功者可被後援，之後進再挑戰。<br/>兩邊 0：需要同時改善，不能只靠 1 隻後援；記錄「藤橋未穩／小鹿仍等待」。"),
        ("b", "單向支援：成功較多者的超額成功，讓另一邊重擲失敗骰；只做一個方向。"),
        ("h", "轉場"),
        ("b", "避難區敲鐘，受傷動物等藥。翻第 3 張卡。"),
    ]
    task3 = [
        ("h", "翻卡後念"),
        ("b", "玻璃藥瓶不能摔，也不能抱得太緊。把藥箱安全送過泥濘樹根。"),
        ("h", "位置 3｜小格 1-3｜力量／速度"),
        ("b", "問：牠要怎麼用選好的能力，輕輕把藥瓶送過樹根？"),
        ("b", "力量卡住：一次拿一小箱；托住底部、不擠側面。<br/>速度卡住：每根樹根前停下；等藥瓶不晃再走。"),
        ("h", "結果"),
        ("b", "成功：藥箱送達且沒有破；劃掉 1 面盾。<br/>0 成功：藥箱安全到乾燥樹墩，但最後一段沒完成；可問是否後援。<br/>後援成功：接著送達；劃盾。後援也失敗：藥品仍安全，記錄「藥品留在樹墩」。"),
        ("h", "轉場"),
        ("b", "大地震動，河水在村前立起高牆。洪水巨獸到了。數剩餘水盾，翻指南背面。"),
    ]

    for index, (title, blocks) in enumerate(
        (("第一關｜找出安全道路", task1), ("第二關｜搖晃藤橋", task2), ("第三關｜搬運藥品", task3))
    ):
        x = 10 * mm + index * (col_w + gap)
        draw_flow_box(c, title, blocks, x, columns_y, col_w, columns_h, body_style=S["guide_small"])


def draw_dm_guide_page_two(c: canvas.Canvas) -> None:
    page_width, page_height = landscape(A4)
    guide_header(c, 2, "背面｜Boss、後援與結局")

    content_y = 11 * mm
    content_top = page_height - 22 * mm
    content_h = content_top - content_y
    gap = 4 * mm
    left_w = 145 * mm
    right_x = 10 * mm + left_w + gap
    right_w = page_width - 10 * mm - right_x

    boss_blocks = [
        ("h", "抵達時：先數剩餘水盾，再念門檻"),
        ("b", "0 盾：兩邊都有成功，合計至少 2（1＋1）。<br/>1 盾：兩邊都有成功，合計至少 3（1＋2）。<br/>2 盾：兩邊都有成功，合計至少 4（1＋3／2＋2／3＋1）。<br/>3 盾：兩邊各至少 2（2＋2）。一邊只有 1 顆骰時，擲骰前提醒孩子這個位置自己做不到。"),
        ("h", "Boss 念"),
        ("b", "洪水巨獸到了。一隻動物要突破水牆，另一隻要穩住避難區並指揮大家移動。現在才選兩隻主要動物。"),
        ("h", "4A｜大格 7-9｜力量／攻擊"),
        ("b", "問：怎麼在水牆打開大缺口？<br/>力量：推開重漂流木；撐開裂縫。<br/>攻擊：打最薄裂紋；打散纏住的樹枝。<br/>0 成功：已有小裂縫，但新水流補上缺口。"),
        ("h", "4B｜剛好格 4-6｜防禦／智慧"),
        ("b", "問：怎麼一邊保護、一邊讓避難區安全？<br/>防禦：擋危險水流再移動；護住缺口並留通道。<br/>智慧：高處看水流、分批通知；用走／停／轉彎指揮。<br/>0 成功：部分動物到高地，但外圍仍有缺口。"),
        ("h", "Boss 判斷"),
        ("b", "達門檻：直接成功，不再後援。<br/>未達門檻：先試算只改善 4A 或只改善 4B 能否達標；只有一個位置需要改善，才可呼叫 1 隻後援。兩邊都必須改善時不能後援。"),
        ("h", "單向支援旁白"),
        ("b", "4A 支援：打開水牆使水壓降低。<br/>4B 支援：從高處指出水牆最薄位置。"),
    ]
    draw_flow_box(c, "Boss｜洪水巨獸", boss_blocks, 10 * mm, content_y, left_w, content_h, body_style=S["guide_small"])

    box_gap = 3 * mm
    rules_h = 80 * mm
    ending_h = content_h - rules_h - box_gap
    rules_y = content_top - rules_h
    rules_blocks = [
        ("h", "骰池"),
        ("b", "屬性在區間 2 顆，不在 1 顆；所選屬性有 skillBonus 再加 1 顆；最多 3 顆。4、5、6 各算 1 成功。"),
        ("h", "單向支援"),
        ("b", "雙動物尚未通關時，成功較多的一邊，每個超過第 1 個的成功，可讓另一邊重擲 1 顆失敗骰。只做一個方向；後援不再觸發支援。"),
        ("h", "後援 A：取較高、不相加"),
        ("b", "正常擲骰與支援後仍失敗，且只補一個位置就可能通關，才可呼叫。每關最多 1 隻、整局 2 次。來源可選待命區或前面關卡的再挑戰區；本關剛失敗的動物不能救自己。先算被補位置最低需要幾個成功；後援骰池上限不足就不能呼叫。後援選被補位置允許的屬性，與原位置成功數取較高。"),
    ]
    draw_flow_box(c, "規則速查", rules_blocks, right_x, rules_y, right_w, rules_h, body_style=S["guide_small"])

    ending_blocks = [
        ("h", "成功結局"),
        ("b", "水牆落回河道，漂流木停在岸邊；動物村安全了。接著交代未完成後果與未出場動物的後勤工作。"),
        ("h", "失敗結局"),
        ("b", "有水盾：巨獸帶著剩餘水盾退回上游。<br/>0 水盾：外層保護已破，但兩個 Boss 工作沒有全部完成；危機未完全解除。<br/>都要補一句：前面完成的救援仍有效，下次可換隊伍再挑戰。"),
        ("h", "未完成後果"),
        ("b", "道路繞遠：補畫安全記號。<br/>藤橋未穩：守在橋頭提醒大家。<br/>小鹿仍等待：留在高石附近陪伴。<br/>藥品留在樹墩：沿撤退線接應。<br/>後勤不擲骰，不回溯護盾與勝負。"),
        ("h", "失敗旁白原則"),
        ("b", "怪環境或 Boss，不怪孩子；保留動物已完成的小成果；故事繼續，不回溯重玩。"),
    ]
    draw_flow_box(c, "結果與結局", ending_blocks, right_x, content_y, right_w, ending_h, body_style=S["guide_small"])


def draw_dm_guide() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(DM_GUIDE_PDF), pagesize=landscape(A4))
    c.setTitle("暴雨森林救援隊：DM 雙面指南")
    draw_dm_guide_page_one(c)
    c.showPage()
    draw_dm_guide_page_two(c)
    c.showPage()
    c.save()


def main() -> None:
    draw_control_board()
    draw_reveal_cards()
    draw_dm_guide()
    for path in (CONTROL_BOARD_PDF, REVEAL_CARDS_PDF, DM_GUIDE_PDF):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
