"""
動物大對決蒙地卡羅模擬器

模擬 16 隻動物兩兩對戰，統計勝率。
規則詳見 game/battle-rules.md
"""
from dataclasses import dataclass
from random import randint
import csv
from pathlib import Path


@dataclass
class Animal:
    name: str
    stats: list[int]  # [力量, 速度, 攻擊, 防禦, 智慧] 對應骰子 1-5
    special: dict[int, int]  # {屬性索引: 加成值}


# === 16 隻動物數據 ===
ANIMALS: dict[str, Animal] = {
    "非洲獅": Animal("非洲獅", [7, 5, 7, 5, 4], {0: 2, 2: 2}),
    "非洲象": Animal("非洲象", [8, 2, 6, 7, 5], {2: 1, 3: 3}),
    "貓頭鷹": Animal("貓頭鷹", [2, 5, 4, 3, 9], {1: 1, 3: 1, 4: 2}),
    "獵豹": Animal("獵豹", [4, 9, 6, 3, 4], {1: 2, 2: 1, 3: 1}),
    "穿山甲": Animal("穿山甲", [3, 4, 2, 9, 5], {1: 2, 3: 2}),
    "海豚": Animal("海豚", [3, 7, 5, 4, 8], {3: 2, 4: 2}),
    "遊隼": Animal("遊隼", [2, 8, 6, 1, 6], {2: 1, 3: 2, 4: 1}),
    "科摩多龍": Animal("科摩多龍", [6, 4, 8, 5, 3], {2: 1, 3: 3}),
    "大猩猩": Animal("大猩猩", [7, 4, 5, 5, 7], {0: 1, 1: 1, 3: 2}),
    "蜜獾": Animal("蜜獾", [5, 5, 7, 6, 4], {3: 3, 4: 1}),
    "加拉巴哥象龜": Animal("加拉巴哥象龜", [4, 1, 3, 8, 7], {3: 3, 4: 1}),
    "黑斑羚": Animal("黑斑羚", [3, 9, 4, 2, 5], {1: 2, 3: 2}),
    "蘇門答臘虎": Animal("蘇門答臘虎", [6, 6, 8, 4, 3], {0: 1, 2: 2, 4: 1}),
    "灣鱷": Animal("灣鱷", [7, 3, 9, 6, 2], {0: 2, 3: 2}),
    "北極狐": Animal("北極狐", [3, 7, 4, 3, 8], {1: 1, 3: 1, 4: 2}),
    "紅袋鼠": Animal("紅袋鼠", [5, 6, 6, 4, 3], {0: 1, 1: 1, 2: 2}),
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


def fight_round(animal1: Animal, animal2: Animal) -> int:
    """
    單場對戰

    Returns:
        1 = animal1 勝, -1 = animal2 勝, 0 = 平手
    """
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
    """
    三戰兩勝制

    Returns:
        1 = animal1 勝, -1 = animal2 勝
    """
    wins_a, wins_b = 0, 0

    while wins_a < 2 and wins_b < 2:
        result = fight_round(animal1, animal2)
        if result == 1:
            wins_a += 1
        elif result == -1:
            wins_b += 1
        # 平手不計分，繼續戰

    return 1 if wins_a == 2 else -1


def run_simulation(n_matches: int = 1000) -> dict:
    """
    執行全矩陣模擬

    Args:
        n_matches: 每組對戰場數

    Returns:
        dict with keys: names, matrix, overall
    """
    names = list(ANIMALS.keys())
    n = len(names)

    # 勝率矩陣：win_matrix[i][j] = animal_i 對 animal_j 的勝率
    win_matrix = [[0.0] * n for _ in range(n)]

    total_pairs = n * (n - 1) // 2
    completed = 0

    print(f"Starting simulation: {total_pairs} matchups, {n_matches} matches each...")
    print()

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
            progress = completed / total_pairs * 100
            print(f"\rProgress: {progress:5.1f}% ({completed}/{total_pairs})", end="", flush=True)

    print("\n")

    # 計算整體勝率（對其他 15 隻的平均勝率）
    overall = []
    for i in range(n):
        total_win_rate = sum(win_matrix[i][j] for j in range(n) if j != i)
        overall.append(total_win_rate / (n - 1))

    return {
        "names": names,
        "matrix": win_matrix,
        "overall": overall,
    }


def print_ranking(results: dict) -> None:
    """印出勝率排行榜"""
    names = results["names"]
    overall = results["overall"]

    # 排序
    ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)

    print("=" * 50)
    print("       Win Rate Ranking")
    print("=" * 50)
    print(f"{'Rank':<6} {'Animal':<14} {'Win Rate':<10} Bar")
    print("-" * 50)

    for rank, (name, rate) in enumerate(ranked, 1):
        bar_len = int(rate * 20)
        bar = "#" * bar_len + "-" * (20 - bar_len)
        print(f"{rank:<6} {name:<14} {rate*100:>5.1f}%    {bar}")

    print("=" * 50)


