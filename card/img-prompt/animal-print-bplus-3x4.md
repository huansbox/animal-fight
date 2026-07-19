# 動物卡 B+ 黑白印刷風格 3×4 測試 Prompt

> 日期：2026-07-18
> 用途：以 3 個 B+ 微調版本測試 4 種高風險動物，定案 132 張實體動物卡的共同圖片風格。
> 輸出尺寸基準：卡面圖片約 114×70mm，黑白雷射列印。

> **定案（2026-07-19）**：四種測試動物全部選擇 V2「圖鑑平衡版」。後續正式動物圖片統一使用 V2；V1／V3 僅保留為比較紀錄。

## 產生方法

1. 先用 V2「圖鑑平衡版」分別產生非洲象、黑豹、河豚、行軍蟻。
2. 每隻動物的 V2 圖作為 edit target，分別轉成 V1、V3。
3. edit 時鎖定動物身體、動作、方向、構圖、比例與背景，只改灰階階數、外輪廓粗細、物種紋理密度。
4. 12 張圖均使用 3:2 橫式構圖，禁止文字、外框與水印。

## 共用 Prompt

```text
Use case: scientific-educational
Asset type: final 3:2 landscape animal artwork for a children's board-game card, printed about 114 by 70 mm on a monochrome laser printer
Primary request: create one simplified natural-history field-guide illustration in the B+ style. Make the intended special-ability action understandable to a five-year-old from the silhouette and one clear cause-and-effect cue, without text or symbolic effects.
Style/medium: anatomically realistic mature natural-history illustration, not photographic and not cartoon. Use discrete flat grayscale regions, a clean print-safe outer contour, broad readable body planes, and only the species-identifying details needed to recognize the animal.
Composition/framing: 3:2 landscape, believable three-quarter side view, one clear motion direction. Keep the complete subject and complete ability effect inside the frame. The subject group occupies 70–75 percent of the longest image dimension with at least 8 percent clear crop-safe space on every edge.
Scene/backdrop: paper-white background with at most one minimal pale-gray grounding shape. No habitat scene or decorative background.
Print construction: use discrete flat grayscale regions only. No smooth gradients, continuous-tone lighting, photographic grain, dense fur or skin microtexture, stippling, crosshatching, engraving marks, halftone screens, or hairline detail. Keep every essential feature readable when printed at 114 by 70 mm.
Ink control: reserve solid black for the outer contour, pupils, and a few structural accents. Avoid any large connected solid-black mass. Separate overlapping legs, fins, tails, antennae, and body parts with light negative-space gaps.
Child clarity: show only one action and one motion direction. Keep the animal's expression calm and alert. No victim, injury, threat toward the viewer, horror imagery, blood, prey, carcass, exposed teeth, attack impact, text, border, logo, or watermark.
Rendering lock: keep animal anatomy, action, three-quarter side view, motion direction, framing, subject scale, crop-safe margin, and white background identical across all three variants. The only permitted differences are grayscale tone count, outer-contour weight, and species-texture density.
```

## 三個版本

### V1：柔和色塊版

```text
Style variant V1 only: use exactly five output tones including paper white, a fine but print-safe outer contour equivalent to 0.30–0.35 mm at final print size, broad clean tonal shapes, and almost no internal texture. Species-identifying texture may cover no more than about 5 percent of the animal. Preserve the exact anatomy, action, pose, framing, scale, background, and ability effect of the V2 edit target; change only the tone treatment, contour weight, and texture density.
```

### V2：圖鑑平衡版（正式採用）

```text
Style variant V2 only: use exactly five output tones including paper white, a medium outer contour equivalent to 0.45–0.50 mm at final print size, and sparse species-identifying texture confined to the face, major joints, and the most recognizable skin, fur, spine, or exoskeleton features. Texture may cover about 8–15 percent of the animal. Keep the result mature, realistic, and readable rather than cute or photographic.
```

### V3：粗線印刷版

```text
Style variant V3 only: use exactly four output tones including paper white, a bold outer contour equivalent to 0.65–0.75 mm at final print size, large simplified tonal shapes, and virtually no internal texture. Species-identifying texture may cover no more than about 3 percent of the animal. Preserve the exact anatomy, action, pose, framing, scale, background, and ability effect of the V2 edit target; change only the tone treatment, contour weight, and texture density.
```

## 四種動物

### 非洲象：鼻子噴水

