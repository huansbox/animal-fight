#!/bin/bash
cd "$(dirname "$0")"
PORT=8080
open "http://localhost:$PORT/game/digital/"
python3 -m http.server $PORT
osascript -e 'tell application "Terminal" to close front window'
