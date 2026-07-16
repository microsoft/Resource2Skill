# SVG Recipe — Modern Grid & Sidebar BI Dashboard

## Visual mechanism
A high-contrast KPI sidebar anchors the slide while the main canvas uses a strict modular grid of floating white data cards. Subtle shadows, muted BI colors, and miniature native-SVG chart constructions make the dashboard feel like a polished executive analytics screen while remaining editable in PowerPoint.

## SVG primitives needed
- 1× full-slide `<rect>` for the pale dashboard background
- 1× large `<rect>` for the dark vertical sidebar
- 6–8× rounded `<rect>` for floating white dashboard cards with shadows
- Multiple small `<rect>` elements for KPI pills, filter controls, bar charts, stacked bars, and heatmap cells
- Multiple `<line>` elements for chart axes, gridlines, and divider rules
- Multiple `<path>` elements for line charts, area fills, donut segments, stylized map regions, and decorative sidebar accents
- Multiple `<circle>` elements for line-chart data points, donut holes, status dots, and legend keys
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to card rectangles
- 1× `<filter id="softGlow">` using `feGaussianBlur` applied to decorative paths/circles
- 1× `<linearGradient>` for the sidebar depth treatment
- 1× `<radialGradient>` for a soft background glow
- Many `<text>` elements with explicit `width` attributes for dashboard title, KPI values, chart titles, labels, legends, and data annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sidebarGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0E2F21"/>
      <stop offset="100%" stop-color="#163626"/>
    </linearGradient>
    <radialGradient id="mintGlow" cx="78%" cy="12%" r="70%">
      <stop offset="0%" stop-color="#F9FFE8"/>
      <stop offset="58%" stop-color="#EBF1DE"/>
      <stop offset="100%" stop-color="#DDE8CD"/>
    </radialGradient>
    <filter id="cardShadow" x="-12%" y="-12%" width="124%" height="130%">
      <feOffset dx="0" dy="7" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .18 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#mintGlow)"/>
  <circle cx="1100" cy="84" r="160" fill="#FFFFFF" opacity="0.28" filter="url(#softGlow)"/>
  <rect x="0" y="0" width="282" height="720" fill="url(#sidebarGrad)"/>
  <path d="M0,560 C70,520 128,610 282,570 L282,720 L0,720 Z" fill="#0B2419" opacity="0.45"/>
  <path d="M236,0 C210,130 292,230 250,352 C229,414 217,492 282,596 L282,0 Z" fill="#F9C846" opacity="0.08"/>

  <text x="34" y="56" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">VIVO CALIF</text>
  <text x="34" y="82" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#B8C8BD">Executive performance dashboard</text>
  <line x1="34" y1="112" x2="244" y2="112" stroke="#355E47" stroke-width="1"/>

  <text x="34" y="146" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#F9C846" letter-spacing="1.6">TOTAL REVENUE</text>
  <text x="34" y="188" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#FFFFFF">$24.8M</text>
  <text x="34" y="211" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C7D7CB">+18.4% vs prior quarter</text>
  <path d="M36,234 C72,218 96,246 130,228 C162,211 187,220 230,196" fill="none" stroke="#F9C846" stroke-width="4" stroke-linecap="round"/>

  <rect x="34" y="270" width="210" height="72" rx="14" fill="#214E37"/>
  <text x="52" y="295" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#AFC1B5">ACTIVE ACCOUNTS</text>
  <text x="52" y="326" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">1,284</text>
  <circle cx="218" cy="306" r="12" fill="#70AD47"/>

  <rect x="34" y="362" width="210" height="72" rx="14" fill="#214E37"/>
  <text x="52" y="387" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#AFC1B5">CHURN RISK</text>
  <text x="52" y="418" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFC000">6.2%</text>
  <circle cx="218" cy="398" r="12" fill="#ED7D31"/>

  <text x="34" y="476" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#F9C846" letter-spacing="1.6">FILTERS</text>
  <rect x="34" y="494" width="210" height="36" rx="18" fill="#FFFFFF" opacity="0.12"/>
  <text x="52" y="517" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">Region: California</text>
  <rect x="34" y="542" width="210" height="36" rx="18" fill="#FFFFFF" opacity="0.12"/>
  <text x="52" y="565" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">Period: Q3 FY26</text>
  <rect x="34" y="590" width="210" height="36" rx="18" fill="#FFFFFF" opacity="0.12"/>
  <text x="52" y="613" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">Segment: Enterprise</text>

  <text x="314" y="48" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#25352B">Modern Grid & Sidebar BI Dashboard</text>
  <text x="314" y="74" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#667062">Revenue, pipeline, geography, and operational health</text>
  <text x="1092" y="54" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#667062">Last refresh</text>
  <text x="1092" y="74" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#25352B">Sep 30, 2026</text>

  <rect x="314" y="104" width="286" height="172" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="336" y="132" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Revenue trend</text>
  <line x1="340" y1="238" x2="570" y2="238" stroke="#E5E9E0" stroke-width="1"/>
  <line x1="340" y1="198" x2="570" y2="198" stroke="#E5E9E0" stroke-width="1"/>
  <line x1="340" y1="158" x2="570" y2="158" stroke="#E5E9E0" stroke-width="1"/>
  <path d="M342,232 L378,214 L414,220 L450,184 L486,190 L522,154 L568,140 L568,238 L342,238 Z" fill="#2F75B5" opacity="0.16"/>
  <path d="M342,232 C378,214 396,228 414,220 C440,207 440,190 450,184 C471,170 482,198 486,190 C504,162 528,154 568,140" fill="none" stroke="#2F75B5" stroke-width="4" stroke-linecap="round"/>
  <circle cx="450" cy="184" r="5" fill="#2F75B5"/><circle cx="568" cy="140" r="5" fill="#2F75B5"/>
  <text x="340" y="260" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">Jan  Feb  Mar  Apr  May  Jun</text>

  <rect x="620" y="104" width="286" height="172" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="642" y="132" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Channel mix</text>
  <line x1="650" y1="238" x2="872" y2="238" stroke="#E5E9E0" stroke-width="1"/>
  <rect x="660" y="176" width="28" height="62" rx="5" fill="#2F75B5"/><rect x="694" y="150" width="28" height="88" rx="5" fill="#ED7D31"/>
  <rect x="744" y="196" width="28" height="42" rx="5" fill="#2F75B5"/><rect x="778" y="166" width="28" height="72" rx="5" fill="#ED7D31"/>
  <rect x="828" y="138" width="28" height="100" rx="5" fill="#2F75B5"/><rect x="862" y="182" width="28" height="56" rx="5" fill="#ED7D31"/>
  <text x="660" y="260" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">Direct</text>
  <text x="744" y="260" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">Partner</text>
  <text x="828" y="260" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">Digital</text>

  <rect x="926" y="104" width="286" height="172" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="948" y="132" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Margin composition</text>
  <path d="M1036,154 A46,46 0 1,1 1005,234 L1036,200 Z" fill="#70AD47"/>
  <path d="M1005,234 A46,46 0 0,1 1074,169 L1036,200 Z" fill="#ED7D31"/>
  <path d="M1074,169 A46,46 0 0,1 1036,154 L1036,200 Z" fill="#2F75B5"/>
  <circle cx="1036" cy="200" r="25" fill="#FFFFFF"/>
  <text x="1015" y="205" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#404040">42%</text>
  <circle cx="1124" cy="164" r="5" fill="#70AD47"/><text x="1136" y="168" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Gross</text>
  <circle cx="1124" cy="190" r="5" fill="#ED7D31"/><text x="1136" y="194" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Sales</text>
  <circle cx="1124" cy="216" r="5" fill="#2F75B5"/><text x="1136" y="220" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Ops</text>

  <rect x="314" y="300" width="430" height="188" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="336" y="328" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Regional demand heatmap</text>
  <text x="338" y="358" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">North</text><text x="338" y="390" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">Bay</text><text x="338" y="422" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">LA</text><text x="338" y="454" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#808080">SD</text>
  <rect x="394" y="344" width="54" height="24" rx="5" fill="#DEEBF6"/><rect x="454" y="344" width="54" height="24" rx="5" fill="#9DC3E6"/><rect x="514" y="344" width="54" height="24" rx="5" fill="#5B9BD5"/><rect x="574" y="344" width="54" height="24" rx="5" fill="#ED7D31"/><rect x="634" y="344" width="54" height="24" rx="5" fill="#FF5757"/>
  <rect x="394" y="376" width="54" height="24" rx="5" fill="#9DC3E6"/><rect x="454" y="376" width="54" height="24" rx="5" fill="#DEEBF6"/><rect x="514" y="376" width="54" height="24" rx="5" fill="#ED7D31"/><rect x="574" y="376" width="54" height="24" rx="5" fill="#F4B183"/><rect x="634" y="376" width="54" height="24" rx="5" fill="#5B9BD5"/>
  <rect x="394" y="408" width="54" height="24" rx="5" fill="#FF5757"/><rect x="454" y="408" width="54" height="24" rx="5" fill="#ED7D31"/><rect x="514" y="408" width="54" height="24" rx="5" fill="#F4B183"/><rect x="574" y="408" width="54" height="24" rx="5" fill="#9DC3E6"/><rect x="634" y="408" width="54" height="24" rx="5" fill="#DEEBF6"/>
  <rect x="394" y="440" width="54" height="24" rx="5" fill="#5B9BD5"/><rect x="454" y="440" width="54" height="24" rx="5" fill="#9DC3E6"/><rect x="514" y="440" width="54" height="24" rx="5" fill="#DEEBF6"/><rect x="574" y="440" width="54" height="24" rx="5" fill="#F4B183"/><rect x="634" y="440" width="54" height="24" rx="5" fill="#ED7D31"/>

  <rect x="764" y="300" width="448" height="188" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="786" y="328" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">California opportunity map</text>
  <path d="M914,350 C936,335 954,348 948,371 C942,393 970,410 952,431 C936,451 941,472 916,476 C890,480 875,456 882,435 C890,410 865,393 878,372 C886,359 900,359 914,350 Z" fill="#F2F2F2" stroke="#D8D8D8"/>
  <path d="M903,366 C922,360 936,370 929,388 C914,392 901,383 903,366 Z" fill="#5B9BD5"/>
  <path d="M922,397 C943,398 954,416 940,431 C920,426 915,411 922,397 Z" fill="#ED7D31"/>
  <path d="M896,421 C916,426 920,450 902,462 C884,454 882,435 896,421 Z" fill="#2F75B5"/>
  <text x="1012" y="366" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#404040">Top counties</text>
  <rect x="1012" y="384" width="118" height="12" rx="6" fill="#2F75B5"/><text x="1138" y="395" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">LA</text>
  <rect x="1012" y="410" width="92" height="12" rx="6" fill="#5B9BD5"/><text x="1138" y="421" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Bay</text>
  <rect x="1012" y="436" width="74" height="12" rx="6" fill="#ED7D31"/><text x="1138" y="447" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">SD</text>

  <rect x="314" y="512" width="286" height="144" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="336" y="540" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Pipeline stages</text>
  <rect x="338" y="564" width="210" height="16" rx="8" fill="#2F75B5"/><rect x="338" y="592" width="160" height="16" rx="8" fill="#70AD47"/><rect x="338" y="620" width="104" height="16" rx="8" fill="#ED7D31"/>
  <text x="558" y="577" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">92%</text><text x="508" y="605" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">71%</text><text x="452" y="633" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">46%</text>

  <rect x="620" y="512" width="286" height="144" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="642" y="540" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Service health</text>
  <circle cx="704" cy="596" r="42" fill="none" stroke="#E8ECE4" stroke-width="13"/>
  <path d="M704,554 A42,42 0 1,1 668,617" fill="none" stroke="#70AD47" stroke-width="13" stroke-linecap="round"/>
  <text x="682" y="602" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#404040">88</text>
  <text x="770" y="586" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">SLA score</text>
  <text x="770" y="614" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">+6 pts QoQ</text>

  <rect x="926" y="512" width="286" height="144" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="948" y="540" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#404040">Forecast confidence</text>
  <path d="M950,626 C980,602 1012,620 1042,586 C1072,552 1110,566 1186,548" fill="none" stroke="#FFC000" stroke-width="5" stroke-linecap="round"/>
  <path d="M950,626 C980,602 1012,620 1042,586 C1072,552 1110,566 1186,548 L1186,638 L950,638 Z" fill="#FFC000" opacity="0.14"/>
  <text x="948" y="584" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#404040">94%</text>
  <text x="1040" y="584" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">weighted commit</text>
</svg>
```

## Avoid in this skill
- ❌ Using embedded BI widgets, Excel slicers, or interactive controls; reproduce them as static editable SVG pills and panels instead.
- ❌ Building charts as raster screenshots unless a real UI capture is essential; native `<rect>`, `<line>`, `<path>`, and `<circle>` charts remain editable.
- ❌ Applying `filter` to `<line>` gridlines or axes; use filters only on cards, paths, text, circles, ellipses, or rectangles.
- ❌ Using `<foreignObject>` for tables or HTML dashboards; it will hard-fail translation.
- ❌ Using `clip-path` on chart panels or shapes; clipping is reliable only for `<image>` crops.
- ❌ Relying on `<pattern>` fills for heatmaps or grids; use individual editable rectangles.

## Composition notes
- Keep the sidebar around 20–23% of the slide width; it should feel visually heavy and contain only top-level KPIs, filters, and brand context.
- Use a consistent card gutter of roughly 18–24 px; the grid discipline is what makes the busy dashboard feel calm.
- The main content area should stay light, with white cards over a pale mint background and only 3–4 recurring chart accent colors.
- Put the most important trend card in the upper-left of the main grid, because viewers read from sidebar summary into detailed analysis.