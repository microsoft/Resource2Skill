# SVG Recipe — Circular Pin Gauge Infographic

## Visual mechanism
Build three dashboard metric nodes as “map pin” silhouettes: a teardrop-shaped pin base holds a dark inner circular gauge, while a thick gold arc wraps around the number to show completion. Red triangular pointers and compact captions beneath each pin turn the gauges into a clean executive infographic row.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark slate background
- 1× `<radialGradient>` for subtle background depth
- 1× `<linearGradient>` for the blue pin-body fill
- 1× `<linearGradient>` for the gold progress arc stroke
- 1× `<filter id="softShadow">` applied to pin bases for lifted depth
- 1× `<filter id="textGlow">` applied to the title for a faint keynote-style glow
- 3× `<path>` for custom location-pin silhouettes
- 3× `<circle>` for dark circular gauge holes / negative-space centers
- 3× `<circle>` for muted circular gauge tracks
- 3× `<path>` for percentage progress arcs
- 3× `<path>` for small red triangular label pointers
- 4× `<line>` for subtle vertical column separators and caption rules
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, percentages, “PERCENT” labels, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="18%" r="85%">
      <stop offset="0%" stop-color="#304057"/>
      <stop offset="55%" stop-color="#232e3e"/>
      <stop offset="100%" stop-color="#1b2431"/>
    </radialGradient>

    <linearGradient id="pinBlue" x1="0" y1="-120" x2="0" y2="180" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#344963"/>
      <stop offset="100%" stop-color="#253448"/>
    </linearGradient>

    <linearGradient id="goldArc" x1="-90" y1="-90" x2="90" y2="90" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffe277"/>
      <stop offset="48%" stop-color="#ffc000"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <circle cx="95" cy="90" r="170" fill="none" stroke="#41546e" stroke-width="1.2" opacity="0.20"/>
  <circle cx="1190" cy="650" r="230" fill="none" stroke="#41546e" stroke-width="1.2" opacity="0.18"/>
  <line x1="426" y1="245" x2="426" y2="645" stroke="#4b5f78" stroke-width="1" opacity="0.22"/>
  <line x1="854" y1="245" x2="854" y2="645" stroke="#4b5f78" stroke-width="1" opacity="0.22"/>

  <text x="640" y="92" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700"
        letter-spacing="12" fill="#ffffff" filter="url(#textGlow)">INFOGRAPHICS</text>

  <text x="640" y="134" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#a8b3c1">
    <tspan x="640" dy="0">Transform key percentages into polished circular pin gauges</tspan>
    <tspan x="640" dy="23">for milestones, performance reporting, and executive summaries.</tspan>
  </text>

  <g transform="translate(260 365)">
    <path d="M 0 172 C -18 132 -108 82 -108 0 C -108 -64 -64 -108 0 -108 C 64 -108 108 -64 108 0 C 108 82 18 132 0 172 Z"
          fill="url(#pinBlue)" filter="url(#softShadow)"/>
    <circle cx="0" cy="0" r="86" fill="none" stroke="#1a2533" stroke-width="18" opacity="0.95"/>
    <path d="M 0 -86 A 86 86 0 0 1 58.9 62.7"
          fill="none" stroke="url(#goldArc)" stroke-width="18" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="58" fill="#232e3e"/>
    <text x="0" y="-8" width="140" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#ffffff">38</text>
    <text x="0" y="29" width="140" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2.6" fill="#9ca3af">PERCENT</text>
    <path d="M -10 205 L 10 205 L 0 222 Z" fill="#ef4444"/>
    <line x1="-70" y1="238" x2="70" y2="238" stroke="#53677f" stroke-width="1" opacity="0.55"/>
    <text x="0" y="268" width="250" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Market Reach</text>
    <text x="0" y="296" width="250" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#a8b3c1">New audience penetration</text>
  </g>

  <g transform="translate(640 365)">
    <path d="M 0 172 C -18 132 -108 82 -108 0 C -108 -64 -64 -108 0 -108 C 64 -108 108 -64 108 0 C 108 82 18 132 0 172 Z"
          fill="url(#pinBlue)" filter="url(#softShadow)"/>
    <circle cx="0" cy="0" r="86" fill="none" stroke="#1a2533" stroke-width="18" opacity="0.95"/>
    <path d="M 0 -86 A 86 86 0 0 1 36.6 77.8"
          fill="none" stroke="url(#goldArc)" stroke-width="18" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="58" fill="#232e3e"/>
    <text x="0" y="-8" width="140" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#ffffff">43</text>
    <text x="0" y="29" width="140" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2.6" fill="#9ca3af">PERCENT</text>
    <path d="M -10 205 L 10 205 L 0 222 Z" fill="#ef4444"/>
    <line x1="-70" y1="238" x2="70" y2="238" stroke="#53677f" stroke-width="1" opacity="0.55"/>
    <text x="0" y="268" width="250" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Product Adoption</text>
    <text x="0" y="296" width="250" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#a8b3c1">Active feature utilization</text>
  </g>

  <g transform="translate(1020 365)">
    <path d="M 0 172 C -18 132 -108 82 -108 0 C -108 -64 -64 -108 0 -108 C 64 -108 108 -64 108 0 C 108 82 18 132 0 172 Z"
          fill="url(#pinBlue)" filter="url(#softShadow)"/>
    <circle cx="0" cy="0" r="86" fill="none" stroke="#1a2533" stroke-width="18" opacity="0.95"/>
    <path d="M 0 -86 A 86 86 0 1 1 -77.8 36.6"
          fill="none" stroke="url(#goldArc)" stroke-width="18" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="58" fill="#232e3e"/>
    <text x="0" y="-8" width="140" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#ffffff">68</text>
    <text x="0" y="29" width="140" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2.6" fill="#9ca3af">PERCENT</text>
    <path d="M -10 205 L 10 205 L 0 222 Z" fill="#ef4444"/>
    <line x1="-70" y1="238" x2="70" y2="238" stroke="#53677f" stroke-width="1" opacity="0.55"/>
    <text x="0" y="268" width="250" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Milestone Health</text>
    <text x="0" y="296" width="250" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#a8b3c1">Delivery progress this quarter</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using SVG `<mask>` to punch out the inner hole; instead, overlay a background-colored `<circle>` so PowerPoint keeps it editable.
- ❌ Applying `clip-path` to gauge shapes; clipping is only reliable for `<image>` elements in this workflow.
- ❌ Using `marker-end` on curved paths for the red pointers; draw small triangular `<path>` shapes directly.
- ❌ Relying on `<textPath>` for curved labels around the gauge; keep labels as normal editable `<text>`.
- ❌ Creating the pin from many tiny decorative shapes; one clean editable `<path>` per pin gives a more premium, stable result.

## Composition notes
- Keep the slide in three strict vertical columns, with each pin centered horizontally in its column and aligned to the same baseline.
- Reserve the upper 20–25% of the canvas for title and subtitle; the gauges should occupy the visual middle and lower-middle.
- Use a dark slate background and slightly lighter blue pins so the gold arcs become the primary visual focus.
- Place captions below the pin tips, not inside the gauge, to preserve the number’s clarity and maintain generous negative space.