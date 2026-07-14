# SVG Recipe — Circular Triforce Infographic with Radial Shadow Nodes

## Visual mechanism
A three-step process is arranged as an equilateral triangular loop: three elevated white circular cards sit on a colored circular flow ring, with each 120° arc and accent dot matching its corresponding node. The premium effect comes from large negative space, soft radial shadows, crisp white nodes, and concise outward-facing annotations.

## SVG primitives needed
- 1× `<rect>` for the light-gray slide background
- 3× `<path>` for the colored 120° circular arc segments
- 3× `<circle>` for small colored midpoint dots on the ring
- 3× `<circle>` for large white floating node cards
- 1× `<circle>` for a subtle translucent center hub
- 1× `<text>` for the center concept label
- 3× `<text>` for large node numbers
- 3× `<text>` for node labels
- 3× `<text>` for outward explanatory copy blocks
- 1× `<filter id="nodeShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft elevation on nodes
- 1× `<filter id="dotShadow">` for small raised accent dots
- 1× `<filter id="softGlow">` for a faint colored glow behind the circular flow
- 1× `<radialGradient>` for the center hub fill
- 1× `<linearGradient>` for the background’s subtle premium lighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAFBFC"/>
      <stop offset="55%" stop-color="#F4F5F7"/>
      <stop offset="100%" stop-color="#ECEFF3"/>
    </linearGradient>

    <radialGradient id="hubFill" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.25"/>
    </radialGradient>

    <filter id="nodeShadow" x="-40%" y="-35%" width="180%" height="190%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feFlood flood-color="#273142" flood-opacity="0.18" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="dotShadow" x="-80%" y="-80%" width="260%" height="260%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feFlood flood-color="#1C2430" flood-opacity="0.22" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <circle cx="640" cy="360" r="116" fill="url(#hubFill)" stroke="#FFFFFF" stroke-width="2" opacity="0.9"/>

  <path d="M 640 175 A 185 185 0 0 1 800.2 452.5"
        fill="none" stroke="#28A745" stroke-width="18" stroke-linecap="round"
        opacity="0.22" filter="url(#softGlow)"/>
  <path d="M 800.2 452.5 A 185 185 0 0 1 479.8 452.5"
        fill="none" stroke="#FD7E14" stroke-width="18" stroke-linecap="round"
        opacity="0.22" filter="url(#softGlow)"/>
  <path d="M 479.8 452.5 A 185 185 0 0 1 640 175"
        fill="none" stroke="#007BFF" stroke-width="18" stroke-linecap="round"
        opacity="0.22" filter="url(#softGlow)"/>

  <path d="M 640 175 A 185 185 0 0 1 800.2 452.5"
        fill="none" stroke="#28A745" stroke-width="12" stroke-linecap="round"/>
  <path d="M 800.2 452.5 A 185 185 0 0 1 479.8 452.5"
        fill="none" stroke="#FD7E14" stroke-width="12" stroke-linecap="round"/>
  <path d="M 479.8 452.5 A 185 185 0 0 1 640 175"
        fill="none" stroke="#007BFF" stroke-width="12" stroke-linecap="round"/>

  <circle cx="800.2" cy="267.5" r="16" fill="#28A745" stroke="#FFFFFF" stroke-width="6" filter="url(#dotShadow)"/>
  <circle cx="640" cy="545" r="16" fill="#FD7E14" stroke="#FFFFFF" stroke-width="6" filter="url(#dotShadow)"/>
  <circle cx="479.8" cy="267.5" r="16" fill="#007BFF" stroke="#FFFFFF" stroke-width="6" filter="url(#dotShadow)"/>

  <circle cx="640" cy="175" r="78" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="800.2" cy="452.5" r="78" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="479.8" cy="452.5" r="78" fill="#FFFFFF" filter="url(#nodeShadow)"/>

  <text x="640" y="345" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#333B45">
    STRATEGIC
  </text>
  <text x="640" y="374" width="230" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#1E2630">
    FLYWHEEL
  </text>
  <text x="640" y="402" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7B8490">
    three equal pillars in motion
  </text>

  <text x="640" y="164" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#28A745">01</text>
  <text x="640" y="198" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#646464">DISCOVER</text>

  <text x="800.2" y="441.5" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FD7E14">02</text>
  <text x="800.2" y="475.5" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#646464">ACTIVATE</text>

  <text x="479.8" y="441.5" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#007BFF">03</text>
  <text x="479.8" y="475.5" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#646464">SCALE</text>

  <text x="640" y="72" width="410" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6C7682">
    <tspan x="640" dy="0">Map customer signals, market whitespace, and</tspan>
    <tspan x="640" dy="23">operational constraints into one shared view.</tspan>
  </text>

  <text x="925" y="448" width="250" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6C7682">
    <tspan x="925" dy="0">Launch focused plays with</tspan>
    <tspan x="925" dy="23">owners, milestones, and</tspan>
    <tspan x="925" dy="23">measurable activation gates.</tspan>
  </text>

  <text x="355" y="448" width="250" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6C7682">
    <tspan x="355" dy="0">Convert learning into repeatable</tspan>
    <tspan x="355" dy="23">systems, automation, and</tspan>
    <tspan x="355" dy="23">compounding growth loops.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rasterizing the circular arcs as an image; use native `<path>` arc strokes so the ring stays editable in PowerPoint.
- ❌ Applying `filter` to `<line>` elements for shadows; use circles and paths for shadowed elements.
- ❌ Using SVG markers for arrowheads on the flow ring; this technique reads as a continuous cycle through colored arc segmentation, not explicit arrows.
- ❌ Clipping or masking the node circles; regular filled circles with native filters translate more reliably.
- ❌ Overcrowding the center with long copy; keep the center label short so the three-node geometry remains dominant.

## Composition notes
- Place the whole mechanism around slide center, with the large nodes forming an equilateral triangle: top, lower-right, and lower-left.
- Keep the circular ring behind the white nodes; the nodes should obscure the arc joins and feel like raised cards.
- Use outward text blocks only where the node points: top annotation above, right annotation to the right, left annotation to the left.
- Maintain a calm gray-white background and reserve saturated green, orange, and blue only for numbers, arcs, and midpoint dots.