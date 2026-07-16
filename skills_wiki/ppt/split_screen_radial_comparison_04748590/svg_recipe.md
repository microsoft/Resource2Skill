# SVG Recipe — Split-Screen Radial Comparison

## Visual mechanism
A balanced two-sided comparison is built around a central dashed divider, with each concept represented by a large inward-facing semicircle. Supporting points orbit the concept along outer semicircular bands, using numbered color nodes that align with compact explanatory text blocks on each side.

## SVG primitives needed
- 4× `<rect>` for the black stage, white content card, yellow headline banner, and subtle title separator shadow.
- 4× `<path>` for the two inner semicircle concept anchors and two thick outer semicircular arc bands.
- 6× `<circle>` for numbered indicator nodes positioned along the arcs.
- 7× `<text>` groups for the main headline, two concept labels, six node numbers, and six explanatory text blocks.
- 1× `<line>` for the central vertical dashed comparison axis.
- 3× `<linearGradient>` for the yellow banner and subtle dimensional fills on the two core semicircles.
- 1× `<filter id="softShadow">` applied to the banner/card and nodes for a premium presentation feel.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bannerYellow" x1="0" y1="22" x2="0" y2="147">
      <stop offset="0" stop-color="#ffff3a"/>
      <stop offset="1" stop-color="#f4f000"/>
    </linearGradient>

    <linearGradient id="leftCore" x1="455" y1="260" x2="620" y2="580">
      <stop offset="0" stop-color="#b8d6ef"/>
      <stop offset="1" stop-color="#8fb8dc"/>
    </linearGradient>

    <linearGradient id="rightCore" x1="660" y1="260" x2="825" y2="580">
      <stop offset="0" stop-color="#8d8d8d"/>
      <stop offset="1" stop-color="#747474"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Stage and content area -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>
  <rect x="37" y="147" width="1206" height="573" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="0" y="22" width="1280" height="125" fill="url(#bannerYellow)" filter="url(#softShadow)"/>
  <rect x="0" y="145" width="1280" height="4" fill="#d9d9d9" opacity="0.65"/>

  <!-- Main headline -->
  <text x="640" y="108" width="1120" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif" font-size="108" font-weight="700" fill="#000000">
    Comparison Slide
  </text>

  <!-- Outer radial comparison arcs -->
  <path d="M 615 205 A 215 215 0 0 0 615 635 L 615 609 A 189 189 0 0 1 615 231 Z"
        fill="#9cc7e8"/>
  <path d="M 665 205 A 215 215 0 0 1 665 635 L 665 609 A 189 189 0 0 0 665 231 Z"
        fill="#767676"/>

  <!-- Inner concept semicircles -->
  <path d="M 615 267 A 153 153 0 0 0 615 573 Z"
        fill="url(#leftCore)"/>
  <path d="M 665 267 A 153 153 0 0 1 665 573 Z"
        fill="url(#rightCore)"/>

  <!-- Central dashed divider -->
  <line x1="640" y1="172" x2="640" y2="665"
        stroke="#111111" stroke-width="4" stroke-dasharray="28 14"/>

  <!-- Concept labels -->
  <text x="548" y="388" width="130" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="36" font-weight="300" fill="#ffffff">
    <tspan x="548" dy="0">Idea 1</tspan>
    <tspan x="548" dy="42">Title</tspan>
    <tspan x="548" dy="48">Here</tspan>
  </text>

  <text x="733" y="388" width="130" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="36" font-weight="300" fill="#ffffff">
    <tspan x="733" dy="0">Idea 2</tspan>
    <tspan x="733" dy="42">Title</tspan>
    <tspan x="733" dy="48">Here</tspan>
  </text>

  <!-- Left-side numbered nodes -->
  <circle cx="479" cy="273" r="33" fill="#ed7d31" filter="url(#softShadow)"/>
  <circle cx="400" cy="420" r="33" fill="#00b050" filter="url(#softShadow)"/>
  <circle cx="479" cy="576" r="33" fill="#ffc000" filter="url(#softShadow)"/>

  <!-- Right-side numbered nodes -->
  <circle cx="801" cy="273" r="33" fill="#c00000" filter="url(#softShadow)"/>
  <circle cx="880" cy="420" r="33" fill="#7030a0" filter="url(#softShadow)"/>
  <circle cx="801" cy="576" r="33" fill="#1f4e79" filter="url(#softShadow)"/>

  <!-- Node numbers -->
  <text x="479" y="285" width="50" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="26" fill="#ffffff">1</text>
  <text x="400" y="432" width="50" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="26" fill="#ffffff">2</text>
  <text x="479" y="588" width="50" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="26" fill="#ffffff">3</text>
  <text x="801" y="285" width="50" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="26" fill="#ffffff">1</text>
  <text x="880" y="432" width="50" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="26" fill="#ffffff">2</text>
  <text x="801" y="588" width="50" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" font-size="26" fill="#ffffff">3</text>

  <!-- Left explanatory text blocks -->
  <text x="330" y="249" width="220" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" fill="#111111">
    <tspan x="330" font-size="22" font-weight="700">TITLE HERE</tspan>
    <tspan x="330" dy="22" font-size="16">Add details in 2-3 lines to</tspan>
    <tspan x="330" dy="18" font-size="16">describe the title. Lesser the</tspan>
    <tspan x="330" dy="18" font-size="16">content better it will look like.</tspan>
  </text>

  <text x="305" y="407" width="240" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" fill="#111111">
    <tspan x="305" font-size="22" font-weight="700">TITLE HERE</tspan>
    <tspan x="305" dy="22" font-size="16">Add details in 2-3 lines to</tspan>
    <tspan x="305" dy="18" font-size="16">describe the title. Lesser the</tspan>
    <tspan x="305" dy="18" font-size="16">content better it will look like.</tspan>
  </text>

  <text x="325" y="581" width="240" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" fill="#111111">
    <tspan x="325" font-size="22" font-weight="700">TITLE HERE</tspan>
    <tspan x="325" dy="22" font-size="16">Add details in 2-3 lines to</tspan>
    <tspan x="325" dy="18" font-size="16">describe the title. Lesser the</tspan>
    <tspan x="325" dy="18" font-size="16">content better it will look like.</tspan>
  </text>

  <!-- Right explanatory text blocks -->
  <text x="1055" y="249" width="240" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" fill="#111111">
    <tspan x="1055" font-size="22" font-weight="700">TITLE HERE</tspan>
    <tspan x="1055" dy="22" font-size="16">Add details in 2-3 lines to</tspan>
    <tspan x="1055" dy="18" font-size="16">describe the title. Lesser the</tspan>
    <tspan x="1055" dy="18" font-size="16">content better it will look like.</tspan>
  </text>

  <text x="1060" y="407" width="240" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" fill="#111111">
    <tspan x="1060" font-size="22" font-weight="700">TITLE HERE</tspan>
    <tspan x="1060" dy="22" font-size="16">Add details in 2-3 lines to</tspan>
    <tspan x="1060" dy="18" font-size="16">describe the title. Lesser the</tspan>
    <tspan x="1060" dy="18" font-size="16">content better it will look like.</tspan>
  </text>

  <text x="1060" y="581" width="240" text-anchor="middle"
        font-family="'Segoe UI', 'Microsoft YaHei', sans-serif" fill="#111111">
    <tspan x="1060" font-size="22" font-weight="700">TITLE HERE</tspan>
    <tspan x="1060" dy="22" font-size="16">Add details in 2-3 lines to</tspan>
    <tspan x="1060" dy="18" font-size="16">describe the title. Lesser the</tspan>
    <tspan x="1060" dy="18" font-size="16">content better it will look like.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut semicircles or donut arcs; create the half-rings directly with closed `<path>` geometry.
- ❌ Do not rely on `stroke-linecap="round"` for the outer arc endpoints if exact PPT editability matters; filled annular paths give more predictable semicircle bands.
- ❌ Do not place text along the circular arc with `<textPath>`; it will not translate reliably and also hurts readability.
- ❌ Do not use `marker-end` arrows for radial callouts; if callouts are needed, use simple `<line>` segments with manually drawn small triangle `<path>` arrowheads.
- ❌ Do not put the six feature descriptions too close to the radial graphic; the premium look depends on generous whitespace around the orbit.

## Composition notes
- Keep the radial comparison centered slightly below the title banner; the vertical divider should run through the visual’s full height and visibly separate the two concepts.
- Use strong left/right color coding: soft blue for the left concept, neutral charcoal for the right, then brighter accent colors for the individual numbered nodes.
- Text blocks should sit outside the arcs and align horizontally with their matching nodes, making the slide scannable without connector clutter.
- Reserve the top 15–20% of the slide for a high-impact title; the infographic should occupy the middle and lower portion with ample white space on both sides.