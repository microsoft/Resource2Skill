# SVG Recipe — Nine-Square Matrix Reveal

## Visual mechanism
A single square hero photograph is repeated nine times, each instance clipped to one cell of a 3×3 matrix so the image reads as one continuous scene broken by crisp white gutters. The result feels like an editorial image reveal: structured, premium, and ideal for pairing with strong cover-slide typography.

## SVG primitives needed
- 1× `<rect>` full-slide background with subtle gradient fill
- 1× `<rect>` behind the matrix for soft shadow depth
- 9× `<clipPath>` using `<rect>` to define each square image cell
- 9× `<image>` instances of the same square photo, each clipped to a different cell
- 4× `<rect>` overlays for thick white vertical/horizontal grid gutters
- 1× `<path>` decorative organic accent blob behind the text
- 1× `<circle>` small accent marker
- 1× `<line>` fine editorial divider
- 4× `<text>` blocks for eyebrow, title, subtitle, and caption; every text element has explicit `width`
- 1× `<linearGradient>` for background
- 1× `<radialGradient>` for the accent blob
- 1× `<filter id="softShadow">` applied to the matrix backing card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="58%" stop-color="#EEF4F7"/>
      <stop offset="100%" stop-color="#E8EEF2"/>
    </linearGradient>

    <radialGradient id="aquaGlow" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#35D3E8" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#35D3E8" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Matrix geometry: grid origin 690,105; cell 156; gap 16; total visual size 500 -->
    <clipPath id="c00"><rect x="690" y="105" width="156" height="156"/></clipPath>
    <clipPath id="c01"><rect x="862" y="105" width="156" height="156"/></clipPath>
    <clipPath id="c02"><rect x="1034" y="105" width="156" height="156"/></clipPath>
    <clipPath id="c10"><rect x="690" y="277" width="156" height="156"/></clipPath>
    <clipPath id="c11"><rect x="862" y="277" width="156" height="156"/></clipPath>
    <clipPath id="c12"><rect x="1034" y="277" width="156" height="156"/></clipPath>
    <clipPath id="c20"><rect x="690" y="449" width="156" height="156"/></clipPath>
    <clipPath id="c21"><rect x="862" y="449" width="156" height="156"/></clipPath>
    <clipPath id="c22"><rect x="1034" y="449" width="156" height="156"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M96,507 C132,421 215,407 292,434 C374,462 410,542 370,602 C326,668 224,681 152,646 C91,616 69,573 96,507 Z"
        fill="url(#aquaGlow)"/>
  <circle cx="562" cy="142" r="7" fill="#14B8C8"/>

  <text x="96" y="122" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700"
        letter-spacing="3" fill="#14A6B8">IMAGE LAYOUT / EDITORIAL REVEAL</text>

  <text x="92" y="210" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800"
        fill="#111827">
    <tspan x="92" dy="0">NINE-SQUARE</tspan>
    <tspan x="92" dy="74">MATRIX</tspan>
  </text>

  <line x1="96" y1="338" x2="236" y2="338" stroke="#111827" stroke-width="3"/>

  <text x="96" y="386" width="455" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="400"
        fill="#3B4552">
    <tspan x="96" dy="0">Turn one photograph into a structured</tspan>
    <tspan x="96" dy="34">visual system with crisp editorial rhythm,</tspan>
    <tspan x="96" dy="34">perfect for covers, lookbooks, and intros.</tspan>
  </text>

  <text x="96" y="586" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600"
        fill="#667085">
    <tspan x="96" dy="0">01</tspan>
    <tspan dx="18" fill="#14A6B8">REVEAL SEQUENCE</tspan>
    <tspan x="96" dy="24">Animate cells top-left to bottom-right for a cascading build.</tspan>
  </text>

  <rect x="660" y="75" width="560" height="560" rx="28" fill="#FFFFFF" opacity="0.88" filter="url(#softShadow)"/>

  <!-- Same square image repeated and clipped, creating true nine-piece editable crops -->
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c00)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c01)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c02)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c10)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c11)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c12)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c20)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c21)"/>
  <image href="https://images.example.com/editorial-aerial-nature-square-1200.jpg"
         x="690" y="105" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#c22)"/>

  <!-- White gutters make the split deliberate and premium -->
  <rect x="846" y="105" width="16" height="500" fill="#FFFFFF"/>
  <rect x="1018" y="105" width="16" height="500" fill="#FFFFFF"/>
  <rect x="690" y="261" width="500" height="16" fill="#FFFFFF"/>
  <rect x="690" y="433" width="500" height="16" fill="#FFFFFF"/>

  <rect x="690" y="105" width="500" height="500" fill="none" stroke="#FFFFFF" stroke-width="10"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use href="#image">` to duplicate the photo; `<use>` hard-fails translation. Repeat the `<image>` element nine times instead.
- ❌ Do not apply `clip-path` to `<rect>` or `<g>` for this effect; clipping is reliable on `<image>` only.
- ❌ Do not use `<mask>` to create the gutters; use explicit white `<rect>` gutter overlays or physical spacing between clipped images.
- ❌ Do not use `marker-end` paths for reveal arrows; if you add callouts, use plain `<line>` elements or separate vector arrowhead paths.
- ❌ Do not omit `width` on any `<text>` element; PowerPoint rendering will not auto-fit predictably.

## Composition notes
- Keep the matrix close to a true square and allocate roughly 45–50% of slide width; it should feel like the visual hero, not a thumbnail.
- Pair the heavy grid with generous negative space and a bold left-side headline for an executive keynote balance.
- Use pure white gutters on light or dark images; the grid must read as intentional structure, not accidental spacing.
- For manual PowerPoint animation, reveal the nine clipped images sequentially from top-left to bottom-right with short fade or zoom delays.