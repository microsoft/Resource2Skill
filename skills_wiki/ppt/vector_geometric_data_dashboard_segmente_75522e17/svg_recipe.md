# SVG Recipe — Vector Geometric Data Dashboard (Segmented Donuts & Filled Pyramids)

## Visual mechanism
A split-tone executive dashboard replaces default charts with editable vector geometry: dashed concentric donut rings for polar progress, annular sector donuts for categorical shares, and triangle “pyramids” filled from the bottom to encode percentages. The premium feel comes from strict alignment, large editorial typography, and a restrained palette of indigo, coral, mint, and violet.

## SVG primitives needed
- 2× `<rect>` for the left indigo title panel and right white data canvas
- 3× `<circle>` with dashed strokes for the segmented concentric donut scale
- 6× `<circle>` with solid/dashed strokes for circular KPI tracks and progress arcs
- 12× `<path>` for annular donut sectors, pyramid outlines, pyramid fills, AI logo frame accents, and small decorative laurels
- 1× `<linearGradient>` for the indigo panel depth
- 1× `<radialGradient>` for subtle right-panel atmospheric glow
- 1× `<filter id="softShadow">` applied to the chart cluster shapes for premium depth
- Multiple `<text>` elements with explicit `width` for title typography, labels, legends, and KPI percentages

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="indigoPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6E5AF0"/>
      <stop offset="55%" stop-color="#7A60E0"/>
      <stop offset="100%" stop-color="#5445C8"/>
    </linearGradient>
    <radialGradient id="rightGlow" cx="50%" cy="40%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="72%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F5F6F8"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.18 0 0 0 0 0.17 0 0 0 0 0.30 0 0 0 0.16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="640" height="720" fill="url(#indigoPanel)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#rightGlow)"/>

  <text x="62" y="145" width="500" font-family="Microsoft YaHei, Segoe UI" font-size="42" font-weight="700" fill="#FFFFFF">一步一步教你用AI做</text>
  <text x="62" y="260" width="500" font-family="Microsoft YaHei, Segoe UI" font-size="86" font-weight="800" fill="#FFFFFF" letter-spacing="2">信息图表</text>
  <line x1="64" y1="333" x2="560" y2="333" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55"/>
  <text x="64" y="422" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="300" fill="#FFFFFF" letter-spacing="3">Adobe Illustrator Tutorial</text>

  <rect x="64" y="503" width="124" height="124" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <text x="93" y="585" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="500" fill="#FFFFFF">Ai</text>
  <path d="M238 607 C214 586 214 545 240 522 M254 618 C224 594 223 541 256 509" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="9 8" opacity="0.9"/>
  <path d="M345 607 C369 586 369 545 343 522 M329 618 C359 594 360 541 327 509" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="9 8" opacity="0.9"/>
  <text x="253" y="548" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">CREATIVE DESIGN</text>
  <text x="253" y="578" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF" text-anchor="middle">LEITU</text>
  <text x="253" y="601" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#FFFFFF" text-anchor="middle">DIGITAL GRAPHICS</text>

  <g filter="url(#softShadow)">
    <circle cx="796" cy="152" r="72" fill="none" stroke="#E9EEF1" stroke-width="14" stroke-dasharray="8 10" transform="rotate(-90 796 152)"/>
    <circle cx="796" cy="152" r="72" fill="none" stroke="#5D55E8" stroke-width="14" stroke-dasharray="8 10" stroke-dashoffset="0" transform="rotate(-90 796 152)"/>
    <circle cx="796" cy="152" r="48" fill="none" stroke="#E9EEF1" stroke-width="8" stroke-dasharray="4 8" transform="rotate(-90 796 152)"/>
    <circle cx="796" cy="152" r="48" fill="none" stroke="#54CC94" stroke-width="8" stroke-dasharray="4 8" stroke-dashoffset="44" transform="rotate(-90 796 152)"/>
    <circle cx="796" cy="152" r="27" fill="none" stroke="#E9EEF1" stroke-width="5" stroke-dasharray="3 6" transform="rotate(-90 796 152)"/>
    <circle cx="796" cy="152" r="27" fill="none" stroke="#E86F73" stroke-width="5" stroke-dasharray="3 6" stroke-dashoffset="54" transform="rotate(-90 796 152)"/>
  </g>

  <circle cx="948" cy="137" r="8" fill="#E86F73"/>
  <text x="966" y="142" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#151515">15%</text>
  <circle cx="948" cy="166" r="8" fill="#54CC94"/>
  <text x="966" y="171" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#151515">31%</text>
  <circle cx="948" cy="195" r="8" fill="#5D55E8"/>
  <text x="966" y="200" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#151515">45%</text>

  <g filter="url(#softShadow)">
    <path d="M1159 90 A76 76 0 0 1 1159 220 L1133 195 A45 45 0 0 0 1133 115 Z" fill="#5D55E8"/>
    <path d="M1048 161 A76 76 0 0 1 1150 88 L1132 116 A45 45 0 0 0 1078 159 Z" fill="#54CC94"/>
    <path d="M1142 226 A76 76 0 0 1 1049 176 L1080 166 A45 45 0 0 0 1130 196 Z" fill="#E9EEF1"/>
  </g>
  <text x="1118" y="112" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#111111">01</text>
  <text x="1161" y="221" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#111111">02</text>
  <text x="1045" y="198" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#111111">03</text>

  <path d="M786 290 L854 448 L718 448 Z" fill="#E5EEF1"/>
  <path d="M741 357 L831 357 L854 448 L718 448 Z" fill="#E86F73"/>
  <text x="765" y="484" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">70%</text>

  <path d="M960 290 L1026 448 L894 448 Z" fill="#E5EEF1"/>
  <path d="M931 379 L989 379 L1026 448 L894 448 Z" fill="#54CC94"/>
  <text x="939" y="484" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">45%</text>

  <path d="M1134 290 L1202 448 L1066 448 Z" fill="#E5EEF1"/>
  <path d="M1080 349 L1188 349 L1202 448 L1066 448 Z" fill="#5D55E8"/>
  <text x="1114" y="484" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">80%</text>

  <circle cx="786" cy="584" r="61" fill="none" stroke="#E5EEF1" stroke-width="14"/>
  <circle cx="786" cy="584" r="61" fill="none" stroke="#E86F73" stroke-width="14" stroke-linecap="round" stroke-dasharray="134 249" transform="rotate(-90 786 584)"/>
  <text x="759" y="592" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="28" fill="#111111">35%</text>

  <circle cx="960" cy="584" r="61" fill="none" stroke="#E5EEF1" stroke-width="14"/>
  <circle cx="960" cy="584" r="61" fill="none" stroke="#54CC94" stroke-width="14" stroke-linecap="round" stroke-dasharray="38 345" transform="rotate(-90 960 584)"/>
  <text x="934" y="592" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="28" fill="#111111">10%</text>

  <circle cx="1134" cy="584" r="61" fill="none" stroke="#E5EEF1" stroke-width="14"/>
  <circle cx="1134" cy="584" r="61" fill="none" stroke="#5D55E8" stroke-width="14" stroke-linecap="round" stroke-dasharray="77 306" transform="rotate(-90 1134 584)"/>
  <text x="1108" y="592" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="28" fill="#111111">20%</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create donut holes; build annular wedges directly as compound-like `<path>` shapes or use stroked circles.
- ❌ Do not rely on embedded chart images for the donuts or pyramids; the point of this technique is editable vector geometry.
- ❌ Do not place `clip-path` on pyramid fills or circles; clipping non-image elements is ignored by the translator.
- ❌ Do not use `marker-end` for arrows or chart ticks; segmented rings should be made with `stroke-dasharray`.
- ❌ Do not omit `width` on any `<text>` element, especially large CJK titles, or PowerPoint text layout will drift.

## Composition notes
- Keep the left 45–50% as a bold title slab; the data graphics should live on a calm white field with generous spacing.
- Use one dominant accent per metric: coral, mint, and violet repeat across legend dots, pyramid fills, and KPI rings.
- Align the three pyramids and three KPI donuts on a strict grid; the precision is what makes the dashboard feel designed rather than generated.
- Let the segmented donut and exploded annular chart occupy the top right as the most complex visual area, with simpler metrics below for reading rhythm.