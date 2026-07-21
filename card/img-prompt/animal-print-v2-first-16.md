# 動物卡 V2 首批 16 張正式 Prompt

> 日期：2026-07-20
> 用途：首批實體動物卡圖片與完整卡面試印
> 輸出：3:2 橫式、1536×1024、黑白雷射列印
> 定案：V2「圖鑑平衡版」；4 張既有定錨圖保留，另外產生 12 張

## 共用 V2 規格

每次產圖必須串接「共用 V2 規格＋該動物 Subject/action＋該動物 Avoid」。舊 SOP 的 `coloring book style`／`no shading` 後綴不再使用，因為會與 V2 五階灰階衝突。

```text
Use case: scientific-educational
Asset type: final 3:2 landscape animal artwork for a children's board-game card, printed about 114 by 70 mm on a monochrome laser printer
Input images: use the supplied approved V2 animal images only as references for grayscale treatment, contour weight, sparse texture, white background, and print readability; do not copy their species, pose, props, or composition
Primary request: create one simplified natural-history field-guide illustration. Make the named special-ability action understandable to a five-year-old from the animal's silhouette and one concrete cause-and-effect cue, without text or abstract symbols.
Style/medium: anatomically believable mature natural-history illustration, not photographic and not cute cartoon. Use exactly five discrete flat grayscale values including paper white, a medium print-safe outer contour equivalent to 0.45–0.50 mm at final size, broad readable body planes, and sparse species-identifying texture covering only 8–15 percent of the animal.
Composition/framing: 3:2 landscape, believable three-quarter side view, one clear motion direction. Keep the complete animal, every limb and appendage, and the complete ability effect inside the frame. The subject group occupies 70–75 percent of the longest image dimension with at least 8 percent clear crop-safe space on every edge.
Scene/backdrop: paper-white background with at most one minimal pale-gray grounding shape. No habitat scene or decorative background.
Print construction: discrete flat grayscale regions only. No smooth gradients, continuous-tone lighting, photographic grain, dense fur or skin microtexture, stippling, crosshatching, engraving marks, halftone screens, hairline detail, or large connected solid-black masses. Reserve solid black for the outer contour, pupils, and a few structural accents. Separate overlapping limbs and appendages with light negative-space gaps.
Child clarity: show only one action and one motion direction. Keep the expression calm and alert. No victim, injury, threat toward the viewer, horror, blood, prey, carcass, exposed teeth, attack impact, text, border, logo, or watermark.
```

## 1. 非洲獅（lion）— 雄獅怒吼

辨識特徵：

1. 成年雄獅完整環狀鬃毛
2. 尾端毛簇
3. 厚實胸肩與較平滑的身體輪廓

```text
Subject/action: one adult male African lion standing alone in a stable broad three-quarter side stance. Raise the head slightly and show the mouth naturally open in the middle of one powerful roar, with the complete circular mane lifting gently backward from the motion. Keep the lips and jaw readable but do not emphasize individual teeth. Show a muscular chest, four separated weight-bearing legs, rounded ears visible through the mane, and one long tail ending in a distinct tuft. The roar is communicated only by the open-mouth posture, raised head, expanded chest, and moving mane; add no sound-wave symbols.
Avoid: lioness, cub proportions, prey, opponent, chase, pounce, snarling at the viewer, bared fangs, oversized mouth, flattened ears, claws, sound rings, speed lines, extra legs, cropped mane or tail.
```

## 2. 非洲象（elephant）— 鼻子噴水｜既有 V2 定錨圖

辨識特徵：

1. 非洲草原象大型扇形耳朵
2. 兩根自然象牙
3. 長鼻與四隻承重腿

```text
Subject/action: an adult African savanna elephant with very large fan-shaped ears, two natural tusks, and four clearly separated weight-bearing legs. Pose it in a stable relaxed three-quarter stance, not charging. The trunk curves upward naturally with the tip pointing outward and expels one bold continuous arc of water from the trunk tip only. The arc ends in one small harmless splash on empty ground. Render the water as one continuous light-gray band with a medium-gray edge and only three to five large droplets. Keep the complete trunk, water arc, tusks, feet, and tail inside the crop-safe area. Mouth closed, calm eyes, ears relaxed.
Avoid: Asian-elephant ear proportions, water from the mouth or tusks, straight hose-like trunk, charging posture, frontal threat pose, fire, smoke, transparent mist, mud, other animals, extra limbs, duplicated tusks.
```

