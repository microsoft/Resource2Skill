# SVG Recipe — Vertical Metric Stack

## Visual mechanism
A tall, centered “metric tower” uses oversized numerals as the primary visual weight, with each KPI sitting in a soft glass card and aligned to a thin vertical index rail. Subtle gradients, glow blobs, divider lines, and compact label/pill annotations make the stack feel premium while preserving the simple vertical-reading rhythm.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× large rounded `<rect>` for the central glass container
- 4× rounded `<rect>` for individual metric rows
- 4× small rounded `<rect>` for change/status pills
- 1× narrow rounded `<rect>` for the vertical index rail
- 4× `<circle>` for rail nodes aligned to each metric
- 3× `<line>` for row dividers
- 3× decorative `<path>` elements for organic glow/swoosh accents
- 16× `<text>` elements for eyebrow, title, metric values, labels, sublabels, and pills
- 3× `<linearGradient>` for background, glass cards, and accent fills
- 1× `<radialGradient>` for ambient glow
- 2× `<filter>` definitions: one soft shadow for cards, one blur glow for decorative paths/circles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#08111F"/>
      <stop offset="48%" stop-color="#111A2E"/>
      <stop offset="100%" stop-color="#071019"/>
    </linearGradient>

    <linearGradient id="glass" x1="250" y1="80" x2="1030" y2="640">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.17"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="rowFill" x1="270" y1="110" x2="1010" y2="610">
      <stop offset="0%" stop-color="#172A42" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#0D1727" stop-opacity="0.92"/>
    </linearGradient>

    <linearGradient id="accent" x1="0" y1="0" x2="0" y2="520">
      <stop offset="0%" stop-color="#58E6FF"/>
      <stop offset="45%" stop-color="#9B7CFF"/>
      <stop offset="100%" stop-color="#FFCF5A"/>
    </linearGradient>

    <radialGradient id="orb" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5CE1FF" stop-opacity="0.52"/>
      <stop offset="70%" stop-color="#5CE1FF" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="#5CE1FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0.03  0 0 0 0 0.09  0 0 0 0.42 0" result="shade"/>
      <feMerge>
        <feMergeNode in="shade"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="20" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <circle cx="1040" cy="126" r="230" fill="url(#orb)" filter="url(#glow)" opacity="0.75"/>
  <path d="M-70,122 C110,18 225,34 337,112 C438,183 548,180 662,128"
        fill="none" stroke="#58E6FF" stroke-width="34" stroke-linecap="round" opacity="0.10" filter="url(#glow)"/>
  <path d="M1010,705 C1115,590 1203,571 1352,623 L1352,760 L1010,760 Z"
        fill="#FFCF5A" opacity="0.13" filter="url(#glow)"/>

  <text x="80" y="64" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="700" letter-spacing="3" fill="#8EA3BD">EXECUTIVE KPI SNAPSHOT</text>
  <text x="80" y="102" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="30"
        font-weight="700" fill="#FFFFFF">Vertical Metric Stack</text>
  <text x="80" y="132" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#9CAFCA">One read path. Four decisive numbers. No chart decoding required.</text>

  <rect x="230" y="84" width="820" height="566" rx="46" fill="url(#glass)" stroke="#FFFFFF"
        stroke-opacity="0.16" stroke-width="1.2" filter="url(#shadow)"/>

  <text x="188" y="596" width="280" transform="rotate(-90 188 596)"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="5" fill="#61748F">FY26 OPERATING PULSE</text>

  <rect x="274" y="128" width="8" height="478" rx="4" fill="url(#accent)"/>
  <circle cx="278" cy="166" r="9" fill="#58E6FF"/>
  <circle cx="278" cy="298" r="9" fill="#9B7CFF"/>
  <circle cx="278" cy="430" r="9" fill="#C093FF"/>
  <circle cx="278" cy="562" r="9" fill="#FFCF5A"/>

  <rect x="308" y="112" width="686" height="108" rx="28" fill="url(#rowFill)" stroke="#FFFFFF"
        stroke-opacity="0.11" filter="url(#shadow)"/>
  <text x="344" y="181" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="72"
        font-weight="800" fill="#FFFFFF">87%</text>
  <text x="660" y="154" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#DDE8F8">Retention</text>
  <text x="660" y="181" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#8DA1BE">enterprise accounts renewed</text>
  <rect x="878" y="143" width="82" height="32" rx="16" fill="#143B46" stroke="#58E6FF" stroke-opacity="0.45"/>
  <text x="894" y="165" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        font-weight="700" fill="#77F1FF">+9 pts</text>

  <line x1="340" y1="244" x2="962" y2="244" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>

  <rect x="308" y="244" width="686" height="108" rx="28" fill="url(#rowFill)" stroke="#FFFFFF"
        stroke-opacity="0.11" filter="url(#shadow)"/>
  <text x="344" y="313" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="72"
        font-weight="800" fill="#FFFFFF">$42M</text>
  <text x="660" y="286" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#DDE8F8">Pipeline</text>
  <text x="660" y="313" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#8DA1BE">qualified next-quarter value</text>
  <rect x="878" y="275" width="82" height="32" rx="16" fill="#241E46" stroke="#9B7CFF" stroke-opacity="0.50"/>
  <text x="895" y="297" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        font-weight="700" fill="#BBA8FF">1.6×</text>

  <line x1="340" y1="376" x2="962" y2="376" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>

  <rect x="308" y="376" width="686" height="108" rx="28" fill="url(#rowFill)" stroke="#FFFFFF"
        stroke-opacity="0.11" filter="url(#shadow)"/>
  <text x="344" y="445" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="72"
        font-weight="800" fill="#FFFFFF">14.8</text>
  <text x="660" y="418" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#DDE8F8">Cycle Days</text>
  <text x="660" y="445" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#8DA1BE">median time to launch</text>
  <rect x="878" y="407" width="82" height="32" rx="16" fill="#332246" stroke="#C093FF" stroke-opacity="0.50"/>
  <text x="895" y="429" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        font-weight="700" fill="#D9C4FF">-22%</text>

  <line x1="340" y1="508" x2="962" y2="508" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>

  <rect x="308" y="508" width="686" height="108" rx="28" fill="url(#rowFill)" stroke="#FFFFFF"
        stroke-opacity="0.11" filter="url(#shadow)"/>
  <text x="344" y="577" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="72"
        font-weight="800" fill="#FFFFFF">3.2×</text>
  <text x="660" y="550" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#DDE8F8">Expansion</text>
  <text x="660" y="577" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#8DA1BE">net revenue multiplier</text>
  <rect x="878" y="539" width="82" height="32" rx="16" fill="#3A3317" stroke="#FFCF5A" stroke-opacity="0.55"/>
  <text x="894" y="561" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        font-weight="700" fill="#FFE083">AHEAD</text>

  <path d="M1016,134 C1064,210 1062,492 1018,584" fill="none" stroke="#FFFFFF"
        stroke-width="2" stroke-linecap="round" stroke-dasharray="2 12" opacity="0.18"/>
</svg>
```

## Avoid in this skill
- ❌ Building the stack as an HTML table inside `<foreignObject>`; PowerPoint editability will fail.
- ❌ Using `<textPath>` for the vertical side label; rotate a normal `<text>` element instead.
- ❌ Applying blur/shadow filters to `<line>` dividers; filters on lines are dropped, so keep dividers simple.
- ❌ Overcrowding each row with mini charts; this shell works because the numerals dominate and the annotations stay secondary.
- ❌ Using `<use>` or `<symbol>` to repeat row components; duplicate native shapes explicitly for reliable translation.

## Composition notes
- Keep the metric column centered and tall, occupying roughly 60–70% of slide height so the numbers read as one stacked object.
- Place labels and change pills to the right of each number; avoid splitting attention with large text on both sides.
- Use a narrow vertical rail or node system to reinforce the stack rhythm without becoming a chart axis.
- Maintain generous dark negative space around the glass container; ambient glow accents should frame the stack, not compete with the KPIs.