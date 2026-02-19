/**
 * 動物猜猜看 — 提示資料庫（MVP 25 隻）
 *
 * 每隻動物有：
 *   hints: [提示1, 提示2, 提示3]  — 由廣到窄，越來越明確
 *   groups: [分組標籤]            — 用於挑選干擾選項
 */

// ===== 干擾選項分組 =====
// 同組的動物容易混淆，適合當干擾選項
export const DISTRACTOR_GROUPS = {
  big_cats:        ['lion', 'cheetah', 'tiger'],
  african_large:   ['elephant', 'giraffe', 'hippopotamus', 'rhinoceros'],
  bears:           ['polar_bear', 'giant_panda', 'brown_bear'],
  ocean:           ['dolphin', 'orca', 'great_white_shark', 'blue_whale'],
  birds:           ['owl', 'emperor_penguin', 'ostrich', 'peacock'],
  reptiles:        ['komodo', 'chameleon'],
  unique_mammals:  ['pangolin', 'platypus', 'sloth', 'badger', 'kangaroo'],
  african:         ['lion', 'cheetah', 'elephant', 'giraffe', 'hippopotamus', 'rhinoceros'],
  swimmers:        ['dolphin', 'orca', 'great_white_shark', 'blue_whale', 'polar_bear', 'hippopotamus', 'platypus', 'emperor_penguin'],
  nocturnal:       ['owl', 'badger', 'pangolin'],
  armored:         ['pangolin', 'rhinoceros', 'komodo'],
  cute:            ['giant_panda', 'dolphin', 'sloth', 'kangaroo', 'emperor_penguin'],
  large:           ['elephant', 'hippopotamus', 'rhinoceros', 'brown_bear', 'polar_bear', 'blue_whale', 'orca', 'giraffe'],
  fast:            ['cheetah', 'ostrich', 'dolphin', 'kangaroo', 'lion'],
  cold:            ['polar_bear', 'emperor_penguin', 'owl'],
  australian:      ['kangaroo', 'platypus'],
};

