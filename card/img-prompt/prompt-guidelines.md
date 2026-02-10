# 動物卡片 AI 繪圖 Prompt 撰寫指南

> **核心原則**：動物姿勢必須視覺化呈現特殊技能，而非單純描述外觀。

---

## 1. Prompt 結構模板

```
black and white vector line art of [動物名稱], [技能動作描述], [關鍵外觀特徵], [姿態/表情], centered composition, bold lines, coloring book style, white background, high contrast, no shading
```

### 必要元素

| 元素 | 說明 | 範例 |
|------|------|------|
| **動物名稱** | 英文正式名稱 | `African Wild Dog`, `Spotted Hyena` |
| **技能動作** | 直接對應技能的動態描述 | `crushing a bone`, `splashing through water` |
| **外觀特徵** | 該動物辨識度最高的特徵 | `large rounded ears`, `curved tusks` |
| **姿態描述** | 動態感、攻擊性、情緒 | `aggressive stance`, `alert pose` |

---

## 2. 技能→動作轉換指南

### 攻擊型技能

| 技能類型 | 動作方向 | 範例 |
|----------|----------|------|
| 衝撞類 | 頭部低垂、身體前傾、衝刺姿勢 | `head lowered for a charge`, `charging pose` |
| 咬擊類 | 張嘴、牙齒外露、咬住物體 | `jaws wide open crushing a bone`, `teeth bared` |
| 揮擊類 | 站立、爪子高舉、揮砍動作 | `swiping with powerful claws`, `claws raised in striking pose` |
| 尾擊類 | 尾巴高舉或揮動、製造衝擊 | `tail flukes smashing down on water`, `powerful tail swing` |

### 防禦型技能

| 技能類型 | 動作方向 | 範例 |
|----------|----------|------|
| 護甲類 | 防禦姿態、特徵強調 | `quills fully raised and fanned out in defense` |
| 厚皮類 | 穩固站姿、毛髮/皮膚紋理 | `standing firm like a mountain`, `long shaggy hair` |
| 偽裝類 | 靜止、融入環境、蜷縮 | `hanging motionless`, `curled up clinging to branch` |

### 移動型技能

| 技能類型 | 動作方向 | 範例 |
|----------|----------|------|
| 奔跑類 | 全速奔跑、腿部伸展 | `running fast`, `dynamic pose` |
| 跳躍類 | 空中姿態、腿部伸展 | `leaping high in the air, legs extended` |
| 游泳類 | 水中動作、濺水效果 | `splashing through water`, `swimming pose` |
| 擺盪類 | 手臂伸展、空中動作 | `mid-swing between branches`, `arm fully extended` |

### 感知型技能

| 技能類型 | 動作方向 | 範例 |
|----------|----------|------|
| 聽覺類 | 耳朵轉向、頭部傾斜 | `head tilted listening intently`, `ears swiveled forward` |
| 視覺類 | 眼睛明亮、注視方向 | `sharp eyes looking down`, `large glowing eyes` |
| 哨兵類 | 直立、警戒、掃視 | `standing upright`, `alert posture looking for danger` |

### 團隊型技能

| 技能類型 | 動作方向 | 範例 |
|----------|----------|------|
| 群體狩獵 | 多隻動物、協調動作 | `a pack of three dogs, coordinated hunting stance, circling a target` |
| 合作防禦 | 警戒姿勢、守望 | `alert sentinel pose, scanning horizon` |

---

## 3. 審核清單

撰寫完成後，逐項檢查：

### 基本項
- [ ] **技能對應**：動作是否直接呈現技能名稱的含義？
- [ ] **動態感**：是否有動作進行中的感覺（而非靜態站立）？
- [ ] **特徵辨識**：關鍵外觀特徵是否有強調？
- [ ] **全身可見**：是否為 full body，避免只有頭部特寫？
- [ ] **風格一致**：是否包含完整的風格後綴？

### 進階項
- [ ] **無禁用詞**：是否含有顏色、光澤、透明等線稿無效詞彙？（§7）
- [ ] **姿態不重疊**：是否與現有同類動物的構圖明顯不同？（§8）
- [ ] **AI 可渲染**：所有描述是否都是「看得見」的？無抽象概念？（§9）
- [ ] **場景簡潔**：互動物件是否 ≤1 個且滿足四項條件？（§10）
- [ ] **橫向構圖**：動作剪影是否適合橫向矩形框？（§11）
- [ ] **兒童適性**：是否無血腥、恐怖、人體部位相關描述？（§12）

