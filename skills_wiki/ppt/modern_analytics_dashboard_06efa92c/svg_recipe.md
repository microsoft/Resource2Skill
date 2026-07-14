# SVG Recipe — Modern Analytics Dashboard

## Visual mechanism
A premium BI dashboard is built from a muted architectural/photo background, a large frosted main panel, and modular white KPI cards with soft shadows. Custom SVG gauges, progress bars, mini bar charts, sparklines, and map-like paths create an editable “web app analytics” look without relying on PowerPoint chart objects.

## SVG primitives needed
- 1× `<image>` for the desaturated architectural/dashboard background texture.
- 1× full-slide `<rect>` overlay to mute and darken the background image.
- 1× large rounded `<rect>` for the main dashboard shell.
- 1× top toolbar `<rect>` plus 1× search input `<rect>` and several small menu/icon shapes.
- 8× white rounded `<rect>` cards for KPI and chart modules, all using a soft shadow filter.
- Multiple `<text>` elements with explicit `width` for dashboard title, KPI values, labels, legends, and annotations.
- 2× `<path>` semicircle gauges using thick stroked arcs for target progress.
- 1× `<path>` filled area chart and 1× stroked `<path>` sparkline for trend visualization.
- Multiple `<rect>` bars for vertical bar charts and horizontal progress bars.
- 4× organic `<path>` shapes for a simplified editable geographic/map visualization.
- 2× `<filter>` definitions: one soft card shadow and one subtle colored glow.
- 2× `<linearGradient>` definitions for the dashboard panel and chart fills.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f8fb"/>
      <stop offset="100%" stop-color="#e8ebf1"/>
    </linearGradient>
    <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#da017a" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#da017a" stop-opacity="0.04"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="magentaGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <image href="https://images.example.com/muted-abstract-architecture-lines-background.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="#20242b" opacity="0.68"/>

  <rect x="42" y="36" width="1196" height="648" rx="30" fill="url(#panelGrad)" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="42" y="36" width="1196" height="68" rx="30" fill="#0d0f13"/>
  <rect x="42" y="78" width="1196" height="34" fill="#0d0f13"/>
  <text x="78" y="79" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="600" fill="#ffffff">Executive Dashboard</text>
  <rect x="760" y="55" width="300" height="32" rx="16" fill="#242833"/>
  <circle cx="786" cy="71" r="7" fill="none" stroke="#8c93a3" stroke-width="2"/>
  <line x1="792" y1="77" x2="800" y2="85" stroke="#8c93a3" stroke-width="2"/>
  <text x="816" y="77" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9ba3b5">Search metrics</text>
  <line x1="1110" y1="61" x2="1145" y2="61" stroke="#ffffff" stroke-width="3"/>
  <line x1="1110" y1="72" x2="1145" y2="72" stroke="#ffffff" stroke-width="3"/>
  <line x1="1110" y1="83" x2="1145" y2="83" stroke="#ffffff" stroke-width="3"/>

  <rect x="76" y="132" width="262" height="130" rx="20" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="102" y="164" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#101318">Revenue</text>
  <text x="102" y="213" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#101318">$4.82M</text>
  <text x="104" y="241" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#76bc21">▲ 18.4% vs last qtr</text>
  <path d="M246 224 C268 192 289 210 314 174" fill="none" stroke="#76bc21" stroke-width="5" stroke-linecap="round"/>

  <rect x="362" y="132" width="262" height="130" rx="20" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="388" y="164" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#101318">Active Accounts</text>
  <text x="388" y="213" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#101318">28.6K</text>
  <text x="390" y="241" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#da017a">● retention 91%</text>
  <rect x="532" y="181" width="18" height="52" rx="5" fill="#ffcc00"/>
  <rect x="558" y="158" width="18" height="75" rx="5" fill="#800080"/>
  <rect x="584" y="197" width="18" height="36" rx="5" fill="#da017a"/>

  <rect x="648" y="132" width="262" height="130" rx="20" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="674" y="164" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#101318">Target Achievement</text>
  <path d="M700 224 A70 70 0 0 1 840 224" fill="none" stroke="#e6e8ee" stroke-width="22" stroke-linecap="round"/>
  <path d="M700 224 A70 70 0 0 1 807 169" fill="none" stroke="#ffcc00" stroke-width="22" stroke-linecap="round"/>
  <text x="743" y="218" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#101318">76%</text>
  <text x="716" y="246" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6b7280">quarterly goal</text>

  <rect x="934" y="132" width="260" height="130" rx="20" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="960" y="164" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#101318">Customer Health</text>
  <circle cx="986" cy="214" r="10" fill="#76bc21"/>
  <rect x="1010" y="206" width="136" height="14" rx="7" fill="#e8ebf1"/>
  <rect x="1010" y="206" width="108" height="14" rx="7" fill="#76bc21"/>
  <circle cx="986" cy="241" r="10" fill="#db4437"/>
  <rect x="1010" y="233" width="136" height="14" rx="7" fill="#e8ebf1"/>
  <rect x="1010" y="233" width="42" height="14" rx="7" fill="#db4437"/>
  <text x="1154" y="219" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#4b5563">79%</text>
  <text x="1154" y="246" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#4b5563">31%</text>

  <rect x="76" y="292" width="548" height="330" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="104" y="326" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#101318">Sales Trend</text>
  <text x="104" y="348" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-style="italic" fill="#7b8190">rolling 12-week pipeline performance</text>
  <line x1="116" y1="560" x2="590" y2="560" stroke="#d8dce5" stroke-width="1"/>
  <line x1="116" y1="500" x2="590" y2="500" stroke="#eef0f4" stroke-width="1"/>
  <line x1="116" y1="440" x2="590" y2="440" stroke="#eef0f4" stroke-width="1"/>
  <path d="M116 543 C158 518 188 536 226 486 C270 427 305 468 344 424 C386 379 419 412 458 366 C504 313 543 351 590 300 L590 560 L116 560 Z" fill="url(#areaGrad)"/>
  <path d="M116 543 C158 518 188 536 226 486 C270 427 305 468 344 424 C386 379 419 412 458 366 C504 313 543 351 590 300" fill="none" stroke="#da017a" stroke-width="5" stroke-linecap="round"/>
  <circle cx="590" cy="300" r="8" fill="#da017a" filter="url(#magentaGlow)"/>
  <text x="500" y="294" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#da017a">$1.24M</text>

  <rect x="648" y="292" width="260" height="330" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="674" y="326" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#101318">Regional Mix</text>
  <path d="M734 398 C752 360 804 350 835 383 C872 422 839 483 787 489 C735 496 709 450 734 398 Z" fill="#ffcc00" opacity="0.92"/>
  <path d="M705 472 C735 448 775 468 778 507 C781 542 738 566 708 545 C674 522 676 492 705 472 Z" fill="#800080" opacity="0.9"/>
  <path d="M810 502 C846 475 888 496 888 536 C888 572 850 592 819 575 C790 559 783 523 810 502 Z" fill="#76bc21" opacity="0.9"/>
  <path d="M696 384 C710 356 745 345 765 366 C782 384 772 416 743 425 C714 434 683 411 696 384 Z" fill="#da017a" opacity="0.92"/>
  <text x="678" y="590" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4b5563">Editable path regions simulate a clean map chart.</text>

  <rect x="934" y="292" width="260" height="330" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
  <text x="960" y="326" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#101318">Channel Performance</text>
  <text x="960" y="354" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6b7280">Enterprise</text>
  <rect x="960" y="366" width="194" height="16" rx="8" fill="#e8ebf1"/>
  <rect x="960" y="366" width="164" height="16" rx="8" fill="#ffcc00"/>
  <text x="960" y="412" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6b7280">Mid-market</text>
  <rect x="960" y="424" width="194" height="16" rx="8" fill="#e8ebf1"/>
  <rect x="960" y="424" width="126" height="16" rx="8" fill="#800080"/>
  <text x="960" y="470" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6b7280">SMB</text>
  <rect x="960" y="482" width="194" height="16" rx="8" fill="#e8ebf1"/>
  <rect x="960" y="482" width="88" height="16" rx="8" fill="#da017a"/>
  <path d="M966 564 C995 540 1026 553 1056 528 C1089 501 1124 523 1158 492" fill="none" stroke="#76bc21" stroke-width="5" stroke-linecap="round"/>
  <text x="960" y="596" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4b5563">Momentum improving across high-value channels.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<foreignObject>` to embed HTML dashboard widgets; it will hard-fail translation.
- ❌ Do not rely on PowerPoint chart objects or SVG `<pattern>` fills for the dashboard texture; build editable visualizations from paths, rects, circles, and text.
- ❌ Do not apply `filter` to `<line>` elements; use filters only on cards, paths, circles, ellipses, rects, or text.
- ❌ Do not use `marker-end` on paths for chart arrows; if arrows are required, use plain `<line>` with marker attributes directly on each line.
- ❌ Do not clip non-image shapes; clipping should be reserved for `<image>` crops only.

## Composition notes
- Keep the main dashboard shell inset from the slide edges so the muted background remains visible as a premium frame.
- Use a strict grid: KPI cards across the top, larger analytical modules below, with consistent gutters between cards.
- Reserve high-saturation colors for data marks only; keep cards white and the panel light gray to preserve executive readability.
- Use large KPI numerals and small secondary labels to create hierarchy, while charts and gauges act as visual confirmation rather than decorative clutter.