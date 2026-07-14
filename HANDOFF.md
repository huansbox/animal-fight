# HANDOFF — 2026-07-14 repo wiki 已建置完成上線，留三項待裁決

## 目標

為 repo 初始化 GitHub wiki（正體中文五頁：簡介／維運／路線圖／計畫／技術債）。

**此目標已完成。** 這份交接檔不是為了接續未完成的工作，而是把三項「已做但未經你確認」與「已發現但未開單」的事情交出去，避免它們只活在對話裡。

## 進度

- **已完成**：wiki 五頁 + `_Sidebar` + `_Footer` 共七檔已發佈上線 → <https://github.com/huansbox/animal-fight/wiki>
  - `wiki/` 目錄（唯一編輯處）、`.github/workflows/publish-wiki.yml`（CI 發佈鏈）、`CLAUDE.md` 索引行 → commit `ab6c203`，已 push master
  - CI 發佈鏈已實測跑通（wiki 上的 `b6af6f1 Update wiki ab6c203...` 那筆是 CI 自己推的，不是手動推的）
- **進行中**：無
- **下一步**：見下方「對話中已對齊、尚未落檔的決策」的三項，都需要你裁決

## 對話中已對齊、尚未落檔的決策

### 1. wiki 維護機制我自行選了「同步派」，你還沒確認

`/repo-wiki` skill 要求在兩種維護機制中問使用者一次。當時是 autonomous 模式（`/goal`）不能停下來問，我依 skill 判準自決：這個 repo 仍在持續開發 → 選**同步派（選項 A）**。

落地結果：`wiki/` 是唯一編輯處，push master 時 CI 自動發佈；網頁上不能直接編輯（會被覆蓋）。

若你其實想要**選項 B（重生成派）**——低頻維護、不建 CI、之後直接跑 `/repo-wiki refresh` 重生成——把 `.github/workflows/publish-wiki.yml` 刪掉即可，其餘不用動。

### 2. wiki 尚未經過 `/doc-review`

依全域 CLAUDE.md 的 review 分層，wiki 屬於「由使用者呼叫」的層級，agent 不自動跑。我沒有跑。內容是新寫的、未經對抗式審查。

### 3. 三個高利息技術債發現，只寫在 wiki，尚未開 issue

生成 wiki 時做了一次 repo 體檢，挖到三件會讓人白花時間的事。全部寫進 `wiki/Tech-Debt.md`（附成本與償還策略），但**都還沒開 GitHub issue**（Tech-Debt 頁自己標了「尚未開 issue」）：

1. **列印版現在印出來是 132 張無圖卡片** — `card/final_cards.html` 取 `images/{id}.png`，但 `card/images/` 底下只剩 `archive-cartoon/` 那 10 張封存的卡通測試圖。不會報錯，印出來才知道。數位版的 132 張寫實圖（`card/images-realistic/`）是完好的，取圖路徑指過去即可止血。
2. **線上站台的動物遊戲看不到任何圖** — 240MB 的 PNG 被 `.gitignore` 排除，GitHub Pages 上根本沒這些檔案。根治要先轉 WebP（2.3MB → 約 150KB，總量降到 20–30MB）才進得了 git。
3. **GitHub Pages 部署自 `claude/world-cup-travel-game-zlcnyd` 這條未合併分支，不是 master** — 在 master 修好的東西推上去不會上線，症狀是「網頁沒變」，極易誤判為快取問題。該分支比 master 多 4 個 commit（世界盃遊戲 + 遊戲合輯首頁）。

另有一項時效性判斷寫在 `wiki/Roadmap.md` 的「收斂點」：世界盃的 issues #1–#5 裡最有價值的兩項綁在賽事上，賽事 7 月中結束後就沒有玩的場合——要做是現在，否則建議直接關掉。

## 注意事項

- **wiki.git 的誕生無法自動化**：GitHub 硬限制，`.wiki.git` 在網頁 UI 存下第一頁前不存在，API / token push / SSH push 全部 404。本次是由你手動建第一頁後才推得上去。若未來 wiki 被整個刪掉重來，同樣要再手動建一次。
- **不要在 wiki 網頁上直接編輯**（除非改走選項 B）：CI 下次發佈會覆蓋掉。改內容請改主 repo 的 `wiki/`。
- **`wiki/` 的快照頁**（Plan / Roadmap / Tech-Debt）標了快照日期 2026-07-14，過期時跑 `/repo-wiki refresh` 只會重寫這三頁，Home / Maintenance 不動。
- 工作區有 4 個 untracked 檔（`.DS_Store` ×3、`AGENTS.md`），是本 session 之前就存在的，我沒有動它們。`AGENTS.md` 是 `CLAUDE.md` 的未版控複本（只差 2 行檔名），必然漂移——這筆已記在 Tech-Debt 低利息區。

## Suggested skills

- `/doc-review` — 對抗式審查剛生成的 wiki 五頁（見上方第 2 項）
- `/repo-wiki refresh` — 快照頁過期時（milestone 或每月）刷新，只動 Plan / Roadmap / Tech-Debt
- `/grill-with-docs` — 若要推進玩法重設計的方向抉擇（那 7 個待討論事項是本專案唯一的關鍵路徑，見 `wiki/Plan.md`）

## 如何接續

任一台機器 `git checkout master && git pull`，然後：

1. 先讀 <https://github.com/huansbox/animal-fight/wiki>（或 repo 內的 `wiki/` 目錄），五頁十分鐘看完，等於接手了整個專案現況
2. 裁決上方三項（維護機制要不要改選項 B、要不要跑 `/doc-review`、三個技術債要不要開 issue）
3. 真正要推進專案的話，關鍵路徑只有一條：玩法重設計的方向抉擇，讀 `docs/plans/2026-04-08-review-synthesis.md` 的「七、待討論事項」

---
本檔讀完即刪（`/handoff` 接班流程會處理）。
