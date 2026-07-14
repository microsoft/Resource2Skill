# SVG Recipe — Interactive Morphing Carousel Menu

## Visual mechanism
A horizontally sliding image filmstrip creates an app-like carousel, with the center item in full color and neighboring items in grayscale to signal focus. Large white ellipses layered over the top and bottom of the strip simulate a curved panoramic viewport while Morph transitions between duplicated slides move the strip smoothly.

## SVG primitives needed
- 1× `<rect>` for the slide background with a subtle premium gradient
- 7× `<image>` for carousel photos, each clipped into rounded vertical cards
- 7× `<clipPath>` with rounded `<rect>` for editable rounded photo crops
- 7× shadow `<rect>` cards behind photos, using `filter id="cardShadow"`
- 2× large white `<ellipse>` overlays for the curved viewport illusion
- 2× outlined `<rect>` label frames for the header and active item name
- 6× `<line>` for left/right chevron navigation arrows
- 5× `<circle>` pagination dots, with the active dot filled dark
- 4× `<text>` blocks with explicit `width` attributes for header, active item, hint text, and small metadata
- 1× `<linearGradient>` for the background
- 1× `<linearGradient>` for the active-card highlight stroke
- 1× `<filter>` with `feOffset`, `feGaussianBlur`, and `feMerge` for soft card shadows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#f7f5f0"/>
      <stop offset="100%" stop-color="#efe9dd"/>
    </linearGradient>

    <linearGradient id="activeStroke" x1="520" y1="170" x2="760" y2="500">
      <stop offset="0%" stop-color="#f2c36b"/>
      <stop offset="45%" stop-color="#ff7a45"/>
      <stop offset="100%" stop-color="#c93f2b"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipFarLeft"><rect x="-175" y="208" width="198" height="270" rx="28"/></clipPath>
    <clipPath id="clipLeftEdge"><rect x="62" y="198" width="210" height="288" rx="30"/></clipPath>
    <clipPath id="clipLeft"><rect x="300" y="190" width="218" height="304" rx="34"/></clipPath>
    <clipPath id="clipActive"><rect x="522" y="174" width="236" height="334" rx="40"/></clipPath>
    <clipPath id="clipRight"><rect x="762" y="190" width="218" height="304" rx="34"/></clipPath>
    <clipPath id="clipRightEdge"><rect x="1008" y="198" width="210" height="288" rx="30"/></clipPath>
    <clipPath id="clipFarRight"><rect x="1257" y="208" width="198" height="270" rx="28"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="490" y="48" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="4" fill="#7b7369" text-anchor="middle">
    INTERACTIVE CATALOG
  </text>
  <rect x="528" y="70" width="224" height="48" rx="0" fill="none" stroke="#111111" stroke-width="1.2"/>
  <text x="528" y="101" width="224" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="300" letter-spacing="6" fill="#111111" text-anchor="middle">
    OUR MENU
  </text>

  <rect x="-175" y="208" width="198" height="270" rx="28" fill="#ffffff" opacity="0.55" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/grayscale-strawberry-smoothie-vertical-photo.jpg" x="-175" y="208" width="198" height="270" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipFarLeft)" opacity="0.55"/>

  <rect x="62" y="198" width="210" height="288" rx="30" fill="#ffffff" opacity="0.72" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/grayscale-cola-can-vertical-photo.jpg" x="62" y="198" width="210" height="288" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipLeftEdge)" opacity="0.72"/>

  <rect x="300" y="190" width="218" height="304" rx="34" fill="#ffffff" opacity="0.86" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/grayscale-french-fries-vertical-photo.jpg" x="300" y="190" width="218" height="304" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipLeft)" opacity="0.88"/>

  <rect x="516" y="168" width="248" height="346" rx="44" fill="url(#activeStroke)" opacity="0.95" filter="url(#cardShadow)"/>
  <rect x="522" y="174" width="236" height="334" rx="40" fill="#ffffff"/>
  <image href="https://images.example.com/full-color-gourmet-burger-vertical-photo.jpg" x="522" y="174" width="236" height="334" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipActive)"/>

  <rect x="762" y="190" width="218" height="304" rx="34" fill="#ffffff" opacity="0.86" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/grayscale-colorful-macaron-vertical-photo.jpg" x="762" y="190" width="218" height="304" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipRight)" opacity="0.88"/>

  <rect x="1008" y="198" width="210" height="288" rx="30" fill="#ffffff" opacity="0.72" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/grayscale-pepperoni-pizza-vertical-photo.jpg" x="1008" y="198" width="210" height="288" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipRightEdge)" opacity="0.72"/>

  <rect x="1257" y="208" width="198" height="270" rx="28" fill="#ffffff" opacity="0.55" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/grayscale-sprinkle-donut-vertical-photo.jpg" x="1257" y="208" width="198" height="270" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipFarRight)" opacity="0.55"/>

  <ellipse cx="640" cy="75" rx="820" ry="118" fill="#ffffff"/>
  <ellipse cx="640" cy="602" rx="820" ry="148" fill="#ffffff"/>

  <line x1="139" y1="344" x2="111" y2="372" stroke="#111111" stroke-width="2.4" stroke-linecap="round"/>
  <line x1="111" y1="372" x2="139" y2="400" stroke="#111111" stroke-width="2.4" stroke-linecap="round"/>
  <line x1="1141" y1="344" x2="1169" y2="372" stroke="#111111" stroke-width="2.4" stroke-linecap="round"/>
  <line x1="1169" y1="372" x2="1141" y2="400" stroke="#111111" stroke-width="2.4" stroke-linecap="round"/>

  <rect x="535" y="548" width="210" height="54" fill="none" stroke="#111111" stroke-width="1.2"/>
  <text x="535" y="584" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="300" letter-spacing="5" fill="#111111" text-anchor="middle">
    BURGER
  </text>

  <text x="448" y="632" width="384" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6d655c" text-anchor="middle">
    Click the center card to open details • use arrows to browse
  </text>

  <circle cx="596" cy="666" r="4.5" fill="#b8b0a5"/>
  <circle cx="618" cy="666" r="4.5" fill="#b8b0a5"/>
  <circle cx="640" cy="666" r="6.5" fill="#111111"/>
  <circle cx="662" cy="666" r="4.5" fill="#b8b0a5"/>
  <circle cx="684" cy="666" r="4.5" fill="#b8b0a5"/>

  <line x1="604" y1="684" x2="676" y2="684" stroke="#111111" stroke-width="1.2" stroke-linecap="round"/>
  <text x="1036" y="666" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#8a8176" text-anchor="middle">
    MORPH READY
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG grayscale filters such as `feColorMatrix`; instead, supply preprocessed grayscale image assets for non-active cards.
- ❌ Real SVG masks for the curved viewport; use large background-colored ellipses layered above the carousel.
- ❌ `clip-path` on groups or shape elements; apply clip paths only to `<image>` elements.
- ❌ `marker-end` arrowheads on `<path>` elements; build navigation chevrons from simple `<line>` segments.
- ❌ Rebuilding each slide with different object counts; Morph works best when every carousel slide keeps the same element IDs/order and only changes x-positions, image color state, and labels.

## Composition notes
- Keep the carousel centered vertically, with the active card occupying the optical center and adjacent cards partially visible to imply more content off-screen.
- Reserve the top 120 px for the menu title and the bottom 170 px for the active item label, pagination, and interaction hints.
- For Morph slides, duplicate the slide, shift all card/photo/shadow x-coordinates by one card interval, then swap the new center card to the color image and all others to grayscale.
- Use a quiet warm-white background so the color center image becomes the dominant focal point while grayscale cards remain contextual.