# SVG Recipe — Cinematic Gradient Fade & Geometric Badge

## Visual mechanism
A full-bleed cinematic photo is darkened with a transparent-to-solid gradient fade, creating a clean lower typography zone without a visible text box. A thick-stroked central hexagon badge anchors the composition like a premium title-card emblem.

## SVG primitives needed
- 1× `<image>` for the full-slide hero landscape/background photo
- 1× `<rect>` with a subtle radial/linear overlay for overall cinematic color grading
- 1× `<rect>` with transparent-to-black `<linearGradient>` for the bottom fade
- 1× `<path>` for the main hexagon badge
- 1× `<path>` for the inner hexagon accent stroke
- 2× `<path>` for simple editable mountain/peak icon details inside the badge
- 1× `<filter id="badgeShadow">` applied to the hexagon badge for depth
- 1× `<filter id="softGlow">` applied to the badge stroke/accent for a faint premium glow
- 5× `<text>` elements for badge label, title, subtitle, and small metadata; all with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bottomFade" x1="0" y1="250" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="42%" stop-color="#000000" stop-opacity="0.38"/>
      <stop offset="72%" stop-color="#000000" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="1"/>
    </linearGradient>

    <linearGradient id="coolGrade" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0A1B2D" stop-opacity="0.22"/>
      <stop offset="48%" stop-color="#111827" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.34"/>
    </linearGradient>

    <radialGradient id="centerLift" cx="50%" cy="38%" r="62%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.11"/>
      <stop offset="62%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.35"/>
    </radialGradient>

    <linearGradient id="badgeFill" x1="480" y1="170" x2="800" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="54%" stop-color="#020617"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>

    <filter id="badgeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <image
    href="https://images.example.com/hero-photo-misty-alpine-mountain-range-sunrise-16x9.jpg"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#coolGrade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerLift)"/>
  <rect x="0" y="250" width="1280" height="470" fill="url(#bottomFade)"/>

  <path
    d="M640 132 L814 232 L814 432 L640 532 L466 432 L466 232 Z"
    fill="#000000"
    opacity="0.32"
    filter="url(#badgeShadow)"/>

  <path
    d="M640 118 L826 226 L826 442 L640 550 L454 442 L454 226 Z"
    fill="url(#badgeFill)"
    stroke="#FFFFFF"
    stroke-width="9"
    stroke-linejoin="round"
    filter="url(#badgeShadow)"/>

  <path
    d="M640 147 L800 240 L800 426 L640 519 L480 426 L480 240 Z"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="2.4"
    stroke-opacity="0.42"
    stroke-linejoin="round"
    filter="url(#softGlow)"/>

  <path
    d="M548 370 L610 296 L650 344 L688 284 L748 370 Z"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="9"
    stroke-linecap="round"
    stroke-linejoin="round"/>

  <path
    d="M588 370 C622 392 672 392 712 370"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="4"
    stroke-opacity="0.65"
    stroke-linecap="round"/>

  <text x="640" y="232" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" letter-spacing="4"
        fill="#FFFFFF" opacity="0.9">ALPINE</text>

  <text x="640" y="455" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" letter-spacing="2"
        fill="#FFFFFF">EXPEDITION</text>

  <text x="640" y="604" width="880" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" letter-spacing="7"
        fill="#FFFFFF">MOUNTAIN</text>

  <text x="640" y="646" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="400"
        fill="#D1D5DB">A cinematic opening slide for journeys, launches, and bold strategic narratives</text>

  <text x="640" y="684" width="540" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" letter-spacing="3"
        fill="#9CA3AF">2026 FIELD REPORT · NORTH RIDGE</text>
</svg>
```

## Avoid in this skill
- ❌ Using a solid black rectangle behind text; it destroys the cinematic fade and feels like a basic caption box.
- ❌ Applying `clip-path` or masking to the gradient rectangle; only use gradients directly on editable shapes.
- ❌ Building the hexagon with `<use>` or symbols; draw it as a standalone editable `<path>`.
- ❌ Placing light text over the brightest part of the photo without the fade overlay.
- ❌ Overcomplicating the badge with tiny details; the badge should remain legible from a distance.

## Composition notes
- Keep the hero image full-bleed; the fade should begin around the lower-middle of the slide and become fully dark by the bottom edge.
- Center the badge slightly above the vertical midpoint so it feels emblematic, while leaving the bottom 15–20% for title typography.
- Use white typography and a restrained gray subtitle palette; the photo provides atmosphere, not competing color.
- The strongest visual focus should be the badge first, the main title second, and the landscape mood third.