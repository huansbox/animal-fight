import { shuffleArray } from './utils.js';

/**
 * 建立淘汰賽 bracket
 * @param {Object[]} teamA - A 隊動物
 * @param {Object[]} teamB - B 隊動物
 * @returns {Object} bracket state
 *
 * 配對規則：先 shuffle 各隊順序，然後 A[0] vs B[0], A[1] vs B[1]...
 */
function createBracket(teamA, teamB) {
    const a = shuffleArray([...teamA]);
    const b = shuffleArray([...teamB]);
    const matches = [];
    for (let i = 0; i < a.length; i++) {
        matches.push({ a: a[i], b: b[i], winner: null });
    }
    return {
        rounds: [matches],
        currentRound: 0,
        currentMatch: 0,
    };
}

/**
 * 記錄勝者，推進到下一場/下一輪
 * @param {Object} bracket
 * @param {Object} winner - 勝出的動物物件
 * @returns {Object|null} 下一場配對，或 null = 冠軍產生
 */
function advanceBracket(bracket, winner) {
    const round = bracket.rounds[bracket.currentRound];
    round[bracket.currentMatch].winner = winner;
    bracket.currentMatch++;

    // 本輪打完 → 建立下一輪
    if (bracket.currentMatch >= round.length) {
        const winners = round.map(m => m.winner);
        if (winners.length === 1) return null; // 冠軍！

        const nextRound = [];
        for (let i = 0; i < winners.length; i += 2) {
            nextRound.push({ a: winners[i], b: winners[i + 1], winner: null });
        }
        bracket.rounds.push(nextRound);
        bracket.currentRound++;
        bracket.currentMatch = 0;
    }

    return bracket.rounds[bracket.currentRound][bracket.currentMatch];
}

/** 取得當前要打的配對 */
function getCurrentMatch(bracket) {
    return bracket.rounds[bracket.currentRound][bracket.currentMatch];
}

/** 取得冠軍 */
function getChampion(bracket) {
    const lastRound = bracket.rounds[bracket.rounds.length - 1];
    return lastRound[0]?.winner || null;
}

/**
 * 渲染淘汰賽樹到指定容器
 * @param {Object} bracket
 * @param {HTMLElement} container
 */
function renderBracket(bracket, container) {
    container.innerHTML = '';

    bracket.rounds.forEach((round, ri) => {
        const col = document.createElement('div');
        col.className = 'bracket-round';
        col.dataset.round = ri;

        round.forEach((match, mi) => {
            const matchEl = document.createElement('div');
            matchEl.className = 'bracket-match';
            if (ri === bracket.currentRound && mi === bracket.currentMatch) {
                matchEl.classList.add('current');
            }

            const nameA = match.a?.name || '?';
            const nameB = match.b?.name || '?';
            const winClass = match.winner
                ? (match.winner === match.a ? 'winner-a' : 'winner-b')
                : '';

            matchEl.innerHTML = `
                <span class="bracket-name ${winClass === 'winner-a' ? 'won' : ''}">${nameA}</span>
                <span class="bracket-vs">vs</span>
                <span class="bracket-name ${winClass === 'winner-b' ? 'won' : ''}">${nameB}</span>
            `;
            col.appendChild(matchEl);
        });

        container.appendChild(col);
    });
}

export { createBracket, advanceBracket, getCurrentMatch, getChampion, renderBracket };
