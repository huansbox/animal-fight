/**
 * 動物猜猜看 — 提示資料庫（55 隻）
 *
 * 每隻動物有：
 *   hints: [提示1, 提示2, 提示3]  — 由廣到窄，越來越明確
 *   groups: [分組標籤]            — 用於挑選干擾選項
 */

// ===== 干擾選項分組 =====
// 同組的動物容易混淆，適合當干擾選項
export const DISTRACTOR_GROUPS = {
  big_cats:        ['lion', 'cheetah', 'tiger', 'jaguar', 'snow_leopard'],
  african_large:   ['elephant', 'giraffe', 'hippopotamus', 'rhinoceros', 'gorilla', 'zebra'],
  bears:           ['polar_bear', 'giant_panda', 'brown_bear', 'gorilla'],
  ocean:           ['dolphin', 'orca', 'great_white_shark', 'blue_whale', 'humpback_whale', 'sea_turtle', 'jellyfish', 'walrus', 'sea_otter', 'electric_eel'],
  birds:           ['owl', 'emperor_penguin', 'ostrich', 'peacock', 'bald_eagle', 'hummingbird', 'scarlet_macaw', 'red_crowned_crane', 'falcon'],
  reptiles:        ['komodo', 'chameleon', 'crocodile', 'anaconda', 'sea_turtle'],
  unique_mammals:  ['pangolin', 'platypus', 'sloth', 'badger', 'kangaroo', 'armadillo', 'hedgehog', 'porcupine', 'wombat'],
  african:         ['lion', 'cheetah', 'elephant', 'giraffe', 'hippopotamus', 'rhinoceros', 'gorilla', 'zebra', 'hyena'],
  swimmers:        ['dolphin', 'orca', 'great_white_shark', 'blue_whale', 'polar_bear', 'hippopotamus', 'platypus', 'emperor_penguin', 'sea_turtle', 'walrus', 'sea_otter', 'crocodile', 'humpback_whale', 'electric_eel'],
  nocturnal:       ['owl', 'badger', 'pangolin', 'raccoon', 'arctic_fox'],
  armored:         ['pangolin', 'rhinoceros', 'komodo', 'armadillo', 'porcupine', 'hedgehog', 'crocodile'],
  cute:            ['giant_panda', 'dolphin', 'sloth', 'kangaroo', 'emperor_penguin', 'red_panda', 'koala', 'sea_otter', 'hedgehog', 'wombat', 'arctic_fox'],
  large:           ['elephant', 'hippopotamus', 'rhinoceros', 'brown_bear', 'polar_bear', 'blue_whale', 'orca', 'giraffe', 'gorilla', 'moose', 'walrus', 'humpback_whale', 'crocodile', 'anaconda'],
  fast:            ['cheetah', 'ostrich', 'dolphin', 'kangaroo', 'lion', 'falcon', 'hummingbird', 'jaguar'],
  cold:            ['polar_bear', 'emperor_penguin', 'owl', 'arctic_fox', 'moose', 'snow_leopard', 'walrus'],
  australian:      ['kangaroo', 'platypus', 'koala', 'wombat'],
  primates:        ['gorilla', 'chimpanzee'],
  canines:         ['gray_wolf', 'arctic_fox', 'hyena', 'raccoon'],
  snakes:          ['anaconda', 'king_cobra'],
  ocean_mammals:   ['dolphin', 'orca', 'blue_whale', 'humpback_whale', 'walrus', 'sea_otter'],
  raptors:         ['bald_eagle', 'falcon', 'owl'],
  colorful:        ['peacock', 'scarlet_macaw', 'hummingbird', 'chameleon'],
  desert:          ['camel', 'scorpion', 'armadillo'],
  spiky:           ['hedgehog', 'porcupine', 'armadillo'],
  south_america:   ['jaguar', 'anaconda', 'armadillo', 'sloth'],
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

  // ===== 第二波 30 隻 =====

  // --- 貓科追加 ---
  jaguar: {
    hints: [
      '我是美洲最大的貓科動物，住在中南美洲的雨林裡',
      '我的咬合力在貓科裡排第一，可以直接咬穿烏龜殼',
      '我身上的花紋不是圓點，而是像玫瑰花一樣的「梅花斑」',
    ],
    groups: ['big_cats', 'south_america', 'large', 'fast', 'swimmers'],
  },
  snow_leopard: {
    hints: [
      '我住在亞洲最高的山脈上，海拔三千到五千公尺',
      '我的尾巴超級長又蓬鬆，冷的時候會拿來蓋住鼻子取暖',
      '我全身是灰白色加黑色斑點，被稱為「雪山之王」',
    ],
    groups: ['big_cats', 'cold'],
  },

  // --- 靈長類 ---
  gorilla: {
    hints: [
      '我住在非洲的熱帶森林裡，是地球上最大的靈長類',
      '我們的領袖背上的毛會變成銀色，大家叫他「銀背」',
      '我看起來很兇，但其實是溫柔的素食主義者，最愛吃葉子和水果',
    ],
    groups: ['primates', 'african', 'large'],
  },
  chimpanzee: {
    hints: [
      '我的 DNA 跟人類有 98% 一樣，是人類最親近的動物',
      '我會自己做工具！會用樹枝去釣白蟻出來吃',
      '我住在非洲的森林裡，會互相幫對方抓背上的蟲子',
    ],
    groups: ['primates', 'african'],
  },

  // --- 犬科 / 鬣狗 ---
  gray_wolf: {
    hints: [
      '我們是團隊合作的高手，整群家人一起打獵',
      '到了晚上，我會仰頭對著月亮發出長長的聲音',
      '我是狗狗的祖先！所有的狗都是從我們馴化來的',
    ],
    groups: ['canines', 'cold'],
  },
  arctic_fox: {
    hints: [
      '我住在北極圈附近，零下五十度我也不怕冷',
      '冬天的時候我的毛會變成全白，在雪地裡完美隱身',
      '我有一張超可愛的圓臉和一條蓬蓬的大尾巴，耳朵小小圓圓的',
    ],
    groups: ['canines', 'cold', 'cute', 'nocturnal'],
  },
  hyena: {
    hints: [
      '我住在非洲草原，常常被誤以為是狗，但其實跟貓比較近親',
      '我的叫聲很奇特，聽起來好像在大笑一樣',
      '我的下巴超級有力，可以把骨頭直接咬碎吞下去',
    ],
    groups: ['canines', 'african'],
  },

  // --- 海洋追加 ---
  humpback_whale: {
    hints: [
      '我是海洋裡的大個子，每年都會游好幾千公里遷移',
      '我會唱歌！我的歌聲可以傳到幾百公里之外',
      '我最有名的動作就是跳出海面再重重摔回水裡，超壯觀',
    ],
    groups: ['ocean', 'ocean_mammals', 'swimmers', 'large'],
  },
  sea_turtle: {
    hints: [
      '我住在海裡，但是媽媽要上岸到沙灘上生蛋',
      '我可以活超過一百年，慢慢地在海裡游一輩子',
      '我背上有一個大大的殼，用四片像船槳一樣的鰭在海裡游泳',
    ],
    groups: ['ocean', 'reptiles', 'swimmers', 'armored'],
  },
  walrus: {
    hints: [
      '我住在北極附近的冰冷海域，喜歡跟一大群朋友擠在一起',
      '我厚厚的脂肪有十幾公分，幫我在冰水裡保暖',
      '我有兩根長長的象牙從嘴巴伸出來，還有一臉帥氣的大鬍鬚',
    ],
    groups: ['ocean', 'ocean_mammals', 'swimmers', 'cold', 'large'],
  },
  sea_otter: {
    hints: [
      '我住在太平洋沿岸的海裡，大部分時間都仰躺著漂在水面上',
      '睡覺的時候我會跟同伴手牽手，這樣才不會被海流沖散',
      '我會把石頭放在肚子上，拿來敲開貝殼吃裡面的肉',
    ],
    groups: ['ocean', 'ocean_mammals', 'swimmers', 'cute'],
  },
  jellyfish: {
    hints: [
      '我住在海裡，但我沒有大腦、沒有心臟、也沒有血',
      '我的身體幾乎是透明的，百分之九十五都是水',
      '我有長長的觸手會螫人，身體像一把漂浮的雨傘',
    ],
    groups: ['ocean', 'swimmers'],
  },
  electric_eel: {
    hints: [
      '我住在南美洲的河流裡，看起來像蛇但其實是魚',
      '我能放出超強的電，足夠讓一匹馬倒下',
      '我全身像電池一樣會發電，最高可以放出 860 伏特',
    ],
    groups: ['ocean', 'swimmers', 'south_america'],
  },

  // --- 鳥類追加 ---
  bald_eagle: {
    hints: [
      '我是一種大型猛禽，最愛抓魚來吃',
      '我是一個很有名的國家的國鳥，印在他們的錢幣上',
      '我的頭上有一片雪白的羽毛，身體是深棕色的，看起來好像禿頭',
    ],
    groups: ['birds', 'raptors'],
  },
  falcon: {
    hints: [
      '我是一種猛禽，從高空俯衝下來抓獵物',
      '我俯衝的速度是地球上所有動物裡最快的，超過時速 300 公里',
      '我的名字跟「遊」有關，因為我總是在天空中巡遊',
    ],
    groups: ['birds', 'raptors', 'fast'],
  },
  hummingbird: {
    hints: [
      '我是世界上最小的鳥類之一，體重比一個硬幣還輕',
      '我的翅膀一秒可以拍超過五十次，快到人眼看不清楚',
      '我是唯一可以在空中倒退飛和懸停的鳥，像直升機一樣',
    ],
    groups: ['birds', 'fast', 'colorful'],
  },
  scarlet_macaw: {
    hints: [
      '我住在中南美洲的熱帶雨林裡，是一種大型的鳥',
      '我超級聰明，可以學會說人類的話',
      '我全身是鮮紅色、黃色、藍色的羽毛，像彩虹一樣繽紛',
    ],
    groups: ['birds', 'colorful', 'south_america'],
  },
  red_crowned_crane: {
    hints: [
      '我是一種非常優雅的大型鳥類，走路像在跳舞',
      '在東方文化裡，我代表長壽和幸運',
      '我的頭頂有一塊鮮紅色的皮膚，身體是白色配黑色的',
    ],
    groups: ['birds'],
  },

  // --- 爬蟲 / 蛇追加 ---
  crocodile: {
    hints: [
      '我是一種非常古老的爬蟲類，恐龍時代就存在了',
      '我可以在水裡只露出眼睛和鼻孔，等獵物靠近再一口咬住',
      '我的嘴巴超長，咬合力是地球上所有動物裡最強的',
    ],
    groups: ['reptiles', 'swimmers', 'large', 'armored'],
  },
  anaconda: {
    hints: [
      '我住在南美洲的沼澤和河流裡，大部分時間待在水中',
      '我沒有毒，靠超強的身體把獵物纏住讓他不能呼吸',
      '我是世界上最重的蛇，可以長到超過五公尺',
    ],
    groups: ['reptiles', 'snakes', 'swimmers', 'large', 'south_america'],
  },
  king_cobra: {
    hints: [
      '我是世界上最長的毒蛇，可以長到五公尺以上',
      '我發怒的時候會把身體前段撐起來站得很高',
      '我的脖子兩邊可以展開成一片扁扁的「頭巾」，看起來超帥超可怕',
    ],
    groups: ['reptiles', 'snakes'],
  },

  // --- 特色哺乳類追加 ---
  raccoon: {
    hints: [
      '我晚上才出來活動，什麼東西都吃，垃圾桶也會翻',
      '我的前爪跟人的手一樣靈活，什麼蓋子都打得開',
      '我的臉上有一條黑色的帶狀花紋，看起來像戴了面具',
    ],
    groups: ['nocturnal', 'canines', 'cute'],
  },
  koala: {
    hints: [
      '我住在澳洲，一天要睡將近二十個小時',
      '我只吃一種樹的葉子，而且那種葉子對大部分動物有毒',
      '我有圓圓的耳朵和大大的鼻子，抱著尤加利樹睡覺超可愛',
    ],
    groups: ['australian', 'cute'],
  },
  red_panda: {
    hints: [
      '我跟大熊貓名字很像，但我們其實一點都不像',
      '我住在亞洲的高山竹林裡，也愛吃竹子',
      '我全身是紅棕色的，有一條蓬蓬的長尾巴，跟貓咪差不多大',
    ],
    groups: ['cute', 'cold'],
  },
  hedgehog: {
    hints: [
      '我是一種很小的哺乳類，遇到危險會縮成一顆球',
      '我背上有超過五千根尖刺，但肚子的毛是軟軟的',
      '我在電玩遊戲裡有一個跑超快的藍色角色，跟我同名',
    ],
    groups: ['spiky', 'cute', 'nocturnal', 'armored', 'unique_mammals'],
  },
  porcupine: {
    hints: [
      '我全身長滿了尖尖的硬刺，任何想吃我的動物都會被戳到',
      '我的刺尖端有倒鉤，扎進去就很難拔出來',
      '我是齧齒類動物，跟老鼠是遠親，但我背上的刺可以超過 30 公分',
    ],
    groups: ['spiky', 'armored', 'unique_mammals', 'nocturnal'],
  },
  armadillo: {
    hints: [
      '我住在美洲，身上穿著像盔甲一樣的硬殼保護自己',
      '有些品種遇到危險可以把自己捲成一顆完美的圓球',
      '我的殼是一片一片的骨板，看起來像穿了中世紀的鎖子甲',
    ],
    groups: ['armored', 'unique_mammals', 'south_america', 'desert', 'nocturnal'],
  },
  wombat: {
    hints: [
      '我住在澳洲，會挖很深很長的地底隧道當家',
      '我最神奇的地方是——我的便便是方形的！',
      '我長得圓滾滾的像小熊，有強壯的短腿和小小的耳朵',
    ],
    groups: ['australian', 'cute', 'unique_mammals'],
  },
  camel: {
    hints: [
      '我住在沙漠裡，可以好幾天不喝水也沒問題',
      '我的眼睫毛超長超厚，可以擋住沙漠的風沙',
      '我的背上有突起來的「駝峰」，裡面存的不是水而是脂肪',
    ],
    groups: ['desert', 'large'],
  },
  moose: {
    hints: [
      '我是鹿科裡體型最大的，住在北方的森林和沼澤',
      '我超會游泳，甚至會潛到水底去吃水草',
      '公的頭上有一對超寬大的鏟形鹿角，像兩片大盤子',
    ],
    groups: ['large', 'cold', 'swimmers'],
  },
  zebra: {
    hints: [
      '我住在非洲的草原上，是群居動物，喜歡跟朋友在一起',
      '科學家到現在還在爭論我到底是白底黑紋還是黑底白紋',
      '我全身有黑白相間的條紋，每一隻的花紋都獨一無二',
    ],
    groups: ['african_large', 'african', 'fast'],
  },
};

// ===== 所有有提示的動物 ID 清單 =====
export const MVP_ANIMAL_IDS = Object.keys(HINTS);
