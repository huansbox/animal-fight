import { shuffleArray } from './utils.js';

/**
 * 快速隨機：從全部動物中隨機抽 N 隻，平分給雙方
 */
function randomAssign(animals, totalSize) {
    const pool = shuffleArray([...animals]).slice(0, totalSize);
    const half = totalSize / 2;
    return {
        teamA: pool.slice(0, half),
        teamB: pool.slice(half),
    };
}

/**
 * 產生 Snake Draft 順序
 * A 先選 1，之後 B2-A2-B2-A2...
 * @param {number} total - 總選秀數
 * @returns {string[]} - ['a','b','b','a','a','b','b','a',...]
 */
function generateDraftOrder(total) {
    const order = ['a'];
    let remaining = total - 1;
    let turn = 'b';
    while (remaining > 0) {
        const picks = Math.min(2, remaining);
        for (let i = 0; i < picks; i++) order.push(turn);
        remaining -= picks;
        turn = turn === 'a' ? 'b' : 'a';
    }
    return order;
}

/**
 * 產生選秀用的動物池
 * @param {'draft'|'manual'} mode
 * @param {Object[]} allAnimals - 全部 106 隻
 * @param {number} totalSize - 要選的總數
 */
function createPool(mode, allAnimals, totalSize) {
    if (mode === 'manual') return [...allAnimals];
    return shuffleArray([...allAnimals]).slice(0, totalSize);
}

export { randomAssign, generateDraftOrder, createPool };
