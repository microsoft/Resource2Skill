# SVG Recipe — Symmetrical Divergent Comparison Dashboard

## Visual mechanism
A dark executive-dashboard comparison uses a central criteria spine as the visual axis, with pill-shaped bars growing outward to the left and right for two competing products. The viewer compares each metric by horizontal bar length while labels stay locked in the middle for fast row-by-row scanning.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep charcoal background
- 5× translucent `<path>` / `<circle>` decorative background accents for premium depth
- 2× `<rect>` for product header cards on the left and right
- 2× `<circle>` for product initial badges
- 2× `<rect>` for the central dark spine panels
- 10× `<rect>` for dark pill tracks behind each data value
- 10× `<rect>` for colored divergent value bars, anchored to the center and extending outward
- 5× `<rect>` for subtle row separators / central label capsules
- 20+ `<text>` elements with explicit `width` for title, product names, metric labels, and percentages
- 4× `<linearGradient>` for background glow and green/blue value bars
- 1× `<filter id="cardShadow">` for the dashboard card / panel shadow
- 2× `<filter>` glow effects applied to the green and blue value bars

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#14191f"/>
      <stop offset="55%" stop-color="#1e1e24"/>
      <stop offset="100%" stop-color="#102737"/>
    </linearGradient>
    <linearGradient id="greenBar" x1="500" y1="0" x2="150" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4caf50"/>
      <stop offset="100%" stop-color="#9be15d"/>
    </linearGradient>
    <linearGradient id="blueBar" x1="780" y1="0" x2="1130" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0288d1"/>
      <stop offset="100%" stop-color="#27c6ff"/>
    </linearGradient>
    <linearGradient id="spineGrad" x1="500" y1="140" x2="780" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2d3039"/>
      <stop offset="100%" stop-color="#20232b"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="greenGlow" x="-10%" y="-80%" width="120%" height="260%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
    <filter id="blueGlow" x="-10%" y="-80%" width="120%" height="260%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-80 620 L210 330 L330 450 L55 720 Z" fill="#49a942" opacity="0.20"/>
  <path d="M815 -60 L1040 165 L874 330 L650 105 Z" fill="#18b7d8" opacity="0.20"/>
  <path d="M1110 -10 L1370 250 L1210 410 L950 150 Z" fill="#0b84b6" opacity="0.20"/>
  <circle cx="70" cy="250" r="70" fill="#52c41a" opacity="0.13"/>
  <circle cx="1130" cy="125" r="33" fill="#24c7ff" opacity="0.25"/>

  <text x="90" y="68" width="1100" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#8b93a4" letter-spacing="3">BENCHMARK DASHBOARD</text>
  <text x="90" y="118" width="1100" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#f5f7fa">Product Comparison: Alpha vs. Nova</text>
  <text x="90" y="151" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9da5b4">Divergent bars reveal relative strength by metric while the criteria stay fixed on the center spine.</text>

  <rect x="95" y="180" width="1090" height="460" rx="30" fill="#20232b" filter="url(#cardShadow)"/>
  <rect x="118" y="202" width="1044" height="416" rx="24" fill="#242832"/>
  <rect x="130" y="214" width="1020" height="392" rx="20" fill="#1f232c"/>

  <rect x="150" y="235" width="330" height="72" rx="20" fill="#272c36"/>
  <circle cx="442" cy="271" r="25" fill="#8bc34a"/>
  <text x="176" y="262" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#eaf6df" text-anchor="end">Product Alpha</text>
  <text x="176" y="285" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9fa8b4" text-anchor="end">Efficient legacy offer with strong margin economics</text>
  <text x="433" y="280" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff" text-anchor="middle">A</text>

  <rect x="800" y="235" width="330" height="72" rx="20" fill="#272c36"/>
  <circle cx="838" cy="271" r="25" fill="#03a9f4"/>
  <text x="878" y="262" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#e2f7ff">Product Nova</text>
  <text x="878" y="285" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9fa8b4">Aggressive cloud-native challenger with higher reach</text>
  <text x="829" y="280" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff" text-anchor="middle">B</text>

  <rect x="500" y="224" width="130" height="382" rx="18" fill="url(#spineGrad)"/>
  <rect x="650" y="224" width="130" height="382" rx="18" fill="url(#spineGrad)"/>
  <line x1="640" y1="238" x2="640" y2="590" stroke="#3a3f4a" stroke-width="1"/>

  <rect x="520" y="326" width="240" height="42" rx="12" fill="#262a33"/>
  <rect x="520" y="386" width="240" height="42" rx="12" fill="#262a33"/>
  <rect x="520" y="446" width="240" height="42" rx="12" fill="#262a33"/>
  <rect x="520" y="506" width="240" height="42" rx="12" fill="#262a33"/>
  <rect x="520" y="566" width="240" height="42" rx="12" fill="#262a33"/>

  <rect x="150" y="335" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="325" y="335" width="175" height="22" rx="11" fill="url(#greenBar)" filter="url(#greenGlow)"/>
  <text x="337" y="351" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">50%</text>
  <rect x="780" y="335" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="780" y="335" width="333" height="22" rx="11" fill="url(#blueBar)" filter="url(#blueGlow)"/>
  <text x="1072" y="351" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">95%</text>
  <text x="545" y="343" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#e9edf4" text-anchor="middle">Target Market<tspan x="545" dy="15">Penetration</tspan></text>

  <rect x="150" y="395" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="238" y="395" width="262" height="22" rx="11" fill="url(#greenBar)"/>
  <text x="250" y="411" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">75%</text>
  <rect x="780" y="395" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="780" y="395" width="228" height="22" rx="11" fill="url(#blueBar)"/>
  <text x="965" y="411" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">65%</text>
  <text x="545" y="411" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#e9edf4" text-anchor="middle">Market Share</text>

  <rect x="150" y="455" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="150" y="455" width="350" height="22" rx="11" fill="url(#greenBar)"/>
  <text x="164" y="471" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">100%</text>
  <rect x="780" y="455" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="780" y="455" width="175" height="22" rx="11" fill="url(#blueBar)"/>
  <text x="913" y="471" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">50%</text>
  <text x="545" y="456" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#e9edf4" text-anchor="middle">Customer Acquisition<tspan x="545" dy="15">Cost (CAC)</tspan></text>

  <rect x="150" y="515" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="360" y="515" width="140" height="22" rx="11" fill="url(#greenBar)"/>
  <text x="372" y="531" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">40%</text>
  <rect x="780" y="515" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="780" y="515" width="175" height="22" rx="11" fill="url(#blueBar)"/>
  <text x="913" y="531" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">50%</text>
  <text x="545" y="513" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#e9edf4" text-anchor="middle">Average Revenue<tspan x="545" dy="15">Per User</tspan></text>

  <rect x="150" y="575" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="203" y="575" width="297" height="22" rx="11" fill="url(#greenBar)" filter="url(#greenGlow)"/>
  <text x="215" y="591" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">85%</text>
  <rect x="780" y="575" width="350" height="22" rx="11" fill="#171a22"/>
  <rect x="780" y="575" width="350" height="22" rx="11" fill="url(#blueBar)" filter="url(#blueGlow)"/>
  <text x="1088" y="591" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#ffffff">100%</text>
  <text x="545" y="573" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#e9edf4" text-anchor="middle">Customer Lifetime<tspan x="545" dy="15">Value (CLV)</tspan></text>
</svg>
```

## Avoid in this skill
- ❌ Do not build this as a normal left-to-right table; the comparison must grow outward from the central label axis.
- ❌ Do not use `marker-end` arrows to imply direction; the divergent bar anchoring already communicates direction.
- ❌ Do not apply `filter` to `<line>` separators; use subtle filled rectangles or unfiltered lines instead.
- ❌ Do not rely on clipped shapes for bar fills; use rounded `<rect>` pills directly so the bars remain editable.
- ❌ Do not omit `width` on text elements, especially central metric labels, or PowerPoint text wrapping may shift.

## Composition notes
- Keep the central spine about 20–24% of slide width; it should feel like the dashboard’s axis, not a narrow table column.
- Leave generous negative space above the chart for the title and context; the dense comparison area should sit in the lower two-thirds.
- Use one saturated color per product and keep tracks dark, so length differences are visible before the viewer reads the percentages.
- Align left product values to the center edge and grow them leftward; align right product values to the center edge and grow them rightward.