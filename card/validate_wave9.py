"""Wave 9 自動化前置檢查（SOP 步驟 3 + 3.5）"""
import json, re, sys
from pathlib import Path

BASE = Path(__file__).parent

# ── 讀取 wave9 ──────────────────────────────────────
wave9 = json.loads((BASE / "data/animals-wave9.json").read_text(encoding="utf-8"))

# ── 從 final_cards.html 解析全部現有動物 ─────────────
html = (BASE / "final_cards.html").read_text(encoding="utf-8")
# 找到 const animals = [ ... ]; 區塊
m = re.search(r'const animals = \[(.*?)\];', html, re.DOTALL)
if not m:
    sys.exit("ERROR: 無法從 final_cards.html 解析 animals 陣列")

raw = m.group(1)
# 移除 JS 單行註解
raw = re.sub(r'//.*', '', raw)
# 將 JS 物件轉為合法 JSON：加上雙引號 key
raw_json = re.sub(r'(\b)(name|en|img|stats|skillName|skillDesc|skillBonus|attr|val):', r'"\2":', raw)
# 處理 JS 字串中可能有的單引號（不適用此專案，但做保險）
# 移除行尾多餘逗號
raw_json = re.sub(r',\s*([\]}])', r'\1', raw_json)
# 包成陣列
try:
    existing = json.loads(f"[{raw_json}]")
except json.JSONDecodeError as e:
    # 除錯：找出問題位置
    lines = f"[{raw_json}]".split('\n')
    for i, line in enumerate(lines[max(0,16):20], start=max(0,16)):
        print(f"  LINE {i}: {line[:100]}")
    sys.exit(f"ERROR: JSON 解析失敗: {e}")

print(f"現有動物: {len(existing)} 隻")
print(f"Wave 9 動物: {len(wave9)} 隻")
print("=" * 60)

errors = []
warnings = []

# ══ 檢查 1：skillBonus 加總 = 4 ═══════════════════════
print("\n【檢查 1】skillBonus 加總 = 4")
for a in wave9:
    total = sum(b["val"] for b in a["skillBonus"])
    if total != 4:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）bonus 加總 = {total}（應為 4）")
if not any("檢查 1" in e for e in errors):
    print("  PASS: 全部 22 隻 bonus 加總 = 4")
else:
    for e in errors:
        print(e)

# ══ 檢查 2：skillName 四字 + 不撞名 ═══════════════════
print("\n【檢查 2】skillName 四字 + 不撞名")
existing_names = {a["skillName"] for a in existing}
wave9_names = set()
for a in wave9:
    name_len = len(a["skillName"])
    if name_len != 4:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）skillName「{a['skillName']}」= {name_len} 字（應為 4）")
    if a["skillName"] in existing_names:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）skillName「{a['skillName']}」與現有動物撞名！")
    if a["skillName"] in wave9_names:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）skillName「{a['skillName']}」Wave 9 內部撞名！")
    wave9_names.add(a["skillName"])

check2_errs = [e for e in errors if "檢查 2" in e or "skillName" in e]
if not check2_errs:
    print("  PASS: 全部 22 隻 skillName 四字且無撞名")
else:
    for e in check2_errs:
        print(e)

# ══ 檢查 3：skillDesc 字數（15-25 字，不含標點） ═══════
print("\n【檢查 3】skillDesc 字數（15-25 字，不含標點）")
punct = set("，。！？、；：「」『』（）—…《》〈〉【】")
for a in wave9:
    chars = [c for c in a["skillDesc"] if c not in punct]
    clen = len(chars)
    if clen < 15 or clen > 25:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）skillDesc = {clen} 字（應為 15-25）：「{a['skillDesc']}」")
    else:
        pass  # OK

check3_errs = [e for e in errors if "skillDesc" in e]
if not check3_errs:
    print("  PASS: 全部 22 隻 skillDesc 字數在 15-25 範圍")
else:
    for e in check3_errs:
        print(e)

