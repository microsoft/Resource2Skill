# SVG Recipe — Triple Gauge Dashboard

## Visual mechanism
Three equal-width metric cards hold large semi-circular gauges with thick background arcs, colored progress arcs, end-cap dots, and oversized percentage labels. A restrained corporate palette, soft shadows, and small tick marks make the layout feel like an executive KPI dashboard while keeping every element editable.

## SVG primitives needed
- 5× `<rect>` for the slide background, top accent bar, and three rounded metric cards
- 2× decorative `<path>` blobs for subtle background atmosphere
- 6× gauge `<path>` arcs for the three pale track arcs and three colored progress arcs
- 3× `<circle>` end-cap dots on the progress arcs
- 15× `<line>` tick marks distributed around the semi-circular gauges
- 18× `<text>` elements for title, subtitle, metric names, values, captions, and deltas
- 4× `<linearGradient>` definitions for background and gauge colors
- 1× `<filter id="softShadow">` applied to cards
- 1× `<filter id="arcGlow">` applied to colored progress arcs and end dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFF"/>
      <stop offset="100%" stop-color="#EEF3FA"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="170" y1="400" x2="405" y2="300">
      <stop offset="0%" stop-color="#19C3FF"/>
      <stop offset="100%" stop-color="#246BFE"/>
    </linearGradient>
    <linearGradient id="amberGrad" x1="525" y1="400" x2="760" y2="300">
      <stop offset="0%" stop-color="#FFB84D"/>
      <stop offset="100%" stop-color="#FF6A3D"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="880" y1="400" x2="1115" y2="300">
      <stop offset="0%" stop-color="#31D7A1"/>
      <stop offset="100%" stop-color="#0E9F6E"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="arcGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="8" fill="#246BFE"/>
  <path d="M1045 52 C1135 18 1235 66 1268 146 C1307 240 1211 288 1124 261 C1032 232 967 82 1045 52 Z" fill="#DDE8FF" opacity="0.55"/>
  <path d="M-70 582 C55 520 132 610 224 574 C310 540 346 654 240 706 C126 762 -27 727 -70 582 Z" fill="#D9F6EF" opacity="0.55"/>

  <text x="72" y="78" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#18233F">Quarterly Performance Pulse</text>
  <text x="74" y="115" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#61708C">Three executive indicators normalized to a consistent semi-circular gauge scale.</text>
  <text x="1000" y="78" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#246BFE" text-anchor="end">FY26 · LIVE SNAPSHOT</text>

  <rect x="110" y="172" width="350" height="450" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="465" y="172" width="350" height="450" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="820" y="172" width="350" height="450" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="152" y="230" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#18233F">Revenue Velocity</text>
  <text x="152" y="257" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A879B">Bookings against quarterly target</text>
  <path d="M170 410 A115 115 0 0 1 400 410" fill="none" stroke="#E7ECF4" stroke-width="28" stroke-linecap="round"/>
  <path d="M170 410 A115 115 0 0 1 373.5 336.7" fill="none" stroke="url(#cyanGrad)" stroke-width="28" stroke-linecap="round" filter="url(#arcGlow)"/>
  <circle cx="373.5" cy="336.7" r="10" fill="#246BFE" filter="url(#arcGlow)"/>
  <line x1="170" y1="410" x2="151" y2="410" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="203.7" y1="328.7" x2="190.3" y2="315.3" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="285" y1="295" x2="285" y2="276" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="366.3" y1="328.7" x2="379.7" y2="315.3" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="400" y1="410" x2="419" y2="410" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <text x="190" y="396" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#18233F" text-anchor="middle">78%</text>
  <text x="190" y="432" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A879B" text-anchor="middle">Target completion</text>
  <text x="152" y="548" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0E9F6E">▲ +12.4%</text>
  <text x="262" y="548" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A879B">vs. prior quarter</text>

  <text x="507" y="230" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#18233F">Delivery Health</text>
  <text x="507" y="257" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A879B">Milestones shipped on committed date</text>
  <path d="M525 410 A115 115 0 0 1 755 410" fill="none" stroke="#E7ECF4" stroke-width="28" stroke-linecap="round"/>
  <path d="M525 410 A115 115 0 0 1 689 306.1" fill="none" stroke="url(#amberGrad)" stroke-width="28" stroke-linecap="round" filter="url(#arcGlow)"/>
  <circle cx="689" cy="306.1" r="10" fill="#FF6A3D" filter="url(#arcGlow)"/>
  <line x1="525" y1="410" x2="506" y2="410" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="558.7" y1="328.7" x2="545.3" y2="315.3" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="640" y1="295" x2="640" y2="276" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="721.3" y1="328.7" x2="734.7" y2="315.3" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="755" y1="410" x2="774" y2="410" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <text x="545" y="396" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#18233F" text-anchor="middle">64%</text>
  <text x="545" y="432" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A879B" text-anchor="middle">Schedule confidence</text>
  <text x="507" y="548" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FF6A3D">▼ −4.8%</text>
  <text x="617" y="548" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A879B">requires attention</text>

  <text x="862" y="230" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#18233F">Customer Trust</text>
  <text x="862" y="257" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A879B">Composite NPS and renewal intent</text>
  <path d="M880 410 A115 115 0 0 1 1110 410" fill="none" stroke="#E7ECF4" stroke-width="28" stroke-linecap="round"/>
  <path d="M880 410 A115 115 0 0 1 1105.4 377.9" fill="none" stroke="url(#greenGrad)" stroke-width="28" stroke-linecap="round" filter="url(#arcGlow)"/>
  <circle cx="1105.4" cy="377.9" r="10" fill="#0E9F6E" filter="url(#arcGlow)"/>
  <line x1="880" y1="410" x2="861" y2="410" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="913.7" y1="328.7" x2="900.3" y2="315.3" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="995" y1="295" x2="995" y2="276" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="1076.3" y1="328.7" x2="1089.7" y2="315.3" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <line x1="1110" y1="410" x2="1129" y2="410" stroke="#B8C2D4" stroke-width="3" stroke-linecap="round"/>
  <text x="900" y="396" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#18233F" text-anchor="middle">91%</text>
  <text x="900" y="432" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A879B" text-anchor="middle">Advocacy index</text>
  <text x="862" y="548" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#0E9F6E">▲ +6.1%</text>
  <text x="972" y="548" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A879B">best-in-class zone</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to hide the lower half of a donut; build the gauge directly as semi-circular arc paths.
- ❌ Do not use `marker-end` for gauge pointers or arrows; if needed, construct pointers from editable `<line>` and `<circle>` primitives.
- ❌ Do not apply filters to `<line>` tick marks; shadows and glows on lines may be dropped.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint text boxes may render with unexpected wrapping.
- ❌ Do not use `<textPath>` for curved labels around the gauges; use straight captions instead.

## Composition notes
- Keep the three cards identical in size and aligned to a strict horizontal rhythm; the dashboard reads best when the gauges share the same centerline and radius.
- Reserve the upper 15–18% of the slide for headline and context; the visual focus should sit in the middle third.
- Use one accent color per gauge, but keep the track arcs, ticks, captions, and cards neutral so the values remain dominant.
- Place percentages inside the open area under each arc, with small explanatory captions and deltas below to avoid cluttering the gauge itself.