## 3. 獵豹（cheetah）— 極限衝刺

辨識特徵：

1. 眼角到嘴邊的淚痕
2. 纖細胸腰與特別長的腿
3. 小型實心圓斑與長尾

```text
Subject/action: one adult cheetah sprinting alone horizontally across the frame in a believable extended-gallop phase, with the long flexible spine smoothly stretched, both forelegs reaching forward, both hind legs extending backward, and every paw clearly separated. Turn the small calm closed-mouth head slightly toward the open running direction. Show distinct tear marks from the inner eyes toward the mouth, a deep chest and narrow waist, long slender legs, and one long balancing tail with a gentle counter-curve. Use sparse representative solid round spots rather than dense coat texture, plus four to six broad rings near the tail tip and one darker tail tip. Add only one small pale-gray sweep of dust behind the rear paws as the concrete speed cue.
Avoid: leopard or jaguar build, rosettes, prey, chase target, attack, open mouth, exposed teeth, claws, comic speed lines, multiple dust clouds, floating paws with impossible joints, duplicated legs or tail, cropped feet or tail.
```

## 4. 灣鱷（crocodile）— 巨鱷翻滾

辨識特徵：

1. 寬長吻部與眼鼻位於頭頂
2. 背部大型甲片
3. 粗壯長尾

```text
Subject/action: one adult saltwater crocodile alone in very shallow water, captured midway through one believable axial body roll without biting anything. Keep the head-to-tail centerline almost straight and horizontal across the landscape frame, with only one slight natural S-bend; the silhouette must read as a long crocodile, never as a circle. Rotate the head, shoulders, torso cross-section, and tail about sixty degrees together around that long axis, exposing one broad continuous lighter belly plane along the viewer-facing side while dorsal scutes remain visible along the opposite edge. Keep the jaws completely closed. Show exactly four correctly attached short legs: both viewer-facing legs clearly readable and the two far-side legs only partly visible, with pale gaps and correct front-to-rear positions. Wrap one broad pale-gray water ribbon once around the body axis: it passes behind the upper edge near the shoulders and reappears in front of the lower edge near the hips, making the roll direction concrete without forming a circle around the whole animal. Add only three to five large droplets. Emphasize the broad long snout, high-set eyes and nostrils, large dorsal scutes, and complete massive tail.
Avoid: C-shaped or U-shaped body, head and tail pointing toward each other, circular swimming turn, coiled crocodile, alligator-short snout, prey, victim, biting, torn object, open jaws, exposed teeth, blood, violent impact, helical spine, twisted vertebral column, legs attached to the back, more than four legs, detached legs, duplicated tail, full river scene, dense splash texture, attack toward the viewer.
```

## 5. 紅袋鼠（kangaroo）— 強腿飛踢

辨識特徵：

1. 特別粗壯的後腿與長腳掌
2. 粗長尾巴
3. 小型前肢與直立長耳

```text
Subject/action: one adult male red kangaroo alone in a controlled side-kick demonstration. Lean the torso diagonally backward while the thick tail and one supporting hind foot make two clearly separated ground-contact points. Extend the other powerful hind leg forward horizontally in one clear kick, so the overall silhouette is wider than it is tall. Keep both small forearms raised loosely near the chest for balance in a boxing-like posture, not striking. Show upright long ears, a narrow deer-like muzzle, a deep chest tapering to the waist, very muscular thighs, elongated feet, and the complete heavy tail. The calm closed-mouth face looks toward the empty kick direction.
Avoid: opponent, impact target, attack toward the viewer, vertical jump, single human-style hip rotation, crossed hind legs, human boxing gloves, clenched human fists, threatening face, extra legs, broken ankle angle, tail fused to a leg, cropped ears, feet or tail.
```

## 6. 長頸鹿（giraffe）— 長頸橫掃

