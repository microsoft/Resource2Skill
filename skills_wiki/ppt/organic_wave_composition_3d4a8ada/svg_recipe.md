# SVG Recipe — Organic Wave Composition

## Visual mechanism
Large Bézier wave paths bleed off the slide edges and overlap in high-contrast brand colors, creating a sense of movement before any content appears. A calm central card or message zone sits on top of the waves, giving the eye a stable focal point inside the energetic organic background.

## SVG primitives needed
- 1× `<rect>` for the clean white slide base
- 3× `<linearGradient>` for premium purple, orange, and white-card depth
- 1× `<radialGradient>` for the soft lilac lower wave
- 2× `<filter>` for soft shadows and subtle glow on large organic forms
- 5× `<path>` for the main organic wave layers and small decorative blobs
- 1× `<rect>` for the central rounded content card
- 10× `<rect>` for the flat dashboard / CTA illustration inside the card
- 5× `<circle>` for decorative bubbles and chart nodes
- 3× `<line>` for the miniature connected-data graphic
- 5× `<text>` elements with explicit `width` attributes for headline, subtitle, labels, and button text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="purpleWave" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6E3BC0"/>
      <stop offset="55%" stop-color="#4C2686"/>
      <stop offset="100%" stop-color="#31145F"/>
    </linearGradient>

    <linearGradient id="orangeWave" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFB04A"/>
      <stop offset="45%" stop-color="#F47A21"/>
      <stop offset="100%" stop-color="#D95810"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F3FF"/>
    </linearGradient>

    <radialGradient id="lilacWave" cx="60%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#F4EEFF"/>
      <stop offset="65%" stop-color="#D8CBEB"/>
      <stop offset="100%" stop-color="#BCA9DE"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="waveGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- lower supporting wave -->
  <path d="M0 430
           C160 360 300 430 455 500
           C625 575 760 655 955 598
           C1115 552 1195 515 1280 562
           L1280 720 L0 720 Z"
        fill="url(#lilacWave)"/>

  <!-- dominant purple wave -->
  <path d="M0 0 L1190 0
           C1140 112 1055 205 930 268
           C760 352 650 512 438 505
           C270 500 150 405 0 442 Z"
        fill="url(#purpleWave)"/>

  <!-- orange top-right counter-wave -->
  <path d="M395 0
           C548 30 660 88 790 178
           C925 270 1058 323 1280 245
           L1280 0 Z"
        fill="url(#orangeWave)"/>

  <!-- bright swoosh that creates an overlap seam -->
  <path d="M0 316
           C170 255 330 304 472 384
           C574 442 666 456 760 406
           C675 535 520 602 340 568
           C185 540 68 454 0 486 Z"
        fill="#FFFFFF" opacity="0.18" filter="url(#waveGlow)"/>

  <!-- small organic accent blob -->
  <path d="M1015 500
           C1062 458 1135 478 1164 532
           C1198 596 1134 648 1064 628
           C1001 610 974 545 1015 500 Z"
        fill="#FFD543" opacity="0.92"/>

  <circle cx="104" cy="122" r="16" fill="#FFD543"/>
  <circle cx="1135" cy="108" r="9" fill="#FFFFFF" opacity="0.78"/>
  <circle cx="1186" cy="455" r="13" fill="#4C2686" opacity="0.18"/>

  <!-- stable focal card -->
  <rect x="342" y="202" width="596" height="322" rx="36"
        fill="url(#cardFill)" filter="url(#softShadow)"/>

  <!-- headline block -->
  <text x="392" y="294" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800" fill="#444444">
    <tspan>Call to </tspan><tspan fill="#F47A21">Action</tspan>
  </text>

  <text x="396" y="341" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="400" fill="#6A5F7D">
    Digital Action Project
  </text>

  <text x="396" y="394" width="365"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="400" fill="#777078">
    Use flowing color fields to frame a single decision, launch, or campaign message.
  </text>

  <!-- CTA button -->
  <rect x="396" y="433" width="174" height="48" rx="24" fill="#4C2686"/>
  <text x="431" y="464" width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#FFFFFF">
    Start now
  </text>

  <!-- flat data / monitor illustration -->
  <rect x="682" y="255" width="184" height="126" rx="16" fill="#E8E2F4"/>
  <rect x="700" y="273" width="148" height="84" rx="10" fill="#FFFFFF"/>
  <rect x="746" y="382" width="56" height="18" rx="5" fill="#C9B8E6"/>
  <rect x="722" y="403" width="104" height="13" rx="6" fill="#4C2686"/>

  <rect x="716" y="326" width="18" height="24" rx="4" fill="#F47A21"/>
  <rect x="748" y="304" width="18" height="46" rx="4" fill="#FFD543"/>
  <rect x="780" y="289" width="18" height="61" rx="4" fill="#4C2686"/>
  <rect x="812" y="313" width="18" height="37" rx="4" fill="#D8CBEB"/>

  <line x1="720" y1="303" x2="760" y2="292" stroke="#4C2686" stroke-width="4" stroke-linecap="round"/>
  <line x1="760" y1="292" x2="798" y2="310" stroke="#4C2686" stroke-width="4" stroke-linecap="round"/>
  <line x1="798" y1="310" x2="835" y2="282" stroke="#4C2686" stroke-width="4" stroke-linecap="round"/>

  <circle cx="720" cy="303" r="6" fill="#F47A21"/>
  <circle cx="760" cy="292" r="6" fill="#F47A21"/>
  <circle cx="798" cy="310" r="6" fill="#F47A21"/>
  <circle cx="835" cy="282" r="6" fill="#F47A21"/>

  <text x="710" y="452" width="145"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#4C2686">
    Momentum +42%
  </text>
</svg>
```

## Avoid in this skill
- ❌ Perfect sine-wave bands that look mechanically generated; use asymmetric Bézier paths with uneven peaks and valleys.
- ❌ Placing all text directly on saturated waves; reserve a calm white or pale card zone for readability.
- ❌ Using `clip-path` on the wave shapes themselves; draw the waves as closed `<path>` shapes instead.
- ❌ Overusing tiny decorative bubbles; the composition should feel organic and premium, not confetti-heavy.
- ❌ Arrowheads via `marker-end` on paths; if directional cues are needed, use simple `<line>` elements or custom arrowhead paths.

## Composition notes
- Keep the largest purple wave bleeding off the top and left edges; it should occupy roughly 45–60% of the canvas and establish the visual rhythm.
- Use orange as a counter-wave or accent, not as the dominant field; it works best in the upper-right or as a CTA color.
- Place the main text/card in the central third where the curves create visual stability.
- Leave at least one large white or pale area so the organic waves feel intentional rather than visually crowded.