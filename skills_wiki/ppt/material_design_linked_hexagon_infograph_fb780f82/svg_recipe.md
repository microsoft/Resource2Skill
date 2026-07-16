# SVG Recipe — Material Design Linked Hexagon Infographic

## Visual mechanism
Six custom concave “chain link” paths are rotated into a closed hexagonal loop, with white recessed circular nodes sitting at the vertices. Color-coded Material Design segments, soft shadows, connector lines, and external text cards turn the loop into a premium six-step process infographic; animate it in PowerPoint by duplicating the slide and using Morph between a scattered-link version and this assembled version.

## SVG primitives needed
- 1× `<rect>` for the light neutral background.
- 6× `<linearGradient>` for vibrant Material-style colored link fills.
- 1× `<radialGradient>` for recessed white node fills that mimic inner shadow.
- 1× `<filter id="softShadow">` applied to colored link paths, text cards, and nodes.
- 1× `<filter id="textLift">` applied to key labels for subtle outer shadow.
- 6× `<path>` for the concave dumbbell-like chain links, each rotated to form a hexagon side.
- 6× `<circle>` for white node containers at the hexagon vertices.
- 6× `<text>` for node numbers/icons.
- 6× `<line>` for thin connector rules from nodes to external copy.
- 6× `<rect rx>` for rounded Material-style label cards.
- 12× `<text>` blocks for step headers and descriptions.
- 1× optional center `<text>` label to reinforce the cyclical theme.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="46%" r="70%">
      <stop offset="0%" stop-color="#F7F8FA"/>
      <stop offset="100%" stop-color="#DCDCDC"/>
    </radialGradient>

    <linearGradient id="gRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF5252"/><stop offset="100%" stop-color="#ED1C24"/>
    </linearGradient>
    <linearGradient id="gPurple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8E5AD8"/><stop offset="100%" stop-color="#7030A0"/>
    </linearGradient>
    <linearGradient id="gBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2F80ED"/><stop offset="100%" stop-color="#0070C0"/>
    </linearGradient>
    <linearGradient id="gCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#22D3EE"/><stop offset="100%" stop-color="#00B0F0"/>
    </linearGradient>
    <linearGradient id="gYellow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD95A"/><stop offset="100%" stop-color="#FFC000"/>
    </linearGradient>
    <linearGradient id="gOrange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF9F2E"/><stop offset="100%" stop-color="#FF7C00"/>
    </linearGradient>

    <radialGradient id="nodeInset" cx="42%" cy="35%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="68%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#D5D9DE"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .24 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <filter id="textLift" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="2" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <text x="640" y="74" width="680" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="700" fill="#263238">
    Linked Hexagon Process
  </text>
  <text x="640" y="106" width="560" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6B747C">
    Six connected phases, one continuous operating rhythm
  </text>

  <!-- Concave chain-link geometry: same editable path, rotated into a hexagon -->
  <path d="M -118 0 C -118 -40 -84 -50 -58 -28 C -22 2 22 2 58 -28 C 84 -50 118 -40 118 0 C 118 40 84 50 58 28 C 22 -2 -22 -2 -58 28 C -84 50 -118 40 -118 0 Z" transform="translate(722.5 217.5) rotate(30)" fill="url(#gRed)" filter="url(#softShadow)"/>
  <path d="M -118 0 C -118 -40 -84 -50 -58 -28 C -22 2 22 2 58 -28 C 84 -50 118 -40 118 0 C 118 40 84 50 58 28 C 22 -2 -22 -2 -58 28 C -84 50 -118 40 -118 0 Z" transform="translate(805 360) rotate(90)" fill="url(#gPurple)" filter="url(#softShadow)"/>
  <path d="M -118 0 C -118 -40 -84 -50 -58 -28 C -22 2 22 2 58 -28 C 84 -50 118 -40 118 0 C 118 40 84 50 58 28 C 22 -2 -22 -2 -58 28 C -84 50 -118 40 -118 0 Z" transform="translate(722.5 502.5) rotate(150)" fill="url(#gBlue)" filter="url(#softShadow)"/>
  <path d="M -118 0 C -118 -40 -84 -50 -58 -28 C -22 2 22 2 58 -28 C 84 -50 118 -40 118 0 C 118 40 84 50 58 28 C 22 -2 -22 -2 -58 28 C -84 50 -118 40 -118 0 Z" transform="translate(557.5 502.5) rotate(210)" fill="url(#gCyan)" filter="url(#softShadow)"/>
  <path d="M -118 0 C -118 -40 -84 -50 -58 -28 C -22 2 22 2 58 -28 C 84 -50 118 -40 118 0 C 118 40 84 50 58 28 C 22 -2 -22 -2 -58 28 C -84 50 -118 40 -118 0 Z" transform="translate(475 360) rotate(270)" fill="url(#gYellow)" filter="url(#softShadow)"/>
  <path d="M -118 0 C -118 -40 -84 -50 -58 -28 C -22 2 22 2 58 -28 C 84 -50 118 -40 118 0 C 118 40 84 50 58 28 C 22 -2 -22 -2 -58 28 C -84 50 -118 40 -118 0 Z" transform="translate(557.5 217.5) rotate(330)" fill="url(#gOrange)" filter="url(#softShadow)"/>

  <circle cx="640" cy="170" r="44" fill="url(#nodeInset)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="805" cy="265" r="44" fill="url(#nodeInset)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="805" cy="455" r="44" fill="url(#nodeInset)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="640" cy="550" r="44" fill="url(#nodeInset)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="475" cy="455" r="44" fill="url(#nodeInset)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="475" cy="265" r="44" fill="url(#nodeInset)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>

  <text x="640" y="181" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#ED1C24">01</text>
  <text x="805" y="276" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#7030A0">02</text>
  <text x="805" y="466" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#0070C0">03</text>
  <text x="640" y="561" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#00B0F0">04</text>
  <text x="475" y="466" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#FFC000">05</text>
  <text x="475" y="276" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#FF7C00">06</text>

  <text x="640" y="354" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#37474F">CONTINUOUS</text>
  <text x="640" y="380" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#37474F">VALUE LOOP</text>

  <line x1="684" y1="170" x2="930" y2="170" stroke="#B0B7BE" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="849" y1="265" x2="930" y2="265" stroke="#B0B7BE" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="849" y1="455" x2="930" y2="455" stroke="#B0B7BE" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="596" y1="550" x2="350" y2="550" stroke="#B0B7BE" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="431" y1="455" x2="350" y2="455" stroke="#B0B7BE" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="431" y1="265" x2="350" y2="265" stroke="#B0B7BE" stroke-width="2" stroke-dasharray="5 7"/>

  <rect x="930" y="132" width="250" height="76" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="954" y="162" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#ED1C24" filter="url(#textLift)">STEP 01 · DISCOVER</text>
  <text x="954" y="187" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6B73">Map signals, needs, and opportunity spaces.</text>

  <rect x="930" y="227" width="250" height="76" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="954" y="257" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#7030A0" filter="url(#textLift)">STEP 02 · DEFINE</text>
  <text x="954" y="282" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6B73">Align priorities, scope, and success metrics.</text>

  <rect x="930" y="417" width="250" height="76" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="954" y="447" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#0070C0" filter="url(#textLift)">STEP 03 · DESIGN</text>
  <text x="954" y="472" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6B73">Shape the solution system and experience flow.</text>

  <rect x="100" y="512" width="250" height="76" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="124" y="542" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#00B0F0" filter="url(#textLift)">STEP 04 · BUILD</text>
  <text x="124" y="567" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6B73">Prototype, integrate, and prepare for launch.</text>

  <rect x="100" y="417" width="250" height="76" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="124" y="447" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#C99A00" filter="url(#textLift)">STEP 05 · DEPLOY</text>
  <text x="124" y="472" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6B73">Release with governance, enablement, and support.</text>

  <rect x="100" y="227" width="250" height="76" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="124" y="257" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#FF7C00" filter="url(#textLift)">STEP 06 · LEARN</text>
  <text x="124" y="282" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5F6B73">Measure outcomes and feed insight into the next cycle.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the “build” effect; create two PowerPoint slides and use Morph instead.
- ❌ Do not use `<use>` to repeat the link shape; duplicate the editable `<path>` elements manually so the translator preserves them.
- ❌ Do not apply filters to connector `<line>` elements; line filters are dropped, so keep connector rules flat and clean.
- ❌ Do not use masks to fake inner shadows on nodes; use a radial gradient plus outer shadow for reliable editable rendering.
- ❌ Do not use `marker-end` on paths for arrows; if arrows are required, use simple `<line>` connectors or draw arrowheads as small editable `<path>` triangles.

## Composition notes
- Keep the hexagon centered and slightly larger than the surrounding labels; the loop should be the visual anchor, not a small decoration.
- Use three label cards on each side so the slide remains symmetrical and executive-clean, with generous negative space around the title.
- Let each link own one vivid color, then repeat that color in the matching node number and step header for clear visual rhythm.
- For Morph animation, make a first slide where the same six link paths are scattered outward and rotated randomly, then a second slide with the assembled positions shown here.