辨識特徵：

1. 極長脖子
2. 頭頂成對 ossicones
3. 大塊多角形斑紋與長腿

```text
Subject/action: one adult giraffe alone in a wide stable three-quarter side stance, using its long neck in one controlled lateral sweeping motion. Keep all four long legs planted and separated, place the torso in the lower half of the frame, and make the torso occupy at least one third of the image width. Let the shoulders and chest lean slightly opposite the sweep. Swing the neck as one mostly straight heavy lever with only the giraffe's natural gentle S-curve, angled broadly across the upper half of the landscape frame. Keep the skull, jaw, and upper neck in one continuous anatomical alignment with the chin slightly tucked, both ossicones and both ears fully visible. Add exactly one broad pale-gray motion trail close behind the rear edge of the neck, ending before the head, so it cannot be mistaken for a second neck. Emphasize the sloping back, tall shoulders, long legs, tufted tail, and sparse large polygonal coat patches.
Avoid: another giraffe, opponent, neck collision, whip or rope, snake-like neck, flexible whip neck, sharp folded neck, spiral neck, head rotated independently from the upper neck, head detached from neck, second neck, kneeling, running, tiny body with oversized neck, cropped head, ossicones, hooves or tail, dense spot texture.
```

## 7. 海獺（sea_otter）— 石擊破殼

辨識特徵：

1. 圓頭、小耳與濃密鬍鬚
2. 寬大的後腳與較短的寬扁尾巴
3. 仰躺水面的招牌姿態

```text
Subject/action: one adult sea otter floating calmly on its back in a horizontal three-quarter side view. Place exactly one simple shell on the belly and exactly one smooth rounded stone in one forepaw raised just above it; the other forepaw steadies the shell. At final 114 by 70 mm print size, keep the stone at least 8 mm across, the shell at least 12 mm across, and the bold shell crack at least 0.6 mm wide. Preserve pale negative-space gaps between paw, stone, and shell. Show the stone at the end of one short downward tapping motion and one clear crack on the shell as the concrete cause-and-effect cue. Emphasize the rounded head, very small external ears, dense whiskers, compact forepaws, broad webbed hind feet, and one complete relatively short, broad, flattened tail tapering gently from the body, clearly shorter and less cylindrical than a river otter's tail. Use one minimal pale-gray oval water shape beneath the body. This is the approved two-object exception because both stone and shell are required to explain the ability.
Avoid: extra stones or shells, food pieces, open shellfish flesh, prey, blood, full ocean scene, kelp, waves, cute smile, huge eyes, human hammer grip, standing pose, long cylindrical river-otter tail, cropped paws, hind feet or tail.
```

## 8. 皇帝企鵝（emperor_penguin）— 極地潛行

辨識特徵：

1. 高而流線的身形
2. 小頭、短喙與短鰭狀翅
3. 清楚的腹部與背部對比色塊

```text
Subject/action: one adult emperor penguin swimming alone underwater in a fast shallow diagonal that reads mainly left-to-right across the landscape frame. Streamline the tall body almost horizontally, extend both short stiff flippers in a believable swimming stroke, and keep both feet parallel behind the body with a print-size pale gap of 1–2 mm between them. Turn the small head slightly toward the open swimming direction. Show a slender medium-long bill with a slight downward curve and one narrow print-safe pale-gray stripe along the lower mandible. Keep a smooth streamlined transition from the small head through the neck into the broad spindle-shaped torso, without a pinched neck. Separate the head, back, side-neck patches, and belly into large clean charcoal, medium-gray, light-gray, and paper-white planes; do not merge the head and back into one black mass. Add only three to five large simple bubbles behind the feet as the motion cue, with one minimal pale-gray water band.
Avoid: chick, standing pose, ice cliff, fish, prey, underwater chase, attack, open beak, short stubby beak, thick parrot-like beak, pinched narrow neck, extra flippers or feet, fused feet, human-like arms, vertical dive, large seascape, dense bubbles, photographic feathers, cropped beak, flippers or feet.
```

## 9. 大熊貓（giant_panda）— 鐵掌劈竹

辨識特徵：

