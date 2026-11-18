import sys, subprocess
from playwright.sync_api import sync_playwright
html, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
times = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file://"+html); pg.wait_for_timeout(800)
    if times:
        for t in times:
            pg.evaluate(f"render({t})"); pg.screenshot(path=f"{out}_{t}.jpg", type="jpeg", quality=92)
    else:
        ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","image2pipe","-framerate","30","-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart",out], stdin=subprocess.PIPE)
        n = int(dur*30)
        for i in range(n):
            pg.evaluate(f"render({i/30})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
        ff.stdin.close(); ff.wait()
    b.close()
