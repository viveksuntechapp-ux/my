import numpy as np, wave
SR=44100; DUR=27.0; N=int(SR*DUR); t=np.arange(N)/SR
rng=np.random.default_rng(3)
out=np.zeros((N,2))
def env(a,b,fi,fo):
    return np.clip(np.minimum((t-a)/fi,(b-t)/fo),0,1)
def add(sig,s=0,pan=0.0,g=1.0):
    i=int(s*SR); n=min(len(sig),N-i)
    out[i:i+n,0]+=sig[:n]*g*(1-pan)/1; out[i:i+n,1]+=sig[:n]*g*(1+pan)/1
def note(f): return 440*2**((f-69)/12)
# pad: A minor -> F -> C -> G progression, detuned saws softened
chords=[(0,[57,60,64]),(6.75,[53,57,60]),(13.5,[48,55,64]),(17.4,[55,59,62]),(18.6,[57,64,69]),]
pad=np.zeros(N)
for i,(st,ns) in enumerate(chords):
    en=chords[i+1][0] if i+1<len(chords) else DUR
    e=env(st,en+0.6,0.8 if i else 1.5,1.0)
    for m in ns:
        for d in (-0.08,0.08):
            f=note(m)*(1+d/100*12)
            pad+=e*(np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)+0.12*np.sin(2*np.pi*3*f*t))
pad*=0.035*np.clip(1-np.clip((t-25.5)/1.5,0,1),0,1)
out[:,0]+=pad; out[:,1]+=pad
# sub bass pulses (eighth notes @120bpm) from 3.2s until 17.4
bassroots={0:45,6.75:41,13.5:36}
def root(x):
    r=45
    for k,v in bassroots.items():
        if x>=k: r=v
    return r
for k in np.arange(3.2,17.4,0.25):
    L=int(0.22*SR); tt=np.arange(L)/SR; f=note(root(k)-12)
    s=np.sin(2*np.pi*f*tt)*np.exp(-tt*9)*(0.5 if (round((k-3.2)/0.25))%2 else 0.8)
    add(s,k,g=0.35)
# kicks on beats 3.2..17.4 (skip during category breathing? keep)
def kick():
    L=int(0.4*SR); tt=np.arange(L)/SR; f=50+120*np.exp(-tt*35)
    ph=2*np.pi*np.cumsum(f)/SR; return np.sin(ph)*np.exp(-tt*7)
K=kick()
for k in np.arange(3.2,17.4,0.5): add(K,k,g=0.55)
# hats
def hat():
    L=int(0.06*SR); n=rng.standard_normal(L); n=np.diff(n,prepend=0); return n*np.exp(-np.arange(L)/SR*60)
for k in np.arange(6.6,17.4,0.25):
    if round((k-6.6)/0.25)%2: add(hat(),k,pan=0.3,g=0.06)
# whooshes at transitions
def whoosh(L=1.0):
    n=int(L*SR); x=rng.standard_normal(n); tt=np.arange(n)/SR
    # moving lowpass by one-pole with varying coefficient
    y=np.zeros(n); a=np.clip(0.02+0.25*np.sin(np.pi*tt/L)**2,0,1); acc=0
    for i in range(n): acc+=a[i]*(x[i]-acc); y[i]=acc
    return y*np.sin(np.pi*tt/L)**2
for st,L,g in [(0.2,2.6,0.5),(3.0,0.8,0.6),(6.3,0.8,0.5),(13.3,0.8,0.5),(17.3,1.0,0.7),(21.0,1.2,0.4)]:
    add(whoosh(L),st,pan=0.0,g=g)
# riser 15.6 -> 17.8
L=2.2; n=int(L*SR); tt=np.arange(n)/SR; f=200*2**(tt/L*3)
r=np.sin(2*np.pi*np.cumsum(f)/SR)*(tt/L)**2*0.12+rng.standard_normal(n)*(tt/L)**3*0.05
add(r,15.6)
# impact at 18.1 (logo hit)
L=3.5; n=int(L*SR); tt=np.arange(n)/SR
boom=np.sin(2*np.pi*np.cumsum(40+60*np.exp(-tt*6))/SR)*np.exp(-tt*1.6)
noise=rng.standard_normal(n); sm=np.convolve(noise,np.ones(40)/40,'same')*np.exp(-tt*3)
add(boom*0.9+sm*0.6,18.1)
# shimmer chime at 20.0 (sweep) and 22.6 (url)
def chime(m,L=2.5):
    n=int(L*SR); tt=np.arange(n)/SR; f=note(m)
    return (np.sin(2*np.pi*f*tt)+0.5*np.sin(2*np.pi*f*2.01*tt)+0.25*np.sin(2*np.pi*f*3*tt))*np.exp(-tt*2.2)
for st,m in [(20.0,81),(20.12,88),(22.6,84),(22.72,88),(23.7,91)]:
    add(chime(m),st,pan=0.2,g=0.07)
# simple stereo reverb-ish: delays
wet=np.zeros_like(out)
for d,g in [(0.031,0.35),(0.067,0.3),(0.113,0.25),(0.171,0.2),(0.243,0.15)]:
    k=int(d*SR); wet[k:,0]+=out[:-k,1]*g; wet[k:,1]+=out[:-k,0]*g
out=out+wet*0.6
out*=np.clip(np.minimum(t/0.3,(DUR-t)/0.6),0,1)[:,None]
out=np.tanh(out*1.3)
out/=np.abs(out).max()/0.89
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out*32767).astype('<i2').tobytes())
print('ok')
