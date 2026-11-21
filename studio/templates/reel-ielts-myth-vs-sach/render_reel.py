"""Render a Motion/HyperFrames-style HTML film (window.__seek, window.__ready) to MP4, plus its event list.
Usage: python3 render_reel.py page.html out.mp4 duration [stills t1,t2,...]"""
import sys, subprocess, json
from playwright.sync_api import sync_playwright

html, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
stills = [float(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 and sys.argv[4] == "stills" else None
FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=[
        "--allow-file-access-from-files", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
        "--ignore-gpu-blocklist", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + html)
    pg.evaluate("document.fonts.ready")
    pg.evaluate("window.__ready.then(() => true)")
    events = pg.evaluate("window.__events || []")
    json.dump(events, open(out + ".events.json", "w"), indent=1)
    if stills:
        for t in stills:
            pg.evaluate(f"window.__seek({t})")
            pg.screenshot(path=f"{out}_{t:05.2f}.jpg", type="jpeg", quality=90)
    else:
        ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out],
                              stdin=subprocess.PIPE)
        n = int(round(dur * FPS))
        for i in range(n):
            pg.evaluate(f"window.__seek({i / FPS})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
            if i % 60 == 0:
                print("frame", i, "/", n, flush=True)
        ff.stdin.close(); ff.wait()
    b.close()
print("events:", len(events))
for e in errs[:15]:
    print("PAGE:", e)