// ===== 25 隻動物提示資料 =====
export const HINTS = {
  // --- 貓科 ---
  lion: {
    hints: [
      '我住在非洲的大草原上，是跟一大群家人住在一起的動物',
      '在我們家，媽媽負責打獵，爸爸負責保護大家',
      '我爸爸的脖子周圍有一圈又厚又帥的毛，叫做「鬃毛」',
    ],
    groups: ['big_cats', 'african', 'large', 'fast'],
  },
  cheetah: {
    hints: [
      '我住在非洲草原，身上有很多小圓黑點',
      '我是地球上跑得最快的動物，比汽車起步還快！',
      '我的眼睛下面有兩條黑色的線，像哭過的淚痕',
    ],
    groups: ['big_cats', 'african', 'fast'],
  },
  tiger: {
    hints: [
      '我是貓科家族裡體型最大的成員',
      '我跟其他大貓不一樣，我超愛游泳！',
      '我身上有橘色和黑色的條紋，每一隻的花紋都不一樣',
    ],
    groups: ['big_cats', 'large', 'swimmers'],
  },

  // --- 非洲大型 ---
  elephant: {
    hints: [
      '我是陸地上體型最大的動物',
      '我的記憶力超好，走過的路幾十年都記得',
      '我有一根長長的鼻子，可以用來喝水、打招呼和洗澡',
    ],
    groups: ['african_large', 'african', 'large'],
  },
  giraffe: {
    hints: [
      '我是世界上最高的動物，住在非洲',
      '我的舌頭是深紫色的，可以伸得超長來捲樹葉吃',
      '我的脖子超～級長，連喝水都要劈開前腿彎下去',
    ],
    groups: ['african_large', 'african', 'large'],
  },
  hippopotamus: {
    hints: [
      '我住在非洲的河流跟湖泊裡，大部分時間都泡在水中',
      '別看我胖胖的，我在陸地上跑得比人還快喔！',
      '我可以把嘴巴張到超級超級大，張開將近 150 度',
    ],
    groups: ['african_large', 'african', 'large', 'swimmers'],
  },
  rhinoceros: {
    hints: [
      '我是非洲草原上的大塊頭，皮膚超級厚像穿了盔甲',
      '我的眼睛很小看不太清楚，但鼻子和耳朵超靈敏',
      '我的鼻子上面長了一根或兩根很硬的角',
    ],
    groups: ['african_large', 'african', 'large', 'armored'],
  },

  // --- 熊 ---
  polar_bear: {
    hints: [
      '我住在地球最北邊，那裡到處都是冰和雪',
      '我是游泳高手，可以在冰冷的海裡游好幾個小時',
      '我的毛看起來是白色的，但其實皮膚是黑色的喔！',
    ],
    groups: ['bears', 'large', 'swimmers', 'cold'],
  },
  giant_panda: {
    hints: [
      '我是熊的家族成員，住在高高的山上',
      '我幾乎只吃一種植物，每天要花十幾個小時吃東西',
      '我是黑白配色的大胖子，超愛吃竹子',
    ],
    groups: ['bears', 'cute', 'large'],
  },
  brown_bear: {
    hints: [
      '我體型很大，冬天會躲起來睡覺好幾個月不吃東西',
      '我最喜歡站在瀑布旁邊，等魚跳起來時一口接住',
      '我全身棕色毛茸茸的，背上有一個明顯的隆起',
    ],
    groups: ['bears', 'large', 'swimmers'],
  },

  // --- 海洋 ---
  dolphin: {
    hints: [
      '我住在海裡，但我不是魚喔，我需要浮上來呼吸空氣',
      '我會用超音波找東西，就像蝙蝠一樣',
      '我的嘴巴看起來一直在微笑，而且我超級聰明會表演特技',
    ],
    groups: ['ocean', 'swimmers', 'cute', 'fast'],
  },
  orca: {
    hints: [
      '我住在海裡，是海洋食物鏈最頂端的獵食者',
      '我會跟家人一起合作打獵，還會教小孩捕獵技巧',
      '我身上是黑白兩色，眼睛旁邊有白色的橢圓斑塊',
    ],
    groups: ['ocean', 'swimmers', 'large'],
  },
  great_white_shark: {
    hints: [
      '我住在海裡，幾乎所有海洋動物看到我都會閃開',
      '我的牙齒掉了會再長新的，一輩子可以換好幾千顆',
      '我是灰白色的，嘴巴裡有好幾排三角形的尖牙，電影裡超有名',
    ],
    groups: ['ocean', 'swimmers', 'large', 'fast'],
  },
  blue_whale: {
    hints: [
      '我是地球上有史以來最大的動物，比恐龍還大',
      '光是我的心臟就跟一輛小汽車差不多大',
      '我是藍灰色的，頭頂有個噴氣孔可以噴出好高的水柱',
    ],
    groups: ['ocean', 'swimmers', 'large'],
  },

  // --- 鳥類 ---
  owl: {
    hints: [
      '我是晚上才出來活動的鳥，白天都在睡覺',
      '我飛行的時候完全沒有聲音，獵物根本聽不到我來了',
      '我有一雙超大的圓眼睛，脖子可以轉到幾乎正後方',
    ],
    groups: ['birds', 'nocturnal'],
  },
  emperor_penguin: {
    hints: [
      '我是一種鳥，但完全不會飛，住在地球上最冷的地方',
      '在我們家是爸爸把蛋放在腳上孵化，站著不動好幾個月',
      '我穿著像燕尾服一樣的黑白衣服，是全世界最大的企鵝',
    ],
    groups: ['birds', 'swimmers', 'cold', 'cute'],
  },
  ostrich: {
    hints: [
      '我是全世界最大的鳥，但是不會飛',
      '我的蛋也是世界上最大的，一顆就有二十幾顆雞蛋那麼重',
      '我有兩條超長的腿，跑起來比馬還快',
    ],
    groups: ['birds', 'african', 'fast'],
  },
  peacock: {
    hints: [
      '我是一種非常漂亮的鳥，雄性和雌性長得差很多',
      '我的羽毛上有像眼睛一樣的圓形花紋',
      '我會把超長的尾巴展開成一把大扇子，叫做「開屏」',
    ],
    groups: ['birds'],
  },

  // --- 爬蟲 ---
  komodo: {
    hints: [
      '我是現存爬蟲類裡體型最大的，住在一座熱帶小島上',
      '我的口水裡有很多細菌和毒素，被咬到非常危險',
      '我看起來就像一隻活生生的小恐龍，住在印尼的島上',
    ],
    groups: ['reptiles', 'armored', 'large'],
  },
  chameleon: {
    hints: [
      '我是一種很特別的爬蟲類，住在樹上',
      '我的兩隻眼睛可以各看不同方向，一隻看前面一隻看後面',
      '我最厲害的是皮膚可以隨著心情和環境改變顏色',
    ],
    groups: ['reptiles'],
  },

  // --- 特色哺乳類 ---
  pangolin: {
    hints: [
      '我是全世界唯一一種全身覆蓋硬鱗片的哺乳類動物',
      '遇到危險我會把自己捲成一顆球，連獅子都咬不開',
      '我沒有牙齒，用超長的舌頭伸進蟻窩裡舔螞蟻吃',
    ],
    groups: ['unique_mammals', 'nocturnal', 'armored'],
  },
  platypus: {
    hints: [
      '我住在澳洲的小溪裡，是地球上最奇怪的動物之一',
      '我是哺乳類但是會下蛋！而且公的後腳還有毒刺',
      '我的嘴巴像鴨子、尾巴像海狸、腳掌像水獺，像拼裝出來的',
    ],
    groups: ['unique_mammals', 'swimmers', 'australian'],
  },
  sloth: {
    hints: [
      '我住在熱帶雨林的樹上，幾乎不會下到地面',
      '我身上會長出綠色的藻類，讓我和樹葉融為一體',
      '我是世界上動作最慢的哺乳類，一整天都掛在樹上不太動',
    ],
    groups: ['unique_mammals', 'cute'],
  },
  badger: {
    hints: [
      '我體型不大，但是超級兇，什麼動物我都不怕',
      '被毒蛇咬了我也沒事，因為我對毒液有天生的抵抗力',
      '我最愛吃蜂蜜了，連蜜蜂螫我我都不在乎',
    ],
    groups: ['unique_mammals', 'nocturnal', 'african'],
  },
  kangaroo: {
    hints: [
      '我住在澳洲，是那裡最有名的動物之一',
      '我的寶寶出生時只有花生那麼小，要在口袋裡養好幾個月',
      '我用兩條超強壯的後腿跳著移動，還會用尾巴撐地站起來',
    ],
    groups: ['unique_mammals', 'fast', 'cute', 'australian'],
  },
};

// ===== MVP 動物 ID 清單 =====
export const MVP_ANIMAL_IDS = Object.keys(HINTS);
