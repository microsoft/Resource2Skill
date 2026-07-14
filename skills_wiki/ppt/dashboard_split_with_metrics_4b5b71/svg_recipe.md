# SVG Recipe — Dashboard Split with Metrics

## Visual mechanism
A dark executive dashboard split into one dominant primary analytics card on the left, a compact secondary chart card on the top-right, and four KPI metric tiles in a 2×2 grid below. The technique relies on luminous gradients, soft card shadows, thin grid lines, and dense but disciplined chart details to create a premium technical overview.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× blurred decorative `<path>` blobs for atmospheric depth
- 7× rounded `<rect>` cards for the main chart, secondary chart, and four metric tiles
- Multiple `<line>` elements for chart gridlines and subtle dividers
- Multiple `<path>` elements for the area chart, trend lines, sparklines, and decorative glows
- Multiple `<rect>` elements for bar-chart overlays and tiny metric indicators
- Multiple `<circle>` elements for data points and the donut chart rings
- Multiple `<text>` elements with explicit `width` for title, labels, chart annotations, KPI values, and legends
- 4× `<linearGradient>` definitions for background, cards, and accent fills
- 1× `<radialGradient>` for chart glow accents
- 2× `<filter>` definitions: one soft shadow for cards and one blur/glow for atmospheric shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.55" stop-color="#0B1628"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#172338"/>
      <stop offset="1" stop-color="#0D1423"/>
    </linearGradient>
    <linearGradient id="areaGrad" x1="0" y1="150" x2="0" y2="570">
      <stop offset="0" stop-color="#33D6FF" stop-opacity="0.52"/>
      <stop offset="1" stop-color="#33D6FF" stop-opacity="0.03"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="80" y1="0" x2="760" y2="0">
      <stop offset="0" stop-color="#33D6FF"/>
      <stop offset="0.55" stop-color="#7C5CFF"/>
      <stop offset="1" stop-color="#FF4FD8"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#53FFB7"/>
      <stop offset="1" stop-color="#1DCE87"/>
    </linearGradient>
    <radialGradient id="cyanGlow" cx="50%" cy="40%" r="70%">
      <stop offset="0" stop-color="#33D6FF" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#33D6FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-60,118 C170,8 281,34 383,154 C229,208 74,260 -60,230 Z" fill="#2367FF" opacity="0.26" filter="url(#glow)"/>
  <path d="M1040,602 C1162,492 1305,496 1370,658 C1230,750 1116,748 1012,690 Z" fill="#A855F7" opacity="0.28" filter="url(#glow)"/>

  <text x="40" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F7FAFC">Executive Performance Dashboard</text>
  <text x="43" y="86" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8EA3BE">Revenue, adoption, and operational health across the current quarter</text>
  <rect x="1030" y="36" width="200" height="42" rx="21" fill="#101A2B" stroke="#263852"/>
  <circle cx="1054" cy="57" r="6" fill="#53FFB7"/>
  <text x="1070" y="63" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#CDE7FF">LIVE Q4 UPDATE</text>

  <rect x="40" y="110" width="760" height="560" rx="28" fill="url(#cardGrad)" stroke="#263852" filter="url(#shadow)"/>
  <text x="72" y="154" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#F5F9FF">Primary Growth Curve</text>
  <text x="72" y="178" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA3BE">Monthly recurring revenue with expansion overlay</text>
  <text x="643" y="153" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" text-anchor="end" fill="#FFFFFF">$18.4M</text>
  <text x="642" y="178" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="end" fill="#53FFB7">+22.8% YoY</text>

  <line x1="92" y1="238" x2="748" y2="238" stroke="#24344D" stroke-width="1"/>
  <line x1="92" y1="296" x2="748" y2="296" stroke="#24344D" stroke-width="1"/>
  <line x1="92" y1="354" x2="748" y2="354" stroke="#24344D" stroke-width="1"/>
  <line x1="92" y1="412" x2="748" y2="412" stroke="#24344D" stroke-width="1"/>
  <line x1="92" y1="470" x2="748" y2="470" stroke="#24344D" stroke-width="1"/>
  <line x1="92" y1="528" x2="748" y2="528" stroke="#24344D" stroke-width="1"/>

  <rect x="132" y="445" width="26" height="83" rx="6" fill="#1E88E5" opacity="0.32"/>
  <rect x="220" y="412" width="26" height="116" rx="6" fill="#1E88E5" opacity="0.32"/>
  <rect x="308" y="385" width="26" height="143" rx="6" fill="#1E88E5" opacity="0.32"/>
  <rect x="396" y="352" width="26" height="176" rx="6" fill="#1E88E5" opacity="0.32"/>
  <rect x="484" y="318" width="26" height="210" rx="6" fill="#1E88E5" opacity="0.32"/>
  <rect x="572" y="286" width="26" height="242" rx="6" fill="#1E88E5" opacity="0.32"/>
  <rect x="660" y="252" width="26" height="276" rx="6" fill="#1E88E5" opacity="0.32"/>

  <path d="M92,528 L92,455 C142,430 183,462 224,405 C263,351 309,381 350,330 C391,277 430,317 471,292 C512,266 554,231 595,260 C635,288 683,194 748,180 L748,528 Z" fill="url(#areaGrad)"/>
  <path d="M92,455 C142,430 183,462 224,405 C263,351 309,381 350,330 C391,277 430,317 471,292 C512,266 554,231 595,260 C635,288 683,194 748,180" fill="none" stroke="url(#accentGrad)" stroke-width="5" stroke-linecap="round"/>
  <path d="M92,492 C150,476 190,488 242,455 C306,416 356,438 414,396 C472,354 535,362 594,330 C642,304 692,292 748,258" fill="none" stroke="#53FFB7" stroke-width="3" stroke-linecap="round" opacity="0.78"/>

  <circle cx="224" cy="405" r="6" fill="#FFFFFF" stroke="#33D6FF" stroke-width="4"/>
  <circle cx="350" cy="330" r="6" fill="#FFFFFF" stroke="#7C5CFF" stroke-width="4"/>
  <circle cx="471" cy="292" r="6" fill="#FFFFFF" stroke="#7C5CFF" stroke-width="4"/>
  <circle cx="595" cy="260" r="6" fill="#FFFFFF" stroke="#33D6FF" stroke-width="4"/>
  <circle cx="748" cy="180" r="8" fill="#FFFFFF" stroke="#FF4FD8" stroke-width="4"/>
  <rect x="600" y="206" width="124" height="44" rx="14" fill="#0B1220" stroke="#354866"/>
  <text x="618" y="225" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8EA3BE">Forecast peak</text>
  <text x="618" y="242" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">+31.2%</text>

  <text x="104" y="560" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7488A3">Jan</text>
  <text x="218" y="560" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7488A3">Mar</text>
  <text x="332" y="560" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7488A3">May</text>
  <text x="446" y="560" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7488A3">Jul</text>
  <text x="560" y="560" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7488A3">Sep</text>
  <text x="674" y="560" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7488A3">Nov</text>

  <rect x="830" y="110" width="410" height="250" rx="28" fill="url(#cardGrad)" stroke="#263852" filter="url(#shadow)"/>
  <text x="862" y="154" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#F5F9FF">Channel Mix</text>
  <text x="862" y="178" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA3BE">Pipeline contribution by acquisition source</text>
  <circle cx="956" cy="256" r="66" fill="none" stroke="#1C2A42" stroke-width="22"/>
  <circle cx="956" cy="256" r="66" fill="none" stroke="#33D6FF" stroke-width="22" stroke-dasharray="210 414" stroke-linecap="round" transform="rotate(-90 956 256)"/>
  <circle cx="956" cy="256" r="66" fill="none" stroke="#7C5CFF" stroke-width="22" stroke-dasharray="128 496" stroke-linecap="round" transform="rotate(92 956 256)"/>
  <circle cx="956" cy="256" r="66" fill="none" stroke="#53FFB7" stroke-width="22" stroke-dasharray="82 542" stroke-linecap="round" transform="rotate(204 956 256)"/>
  <circle cx="956" cy="256" r="38" fill="#0D1423"/>
  <text x="921" y="252" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" text-anchor="middle" fill="#FFFFFF">64%</text>
  <text x="921" y="274" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle" fill="#8EA3BE">digital</text>
  <circle cx="1076" cy="222" r="6" fill="#33D6FF"/>
  <text x="1092" y="227" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9E8FF">Paid search</text>
  <circle cx="1076" cy="254" r="6" fill="#7C5CFF"/>
  <text x="1092" y="259" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9E8FF">Partner</text>
  <circle cx="1076" cy="286" r="6" fill="#53FFB7"/>
  <text x="1092" y="291" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D9E8FF">Organic</text>

  <rect x="830" y="390" width="190" height="130" rx="24" fill="url(#cardGrad)" stroke="#263852" filter="url(#shadow)"/>
  <text x="858" y="424" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA3BE">Net retention</text>
  <text x="858" y="462" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#FFFFFF">118%</text>
  <text x="858" y="487" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#53FFB7">▲ 6.4 pts</text>
  <path d="M858,500 C884,486 902,507 926,493 C950,479 974,482 994,462" fill="none" stroke="#53FFB7" stroke-width="3" stroke-linecap="round"/>

  <rect x="1050" y="390" width="190" height="130" rx="24" fill="url(#cardGrad)" stroke="#263852" filter="url(#shadow)"/>
  <text x="1078" y="424" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA3BE">Active users</text>
  <text x="1078" y="462" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#FFFFFF">2.8M</text>
  <text x="1078" y="487" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#53FFB7">▲ 14.1%</text>
  <path d="M1078,502 C1105,510 1126,488 1148,493 C1173,499 1190,474 1214,468" fill="none" stroke="#33D6FF" stroke-width="3" stroke-linecap="round"/>

  <rect x="830" y="540" width="190" height="130" rx="24" fill="url(#cardGrad)" stroke="#263852" filter="url(#shadow)"/>
  <text x="858" y="574" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA3BE">Gross margin</text>
  <text x="858" y="612" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#FFFFFF">72%</text>
  <text x="858" y="637" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#53FFB7">▲ 3.8 pts</text>
  <rect x="858" y="648" width="116" height="8" rx="4" fill="#1C2A42"/>
  <rect x="858" y="648" width="84" height="8" rx="4" fill="url(#greenGrad)"/>

  <rect x="1050" y="540" width="190" height="130" rx="24" fill="url(#cardGrad)" stroke="#263852" filter="url(#shadow)"/>
  <text x="1078" y="574" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA3BE">Churn risk</text>
  <text x="1078" y="612" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#FFFFFF">3.1%</text>
  <text x="1078" y="637" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FF8A8A">▼ 1.2 pts</text>
  <path d="M1078,652 C1102,635 1124,644 1146,628 C1171,610 1190,622 1214,604" fill="none" stroke="#FF4FD8" stroke-width="3" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the dashboard as a flat table of identical rectangles; the left chart must dominate and establish visual hierarchy.
- ❌ Do not apply filters to `<line>` gridlines; shadows and glows should be on cards, paths, circles, or text only.
- ❌ Do not use `<foreignObject>` for chart labels or HTML metric blocks; use native `<text>` with explicit `width`.
- ❌ Do not use `marker-end` arrows for trend annotations; use simple paths, lines, or small geometric shapes instead.
- ❌ Do not clip non-image chart shapes; if clipping is required, reserve `clipPath` for `<image>` crops only.

## Composition notes
- Keep the left card around 60% of the slide width; it should feel like the “command center” while the right column provides supporting evidence.
- Use a dark background with slightly lighter cards, then reserve saturated cyan, violet, green, and magenta for data emphasis.
- Maintain generous outer margins, but allow dense internal chart details: gridlines, labels, points, legends, and callouts create dashboard credibility.
- The four metric tiles should share size and rhythm, but each needs a different micro-visual so the grid does not feel repetitive.