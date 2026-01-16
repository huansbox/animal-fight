"""
動物大對決蒙地卡羅模擬器 - 共用骰子版

規則變體：雙方使用同一個骰子結果，比較各自分數
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


# === 35 隻動物數據 ===
ANIMALS: dict[str, Animal] = {
    # 第一波 16 隻 (v2.1)
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
    "鬣狗": Animal("鬣狗", [6, 6, 7, 4, 6], {0: 2, 2: 2}),
    "美洲野牛": Animal("美洲野牛", [8, 6, 5, 7, 3], {0: 2, 3: 2}),
    "山豬": Animal("山豬", [6, 5, 6, 6, 5], {0: 1, 1: 2, 2: 1}),
    "犛牛": Animal("犛牛", [8, 4, 5, 7, 3], {0: 1, 3: 3}),
    "麋鹿": Animal("麋鹿", [7, 6, 5, 5, 3], {0: 1, 2: 2, 3: 1}),
    "駱駝": Animal("駱駝", [7, 5, 3, 6, 3], {1: 1, 3: 2, 4: 1}),
    "非洲野犬": Animal("非洲野犬", [3, 7, 5, 2, 6], {1: 1, 2: 2, 4: 1}),
    "疣豬": Animal("疣豬", [5, 5, 5, 4, 4], {0: 1, 2: 2, 3: 1}),
    "水鹿": Animal("水鹿", [6, 6, 4, 4, 3], {1: 2, 3: 2}),
    "長臂猿": Animal("長臂猿", [4, 7, 3, 2, 7], {1: 2, 3: 1, 4: 1}),
    "食蟻獸": Animal("食蟻獸", [4, 3, 5, 5, 2], {0: 1, 2: 2, 3: 1}),
    "豪豬": Animal("豪豬", [2, 2, 3, 8, 3], {2: 1, 3: 3}),
    "黃鼠狼": Animal("黃鼠狼", [1, 7, 4, 2, 4], {1: 2, 2: 2}),
    "鴨嘴獸": Animal("鴨嘴獸", [2, 4, 5, 3, 4], {2: 3, 3: 1}),
    "大耳狐": Animal("大耳狐", [2, 6, 2, 2, 5], {1: 1, 3: 1, 4: 2}),
    "狐獴": Animal("狐獴", [1, 5, 2, 2, 7], {1: 1, 3: 1, 4: 2}),
    "火雞": Animal("火雞", [2, 4, 2, 2, 3], {1: 2, 3: 1, 4: 1}),
    "樹懶": Animal("樹懶", [3, 1, 2, 5, 2], {3: 3, 4: 1}),
    "藍鯨": Animal("藍鯨", [9, 4, 2, 9, 7], {0: 2, 3: 2}),
}


def roll_dice() -> tuple[int, int]:
    """擲 2d6"""
    return randint(1, 6), randint(1, 6)


def calculate_score(animal: Animal, d1: int, d2: int, special_active: bool = False) -> int:
    """
    計算單次擲骰得分

    Args:
        animal: 動物資料
        d1, d2: 兩顆骰子點數
        special_active: 是否已觸發特殊能力（雙6重骰後為 True）

    Returns:
        分數, 新的 d1, 新的 d2 (重骰後)
    """
    # 雙 6：重骰，特殊能力觸發
    if d1 == 6 and d2 == 6:
        new_d1, new_d2 = roll_dice()
        return calculate_score(animal, new_d1, new_d2, special_active=True)

    # 單 6：另一顆的屬性 + 該屬性的特殊加成
    if d1 == 6:
        attr_idx = d2 - 1
        base = animal.stats[attr_idx]
        bonus = animal.special.get(attr_idx, 0)
        return base + bonus

    if d2 == 6:
        attr_idx = d1 - 1
        base = animal.stats[attr_idx]
        bonus = animal.special.get(attr_idx, 0)
        return base + bonus

    # 相同點數：該屬性 ×2
    if d1 == d2:
        attr_idx = d1 - 1
        base = animal.stats[attr_idx]
        if special_active:
            bonus = animal.special.get(attr_idx, 0)
            return (base + bonus) * 2
        return base * 2

    # 普通情況：兩屬性相加
    if special_active:
        score = 0
        for d in [d1, d2]:
            attr_idx = d - 1
            base = animal.stats[attr_idx]
            bonus = animal.special.get(attr_idx, 0)
            score += base + bonus
        return score

    return animal.stats[d1 - 1] + animal.stats[d2 - 1]


def calculate_score_shared(animal: Animal, d1: int, d2: int) -> int:
    """
    共用骰子版計分（不重骰，保持骰子結果一致）

    雙6 處理：兩動物都觸發特殊能力，但不重骰
    """
    # 雙 6：特殊能力觸發，但不重骰（用 1+2 作為基礎）
    if d1 == 6 and d2 == 6:
        # 全部屬性加成
        score = 0
        for i in range(5):
            score += animal.stats[i] + animal.special.get(i, 0)
        return score // 2  # 取平均兩個屬性

    # 單 6：另一顆的屬性 + 該屬性的特殊加成
    if d1 == 6:
        attr_idx = d2 - 1
        base = animal.stats[attr_idx]
        bonus = animal.special.get(attr_idx, 0)
        return base + bonus

    if d2 == 6:
        attr_idx = d1 - 1
        base = animal.stats[attr_idx]
        bonus = animal.special.get(attr_idx, 0)
        return base + bonus

    # 相同點數：該屬性 ×2
    if d1 == d2:
        attr_idx = d1 - 1
        base = animal.stats[attr_idx]
        return base * 2

    # 普通情況：兩屬性相加
    return animal.stats[d1 - 1] + animal.stats[d2 - 1]


def fight_round_shared(animal1: Animal, animal2: Animal) -> int:
    """
    共用骰子對戰（雙方用同一個骰子結果）

    Returns:
        1 = animal1 勝, -1 = animal2 勝, 0 = 平手
    """
    d1, d2 = roll_dice()

    score_a = calculate_score_shared(animal1, d1, d2)
    score_b = calculate_score_shared(animal2, d1, d2)

    if score_a > score_b:
        return 1
    elif score_a < score_b:
        return -1
    return 0


def fight_match_shared(animal1: Animal, animal2: Animal) -> int:
    """
    1 戰定勝負（平手則加賽）

    Returns:
        1 = animal1 勝, -1 = animal2 勝
    """
    while True:
        result = fight_round_shared(animal1, animal2)
        if result != 0:
            return result


def run_h2h_simulation(n_matches: int = 10000) -> dict:
    """
    執行全矩陣 1v1 模擬（共用骰子）
    """
    names = list(ANIMALS.keys())
    n = len(names)

    win_matrix = [[0.0] * n for _ in range(n)]
    total_pairs = n * (n - 1) // 2
    completed = 0

    print(f"H2H Simulation: {total_pairs} matchups, {n_matches} matches each...")
    print()

    for i in range(n):
        for j in range(i + 1, n):
            wins_i = 0
            for _ in range(n_matches):
                if fight_match_shared(ANIMALS[names[i]], ANIMALS[names[j]]) == 1:
                    wins_i += 1

            win_rate_i = wins_i / n_matches
            win_matrix[i][j] = win_rate_i
            win_matrix[j][i] = 1 - win_rate_i

            completed += 1
            if completed % 50 == 0:
                progress = completed / total_pairs * 100
                print(f"\rProgress: {progress:5.1f}% ({completed}/{total_pairs})", end="", flush=True)

    print("\n")

    # 計算整體勝率
    overall = []
    for i in range(n):
        total_win_rate = sum(win_matrix[i][j] for j in range(n) if j != i)
        overall.append(total_win_rate / (n - 1))

    return {
        "names": names,
        "matrix": win_matrix,
        "overall": overall,
    }


def run_tournament(animals: list[Animal]) -> Animal:
    """單次淘汰賽"""
    participants = animals.copy()

    while len(participants) > 1:
        next_round = []
        for i in range(0, len(participants), 2):
            result = fight_match_shared(participants[i], participants[i + 1])
            winner = participants[i] if result == 1 else participants[i + 1]
            next_round.append(winner)
        participants = next_round

    return participants[0]


def run_tournament_simulation(n_tournaments: int = 100000) -> dict:
    """執行多次淘汰賽模擬"""
    # 排除 3 隻高度相似動物，保留 32 隻
    excluded = {"加拉巴哥象龜", "犛牛", "水鹿"}
    animals = [a for a in ANIMALS.values() if a.name not in excluded]
    champion_count = {a.name: 0 for a in animals}

    print(f"Tournament Simulation: {n_tournaments} tournaments with {len(animals)} animals...")
    print()

    for i in range(n_tournaments):
        shuffled = animals.copy()
        shuffle(shuffled)
        champion = run_tournament(shuffled)
        champion_count[champion.name] += 1

        if (i + 1) % 10000 == 0:
            progress = (i + 1) / n_tournaments * 100
            print(f"\rProgress: {progress:5.1f}% ({i+1}/{n_tournaments})", end="", flush=True)

    print("\n")

    ranked = sorted(champion_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "champion_count": champion_count,
        "ranked": ranked,
        "n_tournaments": n_tournaments,
    }


def print_h2h_ranking(results: dict) -> None:
    """印出 1v1 勝率排行榜"""
    names = results["names"]
    overall = results["overall"]

    ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)

    print("=" * 60)
    print("   1v1 Win Rate Ranking (Shared Dice)")
    print("=" * 60)
    print(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Win Rate':<10} Bar")
    print("-" * 60)

    for rank, (name, rate) in enumerate(ranked, 1):
        total = ANIMALS[name].total
        bar_len = int(rate * 30)
        bar = "#" * bar_len + "-" * (30 - bar_len)
        print(f"{rank:<6} {name:<14} {total:<6} {rate*100:>5.1f}%    {bar}")

    print("=" * 60)


def print_tournament_results(results: dict) -> None:
    """印出淘汰賽結果"""
    ranked = results["ranked"]
    n = results["n_tournaments"]

    print("=" * 65)
    print("   Tournament Champion Rate (Shared Dice)")
    print("=" * 65)
    print(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Wins':<8} {'Rate':<8} Bar")
    print("-" * 65)

    for rank, (name, wins) in enumerate(ranked, 1):
        if wins == 0:
            continue
        total = ANIMALS[name].total
        rate = wins / n
        bar_len = int(rate * 50)
        bar = "#" * bar_len
        print(f"{rank:<6} {name:<14} {total:<6} {wins:<8} {rate*100:>5.2f}%  {bar}")

    print("=" * 65)


def export_csv(h2h_results: dict, tournament_results: dict, output_dir: Path) -> None:
    """匯出 CSV"""
    output_dir.mkdir(parents=True, exist_ok=True)

    names = h2h_results["names"]
    matrix = h2h_results["matrix"]
    overall = h2h_results["overall"]

    # H2H 排行
    ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)

    with open(output_dir / "shared_dice_h2h.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Total Stats", "Win Rate"])
        for rank, (name, rate) in enumerate(ranked, 1):
            total = ANIMALS[name].total
            writer.writerow([rank, name, total, f"{rate*100:.2f}%"])

    # 對戰矩陣
    with open(output_dir / "shared_dice_matchup_matrix.csv", "w", newline="", encoding="utf-8-sig") as f:
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

    # Tournament 排行
    t_ranked = tournament_results["ranked"]
    n = tournament_results["n_tournaments"]

    with open(output_dir / "shared_dice_tournament.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Total Stats", "Champion Count", "Champion Rate"])
        for rank, (name, wins) in enumerate(t_ranked, 1):
            total = ANIMALS[name].total
            writer.writerow([rank, name, total, wins, f"{wins/n*100:.2f}%"])

    print(f"Results exported to {output_dir}/")


def main():
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "shared_dice_report.txt"

    print("Running simulation...")

    # 1. H2H 模擬
    print("=== Part 1: 1v1 Win Rate ===")
    h2h_results = run_h2h_simulation(n_matches=10000)

    # 2. 淘汰賽模擬
    print("\n=== Part 2: Tournament Simulation ===")
    tournament_results = run_tournament_simulation(n_tournaments=100000)

    # 寫入報告
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("   Animal Fight - Shared Dice Simulation\n")
        f.write("   (雙方使用同一個骰子結果)\n")
        f.write("=" * 65 + "\n\n")

        # H2H 排行
        f.write("=== 1v1 Win Rate Ranking ===\n\n")
        names = h2h_results["names"]
        overall = h2h_results["overall"]
        ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)

        f.write(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Win Rate':<10}\n")
        f.write("-" * 45 + "\n")
        for rank, (name, rate) in enumerate(ranked, 1):
            total = ANIMALS[name].total
            f.write(f"{rank:<6} {name:<14} {total:<6} {rate*100:>6.2f}%\n")

        # Tournament 排行
        f.write("\n" + "=" * 65 + "\n")
        f.write("=== Tournament Champion Rate ===\n\n")
        t_ranked = tournament_results["ranked"]
        n = tournament_results["n_tournaments"]

        f.write(f"{'Rank':<6} {'Animal':<14} {'Total':<6} {'Wins':<10} {'Rate':<10}\n")
        f.write("-" * 55 + "\n")
        for rank, (name, wins) in enumerate(t_ranked, 1):
            if wins == 0:
                continue
            total = ANIMALS[name].total
            rate = wins / n
            f.write(f"{rank:<6} {name:<14} {total:<6} {wins:<10} {rate*100:>6.2f}%\n")

    # 匯出 CSV
    try:
        export_csv(h2h_results, tournament_results, output_dir)
    except PermissionError:
        print("Warning: CSV file locked, skipping export.")

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
