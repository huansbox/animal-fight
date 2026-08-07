# HANDOFF

- Status: active
- Task/issue: GitHub #7 — 執行 v0.8-M 兄弟真人完整局
- Branch: test/issue-7-v08m-child-playtest
- Updated: 2026-08-07

## Progress

完成 Issue #7 兄弟真人局的事後證據檢討，正式選擇「局部修正後再做一次最小兒童回歸」。新增 v0.9 設計正本：基本 `2d6`、屬性符合時 `3d6` 取高 2、技能符合 `＋1`、一般 DC 7、Boss DC 8、單向屬性門檻、取消公布後免費換卡／改方法，並重整三寶物效果與機率。tutorial-in-play 成為首局預設；略過的局後訪談不補做，後續只採可觀察行為作結論。已同步 v0.8-M 歷史文件與 `AGENTS.md`，未修改 DM Web、卡片或 PDF。

## Next step

審查並合併 `test/issue-7-v08m-child-playtest` 至 `master`。合併後另行安排 v0.9 紙筆最小兒童回歸；先驗證 5 歲孩子能否從 3～4 顆骰選最大 2 顆並相加、多骰的可觀察投入，以及屬性不符仍以 `2d6` 嘗試但不能換卡／改方法。

## Validation

`game/digital/data/animals.json` 的 132 張正式資料重算後，十二條單向門檻覆蓋與文件一致；完整枚舉 d6 骰面後，一般／Boss 核心成功率、三寶物隨機組合與後援機率均與文件一致。5 份相關文件的本地 Markdown 連結、過期狀態字串與 conflict marker 掃描通過；`git diff --check` 與 `git diff --cached --check` 通過。文件 scope 不適用 code tests、lint 或 type checks。

## Blockers

None.
