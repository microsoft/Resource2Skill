# SVG Recipe — Gallery Moodboard

## Visual mechanism
A premium editorial moodboard built from one oversized hero image and four smaller supporting image tiles, all held in a disciplined grid with generous gutters. Subtle rounded crops, soft shadows, warm background tinting, and restrained typography make the gallery feel curated rather than like a raw image dump.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm off-white background
- 1× `<path>` for a large low-contrast decorative color wash behind the gallery
- 5× `<clipPath>` using rounded `<rect>` shapes for editable rounded image crops
- 5× `<image>` for the hero image and four supporting moodboard images
- 5× shadow-card `<rect>` elements behind images to create depth
- 5× subtle overlay `<rect>` elements on top of image crops for editorial tinting / caption readability
- 1× `<linearGradient>` for the background wash
- 1× `<linearGradient>` for image-top-to-bottom overlay shading
- 1× `<filter id="softShadow">` applied to image backing cards
- 1× `<filter id="ambientBlur">` applied to the decorative background path
- 6× `<text>` elements for headline, eyebrow, caption, and small tile labels; every text element includes explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="washGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EED9C4"/>
      <stop offset="55%" stop-color="#D9E2D0"/>
      <stop offset="100%" stop-color="#F6EFE7"/>
    </linearGradient>

    <linearGradient id="imageShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#111111" stop-opacity="0"/>
      <stop offset="62%" stop-color="#111111" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#111111" stop-opacity="0.34"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>

    <clipPath id="clipHero">
      <rect x="70" y="178" width="680" height="450" rx="34" ry="34"/>
    </clipPath>
    <clipPath id="clipGrid1">
      <rect x="790" y="178" width="190" height="190" rx="26" ry="26"/>
    </clipPath>
    <clipPath id="clipGrid2">
      <rect x="1010" y="178" width="190" height="190" rx="26" ry="26"/>
    </clipPath>
    <clipPath id="clipGrid3">
      <rect x="790" y="398" width="190" height="190" rx="26" ry="26"/>
    </clipPath>
    <clipPath id="clipGrid4">
      <rect x="1010" y="398" width="190" height="190" rx="26" ry="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F1EA"/>

  <path d="M804,77 C948,22 1122,58 1217,170 C1330,303 1262,514 1092,625 C950,718 731,695 621,576 C514,462 548,287 655,184 C696,145 742,101 804,77 Z"
        fill="url(#washGrad)" opacity="0.55" filter="url(#ambientBlur)"/>

  <text x="70" y="72" width="680"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3"
        fill="#8B6F58">VISUAL DIRECTION</text>

  <text x="70" y="132" width="850"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="650"
        fill="#1F1B18">
    <tspan x="70" dy="0">Warm minimalism for a</tspan>
    <tspan fill="#A86E4E"> tactile retail launch</tspan>
  </text>

  <rect x="70" y="178" width="680" height="450" rx="34" ry="34"
        fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <image x="70" y="178" width="680" height="450"
         href="https://images.example.com/moodboard/hero-warm-minimal-interior-with-natural-light.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipHero)"/>
  <rect x="70" y="178" width="680" height="450" rx="34" ry="34"
        fill="url(#imageShade)" opacity="0.78"/>

  <text x="105" y="565" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2.2"
        fill="#FFFFFF">01 / HERO ATMOSPHERE</text>
  <text x="105" y="594" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600"
        fill="#FFFFFF">Sun-washed material palette, quiet geometry, crafted restraint.</text>

  <rect x="790" y="178" width="190" height="190" rx="26" ry="26"
        fill="#FFFFFF" opacity="0.95" filter="url(#softShadow)"/>
  <image x="790" y="178" width="190" height="190"
         href="https://images.example.com/moodboard/closeup-linen-texture-stone-neutral.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipGrid1)"/>
  <rect x="790" y="178" width="190" height="190" rx="26" ry="26"
        fill="url(#imageShade)" opacity="0.48"/>

  <rect x="1010" y="178" width="190" height="190" rx="26" ry="26"
        fill="#FFFFFF" opacity="0.95" filter="url(#softShadow)"/>
  <image x="1010" y="178" width="190" height="190"
         href="https://images.example.com/moodboard/minimal-product-still-life-ceramic-wood.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipGrid2)"/>
  <rect x="1010" y="178" width="190" height="190" rx="26" ry="26"
        fill="url(#imageShade)" opacity="0.44"/>

  <rect x="790" y="398" width="190" height="190" rx="26" ry="26"
        fill="#FFFFFF" opacity="0.95" filter="url(#softShadow)"/>
  <image x="790" y="398" width="190" height="190"
         href="https://images.example.com/moodboard/architectural-arch-shadow-warm-plaster.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipGrid3)"/>
  <rect x="790" y="398" width="190" height="190" rx="26" ry="26"
        fill="url(#imageShade)" opacity="0.5"/>

  <rect x="1010" y="398" width="190" height="190" rx="26" ry="26"
        fill="#FFFFFF" opacity="0.95" filter="url(#softShadow)"/>
  <image x="1010" y="398" width="190" height="190"
         href="https://images.example.com/moodboard/botanical-branch-against-soft-beige-wall.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipGrid4)"/>
  <rect x="1010" y="398" width="190" height="190" rx="26" ry="26"
        fill="url(#imageShade)" opacity="0.45"/>

  <text x="790" y="635" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500"
        fill="#5C5148">A structured 1+4 gallery for moodboards, portfolios, campaign worlds, and visual territories.</text>

  <text x="790" y="350" width="160"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.8"
        fill="#FFFFFF">TEXTURE</text>
  <text x="1010" y="350" width="160"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.8"
        fill="#FFFFFF">OBJECTS</text>
  <text x="790" y="570" width="160"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.8"
        fill="#FFFFFF">SPACE</text>
  <text x="1010" y="570" width="160"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.8"
        fill="#FFFFFF">NATURE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to crop or fade the images; use `<clipPath>` applied directly to each `<image>` instead.
- ❌ Do not apply `clip-path` to a `<g>` or `<rect>` expecting it to crop the full tile; only image clipping is reliable here.
- ❌ Do not build the moodboard from many tiny equal rectangles; the technique depends on a dominant hero image plus four supporting images.
- ❌ Do not rely on `<pattern>` fills for photo texture; place actual `<image>` elements so the result remains editable and visually rich.
- ❌ Do not place text without a `width` attribute; captions and labels will render unpredictably in PowerPoint.

## Composition notes
- Keep the hero image around 50–55% of slide width and 60% of slide height; it should clearly dominate the composition.
- Use consistent gutters between all images, ideally 28–36 px, so the gallery reads as one curated system.
- Reserve the top-left band for headline typography and the lower-right band for a short explanatory caption.
- Let supporting grid images vary in subject matter but share a palette; the layout looks strongest when color rhythm is cohesive.