"""
動物大對決模擬器 - 1 戰定勝負版本

模擬規則：單場決勝（非 3 戰 2 勝）
"""
import csv
from pathlib import Path
import random

from battle_sim import ANIMALS, fight_round


def fight_match_single(animal1, animal2) -> int:
    """
    1 戰定勝負

    Returns:
        1 = animal1 勝, -1 = animal2 勝
    """
    while True:
        result = fight_round(animal1, animal2)
        if result != 0:
            return result


def run_h2h_simulation(n_matches: int = 10000) -> dict:
    """
    1v1 兩兩對戰勝率統計
    """
    names = list(ANIMALS.keys())
    n = len(names)
    win_matrix = [[0.0] * n for _ in range(n)]

    total_pairs = n * (n - 1) // 2
    completed = 0

    print(f"[1v1] {total_pairs} 組對戰，每組 {n_matches} 場...")

    for i in range(n):
        for j in range(i + 1, n):
            wins_i = 0
            for _ in range(n_matches):
                if fight_match_single(ANIMALS[names[i]], ANIMALS[names[j]]) == 1:
                    wins_i += 1

            win_rate_i = wins_i / n_matches
            win_matrix[i][j] = win_rate_i
            win_matrix[j][i] = 1 - win_rate_i

            completed += 1
            progress = completed / total_pairs * 100
            print(f"\r進度: {progress:5.1f}% ({completed}/{total_pairs})", end="", flush=True)

    print("\n")

    overall = []
    for i in range(n):
        total_win_rate = sum(win_matrix[i][j] for j in range(n) if j != i)
        overall.append(total_win_rate / (n - 1))

    return {"names": names, "matrix": win_matrix, "overall": overall}


def run_tournament_single(animals: list) -> object:
    """單次淘汰賽（1 戰定勝負），回傳冠軍"""
    participants = animals.copy()

    while len(participants) > 1:
        next_round = []
        for i in range(0, len(participants), 2):
            result = fight_match_single(participants[i], participants[i + 1])
            winner = participants[i] if result == 1 else participants[i + 1]
            next_round.append(winner)
        participants = next_round

    return participants[0]


def run_tournament_simulation(n_tournaments: int = 10000) -> dict:
    """淘汰賽模擬"""
    animals = list(ANIMALS.values())
    champion_count = {a.name: 0 for a in animals}

    print(f"[淘汰賽] {n_tournaments} 次模擬...")

    for i in range(n_tournaments):
        shuffled = animals.copy()
        random.shuffle(shuffled)
        champion = run_tournament_single(shuffled)
        champion_count[champion.name] += 1

        if (i + 1) % 500 == 0:
            progress = (i + 1) / n_tournaments * 100
            print(f"\r進度: {progress:5.1f}% ({i+1}/{n_tournaments})", end="", flush=True)

    print("\n")

    ranked = sorted(champion_count.items(), key=lambda x: x[1], reverse=True)
    return {"champion_count": champion_count, "ranked": ranked, "n_tournaments": n_tournaments}


def export_results(h2h_results: dict, tournament_results: dict, output_dir: Path) -> None:
    """匯出 CSV"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1v1 整體勝率
    names = h2h_results["names"]
    overall = h2h_results["overall"]
    matrix = h2h_results["matrix"]

    ranked_h2h = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)
    with open(output_dir / "h2h_winrate_single.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Win Rate"])
        for rank, (name, rate) in enumerate(ranked_h2h, 1):
            writer.writerow([rank, name, f"{rate*100:.1f}%"])

    # 1v1 對戰矩陣
    with open(output_dir / "matchup_matrix_single.csv", "w", newline="", encoding="utf-8-sig") as f:
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

    # 淘汰賽
    ranked_t = tournament_results["ranked"]
    n = tournament_results["n_tournaments"]
    with open(output_dir / "tournament_single.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Animal", "Champion Count", "Champion Rate"])
        for rank, (name, wins) in enumerate(ranked_t, 1):
            writer.writerow([rank, name, wins, f"{wins/n*100:.2f}%"])

    print(f"結果已匯出至 {output_dir}/")


def print_results(h2h_results: dict, tournament_results: dict) -> None:
    """印出結果摘要"""
    print("=" * 55)
    print("  1v1 勝率排行（1 戰定勝負）")
    print("=" * 55)

    names = h2h_results["names"]
    overall = h2h_results["overall"]
    ranked = sorted(zip(names, overall), key=lambda x: x[1], reverse=True)

    print(f"{'排名':<6} {'動物':<14} {'勝率':<10}")
    print("-" * 35)
    for rank, (name, rate) in enumerate(ranked, 1):
        print(f"{rank:<6} {name:<14} {rate*100:>5.1f}%")

    print("\n")
    print("=" * 55)
    print("  淘汰賽奪冠率（1 戰定勝負）")
    print("=" * 55)

    ranked_t = tournament_results["ranked"]
    n = tournament_results["n_tournaments"]

    print(f"{'排名':<6} {'動物':<14} {'奪冠次數':<10} {'奪冠率':<10}")
    print("-" * 45)
    for rank, (name, wins) in enumerate(ranked_t, 1):
        print(f"{rank:<6} {name:<14} {wins:<10} {wins/n*100:>5.2f}%")


def main():
    output_dir = Path(__file__).parent / "results"

    print("=== 動物大對決模擬器（1 戰定勝負）===\n")

    # 1v1 模擬
    print("--- Part 1: 1v1 兩兩對戰 ---\n")
    h2h_results = run_h2h_simulation(10000)

    # 淘汰賽模擬
    print("--- Part 2: 淘汰賽 ---\n")
    tournament_results = run_tournament_simulation(10000)

    # 印出結果
    print_results(h2h_results, tournament_results)

    # 匯出 CSV
    export_results(h2h_results, tournament_results, output_dir)


if __name__ == "__main__":
    main()
