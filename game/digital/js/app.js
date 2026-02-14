// game/digital/js/app.js
import { randomAssign } from './draft.js';
import { createBracket } from './bracket.js';

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
        // startDraft() 將在 Task 7 實作
    }
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
