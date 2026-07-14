# SVG Recipe — Interactive Financial Waterfall Dashboard

## Visual mechanism
A static “what-if” finance dashboard that looks interactive: slider-style controls on the left feed a P&L table in the center and an editable waterfall chart on the right. The key effect is the visual linkage between adjustable cost drivers, conditional table highlights, and profit impact bars.

## SVG primitives needed
- 1× full-slide `<rect>` for the premium dark-to-light background.
- 3× panel `<rect>` shapes for controls, P&L table, and waterfall chart containers.
- Multiple small `<rect>` shapes for table cells, slider tracks, value chips, waterfall bars, KPI badges, and chart labels.
- Multiple `<line>` elements for table gridlines, chart axes, chart gridlines, and waterfall connector rules.
- Multiple `<circle>` elements for slider thumbs and small status indicators.
- 2× decorative `<path>` elements for subtle financial-flow curves and callout accents.
- Many `<text>` elements with explicit `width` attributes for titles, labels, table values, axis labels, bar labels, and insights.
- 3× `<linearGradient>` fills for background, cards, and chart bars.
- 1× `<radialGradient>` for a soft dashboard glow.
- 2× `<filter>` definitions using blur/offset/merge for soft card shadows and glow accents.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="55%" stop-color="#172033"/>
      <stop offset="100%" stop-color="#0b1020"/>
    </linearGradient>
    <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.98"/>
      <stop offset="100%" stop-color="#eef2f7" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="chartPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3d4450"/>
      <stop offset="100%" stop-color="#242a33"/>
    </linearGradient>
    <linearGradient id="greenBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2fe06f"/>
      <stop offset="100%" stop-color="#00a64a"/>
    </linearGradient>
    <linearGradient id="redBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff6b6b"/>
      <stop offset="100%" stop-color="#e60000"/>
    </linearGradient>
    <radialGradient id="glow" cx="78%" cy="28%" r="54%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#glow)"/>
  <path d="M48 640 C260 565, 420 660, 640 575 C830 500, 990 550, 1218 470" fill="none" stroke="#38bdf8" stroke-opacity="0.16" stroke-width="3"/>
  <path d="M1060 44 C1130 58, 1186 88, 1224 138 C1160 122, 1100 114, 1034 130 C1056 102, 1066 75, 1060 44Z" fill="#22c55e" opacity="0.12"/>

  <text x="46" y="48" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">Interactive Financial Waterfall Dashboard</text>
  <text x="48" y="77" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#b8c4d8">Static SVG snapshot of a what-if P&amp;L model: cost sliders, conditional table, and profit bridge visualization.</text>
  <rect x="1030" y="34" width="190" height="40" rx="20" fill="#102a1b" stroke="#20c867" stroke-width="1"/>
  <circle cx="1052" cy="54" r="5" fill="#22c55e"/>
  <text x="1070" y="59" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#c7f9d4">Scenario: Base Case</text>

  <rect x="38" y="105" width="287" height="545" rx="24" fill="url(#panel)" filter="url(#shadow)"/>
  <text x="66" y="145" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#111827">What-if controls</text>
  <text x="66" y="169" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748b">Drag-style inputs shown as editable shapes</text>

  <rect x="66" y="205" width="230" height="126" rx="18" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="84" y="235" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0f172a">Cost of Revenue</text>
  <rect x="218" y="218" width="58" height="26" rx="13" fill="#fff7ed" stroke="#fb923c"/>
  <text x="230" y="237" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#c2410c">400</text>
  <rect x="84" y="265" width="174" height="8" rx="4" fill="#dbe4ef"/>
  <rect x="84" y="265" width="69" height="8" rx="4" fill="#fb923c"/>
  <circle cx="153" cy="269" r="14" fill="#ffffff" stroke="#f97316" stroke-width="4"/>
  <text x="84" y="304" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748b">200</text>
  <text x="224" y="304" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748b">700</text>

  <rect x="66" y="352" width="230" height="126" rx="18" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="84" y="382" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0f172a">Sales Expenses</text>
  <rect x="218" y="365" width="58" height="26" rx="13" fill="#fff7ed" stroke="#fb923c"/>
  <text x="230" y="384" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#c2410c">250</text>
  <rect x="84" y="412" width="174" height="8" rx="4" fill="#dbe4ef"/>
  <rect x="84" y="412" width="82" height="8" rx="4" fill="#fb923c"/>
  <circle cx="166" cy="416" r="14" fill="#ffffff" stroke="#f97316" stroke-width="4"/>
  <text x="84" y="451" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748b">100</text>
  <text x="224" y="451" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748b">500</text>

  <rect x="66" y="512" width="230" height="92" rx="18" fill="#0f172a"/>
  <text x="84" y="542" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff">Operating Profit</text>
  <text x="84" y="582" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#22c55e">1,050</text>
  <text x="186" y="580" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#a7f3d0">52.5% margin</text>

  <rect x="355" y="105" width="350" height="545" rx="24" fill="url(#panel)" filter="url(#shadow)"/>
  <text x="383" y="145" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#111827">Profit &amp; Loss Account</text>
  <text x="383" y="169" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748b">Conditional highlights flag controllable expense ratios</text>

  <rect x="383" y="205" width="294" height="42" rx="10" fill="#1f2937"/>
  <text x="398" y="231" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Account</text>
  <text x="528" y="231" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Amount</text>
  <text x="603" y="231" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">% Rev</text>

  <rect x="383" y="247" width="294" height="42" fill="#ffffff"/><text x="398" y="273" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Revenue</text><text x="528" y="273" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">2,000</text><text x="612" y="273" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">100%</text>
  <rect x="383" y="289" width="294" height="42" fill="#f8fafc"/><rect x="602" y="296" width="58" height="28" rx="7" fill="#ffc000"/><text x="398" y="315" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">CoR</text><text x="528" y="315" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">400</text><text x="615" y="315" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">20%</text>
  <rect x="383" y="331" width="294" height="42" fill="#ffffff"/><text x="398" y="357" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Gross Profit</text><text x="528" y="357" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">1,600</text><text x="612" y="357" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">80%</text>
  <rect x="383" y="373" width="294" height="42" fill="#f8fafc"/><rect x="602" y="380" width="58" height="28" rx="7" fill="#ffc000"/><text x="398" y="399" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Sales Expenses</text><text x="528" y="399" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">250</text><text x="615" y="399" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">13%</text>
  <rect x="383" y="415" width="294" height="42" fill="#ffffff"/><rect x="602" y="422" width="58" height="28" rx="7" fill="#ffc000"/><text x="398" y="441" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">G&amp;A</text><text x="528" y="441" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">300</text><text x="615" y="441" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">15%</text>
  <rect x="383" y="457" width="294" height="50" rx="10" fill="#dcfce7" stroke="#86efac"/><text x="398" y="489" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#14532d">Operating Profit</text><text x="528" y="489" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#14532d">1,050</text><text x="612" y="489" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#14532d">53%</text>

  <line x1="383" y1="247" x2="677" y2="247" stroke="#e5e7eb"/><line x1="383" y1="331" x2="677" y2="331" stroke="#e5e7eb"/><line x1="383" y1="415" x2="677" y2="415" stroke="#e5e7eb"/>
  <line x1="518" y1="205" x2="518" y2="507" stroke="#e5e7eb"/><line x1="596" y1="205" x2="596" y2="507" stroke="#e5e7eb"/>

  <rect x="745" y="105" width="495" height="545" rx="24" fill="url(#chartPanel)" filter="url(#shadow)"/>
  <text x="775" y="145" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#ffffff">Waterfall impact bridge</text>
  <text x="775" y="169" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cbd5e1">How revenue converts into operating profit under current assumptions</text>
  <rect x="1108" y="126" width="92" height="30" rx="15" fill="#064e3b" stroke="#22c55e"/>
  <text x="1124" y="146" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#bbf7d0">+1,050</text>

  <line x1="785" y1="485" x2="1195" y2="485" stroke="#94a3b8" stroke-width="1"/>
  <line x1="785" y1="415" x2="1195" y2="415" stroke="#94a3b8" stroke-opacity="0.22" stroke-dasharray="5 6"/>
  <line x1="785" y1="345" x2="1195" y2="345" stroke="#94a3b8" stroke-opacity="0.22" stroke-dasharray="5 6"/>
  <line x1="785" y1="275" x2="1195" y2="275" stroke="#94a3b8" stroke-opacity="0.22" stroke-dasharray="5 6"/>
  <line x1="785" y1="205" x2="1195" y2="205" stroke="#94a3b8" stroke-opacity="0.22" stroke-dasharray="5 6"/>

  <rect x="800" y="199" width="48" height="286" rx="8" fill="url(#greenBar)"/>
  <rect x="865" y="199" width="48" height="57" rx="8" fill="url(#redBar)"/>
  <rect x="930" y="256" width="48" height="229" rx="8" fill="url(#greenBar)"/>
  <rect x="995" y="256" width="48" height="36" rx="8" fill="url(#redBar)"/>
  <rect x="1060" y="292" width="48" height="43" rx="8" fill="url(#redBar)"/>
  <rect x="1125" y="335" width="48" height="150" rx="8" fill="url(#greenBar)"/>

  <line x1="848" y1="199" x2="865" y2="199" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="913" y1="256" x2="930" y2="256" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="978" y1="256" x2="995" y2="256" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="1043" y1="292" x2="1060" y2="292" stroke="#cbd5e1" stroke-width="2"/>
  <line x1="1108" y1="335" x2="1125" y2="335" stroke="#cbd5e1" stroke-width="2"/>

  <text x="798" y="189" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#bbf7d0">2,000</text>
  <text x="866" y="190" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fecaca">-400</text>
  <text x="928" y="246" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#bbf7d0">1,600</text>
  <text x="997" y="246" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fecaca">-250</text>
  <text x="1062" y="282" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#fecaca">-300</text>
  <text x="1126" y="325" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#bbf7d0">1,050</text>

  <text x="793" y="520" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#e2e8f0">Revenue</text>
  <text x="872" y="520" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#e2e8f0">CoR</text>
  <text x="922" y="520" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#e2e8f0">Gross Profit</text>
  <text x="988" y="520" width="75" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#e2e8f0">Sales Exp.</text>
  <text x="1067" y="520" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#e2e8f0">G&amp;A</text>
  <text x="1112" y="520" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#e2e8f0">Operating Profit</text>

  <rect x="780" y="562" width="184" height="52" rx="16" fill="#111827" stroke="#334155"/>
  <rect x="984" y="562" width="214" height="52" rx="16" fill="#111827" stroke="#334155"/>
  <circle cx="805" cy="588" r="7" fill="#ef4444" filter="url(#softGlow)"/>
  <text x="824" y="584" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Expenses consume</text>
  <text x="824" y="602" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cbd5e1">47.5% of revenue</text>
  <circle cx="1009" cy="588" r="7" fill="#22c55e" filter="url(#softGlow)"/>
  <text x="1028" y="584" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">Profit retained</text>
  <text x="1028" y="602" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#cbd5e1">Healthy margin buffer</text>
</svg>
```

## Avoid in this skill
- ❌ Real Excel/PPT form controls or formulas; represent interactivity as slider-like editable SVG shapes.
- ❌ Native PowerPoint chart objects if the goal is full SVG-to-shape editability; build the waterfall from rectangles and connector lines.
- ❌ `marker-end` arrows on paths for financial flow annotations; use plain `<line>` or custom small paths instead.
- ❌ Filters on `<line>` gridlines or connectors; apply shadows/glows only to cards, bars, or text.
- ❌ Text without explicit `width`; dashboard labels are dense and must render predictably in PowerPoint.

## Composition notes
- Use a three-zone executive dashboard: controls left, P&L table center, waterfall chart right; the chart should own roughly 40% of slide width.
- Keep the table visually functional but premium: white card, dark header, light gridlines, and gold conditional-format badges for expense ratios.
- The waterfall panel works best on a dark charcoal background so green positive bars and red expense bars read instantly.
- Treat sliders as “static interaction cues”: show track, filled progress, thumb, min/max ticks, and a numeric value chip to imply live scenario control.