```text
Subject/action: an adult African savanna elephant with very large fan-shaped ears, two natural tusks, and four clearly separated weight-bearing legs. Pose it in a stable relaxed three-quarter stance, not charging. The trunk curves upward naturally with the tip pointing outward and expels one bold continuous arc of water from the trunk tip only. The arc ends in one small harmless splash on empty ground. Render the water as one continuous light-gray band with a medium-gray edge and only three to five large droplets; it must remain at least 1.2 mm wide at final print size. Keep the complete trunk, water arc, tusks, feet, and tail inside the crop-safe area. Mouth closed, calm eyes, ears relaxed.
Avoid: Asian-elephant ear proportions, water from the mouth or tusks, straight hose-like trunk, charging posture, frontal threat pose, fire, smoke, transparent mist, mud, other animals, extra limbs, duplicated tusks.
```

### 黑豹：暗夜飛撲

```text
Subject/action: a melanistic leopard with a lean powerful leopard build, not the heavier build of a jaguar. Show one believable airborne pounce across the frame: the body elongated horizontally, both forelegs reaching toward an empty landing area, both hind legs trailing naturally just after takeoff, the spine flexed smoothly, and one long tail extended for balance. Leave a clear gap between every paw and the ground. Turn the calm closed-mouth face slightly toward the empty landing area, not toward the viewer. Use several charcoal-gray body planes so the face, shoulders, belly, four legs, paws, and tail remain separate; retain only six to ten broad faint leopard-rosette groups. Add one very small pale crescent moon high in a corner as the only night cue while keeping the background paper white.
Avoid: black or night background, featureless black silhouette, jaguar body proportions, prey, chase, biting, impact, snarling, visible fangs, emphasized claws, flattened ears, extra limbs, duplicated tail, twisted spine.
```

### 河豚：膨脹毒球

```text
Subject/action: a true pufferfish, family Tetraodontidae, fully inflated by water into a rounded defensive body while preserving a clear head-to-tail fish shape. Keep two high-set lateral eyes, a small closed beak-like mouth, two small pectoral fins, one small dorsal fin and one anal fin near the tail, and a clearly separated tail fin; no pelvic fins. Use roughly twenty-four to thirty-two short tapered, well-separated representative silhouette prickles rather than dense needle-like spines, with clear gaps between their bases and only a few short internal prickles. Add only three to five large simple bubbles. Expression neutral and alert. Communicate inflation and defense only; do not visualize poison.
Avoid: porcupinefish-style long needles, dense hairlike spikes, sea-mine symmetry, missing tail or fins, extra pelvic fins, smiling face, huge cute eyes, cheeks, poison cloud, dripping venom, skull symbol, predators, victims.
```

### 行軍蟻：蟻海吞噬

```text
Subject/action: exactly twelve anatomically plausible army ants moving together across pale ground from left to right. Place one soldier ant in the foreground, only moderately larger than the workers, with enlarged curved defensive mandibles held relaxed rather than attacking. Make five other foreground workers fully readable and arrange six slightly smaller midground workers in two clean staggered rows. Every clearly visible ant has three body sections, a narrow waist, six jointed legs, and two antennae. The group flows naturally around and partly over one simple fallen leaf as a harmless scale cue. Use overlap and the flowing formation to suggest a much larger raid beyond the frame without adding tiny distant ants.
Avoid: queen, wings, giant leader ant, military rows, armor, weapons, flags, cartoon faces, oversized open jaws, prey, body parts, blood, hundreds of dots, black carpet, dense swarm texture, other animals.
```

## 檔名

| 動物 | V1 | V2 | V3 |
|---|---|---|---|
| 非洲象 | `v1/elephant.png` | `v2/elephant.png` | `v3/elephant.png` |
| 黑豹 | `v1/black-panther.png` | `v2/black-panther.png` | `v3/black-panther.png` |
| 河豚 | `v1/pufferfish.png` | `v2/pufferfish.png` | `v3/pufferfish.png` |
| 行軍蟻 | `v1/army-ant.png` | `v2/army-ant.png` | `v3/army-ant.png` |

輸出目錄：`card/images-print-style-test/`。

## 生成後檢查

- 縮至 114×70mm 後，仍能一眼說出動物與正在做的動作。
- 50% threshold 黑白預覽仍保有完整動物輪廓與能力效果。
- 黑豹不是整片黑色；河豚不是灰色毛球；行軍蟻不是黑點地毯；象鼻水柱不消失。
- 三版本之間只能看到灰階、輪廓與紋理差異，不能出現姿勢或構圖漂移。
- 所有圖都適合幼兒：不血腥、不恐怖、沒有受害者。