1. 圓耳與眼周深色塊
2. 厚實肩胸與短尾
3. 前肢能以假拇指抓握竹子

```text
Subject/action: one adult giant panda seated alone in a stable three-quarter side pose, holding exactly one thick bamboo stalk horizontally with one forepaw and its visible pseudo-thumb. The other forepaw presses down firmly at the middle so the bamboo splits into two still-connected halves with one bold clean crack. Show rounded ears, distinct eye patches, a broad stocky head, heavy shoulders, thick forelimbs, compact hindquarters, and one small tail. Build the familiar coat pattern from separate medium and charcoal-gray planes with negative-space gaps; avoid connected black masses. Keep the mouth closed and expression focused.
Avoid: bamboo forest, extra stalks or leaves, eating pose, smiling cub face, oversized eyes, human hand, karate-chop gesture through empty air, flying fragments, violent impact lines, large solid-black body areas, extra paws, cropped ears, feet or bamboo.
```

## 10. 河豚（pufferfish）— 膨脹刺球｜既有 V2 定錨圖

辨識特徵：

1. 膨脹但仍保留頭尾方向的圓形身體
2. 短而分離的棘刺
3. 小嘴、側眼與靠近尾部的魚鰭

```text
Subject/action: a true pufferfish, family Tetraodontidae, fully inflated by water into a rounded defensive body while preserving a clear head-to-tail fish shape. Keep two high-set lateral eyes, a small closed beak-like mouth, two small pectoral fins, one small dorsal fin and one anal fin near the tail, and a clearly separated tail fin; no pelvic fins. Use roughly twenty-four to thirty-two short tapered, well-separated representative silhouette prickles rather than dense needle-like spines, with clear gaps between their bases and only a few short internal prickles. Add only three to five large simple bubbles. Expression neutral and alert. Communicate inflation and defense only; do not visualize poison.
Avoid: porcupinefish-style long needles, dense hairlike spikes, sea-mine symmetry, missing tail or fins, extra pelvic fins, smiling face, huge cute eyes, cheeks, poison cloud, dripping venom, skull symbol, predators, victims.
```

## 11. 紅毛猩猩（orangutan）— 巧手造物

辨識特徵：

1. 極長手臂與大型靈活手掌
2. 蓬鬆長毛
3. 成年雄性的寬大臉頰墊

```text
Subject/action: one adult male Bornean orangutan crouching alone in a forward-leaning three-quarter side pose. Hold exactly one straight print-safe stick, at least 1.2 mm wide at final size, delicately between the fingers of one large hand and insert its tip into one round 4–5 mm opening contained within the minimal pale-gray ground shape; the other long arm supports the body. On the tool-holding hand, show four long curved fingers and one shorter opposable thumb, but group overlaps into no more than three clearly separated foreground finger shapes so the hand remains readable after reduction. Keep the stick, fingers, opening, and direction of use clearly readable as deliberate tool use matching the card description. Emphasize very long arms, large dexterous hands, shaggy long body hair simplified into broad edge tufts, a broad adult male face framed by two broad flat anatomically proportionate lateral cheek flanges, one small visible pendulous throat pouch, short bowed legs, and grasping feet. The mouth is closed and the gaze is focused on the stick tip.
Avoid: insect, food, log, branch pile, umbrella, extra tools, forest scene, human clothing, human-like upright stance, gorilla proportions, gorilla sagittal crest, chimpanzee ears, unflanged juvenile face, oversized cheek flanges, cute smile, dense hair strands, more than five digits on either hand, extra fingers or limbs, cropped hands, feet or stick.
```

## 12. 黑豹（black_panther）— 暗夜飛撲｜既有 V2 定錨圖

辨識特徵：

1. 花豹的纖長體態
2. 深色毛皮中的淡玫瑰斑
3. 特別長的平衡尾巴

