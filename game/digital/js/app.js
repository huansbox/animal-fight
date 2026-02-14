// game/digital/js/app.js
import { randomAssign, generateDraftOrder, createPool } from './draft.js';
import { createBracket } from './bracket.js';
import { aiPick } from './ai.js';

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
        // startBattle() 將在 Task 8 實作
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
                // startBattle() 將在 Task 8 實作
            });
        }
    }

    render();
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
