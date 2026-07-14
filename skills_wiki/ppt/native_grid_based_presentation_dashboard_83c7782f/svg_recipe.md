# SVG Recipe — Native Grid-Based Presentation Dashboard

## Visual mechanism
A static, fully editable dashboard mimics an Excel-style pivot dashboard inside a PowerPoint slide: top-row slicer pills establish the filtered context, while a disciplined grid of native vector chart panels creates the illusion of a polished BI workspace without embedded OLE objects or screenshots.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× `<linearGradient>` for a premium dark-to-white dashboard header accent
- 2× `<filter>` definitions for soft panel shadows and subtle glow accents
- 10× `<rect>` for dashboard cards, slicer buttons, KPI tiles, and chart plot backgrounds
- 20+× `<line>` for chart gridlines, axes, separators, and tick marks
- 18× `<rect>` for bar and column chart data marks
- 1× `<path>` for the line chart trend stroke
- 5× `<circle>` for line chart markers
- 3× `<path>` for small native “Excel / PowerPoint / filter” UI-style icons
- Multiple `<text>` elements with explicit `width` for titles, labels, slicers, chart captions, and KPI values
- Nested `<tspan>` inside the main title for inline color styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0E1F2A"/>
      <stop offset="0.55" stop-color="#123E4B"/>
      <stop offset="1" stop-color="#1B8A70"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#39D98A"/>
      <stop offset="1" stop-color="#0F8F5D"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF8A5B"/>
      <stop offset="1" stop-color="#D84B2A"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F6F8FB"/>
  <rect x="0" y="0" width="1280" height="126" fill="url(#headerGrad)"/>
  <circle cx="1130" cy="48" r="72" fill="#45D3C2" opacity="0.14" filter="url(#softGlow)"/>
  <circle cx="1210" cy="95" r="112" fill="#FFFFFF" opacity="0.06" filter="url(#softGlow)"/>

  <text x="46" y="56" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">
    Native <tspan fill="#41D98E">Excel Dashboard</tspan>
  </text>
  <text x="49" y="91" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#CFE7EA">
    Executive presentation view · no OLE object · every chart element remains editable
  </text>

  <rect x="822" y="28" width="78" height="52" rx="12" fill="#107C41"/>
  <path d="M846 42 L866 42 L882 66 L862 66 Z" fill="#FFFFFF" opacity="0.95"/>
  <text x="837" y="69" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#107C41">X</text>
  <text x="913" y="63" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">in</text>
  <rect x="962" y="28" width="78" height="52" rx="12" fill="#C7432A"/>
  <path d="M985 42 L1014 42 L1026 54 L1026 66 L985 66 Z" fill="#FFFFFF" opacity="0.95"/>
  <text x="993" y="68" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#C7432A">P</text>

  <rect x="44" y="148" width="1192" height="62" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="70" y="185" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#4A5568">Slicers</text>
  <rect x="156" y="163" width="142" height="32" rx="16" fill="url(#greenGrad)"/>
  <text x="182" y="184" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Bikes</text>
  <rect x="312" y="163" width="142" height="32" rx="16" fill="#F2F5F8" stroke="#CBD5E1"/>
  <text x="335" y="184" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#516070">Accessories</text>
  <rect x="468" y="163" width="142" height="32" rx="16" fill="#F2F5F8" stroke="#CBD5E1"/>
  <text x="496" y="184" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#516070">Clothing</text>
  <rect x="624" y="163" width="142" height="32" rx="16" fill="#F2F5F8" stroke="#CBD5E1"/>
  <text x="648" y="184" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#516070">Components</text>
  <path d="M1138 164 L1186 164 L1167 184 L1167 195 L1157 199 L1157 184 Z" fill="#94A3B8"/>
  <text x="1040" y="185" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#64748B">FY 2024</text>

  <rect x="44" y="232" width="278" height="116" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="70" y="266" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Revenue</text>
  <text x="70" y="314" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#172033">$4.82M</text>
  <text x="228" y="314" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#12A66A">▲ 18%</text>

  <rect x="344" y="232" width="278" height="116" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="370" y="266" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Gross Margin</text>
  <text x="370" y="314" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#172033">38.6%</text>
  <text x="522" y="314" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#12A66A">▲ 4.1</text>

  <rect x="644" y="232" width="278" height="116" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="670" y="266" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Orders</text>
  <text x="670" y="314" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#172033">29.4K</text>
  <text x="824" y="314" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E05A35">▼ 2%</text>

  <rect x="944" y="232" width="292" height="116" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="970" y="266" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Avg. Deal Size</text>
  <text x="970" y="314" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#172033">$164</text>
  <text x="1124" y="314" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#12A66A">▲ 7%</text>

  <rect x="44" y="374" width="390" height="294" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="70" y="410" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#172033">Sales by Category</text>
  <line x1="116" y1="444" x2="390" y2="444" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="116" y1="492" x2="390" y2="492" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="116" y1="540" x2="390" y2="540" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="116" y1="588" x2="390" y2="588" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="116" y1="636" x2="390" y2="636" stroke="#CBD5E1"/>
  <text x="70" y="459" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Bikes</text>
  <text x="70" y="507" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Components</text>
  <text x="70" y="555" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Accessories</text>
  <text x="70" y="603" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Clothing</text>
  <rect x="116" y="431" width="248" height="24" rx="12" fill="url(#greenGrad)"/>
  <rect x="116" y="479" width="210" height="24" rx="12" fill="#26A6D1"/>
  <rect x="116" y="527" width="158" height="24" rx="12" fill="#7C6BEA"/>
  <rect x="116" y="575" width="112" height="24" rx="12" fill="url(#orangeGrad)"/>

  <rect x="462" y="374" width="774" height="294" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="492" y="410" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#172033">Revenue Trend and YoY Lift</text>
  <line x1="512" y1="630" x2="806" y2="630" stroke="#CBD5E1"/>
  <line x1="512" y1="450" x2="512" y2="630" stroke="#CBD5E1"/>
  <line x1="512" y1="585" x2="806" y2="585" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="512" y1="540" x2="806" y2="540" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="512" y1="495" x2="806" y2="495" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <path d="M520 590 C555 560 585 575 620 528 S690 468 730 502 S775 548 804 462" fill="none" stroke="#10B981" stroke-width="6" stroke-linecap="round"/>
  <circle cx="520" cy="590" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="4"/>
  <circle cx="620" cy="528" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="4"/>
  <circle cx="690" cy="468" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="4"/>
  <circle cx="730" cy="502" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="4"/>
  <circle cx="804" cy="462" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="4"/>
  <text x="512" y="653" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">2020</text>
  <text x="608" y="653" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">2021</text>
  <text x="690" y="653" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">2022</text>
  <text x="786" y="653" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">2024</text>

  <line x1="874" y1="630" x2="1190" y2="630" stroke="#CBD5E1"/>
  <line x1="874" y1="450" x2="874" y2="630" stroke="#CBD5E1"/>
  <line x1="874" y1="585" x2="1190" y2="585" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="874" y1="540" x2="1190" y2="540" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <line x1="874" y1="495" x2="1190" y2="495" stroke="#E6ECF2" stroke-dasharray="4 6"/>
  <rect x="910" y="558" width="34" height="72" rx="6" fill="#A7F3D0"/>
  <rect x="952" y="520" width="34" height="110" rx="6" fill="#34D399"/>
  <rect x="994" y="488" width="34" height="142" rx="6" fill="#10B981"/>
  <rect x="1056" y="574" width="34" height="56" rx="6" fill="#FED7AA"/>
  <rect x="1098" y="536" width="34" height="94" rx="6" fill="#FB923C"/>
  <rect x="1140" y="506" width="34" height="124" rx="6" fill="#EA580C"/>
  <text x="908" y="653" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">Actual</text>
  <text x="1050" y="653" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">Forecast</text>
</svg>
```

## Avoid in this skill
- ❌ Embedding a screenshot of an Excel dashboard; it will blur when scaled and cannot be animated or edited.
- ❌ Real spreadsheet/OLE interactivity as the core slide object; it breaks presenter-mode flow and is not reliable for static executive decks.
- ❌ Overly tiny labels inside every chart cell; use simplified chart marks and only the labels needed to communicate the takeaway.
- ❌ `<foreignObject>` HTML tables or CSS dashboards; build the grid from native SVG shapes so PPT-Master converts them to editable PowerPoint objects.
- ❌ Masked chart panels or clipped non-image shapes; use rounded `<rect>` cards directly instead.

## Composition notes
- Keep the top 15–18% of the slide for title, source/context, and slicer simulation; the audience should immediately understand the dashboard state.
- Use a 12-column grid feel: KPI cards across the upper middle, one large categorical chart on the left, and trend/YoY analysis on the right.
- Reserve generous gutters between cards so dense data still feels executive and readable.
- Use one primary accent color for “selected / positive / Excel-native” states, with a secondary warm accent for forecast, risk, or PowerPoint comparison data.