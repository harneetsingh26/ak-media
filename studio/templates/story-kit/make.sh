#!/bin/bash
# Usage: make.sh <cfg.js> <workdir> <out.mp4> [stills t1,t2]
set -e
K=$(cd "$(dirname "$0")" && pwd); R=$K/../reel-kit; CFG=$1; WD=$2; OUT=$3
mkdir -p "$WD"; WD=$(cd "$WD" && pwd); cp "$K/story.html" "$WD/index.html"; cp "$CFG" "$WD/cfg.js"
if [ "$4" = "stills" ]; then python3 "$R/render_reel.py" "$WD/index.html" "$WD/qa" 0 stills "$5"; exit 0; fi
python3 "$R/render_reel.py" "$WD/index.html" "$WD/silent.mp4" 0
python3 "$R/sfx_mix.py" "$WD/silent.mp4.events.json" "$(cat $WD/silent.mp4.dur)" "$WD/mix.wav"
ffmpeg -v error -y -i "$WD/silent.mp4" -i "$WD/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo DONE "$OUT"
