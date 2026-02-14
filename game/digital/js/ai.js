/**
 * AI 從可選池中挑一隻
 * @param {'easy'|'normal'|'hard'} difficulty
 * @param {Object[]} available - 可選動物
 * @param {Object[]} myTeam - AI 已選的動物（用於 hard 模式）
 * @returns {Object} 選中的動物
 */
function aiPick(difficulty, available, myTeam) {
    if (difficulty === 'easy') {
        return available[Math.floor(Math.random() * available.length)];
    }

    const withTotal = available.map(a => ({
        animal: a,
        total: a.stats.reduce((s, v) => s + v, 0),
    }));
    withTotal.sort((a, b) => b.total - a.total);

    if (difficulty === 'normal') {
        const topHalf = withTotal.slice(0, Math.max(1, Math.ceil(withTotal.length / 2)));
        return topHalf[Math.floor(Math.random() * topHalf.length)].animal;
    }

    // hard: 貪心 — 選總和最高的
    return withTotal[0].animal;
}

export { aiPick };
