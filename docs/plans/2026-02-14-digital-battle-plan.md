# 動物大對決數位版 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 建立離線單機版「動物大對決」Web App，可在 MacBook Pro 14 吋瀏覽器中遊玩。

**Architecture:** 純前端單頁應用，無後端。所有 106 隻動物資料以 JSON 載入，遊戲狀態存於 JS 物件。畫面以 CSS class 切換 + fade 過渡實現。對戰邏輯從 `sim/battle_sim_v5.py` 移植為 JS。

**Tech Stack:** Vanilla HTML/CSS/JS（無框架），ES Modules，CSS Animations/Transitions

---

## Task 1: 建立專案骨架 + 合併動物 JSON

**Files:**
- Create: `game/digital/index.html`
- Create: `game/digital/css/style.css`
- Create: `game/digital/js/app.js`
- Create: `game/digital/data/animals.json`

**Step 1: 建立目錄結構**

```bash
mkdir -p game/digital/css game/digital/js game/digital/data
```

**Step 2: 合併動物 JSON**

從 `card/final_cards.html` 的 `const animals = [...]` 陣列提取全部 106 隻動物資料，轉為獨立 JSON 檔。

每筆格式：
```json
{
  "id": "lion",
  "name": "非洲獅",
  "en": "Lion",
  "img": "lion.png",
  "stats": [7, 6, 8, 4, 5],
  "skillName": "大吼",
  "skillDesc": "嚇跑體型比你小的動物，或讓敵人嚇到不敢亂動。",
  "skillBonus": [{"attr": 0, "val": 2}, {"attr": 2, "val": 2}]
}
```

注意：
- `img` 只存檔名（不含 `images/` 前綴），因為數位版的圖片路徑會不同
- 需從 `final_cards.html` 的 `img` 欄位擷取檔名部分
- 對照 `card/images/` 確認所有 106 張圖都有對應檔案（目前有 84 張 + `new/` 裡 5 張，第八波有些尚未生成）
- 缺圖的動物仍放入 JSON，UI 顯示 placeholder

**Step 3: 建立 index.html 骨架**

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>動物大對決</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Screen 1: 主選單 -->
    <div id="screen-menu" class="screen active">
        <h1 class="game-title">動物大對決</h1>
        <div class="menu-buttons">
            <button id="btn-vs-ai">VS 電腦</button>
            <button id="btn-vs-player">雙人對戰</button>
        </div>
        <!-- AI 難度選擇（預設隱藏） -->
        <div id="ai-difficulty" class="hidden">
            <h2>選擇難度</h2>
            <button data-difficulty="easy">簡單</button>
            <button data-difficulty="normal">普通</button>
            <button data-difficulty="hard">困難</button>
        </div>
    </div>

    <!-- Screen 2: 賽制設定 -->
    <div id="screen-setup" class="screen">
        <h2>賽制設定</h2>
        <div class="setup-section">
            <h3>賽制規模</h3>
            <div class="btn-group" id="size-group">
                <button data-size="4">4 強</button>
                <button data-size="8">8 強</button>
                <button data-size="16" class="selected">16 強</button>
                <button data-size="32">32 強</button>
            </div>
        </div>
        <div class="setup-section">
            <h3>選角方式</h3>
            <div class="btn-group" id="draft-group">
                <button data-draft="random">快速隨機</button>
                <button data-draft="draft" class="selected">選秀</button>
                <button data-draft="manual">自選</button>
            </div>
        </div>
        <button id="btn-start">開始</button>
    </div>

    <!-- Screen 3: 選角 -->
    <div id="screen-draft" class="screen"></div>

    <!-- Screen 4: 對戰 -->
    <div id="screen-battle" class="screen"></div>

    <!-- Screen 5: 冠軍 -->
    <div id="screen-champion" class="screen"></div>

    <script type="module" src="js/app.js"></script>
