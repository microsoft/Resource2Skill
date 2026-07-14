# SVG Recipe — Icon-Anchored Flat Ribbon Chart

## Visual mechanism
A small-category bar chart is turned into a polished infographic by removing the conventional axis/legend clutter and anchoring each bar to a vivid circular icon badge. A flat folded ribbon title provides the presentation-style header while direct value labels make the data readable without a Y-axis.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 4× `<line>` for very subtle horizontal reference gridlines and 1× `<line>` for the baseline
- 5× `<rect>` for the vertical colored ribbon bars
- 5× `<circle>` for icon anchor badges beneath the bars
- 10–14× simple `<rect>`, `<circle>`, `<ellipse>`, and `<path>` elements for editable white category icons inside the badges
- 3× `<path>` for the folded ribbon tails and small fold shadows
- 1× `<rect>` for the main title ribbon face
- 5× `<linearGradient>` for slight top-to-bottom bar depth
- 1× `<filter id="softShadow">` applied directly to bars, badges, and the main ribbon
- Multiple `<text width="...">` labels for title, values, category names, and optional scale hints

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="barCyan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#26D6FF"/><stop offset="100%" stop-color="#00A8E8"/>
    </linearGradient>
    <linearGradient id="barGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFD65A"/><stop offset="100%" stop-color="#FFB400"/>
    </linearGradient>
    <linearGradient id="barGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#A8EA4A"/><stop offset="100%" stop-color="#7ED321"/>
    </linearGradient>
    <linearGradient id="barPurple" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#D98AF0"/><stop offset="100%" stop-color="#BA55D3"/>
    </linearGradient>
    <linearGradient id="barBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#70B7FF"/><stop offset="100%" stop-color="#4A90E2"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F5F5"/>

  <!-- Folded flat ribbon title -->
  <path d="M372 96 L258 96 L292 126 L258 156 L372 156 Z" fill="#505F6E"/>
  <path d="M908 96 L1022 96 L988 126 L1022 156 L908 156 Z" fill="#505F6E"/>
  <path d="M372 156 L332 186 L372 156 Z" fill="#3F4B58"/>
  <path d="M908 156 L948 186 L908 156 Z" fill="#3F4B58"/>
  <rect x="340" y="78" width="600" height="78" rx="2" fill="#708090" filter="url(#softShadow)"/>
  <text x="340" y="127" width="600" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">
    Last Year Product Sales
  </text>

  <!-- Minimal reference grid: intentionally pale, no visible Y-axis -->
  <line x1="142" y1="510" x2="1138" y2="510" stroke="#E2E2E2" stroke-width="1"/>
  <line x1="142" y1="430" x2="1138" y2="430" stroke="#E6E6E6" stroke-width="1"/>
  <line x1="142" y1="350" x2="1138" y2="350" stroke="#E6E6E6" stroke-width="1"/>
  <line x1="142" y1="270" x2="1138" y2="270" stroke="#E6E6E6" stroke-width="1"/>
  <line x1="142" y1="570" x2="1138" y2="570" stroke="#CFCFCF" stroke-width="2"/>

  <text x="88" y="274" width="90" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B2B2B2">4k</text>
  <text x="88" y="354" width="90" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B2B2B2">3k</text>
  <text x="88" y="434" width="90" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B2B2B2">2k</text>
  <text x="88" y="514" width="90" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B2B2B2">1k</text>

  <!-- Bars with direct labels -->
  <rect x="209" y="451" width="82" height="119" rx="8" fill="url(#barCyan)" filter="url(#softShadow)"/>
  <rect x="399" y="539" width="82" height="31" rx="8" fill="url(#barGold)" filter="url(#softShadow)"/>
  <rect x="589" y="357" width="82" height="213" rx="8" fill="url(#barGreen)" filter="url(#softShadow)"/>
  <rect x="779" y="386" width="82" height="184" rx="8" fill="url(#barPurple)" filter="url(#softShadow)"/>
  <rect x="969" y="270" width="82" height="300" rx="8" fill="url(#barBlue)" filter="url(#softShadow)"/>

  <text x="250" y="433" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#00A8E8">1,478</text>
  <text x="440" y="521" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#E59A00">381</text>
  <text x="630" y="339" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#65B915">2,640</text>
  <text x="820" y="368" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#A846C5">2,280</text>
  <text x="1010" y="252" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#347FCC">3,715</text>

  <!-- Icon anchor badges -->
  <circle cx="250" cy="617" r="43" fill="#00BFFF" filter="url(#softShadow)"/>
  <circle cx="440" cy="617" r="43" fill="#FFB400" filter="url(#softShadow)"/>
  <circle cx="630" cy="617" r="43" fill="#7ED321" filter="url(#softShadow)"/>
  <circle cx="820" cy="617" r="43" fill="#BA55D3" filter="url(#softShadow)"/>
  <circle cx="1010" cy="617" r="43" fill="#4A90E2" filter="url(#softShadow)"/>

  <!-- Editable white icons: phone, music, laptop, tablet, cloud -->
  <rect x="232" y="589" width="36" height="56" rx="7" fill="#FFFFFF"/>
  <rect x="239" y="597" width="22" height="37" rx="2" fill="#00BFFF"/>
  <circle cx="250" cy="639" r="3" fill="#00BFFF"/>

  <path d="M454 592 L454 628 C454 638 444 644 434 640 C424 636 424 625 435 622 C440 620 445 621 449 624 L449 604 L426 609 L426 634" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="604" y="594" width="52" height="34" rx="4" fill="#FFFFFF"/>
  <rect x="611" y="601" width="38" height="20" rx="2" fill="#7ED321"/>
  <path d="M596 634 L664 634 L654 644 L606 644 Z" fill="#FFFFFF"/>

  <rect x="800" y="588" width="40" height="58" rx="6" fill="#FFFFFF"/>
  <rect x="806" y="597" width="28" height="38" rx="2" fill="#BA55D3"/>
  <circle cx="820" cy="640" r="3" fill="#BA55D3"/>

  <ellipse cx="998" cy="623" rx="25" ry="15" fill="#FFFFFF"/>
  <circle cx="990" cy="613" r="15" fill="#FFFFFF"/>
  <circle cx="1010" cy="609" r="19" fill="#FFFFFF"/>
  <circle cx="1025" cy="623" r="14" fill="#FFFFFF"/>

  <!-- Category names -->
  <text x="250" y="692" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#505050">Phone</text>
  <text x="440" y="692" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#505050">Music</text>
  <text x="630" y="692" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#505050">Mac</text>
  <text x="820" y="692" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#505050">Tablet</text>
  <text x="1010" y="692" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#505050">Services</text>
</svg>
```

## Avoid in this skill
- ❌ Default chart furniture: heavy Y-axis, legend boxes, dense tick labels, or chart-title placeholders.
- ❌ Using emoji text as the only icon treatment; it can render inconsistently across systems. Prefer simple editable SVG icons made from paths, circles, and rectangles.
- ❌ Applying `filter` to gridlines or baseline `<line>` elements; shadows on lines are dropped by the translator.
- ❌ Overloading the chart with more than 7 bars; the icon badges lose their value when squeezed.
- ❌ Using clipped/masked non-image shapes for badge effects; keep badges as native circles with direct fills and shadows.

## Composition notes
- Keep the ribbon title centered in the top 20–25% of the slide; it should feel like a presentation banner, not a chart object.
- Use the middle 55–60% for the bars, leaving generous side margins and removing most axis detail.
- Align every bar center exactly with its badge center; the badge acts as the category label, anchor, and legend simultaneously.
- Use one saturated color per category and repeat that color in the bar, badge, and value label for instant visual grouping.