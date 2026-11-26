# NH ONE – Intro Video

`NH_ONE_Intro.mp4`: 27 s, 1920×1080, 30 fps, H.264 + AAC, with an original synthesized soundtrack.

Scenes: opening line → "Excellence in Motion" → product categories → Why NH ONE → logo reveal → end card with website and social handles.

## Re-render
```
python3 audio.py      # writes music.wav
node render.js        # renders frames from intro.html, writes NH_ONE_Intro.mp4 (needs playwright + ffmpeg)
```
Open `intro.html` in a browser to watch a live loop. Text, timings and colours are in `intro.html`.
