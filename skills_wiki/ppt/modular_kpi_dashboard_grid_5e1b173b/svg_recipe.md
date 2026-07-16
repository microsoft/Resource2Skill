# SVG Recipe — Modular KPI Dashboard Grid

## Visual mechanism
A high-density executive dashboard built from a strict modular card grid: each card combines a compact icon/title header, one oversized KPI number, and a mini chart that communicates trend or status at a glance. The premium look comes from a dark gradient canvas, soft elevated cards, neon accent colors, and consistent internal spacing.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark dashboard background.
- 6× rounded `<rect>` for KPI card containers with subtle gradient fills and shadows.
- 6× narrow `<rect>` accent strips to color-code each KPI module.
- Multiple small `<rect>` elements for bar charts, progress bars, and card microstructure.
- Multiple `<line>` elements for chart axes, gridlines, and subtle dividers.
- Multiple `<path>` elements for sparkline charts, filled chart areas, donut segments, decorative blobs, and simple editable icons.
- 6× `<circle>` elements for icon badges.
- 1× `<linearGradient>` background plus additional gradients for cards, chart fills, and accent bars.
- 1× `<radialGradient>` for ambient background glow.
- 1× `<filter id="softShadow">` applied to card rectangles.
- 1× `<filter id="neonGlow">` applied to selected chart paths and decorative accent shapes.
- Multiple `<text>` elements with explicit `width` attributes for dashboard title, labels, KPI values, deltas, and chart annotations.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#342844"/>
      <stop offset="55%" stop-color="#4C3A5A"/>
      <stop offset="100%" stop-color="#263F59"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="70%" cy="18%" r="60%">
      <stop offset="0%" stop-color="#00D6FF" stop-opacity="0.28"/>
      <stop offset="55%" stop-color="#7B61FF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#625079" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="#3B3150" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#FF9F1C"/>
      <stop offset="100%" stop-color="#FFD700"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#00A7FF"/>
      <stop offset="100%" stop-color="#00FFFF"/>
    </linearGradient>
    <linearGradient id="pinkGrad" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF4D9D"/>
      <stop offset="100%" stop-color="#FFA3D7"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#2CE59B"/>
      <stop offset="100%" stop-color="#B7FF4A"/>
    </linearGradient>
    <linearGradient id="areaCyan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#00FFFF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#00FFFF" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambientGlow)"/>
  <path d="M1030,18 C1130,10 1210,74 1230,162 C1254,268 1175,324 1078,305 C986,287 931,210 948,124 C958,70 982,31 1030,18 Z" fill="#00FFFF" opacity="0.10" filter="url(#neonGlow)"/>
  <path d="M-70,530 C35,470 116,520 146,612 C176,704 66,756 -44,720 Z" fill="#FFD700" opacity="0.10"/>

  <text x="48" y="54" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF" letter-spacing="1.5">BUSINESS PERFORMANCE DASHBOARD</text>
  <text x="50" y="82" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D8D3E4" opacity="0.86">Q2 executive summary · live KPI snapshot · refreshed 08:30</text>
  <rect x="1038" y="42" width="194" height="38" rx="19" fill="#FFFFFF" opacity="0.10"/>
  <circle cx="1063" cy="61" r="7" fill="#2CE59B" filter="url(#neonGlow)"/>
  <text x="1080" y="66" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">SYSTEM HEALTHY</text>

  <rect x="48" y="116" width="372" height="250" rx="22" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="48" y="116" width="372" height="5" rx="2.5" fill="url(#goldGrad)"/>
  <circle cx="83" cy="153" r="18" fill="#FFD700" opacity="0.18"/>
  <path d="M73,158 L80,151 L88,156 L96,143" fill="none" stroke="#FFD700" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="112" y="151" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">SALES GROWTH</text>
  <text x="112" y="176" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">$13.5M</text>
  <text x="286" y="172" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2CE59B">▲ 18.4%</text>
  <line x1="82" y1="312" x2="386" y2="312" stroke="#FFFFFF" stroke-opacity="0.18"/>
  <line x1="82" y1="266" x2="386" y2="266" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="82" y1="220" x2="386" y2="220" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <rect x="92" y="275" width="27" height="37" rx="5" fill="url(#goldGrad)"/>
  <rect x="140" y="249" width="27" height="63" rx="5" fill="url(#goldGrad)"/>
  <rect x="188" y="243" width="27" height="69" rx="5" fill="url(#goldGrad)"/>
  <rect x="236" y="229" width="27" height="83" rx="5" fill="url(#goldGrad)"/>
  <rect x="284" y="207" width="27" height="105" rx="5" fill="url(#goldGrad)"/>
  <rect x="332" y="184" width="27" height="128" rx="5" fill="url(#goldGrad)"/>
  <text x="88" y="338" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#D8D3E4">Jan        Feb        Mar        Apr        May        Jun</text>

  <rect x="454" y="116" width="372" height="250" rx="22" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="454" y="116" width="372" height="5" rx="2.5" fill="url(#cyanGrad)"/>
  <circle cx="489" cy="153" r="18" fill="#00FFFF" opacity="0.16"/>
  <path d="M479,161 C486,143 496,143 503,161 M482,154 L500,154" fill="none" stroke="#00FFFF" stroke-width="3.5" stroke-linecap="round"/>
  <text x="518" y="151" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">PRODUCT RANKING</text>
  <text x="518" y="176" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">#2</text>
  <text x="692" y="172" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFD700">+4 pts</text>
  <path d="M490,314 L490,218 L790,218" fill="none" stroke="#FFFFFF" stroke-opacity="0.16"/>
  <line x1="490" y1="282" x2="790" y2="282" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <line x1="490" y1="250" x2="790" y2="250" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <path d="M492,300 C538,276 568,292 606,260 C642,230 678,244 716,210 C746,184 768,194 790,178" fill="none" stroke="#00FFFF" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M492,313 L492,300 C538,276 568,292 606,260 C642,230 678,244 716,210 C746,184 768,194 790,178 L790,313 Z" fill="url(#areaCyan)"/>
  <path d="M492,286 C546,270 586,276 626,250 C674,219 728,232 790,204" fill="none" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
  <text x="492" y="338" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#D8D3E4">2021             2022             2023             2024</text>

  <rect x="860" y="116" width="372" height="250" rx="22" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="860" y="116" width="372" height="5" rx="2.5" fill="url(#pinkGrad)"/>
  <circle cx="895" cy="153" r="18" fill="#FF4D9D" opacity="0.17"/>
  <path d="M887,160 C887,149 903,149 903,160 M895,143 C899,143 902,146 902,150 C902,154 899,157 895,157 C891,157 888,154 888,150 C888,146 891,143 895,143 Z" fill="none" stroke="#FFA3D7" stroke-width="3"/>
  <text x="924" y="151" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">CUSTOMER NPS</text>
  <text x="924" y="176" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">72</text>
  <text x="1098" y="172" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2CE59B">▲ 6</text>
  <path d="M980,296 A70,70 0 1,1 1102,236" fill="none" stroke="#FFFFFF" stroke-width="18" stroke-opacity="0.12" stroke-linecap="round"/>
  <path d="M980,296 A70,70 0 1,1 1115,262" fill="none" stroke="url(#pinkGrad)" stroke-width="18" stroke-linecap="round" filter="url(#neonGlow)"/>
  <text x="1013" y="272" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">78%</text>
  <text x="966" y="334" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#D8D3E4">Promoters rising across enterprise segment</text>

  <rect x="48" y="398" width="372" height="250" rx="22" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="48" y="398" width="372" height="5" rx="2.5" fill="url(#greenGrad)"/>
  <circle cx="83" cy="435" r="18" fill="#2CE59B" opacity="0.16"/>
  <path d="M83,446 C83,432 83,425 83,418 M73,433 C83,433 86,424 76,421 M93,433 C83,433 80,424 90,421" fill="none" stroke="#2CE59B" stroke-width="3" stroke-linecap="round"/>
  <text x="112" y="433" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">MARKET EXPANSION</text>
  <text x="112" y="458" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">42</text>
  <text x="176" y="458" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#D8D3E4">new regions</text>
  <rect x="82" y="508" width="292" height="16" rx="8" fill="#FFFFFF" opacity="0.10"/>
  <rect x="82" y="508" width="226" height="16" rx="8" fill="url(#greenGrad)"/>
  <rect x="82" y="548" width="292" height="16" rx="8" fill="#FFFFFF" opacity="0.10"/>
  <rect x="82" y="548" width="184" height="16" rx="8" fill="#00FFFF"/>
  <rect x="82" y="588" width="292" height="16" rx="8" fill="#FFFFFF" opacity="0.10"/>
  <rect x="82" y="588" width="252" height="16" rx="8" fill="#FFD700"/>
  <text x="82" y="498" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#D8D3E4">EMEA pipeline</text>
  <text x="82" y="538" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#D8D3E4">APAC activation</text>
  <text x="82" y="578" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#D8D3E4">Americas coverage</text>

  <rect x="454" y="398" width="372" height="250" rx="22" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="454" y="398" width="372" height="5" rx="2.5" fill="url(#goldGrad)"/>
  <circle cx="489" cy="435" r="18" fill="#FFD700" opacity="0.17"/>
  <path d="M479,438 L499,438 M483,429 L495,429 M489,421 L489,446" fill="none" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>
  <text x="518" y="433" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">OPERATING MARGIN</text>
  <text x="518" y="458" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">31.2%</text>
  <text x="690" y="454" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFB84D">−1.1%</text>
  <line x1="492" y1="594" x2="790" y2="594" stroke="#FFFFFF" stroke-opacity="0.16"/>
  <path d="M496,560 C526,524 558,538 588,510 C620,480 650,522 680,492 C716,458 752,474 786,446" fill="none" stroke="#FFD700" stroke-width="4" stroke-linecap="round"/>
  <path d="M496,588 C530,568 562,574 594,548 C630,520 660,550 692,532 C724,512 754,516 786,500" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round" stroke-dasharray="7 8"/>
  <text x="492" y="624" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#D8D3E4">Plan                         Actual                         Forecast</text>

  <rect x="860" y="398" width="372" height="250" rx="22" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="860" y="398" width="372" height="5" rx="2.5" fill="url(#cyanGrad)"/>
  <circle cx="895" cy="435" r="18" fill="#00FFFF" opacity="0.16"/>
  <path d="M885,445 L885,425 L904,425 L904,445 M885,434 L904,434" fill="none" stroke="#00FFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="924" y="433" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">DELIVERY RELIABILITY</text>
  <text x="924" y="458" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">94.6%</text>
  <text x="1098" y="454" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2CE59B">▲ 2.8</text>
  <rect x="900" y="512" width="270" height="68" rx="16" fill="#FFFFFF" opacity="0.08"/>
  <path d="M920,560 C950,520 980,550 1010,518 C1042,484 1070,544 1102,504 C1128,472 1148,494 1166,476" fill="none" stroke="#00FFFF" stroke-width="4" stroke-linecap="round" filter="url(#neonGlow)"/>
  <circle cx="920" cy="560" r="4" fill="#00FFFF"/>
  <circle cx="1010" cy="518" r="4" fill="#00FFFF"/>
  <circle cx="1102" cy="504" r="4" fill="#00FFFF"/>
  <circle cx="1166" cy="476" r="4" fill="#00FFFF"/>
  <text x="906" y="613" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#D8D3E4">SLA breach risk remains low; logistics volatility contained.</text>
</svg>
```

## Avoid in this skill
- ❌ Overcrowding the grid with long narrative text; each card should stay KPI-first and chart-second.
- ❌ Using inconsistent card sizes or uneven gutters; the technique depends on strict modular alignment.
- ❌ Applying `filter` effects to `<line>` chart gridlines; use filters only on card rectangles, paths, circles, or text.
- ❌ Building charts as screenshots when simple editable SVG bars, paths, and axes will translate better to PowerPoint.
- ❌ Using `clip-path` on card shapes or chart groups; clipping should only be used for images if a dashboard card needs a photo/avatar.

## Composition notes
- Keep the title band shallow, around 90–105 px high, so the dashboard grid dominates the slide.
- Use a 3×2 grid for high-density executive dashboards; preserve equal gutters of roughly 24–36 px between modules.
- Inside each card, reserve the top third for icon, title, KPI number, and delta; reserve the lower two-thirds for the chart.
- Use one dark neutral card treatment throughout, then rotate accent colors by KPI category to create rhythm without visual chaos.