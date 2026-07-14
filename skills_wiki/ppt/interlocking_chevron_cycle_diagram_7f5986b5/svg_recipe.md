# SVG Recipe — Interlocking Chevron Cycle Diagram

## Visual mechanism
A donut cycle is built from curved custom `<path>` segments whose leading edge protrudes into a chevron point while the trailing edge contains a matching V-shaped cut. The repeated interlocks create clockwise momentum without adding separate arrow shapes.

## SVG primitives needed
- 1× `<rect>` for the soft presentation background.
- 6× `<path>` for the interlocking curved chevron donut segments.
- 1× `<circle>` for the clean central aperture / hollow donut opening.
- 6× `<linearGradient>` for premium, slightly dimensional segment fills.
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied directly to each segment path.
- 1× `<filter id="innerGlow">` using `feGaussianBlur` applied to the central circle for subtle depth.
- 8× `<text>` elements for title, subtitle, and six segment labels; every text element includes an explicit `width`.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#EAF0F6"/>
    </linearGradient>

    <linearGradient id="segBlue" x1="520" y1="150" x2="820" y2="360">
      <stop offset="0%" stop-color="#3498DB"/>
      <stop offset="100%" stop-color="#1F6FA5"/>
    </linearGradient>
    <linearGradient id="segOrange" x1="750" y1="270" x2="880" y2="520">
      <stop offset="0%" stop-color="#F39C12"/>
      <stop offset="100%" stop-color="#C65A08"/>
    </linearGradient>
    <linearGradient id="segYellow" x1="760" y1="500" x2="540" y2="630">
      <stop offset="0%" stop-color="#F7DC6F"/>
      <stop offset="100%" stop-color="#D4A800"/>
    </linearGradient>
    <linearGradient id="segGreen" x1="630" y1="620" x2="420" y2="480">
      <stop offset="0%" stop-color="#2ECC71"/>
      <stop offset="100%" stop-color="#208E4F"/>
    </linearGradient>
    <linearGradient id="segPurple" x1="430" y1="500" x2="460" y2="260">
      <stop offset="0%" stop-color="#9B59B6"/>
      <stop offset="100%" stop-color="#6C3483"/>
    </linearGradient>
    <linearGradient id="segCyan" x1="470" y1="260" x2="640" y2="150">
      <stop offset="0%" stop-color="#48C9B0"/>
      <stop offset="100%" stop-color="#168F7A"/>
    </linearGradient>

    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="innerGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="640" y="58" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#1F2D3D">
    Continuous Cycle Flow
  </text>
  <text x="640" y="92" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66788A">
    Interlocking chevrons make each stage distinct while preserving clockwise momentum
  </text>

  <!-- Center: 640,390 | outer radius: 230 | inner radius: 118 | mid radius: 174 -->
  <path d="M 642.1 272.0 L 696.7 225.5 L 644.0 160.0 A 230 230 0 0 1 837.2 272.0 L 809.6 350.9 L 741.2 329.5 A 118 118 0 0 0 642.1 272.0 Z"
        fill="url(#segBlue)" stroke="#F7FAFC" stroke-width="5" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M 743.2 332.8 L 810.8 356.8 L 841.2 278.5 A 230 230 0 0 1 841.2 501.5 L 758.7 517.3 L 743.2 447.2 A 118 118 0 0 0 743.2 332.8 Z"
        fill="url(#segOrange)" stroke="#F7FAFC" stroke-width="5" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M 741.2 450.8 L 754.2 521.3 L 837.2 508.4 A 230 230 0 0 1 644.0 620.0 L 589.1 556.4 L 642.1 508.0 A 118 118 0 0 0 741.2 450.8 Z"
        fill="url(#segYellow)" stroke="#F7FAFC" stroke-width="5" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M 637.9 508.0 L 583.3 554.5 L 636.0 620.0 A 230 230 0 0 1 442.8 508.4 L 470.4 429.1 L 538.8 450.8 A 118 118 0 0 0 637.9 508.0 Z"
        fill="url(#segGreen)" stroke="#F7FAFC" stroke-width="5" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M 536.8 447.2 L 469.2 423.2 L 438.8 501.5 A 230 230 0 0 1 438.8 278.5 L 521.3 262.7 L 536.8 332.8 A 118 118 0 0 0 536.8 447.2 Z"
        fill="url(#segPurple)" stroke="#F7FAFC" stroke-width="5" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M 538.8 329.2 L 525.8 258.7 L 442.8 271.6 A 230 230 0 0 1 636.0 160.0 L 690.9 223.6 L 637.9 272.0 A 118 118 0 0 0 538.8 329.2 Z"
        fill="url(#segCyan)" stroke="#F7FAFC" stroke-width="5" stroke-linejoin="round" filter="url(#softShadow)"/>

  <circle cx="640" cy="390" r="103" fill="#F7FAFC" stroke="#DCE5EE" stroke-width="2" filter="url(#innerGlow)"/>

  <text x="640" y="377" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2C3E50">
    ITERATE
  </text>
  <text x="640" y="404" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#78909C">
    repeat • learn • improve
  </text>

  <text x="720" y="232" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan x="720" dy="0" font-size="28" font-weight="800">1.</tspan>
    <tspan x="720" dy="25" font-size="14" font-weight="600">DISCOVER</tspan>
  </text>
  <text x="810" y="384" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan x="810" dy="0" font-size="28" font-weight="800">2.</tspan>
    <tspan x="810" dy="25" font-size="14" font-weight="600">DEFINE</tspan>
  </text>
  <text x="720" y="535" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan x="720" dy="0" font-size="28" font-weight="800">3.</tspan>
    <tspan x="720" dy="25" font-size="14" font-weight="600">BUILD</tspan>
  </text>
  <text x="560" y="535" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan x="560" dy="0" font-size="28" font-weight="800">4.</tspan>
    <tspan x="560" dy="25" font-size="14" font-weight="600">LAUNCH</tspan>
  </text>
  <text x="470" y="384" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan x="470" dy="0" font-size="28" font-weight="800">5.</tspan>
    <tspan x="470" dy="25" font-size="14" font-weight="600">MEASURE</tspan>
  </text>
  <text x="560" y="232" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#FFFFFF">
    <tspan x="560" dy="0" font-size="28" font-weight="800">6.</tspan>
    <tspan x="560" dy="25" font-size="14" font-weight="600">REFINE</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Plain pie-slice sectors with straight radial cuts; they lose the directional “interlocking” idea.
- ❌ Separate arrowheads using `marker-end` on paths; marker arrowheads may disappear, and the chevron should be part of the segment geometry.
- ❌ `<use>` or `<symbol>` to repeat segments; duplicate the editable paths directly instead.
- ❌ `textPath` labels along the ring; use normal horizontal `<text>` boxes with explicit `width`.
- ❌ Applying `clip-path` or masks to the colored segment paths; build the donut and chevrons directly as path geometry.

## Composition notes
- Keep the cycle as the hero object, roughly 500px wide and centered slightly below the title band.
- Use white or near-white strokes between segments to create the puzzle-piece separation and prevent adjacent colors from bleeding together.
- Place labels at the mid-angle of each segment, not near the chevron joints, so the text sits in the widest part of the colored mass.
- Preserve the central aperture as negative space; a small center label is acceptable, but avoid filling it with dense content.