```text
Subject/action: a melanistic leopard with a lean powerful leopard build, not the heavier build of a jaguar. Show one believable airborne pounce across the frame: the body elongated horizontally, both forelegs reaching toward an empty landing area, both hind legs trailing naturally just after takeoff, the spine flexed smoothly, and one long tail extended for balance. Leave a clear gap between every paw and the ground. Turn the calm closed-mouth face slightly toward the empty landing area, not toward the viewer. Use several charcoal-gray body planes so the face, shoulders, belly, four legs, paws, and tail remain separate; retain only six to ten broad faint leopard-rosette groups. Add one very small pale crescent moon high in a corner as the approved anchor image's only background exception while keeping the background paper white; add no other night scenery.
Avoid: black or night background, featureless black silhouette, jaguar body proportions, prey, chase, biting, impact, snarling, visible fangs, emphasized claws, flattened ears, extra limbs, duplicated tail, twisted spine.
```

## 13. 變色龍（chameleon）— 瞬舌獵擊

辨識特徵：

1. 可分別轉動的砲塔狀眼睛
2. 對趾足與側扁身體
3. 頭冠、長舌與捲曲尾巴

```text
Subject/action: one adult veiled chameleon alone in a horizontal three-quarter side view, gripping exactly one plain branch at least 2 mm wide at final print size. Render each foot as two broad separated opposing toe bundles rather than dense individual toe lines. Aim one raised turret-shaped eye toward the tongue tip while the other turret remains turned slightly outward, compressing the animal's independent-eye behavior and tongue strike into one readable educational pose without crossed eyes. Extend the complete tongue rapidly and almost horizontally into empty space, at least 1.2 mm wide at final size, with one rounded sticky tip at least 3 mm across; keep the tongue entirely inside the frame. Emphasize the tall casque, laterally compressed body, sparse geometric scale groups, zygodactyl feet, and one complete tightly curled tail. The body remains stable while the tongue supplies the single motion direction.
Avoid: insect, prey, caught object, forest or leaves, color-change effect, camouflage background, smiling cartoon face, frog-like tongue, multiple tongues, both eyes looking away from the tongue, crossed eyes, ordinary lizard feet, dense individual toe lines, missing toes, extra legs, uncurling or cropped tail, cropped tongue tip.
```

## 14. 蜂鳥（hummingbird）— 懸停疾閃

辨識特徵：

1. 細長筆直嘴喙
2. 極小緊湊身體
3. 尖長翅膀與收起的小腳

```text
Subject/action: one adult hummingbird hovering alone in a clean horizontal side view, body level and perfectly stationary in the center while a long straight slender bill with a clearly print-safe filled width and clean closed tip points toward open space. Show exactly one pair of long narrow wings angled outward and slightly backward in a believable high upstroke, fully separated from the body, with the complete wingspan wider than it is tall. Add exactly one broad featherless pale-gray motion crescent immediately behind the trailing edge of each real wing, two crescents total. Keep each crescent visually distinct from the anatomical wing, without feather structure, to communicate rapid repeated wingbeats without creating extra wings. Emphasize the compact body, small head, long bill, tiny feet tucked close to the belly, a short fan-shaped tail, and one restrained throat-texture patch. Keep the calm eye and closed bill readable.
Avoid: flower, feeder, insect, extra wing pairs, ghost wings, more than two motion crescents total, feather details inside motion crescents, dense motion blur, comic speed lines, hairline bill, vertical body, perched pose, oversized cute head or eyes, open bill, long legs, cropped bill, wings or tail, full garden scene.
```

## 15. 金剛鸚鵡（scarlet_macaw）— 彩喙破殼

辨識特徵：

1. 巨大彎曲上喙
2. 裸露面部區與厚實下喙
3. 特別長的尖尾羽

```text
Subject/action: one adult scarlet macaw standing alone in a stable three-quarter side pose on one foot while the other zygodactyl foot grips exactly one large round hard nut near the beak. Close the massive curved upper beak firmly onto the shell and show one bold clean crack at least 0.6 mm wide at final print size spreading from the contact point, with no flying fragments. Keep both wings folded against the body and arrange the complete very long pointed tail diagonally across the landscape frame. Emphasize the bare facial patch around the calm eye, thick lower beak, layered wing planes, gripping toes, and long graduated tail feathers. Build the feathers from three broad non-white gray values plus paper white and a few structural black accents, for exactly five output values total; do not rely on color names.
Avoid: branch, extra nuts, food pieces, prey, open mouth, exposed tongue, smiling cartoon face, human speech symbols, flying shell fragments, spread wings, dense feather lines, extra toes, clipped beak, feet, wings or tail.
```