def print_matrix(results: dict) -> None:
    """印出對戰矩陣（簡化版）"""
    names = results["names"]
    matrix = results["matrix"]
    n = len(names)

    print("\nMatchup Matrix (row vs col, showing row's win rate)")
    print("-" * 60)

    # 縮寫名稱
    short_names = [n[:4] for n in names]

    # 表頭
    header = "        " + " ".join(f"{s:>5}" for s in short_names)
    print(header)
    print("-" * 60)

    for i in range(n):
        row = f"{short_names[i]:<6}"
        for j in range(n):
            if i == j:
                row += "    - "
            else:
                rate = matrix[i][j] * 100
                row += f"{rate:5.0f}%"
        print(row)


def export_csv(results: dict, output_dir: Path) -> None:
    """匯出 CSV 檔案"""
    output_dir.mkdir(parents=True, exist_ok=True)

    names = results["names"]
    matrix = results["matrix"]
    overall = results["overall"]

    # 整體勝率
    ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)
    with open(output_dir / "overall_winrate.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Win Rate"])
        for rank, (name, rate) in enumerate(ranked, 1):
            writer.writerow([rank, name, f"{rate*100:.1f}%"])

    # 對戰矩陣
    with open(output_dir / "matchup_matrix.csv", "w", newline="", encoding="utf-8-sig") as f:
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

    print(f"Results exported to {output_dir}/")


def run_tournament(animals: list[Animal]) -> Animal:
    """
    單次淘汰賽，回傳冠軍

    Args:
        animals: 參賽動物列表（需為 2 的冪次）
    """
    participants = animals.copy()

    while len(participants) > 1:
        next_round = []
        for i in range(0, len(participants), 2):
            result = fight_match(participants[i], participants[i + 1])
            winner = participants[i] if result == 1 else participants[i + 1]
            next_round.append(winner)
        participants = next_round

    return participants[0]


def run_tournament_simulation(n_tournaments: int = 1000) -> dict:
    """
    執行多次淘汰賽模擬，統計奪冠次數

    Args:
        n_tournaments: 模擬次數
    """
    import random

    animals = list(ANIMALS.values())
    champion_count = {a.name: 0 for a in animals}

    print(f"Starting tournament simulation: {n_tournaments} tournaments...")
    print()

    for i in range(n_tournaments):
        # 隨機排序參賽者
        shuffled = animals.copy()
        random.shuffle(shuffled)

        champion = run_tournament(shuffled)
        champion_count[champion.name] += 1

        if (i + 1) % 100 == 0:
            progress = (i + 1) / n_tournaments * 100
            print(f"\rProgress: {progress:5.1f}% ({i+1}/{n_tournaments})", end="", flush=True)

    print("\n")

    # 排序
    ranked = sorted(champion_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "champion_count": champion_count,
        "ranked": ranked,
        "n_tournaments": n_tournaments,
    }


def print_tournament_results(results: dict) -> None:
    """印出淘汰賽結果"""
    ranked = results["ranked"]
    n = results["n_tournaments"]

    print("=" * 55)
    print("       Tournament Champion Statistics")
    print("=" * 55)
    print(f"{'Rank':<6} {'Animal':<14} {'Wins':<8} {'Rate':<10} Bar")
    print("-" * 55)

    for rank, (name, wins) in enumerate(ranked, 1):
        rate = wins / n
        bar_len = int(rate * 40)
        bar = "#" * bar_len + "-" * (40 - bar_len)
        print(f"{rank:<6} {name:<14} {wins:<8} {rate*100:>5.1f}%    {bar}")

    print("=" * 55)


def export_tournament_csv(results: dict, output_dir: Path, filename: str = "tournament_champions.csv") -> None:
    """匯出淘汰賽結果 CSV"""
    output_dir.mkdir(parents=True, exist_ok=True)

    ranked = results["ranked"]
    n = results["n_tournaments"]

    with open(output_dir / filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Champion Count", "Champion Rate"])
        for rank, (name, wins) in enumerate(ranked, 1):
            writer.writerow([rank, name, wins, f"{wins/n*100:.1f}%"])

    print(f"Tournament results exported to {output_dir}/{filename}")


def main():
    import sys

    output_dir = Path(__file__).parent / "results"

    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    # 淘汰賽次數（預設 1000，可用第二參數指定）
    tournament_count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

    # 輸出檔名（預設 tournament_champions.csv，可用第三參數指定）
    tournament_filename = sys.argv[3] if len(sys.argv) > 3 else "tournament_champions.csv"

    if mode in ("all", "h2h"):
        # 1. 兩兩對戰勝率統計
        print("=== Part 1: Head-to-Head Win Rate ===\n")
        n = 1000
        results = run_simulation(n)
        print_ranking(results)
        try:
            export_csv(results, output_dir)
        except PermissionError:
            print("Warning: CSV file locked, skipping export.")

    if mode in ("all", "tournament"):
        # 2. 淘汰賽模擬
        print("\n=== Part 2: Tournament Simulation ===\n")
        tournament_results = run_tournament_simulation(tournament_count)
        print_tournament_results(tournament_results)
        try:
            export_tournament_csv(tournament_results, output_dir, tournament_filename)
        except PermissionError:
            print("Warning: CSV file locked, skipping export.")


if __name__ == "__main__":
    main()
