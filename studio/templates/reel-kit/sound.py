"""Auto-matched sound design from the film's motion events (window.__events). Everything synthesized: no copyrighted audio.
Usage: python3 sound.py events.json duration out.wav"""
import json, sys, wave
import numpy as np

ev = json.load(open(sys.argv[1])); DUR = float(sys.argv[2]); OUT = sys.argv[3]
SR, FPS = 48000, 30
N = int(DUR * SR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)
t_ = lambda d: np.arange(int(d * SR)) / SR

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    s = sig[: N - i] * gain
    L[i:i + len(s)] += s * (1 - max(0, pan)); R[i:i + len(s)] += s * (1 + min(0, pan))

def env(n, a, d):  # attack / exponential decay
    x = np.arange(n) / SR
    return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)

def lp(x, k):  # one-pole low-pass, k in 0..1 (smaller = darker)
    y = np.zeros_like(x); acc = 0.0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y

def whoosh(d=0.45, up=True):
    n = int(d * SR); x = rng.standard_normal(n)
    sweep = np.linspace(0.02, 0.35, n) if up else np.linspace(0.35, 0.02, n)
    y = np.zeros(n); acc = 0.0
    for i in range(n): acc += sweep[i] * (x[i] - acc); y[i] = acc
    shape = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6
    return y * shape * 2.2

def impact(d=1.1):
    t = t_(d); f = 52 * np.exp(-t * 5) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, 0.35)
    click = lp(rng.standard_normal(len(t)), 0.25) * env(len(t), 0.0005, 0.02)
    return body * 1.1 + click * 0.8

def pop(d=0.16, f0=900):
    t = t_(d); f = f0 * np.exp(-t * 18) + 260
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.001, 0.045)

def tick(d=0.09, f=2600):
    t = t_(d); return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * env(len(t), 0.0005, 0.012)

def soft_tk(d=0.05):
    t = t_(d); return lp(rng.standard_normal(len(t)), 0.5) * env(len(t), 0.0005, 0.008)

def riser(d=1.6):
    t = t_(d); f = 180 + 900 * (t / d) ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35
    noise = lp(rng.standard_normal(len(t)), 0.15) * 0.8
    return (tone + noise) * (t / d) ** 2.2

def engine(d):
    t = t_(d); n = lp(rng.standard_normal(len(t)), 0.03) * 3
    hum = 0.25 * np.sin(2 * np.pi * 110 * t + 0.6 * np.sin(2 * np.pi * 0.7 * t))
    shape = np.sin(np.pi * np.linspace(0, 1, len(t))) ** 0.8
    return (n + hum) * shape

# --- music bed: 120 bpm, soft kick, offbeat hats, warm pad (A minor -> F -> C -> G) ---
beat = 0.5
for k in range(int(DUR / beat)):
    tb = k * beat
    if 0.4 < tb < DUR - 0.3:
        tk = t_(0.35); kf = 110 * np.exp(-tk * 28) + 45
        add(np.sin(2 * np.pi * np.cumsum(kf) / SR) * env(len(tk), 0.001, 0.11), tb, 0.55)
        h = rng.standard_normal(int(0.05 * SR)); h = h - lp(h, 0.6)
        add(h * env(len(h), 0.0005, 0.012), tb + beat / 2, 0.16, pan=0.3)
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
bar = 2.0
for k in range(int(DUR / bar) + 1):
    tc = t_(bar + 0.3); s = np.zeros(len(tc))
    for f in chords[k % 4]:
        s += np.sin(2 * np.pi * f * tc) + 0.3 * np.sin(2 * np.pi * f * 2.003 * tc)
    s *= np.minimum(1, tc / 0.25) * np.minimum(1, (bar + 0.3 - tc) / 0.3)
    add(lp(s, 0.08) * 0.09, k * bar)

# --- event-matched effects ---
F = lambda e: e["frame"] / FPS
cuts = sorted(F(e) for e in ev if e["type"] == "cut")
for c in cuts:
    add(whoosh(0.42), c - 0.35, 0.55, pan=-0.2)          # whoosh lands on the cut
    add(impact(0.5), c, 0.35)
for e in ev:
    ty, tt, lab = e["type"], F(e), e.get("label", "")
    if ty == "impact": add(impact(1.2), tt, 0.95)
    elif ty == "pop": add(pop(0.18, 1100), tt, 0.5)
    elif ty == "tick":
        for j in range(5): add(tick(0.08, 1800 + 300 * j), tt + j * 0.045, 0.22)   # rising ticks with the bar
    elif ty == "whoosh": add(whoosh(0.7, up=False), tt - 0.2, 0.45, pan=0.3)
    elif ty == "enter" and not lab.startswith("#") and not lab.startswith("."):
        add(soft_tk(), tt, 0.12)                               # kinetic word taps
    elif ty == "enter" and lab in ("#k1", "#k2", "#k3", "#tag", "#prog", "#wa"):
        add(whoosh(0.3), tt - 0.12, 0.25, pan=0.2)
add(engine(3.0), 0.45, 0.22)                                   # plane flight under the hook
add(impact(0.9), 14 / FPS, 0.55)                               # hook word lands
add(riser(1.7), cuts[-1] - 1.7, 0.45)                          # riser into the CTA cut
add(pop(0.22, 700), 584 / FPS, 0.4)                            # WhatsApp pill

# --- master: soft limiter, normalise to -1 dB, short fades ---
mix = np.stack([L, R], 1)
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix *= 10 ** (-1 / 20) / max(1e-9, np.abs(mix).max())
fade = int(0.25 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
pcm = (mix * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", OUT, round(N / SR, 2), "s,", len(cuts), "cuts")
