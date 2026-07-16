# SVG Recipe — 3D Ribbon Wrap Infographic Timeline

## Visual mechanism
A vertical neutral pillar anchors the timeline while saturated ribbons appear to wrap around it through 2.5D layering: dark rear fold pieces sit behind the pillar, the pillar overlays them, and bright front ribbon faces sit on top. Drop shadows, subtle gradients, and staggered ribbon lengths create the premium “folded object in space” illusion.

## SVG primitives needed
- 1× `<rect>` full-slide background filled with a radial gradient for a soft studio backdrop
- 4× dark `<path>` rear fold shapes placed behind the pillar to simulate ribbon wrapping
- 1× tall rounded `<rect>` for the central pillar, with a light vertical gradient
- 2× `<ellipse>` highlights/shadows for the pillar cap and base
- 4× main front ribbon `<path>` shapes with semicircular left ends and flat right ends
- 4× narrow translucent `<rect>` crease overlays where the ribbon crosses the pillar face
- 8× `<circle>` endpoint/node accents on the front ribbons
- 9× `<text>` blocks with explicit `width` attributes for title, subtitle, years, and descriptions
- 1× `<radialGradient>` for the background
- 5× `<linearGradient>` fills for pillar and ribbon faces
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` applied to pillar and ribbon paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="48%" cy="43%" r="78%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="62%" stop-color="#eef2f6"/>
      <stop offset="100%" stop-color="#dce2ea"/>
    </radialGradient>

    <linearGradient id="pillarGrad" x1="940" y1="0" x2="1040" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="42%" stop-color="#f1f3f6"/>
      <stop offset="100%" stop-color="#cfd5dd"/>
    </linearGradient>

    <linearGradient id="magentaGrad" x1="250" y1="0" x2="990" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#e82680"/>
      <stop offset="100%" stop-color="#c80f63"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="200" y1="0" x2="980" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ff9f35"/>
      <stop offset="100%" stop-color="#e87414"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="245" y1="0" x2="988" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#12c5ad"/>
      <stop offset="100%" stop-color="#008e7c"/>
    </linearGradient>
    <linearGradient id="purpleGrad" x1="185" y1="0" x2="982" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#a667c8"/>
      <stop offset="100%" stop-color="#7340a5"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset in="SourceAlpha" dx="0" dy="9" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <ellipse cx="990" cy="654" rx="132" ry="24" fill="#9aa5b1" opacity="0.18"/>

  <text x="72" y="66" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#3f4650">
    3D RIBBON WRAP TIMELINE
  </text>
  <text x="74" y="98" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7b8490">
    Corporate milestones visualized as folded color bands around a central structural spine
  </text>

  <!-- rear folded ribbon flaps: draw first so the pillar hides their inner edge -->
  <path d="M960 152 L1118 179 L1118 233 L960 216 Z" fill="#8f0b44" filter="url(#softShadow)"/>
  <path d="M950 276 L1092 301 L1092 355 L950 340 Z" fill="#aa5510" filter="url(#softShadow)"/>
  <path d="M960 401 L1128 428 L1128 482 L960 466 Z" fill="#006d61" filter="url(#softShadow)"/>
  <path d="M948 526 L1082 551 L1082 605 L948 590 Z" fill="#56307d" filter="url(#softShadow)"/>

  <!-- neutral pillar in front of rear folds -->
  <rect x="940" y="118" width="96" height="508" rx="12" fill="url(#pillarGrad)" filter="url(#softShadow)"/>
  <rect x="1026" y="130" width="5" height="482" rx="3" fill="#b9c0c9" opacity="0.45"/>
  <rect x="948" y="130" width="5" height="482" rx="3" fill="#ffffff" opacity="0.75"/>
  <ellipse cx="988" cy="121" rx="46" ry="11" fill="#ffffff" opacity="0.82"/>
  <ellipse cx="988" cy="626" rx="46" ry="11" fill="#bdc5cf" opacity="0.35"/>

  <!-- front ribbon faces -->
  <path d="M290 145 H990 V215 H290 A35 35 0 0 1 290 145 Z" fill="url(#magentaGrad)" filter="url(#softShadow)"/>
  <rect x="940" y="145" width="15" height="70" fill="#730832" opacity="0.24"/>
  <circle cx="928" cy="180" r="18" fill="#ffffff" opacity="0.95"/>
  <circle cx="928" cy="180" r="8" fill="#d9166f"/>

  <path d="M240 270 H978 V340 H240 A35 35 0 0 1 240 270 Z" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <rect x="940" y="270" width="15" height="70" fill="#8d4209" opacity="0.22"/>
  <circle cx="918" cy="305" r="18" fill="#ffffff" opacity="0.95"/>
  <circle cx="918" cy="305" r="8" fill="#f28e2b"/>

  <path d="M280 395 H992 V465 H280 A35 35 0 0 1 280 395 Z" fill="url(#tealGrad)" filter="url(#softShadow)"/>
  <rect x="940" y="395" width="15" height="70" fill="#004f47" opacity="0.22"/>
  <circle cx="930" cy="430" r="18" fill="#ffffff" opacity="0.95"/>
  <circle cx="930" cy="430" r="8" fill="#00a88f"/>

  <path d="M220 520 H982 V590 H220 A35 35 0 0 1 220 520 Z" fill="url(#purpleGrad)" filter="url(#softShadow)"/>
  <rect x="940" y="520" width="15" height="70" fill="#3d225e" opacity="0.22"/>
  <circle cx="920" cy="555" r="18" fill="#ffffff" opacity="0.95"/>
  <circle cx="920" cy="555" r="8" fill="#894cae"/>

  <!-- ribbon labels -->
  <text x="320" y="175" width="520" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan font-size="31" font-weight="800">2015</tspan>
    <tspan dx="22" font-size="18" font-weight="700" letter-spacing="1">FOUNDATION</tspan>
  </text>
  <text x="321" y="201" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff" opacity="0.86">
    Global launch, first enterprise clients, and initial market validation
  </text>

  <text x="270" y="300" width="520" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan font-size="31" font-weight="800">2018</tspan>
    <tspan dx="22" font-size="18" font-weight="700" letter-spacing="1">SCALE-UP</tspan>
  </text>
  <text x="271" y="326" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff" opacity="0.86">
    Platform expansion, regional teams, and repeatable operating model
  </text>

  <text x="310" y="425" width="520" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan font-size="31" font-weight="800">2020</tspan>
    <tspan dx="22" font-size="18" font-weight="700" letter-spacing="1">DIGITAL SHIFT</tspan>
  </text>
  <text x="311" y="451" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff" opacity="0.86">
    Cloud migration, analytics capability, and automated workflows
  </text>

  <text x="250" y="550" width="520" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan font-size="31" font-weight="800">2024</tspan>
    <tspan dx="22" font-size="18" font-weight="700" letter-spacing="1">NEXT HORIZON</tspan>
  </text>
  <text x="251" y="576" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff" opacity="0.86">
    AI-assisted products, partner ecosystem, and category leadership
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` transforms to fake the folded ribbon angle; use editable polygon/path geometry instead.
- ❌ Do not use masks or clipping on non-image ribbon shapes; the wrap illusion should come from explicit layer ordering.
- ❌ Do not place one shadow filter on a parent `<g>`; apply filters directly to individual `<path>` or `<rect>` elements.
- ❌ Do not use `marker-end` arrows for timeline direction; arrowheads may disappear. Use ribbon geometry and sequencing instead.
- ❌ Do not omit `width` on timeline text blocks; PowerPoint text layout depends on explicit widths.

## Composition notes
- Keep the pillar right-weighted around 73–82% of slide width, leaving the left two-thirds for long ribbon labels.
- Stagger ribbon start positions and lengths so the design feels rhythmic instead of like a rigid table.
- Use dark rear flaps only on the far side of the pillar; the pillar must sit above them and below the bright front ribbons.
- Pair saturated ribbon colors with a cool neutral background and light grey pillar so the chronological sequence remains the visual focus.