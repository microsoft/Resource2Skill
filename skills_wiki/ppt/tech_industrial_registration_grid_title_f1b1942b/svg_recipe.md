# SVG Recipe — Tech-Industrial Registration Grid Title

## Visual mechanism
A massive uppercase title is locked to the center of a dark industrial canvas, surrounded by thin red crop marks, registration crosses, and micro grid labels. The effect comes from extreme scale contrast: heavy white typography versus hairline geometry, with one asymmetric yellow tag adding a “calibration target” accent.

## SVG primitives needed
- 1× `<rect>` for the full dark background
- 1× `<radialGradient>` for a subtle center glow behind the title
- 1× `<linearGradient>` for a faint diagonal industrial sheen
- 1× `<filter id="softGlow">` applied to red registration geometry
- 1× `<filter id="textShadow">` applied to the main title
- 20–30× thin `<rect>` for crop marks, partial grid rails, scan lines, and corner brackets
- 8–12× small `<rect>` pairs for plus/cross registration marks
- 1× `<rect>` for the yellow accent tag
- 1× `<path>` for a small red angular targeting chevron
- 8–12× `<text>` elements for main title, accent tag, and tiny technical labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="centerGlow" cx="50%" cy="50%" r="58%">
      <stop offset="0%" stop-color="#2f3440"/>
      <stop offset="45%" stop-color="#1c1f26"/>
      <stop offset="100%" stop-color="#111318"/>
    </radialGradient>

    <linearGradient id="steelSheen" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.06"/>
      <stop offset="40%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="72%" stop-color="#e03131" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#steelSheen)"/>

  <!-- faint industrial baseline grid: keep very subtle -->
  <rect x="160" y="140" width="960" height="1" fill="#ffffff" opacity="0.055"/>
  <rect x="160" y="580" width="960" height="1" fill="#ffffff" opacity="0.055"/>
  <rect x="220" y="96" width="1" height="528" fill="#ffffff" opacity="0.045"/>
  <rect x="1060" y="96" width="1" height="528" fill="#ffffff" opacity="0.045"/>
  <rect x="100" y="360" width="1080" height="1" fill="#ffffff" opacity="0.035"/>
  <rect x="640" y="74" width="1" height="572" fill="#ffffff" opacity="0.035"/>

  <!-- primary red crop marks -->
  <g fill="#e03131" filter="url(#softGlow)">
    <rect x="152" y="112" width="168" height="3"/>
    <rect x="152" y="112" width="3" height="168"/>
    <rect x="960" y="112" width="168" height="3"/>
    <rect x="1125" y="112" width="3" height="168"/>

    <rect x="152" y="605" width="168" height="3"/>
    <rect x="152" y="440" width="3" height="168"/>
    <rect x="960" y="605" width="168" height="3"/>
    <rect x="1125" y="440" width="3" height="168"/>

    <rect x="412" y="280" width="96" height="2"/>
    <rect x="772" y="280" width="96" height="2"/>
    <rect x="412" y="440" width="96" height="2"/>
    <rect x="772" y="440" width="96" height="2"/>
  </g>

  <!-- secondary short alignment ticks -->
  <g fill="#e03131" opacity="0.82">
    <rect x="268" y="168" width="46" height="2"/>
    <rect x="966" y="168" width="46" height="2"/>
    <rect x="268" y="550" width="46" height="2"/>
    <rect x="966" y="550" width="46" height="2"/>

    <rect x="384" y="216" width="2" height="38"/>
    <rect x="894" y="216" width="2" height="38"/>
    <rect x="384" y="466" width="2" height="38"/>
    <rect x="894" y="466" width="2" height="38"/>
  </g>

  <!-- registration crosses made from editable rects -->
  <g fill="#e03131">
    <rect x="1090" y="172" width="36" height="2"/>
    <rect x="1107" y="155" width="2" height="36"/>
    <rect x="154" y="548" width="36" height="2"/>
    <rect x="171" y="531" width="2" height="36"/>

    <rect x="628" y="128" width="24" height="2" opacity="0.7"/>
    <rect x="639" y="117" width="2" height="24" opacity="0.7"/>
    <rect x="628" y="590" width="24" height="2" opacity="0.7"/>
    <rect x="639" y="579" width="2" height="24" opacity="0.7"/>

    <rect x="308" y="356" width="30" height="2" opacity="0.5"/>
    <rect x="322" y="342" width="2" height="30" opacity="0.5"/>
    <rect x="942" y="356" width="30" height="2" opacity="0.5"/>
    <rect x="956" y="342" width="2" height="30" opacity="0.5"/>
  </g>

  <!-- angular targeting chevron -->
  <path d="M 720 250 L 748 250 L 762 264 L 748 278 L 720 278 L 734 264 Z"
        fill="#e03131" opacity="0.9" filter="url(#softGlow)"/>

  <!-- central title lockup -->
  <rect x="604" y="226" width="72" height="58" fill="#ffd43b"/>
  <text x="640" y="266" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="800" fill="#17191f">U,</text>

  <text x="640" y="400" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="900" letter-spacing="4"
        fill="#ffffff" filter="url(#textShadow)">UNSTOPPABLE</text>

  <rect x="370" y="421" width="540" height="2" fill="#ffffff" opacity="0.18"/>
  <rect x="508" y="432" width="264" height="2" fill="#e03131" opacity="0.75"/>

  <!-- micro technical labels -->
  <text x="152" y="94" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="2" fill="#e03131">REG / 04-A TARGET</text>
  <text x="928" y="94" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="2" fill="#e03131">FRAME LOCK 1280</text>
  <text x="152" y="638" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="1.5" fill="#ffffff" opacity="0.42">ALIGNMENT GRID ACTIVE</text>
  <text x="916" y="638" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" letter-spacing="1.5" fill="#ffffff" opacity="0.42">PRECISION MODE / ON</text>

  <text x="640" y="470" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="3"
        fill="#ffd43b">ENGINEERED MOMENTUM SYSTEM</text>

  <!-- tiny numeric calibration text -->
  <text x="236" y="132" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9" letter-spacing="1" fill="#ffffff" opacity="0.28">X:0152 Y:0112</text>
  <text x="1014" y="594" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9" letter-spacing="1" fill="#ffffff" opacity="0.28">X:1128 Y:0608</text>
</svg>
```

## Avoid in this skill
- ❌ Do not draw a complete red box around the title; the premium look depends on broken crop marks and implied structure.
- ❌ Do not make the background pure black without tonal variation; add a subtle radial or linear gradient so the center feels cinematic.
- ❌ Do not use `<line>` with filters for glowing rails; filters on `<line>` are dropped, so use thin `<rect>` elements for illuminated geometry.
- ❌ Do not use `<textPath>`, animated scan lines, or mask-based glitch effects; they will not translate reliably to editable PowerPoint shapes.
- ❌ Do not overcrowd the slide with a dense dashboard grid; the title must remain the dominant object.

## Composition notes
- Keep the main word centered horizontally and vertically, occupying roughly 70–80% of slide width.
- Place red crop marks near the outer thirds of the canvas, not hugging the text too tightly; they should feel like a targeting system.
- Use the yellow tag as the only warm filled block, slightly above the title, to break symmetry and create a focal “registration stamp.”
- Leave generous negative space around the title; micro labels should be small enough to read as texture before they read as content.