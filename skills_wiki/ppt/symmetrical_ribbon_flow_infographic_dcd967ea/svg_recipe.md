# SVG Recipe — Symmetrical Ribbon-Flow Infographic

## Visual mechanism
A symmetrical process-flow layout uses angled ribbon polygons to pull widely spaced left/right content cards into a tightly compressed central vertical spine. The ribbons sit behind white rounded cards and colored center nodes, creating a premium “folded perspective” convergence effect.

## SVG primitives needed
- 1× `<rect>` for the light gray slide background
- 10× `<path>` for the angled ribbon connectors from outer cards to the central axis
- 10× `<rect>` for white rounded content cards with soft drop shadows
- 5× `<rect>` for compact central axis nodes
- 1× `<rect>` for a subtle central spine behind the nodes
- 1× `<filter id="cardShadow">` applied to the content cards
- 1× `<filter id="spineGlow">` applied to the central spine
- 1× `<linearGradient>` for the background vignette
- 5× `<linearGradient>` definitions for row ribbons, adding dimensional color depth
- Multiple `<text>` elements with nested `<tspan>` for titles, descriptions, and center labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#f4f4f4"/>
      <stop offset="100%" stop-color="#e4e4e4"/>
    </linearGradient>

    <linearGradient id="r1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#b7e76f"/>
      <stop offset="100%" stop-color="#7fca38"/>
    </linearGradient>
    <linearGradient id="r2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#20c26a"/>
      <stop offset="100%" stop-color="#009b45"/>
    </linearGradient>
    <linearGradient id="r3" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#18c9f5"/>
      <stop offset="100%" stop-color="#0097d3"/>
    </linearGradient>
    <linearGradient id="r4" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1689d8"/>
      <stop offset="100%" stop-color="#005fae"/>
    </linearGradient>
    <linearGradient id="r5" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#143f93"/>
      <stop offset="100%" stop-color="#001f60"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="spineGlow" x="-80%" y="-30%" width="260%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="640" y="54" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#252525">
    10 OPTIONS PERSPECTIVE
  </text>
  <text x="640" y="82" width="720" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    Disparate workstreams converge into one compressed decision pipeline
  </text>

  <!-- Back-layer perspective ribbons -->
  <path d="M430 103 L610 236 L610 278 L430 155 Z" fill="url(#r1)" opacity="0.94"/>
  <path d="M850 103 L670 236 L670 278 L850 155 Z" fill="url(#r1)" opacity="0.94"/>
  <path d="M430 213 L610 284 L610 326 L430 265 Z" fill="url(#r2)" opacity="0.94"/>
  <path d="M850 213 L670 284 L670 326 L850 265 Z" fill="url(#r2)" opacity="0.94"/>
  <path d="M430 323 L610 332 L610 374 L430 375 Z" fill="url(#r3)" opacity="0.94"/>
  <path d="M850 323 L670 332 L670 374 L850 375 Z" fill="url(#r3)" opacity="0.94"/>
  <path d="M430 433 L610 380 L610 422 L430 485 Z" fill="url(#r4)" opacity="0.94"/>
  <path d="M850 433 L670 380 L670 422 L850 485 Z" fill="url(#r4)" opacity="0.94"/>
  <path d="M430 543 L610 428 L610 470 L430 595 Z" fill="url(#r5)" opacity="0.94"/>
  <path d="M850 543 L670 428 L670 470 L850 595 Z" fill="url(#r5)" opacity="0.94"/>

  <!-- Central compressed axis -->
  <rect x="630" y="220" width="20" height="270" rx="10" fill="#ffffff" opacity="0.6" filter="url(#spineGlow)"/>
  <rect x="610" y="236" width="60" height="42" rx="4" fill="#92d050"/>
  <rect x="610" y="284" width="60" height="42" rx="4" fill="#00b050"/>
  <rect x="610" y="332" width="60" height="42" rx="4" fill="#00b0f0"/>
  <rect x="610" y="380" width="60" height="42" rx="4" fill="#0070c0"/>
  <rect x="610" y="428" width="60" height="42" rx="4" fill="#002060"/>

  <text x="640" y="263" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">01</text>
  <text x="640" y="311" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">02</text>
  <text x="640" y="359" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">03</text>
  <text x="640" y="407" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">04</text>
  <text x="640" y="455" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">05</text>

  <!-- Foreground content cards -->
  <rect x="90" y="95" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="840" y="95" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="90" y="205" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="840" y="205" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="90" y="315" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="840" y="315" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="90" y="425" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="840" y="425" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="90" y="535" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="840" y="535" width="350" height="68" rx="12" fill="#ffffff" filter="url(#cardShadow)"/>

  <text x="122" y="122" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#7fca38" font-weight="700">OPTION 01</tspan><tspan x="122" dy="22">Market sensing and early signal capture</tspan></text>
  <text x="1158" y="122" width="285" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#7fca38" font-weight="700">OPTION 06</tspan><tspan x="1158" dy="22">Customer feedback and validation loop</tspan></text>

  <text x="122" y="232" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#009b45" font-weight="700">OPTION 02</tspan><tspan x="122" dy="22">Resource allocation across initiatives</tspan></text>
  <text x="1158" y="232" width="285" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#009b45" font-weight="700">OPTION 07</tspan><tspan x="1158" dy="22">Partner ecosystem activation plan</tspan></text>

  <text x="122" y="342" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#0097d3" font-weight="700">OPTION 03</tspan><tspan x="122" dy="22">Operational model and governance</tspan></text>
  <text x="1158" y="342" width="285" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#0097d3" font-weight="700">OPTION 08</tspan><tspan x="1158" dy="22">Data platform and reporting cadence</tspan></text>

  <text x="122" y="452" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#005fae" font-weight="700">OPTION 04</tspan><tspan x="122" dy="22">Commercial pilots and launch gates</tspan></text>
  <text x="1158" y="452" width="285" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#005fae" font-weight="700">OPTION 09</tspan><tspan x="1158" dy="22">Risk controls and executive reviews</tspan></text>

  <text x="122" y="562" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#001f60" font-weight="700">OPTION 05</tspan><tspan x="122" dy="22">Scale-up roadmap and capability build</tspan></text>
  <text x="1158" y="562" width="285" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#777777"><tspan fill="#001f60" font-weight="700">OPTION 10</tspan><tspan x="1158" dy="22">Enterprise adoption and value tracking</tspan></text>
</svg>
```

## Avoid in this skill
- ❌ Drawing connectors as simple straight `<line>` elements; the illusion depends on filled quadrilateral ribbons with thickness.
- ❌ Placing ribbons above the content cards or center nodes; they must be back-layer geometry.
- ❌ Using `<mask>` or clipping non-image objects to create folds; use explicit `<path>` shapes instead.
- ❌ Overcrowding the center spine with long labels; keep center nodes short and compressed.
- ❌ Making outer and center rows equally spaced; the perspective effect requires wide outer spacing and tight center spacing.

## Composition notes
- Keep the slide bilaterally symmetrical: left and right cards should mirror each other around the vertical center axis.
- Use a light neutral background so the white cards and saturated ribbons separate clearly.
- Let the ribbons occupy the middle third of the slide; the outer cards should remain readable with generous padding.
- Apply color row-by-row from light to dark to imply top-to-bottom reading order and maintain visual rhythm.