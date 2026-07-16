# SVG Recipe — Exploded Segmented Process Wheel

## Visual mechanism
A circular process diagram is built from independent SVG arc-sector paths, each moved outward along its own radial midpoint to create real transparent gaps between segments. Bright sequential colors, soft shadows, and embedded numbering make the wheel read as a premium, editable process framework rather than a flat pie chart.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<circle>` for soft decorative background accents
- 8× `<linearGradient>` for saturated wedge fills with subtle depth
- 1× `<filter id="wedgeShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for floating segment shadows
- 1× `<filter id="softGlow">` using `feGaussianBlur` for a faint central glow
- 8× `<path>` for the exploded pie-sector wedges
- 1× `<circle>` for the clean central negative-space hub
- 11× `<text>` for title, subtitle, caption, and wedge labels with explicit `width`
- 1× `<line>` for a small title accent rule

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="wedgeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <linearGradient id="gRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff2b2b"/><stop offset="100%" stop-color="#dc2626"/>
    </linearGradient>
    <linearGradient id="gBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563eb"/><stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>
    <linearGradient id="gCyan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22d3ee"/><stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
    <linearGradient id="gMint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#34d399"/><stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
    <linearGradient id="gLime" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7cff00"/><stop offset="100%" stop-color="#4ade00"/>
    </linearGradient>
    <linearGradient id="gYellow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffff00"/><stop offset="100%" stop-color="#eab308"/>
    </linearGradient>
    <linearGradient id="gMagenta" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ec4899"/><stop offset="100%" stop-color="#d000b8"/>
    </linearGradient>
    <linearGradient id="gPurple" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a855f7"/><stop offset="100%" stop-color="#7e22ce"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f8fafc"/>
  <circle cx="1090" cy="75" r="70" fill="#fff7db"/>
  <circle cx="1205" cy="655" r="54" fill="#fb7185" opacity="0.65"/>
  <circle cx="850" cy="382" r="74" fill="#ffffff" opacity="0.75" filter="url(#softGlow)"/>

  <text x="78" y="116" width="430" fill="#0f172a" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800">
    Exploded Process Wheel
  </text>
  <line x1="82" y1="145" x2="222" y2="145" stroke="#0ea5e9" stroke-width="6"/>
  <text x="80" y="194" width="415" fill="#475569" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="400">
    Eight independent vector segments form one continuous cycle, with real gaps and editable labels.
  </text>
  <text x="82" y="626" width="430" fill="#64748b" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600">
    Use for: operating models · customer journeys · maturity stages · transformation roadmaps
  </text>

  <path d="M 859 360 L 867 130 A 230 230 0 0 1 1016 192 Z" fill="url(#gRed)" filter="url(#wedgeShadow)"/>
  <path d="M 872 373 L 1030 205 A 230 230 0 0 1 1102 365 Z" fill="url(#gBlue)" filter="url(#wedgeShadow)"/>
  <path d="M 872 391 L 1102 399 A 230 230 0 0 1 1030 559 Z" fill="url(#gCyan)" filter="url(#wedgeShadow)"/>
  <path d="M 859 404 L 1016 572 A 230 230 0 0 1 867 634 Z" fill="url(#gMint)" filter="url(#wedgeShadow)"/>
  <path d="M 841 404 L 833 634 A 230 230 0 0 1 684 572 Z" fill="url(#gLime)" filter="url(#wedgeShadow)"/>
  <path d="M 828 391 L 660 548 A 230 230 0 0 1 598 399 Z" fill="url(#gYellow)" filter="url(#wedgeShadow)"/>
  <path d="M 828 373 L 598 365 A 230 230 0 0 1 660 216 Z" fill="url(#gMagenta)" filter="url(#wedgeShadow)"/>
  <path d="M 841 360 L 684 192 A 230 230 0 0 1 833 130 Z" fill="url(#gPurple)" filter="url(#wedgeShadow)"/>

  <circle cx="850" cy="382" r="34" fill="#f8fafc"/>

  <text x="860" y="221" width="120" text-anchor="middle" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="860" dy="0">01</tspan><tspan x="860" dy="25" font-size="13" font-weight="700">INITIATE</tspan>
  </text>
  <text x="1000" y="314" width="130" text-anchor="middle" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="1000" dy="0">02</tspan><tspan x="1000" dy="25" font-size="13" font-weight="700">PLAN</tspan>
  </text>
  <text x="1002" y="450" width="130" text-anchor="middle" fill="#083344" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="1002" dy="0">03</tspan><tspan x="1002" dy="25" font-size="13" font-weight="800">EXECUTE</tspan>
  </text>
  <text x="910" y="539" width="130" text-anchor="middle" fill="#064e3b" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="910" dy="0">04</tspan><tspan x="910" dy="25" font-size="13" font-weight="800">MONITOR</tspan>
  </text>
  <text x="790" y="539" width="130" text-anchor="middle" fill="#14532d" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="790" dy="0">05</tspan><tspan x="790" dy="25" font-size="13" font-weight="800">CONTROL</tspan>
  </text>
  <text x="696" y="450" width="130" text-anchor="middle" fill="#422006" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="696" dy="0">06</tspan><tspan x="696" dy="25" font-size="13" font-weight="800">EVALUATE</tspan>
  </text>
  <text x="698" y="314" width="130" text-anchor="middle" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="698" dy="0">07</tspan><tspan x="698" dy="25" font-size="13" font-weight="700">OPTIMIZE</tspan>
  </text>
  <text x="790" y="221" width="130" text-anchor="middle" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800">
    <tspan x="790" dy="0">08</tspan><tspan x="790" dy="25" font-size="13" font-weight="700">CLOSE</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a normal `<circle>` with thick white radial strokes to fake gaps; build separate wedge `<path>` elements instead.
- ❌ Applying `clip-path` or `mask` to the wedges; these are unnecessary and may not translate reliably.
- ❌ Putting the drop shadow filter on a parent `<g>`; apply `filter="url(#wedgeShadow)"` directly to each wedge path.
- ❌ Using `<textPath>` to bend labels around the arc; keep labels as editable horizontal `<text>` blocks.

## Composition notes
- Keep the wheel large, usually 430–520 px in diameter, and offset it right if the slide also needs an explanatory title block.
- Preserve visible negative space between wedges; the exploded offsets should be large enough to read as intentional separation, not rendering errors.
- Use a clockwise rainbow or sequential palette so the viewer intuitively follows the process loop.
- Place text near each wedge’s radial midpoint, not at the sharp inner point, to avoid cramped labels.