# ══ 檢查 4：加成模式不重疊 ════════════════════════════
print("\n【檢查 4】加成模式不重疊（skillBonus attr+val 組合）")

def bonus_key(bonus_list):
    """將 skillBonus 轉成可比較的 tuple"""
    return tuple(sorted((b["attr"], b["val"]) for b in bonus_list))

existing_patterns = {}
for a in existing:
    k = bonus_key(a["skillBonus"])
    if k not in existing_patterns:
        existing_patterns[k] = []
    existing_patterns[k].append(a["name"])

wave9_patterns = {}
for a in wave9:
    k = bonus_key(a["skillBonus"])
    # 與現有動物比對
    if k in existing_patterns:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）bonus 模式 {k} 與現有動物重疊：{existing_patterns[k]}")
    # Wave 9 內部比對
    if k in wave9_patterns:
        errors.append(f"  FAIL: {a['name']}（{a['id']}）bonus 模式 {k} 與 Wave 9 內部重疊：{wave9_patterns[k]}")
    if k not in wave9_patterns:
        wave9_patterns[k] = []
    wave9_patterns[k].append(a["name"])

check4_errs = [e for e in errors if "bonus 模式" in e]
if not check4_errs:
    print("  PASS: 全部 22 隻 bonus 模式唯一")
else:
    for e in check4_errs:
        print(e)

# ══ 檢查 5：五維差異分數 ≤ 3 必須調整 ═════════════════
print("\n【檢查 5】五維差異分數（<=3 = 必須調整）")

def diff_score(s1, s2):
    return sum(abs(a - b) for a, b in zip(s1, s2))

# Wave 9 內部
print("  --- Wave 9 內部比對 ---")
internal_conflicts = []
for i in range(len(wave9)):
    for j in range(i + 1, len(wave9)):
        d = diff_score(wave9[i]["stats"], wave9[j]["stats"])
        if d <= 3:
            msg = f"  FAIL: {wave9[i]['name']} {wave9[i]['stats']} vs {wave9[j]['name']} {wave9[j]['stats']} → diff = {d}"
            errors.append(msg)
            internal_conflicts.append(msg)

if not internal_conflicts:
    print("  PASS: Wave 9 內部無差異 <= 3 的配對")
else:
    for c in internal_conflicts:
        print(c)

# Wave 9 vs 現有動物
print("  --- Wave 9 vs 現有 106 隻比對 ---")
external_conflicts = []
for new in wave9:
    for old in existing:
        d = diff_score(new["stats"], old["stats"])
        if d <= 3:
            msg = f"  FAIL: {new['name']} {new['stats']} vs {old['name']} {old['stats']} → diff = {d}"
            errors.append(msg)
            external_conflicts.append(msg)

if not external_conflicts:
    print("  PASS: Wave 9 vs 現有動物無差異 <= 3 的配對")
else:
    for c in external_conflicts:
        print(c)

# ══ 檢查 6：stats 範圍（每個屬性 1-9） ════════════════
print("\n【檢查 6】stats 範圍（每個屬性 1-9）")
for a in wave9:
    for idx, v in enumerate(a["stats"]):
        if v < 1 or v > 9:
            errors.append(f"  FAIL: {a['name']}（{a['id']}）stats[{idx}] = {v}（應為 1-9）")

check6_errs = [e for e in errors if "stats[" in e]
if not check6_errs:
    print("  PASS: 全部 22 隻 stats 範圍 1-9")
else:
    for e in check6_errs:
        print(e)

# ══ 總結 ═══════════════════════════════════════════════
print("\n" + "=" * 60)
print(f"總結: {len(errors)} 個錯誤, {len(warnings)} 個警告")
if errors:
    print("\n所有錯誤列表:")
    for i, e in enumerate(errors, 1):
        print(f"  {i}. {e.strip()}")
else:
    print("\n全部通過！可以進入步驟 4（3 Agent 數值審核）")
