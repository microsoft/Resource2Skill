# SVG Recipe — Purpose-Driven Thematic Template Layout

## Visual mechanism
A foundational “theme” palette is fused into a purpose-built 3-column template: the header establishes context, while each column behaves like an editable KPI placeholder with a doughnut chart, metric label, category title, and guided copy area. The result feels like a reusable executive dashboard slide rather than a one-off chart.

## SVG primitives needed
- 1× `<rect>` for the full-slide themed background
- 3× `<path>` for soft organic botanical background accents
- 1× `<rect>` for the thin header divider
- 3× `<rect>` for elevated rounded column cards
- 6× `<circle>` for doughnut chart base rings and progress rings
- 3× `<circle>` for chart center fills
- 6× `<rect>` for small legend / planning indicator pills
- 3× `<path>` for small leaf icons reinforcing the eco theme
- Multiple `<text>` elements with explicit `width` for title, subtitle, KPI values, labels, and body copy
- 2× `<linearGradient>` for background and card accents
- 1× `<radialGradient>` for a soft highlight halo
- 1× `<filter id="cardShadow">` applied to card rectangles
- 1× `<filter id="softGlow">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbf8f0"/>
      <stop offset="60%" stop-color="#f9f6ee"/>
      <stop offset="100%" stop-color="#efe6d4"/>
    </linearGradient>
    <linearGradient id="oliveGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8FAF72"/>
      <stop offset="100%" stop-color="#556B2F"/>
    </linearGradient>
    <linearGradient id="seaGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B7D6B7"/>
      <stop offset="100%" stop-color="#6E9E77"/>
    </linearGradient>
    <radialGradient id="halo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#F3E8D4" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <circle cx="640" cy="90" r="220" fill="url(#halo)" opacity="0.72"/>

  <path d="M-40 115 C90 32 170 92 255 36 C350 -28 428 12 500 84 C378 126 306 188 187 164 C82 144 42 198 -40 250 Z"
        fill="#D4E4C7" opacity="0.42" filter="url(#softGlow)"/>
  <path d="M1048 24 C1150 -10 1236 32 1318 116 L1318 284 C1212 238 1128 276 1044 214 C958 151 948 72 1048 24 Z"
        fill="#D2B48C" opacity="0.28" filter="url(#softGlow)"/>
  <path d="M950 656 C1040 588 1136 614 1244 556 C1294 529 1330 558 1348 610 L1348 760 L928 760 C892 718 900 694 950 656 Z"
        fill="#9ABD9A" opacity="0.25" filter="url(#softGlow)"/>

  <text x="140" y="76" width="1000" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800"
        letter-spacing="4" fill="#556B2F">MARKETING PLAN</text>
  <text x="230" y="124" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#3E4438">
    Quarterly budget focus areas aligned to one reusable eco theme
  </text>
  <rect x="588" y="154" width="104" height="5" rx="2.5" fill="#8FBC8F"/>

  <rect x="82" y="206" width="330" height="438" rx="34" fill="#FFFFFF" opacity="0.92" filter="url(#cardShadow)"/>
  <rect x="475" y="206" width="330" height="438" rx="34" fill="#FFFFFF" opacity="0.94" filter="url(#cardShadow)"/>
  <rect x="868" y="206" width="330" height="438" rx="34" fill="#FFFFFF" opacity="0.92" filter="url(#cardShadow)"/>

  <rect x="118" y="230" width="88" height="10" rx="5" fill="#D2B48C"/>
  <rect x="511" y="230" width="88" height="10" rx="5" fill="#8FBC8F"/>
  <rect x="904" y="230" width="88" height="10" rx="5" fill="#D2B48C"/>

  <circle cx="247" cy="334" r="78" fill="none" stroke="#E8E0D1" stroke-width="24"/>
  <circle cx="247" cy="334" r="78" fill="none" stroke="url(#oliveGrad)" stroke-width="24"
          stroke-linecap="round" stroke-dasharray="122 490" transform="rotate(-90 247 334)"/>
  <circle cx="247" cy="334" r="50" fill="#FBF8F0"/>
  <text x="187" y="345" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#556B2F">25%</text>

  <circle cx="640" cy="334" r="78" fill="none" stroke="#E8E0D1" stroke-width="24"/>
  <circle cx="640" cy="334" r="78" fill="none" stroke="url(#seaGrad)" stroke-width="24"
          stroke-linecap="round" stroke-dasharray="245 490" transform="rotate(-90 640 334)"/>
  <circle cx="640" cy="334" r="50" fill="#FBF8F0"/>
  <text x="580" y="345" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#556B2F">50%</text>

  <circle cx="1033" cy="334" r="78" fill="none" stroke="#E8E0D1" stroke-width="24"/>
  <circle cx="1033" cy="334" r="78" fill="none" stroke="#D2B48C" stroke-width="24"
          stroke-linecap="round" stroke-dasharray="122 490" transform="rotate(-90 1033 334)"/>
  <circle cx="1033" cy="334" r="50" fill="#FBF8F0"/>
  <text x="973" y="345" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#556B2F">25%</text>

  <path d="M198 452 C218 422 247 422 266 452 C238 461 222 481 198 452 Z" fill="#8FBC8F"/>
  <path d="M591 452 C611 422 640 422 659 452 C631 461 615 481 591 452 Z" fill="#8FBC8F"/>
  <path d="M984 452 C1004 422 1033 422 1052 452 C1024 461 1008 481 984 452 Z" fill="#8FBC8F"/>

  <text x="122" y="496" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#556B2F">Social Media</text>
  <text x="122" y="530" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#4C4C42">
    Paid and organic reach across priority channels, with weekly engagement checkpoints.
  </text>

  <text x="515" y="496" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#556B2F">Community</text>
  <text x="515" y="530" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#4C4C42">
    Events, partnerships, and local activations that convert audience trust into demand.
  </text>

  <text x="908" y="496" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#556B2F">Incentives</text>
  <text x="908" y="530" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#4C4C42">
    Discounts, giveaways, and loyalty rewards designed to accelerate quarterly adoption.
  </text>

  <rect x="139" y="590" width="70" height="8" rx="4" fill="#556B2F"/>
  <rect x="222" y="590" width="132" height="8" rx="4" fill="#E4D5BD"/>
  <rect x="532" y="590" width="120" height="8" rx="4" fill="#8FBC8F"/>
  <rect x="666" y="590" width="82" height="8" rx="4" fill="#E4D5BD"/>
  <rect x="925" y="590" width="70" height="8" rx="4" fill="#D2B48C"/>
  <rect x="1009" y="590" width="132" height="8" rx="4" fill="#E4D5BD"/>

  <text x="96" y="676" width="1088" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" letter-spacing="1.6" fill="#7A7A68">
    THEME = COLOR + TYPOGRAPHY  •  TEMPLATE = PURPOSE-SPECIFIC STRUCTURE  •  DATA BLOCKS REMAIN FULLY EDITABLE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the doughnut charts as raster screenshots; use editable circles with `stroke-dasharray` so the chart placeholders remain native.
- ❌ Do not use `<foreignObject>` for multiline body text; use normal `<text>` elements with explicit `width`.
- ❌ Do not use `<use>` to duplicate cards or chart components; repeat the primitives directly so translation remains reliable.
- ❌ Do not apply `filter` to divider lines or arrow lines; shadows should be applied to cards or decorative paths only.
- ❌ Do not rely on clipped non-image elements for the chart rings; `clip-path` should be reserved for images only.

## Composition notes
- Keep the top 20–25% of the slide as a calm header zone; the title, subtitle, and short divider should create the “theme” identity before the template content begins.
- The three cards should occupy the lower 65–70% of the canvas with equal widths, equal spacing, and center-aligned internal content.
- Use the strongest accent color on the KPI rings and title; reserve tan and pale green for secondary rhythm so the layout feels themed but not noisy.
- Add subtle organic background paths outside the main cards to make the template feel branded and premium without reducing chart readability.