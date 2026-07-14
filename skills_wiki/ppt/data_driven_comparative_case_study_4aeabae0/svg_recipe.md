# SVG Recipe — Data-Driven Comparative Case Study

## Visual mechanism
A full-bleed contextual photo creates emotional atmosphere, while a crisp elevated data panel carries the analytical comparison. The slide works by separating “case context” on the open image side from “evidence” in a structured chart card.

## SVG primitives needed
- 1× `<image>` for the full-slide background case-study photo
- 1× `<rect>` with gradient fill for the dark atmospheric overlay
- 1× `<filter id="panelShadow">` applied to the main data panel
- 1× `<filter id="softGlow">` applied to subtle highlight elements
- 1× `<rect>` for the white rounded content panel
- 1× `<image>` clipped with `<clipPath>` for a small contextual thumbnail inside the panel
- 1× `<clipPath>` using rounded `<rect>` for the thumbnail crop
- 10× `<rect>` for comparison bars, legend swatches, KPI cards, and panel dividers
- 7× `<line>` for chart axes, grid lines, and KPI separators
- 2× `<path>` for decorative accent shapes behind the title and panel
- Multiple `<text>` elements with explicit `width` for title, subtitle, labels, values, and annotations
- 2× `<linearGradient>` for the background overlay and accent ribbon

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoOverlay" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071826" stop-opacity="0.86"/>
      <stop offset="48%" stop-color="#28556A" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#071826" stop-opacity="0.52"/>
    </linearGradient>

    <linearGradient id="accentRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5B9BD5"/>
      <stop offset="100%" stop-color="#FFC000"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="thumbClip">
      <rect x="802" y="112" width="164" height="98" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <image href="https://images.example.com/full-bleed-coastal-destination-case-study-sunset.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoOverlay)"/>

  <path d="M-40,570 C120,500 230,555 340,485 C450,415 545,390 650,450 C560,560 430,650 250,705 C120,745 20,720 -40,690 Z"
        fill="#5B9BD5" opacity="0.16" filter="url(#softGlow)"/>
  <path d="M980,-20 C1080,30 1140,110 1295,92 L1295,230 C1160,218 1040,190 930,120 C885,92 880,20 980,-20 Z"
        fill="#FFC000" opacity="0.13" filter="url(#softGlow)"/>

  <text x="86" y="118" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600"
        letter-spacing="3" fill="#FFC000">COMPARATIVE CASE STUDY</text>
  <text x="84" y="180" width="570" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700"
        fill="#FFFFFF">Visitor Experience:
    <tspan x="84" dy="56">Before &amp; After</tspan>
  </text>
  <rect x="86" y="276" width="168" height="5" rx="2.5" fill="url(#accentRibbon)"/>
  <text x="86" y="326" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="21"
        fill="#EAF4F7">A data-backed review of site upgrades, service flow, and perception lift across four key visitor moments.</text>

  <rect x="86" y="552" width="188" height="72" rx="18" fill="#FFFFFF" opacity="0.14"/>
  <text x="108" y="584" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#CDE6EF">Sample size</text>
  <text x="108" y="613" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">1,248</text>

  <rect x="294" y="552" width="188" height="72" rx="18" fill="#FFFFFF" opacity="0.14"/>
  <text x="316" y="584" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#CDE6EF">Study window</text>
  <text x="316" y="613" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">90 days</text>

  <rect x="742" y="64" width="466" height="592" rx="30" fill="#FFFFFF" filter="url(#panelShadow)"/>
  <rect x="742" y="64" width="466" height="10" rx="5" fill="url(#accentRibbon)"/>

  <image href="https://images.example.com/rounded-thumbnail-visitor-lookout-platform.jpg"
         x="802" y="112" width="164" height="98" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumbClip)"/>
  <text x="990" y="132" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600"
        fill="#6A737D">CASE LOCATION</text>
  <text x="990" y="165" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700"
        fill="#222831">Great Ocean</text>
  <text x="990" y="194" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#6A737D">Coastal destination audit</text>

  <line x1="802" y1="240" x2="1148" y2="240" stroke="#E7EBEF" stroke-width="2"/>

  <text x="802" y="278" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700"
        fill="#222831">Satisfaction score by journey stage</text>
  <text x="802" y="307" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#6A737D">Average rating, indexed to 100</text>

  <rect x="805" y="326" width="12" height="12" rx="3" fill="#5B9BD5"/>
  <text x="825" y="337" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555D66">Before</text>
  <rect x="900" y="326" width="12" height="12" rx="3" fill="#FFC000"/>
  <text x="920" y="337" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555D66">After</text>

  <line x1="822" y1="508" x2="1138" y2="508" stroke="#202A33" stroke-width="2"/>
  <line x1="822" y1="458" x2="1138" y2="458" stroke="#DDE3E8" stroke-width="1" stroke-dasharray="5 5"/>
  <line x1="822" y1="408" x2="1138" y2="408" stroke="#DDE3E8" stroke-width="1" stroke-dasharray="5 5"/>
  <line x1="822" y1="358" x2="1138" y2="358" stroke="#DDE3E8" stroke-width="1" stroke-dasharray="5 5"/>

  <text x="780" y="513" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A828A">0</text>
  <text x="772" y="463" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A828A">50</text>
  <text x="768" y="363" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A828A">100</text>

  <rect x="850" y="420" width="22" height="88" rx="5" fill="#5B9BD5"/>
  <rect x="877" y="374" width="22" height="134" rx="5" fill="#FFC000"/>
  <rect x="928" y="432" width="22" height="76" rx="5" fill="#5B9BD5"/>
  <rect x="955" y="390" width="22" height="118" rx="5" fill="#FFC000"/>
  <rect x="1006" y="404" width="22" height="104" rx="5" fill="#5B9BD5"/>
  <rect x="1033" y="358" width="22" height="150" rx="5" fill="#FFC000"/>
  <rect x="1084" y="448" width="22" height="60" rx="5" fill="#5B9BD5"/>
  <rect x="1111" y="410" width="22" height="98" rx="5" fill="#FFC000"/>

  <text x="833" y="535" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#555D66">Arrival</text>
  <text x="911" y="535" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#555D66">Wayfinding</text>
  <text x="989" y="535" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#555D66">Amenities</text>
  <text x="1067" y="535" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="middle" fill="#555D66">Checkout</text>

  <rect x="802" y="572" width="346" height="54" rx="16" fill="#F4F7FA"/>
  <line x1="932" y1="582" x2="932" y2="616" stroke="#D7DEE5" stroke-width="1"/>
  <line x1="1044" y1="582" x2="1044" y2="616" stroke="#D7DEE5" stroke-width="1"/>
  <text x="824" y="594" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6A737D">Net lift</text>
  <text x="824" y="618" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#222831">+27%</text>
  <text x="954" y="594" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6A737D">Top driver</text>
  <text x="954" y="618" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#222831">Flow</text>
  <text x="1064" y="594" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6A737D">Confidence</text>
  <text x="1064" y="618" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#222831">High</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place data directly on the photo without a solid or near-solid panel; readability will collapse over busy imagery.
- ❌ Do not use `<mask>` for photo darkening; use a semi-transparent `<rect>` or gradient overlay instead.
- ❌ Do not rely on native PowerPoint charts if editability through SVG is the goal; build the chart from editable `<rect>`, `<line>`, and `<text>` primitives.
- ❌ Do not use `marker-end` on paths for callouts; if arrows are needed, draw them with `<line>` plus separate triangle `<path>`.
- ❌ Do not apply filters to `<line>` gridlines or axes; shadows/glows should stay on panels, paths, rects, or text.

## Composition notes
- Keep the photo/title side spacious: roughly 55–60% of the slide should remain atmospheric, with only headline, subtitle, and 1–2 small proof chips.
- Place the data panel on the opposite 35–40% of the canvas; use generous internal padding so the chart feels editorial, not dashboard-like.
- Use one cool accent and one warm accent for before/after comparison; repeat them in the ribbon, legend, and bars for visual rhythm.
- The panel shadow should be subtle but visible, lifting the evidence layer above the emotional background.