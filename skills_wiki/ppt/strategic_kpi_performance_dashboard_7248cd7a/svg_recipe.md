# SVG Recipe — Strategic KPI Performance Dashboard

## Visual mechanism
A premium KPI dashboard is built as a disciplined, full-width executive table with merged burgundy header bands, zebra-striped rows, right-aligned numeric columns, and color-coded variance arrows. The slide separates MTD and YTD performance into clear column groups so leaders can scan short-term and cumulative performance in one view.

## SVG primitives needed
- 1× `<rect>` for the soft off-white slide background
- 1× `<rect>` with gradient fill and shadow for the main title banner
- 1× `<rect>` for the month selector pill
- 1× `<rect>` with shadow for the table card background
- 3× `<rect>` for merged table header bands: KPI identity, MTD, and YTD/status
- 4× `<rect>` for zebra-striped data rows
- 8× narrow `<rect>` accents for row category color bars
- 8× rounded `<rect>` status pills for “Ahead / On Track / Watch”
- 2× `<path>` strokes for table grid lines
- 16× small `<path>` triangles for green/red variance arrows
- Multiple `<text>` elements with `width=` for title, headers, column labels, row labels, numbers, variance values, status labels, legend, and footnote
- 1× `<linearGradient>` for the title banner
- 1× `<linearGradient>` for the subtle slide background
- 1× `<filter id="cardShadow">` applied to header/table cards
- 1× `<filter id="softGlow">` applied to the selected month pill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#fbf8f7"/>
      <stop offset="1" stop-color="#eee9e8"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="48" y1="38" x2="1232" y2="94">
      <stop offset="0" stop-color="#4f2528"/>
      <stop offset="0.55" stop-color="#743c3d"/>
      <stop offset="1" stop-color="#9b5a5a"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="48" y="34" width="1184" height="62" rx="12" fill="url(#headerGrad)" filter="url(#cardShadow)"/>
  <text x="640" y="73" width="900" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#ffffff">Recycling Infrastructure KPI Dashboard — 2025</text>
  <rect x="936" y="48" width="250" height="34" rx="17" fill="#ffffff" opacity="0.16" filter="url(#softGlow)"/>
  <text x="958" y="70" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#ffffff">Select Month:  March 2025</text>

  <rect x="48" y="118" width="1184" height="520" rx="14" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="48" y="118" width="496" height="42" rx="14" fill="#623030"/>
  <rect x="544" y="118" width="312" height="42" fill="#945858"/>
  <rect x="856" y="118" width="376" height="42" rx="14" fill="#945858"/>
  <rect x="48" y="160" width="1184" height="44" fill="#c59696"/>

  <text x="296" y="145" width="480" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">KPI CATALOG</text>
  <text x="700" y="145" width="300" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">MONTH-TO-DATE PERFORMANCE</text>
  <text x="1044" y="145" width="350" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">YEAR-TO-DATE PERFORMANCE</text>

  <text x="69" y="187" width="38" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">#</text>
  <text x="149" y="187" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Area</text>
  <text x="318" y="187" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">KPI</text>
  <text x="457" y="187" width="55" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Unit</text>
  <text x="515" y="187" width="55" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Goal</text>
  <text x="583" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Actual</text>
  <text x="661" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Target</text>
  <text x="739" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">PY</text>
  <text x="817" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Var.</text>
  <text x="895" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Actual</text>
  <text x="973" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Target</text>
  <text x="1051" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">PY</text>
  <text x="1129" y="187" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Var.</text>
  <text x="1200" y="187" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Status</text>

  <rect x="48" y="258" width="1184" height="54" fill="#f4f1f1"/>
  <rect x="48" y="366" width="1184" height="54" fill="#f4f1f1"/>
  <rect x="48" y="474" width="1184" height="54" fill="#f4f1f1"/>
  <rect x="48" y="582" width="1184" height="54" fill="#f4f1f1"/>
  <rect x="48" y="204" width="6" height="54" fill="#5b8def"/>
  <rect x="48" y="258" width="6" height="54" fill="#5b8def"/>
  <rect x="48" y="312" width="6" height="54" fill="#8bc34a"/>
  <rect x="48" y="366" width="6" height="54" fill="#f06292"/>
  <rect x="48" y="420" width="6" height="54" fill="#ffb74d"/>
  <rect x="48" y="474" width="6" height="54" fill="#ffb74d"/>
  <rect x="48" y="528" width="6" height="54" fill="#5b8def"/>
  <rect x="48" y="582" width="6" height="54" fill="#8bc34a"/>

  <path d="M90 118V638 M208 118V638 M428 118V638 M486 118V638 M544 118V638 M622 160V638 M700 160V638 M778 160V638 M856 118V638 M934 160V638 M1012 160V638 M1090 160V638 M1168 118V638" stroke="#d8c9c9" stroke-width="1"/>
  <path d="M48 160H1232 M48 204H1232 M48 258H1232 M48 312H1232 M48 366H1232 M48 420H1232 M48 474H1232 M48 528H1232 M48 582H1232 M48 638H1232" stroke="#d8c9c9" stroke-width="1"/>

  <text x="70" y="237" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222"><tspan x="70">1</tspan><tspan x="70" dy="54">2</tspan><tspan x="70" dy="54">3</tspan><tspan x="70" dy="54">4</tspan><tspan x="70" dy="54">5</tspan><tspan x="70" dy="54">6</tspan><tspan x="70" dy="54">7</tspan><tspan x="70" dy="54">8</tspan></text>
  <text x="104" y="237" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#333"><tspan x="104">Operations</tspan><tspan x="104" dy="54">Collection</tspan><tspan x="104" dy="54">Quality</tspan><tspan x="104" dy="54">Safety</tspan><tspan x="104" dy="54">Finance</tspan><tspan x="104" dy="54">Finance</tspan><tspan x="104" dy="54">Fleet</tspan><tspan x="104" dy="54">Partners</tspan></text>
  <text x="222" y="237" width="195" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111"><tspan x="222">Recycling Rate</tspan><tspan x="222" dy="54">Material Collected</tspan><tspan x="222" dy="54">Material Contamination</tspan><tspan x="222" dy="54">Safety Incidents</tspan><tspan x="222" dy="54">Revenue per Ton</tspan><tspan x="222" dy="54">Processing Cost</tspan><tspan x="222" dy="54">Truck Uptime</tspan><tspan x="222" dy="54">Partner SLA</tspan></text>
  <text x="457" y="237" width="54" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#444"><tspan x="457">%</tspan><tspan x="457" dy="54">Tons</tspan><tspan x="457" dy="54">%</tspan><tspan x="457" dy="54">Count</tspan><tspan x="457" dy="54">USD</tspan><tspan x="457" dy="54">USD</tspan><tspan x="457" dy="54">%</tspan><tspan x="457" dy="54">%</tspan></text>
  <text x="515" y="237" width="54" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#444"><tspan x="515">UTB</tspan><tspan x="515" dy="54">UTB</tspan><tspan x="515" dy="54">LTB</tspan><tspan x="515" dy="54">LTB</tspan><tspan x="515" dy="54">UTB</tspan><tspan x="515" dy="54">LTB</tspan><tspan x="515" dy="54">UTB</tspan><tspan x="515" dy="54">UTB</tspan></text>

  <text x="610" y="237" width="64" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111"><tspan x="610">125.0</tspan><tspan x="610" dy="54">98.0</tspan><tspan x="610" dy="54">8.8</tspan><tspan x="610" dy="54">1</tspan><tspan x="610" dy="54">127.6</tspan><tspan x="610" dy="54">41.2</tspan><tspan x="610" dy="54">92.4</tspan><tspan x="610" dy="54">97.8</tspan></text>
  <text x="688" y="237" width="64" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555"><tspan x="688">120.0</tspan><tspan x="688" dy="54">105.0</tspan><tspan x="688" dy="54">9.0</tspan><tspan x="688" dy="54">0</tspan><tspan x="688" dy="54">125.0</tspan><tspan x="688" dy="54">43.0</tspan><tspan x="688" dy="54">95.0</tspan><tspan x="688" dy="54">96.0</tspan></text>
  <text x="766" y="237" width="64" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777"><tspan x="766">118.0</tspan><tspan x="766" dy="54">95.0</tspan><tspan x="766" dy="54">9.2</tspan><tspan x="766" dy="54">2</tspan><tspan x="766" dy="54">122.0</tspan><tspan x="766" dy="54">44.0</tspan><tspan x="766" dy="54">91.0</tspan><tspan x="766" dy="54">94.0</tspan></text>
  <text x="842" y="237" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333"><tspan x="842">4.2%</tspan><tspan x="842" dy="54">6.7%</tspan><tspan x="842" dy="54">2.2%</tspan><tspan x="842" dy="54">1.0</tspan><tspan x="842" dy="54">2.1%</tspan><tspan x="842" dy="54">4.2%</tspan><tspan x="842" dy="54">2.7%</tspan><tspan x="842" dy="54">1.9%</tspan></text>

  <text x="922" y="237" width="64" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111"><tspan x="922">366.0</tspan><tspan x="922" dy="54">290.0</tspan><tspan x="922" dy="54">26.0</tspan><tspan x="922" dy="54">3</tspan><tspan x="922" dy="54">380.0</tspan><tspan x="922" dy="54">124.8</tspan><tspan x="922" dy="54">276.2</tspan><tspan x="922" dy="54">96.5</tspan></text>
  <text x="1000" y="237" width="64" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555"><tspan x="1000">375.0</tspan><tspan x="1000" dy="54">310.0</tspan><tspan x="1000" dy="54">27.0</tspan><tspan x="1000" dy="54">2</tspan><tspan x="1000" dy="54">370.0</tspan><tspan x="1000" dy="54">129.0</tspan><tspan x="1000" dy="54">285.0</tspan><tspan x="1000" dy="54">95.0</tspan></text>
  <text x="1078" y="237" width="64" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777"><tspan x="1078">350.0</tspan><tspan x="1078" dy="54">285.0</tspan><tspan x="1078" dy="54">28.0</tspan><tspan x="1078" dy="54">5</tspan><tspan x="1078" dy="54">360.0</tspan><tspan x="1078" dy="54">133.0</tspan><tspan x="1078" dy="54">272.0</tspan><tspan x="1078" dy="54">92.0</tspan></text>
  <text x="1154" y="237" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#333"><tspan x="1154">2.4%</tspan><tspan x="1154" dy="54">6.5%</tspan><tspan x="1154" dy="54">3.7%</tspan><tspan x="1154" dy="54">1.0</tspan><tspan x="1154" dy="54">2.7%</tspan><tspan x="1154" dy="54">3.3%</tspan><tspan x="1154" dy="54">3.1%</tspan><tspan x="1154" dy="54">1.6%</tspan></text>

  <path d="M790 235 L798 221 L806 235 Z" fill="#00a651"/><path d="M790 275 L806 275 L798 289 Z" fill="#e53935"/><path d="M790 343 L798 329 L806 343 Z" fill="#00a651"/><path d="M790 383 L806 383 L798 397 Z" fill="#e53935"/>
  <path d="M790 451 L798 437 L806 451 Z" fill="#00a651"/><path d="M790 505 L798 491 L806 505 Z" fill="#00a651"/><path d="M790 545 L806 545 L798 559 Z" fill="#e53935"/><path d="M790 613 L798 599 L806 613 Z" fill="#00a651"/>
  <path d="M1102 235 L1118 235 L1110 249 Z" fill="#e53935"/><path d="M1102 289 L1118 289 L1110 303 Z" fill="#e53935"/><path d="M1102 343 L1110 329 L1118 343 Z" fill="#00a651"/><path d="M1102 383 L1118 383 L1110 397 Z" fill="#e53935"/>
  <path d="M1102 451 L1110 437 L1118 451 Z" fill="#00a651"/><path d="M1102 505 L1110 491 L1118 505 Z" fill="#00a651"/><path d="M1102 545 L1118 545 L1110 559 Z" fill="#e53935"/><path d="M1102 613 L1110 599 L1118 613 Z" fill="#00a651"/>

  <rect x="1177" y="219" width="46" height="24" rx="12" fill="#fff1d6"/><text x="1200" y="236" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#9b6200">WATCH</text>
  <rect x="1177" y="273" width="46" height="24" rx="12" fill="#fff1d6"/><text x="1200" y="290" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#9b6200">WATCH</text>
  <rect x="1177" y="327" width="46" height="24" rx="12" fill="#dff5e7"/><text x="1200" y="344" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#087a36">TRACK</text>
  <rect x="1177" y="381" width="46" height="24" rx="12" fill="#fff1d6"/><text x="1200" y="398" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#9b6200">WATCH</text>
  <rect x="1177" y="435" width="46" height="24" rx="12" fill="#dff5e7"/><text x="1200" y="452" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#087a36">AHEAD</text>
  <rect x="1177" y="489" width="46" height="24" rx="12" fill="#dff5e7"/><text x="1200" y="506" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#087a36">AHEAD</text>
  <rect x="1177" y="543" width="46" height="24" rx="12" fill="#fff1d6"/><text x="1200" y="560" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#9b6200">WATCH</text>
  <rect x="1177" y="597" width="46" height="24" rx="12" fill="#dff5e7"/><text x="1200" y="614" width="46" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#087a36">AHEAD</text>

  <circle cx="62" cy="674" r="5" fill="#00a651"/><text x="76" y="679" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555">Green arrow = favorable variance vs target</text>
  <circle cx="358" cy="674" r="5" fill="#e53935"/><text x="372" y="679" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555">Red arrow = unfavorable variance</text>
  <text x="1232" y="679" width="460" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777">Source: Corporate KPI cube • Snapshot generated for March MBR</text>
</svg>
```

## Avoid in this skill
- ❌ Building the dashboard as one screenshot image; use editable SVG shapes and text so PowerPoint users can update values.
- ❌ Using `<foreignObject>` for HTML tables; it will hard-fail and will not translate into editable PowerPoint shapes.
- ❌ Using `<pattern>` fills for row striping; create explicit zebra `<rect>` rows instead.
- ❌ Putting arrowheads on paths with `marker-end`; use small triangle `<path>` shapes or Unicode arrows in `<text>`.
- ❌ Applying filters to `<line>` elements for grid shadows; keep grid lines flat and apply shadows only to card/header rectangles.
- ❌ Omitting `width=` on `<text>` elements; dashboard text will overflow unpredictably in PowerPoint.

## Composition notes
- Keep the table card dominant, occupying roughly 85–90% of slide width; dashboards need density but should still breathe around the edges.
- Use a dark executive header band for authority, then lighter burgundy bands for section hierarchy and neutral body rows for readability.
- Align all numbers to the right, row labels to the left, and section headers to the center; this creates a spreadsheet-like scan path without looking like a raw spreadsheet.
- Use only two strong signal colors for variance—green and red—so conditional formatting remains instantly legible.