</body>
</html>
```

**Step 4: 建立 style.css 基礎樣式**

```css
/* 基礎 reset + 畫面切換 */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
    background: #1a1a2e;
    color: #eee;
    min-height: 100vh;
    overflow: hidden;
}

.screen {
    display: none;
    position: absolute;
    inset: 0;
    padding: 20px;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.screen.active {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 1;
}

.hidden { display: none !important; }
```

**Step 5: 建立 app.js 畫面切換**

```javascript
// game/digital/js/app.js
const state = {
    mode: null,        // 'ai' | 'player'
    difficulty: null,  // 'easy' | 'normal' | 'hard'
    size: 16,          // 4 | 8 | 16 | 32
    draftMode: 'draft', // 'random' | 'draft' | 'manual'
    animals: [],       // 所有動物資料
    teamA: [],
    teamB: [],
    bracket: [],
    currentMatch: 0,
};

let allAnimals = [];

async function init() {
    const res = await fetch('data/animals.json');
    allAnimals = await res.json();
    state.animals = allAnimals;
    showScreen('screen-menu');
    bindMenuEvents();
    bindSetupEvents();
}

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => {
        s.classList.remove('active');
    });
    const target = document.getElementById(id);
    target.classList.add('active');
}

// ... 事件綁定（後續 Task 填入）

init();
```

**Step 6: 圖片符號連結**

數位版的圖片不另外複製，建立相對路徑引用 `../../card/images/`。在 `index.html` 或 JS 中以 `../../card/images/` 為 base path 載入圖片。

或者：在 `game/digital/` 下建立 `images` symlink 指向 `card/images/`。

選用方案：JS 中設定 `const IMG_BASE = '../../card/images/'`，不做 symlink，保持簡單。

**Step 7: Commit**

```bash
git add game/digital/
git commit -m "feat(digital): 建立專案骨架 + 合併 106 隻動物 JSON"
```

---

## Task 2: 對戰引擎（battle.js）

**Files:**
- Create: `game/digital/js/battle.js`

**移植來源:** `sim/battle_sim_v5.py` 第 97-161 行

**Step 1: 實作骰子 + 計分核心**

```javascript
// game/digital/js/battle.js

/** 擲一顆 d6 */
function rollD6() {
    return Math.floor(Math.random() * 6) + 1;
}

/** 解析單顆骰子：回傳 { final: 1-5, triggers: 觸發次數 } */
function resolveDie(d) {
    let triggers = 0;
    while (d === 6 && triggers < 100) {
        triggers++;
        d = rollD6();
    }
    if (d === 6) d = 5; // 安全閥
    return { final: d, triggers };
}

/**
 * 計算單方分數
 * @param {Object} animal - { stats: [5], skillBonus: [{attr, val}] }
 * @param {number} d1 - 第一顆骰子原始值
 * @param {number} d2 - 第二顆骰子原始值
 * @returns {Object} { score, details }
 *   details 包含中間過程（給動畫用）：
 *   { d1Raw, d2Raw, d1Final, d2Final, triggers, baseScore, bonusPerTrigger, totalBonus }
 */
function calculateScore(animal, d1, d2) {
    const r1 = resolveDie(d1);
    const r2 = resolveDie(d2);
    const totalTriggers = r1.triggers + r2.triggers;

    // 基礎分
    const attr1 = r1.final - 1; // 骰面 1-5 對應 stats index 0-4
    const attr2 = r2.final - 1;
    let baseScore;
    if (r1.final === r2.final) {
        baseScore = animal.stats[attr1] * 2;
    } else {
        baseScore = animal.stats[attr1] + animal.stats[attr2];
    }

    // 天賦加分
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
            d1Raw: d1, d2Raw: d2,
            d1Final: r1.final, d2Final: r2.final,
            d1Triggers: r1.triggers, d2Triggers: r2.triggers,
            totalTriggers,
            baseScore,
            bonusPerTrigger,
            totalBonus,
        },
    };
}

