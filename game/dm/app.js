import { scenario } from "./scenarios.js";

const ACTIVE_KEY = "animalFight.dm.active.v2";
const RECORDS_KEY = "animalFight.dm.records.v2";
const modeNames = {
    "dad-younger": "爸爸＋弟弟",
    "dad-older": "爸爸＋哥哥",
    siblings: "兄弟合作"
};
const understandingNames = {
    easy: "大多能自己理解",
    prompted: "偶爾需要提醒",
    confused: "經常搞混"
};
const dmLoadNames = {
    light: "輕鬆",
    normal: "普通",
    busy: "很忙"
};
const treasureNames = {
    backpack: "萬用背包",
    flashlight: "探險手電筒",
    mirror: "變化魔鏡"
};

const app = document.querySelector("#app");
const homeButton = document.querySelector("#home-button");
let activeSession = readJson(ACTIVE_KEY, null);

function readJson(key, fallback) {
    try {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : fallback;
    } catch {
        return fallback;
    }
}

function writeJson(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function cloneTemplate(id) {
    return document.querySelector(id).content.cloneNode(true);
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function setView(fragment, { showHome = true } = {}) {
    app.replaceChildren(fragment);
    homeButton.hidden = !showHome;
    window.scrollTo({ top: 0, behavior: "auto" });
    app.focus({ preventScroll: true });
}

function showToast(message) {
    document.querySelector(".toast")?.remove();
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2200);
}

function showHome() {
    const fragment = cloneTemplate("#home-template");
    fragment.querySelector("#scenario-title").textContent = scenario.title;
    fragment.querySelector("#scenario-summary").textContent = scenario.summary;
    const setup = fragment.querySelector("#scenario-setup");
    scenario.setup.forEach((item) => {
        const row = document.createElement("div");
        row.className = "setup-item";
        row.textContent = item;
        setup.appendChild(row);
    });

    const startButton = fragment.querySelector("#start-button");
    const resumeButton = fragment.querySelector("#resume-button");
    const recordsButton = fragment.querySelector("#records-button");
    resumeButton.hidden = !activeSession;

    startButton.addEventListener("click", () => {
        const mode = document.querySelector('input[name="play-mode"]:checked').value;
        activeSession = {
            id: crypto.randomUUID?.() || `${Date.now()}-${Math.random()}`,
            scenarioId: scenario.id,
            scenarioVersion: scenario.version,
            playMode: mode,
            stepIndex: 0,
            startedAt: new Date().toISOString()
        };
        writeJson(ACTIVE_KEY, activeSession);
        showGame();
    });

    resumeButton.addEventListener("click", showGame);
    recordsButton.addEventListener("click", showRecords);
    setView(fragment, { showHome: false });
}

function renderRequirements(container, requirements = []) {
    container.replaceChildren();
    container.hidden = requirements.length === 0;
    requirements.forEach((requirement) => {
        const card = document.createElement("section");
        card.className = "requirement-card";
        card.innerHTML = `
            <h3>${requirement.title}</h3>
            <div class="requirement-main"><span>${requirement.attributes.join(" 或 ")}</span><strong>${requirement.range}</strong></div>
            <p>${requirement.reason}</p>
        `;
        container.appendChild(card);
    });
}

function renderList(container, title, items = []) {
    container.innerHTML = items.length ? `<h3>${title}</h3><ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>` : "";
}

function renderOutcomes(container, outcomes = []) {
    container.innerHTML = outcomes.length ? outcomes.map((outcome) => `
        <div class="outcome"><strong>${outcome.title}</strong>${outcome.text}</div>
    `).join("") : "";
}

function renderHints(panel, container, hints = []) {
    panel.hidden = hints.length === 0;
    container.innerHTML = `<div class="hint-grid">${hints.map((group) => `
        <section class="hint-group"><h3>${group.attribute}</h3><ul>${group.items.map((item) => `<li>${item}</li>`).join("")}</ul></section>
    `).join("")}</div>`;
}

function renderBossTools(section, step) {
    section.hidden = !step.treasures;
    if (!step.treasures) return;
    const flow = section.querySelector("#treasure-flow");
    const picker = section.querySelector("#threshold-picker");
    const result = section.querySelector("#threshold-result");
    flow.innerHTML = step.treasures.map((treasure, index) => `
        <section class="treasure-step">
            <span>${index + 1}</span>
            <div><h3>${treasure.name}</h3><p>${treasure.dice}</p><strong>${treasure.action}</strong></div>
        </section>
    `).join("");
    picker.replaceChildren();
    step.thresholds.forEach((threshold, index) => {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = threshold.label;
        button.addEventListener("click", () => {
            picker.querySelectorAll("button").forEach((item) => item.classList.remove("active"));
            button.classList.add("active");
            result.textContent = threshold.line;
        });
        picker.appendChild(button);
        if (index === 0) button.click();
    });
}

function showGame() {
    if (!activeSession) return showHome();
    const fragment = cloneTemplate("#game-template");
    const step = scenario.steps[activeSession.stepIndex];

    fragment.querySelector("#progress-label").textContent = `${activeSession.stepIndex + 1} / ${scenario.steps.length}`;
    const track = fragment.querySelector("#progress-track");
    scenario.steps.forEach((item, index) => {
        const dot = document.createElement("span");
        dot.className = `progress-dot ${index < activeSession.stepIndex ? "done" : ""} ${index === activeSession.stepIndex ? "current" : ""}`;
        dot.title = item.label;
        track.appendChild(dot);
    });

    fragment.querySelector("#step-label").textContent = step.label;
    fragment.querySelector("#step-title").textContent = step.title;
    fragment.querySelector("#physical-cue").textContent = step.physicalCue;
    fragment.querySelector("#narration").innerHTML = step.narration.map((paragraph) => `<p>${paragraph}</p>`).join("");
    renderRequirements(fragment.querySelector("#requirements"), step.requirements);

    const questionWrap = fragment.querySelector("#child-question-wrap");
    questionWrap.hidden = !step.question;
    if (step.question) fragment.querySelector("#child-question").textContent = step.question;

    renderList(fragment.querySelector("#dm-rules"), "這一步的規則", step.rules);
    renderOutcomes(fragment.querySelector("#dm-outcomes"), step.outcomes);
    renderHints(fragment.querySelector("#hint-panel"), fragment.querySelector("#hints"), step.hints);
    renderBossTools(fragment.querySelector("#boss-tools"), step);

    const previous = fragment.querySelector("#previous-button");
    const next = fragment.querySelector("#next-button");
    previous.disabled = activeSession.stepIndex === 0;
    next.textContent = activeSession.stepIndex === scenario.steps.length - 1 ? "完成並記錄" : `下一步：${scenario.steps[activeSession.stepIndex + 1].label}`;

    previous.addEventListener("click", () => {
        activeSession.stepIndex -= 1;
        writeJson(ACTIVE_KEY, activeSession);
        showGame();
    });

    next.addEventListener("click", () => {
        if (activeSession.stepIndex === scenario.steps.length - 1) return showDebrief();
        activeSession.stepIndex += 1;
        writeJson(ACTIVE_KEY, activeSession);
        showGame();
    });

    setView(fragment);
}

function showDebrief() {
    if (!activeSession) return showHome();
    const fragment = cloneTemplate("#debrief-template");
    const form = fragment.querySelector("#debrief-form");
    fragment.querySelector("#skip-record-button").addEventListener("click", finishSession);
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const data = new FormData(form);
        const endedAt = new Date();
        const record = {
            sessionId: activeSession.id,
            scenarioId: scenario.id,
            scenarioVersion: scenario.version,
            scenarioTitle: scenario.title,
            playMode: activeSession.playMode,
            startedAt: activeSession.startedAt,
            endedAt: endedAt.toISOString(),
            durationMinutes: Math.max(1, Math.round((endedAt - new Date(activeSession.startedAt)) / 60000)),
            taskResults: [data.get("task1Result"), data.get("task2Result"), data.get("task3Result")],
            treasures: data.getAll("treasures"),
            bossPool: {
                a: Number(data.get("bossPoolA")),
                b: Number(data.get("bossPoolB"))
            },
            treasureResults: {
                backpackDice: data.get("backpackDice"),
                flashlightLevel: data.get("flashlightLevel"),
                mirror: data.get("mirrorResult")
            },
            reservesUsed: Number(data.get("reservesUsed")),
            bossBeforeReserve: data.get("bossBeforeReserve") === "yes",
            bossResult: data.get("bossResult"),
            understanding: data.get("understanding"),
            dmLoad: data.get("dmLoad"),
            note: data.get("note").trim()
        };
        const records = readJson(RECORDS_KEY, []);
        records.unshift(record);
        writeJson(RECORDS_KEY, records.slice(0, 50));
        finishSession();
        showToast("本局紀錄已儲存");
    });
    setView(fragment);
}

