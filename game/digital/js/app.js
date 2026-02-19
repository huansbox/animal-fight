// game/digital/js/app.js
import { randomAssign, generateDraftOrder, createPool } from './draft.js';
import { createBracket, getCurrentMatch, advanceBracket, getChampion, renderBracketTree } from './bracket.js';
import { aiPick } from './ai.js';
import { rollD6, scoreFromResolved } from './battle.js';
import { animateDiceRoll, animateTrigger, animateScore, animateResult, sleep } from './animations.js';
import { ZONES, getZoneIcon } from './zones.js';

const state = {
    mode: null,
    difficulty: null,
    size: 16,
    draftMode: 'draft',
    animals: [],
    teamA: [],
    teamB: [],
    bracket: null,
    teamMap: null,
    currentMatch: 0,
};

const IMG_BASE = '../../card/images-realistic/';

let allAnimals = [];

const ATTR_NAMES = ['力量', '速度', '攻擊', '防禦', '智慧'];
const ATTR_ICONS = ['💪', '⚡', '⚔️', '🛡️', '🧠'];
const SHORT_ATTR = ['力', '速', '攻', '防', '智'];

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => {
        s.classList.remove('active');
    });
    const target = document.getElementById(id);
    target.classList.add('active');
}

/* ===== 主選單事件 ===== */
function bindMenuEvents() {
    // "VS 電腦" → 顯示難度選擇
    document.getElementById('btn-vs-ai').addEventListener('click', () => {
        document.getElementById('ai-difficulty').classList.remove('hidden');
        document.querySelector('.menu-buttons').classList.add('hidden');
    });

    // AI 難度按鈕
    document.querySelectorAll('#ai-difficulty button').forEach(btn => {
        btn.addEventListener('click', () => {
            state.mode = 'ai';
            state.difficulty = btn.dataset.difficulty;
            showScreen('screen-setup');
        });
    });

    // "雙人對戰" → 直接進設定
    document.getElementById('btn-vs-player').addEventListener('click', () => {
        state.mode = 'player';
        state.difficulty = null;
        showScreen('screen-setup');
    });
}

/* ===== 賽制設定事件 ===== */
function bindSetupEvents() {
    // 賽制規模
    document.querySelectorAll('#size-group button').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#size-group button').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            state.size = parseInt(btn.dataset.size);
        });
    });

    // 選角方式
    document.querySelectorAll('#draft-group button').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#draft-group button').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            state.draftMode = btn.dataset.draft;
        });
    });

    // 開始按鈕
    document.getElementById('btn-start').addEventListener('click', () => {
        startGame();
    });
}

/* ===== 開始遊戲 ===== */
function startGame() {
    if (state.draftMode === 'random') {
        // 快速隨機 — 跳過選角，直接進對戰
        const { teamA, teamB } = randomAssign(allAnimals, state.size);
        state.teamA = teamA;
        state.teamB = teamB;
        state.bracket = createBracket(teamA, teamB);
        state.teamMap = new Map();
        teamA.forEach(a => state.teamMap.set(a.id, 'a'));
        teamB.forEach(a => state.teamMap.set(a.id, 'b'));
        showScreen('screen-battle');
        startBattle();
    } else {
        // 選秀或自選 — 進入選角畫面
        showScreen('screen-draft');
        startDraft();
    }
}

