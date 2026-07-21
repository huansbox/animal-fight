import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const source = await readFile(new URL('./battle.js', import.meta.url), 'utf8');
const moduleUrl = `data:text/javascript;base64,${Buffer.from(source).toString('base64')}`;
const { scoreFromResolved } = await import(moduleUrl);

const honeyBadger = {
    stats: [5, 4, 6, 7, 6],
    skillBonus: [
        { attr: 3, val: 3 },
        { attr: 4, val: 1 },
    ],
};

assert.equal(
    scoreFromResolved(honeyBadger, 4, 4, 1).score,
    20,
    '相同骰面應逐顆計算防禦 +3',
);
assert.equal(
    scoreFromResolved(honeyBadger, 4, 4, 3).score,
    32,
    '多次天賦觸發應疊加兩顆骰子的命中加成',
);
assert.equal(
    scoreFromResolved(honeyBadger, 4, 5, 2).score,
    21,
    '不同骰面應分別計算防禦 +3 與智慧 +1',
);
assert.equal(
    scoreFromResolved(honeyBadger, 2, 4, 1).score,
    14,
    '只有命中 skillBonus 的骰子才加分',
);
assert.equal(
    scoreFromResolved(honeyBadger, 4, 4, 0).score,
    14,
    '沒有骰到 6 時不應套用天賦加分',
);

console.log('battle scoring tests passed');
