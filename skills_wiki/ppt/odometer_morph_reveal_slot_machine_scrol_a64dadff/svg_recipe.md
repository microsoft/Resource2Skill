# SVG Recipe — Odometer Slot Machine Number Reveal

## Visual mechanism
A giant metric is built from vertical digit strips that extend above and below a narrow reveal window, then top/bottom cover panels hide the overflow so only one digit per column is visible. In PowerPoint, duplicate the slide and Morph between two Y positions of each digit strip to create the slot-machine / odometer spin.

## SVG primitives needed
- 1× `<image>` for a premium full-slide hero background, optionally clipped to the slide bounds
- 1× `<rect>` for a soft translucent bottom title band
- 1× `<rect>` for the central odometer stage/card behind the digits
- 2× `<rect>` for the top and bottom mask covers that hide the scrolling number strips
- 2× `<text>` digit-strip columns, each using stacked `<tspan>` rows
- 1× `<text>` for a smaller suffix such as `%`, `M`, `K`, or `x`
- 3× `<path>` for green upward chevrons / growth arrows
- 1× compact PowerPoint-style logo group made from `<circle>`, `<rect>`, `<path>`, and `<text>`
- 1× `<filter id="softShadow">` for card and band depth
- 1× `<filter id="numberGlow">` for cyan digit glow
- 2× `<linearGradient>` fills for sky tint and mask fade polish
- 1× `<clipPath>` applied only to the hero `<image>`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="slideClip">
      <rect x="0" y="0" width="1280" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="skyWash" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#18AEEA" stop-opacity="0.26"/>
      <stop offset="0.52" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="1" stop-color="#0B2545" stop-opacity="0.16"/>
    </linearGradient>

    <linearGradient id="topMaskFade" x1="0" y1="125" x2="0" y2="275" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#EAF7FF" stop-opacity="0.98"/>
      <stop offset="0.72" stop-color="#EAF7FF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#EAF7FF" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="bottomMaskFade" x1="0" y1="430" x2="0" y2="565" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#EAF7FF" stop-opacity="0.22"/>
      <stop offset="0.35" stop-color="#EAF7FF" stop-opacity="0.90"/>
      <stop offset="1" stop-color="#EAF7FF" stop-opacity="0.98"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="numberGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/hero-photo-snowy-mountains-blue-sky.jpg"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#slideClip)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#skyWash)"/>

  <g id="pptBadge" transform="translate(34 18)">
    <circle cx="94" cy="94" r="104" fill="#F4F6FA" opacity="0.92"/>
    <rect x="92" y="54" width="78" height="106" rx="4" fill="#FFFFFF" stroke="#CF3F28" stroke-width="5"/>
    <path d="M20 46 L102 28 L102 178 L20 160 Z" fill="#D24726"/>
    <text x="55" y="131" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="64" font-weight="800" fill="#FFFFFF">P</text>
    <path d="M118 72 A24 24 0 1 1 118 120 L118 96 L142 96 A24 24 0 0 0 118 72 Z" fill="#D24726"/>
    <line x1="118" y1="134" x2="154" y2="134" stroke="#D24726" stroke-width="7"/>
    <line x1="118" y1="152" x2="154" y2="152" stroke="#D24726" stroke-width="7"/>
  </g>

  <rect x="390" y="112" width="500" height="360" rx="30" fill="#EAF7FF" opacity="0.54" filter="url(#softShadow)"/>
  <rect x="452" y="205" width="292" height="176" rx="16" fill="#EAF7FF" opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="2"/>

  <!-- Digit strips: duplicate this slide, then move each whole digit-strip group upward for Morph. -->
  <g id="digitStripTens-start-or-end" transform="translate(0 -480)">
    <text x="452" y="332" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="188" font-weight="900" fill="#04A9EF" filter="url(#numberGlow)">
      <tspan x="452" dy="0">0</tspan>
      <tspan x="452" dy="160">1</tspan>
      <tspan x="452" dy="160">2</tspan>
      <tspan x="452" dy="160">3</tspan>
      <tspan x="452" dy="160">4</tspan>
      <tspan x="452" dy="160">5</tspan>
    </text>
  </g>

  <g id="digitStripOnes-start-or-end" transform="translate(0 -480)">
    <text x="615" y="332" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="188" font-weight="900" fill="#04A9EF" filter="url(#numberGlow)">
      <tspan x="615" dy="0">8</tspan>
      <tspan x="615" dy="160">9</tspan>
      <tspan x="615" dy="160">0</tspan>
      <tspan x="615" dy="160">1</tspan>
      <tspan x="615" dy="160">2</tspan>
      <tspan x="615" dy="160">3</tspan>
    </text>
  </g>

  <!-- Mask covers sit above the moving strips, leaving only the center slot visible. -->
  <rect x="372" y="104" width="532" height="168" rx="30" fill="url(#topMaskFade)"/>
  <rect x="372" y="365" width="532" height="125" rx="30" fill="url(#bottomMaskFade)"/>

  <text x="750" y="356" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" fill="#04A9EF" opacity="0.95">%</text>

  <g id="growthChevrons" transform="translate(824 185)">
    <path d="M0 50 L48 2 L96 50" fill="none" stroke="#35D047" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M0 108 L48 60 L96 108" fill="none" stroke="#35D047" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M0 166 L48 118 L96 166" fill="none" stroke="#35D047" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <rect x="0" y="484" width="1280" height="192" fill="#FFFFFF" opacity="0.86" filter="url(#softShadow)"/>
  <text x="204" y="576" width="880" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" letter-spacing="1" fill="#111722">SCROLLING NUMBERS</text>
  <text x="180" y="634" width="920" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="400" fill="#111722">Animation tutorial — all PowerPoint versions</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the scrolling; PPT-Master will not translate it. Use two slides plus PowerPoint Morph instead.
- ❌ `clip-path` on `<text>` or `<g>` to crop the digits; translator only preserves clip paths on `<image>`. Use foreground mask rectangles over the digit strips.
- ❌ `<mask>` for the reveal window or gradient fade; masks can hard-fail. Use stacked rectangles with matching background fills and gradients.
- ❌ `marker-end` arrowheads for the green growth indicators; draw chevrons as simple stroked `<path>` elements.
- ❌ Letting digit-strip text auto-size. Every `<text>` needs an explicit `width`, and the strip rows should use fixed `dy` spacing so the Morph landing positions are predictable.

## Composition notes
- Keep the odometer window in the upper-middle third; the digit size should feel oversized, with only one row fully visible at a time.
- The masks must sit above the moving number strips in z-order. For a cleaner premium look, use slightly translucent gradient covers that visually fade the entering/exiting digits.
- For Morph: on slide 1, place the strip groups with `transform="translate(0 0)"`; on slide 2, move each strip upward by `digitIndex × rowHeight` so the target digit lands in the window.
- Anchor the message with a calm bottom band or caption area; the moving digits are the hero, so keep surrounding labels minimal and high contrast.