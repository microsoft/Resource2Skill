# SVG Recipe — Split Cover with Dual Badges

## Visual mechanism
A dramatic left-side hero photo owns slightly more than half the slide, cropped with a soft organic vertical edge; the right side stays clean for a headline, subhead, and two overlapping square badge images. The badges act as playful brand/category stamps that balance the visual weight of the hero image.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm editorial background
- 1× `<image>` for the large left hero photo, clipped to an organic divider shape
- 2× `<image>` for right-side square badge artwork, each clipped to rounded-square crops
- 4× `<rect>` for badge cards, shadows, borders, and highlight panels
- 3× `<path>` for decorative color blobs and the organic hero-image clipping path
- 3× `<text>` blocks for eyebrow label, headline, and subhead; all with explicit `width`
- 2× `<linearGradient>` for photo overlay and accent glow
- 1× `<radialGradient>` for soft right-side color atmosphere
- 2× `<filter>` definitions for editable soft shadow and glow effects
- 3× `<clipPath>` definitions: one custom path for the hero crop and two rounded squares for badges

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.08"/>
      <stop offset="55%" stop-color="#111827" stop-opacity="0.00"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.22"/>
    </linearGradient>

    <linearGradient id="coralGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6B6B"/>
      <stop offset="100%" stop-color="#FFC857"/>
    </linearGradient>

    <radialGradient id="rightAura" cx="55%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFE8A3" stop-opacity="0.85"/>
      <stop offset="48%" stop-color="#FDEDD8" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#FFF7EF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="20"/>
    </filter>

    <clipPath id="heroClip">
      <path d="M0,0 H756 C706,96 742,181 705,263 C663,356 737,430 700,525 C675,590 709,653 674,720 H0 Z"/>
    </clipPath>

    <clipPath id="badgeClip1">
      <rect x="958" y="96" width="154" height="154" rx="26"/>
    </clipPath>

    <clipPath id="badgeClip2">
      <rect x="1064" y="230" width="154" height="154" rx="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFF7EF"/>
  <rect x="704" y="0" width="576" height="720" fill="url(#rightAura)"/>

  <image
    href="https://images.example.com/hero-photo-playful-team-in-colorful-studio.jpg"
    x="0" y="0" width="780" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroClip)"/>

  <path d="M0,0 H756 C706,96 742,181 705,263 C663,356 737,430 700,525 C675,590 709,653 674,720 H0 Z"
        fill="url(#heroShade)" opacity="0.88"/>

  <path d="M833,78 C900,28 1008,38 1047,104 C1087,171 1038,252 955,252 C861,252 766,177 833,78 Z"
        fill="#B8F1E6" opacity="0.75" filter="url(#softGlow)"/>

  <path d="M1049,430 C1118,380 1215,404 1243,479 C1274,561 1213,641 1121,627 C1032,613 969,488 1049,430 Z"
        fill="#FFD166" opacity="0.46" filter="url(#softGlow)"/>

  <path d="M805,612 C850,583 912,596 935,641 C958,686 914,724 856,710 C801,696 761,641 805,612 Z"
        fill="#FF6B6B" opacity="0.18"/>

  <rect x="944" y="82" width="182" height="182" rx="32" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="958" y="96" width="154" height="154" rx="26" fill="#FFFFFF"/>
  <image
    href="https://images.example.com/badge-square-abstract-product-icon-coral.jpg"
    x="958" y="96" width="154" height="154"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#badgeClip1)"/>
  <rect x="958" y="96" width="154" height="154" rx="26" fill="none" stroke="#FFFFFF" stroke-width="6"/>

  <rect x="1050" y="216" width="182" height="182" rx="32" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="1064" y="230" width="154" height="154" rx="26" fill="#FFFFFF"/>
  <image
    href="https://images.example.com/badge-square-abstract-product-icon-teal.jpg"
    x="1064" y="230" width="154" height="154"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#badgeClip2)"/>
  <rect x="1064" y="230" width="154" height="154" rx="26" fill="none" stroke="#FFFFFF" stroke-width="6"/>

  <rect x="780" y="144" width="132" height="34" rx="17" fill="url(#coralGold)"/>
  <text x="804" y="167" width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="1.6"
        fill="#FFFFFF">NEW ISSUE</text>

  <text x="778" y="438" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        fill="#202124">
    <tspan x="778" dy="0">Designing</tspan>
    <tspan x="778" dy="66">moments that</tspan>
    <tspan x="778" dy="66" fill="#FF6B6B">feel memorable</tspan>
  </text>

  <text x="782" y="638" width="380"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="400"
        fill="#5B5F68">
    <tspan x="782" dy="0">A bold section opener with one hero image,</tspan>
    <tspan x="782" dy="30">two visual badges, and generous white space.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not make the slide a rigid two-column grid; the appeal comes from the organic photo edge and floating badge cluster.
- ❌ Do not apply `clip-path` to badge border rectangles; clip only the `<image>` elements, then draw editable rounded rectangles above them for borders.
- ❌ Do not use `<mask>` or `<pattern>` for the hero crop or image texture; use a direct `<clipPath>` on the image.
- ❌ Do not place the badges too close to the headline; they should read as visual stamps, not inline icons.
- ❌ Do not overfill the right side with body copy; this layout is strongest with low-density cover text.

## Composition notes
- Let the hero image occupy roughly 55–60% of the slide width, with its irregular edge crossing into the center to avoid a flat split.
- Keep headline and subhead in the lower-right quadrant, leaving the upper-right area for the two overlapping badges.
- Use warm neutrals on the right side so the photo and badges can carry saturated color without competing with the text.
- Badge cards should be square, slightly rounded, and shadowed; overlap them diagonally to create playful depth.