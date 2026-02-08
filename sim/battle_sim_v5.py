"""
動物大對決蒙地卡羅模擬器 v5

包含全部 64 隻動物，使用新版骰 6 規則（重骰＋條件加分）
淘汰賽：64 → 32 → 16 → 8 → 4 → 2 → 冠軍（標準單淘汰）
"""
from dataclasses import dataclass
from random import randint, shuffle
import csv
from pathlib import Path


@dataclass
class Animal:
    name: str
    stats: list[int]  # [力量, 速度, 攻擊, 防禦, 智慧] 對應骰子 1-5
    special: dict[int, int]  # {屬性索引: 加成值}

    @property
    def total(self) -> int:
        return sum(self.stats)


# === 64 隻動物數據 ===
ANIMALS: dict[str, Animal] = {
    # 第一波 16 隻
    "非洲獅": Animal("非洲獅", [7, 6, 8, 4, 5], {0: 2, 2: 2}),
    "非洲象": Animal("非洲象", [9, 2, 3, 8, 8], {2: 1, 3: 3}),
    "大猩猩": Animal("大猩猩", [8, 4, 4, 5, 9], {0: 1, 1: 1, 3: 2}),
    "灣鱷": Animal("灣鱷", [8, 3, 9, 7, 2], {0: 2, 3: 2}),
    "蜜獾": Animal("蜜獾", [5, 4, 6, 7, 6], {3: 3, 4: 1}),
    "蘇門答臘虎": Animal("蘇門答臘虎", [7, 5, 8, 4, 4], {0: 1, 2: 2, 4: 1}),
    "海豚": Animal("海豚", [4, 7, 3, 4, 8], {3: 2, 4: 2}),
    "科摩多龍": Animal("科摩多龍", [6, 3, 7, 6, 4], {2: 1, 3: 3}),
    "獵豹": Animal("獵豹", [4, 9, 6, 2, 4], {1: 2, 2: 1, 3: 1}),
    "北極狐": Animal("北極狐", [3, 7, 3, 4, 7], {1: 1, 3: 1, 4: 2}),
    "紅袋鼠": Animal("紅袋鼠", [5, 6, 5, 4, 3], {0: 1, 1: 1, 2: 2}),
    "遊隼": Animal("遊隼", [2, 9, 5, 1, 4], {2: 1, 3: 2, 4: 1}),
    "黑斑羚": Animal("黑斑羚", [3, 8, 2, 3, 3], {1: 2, 3: 2}),
    "貓頭鷹": Animal("貓頭鷹", [2, 5, 4, 2, 6], {1: 1, 3: 1, 4: 2}),
    "穿山甲": Animal("穿山甲", [3, 2, 1, 9, 2], {1: 2, 3: 2}),
    "加拉巴哥象龜": Animal("加拉巴哥象龜", [3, 1, 1, 9, 2], {3: 3, 4: 1}),
    # 第三波 19 隻
    "非洲野犬": Animal("非洲野犬", [3, 7, 5, 2, 6], {1: 1, 2: 2, 4: 1}),
    "鬣狗": Animal("鬣狗", [6, 6, 7, 4, 6], {0: 2, 2: 2}),
    "疣豬": Animal("疣豬", [5, 5, 5, 4, 4], {0: 1, 2: 2, 3: 1}),
    "山豬": Animal("山豬", [6, 5, 6, 6, 5], {0: 1, 1: 2, 2: 1}),
    "駱駝": Animal("駱駝", [7, 5, 3, 6, 3], {1: 1, 3: 2, 4: 1}),
    "豪豬": Animal("豪豬", [2, 2, 3, 8, 3], {2: 1, 3: 3}),
    "火雞": Animal("火雞", [2, 4, 2, 2, 3], {1: 2, 3: 1, 4: 1}),
    "美洲野牛": Animal("美洲野牛", [8, 6, 5, 7, 3], {0: 2, 3: 2}),
    "犛牛": Animal("犛牛", [8, 4, 5, 7, 3], {0: 1, 3: 3}),
    "大耳狐": Animal("大耳狐", [2, 6, 2, 2, 5], {1: 1, 3: 1, 4: 2}),
    "水鹿": Animal("水鹿", [6, 6, 4, 4, 3], {1: 2, 3: 2}),
    "麋鹿": Animal("麋鹿", [7, 6, 5, 5, 3], {0: 1, 2: 2, 3: 1}),
    "狐獴": Animal("狐獴", [1, 5, 2, 2, 7], {1: 1, 3: 1, 4: 2}),
    "黃鼠狼": Animal("黃鼠狼", [1, 7, 4, 2, 4], {1: 2, 2: 2}),
    "長臂猿": Animal("長臂猿", [4, 7, 3, 2, 7], {1: 2, 3: 1, 4: 1}),
    "食蟻獸": Animal("食蟻獸", [4, 3, 5, 5, 2], {0: 1, 2: 2, 3: 1}),
    "鴨嘴獸": Animal("鴨嘴獸", [2, 4, 5, 3, 4], {2: 3, 3: 1}),
    "樹懶": Animal("樹懶", [3, 1, 2, 5, 2], {3: 3, 4: 1}),
    "藍鯨": Animal("藍鯨", [9, 4, 2, 9, 7], {0: 2, 3: 2}),
    # 第四波 13 隻
    "大白鯊": Animal("大白鯊", [7, 7, 9, 5, 4], {1: 2, 2: 2}),
    "河馬": Animal("河馬", [9, 4, 7, 8, 3], {0: 2, 2: 2}),
    "北極熊": Animal("北極熊", [8, 5, 8, 5, 5], {0: 2, 2: 2}),
    "犀牛": Animal("犀牛", [9, 4, 7, 9, 2], {0: 2, 3: 2}),
    "花豹": Animal("花豹", [6, 7, 8, 3, 5], {2: 2, 4: 2}),
    "灰狼": Animal("灰狼", [5, 7, 6, 4, 7], {2: 2, 4: 2}),
    "狼獾": Animal("狼獾", [5, 5, 7, 6, 5], {2: 2, 3: 2}),
    "麝牛": Animal("麝牛", [7, 4, 5, 7, 4], {0: 2, 3: 2}),
    "長頸鹿": Animal("長頸鹿", [7, 6, 5, 5, 3], {0: 2, 1: 1, 2: 1}),
    "蟒蛇": Animal("蟒蛇", [8, 2, 7, 5, 2], {0: 3, 2: 1}),
    "人": Animal("人", [3, 4, 2, 1, 9], {2: 2, 4: 2}),
    "鵜鶘": Animal("鵜鶘", [3, 5, 3, 2, 4], {1: 1, 2: 2, 4: 1}),
    "丹頂鶴": Animal("丹頂鶴", [2, 5, 3, 2, 5], {1: 2, 2: 1, 4: 1}),
    # 第五波 16 隻
    "虎鯨": Animal("虎鯨", [9, 7, 9, 5, 8], {0: 2, 2: 2}),
    "鴕鳥": Animal("鴕鳥", [5, 8, 5, 3, 3], {0: 2, 2: 2}),
    "雪豹": Animal("雪豹", [5, 5, 6, 3, 4], {1: 1, 2: 2, 4: 1}),
    "白頭海鵰": Animal("白頭海鵰", [3, 7, 6, 2, 5], {0: 1, 1: 1, 2: 2}),
    "電鰻": Animal("電鰻", [4, 4, 7, 4, 3], {2: 2, 3: 2}),
    "雪鴞": Animal("雪鴞", [2, 7, 4, 2, 6], {1: 1, 2: 1, 4: 2}),
    "乳牛": Animal("乳牛", [7, 3, 2, 5, 4], {0: 2, 3: 2}),
    "擬態章魚": Animal("擬態章魚", [2, 4, 3, 3, 8], {3: 2, 4: 2}),
    "海獺": Animal("海獺", [3, 4, 2, 4, 7], {2: 2, 4: 2}),
    "浣熊": Animal("浣熊", [2, 4, 3, 3, 7], {1: 2, 4: 2}),
    "蠍子": Animal("蠍子", [1, 3, 7, 5, 2], {2: 2, 3: 2}),
    "皇帝企鵝": Animal("皇帝企鵝", [3, 3, 2, 4, 5], {1: 2, 3: 2}),
    "犰狳": Animal("犰狳", [2, 3, 1, 7, 3], {1: 1, 3: 3}),
    "孔雀": Animal("孔雀", [2, 3, 2, 3, 4], {3: 2, 4: 2}),
    "箭毒蛙": Animal("箭毒蛙", [1, 3, 1, 7, 2], {2: 1, 3: 3}),
    "蘭花螳螂": Animal("蘭花螳螂", [1, 2, 4, 2, 2], {2: 3, 3: 1}),
}


