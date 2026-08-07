import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

import { BOSS_FLOW, CORE_RULE, checkTotal, conditionLabel, dicePoolSize, keepHighestTwo, succeeds } from "./rules.js";
import { scenario } from "./scenarios.js";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "../..");

test("v0.9 核心骰池與取高二正確", () => {
    assert.equal(dicePoolSize(), 2);
    assert.equal(dicePoolSize({ attributeFits: true }), 3);
    assert.equal(dicePoolSize({ attributeFits: true, backpack: true }), 4);
    assert.deepEqual(keepHighestTwo([2, 6, 4, 1]), [6, 4]);
    assert.deepEqual(checkTotal([2, 6, 4], { skillFits: true }), {
        kept: [6, 4],
        subtotal: 10,
        bonus: 1,
        total: 11
    });
    assert.equal(succeeds(7, CORE_RULE.generalDc), true);
    assert.equal(succeeds(7, CORE_RULE.bossDc), false);
    assert.doesNotMatch(scenario.setup.join(""), /取最大的 2 顆/);
    assert.match(scenario.steps.find((step) => step.id === "road").rules.join(""), /3d6，取最大的 2 顆/);
});

test("六個正式位置各有兩條單向門檻基準與固定 DC", () => {
    const checks = scenario.steps.flatMap((step) => step.checks ?? []);
    assert.deepEqual(checks.map((check) => check.id), ["1", "2A", "2B", "3", "4A", "4B"]);
    assert.deepEqual(checks.map((check) => check.dc), [7, 7, 7, 7, 8, 8]);
    checks.forEach((check) => {
        assert.equal(check.routes.length, 2);
        check.routes.forEach((route) => {
            assert.match(route.condition.operator, /^(gte|lte)$/);
            assert.ok([3, 4, 7].includes(route.condition.value));
            assert.ok(route.condition.values.length >= 3);
            assert.equal(conditionLabel(route.condition), route.condition.values.join("、"));
        });
    });
});

test("Boss 寶物與後援順序固定", () => {
    const boss = scenario.steps.find((step) => step.id === "boss");
    assert.deepEqual(boss.treasures.map((item) => item.id), BOSS_FLOW);
    assert.deepEqual(boss.treasures.map((item) => item.order), [1, 2, 3, 4, 5]);
    assert.match(boss.treasures.find((item) => item.id === "mirror").action, /不能再後援/);
    assert.match(boss.treasures.find((item) => item.id === "flashlight").action, /總分 ＋1/);
    assert.match(boss.treasures.find((item) => item.id === "initial").action, /第一次檢定骰池.*背包目標/);
});

test("一般任務保留兩次後援與三區移動規則", () => {
    const road = scenario.steps.find((step) => step.id === "road");
    const bridge = scenario.steps.find((step) => step.id === "bridge");
    const medicine = scenario.steps.find((step) => step.id === "medicine");
    assert.match(road.rules.join(""), /全隊共用 2 次/);
    assert.match(road.rules.join(""), /第二次出場後不論結果都進休息區/);
    assert.match(bridge.rules.join(""), /兩邊都失敗時.*不消耗標記/);
    [road, bridge, medicine].forEach((step) => {
        assert.match([...step.rules, ...step.outcomes.map((outcome) => outcome.text)].join(""), /後援動物依出場次數移區/);
    });
});

test("無效骰面會被拒絕", () => {
    assert.throws(() => keepHighestTwo([6]), /至少需要兩顆/);
    assert.throws(() => keepHighestTwo([0, 6]), /1 到 6/);
    assert.throws(() => succeeds("7", 7), /必須是數字/);
});

test("Web storage 與正式實體來源已切到 v0.9", () => {
    const app = readFileSync(resolve(here, "app.js"), "utf8");
    const index = readFileSync(resolve(here, "index.html"), "utf8");
    const statusCards = readFileSync(resolve(root, "card/team-mission-status-cards-quarter-label.html"), "utf8");
    const revealCards = readFileSync(resolve(root, "card/storm-forest-rescue-reveal-cards-half-label.html"), "utf8");
    const revealData = revealCards.slice(revealCards.lastIndexOf("<script>"));

    assert.match(app, /animalFight\.dm\.active\.v3/);
    assert.match(app, /animalFight\.dm\.records\.v3/);
    assert.doesNotMatch(app, /animalFight\.dm\.(active|records)\.v2/);
    assert.match(index, /團隊任務 v0\.9/);
    assert.match(app, /v\$\{scenario\.version\}｜\$\{step\.label\}/);
    const dmPanelStart = index.indexOf('<details class="dm-panel"');
    const bossTools = index.indexOf('id="boss-tools"');
    const dmPanelEnd = index.indexOf("</details>", dmPanelStart);
    assert.ok(dmPanelStart >= 0 && bossTools > dmPanelStart && bossTools < dmPanelEnd);
    assert.match(statusCards, /該位置<br>總分 ＋1/);
    assert.match(statusCards, /這個位置不能後援/);
    assert.doesNotMatch(statusCards, /降低 [123] 級|最大－最小|＋3 顆/);
    assert.doesNotMatch(revealData, /attrs:|range:|7、8、9|4、5、6|1、2、3/);
});
