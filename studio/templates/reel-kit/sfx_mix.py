"""Auto-matched sound for a Motion film: SFX Kit (CC0) sounds placed on the film's events + a synthesized 120 bpm bed.
whoosh 0.35 s before every cut, pop on cards, click on ticks, impact on slams, rising ticks on progress, riser + hit on CTA.
Master: about -14 LUFS integrated, true-peak ceiling -1 dB.
Usage: python3 sfx_mix.py events.json duration out.wav"""
import json, sys, os
import numpy as np, soundfile as sf, pyloudnorm as pyln

ev = json.load(open(sys.argv[1])); D = float(sys.argv[2]); OUT = sys.argv[3]
SR, FPS = 48000, 30
S = os.path.expanduser('~/ak-toolkit/sfx-kit/sounds/')
out = np.zeros((int(SR * D), 2))
cache = {}

def load(p):
    if p not in cache:
        a, sr = sf.read(S + p, always_2d=True)
        if sr != SR:
            idx = np.arange(0, len(a), sr / SR)
            a = np.stack([np.interp(idx, np.arange(len(a)), a[:, c]) for c in range(a.shape[1])], 1)
        if a.shape[1] == 1: a = np.repeat(a, 2, 1)
        cache[p] = a[:, :2] / max(1e-9, np.abs(a).max())
    return cache[p]

def place(p, t, g, sig=None):
    a = (load(p) if sig is None else sig) * g; i = int(max(0, t) * SR); n = min(len(a), len(out) - i)
    if n > 0: out[i:i + n] += a[:n]

# bed: 120 bpm soft kick, offbeat hat, warm pad (A min, F, C, G)
t = np.arange(len(out)) / SR; bed = np.zeros(len(out)); rng = np.random.default_rng(3)
for b in np.arange(0.5, D - 0.3, 0.5):
    i = int(b * SR); n = int(0.25 * SR); tt = np.arange(n) / SR
    if i + n < len(bed): bed[i:i + n] += 0.5 * np.sin(2 * np.pi * (50 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12)
    j = int((b + 0.25) * SR); m = int(0.05 * SR)
    if j + m < len(bed): bed[j:j + m] += 0.07 * rng.standard_normal(m) * np.exp(-np.arange(m) / SR * 80)
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
pad = np.zeros(len(out))
for k in range(int(D / 2) + 1):
    i0 = int(k * 2 * SR); i1 = min(len(out), int((k * 2 + 2.3) * SR))
    if i0 >= len(out): break
    tc = np.arange(i1 - i0) / SR; s = sum(np.sin(2 * np.pi * f * tc) for f in chords[k % 4])
    s *= np.minimum(1, tc / 0.25) * np.minimum(1, (tc[-1] - tc + 1e-3) / 0.3)
    pad[i0:i1] += s * 0.035
bed = (bed + pad) * np.minimum(1, t / 0.4) * np.minimum(1, (D - t) / 0.6)
out += np.stack([bed, bed], 1) * 0.55

F = lambda e: e['frame'] / FPS
cuts = sorted(F(e) for e in ev if e['type'] == 'cut')
for c in cuts:
    place('whooshes/whoosh-fast-medium.wav', c - 0.35, 0.55)       # whoosh lands on the cut
    place('impacts/impact-light-firm.wav', c, 0.35)
for e in ev:
    ty, tt = e['type'], F(e)
    if ty == 'impact': place('impacts/impact-deep-hard.wav', tt, 0.85); place('cinematic-hits/cinematic-slam-big.wav', tt, 0.25)
    elif ty == 'pop': place('pops/pop-medium-in.wav', tt, 0.5)
    elif ty == 'click': place('interface/click-button-firm.wav', tt, 0.6)
    elif ty == 'tick':
        for j in range(5): place('interface/click-tap-soft.wav', tt - 0.2 + j * 0.05, 0.18 + 0.06 * j)   # rising ticks
    elif ty == 'whoosh': place('whooshes/whoosh-medium-soft.wav', tt - 0.2, 0.45)
    elif ty == 'riser': place('risers-and-fallers/riser-1s-strong.wav', tt + 0.67, 0.5)
if cuts:
    place('cinematic-hits/cinematic-slam-big.wav', cuts[-1], 0.5)                    # hit on the CTA cut
    place('logo-stings/sting-bright-short.wav', cuts[-1] + 1.6, 0.35)

# master to about -14 LUFS, peak ceiling -1 dB
meter = pyln.Meter(SR); ceil = 10 ** (-1.2 / 20)
for _ in range(5):   # loudness up, soft limiter on the peaks, repeat until about -14 LUFS
    out = pyln.normalize.loudness(out, meter.integrated_loudness(out), -14.0)
    out = ceil * np.tanh(out / ceil)
fade = int(0.2 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
sf.write(OUT, out, SR, subtype='PCM_16')
print('mix', OUT, round(D, 2), 's', len(cuts), 'cuts', 'LUFS', round(meter.integrated_loudness(out), 1), 'peak dB', round(20 * np.log10(np.abs(out).max()), 2))
