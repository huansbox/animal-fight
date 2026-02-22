/**
 * 動物猜猜看 — 遊戲主邏輯
 */
import { HINTS, DISTRACTOR_GROUPS, MVP_ANIMAL_IDS } from './hints.js';

// ===== DOM 快取 =====
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const screens = {
  start:  $('#screen-start'),
  quiz:   $('#screen-quiz'),
  reveal: $('#screen-reveal'),
  final:  $('#screen-final'),
};

// ===== 遊戲狀態 =====
let animalsData = [];        // animals.json 載入的完整資料
let animalMap = {};           // id → animal object
let questionCount = 20;
let questionPool = [];        // 本局使用的動物 id 陣列（亂序）
let currentIdx = 0;           // 目前第幾題（0-based）
let currentAnimalId = '';
let currentHintShown = 0;     // 已顯示幾個提示（0/1/2/3）
let answered = false;
let score = 0;
let maxScore = 0;
let results = [];             // { id, correct, hintsUsed, points }
let isChallenge = false;
const SAVE_KEY = 'animal-quiz-challenge';

// ===== 初始化 =====
async function init() {
  // 嘗試多個相對路徑（取決於 HTTP server 根目錄）
  const paths = [
    '../digital/data/animals.json',           // server root = game/
    '../../game/digital/data/animals.json',   // server root = 專案根
    'game/digital/data/animals.json',         // server root = 專案根（絕對）
  ];
  for (const p of paths) {
    try {
      const res = await fetch(p);
      if (res.ok) { animalsData = await res.json(); break; }
    } catch { /* try next */ }
  }
  animalMap = {};
  for (const a of animalsData) {
    animalMap[a.id] = a;
  }
  bindEvents();
  updateChallengeUI();
}

// ===== 事件綁定 =====
function bindEvents() {
  // 題數選擇
  $$('.btn-mode').forEach((btn) => {
    btn.addEventListener('click', () => {
      $$('.btn-mode').forEach((b) => b.classList.remove('selected'));
      btn.classList.add('selected');
      questionCount = parseInt(btn.dataset.count);
    });
  });

  // 開始
  $('#btn-start').addEventListener('click', startGame);

  // 下一個提示
  $('#btn-next-hint').addEventListener('click', showNextHint);

  // 選項點擊
  $$('.btn-option').forEach((btn) => {
    btn.addEventListener('click', () => handleAnswer(btn));
  });

  // 下一題
  $('#btn-next').addEventListener('click', nextQuestion);

  // 再玩一次 / 回主選單
  $('#btn-restart').addEventListener('click', () => isChallenge ? startChallenge() : startGame());
  $('#btn-home').addEventListener('click', goHome);

  // 全制霸模式
  $('#btn-challenge').addEventListener('click', startChallenge);
  $('#btn-resume').addEventListener('click', resumeChallenge);
  $('#btn-reset-save').addEventListener('click', resetChallenge);
  $('#btn-save-exit').addEventListener('click', goHome);
}

// ===== 畫面切換 =====
function switchScreen(name) {
  Object.values(screens).forEach((s) => s.classList.remove('active'));
  screens[name].classList.add('active');
}

// ===== 開始遊戲 =====
function startGame() {
  isChallenge = false;
  $('#btn-save-exit').classList.add('hidden');
  // 只使用有提示的動物
  const available = MVP_ANIMAL_IDS.filter((id) => animalMap[id]);
  questionPool = shuffle(available).slice(0, Math.min(questionCount, available.length));
  currentIdx = 0;
  score = 0;
  maxScore = questionPool.length * 3;
  results = [];
  switchScreen('quiz');
  loadQuestion();
}

// ===== 載入題目 =====
function loadQuestion() {
  const id = questionPool[currentIdx];
  currentAnimalId = id;
  currentHintShown = 0;
  answered = false;

  // 更新進度
  $('#progress-text').textContent = `第 ${currentIdx + 1} / ${questionPool.length} 題`;
  $('#score-text').textContent = `⭐ ${score} 分`;
  $('#progress-fill').style.width = `${((currentIdx) / questionPool.length) * 100}%`;

  // 重置提示
  for (let i = 1; i <= 3; i++) {
    const card = $(`#hint-${i}`);
    card.classList.add('hidden');
    card.querySelector('.hint-text').textContent = '';
  }
  $('#btn-next-hint').classList.remove('hidden');

  // 顯示第一個提示
  showNextHint();

  // 生成選項
  generateOptions(id);
}