/* ===== 選角畫面 ===== */
function startDraft() {
    const pool = createPool(state.draftMode, allAnimals, state.size);
    const order = generateDraftOrder(state.size);
    const teamA = [];
    const teamB = [];
    let pickIndex = 0;

    const container = document.getElementById('screen-draft');

    let sortMode = 'total'; // 'total' or 'name'
    let searchText = '';
    let activeZone = null; // null = 全部, 'ueno' = 只顯示上野

    function render() {
        const currentTurn = order[pickIndex];
        const isAiTurn = state.mode === 'ai' && currentTurn === 'b';

        container.innerHTML = `
            <div class="draft-header">
                <h2>選角 — ${state.draftMode === 'manual' ? '自選模式' : '選秀模式'}</h2>
                <div class="draft-status">
                    ${pickIndex < order.length
                        ? `<span class="turn-indicator ${currentTurn}">輪到 ${currentTurn === 'a' ? '玩家 A' : (state.mode === 'ai' ? '電腦' : '玩家 B')} 選</span>
                           <span class="pick-count">（第 ${pickIndex + 1}/${order.length} 選）</span>`
                        : '<span class="turn-indicator done">選角完成！</span>'
                    }
                </div>
                ${state.draftMode !== 'random' ? `
                    <div class="draft-controls">
                        ${state.draftMode === 'manual' ? `
                            <input type="text" id="draft-search" placeholder="搜尋動物..." class="draft-search">
                        ` : ''}
                        <div class="sort-buttons">
                            <button id="sort-total" class="sort-btn ${sortMode === 'total' ? 'selected' : ''}">依總和</button>
                            <button id="sort-name" class="sort-btn ${sortMode === 'name' ? 'selected' : ''}">依名稱</button>
                        </div>
                        <div class="zone-filters">
                            ${Object.entries(ZONES).map(([key, z]) => `
                                <button class="zone-btn ${activeZone === key ? 'selected' : ''}" data-zone="${key}">
                                    ${z.icon} ${z.name}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
            <div class="draft-pool" id="draft-pool"></div>
            <div class="draft-teams">
                <div class="draft-team team-a">
                    <h3>${state.mode === 'ai' ? '玩家' : '玩家 A'}（${teamA.length}/${state.size / 2}）</h3>
                    <div class="team-cards" id="team-a-cards"></div>
                </div>
                <div class="draft-team team-b">
                    <h3>${state.mode === 'ai' ? '電腦' : '玩家 B'}（${teamB.length}/${state.size / 2}）</h3>
                    <div class="team-cards" id="team-b-cards"></div>
                </div>
            </div>
            ${pickIndex >= order.length ? '<button id="draft-confirm" class="draft-confirm-btn">確認，開始對戰！</button>' : ''}
        `;

        renderPool();
        renderTeamCards('team-a-cards', teamA);
        renderTeamCards('team-b-cards', teamB);
        bindDraftEvents();

        // AI auto-pick
        if (isAiTurn && pickIndex < order.length) {
            setTimeout(() => {
                const available = pool.filter(a => !teamA.includes(a) && !teamB.includes(a));
                const picked = aiPick(state.difficulty, available, teamB);
                teamB.push(picked);
                pickIndex++;
                render();
            }, 600 + Math.random() * 400);
        }
    }

    function renderPool() {
        const poolEl = document.getElementById('draft-pool');
        const picked = new Set([...teamA, ...teamB]);

        let displayPool = pool.filter(a => !picked.has(a));

        // Zone filter
        if (activeZone && ZONES[activeZone]) {
            displayPool = displayPool.filter(a => ZONES[activeZone].ids.has(a.id));
        }

        // Search filter (manual mode only)
        if (searchText) {
            const q = searchText.toLowerCase();
            displayPool = displayPool.filter(a =>
                a.name.toLowerCase().includes(q) ||
                a.en.toLowerCase().includes(q)
            );
        }

        // Sort
        if (sortMode === 'total') {
            displayPool.sort((a, b) => {
                const ta = a.stats.reduce((s, v) => s + v, 0);
                const tb = b.stats.reduce((s, v) => s + v, 0);
                return tb - ta;
            });
        } else {
            displayPool.sort((a, b) => a.name.localeCompare(b.name, 'zh-TW'));
        }

        poolEl.innerHTML = displayPool.map(a => {
            const total = a.stats.reduce((s, v) => s + v, 0);
            const badge = getZoneIcon(a.id);
            return `
                <div class="mini-card" data-id="${a.id}">
                    ${badge ? `<span class="zone-badge">${badge}</span>` : ''}
                    <img src="${IMG_BASE}${a.img}" alt="${a.name}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 70 70%22><rect fill=%22%23333%22 width=%2270%22 height=%2270%22/><text x=%2235%22 y=%2240%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2212%22>?</text></svg>'">
                    <span class="name">${a.name}</span>
                    <span class="total">${total}</span>
                </div>
            `;
        }).join('');
    }

    function renderTeamCards(containerId, team) {
        const el = document.getElementById(containerId);
        el.innerHTML = team.map(a => `
            <div class="mini-card picked-card">
                <img src="${IMG_BASE}${a.img}" alt="${a.name}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 70 70%22><rect fill=%22%23333%22 width=%2270%22 height=%2270%22/><text x=%2235%22 y=%2240%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2212%22>?</text></svg>'">
                <span class="name">${a.name}</span>
            </div>
        `).join('');
    }

    function bindPoolClicks() {
        const currentTurn = pickIndex < order.length ? order[pickIndex] : null;
        const isHumanTurn = currentTurn && !(state.mode === 'ai' && currentTurn === 'b');

        if (isHumanTurn) {
            document.querySelectorAll('#draft-pool .mini-card').forEach(card => {
                card.addEventListener('click', () => {
                    const animal = pool.find(a => a.id === card.dataset.id);
                    if (!animal) return;

                    if (currentTurn === 'a') teamA.push(animal);
                    else teamB.push(animal);

                    pickIndex++;
                    render();
                });
            });
        }
    }

    function bindDraftEvents() {
        // Pool card clicks
        bindPoolClicks();

        // Search (manual mode)
        const searchInput = document.getElementById('draft-search');
        if (searchInput) {
            searchInput.value = searchText;
            searchInput.addEventListener('input', (e) => {
                searchText = e.target.value;
                renderPool();
                bindPoolClicks();
            });
        }

        // Sort buttons
        const sortTotal = document.getElementById('sort-total');
        const sortName = document.getElementById('sort-name');
        if (sortTotal) {
            sortTotal.addEventListener('click', () => {
                sortMode = 'total';
                sortTotal.classList.add('selected');
                sortName.classList.remove('selected');
                renderPool();
                bindPoolClicks();
            });
        }
        if (sortName) {
            sortName.addEventListener('click', () => {
                sortMode = 'name';
                sortName.classList.add('selected');
                sortTotal.classList.remove('selected');
                renderPool();
                bindPoolClicks();
            });
        }

        // Zone filter buttons
        document.querySelectorAll('.zone-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const zone = btn.dataset.zone;
                activeZone = activeZone === zone ? null : zone;
                document.querySelectorAll('.zone-btn').forEach(b => {
                    b.classList.toggle('selected', b.dataset.zone === activeZone);
                });
                renderPool();
                bindPoolClicks();
            });
        });

        // Confirm button (when draft complete)
        const confirmBtn = document.getElementById('draft-confirm');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', () => {
                state.teamA = teamA;
                state.teamB = teamB;
                state.bracket = createBracket(teamA, teamB);
                state.teamMap = new Map();
                teamA.forEach(a => state.teamMap.set(a.id, 'a'));
                teamB.forEach(a => state.teamMap.set(a.id, 'b'));
                showScreen('screen-battle');
                startBattle();
            });
        }
    }

    render();
}

