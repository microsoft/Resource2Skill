# SVG Recipe — Modular Data Dashboard Layout

## Visual mechanism
A neutral gray canvas holds a disciplined grid of rounded white metric cards, each card containing one self-contained visualization. A restrained monochrome blue system unifies KPIs, charts, maps, and tables so the dashboard feels executive, analytical, and cohesive.

## SVG primitives needed
- 1× `<rect>` for the full-slide light gray background.
- 8× `<rect>` for rounded white dashboard cards with subtle borders and shadows.
- Multiple `<text>` elements with explicit `width` for title, KPI numbers, labels, axes, table rows, and callouts.
- Multiple `<rect>` elements for bar charts, table row bands, progress strips, and small legend swatches.
- Multiple `<path>` elements for donut chart slices, line chart strokes, area fill, stylized map silhouette, and mini trend sparklines.
- Multiple `<line>` elements for chart axes, gridlines, and table separators.
- Multiple `<circle>` elements for scatter plot points, donut center, map location bubbles, and status indicators.
- 1× `<ellipse>` for a soft KPI/map emphasis halo.
- 2× `<linearGradient>` definitions for premium blue chart fills and header accents.
- 1× `<radialGradient>` for soft blue focus glow.
- 1× `<filter id="cardShadow">` applied to cards for subtle depth.
- 1× `<filter id="softGlow">` applied to selected paths/circles for an executive-tech finish.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#003366"/>
      <stop offset="55%" stop-color="#0055AA"/>
      <stop offset="100%" stop-color="#3399FF"/>
    </linearGradient>
    <linearGradient id="paleGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#EAF4FF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
    <radialGradient id="haloBlue" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#66AAFF" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#66AAFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8F9FA"/>
  <text x="40" y="48" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#212529">A股上市公司数据总览</text>
  <text x="40" y="76" width="600" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C757D">Executive market intelligence dashboard · refreshed Q4 2026</text>
  <rect x="1010" y="34" width="210" height="34" rx="17" fill="#FFFFFF" stroke="#DEE2E6"/>
  <circle cx="1030" cy="51" r="5" fill="#2BB673"/>
  <text x="1044" y="56" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#495057">Live analytics snapshot</text>

  <rect x="40" y="100" width="270" height="170" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="62" y="130" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">上市公司总数</text>
  <ellipse cx="180" cy="191" rx="96" ry="46" fill="url(#haloBlue)"/>
  <text x="62" y="210" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="300" fill="#212529">4,840</text>
  <text x="224" y="211" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#0055AA">家</text>
  <path d="M62 242 C100 229, 128 251, 164 238 S232 233, 282 218" fill="none" stroke="#3399FF" stroke-width="4" stroke-linecap="round"/>
  <text x="62" y="258" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">同比增长 7.8% · 新增 351 家</text>

  <rect x="330" y="100" width="270" height="170" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="352" y="130" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">上市板块分布</text>
  <path d="M465 134 A52 52 0 1 1 434 228 L449 201 A22 22 0 1 0 465 164 Z" fill="#003366"/>
  <path d="M434 228 A52 52 0 0 1 413 174 L443 181 A22 22 0 0 0 449 201 Z" fill="#0055AA"/>
  <path d="M413 174 A52 52 0 0 1 458 135 L462 164 A22 22 0 0 0 443 181 Z" fill="#3399FF"/>
  <path d="M458 135 A52 52 0 0 1 501 151 L485 176 A22 22 0 0 0 462 164 Z" fill="#66AAFF"/>
  <circle cx="465" cy="187" r="24" fill="#FFFFFF"/>
  <text x="444" y="193" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#212529">65%</text>
  <rect x="528" y="151" width="10" height="10" rx="2" fill="#003366"/>
  <text x="544" y="160" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">主板</text>
  <rect x="528" y="174" width="10" height="10" rx="2" fill="#0055AA"/>
  <text x="544" y="183" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">创业板</text>
  <rect x="528" y="197" width="10" height="10" rx="2" fill="#3399FF"/>
  <text x="544" y="206" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">科创板</text>
  <text x="352" y="250" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">主板仍为核心承载，成长板块扩张明显</text>

  <rect x="620" y="100" width="300" height="270" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="642" y="130" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">上市公司城市 Top 10</text>
  <line x1="700" y1="156" x2="700" y2="330" stroke="#E9ECEF"/>
  <line x1="700" y1="330" x2="882" y2="330" stroke="#CED4DA"/>
  <text x="642" y="169" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">北京</text>
  <rect x="700" y="158" width="158" height="12" rx="6" fill="url(#blueGrad)"/>
  <text x="642" y="191" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">上海</text>
  <rect x="700" y="180" width="144" height="12" rx="6" fill="#0055AA"/>
  <text x="642" y="213" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">深圳</text>
  <rect x="700" y="202" width="138" height="12" rx="6" fill="#3399FF"/>
  <text x="642" y="235" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">杭州</text>
  <rect x="700" y="224" width="72" height="12" rx="6" fill="#66AAFF"/>
  <text x="642" y="257" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">广州</text>
  <rect x="700" y="246" width="58" height="12" rx="6" fill="#9BCBFF"/>
  <text x="642" y="279" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">苏州</text>
  <rect x="700" y="268" width="58" height="12" rx="6" fill="#B7DAFF"/>
  <text x="642" y="301" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">南京</text>
  <rect x="700" y="290" width="49" height="12" rx="6" fill="#CCE5FF"/>
  <text x="860" y="169" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#495057">439</text>

  <rect x="940" y="100" width="300" height="270" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="962" y="130" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">区域热度地图</text>
  <ellipse cx="1092" cy="235" rx="106" ry="78" fill="url(#haloBlue)"/>
  <path d="M1037 171 C1074 147,1123 156,1148 181 C1172 205,1202 205,1206 236 C1210 270,1175 284,1149 298 C1114 317,1079 307,1055 285 C1030 262,994 265,990 231 C986 203,1010 190,1037 171 Z" fill="url(#paleGrad)" stroke="#99C8F5" stroke-width="2"/>
  <circle cx="1088" cy="205" r="17" fill="#0055AA" opacity="0.88" filter="url(#softGlow)"/>
  <circle cx="1132" cy="232" r="22" fill="#3399FF" opacity="0.82"/>
  <circle cx="1062" cy="252" r="12" fill="#66AAFF" opacity="0.92"/>
  <circle cx="1162" cy="265" r="9" fill="#003366" opacity="0.75"/>
  <text x="962" y="334" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">气泡半径表示公司密度，沿海与一线城市高度聚集</text>

  <rect x="40" y="290" width="560" height="350" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="62" y="322" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">IPO 年度趋势</text>
  <text x="462" y="322" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">1992–2021</text>
  <line x1="88" y1="574" x2="552" y2="574" stroke="#CED4DA"/>
  <line x1="88" y1="374" x2="88" y2="574" stroke="#CED4DA"/>
  <line x1="88" y1="524" x2="552" y2="524" stroke="#EEF1F4"/>
  <line x1="88" y1="474" x2="552" y2="474" stroke="#EEF1F4"/>
  <line x1="88" y1="424" x2="552" y2="424" stroke="#EEF1F4"/>
  <path d="M88 568 L112 556 L136 535 L160 560 L184 552 L208 520 L232 498 L256 530 L280 512 L304 540 L328 530 L352 486 L376 510 L400 452 L424 504 L448 492 L472 432 L496 388 L520 456 L552 360" fill="none" stroke="#0055AA" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M88 568 L112 556 L136 535 L160 560 L184 552 L208 520 L232 498 L256 530 L280 512 L304 540 L328 530 L352 486 L376 510 L400 452 L424 504 L448 492 L472 432 L496 388 L520 456 L552 360 L552 574 L88 574 Z" fill="#3399FF" opacity="0.12"/>
  <circle cx="552" cy="360" r="6" fill="#003366"/>
  <text x="512" y="350" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#003366">524</text>
  <text x="84" y="596" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">1992</text>
  <text x="512" y="596" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">2021</text>
  <rect x="82" y="612" width="470" height="8" rx="4" fill="#E9ECEF"/>
  <rect x="82" y="612" width="384" height="8" rx="4" fill="url(#blueGrad)"/>

  <rect x="620" y="390" width="300" height="250" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="642" y="422" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">公司数量 × GDP 相关性</text>
  <line x1="664" y1="590" x2="884" y2="590" stroke="#CED4DA"/>
  <line x1="664" y1="456" x2="664" y2="590" stroke="#CED4DA"/>
  <circle cx="694" cy="566" r="5" fill="#CCE5FF"/><circle cx="724" cy="532" r="7" fill="#66AAFF"/><circle cx="765" cy="506" r="9" fill="#3399FF"/>
  <circle cx="801" cy="548" r="6" fill="#99C8F5"/><circle cx="836" cy="486" r="11" fill="#0055AA"/><circle cx="864" cy="466" r="14" fill="#003366"/>
  <path d="M686 568 C735 544,787 514,872 468" fill="none" stroke="#3399FF" stroke-width="3" stroke-dasharray="7 6"/>
  <text x="664" y="616" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">气泡越大表示总市值越高</text>

  <rect x="940" y="390" width="300" height="250" rx="18" fill="#FFFFFF" stroke="#DEE2E6" filter="url(#cardShadow)"/>
  <text x="962" y="422" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#495057">总市值 Top 6</text>
  <rect x="962" y="444" width="256" height="28" rx="8" fill="#F1F5F9"/>
  <text x="974" y="463" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#495057">代码</text>
  <text x="1054" y="463" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#495057">证券简称</text>
  <text x="1140" y="463" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#495057">市值</text>
  <line x1="962" y1="494" x2="1218" y2="494" stroke="#E9ECEF"/>
  <line x1="962" y1="524" x2="1218" y2="524" stroke="#E9ECEF"/>
  <line x1="962" y1="554" x2="1218" y2="554" stroke="#E9ECEF"/>
  <line x1="962" y1="584" x2="1218" y2="584" stroke="#E9ECEF"/>
  <text x="974" y="493" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">600519</text>
  <text x="1054" y="493" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#212529">贵州茅台</text>
  <text x="1140" y="493" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#0055AA">24,114</text>
  <text x="974" y="523" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">601398</text>
  <text x="1054" y="523" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#212529">工商银行</text>
  <text x="1140" y="523" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#0055AA">14,944</text>
  <text x="974" y="553" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6C757D">300750</text>
  <text x="1054" y="553" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#212529">宁德时代</text>
  <text x="1140" y="553" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#0055AA">12,874</text>
  <text x="974" y="613" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6C757D">单位：亿元 · 仅展示核心样本</text>
</svg>
```

## Avoid in this skill
- ❌ Rasterizing charts as screenshots when editable SVG bars, lines, circles, and paths can communicate the same data cleanly.
- ❌ Dense axis labels and micro-legends that become unreadable after conversion to PowerPoint.
- ❌ Applying `filter` to `<line>` gridlines; use filters only on cards, paths, circles, ellipses, or text.
- ❌ Using `<foreignObject>` for HTML-style dashboard widgets; build every card from native SVG primitives.
- ❌ Using `clip-path` on non-image chart shapes; it will be ignored by the translator.

## Composition notes
- Keep a consistent card gutter of roughly 20px and internal padding of 20–24px; the grid discipline is what makes the dashboard feel premium.
- Reserve the top-left for the dashboard title and the top-right for a compact status pill or timestamp.
- Use white cards on `#F8F9FA`, then repeat one blue palette across every visualization to avoid “chart salad.”
- Mix card sizes deliberately: small KPI cards for headline numbers, wider cards for temporal trends, and medium cards for map/table/chart modules.