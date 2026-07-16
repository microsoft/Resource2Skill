# SVG Recipe — Masonry Image Grid

## Visual mechanism
A staggered 3-column image wall uses varied tile heights, rounded crops, offset color backplates, and translucent duotone overlays to create an editorial masonry rhythm. Keep copy in a calm side rail while the image grid carries the playful, bold energy.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<linearGradient>` for the warm editorial background wash
- 6× `<clipPath>` with rounded `<rect>` crops, one per masonry image
- 6× `<image>` elements clipped into different-height rounded tiles
- 6× `<rect>` backplates behind images for bright offset color blocks
- 6× translucent rounded `<rect>` overlays for duotone color washes on image tiles
- 1× `<filter id="tileShadow">` applied to image backplates for soft depth
- 1× `<filter id="softGlow">` applied to decorative blobs/accent shapes
- 2× organic `<path>` shapes for energetic blobs behind the grid
- 2× decorative dashed/curved `<path>` accents for playful editorial motion
- 3× `<text>` elements with explicit `width` for headline, subtitle, and eyebrow label
- Multiple small `<circle>` elements for confetti-like rhythm dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF4DA"/>
      <stop offset="0.55" stop-color="#FFE7EF"/>
      <stop offset="1" stop-color="#DDF7FF"/>
    </linearGradient>

    <linearGradient id="hotOverlay" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF2A8A" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#FFB000" stop-opacity="0.15"/>
    </linearGradient>
    <linearGradient id="coolOverlay" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#00C2FF" stop-opacity="0.40"/>
      <stop offset="1" stop-color="#6D39FF" stop-opacity="0.18"/>
    </linearGradient>

    <filter id="tileShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="crop1" clipPathUnits="userSpaceOnUse"><rect x="560" y="88" width="190" height="208" rx="28"/></clipPath>
    <clipPath id="crop2" clipPathUnits="userSpaceOnUse"><rect x="560" y="320" width="190" height="286" rx="28"/></clipPath>
    <clipPath id="crop3" clipPathUnits="userSpaceOnUse"><rect x="775" y="42" width="190" height="300" rx="28"/></clipPath>
    <clipPath id="crop4" clipPathUnits="userSpaceOnUse"><rect x="775" y="366" width="190" height="214" rx="28"/></clipPath>
    <clipPath id="crop5" clipPathUnits="userSpaceOnUse"><rect x="990" y="116" width="190" height="238" rx="28"/></clipPath>
    <clipPath id="crop6" clipPathUnits="userSpaceOnUse"><rect x="990" y="378" width="190" height="278" rx="28"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M902 18 C1015 -14 1148 35 1210 126 C1267 211 1212 305 1112 309 C1004 314 930 269 867 200 C808 136 799 48 902 18 Z"
        fill="#FFE100" opacity="0.36" filter="url(#softGlow)"/>
  <path d="M604 595 C684 532 802 558 846 625 C879 675 831 728 741 735 C639 743 552 690 604 595 Z"
        fill="#00D2FF" opacity="0.26" filter="url(#softGlow)"/>

  <text x="72" y="94" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="3" fill="#E01973">EDITORIAL FEATURE GRID</text>

  <text x="70" y="174" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="60" font-weight="800" line-height="1.02" fill="#18111F">
    <tspan x="70" dy="0">Culture</tspan>
    <tspan x="70" dy="64">in full</tspan>
    <tspan x="70" dy="64">color.</tspan>
  </text>

  <text x="74" y="398" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#4E4656">
    Six visual moments, stacked like a magazine wall: uneven, confident, and made for fast executive scanning.
  </text>

  <path d="M77 505 C150 470 234 494 300 464 C348 442 385 404 428 418"
        fill="none" stroke="#18111F" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 16"/>
  <path d="M420 565 C459 535 497 531 527 557 C553 580 542 618 506 630 C464 644 421 613 420 565 Z"
        fill="#FF2A8A" opacity="0.16"/>

  <circle cx="94" cy="566" r="7" fill="#00A8FF"/>
  <circle cx="130" cy="606" r="5" fill="#FFB000"/>
  <circle cx="184" cy="557" r="9" fill="#FF2A8A"/>
  <circle cx="252" cy="618" r="6" fill="#18111F"/>
  <circle cx="314" cy="575" r="4" fill="#6D39FF"/>

  <rect x="572" y="100" width="190" height="208" rx="28" fill="#FFB000" filter="url(#tileShadow)"/>
  <image href="https://images.example.com/editorial-street-fashion-bright-jacket.jpg"
         x="560" y="88" width="190" height="208" preserveAspectRatio="xMidYMid slice" clip-path="url(#crop1)"/>
  <rect x="560" y="88" width="190" height="208" rx="28" fill="url(#hotOverlay)" opacity="0.72"/>

  <rect x="546" y="334" width="190" height="286" rx="28" fill="#00D2FF" filter="url(#tileShadow)"/>
  <image href="https://images.example.com/creative-team-workshop-colorful-posters.jpg"
         x="560" y="320" width="190" height="286" preserveAspectRatio="xMidYMid slice" clip-path="url(#crop2)"/>
  <rect x="560" y="320" width="190" height="286" rx="28" fill="url(#coolOverlay)" opacity="0.66"/>

  <rect x="790" y="56" width="190" height="300" rx="28" fill="#FF2A8A" filter="url(#tileShadow)"/>
  <image href="https://images.example.com/pop-art-portrait-neon-sunglasses.jpg"
         x="775" y="42" width="190" height="300" preserveAspectRatio="xMidYMid slice" clip-path="url(#crop3)"/>
  <rect x="775" y="42" width="190" height="300" rx="28" fill="url(#hotOverlay)" opacity="0.62"/>

  <rect x="764" y="378" width="190" height="214" rx="28" fill="#6D39FF" filter="url(#tileShadow)"/>
  <image href="https://images.example.com/bold-product-detail-electric-blue-background.jpg"
         x="775" y="366" width="190" height="214" preserveAspectRatio="xMidYMid slice" clip-path="url(#crop4)"/>
  <rect x="775" y="366" width="190" height="214" rx="28" fill="url(#coolOverlay)" opacity="0.70"/>

  <rect x="1004" y="102" width="190" height="238" rx="28" fill="#00A8FF" filter="url(#tileShadow)"/>
  <image href="https://images.example.com/music-festival-crowd-confetti-daylight.jpg"
         x="990" y="116" width="190" height="238" preserveAspectRatio="xMidYMid slice" clip-path="url(#crop5)"/>
  <rect x="990" y="116" width="190" height="238" rx="28" fill="url(#coolOverlay)" opacity="0.58"/>

  <rect x="1002" y="390" width="190" height="278" rx="28" fill="#FFE100" filter="url(#tileShadow)"/>
  <image href="https://images.example.com/design-studio-table-tools-color-swatches.jpg"
         x="990" y="378" width="190" height="278" preserveAspectRatio="xMidYMid slice" clip-path="url(#crop6)"/>
  <rect x="990" y="378" width="190" height="278" rx="28" fill="url(#hotOverlay)" opacity="0.60"/>

  <path d="M1110 63 C1140 42 1182 47 1202 77 C1221 105 1204 139 1167 144"
        fill="none" stroke="#18111F" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 10"/>
  <circle cx="1198" cy="202" r="8" fill="#FF2A8A"/>
  <circle cx="1220" cy="245" r="5" fill="#18111F"/>
  <circle cx="1202" cy="622" r="9" fill="#00A8FF"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` fills to fake tiled image repetition; use separate clipped `<image>` tiles so each crop remains editable.
- ❌ Do not apply `clip-path` to overlay rectangles; only clipped `<image>` elements reliably translate. Match overlays with rounded `<rect>` geometry instead.
- ❌ Do not use `<mask>` for duotone effects; use translucent rounded rectangles or gradients over the images.
- ❌ Do not use `<use>` to duplicate tile groups; create each tile explicitly because `<use>` hard-fails translation.
- ❌ Do not make all tiles the same height; the technique depends on staggered vertical rhythm and mismatched tile proportions.

## Composition notes
- Reserve roughly the left 38–42% of the slide for headline, subtitle, and small editorial accents; keep the masonry grid on the right.
- Use three fixed-width columns with consistent gutters, but vary tile heights and y-offsets so the top and bottom edges do not align.
- Offset saturated backplates 10–16 px from the image crops to create a playful print-collage feeling.
- Alternate warm and cool overlays across adjacent tiles so the grid feels rhythmic rather than randomly colored.