# SVG Recipe — Corporate Dashboard with Data Cards

## Visual mechanism
A premium corporate dashboard is built from a disciplined grid of elevated white cards on a soft gray canvas, with one strong accent color used for KPIs, chart emphasis, and status cues. The slide feels like an executive analytics product: modular, calm, scannable, and data-dense without becoming visually noisy.

## SVG primitives needed
- 1× `<rect>` for the full-slide light gray background
- 1× `<rect>` for the thin top corporate accent rule
- 9× `<rect>` for elevated data cards with subtle borders and shadows
- 8× `<rect>` for KPI progress tracks and fills
- 10× `<rect>` for bar chart columns and mini table rows
- 8× `<line>` for chart gridlines and table separators
- 7× `<circle>` for status dots, KPI icons, and highlighted chart points
- 10× `<path>` for sparkline charts, area chart fill, trend arrows, icons, and decorative dashboard accents
- 1× `<linearGradient>` for the orange top rule
- 1× `<linearGradient>` for the soft orange chart area fill
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` applied to card rectangles
- 1× `<filter id="softGlow">` using `feGaussianBlur` applied to the highlighted chart point
- Multiple `<text>` elements with explicit `width` attributes for slide title, KPI labels, values, table cells, and chart annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="topAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ED7D31"/>
      <stop offset="65%" stop-color="#F5B482"/>
      <stop offset="100%" stop-color="#ED7D31"/>
    </linearGradient>
    <linearGradient id="areaOrange" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ED7D31" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#ED7D31" stop-opacity="0.03"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .12 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8F8F8"/>
  <rect x="48" y="0" width="1184" height="8" fill="url(#topAccent)"/>

  <text x="48" y="52" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#404040">Sales Review: Current Pipeline</text>
  <text x="48" y="82" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#969696">Q3 executive dashboard · revenue, margin, partner health, and regional momentum</text>
  <text x="1050" y="52" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#969696" text-anchor="end">Updated 18 Oct 2026</text>

  <rect x="48" y="112" width="274" height="150" rx="14" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <circle cx="76" cy="142" r="12" fill="#FFF1E8"/>
  <path d="M71 144 L76 136 L81 144 Z" fill="#ED7D31"/>
  <text x="98" y="147" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#666666">TOTAL REVENUE</text>
  <text x="72" y="194" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#ED7D31">$44.2M</text>
  <text x="235" y="194" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#42A66A">+5.3%</text>
  <rect x="72" y="222" width="210" height="8" rx="4" fill="#EEEEEE"/>
  <rect x="72" y="222" width="168" height="8" rx="4" fill="#ED7D31"/>
  <text x="72" y="246" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">80% of annual plan secured</text>

  <rect x="342" y="112" width="274" height="150" rx="14" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <circle cx="370" cy="142" r="12" fill="#FFF1E8"/>
  <path d="M363 146 C367 134, 376 134, 380 146" fill="none" stroke="#ED7D31" stroke-width="3" stroke-linecap="round"/>
  <text x="392" y="147" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#666666">EBITDA MARGIN</text>
  <text x="366" y="194" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#404040">18.5%</text>
  <text x="529" y="194" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#42A66A">+1.8</text>
  <rect x="366" y="222" width="210" height="8" rx="4" fill="#EEEEEE"/>
  <rect x="366" y="222" width="126" height="8" rx="4" fill="#ED7D31"/>
  <text x="366" y="246" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">Mix shift improving margin quality</text>

  <rect x="636" y="112" width="274" height="150" rx="14" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <circle cx="664" cy="142" r="12" fill="#FFF1E8"/>
  <path d="M657 147 C660 138, 668 138, 671 147 M653 147 C657 134, 674 134, 678 147" fill="none" stroke="#ED7D31" stroke-width="2.5" stroke-linecap="round"/>
  <text x="686" y="147" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#666666">ACTIVE PARTNERS</text>
  <text x="660" y="194" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#404040">102</text>
  <text x="805" y="194" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#42A66A">On track</text>
  <rect x="660" y="222" width="210" height="8" rx="4" fill="#EEEEEE"/>
  <rect x="660" y="222" width="189" height="8" rx="4" fill="#ED7D31"/>
  <text x="660" y="246" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">Strong renewal momentum in enterprise</text>

  <rect x="930" y="112" width="302" height="150" rx="14" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <circle cx="958" cy="142" r="12" fill="#FFF1E8"/>
  <path d="M952 146 L958 135 L964 146 Z M958 135 L958 149" fill="none" stroke="#ED7D31" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="980" y="147" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#666666">KEY MARKETS</text>
  <text x="954" y="194" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#404040">13</text>
  <text x="1082" y="194" width="115" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ED7D31">Needs review</text>
  <rect x="954" y="222" width="230" height="8" rx="4" fill="#EEEEEE"/>
  <rect x="954" y="222" width="92" height="8" rx="4" fill="#ED7D31"/>
  <text x="954" y="246" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">APAC conversion below benchmark</text>

  <rect x="48" y="290" width="704" height="372" rx="16" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <text x="78" y="330" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040">Pipeline Value by Quarter</text>
  <text x="78" y="352" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A6A6A6">Weighted pipeline, bookings, and forecast confidence</text>
  <text x="612" y="330" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A6A6A6" text-anchor="end">USD millions</text>

  <line x1="92" y1="580" x2="710" y2="580" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="92" y1="526" x2="710" y2="526" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="92" y1="472" x2="710" y2="472" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="92" y1="418" x2="710" y2="418" stroke="#EEEEEE" stroke-width="1"/>
  <path d="M100 555 C165 535, 190 510, 245 520 C318 534, 330 465, 395 474 C458 482, 470 425, 535 432 C602 440, 628 378, 700 388 L700 580 L100 580 Z" fill="url(#areaOrange)"/>
  <path d="M100 555 C165 535, 190 510, 245 520 C318 534, 330 465, 395 474 C458 482, 470 425, 535 432 C602 440, 628 378, 700 388" fill="none" stroke="#ED7D31" stroke-width="4" stroke-linecap="round"/>
  <path d="M100 565 C165 548, 206 542, 260 548 C330 554, 365 518, 420 526 C495 537, 535 490, 590 500 C640 508, 670 458, 700 466" fill="none" stroke="#B8B8B8" stroke-width="3" stroke-linecap="round" stroke-dasharray="7 7"/>
  <circle cx="700" cy="388" r="8" fill="#ED7D31" filter="url(#softGlow)"/>
  <circle cx="700" cy="388" r="4" fill="#FFFFFF"/>
  <text x="666" y="370" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ED7D31">44.2</text>

  <text x="98" y="606" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">Q1</text>
  <text x="244" y="606" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">Q2</text>
  <text x="390" y="606" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">Q3</text>
  <text x="536" y="606" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#A6A6A6">Q4</text>
  <circle cx="108" cy="636" r="5" fill="#ED7D31"/>
  <text x="120" y="640" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">Current forecast</text>
  <circle cx="250" cy="636" r="5" fill="#B8B8B8"/>
  <text x="262" y="640" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">Prior forecast</text>

  <rect x="780" y="290" width="452" height="172" rx="16" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <text x="810" y="330" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040">Regional Mix</text>
  <text x="810" y="352" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A6A6A6">Contribution to qualified pipeline</text>
  <rect x="826" y="405" width="42" height="28" rx="4" fill="#ED7D31"/>
  <rect x="884" y="382" width="42" height="51" rx="4" fill="#F5B482"/>
  <rect x="942" y="358" width="42" height="75" rx="4" fill="#ED7D31"/>
  <rect x="1000" y="395" width="42" height="38" rx="4" fill="#F5B482"/>
  <rect x="1058" y="342" width="42" height="91" rx="4" fill="#ED7D31"/>
  <rect x="1116" y="374" width="42" height="59" rx="4" fill="#F5B482"/>
  <line x1="810" y1="434" x2="1178" y2="434" stroke="#EEEEEE" stroke-width="1"/>
  <text x="822" y="451" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A6A6A6">NA</text>
  <text x="884" y="451" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A6A6A6">UK</text>
  <text x="940" y="451" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A6A6A6">EU</text>
  <text x="998" y="451" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A6A6A6">LATAM</text>
  <text x="1056" y="451" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#A6A6A6">APAC</text>

  <rect x="780" y="490" width="452" height="172" rx="16" fill="#FFFFFF" stroke="#E8E8E8" filter="url(#cardShadow)"/>
  <text x="810" y="530" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040">Priority Accounts</text>
  <text x="810" y="552" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A6A6A6">Top opportunities requiring executive sponsorship</text>
  <rect x="810" y="572" width="388" height="26" rx="6" fill="#FFF1E8"/>
  <text x="826" y="590" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#ED7D31">ACCOUNT</text>
  <text x="1000" y="590" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#ED7D31">VALUE</text>
  <text x="1110" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#ED7D31">STATUS</text>
  <line x1="810" y1="614" x2="1198" y2="614" stroke="#EEEEEE" stroke-width="1"/>
  <text x="826" y="633" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#404040">Northstar Bank</text>
  <text x="1000" y="633" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#404040">$6.8M</text>
  <circle cx="1120" cy="629" r="5" fill="#42A66A"/>
  <text x="1132" y="633" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#666666">Commit</text>
  <line x1="810" y1="646" x2="1198" y2="646" stroke="#EEEEEE" stroke-width="1"/>
  <text x="826" y="665" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#404040">Orion Retail</text>
  <text x="1000" y="665" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#404040">$4.1M</text>
  <circle cx="1120" cy="661" r="5" fill="#ED7D31"/>
  <text x="1132" y="665" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#666666">Risk</text>
</svg>
```

## Avoid in this skill
- ❌ Embedding raster screenshots of charts when the chart can be recreated with editable SVG paths, rectangles, and text
- ❌ Overusing accent colors; this technique depends on one dominant corporate accent plus restrained neutrals
- ❌ Dense axis labels, legends, and table borders that make the dashboard feel like a spreadsheet
- ❌ Applying filters to `<line>` elements for gridlines or dividers; keep shadows on card rectangles instead
- ❌ Using `<foreignObject>` for HTML tables; build tables from native SVG rectangles, lines, and text

## Composition notes
- Keep the top 25% of the slide for four KPI cards; they should read instantly from left to right.
- Use the bottom-left 55–60% for the primary analytical visual, usually a large line/area chart or waterfall.
- Reserve the right column for supporting modules: regional mix, account table, risk notes, or executive actions.
- Maintain generous internal padding inside every card, and repeat the orange accent only on key numbers, chart highlights, and active status indicators.