def roll_dice() -> tuple[int, int]:
    """擲 2d6"""
    return randint(1, 6), randint(1, 6)


def resolve_die(d: int, max_rerolls: int = 100) -> tuple[int, int]:
    """解析單顆骰子：回傳 (最終值 1-5, 觸發次數)"""
    triggers = 0
    while d == 6 and triggers < max_rerolls:
        triggers += 1
        d = randint(1, 6)
    if d == 6:
        d = 5
    return d, triggers


def calculate_score(animal: Animal, d1: int, d2: int) -> int:
    """
    新版骰 6 規則計分：
    - 骰到 6 → 重骰（可連鎖），每次記 1 次觸發
    - 最終 2 顆骰子定案（1-5），計算基礎分
    - 每次觸發 → 檢查最終骰面命中的屬性加成
    - doubles 時同一屬性加 2 次（每顆骰子獨立檢查）
    """
    final_d1, t1 = resolve_die(d1)
    final_d2, t2 = resolve_die(d2)
    total_triggers = t1 + t2

    # 基礎分
    if final_d1 == final_d2:
        base = animal.stats[final_d1 - 1] * 2
    else:
        base = animal.stats[final_d1 - 1] + animal.stats[final_d2 - 1]

    # 天賦加分
    if total_triggers > 0:
        hit_attrs = [final_d1 - 1, final_d2 - 1]
        bonus_per_trigger = sum(animal.special.get(a, 0) for a in hit_attrs)
        base += total_triggers * bonus_per_trigger

    return base


