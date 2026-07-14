# SVG Recipe — Sleek Sales Performance Dashboard

## Visual mechanism
A premium analytics dashboard built from elevated white cards on a cool gray canvas, combining bold KPI tiles with larger chart widgets. The visual polish comes from consistent grid spacing, soft card shadows, restrained color accents, and miniature editable charts drawn directly as SVG shapes.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 6× `<rect>` for rounded dashboard cards with soft shadows
- 4× `<rect>` for colored KPI icon badges
- 12× `<path>` for minimalist KPI icons, donut segments, sparkline/area chart shapes, and decorative background accents
- 18× `<rect>` for editable bar charts, progress bars, and small metric chips
- 9× `<line>` for chart gridlines and axis dividers
- 8× `<circle>` for line-chart data points and donut center labeling accents
- 1× `<linearGradient>` for the blue chart area fill
- 1× `<radialGradient>` for the subtle background glow
- 1× `<filter id="cardShadow">` applied to card rectangles
- Multiple `<text>` elements with explicit `width` attributes for dashboard title, KPI labels, values, deltas, legends, and chart annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="80%" cy="8%" r="55%">
      <stop offset="0%" stop-color="#E8F1FF"/>
      <stop offset="55%" stop-color="#F8F9FB"/>
      <stop offset="100%" stop-color="#F8F9FB"/>
    </radialGradient>
    <linearGradient id="areaBlue" x1="0" y1="295" x2="0" y2="585" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4285F4" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#4285F4" stop-opacity="0.03"/>
    </linearGradient>
    <filter id="cardShadow" x="-8%" y="-8%" width="116%" height="124%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .14 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <path d="M1040 0 C1160 15 1240 80 1280 160 L1280 0 Z" fill="#DDEAFF" opacity="0.65"/>
  <path d="M0 650 C120 610 240 625 330 720 L0 720 Z" fill="#EAF2FF" opacity="0.75"/>

  <text x="48" y="49" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#202124">Sales Performance Dashboard</text>
  <text x="48" y="76" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Q4 revenue health, pipeline velocity, and channel contribution</text>
  <rect x="1058" y="39" width="174" height="34" rx="17" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="1081" cy="56" r="5" fill="#34A853"/>
  <text x="1094" y="61" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#3C4043">Live forecast view</text>

  <rect x="48" y="96" width="284" height="142" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="72" y="120" width="42" height="42" rx="13" fill="#E8F0FE"/>
  <path d="M84 148 L94 138 L102 144 L112 130" fill="none" stroke="#4285F4" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="72" y="181" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Total Revenue</text>
  <text x="72" y="218" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">$8.42M</text>
  <text x="222" y="218" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#14A753">▲ 12.8%</text>

  <rect x="348" y="96" width="284" height="142" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="372" y="120" width="42" height="42" rx="13" fill="#E9F7EF"/>
  <path d="M386 134 C386 127 400 127 400 134 C400 143 386 143 386 152 M382 152 L405 152" fill="none" stroke="#34A853" stroke-width="4" stroke-linecap="round"/>
  <text x="372" y="181" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Qualified Leads</text>
  <text x="372" y="218" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">14,892</text>
  <text x="528" y="218" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#14A753">▲ 8.1%</text>

  <rect x="648" y="96" width="284" height="142" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="672" y="120" width="42" height="42" rx="13" fill="#FFF7E0"/>
  <path d="M685 150 L693 128 L702 150 Z M682 154 L705 154" fill="none" stroke="#FBBC05" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="672" y="181" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Avg. Deal Size</text>
  <text x="672" y="218" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">$42.7K</text>
  <text x="820" y="218" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#D64537">▼ 2.4%</text>

  <rect x="948" y="96" width="284" height="142" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="972" y="120" width="42" height="42" rx="13" fill="#FCEAE8"/>
  <path d="M985 152 C982 143 986 132 993 129 C1001 132 1005 143 1002 152 M987 152 L1000 152" fill="none" stroke="#D64537" stroke-width="4" stroke-linecap="round"/>
  <text x="972" y="181" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Churn Risk</text>
  <text x="972" y="218" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">3.9%</text>
  <text x="1110" y="218" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#14A753">▼ 1.6%</text>

  <rect x="48" y="265" width="575" height="395" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="78" y="307" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#202124">Revenue Trend</text>
  <text x="78" y="331" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6B7280">Monthly bookings vs. expansion uplift</text>
  <rect x="482" y="286" width="103" height="28" rx="14" fill="#EFF6FF"/>
  <text x="502" y="305" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#4285F4">FY 2025</text>
  <line x1="90" y1="388" x2="570" y2="388" stroke="#EEF1F5" stroke-width="1"/>
  <line x1="90" y1="442" x2="570" y2="442" stroke="#EEF1F5" stroke-width="1"/>
  <line x1="90" y1="496" x2="570" y2="496" stroke="#EEF1F5" stroke-width="1"/>
  <line x1="90" y1="550" x2="570" y2="550" stroke="#EEF1F5" stroke-width="1"/>
  <path d="M105 548 L105 485 L168 458 L231 472 L294 430 L357 412 L420 382 L483 350 L546 326 L546 548 Z" fill="url(#areaBlue)"/>
  <path d="M105 485 C135 475 144 466 168 458 C196 447 205 485 231 472 C263 457 266 438 294 430 C323 421 328 419 357 412 C389 404 390 391 420 382 C454 371 456 361 483 350 C512 338 521 332 546 326" fill="none" stroke="#4285F4" stroke-width="4" stroke-linecap="round"/>
  <circle cx="105" cy="485" r="5" fill="#4285F4"/>
  <circle cx="168" cy="458" r="5" fill="#4285F4"/>
  <circle cx="231" cy="472" r="5" fill="#4285F4"/>
  <circle cx="294" cy="430" r="5" fill="#4285F4"/>
  <circle cx="357" cy="412" r="5" fill="#4285F4"/>
  <circle cx="420" cy="382" r="5" fill="#4285F4"/>
  <circle cx="483" cy="350" r="5" fill="#4285F4"/>
  <circle cx="546" cy="326" r="5" fill="#4285F4"/>
  <rect x="104" y="568" width="22" height="44" rx="5" fill="#D8E6FD"/>
  <rect x="167" y="548" width="22" height="64" rx="5" fill="#D8E6FD"/>
  <rect x="230" y="558" width="22" height="54" rx="5" fill="#D8E6FD"/>
  <rect x="293" y="525" width="22" height="87" rx="5" fill="#D8E6FD"/>
  <rect x="356" y="510" width="22" height="102" rx="5" fill="#D8E6FD"/>
  <rect x="419" y="490" width="22" height="122" rx="5" fill="#D8E6FD"/>
  <rect x="482" y="468" width="22" height="144" rx="5" fill="#D8E6FD"/>
  <rect x="545" y="438" width="22" height="174" rx="5" fill="#D8E6FD"/>
  <text x="102" y="637" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A9099">May</text>
  <text x="290" y="637" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A9099">Aug</text>
  <text x="478" y="637" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A9099">Nov</text>

  <rect x="648" y="265" width="584" height="395" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="678" y="307" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#202124">Channel Mix & Pipeline</text>
  <text x="678" y="331" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6B7280">Contribution by acquisition source and active opportunity stages</text>
  <path d="M915 380 A82 82 0 0 1 1004 459" fill="none" stroke="#4285F4" stroke-width="28" stroke-linecap="butt"/>
  <path d="M1004 459 A82 82 0 0 1 930 540" fill="none" stroke="#34A853" stroke-width="28" stroke-linecap="butt"/>
  <path d="M930 540 A82 82 0 0 1 838 477" fill="none" stroke="#FBBC05" stroke-width="28" stroke-linecap="butt"/>
  <path d="M838 477 A82 82 0 0 1 915 380" fill="none" stroke="#9AA0A6" stroke-width="28" stroke-linecap="butt"/>
  <circle cx="921" cy="459" r="54" fill="#FFFFFF"/>
  <text x="880" y="455" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280" text-anchor="middle">Top source</text>
  <text x="879" y="485" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111827">42%</text>
  <circle cx="1064" cy="398" r="6" fill="#4285F4"/>
  <text x="1080" y="403" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3C4043">Inbound 42%</text>
  <circle cx="1064" cy="426" r="6" fill="#34A853"/>
  <text x="1080" y="431" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3C4043">Partners 28%</text>
  <circle cx="1064" cy="454" r="6" fill="#FBBC05"/>
  <text x="1080" y="459" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3C4043">Outbound 18%</text>
  <circle cx="1064" cy="482" r="6" fill="#9AA0A6"/>
  <text x="1080" y="487" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3C4043">Other 12%</text>
  <line x1="692" y1="555" x2="1194" y2="555" stroke="#EEF1F5" stroke-width="1"/>
  <text x="692" y="584" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6B7280">Prospect</text>
  <rect x="790" y="570" width="324" height="12" rx="6" fill="#EEF1F5"/>
  <rect x="790" y="570" width="284" height="12" rx="6" fill="#4285F4"/>
  <text x="1132" y="584" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#202124">$3.8M</text>
  <text x="692" y="616" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6B7280">Proposal</text>
  <rect x="790" y="602" width="324" height="12" rx="6" fill="#EEF1F5"/>
  <rect x="790" y="602" width="218" height="12" rx="6" fill="#34A853"/>
  <text x="1132" y="616" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#202124">$2.9M</text>
  <text x="692" y="648" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6B7280">Commit</text>
  <rect x="790" y="634" width="324" height="12" rx="6" fill="#EEF1F5"/>
  <rect x="790" y="634" width="152" height="12" rx="6" fill="#FBBC05"/>
  <text x="1132" y="648" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#202124">$2.1M</text>
</svg>
```

## Avoid in this skill
- ❌ Using real PowerPoint chart objects as the only visual plan; SVG should draw editable bars, lines, donut arcs, labels, and legends directly.
- ❌ Applying shadows to `<line>` chart gridlines; use filters only on card `<rect>` elements or decorative paths.
- ❌ Overloading the slide with too many tiny widgets; the executive-dashboard look depends on large readable cards and generous gutters.
- ❌ Using `<foreignObject>` for HTML dashboard components or CSS layout tricks; keep every widget as native SVG primitives.
- ❌ Relying on `marker-end` arrows for trend indicators; use text glyphs like ▲ / ▼ or small custom paths instead.

## Composition notes
- Use a strict grid: wide title band at the top, four equal KPI cards beneath it, and two large chart cards across the lower half.
- Keep the canvas background very light gray-blue; let white cards, soft shadows, and saturated chart accents create hierarchy.
- Place the strongest numbers in the top KPI row, then use the bottom cards for richer visual explanations.
- Maintain consistent gutters of roughly 20–30 px and avoid edge-to-edge charts; premium dashboards breathe.