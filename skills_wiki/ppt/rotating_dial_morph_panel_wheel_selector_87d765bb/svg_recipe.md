# SVG Recipe — Rotating Dial Morph Panel (Wheel Selector)

## Visual mechanism
A giant orange selector wheel sits partially off-canvas on the left, with rotated menu labels placed around its ring and a fixed arrow “read head” pointing into the content panel. Duplicate the slide and rotate only the `rotating-dial` group between slides, then apply PowerPoint Morph to create the wheel-selector animation.

## SVG primitives needed
- 1× `<image>` for a full-bleed blurred city/night hero background.
- 2× `<rect>` for dark photo wash and top call-to-action banner.
- 1× `<linearGradient>` for the top banner glow.
- 1× `<circle>` with thick stroke for the large off-screen donut dial.
- 8× `<text>` for menu labels positioned and rotated around the dial ring.
- 1× `<path>` for the long orange pointer bar with arrow head.
- 1× `<path>` for the darker arrow-side shadow/edge accent.
- 1× `<filter id="softShadow">` applied to wheel, pointer, and label text.
- 1× `<filter id="textGlow">` applied to high-contrast title text.
- Multiple `<text>` blocks with explicit `width` for headline, selected item, subheading, and bullet details.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bannerGrad" x1="360" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#9CAF3E" stop-opacity="0.88"/>
      <stop offset="0.55" stop-color="#E3782E" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#B95A28" stop-opacity="0.9"/>
    </linearGradient>

    <linearGradient id="pointerGrad" x1="310" y1="360" x2="1180" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F08A24"/>
      <stop offset="0.55" stop-color="#D96300"/>
      <stop offset="1" stop-color="#B94A00"/>
    </linearGradient>

    <linearGradient id="dialGrad" x1="-130" y1="0" x2="380" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFB26B"/>
      <stop offset="0.45" stop-color="#F58220"/>
      <stop offset="1" stop-color="#D75C00"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="6" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/blurred-night-river-city-skyline-london.jpg"
         preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#1E2732" opacity="0.56"/>
  <rect x="360" y="0" width="920" height="122" fill="url(#bannerGrad)"/>

  <text x="382" y="95" width="820"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92" font-weight="800" letter-spacing="4"
        fill="#FFFFFF" filter="url(#textGlow)">DOWNLOAD NOW</text>

  <!-- Rotate this whole group on duplicate slides: 0, -40, -80 degrees, etc. -->
  <g id="rotating-dial" transform="rotate(-18 0 360)">
    <circle cx="0" cy="360" r="330"
            fill="none" stroke="url(#dialGrad)" stroke-width="76"
            filter="url(#softShadow)"/>

    <text x="-42" y="42" width="220" text-anchor="middle"
          transform="rotate(16 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="34" font-weight="800" fill="#6A2D98"
          filter="url(#softShadow)">PAKISTAN</text>

    <text x="247" y="198" width="170" text-anchor="middle"
          transform="rotate(58 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="31" font-weight="800" fill="#4E9D3A"
          filter="url(#softShadow)">DUBAI</text>

    <text x="322" y="428" width="180" text-anchor="middle"
          transform="rotate(96 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="33" font-weight="800" fill="#FFF45A"
          filter="url(#softShadow)">RUSSIA</text>

    <text x="246" y="610" width="230" text-anchor="middle"
          transform="rotate(132 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="30" font-weight="800" fill="#6FA8B8"
          filter="url(#softShadow)">BANGLADESH</text>

    <text x="-8" y="688" width="150" text-anchor="middle"
          transform="rotate(180 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="32" font-weight="800" fill="#FFFFFF"
          filter="url(#softShadow)">USA</text>

    <text x="-260" y="610" width="240" text-anchor="middle"
          transform="rotate(228 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="30" font-weight="800" fill="#FFE082"
          filter="url(#softShadow)">AFGHANISTAN</text>

    <text x="-330" y="360" width="170" text-anchor="middle"
          transform="rotate(270 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="32" font-weight="800" fill="#263238"
          filter="url(#softShadow)">CHINA</text>

    <text x="-220" y="115" width="160" text-anchor="middle"
          transform="rotate(314 0 360)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="32" font-weight="800" fill="#3F51B5"
          filter="url(#softShadow)">NEPAL</text>
  </g>

  <!-- Static read-head pointer; do not rotate between Morph slides. -->
  <path d="M310 318 L1092 318 L1140 362 L1092 406 L310 406 Z"
        fill="url(#pointerGrad)" opacity="0.96" filter="url(#softShadow)"/>
  <path d="M1092 292 L1200 362 L1092 433 L1138 362 Z"
        fill="#FF9D58" opacity="0.96" filter="url(#softShadow)"/>
  <path d="M1092 433 L1138 362 L1200 362 L1092 433 Z"
        fill="#9D3E00" opacity="0.35"/>

  <text x="516" y="296" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800" letter-spacing="1"
        fill="#62B447" filter="url(#softShadow)">COUNTRY NAME</text>

  <text x="528" y="371" width="480"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="40" font-weight="300" letter-spacing="1"
        fill="#111111">DETAILS FO COUNTRY</text>

  <text x="498" y="488" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#FFFFFF" filter="url(#softShadow)">• YOUR TEXT HERE</text>

  <text x="498" y="558" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#FFFFFF" filter="url(#softShadow)">• DETAIL ABOUT ....</text>

  <text x="498" y="628" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#FFFFFF" filter="url(#softShadow)">• MORE INFO</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<textPath>` for circular type; PowerPoint translation drops it. Place each menu label as its own rotated `<text>` element around the dial.
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; create the motion by duplicating slides, rotating the dial group, and applying PowerPoint Morph.
- ❌ Do not put `marker-end` on a pointer path; build the arrow from editable `<path>` polygons instead.
- ❌ Do not clip or mask the wheel with SVG masks. Keep the dial as an editable stroked `<circle>` placed partly off-canvas.
- ❌ Do not rotate the pointer or content panel between Morph states; only the dial group should change angle.

## Composition notes
- Keep the dial center slightly off the left edge so the wheel feels oversized and mechanical while leaving the right 60% of the slide for readable content.
- The pointer should horizontally intersect the dial at mid-height and extend into the content area as the visual “selection rail.”
- Use a darkened photographic background to create depth, then rely on orange mechanical elements and white/green typography for keynote-level contrast.
- For the Morph sequence, duplicate the slide and change only `transform="rotate(angle 0 360)"` on `#rotating-dial`; update the selected title/content to match the item aligned with the pointer.