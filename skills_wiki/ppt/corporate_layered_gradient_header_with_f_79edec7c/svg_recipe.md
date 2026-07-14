# SVG Recipe — Corporate Layered Gradient Header with Floating Hero Element

## Visual mechanism
A high-contrast gradient header occupies the upper half of the slide and casts a soft shadow onto a clean white content zone. A large floating geometric hero icon bridges the header boundary, creating a premium layered “Z-axis” effect while balancing left-aligned corporate typography.

## SVG primitives needed
- 2× `<rect>` for the off-white base canvas and gradient header slab
- 1× `<rect>` with blur filter for the header’s soft lower drop shadow
- 2× `<path>` for translucent diagonal light ribbons across the header
- 2× `<circle>` for subtle decorative header bubbles
- 3× `<text>` blocks for company label, title, and subtitle / bottom section label
- 2× `<filter>` definitions for the header shadow and floating hero shadow
- 1× `<linearGradient>` for the branded teal header
- 1× `<radialGradient>` for the magnifying-glass lens glow
- 2× `<path>` for the magnifying-glass handle and its shadow
- 3× `<circle>` for the floating hero disc, magnifier ring, and inner lens
- 5× `<line>` for internal grid / chart connections inside the lens
- 5× `<circle>` for data points inside the floating hero
- 3× `<rect>` for subtle editable placeholder cards in the lower white workspace

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGradient" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#51C4D3"/>
      <stop offset="55%" stop-color="#32AFC6"/>
      <stop offset="100%" stop-color="#2193B0"/>
    </linearGradient>

    <radialGradient id="lensGlow" cx="42%" cy="32%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="58%" stop-color="#E8F7FA" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#C9E6EF" stop-opacity="0.96"/>
    </radialGradient>

    <filter id="headerShadow" x="-5%" y="-30%" width="110%" height="220%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="heroShadow" x="-30%" y="-30%" width="170%" height="180%">
      <feOffset dx="9" dy="16"/>
      <feGaussianBlur stdDeviation="15"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- clean lower workspace -->
  <rect x="0" y="0" width="1280" height="720" fill="#FAFBFC"/>

  <!-- header shadow sits just below the split line -->
  <rect x="0" y="382" width="1280" height="44" fill="#000000" opacity="0.18" filter="url(#headerShadow)"/>

  <!-- main gradient header: 55% of slide height -->
  <rect x="0" y="0" width="1280" height="396" fill="url(#headerGradient)"/>

  <!-- translucent diagonal light folds -->
  <path d="M430 0 L875 0 L650 396 L220 396 Z" fill="#FFFFFF" opacity="0.08"/>
  <path d="M930 0 L1280 0 L1280 145 L760 396 L610 396 Z" fill="#FFFFFF" opacity="0.045"/>

  <!-- quiet atmospheric geometry in the header -->
  <circle cx="1075" cy="88" r="74" fill="#FFFFFF" opacity="0.06"/>
  <circle cx="1185" cy="235" r="34" fill="#FFFFFF" opacity="0.08"/>

  <!-- editable typography -->
  <text x="90" y="92" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3" fill="#E9FAFD" opacity="0.92">
    STRATEGY OFFICE
  </text>

  <text x="88" y="178" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="700" fill="#FFFFFF">
    <tspan x="88" dy="0">Quarterly Sales</tspan>
    <tspan x="88" dy="66">Review</tspan>
  </text>

  <text x="92" y="333" width="540" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#DDF8FC">
    Executive summary · FY2026 Q2 performance outlook
  </text>

  <!-- floating magnifier shadow and handle -->
  <path d="M1067 493 L1165 591" fill="none" stroke="#000000" stroke-width="54"
        stroke-linecap="round" opacity="0.18" filter="url(#heroShadow)"/>
  <path d="M1061 487 L1158 584" fill="none" stroke="#EAF0F4" stroke-width="44"
        stroke-linecap="round"/>

  <!-- floating hero element: large lens crosses the header boundary -->
  <circle cx="980" cy="396" r="151" fill="#F7FBFD" filter="url(#heroShadow)"/>
  <circle cx="980" cy="396" r="132" fill="none" stroke="#F2F7FA" stroke-width="32"/>
  <circle cx="980" cy="396" r="103" fill="url(#lensGlow)" stroke="#D6E9F0" stroke-width="3"/>

  <!-- internal dashboard lines inside the lens -->
  <line x1="913" y1="433" x2="1047" y2="433" stroke="#B9D6DF" stroke-width="3" opacity="0.65"/>
  <line x1="913" y1="385" x2="1047" y2="385" stroke="#B9D6DF" stroke-width="3" opacity="0.45"/>
  <line x1="925" y1="454" x2="925" y2="342" stroke="#B9D6DF" stroke-width="3" opacity="0.55"/>
  <line x1="935" y1="420" x2="966" y2="378" stroke="#1F9BB7" stroke-width="7" stroke-linecap="round"/>
  <line x1="966" y1="378" x2="1002" y2="405" stroke="#1F9BB7" stroke-width="7" stroke-linecap="round"/>
  <line x1="1002" y1="405" x2="1035" y2="356" stroke="#1F9BB7" stroke-width="7" stroke-linecap="round"/>

  <!-- editable data point nodes -->
  <circle cx="935" cy="420" r="10" fill="#FFFFFF" stroke="#1F9BB7" stroke-width="5"/>
  <circle cx="966" cy="378" r="10" fill="#FFFFFF" stroke="#1F9BB7" stroke-width="5"/>
  <circle cx="1002" cy="405" r="10" fill="#FFFFFF" stroke="#1F9BB7" stroke-width="5"/>
  <circle cx="1035" cy="356" r="10" fill="#FFFFFF" stroke="#1F9BB7" stroke-width="5"/>
  <circle cx="1018" cy="450" r="7" fill="#FFB45E" stroke="#FFFFFF" stroke-width="4"/>

  <!-- lower white workspace: faint editable content anchors -->
  <text x="90" y="500" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#22313A">
    Key discussion areas
  </text>
  <rect x="90" y="535" width="270" height="74" rx="16" fill="#FFFFFF" stroke="#E6EDF1" stroke-width="2"/>
  <rect x="390" y="535" width="270" height="74" rx="16" fill="#FFFFFF" stroke="#E6EDF1" stroke-width="2"/>
  <rect x="690" y="535" width="270" height="74" rx="16" fill="#FFFFFF" stroke="#E6EDF1" stroke-width="2"/>
</svg>
```

## Avoid in this skill
- ❌ Do not flatten the header, shadows, and hero icon into a single bitmap; the premium effect depends on editable layered SVG shapes.
- ❌ Do not place the hero icon fully inside the header or fully inside the white area; it should visibly cross the split line.
- ❌ Do not use `<mask>` or clipping on non-image shapes for the magnifier; build the lens and chart from circles and lines instead.
- ❌ Do not apply filters to `<line>` elements; use filtered `<path>` strokes when a blurred handle shadow is needed.
- ❌ Do not make the lower workspace busy; the header is the visual anchor, and the bottom should remain clean for slide content.

## Composition notes
- Keep the gradient header at roughly 55% slide height; the shadow should sit directly under the split line to imply a physical layer.
- Anchor title typography on the left third and the floating hero around 75–78% of slide width for asymmetric executive-keynote balance.
- Use white and pale-cyan typography in the header, then switch to dark neutral text in the lower workspace for strong readability.
- Let the hero icon overlap both zones by at least 100 px vertically so it feels intentionally “floating,” not merely decorative.