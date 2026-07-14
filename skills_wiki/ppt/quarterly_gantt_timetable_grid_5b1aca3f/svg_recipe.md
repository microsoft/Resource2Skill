# SVG Recipe — Quarterly Gantt Timetable Grid

## Visual mechanism
A fiscal-year roadmap is built as four rounded quarter “containers” with colorful month tabs and a strict row grid, then overlaid with floating rounded Gantt pills that span months and quarters. The contrast between the disciplined timetable structure and the free-positioned bars creates an executive-planning look that is easier to scan than a traditional table.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 2× decorative `<path>` blobs for subtle premium background atmosphere
- 4× large rounded `<rect>` quarter cards
- 4× dark rounded `<rect>` quarter header ribbons
- 12× colored rounded `<rect>` month tabs
- 24× `<line>` for horizontal row dividers and vertical month separators
- 6× left-side `<text>` labels for project rows
- 16× header `<text>` elements for quarter and month labels
- 6× rounded `<rect>` Gantt bars with gradient fills
- 5× small `<circle>` milestone/status dots
- 8× annotation `<text>` elements for bar labels and date tags
- 2× `<filter>` definitions: one soft card shadow, one glow for active Gantt bars
- 6× `<linearGradient>` definitions for card and bar color treatments

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAFBFF"/>
      <stop offset="100%" stop-color="#F3F6FA"/>
    </linearGradient>
    <linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F9FC"/>
    </linearGradient>
    <linearGradient id="barBlue" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2DD4BF"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="barViolet" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="100%" stop-color="#A855F7"/>
    </linearGradient>
    <linearGradient id="barWarm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F97316"/>
      <stop offset="100%" stop-color="#E11D48"/>
    </linearGradient>
    <linearGradient id="barSlate" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="barGlow" x="-15%" y="-60%" width="130%" height="220%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-40,130 C95,30 195,55 245,135 C300,225 155,265 45,235 C-45,210 -105,180 -40,130 Z" fill="#DCEBFF" opacity="0.55" filter="url(#barGlow)"/>
  <path d="M1050,54 C1160,-12 1286,35 1320,124 C1364,242 1234,282 1136,222 C1044,166 963,104 1050,54 Z" fill="#FFE7D6" opacity="0.45" filter="url(#barGlow)"/>

  <text x="60" y="68" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#172033">PROJECT TIMETABLE</text>
  <text x="62" y="99" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#7B8494">Annual roadmap grouped by fiscal quarters · editable SVG-to-PowerPoint shapes</text>
  <rect x="1020" y="50" width="158" height="34" rx="17" fill="#172033"/>
  <text x="1040" y="72" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">FY 2026 PLAN</text>

  <text x="62" y="208" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#94A3B8">WORKSTREAM</text>
  <line x1="232" y1="230" x2="232" y2="554" stroke="#CBD5E1" stroke-width="1.5"/>

  <text x="64" y="262" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">Strategy</text>
  <text x="64" y="316" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">Platform Build</text>
  <text x="64" y="370" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">Content Engine</text>
  <text x="64" y="424" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">Pilot Markets</text>
  <text x="64" y="478" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">Global Rollout</text>
  <text x="64" y="532" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E293B">Governance</text>

  <rect x="250" y="144" width="230" height="420" rx="22" fill="url(#cardFill)" stroke="#D8DEE9" filter="url(#softShadow)"/>
  <rect x="496" y="144" width="230" height="420" rx="22" fill="url(#cardFill)" stroke="#D8DEE9" filter="url(#softShadow)"/>
  <rect x="742" y="144" width="230" height="420" rx="22" fill="url(#cardFill)" stroke="#D8DEE9" filter="url(#softShadow)"/>
  <rect x="988" y="144" width="230" height="420" rx="22" fill="url(#cardFill)" stroke="#D8DEE9" filter="url(#softShadow)"/>

  <rect x="250" y="144" width="230" height="58" rx="22" fill="#222A44"/>
  <rect x="496" y="144" width="230" height="58" rx="22" fill="#222A44"/>
  <rect x="742" y="144" width="230" height="58" rx="22" fill="#222A44"/>
  <rect x="988" y="144" width="230" height="58" rx="22" fill="#222A44"/>
  <text x="336" y="181" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">Q1</text>
  <text x="582" y="181" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">Q2</text>
  <text x="828" y="181" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">Q3</text>
  <text x="1074" y="181" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">Q4</text>

  <rect x="263" y="204" width="62" height="27" rx="9" fill="#48CAE4"/><text x="282" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#083344">JAN</text>
  <rect x="334" y="204" width="62" height="27" rx="9" fill="#90E0EF"/><text x="353" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#083344">FEB</text>
  <rect x="405" y="204" width="62" height="27" rx="9" fill="#0077B6"/><text x="424" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">MAR</text>
  <rect x="509" y="204" width="62" height="27" rx="9" fill="#0096C7"/><text x="528" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">APR</text>
  <rect x="580" y="204" width="62" height="27" rx="9" fill="#48BEDC"/><text x="598" y="223" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#083344">MAY</text>
  <rect x="651" y="204" width="62" height="27" rx="9" fill="#0A64A0"/><text x="671" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">JUN</text>
  <rect x="755" y="204" width="62" height="27" rx="9" fill="#E63946"/><text x="776" y="223" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">JUL</text>
  <rect x="826" y="204" width="62" height="27" rx="9" fill="#F4A261"/><text x="845" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#552000">AUG</text>
  <rect x="897" y="204" width="62" height="27" rx="9" fill="#E9C46A"/><text x="916" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#4A2A00">SEP</text>
  <rect x="1001" y="204" width="62" height="27" rx="9" fill="#9B2226"/><text x="1020" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">OCT</text>
  <rect x="1072" y="204" width="62" height="27" rx="9" fill="#CA6702"/><text x="1091" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">NOV</text>
  <rect x="1143" y="204" width="62" height="27" rx="9" fill="#BB3E03"/><text x="1162" y="223" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF">DEC</text>

  <line x1="250" y1="284" x2="1218" y2="284" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="250" y1="338" x2="1218" y2="338" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="250" y1="392" x2="1218" y2="392" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="250" y1="446" x2="1218" y2="446" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="250" y1="500" x2="1218" y2="500" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="250" y1="554" x2="1218" y2="554" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="327" y1="232" x2="327" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="403" y1="232" x2="403" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="573" y1="232" x2="573" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="649" y1="232" x2="649" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="819" y1="232" x2="819" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="895" y1="232" x2="895" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="1065" y1="232" x2="1065" y2="554" stroke="#EEF2F7" stroke-width="1"/>
  <line x1="1141" y1="232" x2="1141" y2="554" stroke="#EEF2F7" stroke-width="1"/>

  <rect x="272" y="245" width="174" height="28" rx="14" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="292" y="264" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#FFFFFF">Discovery Sprint</text>
  <rect x="344" y="299" width="462" height="28" rx="14" fill="url(#barViolet)" filter="url(#softShadow)"/>
  <text x="366" y="318" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#FFFFFF">Core Platform Build</text>
  <circle cx="806" cy="313" r="7" fill="#FFFFFF" stroke="#7C3AED" stroke-width="4"/>
  <rect x="514" y="353" width="182" height="28" rx="14" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="535" y="372" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#FFFFFF">Content Factory</text>
  <rect x="650" y="407" width="296" height="28" rx="14" fill="url(#barWarm)" filter="url(#softShadow)"/>
  <text x="674" y="426" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#FFFFFF">Pilot Market Waves</text>
  <circle cx="946" cy="421" r="7" fill="#FFFFFF" stroke="#E11D48" stroke-width="4"/>
  <rect x="826" y="461" width="372" height="28" rx="14" fill="url(#barWarm)" filter="url(#softShadow)"/>
  <text x="850" y="480" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#FFFFFF">Global Launch Sequence</text>
  <circle cx="1198" cy="475" r="7" fill="#FFFFFF" stroke="#BE123C" stroke-width="4"/>
  <rect x="278" y="515" width="914" height="28" rx="14" fill="url(#barSlate)" opacity="0.92" filter="url(#softShadow)"/>
  <text x="302" y="534" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#FFFFFF">Governance, Risk & Executive Steering</text>
  <circle cx="480" cy="529" r="5" fill="#67E8F9"/>
  <circle cx="742" cy="529" r="5" fill="#FDBA74"/>

  <text x="1003" y="606" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#475569">● Milestone gates mark executive approval points</text>
  <text x="62" y="626" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Tip: animate each Gantt pill with a left-to-right wipe to reveal progress during presentation.</text>
</svg>
```

## Avoid in this skill
- ❌ Building the timetable as an actual SVG/PPT table; individual lines and rectangles are easier to edit and align.
- ❌ Using `<use>` to duplicate month tabs or row lines; repeated native shapes translate more reliably.
- ❌ Applying filters to `<line>` grid rules; shadows and glows should stay on cards, bars, paths, or text.
- ❌ Using `marker-end` for timeline arrows; if arrows are needed, use native `<line>` with direct marker support only where verified, or draw arrowheads as small `<path>` triangles.
- ❌ Clipping or masking non-image shapes to fake header sections; use stacked rounded rectangles instead.

## Composition notes
- Reserve roughly 15–18% of the slide width for workstream labels; the remaining width becomes the four-quarter planning canvas.
- Keep quarter cards evenly spaced with visible gaps so the viewer reads the year in four digestible blocks.
- Use quiet grid lines and high-contrast Gantt pills; the bars should be the dominant visual layer.
- Month tabs provide color rhythm: cool blues early in the year, warm oranges/reds toward launch quarters.