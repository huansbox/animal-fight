// battle.js — 對戰引擎（純邏輯，無 DOM）
// 移植自 sim/battle_sim_v5.py lines 97-161

/** 擲一顆 d6 */
function rollD6() {
    return Math.floor(Math.random() * 6) + 1;
}

/**
 * 解析單顆骰子：骰到 6 就重骰，直到得到 1-5
 * @param {number} d - 骰面原始值 (1-6)
 * @returns {{ final: number, triggers: number }}
 *   final: 最終骰面 (1-5)
 *   triggers: 骰到 6 的次數（天賦觸發次數）
 */
function resolveDie(d) {
    let triggers = 0;
    while (d === 6 && triggers < 100) {
        triggers++;
        d = rollD6();
    }
    if (d === 6) d = 5; // 安全閥：100 次重骰後仍為 6 則視為 5
    return { final: d, triggers };
}

/**
 * 計算單方分數
 * @param {Object} animal - { stats: [力量, 速度, 攻擊, 防禦, 智慧], skillBonus: [{attr, val}] }
 *   stats: 五維數值陣列，index 0-4 對應骰面 1-5
 *   skillBonus: 天賦加成陣列，attr 為 stats index (0-4)，val 為加成值
 * @param {number} d1 - 第一顆骰子原始值
 * @param {number} d2 - 第二顆骰子原始值
 * @returns {{ score: number, details: Object }}
 *   details 包含完整骰子解析與加分明細，供動畫系統重播用
 */
function calculateScore(animal, d1, d2) {
    const r1 = resolveDie(d1);
    const r2 = resolveDie(d2);
    const totalTriggers = r1.triggers + r2.triggers;

    // 骰面 1-5 對應 stats index 0-4
    const attr1 = r1.final - 1;
    const attr2 = r2.final - 1;

    // 基礎分：骰面相同則該屬性 ×2，否則兩屬性相加
    let baseScore;
    if (r1.final === r2.final) {
        baseScore = animal.stats[attr1] * 2;
    } else {
        baseScore = animal.stats[attr1] + animal.stats[attr2];
    }

    // 天賦加分：每次觸發 → 檢查最終骰面命中的加成屬性 → 加總命中的 bonus
    let bonusPerTrigger = 0;
    if (totalTriggers > 0) {
        const hitAttrs = [attr1, attr2];
        for (const b of animal.skillBonus) {
            if (hitAttrs.includes(b.attr)) {
                bonusPerTrigger += b.val;
            }
        }
    }
    const totalBonus = totalTriggers * bonusPerTrigger;

    return {
        score: baseScore + totalBonus,
        details: {
            d1Raw: d1,
            d2Raw: d2,
            d1Final: r1.final,
            d2Final: r2.final,
            d1Triggers: r1.triggers,
            d2Triggers: r2.triggers,
            totalTriggers,
            baseScore,
            bonusPerTrigger,
            totalBonus,
        },
    };
}

/**
 * 執行一場對戰（含加賽）
 * @param {Object} animalA - 動物 A 資料
 * @param {Object} animalB - 動物 B 資料
 * @returns {{ winner: 'a'|'b', scoreA: number, scoreB: number,
 *             detailsA: Object, detailsB: Object, rounds: Array }}
 *   rounds: 所有回合紀錄（含加賽），每回合含雙方 resultA/resultB
 */
function fightMatch(animalA, animalB) {
    const rounds = [];
    while (true) {
        const d1A = rollD6(), d2A = rollD6();
        const d1B = rollD6(), d2B = rollD6();
        const resultA = calculateScore(animalA, d1A, d2A);
        const resultB = calculateScore(animalB, d1B, d2B);
        rounds.push({ resultA, resultB });

        if (resultA.score !== resultB.score) {
            return {
                winner: resultA.score > resultB.score ? 'a' : 'b',
                scoreA: resultA.score,
                scoreB: resultB.score,
                detailsA: resultA.details,
                detailsB: resultB.details,
                rounds,
            };
        }
        // 平手 → 自動加賽（迴圈繼續）
    }
}

export { rollD6, resolveDie, calculateScore, fightMatch };