function finishSession() {
    activeSession = null;
    localStorage.removeItem(ACTIVE_KEY);
    showHome();
}

function recordMarkdown(records) {
    if (!records.length) return "尚無團隊任務測試紀錄。";
    return records.map((record) => [
        `## ${record.scenarioTitle}｜${new Date(record.startedAt).toLocaleString("zh-TW")}`,
        `- 模式：${modeNames[record.playMode]}`,
        `- 時間：${record.durationMinutes} 分鐘`,
        `- 一般任務：${record.taskResults.map((result, index) => `${index + 1}.${result === "success" ? "成功" : "失敗"}`).join("、")}`,
        `- 寶物（${record.treasures.length}）：${record.treasures.map((key) => treasureNames[key] || key).join("、") || "無"}`,
        `- Boss 原始骰池：A ${record.bossPool.a}／B ${record.bossPool.b}`,
        `- 寶物結果：背包 ${formatTreasureValue(record.treasureResults.backpackDice, " 顆")}；手電筒 ${formatFlashlight(record.treasureResults.flashlightLevel)}；魔鏡 ${formatMirror(record.treasureResults.mirror)}`,
        `- 使用後援：${record.reservesUsed}`,
        `- 後援前打敗 Boss：${record.bossBeforeReserve ? "是" : "否"}`,
        `- Boss：${record.bossResult === "success" ? "成功完成" : "危機未解除"}`,
        `- 理解：${understandingNames[record.understanding] || record.understanding}`,
        `- DM 負擔：${dmLoadNames[record.dmLoad] || record.dmLoad}`,
        `- 備註：${record.note || "無"}`
    ].join("\n")).join("\n\n");
}

