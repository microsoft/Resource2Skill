# SVG Recipe — 3D Isometric Morphing Bar Charts

## Visual mechanism
Build a fake 3D isometric bar chart by composing each bar from three editable SVG paths: a top diamond, a left vertical face, and a right vertical face. The “morphing” effect comes from duplicating the slide and changing only the top-face Y positions / side-face heights while keeping the same object order and IDs, so PowerPoint Morph interpolates the bars rising from flat slabs into cubes.

## SVG primitives needed
- 1× `<rect>` for the dark studio background
- 1× `<circle>` and 2× `<rect>` for the PowerPoint-style badge in the upper right
- 4× `<path>` for long isometric floor strips
- 12× `<path>` for the 3D bar faces: top, left side, right side for each of four bars
- 4× `<path>` for white decorative icons sitting on top of the bars
- 2× `<path>` for the curved yellow arrow and its separate arrowhead
- 7× `<text>` for the hero headline, strip labels, and badge letter
- 8× `<linearGradient>` for background, strip colors, and glossy top faces
- 2× `<filter>` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft shadows on text, bars, arrow, and badge

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2c1878"/>
      <stop offset="0.55" stop-color="#26105f"/>
      <stop offset="1" stop-color="#16082f"/>
    </linearGradient>
    <linearGradient id="stripC" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#69d5ff"/><stop offset="1" stop-color="#33a8ee"/></linearGradient>
    <linearGradient id="stripB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5c8cff"/><stop offset="1" stop-color="#3866e8"/></linearGradient>
    <linearGradient id="stripM" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f03cff"/><stop offset="1" stop-color="#c51bd9"/></linearGradient>
    <linearGradient id="stripP" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c43fd1"/><stop offset="1" stop-color="#8d168e"/></linearGradient>
    <linearGradient id="topC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8beaff"/><stop offset="1" stop-color="#26aeea"/></linearGradient>
    <linearGradient id="topB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#72b6ff"/><stop offset="1" stop-color="#356cff"/></linearGradient>
    <linearGradient id="topM" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff45f4"/><stop offset="1" stop-color="#bd22d5"/></linearGradient>
    <linearGradient id="topP" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d742cd"/><stop offset="1" stop-color="#8f128d"/></linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="tightShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="4" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <circle cx="1205" cy="82" r="186" fill="#ff6a2a" opacity="0.95" filter="url(#shadow)"/>
  <rect x="1036" y="28" width="180" height="180" rx="16" fill="#c93318" opacity="0.55" filter="url(#tightShadow)"/>
  <rect x="1024" y="18" width="180" height="180" rx="16" fill="#ff4b22" filter="url(#tightShadow)"/>
  <text x="1070" y="155" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="132" font-weight="800" fill="#ffffff">P</text>

  <text x="56" y="208" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="126" font-weight="900" letter-spacing="-4" fill="#ffffff" filter="url(#tightShadow)">ANIMATED</text>
  <text x="60" y="348" width="550" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="102" font-weight="900" fill="#ffc20d" filter="url(#tightShadow)">BAR CHART</text>
  <text x="60" y="570" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="250" font-weight="900" fill="#ffc20d" filter="url(#shadow)">3D</text>

  <path d="M70 720 L680 368 L825 452 L215 804 Z" fill="url(#stripC)" filter="url(#shadow)"/>
  <path d="M215 720 L825 368 L970 452 L360 804 Z" fill="url(#stripB)"/>
  <path d="M360 720 L970 368 L1115 452 L505 804 Z" fill="url(#stripM)"/>
  <path d="M505 720 L1115 368 L1260 452 L650 804 Z" fill="url(#stripP)"/>

  <text x="455" y="552" width="280" transform="rotate(-29 455 552)" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#ffffff" opacity="0.95">Topic 01</text>
  <text x="600" y="612" width="280" transform="rotate(-29 600 612)" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#ffffff" opacity="0.95">Topic 02</text>
  <text x="745" y="672" width="280" transform="rotate(-29 745 672)" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#ffffff" opacity="0.95">Topic 03</text>
  <text x="900" y="718" width="280" transform="rotate(-29 900 718)" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#ffffff" opacity="0.95">Topic 04</text>

  <path d="M670 250 L780 314 L780 430 L670 366 Z" fill="#2b6e91"/>
  <path d="M780 314 L890 250 L890 366 L780 430 Z" fill="#145b7b"/>
  <path d="M670 250 L780 186 L890 250 L780 314 Z" fill="url(#topC)" filter="url(#tightShadow)"/>
  <path d="M735 240 l15 -8 l9 12 l17 -22 l8 20 l24 -2 l-17 15 l17 16 l-25 -2 l-7 19 l-15 -22 l-19 12 l8 -23 z" fill="#ffffff" opacity="0.95"/>

  <path d="M780 250 L890 314 L890 486 L780 422 Z" fill="#294d9b"/>
  <path d="M890 314 L1000 250 L1000 422 L890 486 Z" fill="#213f82"/>
  <path d="M780 250 L890 186 L1000 250 L890 314 Z" fill="url(#topB)" filter="url(#tightShadow)"/>
  <path d="M858 249 c-18 -20 18 -33 30 -12 c8 -24 43 -19 34 7 c24 -3 32 26 5 34 l-70 0 c-24 -4 -20 -30 1 -29 z" fill="#ffffff" opacity="0.95"/>

  <path d="M900 240 L1010 304 L1010 544 L900 480 Z" fill="#80147d"/>
  <path d="M1010 304 L1120 240 L1120 480 L1010 544 Z" fill="#a322aa"/>
  <path d="M900 240 L1010 176 L1120 240 L1010 304 Z" fill="url(#topM)" filter="url(#tightShadow)"/>
  <path d="M966 253 c22 -28 54 -30 74 -7 c-28 -8 -43 -1 -50 22 c18 -13 38 -11 55 8 c-31 -9 -49 -2 -56 19 l-11 -5 c7 -27 -1 -42 -28 -49 c10 -6 20 -4 30 3 c-2 -10 -7 -17 -14 -21 z" fill="#ffffff" opacity="0.95"/>

  <path d="M1010 380 L1120 444 L1120 560 L1010 496 Z" fill="#5d0c67"/>
  <path d="M1120 444 L1230 380 L1230 496 L1120 560 Z" fill="#951698"/>
  <path d="M1010 380 L1120 316 L1230 380 L1120 444 Z" fill="url(#topP)" filter="url(#tightShadow)"/>
  <path d="M1102 392 c18 18 28 43 30 70 l-10 4 c-3 -30 -14 -52 -34 -66 z M1125 390 c18 -22 43 -18 56 0 c-24 0 -39 8 -45 25 z M1088 406 c-30 0 -42 -22 -34 -39 c19 12 33 23 42 36 z M1144 427 c24 -18 48 -11 58 10 c-25 -2 -43 3 -54 16 z" fill="#ffffff" opacity="0.95"/>

  <path d="M716 108 C782 66 858 84 892 151" fill="none" stroke="#ffc943" stroke-width="22" stroke-linecap="round" filter="url(#tightShadow)"/>
  <path d="M897 128 L876 222 L808 160 Z" fill="#ffc943" filter="url(#tightShadow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on real SVG 3D cameras or extrusion attributes; build the isometric illusion from editable path faces instead.
- ❌ Do not use `marker-end` for the curved arrow; draw the arrowhead as a separate filled path.
- ❌ Do not apply `filter` to `<line>` elements; use stroked `<path>` for glow/shadowed arrows.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake isometric projection; PowerPoint translation may drop them.
- ❌ Do not use masks or clip paths on bar faces; keep each face as a simple editable path.

## Composition notes
- Keep the left 45% of the slide as bold headline space; the isometric chart should occupy the lower-right two-thirds and overlap slightly into the title zone for drama.
- Use four saturated strip colors that match the bar tops, then darken the vertical side faces to create the extrusion illusion.
- Draw floor strips first, then labels, then bars from back-left to front-right so overlaps feel physically correct.
- For Morph, create a second slide with identical objects but shorter/flat side faces on slide 1 and taller side faces on slide 2; maintain the same stacking order and IDs.