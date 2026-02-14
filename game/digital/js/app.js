// game/digital/js/app.js
import { randomAssign, generateDraftOrder, createPool } from './draft.js';
import { createBracket, getCurrentMatch, advanceBracket, getChampion, renderBracket } from './bracket.js';
import { aiPick } from './ai.js';
import { fightMatch } from './battle.js';
import { animateDiceRoll, animateTrigger, animateScore, animateResult, sleep } from './animations.js';

const state = {
    mode: null,
    difficulty: null,
    size: 16,
    draftMode: 'draft',
    animals: [],
    teamA: [],
    teamB: [],
    bracket: null,
    currentMatch: 0,
};

const IMG_BASE = '../../card/images/';

let allAnimals = [];

const ATTR_NAMES = ['力量', '速度', '攻擊', '防禦', '智慧'];
const ATTR_ICONS = ['💪', '⚡', '⚔️', '🛡️', '🧠'];

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
                ${state.draftMode === 'manual' ? `
                    <div class="draft-controls">
                        <input type="text" id="draft-search" placeholder="搜尋動物..." class="draft-search">
                        <div class="sort-buttons">
                            <button id="sort-total" class="sort-btn ${sortMode === 'total' ? 'selected' : ''}">依總和</button>
                            <button id="sort-name" class="sort-btn ${sortMode === 'name' ? 'selected' : ''}">依名稱</button>
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
            return `
                <div class="mini-card" data-id="${a.id}">
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

        // Confirm button (when draft complete)
        const confirmBtn = document.getElementById('draft-confirm');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', () => {
                state.teamA = teamA;
                state.teamB = teamB;
                state.bracket = createBracket(teamA, teamB);
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

    function renderBattleScreen() {
        const match = getCurrentMatch(state.bracket);
        const roundNum = state.bracket.currentRound + 1;
        const matchNum = state.bracket.currentMatch + 1;
        const totalMatches = state.bracket.rounds[state.bracket.currentRound].length;

        container.innerHTML = `
            <div class="bracket-container" id="bracket-display"></div>
            <div class="round-info">第 ${roundNum} 輪 — 第 ${matchNum}/${totalMatches} 場</div>
            <div class="battle-area">
                <div class="battle-card card card-flip" id="card-a">
                    <img src="${IMG_BASE}${match.a.img}" alt="${match.a.name}"
                         onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 200%22><rect fill=%22%23333%22 width=%22200%22 height=%22200%22/><text x=%22100%22 y=%22110%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2240%22>?</text></svg>'">
                    <div class="animal-name">${match.a.name}</div>
                    <div class="animal-en">${match.a.en}</div>
                    <div class="stats">
                        ${match.a.stats.map((v, i) => `
                            <div class="stat">
                                <span class="stat-icon">${ATTR_ICONS[i]}</span>
                                <span class="stat-label">${ATTR_NAMES[i]}</span>
                                <span class="stat-value">${v}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="skill-name">${match.a.skillName}</div>
                </div>

                <div class="battle-center">
                    <div class="dice-area">
                        <div class="dice-group">
                            <div class="dice" id="dice-a1">?</div>
                            <div class="dice" id="dice-a2">?</div>
                        </div>
                        <div class="vs-text">VS</div>
                        <div class="dice-group">
                            <div class="dice" id="dice-b1">?</div>
                            <div class="dice" id="dice-b2">?</div>
                        </div>
                    </div>
                    <div class="score-display">
                        <span class="score" id="score-a">-</span>
                        <span class="score-vs">:</span>
                        <span class="score" id="score-b">-</span>
                    </div>
                    <div class="result-text" id="result-text"></div>
                    <button class="roll-btn" id="btn-roll">擲骰！</button>
                    <button class="next-btn hidden" id="btn-next">下一場</button>
                </div>

                <div class="battle-card card card-flip" id="card-b">
                    <img src="${IMG_BASE}${match.b.img}" alt="${match.b.name}"
                         onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 200%22><rect fill=%22%23333%22 width=%22200%22 height=%22200%22/><text x=%22100%22 y=%22110%22 text-anchor=%22middle%22 fill=%22%23888%22 font-size=%2240%22>?</text></svg>'">
                    <div class="animal-name">${match.b.name}</div>
                    <div class="animal-en">${match.b.en}</div>
                    <div class="stats">
                        ${match.b.stats.map((v, i) => `
                            <div class="stat">
                                <span class="stat-icon">${ATTR_ICONS[i]}</span>
                                <span class="stat-label">${ATTR_NAMES[i]}</span>
                                <span class="stat-value">${v}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="skill-name">${match.b.skillName}</div>
                </div>
            </div>
        `;

        // 渲染淘汰賽樹
        renderBracket(state.bracket, document.getElementById('bracket-display'));

        // 綁定擲骰按鈕
        document.getElementById('btn-roll').addEventListener('click', async () => {
            const rollBtn = document.getElementById('btn-roll');
            rollBtn.disabled = true;
            rollBtn.classList.add('hidden');

            await playBattleAnimation(match);
        });
    }

    async function playBattleAnimation(match) {
        // 預先計算對戰結果
        const result = fightMatch(match.a, match.b);

        // 播放每一回合（含加賽）
        for (let i = 0; i < result.rounds.length; i++) {
            const round = result.rounds[i];

            if (i > 0) {
                // 加賽提示
                document.getElementById('result-text').textContent = '平手！加賽！';
                document.getElementById('score-a').textContent = '-';
                document.getElementById('score-b').textContent = '-';
                document.querySelectorAll('.dice').forEach(d => {
                    d.textContent = '?';
                    d.classList.remove('show-attr');
                });
                await sleep(1200);
                document.getElementById('result-text').textContent = '';
            }

            const detA = round.resultA.details;
            const detB = round.resultB.details;

            // 取得骰子 DOM 元素
            const diceA1 = document.getElementById('dice-a1');
            const diceA2 = document.getElementById('dice-a2');
            const diceB1 = document.getElementById('dice-b1');
            const diceB2 = document.getElementById('dice-b2');

            // 四顆骰子同時滾動（略有時差）
            await Promise.all([
                animateDiceRoll(diceA1, detA.d1Raw === 6 ? 6 : detA.d1Final, 600),
                animateDiceRoll(diceA2, detA.d2Raw === 6 ? 6 : detA.d2Final, 700),
                animateDiceRoll(diceB1, detB.d1Raw === 6 ? 6 : detB.d1Final, 650),
                animateDiceRoll(diceB2, detB.d2Raw === 6 ? 6 : detB.d2Final, 750),
            ]);

            // 處理天賦觸發（支援連續骰 6）
            async function playTriggers(diceEl, triggers, finalVal) {
                for (let t = 0; t < triggers; t++) {
                    await animateTrigger(diceEl);
                    if (t < triggers - 1) {
                        // 中間的重骰：顯示再次骰到 6
                        await animateDiceRoll(diceEl, 6, 400);
                    } else {
                        // 最後一次：顯示最終值
                        await animateDiceRoll(diceEl, finalVal, 500);
                    }
                }
            }
            await Promise.all([
                detA.d1Triggers > 0 ? playTriggers(diceA1, detA.d1Triggers, detA.d1Final) : Promise.resolve(),
                detA.d2Triggers > 0 ? playTriggers(diceA2, detA.d2Triggers, detA.d2Final) : Promise.resolve(),
                detB.d1Triggers > 0 ? playTriggers(diceB1, detB.d1Triggers, detB.d1Final) : Promise.resolve(),
                detB.d2Triggers > 0 ? playTriggers(diceB2, detB.d2Triggers, detB.d2Final) : Promise.resolve(),
            ]);

            await sleep(300);

            // 顯示骰面對應的屬性名稱
            function showDiceAttr(diceEl, val) {
                diceEl.classList.add('show-attr');
                diceEl.innerHTML = `<span style="font-size:28px;font-weight:900">${val}</span><span>${ATTR_NAMES[val - 1]}</span>`;
            }
            showDiceAttr(diceA1, detA.d1Final);
            showDiceAttr(diceA2, detA.d2Final);
            showDiceAttr(diceB1, detB.d1Final);
            showDiceAttr(diceB2, detB.d2Final);

            await sleep(500);

            // 顯示分數
            await Promise.all([
                animateScore(document.getElementById('score-a'), round.resultA.score),
                animateScore(document.getElementById('score-b'), round.resultB.score),
            ]);

            // 若有天賦觸發，顯示加分細節
            if (detA.totalTriggers > 0 && detA.bonusPerTrigger > 0) {
                document.getElementById('score-a').textContent =
                    `${round.resultA.score} (${detA.baseScore}+${detA.totalBonus})`;
            }
            if (detB.totalTriggers > 0 && detB.bonusPerTrigger > 0) {
                document.getElementById('score-b').textContent =
                    `${round.resultB.score} (${detB.baseScore}+${detB.totalBonus})`;
            }

            await sleep(600);
        }

        // 最終結果
        const winner = result.winner === 'a' ? match.a : match.b;
        const winnerName = winner.name;
        const resultText = document.getElementById('result-text');
        resultText.textContent = `${winnerName} 勝利！`;
        resultText.style.color = 'gold';

        const cardA = document.getElementById('card-a');
        const cardB = document.getElementById('card-b');
        if (result.winner === 'a') {
            await animateResult(cardA, cardB);
        } else {
            await animateResult(cardB, cardA);
        }

        await sleep(1500);

        // 推進淘汰賽
        const nextMatch = advanceBracket(state.bracket, winner);

        if (nextMatch === null) {
            // 冠軍產生
            showScreen('screen-champion');
            showChampion(winner);
        } else {
            // 顯示「下一場」按鈕
            const nextBtn = document.getElementById('btn-next');
            nextBtn.classList.remove('hidden');
            nextBtn.addEventListener('click', () => {
                renderBattleScreen();
            });
        }
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
