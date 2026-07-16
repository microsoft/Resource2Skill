# SVG Recipe — Paper Fold Reveal Transition

## Visual mechanism
A cinematic title reveal is simulated by placing bold central typography behind two thick, wavy “paper flaps” that have been pulled toward the slide edges. Layered organic paths, cyan rim highlights, deep shadows, and glossy gradients make the flaps feel like folded paper or parting curtains.

## SVG primitives needed
- 1× `<rect>` for the full-slide pale cyan outer paper/backing layer
- 1× `<rect>` for the revealed dark violet-to-blue stage background
- 2× large `<path>` shapes for the left and right main folded paper flaps with organic wavy inner edges
- 4× secondary `<path>` shapes for darker under-folds and bright cyan rim highlights along the flap edges
- 2× translucent `<ellipse>` shapes for background glow blooms behind the title
- 1× `<text>` group for the small spaced-out eyebrow label
- 1× massive `<text>` title for the revealed message
- 1× subtitle `<text>` below the headline
- 1× rounded `<rect>` pill callout plus 1× small icon-like circle/rect cluster for a PowerPoint badge
- 4× `<linearGradient>` definitions for background, flaps, rim highlights, and metallic text
- 1× `<radialGradient>` for soft center glow
- 3× `<filter>` definitions using blur/offset/merge for flap depth, title shadow, and neon glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="outerPaper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8d8ff"/>
      <stop offset="46%" stop-color="#d7fbff"/>
      <stop offset="100%" stop-color="#f0d3ee"/>
    </linearGradient>

    <linearGradient id="stageBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7800d8"/>
      <stop offset="45%" stop-color="#d000ff"/>
      <stop offset="100%" stop-color="#002d9c"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#ff38ff" stop-opacity="0.72"/>
      <stop offset="55%" stop-color="#7112e6" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#00115e" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="leftFold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#220087"/>
      <stop offset="38%" stop-color="#8e00d7"/>
      <stop offset="100%" stop-color="#27006f"/>
    </linearGradient>

    <linearGradient id="rightFold" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#23007d"/>
      <stop offset="42%" stop-color="#a600e8"/>
      <stop offset="100%" stop-color="#07166f"/>
    </linearGradient>

    <linearGradient id="cyanRim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#aefcff"/>
      <stop offset="55%" stop-color="#10c8ff"/>
      <stop offset="100%" stop-color="#0047ff"/>
    </linearGradient>

    <linearGradient id="titleSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f7d8ff"/>
      <stop offset="22%" stop-color="#ffffff"/>
      <stop offset="42%" stop-color="#c7f8ff"/>
      <stop offset="62%" stop-color="#ffffff"/>
      <stop offset="78%" stop-color="#f4c9ff"/>
      <stop offset="100%" stop-color="#d9fbff"/>
    </linearGradient>

    <linearGradient id="pillFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5b008c"/>
      <stop offset="55%" stop-color="#7b00b9"/>
      <stop offset="100%" stop-color="#4a006c"/>
    </linearGradient>

    <filter id="flapShadow" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset dx="18" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="flapShadowRight" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset dx="-18" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#outerPaper)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#stageBg)"/>
  <ellipse cx="640" cy="275" rx="360" ry="260" fill="url(#centerGlow)" filter="url(#softGlow)"/>
  <ellipse cx="910" cy="470" rx="260" ry="190" fill="#001a8f" opacity="0.42" filter="url(#softGlow)"/>

  <path d="M-40,0 C90,0 165,22 175,84 C186,145 112,244 99,315 C86,386 128,430 201,487 C274,544 314,596 294,720 L-40,720 Z"
        fill="#050047" opacity="0.78" filter="url(#flapShadow)"/>
  <path d="M-22,0 C105,0 183,28 199,93 C216,161 143,251 128,322 C113,391 163,435 232,491 C301,548 344,607 325,720 L-22,720 Z"
        fill="url(#cyanRim)" opacity="0.88"/>
  <path d="M-80,0 C56,0 145,20 166,77 C190,143 121,249 105,316 C87,390 143,432 214,489 C286,547 329,605 305,720 L-80,720 Z"
        fill="url(#leftFold)" filter="url(#flapShadow)"/>
  <path d="M-80,0 C43,0 130,26 151,86 C175,154 104,250 93,319 C82,385 130,426 194,480 C261,536 299,602 276,720 L-80,720 Z"
        fill="#10004f" opacity="0.32"/>

  <path d="M1320,0 C1190,0 1115,22 1105,84 C1094,145 1168,244 1181,315 C1194,386 1152,430 1079,487 C1006,544 966,596 986,720 L1320,720 Z"
        fill="#04003f" opacity="0.76" filter="url(#flapShadowRight)"/>
  <path d="M1302,0 C1175,0 1097,28 1081,93 C1064,161 1137,251 1152,322 C1167,391 1117,435 1048,491 C979,548 936,607 955,720 L1302,720 Z"
        fill="url(#cyanRim)" opacity="0.9"/>
  <path d="M1360,0 C1224,0 1135,20 1114,77 C1090,143 1159,249 1175,316 C1193,390 1137,432 1066,489 C994,547 951,605 975,720 L1360,720 Z"
        fill="url(#rightFold)" filter="url(#flapShadowRight)"/>
  <path d="M1360,0 C1237,0 1150,26 1129,86 C1105,154 1176,250 1187,319 C1198,385 1150,426 1086,480 C1019,536 981,602 1004,720 L1360,720 Z"
        fill="#0d0052" opacity="0.3"/>

  <text x="640" y="66" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" letter-spacing="18"
        fill="#ffffff" opacity="0.15">FOLDING EFFECT MAGIC</text>

  <text x="640" y="376" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="150" font-weight="900"
        fill="url(#titleSheen)" filter="url(#titleShadow)">THANK YOU</text>

  <text x="640" y="448" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800"
        fill="#ffffff" filter="url(#titleShadow)">Slide— With Folding Effect Magic</text>

  <rect x="420" y="500" width="445" height="65" rx="32" fill="url(#pillFill)" opacity="0.88" filter="url(#titleShadow)"/>
  <circle cx="472" cy="532" r="36" fill="#f05a24"/>
  <path d="M472,496 A36,36 0 0 1 508,532 L472,532 Z" fill="#ffd36b" opacity="0.9"/>
  <rect x="420" y="511" width="43" height="42" rx="5" fill="#ffffff" opacity="0.48"/>
  <text x="441" y="543" width="42" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="900"
        fill="#ffffff">P</text>
  <text x="540" y="545" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="400"
        fill="#ffffff">in PowerPoint!</text>

  <text x="640" y="682" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" letter-spacing="18"
        fill="#ffffff" opacity="0.11">FOLDING EFFECT MAGIC</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; create separate closed/open slides and use PowerPoint Morph between them.
- ❌ Do not use `<mask>` for the wavy paper cut; use explicit editable `<path>` geometry instead.
- ❌ Do not apply `clip-path` to flap paths; clipping is only reliable for images, and the folded edges should remain editable paths.
- ❌ Do not rely on `marker-end` or path arrowheads; this transition has no arrow mechanics and markers may disappear.
- ❌ Do not build the flaps as raster PNGs unless absolutely necessary; editable gradient paths give better PowerPoint control.

## Composition notes
- Keep the headline locked in the center 55–65% of the slide; the folded flaps should frame it without covering the main word in the open-state slide.
- Use a pale cyan/pink outer paper layer against a saturated violet-blue reveal stage to maximize the feeling of an opened aperture.
- Give each flap at least three layers: dark under-fold shadow, bright cyan rim, and main purple gradient surface.
- For the actual transition, duplicate the slide: on slide 1 move the left and right flap paths inward until they meet at center; on slide 2 place them at the edges as shown, then apply Morph.