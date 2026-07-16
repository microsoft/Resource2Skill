# SVG Recipe — Wavy Ribbon Split Cover

## Visual mechanism
A clean left-aligned cover panel is split from a bold abstract background by a flowing vertical wave, while stacked curved ribbon bands sweep across the right side like folded paper. Gradients, soft shadows, and darker crease shapes create the illusion of layered 3D ribbons without using non-editable effects.

## SVG primitives needed
- 2× `<rect>` for full-slide base backgrounds and subtle right-side color field
- 1× large `<path>` for the wavy left text panel
- 5× large `<path>` for overlapping ribbon bands with Bezier wave contours
- 5× smaller `<path>` for fold/crease shadows on top of ribbon bands
- 3× thin `<path>` for highlight glints following the ribbon curves
- 1× `<rect>` for the section label pill
- 4× `<text>` elements for eyebrow, headline, subhead, and footer metadata
- 6× `<linearGradient>` definitions for background, panel, and ribbon fills
- 1× `<radialGradient>` for a soft ambient glow
- 2× `<filter>` definitions using blur/offset/merge for editable shadows and glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDeep" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="0.55" stop-color="#172554"/>
      <stop offset="1" stop-color="#4C1D95"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="930" cy="250" r="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#38BDF8" stop-opacity="0.35"/>
      <stop offset="0.52" stop-color="#A855F7" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#111827" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="panelFill" x1="0" y1="0" x2="560" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#EEF2FF"/>
    </linearGradient>
    <linearGradient id="ribbonCyan" x1="480" y1="105" x2="1290" y2="190" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7DD3FC"/>
      <stop offset="0.42" stop-color="#22D3EE"/>
      <stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="ribbonViolet" x1="520" y1="240" x2="1290" y2="315" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#DDD6FE"/>
      <stop offset="0.45" stop-color="#A855F7"/>
      <stop offset="1" stop-color="#6D28D9"/>
    </linearGradient>
    <linearGradient id="ribbonPink" x1="430" y1="392" x2="1290" y2="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FBCFE8"/>
      <stop offset="0.45" stop-color="#EC4899"/>
      <stop offset="1" stop-color="#BE185D"/>
    </linearGradient>
    <linearGradient id="ribbonAmber" x1="600" y1="520" x2="1290" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FEF3C7"/>
      <stop offset="0.45" stop-color="#F59E0B"/>
      <stop offset="1" stop-color="#EA580C"/>
    </linearGradient>
    <linearGradient id="foldDark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#111827" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#111827" stop-opacity="0"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="14" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDeep)"/>
  <rect x="560" y="0" width="720" height="720" fill="url(#ambientGlow)" filter="url(#softGlow)"/>

  <path d="M0 0 H514 C594 67 551 152 602 224 C651 293 601 361 646 431 C700 514 595 605 650 720 H0 Z"
        fill="url(#panelFill)" filter="url(#softShadow)"/>
  <path d="M518 0 C598 72 554 151 604 224 C654 294 604 362 648 431 C702 515 597 604 652 720"
        fill="none" stroke="#FFFFFF" stroke-width="5" stroke-opacity="0.75"/>

  <path d="M470 118 C640 56 760 134 915 94 C1065 55 1178 50 1290 82 L1290 202
           C1142 162 1020 188 913 222 C760 270 635 210 482 254 Z"
        fill="url(#ribbonCyan)" filter="url(#softShadow)"/>
  <path d="M560 246 C655 216 714 233 790 250 C705 277 640 278 570 313 Z"
        fill="url(#foldDark)" opacity="0.55"/>
  <path d="M520 139 C654 95 760 150 908 119 C1030 93 1157 82 1282 108"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.42"/>

  <path d="M540 260 C682 205 811 287 944 249 C1088 208 1195 231 1290 284 L1290 405
           C1168 342 1070 329 931 369 C788 410 665 332 520 388 Z"
        fill="url(#ribbonViolet)" filter="url(#softShadow)"/>
  <path d="M928 249 C1006 229 1076 220 1151 235 C1106 271 1050 292 944 316 Z"
        fill="url(#foldDark)" opacity="0.48"/>
  <path d="M566 280 C700 234 810 306 942 273 C1078 239 1180 256 1278 304"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.34"/>

  <path d="M402 410 C575 330 737 453 900 402 C1057 353 1175 374 1290 455 L1290 580
           C1148 493 1040 489 895 531 C728 579 579 474 420 548 Z"
        fill="url(#ribbonPink)" filter="url(#softShadow)"/>
  <path d="M420 548 C506 506 580 493 662 504 C591 555 515 583 432 617 Z"
        fill="url(#foldDark)" opacity="0.44"/>
  <path d="M450 426 C602 371 742 474 898 426 C1037 383 1168 399 1276 470"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.30"/>

  <path d="M650 540 C770 489 900 548 1017 519 C1145 487 1227 520 1290 574 L1290 720
           H704 C668 661 594 593 650 540 Z"
        fill="url(#ribbonAmber)" filter="url(#softShadow)"/>
  <path d="M1008 520 C1095 500 1173 508 1238 543 C1192 578 1126 600 1022 612 Z"
        fill="url(#foldDark)" opacity="0.42"/>
  <path d="M681 556 C802 517 904 570 1015 543 C1124 516 1212 537 1278 592"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.32"/>

  <path d="M596 70 C640 118 632 174 604 224 C580 189 575 136 596 70 Z"
        fill="#0F172A" opacity="0.18"/>
  <path d="M642 431 C678 485 661 555 620 610 C608 540 617 487 642 431 Z"
        fill="#0F172A" opacity="0.14"/>

  <rect x="96" y="112" width="156" height="40" rx="20" fill="#312E81" opacity="0.95"/>
  <text x="124" y="138" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="2" fill="#FFFFFF">SECTION 01</text>

  <text x="96" y="245" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66" font-weight="800" fill="#111827">
    <tspan x="96" dy="0">Wavy Ribbon</tspan>
    <tspan x="96" dy="76" fill="#4F46E5">Split Cover</tspan>
  </text>
  <text x="100" y="420" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="400" fill="#475569">
    <tspan x="100" dy="0">A dynamic opener for bold strategy,</tspan>
    <tspan x="100" dy="34">brand, or transformation stories.</tspan>
  </text>
  <text x="100" y="624" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="1.3" fill="#64748B">EXECUTIVE KEYNOTE · 2026</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut the wavy split; draw the left panel as a single editable `<path>` instead.
- ❌ Do not use `<pattern>` fills for ribbon texture; use gradients, highlight strokes, and crease paths.
- ❌ Do not place filters on `<line>` elements; use filtered `<path>` ribbons for shadows.
- ❌ Do not rely on `skewX`, `skewY`, or matrix transforms for perspective folds; build the folded look directly with Bezier paths.
- ❌ Do not make the ribbons perfectly parallel rectangles; the premium look comes from asymmetrical wave contours and overlapping creases.

## Composition notes
- Keep the left 35–45% of the slide calm and bright for headline readability; the wavy split edge should intrude slightly into the ribbon field.
- Put the strongest saturation and deepest shadows on the right half, where the eye expects the visual spectacle.
- Layer ribbons from top to bottom with partial overlaps; add darker crease patches exactly where one band appears to tuck under another.
- Use one cool-to-warm color rhythm across the bands so the composition feels energetic but still controlled.