# SVG Recipe — Pull-down Quote Panel

## Visual mechanism
A bold quote sits on a suspended “pull-down blind” panel: an oversized top roller bar visually anchors the composition while the soft hanging panel below creates an editorial, stage-like reveal. Shadows, rods, cords, and subtle paper folds make the quote feel physically pulled into view.

## SVG primitives needed
- 3× `<linearGradient>` for the stage background, top roller bar, and paper panel
- 2× `<radialGradient>` for ambient glow accents behind the panel
- 2× `<filter>` using blur/offset for soft panel shadow and colored glow
- 1× large `<rect>` for the full-slide background
- 2× decorative `<ellipse>` elements for background light blooms
- 1× `<rect>` for the main quote panel
- 1× `<rect>` for the top roller bar
- 1× `<rect>` for the lower pull bar
- 2× small `<rect>` elements for hanging tabs
- 4× `<path>` elements for panel folds, paper highlights, and decorative quote marks
- 3× `<line>` elements for pull cords and a subtle center seam
- 3× `<circle>` elements for cord handles and end caps
- 5× `<text>` elements for headline, quote marks, quote body, attribution, and small label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="52%" stop-color="#172554"/>
      <stop offset="100%" stop-color="#312e81"/>
    </linearGradient>

    <radialGradient id="leftGlow" cx="35%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.34"/>
      <stop offset="68%" stop-color="#38bdf8" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="rightGlow" cx="70%" cy="58%" r="48%">
      <stop offset="0%" stop-color="#f97316" stop-opacity="0.26"/>
      <stop offset="75%" stop-color="#f97316" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="rollerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#facc15"/>
      <stop offset="46%" stop-color="#fb923c"/>
      <stop offset="100%" stop-color="#f43f5e"/>
    </linearGradient>

    <linearGradient id="paperGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff7ed"/>
      <stop offset="58%" stop-color="#fffaf0"/>
      <stop offset="100%" stop-color="#fde68a"/>
    </linearGradient>

    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#78350f"/>
      <stop offset="50%" stop-color="#92400e"/>
      <stop offset="100%" stop-color="#451a03"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="370" cy="250" rx="420" ry="250" fill="url(#leftGlow)" filter="url(#softGlow)"/>
  <ellipse cx="900" cy="500" rx="430" ry="250" fill="url(#rightGlow)" filter="url(#softGlow)"/>

  <text x="640" y="74" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24"
        font-weight="700" letter-spacing="4" fill="#bae6fd">CUSTOMER VOICE</text>

  <text x="640" y="118" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44"
        font-weight="800" fill="#ffffff">What changed after the launch?</text>

  <rect x="230" y="142" width="820" height="54" rx="27" fill="#020617" opacity="0.28"/>
  <rect x="218" y="126" width="844" height="58" rx="29" fill="url(#rollerGrad)" filter="url(#panelShadow)"/>
  <circle cx="250" cy="155" r="16" fill="#fff7ed" opacity="0.55"/>
  <circle cx="1030" cy="155" r="16" fill="#fff7ed" opacity="0.55"/>

  <rect x="334" y="168" width="46" height="54" rx="10" fill="#f97316"/>
  <rect x="900" y="168" width="46" height="54" rx="10" fill="#f43f5e"/>

  <rect x="270" y="196" width="740" height="348" rx="18" fill="url(#paperGrad)" filter="url(#panelShadow)"/>
  <path d="M270 198 C390 222 505 214 640 198 C775 182 888 190 1010 198 L1010 242 C860 224 770 228 640 242 C510 256 410 252 270 242 Z"
        fill="#ffffff" opacity="0.38"/>
  <path d="M270 544 L345 544 C328 518 302 503 270 500 Z" fill="#f59e0b" opacity="0.30"/>
  <path d="M1010 544 L935 544 C952 518 978 503 1010 500 Z" fill="#f59e0b" opacity="0.30"/>

  <line x1="640" y1="210" x2="640" y2="516" stroke="#fed7aa" stroke-width="2" stroke-dasharray="8 12" opacity="0.55"/>

  <path d="M358 274 C340 274 326 290 326 312 C326 336 342 350 364 350 C384 350 398 337 398 319 C398 304 389 293 374 290 C378 276 389 263 406 252 L386 230 C369 240 358 255 358 274 Z"
        fill="#fb923c" opacity="0.34"/>
  <path d="M906 432 C924 432 938 416 938 394 C938 370 922 356 900 356 C880 356 866 369 866 387 C866 402 875 413 890 416 C886 430 875 443 858 454 L878 476 C895 466 906 451 906 432 Z"
        fill="#fb923c" opacity="0.34"/>

  <text x="640" y="310" width="610" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34"
        font-weight="700" fill="#111827">
    <tspan x="640" dy="0">“The new operating model gave</tspan>
    <tspan x="640" dy="46">our teams the confidence to move</tspan>
    <tspan x="640" dy="46">twice as fast — without losing control.”</tspan>
  </text>

  <line x1="492" y1="450" x2="788" y2="450" stroke="#fb923c" stroke-width="4" stroke-linecap="round"/>

  <text x="640" y="490" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22"
        font-weight="800" fill="#7c2d12">Maya Chen, COO</text>

  <text x="640" y="520" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        font-weight="600" letter-spacing="2" fill="#9a3412">GLOBAL RETAIL PLATFORM</text>

  <rect x="294" y="536" width="692" height="24" rx="12" fill="url(#barGrad)"/>
  <circle cx="316" cy="548" r="9" fill="#fed7aa" opacity="0.55"/>
  <circle cx="964" cy="548" r="9" fill="#fed7aa" opacity="0.55"/>

  <line x1="1052" y1="155" x2="1052" y2="410" stroke="#fde68a" stroke-width="4" stroke-linecap="round"/>
  <line x1="1074" y1="155" x2="1074" y2="360" stroke="#fde68a" stroke-width="4" stroke-linecap="round"/>
  <circle cx="1052" cy="430" r="20" fill="#facc15"/>
  <circle cx="1074" cy="379" r="14" fill="#fb923c"/>

  <text x="1084" y="468" width="130" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="700" fill="#fde68a" opacity="0.88">PULL TO REVEAL</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the hanging blind shadow or panel reveal; use gradients, opacity, and editable shapes instead.
- ❌ Do not clip decorative folds or quote marks onto the panel; clipping only reliably translates for `<image>` elements.
- ❌ Do not apply filters to pull-cord `<line>` elements; line filters are dropped, so keep cords clean and unfiltered.
- ❌ Do not use `<textPath>` for curved quote typography; use positioned `<text>` and `<tspan>` blocks for editable quote text.

## Composition notes
- Keep the roller bar wider than the quote panel by 40–80 px on each side to create the “overhanging blind” effect.
- The quote should occupy the central 55–65% of the canvas, with generous dark negative space around it for keynote-style contrast.
- Use a warm accent system for the roller, cords, and quote marks; keep the panel itself light so the quote remains highly legible.
- Place the headline above the roller, not inside the panel, so the panel reads as a distinct testimonial object rather than a generic card.