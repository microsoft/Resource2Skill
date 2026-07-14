# SVG Recipe — Segmented Radial Infographic

## Visual mechanism
A thick 270-degree doughnut arc is split into color-coded segments around a central hub, leaving a deliberate open gap at the bottom. Each segment sends a short radial connector outward, then a clean horizontal leader line into aligned explanation cards on the slide margins.

## SVG primitives needed
- 1× `<rect>` for the soft slide background
- 4× `<path>` for editable doughnut-arc segment wedges
- 4× `<text>` for bold white segment numbers placed inside the arcs
- 8× `<line>` for two-part connectors: radial break-out plus horizontal leader
- 4× `<circle>` for connector elbow nodes
- 4× `<rect>` for white information cards
- 4× `<rect>` for colored card accent bars
- 8× `<text>` for card headings and body copy
- 1× `<circle>` for the central hub panel
- 5× `<circle>` for the inner hub ring and decorative dots
- 2× `<text>` for the central hub label
- 2× `<linearGradient>` for background and hub polish
- 1× `<filter id="softShadow">` applied to cards and hub shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfcff"/>
      <stop offset="55%" stop-color="#f4f6fb"/>
      <stop offset="100%" stop-color="#eef2f8"/>
    </linearGradient>
    <linearGradient id="hubGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#edf2f8"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="70" y="70" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1f2937">
    Segmented Radial Infographic
  </text>
  <text x="72" y="104" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7b8494">
    Four strategic pillars orbit a shared operating core
  </text>

  <!-- Left information cards -->
  <rect x="68" y="154" width="330" height="116" rx="20" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="68" y="174" width="7" height="76" rx="3.5" fill="#13294B"/>
  <text x="96" y="194" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#13294B">Customer Intelligence</text>
  <text x="96" y="222" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667085">
    <tspan x="96" dy="0">Convert research signals into</tspan>
    <tspan x="96" dy="18">clear opportunity territories and</tspan>
    <tspan x="96" dy="18">prioritized experience moments.</tspan>
  </text>

  <rect x="68" y="416" width="330" height="116" rx="20" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="68" y="436" width="7" height="76" rx="3.5" fill="#DA3832"/>
  <text x="96" y="456" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#DA3832">Market Activation</text>
  <text x="96" y="484" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667085">
    <tspan x="96" dy="0">Launch coordinated campaigns</tspan>
    <tspan x="96" dy="18">through regional playbooks,</tspan>
    <tspan x="96" dy="18">partner channels, and offers.</tspan>
  </text>

  <!-- Right information cards -->
  <rect x="882" y="154" width="330" height="116" rx="20" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="1205" y="174" width="7" height="76" rx="3.5" fill="#0072CE"/>
  <text x="912" y="194" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0072CE">Digital Platform</text>
  <text x="912" y="222" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667085">
    <tspan x="912" dy="0">Unify data, workflow, and</tspan>
    <tspan x="912" dy="18">analytics into one scalable</tspan>
    <tspan x="912" dy="18">commercial enablement layer.</tspan>
  </text>

  <rect x="882" y="416" width="330" height="116" rx="20" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="1205" y="436" width="7" height="76" rx="3.5" fill="#FFC000"/>
  <text x="912" y="456" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#B88700">Performance Loop</text>
  <text x="912" y="484" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667085">
    <tspan x="912" dy="0">Track adoption, revenue lift,</tspan>
    <tspan x="912" dy="18">and operational signals, then</tspan>
    <tspan x="912" dy="18">feed learning back into plans.</tspan>
  </text>

  <!-- Segmented 270-degree radial arc; center=(640,400), outer radius=210, inner radius=124 -->
  <path d="M 491.5 548.5 A 210 210 0 0 1 439.2 338.6 L 521.4 363.7 A 124 124 0 0 0 552.3 487.7 Z"
        fill="#DA3832" stroke="#F4F6FB" stroke-width="7" stroke-linejoin="round"/>
  <path d="M 445.3 321.3 A 210 210 0 0 1 618.1 191.2 L 627.0 276.7 A 124 124 0 0 0 525.0 353.6 Z"
        fill="#13294B" stroke="#F4F6FB" stroke-width="7" stroke-linejoin="round"/>
  <path d="M 636.3 190.0 A 210 210 0 0 1 823.7 298.2 L 748.4 339.9 A 124 124 0 0 0 637.8 276.0 Z"
        fill="#0072CE" stroke="#F4F6FB" stroke-width="7" stroke-linejoin="round"/>
  <path d="M 831.8 314.6 A 210 210 0 0 1 805.5 529.3 L 737.7 476.3 A 124 124 0 0 0 753.3 349.6 Z"
        fill="#FFC000" stroke="#F4F6FB" stroke-width="7" stroke-linejoin="round"/>

  <!-- Segment numbers -->
  <text x="478" y="447" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#ffffff">01</text>
  <text x="539" y="274" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#ffffff">02</text>
  <text x="724" y="262" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#ffffff">03</text>
  <text x="806" y="427" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#ffffff">04</text>

  <!-- Connectors: radial then horizontal -->
  <line x1="513.6" y1="232.3" x2="482.3" y2="206.8" stroke="#13294B" stroke-width="2.5"/>
  <line x1="482.3" y1="206.8" x2="398" y2="206.8" stroke="#13294B" stroke-width="2.5"/>
  <circle cx="482.3" cy="206.8" r="6" fill="#13294B"/>

  <line x1="436.2" y1="450.8" x2="405.2" y2="458.5" stroke="#DA3832" stroke-width="2.5"/>
  <line x1="405.2" y1="458.5" x2="398" y2="458.5" stroke="#DA3832" stroke-width="2.5"/>
  <circle cx="405.2" cy="458.5" r="6" fill="#DA3832"/>

  <line x1="745.0" y1="218.1" x2="761.0" y2="190.3" stroke="#0072CE" stroke-width="2.5"/>
  <line x1="761.0" y1="190.3" x2="882" y2="190.3" stroke="#0072CE" stroke-width="2.5"/>
  <circle cx="761.0" cy="190.3" r="6" fill="#0072CE"/>

  <line x1="848.4" y1="425.6" x2="879.7" y2="429.5" stroke="#FFC000" stroke-width="2.5"/>
  <line x1="879.7" y1="429.5" x2="882" y2="429.5" stroke="#FFC000" stroke-width="2.5"/>
  <circle cx="879.7" cy="429.5" r="6" fill="#FFC000"/>

  <!-- Central hub -->
  <circle cx="640" cy="400" r="92" fill="url(#hubGrad)" filter="url(#softShadow)"/>
  <circle cx="640" cy="400" r="54" fill="none" stroke="#d6deea" stroke-width="2"/>
  <circle cx="640" cy="346" r="5" fill="#13294B"/>
  <circle cx="694" cy="400" r="5" fill="#0072CE"/>
  <circle cx="640" cy="454" r="5" fill="#FFC000"/>
  <circle cx="586" cy="400" r="5" fill="#DA3832"/>

  <text x="590" y="395" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" fill="#1f2937">CORE</text>
  <text x="570" y="422" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#7b8494">Operating model</text>
</svg>
```

## Avoid in this skill
- ❌ `<path marker-end="...">` arrowheads for connectors; use plain `<line>` segments and small `<circle>` nodes instead.
- ❌ `<mask>` or clipping on arc shapes to create the doughnut; build each segment as a true closed `<path>` so it remains editable.
- ❌ A single stroked circle with `stroke-dasharray` if you need independently editable colored segments and labels.
- ❌ Filters on connector `<line>` elements; PowerPoint translation drops line filters, so keep connector lines flat.
- ❌ Text without explicit `width`; every label, number, title, and body block should include a `width` attribute.

## Composition notes
- Keep the radial graphic centered and slightly lower than the title area; the open bottom gap gives the diagram breathing room.
- Use the left and right thirds of the slide for text cards, with the arc occupying the central 40–45% of the canvas.
- Match connector color to its segment color, but keep card body text neutral gray for a consulting-style hierarchy.
- The premium look comes from precise geometry: equal segment thickness, consistent gaps, aligned horizontal leaders, and balanced negative space around the hub.