## 16. 行軍蟻（army_ant）— 蟻群行軍｜既有 V2 定錨圖

辨識特徵：

1. 兵蟻大型彎曲大顎
2. 三節身體與細腰
3. 多隻個體形成連續行軍流向

```text
Subject/action: exactly twelve anatomically plausible army ants moving together across pale ground from left to right. Place one soldier ant in the foreground, only moderately larger than the workers, with enlarged curved defensive mandibles held relaxed rather than attacking. Make five other foreground workers fully readable and arrange six slightly smaller midground workers in two clean staggered rows. Every clearly visible ant has three body sections, a narrow waist, six jointed legs, and two antennae. The group flows naturally around and partly over one simple fallen leaf as a harmless scale cue. Use overlap and the flowing formation to suggest a much larger raid beyond the frame without adding tiny distant ants.
Avoid: queen, wings, giant leader ant, military rows, armor, weapons, flags, cartoon faces, oversized open jaws, prey, body parts, blood, hundreds of dots, black carpet, dense swarm texture, other animals.
```

## 生成後共通 QA

- 動物與能力動作在 114×70mm 仍可一眼辨識。
- 完整身體、能力效果與 8% crop-safe margin 都保留。
- 五階灰階與中粗輪廓接近 4 張 V2 定錨圖。
- 50% threshold 預覽仍保有動物輪廓、主要特徵與能力因果。
- 不出現多餘肢體、錯誤物種特徵、受害者、血腥或文字。

## 審核紀錄

| 動物 | A 技能動作 | B 物種解剖 | C 構圖印刷 | 結果 |
|---|:---:|:---:|:---:|---|
| 非洲獅 | ✅ | ✅ | ✅ | 通過 |
| 非洲象 | ✅ | ✅ | ✅ | 既有 V2 定錨圖通過 |
| 獵豹 | ✅ | ✅ | ✅ | 補強尾端環紋後通過 |
| 灣鱷 | ⚠️→✅ | ⚠️→✅ | ⚠️→✅ | 改為整體軸向翻滾、淺 C 曲線與近遠側腿分層；依使用者確認維持無咬合物件 |
| 紅袋鼠 | ✅ | ⚠️→✅ | ⚠️→✅ | 移除 `tripod`，明定尾巴＋支撐腳兩接地點；依使用者確認維持單腿踢 |
| 長頸鹿 | ⚠️→✅ | ⚠️→✅ | ⚠️→✅ | 改為大致筆直的重槓桿、身體反向傾斜與單一道動態尾跡 |
| 海獺 | ✅ | ⚠️→✅ | ⚠️→✅ | 修正較短寬扁尾，放大石頭、貝殼與裂紋 |
| 皇帝企鵝 | ✅ | ⚠️→✅ | ⚠️→✅ | 修正嘴喙、平滑頭頸與雙腳負空間 |
| 大熊貓 | ✅ | ✅ | ✅ | 通過 |
| 河豚 | ✅ | ✅ | ✅ | 既有 V2 定錨圖通過 |
| 紅毛猩猩 | ⚠️→✅ | ⚠️→✅ | ⚠️→✅ | 強化成年雄性臉頰瓣、手指與印刷尺寸；依使用者確認維持樹枝探洞，對應 skillDesc 的工具使用 |
| 黑豹 | ✅ | ✅ | ⚠️→✅ | 標記小月亮為既有定錨圖唯一背景例外 |
| 變色龍 | ✅ | ⚠️→✅ | ⚠️→✅ | 一眼對準舌端、另一眼略向外，並放大舌頭、舌尖、樹枝與趾束 |
| 蜂鳥 | ✅ | ⚠️→✅ | ⚠️→✅ | 限定一對真翅與總共兩道無羽毛動態弧，補強嘴喙線寬 |
| 金剛鸚鵡 | ✅ | ✅ | ⚠️→✅ | 修正總灰階數並放大果殼裂紋 |
| 行軍蟻 | ⚠️→✅ | ✅ | ✅ | 既有 V2 定錨圖已通過實體風格比較；依使用者確認保留繞過／跨過落葉構圖 |

