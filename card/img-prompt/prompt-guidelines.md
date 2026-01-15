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

- [ ] **技能對應**：動作是否直接呈現技能名稱的含義？
- [ ] **動態感**：是否有動作進行中的感覺（而非靜態站立）？
- [ ] **特徵辨識**：關鍵外觀特徵是否有強調？
- [ ] **全身可見**：是否為 full body，避免只有頭部特寫？
- [ ] **風格一致**：是否包含完整的風格後綴？

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

## 參考文件

- `animal-ai-prompts.md` - 第一波 10 隻動物
- `animal-ai-prompts2.md` - 第二波 6 隻動物
- `animal-ai-prompts-3.md` - 第三波 19 隻動物
