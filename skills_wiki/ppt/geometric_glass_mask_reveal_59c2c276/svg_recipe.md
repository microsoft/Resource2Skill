# SVG Recipe — Geometric Glass-Mask Reveal

## Visual mechanism
A soft diagonal glass-gradient veil covers the slide while repeated, clipped copies of the same hero photograph appear only inside rounded diamonds, circles, and vertical capsules, creating the illusion that the image is being revealed through geometric cutouts. Thin offset neon outlines float above the photo-windows, adding architectural depth and motion-ready energy.

## SVG primitives needed
- 1× full-slide `<image>` for a muted photographic base layer.
- 1× full-slide `<rect>` with diagonal `<linearGradient>` for the translucent glass veil.
- 8× clipped `<image>` instances using `<clipPath>` for rounded diamond, circle, and capsule photo reveals.
- 5× `<clipPath>` definitions using rotated `<rect rx>`, `<circle>`, and custom `<path>` geometry.
- 4× outline `<rect>` / `<circle>` shapes with `fill="none"` and bright strokes for floating neon geometry.
- 1× `<filter id="softShadow">` for the central photo-window depth.
- 1× `<filter id="textShadow">` for the main title.
- 2× `<text>` blocks for bold stacked title and faint reflection, each with explicit `width`.
- 2× decorative translucent `<path>` shapes for extra glass facets and visual layering.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="glassVeil" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f7c3a0" stop-opacity="0.76"/>
      <stop offset="0.45" stop-color="#79c8d5" stop-opacity="0.78"/>
      <stop offset="1" stop-color="#a7a9db" stop-opacity="0.74"/>
    </linearGradient>

    <linearGradient id="reflectionFade" x1="0" y1="420" x2="0" y2="575" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="7"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipMainDiamond">
      <rect x="385" y="100" width="500" height="500" rx="54" transform="rotate(45 635 350)"/>
    </clipPath>
    <clipPath id="clipLeftDiamond">
      <rect x="88" y="255" width="315" height="315" rx="42" transform="rotate(45 245.5 412.5)"/>
    </clipPath>
    <clipPath id="clipRightDiamond">
      <rect x="862" y="126" width="335" height="335" rx="42" transform="rotate(45 1029.5 293.5)"/>
    </clipPath>
    <clipPath id="clipCircleTop">
      <circle cx="296" cy="194" r="72"/>
    </clipPath>
    <clipPath id="clipCircleBottom">
      <circle cx="1010" cy="500" r="66"/>
    </clipPath>
    <clipPath id="clipPillA">
      <path d="M166 356 C205 312 264 332 292 386 L352 502 C368 534 357 571 325 587 C294 602 258 590 242 558 L153 417 C139 395 146 376 166 356 Z"/>
    </clipPath>
    <clipPath id="clipPillB">
      <path d="M926 38 C967 12 1017 28 1042 70 L1138 230 C1159 265 1148 310 1113 331 C1077 352 1034 339 1013 304 L895 112 C877 83 891 59 926 38 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#6faab6"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.28"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#glassVeil)"/>

  <path d="M44 667 C246 604 352 651 508 614 C718 563 827 465 1044 526 C1152 556 1226 644 1280 720 L0 720 Z"
        fill="#ffffff" opacity="0.08"/>
  <path d="M1110 0 C1165 90 1215 166 1280 206 L1280 0 Z"
        fill="#ffffff" opacity="0.10"/>

  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipLeftDiamond)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipMainDiamond)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipRightDiamond)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipCircleTop)"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipCircleBottom)"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipPillA)"/>
  <image href="https://images.example.com/hero-photo-wide-aerial-city-skyline-and-waterfront.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipPillB)"/>

  <rect x="405" y="111" width="500" height="500" rx="58"
        transform="rotate(18 655 361)" fill="none" stroke="#f4ff1d" stroke-width="4"/>
  <rect x="392" y="119" width="500" height="500" rx="58"
        transform="rotate(-14 642 369)" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.92"/>
  <rect x="98" y="265" width="298" height="298" rx="38"
        transform="rotate(45 247 414)" fill="none" stroke="#5ad7e9" stroke-width="3" opacity="0.62"/>
  <rect x="875" y="140" width="315" height="315" rx="38"
        transform="rotate(45 1032.5 297.5)" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.44"/>
  <circle cx="296" cy="194" r="74" fill="none" stroke="#62e8f3" stroke-width="2" opacity="0.55"/>

  <text x="465" y="355" width="360" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="800"
        letter-spacing="2" fill="#ffffff" filter="url(#textShadow)">
    <tspan x="640" dy="0">THANK</tspan>
    <tspan x="640" dy="100">YOU</tspan>
  </text>

  <text x="465" y="470" width="360" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="800"
        letter-spacing="2" fill="url(#reflectionFade)" opacity="0.55"
        transform="scale(1 -0.55) translate(0 -1010)">
    <tspan x="640" dy="0">THANK</tspan>
    <tspan x="640" dy="100">YOU</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or boolean subtraction to punch holes in a gradient layer; instead, emulate the reveal by placing clipped photo copies above the veil.
- ❌ Do not apply `clip-path` to gradient rectangles or normal shapes; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Do not use `<use>` to reuse the photo or geometry; repeat the `<image>` elements directly.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the glass shapes; stick to `rotate(...)`, `translate(...)`, and `scale(...)`.
- ❌ Do not put shadows on `<line>` elements; use stroked `<rect>`, `<circle>`, or `<path>` outlines if glow/shadow is needed.

## Composition notes
- Keep the largest rounded diamond centered and occupying roughly 55–65% of slide height; this is the primary reveal and the safest place for the headline.
- Use smaller circles, capsules, and side diamonds as satellites along a diagonal axis so the layout feels engineered rather than random.
- Let the gradient veil own the negative space; the clipped photo-windows should feel like cutouts through frosted glass, not a full collage.
- Neon outlines should be slightly offset from the clipped shapes and cross over the title area to create premium depth and motion-readiness.