# Template: 3D globe hook + 3 galtiyan + CTA (approved sample, 19 Nov 2026)
Built with the toolkit: motionmaxxing runtime (measured easing, words, smear, events) + its hero3d Three.js layer (globe, route, plane).
1. `bash studio/toolkit/install.sh`, then copy the runtime next to the page: `cp -r ~/ak-toolkit/motionmaxxing/runtime studio/templates/reel-3d-globe-3galtiyan/`
2. Edit the text in index.html (hook, 3 cards, CTA). Change DEL/NYC lat-lon for other countries (Canada, UK, Australia...).
3. QA stills: `python3 render_reel.py $PWD/index.html qa/s 21 stills 1.6,3.2,8.6,12.5,16.5,20.9`
4. Video: `python3 render_reel.py $PWD/index.html silent.mp4 21` (about 4 min, 3D in software GL)
5. Sound: `python3 sound.py silent.mp4.events.json 21 sfx.wav` then `ffmpeg -i silent.mp4 -i sfx.wav -c:v copy -c:a aac -b:a 192k -shortest out.mp4`
Lessons: never use backdrop-filter on cards (blurs the whole frame in headless Chrome); switch scenes with opacity steps on wrappers, not visibility (word spans override it); the 3D canvas must be full frame (1080x1920).
