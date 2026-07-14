# SVG Recipe — Center Image Metric Split

## Visual mechanism
A single oversized metric anchors the left side while a clipped hero image overlaps the center seam, visually separating the number from a compact editorial headline on the right. The image acts like a sticker or badge layered above the typography, creating a bold metric reveal with low content density.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<linearGradient>` for the warm background wash and central image rim
- 1× `<filter id="softShadow">` applied to the central image backing shape
- 1× `<clipPath>` with a custom `<path>` for the organic hero image crop
- 1× `<image>` for the central overlapping hero photo
- 3× `<path>` for the image backing blob, gradient rim, and playful accent marks
- 2× `<circle>` for small decorative dots near the image and headline
- 1× `<line>` for the subtle split/accent rule under the headline
- 5× `<text>` blocks for the metric, percent label/accent, headline, footnote, and footer

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF7E8"/>
      <stop offset="0.58" stop-color="#FFF1D1"/>
      <stop offset="1" stop-color="#FFE3C4"/>
    </linearGradient>

    <linearGradient id="rimGradient" x1="445" y1="120" x2="845" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF7A59"/>
      <stop offset="0.45" stop-color="#FFCC4D"/>
      <stop offset="1" stop-color="#29B6A8"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroBlobClip" clipPathUnits="userSpaceOnUse">
      <path d="M636 119
               C711 111 793 144 824 208
               C858 278 833 367 780 425
               C727 482 638 504 562 470
               C489 437 449 362 463 283
               C477 203 558 128 636 119 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M97 115
           C155 65 245 61 307 108
           C374 158 367 256 312 302
           C256 349 155 338 103 283
           C51 226 42 162 97 115 Z"
        fill="#FFE08A" opacity="0.5"/>

  <path d="M998 493
           C1040 455 1113 452 1160 493
           C1206 533 1207 604 1160 643
           C1112 682 1036 674 998 629
           C961 585 958 529 998 493 Z"
        fill="#FFB3A7" opacity="0.42"/>

  <text x="82" y="382" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="184" font-weight="800" letter-spacing="-10"
        fill="#161616">73</text>

  <text x="394" y="377" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="800"
        fill="#FF6B4A">%</text>

  <path d="M636 104
           C722 96 812 133 848 204
           C889 285 858 385 797 450
           C735 516 632 540 544 501
           C460 464 416 377 431 285
           C447 193 546 114 636 104 Z"
        fill="url(#rimGradient)" filter="url(#softShadow)"/>

  <path d="M636 119
           C711 111 793 144 824 208
           C858 278 833 367 780 425
           C727 482 638 504 562 470
           C489 437 449 362 463 283
           C477 203 558 128 636 119 Z"
        fill="#FFFFFF"/>

  <image x="430" y="92" width="430" height="430"
         href="https://images.example.com/center-metric-split/playful-mobile-user-portrait-square.jpg"
         clip-path="url(#heroBlobClip)"
         preserveAspectRatio="xMidYMid slice"/>

  <path d="M445 172
           C417 150 401 132 391 105
           M843 186
           C875 166 899 144 917 113
           M808 474
           C847 498 875 525 896 562"
        fill="none" stroke="#161616" stroke-width="9" stroke-linecap="round"/>

  <circle cx="500" cy="505" r="13" fill="#29B6A8"/>
  <circle cx="892" cy="171" r="10" fill="#FF6B4A"/>

  <text x="790" y="252" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="800" line-height="1.05"
        fill="#161616">
    <tspan x="790" dy="0">choose</tspan>
    <tspan x="790" dy="56">mobile-first</tspan>
    <tspan x="790" dy="56">onboarding</tspan>
  </text>

  <line x1="792" y1="438" x2="1096" y2="438"
        stroke="#161616" stroke-width="4" stroke-linecap="round"/>

  <text x="792" y="483" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="600"
        fill="#5D4A3E">Q3 product activation study · n=18,420</text>

  <text x="82" y="641" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800"
        fill="#161616">2026 growth benchmark</text>

  <text x="792" y="641" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        fill="#876B5A">Metric shown as share of successful first sessions</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to fade the central image into the background; use an image `clipPath` instead.
- ❌ Applying `clip-path` to text or decorative paths; only apply the clip to the `<image>`.
- ❌ Building the center image with `<use>` or `<symbol>` duplicates; draw each blob/rim path directly.
- ❌ Putting `filter` on separator lines; shadows should be applied to filled shapes only.
- ❌ Letting headline text auto-wrap without explicit `width`; every `<text>` needs a width for reliable PowerPoint rendering.

## Composition notes
- Keep the metric huge and left-weighted, occupying roughly the left 40% of the slide; let the center image overlap the right edge of the number.
- The image should sit slightly above vertical center and feel like a sticker layered on top of both sides.
- Place the headline on the right with generous negative space; three short stacked lines work better than a paragraph.
- Use one warm background family plus two or three saturated accent colors so the metric, image rim, and small decorative marks feel coordinated.