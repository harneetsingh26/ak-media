import numpy as np, soundfile as sf, subprocess, os
SR=48000; D=9.0; S=os.path.expanduser('~/ak-toolkit/sfx-kit/sounds/')
out=np.zeros((int(SR*D),2))
def load(p):
    a,sr=sf.read(S+p,always_2d=True)
    if sr!=SR:
        idx=np.arange(0,len(a),sr/SR); a=np.stack([np.interp(idx,np.arange(len(a)),a[:,c]) for c in range(a.shape[1])],1)
    if a.shape[1]==1: a=np.repeat(a,2,1)
    return a[:,:2]
def place(p,t,g):
    a=load(p)*g; i=int(t*SR); n=min(len(a),len(out)-i)
    if n>0: out[i:i+n]+=a[:n]
# 120 bpm bed: soft kick, offbeat hat, pad
t=np.arange(len(out))/SR; bed=np.zeros(len(out))
for b in np.arange(0,D,0.5):
    i=int(b*SR); n=int(0.25*SR); tt=np.arange(n)/SR
    if i+n<len(bed): bed[i:i+n]+=0.5*np.sin(2*np.pi*(50+60*np.exp(-tt*30))*tt)*np.exp(-tt*12)
    j=int((b+0.25)*SR); m=int(0.05*SR)
    rng=np.random.default_rng(int(b*10))
    if j+m<len(bed): bed[j:j+m]+=0.08*rng.standard_normal(m)*np.exp(-np.arange(m)/SR*80)
pad=0.06*(np.sin(2*np.pi*220*t)+np.sin(2*np.pi*277.2*t)+np.sin(2*np.pi*329.6*t))*np.minimum(1,t/1.5)*np.minimum(1,(D-t)/0.8)
out+=np.stack([bed+pad]*2,1)*0.5
ev=[('impacts/impact-deep-hard.wav',0.05,0.9),('whooshes/whoosh-fast-medium.wav',0.0,0.5),
('pops/pop-medium-in.wav',0.75,0.5),('whooshes/whoosh-medium-medium.wav',2.55,0.7),('impacts/impact-deep-firm.wav',2.9,0.8),
('whooshes/whoosh-fast-soft.wav',3.3,0.5),('interface/click-button-firm.wav',3.63,0.8),
('whooshes/whoosh-fast-soft.wav',3.85,0.5),('interface/click-button-firm.wav',4.18,0.8),
('whooshes/whoosh-fast-soft.wav',4.4,0.5),('interface/click-button-firm.wav',4.73,0.8),
('whooshes/whoosh-medium-medium.wav',5.35,0.7),('risers-and-fallers/riser-1s-strong.wav',5.2,0.6),
('cinematic-hits/cinematic-slam-big.wav',6.2,0.8),('pops/pop-large-in.wav',6.8,0.8),('swishes-and-zips/swish-medium.wav',7.12,0.6),
('logo-stings/sting-bright-short.wav',7.4,0.5)]
for p,tt,g in ev: place(p,tt,g)
out*=10**(-1/20)/np.max(np.abs(out))
sf.write('/tmp/claude-0/story/mix.wav',out,SR)
