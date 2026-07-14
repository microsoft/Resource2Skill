# SVG Recipe — Modern Floating Orb Sequence

## Visual mechanism
A horizontal process narrative is anchored by a subtle center axis, with large saturated circular “orbs” floating above it through soft shadows and highlights. Each orb carries a giant step number, while tightly aligned text blocks below convert the sequence into a clean executive roadmap.

## SVG primitives needed
- 1× `<rect>` for the full-slide light background.
- 1× `<rect>` for the central connecting axis behind the orbs.
- 3× `<path>` for soft decorative background blobs and motion accents.
- 4× `<circle>` for translucent colored halos behind each orb.
- 4× `<circle>` for the main gradient-filled floating orbs.
- 4× `<rect>` for small pill labels above the orbs.
- 17× `<text>` for title, subtitle, orb numbers, pill labels, step titles, and body copy.
- 5× `<linearGradient>` for the background wash and orb fills.
- 1× `<radialGradient>` for subtle orb specular highlights.
- 1× `<filter id="orbShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for orb depth.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for background accent glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="orbTeal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2DE2D1"/>
      <stop offset="100%" stop-color="#009688"/>
    </linearGradient>
    <linearGradient id="orbBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#64B5FF"/>
      <stop offset="100%" stop-color="#2196F3"/>
    </linearGradient>
    <linearGradient id="orbIndigo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7986FF"/>
      <stop offset="100%" stop-color="#3F51B5"/>
    </linearGradient>
    <linearGradient id="orbPurple" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D65AE8"/>
      <stop offset="100%" stop-color="#9C27B0"/>
    </linearGradient>

    <radialGradient id="orbHighlight" cx="35%" cy="28%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="orbShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="13" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.05  0 0 0 0 0.08  0 0 0 0 0.13  0 0 0 0.24 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-40,134 C110,60 260,74 338,170 C408,255 324,330 176,312 C48,297 -54,246 -40,134 Z"
        fill="#DFF7F5" opacity="0.72" filter="url(#softGlow)"/>
  <path d="M1130,74 C1254,46 1346,112 1320,214 C1292,326 1132,331 1068,254 C1002,175 1026,96 1130,74 Z"
        fill="#ECEBFF" opacity="0.74" filter="url(#softGlow)"/>
  <path d="M160,612 C318,560 474,610 652,588 C840,565 986,486 1138,536"
        fill="none" stroke="#D9E2EC" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 16" opacity="0.75"/>

  <text x="640" y="78" width="920" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700" fill="#20242A">
    Four Step Process Flow
  </text>
  <text x="640" y="118" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400" fill="#667085">
    A floating orb sequence for roadmaps, launch plans, and transformation journeys
  </text>

  <rect x="209" y="334" width="862" height="10" rx="5" fill="#DEE6EF"/>
  <rect x="209" y="334" width="287" height="10" rx="5" fill="#00B8A9" opacity="0.22"/>
  <rect x="496" y="334" width="287" height="10" rx="5" fill="#2196F3" opacity="0.16"/>
  <rect x="783" y="334" width="288" height="10" rx="5" fill="#9C27B0" opacity="0.13"/>

  <circle cx="260" cy="339" r="82" fill="#00ADAB" opacity="0.10"/>
  <circle cx="260" cy="339" r="66" fill="url(#orbTeal)" filter="url(#orbShadow)"/>
  <circle cx="260" cy="339" r="66" fill="url(#orbHighlight)"/>
  <rect x="214" y="219" width="92" height="30" rx="15" fill="#E6FBF8"/>
  <text x="260" y="239" width="92" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#00897B">DISCOVER</text>
  <text x="260" y="358" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="800" fill="#FFFFFF">01</text>
  <text x="260" y="468" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#2B3036">Research</text>
  <text x="260" y="502" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8491">
    <tspan x="260" dy="0">Map the customer need</tspan>
    <tspan x="260" dy="22">and define success signals.</tspan>
  </text>

  <circle cx="513" cy="339" r="82" fill="#2196F3" opacity="0.10"/>
  <circle cx="513" cy="339" r="66" fill="url(#orbBlue)" filter="url(#orbShadow)"/>
  <circle cx="513" cy="339" r="66" fill="url(#orbHighlight)"/>
  <rect x="467" y="219" width="92" height="30" rx="15" fill="#EAF5FF"/>
  <text x="513" y="239" width="92" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#1976D2">DESIGN</text>
  <text x="513" y="358" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="800" fill="#FFFFFF">02</text>
  <text x="513" y="468" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#2B3036">Prototype</text>
  <text x="513" y="502" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8491">
    <tspan x="513" dy="0">Shape the experience</tspan>
    <tspan x="513" dy="22">into a testable concept.</tspan>
  </text>

  <circle cx="766" cy="339" r="82" fill="#3F51B5" opacity="0.10"/>
  <circle cx="766" cy="339" r="66" fill="url(#orbIndigo)" filter="url(#orbShadow)"/>
  <circle cx="766" cy="339" r="66" fill="url(#orbHighlight)"/>
  <rect x="720" y="219" width="92" height="30" rx="15" fill="#EEF0FF"/>
  <text x="766" y="239" width="92" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#3F51B5">BUILD</text>
  <text x="766" y="358" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="800" fill="#FFFFFF">03</text>
  <text x="766" y="468" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#2B3036">Launch</text>
  <text x="766" y="502" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8491">
    <tspan x="766" dy="0">Coordinate execution</tspan>
    <tspan x="766" dy="22">with clear ownership.</tspan>
  </text>

  <circle cx="1020" cy="339" r="82" fill="#9C27B0" opacity="0.10"/>
  <circle cx="1020" cy="339" r="66" fill="url(#orbPurple)" filter="url(#orbShadow)"/>
  <circle cx="1020" cy="339" r="66" fill="url(#orbHighlight)"/>
  <rect x="974" y="219" width="92" height="30" rx="15" fill="#FAEAFE"/>
  <text x="1020" y="239" width="92" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#8E24AA">SCALE</text>
  <text x="1020" y="358" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="800" fill="#FFFFFF">04</text>
  <text x="1020" y="468" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#2B3036">Optimize</text>
  <text x="1020" y="502" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8491">
    <tspan x="1020" dy="0">Measure outcomes and</tspan>
    <tspan x="1020" dy="22">compound what works.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not put `filter` on the axis `<line>`; use a thin rounded `<rect>` for the connector instead.
- ❌ Do not use `marker-end` arrows for flow direction; the signature is continuity through the axis and orb spacing, not arrowheads.
- ❌ Do not clip or mask non-image elements; halos, orbs, and highlights should be direct circles.
- ❌ Do not shrink the orbs below the step text size; the giant number inside each orb is the key visual hierarchy device.
- ❌ Do not overfill the text blocks; keep each body caption to two short lines so the sequence remains clean.

## Composition notes
- Place the orb centers on a single horizontal axis around mid-slide, with the connector drawn first so it sits behind the circles.
- Keep generous top whitespace for a centered title and subtitle; the orbs should feel like the primary visual payload.
- Use equal center-to-center spacing and align every label, number, title, and body block to the orb’s x-position.
- Maintain a rhythmic color progression across steps, but keep text neutral gray so the saturated orbs carry the emphasis.