# SVG Recipe — Native Orthogonal Flowchart Layout (Draw.io Aesthetic)

## Visual mechanism
A draw.io-style flowchart is built from semantically distinct pastel nodes, dark gray borders, and strictly orthogonal 90-degree connectors. The key is precision: every node aligns to a grid, every connector travels only horizontally or vertically, and arrowheads sit only on the final connector segment.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a subtle top title accent bar
- 10–16× low-opacity `<line>` for an optional faint engineering grid
- 5× `<rect rx>` for rounded process/start/end nodes
- 2× `<path>` for diamond decision nodes
- 2× `<path>` plus 2× `<ellipse>` for editable database-cylinder nodes
- 20–30× `<line>` for orthogonal connector segments; only final segments get `marker-end`
- 1× `<marker id="arrow">` used directly on each arrow-ending `<line>`
- 1× `<filter id="nodeShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for subtle node depth
- Multiple `<text>` elements with explicit `width` attributes for node labels, connector labels, and slide title

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="10" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="#666666"/>
    </marker>

    <filter id="nodeShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="2" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="titleAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6AA84F"/>
      <stop offset="50%" stop-color="#3C78D8"/>
      <stop offset="100%" stop-color="#674EA7"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="64" y="94" width="1152" height="4" rx="2" fill="url(#titleAccent)" opacity="0.75"/>

  <!-- faint draw.io-like alignment grid; use explicit lines, not pattern fills -->
  <line x1="160" y1="120" x2="160" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="320" y1="120" x2="320" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="480" y1="120" x2="480" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="640" y1="120" x2="640" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="800" y1="120" x2="800" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="960" y1="120" x2="960" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="1120" y1="120" x2="1120" y2="660" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="80" y1="180" x2="1200" y2="180" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="80" y1="280" x2="1200" y2="280" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="80" y1="380" x2="1200" y2="380" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="80" y1="480" x2="1200" y2="480" stroke="#E9ECEF" stroke-width="1"/>
  <line x1="80" y1="580" x2="1200" y2="580" stroke="#E9ECEF" stroke-width="1"/>

  <text x="64" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#333333">
    System Authentication Flow
  </text>
  <text x="64" y="84" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">
    Native editable flowchart: pastel semantic nodes, dark strokes, orthogonal routing
  </text>

  <!-- connectors: each orthogonal route is made from editable line segments -->
  <line x1="640" y1="178" x2="640" y2="220" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="640" y1="300" x2="640" y2="340" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="580" y1="400" x2="420" y2="400" stroke="#666666" stroke-width="2"/>
  <line x1="420" y1="400" x2="420" y2="460" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="700" y1="400" x2="860" y2="400" stroke="#666666" stroke-width="2"/>
  <line x1="860" y1="400" x2="860" y2="460" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="420" y1="540" x2="420" y2="590" stroke="#666666" stroke-width="2"/>
  <line x1="420" y1="590" x2="580" y2="590" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="860" y1="540" x2="860" y2="590" stroke="#666666" stroke-width="2"/>
  <line x1="860" y1="590" x2="700" y2="590" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="640" y1="620" x2="640" y2="650" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="760" y1="260" x2="1030" y2="260" stroke="#666666" stroke-width="2"/>
  <line x1="1030" y1="260" x2="1030" y2="340" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <line x1="1030" y1="420" x2="1030" y2="590" stroke="#666666" stroke-width="2"/>
  <line x1="1030" y1="590" x2="700" y2="590" stroke="#666666" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- nodes -->
  <rect x="540" y="128" width="200" height="50" rx="22" fill="#D5E8D4" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="640" y="158" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">
    Start Request
  </text>

  <rect x="520" y="220" width="240" height="80" rx="8" fill="#DAE8FC" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="640" y="252" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">
    Validate Credentials
  </text>
  <text x="640" y="274" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">
    username + password
  </text>

  <path d="M 640 340 L 700 400 L 640 460 L 580 400 Z" fill="#FFF2CC" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="640" y="396" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#333333">
    Valid?
  </text>
  <text x="640" y="416" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">
    auth result
  </text>

  <rect x="300" y="460" width="240" height="80" rx="8" fill="#F8CECC" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="420" y="492" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">
    Reject Login
  </text>
  <text x="420" y="514" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">
    show error state
  </text>

  <rect x="740" y="460" width="240" height="80" rx="8" fill="#D5E8D4" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="860" y="492" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">
    Issue Session
  </text>
  <text x="860" y="514" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">
    token + cookie
  </text>

  <!-- database cylinder: editable path body plus ellipses -->
  <path d="M 930 350 C 930 334 1130 334 1130 350 L 1130 410 C 1130 426 930 426 930 410 Z" fill="#E1D5E7" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <ellipse cx="1030" cy="350" rx="100" ry="16" fill="#E1D5E7" stroke="#666666" stroke-width="2"/>
  <path d="M 930 410 C 930 426 1130 426 1130 410" fill="none" stroke="#666666" stroke-width="2"/>
  <text x="1030" y="381" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#333333">
    Identity Store
  </text>

  <rect x="580" y="560" width="120" height="60" rx="8" fill="#DAE8FC" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="640" y="594" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#333333">
    Audit Log
  </text>

  <rect x="540" y="650" width="200" height="46" rx="22" fill="#D5E8D4" stroke="#666666" stroke-width="2" filter="url(#nodeShadow)"/>
  <text x="640" y="679" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">
    End
  </text>

  <!-- connector labels -->
  <text x="502" y="389" width="55" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-style="italic" fill="#555555">
    No
  </text>
  <text x="778" y="389" width="55" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-style="italic" fill="#555555">
    Yes
  </text>
  <text x="900" y="248" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-style="italic" fill="#555555">
    lookup
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use one `<path>` with `marker-end` for an elbow connector; arrowheads on paths may disappear. Build elbows from separate `<line>` segments and put `marker-end` only on the final `<line>`.
- ❌ Do not use `<pattern>` for the background grid; use explicit low-opacity grid lines if a grid is needed.
- ❌ Do not apply filters to connector `<line>` elements; shadows/glows on lines are dropped.
- ❌ Do not rely on diagonal connectors; the draw.io aesthetic depends on horizontal/vertical routing.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint text boxes need explicit widths for clean rendering.

## Composition notes
- Keep nodes on a strict grid: shared center X/Y coordinates are more important than decorative detail.
- Reserve the upper 90–110 px for the title and subtitle; place the flowchart below with generous whitespace.
- Use pastel fills to encode semantics: green for start/success, blue for process, yellow for decision, red for failure, purple for data stores.
- Connectors should sit visually behind nodes, with labels close to the segment they describe but never crossing node borders.