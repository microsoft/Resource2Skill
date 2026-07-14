# SVG Recipe — Vibrant Geometric Color-Block Overlay

## Visual mechanism
Oversized intersecting color polygons slice the canvas into asymmetric zones, replacing a static grid with energetic diagonal motion. A crisp white title ribbon sits above the geometry, while body content is anchored inside the dominant bright color block for strong hierarchy.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark slate base
- 3× `<path>` for the oversized mustard block, teal triangle, and optional coral accent wedge
- 1× `<rect>` for the white title ribbon
- 1× `<path>` for the folded ribbon shadow tab
- 4× `<path>` for thin diagonal highlight slashes that echo the main geometry
- 6× `<text>` elements for editable title, section labels, paragraph copy, and small kicker text
- 1× `<filter id="softShadow">` applied to the white title ribbon and fold for light depth
- 1× `<linearGradient>` for a subtle premium variation on the mustard block while preserving the flat color-block feel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mustardGrad" x1="420" y1="40" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFC73A"/>
      <stop offset="0.58" stop-color="#F9BC24"/>
      <stop offset="1" stop-color="#E9A91A"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Base field -->
  <rect x="0" y="0" width="1280" height="720" fill="#4C5C68"/>

  <!-- Dominant right-side skewed block -->
  <path d="M448 0 H1280 V720 H252 Z" fill="url(#mustardGrad)"/>

  <!-- Large downward triangle bridging dark and yellow areas -->
  <path d="M318 0 H878 L606 642 Z" fill="#21B2A6"/>

  <!-- Small warm accent wedge for extra color rhythm -->
  <path d="M1065 0 H1280 V155 L1165 108 Z" fill="#FF6B4A" opacity="0.95"/>

  <!-- Decorative diagonal slashes, kept as editable paths -->
  <path d="M92 560 L154 560 L102 720 L40 720 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M167 520 L213 520 L148 720 L102 720 Z" fill="#FFFFFF" opacity="0.13"/>
  <path d="M1130 405 L1174 405 L1070 720 L1026 720 Z" fill="#FFFFFF" opacity="0.16"/>
  <path d="M1195 360 L1230 360 L1110 720 L1076 720 Z" fill="#FFFFFF" opacity="0.18"/>

  <!-- Folded shadow under the title ribbon -->
  <path d="M46 222 L122 222 L88 282 L12 282 Z" fill="#303A43" opacity="0.95" filter="url(#softShadow)"/>

  <!-- Main white ribbon -->
  <rect x="0" y="112" width="482" height="118" fill="#FFFFFF" stroke="#21B2A6" stroke-width="5" filter="url(#softShadow)"/>

  <!-- Ribbon title -->
  <text x="44" y="184" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#4C5C68" letter-spacing="-0.5">
    Company Values
  </text>

  <!-- Small dark-zone kicker -->
  <text x="54" y="348" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#D7E1E7" letter-spacing="2.2">
    CULTURE PRINCIPLES
  </text>

  <text x="54" y="386" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="600" fill="#FFFFFF">
    Designed to scale with clarity, energy, and trust.
  </text>

  <!-- Body copy on yellow block -->
  <text x="690" y="178" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#2F3A42">
    Respect
  </text>

  <text x="690" y="224" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#2F3A42">
    <tspan x="690" dy="0">We recognise that every supplier,</tspan>
    <tspan x="690" dy="32">customer, and teammate relationship</tspan>
    <tspan x="690" dy="32">is unique — and a privilege to uphold.</tspan>
  </text>

  <text x="690" y="374" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#2F3A42">
    Service
  </text>

  <text x="690" y="420" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#2F3A42">
    <tspan x="690" dy="0">A cornerstone of our business:</tspan>
    <tspan x="690" dy="32">we improve the experience every day</tspan>
    <tspan x="690" dy="32">through ownership and follow-through.</tspan>
  </text>

  <!-- Tiny footer label -->
  <text x="690" y="640" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#70510B" opacity="0.72" letter-spacing="1.4">
    MODERN OPERATING VALUES / 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using only rectangular blocks; the technique depends on oversized diagonal polygons and asymmetry
- ❌ Putting text across the diagonal intersection where contrast changes unpredictably
- ❌ Applying `clip-path` to the color shapes; use direct `<path>` geometry instead for reliable editability
- ❌ Overusing gradients or shadows; this style should remain primarily flat, crisp, and graphic
- ❌ Using `skewX`, `skewY`, or matrix transforms to fake the angled blocks; draw the angles directly with path coordinates

## Composition notes
- Keep the dark slate zone on the left at roughly 25–35% of the slide and let the mustard block dominate the right side.
- Place the title ribbon partly over the dark field and partly near the teal triangle so it feels locked into the geometry.
- Body text works best inside the yellow block, aligned vertically with generous line spacing and strong dark typography.
- Use one secondary accent color sparingly; the main rhythm should be dark slate, mustard, teal, and white.