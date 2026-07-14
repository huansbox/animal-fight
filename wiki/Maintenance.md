# 維運手冊

## 執行環境

沒有 build step，沒有後端，沒有測試套件。要跑的東西只有兩類：靜態網頁，和生圖用的 Python 腳本。

| 項目 | 規格 | 為什麼 |
|---|---|---|
| Python | 由 uv 管理，pin 在 3.13（[`.python-version`](https://github.com/huansbox/animal-fight/blob/master/.python-version) + [`pyproject.toml`](https://github.com/huansbox/animal-fight/blob/master/pyproject.toml)） | 直接呼叫 `python3` 在 macOS 會命中系統的 3.9.6，跨機器版本不一致。一律 `uv run` |
| 前端 | Vanilla HTML/CSS/JS + ES Modules，無框架 | 要能離線玩，也不想維護 build pipeline |
| 圖片生成 | OpenAI Batch API（`openai` + `python-dotenv`，見 `pyproject.toml`） | Batch API 有 50% 折扣，132 張實際花費約 $2.63 |

### 環境鐵律

1. **HTTP server 一定要從專案根目錄啟動。** 三個遊戲都用相對路徑 `../../card/images-realistic/{id}.png` 取圖，從 `game/digital/` 底下起 server 會讓所有圖片 404。
2. **不能直接雙擊 `index.html`。** ES Modules 在 `file://` 下會被瀏覽器的 CORS 政策擋掉，必須走 HTTP。
3. **Python 一律 `uv run`，不裸呼叫 `python` / `python3`。** 注意 README 的指令還停在遷移前的寫法（`pip install` / `python3 batch_generate.py`），照抄會出錯——這筆帳記在 [Tech-Debt](Tech-Debt)。

## 排程 / 自動化

| 觸發 | 內容 |
|---|---|
| push 到 `master` 且動到 `wiki/**` | GitHub Actions 把 `wiki/` 目錄發佈到本 wiki（`.github/workflows/publish-wiki.yml`） |
| push 到 `claude/world-cup-travel-game-zlcnyd` | GitHub Pages 自動重新部署 <https://huansbox.github.io/animal-fight/> |

沒有 CI 測試、沒有 lint、沒有自動化的數值檢查（數值檢查腳本仍是待建項，見 [Tech-Debt](Tech-Debt)）。

## 日常指令

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

## 部署更新

**線上站台部署自 `claude/world-cup-travel-game-zlcnyd` 分支，不是 `master`。** 這是目前最容易讓人白忙一場的地方：你在 master 上修好了 bug、推上去、重整網頁發現沒變，會以為是快取問題——實際上 Pages 根本沒在看 master。

要讓改動上線，得把它推到那條分支。長期解法是把分支合回 master 並把 Pages source 切到 master，這筆帳記在 [Tech-Debt](Tech-Debt) 的高利息區。

## 週期 SOP

**新增動物**走 10 步流程，完整定義在 [`CLAUDE.md`](https://github.com/huansbox/animal-fight/blob/master/CLAUDE.md) 的「動物設計全流程 SOP」段落——觸發語是「用 SOP 設計第 N 波新動物：[清單]」，AI 會自動跑完步驟 1-9（數值 → 審核 → JSON → 繪圖 prompt → HTML 整合），只留步驟 10（批次生圖）給人。動手前讀那一段，不要憑本頁的摘要行事。

流程中兩個最常違反的硬性規則：

- `skillBonus` 的 `val` **加總必須等於 4**，不多不少。
- `skillName` 固定四個字，且不能和既有 131 隻撞名。

## 已知地雷（Gotchas）

只收踩過的，不收想像的。動手前請讀括號裡標的出處。

### 系統面

- **卡片圖片不在版控裡**（`.gitignore` 排除 `card/images/` 與 `card/images-realistic/`）。後果有三層：clone 一份新的 repo 出來，數位版所有動物都是灰色 `?` placeholder（`<img onerror>` 的 fallback）；GitHub Pages 上的動物遊戲同樣全部沒圖；而 **`card/images/`（列印版取圖的目錄）目前是空的**——只剩 `archive-cartoon/` 那 10 張封存的卡通測試圖，所以 `final_cards.html` 直接印會得到 132 張無圖卡片。要復原得重跑 Batch API（約 $2.63 + 等待時間）。根因與償還策略見 [Tech-Debt](Tech-Debt)。
- **列印前務必先看一眼 `final_cards.html` 的圖有沒有出來。** 它引用的是 `images/{id}.png`，和數位版用的 `images-realistic/` 是兩套；破圖不會有任何錯誤訊息，印出來才知道。
- **server 起錯目錄 = 全部沒圖**（`game/digital/README.md` 的「維護筆記」段）。症狀和上一條一模一樣，先確認起 server 的目錄再懷疑圖片。
- **Pages 部署自非預設分支**（見上方「部署更新」）。master 的改動不會上線。

### 決策面

- **兩套數值系統並存**：合作闘關（`rulebook.md`）用 v1（天賦是單一分數 8-12），動物大對決（`battle-rules.md`）用 v2.5（天賦是 +4 分配）。這是**刻意接受**的現狀，兩個模式獨立運作，不要「順手統一」——等實際玩過再決定（`CLAUDE.md`「數值系統分歧」段）。
- **卡片尺寸有三種互相矛盾的說法**散在不同文件裡（Tarot 70×120mm / 撲克牌 63×88mm）。開始做實體卡之前先把這個拍板，否則版面會白做。見 [Plan](Plan)。

## 故障排查

| 症狀 | 先看哪裡 |
|---|---|
| 數位版動物全是灰色 `?` | 1. server 是不是從專案根目錄起的？ 2. `card/images-realistic/` 存不存在、有沒有 132 張？（新 clone 的機器一定沒有） |
| 列印版 `final_cards.html` 破圖 | 已知問題——`card/images/` 目前沒有列印用圖。權宜解是把取圖路徑指向 `images-realistic/` |
| 線上版沒圖 | 已知問題，不用查——圖片不在 git 裡 |
| 改了 master 但線上沒變 | 已知問題，Pages 部署自 `claude/world-cup-travel-game-zlcnyd` 分支 |
| 頁面空白、console 報 module 錯誤 | 十之八九是直接開 `file://` 了，改用 HTTP server |
| Batch API 卡住 | `uv run python card/batch_generate.py status` 看狀態；錯誤會寫進 `card/batch_errors.jsonl` |
| `python` 指令被擋下 | 這是預期行為（全域 hook 攔截裸呼叫），改用 `uv run python` |