### 修正項目

| 類型 | 修正內容 |
|---|---|
| Prompt 組裝 | 明定每次使用共用 V2 規格＋Subject/action＋Avoid，淘汰舊 `no shading` 後綴 |
| 解剖 | 灣鱷改軸向翻滾；長頸鹿改重槓桿頸；海獺改短寬尾；皇帝企鵝修正嘴喙與頭頸 |
| 動作 | 強化長頸鹿橫掃、灣鱷旋轉方向與紅袋鼠兩接地點；保留已確認的後腿前踢與探洞概念 |
| 物種辨識 | 獵豹補尾環；紅毛猩猩補臉頰瓣；變色龍眼睛採教育性壓縮姿勢 |
| 縮印 | 放大海獺道具、紅毛猩猩樹枝與洞、變色龍舌頭與樹枝、金剛鸚鵡裂紋 |
| 多肢風險 | 灣鱷明定近遠側腿；蜂鳥限制一對真翅與兩道動態弧；趾與手指改用寬形群組 |
| 五階灰階 | 金剛鸚鵡改為紙白＋三灰＋少量結構黑；黑豹月亮列為既有定錨圖例外 |

## 生成圖 QA 紀錄

> 2026-07-20：Reviewer A 檢查能力動作、Reviewer B 檢查物種／解剖、Reviewer C 檢查構圖／黑白縮印／兒童適性。

| 動物 | 能力動作 | 物種解剖 | 縮印構圖 | 結果 |
|---|:---:|:---:|:---:|---|
| 非洲獅 | ✅ | ✅ | ✅ | 通過 |
| 非洲象 | ✅ | ✅ | ✅ | 沿用既有 V2 定錨圖 |
| 獵豹 | ✅ | ✅ | ✅ | 通過 |
| 灣鱷 | ❌→✅ | ⚠️→✅ | ⚠️→✅ | 初稿像繞圈游泳；重生為頭尾近水平、腹面朝向觀者的軸向翻滾，再移除箭頭與露齒，三方複核通過 |
| 紅袋鼠 | ✅ | ✅ | ✅ | 初稿移除多餘速度線後通過 |
| 長頸鹿 | ⚠️ | ⚠️ | ⚠️ | 可進實測；觀察淺灰動態尾跡在黑白雷射列印後是否仍可見 |
| 海獺 | ✅ | ⚠️ | ✅ | 可進實測；前掌略像拳頭但石擊破殼因果清楚 |
| 皇帝企鵝 | ✅ | ✅ | ✅ | 通過 |
| 大熊貓 | ✅ | ✅ | ✅ | 通過 |
| 河豚 | ✅ | ✅ | ✅ | 沿用既有 V2 定錨圖 |
| 紅毛猩猩 | ⚠️ | ⚠️ | ✅ | 可進實測；依定案以 skillDesc 的工具使用為準，抓握足仍可沿腿部辨認 |
| 黑豹 | ✅ | ✅ | ✅ | 沿用既有 V2 定錨圖 |
| 變色龍 | ✅ | ✅ | ✅ | 初稿移除多餘速度線後通過 |
| 蜂鳥 | ✅ | ✅ | ✅ | 一對真翅與兩道動態弧可清楚區分 |
| 金剛鸚鵡 | ✅ | ⚠️ | ✅ | 縮小並重新置中後通過；持物腳趾稍密但不影響辨識 |
| 行軍蟻 | ⚠️ | ✅ | ✅ | 沿用既有 V2 定錨圖；群體行軍讀得到，實測觀察「吞噬」語意 |

### 實體試印觀察項目

1. 長頸鹿的淺灰頸部動態尾跡是否仍可見。
2. 灣鱷背甲細節是否糊成灰塊，腹面翻轉是否仍能讀出。
3. 紅毛猩猩的抓握足會不會被誤看成第三隻手。
4. 行軍蟻是否只能讀成「行軍」，無法聯想到群體淹沒。
