# 技術債

> 快照日期：2026-07-14。依**利息**排序——利息高 = 平常就在付出成本；利息低 = 特定情境才痛。技術債 = 已知的權衡，記錄成本與償還條件，**不代表馬上要處理**。Review 節奏：每次玩法／規則大改前重看本頁，過期項目移除或降級。

## 高利息（每天都在付成本）

| 債 | 成本（利息） | 償還策略／條件 | 追蹤 |
|---|---|---|---|
| **所有卡片圖片都不在版控裡**（`.gitignore` 排除 `card/images/` 與 `card/images-realistic/`） | 四層成本：(1) **列印版現在是壞的**——`final_cards.html` 引用 `images/{id}.png` 共 132 張，但 `card/images/` 底下只剩 10 張封存的卡通測試圖（`archive-cartoon/`），直接列印會得到 132 張無圖卡片，而且要印出來才會發現；(2) 線上 Pages 的動物大對決與猜猜看**全部沒圖**，等於公開網址上放著一個壞掉的遊戲；(3) 任何新 clone（換機器、找人幫忙）都要重跑 Batch API，$2.63 + 最長 24 小時的等待窗；(4) **沒有備份**——圖片只存在於某台機器的硬碟上，repo 無從還原 | 分兩段。**短期止血**：數位版那 132 張寫實圖是完好的（`card/images-realistic/`），把 `final_cards.html` 的取圖路徑指過去，列印版立刻能用。**根治**：讓圖片進版控——不能直接 `git add`，PNG 單張 2.3MB × 132 = **240MB**，塞進 git 會永久膨脹歷史（目前 `.git` 只有 1.6MB）；先轉 WebP（1024×1024 寫實照 q80 約 100–200KB）總量可壓到 20–30MB，安全進 git，Pages 也直接吃得到。改副檔名要同步動兩處：`game/quiz/js/app.js:249` 硬編了 `.png`，`game/digital/` 則吃 `animals.json` 的 `img` 欄位 | 本頁為唯一記錄，尚未開 issue |
| **GitHub Pages 部署自未合併分支** | Pages 的 source 是 `claude/world-cup-travel-game-zlcnyd`，不是 `master`。後果：在 master 修好的東西推上去**不會上線**，而且症狀是「網頁沒變」——很容易誤判成快取問題然後白花時間。同時 master 缺了那條分支上的世界盃遊戲與遊戲合輯首頁（分支比 master 多 4 個 commit），兩條線持續發散 | 把 `claude/world-cup-travel-game-zlcnyd` merge 回 master → Pages source 改成 master → 刪分支。**沒有東西擋著，隨時可做** | 本頁 |

## 中利息（特定操作就會痛）

| 債 | 成本（利息） | 償還策略／條件 | 追蹤 |
|---|---|---|---|
| **README 的指令停在 uv 遷移之前** | README 寫的是 `pip install openai`、`python3 batch_generate.py`、`python -m http.server`。專案在 2026-05-18 已改由 uv 管理（pin 3.13），而且全域有 hook 會攔截裸呼叫 `python`／`python3`。照 README 操作 = 被擋下，或裝到系統 Python 去。每次照文件生圖就痛一次 | 把 README 三處指令改成 `uv run python ...`。一句話 diff，隨時可做 | 本頁 |
| **卡片尺寸決策，三份文件三種說法** | `docs/plans/2026-02-10-card-size-production.md` 推 Tarot 70×120mm 並明確寫「撲克牌不推薦」（6-8 歲讀不了那麼密的資訊）；`docs/plans/2026-04-08-review-synthesis.md` 的家長 review 反過來建議撲克牌 63×88mm；README 直接寫「裁切成 63×88mm」。結果是實體製作開不了工，每次想動版面都要重吵一遍 | 拍板一個尺寸，同步更新 README + 兩份 plan 文件。**條件：玩法方向定案後**（版面要印什麼取決於最終規則，現在定會白做） | [Plan](Plan) |
| **平衡模擬結果沒涵蓋全部動物**（v5 只跑 64 隻） | 第十波的 4 隻從未進過模擬（`CLAUDE.md` 自己標了 ⚠️）。現有的平衡結論對這批動物不成立 | 重跑 `sim/battle_sim_v5.py`，涵蓋 132 隻。**條件：玩法方向定案後**——規則若改成三回合制，現在跑的數據整批作廢 | `CLAUDE.md`「對戰模擬結果」段 |
| **兩套數值系統並存**【接受現狀】 | 合作闘關（`rulebook.md`）用 v1（天賦 = 單一分數 8-12），動物大對決（`battle-rules.md`）用 v2.5（天賦 = +4 分配）。改數值時要先想清楚動到哪一套，新接手的人（含 AI）容易搞混 | **刻意接受，不要順手統一。** 兩個模式獨立運作，等真的玩過再決定要不要收斂 | `CLAUDE.md`「數值系統分歧」段 |

## 低利息（記錄在案）

| 債 | 成本（利息） | 償還策略／條件 |
|---|---|---|
| **`AGENTS.md` 是 `CLAUDE.md` 的未版控複本** | 兩份檔案只差 2 行（互相把對方的檔名換掉），但 `AGENTS.md` 沒進 git。這是必然漂移的第二真相：改了 `CLAUDE.md`，`AGENTS.md` 靜默過期，而讀它的 agent 拿到的是舊規範 | 二選一：做成指向 `CLAUDE.md` 的 symlink 並 commit，或直接刪掉 |
| **`CLAUDE.md` 內部數字打架** | 同一份檔案裡，「後續擴充 35 隻待建」和「更多動物（39 隻待建）」並存；`docs/backlog.md` 實際列 39 隻。AI 每個 session 讀到都會有一次困惑 | 改成 39。一句話 diff |
| **數值前置檢查腳本仍未建** | `skillBonus` 加總 = 4、`skillName` 四字不撞名、`skillDesc` 15-25 字、加成模式不重疊、五維差異分數 ≤ 3、繪圖 prompt 禁用詞掃描——全部靠 AI 手動查。132 隻已完成，只有新增動物時才痛，所以利息低 | 腳本化。**條件：下次要開新一波動物時**（要求已寫在 `CLAUDE.md`「技術債 / 待建工具」段） |
| **陳舊分支未清** | `feat/wave8-animals` 與 `claude/animal-guessing-game-gSbt4` 都已完全合併進 master（0 commits ahead），還掛在 remote 上，讓分支列表看起來像有三條線在跑 | 直接刪 remote 分支 |
| **`.gitignore` 沒排除 `.DS_Store`** | macOS 上每次 `git status` 都夾雜雜訊，久了會習慣性忽略 untracked 區塊——真的有東西該 commit 時反而看不到 | 加一行 |

## 記帳原則

- **入場資格**：新債必須寫明「成本（利息）→ 償還策略或條件」。沒有成本描述的不收，否則這張清單會變成垃圾場。
- **接受現狀要明文標註**（例如兩套數值系統），避免每次盤點都重新吵一遍。
- **修完即刪**：償還後刪掉條目，一句話摘要移進下面的歷史紀錄。

## 歷史償還紀錄

| 日期 | commit | 還了什麼 |
|---|---|---|
| 2026-05-18 | `254d948` | Python 環境改 uv 管理並 pin 3.13——終結「`python3` 在 macOS 命中系統 3.9.6、在 Windows 命中 PATH 第一個」的跨機器版本不一致 |
| 2026-02-17 | `17e22b4` | `CLAUDE.md` 從 527 行壓到 195 行，動物數值表與 backlog 搬進 `docs/`——AI 每個 session 都要讀的檔案瘦身，直接降低每次對話的固定成本 |