def fight_round(animal1: Animal, animal2: Animal) -> int:
    """單場對戰（各自擲骰）"""
    d1_a, d2_a = roll_dice()
    d1_b, d2_b = roll_dice()

    score_a = calculate_score(animal1, d1_a, d2_a)
    score_b = calculate_score(animal2, d1_b, d2_b)

    if score_a > score_b:
        return 1
    elif score_a < score_b:
        return -1
    return 0


def fight_match(animal1: Animal, animal2: Animal) -> int:
    """1 戰定勝負（平手則加賽）"""
    while True:
        result = fight_round(animal1, animal2)
        if result != 0:
            return result


def run_h2h_simulation(n_matches: int = 10000) -> dict:
    """執行全矩陣 1v1 模擬"""
    names = list(ANIMALS.keys())
    n = len(names)

    win_matrix = [[0.0] * n for _ in range(n)]
    total_pairs = n * (n - 1) // 2
    completed = 0

    print(f"H2H Simulation: {total_pairs} matchups, {n_matches} matches each...")

    for i in range(n):
        for j in range(i + 1, n):
            wins_i = 0
            for _ in range(n_matches):
                if fight_match(ANIMALS[names[i]], ANIMALS[names[j]]) == 1:
                    wins_i += 1

            win_rate_i = wins_i / n_matches
            win_matrix[i][j] = win_rate_i
            win_matrix[j][i] = 1 - win_rate_i

            completed += 1
            if completed % 100 == 0:
                progress = completed / total_pairs * 100
                print(f"\rProgress: {progress:5.1f}% ({completed}/{total_pairs})", end="", flush=True)

    print("\n")

    overall = []
    for i in range(n):
        total_win_rate = sum(win_matrix[i][j] for j in range(n) if j != i)
        overall.append(total_win_rate / (n - 1))

    return {
        "names": names,
        "matrix": win_matrix,
        "overall": overall,
    }


def run_tournament_64(animals: list[Animal]) -> tuple[list[Animal], Animal]:
    """
    64 隻動物標準單淘汰
    64 → 32 → 16 → 8 → 4 → 2 → 冠軍（6 輪）

    Returns:
        tuple: (4 強名單, 冠軍)
    """
    participants = animals.copy()
    assert len(participants) == 64, f"Expected 64 animals, got {len(participants)}"

    # 6 輪淘汰（64→32→16→8→4→2→1）
    semifinalists = None
    for round_num in range(6):
        next_round = []
        for i in range(0, len(participants), 2):
            result = fight_match(participants[i], participants[i + 1])
            winner = participants[i] if result == 1 else participants[i + 1]
            next_round.append(winner)

        # 記錄四強（8→4 那輪結束後）
        if len(next_round) == 4:
            semifinalists = next_round.copy()

        participants = next_round

    champion = participants[0]
    return semifinalists, champion


def run_tournament_simulation(n_tournaments: int = 100000) -> dict:
    """執行多次淘汰賽模擬"""
    animals = list(ANIMALS.values())

    top4_count = {a.name: 0 for a in animals}
    champion_count = {a.name: 0 for a in animals}

    print(f"Tournament Simulation: {n_tournaments} tournaments with {len(animals)} animals...")

    for i in range(n_tournaments):
        shuffled = animals.copy()
        shuffle(shuffled)

        semifinalists, champion = run_tournament_64(shuffled)

        for f in semifinalists:
            top4_count[f.name] += 1

        champion_count[champion.name] += 1

        if (i + 1) % 10000 == 0:
            progress = (i + 1) / n_tournaments * 100
            print(f"\rProgress: {progress:5.1f}% ({i+1}/{n_tournaments})", end="", flush=True)

    print("\n")

    top4_ranked = sorted(top4_count.items(), key=lambda x: x[1], reverse=True)
    champion_ranked = sorted(champion_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "top4_count": top4_count,
        "champion_count": champion_count,
        "top4_ranked": top4_ranked,
        "champion_ranked": champion_ranked,
        "n_tournaments": n_tournaments,
    }


