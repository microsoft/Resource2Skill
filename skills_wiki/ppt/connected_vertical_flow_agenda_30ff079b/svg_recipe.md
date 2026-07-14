# SVG Recipe — Connected Vertical Flow Agenda

## Visual mechanism
A vertical white track links numbered circular nodes into a continuous agenda journey, while each node anchors a right-aligned topic label. The slide is asymmetrically balanced: a compact title block sits in the left third, and the agenda flow occupies the right side with precise vertical rhythm.

## SVG primitives needed
- 1× `<rect>` for the full-slide teal background
- 2× `<path>` for subtle oversized ambient decorative curves in the background
- 1× `<rect>` for the thin vertical title accent bar
- 1× `<line>` for the central connected agenda track
- 5× `<circle>` for dark numbered agenda nodes
- 12× `<text>` for title words, node numbers, and agenda item labels
- 2× `<linearGradient>` for premium background and node fills
- 1× `<radialGradient>` for a soft background glow
- 1× `<filter id="nodeShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge`, applied to node circles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgTeal" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#19C7AE"/>
      <stop offset="55%" stop-color="#17BFA8"/>
      <stop offset="100%" stop-color="#10AF9D"/>
    </linearGradient>

    <radialGradient id="softGlow" cx="76%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#4FE3D1" stop-opacity="0.36"/>
      <stop offset="56%" stop-color="#1ABFA8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0EA995" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="nodeFill" x1="735" y1="55" x2="807" y2="128">
      <stop offset="0%" stop-color="#53606A"/>
      <stop offset="100%" stop-color="#26313A"/>
    </linearGradient>

    <filter id="nodeShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="3" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgTeal)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#softGlow)"/>

  <path d="M-80,610 C120,530 230,670 410,590 C570,520 660,610 790,570 C910,532 990,430 1370,500 L1370,760 L-80,760 Z"
        fill="#FFFFFF" opacity="0.055"/>
  <path d="M990,-90 C1110,-20 1110,90 1230,125 C1320,152 1390,100 1435,70 L1435,-120 Z"
        fill="#FFFFFF" opacity="0.07"/>

  <rect x="92" y="294" width="6" height="134" rx="3" fill="#FFFFFF"/>

  <text x="108" y="349" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="36" font-weight="800" fill="#344955" letter-spacing="-1">
    PRESENTATION
  </text>
  <text x="108" y="391" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="36" font-weight="800" fill="#FFFFFF" letter-spacing="-1">
    AGENDA
  </text>

  <line x1="770" y1="92" x2="770" y2="612"
        stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.92"/>

  <circle cx="770" cy="92" r="36" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="3" filter="url(#nodeShadow)"/>
  <text x="746" y="103" width="48"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="500" fill="#FFFFFF" text-anchor="middle">
    01
  </text>
  <text x="818" y="103" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="400" fill="#FFFFFF">
    Introduction
  </text>

  <circle cx="770" cy="222" r="36" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="3" filter="url(#nodeShadow)"/>
  <text x="746" y="233" width="48"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="500" fill="#FFFFFF" text-anchor="middle">
    02
  </text>
  <text x="818" y="233" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="400" fill="#FFFFFF">
    Services
  </text>

  <circle cx="770" cy="352" r="36" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="3" filter="url(#nodeShadow)"/>
  <text x="746" y="363" width="48"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="500" fill="#FFFFFF" text-anchor="middle">
    03
  </text>
  <text x="818" y="363" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="400" fill="#FFFFFF">
    Clients
  </text>

  <circle cx="770" cy="482" r="36" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="3" filter="url(#nodeShadow)"/>
  <text x="746" y="493" width="48"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="500" fill="#FFFFFF" text-anchor="middle">
    04
  </text>
  <text x="818" y="493" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="400" fill="#FFFFFF">
    Portfolio
  </text>

  <circle cx="770" cy="612" r="36" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="3" filter="url(#nodeShadow)"/>
  <text x="746" y="623" width="48"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="500" fill="#FFFFFF" text-anchor="middle">
    05
  </text>
  <text x="818" y="623" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="400" fill="#FFFFFF">
    Contact us
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` to repeat the agenda nodes; duplicate each circle/text group explicitly so PowerPoint can edit every node.
- ❌ Do not apply filters to the vertical `<line>`; line filters may be dropped, so put shadow/glow only on circles or paths.
- ❌ Do not use `marker-end` arrows for the flow; this agenda relies on a clean track, not arrowheads.
- ❌ Do not place text without `width`; agenda labels need explicit widths to render predictably in PowerPoint.
- ❌ Do not use masks or clip paths for non-image shapes; simple circles and lines reproduce this technique cleanly.

## Composition notes
- Keep the left title block around the left 25–30% of the slide; the vertical accent bar visually anchors the otherwise minimal text.
- Place the agenda track slightly right of center, around x=760–790, leaving enough room for labels to the right.
- Use equal vertical spacing between node centers; this mathematical rhythm is the main reason the slide feels polished.
- Maintain high contrast: bright white text and track against teal, with dark charcoal nodes for visual punctuation.