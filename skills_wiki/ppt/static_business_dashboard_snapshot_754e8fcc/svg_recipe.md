# SVG Recipe — Static Business Dashboard Snapshot

## Visual mechanism
A static executive dashboard compresses business performance into a single grid: KPI cards create the top-level story, while chart cards below provide trend, category, mix, and regional context. The visual language should feel like a polished BI product—soft cards, precise alignment, restrained accent color, and chart marks drawn as editable SVG shapes rather than embedded screenshots.

## SVG primitives needed
- 1× `<rect>` for the full-slide neutral dashboard background.
- 1× `<rect>` for the accent title bar.
- 1× `<path>` for a subtle decorative highlight wave in the header.
- 1× `<rect>` for the left filter/slicer panel.
- 8× `<rect>` for static slicer pills and selected filter states.
- 4× `<rect>` for KPI cards, with shadow filter applied.
- 4× `<text>` groups for KPI labels, values, and deltas.
- 4× `<rect>` for chart card containers, with shadow filter applied.
- Multiple `<line>` elements for chart axes, gridlines, and tick marks.
- Multiple `<rect>` elements for vertical and horizontal bar charts.
- 1× `<path>` for the line-chart filled area.
- 1× `<path>` for the line-chart trend stroke.
- 6× `<circle>` for line-chart data points.
- 4× `<path>` for donut chart segments.
- Multiple `<text>` elements for chart titles, axis labels, legends, and annotations.
- 2× `<linearGradient>` definitions for header and chart-area fills.
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft card depth.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for a restrained highlight on the active KPI.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFC000"/>
      <stop offset="62%" stop-color="#FFD966"/>
      <stop offset="100%" stop-color="#FFF2CC"/>
    </linearGradient>
    <linearGradient id="areaGrad" x1="0" y1="210" x2="0" y2="380">
      <stop offset="0%" stop-color="#FFC000" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#FFC000" stop-opacity="0.04"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.12 0 0 0 0 0.10 0 0 0 0 0.05 0 0 0 0.20 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#D9D9D9"/>
  <rect x="0" y="0" width="1280" height="76" fill="url(#headerGrad)"/>
  <path d="M860,0 C980,18 1050,76 1280,38 L1280,0 Z" fill="#FFFFFF" opacity="0.25"/>
  <text x="34" y="50" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#111111">SALES DASHBOARD</text>
  <text x="1010" y="33" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#5B4300">Q1 Snapshot · Static View</text>
  <text x="1010" y="55" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6E5500">Updated 31 Mar 2026</text>

  <rect x="28" y="96" width="220" height="588" rx="22" fill="#F7F4EC" filter="url(#cardShadow)"/>
  <text x="50" y="130" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#171717">Filters</text>
  <text x="50" y="160" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">Static slicer-style controls</text>
  <text x="50" y="203" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#333333">City</text>
  <rect x="50" y="218" width="158" height="34" rx="10" fill="#FFC000"/>
  <text x="68" y="240" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111111">All Cities</text>
  <rect x="50" y="260" width="158" height="30" rx="9" fill="#FFF2CC"/>
  <text x="68" y="280" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333333">Yangon</text>
  <rect x="50" y="296" width="158" height="30" rx="9" fill="#FFF8E5"/>
  <text x="68" y="316" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">Mandalay</text>
  <text x="50" y="371" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#333333">Payment</text>
  <rect x="50" y="386" width="72" height="30" rx="9" fill="#FFC000"/>
  <text x="66" y="406" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#111111">Cash</text>
  <rect x="132" y="386" width="76" height="30" rx="9" fill="#FFF2CC"/>
  <text x="146" y="406" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#333333">Wallet</text>
  <rect x="50" y="426" width="158" height="30" rx="9" fill="#FFF8E5"/>
  <text x="68" y="446" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#555555">Credit Card</text>
  <path d="M50,595 C82,560 110,615 140,578 C164,548 188,570 208,548" fill="none" stroke="#FFC000" stroke-width="5" stroke-linecap="round"/>
  <text x="50" y="640" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#333333">Dashboard Mode</text>
  <text x="50" y="662" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#777777">Presentation-ready, not interactive</text>

  <rect x="278" y="96" width="226" height="74" rx="18" fill="#FFF8E5" filter="url(#cardShadow)"/>
  <text x="298" y="122" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#625222">Total Sales</text>
  <text x="298" y="154" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#111111">$305K</text>
  <text x="448" y="154" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1F8A45">▲ 8%</text>

  <rect x="520" y="96" width="226" height="74" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="540" y="122" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#625222">Products Sold</text>
  <text x="540" y="154" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#111111">5,510</text>
  <text x="690" y="154" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1F8A45">▲ 5%</text>

  <rect x="762" y="96" width="226" height="74" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="782" y="122" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#625222">Gross Income</text>
  <text x="782" y="154" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#111111">$15.4K</text>
  <text x="930" y="154" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#C26A00">● flat</text>

  <rect x="1004" y="96" width="226" height="74" rx="18" fill="#FFC000" filter="url(#softGlow)"/>
  <text x="1024" y="122" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5E4700">Average Rating</text>
  <text x="1024" y="154" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#111111">7.2</text>
  <text x="1126" y="154" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#3F3100">target 8.0</text>

  <rect x="278" y="194" width="452" height="226" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="304" y="226" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111111">Sales Trend by Month</text>
  <line x1="322" y1="370" x2="694" y2="370" stroke="#E5E5E5" stroke-width="1"/>
  <line x1="322" y1="325" x2="694" y2="325" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="322" y1="280" x2="694" y2="280" stroke="#EEEEEE" stroke-width="1"/>
  <path d="M324,352 L392,330 L460,342 L528,286 L596,300 L686,248 L686,370 L324,370 Z" fill="url(#areaGrad)"/>
  <path d="M324,352 C358,340 370,336 392,330 C426,318 438,350 460,342 C494,332 500,298 528,286 C560,270 572,315 596,300 C630,280 650,258 686,248" fill="none" stroke="#FFC000" stroke-width="5" stroke-linecap="round"/>
  <circle cx="324" cy="352" r="5" fill="#111111"/><circle cx="392" cy="330" r="5" fill="#111111"/><circle cx="460" cy="342" r="5" fill="#111111"/>
  <circle cx="528" cy="286" r="5" fill="#111111"/><circle cx="596" cy="300" r="5" fill="#111111"/><circle cx="686" cy="248" r="5" fill="#111111"/>
  <text x="322" y="396" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Jan</text>
  <text x="514" y="396" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Feb</text>
  <text x="664" y="396" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Mar</text>

  <rect x="752" y="194" width="478" height="226" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="778" y="226" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111111">Revenue by Product Line</text>
  <line x1="790" y1="370" x2="1190" y2="370" stroke="#E5E5E5" stroke-width="1"/>
  <rect x="816" y="300" width="38" height="70" rx="7" fill="#FFF2CC"/><rect x="876" y="270" width="38" height="100" rx="7" fill="#FFD966"/>
  <rect x="936" y="246" width="38" height="124" rx="7" fill="#FFC000"/><rect x="996" y="284" width="38" height="86" rx="7" fill="#FFE699"/>
  <rect x="1056" y="260" width="38" height="110" rx="7" fill="#F4B400"/><rect x="1116" y="318" width="38" height="52" rx="7" fill="#FFF2CC"/>
  <text x="806" y="394" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Health</text>
  <text x="866" y="394" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Fashion</text>
  <text x="930" y="394" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Food</text>
  <text x="994" y="394" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Home</text>
  <text x="1050" y="394" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Electro</text>
  <text x="1112" y="394" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">Sports</text>

  <rect x="278" y="444" width="452" height="240" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="304" y="476" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111111">Payment Mix</text>
  <path d="M500,506 A70,70 0 0,1 566,600 L526,584 A28,28 0 0,0 500,546 Z" fill="#FFC000"/>
  <path d="M566,600 A70,70 0 0,1 432,622 L471,598 A28,28 0 0,0 526,584 Z" fill="#FFD966"/>
  <path d="M432,622 A70,70 0 0,1 456,508 L474,547 A28,28 0 0,0 471,598 Z" fill="#FFF2CC"/>
  <path d="M456,508 A70,70 0 0,1 500,506 L500,546 A28,28 0 0,0 474,547 Z" fill="#D49A00"/>
  <circle cx="500" cy="576" r="30" fill="#FFFFFF"/>
  <text x="470" y="581" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#111111">100%</text>
  <rect x="600" y="520" width="14" height="14" rx="3" fill="#FFC000"/><text x="622" y="532" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333333">Cash 38%</text>
  <rect x="600" y="552" width="14" height="14" rx="3" fill="#FFD966"/><text x="622" y="564" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333333">Ewallet 34%</text>
  <rect x="600" y="584" width="14" height="14" rx="3" fill="#FFF2CC"/><text x="622" y="596" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333333">Credit 22%</text>
  <rect x="600" y="616" width="14" height="14" rx="3" fill="#D49A00"/><text x="622" y="628" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333333">Other 6%</text>

  <rect x="752" y="444" width="478" height="240" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="778" y="476" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111111">Sales by City</text>
  <text x="778" y="526" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">Yangon</text>
  <rect x="870" y="510" width="300" height="22" rx="11" fill="#F2F2F2"/><rect x="870" y="510" width="255" height="22" rx="11" fill="#FFC000"/>
  <text x="1140" y="526" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#111111">$106K</text>
  <text x="778" y="576" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">Mandalay</text>
  <rect x="870" y="560" width="300" height="22" rx="11" fill="#F2F2F2"/><rect x="870" y="560" width="228" height="22" rx="11" fill="#FFD966"/>
  <text x="1140" y="576" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#111111">$98K</text>
  <text x="778" y="626" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">Naypyitaw</text>
  <rect x="870" y="610" width="300" height="22" rx="11" fill="#F2F2F2"/><rect x="870" y="610" width="206" height="22" rx="11" fill="#FFF2CC"/>
  <text x="1140" y="626" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#111111">$91K</text>
</svg>
```

## Avoid in this skill
- ❌ Embedding chart screenshots when the chart can be drawn with editable SVG bars, lines, circles, and paths.
- ❌ Trying to reproduce Excel slicer interactivity; represent filters as static decorative pills only.
- ❌ Using `<foreignObject>` for HTML-like dashboard widgets; PowerPoint translation will fail.
- ❌ Applying `filter` to `<line>` chart gridlines or axes; use filters only on cards, paths, rects, circles, or text.
- ❌ Using `marker-end` on trend arrows or paths; if arrows are needed, draw them with plain `<line>` plus a small triangular `<path>` arrowhead.

## Composition notes
- Keep the title/header and KPI band in the top 20–25% of the slide; this gives executives the answer before they inspect the charts.
- Reserve the left 18–20% for filter context, then use the remaining width for a clean 2×2 chart grid.
- Use one dominant accent color across KPIs, chart marks, selected slicers, and legends so the dashboard feels unified rather than busy.
- Let card shadows and rounded corners create hierarchy; avoid heavy borders, dense tick labels, or spreadsheet-like grid clutter.