/**
 * 執行一場對戰
 * @returns {Object} { winner: 'a'|'b', scoreA, scoreB, detailsA, detailsB, rounds }
 *   rounds 紀錄加賽過程（給動畫用）
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
        // 平手 → 繼續加賽
    }
}

export { rollD6, resolveDie, calculateScore, fightMatch };
```

**Step 2: 手動驗證**

在瀏覽器 Console 中載入 `battle.js`，呼叫 `calculateScore` 驗證：
- 蜜獾 `[5,4,6,7,6]` 骰 2+4 → 速度(4)+防禦(7)=11
- 蜜獾 骰 4+6 → 觸發 1 次 → 假設重骰得 5 → 防禦(7)+智慧(6)=13, bonus=3+1=4 → 17
- 蜜獾 骰 3+3 → 攻擊(6)×2=12

**Step 3: Commit**

```bash
git add game/digital/js/battle.js
git commit -m "feat(digital): 對戰引擎 — 骰子、計分、天賦觸發"
```

---

## Task 3: 選角系統（draft.js）

**Files:**
- Create: `game/digital/js/draft.js`
- Create: `game/digital/js/ai.js`

**Step 1: 實作三種選角模式**

```javascript
// game/digital/js/draft.js
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
 * @param {number} total - 總選秀數
 * @returns {string[]} - ['a','b','b','a','a','b','b','a',...]
 */
