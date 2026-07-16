# SVG Recipe — Isometric 3D Data Visualization

## Visual mechanism
Build 3D data bars manually from editable 2D faces: each bar is a stack of diamond/parallelogram paths with different gradient fills for top, left, and right faces. A deep neon background, floating translucent report panel, glowing wave, and soft platform shadow create the premium spatial dashboard environment.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 3× translucent `<rect>` for vertical light shafts behind the metric labels
- 2× `<ellipse>` for the isometric stage/platform and its cast shadow
- 6× decorative `<path>` for blurred ambient waves, glowing ribbon, floating report panel, and line-chart detail
- 9× `<path>` for the three isometric bars: top, left/front face, and right face per bar
- 6× small stroked `<path>` details for simple white data icons on the bar faces
- 3× `<line>` for vertical reference lines from metric labels to bar tops
- 7× `<text>` for title, percentages, and vertical data labels; every text has explicit `width`
- Multiple `<linearGradient>` definitions for background, bar faces, platform, side panel, and light shafts
- 2× `<filter>` definitions: one soft blur/glow filter for atmospheric shapes and one offset shadow filter for platform/panel depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4b43f2"/>
      <stop offset="45%" stop-color="#21165d"/>
      <stop offset="100%" stop-color="#14051f"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7e19ff" stop-opacity="0.62"/>
      <stop offset="55%" stop-color="#d500ff" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#24105e" stop-opacity="0.35"/>
    </linearGradient>
    <linearGradient id="shaftGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.20"/>
      <stop offset="58%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="platformGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#15206d"/>
      <stop offset="100%" stop-color="#080b2a"/>
    </linearGradient>
    <linearGradient id="orangeFace" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff34a"/>
      <stop offset="45%" stop-color="#ff9d45"/>
      <stop offset="100%" stop-color="#ff0f8d"/>
    </linearGradient>
    <linearGradient id="cyanFace" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7df6ff"/>
      <stop offset="48%" stop-color="#1bb9f3"/>
      <stop offset="100%" stop-color="#5042f5"/>
    </linearGradient>
    <linearGradient id="magentaFace" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff28b9"/>
      <stop offset="55%" stop-color="#e217c6"/>
      <stop offset="100%" stop-color="#7620e7"/>
    </linearGradient>
    <linearGradient id="ribbonGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#24f6ff" stop-opacity="0.95"/>
      <stop offset="45%" stop-color="#26c5ff" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ff2ccf" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
    <filter id="dropShadow" x="-25%" y="-25%" width="160%" height="160%">
      <feOffset dx="18" dy="22"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40 680 C210 520 360 590 560 500 C740 420 890 455 1080 560 C1190 620 1270 610 1340 560 L1340 760 L-40 760 Z"
        fill="#1ff1ff" opacity="0.13" filter="url(#softGlow)"/>
  <path d="M760 524 C820 150 905 110 958 372 C991 535 1068 336 1165 324 C1245 314 1298 470 1310 720 L1260 720 C1228 510 1165 418 1100 438 C1010 465 975 612 930 466 C875 287 830 310 785 542 Z"
        fill="#071130" opacity="0.72"/>
  <path d="M742 505 C812 132 906 112 958 363 C991 520 1062 325 1160 316 C1244 309 1298 464 1310 720 L1255 720 C1228 520 1165 430 1102 446 C1008 470 974 610 930 468 C878 296 830 320 787 545 Z"
        fill="url(#ribbonGrad)" opacity="0.92"/>

  <path d="M160 220 L596 104 L606 395 L170 492 Z" fill="url(#panelGrad)" filter="url(#dropShadow)" opacity="0.92"/>
  <text x="190" y="264" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-style="italic"
        letter-spacing="2" fill="#ffffff" opacity="0.72" transform="rotate(-13 190 264)">SALES REPORT</text>
  <path d="M232 407 C270 278 316 265 370 328 C422 389 458 322 493 169"
        fill="none" stroke="#ffffff" stroke-width="2" opacity="0.18"/>

  <ellipse cx="646" cy="566" rx="395" ry="74" fill="#03051a" opacity="0.55" filter="url(#softGlow)"/>
  <ellipse cx="646" cy="548" rx="392" ry="74" fill="url(#platformGrad)" opacity="0.96"/>

  <rect x="500" y="268" width="70" height="210" fill="url(#shaftGrad)" opacity="0.65"/>
  <rect x="585" y="142" width="70" height="300" fill="url(#shaftGrad)" opacity="0.68"/>
  <rect x="635" y="0" width="136" height="390" fill="url(#shaftGrad)" opacity="0.56"/>

  <line x1="535" y1="280" x2="535" y2="344" stroke="#ffffff" stroke-width="2" opacity="0.35"/>
  <line x1="620" y1="156" x2="620" y2="249" stroke="#ffffff" stroke-width="2" opacity="0.35"/>
  <line x1="710" y1="56" x2="710" y2="144" stroke="#ffffff" stroke-width="2" opacity="0.35"/>

  <text x="492" y="236" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">40%</text>
  <text x="572" y="146" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">65%</text>
  <text x="664" y="58" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">80%</text>

  <path d="M465 344 L535 306 L605 344 L535 382 Z" fill="#fff457"/>
  <path d="M465 344 L535 382 L535 612 L465 584 Z" fill="url(#orangeFace)"/>
  <path d="M535 382 L605 344 L605 574 L535 612 Z" fill="url(#orangeFace)" opacity="0.86"/>
  <path d="M555 406 L583 394 L583 419 L555 431 Z M561 414 L561 426 M568 411 L568 423 M575 408 L575 420"
        fill="none" stroke="#ffffff" stroke-width="2" opacity="0.75"/>
  <text x="566" y="558" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700"
        fill="#ffffff" opacity="0.85" transform="rotate(-90 566 558)">DATA 01</text>

  <path d="M550 249 L620 211 L690 249 L620 287 Z" fill="#8df4f6"/>
  <path d="M550 249 L620 287 L620 612 L550 574 Z" fill="url(#cyanFace)"/>
  <path d="M620 287 L690 249 L690 574 L620 612 Z" fill="url(#cyanFace)" opacity="0.82"/>
  <path d="M642 337 C654 304 671 291 681 292 M678 292 L680 306 M678 292 L667 299"
        fill="none" stroke="#ffffff" stroke-width="3" opacity="0.76"/>
  <text x="648" y="498" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700"
        fill="#ffffff" opacity="0.85" transform="rotate(-90 648 498)">DATA 02</text>

  <path d="M640 144 L710 106 L780 144 L710 182 Z" fill="#e78acb"/>
  <path d="M640 144 L710 182 L710 542 L640 504 Z" fill="url(#magentaFace)"/>
  <path d="M710 182 L780 144 L780 504 L710 542 Z" fill="url(#magentaFace)" opacity="0.82"/>
  <path d="M735 201 C748 188 766 196 764 212 C762 227 741 228 735 214 C729 201 747 190 756 202 C766 216 747 232 738 218"
        fill="none" stroke="#ffffff" stroke-width="3" opacity="0.64"/>
  <text x="736" y="424" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700"
        fill="#ffffff" opacity="0.85" transform="rotate(-90 736 424)">DATA 03</text>
</svg>
```

## Avoid in this skill
- ❌ Native PowerPoint 3D extrusion or camera effects; construct every prism face manually with editable paths for precise lighting control
- ❌ `skewX`, `skewY`, or `matrix(...)` transforms for the report panel; draw the panel as a quadrilateral path instead
- ❌ `<polygon>` for bar faces if you need maximum translator safety; use closed `<path d="... Z">` faces
- ❌ `marker-end` arrows on reference lines; use plain `<line>` elements without arrowheads
- ❌ Filters on `<line>` elements; apply glow/shadow only to paths, ellipses, rects, or text

## Composition notes
- Keep the chart mass slightly right of center, with the tallest bar near the visual focal point and shorter bars stepping forward-left.
- Use generous negative space in the upper-left and far-right so the translucent panel and cyan wave feel atmospheric rather than crowded.
- Align all bar bottoms to the same virtual platform plane; misaligned bases break the isometric illusion immediately.
- Use brighter, flatter colors on top faces and deeper vertical gradients on side faces to simulate overhead lighting.