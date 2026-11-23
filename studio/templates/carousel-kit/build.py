"""AK carousel kit: slides JSON -> 1080x1350 JPEG slides (navy + gold AK poster look).
Usage: python3 build.py slides.json outdir
slides.json: [{"type":"cover","kicker","title":[lines],"sub"}, {"type":"stake","text","small"},
  {"type":"step","n","label","title","body","icon"}, {"type":"recap","title","items":[...]}, {"type":"cta","line","key","sub"}]"""
import json, sys, os, html
from playwright.sync_api import sync_playwright
S, OUT = json.load(open(sys.argv[1])), sys.argv[2]; os.makedirs(OUT, exist_ok=True)
E = html.escape; N = len(S)
CSS = """
@font-face{font-family:M;src:url("file:///usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf");font-weight:100 900}
@font-face{font-family:P;src:url("file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf");font-weight:700}
@font-face{font-family:P;src:url("file:///usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf");font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:P;color:#fff;background:radial-gradient(ellipse at 50% 35%,#1c3a80 0%,#0d1b3d 50%,#050b1e 100%);position:relative}
.grid{position:absolute;left:-200px;right:-200px;bottom:0;height:420px;background-image:linear-gradient(rgba(242,193,78,.16) 2px,transparent 2px),linear-gradient(90deg,rgba(242,193,78,.16) 2px,transparent 2px);background-size:80px 80px;transform:perspective(600px) rotateX(60deg);transform-origin:50% 100%;opacity:.5;-webkit-mask-image:linear-gradient(transparent,#000 70%)}
.top{position:absolute;left:120px;right:120px;top:120px;display:flex;justify-content:space-between;font:900 28px M;letter-spacing:.28em;color:#f2c14e}
.top .n{letter-spacing:.05em;color:#cfd8f0;font-weight:700}
.gold{font-family:M;font-weight:900;letter-spacing:-.035em;background:linear-gradient(180deg,#fff3c4 0%,#ffdf8a 35%,#f2c14e 60%,#b8862a 100%);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 4px 0 #7a5410) drop-shadow(0 10px 18px rgba(0,0,0,.5))}
.box{position:absolute;left:120px;right:120px;top:220px;bottom:230px;display:flex;flex-direction:column;justify-content:center}
.handle{position:absolute;right:120px;bottom:120px;font:600 28px P;color:#9fb0d8}
.wa{position:absolute;left:120px;bottom:112px;font:700 28px P;color:#25d366}
.pill{display:inline-block;padding:16px 34px;border-radius:60px;border:2px solid rgba(242,193,78,.6);background:rgba(255,255,255,.07);font:700 30px P;color:#ffdf8a;letter-spacing:.04em;align-self:flex-start}
.card{background:#fff;color:#0d1b3d;border-radius:36px;padding:48px 50px;box-shadow:0 24px 50px rgba(0,0,0,.45)}
.num{width:120px;height:120px;border-radius:30px;background:linear-gradient(160deg,#ffdf8a,#d9a032);color:#0d1b3d;font:900 64px/120px M;text-align:center;margin-bottom:36px;box-shadow:0 14px 30px rgba(0,0,0,.4)}
.row{display:flex;align-items:center;gap:26px;background:#fff;color:#0d1b3d;border-radius:28px;padding:22px 30px;margin:0 0 20px;font:700 36px/46px P;box-shadow:0 12px 26px rgba(0,0,0,.35)}
.row b{flex:none;width:64px;height:64px;border-radius:18px;background:#0d1b3d;color:#f2c14e;font:900 34px/64px M;text-align:center}
.btn{display:inline-block;margin-top:40px;padding:26px 50px;border-radius:70px;background:linear-gradient(180deg,#ffd768,#f2b62e);color:#0d1b3d;font:900 48px M;box-shadow:0 12px 0 #9a6b12,0 22px 36px rgba(0,0,0,.45);align-self:center}
.wabar{margin-top:34px;align-self:center;padding:22px 44px;border-radius:26px;background:#25d366;font:700 44px P;color:#fff}
"""
def page(i, s):
    t = s['type']; inner = ''
    if t == 'cover':
        inner = f"<span class='pill'>{E(s['kicker'])}</span><div class='gold' style='font-size:{s.get('size',150)}px;line-height:.98;margin:40px 0 36px'>{'<br>'.join(map(E, s['title']))}</div><div style='font:700 50px/66px P;color:#fff'>{E(s['sub'])}</div><div style='margin-top:40px;font:600 34px P;color:#ffdf8a'>Swipe karo &rarr;</div>"
    elif t == 'stake':
        inner = f"<div style='font:900 76px/92px M;letter-spacing:-.03em'>{E(s['text'])}</div><div style='margin-top:40px;font:500 38px/54px P;color:#cfd8f0'>{E(s.get('small',''))}</div>"
    elif t == 'step':
        inner = f"<div class='num'>{s['n']}</div><div style='font:700 32px P;color:#ffdf8a;letter-spacing:.12em;margin-bottom:16px'>{E(s['label'])}</div><div class='gold' style='font-size:{s.get('size',88)}px;line-height:1.02;margin-bottom:40px'>{E(s['title'])}</div><div class='card' style='font:700 40px/58px P'>{E(s['body'])}</div>"
    elif t == 'recap':
        inner = f"<div class='gold' style='font-size:90px;line-height:1;margin-bottom:44px'>{E(s['title'])}</div>" + ''.join(f"<div class='row'><b>{k+1}</b>{E(x)}</div>" for k, x in enumerate(s['items'])) + "<div style='margin-top:18px;font:600 32px P;color:#ffdf8a'>Screenshot lo ya save karo</div>"
    elif t == 'cta':
        inner = f"<div style='text-align:center'><div style='font:800 64px M'>{E(s['line'])}</div><div class='gold' style='font-size:200px;line-height:1.1'>{E(s['key'])}</div><div style='font:700 44px/60px P;color:#dfe6ff'>{E(s['sub'])}</div></div><div class='wabar'>WhatsApp +91 97803 10024</div><div style='text-align:center;margin-top:30px;font:500 32px P;color:#cfd8f0'>AK Consultancy · Vikas Puri, New Delhi</div>"
    foot = "<div class='wa'>WhatsApp 97803 10024</div>" if t != 'cta' else ''
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='grid'></div><div class='top'><span>AK CONSULTANCY</span><span class='n'>{i+1}/{N}</span></div><div class='box'>{inner}</div>{foot}<div class='handle'>@ak_consultancyindia</div></body></html>"
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, s in enumerate(S):
        f = os.path.abspath(f"{OUT}/_s{i+1}.html"); open(f, 'w').write(page(i, s))
        pg.goto("file://" + f); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
        over = pg.evaluate("(()=>{const b=document.querySelector('.box');return b.scrollHeight>b.clientHeight+2 || [...document.querySelectorAll('.gold')].some(e=>e.scrollWidth>e.clientWidth+2)})()")
        if over: print('WARN overflow slide', i + 1)
        pg.screenshot(path=f"{OUT}/{i+1}.jpg", type="jpeg", quality=92); os.remove(f)
    b.close()
print('slides', N)
