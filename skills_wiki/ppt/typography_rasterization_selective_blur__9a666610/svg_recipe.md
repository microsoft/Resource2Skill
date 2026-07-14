# SVG Recipe — Typography Rasterization: Selective Blur & 3D Bisection

## Visual mechanism
Turn one oversized word into a photographic focus object by layering a blurred full-word copy behind a razor-sharp middle syllable, then create a second word that appears sliced horizontally and bent onto two opposing 3D planes. The effect relies on massive black typography, selective Gaussian blur, white “cut” covers, colored lower-half typography, and angled extrusion slabs that imply depth.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 2× `<rect>` for bisection cover cuts that hide the unwanted half of each duplicated word
- 3× `<linearGradient>` for 3D slab faces and subtle accent fills
- 2× `<filter>`: one Gaussian blur for the defocused word layer, one offset/blur/merge shadow for 3D depth
- 5× `<text>` for blurred full word, sharp center syllable, split top word, split bottom word, and small editorial labels
- 5× `<path>` for angled 3D extrusion slabs, fracture seams, and small typographic shards
- 2× `<line>` for focus guide marks beside the sharp region
- 2× transformed `<g>` groups for the top and bottom bisection planes using only `translate`, `rotate`, and `scale`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pinkFace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff007f"/>
      <stop offset="55%" stop-color="#ff4aa3"/>
      <stop offset="100%" stop-color="#8b0047"/>
    </linearGradient>

    <linearGradient id="darkFace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111111"/>
      <stop offset="100%" stop-color="#3b3b3b"/>
    </linearGradient>

    <linearGradient id="cyanGlint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00d4ff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#00d4ff" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
    </linearGradient>

    <filter id="blurWide" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>

    <filter id="slabShadow" x="-20%" y="-20%" width="150%" height="160%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Selective blur word: full word is defocused, center syllable is crisp -->
  <text x="118" y="246" width="1060"
        font-family="Segoe UI Black, Arial Black, Microsoft YaHei, sans-serif"
        font-size="178" font-weight="900" letter-spacing="-10"
        fill="#050505" opacity="0.72" filter="url(#blurWide)">FOCUS</text>

  <text x="315" y="246" width="560"
        font-family="Segoe UI Black, Arial Black, Microsoft YaHei, sans-serif"
        font-size="178" font-weight="900" letter-spacing="-10"
        fill="#000000">OCU</text>

  <line x1="300" y1="96" x2="300" y2="282" stroke="#00d4ff" stroke-width="3" stroke-dasharray="8 12"/>
  <line x1="875" y1="96" x2="875" y2="282" stroke="#00d4ff" stroke-width="3" stroke-dasharray="8 12"/>

  <text x="86" y="70" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" letter-spacing="4"
        fill="#777777">SELECTIVE FOCUS TYPOGRAPHY</text>

  <path d="M304 292 L878 292 L850 300 L330 300 Z" fill="url(#cyanGlint)" opacity="0.55"/>

  <!-- 3D extrusion slabs behind bisected word -->
  <path d="M416 414 L872 356 L930 390 L474 450 Z"
        fill="url(#darkFace)" opacity="0.96" filter="url(#slabShadow)"/>
  <path d="M438 474 L900 536 L940 498 L486 438 Z"
        fill="url(#pinkFace)" opacity="0.98" filter="url(#slabShadow)"/>

  <path d="M453 421 L908 364 L916 379 L461 438 Z"
        fill="#ffffff" opacity="0.52"/>
  <path d="M472 458 L918 516 L906 530 L460 471 Z"
        fill="#510027" opacity="0.38"/>

  <!-- Top half of BEND: duplicate word, lower half covered with background color -->
  <g transform="translate(420 437) rotate(-7) scale(1 0.86)">
    <text x="0" y="0" width="560"
          font-family="Segoe UI Black, Arial Black, Microsoft YaHei, sans-serif"
          font-size="158" font-weight="900" letter-spacing="-8"
          fill="#050505">BEND</text>
    <rect x="-18" y="-48" width="610" height="94" fill="#ffffff"/>
    <path d="M-4 -48 C102 -37 198 -62 294 -48 C402 -32 486 -58 586 -44"
          fill="none" stroke="#050505" stroke-width="5" stroke-linecap="round"/>
  </g>

  <!-- Bottom half of BEND: duplicate word, upper half covered with background color -->
  <g transform="translate(408 486) rotate(8) scale(1 0.88)">
    <text x="0" y="0" width="580"
          font-family="Segoe UI Black, Arial Black, Microsoft YaHei, sans-serif"
          font-size="158" font-weight="900" letter-spacing="-8"
          fill="#ff007f">BEND</text>
    <rect x="-18" y="-158" width="620" height="108" fill="#ffffff"/>
    <path d="M-2 -52 C96 -38 204 -64 302 -50 C402 -34 493 -62 590 -46"
          fill="none" stroke="#ff007f" stroke-width="5" stroke-linecap="round"/>
  </g>

  <!-- Small fracture shards to sell the physical slice -->
  <path d="M368 446 L392 433 L386 463 Z" fill="#050505"/>
  <path d="M930 424 L962 411 L948 446 Z" fill="#ff007f"/>
  <path d="M888 478 L918 489 L884 502 Z" fill="#111111" opacity="0.75"/>

  <text x="870" y="665" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="3"
        fill="#8a8a8a">3D BISECTION / TWO PLANES</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<clipPath>` on `<text>` to slice the word; clipping non-image elements is ignored by the translator.
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` for fake perspective; use `rotate(...)` and `scale(...)` only.
- ❌ Do not use `<mask>` for the half-word cutout; use background-colored cover rectangles or pre-rendered image halves instead.
- ❌ Do not apply filters to `<line>` elements; blur/shadow filters should be applied to `<text>`, `<path>`, `<rect>`, `<circle>`, or `<ellipse>`.
- ❌ Do not make the typography small. This technique fails unless the word dominates the slide.

## Composition notes
- Keep the slide mostly empty: the manipulated typography should consume 70–85% of the width, with only small editorial labels at the margins.
- Use a stark white or near-black background so the blur halos, sliced edges, and neon lower half remain visually crisp.
- For the bisection effect, duplicate the same word twice, rotate the halves in opposite directions, and hide the unwanted half with a background-colored rectangle.
- Add simple angled slab paths behind the halves to imply dimensionality; they do not need true perspective to read as a premium 3D typographic object.