# SVG Recipe — Tabular Project Gantt Chart

## Visual mechanism
A structured table grid maps tasks vertically and weeks horizontally, while colored arrow bars sit precisely inside the grid to show task duration and sequencing. Month headers, week subheaders, milestones, and a compact legend add hierarchy so the schedule reads like an executive project roadmap rather than a spreadsheet.

## SVG primitives needed
- 1× full-slide `<rect>` for the soft presentation background
- 1× large rounded `<rect>` for the chart card surface
- 1× `<rect>` for the task-column header spanning both timeline header rows
- 3× `<rect>` with `<linearGradient>` fills for month headers
- 12× `<rect>` for week header cells
- 8× `<rect>` for alternating task-row bands
- 20+× `<line>` for vertical and horizontal table grid rules
- 9× `<path>` pentagon/arrow bars for scheduled task durations
- 3× milestone marker groups made from small `<rect>` flag poles and `<path>` flags/diamonds
- Multiple `<text width="...">` elements for title, subtitle, headers, week labels, task labels, and legend labels
- 3× small legend `<path>` or `<rect>` swatches for team/category color coding
- 1× `<filter id="cardShadow">` applied to the chart card
- 1× `<filter id="barShadow">` applied to duration bars and milestone flags
- 5× `<linearGradient>` definitions for polished header and bar fills

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFD"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="monthBlue" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#17365D"/>
      <stop offset="100%" stop-color="#2F5597"/>
    </linearGradient>
    <linearGradient id="monthOrange" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#C55A11"/>
      <stop offset="100%" stop-color="#ED7D31"/>
    </linearGradient>
    <linearGradient id="monthGreen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#548235"/>
      <stop offset="100%" stop-color="#70AD47"/>
    </linearGradient>
    <linearGradient id="barBlue" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2F528F"/>
      <stop offset="100%" stop-color="#5B9BD5"/>
    </linearGradient>
    <linearGradient id="barOrange" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ED7D31"/>
      <stop offset="100%" stop-color="#F4B183"/>
    </linearGradient>
    <linearGradient id="barPurple" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7030A0"/>
      <stop offset="100%" stop-color="#A86EDB"/>
    </linearGradient>
    <filter id="cardShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="barShadow" x="-10%" y="-30%" width="120%" height="160%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="2.5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="60" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1F2937">Gantt Chart — 3 Month Activity Roadmap</text>
  <text x="62" y="88" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#667085">Kickoff-to-launch plan with weekly cadence, ownership color coding, and visible delivery milestones.</text>

  <rect x="60" y="120" width="1160" height="520" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="60" y="120" width="1160" height="520" rx="18" fill="none" stroke="#D9E2EC" stroke-width="1"/>

  <rect x="60" y="130" width="280" height="86" fill="#6B7280"/>
  <text x="82" y="181" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">WORKSTREAM / ACTIVITY</text>

  <rect x="340" y="130" width="293.33" height="50" fill="url(#monthBlue)"/>
  <rect x="633.33" y="130" width="293.34" height="50" fill="url(#monthOrange)"/>
  <rect x="926.67" y="130" width="293.33" height="50" fill="url(#monthGreen)"/>
  <text x="486.7" y="162" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">MONTH 1 · DISCOVER</text>
  <text x="780" y="162" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">MONTH 2 · BUILD</text>
  <text x="1073.3" y="162" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">MONTH 3 · LAUNCH</text>

  <rect x="340" y="180" width="73.33" height="36" fill="#DEEBF7"/>
  <rect x="413.33" y="180" width="73.33" height="36" fill="#F2F7FC"/>
  <rect x="486.66" y="180" width="73.33" height="36" fill="#DEEBF7"/>
  <rect x="559.99" y="180" width="73.34" height="36" fill="#F2F7FC"/>
  <rect x="633.33" y="180" width="73.33" height="36" fill="#DEEBF7"/>
  <rect x="706.66" y="180" width="73.33" height="36" fill="#F2F7FC"/>
  <rect x="779.99" y="180" width="73.34" height="36" fill="#DEEBF7"/>
  <rect x="853.33" y="180" width="73.34" height="36" fill="#F2F7FC"/>
  <rect x="926.67" y="180" width="73.33" height="36" fill="#DEEBF7"/>
  <rect x="1000" y="180" width="73.33" height="36" fill="#F2F7FC"/>
  <rect x="1073.33" y="180" width="73.34" height="36" fill="#DEEBF7"/>
  <rect x="1146.67" y="180" width="73.33" height="36" fill="#F2F7FC"/>

  <text x="376.7" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W1</text>
  <text x="450" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W2</text>
  <text x="523.3" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W3</text>
  <text x="596.7" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W4</text>
  <text x="670" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W5</text>
  <text x="743.3" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W6</text>
  <text x="816.7" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W7</text>
  <text x="890" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W8</text>
  <text x="963.3" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W9</text>
  <text x="1036.7" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W10</text>
  <text x="1110" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W11</text>
  <text x="1183.3" y="204" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1F2937">W12</text>

  <rect x="60" y="216" width="1160" height="54" fill="#FFFFFF"/>
  <rect x="60" y="270" width="1160" height="54" fill="#F8FAFC"/>
  <rect x="60" y="324" width="1160" height="54" fill="#FFFFFF"/>
  <rect x="60" y="378" width="1160" height="54" fill="#F8FAFC"/>
  <rect x="60" y="432" width="1160" height="54" fill="#FFFFFF"/>
  <rect x="60" y="486" width="1160" height="54" fill="#F8FAFC"/>
  <rect x="60" y="540" width="1160" height="54" fill="#FFFFFF"/>
  <rect x="60" y="594" width="1160" height="36" fill="#F8FAFC"/>

  <line x1="340" y1="130" x2="340" y2="630" stroke="#C9D4E2" stroke-width="1.3"/>
  <line x1="413.33" y1="180" x2="413.33" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="486.66" y1="180" x2="486.66" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="559.99" y1="180" x2="559.99" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="633.33" y1="130" x2="633.33" y2="630" stroke="#B8C4D3" stroke-width="1.4"/>
  <line x1="706.66" y1="180" x2="706.66" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="779.99" y1="180" x2="779.99" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="853.33" y1="180" x2="853.33" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="926.67" y1="130" x2="926.67" y2="630" stroke="#B8C4D3" stroke-width="1.4"/>
  <line x1="1000" y1="180" x2="1000" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="1073.33" y1="180" x2="1073.33" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="1146.67" y1="180" x2="1146.67" y2="630" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="216" x2="1220" y2="216" stroke="#C9D4E2" stroke-width="1.3"/>
  <line x1="60" y1="270" x2="1220" y2="270" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="324" x2="1220" y2="324" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="378" x2="1220" y2="378" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="432" x2="1220" y2="432" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="486" x2="1220" y2="486" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="540" x2="1220" y2="540" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="60" y1="594" x2="1220" y2="594" stroke="#E2E8F0" stroke-width="1"/>

  <text x="82" y="249" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Market research</text>
  <text x="82" y="303" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Requirements & specs</text>
  <text x="82" y="357" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Program planning</text>
  <text x="82" y="411" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Experience design</text>
  <text x="82" y="465" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Development sprint</text>
  <text x="82" y="519" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Training & enablement</text>
  <text x="82" y="573" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Assessment & QA</text>
  <text x="82" y="621" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#374151">Final documentation</text>

  <path d="M350 231 L532 231 L550 243 L532 255 L350 255 Z" fill="url(#barBlue)" filter="url(#barShadow)"/>
  <path d="M423 285 L679 285 L697 297 L679 309 L423 309 Z" fill="url(#barBlue)" filter="url(#barShadow)"/>
  <path d="M643 339 L752 339 L770 351 L752 363 L643 363 Z" fill="url(#barOrange)" filter="url(#barShadow)"/>
  <path d="M790 393 L972 393 L990 405 L972 417 L790 417 Z" fill="url(#barPurple)" filter="url(#barShadow)"/>
  <path d="M863 447 L1119 447 L1137 459 L1119 471 L863 471 Z" fill="url(#barOrange)" filter="url(#barShadow)"/>
  <path d="M937 501 L1119 501 L1137 513 L1119 525 L937 525 Z" fill="url(#barBlue)" filter="url(#barShadow)"/>
  <path d="M1010 548 L1119 548 L1137 557 L1119 566 L1010 566 Z" fill="url(#barPurple)" filter="url(#barShadow)"/>
  <path d="M1083 572 L1192 572 L1210 581 L1192 590 L1083 590 Z" fill="url(#barPurple)" filter="url(#barShadow)"/>
  <path d="M1157 609 L1192 609 L1210 621 L1192 633 L1157 633 Z" fill="url(#barPurple)" filter="url(#barShadow)"/>

  <rect x="842" y="321" width="4" height="35" rx="2" fill="#4B5563"/>
  <path d="M846 323 L877 331 L846 339 Z" fill="#70AD47" filter="url(#barShadow)"/>
  <rect x="1146" y="429" width="4" height="35" rx="2" fill="#4B5563"/>
  <path d="M1150 431 L1181 439 L1150 447 Z" fill="#70AD47" filter="url(#barShadow)"/>
  <path d="M1205 546 L1218 559 L1205 572 L1192 559 Z" fill="#70AD47" filter="url(#barShadow)"/>

  <rect x="860" y="48" width="300" height="40" rx="20" fill="#FFFFFF" stroke="#D9E2EC"/>
  <path d="M883 60 L910 60 L918 68 L910 76 L883 76 Z" fill="url(#barBlue)"/>
  <text x="927" y="73" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">Team A</text>
  <path d="M997 60 L1024 60 L1032 68 L1024 76 L997 76 Z" fill="url(#barOrange)"/>
  <text x="1041" y="73" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">Team B</text>
  <path d="M1111 60 L1138 60 L1146 68 L1138 76 L1111 76 Z" fill="url(#barPurple)"/>
  <text x="1155" y="73" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475467">Team C</text>
</svg>
```

## Avoid in this skill
- ❌ Using an actual HTML table or `<foreignObject>`; build the table visually from editable SVG rectangles, lines, and text.
- ❌ Relying on `marker-end` for arrows; duration bars should be explicit pentagon `<path>` shapes so the arrowheads remain editable.
- ❌ Applying filters to `<line>` grid rules; shadows/glows on lines are dropped, so keep grid lines flat and apply shadows only to rect/path/text.
- ❌ Using `<mask>` or clipping non-image elements to create row effects; alternating row bands are safer as plain `<rect>` layers.
- ❌ Omitting `width` on text labels; every `<text>` element needs an explicit width for clean PowerPoint rendering.

## Composition notes
- Keep the task column around 24–26% of the table width; the timeline needs the remaining space for accurate week-to-week proportionality.
- Use saturated color only for month headers, bars, and milestones; keep grid lines and row fills pale so the schedule data dominates.
- Align each bar to week boundaries with a small horizontal inset, leaving visible grid context around every duration marker.
- Place title, subtitle, and legend above the chart card; the table itself should occupy the majority of the slide for immediate readability.