# SVG Recipe — Perspective Grid Cover

## Visual mechanism
A split-horizon cover slide uses a dark upper “sky” and a neon lower “floor” made from perspective grid lines converging to a vanishing point. Large editorial typography sits in the quiet upper-left space while glowing horizon geometry creates a technical, retro-futuristic focal point.

## SVG primitives needed
- 2× `<rect>` for the split background: upper sky and lower floor plane.
- 1× `<rect>` for a translucent title backing panel.
- 1× `<circle>` for a glowing horizon sun / vanishing-point anchor.
- 1× `<ellipse>` for atmospheric glow around the horizon.
- 4× `<path>` for diagonal geometric shards, horizon plates, and angular accent shapes.
- 21× `<line>` for the perspective grid rays, horizontal grid bands, and horizon accent strokes.
- 4× `<text>` blocks for eyebrow label, main headline, subtitle, and small footer metadata.
- 5× `<linearGradient>` / `<radialGradient>` for premium background, floor, title, sun, and glow coloring.
- 2× `<filter>` definitions: one soft glow for large shapes, one shadow for headline text.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0A102A"/>
      <stop offset="55%" stop-color="#13194A"/>
      <stop offset="100%" stop-color="#2A1358"/>
    </linearGradient>

    <linearGradient id="floorGrad" x1="0" y1="350" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#210B3D"/>
      <stop offset="52%" stop-color="#120826"/>
      <stop offset="100%" stop-color="#070712"/>
    </linearGradient>

    <linearGradient id="titleGrad" x1="90" y1="115" x2="720" y2="290" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#DFF7FF"/>
      <stop offset="100%" stop-color="#77F7FF"/>
    </linearGradient>

    <linearGradient id="horizonPlate" x1="0" y1="330" x2="1280" y2="390" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF2EB8" stop-opacity="0.05"/>
      <stop offset="48%" stop-color="#34F6FF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#FFB000" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="sunGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFF7B0"/>
      <stop offset="42%" stop-color="#FF4FD8"/>
      <stop offset="100%" stop-color="#6A2CFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="vpGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4DFFFF" stop-opacity="0.55"/>
      <stop offset="58%" stop-color="#743BFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="textShadow" x="-12%" y="-12%" width="124%" height="124%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="365" fill="url(#skyGrad)"/>
  <rect x="0" y="350" width="1280" height="370" fill="url(#floorGrad)"/>

  <path d="M0,0 L500,0 L350,86 L0,140 Z" fill="#2DEBFF" opacity="0.08"/>
  <path d="M1280,0 L1280,170 L1030,120 L1125,0 Z" fill="#FF2EB8" opacity="0.11"/>
  <path d="M0,332 C220,348 390,338 570,351 C760,366 955,338 1280,354 L1280,394 C960,376 735,390 548,374 C345,358 180,374 0,356 Z" fill="url(#horizonPlate)"/>
  <path d="M890,317 L1165,342 L1280,386 L1010,372 Z" fill="#7A3CFF" opacity="0.22"/>

  <ellipse cx="760" cy="360" rx="390" ry="95" fill="url(#vpGlow)" filter="url(#softGlow)" opacity="0.9"/>
  <circle cx="760" cy="358" r="125" fill="url(#sunGrad)" opacity="0.62" filter="url(#softGlow)"/>

  <line x1="0" y1="358" x2="1280" y2="358" stroke="#57F7FF" stroke-width="2.5" opacity="0.9"/>
  <line x1="0" y1="365" x2="1280" y2="365" stroke="#FF3BCD" stroke-width="1.5" opacity="0.45"/>

  <g stroke="#37F6FF" stroke-width="1.7" opacity="0.72">
    <line x1="760" y1="360" x2="-240" y2="720"/>
    <line x1="760" y1="360" x2="-60" y2="720"/>
    <line x1="760" y1="360" x2="120" y2="720"/>
    <line x1="760" y1="360" x2="300" y2="720"/>
    <line x1="760" y1="360" x2="480" y2="720"/>
    <line x1="760" y1="360" x2="660" y2="720"/>
    <line x1="760" y1="360" x2="840" y2="720"/>
    <line x1="760" y1="360" x2="1020" y2="720"/>
    <line x1="760" y1="360" x2="1200" y2="720"/>
    <line x1="760" y1="360" x2="1380" y2="720"/>
    <line x1="760" y1="360" x2="1560" y2="720"/>
  </g>

  <g stroke="#FF33C7" stroke-width="1.8" opacity="0.78">
    <line x1="0" y1="395" x2="1280" y2="395"/>
    <line x1="0" y1="425" x2="1280" y2="425"/>
    <line x1="0" y1="462" x2="1280" y2="462"/>
    <line x1="0" y1="508" x2="1280" y2="508"/>
    <line x1="0" y1="562" x2="1280" y2="562"/>
    <line x1="0" y1="626" x2="1280" y2="626"/>
    <line x1="0" y1="700" x2="1280" y2="700"/>
  </g>

  <rect x="72" y="72" width="690" height="250" rx="28" fill="#050817" opacity="0.46"/>
  <path d="M72,322 L762,322 L714,350 L104,350 Z" fill="#00F0FF" opacity="0.11"/>

  <text x="96" y="116" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" letter-spacing="4" fill="#7EF9FF" opacity="0.92">
    STRATEGIC SYSTEMS BRIEF
  </text>

  <text x="92" y="196" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" letter-spacing="-2" fill="url(#titleGrad)" filter="url(#textShadow)">
    <tspan x="92" dy="0">PERSPECTIVE</tspan>
    <tspan x="92" dy="78">GRID COVER</tspan>
  </text>

  <text x="98" y="306" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="400" fill="#D7E6FF" opacity="0.86">
    A bold section divider shell for technical launches, future roadmaps, and keynote openings.
  </text>

  <text x="920" y="650" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" letter-spacing="2.5" fill="#FFE27A" opacity="0.76">
    VANISHING POINT  /  07
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` fills for the grid; draw each perspective line explicitly so it remains editable in PowerPoint.
- ❌ Do not apply filters to `<line>` elements for neon glow; line filters are dropped, so use nearby glowing ellipses/circles instead.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the perspective planes; draw trapezoids and shards directly as `<path>` coordinates.
- ❌ Do not rely on masks or clip paths to create the horizon split; layer rectangles and paths to keep the shell robust.
- ❌ Do not place the title over the densest grid area; it will reduce legibility and weaken the vanishing-point effect.

## Composition notes
- Keep the headline in the upper-left 55–60% of the canvas, where the background is calmer and darker.
- Place the vanishing point slightly right of center on the horizon line to create motion and avoid a static symmetrical layout.
- Use cyan for vertical/radial grid rays and magenta for horizontal floor bands; this two-color rhythm sells the retro-technical look.
- The lower third should feel visually active, while the upper third should preserve enough negative space for premium cover-slide typography.