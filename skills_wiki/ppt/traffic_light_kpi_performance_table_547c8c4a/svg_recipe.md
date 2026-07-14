# SVG Recipe — Traffic Light KPI Performance Table

## Visual mechanism
A dense executive KPI table becomes instantly scannable by pairing actual/target numbers with compact “traffic light” status badges: green upward arrows for favorable performance, red downward arrows for unfavorable performance, and gray neutral dashes for on-track values. Strong colored header bands, grouped MTD/YTD columns, and disciplined grid alignment keep the data readable while making exceptions pop visually.

## SVG primitives needed
- 1× `<rect>` full-slide background plus decorative header/card rectangles
- 1× `<linearGradient>` for a premium purple title bar
- 1× `<filter id="cardShadow">` applied to the main table card
- Multiple `<rect>` elements for header bands, row striping, status badge circles, and neutral dash icons
- Multiple `<path>` elements for grid rules, decorative corner waves, and editable up/down arrow glyphs
- Multiple `<text>` elements for title, period selector, column headers, KPI names, units, numeric values, and footer note
- Optional `<line>` elements may be used for simple separators, but this recipe uses stroked paths for compact grid construction

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#351075"/>
      <stop offset="52%" stop-color="#4C2491"/>
      <stop offset="100%" stop-color="#7151C7"/>
    </linearGradient>
    <linearGradient id="softBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F7F5FC"/>
      <stop offset="100%" stop-color="#EEF2FA"/>
    </linearGradient>
    <filter id="cardShadow" x="-8%" y="-8%" width="116%" height="120%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#softBg)"/>
  <path d="M1010,0 C1120,48 1205,18 1280,82 L1280,0 Z" fill="#E6DFF8"/>
  <path d="M0,650 C130,608 255,720 410,670 L410,720 L0,720 Z" fill="#DFE8FA"/>

  <rect x="48" y="32" width="1184" height="82" rx="22" fill="url(#titleGrad)"/>
  <text x="78" y="84" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Water Desalination KPI Dashboard — 2025</text>
  <rect x="968" y="51" width="220" height="44" rx="22" fill="#FFFFFF" opacity="0.18"/>
  <text x="990" y="80" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF">November 2025</text>

  <rect x="62" y="136" width="1156" height="484" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="70" y="150" width="1150" height="38" rx="10" fill="#DDD6ED"/>
  <rect x="70" y="188" width="1150" height="48" fill="#4472C4"/>

  <rect x="70" y="150" width="450" height="38" rx="10" fill="#DDD6ED"/>
  <rect x="520" y="150" width="340" height="38" fill="#D2C8EA"/>
  <rect x="860" y="150" width="360" height="38" rx="10" fill="#DDD6ED"/>
  <text x="295" y="175" width="300" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#4C2491">KPI DETAIL</text>
  <text x="690" y="175" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#4C2491">MONTH TO DATE</text>
  <text x="1040" y="175" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#4C2491">YEAR TO DATE</text>

  <text x="145" y="218" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Group</text>
  <text x="330" y="218" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">KPI</text>
  <text x="480" y="218" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Unit</text>
  <text x="570" y="218" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Actual</text>
  <text x="670" y="218" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Target</text>
  <text x="755" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">vs</text>
  <text x="755" y="226" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Target</text>
  <text x="825" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">vs</text>
  <text x="825" y="226" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">PY</text>
  <text x="910" y="218" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Actual</text>
  <text x="1010" y="218" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Target</text>
  <text x="1095" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">vs</text>
  <text x="1095" y="226" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Target</text>
  <text x="1165" y="210" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">vs</text>
  <text x="1165" y="226" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">PY</text>

  <rect x="70" y="236" width="1150" height="58" fill="#FFFFFF"/>
  <rect x="70" y="294" width="1150" height="58" fill="#F7F9FE"/>
  <rect x="70" y="352" width="1150" height="58" fill="#FFFFFF"/>
  <rect x="70" y="410" width="1150" height="58" fill="#F7F9FE"/>
  <rect x="70" y="468" width="1150" height="58" fill="#FFFFFF"/>
  <rect x="70" y="526" width="1150" height="58" fill="#F7F9FE"/>

  <path d="M70 236 H1220 M70 294 H1220 M70 352 H1220 M70 410 H1220 M70 468 H1220 M70 526 H1220 M70 584 H1220 M220 188 V584 M440 188 V584 M520 150 V584 M620 188 V584 M720 188 V584 M790 188 V584 M860 150 V584 M960 188 V584 M1060 188 V584 M1130 188 V584" stroke="#CBD3E2" stroke-width="1" fill="none"/>
  <path d="M70 150 H1220 V584 H70 Z" stroke="#9EACCA" stroke-width="1.5" fill="none"/>

  <text x="84" y="270" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4A4A5A">Production</text>
  <text x="230" y="270" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">Freshwater Output</text>
  <text x="480" y="270" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">MGD</text>
  <text x="570" y="270" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">136.0</text>
  <text x="670" y="270" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">130.1</text>
  <text x="910" y="270" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">1,386.5</text>
  <text x="1010" y="270" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">1,318.8</text>

  <text x="84" y="328" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4A4A5A">Operations</text>
  <text x="230" y="328" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">Capacity Utilization</text>
  <text x="480" y="328" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">%</text>
  <text x="570" y="328" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">100.0</text>
  <text x="670" y="328" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">105.0</text>
  <text x="910" y="328" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">1,018.6</text>
  <text x="1010" y="328" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">1,096.6</text>

  <text x="84" y="386" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4A4A5A">Quality</text>
  <text x="230" y="386" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">Water Quality Index</text>
  <text x="480" y="386" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">Score</text>
  <text x="570" y="386" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">95.8</text>
  <text x="670" y="386" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">98.0</text>
  <text x="910" y="386" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">979.7</text>
  <text x="1010" y="386" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">998.6</text>

  <text x="84" y="444" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4A4A5A">Efficiency</text>
  <text x="230" y="444" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">Energy Consumption</text>
  <text x="480" y="444" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">kWh/Gal</text>
  <text x="570" y="444" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">8.8</text>
  <text x="670" y="444" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">8.3</text>
  <text x="910" y="444" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">89.8</text>
  <text x="1010" y="444" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">85.1</text>

  <text x="84" y="502" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4A4A5A">Maintenance</text>
  <text x="230" y="502" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">Uptime Rate</text>
  <text x="480" y="502" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">%</text>
  <text x="570" y="502" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">98.0</text>
  <text x="670" y="502" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">99.0</text>
  <text x="910" y="502" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">98.2</text>
  <text x="1010" y="502" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">99.1</text>

  <text x="84" y="560" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4A4A5A">Safety</text>
  <text x="230" y="560" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">Safety Incidents</text>
  <text x="480" y="560" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">Count</text>
  <text x="570" y="560" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">1</text>
  <text x="670" y="560" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">0</text>
  <text x="910" y="560" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">5</text>
  <text x="1010" y="560" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222238">2</text>

  <circle cx="755" cy="265" r="16" fill="#E7F7EE"/><path d="M755 252 L766 267 L760 267 L760 278 L750 278 L750 267 L744 267 Z" fill="#00B050"/><circle cx="825" cy="265" r="16" fill="#F0F1F4"/><rect x="815" y="261" width="20" height="8" rx="4" fill="#808080"/><circle cx="1095" cy="265" r="16" fill="#E7F7EE"/><path d="M1095 252 L1106 267 L1100 267 L1100 278 L1090 278 L1090 267 L1084 267 Z" fill="#00B050"/><circle cx="1165" cy="265" r="16" fill="#E7F7EE"/><path d="M1165 252 L1176 267 L1170 267 L1170 278 L1160 278 L1160 267 L1154 267 Z" fill="#00B050"/>
  <circle cx="755" cy="323" r="16" fill="#FDEAEA"/><path d="M755 336 L744 321 L750 321 L750 310 L760 310 L760 321 L766 321 Z" fill="#FF0000"/><circle cx="825" cy="323" r="16" fill="#FDEAEA"/><path d="M825 336 L814 321 L820 321 L820 310 L830 310 L830 321 L836 321 Z" fill="#FF0000"/><circle cx="1095" cy="323" r="16" fill="#FDEAEA"/><path d="M1095 336 L1084 321 L1090 321 L1090 310 L1100 310 L1100 321 L1106 321 Z" fill="#FF0000"/><circle cx="1165" cy="323" r="16" fill="#FDEAEA"/><path d="M1165 336 L1154 321 L1160 321 L1160 310 L1170 310 L1170 321 L1176 321 Z" fill="#FF0000"/>
  <circle cx="755" cy="381" r="16" fill="#FDEAEA"/><path d="M755 394 L744 379 L750 379 L750 368 L760 368 L760 379 L766 379 Z" fill="#FF0000"/><circle cx="825" cy="381" r="16" fill="#FDEAEA"/><path d="M825 394 L814 379 L820 379 L820 368 L830 368 L830 379 L836 379 Z" fill="#FF0000"/><circle cx="1095" cy="381" r="16" fill="#FDEAEA"/><path d="M1095 394 L1084 379 L1090 379 L1090 368 L1100 368 L1100 379 L1106 379 Z" fill="#FF0000"/><circle cx="1165" cy="381" r="16" fill="#FDEAEA"/><path d="M1165 394 L1154 379 L1160 379 L1160 368 L1170 368 L1170 379 L1176 379 Z" fill="#FF0000"/>
  <circle cx="755" cy="439" r="16" fill="#FDEAEA"/><path d="M755 452 L744 437 L750 437 L750 426 L760 426 L760 437 L766 437 Z" fill="#FF0000"/><circle cx="825" cy="439" r="16" fill="#F0F1F4"/><rect x="815" y="435" width="20" height="8" rx="4" fill="#808080"/><circle cx="1095" cy="439" r="16" fill="#FDEAEA"/><path d="M1095 452 L1084 437 L1090 437 L1090 426 L1100 426 L1100 437 L1106 437 Z" fill="#FF0000"/><circle cx="1165" cy="439" r="16" fill="#E7F7EE"/><path d="M1165 426 L1176 441 L1170 441 L1170 452 L1160 452 L1160 441 L1154 441 Z" fill="#00B050"/>
  <circle cx="755" cy="497" r="16" fill="#FDEAEA"/><path d="M755 510 L744 495 L750 495 L750 484 L760 484 L760 495 L766 495 Z" fill="#FF0000"/><circle cx="825" cy="497" r="16" fill="#E7F7EE"/><path d="M825 484 L836 499 L830 499 L830 510 L820 510 L820 499 L814 499 Z" fill="#00B050"/><circle cx="1095" cy="497" r="16" fill="#FDEAEA"/><path d="M1095 510 L1084 495 L1090 495 L1090 484 L1100 484 L1100 495 L1106 495 Z" fill="#FF0000"/><circle cx="1165" cy="497" r="16" fill="#E7F7EE"/><path d="M1165 484 L1176 499 L1170 499 L1170 510 L1160 510 L1160 499 L1154 499 Z" fill="#00B050"/>
  <circle cx="755" cy="555" r="16" fill="#FDEAEA"/><path d="M755 568 L744 553 L750 553 L750 542 L760 542 L760 553 L766 553 Z" fill="#FF0000"/><circle cx="825" cy="555" r="16" fill="#E7F7EE"/><path d="M825 542 L836 557 L830 557 L830 568 L820 568 L820 557 L814 557 Z" fill="#00B050"/><circle cx="1095" cy="555" r="16" fill="#FDEAEA"/><path d="M1095 568 L1084 553 L1090 553 L1090 542 L1100 542 L1100 553 L1106 553 Z" fill="#FF0000"/><circle cx="1165" cy="555" r="16" fill="#E7F7EE"/><path d="M1165 542 L1176 557 L1170 557 L1170 568 L1160 568 L1160 557 L1154 557 Z" fill="#00B050"/>

  <rect x="70" y="640" width="18" height="18" rx="9" fill="#00B050"/><text x="96" y="655" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4A4A5A">Good / favorable variance</text>
  <rect x="305" y="640" width="18" height="18" rx="9" fill="#FF0000"/><text x="331" y="655" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4A4A5A">Bad / unfavorable variance</text>
  <rect x="560" y="640" width="18" height="18" rx="9" fill="#808080"/><text x="586" y="655" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4A4A5A">Neutral or within tolerance band</text>
  <text x="930" y="655" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#697084">Traffic logic should respect KPI direction: UTB vs LTB.</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<foreignObject>` or embedded HTML tables; build the table from editable SVG rectangles, paths, and text.
- ❌ Applying `clip-path` or masks to table cells or status icons; clipping is only reliable on `<image>` elements.
- ❌ Using `marker-end` for KPI arrows; create arrows as filled `<path>` shapes or Unicode text instead.
- ❌ Relying on tiny low-contrast red/green text alone; the performance cue should be a distinct colored badge or icon.
- ❌ Omitting `width` on `<text>` elements; PowerPoint text boxes need explicit widths for stable rendering.

## Composition notes
- Keep the table as the dominant object, occupying roughly 80–85% of slide width, with generous outer margins and a strong title band.
- Use grouped column headers for MTD and YTD so the audience can compare short-term and cumulative performance without reading every column label.
- Reserve the strongest saturated colors for the title bar, column header row, and traffic-light icons; keep data rows mostly white or pale blue.
- Numeric columns should be center-aligned, descriptive KPI labels left-aligned, and status columns narrow so the colored icons form vertical “health” stripes.