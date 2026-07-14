# SVG Recipe — Data Analytics Dashboard Grid

## Visual mechanism
A SaaS-style analytics dashboard built from a strict 3-column card grid, where each card isolates one metric story with a title, compact chart, and small annotations. The visual hierarchy comes from white elevated cards on a pale background, colorful donut distributions in the top row, and ranked horizontal bar charts in the bottom row.

## SVG primitives needed
- 1× `<rect>` for the full-slide pale dashboard background
- 1× `<rect>` with `<linearGradient>` for the dark executive header ribbon
- 6× rounded `<rect>` cards with subtle shadow filters for the dashboard panels
- 3× `<circle>` background rings for donut chart tracks
- 9× stroked `<path>` arc segments for editable donut chart slices
- 18× small `<circle>` legend bullets and status dots
- 24× `<rect>` for horizontal bar tracks and filled ranked bars
- 6× `<line>` dashed gridlines inside bar-chart cards
- Multiple `<text>` elements with explicit `width` for titles, KPI values, labels, and bar values
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to card rectangles
- 2× `<linearGradient>` fills for header and accent KPI pills

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0B2E6F"/>
      <stop offset="55%" stop-color="#0D47A1"/>
      <stop offset="100%" stop-color="#1565C0"/>
    </linearGradient>
    <linearGradient id="pillGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E3F2FD"/>
      <stop offset="100%" stop-color="#BBDEFB"/>
    </linearGradient>
    <filter id="cardShadow" x="-8%" y="-8%" width="116%" height="124%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F7FA"/>
  <rect x="0" y="0" width="1280" height="76" fill="url(#headerGrad)"/>
  <text x="48" y="47" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">PERFORMANCE DASHBOARD</text>
  <text x="920" y="31" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D8E9FF">Snapshot period</text>
  <text x="920" y="54" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">FY2026 · Week 18</text>
  <rect x="1138" y="22" width="94" height="32" rx="16" fill="#FFFFFF" opacity="0.14"/>
  <circle cx="1159" cy="38" r="5" fill="#4CAF50"/>
  <text x="1171" y="43" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">LIVE</text>

  <rect x="48" y="104" width="380" height="270" rx="18" fill="#FFFFFF" stroke="#DDE2EA" filter="url(#cardShadow)"/>
  <rect x="450" y="104" width="380" height="270" rx="18" fill="#FFFFFF" stroke="#DDE2EA" filter="url(#cardShadow)"/>
  <rect x="852" y="104" width="380" height="270" rx="18" fill="#FFFFFF" stroke="#DDE2EA" filter="url(#cardShadow)"/>
  <rect x="48" y="398" width="380" height="274" rx="18" fill="#FFFFFF" stroke="#DDE2EA" filter="url(#cardShadow)"/>
  <rect x="450" y="398" width="380" height="274" rx="18" fill="#FFFFFF" stroke="#DDE2EA" filter="url(#cardShadow)"/>
  <rect x="852" y="398" width="380" height="274" rx="18" fill="#FFFFFF" stroke="#DDE2EA" filter="url(#cardShadow)"/>

  <text x="74" y="136" width="328" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#323842">Current Year To Date Snapshot</text>
  <text x="476" y="136" width="328" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#323842">Current Quarter To Date Snapshot</text>
  <text x="878" y="136" width="328" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#323842">Current Month To Date Snapshot</text>

  <circle cx="238" cy="245" r="68" fill="none" stroke="#EEF2F6" stroke-width="27"/>
  <path d="M238 177 A68 68 0 0 1 299 274" fill="none" stroke="#4CAF50" stroke-width="27" stroke-linecap="round"/>
  <path d="M299 274 A68 68 0 0 1 175 268" fill="none" stroke="#2196F3" stroke-width="27" stroke-linecap="round"/>
  <path d="M175 268 A68 68 0 0 1 238 177" fill="none" stroke="#F44336" stroke-width="27" stroke-linecap="round"/>
  <text x="194" y="241" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#222B35">68%</text>
  <text x="194" y="263" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#6B7280">won + pipeline</text>

  <circle cx="640" cy="245" r="68" fill="none" stroke="#EEF2F6" stroke-width="27"/>
  <path d="M640 177 A68 68 0 0 1 705 266" fill="none" stroke="#4CAF50" stroke-width="27" stroke-linecap="round"/>
  <path d="M705 266 A68 68 0 0 1 575 266" fill="none" stroke="#2196F3" stroke-width="27" stroke-linecap="round"/>
  <path d="M575 266 A68 68 0 0 1 640 177" fill="none" stroke="#F44336" stroke-width="27" stroke-linecap="round"/>
  <text x="596" y="241" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#222B35">70%</text>
  <text x="596" y="263" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#6B7280">active coverage</text>

  <circle cx="1042" cy="245" r="68" fill="none" stroke="#EEF2F6" stroke-width="27"/>
  <path d="M1042 177 A68 68 0 0 1 1107 224" fill="none" stroke="#4CAF50" stroke-width="27" stroke-linecap="round"/>
  <path d="M1107 224 A68 68 0 0 1 977 266" fill="none" stroke="#2196F3" stroke-width="27" stroke-linecap="round"/>
  <path d="M977 266 A68 68 0 0 1 1042 177" fill="none" stroke="#F44336" stroke-width="27" stroke-linecap="round"/>
  <text x="998" y="241" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="middle" fill="#222B35">73%</text>
  <text x="998" y="263" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#6B7280">healthy mix</text>

  <circle cx="107" cy="330" r="5" fill="#4CAF50"/><text x="120" y="335" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Closed</text>
  <circle cx="202" cy="330" r="5" fill="#2196F3"/><text x="215" y="335" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Pipeline</text>
  <circle cx="310" cy="330" r="5" fill="#F44336"/><text x="323" y="335" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">At risk</text>
  <circle cx="509" cy="330" r="5" fill="#4CAF50"/><text x="522" y="335" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Closed</text>
  <circle cx="604" cy="330" r="5" fill="#2196F3"/><text x="617" y="335" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Pipeline</text>
  <circle cx="712" cy="330" r="5" fill="#F44336"/><text x="725" y="335" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">At risk</text>
  <circle cx="911" cy="330" r="5" fill="#4CAF50"/><text x="924" y="335" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Closed</text>
  <circle cx="1006" cy="330" r="5" fill="#2196F3"/><text x="1019" y="335" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Pipeline</text>
  <circle cx="1114" cy="330" r="5" fill="#F44336"/><text x="1127" y="335" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">At risk</text>

  <text x="74" y="431" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#323842">Lead Source Conversion</text>
  <text x="476" y="431" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#323842">Top Accounts Forecast</text>
  <text x="878" y="431" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#323842">Campaign ROI Ranking</text>

  <line x1="220" y1="463" x2="220" y2="637" stroke="#E6EAF0" stroke-dasharray="4 5"/>
  <line x1="330" y1="463" x2="330" y2="637" stroke="#E6EAF0" stroke-dasharray="4 5"/>
  <text x="74" y="484" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Organic search</text>
  <rect x="190" y="471" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="190" y="471" width="152" height="14" rx="7" fill="#FF9800"/>
  <text x="348" y="483" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">80%</text>
  <text x="74" y="520" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Partner</text>
  <rect x="190" y="507" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="190" y="507" width="131" height="14" rx="7" fill="#FF9800"/>
  <text x="327" y="519" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">69%</text>
  <text x="74" y="556" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Outbound</text>
  <rect x="190" y="543" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="190" y="543" width="103" height="14" rx="7" fill="#FF9800"/>
  <text x="299" y="555" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">54%</text>
  <text x="74" y="592" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Events</text>
  <rect x="190" y="579" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="190" y="579" width="84" height="14" rx="7" fill="#FF9800"/>
  <text x="280" y="591" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">44%</text>

  <line x1="622" y1="463" x2="622" y2="637" stroke="#E6EAF0" stroke-dasharray="4 5"/>
  <line x1="732" y1="463" x2="732" y2="637" stroke="#E6EAF0" stroke-dasharray="4 5"/>
  <text x="476" y="484" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Apex Retail</text>
  <rect x="592" y="471" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="592" y="471" width="165" height="14" rx="7" fill="#FF9800"/>
  <text x="763" y="483" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">$4.1M</text>
  <text x="476" y="520" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Northstar</text>
  <rect x="592" y="507" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="592" y="507" width="140" height="14" rx="7" fill="#FF9800"/>
  <text x="738" y="519" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">$3.5M</text>
  <text x="476" y="556" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">BluePeak</text>
  <rect x="592" y="543" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="592" y="543" width="112" height="14" rx="7" fill="#FF9800"/>
  <text x="710" y="555" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">$2.8M</text>
  <text x="476" y="592" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Atlas Group</text>
  <rect x="592" y="579" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="592" y="579" width="88" height="14" rx="7" fill="#FF9800"/>
  <text x="686" y="591" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">$2.2M</text>

  <line x1="1024" y1="463" x2="1024" y2="637" stroke="#E6EAF0" stroke-dasharray="4 5"/>
  <line x1="1134" y1="463" x2="1134" y2="637" stroke="#E6EAF0" stroke-dasharray="4 5"/>
  <text x="878" y="484" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">ABM pods</text>
  <rect x="994" y="471" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="994" y="471" width="171" height="14" rx="7" fill="#FF9800"/>
  <text x="1171" y="483" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">9.0×</text>
  <text x="878" y="520" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Webinars</text>
  <rect x="994" y="507" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="994" y="507" width="146" height="14" rx="7" fill="#FF9800"/>
  <text x="1146" y="519" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">7.7×</text>
  <text x="878" y="556" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Paid social</text>
  <rect x="994" y="543" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="994" y="543" width="118" height="14" rx="7" fill="#FF9800"/>
  <text x="1118" y="555" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">6.2×</text>
  <text x="878" y="592" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#56606B">Sponsorships</text>
  <rect x="994" y="579" width="190" height="14" rx="7" fill="#EEF2F6"/><rect x="994" y="579" width="91" height="14" rx="7" fill="#FF9800"/>
  <text x="1091" y="591" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#323842">4.8×</text>

  <rect x="74" y="620" width="300" height="28" rx="14" fill="url(#pillGrad)"/>
  <text x="92" y="639" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#0D47A1">▲ Conversion up 12% versus prior period</text>
  <rect x="476" y="620" width="300" height="28" rx="14" fill="url(#pillGrad)"/>
  <text x="494" y="639" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#0D47A1">Pipeline concentration remains healthy</text>
  <rect x="878" y="620" width="300" height="28" rx="14" fill="url(#pillGrad)"/>
  <text x="896" y="639" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#0D47A1">ABM delivers the strongest payback</text>
</svg>
```

## Avoid in this skill
- ❌ Native chart objects are not required; reproduce donut and bar charts with editable SVG paths, circles, and rectangles instead.
- ❌ Do not use `<pattern>` fills for dashboard backgrounds or grid textures; use simple fills, dashed lines, and gradients.
- ❌ Do not clip or mask chart shapes; donut segments should be stroked `<path>` arcs or explicit filled wedge paths.
- ❌ Do not rely on tiny axis labels everywhere; dashboard cards need enough whitespace to remain executive-readable.
- ❌ Do not apply filters to `<line>` gridlines; filters on lines are dropped.

## Composition notes
- Keep a strong app-like frame: 70–80 px header, then a 3-column card grid with consistent margins and gutters.
- Use top-row cards for glanceable part-to-whole metrics; reserve bottom-row cards for rankings where labels need horizontal reading space.
- White cards should float on a pale gray-blue background with very subtle shadows; avoid heavy borders that make the dashboard feel like a spreadsheet.
- Use one repeated accent color for bars and three categorical colors for donuts so the eye understands chart type before reading details.