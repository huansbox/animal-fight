# 正式卡片注音字型

此目錄由 [`card/build_bopomofo_fonts.py`](../../build_bopomofo_fonts.py) 依 132 張正式動物卡與團隊任務寶物／後援／區域卡文字產生，不應手動編輯 WOFF2 或 corpus。

## 建置

macOS／Windows 均使用 Python 3.9 以上：

```bash
uv run --with-requirements card/requirements-fonts.txt python card/build_bopomofo_fonts.py
```

離線重建時，先確保快取已有官方 ZIP：

```bash
uv run --with-requirements card/requirements-fonts.txt python card/build_bopomofo_fonts.py --offline
```

## 固定來源

- 官方版本：BpmfGenSenRounded v1.500
- 官方 Release：<https://github.com/ButTaiwan/bpmfvs/releases/tag/v1.500>
- ZIP SHA-256：`01548ac7216758bd2a2a46143ed41b26004198df2b07ab24b337c88505f8e558`
- Bold：`BpmfGenSenRounded-B.ttf`
- Medium：`BpmfGenSenRounded-M.ttf`

輸出會保留 GSUB 與 IVS 讀音選擇功能、字型 hinting、授權與 NOTICE。

## 已知例外

官方完整字型缺少 `獴、㺢、㹢、狓`。卡片仍保留正式名稱「狐獴、㺢㹢狓」，由 [`card/data/bopomofo-overrides.json`](../../data/bopomofo-overrides.json) 提供人工注音，不允許靜默 fallback。

`屁股`的「股」與`腦袋`的「袋」雖有字形，但官方字型沒有本專案採用的輕聲讀音 IVS，也由同一份 override 資料人工排注音。

讀音政策：`一、不`維持字典本調；名詞尾與助詞輕聲依語境以 IVS 校正。

## QA

瀏覽器檢查頁：[`card/bopomofo-coverage-qa.html`](../../bopomofo-coverage-qa.html)

可列印 PDF：[`output/pdf/bopomofo-font-coverage-qa.pdf`](../../../output/pdf/bopomofo-font-coverage-qa.pdf)

QA 首頁集中顯示 `鱷龜、蠍子、狐獴、㺢㹢狓、袋熊、黑猩猩`；其餘頁面以正式卡面字級列出全部 132 隻動物的名稱、特殊能力名稱與說明。