function generateDraftOrder(total) {
    // A 先選 1，之後 B2-A2-B2-A2...
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
 * @param {Object[]} allAnimals
 * @param {number} totalSize
 */
function createPool(mode, allAnimals, totalSize) {
    if (mode === 'manual') return [...allAnimals]; // 全部 106 隻
    // draft: 隨機抽 totalSize 隻
    return shuffleArray([...allAnimals]).slice(0, totalSize);
}

export { randomAssign, generateDraftOrder, createPool };
```

**Step 2: 建立工具模組**

```javascript
// game/digital/js/utils.js

/** Fisher-Yates shuffle */
function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

export { shuffleArray };
```

**Step 3: 實作 AI 選角策略**

```javascript
// game/digital/js/ai.js

/**
 * AI 從可選池中挑一隻
 * @param {'easy'|'normal'|'hard'} difficulty
 * @param {Object[]} available - 可選動物
 * @param {Object[]} myTeam - AI 已選的動物
 * @returns {Object} 選中的動物
 */
function aiPick(difficulty, available, myTeam) {
    if (difficulty === 'easy') {
        // 隨機
        return available[Math.floor(Math.random() * available.length)];
    }

    // 計算每隻的總和
    const withTotal = available.map(a => ({
        animal: a,
        total: a.stats.reduce((s, v) => s + v, 0),
    }));
    withTotal.sort((a, b) => b.total - a.total);

    if (difficulty === 'normal') {
        // 從前 50% 中隨機挑
        const topHalf = withTotal.slice(0, Math.max(1, Math.ceil(withTotal.length / 2)));
        return topHalf[Math.floor(Math.random() * topHalf.length)].animal;
    }

    // hard: 貪心 — 選總和最高的，若已有相同屬性分布則次優
    return withTotal[0].animal;
}

export { aiPick };
```

**Step 4: Commit**

```bash
git add game/digital/js/draft.js game/digital/js/ai.js game/digital/js/utils.js
git commit -m "feat(digital): 選角系統 — 隨機/選秀/自選 + AI 策略"
```

---

## Task 4: 淘汰賽樹（bracket.js）

**Files:**
- Create: `game/digital/js/bracket.js`

**Step 1: 淘汰賽配對 + 狀態管理**

```javascript
// game/digital/js/bracket.js
import { shuffleArray } from './utils.js';

/**
 * 建立淘汰賽 bracket
 * @param {Object[]} teamA
 * @param {Object[]} teamB
 * @returns {Object} bracket 狀態
 *
 * 配對規則：A1 vs B1, A2 vs B2, ... 先 shuffle 各自順序
 */
function createBracket(teamA, teamB) {
    const a = shuffleArray([...teamA]);
    const b = shuffleArray([...teamB]);
    const matches = [];
    for (let i = 0; i < a.length; i++) {
        matches.push({ a: a[i], b: b[i], winner: null });
    }
    return {
        rounds: [matches],     // rounds[0] = 第一輪, rounds[1] = 第二輪...
        currentRound: 0,
        currentMatch: 0,
    };
}

/**
 * 記錄勝者，推進到下一場/下一輪
 * @returns {Object|null} 下一場配對，或 null 代表冠軍產生
 */
function advanceBracket(bracket, winner) {
    const round = bracket.rounds[bracket.currentRound];
    round[bracket.currentMatch].winner = winner;
    bracket.currentMatch++;

    // 本輪打完 → 建立下一輪
    if (bracket.currentMatch >= round.length) {
        const winners = round.map(m => m.winner);
        if (winners.length === 1) return null; // 冠軍！

        const nextRound = [];
        for (let i = 0; i < winners.length; i += 2) {
            nextRound.push({ a: winners[i], b: winners[i + 1], winner: null });
        }
        bracket.rounds.push(nextRound);
        bracket.currentRound++;
        bracket.currentMatch = 0;
    }

    const curRound = bracket.rounds[bracket.currentRound];
    return curRound[bracket.currentMatch];
}

/** 取得當前要打的配對 */
function getCurrentMatch(bracket) {
    return bracket.rounds[bracket.currentRound][bracket.currentMatch];
}

/** 取得冠軍（最後一輪的勝者） */
function getChampion(bracket) {
    const lastRound = bracket.rounds[bracket.rounds.length - 1];
    return lastRound[0]?.winner || null;
}

export { createBracket, advanceBracket, getCurrentMatch, getChampion };
```

**Step 2: 淘汰賽樹 DOM 渲染**

```javascript
/**
 * 渲染淘汰賽樹到指定容器
 * 使用 CSS Grid，每一輪一個 column
 */
function renderBracket(bracket, container) {
    container.innerHTML = '';
    const totalRounds = Math.log2(bracket.rounds[0].length * 2);

    bracket.rounds.forEach((round, ri) => {
        const col = document.createElement('div');
        col.className = 'bracket-round';
        col.dataset.round = ri;

        round.forEach((match, mi) => {
            const matchEl = document.createElement('div');
            matchEl.className = 'bracket-match';
            if (ri === bracket.currentRound && mi === bracket.currentMatch) {
                matchEl.classList.add('current');
            }

            const nameA = match.a?.name || '?';
            const nameB = match.b?.name || '?';
            const winnerMark = match.winner
                ? (match.winner === match.a ? 'winner-a' : 'winner-b')
                : '';

            matchEl.innerHTML = `
                <span class="bracket-name ${winnerMark === 'winner-a' ? 'won' : ''}">${nameA}</span>
                <span class="bracket-vs">vs</span>
                <span class="bracket-name ${winnerMark === 'winner-b' ? 'won' : ''}">${nameB}</span>
            `;
            col.appendChild(matchEl);
        });

        container.appendChild(col);
    });
}

export { createBracket, advanceBracket, getCurrentMatch, getChampion, renderBracket };
```

**Step 3: Commit**

```bash
git add game/digital/js/bracket.js
git commit -m "feat(digital): 淘汰賽 bracket 邏輯 + 賽程樹渲染"
```

---

## Task 5: 動畫系統（animations.js + CSS）

**Files:**
- Create: `game/digital/js/animations.js`
- Modify: `game/digital/css/style.css`

**Step 1: CSS 動畫定義**

在 `style.css` 中加入：

```css
/* 骰子滾動 */
.dice {
    width: 80px; height: 80px;
    background: #fff; color: #1a1a2e;
    border-radius: 12px;
    font-size: 48px; font-weight: 900;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.1s;
}

.dice.rolling {
    animation: dice-shake 0.1s infinite;
}

@keyframes dice-shake {
    0%, 100% { transform: rotate(0deg) scale(1); }
    25% { transform: rotate(-15deg) scale(1.1); }
    75% { transform: rotate(15deg) scale(1.1); }
}

/* 天賦觸發閃光 */
.dice.trigger {
    animation: trigger-flash 0.5s ease;
    box-shadow: 0 0 20px gold;
}

@keyframes trigger-flash {
    0% { background: gold; transform: scale(1.3); }
    100% { background: #fff; transform: scale(1); }
}

/* 卡片翻牌 */
.card-flip {
    animation: flip-in 0.6s ease;
}

@keyframes flip-in {
    0% { transform: rotateY(90deg); opacity: 0; }
    100% { transform: rotateY(0deg); opacity: 1; }
}

/* 勝者發光 */
.card.winner {
    box-shadow: 0 0 30px 10px gold;
    transition: box-shadow 0.5s;
}

/* 敗者灰掉 */
.card.loser {
    filter: grayscale(1) brightness(0.5);
    transition: filter 0.5s;
}

/* 分數跳動 */
.score-pop {
    animation: score-bump 0.3s ease;
}

@keyframes score-bump {
    0% { transform: scale(0.5); opacity: 0; }
    70% { transform: scale(1.2); }
    100% { transform: scale(1); opacity: 1; }
}

/* 畫面 fade 過渡 */
.screen.fade-in {
    animation: fade-in 0.3s ease forwards;
}

.screen.fade-out {
    animation: fade-out 0.3s ease forwards;
}

@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes fade-out { from { opacity: 1; } to { opacity: 0; } }
```

**Step 2: JS 動畫控制**

```javascript
// game/digital/js/animations.js

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

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

export { animateDiceRoll, animateTrigger, animateScore, animateResult, sleep };
```

**Step 3: Commit**

```bash
git add game/digital/js/animations.js game/digital/css/style.css
git commit -m "feat(digital): 動畫系統 — 骰子滾動、天賦觸發、勝負特效"
```

---

## Task 6: 主選單 + 賽制設定畫面

**Files:**
- Modify: `game/digital/js/app.js`
- Modify: `game/digital/css/style.css`

**Step 1: 主選單事件綁定**

在 `app.js` 中實作：
- 點「VS 電腦」→ 顯示 AI 難度選擇
- 選難度後 → 記入 `state.mode = 'ai'`, `state.difficulty` → 切換到賽制設定
- 點「雙人對戰」→ `state.mode = 'player'` → 切換到賽制設定

**Step 2: 賽制設定事件綁定**

- 賽制規模按鈕組 → 點擊切換 `selected` class + 更新 `state.size`
- 選角方式按鈕組 → 同上 + 更新 `state.draftMode`
- 點「開始」→ 依 `state.draftMode` 決定進入選角或直接進對戰

**Step 3: 樣式**

- 主選單大標題居中
- 按鈕組橫排，選中狀態高亮
- 深色背景 + 明亮按鈕

**Step 4: Commit**

```bash
git add game/digital/js/app.js game/digital/css/style.css
git commit -m "feat(digital): 主選單 + 賽制設定畫面互動"
```

---

## Task 7: 選角畫面 — 選秀 UI

**Files:**
- Modify: `game/digital/js/app.js`
- Modify: `game/digital/css/style.css`

**Step 1: 選秀畫面 DOM 結構**

動態生成 `#screen-draft` 的內容：
- 上方：動物池卡片網格（迷你卡，顯示圖片+名稱+總和）
- 搜尋列（自選模式才顯示）+ 排序按鈕
- 下方分左右：A 已選 / B 已選
- 中間提示：「輪到 A 選」或「電腦思考中...」

**Step 2: 點選邏輯**

- 人類玩家回合：點擊池中卡片 → 移入對應隊伍 → 推進 draft 順序
- AI 回合：延遲 500-1000ms → 自動選 → 移入隊伍
- 全部選完 → 切換到對戰畫面

**Step 3: 快速隨機模式**

- 不顯示選秀 UI
- 直接呼叫 `randomAssign()` → 顯示分配結果確認畫面 → 點「確認」進入對戰

**Step 4: 自選模式**

- 同選秀 UI，但池子是全部 106 隻
- 加搜尋：即時過濾卡片（比對名稱、英文名）
- 加排序：按總和高→低 / 按名稱

**Step 5: 迷你卡片樣式**

```css
.mini-card {
    width: 100px; height: 130px;
    border: 2px solid #444;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4px;
    transition: transform 0.2s, border-color 0.2s;
}

.mini-card:hover {
    transform: scale(1.05);
    border-color: gold;
}

.mini-card.picked { opacity: 0.3; pointer-events: none; }

.mini-card img {
    width: 70px; height: 70px;
    object-fit: contain;
}

.mini-card .name { font-size: 11px; font-weight: bold; }
.mini-card .total { font-size: 10px; color: #aaa; }
```

**Step 6: Commit**

```bash
git add game/digital/js/app.js game/digital/css/style.css
git commit -m "feat(digital): 選秀畫面 — 選秀/自選/快速隨機 UI"
```

---

## Task 8: 對戰畫面 — 核心遊戲循環

**Files:**
- Modify: `game/digital/js/app.js`
- Modify: `game/digital/css/style.css`

**Step 1: 對戰畫面 DOM 結構**

動態生成 `#screen-battle`：
- 上方：迷你淘汰賽樹（bracket 渲染）
- 中間左：A 動物卡（圖片、名稱、五維數值、技能名）
- 中間中：骰子區（2 顆 A 骰 + 2 顆 B 骰）+ 分數顯示 + 結果文字
- 中間右：B 動物卡
- 下方：「擲骰！」按鈕

**Step 2: 對戰流程實作**

```javascript
async function playBattle(match) {
    // 1. 翻牌動畫顯示雙方
    await showCards(match.a, match.b);

    // 2. 等待點擊「擲骰」
    await waitForRollClick();

    // 3. 執行 fightMatch，取得完整結果
    const result = fightMatch(match.a, match.b);

    // 4. 動畫播放每一輪（含加賽）
    for (let i = 0; i < result.rounds.length; i++) {
        const round = result.rounds[i];
        if (i > 0) {
            // 加賽提示
            showMessage('加賽！');
            await sleep(1000);
        }
        await animateRound(round);
    }

    // 5. 勝負動畫
    await animateResult(winnerCard, loserCard);

    // 6. 更新 bracket + 顯示「下一場」
    const winner = result.winner === 'a' ? match.a : match.b;
    return winner;
}
```

**注意：對戰結果要預先算好，動畫只是播放。** `fightMatch` 在點「擲骰」時就算完，之後用動畫「重播」結果，不是邊擲邊算。

**Step 3: 屬性名對照**

```javascript
const ATTR_NAMES = ['力量', '速度', '攻擊', '防禦', '智慧'];
const ATTR_ICONS = ['💪', '⚡', '⚔️', '🛡️', '🧠'];
```

骰子結果顯示時，除了數字也顯示對應屬性名，讓小孩看懂。

**Step 4: 動物卡片樣式（對戰用大卡）**

```css
.battle-card {
    width: 280px;
    background: #2a2a4a;
    border: 3px solid #555;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
}

.battle-card img {
    width: 200px; height: 200px;
    object-fit: contain;
}

.battle-card .animal-name {
    font-size: 28px;
    font-weight: 900;
    margin: 8px 0;
}

.battle-card .stats {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
    font-size: 14px;
}

.battle-card .stat {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.battle-card .stat-value {
    font-size: 24px;
    font-weight: 900;
}

.battle-card .skill-name {
    font-size: 16px;
    color: gold;
    margin-top: 8px;
}
```

**Step 5: Commit**

```bash
git add game/digital/js/app.js game/digital/css/style.css
git commit -m "feat(digital): 對戰畫面 — 核心遊戲循環 + 動畫播放"
```

---

## Task 9: 冠軍畫面 + 遊戲重開

**Files:**
- Modify: `game/digital/js/app.js`
- Modify: `game/digital/css/style.css`

**Step 1: 冠軍畫面**

淘汰賽打完後切換到 `#screen-champion`：
- 冠軍動物大圖 + 名稱 + 英文名
- 「冠軍！」大字 + 金色特效
- 戰績統計（總共打了幾場）
- 「再來一局」按鈕 → 回到賽制設定（保留上次設定）
- 「回主選單」按鈕 → 回到主選單

**Step 2: 狀態重置**

「再來一局」→ 只重置 `teamA/teamB/bracket`，保留 `mode/difficulty/size/draftMode`
「回主選單」→ 全部重置

**Step 3: Commit**

```bash
git add game/digital/js/app.js game/digital/css/style.css
git commit -m "feat(digital): 冠軍畫面 + 遊戲重開"
```

---

## Task 10: 整合測試 + 收尾

**Files:**
- Modify: `game/digital/index.html`（視需要調整）
- Modify: `game/digital/css/style.css`（視需要調整）

**Step 1: 端到端測試**

在瀏覽器中完整跑一遍：
1. 主選單 → vs 電腦 → 困難
2. 賽制設定 → 8 強 → 選秀
3. 選秀 → snake draft 完成
4. 對戰 → 逐場打完（確認動畫、分數、天賦觸發都正確）
5. 冠軍 → 再來一局 → 4 強 → 快速隨機 → 打完
6. 雙人模式 → 16 強 → 自選 → 打完

**Step 2: 檢查項目**

- [ ] 所有動物圖片正確載入（缺圖顯示 placeholder）
- [ ] 骰到 6 有天賦觸發動畫 + 重骰
- [ ] 連續骰 6 正確累加觸發次數
- [ ] 平手正確加賽
- [ ] 淘汰賽樹正確更新晉級
- [ ] 冠軍畫面顯示正確
- [ ] 重開遊戲狀態乾淨

**Step 3: 視覺微調**

- 字體大小適合 14 吋螢幕觀看距離
- 顏色對比度足夠
- 動畫節奏：骰子 0.8s、天賦 0.6s、結果 0.5s → 整場約 3-5 秒，不拖

**Step 4: Commit**

```bash
git add -A game/digital/
git commit -m "feat(digital): 整合測試 + 視覺微調"
```

---

## Task 11: 更新專案文件

**Files:**
- Modify: `CLAUDE.md`
- Modify: `game/digital/index.html`（加入字型 fallback）

**Step 1: 更新 CLAUDE.md**

- 在專案結構中加入 `game/digital/` 區段
- 在「當前狀態」加入數位版相關 checklist
- 更新技術決策區段

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: CLAUDE.md 加入數位版專案結構與狀態"
```

---

## 依賴關係

```
Task 1 (骨架 + JSON)
  ├→ Task 2 (battle.js)
  ├→ Task 3 (draft.js + ai.js)
  ├→ Task 4 (bracket.js)
  └→ Task 5 (animations.js + CSS)
       ↓
Task 6 (主選單 + 設定) ← 依賴 Task 1
       ↓
Task 7 (選角 UI) ← 依賴 Task 3, 6
       ↓
Task 8 (對戰畫面) ← 依賴 Task 2, 4, 5, 7
       ↓
Task 9 (冠軍畫面) ← 依賴 Task 8
       ↓
Task 10 (整合測試) ← 依賴 Task 9
       ↓
Task 11 (文件更新) ← 依賴 Task 10
```

**可平行的 Task：** Task 2, 3, 4, 5 彼此獨立，可同時開發。
