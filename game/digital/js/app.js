// game/digital/js/app.js
const state = {
    mode: null,
    difficulty: null,
    size: 16,
    draftMode: 'draft',
    animals: [],
    teamA: [],
    teamB: [],
    bracket: [],
    currentMatch: 0,
};

const IMG_BASE = '../../card/images/';

let allAnimals = [];

async function init() {
    const res = await fetch('data/animals.json');
    allAnimals = await res.json();
    state.animals = allAnimals;
    console.log(`Loaded ${allAnimals.length} animals`);
    showScreen('screen-menu');
}

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => {
        s.classList.remove('active');
    });
    const target = document.getElementById(id);
    target.classList.add('active');
}

export { state, allAnimals, IMG_BASE, showScreen };

init();