---

## 4. 良好範例對照表

> 以下範例來自第一、二波動物（已驗證品質）

| 動物 | 技能 | 良好 Prompt（動作描述部分） |
|------|------|---------------------------|
| 非洲獅 | 大吼 | `mouth wide open roaring, mane flowing` |
| 非洲象 | 鼻子噴水 | `raising its trunk high and spraying water` |
| 獵豹 | 極限衝刺 | `running fast, dynamic pose` |
| 穿山甲 | 捲成球 | `in the middle of curling into a ball` |
| 海豚 | 超音波 | `jumping out of water, with circular sonar wave lines radiating from its head` |
| 遊隼 | 千里眼 | `diving down from the sky, sharp eyes looking down` |
| 科摩多龍 | 強酸口水 | `tongue out with corrosive saliva dripping` |
| 大猩猩 | 攀爬高手 | `climbing a thick tree trunk, looking upwards` |
| 蜜獾 | 百毒不侵 | `standing in a fierce defensive stance, looking fearless` |
| 黑斑羚 | 靈活跳躍 | `leaping high in the air, legs extended, dynamic pose` |
| 蘇門答臘虎 | 隱密伏擊 | `prowling low to the ground, intense eyes hunting, ready to pounce` |
| 灣鱷 | 死亡翻滾 | `massive jaws open, powerful tail curved, aggressive stance` |
| 北極狐 | 雪地隱身 | `pouncing into snow, dynamic pose` |
| 紅袋鼠 | 拳擊踢腿 | `standing upright in a boxing stance, looking ready to fight` |

---

## 5. 常見錯誤

| 錯誤類型 | 錯誤範例 | 修正方向 |
|----------|----------|----------|
| 靜態描述 | `patient dignified expression` | 改為動態：`walking steadily against the wind` |
| 未對應技能 | 水鹿「水中逃脫」→ `leaping pose` | 改為：`splashing through water` |
| 缺少動作 | `duck-like bill, beaver-like tail` | 加入技能動作：`kicking out with hind leg` |
| 僅描述外觀 | `large branching antlers` | 加入動作：`lowering antlers for a sweep` |

---

## 6. 風格後綴（固定）

所有 prompt 結尾必須包含：

```
centered composition, bold lines, coloring book style, white background, high contrast, no shading
```

---

## 7. 線稿禁用詞彙

黑白線稿風格中，以下詞彙無效或會產生矛盾結果：

| 禁用類別 | 禁用詞彙 | 替代方案 |
|----------|---------|---------|
| 顏色 | vivid, colorful, bright, golden, red, blue | 用花紋描述：`bold pattern`, `geometric markings` |
| 光澤 | glossy, shiny, iridescent, glowing | 用質感描述：`smooth`, `textured`, `rough` |
| 透明 | translucent, transparent, see-through | 用結構描述：`thin membrane`, `delicate wings` |
| 陰影 | shadow, dark patches, silhouette | 用線條描述：`bold outline`, `thick lines` |

**自檢方式**：
> 遮住所有顏色/材質詞，剩下的描述是否仍能辨識這隻動物？若不能，需補強結構特徵。

---

## 8. 姿態重疊比對

撰寫 prompt 前，必須列出「最可能撞姿態」的現有動物，確認視覺區隔。

### 高風險重疊群組

| 群組 | 成員 | 區隔策略 |
|------|------|---------|
| 大貓撲殺 | 非洲獅、花豹、猞猁、雪豹、雲豹、美洲豹 | 各自不同動作：吼叫/撲殺/草叢躍出/蹲伏/樹上俯撲/咬龜殼 |
| 猛禽俯衝 | 遊隼、白頭海鵰、雪鴞、兀鷲 | 垂直俯衝/水面低掠/水平滑翔/地面張嘴 |
| 護甲捲球 | 穿山甲、犰狳 | 鱗片重疊/矩形甲片帶狀紋理 |
| 蛇類攻擊 | 蟒蛇、眼鏡蛇 | 纏繞絞殺/展頸噴毒 |

### 比對流程
1. 找出同科或相似體型的已有動物
2. 比較動作類型（撲/衝/咬/站）和身體方向（水平/垂直/蜷縮）
3. 若重疊 → 必須改用不同動作或角度

---

## 9. AI 可渲染性規則

AI 圖像生成器的能力邊界：只能畫「看得見的東西」。

### 禁止描述

