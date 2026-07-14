# SVG Recipe — Vintage Editorial Master Layout ("Renaissance" Style)

## Visual mechanism
A premium editorial slide built from a sage linen/parchment atmosphere, a large cropped “mounted print” photograph, and an overlapping aged paper title band. The elegance comes from warm radial vignettes, delicate hairline rules, tactile shadows, and serif typography with italic supporting copy.

## SVG primitives needed
- 3× `<rect>` for the full-slide base, mounted photo backing, and photo mat border
- 1× `<image>` clipped into the photo area for the hero editorial photograph
- 1× `<clipPath>` with rounded `<rect>` applied to the photo image
- 1× `<path>` for the irregular parchment title panel with subtly uneven/deckled edges
- 10–16× `<path>` for faint linen grain, paper fibers, and hand-drawn accent scratches
- 4× `<line>` for thin editorial guide rules and inset page borders
- 5× `<text>` for the large title, small kicker, italic body levels, and folio label
- 2× `<radialGradient>` for aged vignette backgrounds
- 2× `<linearGradient>` for parchment panel depth and photo mat warmth
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` applied to the mounted photo and paper panel
- 1× `<filter id="paperGlow">` using `feGaussianBlur` for a soft luminous paper edge

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="linenVignette" cx="52%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#c6d4a1"/>
      <stop offset="58%" stop-color="#aebe82"/>
      <stop offset="100%" stop-color="#7f9365"/>
    </radialGradient>

    <radialGradient id="photoWarmth" cx="50%" cy="44%" r="70%">
      <stop offset="0%" stop-color="#fffaf0" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#4b3325" stop-opacity="0.16"/>
    </radialGradient>

    <linearGradient id="matPaper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fffdf6"/>
      <stop offset="55%" stop-color="#f4efe3"/>
      <stop offset="100%" stop-color="#ddd2bd"/>
    </linearGradient>

    <linearGradient id="agedPanel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f3e9b8"/>
      <stop offset="52%" stop-color="#efe2a2"/>
      <stop offset="100%" stop-color="#d8c57e"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="10" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="paperGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="1.4"/>
    </filter>

    <clipPath id="photoClip">
      <rect x="360" y="34" width="730" height="430" rx="3"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#linenVignette)"/>

  <path d="M14 84 C154 62 265 76 383 48 M22 143 C162 132 264 151 396 125 M35 230 C170 206 296 222 433 198"
        fill="none" stroke="#e7e0bd" stroke-width="1.1" stroke-opacity="0.16"/>
  <path d="M42 360 C190 338 312 359 470 335 M20 494 C168 470 307 491 452 462 M78 624 C219 608 348 618 520 590"
        fill="none" stroke="#506643" stroke-width="1.2" stroke-opacity="0.20"/>
  <path d="M1120 26 C1178 108 1174 196 1226 282 M1168 390 C1215 458 1207 554 1246 646"
        fill="none" stroke="#6f8055" stroke-width="1.2" stroke-opacity="0.22"/>
  <path d="M100 42 L101 690 M151 40 L149 690 M206 36 L208 690 M262 42 L260 690"
        fill="none" stroke="#f3edca" stroke-width="0.8" stroke-opacity="0.14"/>
  <path d="M24 114 L1238 112 M31 268 L1246 264 M22 546 L1254 542"
        fill="none" stroke="#f6efbf" stroke-width="0.8" stroke-opacity="0.14"/>

  <line x1="70" y1="58" x2="1210" y2="58" stroke="#e7ddb5" stroke-width="1.2" stroke-opacity="0.55"/>
  <line x1="70" y1="662" x2="1210" y2="662" stroke="#6d5b42" stroke-width="1.1" stroke-opacity="0.32"/>
  <line x1="70" y1="58" x2="70" y2="662" stroke="#e7ddb5" stroke-width="1.1" stroke-opacity="0.42"/>
  <line x1="1210" y1="58" x2="1210" y2="662" stroke="#6d5b42" stroke-width="1.1" stroke-opacity="0.25"/>

  <rect x="333" y="18" width="786" height="493" rx="4" fill="#473629" opacity="0.30" filter="url(#softShadow)"/>
  <rect x="326" y="14" width="785" height="490" rx="4" fill="url(#matPaper)"/>
  <rect x="354" y="28" width="742" height="444" rx="3" fill="#eee5d3" stroke="#cfc0a4" stroke-width="1"/>
  <image href="https://images.unsplash.com/photo-1470337458703-46ad1756a187?q=vintage-italian-table-risotto-wooden-spoon"
         x="360" y="34" width="730" height="430" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip)"/>
  <rect x="360" y="34" width="730" height="430" rx="3" fill="url(#photoWarmth)" stroke="#7b5d45" stroke-width="1.2" stroke-opacity="0.38"/>

  <path d="M188 454
           C310 445 450 454 592 448
           C730 442 892 452 1058 445
           C1081 468 1088 532 1074 677
           C930 679 780 673 626 680
           C468 687 325 676 196 684
           C184 626 178 508 188 454 Z"
        fill="url(#agedPanel)" stroke="#c5ad68" stroke-width="1.2" filter="url(#softShadow)"/>

  <path d="M205 471 C354 463 478 474 627 466 C765 459 903 469 1050 461"
        fill="none" stroke="#fff7cf" stroke-width="2" stroke-opacity="0.42" filter="url(#paperGlow)"/>
  <path d="M209 492 C366 483 514 495 680 486 M220 641 C410 626 610 647 804 630 M860 635 C932 628 1000 632 1061 624"
        fill="none" stroke="#7e6a3e" stroke-width="0.9" stroke-opacity="0.16"/>
  <path d="M244 525 C260 520 271 523 282 517 M330 595 C350 588 368 595 388 586 M930 505 C954 499 972 504 997 497"
        fill="none" stroke="#fff6c6" stroke-width="1.2" stroke-opacity="0.40"/>

  <text x="224" y="114" width="250" font-family="Georgia, 'Times New Roman', serif" font-size="18" letter-spacing="2.5"
        fill="#5c4a35" opacity="0.74">RENAISSANCE TABLE</text>
  <text x="720" y="568" width="350" font-family="Georgia, 'Times New Roman', serif" font-size="70"
        fill="#6f4f45" letter-spacing="-2">Title Text</text>
  <text x="804" y="618" width="240" font-family="Georgia, 'Times New Roman', serif" font-size="20"
        font-style="italic" fill="#7c6a48">Body Level One</text>
  <text x="806" y="652" width="250" font-family="Georgia, 'Times New Roman', serif" font-size="18"
        font-style="italic" fill="#7c6a48" opacity="0.84">Body Level Two</text>
  <text x="806" y="684" width="250" font-family="Georgia, 'Times New Roman', serif" font-size="17"
        font-style="italic" fill="#7c6a48" opacity="0.72">Body Level Three</text>

  <text x="218" y="625" width="320" font-family="Georgia, 'Times New Roman', serif" font-size="14"
        fill="#6d5a3b" letter-spacing="1.2" opacity="0.58">HANDCRAFTED HERITAGE · SEASONAL NOTES</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` for linen or paper grain; use faint editable paths/lines instead.
- ❌ Applying `clip-path` to the parchment panel or other non-image shapes; only clip the hero `<image>`.
- ❌ Heavy bitmap-only backgrounds that flatten the whole slide; keep borders, panels, and typography as editable shapes.
- ❌ Modern sans-serif blocks, bright corporate colors, or hard black shadows, which break the aged editorial tone.
- ❌ `mask`, `foreignObject`, `textPath`, or skew/matrix transforms for deckled paper effects.

## Composition notes
- Keep the large photograph in the upper/right 55–60% of the canvas, then overlap it with the parchment title band to create physical layering.
- Reserve the left side for negative space, subtle texture, and a small editorial kicker rather than dense text.
- Use warm browns, sage greens, cream, and muted gold; avoid pure white except for tiny paper highlights.
- Hairline borders and guide rules should be barely visible, giving the slide a printed-page discipline without looking like a grid.