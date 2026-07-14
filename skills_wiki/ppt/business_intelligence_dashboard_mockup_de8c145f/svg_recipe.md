# SVG Recipe — Business Intelligence Dashboard Mockup

## Visual mechanism
A polished BI dashboard is created by combining a strict modular grid, elevated white cards, KPI tiles, and several miniature chart types into one executive-summary surface. The visual credibility comes from consistent typography, muted app-like chrome, subtle shadows, and a repeated analytical color palette across all visualizations.

## SVG primitives needed
- 1× `<rect>` for the slide background.
- 1× `<rect>` for the dark vertical navigation rail.
- 8–12× `<rect>` for dashboard cards, KPI cards, chart containers, pills, bars, and heatmap cells.
- 8–12× `<circle>` for KPI icons, chart markers, donut center, and navigation dots.
- 2–4× `<ellipse>` for soft decorative glows or map markers.
- 15–25× `<line>` for chart axes, gridlines, tick marks, and small divider rules.
- 8–14× `<path>` for sparklines, trend lines, donut segments, map-like regional shapes, and decorative UI strokes.
- Many `<text>` elements with explicit `width` attributes for title, KPIs, labels, legends, axis values, and annotations.
- 1× `<linearGradient>` for the navigation rail or premium header accents.
- 1× `<radialGradient>` for subtle background glow.
- 1× `<filter id="shadow">` using `feOffset + feGaussianBlur + feMerge`, applied directly to card `<rect>` elements.
- Optional 1× `<filter id="lineGlow">` using `feGaussianBlur`, applied to a highlight `<path>` trend line.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#17213a"/>
      <stop offset="100%" stop-color="#0b1020"/>
    </linearGradient>
    <radialGradient id="bgGlow" cx="70%" cy="10%" r="70%">
      <stop offset="0%" stop-color="#eaf0ff"/>
      <stop offset="100%" stop-color="#f4f6fa"/>
    </radialGradient>
    <filter id="shadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="lineGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="2.5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <rect x="0" y="0" width="88" height="720" fill="url(#navGrad)"/>
  <circle cx="44" cy="48" r="18" fill="#3962ac"/>
  <text x="31" y="56" width="30" font-family="Segoe UI" font-size="20" font-weight="700" fill="#ffffff">BI</text>
  <circle cx="44" cy="136" r="5" fill="#ffffff"/>
  <circle cx="44" cy="184" r="5" fill="#6f7fa6"/>
  <circle cx="44" cy="232" r="5" fill="#6f7fa6"/>
  <circle cx="44" cy="280" r="5" fill="#6f7fa6"/>
  <rect x="25" y="610" width="38" height="38" rx="12" fill="#222d4b"/>
  <text x="35" y="635" width="20" font-family="Segoe UI" font-size="15" font-weight="700" fill="#9fb0dc">?</text>

  <text x="116" y="48" width="460" font-family="Segoe UI" font-size="30" font-weight="700" fill="#202636">Revenue Performance Dashboard</text>
  <text x="116" y="76" width="520" font-family="Segoe UI" font-size="13" fill="#788092">Executive snapshot · FY2026 Q2 · Global commercial operations</text>
  <rect x="1006" y="36" width="106" height="32" rx="16" fill="#ffffff" stroke="#dfe4ef"/>
  <text x="1026" y="57" width="70" font-family="Segoe UI" font-size="12" font-weight="600" fill="#3962ac">Live view</text>
  <rect x="1126" y="36" width="114" height="32" rx="16" fill="#202636"/>
  <text x="1148" y="57" width="76" font-family="Segoe UI" font-size="12" font-weight="600" fill="#ffffff">Export PPT</text>

  <rect x="116" y="102" width="244" height="88" rx="18" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <circle cx="147" cy="132" r="15" fill="#e8eefb"/><path d="M140 134 L146 128 L151 132 L157 123" fill="none" stroke="#3962ac" stroke-width="3"/>
  <text x="178" y="138" width="145" font-family="Segoe UI" font-size="28" font-weight="700" fill="#202636">$42.8M</text>
  <text x="178" y="164" width="120" font-family="Segoe UI" font-size="12" fill="#788092">Net revenue</text>
  <text x="306" y="164" width="42" font-family="Segoe UI" font-size="12" font-weight="700" fill="#73b262">▲ 8.4%</text>

  <rect x="386" y="102" width="244" height="88" rx="18" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <circle cx="417" cy="132" r="15" fill="#edf7eb"/><path d="M410 132 C414 124 424 124 428 132 C424 141 414 141 410 132Z" fill="#73b262"/>
  <text x="448" y="138" width="145" font-family="Segoe UI" font-size="28" font-weight="700" fill="#202636">31.6%</text>
  <text x="448" y="164" width="125" font-family="Segoe UI" font-size="12" fill="#788092">Gross margin</text>
  <text x="576" y="164" width="42" font-family="Segoe UI" font-size="12" font-weight="700" fill="#73b262">▲ 2.1</text>

  <rect x="656" y="102" width="244" height="88" rx="18" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <circle cx="687" cy="132" r="15" fill="#fff3da"/><path d="M681 139 L687 123 L693 139 Z" fill="#f7b648"/>
  <text x="718" y="138" width="145" font-family="Segoe UI" font-size="28" font-weight="700" fill="#202636">18.2K</text>
  <text x="718" y="164" width="130" font-family="Segoe UI" font-size="12" fill="#788092">New customers</text>
  <text x="846" y="164" width="42" font-family="Segoe UI" font-size="12" font-weight="700" fill="#ec7067">▼ 1.3%</text>

  <rect x="926" y="102" width="244" height="88" rx="18" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <circle cx="957" cy="132" r="15" fill="#f0ebf7"/><path d="M950 139 C954 127 961 127 965 139" fill="none" stroke="#7c52a1" stroke-width="4"/>
  <text x="988" y="138" width="145" font-family="Segoe UI" font-size="28" font-weight="700" fill="#202636">94.7%</text>
  <text x="988" y="164" width="130" font-family="Segoe UI" font-size="12" fill="#788092">SLA attainment</text>
  <text x="1116" y="164" width="42" font-family="Segoe UI" font-size="12" font-weight="700" fill="#73b262">▲ 0.9</text>

  <rect x="116" y="218" width="520" height="260" rx="20" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <text x="140" y="250" width="250" font-family="Segoe UI" font-size="15" font-weight="700" fill="#303747">Revenue trend by month</text>
  <text x="482" y="250" width="120" font-family="Segoe UI" font-size="11" fill="#788092">USD millions</text>
  <line x1="158" y1="425" x2="596" y2="425" stroke="#e7ebf3"/>
  <line x1="158" y1="378" x2="596" y2="378" stroke="#eef1f6"/>
  <line x1="158" y1="331" x2="596" y2="331" stroke="#eef1f6"/>
  <line x1="158" y1="284" x2="596" y2="284" stroke="#eef1f6"/>
  <path d="M166 405 C210 392 228 358 264 363 C302 368 316 314 356 326 C395 338 405 300 446 292 C492 283 516 315 590 270" fill="none" stroke="#3962ac" stroke-width="5" stroke-linecap="round" filter="url(#lineGlow)"/>
  <path d="M166 405 C210 392 228 358 264 363 C302 368 316 314 356 326 C395 338 405 300 446 292 C492 283 516 315 590 270" fill="none" stroke="#3962ac" stroke-width="3" stroke-linecap="round"/>
  <circle cx="166" cy="405" r="4" fill="#3962ac"/><circle cx="264" cy="363" r="4" fill="#3962ac"/><circle cx="356" cy="326" r="4" fill="#3962ac"/><circle cx="446" cy="292" r="4" fill="#3962ac"/><circle cx="590" cy="270" r="5" fill="#ffffff" stroke="#3962ac" stroke-width="3"/>
  <text x="158" y="450" width="36" font-family="Segoe UI" font-size="10" fill="#788092">Jan</text><text x="254" y="450" width="36" font-family="Segoe UI" font-size="10" fill="#788092">Mar</text><text x="346" y="450" width="36" font-family="Segoe UI" font-size="10" fill="#788092">May</text><text x="438" y="450" width="36" font-family="Segoe UI" font-size="10" fill="#788092">Jul</text><text x="578" y="450" width="36" font-family="Segoe UI" font-size="10" fill="#788092">Sep</text>

  <rect x="660" y="218" width="260" height="260" rx="20" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <text x="684" y="250" width="180" font-family="Segoe UI" font-size="15" font-weight="700" fill="#303747">Product mix</text>
  <path d="M790 298 A66 66 0 0 1 847 397 L812 378 A26 26 0 0 0 790 338 Z" fill="#3962ac"/>
  <path d="M847 397 A66 66 0 0 1 738 415 L769 388 A26 26 0 0 0 812 378 Z" fill="#73b262"/>
  <path d="M738 415 A66 66 0 0 1 719 316 L762 331 A26 26 0 0 0 769 388 Z" fill="#f7b648"/>
  <path d="M719 316 A66 66 0 0 1 790 298 L790 338 A26 26 0 0 0 762 331 Z" fill="#7c52a1"/>
  <circle cx="790" cy="364" r="31" fill="#ffffff"/>
  <text x="765" y="360" width="52" font-family="Segoe UI" font-size="18" font-weight="700" fill="#202636">100%</text>
  <text x="704" y="438" width="60" font-family="Segoe UI" font-size="11" fill="#3962ac">Core 42%</text>
  <text x="780" y="438" width="70" font-family="Segoe UI" font-size="11" fill="#73b262">Cloud 28%</text>
  <text x="704" y="458" width="70" font-family="Segoe UI" font-size="11" fill="#f7b648">Services 19%</text>
  <text x="800" y="458" width="70" font-family="Segoe UI" font-size="11" fill="#7c52a1">Other 11%</text>

  <rect x="944" y="218" width="296" height="260" rx="20" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <text x="968" y="250" width="180" font-family="Segoe UI" font-size="15" font-weight="700" fill="#303747">Regional performance</text>
  <path d="M1003 331 C1028 284 1086 282 1113 320 C1145 314 1177 336 1168 373 C1156 421 1095 428 1056 404 C1022 415 982 390 1003 331Z" fill="#e9eef8" stroke="#cfd8e8"/>
  <path d="M1035 338 C1053 312 1086 313 1100 339 C1080 354 1057 356 1035 338Z" fill="#3962ac" opacity="0.85"/>
  <path d="M1111 348 C1137 345 1154 360 1147 385 C1126 383 1113 369 1111 348Z" fill="#73b262" opacity="0.9"/>
  <path d="M1026 371 C1054 363 1077 375 1089 402 C1057 411 1034 399 1026 371Z" fill="#f7b648" opacity="0.9"/>
  <ellipse cx="1088" cy="352" rx="8" ry="8" fill="#ffffff" stroke="#202636" stroke-width="2"/>
  <text x="982" y="442" width="230" font-family="Segoe UI" font-size="11" fill="#788092">North America and EMEA drive 71% of quarterly pipeline.</text>

  <rect x="116" y="502" width="374" height="172" rx="20" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <text x="140" y="534" width="190" font-family="Segoe UI" font-size="15" font-weight="700" fill="#303747">Conversion funnel</text>
  <rect x="152" y="558" width="280" height="16" rx="8" fill="#3962ac"/><rect x="152" y="590" width="224" height="16" rx="8" fill="#73b262"/><rect x="152" y="622" width="168" height="16" rx="8" fill="#f7b648"/>
  <text x="442" y="572" width="38" font-family="Segoe UI" font-size="11" fill="#788092">100%</text><text x="386" y="604" width="38" font-family="Segoe UI" font-size="11" fill="#788092">80%</text><text x="330" y="636" width="38" font-family="Segoe UI" font-size="11" fill="#788092">60%</text>
  <text x="152" y="656" width="240" font-family="Segoe UI" font-size="11" fill="#788092">Lead → MQL → SQL progression</text>

  <rect x="514" y="502" width="374" height="172" rx="20" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <text x="538" y="534" width="210" font-family="Segoe UI" font-size="15" font-weight="700" fill="#303747">Pipeline by channel</text>
  <text x="538" y="575" width="65" font-family="Segoe UI" font-size="11" fill="#788092">Partner</text><rect x="608" y="562" width="220" height="14" rx="7" fill="#3962ac"/>
  <text x="538" y="607" width="65" font-family="Segoe UI" font-size="11" fill="#788092">Inbound</text><rect x="608" y="594" width="172" height="14" rx="7" fill="#73b262"/>
  <text x="538" y="639" width="65" font-family="Segoe UI" font-size="11" fill="#788092">Outbound</text><rect x="608" y="626" width="126" height="14" rx="7" fill="#f7b648"/>

  <rect x="912" y="502" width="328" height="172" rx="20" fill="#ffffff" stroke="#dfe4ef" filter="url(#shadow)"/>
  <text x="936" y="534" width="190" font-family="Segoe UI" font-size="15" font-weight="700" fill="#303747">Risk heatmap</text>
  <rect x="936" y="558" width="42" height="34" rx="8" fill="#edf7eb"/><rect x="986" y="558" width="42" height="34" rx="8" fill="#fff3da"/><rect x="1036" y="558" width="42" height="34" rx="8" fill="#fff3da"/><rect x="1086" y="558" width="42" height="34" rx="8" fill="#fde8e5"/>
  <rect x="936" y="600" width="42" height="34" rx="8" fill="#edf7eb"/><rect x="986" y="600" width="42" height="34" rx="8" fill="#edf7eb"/><rect x="1036" y="600" width="42" height="34" rx="8" fill="#fff3da"/><rect x="1086" y="600" width="42" height="34" rx="8" fill="#fde8e5"/>
  <text x="1144" y="578" width="74" font-family="Segoe UI" font-size="11" fill="#788092">High impact</text>
  <text x="1144" y="620" width="74" font-family="Segoe UI" font-size="11" fill="#788092">Medium</text>
  <text x="936" y="656" width="250" font-family="Segoe UI" font-size="11" fill="#788092">Primary exposure: enterprise renewal timing.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not flatten the entire dashboard as one screenshot; build charts and cards from editable SVG shapes.
- ❌ Do not use `<foreignObject>` for HTML tables or dashboard widgets; it will hard-fail translation.
- ❌ Do not use `<pattern>` fills for grids or chart backgrounds; use simple lines and light rectangles instead.
- ❌ Do not put `filter` on `<line>` elements for glowing chart axes; apply glow to a `<path>` trend line instead.
- ❌ Do not use `marker-end` on paths for arrows; if arrows are needed, use editable `<line>` elements and draw arrowheads manually with small paths.
- ❌ Do not omit `width` on any `<text>` element; dashboard labels are dense and need predictable PowerPoint text boxes.

## Composition notes
- Keep the title/header band shallow, then use a top KPI row and a two-level chart grid below it; this mirrors real BI tools and keeps scanning natural.
- Use white cards on a pale grey or blue-grey background, with 16–22 px rounded corners and subtle shadows to create an app-like surface.
- Repeat the same 4–5 data colors across all charts so the slide feels like one system rather than separate visuals.
- Reserve the largest card for the main trend line; supporting charts should be smaller and arranged as evidence around that primary narrative.