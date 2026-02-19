// 動物園特區定義
// 用途：選角畫面篩選 + mini-card 徽章顯示
const ZONES = {
    ueno: {
        name: '上野動物園',
        icon: '🏯',
        ids: new Set([
            'polar_bear', 'gorilla', 'tiger', 'brown_bear',
            'japanese_macaque', 'hippopotamus', 'giraffe', 'zebra',
            'rhinoceros', 'red_panda', 'kangaroo', 'tortoise',
            'pygmy_hippo', 'aye_aye', 'okapi', 'shoebill',
        ]),
    },
};

function getZoneIcon(animalId) {
    for (const z of Object.values(ZONES)) {
        if (z.ids.has(animalId)) return z.icon;
    }
    return '';
}

export { ZONES, getZoneIcon };
