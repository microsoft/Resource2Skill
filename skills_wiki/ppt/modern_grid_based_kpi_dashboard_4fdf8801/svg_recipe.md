# SVG Recipe — Modern Grid-Based KPI Dashboard

## Visual mechanism
A structured executive dashboard built from a crisp modular grid: each white panel owns one chart type, while a right-side vertical KPI rail gives instant numeric highlights. The slide feels premium through disciplined spacing, muted accent colors, soft card elevation, and editable SVG-native mini charts rather than rasterized chart screenshots.

## SVG primitives needed
- 1× `<rect>` for the full-slide off-white background.
- 7× `<rect>` for dashboard cards/panels with rounded corners and soft elevation.
- 20+× `<rect>` for bar charts, KPI card accent strips, progress bars, and small legend swatches.
- 10+× `<circle>` for donut chart segments, KPI icon containers, line-chart points, and status dots.
- 8× `<path>` for area fills, trend lines, sparklines, and simple editable KPI icons.
- 15+× `<line>` for subtle grid lines, axes, separators, and benchmark ticks.
- 1× `<radialGradient>` for a restrained background glow.
- 3× `<linearGradient>` for area-chart fill, KPI card color wash, and purple metric emphasis.
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge`, applied only to card `<rect>` elements.
- Multiple `<text>` elements with explicit `width` attributes for slide title, chart titles, values, labels, axes, and legends.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="18%" cy="12%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f2f2f2"/>
    </radialGradient>
    <linearGradient id="purpleWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#664EA3"/>
      <stop offset="100%" stop-color="#8A75C6"/>
    </linearGradient>
    <linearGradient id="tealWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1AAF9A"/>
      <stop offset="100%" stop-color="#5DD4C7"/>
    </linearGradient>
    <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#664EA3" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#664EA3" stop-opacity="0.04"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <text x="44" y="48" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#333333">Digital Performance Dashboard</text>
  <text x="44" y="77" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7a7a7a">Executive KPI snapshot · Q3 operating metrics · updated 09:00</text>
  <text x="1044" y="58" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#8a8a8a">Target attainment: 91%</text>
  <rect x="1056" y="67" width="178" height="7" rx="3.5" fill="#dedede"/>
  <rect x="1056" y="67" width="162" height="7" rx="3.5" fill="#1AAF9A"/>

  <rect x="44" y="106" width="280" height="190" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="348" y="106" width="260" height="190" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="632" y="106" width="284" height="190" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="44" y="326" width="872" height="338" rx="18" fill="#ffffff" filter="url(#softShadow)"/>

  <text x="68" y="138" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#595959">Traffic Sources</text>
  <circle cx="175" cy="207" r="48" fill="none" stroke="#eeeeee" stroke-width="19"/>
  <circle cx="175" cy="207" r="48" fill="none" stroke="#1AAF9A" stroke-width="19" stroke-dasharray="218 302" transform="rotate(-90 175 207)"/>
  <circle cx="175" cy="207" r="48" fill="none" stroke="#664EA3" stroke-width="19" stroke-dasharray="36 302" stroke-dashoffset="-222" transform="rotate(-90 175 207)"/>
  <circle cx="175" cy="207" r="48" fill="none" stroke="#5D85BE" stroke-width="19" stroke-dasharray="25 302" stroke-dashoffset="-262" transform="rotate(-90 175 207)"/>
  <circle cx="175" cy="207" r="48" fill="none" stroke="#AA99CC" stroke-width="19" stroke-dasharray="18 302" stroke-dashoffset="-291" transform="rotate(-90 175 207)"/>
  <text x="132" y="202" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" text-anchor="middle" fill="#333333">76%</text>
  <text x="132" y="223" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="10" text-anchor="middle" fill="#8a8a8a">Direct</text>
  <rect x="248" y="164" width="9" height="9" rx="2" fill="#1AAF9A"/><text x="263" y="172" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Direct</text>
  <rect x="248" y="184" width="9" height="9" rx="2" fill="#664EA3"/><text x="263" y="192" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Organic</text>
  <rect x="248" y="204" width="9" height="9" rx="2" fill="#5D85BE"/><text x="263" y="212" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Paid</text>
  <rect x="248" y="224" width="9" height="9" rx="2" fill="#AA99CC"/><text x="263" y="232" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#666666">Social</text>

  <text x="372" y="138" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#595959">Visitor Type</text>
  <line x1="386" y1="247" x2="570" y2="247" stroke="#d8d8d8" stroke-width="1"/>
  <line x1="386" y1="215" x2="570" y2="215" stroke="#eeeeee" stroke-width="1"/>
  <line x1="386" y1="183" x2="570" y2="183" stroke="#eeeeee" stroke-width="1"/>
  <rect x="410" y="172" width="54" height="75" rx="7" fill="#664EA3"/>
  <rect x="492" y="215" width="54" height="32" rx="7" fill="#AA99CC"/>
  <text x="410" y="163" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#595959">70</text>
  <text x="492" y="206" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#595959">30</text>
  <text x="398" y="269" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#777777">New</text>
  <text x="480" y="269" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#777777">Returning</text>

  <text x="656" y="138" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#595959">Conversion Funnel</text>
  <rect x="666" y="164" width="206" height="22" rx="11" fill="#664EA3"/>
  <rect x="666" y="199" width="158" height="22" rx="11" fill="#5D85BE"/>
  <rect x="666" y="234" width="104" height="22" rx="11" fill="#1AAF9A"/>
  <text x="886" y="180" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">100%</text>
  <text x="886" y="215" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">77%</text>
  <text x="886" y="250" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#666666">51%</text>
  <text x="666" y="284" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8a8a8a">Visits → Qualified → Purchases</text>

  <text x="68" y="360" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#595959">Visits by Week of Year</text>
  <text x="790" y="360" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#8a8a8a">in thousands</text>
  <line x1="90" y1="597" x2="874" y2="597" stroke="#d8d8d8" stroke-width="1"/>
  <line x1="90" y1="545" x2="874" y2="545" stroke="#eeeeee" stroke-width="1"/>
  <line x1="90" y1="493" x2="874" y2="493" stroke="#eeeeee" stroke-width="1"/>
  <line x1="90" y1="441" x2="874" y2="441" stroke="#eeeeee" stroke-width="1"/>
  <line x1="90" y1="389" x2="874" y2="389" stroke="#eeeeee" stroke-width="1"/>
  <path d="M92 597 L92 572 L147 553 L202 519 L257 532 L312 501 L367 453 L422 431 L477 438 L532 392 L587 421 L642 477 L697 503 L752 514 L807 539 L862 557 L862 597 Z" fill="url(#areaFill)"/>
  <path d="M92 572 L147 553 L202 519 L257 532 L312 501 L367 453 L422 431 L477 438 L532 392 L587 421 L642 477 L697 503 L752 514 L807 539 L862 557" fill="none" stroke="#664EA3" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="532" cy="392" r="5" fill="#ffffff" stroke="#664EA3" stroke-width="3"/>
  <circle cx="422" cy="431" r="4" fill="#664EA3"/>
  <circle cx="587" cy="421" r="4" fill="#664EA3"/>
  <text x="82" y="620" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">W1</text>
  <text x="254" y="620" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">W4</text>
  <text x="416" y="620" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">W7</text>
  <text x="582" y="620" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">W10</text>
  <text x="746" y="620" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777777">W13</text>
  <text x="70" y="600" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="10" text-anchor="end" fill="#999999">0</text>
  <text x="70" y="444" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="10" text-anchor="end" fill="#999999">30</text>
  <text x="70" y="392" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="10" text-anchor="end" fill="#999999">40</text>

  <rect x="956" y="106" width="280" height="126" rx="20" fill="url(#purpleWash)" filter="url(#softShadow)"/>
  <rect x="956" y="250" width="280" height="126" rx="20" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="956" y="394" width="280" height="126" rx="20" fill="#ffffff" filter="url(#softShadow)"/>
  <rect x="956" y="538" width="280" height="126" rx="20" fill="url(#tealWash)" filter="url(#softShadow)"/>

  <circle cx="992" cy="145" r="16" fill="#ffffff" opacity="0.18"/>
  <path d="M984 145 L990 151 L1003 137" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1018" y="150" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff" opacity="0.86">Revenue</text>
  <text x="984" y="192" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#ffffff">$4.8M</text>
  <text x="1160" y="190" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff">▲ 12%</text>

  <circle cx="992" cy="289" r="16" fill="#F0EDFA"/>
  <path d="M984 292 C988 282 996 282 1002 292" fill="none" stroke="#664EA3" stroke-width="3" stroke-linecap="round"/>
  <text x="1018" y="294" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">Active Users</text>
  <text x="984" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#333333">128K</text>
  <path d="M1152 334 L1166 322 L1180 328 L1202 303" fill="none" stroke="#1AAF9A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="992" cy="433" r="16" fill="#E9F7F5"/>
  <path d="M986 433 L998 433 M992 427 L992 439" fill="none" stroke="#1AAF9A" stroke-width="3" stroke-linecap="round"/>
  <text x="1018" y="438" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">Avg. Order Value</text>
  <text x="984" y="480" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#333333">$76</text>
  <rect x="1146" y="454" width="58" height="10" rx="5" fill="#e6e6e6"/>
  <rect x="1146" y="454" width="43" height="10" rx="5" fill="#664EA3"/>

  <circle cx="992" cy="577" r="16" fill="#ffffff" opacity="0.22"/>
  <path d="M984 577 C990 566 999 566 1005 577 C999 588 990 588 984 577 Z" fill="none" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>
  <text x="1018" y="582" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff" opacity="0.9">Retention</text>
  <text x="984" y="624" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#ffffff">84%</text>
  <text x="1152" y="624" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff">▲ 5.4</text>
</svg>
```

## Avoid in this skill
- ❌ Rasterizing charts into screenshots; keep donuts, bars, lines, and areas as editable SVG shapes.
- ❌ Overloading every panel with full axes, dense ticks, or tiny legends; dashboard panels should be scannable at presentation distance.
- ❌ Heavy 3D effects, bevels, or noisy gradients that compete with the data hierarchy.
- ❌ Applying `filter` to `<line>` elements for glowing axes or chart lines; use filters only on card rectangles or supported shape types.
- ❌ Using `marker-end` for arrows in sparklines or trend callouts; draw arrow-like trend strokes as simple `<path>` or use separate `<line>` elements if needed.

## Composition notes
- Reserve roughly 70% of the width for chart panels and 25% for a right-side KPI rail; keep gutters consistent, usually 24–32 px.
- Use white cards on a very light gray background, then repeat 2–3 accent colors across charts and KPI cards for visual rhythm.
- Put the most important trend chart in a wide lower panel; smaller composition or comparison charts work best in the top row.
- KPI values should be the largest text on the slide after the title, with labels and deltas secondary but still highly legible.