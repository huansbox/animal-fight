#!/bin/bash
cd "$(dirname "$0")"
PORT=8080

echo ""
echo "  動物守護者 — 選擇遊戲"
echo "  ─────────────────────"
echo "  1) 動物大對決"
echo "  2) 動物猜猜看"
echo ""
read -p "  輸入選項 (1/2): " choice

case "$choice" in
  2) URL="http://localhost:$PORT/game/quiz/" ;;
  *) URL="http://localhost:$PORT/game/digital/" ;;
esac

python3 -m http.server $PORT &
SERVER_PID=$!
sleep 1
open "$URL"
wait $SERVER_PID
osascript -e 'tell application "Terminal" to close front window'
