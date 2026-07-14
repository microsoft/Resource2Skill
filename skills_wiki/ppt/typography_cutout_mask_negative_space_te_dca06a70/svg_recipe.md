# SVG Recipe — Typography Cutout Mask (Negative Space Text Reveal)

## Visual mechanism
A solid foreground plane appears to have giant typography punched out of it, with vivid photography visible only inside the letterforms. In SVG-to-PPT, reproduce the “cutout” illusion by placing clipped photo images on top of the solid plane using letter-shaped `clipPath`s rather than unsupported SVG masks.

## SVG primitives needed
- 1× full-slide `<rect>` for the matte foreground color.
- 2× `<image>` elements for photographic content revealed inside the typography: one scenic image for “THANK”, one transit/urban image for “YOU”.
- 2× `<clipPath>` definitions containing many `<rect>` and `<polygon>` letter components to create heavy block-letter cutouts.
- 1× tall `<rect>` for the intersecting black vertical divider accent.
- 3× `<text>` elements for the small spaced subtitle and bottom-left tutorial-style callouts.
- 1× `<path>` for the oversized orange curved arrow.
- 1× `<circle>`, 2× `<rect>`, 1× `<path>`, and 1× `<text>` for the floating PowerPoint-style badge.
- 2× `<linearGradient>` fills for premium logo/arrow color depth.
- 2× `<filter>` definitions: one soft shadow for floating objects and one warm glow for the white callout text.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pptCircleGrad" x1="1080" y1="40" x2="1260" y2="200" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff8a66"/>
      <stop offset="0.55" stop-color="#f05a38"/>
      <stop offset="1" stop-color="#d8482d"/>
    </linearGradient>
    <linearGradient id="arrowGrad" x1="520" y1="620" x2="790" y2="705" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffb21a"/>
      <stop offset="1" stop-color="#ff8a00"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="warmGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Geometric, ultra-bold block typography for THANK -->
    <clipPath id="thankClip" clipPathUnits="userSpaceOnUse">
      <!-- T -->
      <rect x="80" y="252" width="122" height="42"/>
      <rect x="120" y="252" width="42" height="214"/>
      <!-- H -->
      <rect x="214" y="252" width="42" height="214"/>
      <rect x="300" y="252" width="42" height="214"/>
      <rect x="214" y="338" width="128" height="42"/>
      <!-- A -->
      <polygon points="374,466 421,252 462,252 418,466"/>
      <polygon points="444,252 496,466 454,466 424,330"/>
      <rect x="405" y="374" width="76" height="39"/>
      <!-- N -->
      <rect x="510" y="252" width="42" height="214"/>
      <rect x="598" y="252" width="42" height="214"/>
      <polygon points="548,252 588,252 640,466 600,466"/>
      <!-- K -->
      <rect x="658" y="252" width="42" height="214"/>
      <polygon points="700,358 750,252 790,252 736,366"/>
      <polygon points="704,364 748,364 795,466 752,466"/>
    </clipPath>

    <!-- Separate clip for YOU so the revealed image can change mood -->
    <clipPath id="youClip" clipPathUnits="userSpaceOnUse">
      <!-- Y -->
      <polygon points="818,252 862,252 894,350 856,350"/>
      <polygon points="940,252 983,252 924,350 886,350"/>
      <rect x="874" y="344" width="45" height="122"/>
      <!-- O -->
      <rect x="958" y="252" width="126" height="42"/>
      <rect x="958" y="424" width="126" height="42"/>
      <rect x="958" y="252" width="42" height="214"/>
      <rect x="1042" y="252" width="42" height="214"/>
      <!-- U -->
      <rect x="1104" y="252" width="42" height="172"/>
      <rect x="1184" y="252" width="42" height="172"/>
      <rect x="1104" y="424" width="122" height="42"/>
    </clipPath>
  </defs>

  <!-- Matte foreground plane -->
  <rect x="0" y="0" width="1280" height="720" fill="#d9d9d9"/>

  <!-- Photo revealed only inside the massive letters -->
  <image x="0" y="0" width="1280" height="720"
         href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#thankClip)"/>
  <image x="0" y="0" width="1280" height="720"
         href="https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&amp;fit=crop&amp;w=1600&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#youClip)"/>

  <!-- Sharp editorial divider crossing the title -->
  <rect x="868" y="206" width="21" height="340" fill="#050505"/>

  <!-- Widely tracked secondary question -->
  <text x="150" y="504" width="1000" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="800" letter-spacing="20" fill="#17232a">
    DO YOU HAVE ANY QUESTION?
  </text>

  <!-- Floating PowerPoint-style icon in upper-right corner -->
  <circle cx="1172" cy="107" r="92" fill="url(#pptCircleGrad)" filter="url(#softShadow)"/>
  <path d="M1172 16 A91 91 0 0 1 1263 107 L1172 107 Z" fill="#ff8d6c" opacity="0.72"/>
  <path d="M1172 107 L1263 107 A91 91 0 0 1 1172 198 Z" fill="#ca3e29" opacity="0.65"/>
  <rect x="1070" y="48" width="102" height="120" rx="9" fill="#8d2e21" opacity="0.32"/>
  <rect x="1060" y="55" width="100" height="104" rx="8" fill="#d43a26" filter="url(#softShadow)"/>
  <text x="1085" y="138" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="88" font-weight="800" fill="#ffffff">P</text>

  <!-- Thumbnail-style lower-left supporting graphic -->
  <ellipse cx="210" cy="735" rx="315" ry="215" fill="#aebed4" opacity="0.75"/>
  <text x="34" y="610" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#ffffff" filter="url(#warmGlow)"
        transform="rotate(-8 34 610)">2 Minutes</text>
  <text x="26" y="690" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#ffffff" filter="url(#warmGlow)"
        transform="rotate(10 26 690)">MAKE SLIDE</text>

  <!-- Oversized curved arrow -->
  <path d="M628 576
           C710 610 758 657 779 720
           L719 720
           C695 685 662 665 621 670
           L608 720
           L512 624
           L634 574 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(#...)"` to punch real transparency; this breaks or is ignored in PPT translation.
- ❌ Do not apply `clip-path` to the grey foreground rectangle; clipping is reliable here only when applied to `<image>`.
- ❌ Do not use `<pattern>` image fills for the text; pattern fills are not preserved.
- ❌ Do not rely on live font text as the cutout unless you convert the letterforms into clip geometry; different machines may reflow or substitute the heavy font.
- ❌ Do not use `<textPath>` for curved sticker text; use rotated text blocks or individual positioned text instead.

## Composition notes
- Keep the main cutout word huge, centered, and monolithic; it should occupy roughly 65–75% of slide width and sit slightly above vertical center.
- Use a calm matte foreground color so the photography inside the letters becomes the only high-detail area.
- Add one sharp geometric interruption, such as a vertical black bar, to make the composition feel editorial rather than purely centered.
- Secondary text should be small, widely tracked, and placed close under the cutout word to reinforce the premium title-slide hierarchy.