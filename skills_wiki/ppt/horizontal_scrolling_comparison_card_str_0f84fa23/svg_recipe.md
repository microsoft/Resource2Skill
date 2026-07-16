# SVG Recipe — Horizontal Scrolling Comparison Card Strip

## Visual mechanism
A wide panoramic strip of uniform comparison cards extends beyond the right edge of the 16:9 slide, so the visible canvas behaves like a viewport over a much longer ranking sequence. Each card repeats the same stacked structure — rank, entity name, visual anchor, and description — enabling fast row-by-row comparison as the strip is panned in PowerPoint.

## SVG primitives needed
- 1× `<rect>` for the dark slide background
- 1× `<linearGradient>` for subtle background depth
- 1× `<filter id="cardShadow">` applied to selected header/card blocks for premium separation
- 6× card groups composed of stacked `<rect>` blocks for rank, title, image bay, and description zones
- 6× `<image>` elements for flag/product/photo anchors
- 6× `<clipPath>` definitions using rounded `<rect>` crops applied only to `<image>`
- 24× `<text>` elements for ranks, names, descriptions, title, and viewport cue; every text element includes explicit `width`
- 7× `<line>` elements for vertical card separators and scroll guide rail
- 1× `<path>` for a custom arrowhead indicating horizontal motion
- 2× overlay `<rect>` elements with gradient fills for left/right viewport fade edges

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101114"/>
      <stop offset="55%" stop-color="#1b1b1f"/>
      <stop offset="100%" stop-color="#08090b"/>
    </linearGradient>
    <linearGradient id="rightFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#08090b" stop-opacity="0"/>
      <stop offset="100%" stop-color="#08090b" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="leftFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#08090b" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#08090b" stop-opacity="0"/>
    </linearGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photo01"><rect x="72" y="264" width="236" height="158" rx="12"/></clipPath>
    <clipPath id="photo02"><rect x="372" y="264" width="236" height="158" rx="12"/></clipPath>
    <clipPath id="photo03"><rect x="672" y="264" width="236" height="158" rx="12"/></clipPath>
    <clipPath id="photo04"><rect x="972" y="264" width="236" height="158" rx="12"/></clipPath>
    <clipPath id="photo05"><rect x="1272" y="264" width="236" height="158" rx="12"/></clipPath>
    <clipPath id="photo06"><rect x="1572" y="264" width="236" height="158" rx="12"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDepth)"/>

  <text x="42" y="42" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#f2f2f2">
    Global Market Attractiveness Index
  </text>
  <text x="930" y="43" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#a8a8a8" text-anchor="end">
    panoramic strip continues
  </text>
  <line x1="958" y1="38" x2="1188" y2="38" stroke="#c9c9c9" stroke-width="2" stroke-dasharray="8 8"/>
  <path d="M1204 38 L1186 28 L1186 48 Z" fill="#c9c9c9"/>

  <!-- Card 01 -->
  <rect x="40" y="70" width="300" height="88" fill="#b80000" filter="url(#cardShadow)"/>
  <text x="190" y="131" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle">#10</text>
  <rect x="40" y="158" width="300" height="70" fill="#e4e4e4"/>
  <text x="190" y="203" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111111" text-anchor="middle">Brazil</text>
  <rect x="40" y="228" width="300" height="224" fill="#f3f3f3"/>
  <image href="https://images.example.com/flags/brazil-flag-4x3.jpg" x="72" y="264" width="236" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo01)"/>
  <rect x="72" y="264" width="236" height="158" rx="12" fill="none" stroke="#cccccc" stroke-width="2"/>
  <rect x="40" y="452" width="300" height="184" fill="#191919"/>
  <text x="64" y="493" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff">
    <tspan x="64" dy="0">Large domestic demand,</tspan>
    <tspan x="64" dy="26">young consumers, and</tspan>
    <tspan x="64" dy="26">strong digital adoption.</tspan>
  </text>
  <line x1="340" y1="70" x2="340" y2="636" stroke="#3c3c3c" stroke-width="2"/>

  <!-- Card 02 -->
  <rect x="340" y="70" width="300" height="88" fill="#c00000" filter="url(#cardShadow)"/>
  <text x="490" y="131" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle">#9</text>
  <rect x="340" y="158" width="300" height="70" fill="#dedede"/>
  <text x="490" y="203" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111111" text-anchor="middle">Thailand</text>
  <rect x="340" y="228" width="300" height="224" fill="#f3f3f3"/>
  <image href="https://images.example.com/flags/thailand-flag-4x3.jpg" x="372" y="264" width="236" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo02)"/>
  <rect x="372" y="264" width="236" height="158" rx="12" fill="none" stroke="#cccccc" stroke-width="2"/>
  <rect x="340" y="452" width="300" height="184" fill="#191919"/>
  <text x="364" y="493" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff">
    <tspan x="364" dy="0">Tourism recovery boosts</tspan>
    <tspan x="364" dy="26">retail, mobility, and</tspan>
    <tspan x="364" dy="26">consumer services.</tspan>
  </text>
  <line x1="640" y1="70" x2="640" y2="636" stroke="#3c3c3c" stroke-width="2"/>

  <!-- Card 03 -->
  <rect x="640" y="70" width="300" height="88" fill="#c60000" filter="url(#cardShadow)"/>
  <text x="790" y="131" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle">#8</text>
  <rect x="640" y="158" width="300" height="70" fill="#e4e4e4"/>
  <text x="790" y="203" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111111" text-anchor="middle">Japan</text>
  <rect x="640" y="228" width="300" height="224" fill="#f3f3f3"/>
  <image href="https://images.example.com/flags/japan-flag-4x3.jpg" x="672" y="264" width="236" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo03)"/>
  <rect x="672" y="264" width="236" height="158" rx="12" fill="none" stroke="#cccccc" stroke-width="2"/>
  <rect x="640" y="452" width="300" height="184" fill="#191919"/>
  <text x="664" y="493" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff">
    <tspan x="664" dy="0">Premium customers, high</tspan>
    <tspan x="664" dy="26">quality expectations, and</tspan>
    <tspan x="664" dy="26">stable purchasing power.</tspan>
  </text>
  <line x1="940" y1="70" x2="940" y2="636" stroke="#3c3c3c" stroke-width="2"/>

  <!-- Card 04 -->
  <rect x="940" y="70" width="300" height="88" fill="#b80000" filter="url(#cardShadow)"/>
  <text x="1090" y="131" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle">#7</text>
  <rect x="940" y="158" width="300" height="70" fill="#dedede"/>
  <text x="1090" y="203" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111111" text-anchor="middle">Netherlands</text>
  <rect x="940" y="228" width="300" height="224" fill="#f3f3f3"/>
  <image href="https://images.example.com/flags/netherlands-flag-4x3.jpg" x="972" y="264" width="236" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo04)"/>
  <rect x="972" y="264" width="236" height="158" rx="12" fill="none" stroke="#cccccc" stroke-width="2"/>
  <rect x="940" y="452" width="300" height="184" fill="#191919"/>
  <text x="964" y="493" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff">
    <tspan x="964" dy="0">Compact geography, high</tspan>
    <tspan x="964" dy="26">logistics efficiency, and</tspan>
    <tspan x="964" dy="26">excellent test-market fit.</tspan>
  </text>
  <line x1="1240" y1="70" x2="1240" y2="636" stroke="#3c3c3c" stroke-width="2"/>

  <!-- Off-canvas cards that create the scrollable panorama -->
  <rect x="1240" y="70" width="300" height="88" fill="#c00000"/>
  <text x="1390" y="131" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle">#6</text>
  <rect x="1240" y="158" width="300" height="70" fill="#e4e4e4"/>
  <text x="1390" y="203" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111111" text-anchor="middle">Korea</text>
  <rect x="1240" y="228" width="300" height="224" fill="#f3f3f3"/>
  <image href="https://images.example.com/flags/south-korea-flag-4x3.jpg" x="1272" y="264" width="236" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo05)"/>
  <rect x="1240" y="452" width="300" height="184" fill="#191919"/>
  <text x="1264" y="493" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff"><tspan x="1264" dy="0">Trend-sensitive buyers and</tspan><tspan x="1264" dy="26">world-class digital culture.</tspan></text>

  <rect x="1540" y="70" width="300" height="88" fill="#b80000"/>
  <text x="1690" y="131" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle">#5</text>
  <rect x="1540" y="158" width="300" height="70" fill="#dedede"/>
  <text x="1690" y="203" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#111111" text-anchor="middle">Mexico</text>
  <rect x="1540" y="228" width="300" height="224" fill="#f3f3f3"/>
  <image href="https://images.example.com/flags/mexico-flag-4x3.jpg" x="1572" y="264" width="236" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo06)"/>
  <rect x="1540" y="452" width="300" height="184" fill="#191919"/>
  <text x="1564" y="493" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff"><tspan x="1564" dy="0">Nearshore growth, scale,</tspan><tspan x="1564" dy="26">and youthful urban demand.</tspan></text>

  <rect x="0" y="54" width="56" height="606" fill="url(#leftFade)"/>
  <rect x="1110" y="54" width="170" height="606" fill="url(#rightFade)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG animation to create the scroll; build the full off-canvas strip, then animate/pan the grouped shapes in PowerPoint if needed.
- ❌ Do not use `<mask>` or clip non-image card shapes; only apply `clip-path` to `<image>` elements for the visual anchor crop.
- ❌ Do not use `<use>` to duplicate cards, even though the layout is repetitive; explicitly draw each card so every element remains editable.
- ❌ Do not put `marker-end` on paths for arrows; use a normal `<line>` plus a small triangular `<path>` arrowhead.
- ❌ Do not omit `width` on text elements; comparison cards need predictable PowerPoint text wrapping.

## Composition notes
- Keep each card the same width and vertical structure; the comparison effect depends on exact row alignment across ranks, names, images, and descriptions.
- Let the strip extend far beyond `x=1280`; the visible slide is only a viewport, and the off-canvas cards are what enable a cinematic horizontal pan.
- Use red rank headers as the dominant rhythm, pale grey title headers as neutral labels, and dark description panels to anchor the bottom.
- Add a right-edge fade or partial next card to imply continuation without needing visible scroll controls.