| 類型 | 禁用範例 | 原因 |
|------|---------|------|
| 不可見物體 | `invisible target`, `unseen prey` | AI 會忽略或生成懸空肢體 |
| 漫畫效果 | `impact burst lines`, `speed lines`, `shock waves` | AI 處理不一致，可能變成隨機線條 |
| 抽象概念 | `pure rage`, `ultimate power`, `aura of fear` | 無法轉化為視覺元素 |

### 不可見力量的處理方式

將不可見力量轉化為「身體姿態 + 可見副產物」：

| 不可見力量 | 不要寫 | 改為 |
|-----------|--------|------|
| 電流 | `electricity crackling` | 身體弓起蓄力的姿態 |
| 超音波 | `sound waves radiating` | 張嘴 + 頭部傾斜的偵測姿態 |
| 毒液 | `venom invisible in bloodstream` | 張嘴露牙 + 液滴滴落 |
| 臭氣 | `smell cloud` | 尾巴高舉 + 噴射方向線 |

### 允許的效果線
- `motion blur lines`（動態模糊線）— 表達速度 ✅
- `spray lines`（噴射方向線）— 表達噴射方向 ✅
- `dust kicking up`（揚塵）— 表達地面衝擊 ✅
- `impact burst lines`（衝擊爆裂線）— 漫畫效果 ❌
- `shock wave rings`（衝擊波環）— 過於抽象 ❌

---

## 10. 場景複雜度限制

### 核心規則：動物是唯一主角

| 允許 | 限制 | 禁止 |
|------|------|------|
| 動物自身身體 | 1 個簡單互動物件 | 完整場景/背景 |
| 姿態 + 表情 | 物件必須有明確輪廓 | 其他動物作為獵物 |
| 自身產出物（唾液、刺） | 物件面積 < 動物的 1/3 | 模糊物件（`food`, `prey`） |

### 互動物件的選用條件

若技能需要外部物件才能傳達，物件必須同時滿足：

1. **具體明確**：`turtle shell`（有明確形狀）而非 `food`（模糊）
2. **兒童友善**：不會生成恐怖或血腥畫面
3. **該動物獨有**：能強化辨識度（美洲豹是唯一能咬碎龜殼的貓科）
4. **視覺簡單**：不超過 1 個物件，輪廓清晰

### 物件使用範例

| 動物 | 物件 | 合格？ | 理由 |
|------|------|:-----:|------|
| 美洲豹 | 龜殼（有裂紋） | ✅ | 獨有行為 + 明確輪廓 + 兒童友善 |
| 大熊貓 | 竹子 | ✅ | 標誌性關聯 + 簡單形狀 |
| 巨嘴鳥 | 樹枝 | ✅ | 站立支撐 + 不搶焦點 |
| 虎鯨 | 冰面 + 海豹 | ❌ | 場景過於複雜 |
| 蘭花螳螂 | 花朵背景 | ❌ | 背景搶焦點 |

---

## 11. 構圖方向指南

### 目標比例
卡片容器為橫向矩形，圖片必須為 **1:1 正方或橫向**（1024×1024 或 1536×1024），嚴禁直幅。

### 動作方向與構圖的關係

| 動作方向 | 構圖風險 | 處理方式 |
|----------|---------|---------|
| 水平移動（奔跑、飛撲） | 安全 | 自然橫構圖 |
| 垂直動作（跳躍、俯衝） | 高風險 | 改為斜向或水平變體 |
| 靜態站立 | 安全 | 自然正方 |
| 蜷縮/捲球 | 安全 | 自然正方 |

### 垂直動作的橫化技巧

| 原始描述 | 問題 | 修正 |
|----------|------|------|
| `springing upward` | 縱向構圖 | `bursting forward out of tall grass`（水平躍出） |
| `lunging downward from tree` | 縱向構圖 | `lunging diagonally from branch`（斜向撲出） |
| `diving straight down` | 縱向構圖 | `sweeping low over water surface`（水平低掠） |

**自檢方式**：
> 想像這個動作的剪影，放進一個橫向矩形框。如果剪影的高度遠大於寬度，就需要調整動作方向。

---

## 12. 兒童適性檢查

目標受眾 6-12 歲，所有畫面必須適合作為塗色頁。

### 禁止內容

