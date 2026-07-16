# SVG Recipe — Pillar Layout with Overlapping Badge Headers

## Visual mechanism
A row of equal-width pillar cards is distributed horizontally, with each card’s header represented by a large circular badge that overlaps the card’s top edge. The thick colored badge stroke and matching pastel card fill create clear conceptual separation while preserving a unified framework structure.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× `<rect>` for the rounded pillar body containers
- 3× `<circle>` for soft badge glow/halo layers behind the header badges
- 3× `<circle>` for the white badge headers with thick colored outlines
- 2× `<path>` for subtle decorative background ribbons/blobs
- 1× `<rect>` for a small title eyebrow label
- 1× `<filter id="cardShadow">` applied to body cards and badge circles for executive-slide depth
- 1× `<filter id="softGlow">` applied to badge halo circles
- 4× `<linearGradient>` for the background and pastel pillar fills
- Multiple `<text>` elements with explicit `width` for title, subtitle, badge letters, pillar headings, and body copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>

    <linearGradient id="greenCard" x1="0" y1="250" x2="0" y2="620">
      <stop offset="0%" stop-color="#F0F8EA"/>
      <stop offset="100%" stop-color="#DDEFD4"/>
    </linearGradient>
    <linearGradient id="blueCard" x1="0" y1="250" x2="0" y2="620">
      <stop offset="0%" stop-color="#EEF6FD"/>
      <stop offset="100%" stop-color="#DCEBF7"/>
    </linearGradient>
    <linearGradient id="orangeCard" x1="0" y1="250" x2="0" y2="620">
      <stop offset="0%" stop-color="#FFF3EC"/>
      <stop offset="100%" stop-color="#FCE3D5"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40,140 C180,65 300,110 440,54 C610,-12 770,34 900,10 C1070,-22 1190,6 1320,-36 L1320,110 C1120,150 980,96 820,132 C665,166 540,128 370,178 C210,226 92,202 -40,246 Z"
        fill="#EAF2FF" opacity="0.65"/>
  <path d="M1015,612 C1086,548 1165,535 1295,566 L1295,735 L805,735 C855,676 929,690 1015,612 Z"
        fill="#FCE9DC" opacity="0.72"/>

  <rect x="523" y="54" width="234" height="32" rx="16" fill="#E2E8F0"/>
  <text x="640" y="76" width="234" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        letter-spacing="1.8" fill="#475569">STRATEGY FRAMEWORK</text>

  <text x="640" y="128" width="960" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800"
        fill="#1E293B">Pillar Layout with Badge Headers</text>
  <text x="640" y="164" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#64748B">Use overlapping circular nodes to make each business pillar instantly scannable and visually equal.</text>

  <!-- Pillar 1 -->
  <rect x="150" y="250" width="300" height="360" rx="26" fill="url(#greenCard)"
        filter="url(#cardShadow)"/>
  <circle cx="300" cy="250" r="78" fill="#92D050" opacity="0.18" filter="url(#softGlow)"/>
  <circle cx="300" cy="250" r="66" fill="#FFFFFF" stroke="#92D050" stroke-width="12"
          filter="url(#cardShadow)"/>
  <text x="300" y="273" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="70" font-weight="800"
        fill="#65A832">S</text>

  <text x="300" y="352" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800"
        fill="#263A1F">Segment</text>
  <text x="190" y="398" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17"
        fill="#334155">
    <tspan x="190" dy="0">Identify addressable customer</tspan>
    <tspan x="190" dy="27">groups using behavioral,</tspan>
    <tspan x="190" dy="27">demographic, and value-based</tspan>
    <tspan x="190" dy="27">signals.</tspan>
  </text>
  <text x="190" y="525" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        fill="#5B8F2C">
    <tspan x="190" dy="0">Output:</tspan>
    <tspan fill="#334155"> clear opportunity map</tspan>
  </text>

  <!-- Pillar 2 -->
  <rect x="490" y="250" width="300" height="360" rx="26" fill="url(#blueCard)"
        filter="url(#cardShadow)"/>
  <circle cx="640" cy="250" r="78" fill="#9BC2E6" opacity="0.20" filter="url(#softGlow)"/>
  <circle cx="640" cy="250" r="66" fill="#FFFFFF" stroke="#9BC2E6" stroke-width="12"
          filter="url(#cardShadow)"/>
  <text x="640" y="273" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="70" font-weight="800"
        fill="#4B83B7">T</text>

  <text x="640" y="352" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800"
        fill="#20384F">Target</text>
  <text x="530" y="398" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17"
        fill="#334155">
    <tspan x="530" dy="0">Prioritize the segments with</tspan>
    <tspan x="530" dy="27">strongest fit, attractive margins,</tspan>
    <tspan x="530" dy="27">and the highest probability of</tspan>
    <tspan x="530" dy="27">conversion.</tspan>
  </text>
  <text x="530" y="525" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        fill="#477FAC">
    <tspan x="530" dy="0">Output:</tspan>
    <tspan fill="#334155"> ranked focus accounts</tspan>
  </text>

  <!-- Pillar 3 -->
  <rect x="830" y="250" width="300" height="360" rx="26" fill="url(#orangeCard)"
        filter="url(#cardShadow)"/>
  <circle cx="980" cy="250" r="78" fill="#F4B183" opacity="0.22" filter="url(#softGlow)"/>
  <circle cx="980" cy="250" r="66" fill="#FFFFFF" stroke="#F4B183" stroke-width="12"
          filter="url(#cardShadow)"/>
  <text x="980" y="273" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="70" font-weight="800"
        fill="#D9783E">P</text>

  <text x="980" y="352" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800"
        fill="#51301E">Position</text>
  <text x="870" y="398" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17"
        fill="#334155">
    <tspan x="870" dy="0">Craft the differentiated promise</tspan>
    <tspan x="870" dy="27">and proof points that make the</tspan>
    <tspan x="870" dy="27">offer memorable against</tspan>
    <tspan x="870" dy="27">competitors.</tspan>
  </text>
  <text x="870" y="525" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        fill="#C36D3B">
    <tspan x="870" dy="0">Output:</tspan>
    <tspan fill="#334155"> distinct value narrative</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use masks or clipped shapes to fake the badge overlap; simply layer the circle above the card so it remains editable.
- ❌ Do not use `<use>` or `<symbol>` to repeat pillars; duplicate the SVG elements directly so PowerPoint receives independent editable shapes.
- ❌ Do not place body copy in a single auto-wrapping SVG text block without `width`; use explicit `width` and line-broken `<tspan>` rows for predictable PPT rendering.
- ❌ Do not add arrowheads with `marker-end` between pillars; if sequence cues are needed, use simple editable `<line>` elements or small triangular `<path>` shapes.

## Composition notes
- Keep the badge center exactly aligned to the top edge of the card body; this is the signature overlap that creates the “header node” effect.
- Use equal card widths and mathematically even horizontal spacing to communicate parity across pillars.
- Reserve the top 20–25% of the slide for title and context; the framework should dominate the middle and lower canvas.
- Match each badge stroke, badge letter, and small emphasis text to the same hue, while using a much lighter tint for the corresponding card fill.