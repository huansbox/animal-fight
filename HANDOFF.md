# HANDOFF

- Status: active
- Task/issue: GitHub #7 — 執行 v0.8-M 兄弟真人完整局
- Branch: master
- Updated: 2026-08-07

## Progress

完成 Issue #7 兄弟真人局、事後證據檢討與 v0.9 分流，正式選擇「局部修正後再做一次最小兒童回歸」。v0.9 設計正本已定案為基本 `2d6`、屬性符合時 `3d6` 取高 2、技能符合 `＋1`、一般 DC 7、Boss DC 8、單向屬性門檻及新版三寶物。commits `9991214`、`4e39a19` 已 fast-forward 合併至 `master`。Issue #7 保持 OPEN，未完成的局後訪談與資源流程沒有追溯標成完成；未修改 DM Web、卡片或 PDF。

## Next step

新 session 先確認 Issue #7 的行政收尾方式；不得因不再要求訪談而改寫其歷史缺口。另行建立或確認 v0.9 紙筆最小兒童回歸的 tracker work，再驗證 5 歲孩子能否從 3～4 顆骰選最大 2 顆並相加、多骰的可觀察投入，以及屬性不符仍以 `2d6` 嘗試但不能換卡／改方法。

## Validation

`game/digital/data/animals.json` 的 132 張正式資料重算後，十二條單向門檻覆蓋與文件一致；完整枚舉 d6 骰面後，一般／Boss 核心成功率、三寶物隨機組合與後援機率均與文件一致。5 份相關文件的本地 Markdown 連結、過期狀態字串與 conflict marker 掃描通過；`git merge --ff-only`、`git diff --check` 與 `git diff --cached --check` 通過。文件 scope 不適用 code tests、lint 或 type checks。

## Blockers

None.
