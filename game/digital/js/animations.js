/** sleep helper */
function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

/** 骰子滾動動畫（視覺假骰，最終顯示真實值） */
async function animateDiceRoll(diceEl, finalValue, duration = 800) {
    diceEl.classList.add('rolling');
    const interval = 80;
    const steps = Math.floor(duration / interval);

    for (let i = 0; i < steps; i++) {
        diceEl.textContent = Math.floor(Math.random() * 6) + 1;
        await sleep(interval);
    }
    diceEl.classList.remove('rolling');
    diceEl.textContent = finalValue;
}

/** 天賦觸發特效 */
async function animateTrigger(diceEl) {
    diceEl.classList.add('trigger');
    diceEl.textContent = '6';
    await sleep(600);
    diceEl.classList.remove('trigger');
}

/** 分數顯示動畫 */
async function animateScore(el, score) {
    el.textContent = score;
    el.classList.add('score-pop');
    await sleep(400);
    el.classList.remove('score-pop');
}

/** 勝負結果動畫 */
async function animateResult(winnerCard, loserCard) {
    winnerCard.classList.add('winner');
    loserCard.classList.add('loser');
}

export { sleep, animateDiceRoll, animateTrigger, animateScore, animateResult };
