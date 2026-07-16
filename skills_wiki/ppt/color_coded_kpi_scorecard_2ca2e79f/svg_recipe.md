# SVG Recipe — Color-Coded KPI Scorecard

## Visual mechanism
A structured grid of rounded KPI cards uses background color and a strong status band to make performance readable at a glance. Each card has a strict hierarchy: category header, KPI label, oversized metric, small target/prior comparisons, and a compact sparkline to reinforce trend direction.

## SVG primitives needed
- 1× `<rect>` for the full-slide executive dark background
- 1× `<linearGradient>` for the subtle presentation backdrop
- 1× `<filter id="cardShadow">` with `feOffset + feGaussianBlur + feMerge` applied to KPI card rectangles
- 3× `<rect>` for category header bars
- 9× `<rect>` for rounded KPI card bodies, color-coded by status
- 9× `<rect>` for narrow left status bands on each KPI card
- 9× `<line>` for internal dividers between metric and comparison footer
- 9× `<path>` for mini sparklines / trend strokes
- 9× small `<circle>` endpoints for sparkline emphasis
- Multiple `<text>` elements with explicit `width=` for slide title, period chip, category labels, KPI names, large values, and footer comparisons

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101827"/>
      <stop offset="62%" stop-color="#172033"/>
      <stop offset="100%" stop-color="#0B1020"/>
    </linearGradient>
    <linearGradient id="heroLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6EE7F9" stop-opacity="0.0"/>
      <stop offset="50%" stop-color="#6EE7F9" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#6EE7F9" stop-opacity="0.0"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M0,116 C210,68 380,150 590,100 C785,54 940,91 1280,38 L1280,0 L0,0 Z" fill="#23304A" opacity="0.55"/>
  <rect x="64" y="112" width="1152" height="2" rx="1" fill="url(#heroLine)"/>

  <text x="64" y="64" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">KPI Performance Scorecard</text>
  <text x="66" y="94" width="690" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A9B7CF">Executive snapshot · conditional color shows status against target</text>
  <rect x="1034" y="50" width="182" height="42" rx="21" fill="#FFFFFF" opacity="0.10" stroke="#FFFFFF" stroke-opacity="0.18"/>
  <text x="1058" y="77" width="138" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#E8F0FF">Q2 · Jun 2026</text>

  <rect x="64" y="138" width="354" height="38" rx="12" fill="#4B5563"/>
  <rect x="463" y="138" width="354" height="38" rx="12" fill="#2563EB"/>
  <rect x="862" y="138" width="354" height="38" rx="12" fill="#B91C1C"/>
  <text x="84" y="163" width="314" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">WORKING CAPITAL</text>
  <text x="483" y="163" width="314" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">SALES MOMENTUM</text>
  <text x="882" y="163" width="314" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">COST &amp; RISK</text>

  <rect x="64" y="194" width="354" height="132" rx="18" fill="#E8F5E9" filter="url(#cardShadow)"/>
  <rect x="64" y="194" width="10" height="132" rx="5" fill="#16A34A"/>
  <text x="90" y="222" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Cash Conversion Cycle</text>
  <text x="90" y="270" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">38<tspan font-size="22" font-weight="700">d</tspan></text>
  <text x="268" y="238" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#15803D">● ON TRACK</text>
  <path d="M268,276 C288,260 303,284 322,266 C338,251 356,258 378,238" fill="none" stroke="#16A34A" stroke-width="4" stroke-linecap="round"/>
  <circle cx="378" cy="238" r="4" fill="#16A34A"/>
  <line x1="90" y1="294" x2="392" y2="294" stroke="#B8C7B7" stroke-width="1"/>
  <text x="90" y="314" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 42d</text>
  <text x="250" y="314" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 45d</text>

  <rect x="463" y="194" width="354" height="132" rx="18" fill="#E8F5E9" filter="url(#cardShadow)"/>
  <rect x="463" y="194" width="10" height="132" rx="5" fill="#16A34A"/>
  <text x="489" y="222" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Revenue Attainment</text>
  <text x="489" y="270" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">107<tspan font-size="22">%</tspan></text>
  <text x="667" y="238" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#15803D">● ABOVE</text>
  <path d="M667,278 C685,270 699,268 716,252 C735,234 750,248 777,220" fill="none" stroke="#16A34A" stroke-width="4" stroke-linecap="round"/>
  <circle cx="777" cy="220" r="4" fill="#16A34A"/>
  <line x1="489" y1="294" x2="791" y2="294" stroke="#B8C7B7" stroke-width="1"/>
  <text x="489" y="314" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 100%</text>
  <text x="649" y="314" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 101%</text>

  <rect x="862" y="194" width="354" height="132" rx="18" fill="#FDECEC" filter="url(#cardShadow)"/>
  <rect x="862" y="194" width="10" height="132" rx="5" fill="#DC2626"/>
  <text x="888" y="222" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Operating Expense Ratio</text>
  <text x="888" y="270" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">31<tspan font-size="22">%</tspan></text>
  <text x="1066" y="238" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B91C1C">● WATCH</text>
  <path d="M1066,244 C1085,258 1098,248 1116,266 C1138,289 1152,276 1176,294" fill="none" stroke="#DC2626" stroke-width="4" stroke-linecap="round"/>
  <circle cx="1176" cy="294" r="4" fill="#DC2626"/>
  <line x1="888" y1="294" x2="1190" y2="294" stroke="#E3B8B8" stroke-width="1"/>
  <text x="888" y="314" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 28%</text>
  <text x="1048" y="314" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 29%</text>

  <rect x="64" y="350" width="354" height="132" rx="18" fill="#FFF4D8" filter="url(#cardShadow)"/>
  <rect x="64" y="350" width="10" height="132" rx="5" fill="#D97706"/>
  <text x="90" y="378" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Inventory Turns</text>
  <text x="90" y="426" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">7.8<tspan font-size="22">×</tspan></text>
  <text x="268" y="394" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B45309">● NEAR</text>
  <path d="M268,424 C286,417 303,427 322,416 C342,405 358,414 378,404" fill="none" stroke="#D97706" stroke-width="4" stroke-linecap="round"/>
  <circle cx="378" cy="404" r="4" fill="#D97706"/>
  <line x1="90" y1="450" x2="392" y2="450" stroke="#DEC88C" stroke-width="1"/>
  <text x="90" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 8.0×</text>
  <text x="250" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 7.4×</text>

  <rect x="463" y="350" width="354" height="132" rx="18" fill="#FDECEC" filter="url(#cardShadow)"/>
  <rect x="463" y="350" width="10" height="132" rx="5" fill="#DC2626"/>
  <text x="489" y="378" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Net New Pipeline</text>
  <text x="489" y="426" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">$42<tspan font-size="22">M</tspan></text>
  <text x="667" y="394" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B91C1C">● BELOW</text>
  <path d="M667,396 C688,405 702,398 719,416 C739,438 756,430 777,446" fill="none" stroke="#DC2626" stroke-width="4" stroke-linecap="round"/>
  <circle cx="777" cy="446" r="4" fill="#DC2626"/>
  <line x1="489" y1="450" x2="791" y2="450" stroke="#E3B8B8" stroke-width="1"/>
  <text x="489" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: $50M</text>
  <text x="649" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: $48M</text>

  <rect x="862" y="350" width="354" height="132" rx="18" fill="#E8F5E9" filter="url(#cardShadow)"/>
  <rect x="862" y="350" width="10" height="132" rx="5" fill="#16A34A"/>
  <text x="888" y="378" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Gross Margin</text>
  <text x="888" y="426" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">58<tspan font-size="22">%</tspan></text>
  <text x="1066" y="394" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#15803D">● ABOVE</text>
  <path d="M1066,434 C1086,426 1098,416 1118,419 C1139,421 1154,399 1176,390" fill="none" stroke="#16A34A" stroke-width="4" stroke-linecap="round"/>
  <circle cx="1176" cy="390" r="4" fill="#16A34A"/>
  <line x1="888" y1="450" x2="1190" y2="450" stroke="#B8C7B7" stroke-width="1"/>
  <text x="888" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 55%</text>
  <text x="1048" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 56%</text>

  <rect x="64" y="506" width="354" height="132" rx="18" fill="#E8F5E9" filter="url(#cardShadow)"/>
  <rect x="64" y="506" width="10" height="132" rx="5" fill="#16A34A"/>
  <text x="90" y="534" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">DSO</text>
  <text x="90" y="582" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">41<tspan font-size="22">d</tspan></text>
  <text x="268" y="550" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#15803D">● BETTER</text>
  <path d="M268,586 C286,579 304,560 322,568 C342,575 356,548 378,540" fill="none" stroke="#16A34A" stroke-width="4" stroke-linecap="round"/>
  <circle cx="378" cy="540" r="4" fill="#16A34A"/>
  <line x1="90" y1="606" x2="392" y2="606" stroke="#B8C7B7" stroke-width="1"/>
  <text x="90" y="626" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 45d</text>
  <text x="250" y="626" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 49d</text>

  <rect x="463" y="506" width="354" height="132" rx="18" fill="#E8F5E9" filter="url(#cardShadow)"/>
  <rect x="463" y="506" width="10" height="132" rx="5" fill="#16A34A"/>
  <text x="489" y="534" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Logo Retention</text>
  <text x="489" y="582" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">96<tspan font-size="22">%</tspan></text>
  <text x="667" y="550" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#15803D">● STABLE</text>
  <path d="M667,568 C686,562 704,570 722,563 C740,556 758,560 777,552" fill="none" stroke="#16A34A" stroke-width="4" stroke-linecap="round"/>
  <circle cx="777" cy="552" r="4" fill="#16A34A"/>
  <line x1="489" y1="606" x2="791" y2="606" stroke="#B8C7B7" stroke-width="1"/>
  <text x="489" y="626" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: 94%</text>
  <text x="649" y="626" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 95%</text>

  <rect x="862" y="506" width="354" height="132" rx="18" fill="#FDECEC" filter="url(#cardShadow)"/>
  <rect x="862" y="506" width="10" height="132" rx="5" fill="#DC2626"/>
  <text x="888" y="534" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Open Risk Items</text>
  <text x="888" y="582" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#1F2937">18</text>
  <text x="1066" y="550" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B91C1C">● HIGH</text>
  <path d="M1066,548 C1088,552 1098,566 1118,560 C1138,555 1158,584 1176,590" fill="none" stroke="#DC2626" stroke-width="4" stroke-linecap="round"/>
  <circle cx="1176" cy="590" r="4" fill="#DC2626"/>
  <line x1="888" y1="606" x2="1190" y2="606" stroke="#E3B8B8" stroke-width="1"/>
  <text x="888" y="626" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Target: ≤12</text>
  <text x="1048" y="626" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Prior: 14</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on red/green alone; add status text, bands, or dots so the meaning survives projection and color-blind viewing.
- ❌ Do not put `filter` on `<line>` sparklines; apply shadows only to card `<rect>` elements.
- ❌ Do not cram full tables into the cards; KPI cards need one dominant number and two or three supporting facts.
- ❌ Do not use `clip-path` on card rectangles to fake angled corners; use rounded `<rect>` and simple status bands for reliable editable PowerPoint output.

## Composition notes
- Keep the slide title and period metadata in the top 15% of the canvas; the KPI grid should own the main visual field.
- Use three equal-width columns for categories and consistent card height/gutters so executives can scan vertically and compare horizontally.
- Let the large metric number occupy the center-left of each card; place trend/status evidence on the right to avoid competing focal points.
- Use muted pastel card fills with saturated status bands, so color communicates urgency without making the dashboard feel noisy.