# SVG Recipe — Panoramic Card Reveal

## Visual mechanism
A cinematic full-bleed panorama is divided into four tall vertical cards, each card showing the same background image through its own clipped slice while soft edge shadows make the slices feel like raised panels. For the reveal, duplicate the slide: in the start state move the full card group off-canvas left and keep the title centered; in the end state move the card group into place and move the title off-canvas right, then apply PowerPoint Morph.

## SVG primitives needed
- 1× full-slide `<image>` for the atmospheric panoramic background
- 4× `<rect>` shadow panels behind the cards, each using a soft right-edge shadow filter
- 4× `<clipPath>` definitions with rounded `<rect>` crops for card image slices
- 4× clipped `<image>` elements, all using the same panorama href and slide-sized positioning so the photo appears continuous
- 4× semi-transparent `<rect>` overlays for contrast and premium glass-card tint
- 4× `<linearGradient>` fills for subtle card-edge darkening/highlight
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` for raised card depth
- 1× `<filter id="titleGlow">` using `feGaussianBlur` for soft hero-title glow
- 8× main `<text>` elements for card numbers and uppercase labels
- 8× reflected duplicate `<text>` elements using `transform="scale(1 -1)"` and low opacity to simulate polished text reflection
- 1× centered opening title `<text>` group, used on the start slide and moved off-canvas on the end slide
- 3× decorative `<path>` light streaks to add cinematic motion energy without relying on animation inside SVG

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.55"/>
      <stop offset="42%" stop-color="#020617" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.58"/>
    </linearGradient>

    <linearGradient id="cardSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.13"/>
      <stop offset="16%" stop-color="#ffffff" stop-opacity="0.03"/>
      <stop offset="80%" stop-color="#000000" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.24"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="70%" stop-color="#000000" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.56"/>
    </linearGradient>

    <linearGradient id="streak" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#67e8f9" stop-opacity="0"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#a78bfa" stop-opacity="0"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-5%" width="140%" height="112%">
      <feOffset dx="10" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>

    <clipPath id="clipCard1"><rect x="0" y="0" width="320" height="720" rx="0"/></clipPath>
    <clipPath id="clipCard2"><rect x="320" y="0" width="320" height="720" rx="0"/></clipPath>
    <clipPath id="clipCard3"><rect x="640" y="0" width="320" height="720" rx="0"/></clipPath>
    <clipPath id="clipCard4"><rect x="960" y="0" width="320" height="720" rx="0"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#06111f"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- Opening title: keep this centered on Slide 1; move the group to translate(1280 0) on Slide 2 for Morph. -->
  <g id="openingTitle" transform="translate(1280 0)" opacity="0.95">
    <text x="640" y="310" width="900" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="800"
          letter-spacing="8" fill="#ffffff" filter="url(#titleGlow)">NEW HORIZONS</text>
    <text x="640" y="378" width="740" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="500"
          letter-spacing="10" fill="#dbeafe">STRATEGIC ROADMAP</text>
  </g>

  <!-- For Slide 1 start state, set this group to transform="translate(-1280 0)"; for Slide 2 end state, use translate(0 0). -->
  <g id="panoramaCards" transform="translate(0 0)">
    <rect x="0" y="0" width="320" height="720" fill="#000000" opacity="0.22" filter="url(#cardShadow)"/>
    <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCard1)"/>
    <rect x="0" y="0" width="320" height="720" fill="url(#cardSheen)"/>
    <rect x="0" y="0" width="320" height="720" fill="url(#bottomFade)"/>
    <text x="44" y="566" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="118" font-weight="800" fill="#ffffff" opacity="0.98">01</text>
    <text x="50" y="628" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="700" letter-spacing="4" fill="#ffffff">VISION</text>
    <text x="44" y="-592" width="230" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="118" font-weight="800"
          fill="#ffffff" opacity="0.12">01</text>
    <text x="50" y="-652" width="230" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
          letter-spacing="4" fill="#ffffff" opacity="0.10">VISION</text>

    <rect x="320" y="0" width="320" height="720" fill="#000000" opacity="0.22" filter="url(#cardShadow)"/>
    <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCard2)"/>
    <rect x="320" y="0" width="320" height="720" fill="url(#cardSheen)"/>
    <rect x="320" y="0" width="320" height="720" fill="url(#bottomFade)"/>
    <text x="364" y="566" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="118" font-weight="800" fill="#ffffff">02</text>
    <text x="370" y="628" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="700" letter-spacing="4" fill="#ffffff">PRODUCT</text>
    <text x="364" y="-592" width="230" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="118" font-weight="800"
          fill="#ffffff" opacity="0.12">02</text>
    <text x="370" y="-652" width="230" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
          letter-spacing="4" fill="#ffffff" opacity="0.10">PRODUCT</text>

    <rect x="640" y="0" width="320" height="720" fill="#000000" opacity="0.22" filter="url(#cardShadow)"/>
    <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCard3)"/>
    <rect x="640" y="0" width="320" height="720" fill="url(#cardSheen)"/>
    <rect x="640" y="0" width="320" height="720" fill="url(#bottomFade)"/>
    <text x="684" y="566" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="118" font-weight="800" fill="#ffffff">03</text>
    <text x="690" y="628" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="700" letter-spacing="4" fill="#ffffff">GROWTH</text>
    <text x="684" y="-592" width="230" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="118" font-weight="800"
          fill="#ffffff" opacity="0.12">03</text>
    <text x="690" y="-652" width="250" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
          letter-spacing="4" fill="#ffffff" opacity="0.10">GROWTH</text>

    <rect x="960" y="0" width="320" height="720" fill="#000000" opacity="0.22" filter="url(#cardShadow)"/>
    <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
           x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCard4)"/>
    <rect x="960" y="0" width="320" height="720" fill="url(#cardSheen)"/>
    <rect x="960" y="0" width="320" height="720" fill="url(#bottomFade)"/>
    <text x="1004" y="566" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="118" font-weight="800" fill="#ffffff">04</text>
    <text x="1010" y="628" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="700" letter-spacing="4" fill="#ffffff">IMPACT</text>
    <text x="1004" y="-592" width="230" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="118" font-weight="800"
          fill="#ffffff" opacity="0.12">04</text>
    <text x="1010" y="-652" width="240" transform="scale(1 -1)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
          letter-spacing="4" fill="#ffffff" opacity="0.10">IMPACT</text>
  </g>

  <path d="M-80 154 C 180 102, 408 108, 672 166 S 1090 220, 1370 134" fill="none" stroke="url(#streak)" stroke-width="2" opacity="0.58"/>
  <path d="M-60 242 C 230 184, 478 202, 720 258 S 1040 320, 1340 246" fill="none" stroke="url(#streak)" stroke-width="1.3" opacity="0.34"/>
  <path d="M-90 430 C 160 380, 412 392, 690 456 S 1100 520, 1390 432" fill="none" stroke="url(#streak)" stroke-width="1.6" opacity="0.25"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; create two static SVG slides and use PowerPoint Morph.
- ❌ Do not use `<mask>` to create text reflections or card fades; use duplicate low-opacity text and gradient overlays instead.
- ❌ Do not apply `clip-path` to rectangles or groups expecting it to translate; only clip the `<image>` slices.
- ❌ Do not use `<pattern>` fills for the panoramic card texture; duplicate the same full-slide image and crop it with card clip paths.
- ❌ Do not put the shadow filter on divider `<line>` elements; use shadowed `<rect>` panels behind each image slice.
- ❌ Do not rely on a single transparent card shape with “slide background fill”; in SVG, use repeated full-size images clipped to each card.

## Composition notes
- Build the slide as two Morph states: Slide 1 has `panoramaCards` at `translate(-1280 0)` and `openingTitle` centered; Slide 2 has `panoramaCards` at `translate(0 0)` and `openingTitle` at `translate(1280 0)`.
- Keep the cards exactly equal width for a premium panoramic split: four cards at `320px` each on a `1280px` canvas.
- Place numbers and labels in the lower third so the image remains cinematic and the audience reads left-to-right like a table of contents.
- Use a landscape, city, architecture, product-environment, or abstract horizon image with strong horizontal continuity; avoid busy portraits because slicing faces across cards looks accidental.