# SVG Recipe — Morphing Odometer Reveal

## Visual mechanism
A giant KPI number is built from static digits plus one or more vertical digit stacks that slide upward between two Morph-matched slides, creating an odometer roll. The stack is not truly clipped in SVG; instead, background-colored “letterbox” rectangles cover the overflow above and below the visible digit window.

## SVG primitives needed
- 1× `<rect>` for the solid blue presentation background
- 2× `<circle>` for large warm accent halos behind the PowerPoint badge / presenter area
- 2× `<path>` for soft editorial swooshes and depth accents
- 1× `<image>` for a right-side presenter / torso pointing toward the number, clipped to a rectangular crop
- 1× `<clipPath>` with `<rect rx>` applied only to the presenter image
- 3× `<rect>` for the tilted PowerPoint-style badge and its shadow face
- 5× `<text>` for headline, static year digits, rolling digit stack, bottom label, and badge letter
- 2× `<rect>` for odometer overflow masks that exactly match the background color
- 2× `<line>` for subtle window-edge guide highlights
- 2× `<filter>`: one pink text glow, one soft badge/image shadow
- 3× gradients for blue background depth, pink headline fill, and red/orange badge fill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0759bd"/>
      <stop offset="58%" stop-color="#034da6"/>
      <stop offset="100%" stop-color="#073f8e"/>
    </linearGradient>

    <linearGradient id="pinkTitle" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff9ea3"/>
      <stop offset="58%" stop-color="#ff7f91"/>
      <stop offset="100%" stop-color="#ff657d"/>
    </linearGradient>

    <linearGradient id="pptRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f26338"/>
      <stop offset="100%" stop-color="#c93214"/>
    </linearGradient>

    <filter id="pinkGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="10" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="presenterCrop">
      <rect x="805" y="42" width="450" height="678" rx="0"/>
    </clipPath>
  </defs>

  <!-- Base stage -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <!-- Editorial depth accents -->
  <circle cx="956" cy="112" r="160" fill="#ff795c" opacity="0.92"/>
  <circle cx="1008" cy="660" r="250" fill="#062f72" opacity="0.25"/>
  <path d="M-40,690 C185,610 320,650 500,592 C685,530 795,565 930,505"
        fill="none" stroke="#0d6fd8" stroke-width="54" opacity="0.22"/>
  <path d="M750,0 C710,96 720,170 790,230 C858,288 952,292 1055,252 L1055,0 Z"
        fill="#ff8d6a" opacity="0.18"/>

  <!-- Tilted PowerPoint badge -->
  <rect x="808" y="10" width="164" height="154" rx="20"
        fill="#9c2d18" opacity="0.45" transform="rotate(20 890 87)"/>
  <rect x="782" y="-4" width="164" height="154" rx="20"
        fill="url(#pptRed)" filter="url(#softShadow)" transform="rotate(20 864 73)"/>
  <text x="820" y="112" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92" font-weight="700" fill="#ffffff"
        transform="rotate(20 864 73)">P</text>

  <!-- Presenter / body image, face intentionally avoided or cropped out -->
  <image x="805" y="42" width="450" height="678"
         href="https://images.example.com/presenter-torso-pointing-at-kpi-no-face.png"
         clip-path="url(#presenterCrop)" opacity="0.96"/>

  <!-- Top headline -->
  <text x="70" y="165" width="735"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="126" font-weight="900" letter-spacing="5"
        fill="url(#pinkTitle)" filter="url(#pinkGlow)">ANIMATED</text>

  <!-- Static part of the KPI -->
  <text x="60" y="470" width="590"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="305" font-weight="900"
        fill="#ffffff">202</text>

  <!-- Rolling units column.
       For slide 1, place this stack lower so "3" sits in the window.
       For slide 2, move the same element upward by one line height so "4" sits in the window. -->
  <text id="YearUnitsRoll" x="625" y="-153" width="210"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="186" font-weight="900"
        fill="#ffffff" text-anchor="middle">
    <tspan x="720" dy="0">0</tspan>
    <tspan x="720" dy="160">1</tspan>
    <tspan x="720" dy="160">2</tspan>
    <tspan x="720" dy="160">3</tspan>
    <tspan x="720" dy="160">4</tspan>
    <tspan x="720" dy="160">5</tspan>
    <tspan x="720" dy="160">6</tspan>
    <tspan x="720" dy="160">7</tspan>
    <tspan x="720" dy="160">8</tspan>
    <tspan x="720" dy="160">9</tspan>
  </text>

  <!-- Odometer masks: these are ordinary background-colored rectangles placed over the rolling stack. -->
  <rect x="600" y="0" width="238" height="202" fill="#0759bd"/>
  <rect x="600" y="535" width="238" height="185" fill="#0759bd"/>

  <!-- Subtle visible edge cues for the viewing slot -->
  <line x1="626" y1="205" x2="810" y2="205" stroke="#ffffff" stroke-width="2" opacity="0.18"/>
  <line x1="626" y1="532" x2="810" y2="532" stroke="#ffffff" stroke-width="2" opacity="0.15"/>

  <!-- Bottom label restored above the lower mask -->
  <text x="78" y="650" width="710"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="134" font-weight="900" letter-spacing="5"
        fill="url(#pinkTitle)" filter="url(#pinkGlow)">NUMBERS</text>

  <!-- Small kinetic accent near the pointing gesture -->
  <path d="M742,316 C766,304 788,300 812,303"
        fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.75"/>
  <path d="M796,288 L828,303 L796,322"
        fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0.75"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the rolling motion should come from PowerPoint Morph between two slides.
- ❌ Do not rely on `clip-path` for the digit text stack; clip paths on non-image elements may be ignored. Use background-colored overlay rectangles as the odometer masks.
- ❌ Do not use a gradient or photo directly behind the digit window unless the masking rectangles exactly match that area; otherwise the “hidden” digits will show through visually.
- ❌ Do not make each digit a separate unrelated shape if you want Morph to feel continuous; keep each rolling column as one stable text element between slides.
- ❌ Do not use `marker-end` arrows for the pointing accent; use simple editable `<path>` strokes or `<line>` arrows instead.

## Composition notes
- Keep the metric on the left two-thirds of the canvas; reserve the right third for a presenter crop, product image, or supporting visual that points attention back to the KPI.
- Use one solid background color behind the odometer window so the top and bottom masks can perfectly hide the rolling stack.
- For Morph setup, duplicate the slide: on slide 1 position the stack so the starting digit is centered; on slide 2 move the same stack upward by exactly one digit line height per increment.
- Overscale the typography dramatically: headline and label provide energy, but the white KPI digits should remain the brightest, largest focal point.