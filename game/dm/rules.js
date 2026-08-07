export const CORE_RULE = Object.freeze({
    baseDice: 2,
    attributeDice: 1,
    keptDice: 2,
    skillBonus: 1,
    generalDc: 7,
    bossDc: 8
});

export const BOSS_FLOW = Object.freeze(["backpack", "initial", "flashlight", "mirror", "reserve"]);

export function dicePoolSize({ attributeFits = false, backpack = false } = {}) {
    return CORE_RULE.baseDice + Number(attributeFits) + Number(backpack);
}

export function keepHighestTwo(dice) {
    if (!Array.isArray(dice) || dice.length < CORE_RULE.keptDice) {
        throw new TypeError("至少需要兩顆骰子");
    }
    if (dice.some((die) => !Number.isInteger(die) || die < 1 || die > 6)) {
        throw new RangeError("骰面必須是 1 到 6 的整數");
    }
    return [...dice].sort((a, b) => b - a).slice(0, CORE_RULE.keptDice);
}

export function checkTotal(dice, { skillFits = false } = {}) {
    const kept = keepHighestTwo(dice);
    const subtotal = kept.reduce((sum, die) => sum + die, 0);
    const bonus = skillFits ? CORE_RULE.skillBonus : 0;
    return { kept, subtotal, bonus, total: subtotal + bonus };
}

export function succeeds(total, dc) {
    if (!Number.isFinite(total) || !Number.isFinite(dc)) {
        throw new TypeError("總分與 DC 必須是數字");
    }
    return total >= dc;
}

export function conditionLabel(condition) {
    return condition.values.join("、");
}
