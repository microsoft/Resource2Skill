# SVG Recipe — Dashboard 2x2 with Side Tabs

## Visual mechanism
A premium dark analytics dashboard built from four glassy chart cards: two wide primary charts on the left and two compact secondary panels on the right. The right panels gain hierarchy through protruding vertical side tabs, glowing accents, and dense but readable chart furniture.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 4× `<rect>` for the main rounded dashboard panels
- 4× `<rect>` for vertical side tabs attached to the right-side panels
- 20+ `<line>` elements for chart gridlines, axes, tick marks, and connector rules
- 10+ `<path>` elements for line charts, area fills, decorative glow blobs, and tab notches
- 20+ `<rect>` elements for bars, KPI chips, legends, and micro-metric blocks
- 4× `<circle>` / `<ellipse>` elements for status dots and donut-style indicators
- Multiple `<text>` elements with explicit `width` attributes for titles, metric labels, tabs, legends, and annotations
- 3× `<linearGradient>` definitions for background, panels, and active tab styling
- 1× `<radialGradient>` definition for ambient glow
- 2× `<filter>` definitions: soft panel shadow and neon glow, applied only to rect/path/text/circle shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111f"/>
      <stop offset="55%" stop-color="#0b1628"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#17243a"/>
      <stop offset="100%" stop-color="#0e1728"/>
    </linearGradient>
    <linearGradient id="tabActive" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1bf2ff"/>
      <stop offset="100%" stop-color="#6d5dfc"/>
    </linearGradient>
    <linearGradient id="areaCyan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#13d8ff" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#13d8ff" stop-opacity="0.03"/>
    </linearGradient>
    <radialGradient id="ambient" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#1bf2ff" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#1bf2ff" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <ellipse cx="980" cy="80" rx="330" ry="120" fill="url(#ambient)" filter="url(#glow)"/>
  <path d="M-40,640 C160,565 280,720 455,622 C610,535 730,620 850,555 C1010,470 1120,555 1320,475 L1320,760 L-40,760 Z" fill="#13233a" opacity="0.42"/>

  <text x="60" y="56" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#f5f8ff">Revenue Operations Dashboard</text>
  <text x="60" y="84" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#91a4bd">2x2 executive view · live pipeline, channel velocity, retention risk, and regional mix</text>
  <rect x="1010" y="38" width="170" height="34" rx="17" fill="#10243a" stroke="#24415f"/>
  <circle cx="1030" cy="55" r="5" fill="#35f39b"/>
  <text x="1042" y="60" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#d9fff0">LIVE REFRESH</text>

  <rect x="60" y="118" width="760" height="252" rx="24" fill="url(#panel)" stroke="#243a56" filter="url(#shadow)"/>
  <text x="88" y="154" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Pipeline creation</text>
  <text x="88" y="181" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#21e7ff">$48.2M</text>
  <text x="235" y="178" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#35f39b">▲ 18.4% QoQ</text>
  <line x1="98" y1="325" x2="780" y2="325" stroke="#2a3d58" stroke-width="1"/>
  <line x1="98" y1="278" x2="780" y2="278" stroke="#233650" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="98" y1="231" x2="780" y2="231" stroke="#233650" stroke-width="1" stroke-dasharray="5 7"/>
  <path d="M100,318 C165,292 205,303 260,260 C315,216 356,252 415,230 C485,203 525,168 586,196 C646,224 704,178 780,150 L780,326 L100,326 Z" fill="url(#areaCyan)"/>
  <path d="M100,318 C165,292 205,303 260,260 C315,216 356,252 415,230 C485,203 525,168 586,196 C646,224 704,178 780,150" fill="none" stroke="#16dcff" stroke-width="4" stroke-linecap="round"/>
  <path d="M100,300 C165,310 216,288 285,296 C370,305 410,275 482,285 C560,296 628,260 780,268" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round"/>
  <circle cx="780" cy="150" r="6" fill="#ffffff" stroke="#16dcff" stroke-width="4"/>
  <rect x="610" y="142" width="132" height="42" rx="13" fill="#071827" stroke="#1bdfff"/>
  <text x="625" y="160" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#91a4bd">May forecast</text>
  <text x="625" y="178" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#ffffff">$9.6M</text>

  <rect x="60" y="410" width="760" height="250" rx="24" fill="url(#panel)" stroke="#243a56" filter="url(#shadow)"/>
  <text x="88" y="446" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Channel velocity</text>
  <text x="88" y="472" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#91a4bd">Qualified opportunities by source</text>
  <line x1="110" y1="616" x2="780" y2="616" stroke="#2a3d58" stroke-width="1"/>
  <rect x="135" y="535" width="54" height="81" rx="8" fill="#18d8ff"/>
  <rect x="215" y="492" width="54" height="124" rx="8" fill="#6d5dfc"/>
  <rect x="295" y="560" width="54" height="56" rx="8" fill="#35f39b"/>
  <rect x="375" y="510" width="54" height="106" rx="8" fill="#ffb020"/>
  <rect x="455" y="475" width="54" height="141" rx="8" fill="#ff4fd8"/>
  <rect x="535" y="548" width="54" height="68" rx="8" fill="#14b8a6"/>
  <rect x="640" y="482" width="126" height="108" rx="18" fill="#0a1b2f" stroke="#29435f"/>
  <text x="660" y="512" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#91a4bd">Fastest source</text>
  <text x="660" y="542" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">Partner</text>
  <text x="660" y="568" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#35f39b">12.8 days avg</text>

  <rect x="850" y="118" width="350" height="252" rx="24" fill="url(#panel)" stroke="#243a56" filter="url(#shadow)"/>
  <rect x="1190" y="145" width="54" height="54" rx="14" fill="url(#tabActive)" filter="url(#shadow)"/>
  <rect x="1190" y="207" width="54" height="54" rx="14" fill="#13243b" stroke="#2c4868"/>
  <text x="1207" y="178" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#07111f" transform="rotate(90 1207 178)">PLAN</text>
  <text x="1207" y="241" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#8aa1ba" transform="rotate(90 1207 241)">ACT</text>
  <text x="878" y="154" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Retention risk</text>
  <text x="878" y="181" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">7.4%</text>
  <text x="1018" y="178" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffb020">watchlist ↑</text>
  <circle cx="1036" cy="271" r="62" fill="none" stroke="#213750" stroke-width="18"/>
  <circle cx="1036" cy="271" r="62" fill="none" stroke="#ff4fd8" stroke-width="18" stroke-dasharray="180 210" transform="rotate(-90 1036 271)"/>
  <circle cx="1036" cy="271" r="39" fill="#0a1728"/>
  <text x="1008" y="266" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#ffffff">42</text>
  <text x="996" y="287" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#91a4bd">accounts</text>
  <rect x="888" y="232" width="108" height="28" rx="14" fill="#10243a"/>
  <text x="904" y="251" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d7e7ff">Enterprise</text>
  <rect x="888" y="270" width="92" height="28" rx="14" fill="#10243a"/>
  <text x="904" y="289" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d7e7ff">SMB</text>

  <rect x="850" y="410" width="350" height="250" rx="24" fill="url(#panel)" stroke="#243a56" filter="url(#shadow)"/>
  <rect x="1190" y="437" width="54" height="54" rx="14" fill="#13243b" stroke="#2c4868"/>
  <rect x="1190" y="499" width="54" height="54" rx="14" fill="url(#tabActive)" filter="url(#shadow)"/>
  <text x="1207" y="471" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#8aa1ba" transform="rotate(90 1207 471)">REG</text>
  <text x="1207" y="532" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#07111f" transform="rotate(90 1207 532)">OPS</text>
  <text x="878" y="446" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Regional mix</text>
  <text x="878" y="472" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#91a4bd">Booked ARR contribution</text>
  <rect x="888" y="510" width="230" height="18" rx="9" fill="#10243a"/>
  <rect x="888" y="510" width="142" height="18" rx="9" fill="#18d8ff"/>
  <rect x="888" y="548" width="230" height="18" rx="9" fill="#10243a"/>
  <rect x="888" y="548" width="108" height="18" rx="9" fill="#6d5dfc"/>
  <rect x="888" y="586" width="230" height="18" rx="9" fill="#10243a"/>
  <rect x="888" y="586" width="74" height="18" rx="9" fill="#35f39b"/>
  <text x="888" y="502" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d7e7ff">North America</text>
  <text x="1128" y="525" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">62%</text>
  <text x="888" y="540" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d7e7ff">EMEA</text>
  <text x="1128" y="563" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">47%</text>
  <text x="888" y="578" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#d7e7ff">APAC</text>
  <text x="1128" y="601" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ffffff">32%</text>
</svg>
```

## Avoid in this skill
- ❌ Building the dashboard as a flat table of rectangles; the technique depends on layered cards, glowing accents, and tab hierarchy.
- ❌ Putting `filter` on chart grid `<line>` elements; use filters only on panels, paths, circles, or text.
- ❌ Using `marker-end` for arrows in microcharts; use simple `<line>` or custom `<path>` chevrons instead.
- ❌ Applying `clip-path` to chart shapes or groups; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Omitting explicit `width` on dense dashboard labels; PowerPoint will not autofit text.

## Composition notes
- Keep the left 65% of the slide for the two primary chart cards; they should feel like the analytical “engine room.”
- Use the right column for compact decision modules, with side tabs protruding slightly to create navigation affordance.
- Maintain strong negative space inside each card: title/KPI at top, visualization below, annotations floating near the active data point.
- Use one dominant neon accent per panel, then repeat muted navy strokes and soft blue-gray labels for a controlled executive-dashboard rhythm.