// ===== 顯示下一個提示 =====
function showNextHint() {
  if (currentHintShown >= 3 || answered) return;
  currentHintShown++;
  const hint = HINTS[currentAnimalId];
  const card = $(`#hint-${currentHintShown}`);
  card.querySelector('.hint-text').textContent = hint.hints[currentHintShown - 1];
  card.classList.remove('hidden');

  // 第三個提示後隱藏按鈕
  if (currentHintShown >= 3) {
    $('#btn-next-hint').classList.add('hidden');
  }
}

// ===== 生成選項 =====
function generateOptions(correctId) {
  const distractors = pickDistractors(correctId, 4);
  const options = shuffle([correctId, ...distractors]);

  $$('.btn-option').forEach((btn, i) => {
    const id = options[i];
    const animal = animalMap[id];
    btn.textContent = animal ? animal.name : id;
    btn.dataset.id = id;
    btn.className = 'btn btn-option'; // 重置樣式
  });
}

// ===== 挑選干擾選項 =====
function pickDistractors(correctId, count) {
  const hintData = HINTS[correctId];
  if (!hintData) return randomPick(MVP_ANIMAL_IDS.filter((id) => id !== correctId), count);

  // 收集同組動物，計算重疊度
  const overlapCount = {};
  for (const group of hintData.groups) {
    const members = DISTRACTOR_GROUPS[group] || [];
    for (const id of members) {
      if (id !== correctId && animalMap[id]) {
        overlapCount[id] = (overlapCount[id] || 0) + 1;
      }
    }
  }

  // 按重疊度排序，取前 count 個
  const candidates = Object.entries(overlapCount)
    .sort((a, b) => b[1] - a[1])
    .map(([id]) => id);

  // 如果不夠，從剩餘動物補
  if (candidates.length < count) {
    const remaining = MVP_ANIMAL_IDS.filter(
      (id) => id !== correctId && !candidates.includes(id) && animalMap[id]
    );
    candidates.push(...shuffle(remaining));
  }

  return candidates.slice(0, count);
}

// ===== 處理作答 =====
function handleAnswer(btn) {
  if (answered) return;
  answered = true;
  $('#btn-next-hint').classList.add('hidden');

  const selectedId = btn.dataset.id;
  const isCorrect = selectedId === currentAnimalId;
  const points = isCorrect ? (4 - currentHintShown) : 0;
  score += points;

  results.push({
    id: currentAnimalId,
    correct: isCorrect,
    hintsUsed: currentHintShown,
    points,
  });

  // 全制霸模式自動存檔
  if (isChallenge) saveChallengeProgress();

  // 標記選項
  $$('.btn-option').forEach((b) => {
    if (b.dataset.id === currentAnimalId) {
      b.classList.add(isCorrect ? 'correct' : 'reveal-correct');
    } else if (b === btn && !isCorrect) {
      b.classList.add('wrong');
    } else {
      b.classList.add('dimmed');
    }
  });

  // 短暫延遲後顯示揭曉畫面
  setTimeout(() => showReveal(isCorrect, points), 800);
}

// ===== 揭曉畫面 =====
function showReveal(isCorrect, points) {
  const animal = animalMap[currentAnimalId];
  const resultEl = $('#reveal-result');
  if (isCorrect) {
    resultEl.textContent = '答對了！';
    resultEl.className = 'reveal-result correct';
  } else {
    resultEl.textContent = `答錯了！正確答案是 ${animal.name}`;
    resultEl.className = 'reveal-result wrong';
  }

  // 圖片
  const img = $('#reveal-img');
  const imgPath = `../../card/images-realistic/${animal.id}.png`;
  img.src = imgPath;
  img.alt = animal.name;
  img.onerror = () => {
    img.style.display = 'none';
  };
  img.onload = () => {
    img.style.display = '';
  };

  // 名稱
  $('#reveal-name').textContent = animal.name;
  $('#reveal-en').textContent = animal.en;

  // 技能
  $('#reveal-skill').innerHTML = `<strong>🎯 ${animal.skillName}</strong>：${animal.skillDesc}`;

  // 分數
  const stars = '⭐'.repeat(points) || '😢';
  $('#reveal-points').textContent = `${stars} +${points} 分`;

  // 最後一題？
  if (currentIdx >= questionPool.length - 1) {
    $('#btn-next').textContent = '看結果 🏆';
  } else {
    $('#btn-next').textContent = '下一題 ➜';
  }

  switchScreen('reveal');
}

