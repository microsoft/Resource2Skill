# SVG Recipe — Segmented Radial Infographic (Precision Donut Slicing)

## Visual mechanism
A thick donut ring is broken into mathematically even radial segments by using dash-length-controlled circular strokes, creating crisp negative-space cuts between modules. The result feels engineered and modular, ideal for cycles, capability systems, maturity models, or “N-part architecture” visuals.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark executive background
- 2× `<path>` for large blurred ambient color glows behind the infographic
- 18× `<circle>` total: 1 dashed shadow ring, 14 individually colored single-dash arc segments, 1 central hub disk, and 2 thin guide/detail rings
- 1× `<line>` for the left-side editorial accent rule
- 7× `<text>` for title, subtitle, center label, and perimeter labels
- 1× `<linearGradient>` for the background
- 1× `<radialGradient>` for the central glassy hub
- 2× `<filter>`: one soft glow for ambient shapes, one offset blur shadow for the segmented ring

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0F131A"/>
      <stop offset="58%" stop-color="#141922"/>
      <stop offset="100%" stop-color="#090C11"/>
    </linearGradient>

    <radialGradient id="hubGrad" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#313B4A"/>
      <stop offset="55%" stop-color="#151B24"/>
      <stop offset="100%" stop-color="#080B10"/>
    </radialGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="32"/>
    </filter>

    <filter id="ringShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- Ambient executive-keynote lighting -->
  <path d="M772 78 C922 18 1106 52 1190 158 C1258 244 1188 334 1042 315 C894 296 738 190 772 78 Z"
        fill="#00BFFF" opacity="0.13" filter="url(#softGlow)"/>
  <path d="M884 642 C1018 560 1190 566 1276 660 C1322 710 1202 758 1048 740 C928 726 820 696 884 642 Z"
        fill="#FF8C00" opacity="0.14" filter="url(#softGlow)"/>

  <!-- Left editorial panel -->
  <line x1="86" y1="148" x2="86" y2="538" stroke="#00BFFF" stroke-width="4"/>
  <text x="118" y="170" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="3" fill="#7ADFFF">PRECISION DONUT SLICING</text>
  <text x="116" y="250" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="800" fill="#FFFFFF">
    <tspan x="116" dy="0">Core</tspan>
    <tspan x="116" dy="58">Architecture</tspan>
  </text>
  <text x="118" y="400" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#AEB7C6">
    A precisely engineered 14-part cycle with equal radial cuts, clean negative space, and premium modular color rhythm.
  </text>

  <!-- Precision segmented ring: r=205, circumference≈1288; 14 pitch≈92.0; dash≈79.5; gap≈12.5 -->
  <circle cx="865" cy="360" r="205" fill="none" stroke="#000000" stroke-opacity="0.58"
          stroke-width="76" stroke-linecap="butt" stroke-dasharray="79.5 12.5"
          transform="rotate(-88.25 865 360)" filter="url(#ringShadow)"/>

  <!-- Fourteen editable arc segments, each as a one-dash circle rotated into place -->
  <circle cx="865" cy="360" r="205" fill="none" stroke="#00BFFF" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(-88.25 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#24D8FF" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(-62.54 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#00FA9A" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(-36.82 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#68FFB5" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(-11.11 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#FF8C00" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(14.61 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#FFB000" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(40.32 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#9370DB" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(66.04 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#D748FF" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(91.75 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#00BFFF" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(117.46 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#00FA9A" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(143.18 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#FF8C00" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(168.89 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#FF5C35" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(194.61 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#9370DB" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(220.32 865 360)"/>
  <circle cx="865" cy="360" r="205" fill="none" stroke="#4B6CFF" stroke-width="76" stroke-linecap="butt"
          stroke-dasharray="79.5 2000" transform="rotate(246.04 865 360)"/>

  <!-- Detail rings and central hub -->
  <circle cx="865" cy="360" r="252" fill="none" stroke="#8FFFF0" stroke-width="1.5" stroke-opacity="0.28"
          stroke-dasharray="2 13"/>
  <circle cx="865" cy="360" r="121" fill="url(#hubGrad)" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="2"/>
  <circle cx="865" cy="360" r="151" fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>

  <text x="765" y="345" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2" fill="#81E8FF">OPERATING MODEL</text>
  <text x="765" y="385" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#FFFFFF">14</text>
  <text x="765" y="414" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#AEB7C6">EQUAL MODULES</text>

  <!-- Sparse perimeter annotations -->
  <text x="785" y="74" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#CFEFFF">01 DISCOVER</text>
  <text x="1100" y="347" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#FFE0A6">04 BUILD</text>
  <text x="790" y="663" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#E8D7FF">08 SCALE</text>
  <text x="586" y="347" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#C9FFE3">12 GOVERN</text>
</svg>
```

## Avoid in this skill
- ❌ Do not fake the cuts by drawing thick background-colored radial lines over a continuous donut; it fails on gradients/photos and loses the “true negative space” precision.
- ❌ Do not use `<mask>` or clip-paths on non-image shapes to subtract gaps; those will not translate reliably into editable PowerPoint shapes.
- ❌ Do not use `<use>` to clone the 14 segments; duplicate the editable `<circle>` or `<path>` elements explicitly.
- ❌ Do not rely on pie-chart wedges unless the design needs variable data values; this technique is about equal modular slicing with controlled gaps.

## Composition notes
- Put the radial graphic on the visual-dominant side, occupying roughly 60–70% of slide height; leave the donut center open for a concise metric or concept label.
- Use one exact radius and one exact dash formula: `dash length = circumference × (360/N − gapDegrees) / 360`.
- Keep labels sparse; too many perimeter labels will weaken the engineered symmetry.
- Use a dark background, blurred ambient glows, and a limited high-energy palette to make the negative cuts feel premium rather than like a default chart.