# 維運手冊

## 執行環境

沒有 build step，沒有後端，沒有測試套件。要跑的東西只有兩類：靜態網頁，和生圖用的 Python 腳本。

| 項目 | 規格 | 為什麼 |
|---|---|---|
| Python | 由 uv 管理，pin 在 3.13（[`.python-version`](https://github.com/huansbox/animal-fight/blob/master/.python-version) + [`pyproject.toml`](https://github.com/huansbox/animal-fight/blob/master/pyproject.toml)） | 直接呼叫 `python3` 在 macOS 會命中系統的 3.9.6，跨機器版本不一致。一律 `uv run` |
| 前端 | Vanilla HTML/CSS/JS + ES Modules，無框架 | 要能離線玩，也不想維護 build pipeline |
| 圖片生成 | OpenAI Batch API（`openai` + `python-dotenv`，見 `pyproject.toml`） | Batch API 有 50% 折扣，132 張實際花費約 $2.63 |

### 環境鐵律

1. **HTTP server 一定要從專案根目錄啟動。** 兩個遊戲都用相對路徑 `../../card/images-realistic/{id}.png` 取圖，從 `game/digital/` 底下起 server 會讓所有圖片 404。
2. **不能直接雙擊 `index.html`。** ES Modules 在 `file://` 下會被瀏覽器的 CORS 政策擋掉，必須走 HTTP。
3. **Python 一律 `uv run`，不裸呼叫 `python` / `python3`。** 注意 README 的指令還停在遷移前的寫法（`pip install` / `python3 batch_generate.py`），照抄會出錯——這筆帳記在 [Tech-Debt](Tech-Debt)。

## 排程 / 自動化

| 觸發 | 內容 |
|---|---|
| push 到 `master` 且動到 `wiki/**` | GitHub Actions 把 `wiki/` 目錄發佈到本 wiki（`.github/workflows/publish-wiki.yml`） |

沒有 CI 測試、沒有 lint、沒有自動化的數值檢查（數值檢查腳本仍是待建項，見 [Tech-Debt](Tech-Debt)）。

## 日常指令

實體版目前使用 `card/final_cards.html` 的 A4 全頁版，以黑白雷射列印。可先選 4、8 或 16 隻組單淘汰：兩位玩家各自擲骰，每場一戰定勝負，平手才重骰。這個原型已經實際給孩子遊玩，反應良好。

放大版 Poker 暫定採 122×175mm，測試檔如下：

- HTML：[`card/print-size-test-122x175.html`](https://github.com/huansbox/animal-fight/blob/master/card/print-size-test-122x175.html)
- PDF：[`output/pdf/animal-fight-card-size-test-122x175.pdf`](https://github.com/huansbox/animal-fight/blob/master/output/pdf/animal-fight-card-size-test-122x175.pdf)
- 列印設定：A4 橫式、100%／實際大小、無邊界、關閉頁首與頁尾。
- A4 黑白雷射標籤紙每頁排 2 張；先用普通紙量 100mm 校正尺，再使用標籤紙。
- 無圖測試已試印，大小可接受；等放大版 Poker 到貨後量實際尺寸，再決定貼紙四周內縮量。

啟動遊戲（最省事的方式是雙擊專案根目錄的 `start-game.command`，它會跳選單並自動開瀏覽器）：

```bash
# 從專案根目錄執行，這點不能省
uv run python -m http.server 8080
# 動物大對決  http://localhost:8080/game/digital/
# 動物猜猜看  http://localhost:8080/game/quiz/
```

生成動物圖片（先在 `card/.env` 填 `OPENAI_API_KEY`，範本見 `card/.env.example`）：

```bash
uv run python card/batch_generate.py generate --skip-existing  # 產生 JSONL
uv run python card/batch_generate.py submit                    # 提交 batch job
uv run python card/batch_generate.py status --wait             # 等待完成（Batch API 最長 24h）
uv run python card/batch_generate.py download                  # 下載到 card/images-realistic/
```

跑平衡模擬：

```bash
uv run python sim/battle_sim_v5.py   # 結果寫到 sim/results/
```

## 公開部署

GitHub Pages 已於 2026-07-15 關閉。專案維持離線本機使用，沒有公開試玩網址。Wiki 仍透過上方的 GitHub Actions 獨立發佈，不受 Pages 關閉影響。

## 週期 SOP

**新增動物**走 10 步流程，完整定義在 [`CLAUDE.md`](https://github.com/huansbox/animal-fight/blob/master/CLAUDE.md) 的「動物設計全流程 SOP」段落——觸發語是「用 SOP 設計第 N 波新動物：[清單]」，AI 會自動跑完步驟 1-9（數值 → 審核 → JSON → 繪圖 prompt → HTML 整合），只留步驟 10（批次生圖）給人。動手前讀那一段，不要憑本頁的摘要行事。

流程中兩個最常違反的硬性規則：

- `skillBonus` 的 `val` **加總必須等於 4**，不多不少。
- `skillName` 固定四個字，且不能和既有 131 隻撞名。

## 已知地雷（Gotchas）

只收踩過的，不收想像的。動手前請讀括號裡標的出處。

### 系統面

- **卡片圖片不在版控裡**（`.gitignore` 排除 `card/images/` 與 `card/images-realistic/`）。本機已有可玩的 A4 黑白實體原型，但 clone 一份新 repo 後，數位版所有動物會變成灰色 `?` placeholder（`<img onerror>` 的 fallback），而 `card/images/` 也無法從 repo 還原。在新機器列印或啟動數位版前，先確認圖片資產。根因與償還策略見 [Tech-Debt](Tech-Debt)。
- **列印前務必先看一眼 `final_cards.html` 的圖有沒有出來。** 它引用的是 `images/{id}.png`，和數位版用的 `images-realistic/` 是兩套；破圖不會有任何錯誤訊息，印出來才知道。
- **server 起錯目錄 = 全部沒圖**（`game/digital/README.md` 的「維護筆記」段）。症狀和上一條一模一樣，先確認起 server 的目錄再懷疑圖片。

### 決策面

- **三套判定規則並存**：舊合作闘關（`rulebook.md`）用 v1；團隊任務 v0.6 沿用 v2.5 卡面數值與 `skillBonus` 標記，但改用 1–3 顆骰；動物大對決（`battle-rules.md`）直接使用 v2.5 加分。這是**刻意接受**的現狀，不要順手統一——先完成團隊任務真人實玩再決定（`AGENTS.md`「數值系統分歧」段）。
- **122×175mm 是暫定卡面，不是已確認的底板尺寸。** 無圖 PDF 已試印通過，但市售放大版 Poker 尚未到貨；正式排 132 張前必須先量實物，並以底板四周內縮 1–2mm 作為貼紙起始測試值。見 [Plan](Plan)。

## 故障排查

| 症狀 | 先看哪裡 |
|---|---|
| 數位版動物全是灰色 `?` | 1. server 是不是從專案根目錄起的？ 2. `card/images-realistic/` 存不存在、有沒有 132 張？（新 clone 的機器一定沒有） |
| 列印版 `final_cards.html` 破圖 | 已知問題——`card/images/` 目前沒有列印用圖。權宜解是把取圖路徑指向 `images-realistic/` |
| 頁面空白、console 報 module 錯誤 | 十之八九是直接開 `file://` 了，改用 HTTP server |
| Batch API 卡住 | `uv run python card/batch_generate.py status` 看狀態；錯誤會寫進 `card/batch_errors.jsonl` |
| `python` 指令被擋下 | 這是預期行為（全域 hook 攔截裸呼叫），改用 `uv run python` |
