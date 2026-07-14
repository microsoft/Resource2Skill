# SVG Recipe — Dark Neon Dashboard Visualization

## Visual mechanism
A premium dark-mode analytics interface built from floating rounded cards, faint UI borders, and neon chart marks that glow against a charcoal/navy background. Each widget is encapsulated like a software dashboard module, with bright overlapping pill labels and simplified chart geometry drawn directly as editable SVG shapes.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep charcoal background
- 4× large rounded `<rect>` for dashboard widget cards
- 4× small rounded `<rect>` for vivid pill-shaped widget tags
- Multiple thin `<line>` elements for subdued chart gridlines and axes
- Multiple `<path>` elements for neon line charts, area fills, donut arcs, and decorative UI strokes
- Multiple `<rect>` elements for neon bar charts and metric blocks
- Multiple `<circle>` elements for line-chart data points and status dots
- Multiple `<text>` elements with explicit `width` for titles, metric labels, axes, and KPI values
- 2× `<linearGradient>` for background/card depth and area-chart fills
- 1× `<radialGradient>` for subtle ambient neon glow
- 2× `<filter>` definitions using blur/shadow for soft card elevation and neon strokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#10131b"/>
      <stop offset="55%" stop-color="#14161c"/>
      <stop offset="100%" stop-color="#090b10"/>
    </linearGradient>
    <linearGradient id="areaCyan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00dcff" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#00dcff" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#ff287f"/>
      <stop offset="100%" stop-color="#b4ff32"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#18334a" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#10131b" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neonGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="650" cy="360" rx="580" ry="310" fill="url(#ambientGlow)" opacity="0.55"/>

  <text x="54" y="58" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">Dark Neon Dashboard</text>
  <text x="56" y="88" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8f96a3">LIVE REVENUE INTELLIGENCE · Q4 PERFORMANCE GRID</text>
  <circle cx="1136" cy="58" r="5" fill="#b4ff32" filter="url(#neonGlow)"/>
  <text x="1150" y="63" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#c7ccd6">ONLINE</text>

  <rect x="54" y="118" width="560" height="250" rx="24" fill="#1e2026" stroke="#343943" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="42" y="142" width="132" height="32" rx="16" fill="#dc3c28"/>
  <text x="68" y="164" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">TRAFFIC</text>
  <text x="90" y="212" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff">2.84M</text>
  <text x="92" y="236" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#969ca8">monthly sessions</text>
  <line x1="306" y1="174" x2="570" y2="174" stroke="#333943" stroke-width="1"/>
  <line x1="306" y1="218" x2="570" y2="218" stroke="#333943" stroke-width="1"/>
  <line x1="306" y1="262" x2="570" y2="262" stroke="#333943" stroke-width="1"/>
  <line x1="306" y1="306" x2="570" y2="306" stroke="#333943" stroke-width="1"/>
  <path d="M306 322 L306 280 C338 252 356 260 380 236 C410 204 435 218 462 190 C492 158 520 180 570 146 L570 322 Z" fill="url(#areaCyan)"/>
  <path d="M306 280 C338 252 356 260 380 236 C410 204 435 218 462 190 C492 158 520 180 570 146" fill="none" stroke="#00dcff" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>
  <circle cx="380" cy="236" r="5" fill="#00dcff"/>
  <circle cx="462" cy="190" r="5" fill="#00dcff"/>
  <circle cx="570" cy="146" r="5" fill="#00dcff"/>

  <rect x="666" y="118" width="560" height="250" rx="24" fill="#1e2026" stroke="#343943" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="654" y="142" width="132" height="32" rx="16" fill="#dc3c28"/>
  <text x="682" y="164" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">REVENUE</text>
  <text x="704" y="214" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff">$9.6M</text>
  <text x="706" y="238" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#969ca8">net recurring revenue</text>
  <line x1="922" y1="174" x2="1178" y2="174" stroke="#333943" stroke-width="1"/>
  <line x1="922" y1="218" x2="1178" y2="218" stroke="#333943" stroke-width="1"/>
  <line x1="922" y1="262" x2="1178" y2="262" stroke="#333943" stroke-width="1"/>
  <line x1="922" y1="306" x2="1178" y2="306" stroke="#333943" stroke-width="1"/>
  <rect x="936" y="260" width="26" height="62" rx="8" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <rect x="978" y="226" width="26" height="96" rx="8" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <rect x="1020" y="246" width="26" height="76" rx="8" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <rect x="1062" y="194" width="26" height="128" rx="8" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <rect x="1104" y="214" width="26" height="108" rx="8" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <rect x="1146" y="166" width="26" height="156" rx="8" fill="url(#barGrad)" filter="url(#neonGlow)"/>
  <text x="934" y="342" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#9097a4">JUL</text>
  <text x="1102" y="342" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#9097a4">NOV</text>

  <rect x="54" y="410" width="560" height="250" rx="24" fill="#1e2026" stroke="#343943" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="42" y="434" width="132" height="32" rx="16" fill="#dc3c28"/>
  <text x="76" y="456" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">FUNNEL</text>
  <path d="M137 510 A74 74 0 1 1 136.9 510" fill="none" stroke="#343943" stroke-width="22"/>
  <path d="M137 510 A74 74 0 1 1 196 628" fill="none" stroke="#ff2882" stroke-width="22" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M137 510 A74 74 0 0 1 203 544" fill="none" stroke="#00dcff" stroke-width="22" stroke-linecap="round" filter="url(#neonGlow)"/>
  <text x="108" y="560" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff">74%</text>
  <text x="104" y="584" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#969ca8">conversion</text>
  <rect x="302" y="492" width="240" height="18" rx="9" fill="#343943"/>
  <rect x="302" y="492" width="196" height="18" rx="9" fill="#ff2882" filter="url(#neonGlow)"/>
  <rect x="302" y="540" width="240" height="18" rx="9" fill="#343943"/>
  <rect x="302" y="540" width="152" height="18" rx="9" fill="#00dcff" filter="url(#neonGlow)"/>
  <rect x="302" y="588" width="240" height="18" rx="9" fill="#343943"/>
  <rect x="302" y="588" width="118" height="18" rx="9" fill="#b4ff32" filter="url(#neonGlow)"/>
  <text x="302" y="482" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfd3dc">Lead quality</text>
  <text x="302" y="530" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfd3dc">Activation</text>
  <text x="302" y="578" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cfd3dc">Retention</text>

  <rect x="666" y="410" width="560" height="250" rx="24" fill="#1e2026" stroke="#343943" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="654" y="434" width="132" height="32" rx="16" fill="#dc3c28"/>
  <text x="690" y="456" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">LATENCY</text>
  <text x="708" y="515" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff">38ms</text>
  <text x="710" y="540" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#969ca8">p95 response time</text>
  <line x1="924" y1="486" x2="1180" y2="486" stroke="#333943" stroke-width="1"/>
  <line x1="924" y1="530" x2="1180" y2="530" stroke="#333943" stroke-width="1"/>
  <line x1="924" y1="574" x2="1180" y2="574" stroke="#333943" stroke-width="1"/>
  <path d="M924 594 C954 548 982 604 1014 548 C1048 490 1070 560 1100 520 C1134 474 1154 506 1180 462" fill="none" stroke="#b4ff32" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M924 570 C954 584 982 528 1014 560 C1048 598 1070 506 1100 548 C1134 580 1154 486 1180 520" fill="none" stroke="#9650ff" stroke-width="3" stroke-linecap="round" opacity="0.9" filter="url(#neonGlow)"/>
  <circle cx="1180" cy="462" r="6" fill="#b4ff32"/>
  <circle cx="1180" cy="520" r="5" fill="#9650ff"/>
  <text x="934" y="626" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#9097a4">00:00</text>
  <text x="1112" y="626" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#9097a4">23:59</text>
</svg>
```

## Avoid in this skill
- ❌ Using native SVG `<mask>` or `mask="url(...)"` for glow cutouts; use gradients and editable shapes instead.
- ❌ Applying filters to `<line>` gridlines; keep gridlines flat and apply glow only to `<path>`, `<rect>`, `<circle>`, or `<text>`.
- ❌ Relying on real PowerPoint chart objects if editability of every visual mark is required; draw charts as SVG paths, rects, circles, and text.
- ❌ Overloading the dashboard with legends and axis labels; the dark neon style works best with minimal UI labels and strong color coding.

## Composition notes
- Use a strict 2×2 or 3×2 card grid with consistent gutters; the precision of the layout is what makes it feel like premium software.
- Keep the slide background very dark and push borders/gridlines into low-contrast blue-gray so neon cyan, pink, lime, and purple become the visual hierarchy.
- Let pill tags overlap the card edge slightly; this creates a layered interface feel without adding clutter.
- Reserve about 25–35% of each card for large KPI typography and the rest for simplified chart geometry.