# SVG Recipe — Four-Quadrant Image Collage

## Visual mechanism
A full-bleed 2×2 grid of context images creates an immersive, multi-faceted backdrop, while a dark cinematic center band protects the message from visual noise. Thin accent rules and high-contrast centered typography turn the collage into a premium title or section opener.

## SVG primitives needed
- 4× `<image>` for the edge-to-edge quadrant photos
- 4× `<clipPath>` with `<rect>` for exact quadrant cropping boundaries
- 1× full-slide `<rect>` with vertical gradient for subtle global darkening
- 1× central `<rect>` for the semi-transparent text band
- 2× feather `<rect>` overlays with gradients to soften the band edges
- 2× `<line>` for thin accent rules above and below the band
- 1× `<filter id="softShadow">` applied to the band for depth
- 1× `<filter id="textGlow">` applied to headline text for readability
- 3× `<text>` elements for eyebrow, main title, and subtitle / metadata
- Optional 4× translucent `<rect>` labels or color washes if quadrant meaning needs to be hinted

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="quadTL">
      <rect x="0" y="0" width="640" height="360"/>
    </clipPath>
    <clipPath id="quadTR">
      <rect x="640" y="0" width="640" height="360"/>
    </clipPath>
    <clipPath id="quadBL">
      <rect x="0" y="360" width="640" height="360"/>
    </clipPath>
    <clipPath id="quadBR">
      <rect x="640" y="360" width="640" height="360"/>
    </clipPath>

    <linearGradient id="globalDim" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#06101C" stop-opacity="0.20"/>
      <stop offset="45%" stop-color="#06101C" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#06101C" stop-opacity="0.35"/>
    </linearGradient>

    <linearGradient id="fadeDown" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#07101C" stop-opacity="0"/>
      <stop offset="100%" stop-color="#07101C" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="fadeUp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#07101C" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#07101C" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-30%" width="120%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-40%" width="120%" height="180%">
      <feGaussianBlur stdDeviation="2.5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image x="0" y="0" width="640" height="360"
         href="https://picsum.photos/seed/executive-team-collaboration/1280/720"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#quadTL)"/>
  <image x="640" y="0" width="640" height="360"
         href="https://picsum.photos/seed/digital-product-dashboard/1280/720"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#quadTR)"/>
  <image x="0" y="360" width="640" height="360"
         href="https://picsum.photos/seed/customer-retail-experience/1280/720"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#quadBL)"/>
  <image x="640" y="360" width="640" height="360"
         href="https://picsum.photos/seed/urban-growth-night-market/1280/720"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#quadBR)"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#globalDim)"/>

  <line x1="640" y1="0" x2="640" y2="720" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="0" y1="360" x2="1280" y2="360" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>

  <rect x="0" y="214" width="1280" height="72" fill="url(#fadeDown)"/>
  <rect x="0" y="286" width="1280" height="168" fill="#07101C" fill-opacity="0.84" filter="url(#softShadow)"/>
  <rect x="0" y="454" width="1280" height="72" fill="url(#fadeUp)"/>

  <line x1="120" y1="286" x2="1160" y2="286" stroke="#FFCC33" stroke-width="2" stroke-opacity="0.85"/>
  <line x1="120" y1="454" x2="1160" y2="454" stroke="#FFCC33" stroke-width="2" stroke-opacity="0.55"/>

  <text x="640" y="326" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="4" fill="#FFCC33">
    FOUR SCENARIOS · ONE STRATEGIC VIEW
  </text>

  <text x="640" y="386" width="920" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        fill="#FFFFFF" filter="url(#textGlow)">
    <tspan x="640" dy="0">April Marketing Proposal</tspan>
  </text>

  <text x="640" y="427" width="860" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="500"
        fill="#DDE7F3" opacity="0.94">
    <tspan>Customer insight, product value, channel activation, and growth outcomes</tspan>
  </text>

  <text x="42" y="52" width="230"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.72">
    PEOPLE
  </text>
  <text x="1075" y="52" width="170"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.72">
    PRODUCT
  </text>
  <text x="42" y="690" width="220"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.72">
    MARKET
  </text>
  <text x="1090" y="690" width="160"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.72">
    GROWTH
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using four small image cards with margins; the technique depends on full-bleed immersion.
- ❌ Placing title text directly on the raw photos without a dark band or gradient protection.
- ❌ Applying `clip-path` to overlay rectangles or text; clipping is reliable here only on `<image>`.
- ❌ Using `<mask>` for the cinematic fade; use stacked gradient `<rect>` overlays instead.
- ❌ Relying on a single busy image stretched across the slide; the point is multi-scenario contrast.

## Composition notes
- Keep the 2×2 image intersection exactly at slide center; it reinforces the “four perspectives” concept.
- Reserve the middle 30–40% of slide height for the overlay band and message hierarchy.
- Use one bright accent color, such as gold or cyan, for rules and eyebrow text; keep the title white.
- Choose four images with different subjects but compatible color temperature so the collage feels curated, not random.