# SVG Recipe — Central Circle

## Visual mechanism
A giant centered circle becomes the slide’s visual anchor, with a short headline sitting in the middle like a keynote section title. Subtle gradients, halo rings, and sparse orbital accents make the layout feel premium while preserving the simplicity of a bold divider slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<circle>` for the soft outer halo around the central form
- 1× `<circle>` for the main central circle
- 2× `<circle>` for thin concentric accent rings
- 3× `<path>` for elegant orbital arcs and abstract contour accents
- 6× `<circle>` for small satellite dots around the main circle
- 2× `<text>` blocks for section label and headline, each with explicit `width`
- 2× `<linearGradient>` for background and ring strokes
- 1× `<radialGradient>` for the central circle fill
- 2× `<filter>` definitions for editable glow and soft shadow effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#101827"/>
      <stop offset="48%" stop-color="#17233A"/>
      <stop offset="100%" stop-color="#07111F"/>
    </linearGradient>

    <radialGradient id="circleGrad" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="42%" stop-color="#F4F8FF"/>
      <stop offset="100%" stop-color="#D8E5FF"/>
    </radialGradient>

    <linearGradient id="accentGrad" x1="360" y1="130" x2="920" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#62E6FF"/>
      <stop offset="48%" stop-color="#8D7BFF"/>
      <stop offset="100%" stop-color="#FF7AC8"/>
    </linearGradient>

    <linearGradient id="quietLine" x1="230" y1="0" x2="1050" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#62E6FF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#62E6FF" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#62E6FF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="22" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M78 166 C214 72 356 70 492 162" fill="none" stroke="url(#quietLine)" stroke-width="2" opacity="0.55"/>
  <path d="M788 585 C930 656 1106 620 1210 504" fill="none" stroke="url(#quietLine)" stroke-width="2" opacity="0.45"/>
  <path d="M190 552 C245 489 331 470 410 502 C494 536 551 518 602 455" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="7 13" opacity="0.18"/>

  <circle cx="640" cy="360" r="316" fill="#61DFFF" opacity="0.08" filter="url(#glow)"/>
  <circle cx="640" cy="360" r="286" fill="none" stroke="url(#accentGrad)" stroke-width="3" opacity="0.55"/>
  <circle cx="640" cy="360" r="255" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="3 12" opacity="0.32"/>

  <circle cx="640" cy="360" r="218" fill="url(#circleGrad)" filter="url(#softShadow)"/>
  <circle cx="556" cy="276" r="46" fill="#FFFFFF" opacity="0.34"/>
  <circle cx="724" cy="454" r="78" fill="#BFD5FF" opacity="0.16"/>

  <path d="M432 333 C475 231 577 167 692 178 C807 189 902 274 925 387" fill="none" stroke="url(#accentGrad)" stroke-width="8" stroke-linecap="round" opacity="0.88"/>
  <path d="M846 444 C793 532 690 582 585 559 C501 541 432 483 400 406" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.52"/>

  <circle cx="367" cy="203" r="7" fill="#62E6FF" opacity="0.95" filter="url(#glow)"/>
  <circle cx="901" cy="169" r="5" fill="#FF7AC8" opacity="0.9"/>
  <circle cx="1008" cy="389" r="9" fill="#8D7BFF" opacity="0.85" filter="url(#glow)"/>
  <circle cx="302" cy="476" r="5" fill="#FFFFFF" opacity="0.65"/>
  <circle cx="848" cy="611" r="6" fill="#62E6FF" opacity="0.78"/>
  <circle cx="489" cy="626" r="4" fill="#FF7AC8" opacity="0.72"/>

  <text x="440" y="305" width="400" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        font-weight="700" letter-spacing="3.5" fill="#46617F" opacity="0.86">
    SECTION 03
  </text>

  <text x="390" y="373" width="500" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46"
        font-weight="750" fill="#101827">
    <tspan x="640" dy="0">Central Circle</tspan>
    <tspan x="640" dy="54" font-size="30" font-weight="500" fill="#40526D">Bold divider moment</tspan>
  </text>

  <line x1="520" y1="463" x2="760" y2="463" stroke="url(#accentGrad)" stroke-width="3" stroke-linecap="round" opacity="0.8"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the circle as a bitmap; keep it as editable `<circle>` elements with gradients.
- ❌ Do not use `<mask>` to create halo fades; use transparent fills, radial gradients, and blur filters instead.
- ❌ Do not apply `filter` to decorative `<line>` elements; filters on lines are dropped, so use circles or paths for glow accents.
- ❌ Do not overcrowd the divider with many text blocks; the central circle works best with one concise headline.

## Composition notes
- Keep the main circle centered and dominant, roughly 55–65% of slide height, so it reads immediately as the section anchor.
- Place all primary text inside the circle; use a small uppercase label above a short headline for executive keynote pacing.
- Reserve the outer slide edges for faint arcs, dots, and glow accents only, preserving generous negative space.
- Use a dark background with a pale central circle for maximum contrast; repeat one accent gradient in rings, arcs, and the final underline.