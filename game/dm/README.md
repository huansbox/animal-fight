# DM 專注模式原型

團隊任務 v0.9 的家長專用逐關網頁。部署目標為 Cloudflare Pages，手機、平板與電腦皆可使用；DM 私下裁定區不展示給孩子。

首頁與逐關流程採 tutorial-in-play。每個位置先顯示孩子會聽到的情境與目標，再由 DM 展開私下區查看兩條隱藏基準、DC 與提示。Boss 畫面依序提示萬用背包、A／B 第一次檢定、探險手電筒、變化魔鏡與全隊後援。遊戲中仍以桌面實體卡為狀態來源，不要求逐骰輸入；結束後才記錄一般任務、寶物與 Boss 摘要。

## 本機啟動

從專案根目錄執行：

```bash
uv run python -m http.server 8765
```

開啟：

```text
http://127.0.0.1:8765/game/dm/
```

版面檢查可用 `?preview=<step>` 直接打開指定步驟，例如：

```text
http://127.0.0.1:8765/game/dm/?preview=road
http://127.0.0.1:8765/game/dm/?preview=boss
http://127.0.0.1:8765/game/dm/?preview=debrief
```

## Cloudflare Pages

MVP 為純靜態檔案，不需要 build command、Pages Functions 或 D1。

- 若只部署此工具：Build output directory 設為 `game/dm`。
- 若部署整個專案：直接使用 `/game/dm/` 路徑。

## 資料

- 目前遊戲進度：`localStorage` 的 `animalFight.dm.active.v3`。
- 最近 50 局紀錄：`localStorage` 的 `animalFight.dm.records.v3`。
- 不記錄姓名、每次骰子或動物分配。
- v0.6／v0.7 的舊版紀錄不會自動混入 v0.9，避免不同規則資料混在一起。
- 可從紀錄頁複製 Markdown 或匯出 JSON。

清除瀏覽器網站資料會同時清除上述紀錄；不同裝置不會同步。