// ===== 下一題 =====
function nextQuestion() {
  currentIdx++;
  if (currentIdx >= questionPool.length) {
    showFinal();
  } else {
    switchScreen('quiz');
    loadQuestion();
  }
}

// ===== 結算畫面 =====
function showFinal() {
  const pct = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;

  // 段位
  let badge, title;
  if (pct >= 90) { badge = '🏆'; title = '動物大師'; }
  else if (pct >= 70) { badge = '🎓'; title = '動物專家'; }
  else if (pct >= 50) { badge = '🔍'; title = '動物偵探'; }
  else if (pct >= 30) { badge = '📚'; title = '動物學徒'; }
  else { badge = '🌱'; title = '動物新手'; }

  $('#final-badge').textContent = badge;
  $('#final-title').textContent = title;
  $('#final-score').textContent = `${score} / ${maxScore} 分（${pct}%）`;

  // 明細
  const correctCount = results.filter((r) => r.correct).length;
  const h1Count = results.filter((r) => r.correct && r.hintsUsed === 1).length;
  const h2Count = results.filter((r) => r.correct && r.hintsUsed === 2).length;
  const h3Count = results.filter((r) => r.correct && r.hintsUsed === 3).length;
  const wrongCount = results.filter((r) => !r.correct).length;

  $('#final-breakdown').innerHTML = `
    <div class="row"><span class="label">總題數</span><span class="value">${questionPool.length} 題</span></div>
    <div class="row"><span class="label">答對</span><span class="value">${correctCount} 題</span></div>
    <div class="row"><span class="label">⭐⭐⭐ 第一個提示就猜到</span><span class="value">${h1Count} 題</span></div>
    <div class="row"><span class="label">⭐⭐ 第二個提示猜到</span><span class="value">${h2Count} 題</span></div>
    <div class="row"><span class="label">⭐ 第三個提示才猜到</span><span class="value">${h3Count} 題</span></div>
    <div class="row"><span class="label">😢 答錯</span><span class="value">${wrongCount} 題</span></div>
  `;

  // 全制霸模式結算
  if (isChallenge) {
    clearChallengeProgress();
    $('#btn-save-exit').classList.add('hidden');
    $('#btn-restart').textContent = '再挑戰一次';
  } else {
    $('#btn-restart').textContent = '再玩一次';
  }

  switchScreen('final');
}

// ===== 全制霸模式 =====
function goHome() {
  switchScreen('start');
  updateChallengeUI();
}

function startChallenge() {
  isChallenge = true;
  const available = MVP_ANIMAL_IDS.filter((id) => animalMap[id]);
  questionPool = shuffle(available);
  currentIdx = 0;
  score = 0;
  maxScore = questionPool.length * 3;
  results = [];
  saveChallengeProgress();
  $('#btn-save-exit').classList.remove('hidden');
  switchScreen('quiz');
  loadQuestion();
}

function resumeChallenge() {
  const save = loadChallengeProgress();
  if (!save) return startChallenge();
  isChallenge = true;
  questionPool = save.questionPool;
  score = save.score;
  results = save.results;
  currentIdx = results.length;
  maxScore = questionPool.length * 3;
  if (currentIdx >= questionPool.length) {
    showFinal();
    return;
  }
  $('#btn-save-exit').classList.remove('hidden');
  switchScreen('quiz');
  loadQuestion();
}

function resetChallenge() {
  clearChallengeProgress();
  startChallenge();
}

function saveChallengeProgress() {
  localStorage.setItem(SAVE_KEY, JSON.stringify({
    questionPool, score, results, timestamp: Date.now(),
  }));
}

function loadChallengeProgress() {
  try {
    return JSON.parse(localStorage.getItem(SAVE_KEY));
  } catch { return null; }
}

function clearChallengeProgress() {
  localStorage.removeItem(SAVE_KEY);
}

function updateChallengeUI() {
  const save = loadChallengeProgress();
  const newEl = $('#challenge-new');
  const resumeEl = $('#challenge-resume');
  if (save && save.results.length < save.questionPool.length) {
    newEl.classList.add('hidden');
    $('#resume-progress').textContent = save.results.length;
    $('#resume-total').textContent = save.questionPool.length;
    $('#resume-score').textContent = save.score;
    resumeEl.classList.remove('hidden');
  } else {
    newEl.classList.remove('hidden');
    resumeEl.classList.add('hidden');
  }
}

// ===== 工具函式 =====
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function randomPick(arr, n) {
  return shuffle(arr).slice(0, n);
}

// ===== 啟動 =====
init();
