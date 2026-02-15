import { shuffleArray } from './utils.js';

/**
 * 建立淘汰賽 bracket
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
 * @returns {Object|null} 下一場配對，或 null = 冠軍產生
 */
function advanceBracket(bracket, winner) {
    const round = bracket.rounds[bracket.currentRound];
    round[bracket.currentMatch].winner = winner;
    bracket.currentMatch++;

    if (bracket.currentMatch >= round.length) {
        const winners = round.map(m => m.winner);
        if (winners.length === 1) return null;

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

function getCurrentMatch(bracket) {
    return bracket.rounds[bracket.currentRound][bracket.currentMatch];
}

function getChampion(bracket) {
    const lastRound = bracket.rounds[bracket.rounds.length - 1];
    return lastRound[0]?.winner || null;
}

/**
 * 渲染淘汰賽樹（由下往上，含隊伍色標示）
 * @param {Object} bracket
 * @param {Map} teamMap - animal ID → 'a' | 'b'
 * @param {HTMLElement} container
 */
function renderBracketTree(bracket, teamMap, container) {
    const firstRoundLen = bracket.rounds[0].length;
    const totalRounds = Math.ceil(Math.log2(firstRoundLen)) + 1;

    const allRounds = [];
    for (let r = 0; r < totalRounds; r++) {
        const expected = firstRoundLen / Math.pow(2, r);
        allRounds.push(
            bracket.rounds[r] ||
            Array.from({ length: expected }, () => ({ a: null, b: null, winner: null }))
        );
    }

    const ROUND_NAMES = { 1: '冠軍賽', 2: '四強', 4: '八強', 8: '十六強', 16: '三十二強' };

    function slot(match, side) {
        const animal = match[side];
        if (!animal) return '<div class="bt-slot bt-pending">?</div>';
        const team = teamMap ? teamMap.get(animal.id) : null;
        const won = match.winner === animal;
        const lost = match.winner && match.winner !== animal;
        let cls = 'bt-slot';
        if (won) cls += ' bt-won';
        if (lost) cls += ' bt-lost';
        const dot = team ? `<span class="bt-dot bt-dot-${team}"></span>` : '';
        const scoreKey = side === 'a' ? 'scoreA' : 'scoreB';
        const score = match[scoreKey] != null ? `<span class="bt-score">${match[scoreKey]}</span>` : '';
        return `<div class="${cls}">${dot}<span class="bt-name">${animal.name}</span>${score}</div>`;
    }

    let html = '';

    for (let r = 0; r < totalRounds; r++) {
        const round = allRounds[r];
        const roundName = ROUND_NAMES[round.length] || `第 ${r + 1} 輪`;

        html += '<div class="bt-col">';
        html += `<div class="bt-col-lbl">${roundName}</div>`;
        html += '<div class="bt-col-body">';
        round.forEach((match, mi) => {
            const isCurrent = r === bracket.currentRound
                && mi === bracket.currentMatch && !match.winner;
            html += '<div class="bt-mw">';
            html += `<div class="bt-match${isCurrent ? ' bt-current' : ''}">`;
            html += slot(match, 'a');
            html += slot(match, 'b');
            html += '</div></div>';
        });
        html += '</div></div>';

        if (r < totalRounds - 1) {
            const pairs = round.length / 2;
            html += '<div class="bt-conn-col">';
            html += '<div class="bt-col-lbl">&nbsp;</div>';
            for (let p = 0; p < pairs; p++) {
                html += '<div class="bt-bracket-line"></div>';
            }
            html += '</div>';
        }
    }

    html += '<div class="bt-trophy">🏆</div>';

    container.innerHTML = html;
}

export { createBracket, advanceBracket, getCurrentMatch, getChampion, renderBracketTree };
