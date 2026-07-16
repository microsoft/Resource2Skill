# SVG Recipe — Chevron-Tabular Graphic List

## Visual mechanism
A standard table is transformed into stacked ribbon rows: each row begins with a dark icon block and a bright forward-pointing chevron that overlaps into soft grey data cells. Detached rounded “pill” headers label the columns while thin white gaps replace traditional gridlines.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× decorative `<circle>` elements for subtle dashboard atmosphere
- 1× `<text>` for the main title
- 1× `<text>` for the subtitle
- 2× `<rect rx>` for floating pill column headers
- 2× `<text>` for pill header labels
- 8× `<rect>` for grey description/pricing data cells across four rows
- 4× `<path>` for the colored chevron title tabs
- 4× `<rect>` for dark icon blocks
- 4× `<text>` for icon glyphs
- 4× `<text>` for row titles inside chevrons
- 4× `<text>` for description copy
- 4× `<text>` for bold pricing values
- 1× `<filter id="softShadow">` applied to row blocks and headers
- 1× `<linearGradient>` for a subtle background wash

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f6f8fb"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <circle cx="1080" cy="128" r="120" fill="#3498db" fill-opacity="0.07"/>
  <circle cx="164" cy="612" r="150" fill="#2ecc71" fill-opacity="0.06"/>

  <text x="0" y="74" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#3c3c3c">
    LIST OF PRODUCTS
  </text>
  <text x="0" y="112" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" letter-spacing="1.2" fill="#8c8c8c">
    FEATURE COMPARISON WITH MODULAR CHEVRON ROWS
  </text>

  <!-- Detached pill column headers -->
  <rect x="475" y="166" width="500" height="42" rx="21" fill="#505050" filter="url(#softShadow)"/>
  <rect x="982" y="166" width="190" height="42" rx="21" fill="#505050" filter="url(#softShadow)"/>
  <text x="725" y="193" width="500" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">
    DESCRIPTION
  </text>
  <text x="1077" y="193" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">
    PRICING
  </text>

  <!-- Row 1: draw grey cells first, then overlap chevron on top -->
  <rect x="475" y="236" width="500" height="76" fill="#ebebeb" filter="url(#softShadow)"/>
  <rect x="982" y="236" width="190" height="76" fill="#f7f7f7" filter="url(#softShadow)"/>
  <path d="M250 236 L455 236 L500 274 L455 312 L250 312 Z" fill="#3498db"/>
  <rect x="210" y="236" width="78" height="76" fill="#2980b9"/>
  <text x="249" y="283" width="78" text-anchor="middle"
        font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="28" fill="#ffffff">◆</text>
  <text x="310" y="281" width="160"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">
    PRODUCT 01
  </text>
  <text x="515" y="281" width="420"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    Analytics dashboard, export tools, and role-based permissions.
  </text>
  <text x="1077" y="282" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#3f3f3f">
    $ 36
  </text>

  <!-- Row 2 -->
  <rect x="475" y="332" width="500" height="76" fill="#ebebeb" filter="url(#softShadow)"/>
  <rect x="982" y="332" width="190" height="76" fill="#f7f7f7" filter="url(#softShadow)"/>
  <path d="M250 332 L455 332 L500 370 L455 408 L250 408 Z" fill="#e74c3c"/>
  <rect x="210" y="332" width="78" height="76" fill="#c0392b"/>
  <text x="249" y="379" width="78" text-anchor="middle"
        font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="28" fill="#ffffff">⚙</text>
  <text x="310" y="377" width="160"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">
    PRODUCT 02
  </text>
  <text x="515" y="377" width="420"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    Workflow automation, API access, and audit-ready activity logs.
  </text>
  <text x="1077" y="378" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#3f3f3f">
    $ 42
  </text>

  <!-- Row 3 -->
  <rect x="475" y="428" width="500" height="76" fill="#ebebeb" filter="url(#softShadow)"/>
  <rect x="982" y="428" width="190" height="76" fill="#f7f7f7" filter="url(#softShadow)"/>
  <path d="M250 428 L455 428 L500 466 L455 504 L250 504 Z" fill="#f39c12"/>
  <rect x="210" y="428" width="78" height="76" fill="#d35400"/>
  <text x="249" y="475" width="78" text-anchor="middle"
        font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="27" fill="#ffffff">▣</text>
  <text x="310" y="473" width="160"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">
    PRODUCT 03
  </text>
  <text x="515" y="473" width="420"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    Premium integrations, enterprise SSO, and priority support.
  </text>
  <text x="1077" y="474" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#3f3f3f">
    $ 89
  </text>

  <!-- Row 4 -->
  <rect x="475" y="524" width="500" height="76" fill="#ebebeb" filter="url(#softShadow)"/>
  <rect x="982" y="524" width="190" height="76" fill="#f7f7f7" filter="url(#softShadow)"/>
  <path d="M250 524 L455 524 L500 562 L455 600 L250 600 Z" fill="#2ecc71"/>
  <rect x="210" y="524" width="78" height="76" fill="#27ae60"/>
  <text x="249" y="571" width="78" text-anchor="middle"
        font-family="Segoe UI Symbol, Segoe UI, Microsoft YaHei" font-size="27" fill="#ffffff">★</text>
  <text x="310" y="569" width="160"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">
    PRODUCT 04
  </text>
  <text x="515" y="569" width="420"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">
    Collaboration suite, branded portals, and team governance.
  </text>
  <text x="1077" y="570" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#3f3f3f">
    $ 63
  </text>
</svg>
```

## Avoid in this skill
- ❌ Standard `<table>`-like grids or heavy stroked cell borders; the look depends on white gaps and borderless blocks.
- ❌ Leaving a visible gap between the chevron point and the grey description cell; the chevron should overlap the data row.
- ❌ Applying `clip-path` to chevron or rectangle shapes; use direct `<path>` geometry instead.
- ❌ Using `marker-end` arrows for the chevron effect; build the arrow tab as a filled pentagon path.
- ❌ Centering every row element independently; the row feels premium only when all column edges are mathematically aligned.

## Composition notes
- Keep the list block centered, occupying roughly 75% of the slide width, with generous title space above.
- The dark icon square and bright chevron form the visual anchor; the grey cells should recede and stay quiet.
- Use a micro-gap of 6–8 px between data columns so the white background becomes the divider.
- Give each row a distinct accent color, but keep the data cells neutral to preserve tabular readability.