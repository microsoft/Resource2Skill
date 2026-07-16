# SVG Recipe — Semi-Circular Gauge Array

## Visual mechanism
A clean executive dashboard composed of 3–5 equal-width modules, each anchored by a thick semi-circular gauge arc with a pale gray track and a vivid percentage sweep. The same accent color is reused for the gauge, numeric value, and category title so each metric reads as a self-contained visual unit.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 4× `<rect>` for soft white metric cards behind each gauge module
- 8× `<path>` for the semi-circular gauges: 4 pale gray background tracks and 4 colored foreground percentage arcs
- 14× `<text>` elements for master title, subtitle, percentage values, category labels, and explanatory body copy
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to the card rectangles
- Optional decorative `<line>` elements for very subtle column rhythm or baseline alignment, if desired

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Master title -->
  <text x="640" y="76" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="39" font-weight="700"
        fill="#969696">
    P E R C E N T A G E S
  </text>
  <text x="640" y="124" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="400"
        fill="#7A7A7A">
    Four independent capability metrics shown with equal visual weight for rapid executive comparison
  </text>

  <!-- Soft metric cards -->
  <rect x="57" y="205" width="266" height="420" rx="28" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.92"/>
  <rect x="359" y="205" width="266" height="420" rx="28" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.92"/>
  <rect x="661" y="205" width="266" height="420" rx="28" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.92"/>
  <rect x="963" y="205" width="266" height="420" rx="28" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.92"/>

  <!-- Gauge 1: 60% -->
  <path d="M 86 355 A 104 104 0 0 1 294 355"
        fill="none" stroke="#EBEBEB" stroke-width="30" stroke-linecap="butt"/>
  <path d="M 86 355 A 104 104 0 0 1 222.1 256.1"
        fill="none" stroke="#E83A72" stroke-width="30" stroke-linecap="butt"/>
  <text x="190" y="442" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#E83A72">60%</text>
  <text x="190" y="500" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        fill="#E83A72">GRAPHIC DESIGN</text>
  <text x="190" y="537" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="400"
        fill="#8E8E8E">
    <tspan x="190" dy="0">Brand systems, campaign</tspan>
    <tspan x="190" dy="23">visuals, and executive</tspan>
    <tspan x="190" dy="23">presentation polish.</tspan>
  </text>

  <!-- Gauge 2: 70% -->
  <path d="M 388 355 A 104 104 0 0 1 596 355"
        fill="none" stroke="#EBEBEB" stroke-width="30" stroke-linecap="butt"/>
  <path d="M 388 355 A 104 104 0 0 1 553.1 270.9"
        fill="none" stroke="#00998F" stroke-width="30" stroke-linecap="butt"/>
  <text x="492" y="442" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#00998F">70%</text>
  <text x="492" y="500" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        fill="#00998F">WEB DESIGN</text>
  <text x="492" y="537" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="400"
        fill="#8E8E8E">
    <tspan x="492" dy="0">Responsive product pages,</tspan>
    <tspan x="492" dy="23">conversion modules, and</tspan>
    <tspan x="492" dy="23">clean UI foundations.</tspan>
  </text>

  <!-- Gauge 3: 50% -->
  <path d="M 690 355 A 104 104 0 0 1 898 355"
        fill="none" stroke="#EBEBEB" stroke-width="30" stroke-linecap="butt"/>
  <path d="M 690 355 A 104 104 0 0 1 794 251"
        fill="none" stroke="#8BC34A" stroke-width="30" stroke-linecap="butt"/>
  <text x="794" y="442" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#8BC34A">50%</text>
  <text x="794" y="500" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        fill="#8BC34A">VIDEO EDITING</text>
  <text x="794" y="537" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="400"
        fill="#8E8E8E">
    <tspan x="794" dy="0">Short-form product clips,</tspan>
    <tspan x="794" dy="23">social edits, motion cuts,</tspan>
    <tspan x="794" dy="23">and launch explainers.</tspan>
  </text>

  <!-- Gauge 4: 90% -->
  <path d="M 992 355 A 104 104 0 0 1 1200 355"
        fill="none" stroke="#EBEBEB" stroke-width="30" stroke-linecap="butt"/>
  <path d="M 992 355 A 104 104 0 0 1 1194.9 322.9"
        fill="none" stroke="#1A73E8" stroke-width="30" stroke-linecap="butt"/>
  <text x="1096" y="442" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#1A73E8">90%</text>
  <text x="1096" y="500" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        fill="#1A73E8">UX DESIGN</text>
  <text x="1096" y="537" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="400"
        fill="#8E8E8E">
    <tspan x="1096" dy="0">Journey maps, user flows,</tspan>
    <tspan x="1096" dy="23">interaction models, and</tspan>
    <tspan x="1096" dy="23">high-fidelity prototypes.</tspan>
  </text>

  <!-- Footer note -->
  <text x="640" y="676" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="400"
        fill="#B0B0B0">
    Use identical gauge radius, stroke weight, and text hierarchy so the eye compares values rather than layout differences.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use raster PNG gauge images; draw gauges as native `<path>` arcs so they remain editable in PowerPoint.
- ❌ Do not use `<mask>` or `clip-path` on gauge shapes to fake the semi-circle; PowerPoint translation will not preserve those reliably for non-image elements.
- ❌ Do not create arc indicators with thick `<line>` segments; curved percentage sweeps need true `<path>` arc commands.
- ❌ Do not mix unrelated colors between the arc, percentage number, and label; the technique depends on strict color linkage.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint text boxes need explicit widths for clean rendering.

## Composition notes
- Keep the layout modular: 4 equal columns across the slide, with each gauge centered in its card or column.
- Place gauges in the upper-middle band, percentage values directly below the arc, and explanatory copy beneath the category title.
- Use a white or near-white background with pale gray tracks; the accent colors should carry almost all visual energy.
- Leave generous top and side whitespace so the array feels like a premium summary slide, not a crowded dashboard.