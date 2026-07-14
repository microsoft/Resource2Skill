# SVG Recipe — Cinematic Text Cutout Mask

## Visual mechanism
A solid pale overlay dominates the slide while oversized block-letter silhouettes act like windows into vivid photography underneath. In SVG-to-PowerPoint, avoid true SVG masks; reproduce the same cinematic cutout by clipping photos to manually traced letter paths placed above the gray field.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft gray cinematic overlay/background.
- 2× `<image>` for the vibrant photo texture visible only inside the title letters.
- 2× `<clipPath>` applied to the images, each containing multiple `<rect>` and `<path>` letter-stroke silhouettes.
- 1× `<line>` for the stark vertical black divider/accent.
- 1× `<text>` for the widely tracked subtitle below the cutout title.
- 2× `<linearGradient>` and 1× `<radialGradient>` for the background and optional PowerPoint-style corner emblem.
- 1× `<filter id="softShadow">` applied to decorative logo shapes only.
- Several `<circle>`, `<rect>`, `<path>`, and `<text>` elements for the small top-left presentation-brand badge.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="paperGlow" cx="48%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#eeeeee"/>
      <stop offset="70%" stop-color="#d8d8d8"/>
      <stop offset="100%" stop-color="#cfcfcf"/>
    </radialGradient>

    <linearGradient id="orbGrad" x1="30" y1="12" x2="170" y2="154" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ff896c"/>
      <stop offset="52%" stop-color="#ef6046"/>
      <stop offset="100%" stop-color="#cf3f28"/>
    </linearGradient>

    <linearGradient id="badgeGrad" x1="14" y1="38" x2="96" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#e74b32"/>
      <stop offset="100%" stop-color="#b92f22"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="5" dy="7" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Left-side title window: T H A N -->
    <clipPath id="clipTitleLeft" clipPathUnits="userSpaceOnUse">
      <!-- T -->
      <rect x="258" y="280" width="70" height="30"/>
      <rect x="278" y="280" width="31" height="144"/>
      <!-- H -->
      <rect x="344" y="280" width="31" height="144"/>
      <rect x="393" y="280" width="31" height="144"/>
      <rect x="344" y="342" width="80" height="29"/>
      <!-- A, built from legs and crossbar so the triangular counter stays gray -->
      <path d="M440 424 L466 280 L494 280 L468 424 Z"/>
      <path d="M493 280 L523 424 L496 424 L478 342 L485 280 Z"/>
      <rect x="459" y="360" width="46" height="27"/>
      <!-- N -->
      <rect x="540" y="280" width="31" height="144"/>
      <path d="M570 280 L603 280 L622 424 L590 424 Z"/>
      <rect x="620" y="280" width="31" height="144"/>
    </clipPath>

    <!-- Right-side title window: K Y O U -->
    <clipPath id="clipTitleRight" clipPathUnits="userSpaceOnUse">
      <!-- K -->
      <rect x="655" y="280" width="31" height="144"/>
      <path d="M686 354 L724 280 L755 280 L713 358 Z"/>
      <path d="M686 350 L715 350 L758 424 L725 424 Z"/>
      <!-- Y -->
      <path d="M782 280 L816 280 L842 344 L815 344 Z"/>
      <path d="M858 280 L892 280 L850 368 L823 368 Z"/>
      <rect x="823" y="350" width="31" height="74"/>
      <!-- O as four strokes, leaving the center counter gray -->
      <rect x="910" y="280" width="82" height="30" rx="4"/>
      <rect x="910" y="394" width="82" height="30" rx="4"/>
      <rect x="910" y="300" width="31" height="104"/>
      <rect x="961" y="300" width="31" height="104"/>
      <!-- U -->
      <rect x="1015" y="280" width="31" height="113"/>
      <rect x="1070" y="280" width="31" height="113"/>
      <path d="M1015 391 C1015 414 1034 424 1058 424 C1082 424 1101 414 1101 391 L1070 391 C1070 399 1065 403 1058 403 C1051 403 1046 399 1046 391 Z"/>
    </clipPath>
  </defs>

  <!-- Pale solid mask field -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paperGlow)"/>

  <!-- Optional corner presentation emblem echoing the source frame -->
  <circle cx="103" cy="80" r="73" fill="url(#orbGrad)" filter="url(#softShadow)"/>
  <path d="M103 8 A72 72 0 0 1 176 80 L103 80 Z" fill="#ff8b70" opacity="0.78"/>
  <path d="M103 80 L176 80 A72 72 0 0 1 51 130 Z" fill="#cf3b24" opacity="0.72"/>
  <rect x="10" y="38" width="86" height="84" rx="7" fill="url(#badgeGrad)" filter="url(#softShadow)"/>
  <rect x="18" y="47" width="68" height="66" rx="5" fill="#ca3929"/>
  <text x="30" y="104" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="800" font-size="70" fill="#fff">P</text>

  <!-- The photos sit on top of gray but are clipped to letter geometry, creating the cutout illusion -->
  <image x="250" y="250" width="430" height="210"
         href="https://images.example.com/cinematic-golden-hills-at-sunrise.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipTitleLeft)"/>

  <image x="640" y="250" width="500" height="210"
         href="https://images.example.com/cinematic-mountain-temple-and-skyline.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipTitleRight)"/>

  <!-- Stark vertical sweeper / anchor line; do not apply filters to line elements -->
  <line x1="642" y1="162" x2="642" y2="563" stroke="#050505" stroke-width="8"/>

  <!-- Widely spaced subtitle; manual spacing is more reliable than letter-spacing across PPT translators -->
  <text x="274" y="491" width="815"
        font-family="Impact, 'Arial Black', Segoe UI, Microsoft YaHei, sans-serif"
        font-size="32" font-weight="700" fill="#070707">
    D o&nbsp;&nbsp; y o u&nbsp;&nbsp; h a v e&nbsp;&nbsp; A n y&nbsp;&nbsp; Q u e s t i o n ?
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` or `mask="url(#...)"` to punch transparent text holes; this hard-fails or is ignored in the PowerPoint pipeline.
- ❌ Do not use `<text>` as a clipping path directly; convert the large title to simple editable `<path>` / `<rect>` letter silhouettes inside `<clipPath>`.
- ❌ Do not use `<pattern>` or image pattern fills for the title; pattern fills are not preserved reliably.
- ❌ Do not put `clip-path` on a `<rect>`, `<path>`, or `<text>` overlay; in this pipeline clipping is reliable when applied to `<image>`.
- ❌ Do not apply filters to the vertical `<line>`; shadows/glows on lines are silently dropped.

## Composition notes
- Keep the massive title centered horizontally, occupying roughly 65–75% of slide width, with the letter window height around 140–170 px.
- The gray field needs generous negative space; let the image-filled title be the only saturated area in the center.
- Use a thin but high-contrast vertical divider slightly off the midpoint to create tension and a “sliding reveal” cue.
- Place the subtitle directly below the cutout title with extreme tracking or manual spacing, using black for a crisp editorial/keynote feel.