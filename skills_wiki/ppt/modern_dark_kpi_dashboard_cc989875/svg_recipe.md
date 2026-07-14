# SVG Recipe — Modern Dark KPI Dashboard

## Visual mechanism
A premium dark dashboard built from neon-edged rounded cards on a deep navy canvas, with each card containing one KPI and a compact native SVG chart. High-contrast orange KPI values, pink outlines, green/red status signals, and subtle glows create a polished executive BI aesthetic.

## SVG primitives needed
- 1× `<rect>` for the full dark background
- 1× `<rect>` for the orange header band
- 8× `<rect>` for modular rounded KPI panels
- Multiple `<text>` elements with explicit `width=` for title, labels, KPI values, and chart annotations
- Multiple `<line>` elements for chart axes, gridlines, and small tick marks
- Multiple `<rect>` elements for bar charts, progress bars, and status pills
- Multiple `<circle>` elements for line-chart markers, status dots, and gauge centers
- Multiple `<path>` elements for area chart fills, trend lines, and donut/gauge arcs
- 2× `<linearGradient>` for background/header/panel depth
- 1× `<filter id="cardShadow">` for soft card elevation
- 1× `<filter id="softGlow">` for ambient neon glow on accent shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111c31"/>
      <stop offset="60%" stop-color="#172338"/>
      <stop offset="100%" stop-color="#0b1221"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff6600"/>
      <stop offset="100%" stop-color="#f48e3c"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#273f66"/>
      <stop offset="100%" stop-color="#203350"/>
    </linearGradient>
    <linearGradient id="areaFill" x1="0" y1="120" x2="0" y2="300">
      <stop offset="0%" stop-color="#77da66" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#77da66" stop-opacity="0.04"/>
    </linearGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
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

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1160" cy="110" r="120" fill="#ee2667" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="100" cy="650" r="150" fill="#ff6600" opacity="0.10" filter="url(#softGlow)"/>

  <rect x="0" y="0" width="1280" height="76" fill="url(#headerGrad)"/>
  <text x="40" y="50" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff">Executive Performance Dashboard</text>
  <text x="1000" y="32" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff" opacity="0.92" text-anchor="end">Q2 Business Review</text>
  <text x="1000" y="55" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff" text-anchor="end">Updated 11 Jun 2026</text>

  <rect x="40" y="104" width="300" height="190" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="62" y="136" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">TOTAL REVENUE</text>
  <text x="62" y="183" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#f48e3c">$42.8M</text>
  <rect x="237" y="125" width="72" height="28" rx="14" fill="#77da66" opacity="0.18" stroke="#77da66"/>
  <text x="251" y="145" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#77da66">+18%</text>
  <line x1="66" y1="238" x2="304" y2="238" stroke="#ffffff" stroke-opacity="0.14"/>
  <path d="M70 248 L95 232 L120 240 L145 214 L170 222 L195 194 L220 204 L245 176 L270 184 L305 158" fill="none" stroke="#77da66" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="305" cy="158" r="5" fill="#77da66"/>

  <rect x="370" y="104" width="520" height="190" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="394" y="136" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">MONTHLY PIPELINE TREND</text>
  <text x="752" y="136" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#f48e3c" text-anchor="end">Target 96%</text>
  <line x1="404" y1="250" x2="850" y2="250" stroke="#ffffff" stroke-opacity="0.12"/>
  <line x1="404" y1="212" x2="850" y2="212" stroke="#ffffff" stroke-opacity="0.10"/>
  <line x1="404" y1="174" x2="850" y2="174" stroke="#ffffff" stroke-opacity="0.10"/>
  <path d="M405 246 L445 224 L485 230 L525 195 L565 202 L605 168 L645 176 L685 146 L725 156 L765 132 L810 140 L850 116 L850 255 L405 255 Z" fill="url(#areaFill)"/>
  <path d="M405 246 L445 224 L485 230 L525 195 L565 202 L605 168 L645 176 L685 146 L725 156 L765 132 L810 140 L850 116" fill="none" stroke="#77da66" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M405 206 L850 206" fill="none" stroke="#ff0066" stroke-width="2" stroke-dasharray="8 8"/>
  <text x="405" y="277" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff" opacity="0.72">Jan</text>
  <text x="548" y="277" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff" opacity="0.72">Apr</text>
  <text x="690" y="277" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff" opacity="0.72">Jul</text>
  <text x="832" y="277" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff" opacity="0.72">Dec</text>

  <rect x="920" y="104" width="320" height="190" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="944" y="136" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">CUSTOMER HEALTH</text>
  <path d="M988 230 A76 76 0 1 1 1152 230" fill="none" stroke="#334b71" stroke-width="22" stroke-linecap="round"/>
  <path d="M988 230 A76 76 0 0 1 1124 172" fill="none" stroke="#77da66" stroke-width="22" stroke-linecap="round"/>
  <path d="M1127 174 A76 76 0 0 1 1152 230" fill="none" stroke="#f48e3c" stroke-width="22" stroke-linecap="round"/>
  <text x="1032" y="222" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#ffffff" text-anchor="middle">84</text>
  <text x="1032" y="248" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff" opacity="0.75" text-anchor="middle">HEALTH SCORE</text>

  <rect x="40" y="322" width="300" height="150" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="62" y="354" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">ACTIVE USERS</text>
  <text x="62" y="398" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#f48e3c">128K</text>
  <rect x="220" y="360" width="20" height="76" rx="5" fill="#77da66"/>
  <rect x="248" y="338" width="20" height="98" rx="5" fill="#f48e3c"/>
  <rect x="276" y="383" width="20" height="53" rx="5" fill="#ff0066"/>
  <text x="62" y="443" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff" opacity="0.78">+12.4K net new this month</text>

  <rect x="370" y="322" width="250" height="150" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="394" y="354" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">UPTIME</text>
  <text x="394" y="404" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#77da66">99.97%</text>
  <rect x="394" y="430" width="182" height="12" rx="6" fill="#314967"/>
  <rect x="394" y="430" width="176" height="12" rx="6" fill="#77da66"/>

  <rect x="640" y="322" width="250" height="150" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="664" y="354" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">OPEN RISKS</text>
  <text x="664" y="404" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#ff0066">17</text>
  <circle cx="798" cy="390" r="36" fill="#ff0066" opacity="0.14"/>
  <circle cx="798" cy="390" r="24" fill="#ff0066"/>
  <text x="780" y="397" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle">!</text>
  <text x="664" y="443" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff" opacity="0.78">5 high-priority escalations</text>

  <rect x="920" y="322" width="320" height="150" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="944" y="354" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">SLA COMPLIANCE</text>
  <text x="944" y="401" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#f48e3c">92.6%</text>
  <line x1="1080" y1="432" x2="1200" y2="432" stroke="#ffffff" stroke-opacity="0.2"/>
  <path d="M1080 426 L1100 408 L1120 414 L1140 386 L1160 394 L1180 372 L1200 378" fill="none" stroke="#77da66" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="40" y="500" width="580" height="170" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="62" y="532" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">REGIONAL PERFORMANCE</text>
  <text x="62" y="570" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff" opacity="0.75">North</text>
  <text x="62" y="602" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff" opacity="0.75">West</text>
  <text x="62" y="634" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff" opacity="0.75">APAC</text>
  <rect x="132" y="558" width="410" height="14" rx="7" fill="#314967"/>
  <rect x="132" y="590" width="410" height="14" rx="7" fill="#314967"/>
  <rect x="132" y="622" width="410" height="14" rx="7" fill="#314967"/>
  <rect x="132" y="558" width="350" height="14" rx="7" fill="#77da66"/>
  <rect x="132" y="590" width="286" height="14" rx="7" fill="#f48e3c"/>
  <rect x="132" y="622" width="224" height="14" rx="7" fill="#ff0066"/>
  <text x="552" y="570" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">86%</text>
  <text x="552" y="602" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">70%</text>
  <text x="552" y="634" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">55%</text>

  <rect x="640" y="500" width="600" height="170" rx="18" fill="url(#panelGrad)" stroke="#ee2667" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="664" y="532" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">EXECUTIVE SUMMARY</text>
  <circle cx="684" cy="572" r="6" fill="#77da66"/>
  <text x="704" y="577" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff">Revenue growth is ahead of plan across enterprise accounts.</text>
  <circle cx="684" cy="612" r="6" fill="#f48e3c"/>
  <text x="704" y="617" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff">SLA dip isolated to two regions; mitigation in progress.</text>
  <circle cx="684" cy="652" r="6" fill="#ff0066"/>
  <text x="704" y="657" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff">High-priority risks require sponsor decisions this week.</text>
</svg>
```

## Avoid in this skill
- ❌ Using embedded HTML dashboards via `<foreignObject>`; build the dashboard from native SVG shapes instead.
- ❌ Using real SVG `<chart>` abstractions or external chart libraries; approximate charts with editable `<rect>`, `<line>`, `<circle>`, and `<path>`.
- ❌ Applying `filter` to `<line>` elements; use glows/shadows on cards, circles, paths, and text instead.
- ❌ Overcrowding every panel with labels; dark dashboards need generous padding and simplified microcharts.
- ❌ Using `<pattern>` fills for grids or textures; use low-opacity lines, gradients, and blurred accent circles.

## Composition notes
- Keep the header strong and shallow: about 10% of slide height, with the main title left-aligned or centered and metadata on the right.
- Use a consistent 20–30 px gutter between cards; the dashboard should feel like a controlled grid, not a collage.
- Reserve orange for primary KPI numbers, pink for outlines/risk accents, green for positive performance, and muted blue-gray for chart baselines.
- Make one wide trend card the visual anchor, then surround it with smaller KPI cards and summary panels for scannability.