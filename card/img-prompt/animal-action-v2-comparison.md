# 動物卡 V2 動作強度比較

> 日期：2026-07-21  
> 狀態：4 隻動物各完成 V2.1／V2.2 候選；保留現有 V2，不覆蓋正式圖片  
> 用途：找出比圖鑑感更吸睛、但仍維持自然解剖與現有特色的動作範圍

## 實驗設計

每隻動物比較三個版本：

- `V2`：現有正式圖，作為基準。
- `V2.1`：只小幅增加姿勢張力、重心與單一能力線索，目標約 `+10%`。
- `V2.2`：明顯但克制地增加動作張力，目標約 `+20%`。

固定不變的條件：

- 既有物種、成年比例、五階灰階感、中粗輪廓、白底與印刷可讀性。
- `3:2` 橫式、完整身體、相近的畫面占比與裁切安全距離。
- 平靜專注的表情，不新增敵人、獵物、攻擊目標、文字或裝飾背景。
- 每張只保留一個特殊能力因果線索，不使用速度線、爆炸或抽象符號。

## Prompt 共用骨架

```text
Use case: precise-object-edit
Asset type: V2.1 or V2.2 action-strength candidate for a 3:2 landscape children's board-game animal card
Input image: Image 1 is the edit target and the approved V2 baseline.
Primary request: preserve the same animal and special-ability action; change only the named pose tension, weight shift, and one concrete cause-and-effect cue.
Invariants: preserve the grayscale natural-history illustration style, species identity, mature proportions, calm expression, paper-white background, full-body framing, line weight, print readability, crop-safe margin, and essentially the same scale in frame.
Avoid: cartoon exaggeration, added characters or props, attack toward the viewer, speed lines, extra limbs, cropped anatomy, text, logo, watermark.
```

## 各動物變因

| 動物 | V2.1 輕度 | V2.2 中度 |
|---|---|---|
| 非洲獅 | 肩胸略向前、前腳微錯位撐地、鬃毛稍向後 | 重心明顯前移、一步寬站姿、胸口擴張、鬃毛與尾巴平衡動作 |
| 皇帝企鵝 | 身體改為淺 `10–15°` 上升斜線、鰭協調划動、泡泡形成短尾跡 | 身體約 `20–25°` 上升、輕微側傾、鰭形成更強划水動作、泡泡方向集中 |
| 紅毛猩猩 | 頭肩靠近工作手、視線對準棒尖、手—棒—洞形成清楚主線 | 上身重心前移、工作手輕微透視放大、眼—手—棒—洞形成更強因果路徑 |
| 金剛鸚鵡 | 頭身略向堅果靠近、腳掌抬高、堅果與裂痕略放大 | 上身明顯前傾、喙—果殼接觸成為視覺中心、長尾作為平衡線 |

## 產出檔案

- `card/images-action-test/lion-v21.png`
- `card/images-action-test/lion-v22.png`
- `card/images-action-test/emperor-penguin-v21.png`
- `card/images-action-test/emperor-penguin-v22.png`
- `card/images-action-test/orangutan-v21.png`
- `card/images-action-test/orangutan-v22.png`
- `card/images-action-test/scarlet-macaw-v21.png`
- `card/images-action-test/scarlet-macaw-v22.png`
- 比較頁：`card/animal-action-v2-comparison.html`

8 張候選皆為 `1536×1024` PNG；使用 built-in `imagegen`，每張以現有正式 PNG 作 edit target 個別產生。

## 初步 QA

| 動物 | V2.1 | V2.2 | 初步判斷 |
|---|---|---|---|
| 非洲獅 | 通過 | 通過 | V2.2 的站姿與尾巴差異最清楚，仍維持現有雄獅特色 |
| 皇帝企鵝 | 通過 | 通過但差異偏小 | 兩版都保有物種辨識，但 V2.2 未完全呈現預期的 `20–25°` 動作差距 |
| 紅毛猩猩 | 通過 | 觀察 | V2.1 工具主線最清楚；V2.2 後方抓握足可能仍被誤認為額外手掌 |
| 金剛鸚鵡 | 通過 | 觀察 | V2.1 接觸點清楚；V2.2 果殼分裂感較強，可能超出「裂開但不碎裂」的克制範圍 |

## 比較方式

1. 先看比較頁全尺寸畫面，只判斷「是否更吸睛」與「是否仍像同一種動物」。
2. 黑白列印時維持圖片框 `114×70mm`，觀察能力線索是否在縮印後仍清楚。
3. 不因成人偏好直接改正式圖；等孩子能否看圖說出動物與能力後再定案。
4. 若 V2.1 已足夠，就將後續共用 Prompt 的動作幅度鎖在輕度；只有明顯不足的能力才採 V2.2。
