# SVG Recipe — Executive Dashboard with KPI Grid

## Visual mechanism
A premium BI dashboard layout built from floating white KPI cards, strict gutters, large metric typography, and small embedded charts. The top row communicates executive outcomes instantly, while the lower grid provides drill-down context with bar, line, and segment visuals in Tableau-inspired colors.

## SVG primitives needed
- 1× `<rect>` for the cool-gray slide background
- 6× `<rect>` for elevated dashboard cards with rounded corners and shadow
- 4× KPI card groups containing `<text>`, mini `<path>` sparklines, and small status `<circle>` indicators
- 18× `<rect>` for bar-chart columns and horizontal progress bars
- 8× `<line>` for chart gridlines, axes, and card separators
- 3× `<path>` for line-chart series, decorative curves, and filled area accent
- 1× `<linearGradient>` for the background wash
- 3× `<linearGradient>` definitions for chart and KPI accent fills
- 1× `<filter id="cardShadow">` applied to dashboard cards
- 1× `<filter id="softGlow">` applied to the main line-chart path
- Multiple `<text>` elements with explicit `width` attributes for editable KPI labels, values, deltas, axes, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F8FB"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#4E79A7"/>
      <stop offset="100%" stop-color="#8FB5DE"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#59A14F"/>
      <stop offset="100%" stop-color="#9BD18F"/>
    </linearGradient>
    <linearGradient id="areaFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4E79A7" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#4E79A7" stop-opacity="0"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-15%" y="-40%" width="130%" height="180%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M1040 36 C1120 12 1218 42 1260 104" fill="none" stroke="#DCE5F0" stroke-width="3"/>
  <path d="M1034 58 C1130 36 1198 88 1268 158" fill="none" stroke="#E7ECF4" stroke-width="2"/>

  <text x="56" y="58" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#2D3640">Executive Sales Dashboard</text>
  <text x="56" y="86" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A8594">Q4 FY25 performance summary · refreshed 08:30 UTC</text>
  <rect x="1020" y="36" width="204" height="34" rx="17" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="1044" cy="53" r="5" fill="#59A14F"/>
  <text x="1060" y="58" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#44515E">On track to plan</text>

  <rect x="56" y="114" width="270" height="126" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="80" y="145" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#7A8594">TOTAL SALES</text>
  <text x="80" y="188" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#2D3640">$428.9K</text>
  <text x="80" y="218" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#59A14F">▲ 13.8%</text>
  <path d="M208 214 C226 186 244 204 260 170 C274 142 292 152 306 130" fill="none" stroke="#59A14F" stroke-width="4" stroke-linecap="round"/>

  <rect x="350" y="114" width="270" height="126" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="374" y="145" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#7A8594">PROFIT MARGIN</text>
  <text x="374" y="188" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#2D3640">24.5%</text>
  <text x="374" y="218" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#E15759">▼ 2.1%</text>
  <path d="M502 140 C524 154 540 146 558 164 C576 183 590 194 604 206" fill="none" stroke="#E15759" stroke-width="4" stroke-linecap="round"/>

  <rect x="644" y="114" width="270" height="126" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="668" y="145" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#7A8594">TOTAL ORDERS</text>
  <text x="668" y="188" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#2D3640">10,933</text>
  <text x="668" y="218" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#59A14F">▲ 5.4%</text>
  <rect x="798" y="204" width="24" height="18" rx="4" fill="#D9E8F7"/>
  <rect x="828" y="182" width="24" height="40" rx="4" fill="#9DBFE4"/>
  <rect x="858" y="156" width="24" height="66" rx="4" fill="#4E79A7"/>

  <rect x="938" y="114" width="286" height="126" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="962" y="145" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#7A8594">AVG. ORDER VALUE</text>
  <text x="962" y="188" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#2D3640">$39.23</text>
  <text x="962" y="218" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#59A14F">▲ 1.2%</text>
  <circle cx="1166" cy="174" r="34" fill="#EEF6ED"/>
  <path d="M1150 176 L1162 188 L1184 158" fill="none" stroke="#59A14F" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="56" y="270" width="554" height="376" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="84" y="306" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2D3640">Revenue by Region</text>
  <text x="84" y="328" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">Net sales, USD thousands</text>
  <line x1="116" y1="586" x2="560" y2="586" stroke="#D6DEE8" stroke-width="1"/>
  <line x1="116" y1="526" x2="560" y2="526" stroke="#E6EBF2" stroke-width="1"/>
  <line x1="116" y1="466" x2="560" y2="466" stroke="#E6EBF2" stroke-width="1"/>
  <line x1="116" y1="406" x2="560" y2="406" stroke="#E6EBF2" stroke-width="1"/>
  <rect x="142" y="430" width="46" height="156" rx="6" fill="url(#blueGrad)"/>
  <rect x="216" y="366" width="46" height="220" rx="6" fill="url(#blueGrad)"/>
  <rect x="290" y="484" width="46" height="102" rx="6" fill="url(#blueGrad)"/>
  <rect x="364" y="398" width="46" height="188" rx="6" fill="url(#greenGrad)"/>
  <rect x="438" y="338" width="46" height="248" rx="6" fill="url(#blueGrad)"/>
  <text x="132" y="615" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">North</text>
  <text x="206" y="615" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">West</text>
  <text x="286" y="615" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">East</text>
  <text x="354" y="615" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">EMEA</text>
  <text x="432" y="615" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">APAC</text>

  <rect x="638" y="270" width="586" height="226" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="666" y="306" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2D3640">Quarterly Sales Run Rate</text>
  <text x="666" y="328" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">Rolling 12-week view with forecast band</text>
  <line x1="678" y1="448" x2="1188" y2="448" stroke="#D6DEE8" stroke-width="1"/>
  <line x1="678" y1="398" x2="1188" y2="398" stroke="#E6EBF2" stroke-width="1"/>
  <line x1="678" y1="348" x2="1188" y2="348" stroke="#E6EBF2" stroke-width="1"/>
  <path d="M678 448 L678 410 C722 398 748 420 790 390 C834 358 864 372 904 340 C946 306 990 330 1028 316 C1070 300 1118 316 1188 286 L1188 448 Z" fill="url(#areaFade)"/>
  <path d="M678 410 C722 398 748 420 790 390 C834 358 864 372 904 340 C946 306 990 330 1028 316 C1070 300 1118 316 1188 286" fill="none" stroke="#4E79A7" stroke-width="5" stroke-linecap="round" filter="url(#softGlow)" opacity="0.55"/>
  <path d="M678 410 C722 398 748 420 790 390 C834 358 864 372 904 340 C946 306 990 330 1028 316 C1070 300 1118 316 1188 286" fill="none" stroke="#4E79A7" stroke-width="3.2" stroke-linecap="round"/>
  <circle cx="1188" cy="286" r="6" fill="#4E79A7"/>
  <text x="1128" y="274" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4E79A7">$118K</text>

  <rect x="638" y="522" width="286" height="124" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="666" y="558" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2D3640">Channel Mix</text>
  <rect x="666" y="582" width="210" height="12" rx="6" fill="#E7ECF4"/>
  <rect x="666" y="582" width="118" height="12" rx="6" fill="#4E79A7"/>
  <rect x="666" y="606" width="210" height="12" rx="6" fill="#E7ECF4"/>
  <rect x="666" y="606" width="82" height="12" rx="6" fill="#F28E2B"/>
  <text x="666" y="576" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">Enterprise 56%</text>
  <text x="666" y="636" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8594">SMB 39%</text>

  <rect x="948" y="522" width="276" height="124" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="976" y="558" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2D3640">Executive Note</text>
  <text x="976" y="586" width="218" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5F6B78">APAC and West drove 72% of incremental growth; margin softness is concentrated in promotional SKUs.</text>
  <line x1="976" y1="612" x2="1194" y2="612" stroke="#E6EBF2" stroke-width="1"/>
  <text x="976" y="634" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#59A14F">Recommended: hold growth spend</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use embedded HTML tables or `<foreignObject>` for dashboard widgets; build cards and charts from SVG primitives so they stay editable.
- ❌ Do not rely on real PowerPoint chart objects inside SVG; approximate BI charts with editable bars, paths, labels, and axes.
- ❌ Do not use `<pattern>` fills for grid backgrounds; use simple low-opacity lines and flat fills for reliable PowerPoint translation.
- ❌ Do not put `clip-path` on chart shapes or cards; clipping is only reliable on `<image>` elements.
- ❌ Do not use `marker-end` on trend paths; use text triangles, circles, or simple line geometry instead.

## Composition notes
- Keep the top 25–30% reserved for KPI cards; use large metric values, compact labels, and color-coded deltas.
- Use a strict 4-column gutter system: equal outer margins, equal card spacing, and aligned chart panels below.
- Let white cards float over a cool-gray background with soft shadows; this creates the modern BI/web-app feel.
- Use color sparingly: blue for primary data, green/red for performance signals, and muted gray for all secondary structure.