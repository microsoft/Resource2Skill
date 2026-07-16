# SVG Recipe — Neo-Dark Analytics Dashboard

## Visual mechanism
A deep charcoal canvas is divided into rounded, elevated widget panels that mimic a premium SaaS analytics command center. Neon data marks, soft glow filters, and rotated gradient pill tags overlapping each panel create the signature high-contrast “neo-dark” dashboard feel.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 1× `<radialGradient>` for a subtle ambient neon glow behind the dashboard
- 4× large rounded `<rect>` panels for dashboard widgets
- 4× rotated rounded `<rect>` pill tags with orange-to-pink gradient fills
- Multiple `<text>` elements with explicit `width` attributes for title, subtitles, labels, axes, legends, and metrics
- Multiple `<line>` elements for chart axes and gridlines
- 3× glowing `<path>` elements for smooth line-chart series
- Multiple rounded `<rect>` elements for vertical and horizontal bar charts
- 4× thick-stroked `<path>` arc segments for the doughnut chart
- 1× `<linearGradient id="tagGrad">` for rotated category tags
- 3× `<linearGradient>` fills for neon bars
- 2× `<filter>` effects: one soft shadow for panels, one glow for neon chart marks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="48%" cy="42%" r="75%">
      <stop offset="0%" stop-color="#24242c"/>
      <stop offset="58%" stop-color="#121214"/>
      <stop offset="100%" stop-color="#08080a"/>
    </radialGradient>
    <linearGradient id="tagGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff8a00"/>
      <stop offset="48%" stop-color="#ff4b2b"/>
      <stop offset="100%" stop-color="#ff006f"/>
    </linearGradient>
    <linearGradient id="pinkBar" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#ff007f" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff2f8f"/>
    </linearGradient>
    <linearGradient id="cyanBar" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#1ea7ff"/>
    </linearGradient>
    <linearGradient id="greenBar" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#00ff88" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#44d99d"/>
    </linearGradient>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <text x="58" y="54" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">Neo-Dark Analytics Dashboard</text>
  <text x="60" y="84" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8f9099">Executive performance snapshot · Q4 revenue, activation, and retention signals</text>
  <text x="1018" y="54" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#00f0ff" text-anchor="end">LIVE MODEL VIEW</text>

  <rect x="88" y="132" width="540" height="238" rx="24" fill="#1e1e26" stroke="#383844" stroke-width="1.2" filter="url(#panelShadow)"/>
  <rect x="688" y="132" width="500" height="238" rx="24" fill="#1e1e26" stroke="#383844" stroke-width="1.2" filter="url(#panelShadow)"/>
  <rect x="88" y="420" width="720" height="236" rx="24" fill="#1e1e26" stroke="#383844" stroke-width="1.2" filter="url(#panelShadow)"/>
  <rect x="888" y="420" width="330" height="236" rx="24" fill="#1e1e26" stroke="#383844" stroke-width="1.2" filter="url(#panelShadow)"/>

  <rect x="35" y="232" width="116" height="34" rx="17" fill="url(#tagGrad)" transform="rotate(-90 93 249)"/>
  <text x="64" y="254" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle" transform="rotate(-90 93 249)">Line Chart</text>
  <rect x="635" y="232" width="116" height="34" rx="17" fill="url(#tagGrad)" transform="rotate(-90 693 249)"/>
  <text x="664" y="254" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle" transform="rotate(-90 693 249)">Column</text>
  <rect x="35" y="520" width="116" height="34" rx="17" fill="url(#tagGrad)" transform="rotate(-90 93 537)"/>
  <text x="64" y="542" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle" transform="rotate(-90 93 537)">Bar Chart</text>
  <rect x="835" y="520" width="116" height="34" rx="17" fill="url(#tagGrad)" transform="rotate(-90 893 537)"/>
  <text x="864" y="542" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle" transform="rotate(-90 893 537)">Doughnut</text>

  <text x="130" y="166" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">ARR Momentum</text>
  <text x="130" y="190" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9698a3">Revenue, pipeline, and expansion index</text>
  <line x1="170" y1="330" x2="590" y2="330" stroke="#70717a" stroke-width="1"/>
  <line x1="170" y1="210" x2="170" y2="330" stroke="#70717a" stroke-width="1"/>
  <line x1="170" y1="300" x2="590" y2="300" stroke="#393a43" stroke-width="1"/>
  <line x1="170" y1="270" x2="590" y2="270" stroke="#393a43" stroke-width="1"/>
  <line x1="170" y1="240" x2="590" y2="240" stroke="#393a43" stroke-width="1"/>
  <line x1="275" y1="210" x2="275" y2="330" stroke="#31323a" stroke-width="1"/>
  <line x1="380" y1="210" x2="380" y2="330" stroke="#31323a" stroke-width="1"/>
  <line x1="485" y1="210" x2="485" y2="330" stroke="#31323a" stroke-width="1"/>
  <path d="M195 286 C250 250, 288 238, 330 276 S430 281, 565 230" fill="none" stroke="#ff007f" stroke-width="3" filter="url(#neonGlow)"/>
  <path d="M195 275 C275 280, 340 287, 405 260 S500 238, 565 218" fill="none" stroke="#00f0ff" stroke-width="3" filter="url(#neonGlow)"/>
  <path d="M195 298 C275 245, 345 205, 410 285 S505 310, 565 274" fill="none" stroke="#00ff88" stroke-width="3" filter="url(#neonGlow)"/>
  <text x="202" y="354" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2021</text>
  <text x="307" y="354" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2022</text>
  <text x="412" y="354" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2023</text>
  <text x="522" y="354" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2024</text>

  <text x="730" y="166" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Channel Mix</text>
  <text x="730" y="190" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9698a3">Paid, product-led, and partner contribution</text>
  <line x1="742" y1="330" x2="1150" y2="330" stroke="#70717a" stroke-width="1"/>
  <line x1="742" y1="210" x2="742" y2="330" stroke="#70717a" stroke-width="1"/>
  <line x1="742" y1="300" x2="1150" y2="300" stroke="#393a43" stroke-width="1"/>
  <line x1="742" y1="270" x2="1150" y2="270" stroke="#393a43" stroke-width="1"/>
  <line x1="742" y1="240" x2="1150" y2="240" stroke="#393a43" stroke-width="1"/>
  <rect x="772" y="242" width="23" height="88" rx="2" fill="url(#pinkBar)" filter="url(#neonGlow)"/>
  <rect x="803" y="275" width="23" height="55" rx="2" fill="url(#greenBar)"/>
  <rect x="834" y="287" width="23" height="43" rx="2" fill="url(#cyanBar)"/>
  <rect x="880" y="264" width="23" height="66" rx="2" fill="url(#pinkBar)" filter="url(#neonGlow)"/>
  <rect x="911" y="239" width="23" height="91" rx="2" fill="url(#greenBar)"/>
  <rect x="942" y="288" width="23" height="42" rx="2" fill="url(#cyanBar)"/>
  <rect x="987" y="259" width="23" height="71" rx="2" fill="url(#pinkBar)" filter="url(#neonGlow)"/>
  <rect x="1018" y="292" width="23" height="38" rx="2" fill="url(#greenBar)"/>
  <rect x="1049" y="275" width="23" height="55" rx="2" fill="url(#cyanBar)"/>
  <rect x="1092" y="237" width="23" height="93" rx="2" fill="url(#pinkBar)" filter="url(#neonGlow)"/>
  <rect x="1123" y="268" width="23" height="62" rx="2" fill="url(#greenBar)"/>
  <text x="785" y="354" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2021</text>
  <text x="893" y="354" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2022</text>
  <text x="1000" y="354" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2023</text>
  <text x="1103" y="354" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#c7c8cf">2024</text>

  <text x="130" y="454" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Segment Penetration</text>
  <line x1="160" y1="620" x2="780" y2="620" stroke="#70717a" stroke-width="1"/>
  <line x1="160" y1="478" x2="160" y2="620" stroke="#70717a" stroke-width="1"/>
  <line x1="315" y1="478" x2="315" y2="620" stroke="#31323a" stroke-width="1"/>
  <line x1="470" y1="478" x2="470" y2="620" stroke="#31323a" stroke-width="1"/>
  <line x1="625" y1="478" x2="625" y2="620" stroke="#31323a" stroke-width="1"/>
  <rect x="170" y="494" width="230" height="18" rx="2" fill="url(#cyanBar)"/>
  <rect x="400" y="494" width="118" height="18" rx="2" fill="url(#greenBar)"/>
  <rect x="518" y="494" width="210" height="18" rx="2" fill="url(#pinkBar)" filter="url(#neonGlow)"/>
  <rect x="170" y="542" width="185" height="18" rx="2" fill="url(#cyanBar)"/>
  <rect x="355" y="542" width="120" height="18" rx="2" fill="url(#greenBar)"/>
  <rect x="475" y="542" width="128" height="18" rx="2" fill="url(#pinkBar)"/>
  <rect x="170" y="590" width="260" height="18" rx="2" fill="url(#cyanBar)"/>
  <rect x="430" y="590" width="150" height="18" rx="2" fill="url(#greenBar)"/>
  <rect x="580" y="590" width="166" height="18" rx="2" fill="url(#pinkBar)" filter="url(#neonGlow)"/>
  <text x="120" y="508" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">2024</text>
  <text x="120" y="556" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">2023</text>
  <text x="120" y="604" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">2022</text>

  <text x="928" y="454" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Retention Loop</text>
  <circle cx="1054" cy="546" r="76" fill="none" stroke="#2c2d35" stroke-width="54"/>
  <path d="M1086 479 A75 75 0 1 1 1013 609" fill="none" stroke="#ff007f" stroke-width="54" filter="url(#neonGlow)"/>
  <path d="M1013 609 A75 75 0 0 1 980 528" fill="none" stroke="#1ea7ff" stroke-width="54" filter="url(#neonGlow)"/>
  <path d="M980 528 A75 75 0 0 1 1018 483" fill="none" stroke="#44d99d" stroke-width="54"/>
  <path d="M1018 483 A75 75 0 0 1 1086 479" fill="none" stroke="#ff7a32" stroke-width="54"/>
  <circle cx="1054" cy="546" r="46" fill="#1e1e26"/>
  <text x="1014" y="552" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#ffffff" text-anchor="middle">68%</text>
  <text x="954" y="640" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ff2f8f">■ 2021</text>
  <text x="1010" y="640" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#1ea7ff">■ 2022</text>
  <text x="1066" y="640" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#44d99d">■ 2023</text>
  <text x="1122" y="640" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ff7a32">■ 2024</text>
</svg>
```

## Avoid in this skill
- ❌ Native PowerPoint chart objects if exact neo-dark styling is required; manually draw chart marks as editable SVG shapes instead
- ❌ Filters on `<line>` gridlines; use glow only on `<path>`, `<rect>`, `<circle>`, `<ellipse>`, or `<text>`
- ❌ `marker-end` arrowheads for callouts or trend arrows; use plain `<line>` or draw arrowheads as separate `<path>` triangles
- ❌ `<mask>` or clip-path effects on non-image elements for glowing chart cutouts; they will not translate reliably
- ❌ Overcrowded axis labels; the style depends on dark negative space and selective neon emphasis

## Composition notes
- Keep the background almost black and let the panels occupy roughly 75–82% of the slide, leaving a visible dark margin around the dashboard.
- Use the rotated gradient tags as the visual signature: place them slightly outside the left edge of each widget so the grid feels custom rather than templated.
- Neon colors should be reserved for data marks, not panel backgrounds; the panels stay muted charcoal with subtle strokes and shadows.
- Balance one large analytic panel with two smaller panels and one circular summary chart to create an executive “command center” rhythm.