function formatTreasureValue(value, unit) {
    return value === "none" ? "未取得" : `＋${value}${unit}`;
}

function formatMirror(value) {
    if (value === "none") return "未取得";
    if (value === "reverse") return "魔鏡反轉";
    return `${value} 點`;
}

function formatFlashlight(value) {
    return value === "none" ? "未取得" : `降低 ${value} 級`;
}

function showRecords() {
    const fragment = cloneTemplate("#records-template");
    const records = readJson(RECORDS_KEY, []);
    const list = fragment.querySelector("#records-list");
    list.innerHTML = records.length ? records.map((record) => `
        <article class="record-card">
            <div>
                <h3>${escapeHtml(record.scenarioTitle)}</h3>
                <p>${new Date(record.startedAt).toLocaleString("zh-TW")}</p>
                <p>${escapeHtml(modeNames[record.playMode] || record.playMode)}｜${record.durationMinutes} 分鐘</p>
            </div>
            <div>
                <p>一般任務 ${record.taskResults.filter((result) => result === "success").length}/3｜寶物 ${record.treasures.length}｜後援用 ${record.reservesUsed}</p>
                <p>Boss 骰池 ${record.bossPool.a}＋${record.bossPool.b}｜後援前 ${record.bossBeforeReserve ? "已成功" : "未成功"}｜最終 ${record.bossResult === "success" ? "成功" : "未完成"}</p>
                <p>理解：${escapeHtml(understandingNames[record.understanding] || record.understanding)}｜DM：${escapeHtml(dmLoadNames[record.dmLoad] || record.dmLoad)}</p>
                <p>${escapeHtml(record.note || "沒有備註")}</p>
            </div>
        </article>
    `).join("") : `<p class="empty-state">還沒有測試紀錄。</p>`;

    fragment.querySelector("#copy-records-button").disabled = !records.length;
    fragment.querySelector("#export-records-button").disabled = !records.length;
    fragment.querySelector("#clear-records-button").disabled = !records.length;

    fragment.querySelector("#copy-records-button").addEventListener("click", async () => {
        await navigator.clipboard.writeText(recordMarkdown(records));
        showToast("已複製 Markdown");
    });
    fragment.querySelector("#export-records-button").addEventListener("click", () => {
        const blob = new Blob([JSON.stringify(records, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = `animal-fight-playtests-${new Date().toISOString().slice(0, 10)}.json`;
        anchor.click();
        URL.revokeObjectURL(url);
    });
    fragment.querySelector("#clear-records-button").addEventListener("click", () => {
        if (!confirm("確定清除這個瀏覽器裡的全部測試紀錄？")) return;
        localStorage.removeItem(RECORDS_KEY);
        showRecords();
    });
    setView(fragment);
}

homeButton.addEventListener("click", showHome);

const previewStepId = new URLSearchParams(window.location.search).get("preview");
const previewStepIndex = scenario.steps.findIndex((step) => step.id === previewStepId);
if (previewStepId === "debrief") {
    activeSession = {
        id: "preview",
        scenarioId: scenario.id,
        scenarioVersion: scenario.version,
        playMode: "siblings",
        stepIndex: scenario.steps.length - 1,
        startedAt: new Date().toISOString()
    };
    showDebrief();
} else if (previewStepIndex >= 0) {
    activeSession = {
        id: "preview",
        scenarioId: scenario.id,
        scenarioVersion: scenario.version,
        playMode: "siblings",
        stepIndex: previewStepIndex,
        startedAt: new Date().toISOString()
    };
    showGame();
} else {
    showHome();
}
