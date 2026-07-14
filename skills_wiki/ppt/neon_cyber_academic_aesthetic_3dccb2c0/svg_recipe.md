# SVG Recipe — Neon Cyber-Academic Aesthetic

## Visual mechanism
A deep purple-black canvas is overlaid with faint scientific geometry, then energized by blurred neon organic “light leaks” and crisp data/chart elements. The style works by contrasting rigorous academic structure with fluid cyan–magenta glow, keeping a clean text zone for authority and readability.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 2× `<radialGradient>` for cyan and magenta neon blob color falloff
- 1× `<linearGradient>` for subtle chart/data panel fill
- 2× `<filter>` using `feGaussianBlur` for large soft neon bloom and smaller glow accents
- 3× large organic `<path>` blobs for blurred cyan, violet, and magenta edge lighting
- 20–35× faint `<path>` hexagons for the academic/scientific grid texture
- 1× rounded `<rect>` for the glassy data panel
- 4–6× `<line>` for chart axes and guide rules
- 2–3× neon `<path>` data curves for chart_data content
- 8–12× `<circle>` for glowing data nodes
- 5–8× `<text>` elements with explicit `width` for title, subtitle, labels, and metrics
- Optional thin `<path>` brackets/corners for cybernetic HUD framing

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="cyanBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00ffff" stop-opacity="0.95"/>
      <stop offset="45%" stop-color="#00b7ff" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#00ffff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="magentaBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff00ff" stop-opacity="0.95"/>
      <stop offset="46%" stop-color="#7a2cff" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#ff00ff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.11"/>
      <stop offset="55%" stop-color="#2d2150" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00ffff" stop-opacity="0.06"/>
    </linearGradient>
    <filter id="megaBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="55"/>
    </filter>
    <filter id="neonGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="panelShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#120e1f"/>

  <path d="M820 -120 C990 -160 1210 -20 1260 150 C1310 330 1130 410 980 360 C830 310 720 120 820 -120 Z"
        fill="url(#magentaBloom)" filter="url(#megaBlur)" opacity="0.86"/>
  <path d="M-90 470 C40 360 250 430 310 580 C370 730 160 820 -30 760 C-190 710 -220 570 -90 470 Z"
        fill="url(#cyanBloom)" filter="url(#megaBlur)" opacity="0.82"/>
  <path d="M118 92 C210 42 315 78 350 160 C382 238 292 306 182 278 C82 252 38 142 118 92 Z"
        fill="url(#magentaBloom)" filter="url(#megaBlur)" opacity="0.38"/>

  <g stroke="#ffffff" stroke-width="1.1" fill="none" opacity="0.075">
    <path d="M60 68 L95 48 L130 68 L130 108 L95 128 L60 108 Z"/>
    <path d="M130 128 L165 108 L200 128 L200 168 L165 188 L130 168 Z"/>
    <path d="M200 68 L235 48 L270 68 L270 108 L235 128 L200 108 Z"/>
    <path d="M270 128 L305 108 L340 128 L340 168 L305 188 L270 168 Z"/>
    <path d="M340 68 L375 48 L410 68 L410 108 L375 128 L340 108 Z"/>
    <path d="M410 128 L445 108 L480 128 L480 168 L445 188 L410 168 Z"/>
    <path d="M62 248 L97 228 L132 248 L132 288 L97 308 L62 288 Z"/>
    <path d="M132 308 L167 288 L202 308 L202 348 L167 368 L132 348 Z"/>
    <path d="M202 248 L237 228 L272 248 L272 288 L237 308 L202 288 Z"/>
    <path d="M272 308 L307 288 L342 308 L342 348 L307 368 L272 348 Z"/>
    <path d="M930 70 L965 50 L1000 70 L1000 110 L965 130 L930 110 Z"/>
    <path d="M1000 130 L1035 110 L1070 130 L1070 170 L1035 190 L1000 170 Z"/>
    <path d="M1070 70 L1105 50 L1140 70 L1140 110 L1105 130 L1070 110 Z"/>
    <path d="M930 250 L965 230 L1000 250 L1000 290 L965 310 L930 290 Z"/>
    <path d="M1000 310 L1035 290 L1070 310 L1070 350 L1035 370 L1000 350 Z"/>
    <path d="M1070 250 L1105 230 L1140 250 L1140 290 L1105 310 L1070 290 Z"/>
  </g>

  <g opacity="0.22" stroke="#00ffff" stroke-width="1" fill="none">
    <path d="M72 612 L72 568 L116 568"/>
    <path d="M1206 92 L1206 136 L1162 136"/>
    <path d="M552 640 L596 640 L596 684"/>
  </g>

  <text x="78" y="155" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600"
        letter-spacing="5" fill="#00ffff" opacity="0.92">RESEARCH SYSTEMS / 2026</text>
  <text x="76" y="242" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800"
        letter-spacing="1.5" fill="#ffffff">AI-ASSISTED</text>
  <text x="76" y="315" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800"
        letter-spacing="1.5" fill="#ffffff">KNOWLEDGE</text>
  <text x="76" y="388" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800"
        letter-spacing="1.5" fill="#ffffff">DISCOVERY</text>
  <text x="80" y="444" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#c9c6dd" opacity="0.9">
    Mapping evidence, uncertainty, and machine reasoning across high-volume academic corpora.
  </text>

  <rect x="730" y="180" width="430" height="360" rx="28" fill="url(#panelFill)" stroke="#8a7cff"
        stroke-opacity="0.34" stroke-width="1.4" filter="url(#panelShadow)"/>
  <text x="760" y="226" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="3" fill="#ffffff" opacity="0.84">MODEL PERFORMANCE</text>
  <text x="760" y="263" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800"
        fill="#00ffff">94.7%</text>
  <text x="918" y="260" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#d7d2ec" opacity="0.76">
    validated synthesis accuracy
  </text>

  <line x1="780" y1="468" x2="1108" y2="468" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <line x1="780" y1="316" x2="780" y2="468" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>
  <line x1="780" y1="418" x2="1108" y2="418" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="6 8"/>
  <line x1="780" y1="368" x2="1108" y2="368" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="6 8"/>

  <path d="M790 448 C835 426 860 438 900 390 C935 348 972 366 1002 326 C1035 282 1068 304 1102 262"
        fill="none" stroke="#00ffff" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M790 430 C830 410 862 404 896 418 C930 432 970 400 1008 386 C1046 372 1072 390 1102 340"
        fill="none" stroke="#ff00ff" stroke-width="3" stroke-linecap="round" opacity="0.78" filter="url(#neonGlow)"/>

  <circle cx="900" cy="390" r="5.5" fill="#00ffff" filter="url(#neonGlow)"/>
  <circle cx="1002" cy="326" r="5.5" fill="#00ffff" filter="url(#neonGlow)"/>
  <circle cx="1102" cy="262" r="6.5" fill="#ffffff" filter="url(#neonGlow)"/>
  <circle cx="896" cy="418" r="4.5" fill="#ff00ff" filter="url(#neonGlow)"/>
  <circle cx="1008" cy="386" r="4.5" fill="#ff00ff" filter="url(#neonGlow)"/>

  <text x="780" y="504" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#aaa4c3">Q1</text>
  <text x="885" y="504" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#aaa4c3">Q2</text>
  <text x="995" y="504" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#aaa4c3">Q3</text>
  <text x="1080" y="504" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#aaa4c3">Q4</text>

  <path d="M762 562 L790 562 L804 584 L832 520 L862 562 L1115 562"
        fill="none" stroke="#00ffff" stroke-width="2" stroke-linecap="round" opacity="0.58"/>
  <text x="860" y="570" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#dcd8ef" opacity="0.82">
    live corpus signal stream
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the hex grid; draw faint editable `<path>` hexagons instead.
- ❌ Applying blur filters to `<line>` elements for glowing axes; use plain lines for axes and filtered `<path>` curves/circles for glow.
- ❌ Heavy, high-opacity grids behind title text; the academic geometry should be atmospheric, not a readability hazard.
- ❌ Centering every neon blob; place glows partially off-canvas to create cinematic depth.
- ❌ Using bitmap-only backgrounds for the entire look; keep text, charts, grid, and neon paths editable whenever possible.

## Composition notes
- Keep the main title block on the left or center-left with a generous dark “quiet zone” behind it.
- Push the largest neon blobs to opposite corners, usually magenta top-right and cyan bottom-left, for asymmetric balance.
- Use the chart/data panel as the crisp counterweight to the organic background; it should feel like a floating research HUD.
- Maintain a limited palette: deep purple-black base, white text, cyan primary signal, magenta secondary signal.