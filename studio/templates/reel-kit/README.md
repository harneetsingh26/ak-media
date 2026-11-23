# Template: reel kit (data-driven, made 23 Nov 2026)
One page, many reels: all text lives in cfg.js (see examples in the 2026-11-23 week run). Scenes: hook (3D globe with Delhi routes, or gold emblem icon + particles), middle (slam / officer chat / refusal letter with highlighter + lens), 3 cards with progress bar, keyword CTA + WhatsApp.
1. `bash studio/toolkit/install.sh`, then `cp -r ~/ak-toolkit/motionmaxxing/runtime studio/templates/reel-kit/`
2. QA stills: `make.sh cfg.js work/ x stills 1.5,5,8,12,16`
3. Full: `make.sh cfg.js work/ out.mp4` (renders, places SFX Kit CC0 sounds on every motion event, masters to about -14 LUFS, muxes)
Easing: motionmaxxing softLand / snapSettle / crashIn / popOver; hook word animates letter tracking + font weight.
