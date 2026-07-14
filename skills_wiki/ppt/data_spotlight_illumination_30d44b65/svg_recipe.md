# SVG Recipe — Data Spotlight Illumination

## Visual mechanism
A dark executive-stage composition uses translucent trapezoid light beams rising from jewel-toned 3D podium pucks, making selected metrics feel “on stage.” Each data point is isolated by its own vertical cone of light, with bold white numbers suspended inside the beam and labels anchored below the base.

## SVG primitives needed
- 1× `<rect>` for the deep navy slide background.
- 4× `<path>` for the main trapezoidal spotlight beams.
- 4× `<path>` for narrow inner beam highlights.
- 4× `<path>` for the curved side walls of the 3D podium pucks.
- 16× `<ellipse>` for podium glows, top surfaces, bottom shadows, and small specular highlights.
- 10× `<text>` for title, subtitle, metric values, supporting deltas, and labels.
- 1× `<linearGradient>` for the white alpha-fading spotlight beam.
- 4× `<radialGradient>` fills for jewel-toned podium top surfaces.
- 1× `<radialGradient>` for the atmospheric background vignette.
- 2× `<filter>` definitions: one soft glow for colored light spill and one shadow for text/base depth.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgVignette" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#26304a"/>
      <stop offset="58%" stop-color="#171d2d"/>
      <stop offset="100%" stop-color="#0c101b"/>
    </radialGradient>

    <linearGradient id="beamFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="78%" stop-color="#ffffff" stop-opacity="0.44"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.68"/>
    </linearGradient>

    <linearGradient id="innerBeamFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="65%" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.35"/>
    </linearGradient>

    <radialGradient id="magentaTop" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#ff7ac8"/>
      <stop offset="55%" stop-color="#c7247a"/>
      <stop offset="100%" stop-color="#7b164b"/>
    </radialGradient>
    <radialGradient id="tealTop" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#6ff7ff"/>
      <stop offset="55%" stop-color="#00a8b2"/>
      <stop offset="100%" stop-color="#00666c"/>
    </radialGradient>
    <radialGradient id="limeTop" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#d7ff7b"/>
      <stop offset="55%" stop-color="#8ec63f"/>
      <stop offset="100%" stop-color="#4d7520"/>
    </radialGradient>
    <radialGradient id="orangeTop" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#ffc06b"/>
      <stop offset="55%" stop-color="#f26522"/>
      <stop offset="100%" stop-color="#9a3512"/>
    </radialGradient>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgVignette)"/>

  <ellipse cx="640" cy="598" rx="560" ry="82" fill="#000000" opacity="0.26"/>
  <ellipse cx="640" cy="585" rx="430" ry="48" fill="#ffffff" opacity="0.035"/>

  <text x="640" y="72" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700"
        fill="#ffffff">Sales Performance — 2024</text>
  <text x="640" y="115" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400"
        fill="#aab4c9">Quarterly achievement spotlight · revenue uplift by quarter</text>

  <!-- Q1 spotlight -->
  <path d="M210 185 L250 185 L335 548 L125 548 Z" fill="url(#beamFade)"/>
  <path d="M225 220 L240 220 L272 545 L193 545 Z" fill="url(#innerBeamFade)"/>
  <ellipse cx="230" cy="555" rx="128" ry="34" fill="#c7247a" opacity="0.45" filter="url(#softGlow)"/>
  <path d="M120 548 C120 574 340 574 340 548 L340 584 C340 613 120 613 120 584 Z"
        fill="#741445" filter="url(#softShadow)"/>
  <ellipse cx="230" cy="548" rx="110" ry="29" fill="url(#magentaTop)"/>
  <ellipse cx="205" cy="539" rx="48" ry="10" fill="#ffffff" opacity="0.22"/>
  <ellipse cx="230" cy="584" rx="108" ry="25" fill="#4d0d2f" opacity="0.35"/>
  <text x="230" y="313" width="185" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="41" font-weight="800"
        fill="#ffffff" filter="url(#softShadow)">$1.20M</text>
  <text x="230" y="346" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#ffb8dc">+12% vs plan</text>
  <text x="230" y="653" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700"
        fill="#ffffff">Q1 Launch</text>

  <!-- Q2 spotlight -->
  <path d="M480 185 L520 185 L605 548 L395 548 Z" fill="url(#beamFade)"/>
  <path d="M495 220 L510 220 L542 545 L463 545 Z" fill="url(#innerBeamFade)"/>
  <ellipse cx="500" cy="555" rx="128" ry="34" fill="#00a8b2" opacity="0.45" filter="url(#softGlow)"/>
  <path d="M390 548 C390 574 610 574 610 548 L610 584 C610 613 390 613 390 584 Z"
        fill="#00666c" filter="url(#softShadow)"/>
  <ellipse cx="500" cy="548" rx="110" ry="29" fill="url(#tealTop)"/>
  <ellipse cx="475" cy="539" rx="48" ry="10" fill="#ffffff" opacity="0.22"/>
  <ellipse cx="500" cy="584" rx="108" ry="25" fill="#00484c" opacity="0.35"/>
  <text x="500" y="313" width="185" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="41" font-weight="800"
        fill="#ffffff" filter="url(#softShadow)">$1.55M</text>
  <text x="500" y="346" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#a8fbff">+18% vs plan</text>
  <text x="500" y="653" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700"
        fill="#ffffff">Q2 Expansion</text>

  <!-- Q3 spotlight -->
  <path d="M760 185 L800 185 L885 548 L675 548 Z" fill="url(#beamFade)"/>
  <path d="M775 220 L790 220 L822 545 L743 545 Z" fill="url(#innerBeamFade)"/>
  <ellipse cx="780" cy="555" rx="128" ry="34" fill="#8ec63f" opacity="0.43" filter="url(#softGlow)"/>
  <path d="M670 548 C670 574 890 574 890 548 L890 584 C890 613 670 613 670 584 Z"
        fill="#4d7520" filter="url(#softShadow)"/>
  <ellipse cx="780" cy="548" rx="110" ry="29" fill="url(#limeTop)"/>
  <ellipse cx="755" cy="539" rx="48" ry="10" fill="#ffffff" opacity="0.24"/>
  <ellipse cx="780" cy="584" rx="108" ry="25" fill="#304e12" opacity="0.36"/>
  <text x="780" y="313" width="185" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="41" font-weight="800"
        fill="#ffffff" filter="url(#softShadow)">$1.80M</text>
  <text x="780" y="346" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#dcff9d">+23% vs plan</text>
  <text x="780" y="653" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700"
        fill="#ffffff">Q3 Scale</text>

  <!-- Q4 spotlight -->
  <path d="M1030 185 L1070 185 L1155 548 L945 548 Z" fill="url(#beamFade)"/>
  <path d="M1045 220 L1060 220 L1092 545 L1013 545 Z" fill="url(#innerBeamFade)"/>
  <ellipse cx="1050" cy="555" rx="128" ry="34" fill="#f26522" opacity="0.45" filter="url(#softGlow)"/>
  <path d="M940 548 C940 574 1160 574 1160 548 L1160 584 C1160 613 940 613 940 584 Z"
        fill="#9a3512" filter="url(#softShadow)"/>
  <ellipse cx="1050" cy="548" rx="110" ry="29" fill="url(#orangeTop)"/>
  <ellipse cx="1025" cy="539" rx="48" ry="10" fill="#ffffff" opacity="0.22"/>
  <ellipse cx="1050" cy="584" rx="108" ry="25" fill="#6d2109" opacity="0.35"/>
  <text x="1050" y="313" width="185" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="41" font-weight="800"
        fill="#ffffff" filter="url(#softShadow)">$2.40M</text>
  <text x="1050" y="346" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#ffd0a8">+31% vs plan</text>
  <text x="1050" y="653" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700"
        fill="#ffffff">Q4 Peak</text>
</svg>
```

## Avoid in this skill
- ❌ Using PNG-generated beams when editable SVG gradients and paths can create the same spotlight effect natively.
- ❌ Applying `filter` to `<line>` elements for glow rays; use filled `<path>` beams or blurred ellipses instead.
- ❌ Using `<mask>` for the fading cone; use a trapezoid `<path>` filled with a transparent-to-opaque linear gradient.
- ❌ Clipping non-image shapes to create the beam; clip paths should only be used on `<image>` elements in this workflow.
- ❌ Overcrowding the beam with small text; the spotlight metaphor works best with one large value and one short supporting line.

## Composition notes
- Keep the top 20–25% of the slide mostly clear for the title and to let the beams feel tall and atmospheric.
- Align each metric on a strict column center; the beam, value, podium, and label should share the same vertical axis.
- Use a dark navy or charcoal background so the semi-transparent white beams remain visible and premium.
- Let the podium colors carry the data categorization; keep numbers white for maximum contrast and executive readability.