/* ===== 對戰畫面 ===== */
function startBattle() {
    const container = document.getElementById('screen-battle');
    const SVG_PLACEHOLDER = "data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 200%22><rect fill=%22%23333%22 width=%22200%22 height=%22200%22/><text x=%22100%22 y=%22110%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2240%22>?</text></svg>";

    function label(team) {
        if (team === 'a') return state.mode === 'ai' ? '玩家' : '玩家 A';
        return state.mode === 'ai' ? '電腦' : '玩家 B';
    }

    /** 等待按鈕點擊（回傳 Promise） */
    function waitForClick(btnId) {
        return new Promise(resolve => {
            document.getElementById(btnId).addEventListener('click', resolve, { once: true });
        });
    }

    function renderBattleScreen() {
        const match = getCurrentMatch(state.bracket);
        const roundNum = state.bracket.currentRound + 1;
        const matchNum = state.bracket.currentMatch + 1;
        const totalMatches = state.bracket.rounds[state.bracket.currentRound].length;
        const lt = state.teamMap.get(match.a.id);
        const rt = state.teamMap.get(match.b.id);

        container.innerHTML = `
            <div class="battle-top-bar">
                <div class="round-info">第 ${roundNum} 輪 — 第 ${matchNum}/${totalMatches} 場</div>
                <button class="bracket-toggle-btn" id="btn-bracket">🏆 對戰表</button>
            </div>
            <div class="bt-overlay hidden" id="bracket-overlay">
                <button class="bt-close" id="btn-bt-close">✕</button>
                <div class="bt-tree" id="bt-tree"></div>
                <button class="bt-next hidden" id="btn-bt-next">下一場 →</button>
            </div>
            <div class="battle-area">
                <div class="battle-card card card-flip team-${lt}-card" id="card-a">
                    <div class="team-label team-${lt}-label">${label(lt)}</div>
                    <img src="${IMG_BASE}${match.a.img}" alt="${match.a.name}" onerror="this.src='${SVG_PLACEHOLDER}'">
                    <div class="animal-name">${match.a.name}</div>
                    <div class="animal-en">${match.a.en}</div>
                    <div class="stats">
                        ${match.a.stats.map((v, i) => `
                            <div class="stat" id="stat-a-${i}">
                                <span class="stat-icon">${ATTR_ICONS[i]}</span>
                                <span class="stat-label">${ATTR_NAMES[i]}</span>
                                <span class="stat-value">${v}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="skill-name">${match.a.skillName}</div>
                    <div class="skill-bonus">${match.a.skillBonus.map(b => SHORT_ATTR[b.attr] + '+' + b.val).join('  ')}</div>
                </div>

                <div class="battle-center">
                    <div class="dice-area">
                        <div class="dice-side">
                            <div class="dice-group">
                                <div class="dice dice-${lt}" id="dice-a1">?</div>
                                <div class="dice dice-${lt}" id="dice-a2">?</div>
                            </div>
                            <div class="trigger-counter" id="trigger-a"></div>
                        </div>
                        <div class="vs-text">VS</div>
                        <div class="dice-side">
                            <div class="dice-group">
                                <div class="dice dice-${rt}" id="dice-b1">?</div>
                                <div class="dice dice-${rt}" id="dice-b2">?</div>
                            </div>
                            <div class="trigger-counter" id="trigger-b"></div>
                        </div>
                    </div>
                    <div class="breakdown-area" id="breakdown-area"></div>
                    <div class="score-display">
                        <span class="score score-${lt}-text" id="score-a">-</span>
                        <span class="score-vs">:</span>
                        <span class="score score-${rt}-text" id="score-b">-</span>
                    </div>
                    <div class="result-text" id="result-text"></div>
                    <button class="roll-btn" id="btn-roll">擲骰！</button>
                </div>

                <div class="battle-card card card-flip team-${rt}-card" id="card-b">
                    <div class="team-label team-${rt}-label">${label(rt)}</div>
                    <img src="${IMG_BASE}${match.b.img}" alt="${match.b.name}" onerror="this.src='${SVG_PLACEHOLDER}'">
                    <div class="animal-name">${match.b.name}</div>
                    <div class="animal-en">${match.b.en}</div>
                    <div class="stats">
                        ${match.b.stats.map((v, i) => `
                            <div class="stat" id="stat-b-${i}">
                                <span class="stat-icon">${ATTR_ICONS[i]}</span>
                                <span class="stat-label">${ATTR_NAMES[i]}</span>
                                <span class="stat-value">${v}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="skill-name">${match.b.skillName}</div>
                    <div class="skill-bonus">${match.b.skillBonus.map(b => SHORT_ATTR[b.attr] + '+' + b.val).join('  ')}</div>
                </div>
            </div>
        `;

        document.getElementById('btn-bracket').addEventListener('click', () => {
            const overlay = document.getElementById('bracket-overlay');
            overlay.classList.remove('hidden');
            renderBracketTree(state.bracket, state.teamMap, document.getElementById('bt-tree'));
            document.getElementById('btn-bt-next').classList.add('hidden');
        });
        document.getElementById('btn-bt-close').addEventListener('click', () => {
            document.getElementById('bracket-overlay').classList.add('hidden');
        });

        playFullBattle(match);
    }

    /** 完整對戰流程（含加賽迴圈） */
    async function playFullBattle(match) {
        const lt = state.teamMap.get(match.a.id);
        const rt = state.teamMap.get(match.b.id);
        const leftHuman = state.mode === 'player' || lt === 'a';
        const rightHuman = state.mode === 'player' || rt === 'a';

        let overtime = false;

        while (true) {
            const rollBtn = document.getElementById('btn-roll');
            const diceEls = {
                a1: document.getElementById('dice-a1'),
                a2: document.getElementById('dice-a2'),
                b1: document.getElementById('dice-b1'),
                b2: document.getElementById('dice-b2'),
            };
            const dice = { a1: 0, a2: 0, b1: 0, b2: 0 };
            const triggers = { a1: 0, a2: 0, b1: 0, b2: 0 };

            /** 擲一側骰子 + 處理所有 6 */
            async function rollSide(side, interactive) {
                const keys = side === 'a' ? ['a1', 'a2'] : ['b1', 'b2'];
                const triggerId = `trigger-${side}`;
                for (const k of keys) dice[k] = rollD6();
                await Promise.all(keys.map((k, i) =>
                    animateDiceRoll(diceEls[k], dice[k], 600 + i * 100)));

                while (keys.some(k => dice[k] === 6)) {
                    const sixKeys = keys.filter(k => dice[k] === 6);
                    for (const k of sixKeys) triggers[k]++;
                    for (const k of sixKeys) await animateTrigger(diceEls[k]);

                    const trig = keys.reduce((sum, k) => sum + triggers[k], 0);
                    document.getElementById(triggerId).textContent =
                        trig > 0 ? `天賦 x${trig}` : '';

                    if (interactive) {
                        rollBtn.textContent = '重骰！';
                        rollBtn.classList.remove('hidden');
                        rollBtn.disabled = false;
                        await waitForClick('btn-roll');
                        rollBtn.disabled = true;
                        rollBtn.classList.add('hidden');
                    } else {
                        await sleep(600);
                    }

                    for (const k of sixKeys) dice[k] = rollD6();
                    await Promise.all(
                        sixKeys.map(k => animateDiceRoll(diceEls[k], dice[k], 500)));
                }
            }

            if (overtime) {
                document.getElementById('result-text').textContent = '平手！加賽！';
                await sleep(1000);
                resetRoundDisplay();
                document.getElementById('result-text').textContent = '';
            }

            // === 左側擲骰 ===
            rollBtn.textContent = `${label(lt)} 擲骰！`;
            rollBtn.classList.remove('hidden');
            rollBtn.disabled = false;
            await waitForClick('btn-roll');
            rollBtn.disabled = true;
            rollBtn.classList.add('hidden');
            await rollSide('a', leftHuman);

            // === 右側擲骰 ===
            if (rightHuman) {
                rollBtn.textContent = `${label(rt)} 擲骰！`;
                rollBtn.classList.remove('hidden');
                rollBtn.disabled = false;
                await waitForClick('btn-roll');
                rollBtn.disabled = true;
                rollBtn.classList.add('hidden');
                await rollSide('b', true);
            } else {
                await sleep(500);
                await rollSide('b', false);
            }

            // === 分數拆解 ===
            const totalTriggersA = triggers.a1 + triggers.a2;
            const totalTriggersB = triggers.b1 + triggers.b2;
            const resA = scoreFromResolved(match.a, dice.a1, dice.a2, totalTriggersA);
            const resB = scoreFromResolved(match.b, dice.b1, dice.b2, totalTriggersB);

            await showScoreBreakdown('a', match.a, dice.a1, dice.a2, resA, totalTriggersA, diceEls);
            await sleep(400);
            await showScoreBreakdown('b', match.b, dice.b1, dice.b2, resB, totalTriggersB, diceEls);
            await sleep(600);

            if (resA.score === resB.score) {
                overtime = true;
                continue;
            }

            // 勝負宣告
            const winner = resA.score > resB.score ? match.a : match.b;
            const winSide = resA.score > resB.score ? 'a' : 'b';

            const resultText = document.getElementById('result-text');
            resultText.textContent = `${winner.name} 勝利！`;
            resultText.style.color = 'gold';

            const cardA = document.getElementById('card-a');
            const cardB = document.getElementById('card-b');
            await animateResult(winSide === 'a' ? cardA : cardB, winSide === 'a' ? cardB : cardA);
            await sleep(1500);

            // 記錄分數到 match，供 bracket 顯示
            const curMatch = getCurrentMatch(state.bracket);
            curMatch.scoreA = resA.score;
            curMatch.scoreB = resB.score;

            // 推進淘汰賽 + 顯示對戰表 overlay
            const nextMatch = advanceBracket(state.bracket, winner);
            const overlay = document.getElementById('bracket-overlay');
            overlay.classList.remove('hidden');
            renderBracketTree(state.bracket, state.teamMap, document.getElementById('bt-tree'));

            const btNextBtn = document.getElementById('btn-bt-next');
            btNextBtn.textContent = nextMatch === null ? '👑 查看冠軍' : '下一場 →';
            btNextBtn.classList.remove('hidden');
            await waitForClick('btn-bt-next');

            if (nextMatch === null) {
                showScreen('screen-champion');
                showChampion(winner);
            } else {
                renderBattleScreen();
            }
            return;
        }
    }

    /** 顯示單方分數拆解 */
    async function showScoreBreakdown(side, animal, d1, d2, res, totalTriggers, diceEls) {
        const dk1 = side + '1';
        const dk2 = side + '2';

        // 骰子顯示屬性名稱
        function showDiceAttr(el, val) {
            el.classList.add('show-attr');
            el.innerHTML = `<span style="font-size:28px;font-weight:900">${val}</span><span>${ATTR_NAMES[val - 1]}</span>`;
        }
        showDiceAttr(diceEls[dk1], d1);
        showDiceAttr(diceEls[dk2], d2);

        // 高亮對應的屬性列
        const statEl1 = document.getElementById(`stat-${side}-${res.attr1}`);
        const statEl2 = document.getElementById(`stat-${side}-${res.attr2}`);
        if (statEl1) statEl1.classList.add('stat-highlight');
        if (statEl2) statEl2.classList.add('stat-highlight');

        await sleep(600);

        // 計算各屬性的天賦加成
        let bonus1 = 0, bonus2 = 0;
        if (totalTriggers > 0) {
            for (const b of animal.skillBonus) {
                if (b.attr === res.attr1) bonus1 += b.val;
                if (b.attr === res.attr2 && !res.doubled) bonus2 += b.val;
            }
        }

        function attrPart(name, val, bonusVal) {
            if (bonusVal > 0 && totalTriggers > 0)
                return `${name} ${val} <span class="breakdown-bonus">+(${bonusVal}\u00d7${totalTriggers})</span>`;
            return `${name} ${val}`;
        }

        const part1 = attrPart(ATTR_NAMES[res.attr1], res.val1, bonus1);
        const part2 = attrPart(ATTR_NAMES[res.attr2], res.val2, bonus2);

        const team = state.teamMap.get(animal.id);
        const breakdownArea = document.getElementById('breakdown-area');
        const lbl = label(team);
        const colorClass = `breakdown-${team}`;
        const line = document.createElement('div');
        line.className = `breakdown-line ${colorClass}`;
        line.innerHTML = `<span class="breakdown-label">${lbl}</span> ${part1} + ${part2} = ${res.score}`;
        breakdownArea.appendChild(line);
        await sleep(800);

        // 顯示該方總分
        await animateScore(document.getElementById(`score-${side}`), res.score);
    }

    /** 重置回合顯示（加賽用） */
    function resetRoundDisplay() {
        document.querySelectorAll('.dice').forEach(d => {
            d.textContent = '?';
            d.classList.remove('show-attr', 'trigger');
            d.innerHTML = '?';
        });
        document.getElementById('score-a').textContent = '-';
        document.getElementById('score-b').textContent = '-';
        document.getElementById('trigger-a').textContent = '';
        document.getElementById('trigger-b').textContent = '';
        document.getElementById('breakdown-area').innerHTML = '';
        document.querySelectorAll('.stat-highlight').forEach(el => el.classList.remove('stat-highlight'));
    }

    renderBattleScreen();
}

/* ===== 冠軍畫面 ===== */
function showChampion(champion) {
    const container = document.getElementById('screen-champion');
    const totalRounds = state.bracket.rounds.length;
    const total = champion.stats.reduce((s, v) => s + v, 0);

    container.innerHTML = `
        <div class="champion-content">
            <h1 class="champion-title">冠軍！</h1>
            <div class="champion-card">
                <img src="${IMG_BASE}${champion.img}" class="champion-img" alt="${champion.name}"
                     onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 200%22><rect fill=%22%23333%22 width=%22200%22 height=%22200%22/><text x=%22100%22 y=%22110%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2240%22>?</text></svg>'">
                <h2 class="champion-name">${champion.name}</h2>
                <div class="champion-en">${champion.en}</div>
                <div class="champion-stats">
                    ${champion.stats.map((v, i) => `
                        <div class="champion-stat">
                            <span>${ATTR_ICONS[i]}</span>
                            <span>${ATTR_NAMES[i]}</span>
                            <span class="champion-stat-value">${v}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="champion-total">總和 ${total}</div>
                <div class="champion-skill">${champion.skillName}</div>
                <div class="champion-skill-desc">${champion.skillDesc}</div>
            </div>
            <div class="champion-record">${totalRounds} 輪全勝</div>
            <div class="champion-buttons">
                <button id="btn-rematch" class="champion-btn rematch-btn">再來一局</button>
                <button id="btn-home" class="champion-btn home-btn">回主選單</button>
            </div>
        </div>
    `;

    // Rematch — keep mode/difficulty/size/draftMode, reset teams and bracket
    document.getElementById('btn-rematch').addEventListener('click', () => {
        state.teamA = [];
        state.teamB = [];
        state.bracket = null;
        state.teamMap = null;
        state.currentMatch = 0;
        showScreen('screen-setup');
    });

    // Home — full reset
    document.getElementById('btn-home').addEventListener('click', () => {
        state.mode = null;
        state.difficulty = null;
        state.size = 16;
        state.draftMode = 'draft';
        state.teamA = [];
        state.teamB = [];
        state.bracket = null;
        state.teamMap = null;
        state.currentMatch = 0;
        // Reset menu UI state
        document.querySelector('.menu-buttons').classList.remove('hidden');
        document.getElementById('ai-difficulty').classList.add('hidden');
        // Reset setup defaults
        document.querySelectorAll('#size-group button').forEach(b => {
            b.classList.toggle('selected', b.dataset.size === '16');
        });
        document.querySelectorAll('#draft-group button').forEach(b => {
            b.classList.toggle('selected', b.dataset.draft === 'draft');
        });
        showScreen('screen-menu');
    });
}

/* ===== 初始化 ===== */
async function init() {
    const res = await fetch('data/animals.json');
    allAnimals = await res.json();
    state.animals = allAnimals;
    console.log(`Loaded ${allAnimals.length} animals`);
    bindMenuEvents();
    bindSetupEvents();
    showScreen('screen-menu');
}

export { state, allAnimals, IMG_BASE, showScreen };

init();