| 類別 | 禁止範例 | 原因 |
|------|---------|------|
| 人體部位 | `skull`, `human bones` | AI 可能生成人類骨骼 |
| 血腥場面 | `blood dripping`, `torn flesh` | 不適合兒童 |
| 恐怖表情 | `terrifying`, `horrifying` | 改用 `fierce`, `aggressive` |
| 死亡場景 | `dead prey`, `carcass` | 改為動態攻擊姿勢（無受害者） |

### 安全替代詞

| 不要用 | 改為 |
|--------|------|
| `skull bite` / `crushing skull` | `powerful bite` / `crushing shell` |
| `tearing at flesh/food` | `beak open wide aggressively` |
| `blood` | 完全移除 |
| `killing` / `deadly` | `powerful` / `fierce` |
| `terrifying` | `fierce` / `intense` |

### 物件安全性
若 prompt 包含互動物件，檢查 AI 是否可能將物件渲染為人類相關：
- `skull` → 可能生成人類頭骨 ❌
- `bone` → 可能生成人類骨頭 ❌
- `turtle shell` → 明確是動物 ✅
- `bamboo` → 明確是植物 ✅

---

## 13. 三 Agent 並行審核

每批 prompt 完成後，開 3 個 Agent 並行審核，各自獨立檢查不同面向：

| Agent | 角色 | 檢查重點 |
|-------|------|---------|
| A | 技能動作對應 | 動作是否直接呈現技能名稱含義？動態感是否足夠？ |
| B | 外觀辨識度 | 關鍵外觀特徵是否強調？能否一眼辨識物種？ |
| C | 構圖一致性 | 全身可見？風格後綴完整？構圖方向正確？場景複雜度合規？ |

### 審核流程

1. 三個 Agent **同時收到**所有 prompt + §3 審核清單 + §7-§12 進階規則
2. 各自獨立輸出逐隻判定（✅ 通過 / ⚠️ 需修正 + 具體問題 + 修正建議）
3. 彙整三方意見：任一 Agent 標記 ⚠️ 的動物進入修正
4. 修正後更新 prompt，在 .md 檔底部記錄「審核紀錄」和「修正項目」兩張表

### 審核紀錄格式

```markdown
## 審核紀錄

| 動物 | 審核員 A | 審核員 B | 審核員 C | 結果 |
|------|:--------:|:--------:|:--------:|:----:|
| 棕熊 | ✅ | ✅ | ⚠️→✅ | 修正後通過 |

### 修正項目

| 動物 | 原問題 | 修正內容 |
|------|--------|----------|
| 棕熊 | `invisible target` AI 無法渲染 | 移除，改為雙臂舉起內彎姿態 |
```

---

## 14. JSONL 轉換規範

審核通過後，將 .md 中的 prompt 轉換為 API 用 JSONL 檔。

### 檔名慣例

- 人類可讀版：`animal-ai-prompts-{波次}.md`
- API 投入版：`animal-prompts-api-{波次}.jsonl`
- 波次編號：數字遞增（1, 2, 3, 4, 5, 6...）

### JSONL 格式

每行一個 JSON 物件，包含 `id` 和 `prompt` 兩個欄位：

```json
{"id":"brown_bear","prompt":"black and white vector line art of Brown Bear, ..."}
```

### id 命名規則

| 規則 | 範例 |
|------|------|
| 英文小寫 | `brown_bear`（非 `Brown_Bear`） |
| 底線分隔 | `king_cobra`（非 `kingcobra` 或 `king-cobra`） |
| 與圖檔同名 | id `brown_bear` → 圖檔 `brown_bear.png` |
| 簡稱優先 | `rhino_beetle`（非 `rhinoceros_beetle`），但卡片顯示名可為全名 |
| 全域唯一 | 不得與歷史波次的 id 重複 |

### 轉換檢查清單

- [ ] 每行是合法 JSON（可用 `python -m json.tool` 驗證）
- [ ] 所有 `id` 全域唯一（跨波次不重複）
- [ ] prompt 已移除 Midjourney 參數（`--ar`、`--v` 等）
- [ ] 檔案編碼為 UTF-8
- [ ] 行數 = 該波次動物數量（無空行、無尾行）

---

## 參考文件

- `animal-ai-prompts.md` - 第一波 10 隻動物
- `animal-ai-prompts2.md` - 第二波 6 隻動物
- `animal-ai-prompts-3.md` - 第三波 19 隻動物
- `animal-ai-prompts-4.md` - 第四波 13 隻動物
- `animal-ai-prompts-5.md` - 第五波 20 隻動物
- `animal-ai-prompts-6.md` - 第六波 16 隻動物