def export_results(h2h_results: dict, tournament_results: dict, output_dir: Path) -> None:
    """匯出報告和 CSV"""
    output_dir.mkdir(parents=True, exist_ok=True)

    names = h2h_results["names"]
    matrix = h2h_results["matrix"]
    overall = h2h_results["overall"]
    n_tournaments = tournament_results["n_tournaments"]

    # 報告
    report_path = output_dir / "v5_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("   Animal Fight - Simulation v5 (64 Animals)\n")
        f.write("   新規則（骰 6 重骰＋條件加分）+ 64 隻標準單淘汰\n")
        f.write("=" * 70 + "\n\n")

        # H2H 排行
        f.write("=== 1v1 Win Rate Ranking ===\n\n")
        ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)

        f.write(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Win Rate':<10}\n")
        f.write("-" * 45 + "\n")
        for rank, (name, rate) in enumerate(ranked, 1):
            total = ANIMALS[name].total
            f.write(f"{rank:<6} {name:<14} {total:<6} {rate*100:>6.2f}%\n")

        # Top 4 排行
        f.write("\n" + "=" * 70 + "\n")
        f.write("=== Top 4 Rate (進入四強機率) ===\n\n")
        t4_ranked = tournament_results["top4_ranked"]

        f.write(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Count':<10} {'Rate':<10}\n")
        f.write("-" * 55 + "\n")
        for rank, (name, count) in enumerate(t4_ranked, 1):
            if count == 0:
                continue
            total = ANIMALS[name].total
            rate = count / n_tournaments
            f.write(f"{rank:<6} {name:<14} {total:<6} {count:<10} {rate*100:>6.2f}%\n")

        # Champion 排行
        f.write("\n" + "=" * 70 + "\n")
        f.write("=== Champion Rate (冠軍機率) ===\n\n")
        c_ranked = tournament_results["champion_ranked"]

        f.write(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Wins':<10} {'Rate':<10}\n")
        f.write("-" * 55 + "\n")
        for rank, (name, wins) in enumerate(c_ranked, 1):
            if wins == 0:
                continue
            total = ANIMALS[name].total
            rate = wins / n_tournaments
            f.write(f"{rank:<6} {name:<14} {total:<6} {wins:<10} {rate*100:>6.2f}%\n")

    # CSV - H2H 排行
    h2h_ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)
    with open(output_dir / "v5_h2h.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Total Stats", "Win Rate"])
        for rank, (name, rate) in enumerate(h2h_ranked, 1):
            total = ANIMALS[name].total
            writer.writerow([rank, name, total, f"{rate*100:.2f}%"])

    # CSV - 對戰矩陣
    with open(output_dir / "v5_matrix.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([""] + names)
        for i, name in enumerate(names):
            row = [name]
            for j in range(len(names)):
                if i == j:
                    row.append("-")
                else:
                    row.append(f"{matrix[i][j]*100:.1f}%")
            writer.writerow(row)

    # CSV - Top 4
    with open(output_dir / "v5_top4.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Total Stats", "Top4 Count", "Top4 Rate"])
        for rank, (name, count) in enumerate(tournament_results["top4_ranked"], 1):
            total = ANIMALS[name].total
            writer.writerow([rank, name, total, count, f"{count/n_tournaments*100:.2f}%"])

    # CSV - Champion
    with open(output_dir / "v5_champion.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Total Stats", "Champion Count", "Champion Rate"])
        for rank, (name, wins) in enumerate(tournament_results["champion_ranked"], 1):
            total = ANIMALS[name].total
            writer.writerow([rank, name, total, wins, f"{wins/n_tournaments*100:.2f}%"])

    print(f"Results exported to {output_dir}/")


def main():
    output_dir = Path(__file__).parent / "results"

    print("=" * 70)
    print("   Animal Fight - Simulation v5 (64 Animals)")
    print("   新規則（骰 6 重骰＋條件加分）+ 標準單淘汰")
    print("=" * 70)
    print()

    # 1. H2H 模擬
    print("=== Part 1: 1v1 Win Rate ===")
    h2h_results = run_h2h_simulation(n_matches=10000)

    # 2. 淘汰賽模擬
    print("=== Part 2: Tournament Simulation ===")
    tournament_results = run_tournament_simulation(n_tournaments=100000)

    # 匯出
    try:
        export_results(h2h_results, tournament_results, output_dir)
    except PermissionError:
        print("Warning: File locked, skipping export.")


if __name__ == "__main__":
    main()
