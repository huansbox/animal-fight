# 維運手冊

## 執行環境

| 項目 | 規格 | 原因 |
|---|---|---|
| Python | `uv` 管理、Python 3.13 | 避免 macOS／Windows 命中不同系統 Python |
| 前端 | Vanilla HTML/CSS/JS + ES Modules | 離線使用與單人維護，不需要 build pipeline |
| 圖片生成 | OpenAI Images API／Batch API | 正式數位圖片由 `card/batch_generate.py` 批次生成 |

環境規則：HTTP server 必須從 repo root 啟動；不能直接雙擊 `index.html`，否則 ES Modules 與跨目錄圖片路徑會失敗；Python 指令一律使用 `uv run python`。

## 自動化

| 觸發 | 內容 |
|---|---|
| push 到 `master` 且包含 `wiki/**` | GitHub Actions 將 repo 的 `wiki/` 發佈到 `.wiki.git` |

沒有完整 CI pipeline。DM 規則有 Node 內建測試；動物技能 audit 有 Python unittest。

## 日常指令

安裝 Python dependencies：

```bash
uv sync
```

從 repo root 啟動本機 server：

```bash
uv run python -m http.server 8080
# 動物大對決  http://localhost:8080/game/digital/
# 動物猜猜看  http://localhost:8080/game/quiz/
# DM 專注模式 http://localhost:8080/game/dm/
```

生成數位版動物圖片：

```bash
uv run python card/batch_generate.py generate --skip-existing
uv run python card/batch_generate.py submit
uv run python card/batch_generate.py status --wait
uv run python card/batch_generate.py download
```

最相關驗證：

```bash
node --test game/dm/rules.test.mjs
node --check game/dm/app.js
node --check game/dm/data/scenarios.js
node --check game/dm/rules.js
uv run python -m unittest card/test_audit_animal_skills.py
```

## 實體列印

- 動物底卡名義尺寸為 `122×175mm`，首批正式卡面為 `117×170mm`，A4 橫式每頁 2 張。
- 正式團隊任務 PDF 是 [`team-mission-status-zone-cards-quarter-label-a4.pdf`](https://github.com/huansbox/animal-fight/blob/master/output/pdf/team-mission-status-zone-cards-quarter-label-a4.pdf) 與 [`storm-forest-rescue-reveal-cards-half-label-a4.pdf`](https://github.com/huansbox/animal-fight/blob/master/output/pdf/storm-forest-rescue-reveal-cards-half-label-a4.pdf)。
- 黑白雷射列印，縮放固定 `100%`／「實際大小」，不要使用「符合頁面」。
- v0.6 控制板、四分揭露卡與 DM 紙本指南已移到 [`archive/v0.6/output/pdf/`](https://github.com/huansbox/animal-fight/tree/master/archive/v0.6/output/pdf)，不要拿來當現行列印檔。

## 已知地雷

- `card/images/` 與 `card/images-realistic/` 被 `.gitignore` 排除；新 clone 不含完整圖片來源，數位版會顯示 placeholder。正式 PDF 雖在 Git 中，仍不能取代原始圖備份。
- `card/final_cards.html` 與數位版使用不同圖片目錄；列印前先確認圖片沒有破圖。
- 團隊任務 v0.9 是 owner-approved prototype，不是 child-validated；不要把 v0.8-M 真人局證據直接套到新骰池。
- 歷史規則與測試已移到 `archive/docs/plans/`；現行團隊任務入口只看 v0.9 設計正本與 `game/dm/`。

## 故障排查

| 症狀 | 先看哪裡 |
|---|---|
| 數位版動物全是灰色 `?` | server 是否從 repo root 啟動；`card/images-realistic/` 是否存在 |
| 列印版破圖 | `card/images/` 是否有對應 PNG，HTML 引用路徑是否正確 |
| 頁面空白或 module 錯誤 | 是否誤用 `file://`；改走本機 HTTP server |
| Batch API 卡住 | `uv run python card/batch_generate.py status`；錯誤看 `card/batch_errors.jsonl` |
| DM 規則修改後行為不明 | 先跑 `node --test game/dm/rules.test.mjs` |
