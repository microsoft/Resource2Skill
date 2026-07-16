# SVG Recipe — Dynamic KPI Dashboard with Interactive Slicers

## Visual mechanism
A BI-style executive dashboard uses a fixed grid: branded header, KPI scorecards, a left rail of slicer controls, and a 2×2 chart matrix. “Interactivity” is represented visually with selected slicer chips, timeline handles, hover-like highlights, and linked accent colors, while the output remains fully editable PowerPoint shapes.

## SVG primitives needed
- 1× full-slide `<rect>` for the white dashboard background
- 1× header `<rect>` with gradient fill for brand/title area
- 3× KPI card `<rect>` containers with shadow filter, plus small accent bars
- 3× KPI icon `<path>` mini-glyphs to make scorecards feel like product UI
- 4× slicer panel `<rect>` groups for category, size, region, and timeline filters
- 18× slicer chip `<rect>` buttons with selected/unselected states
- 4× chart card `<rect>` containers with shadows and chart titles
- Multiple `<path>` wedges for a donut/pie-style category share chart
- Multiple `<rect>` bars for horizontal ranking and stacked bar charts
- 1× stroked `<path>` for a trend line, plus `<circle>` points
- 1× `<filter id="softShadow">` applied to cards and panels
- 1× `<linearGradient>` for the header and 1× subtle card gradient
- Many `<text width="...">` labels, values, legends, axes, and slicer captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7A0000"/>
      <stop offset="58%" stop-color="#9B1010"/>
      <stop offset="100%" stop-color="#C0504D"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FBF6F3"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="86" fill="url(#headerGrad)"/>
  <path d="M1040 0 C1110 22 1158 62 1280 42 L1280 0 Z" fill="#D76B64" opacity="0.35"/>
  <text x="38" y="54" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#FFFFFF">PIZZA SALES PERFORMANCE</text>
  <text x="910" y="36" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFE5E1">Live dashboard view · Q1–Q4 2024</text>
  <text x="910" y="61" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFD0CA">Static slicer mockup for editable PPT</text>

  <g font-family="Segoe UI, Microsoft YaHei">
    <rect x="28" y="112" width="228" height="558" rx="18" fill="#FFF4EF" stroke="#E0B5A7" filter="url(#softShadow)"/>
    <text x="48" y="145" width="180" font-size="15" font-weight="700" fill="#7A0000">INTERACTIVE SLICERS</text>
    <text x="48" y="165" width="170" font-size="10" fill="#9D5B51">Selected filters shown in red</text>

    <rect x="46" y="188" width="192" height="130" rx="12" fill="#FFFFFF" stroke="#E8C3B9"/>
    <rect x="46" y="188" width="192" height="30" rx="12" fill="#C0504D"/>
    <text x="60" y="208" width="150" font-size="12" font-weight="700" fill="#FFFFFF">Pizza Category</text>
    <rect x="58" y="231" width="78" height="28" rx="14" fill="#C00000"/>
    <text x="76" y="250" width="50" font-size="11" fill="#FFFFFF">Classic</text>
    <rect x="148" y="231" width="78" height="28" rx="14" fill="#F8CBAD"/>
    <text x="168" y="250" width="46" font-size="11" fill="#6B1D18">Veggie</text>
    <rect x="58" y="270" width="78" height="28" rx="14" fill="#F8CBAD"/>
    <text x="73" y="289" width="52" font-size="11" fill="#6B1D18">Chicken</text>
    <rect x="148" y="270" width="78" height="28" rx="14" fill="#C00000"/>
    <text x="164" y="289" width="54" font-size="11" fill="#FFFFFF">Supreme</text>

    <rect x="46" y="334" width="192" height="104" rx="12" fill="#FFFFFF" stroke="#E8C3B9"/>
    <rect x="46" y="334" width="192" height="30" rx="12" fill="#C0504D"/>
    <text x="60" y="354" width="120" font-size="12" font-weight="700" fill="#FFFFFF">Pizza Size</text>
    <rect x="58" y="378" width="34" height="30" rx="8" fill="#F8CBAD"/><text x="70" y="398" width="20" font-size="11" fill="#6B1D18">S</text>
    <rect x="99" y="378" width="34" height="30" rx="8" fill="#C00000"/><text x="111" y="398" width="20" font-size="11" fill="#FFFFFF">M</text>
    <rect x="140" y="378" width="34" height="30" rx="8" fill="#C00000"/><text x="153" y="398" width="20" font-size="11" fill="#FFFFFF">L</text>
    <rect x="181" y="378" width="44" height="30" rx="8" fill="#F8CBAD"/><text x="195" y="398" width="24" font-size="11" fill="#6B1D18">XL</text>

    <rect x="46" y="454" width="192" height="108" rx="12" fill="#FFFFFF" stroke="#E8C3B9"/>
    <rect x="46" y="454" width="192" height="30" rx="12" fill="#C0504D"/>
    <text x="60" y="474" width="130" font-size="12" font-weight="700" fill="#FFFFFF">Order Channel</text>
    <rect x="58" y="496" width="168" height="24" rx="6" fill="#C00000"/><text x="72" y="513" width="130" font-size="10" fill="#FFFFFF">Online · App</text>
    <rect x="58" y="526" width="168" height="24" rx="6" fill="#F8CBAD"/><text x="72" y="543" width="130" font-size="10" fill="#6B1D18">Walk-in Restaurant</text>

    <rect x="46" y="578" width="192" height="70" rx="12" fill="#FFFFFF" stroke="#E8C3B9"/>
    <text x="60" y="600" width="120" font-size="12" font-weight="700" fill="#7A0000">Timeline</text>
    <line x1="66" y1="626" x2="218" y2="626" stroke="#E6B3A7" stroke-width="6" stroke-linecap="round"/>
    <line x1="92" y1="626" x2="186" y2="626" stroke="#C00000" stroke-width="6" stroke-linecap="round"/>
    <circle cx="92" cy="626" r="9" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <circle cx="186" cy="626" r="9" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <text x="64" y="646" width="45" font-size="9" fill="#7A4A43">Jan</text>
    <text x="180" y="646" width="45" font-size="9" fill="#7A4A43">Dec</text>

    <rect x="284" y="112" width="294" height="92" rx="16" fill="url(#cardGrad)" stroke="#E4D8D3" filter="url(#softShadow)"/>
    <rect x="284" y="112" width="8" height="92" rx="4" fill="#C00000"/>
    <path d="M322 160 l18 -30 l18 30 Z M318 166 h44 v8 h-44 Z" fill="#C0504D" opacity="0.9"/>
    <text x="380" y="146" width="160" font-size="13" fill="#6E5A55">Total Revenue</text>
    <text x="380" y="184" width="170" font-size="31" font-weight="800" fill="#202020">$817,860</text>

    <rect x="606" y="112" width="294" height="92" rx="16" fill="url(#cardGrad)" stroke="#E4D8D3" filter="url(#softShadow)"/>
    <rect x="606" y="112" width="8" height="92" rx="4" fill="#ED7D31"/>
    <path d="M646 139 h26 a7 7 0 0 1 7 7 v24 h-40 v-24 a7 7 0 0 1 7 -7 Z M650 133 h18 v8 h-18 Z" fill="#ED7D31"/>
    <text x="702" y="146" width="160" font-size="13" fill="#6E5A55">Total Orders</text>
    <text x="702" y="184" width="170" font-size="31" font-weight="800" fill="#202020">21,350</text>

    <rect x="928" y="112" width="294" height="92" rx="16" fill="url(#cardGrad)" stroke="#E4D8D3" filter="url(#softShadow)"/>
    <rect x="928" y="112" width="8" height="92" rx="4" fill="#70AD47"/>
    <path d="M971 136 c19 0 34 15 34 34 h-68 c0 -19 15 -34 34 -34 Z M963 129 h16 v10 h-16 Z" fill="#70AD47"/>
    <text x="1024" y="146" width="170" font-size="13" fill="#6E5A55">Average Order Value</text>
    <text x="1024" y="184" width="170" font-size="31" font-weight="800" fill="#202020">$38.31</text>

    <rect x="284" y="232" width="294" height="202" rx="16" fill="#FFFFFF" stroke="#E7DDD8" filter="url(#softShadow)"/>
    <text x="306" y="262" width="210" font-size="15" font-weight="700" fill="#272727">Sales by Category</text>
    <path d="M431 335 L431 272 A63 63 0 0 1 491 354 Z" fill="#C00000"/>
    <path d="M431 335 L491 354 A63 63 0 0 1 415 396 Z" fill="#ED7D31"/>
    <path d="M431 335 L415 396 A63 63 0 0 1 370 302 Z" fill="#FFC000"/>
    <path d="M431 335 L370 302 A63 63 0 0 1 431 272 Z" fill="#70AD47"/>
    <circle cx="431" cy="335" r="32" fill="#FFFFFF"/>
    <text x="405" y="339" width="58" font-size="13" font-weight="700" fill="#333333">100%</text>
    <rect x="510" y="292" width="10" height="10" fill="#C00000"/><text x="526" y="301" width="50" font-size="10" fill="#555555">Classic</text>
    <rect x="510" y="316" width="10" height="10" fill="#ED7D31"/><text x="526" y="325" width="50" font-size="10" fill="#555555">Chicken</text>
    <rect x="510" y="340" width="10" height="10" fill="#FFC000"/><text x="526" y="349" width="50" font-size="10" fill="#555555">Supreme</text>
    <rect x="510" y="364" width="10" height="10" fill="#70AD47"/><text x="526" y="373" width="50" font-size="10" fill="#555555">Veggie</text>

    <rect x="606" y="232" width="616" height="202" rx="16" fill="#FFFFFF" stroke="#E7DDD8" filter="url(#softShadow)"/>
    <text x="628" y="262" width="240" font-size="15" font-weight="700" fill="#272727">Revenue Trend by Month</text>
    <line x1="650" y1="386" x2="1172" y2="386" stroke="#ECE4E1" stroke-width="1"/>
    <line x1="650" y1="340" x2="1172" y2="340" stroke="#ECE4E1" stroke-width="1"/>
    <line x1="650" y1="294" x2="1172" y2="294" stroke="#ECE4E1" stroke-width="1"/>
    <path d="M662 370 C705 352 724 358 767 332 C814 304 846 315 884 298 C932 276 958 292 997 271 C1044 246 1083 265 1136 242" fill="none" stroke="#C00000" stroke-width="4" stroke-linecap="round" filter="url(#glow)"/>
    <circle cx="662" cy="370" r="5" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <circle cx="767" cy="332" r="5" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <circle cx="884" cy="298" r="5" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <circle cx="997" cy="271" r="5" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <circle cx="1136" cy="242" r="5" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>
    <text x="650" y="410" width="40" font-size="10" fill="#777777">Jan</text>
    <text x="760" y="410" width="40" font-size="10" fill="#777777">Mar</text>
    <text x="880" y="410" width="40" font-size="10" fill="#777777">Jun</text>
    <text x="995" y="410" width="40" font-size="10" fill="#777777">Sep</text>
    <text x="1128" y="410" width="40" font-size="10" fill="#777777">Dec</text>

    <rect x="284" y="462" width="454" height="190" rx="16" fill="#FFFFFF" stroke="#E7DDD8" filter="url(#softShadow)"/>
    <text x="306" y="492" width="240" font-size="15" font-weight="700" fill="#272727">Top Pizza Names</text>
    <text x="310" y="530" width="120" font-size="11" fill="#555555">Barbecue Chicken</text><rect x="448" y="516" width="235" height="18" rx="9" fill="#C00000"/>
    <text x="310" y="564" width="120" font-size="11" fill="#555555">Classic Deluxe</text><rect x="448" y="550" width="205" height="18" rx="9" fill="#ED7D31"/>
    <text x="310" y="598" width="120" font-size="11" fill="#555555">Thai Chicken</text><rect x="448" y="584" width="178" height="18" rx="9" fill="#FFC000"/>
    <text x="310" y="632" width="120" font-size="11" fill="#555555">Veggie Garden</text><rect x="448" y="618" width="154" height="18" rx="9" fill="#70AD47"/>

    <rect x="766" y="462" width="456" height="190" rx="16" fill="#FFFFFF" stroke="#E7DDD8" filter="url(#softShadow)"/>
    <text x="788" y="492" width="260" font-size="15" font-weight="700" fill="#272727">Sales Mix by Size</text>
    <text x="800" y="535" width="30" font-size="11" fill="#666666">S</text>
    <rect x="840" y="520" width="80" height="24" fill="#C00000"/><rect x="920" y="520" width="70" height="24" fill="#ED7D31"/><rect x="990" y="520" width="55" height="24" fill="#FFC000"/><rect x="1045" y="520" width="42" height="24" fill="#70AD47"/>
    <text x="800" y="579" width="30" font-size="11" fill="#666666">M</text>
    <rect x="840" y="564" width="110" height="24" fill="#C00000"/><rect x="950" y="564" width="84" height="24" fill="#ED7D31"/><rect x="1034" y="564" width="68" height="24" fill="#FFC000"/><rect x="1102" y="564" width="52" height="24" fill="#70AD47"/>
    <text x="800" y="623" width="30" font-size="11" fill="#666666">L</text>
    <rect x="840" y="608" width="132" height="24" fill="#C00000"/><rect x="972" y="608" width="96" height="24" fill="#ED7D31"/><rect x="1068" y="608" width="74" height="24" fill="#FFC000"/><rect x="1142" y="608" width="46" height="24" fill="#70AD47"/>
    <rect x="1014" y="484" width="10" height="10" fill="#C00000"/><text x="1030" y="493" width="55" font-size="10" fill="#555555">Classic</text>
    <rect x="1080" y="484" width="10" height="10" fill="#ED7D31"/><text x="1096" y="493" width="55" font-size="10" fill="#555555">Chicken</text>
    <rect x="1150" y="484" width="10" height="10" fill="#70AD47"/><text x="1166" y="493" width="45" font-size="10" fill="#555555">Veggie</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Real Excel/Power BI interactivity; slicers must be represented as editable visual controls, not functional filters.
- ❌ `<foreignObject>` for embedding HTML dashboard widgets; it will hard-fail translation.
- ❌ `<textPath>` or rotated axis labels on a path; use normal `<text width="...">` labels instead.
- ❌ `marker-end` arrows for trend callouts; if arrows are needed, use `<line>` with direct marker attributes or draw arrowheads manually as paths.
- ❌ Applying `filter` to `<line>` gridlines; shadows/glows should be on cards, paths, circles, or text only.
- ❌ Overcrowding with true chart-level detail; preserve the executive dashboard feel by showing representative bars, slices, and trend points.

## Composition notes
- Keep the slicer rail to the left 18–22% of the slide; it should read as a control surface, not compete with the charts.
- Use the top row for KPI cards with oversized values and tiny contextual labels; this creates immediate “health check” hierarchy.
- Place the most important trend chart in the widest card, usually upper-right, because it benefits from horizontal space.
- Repeat the red accent in slicer selections, KPI accent strips, and chart highlights so the dashboard feels linked and interactive.