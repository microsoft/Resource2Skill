# SVG Recipe — Modern Diagonal Split Hero

## Visual mechanism
A full-bleed contextual photo is overlaid by a large, solid diagonal polygon that creates a sharp asymmetrical split. The solid side carries high-contrast executive typography, while the exposed photo side provides mood and motion without compromising readability.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph.
- 2× `<rect>` for subtle dark/photo-toning overlays on the image side.
- 1× `<path>` for the large editable diagonal slate panel.
- 1× `<path>` for the soft diagonal edge shadow.
- 1× `<path>` for a thin accent slash parallel to the split.
- 1× `<line>` for the title divider rule.
- 5× `<text>` blocks for kicker, main title, metadata, section label, and small photo caption.
- 2× `<linearGradient>` for photo toning and the slate panel fill.
- 1× `<filter>` with `feOffset + feGaussianBlur + feMerge` for the diagonal edge shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoTint" x1="720" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#101525" stop-opacity="0.05"/>
      <stop offset="0.62" stop-color="#101525" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#101525" stop-opacity="0.42"/>
    </linearGradient>

    <linearGradient id="panelFill" x1="0" y1="0" x2="760" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4D4F6B"/>
      <stop offset="0.58" stop-color="#555673"/>
      <stop offset="1" stop-color="#3F415E"/>
    </linearGradient>

    <filter id="diagonalShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="10" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Layer 1: full-bleed hero image -->
  <image
    href="https://images.example.com/hero-photo-modern-office-glass-architecture-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Layer 1b: keep the photo cinematic and calm -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoTint)"/>
  <rect x="900" y="0" width="380" height="720" fill="#0C1220" opacity="0.10"/>

  <!-- Layer 2: diagonal split panel; top reaches ~65%, bottom reaches ~45% -->
  <path
    d="M 0 0 L 832 0 L 576 720 L 0 720 Z"
    fill="url(#panelFill)"/>

  <!-- soft edge shadow, placed just inside the photo side -->
  <path
    d="M 832 0 L 576 720"
    fill="none"
    stroke="#252942"
    stroke-width="8"
    stroke-opacity="0.28"
    filter="url(#diagonalShadow)"/>

  <!-- premium accent slash parallel to the diagonal -->
  <path
    d="M 852 64 L 630 686"
    fill="none"
    stroke="#E7D7A1"
    stroke-width="3"
    stroke-opacity="0.78"/>

  <!-- Layer 3: typography -->
  <text x="82" y="92" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        letter-spacing="3.5"
        fill="#E7D7A1">
    EXECUTIVE RESEARCH BRIEF
  </text>

  <text x="78" y="178" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        letter-spacing="-1.5"
        fill="#FFFFFF">
    <tspan x="78" dy="0">THE FUTURE</tspan>
    <tspan x="78" dy="66">OF HYBRID</tspan>
    <tspan x="78" dy="66">WORKPLACE</tspan>
    <tspan x="78" dy="66">STRATEGY</tspan>
  </text>

  <line x1="82" y1="478" x2="420" y2="478"
        stroke="#FFFFFF" stroke-width="2.2" stroke-opacity="0.82"/>

  <text x="82" y="520" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#F5F6FA">
    <tspan x="82" dy="0">Aisha Morgan</tspan>
    <tspan x="82" dy="34" fill="#D8DAE8">Global Operations Institute</tspan>
    <tspan x="82" dy="34" fill="#D8DAE8">Transformation Program 2026</tspan>
    <tspan x="82" dy="34" fill="#D8DAE8">Advisor: Dr. Elena Voss</tspan>
  </text>

  <!-- small rotated index, optional but reinforces keynote polish -->
  <text x="36" y="648" width="210"
        transform="rotate(-90 36 648)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700"
        letter-spacing="2.8"
        fill="#FFFFFF"
        opacity="0.42">
    SECTION 01 / STRATEGIC CONTEXT
  </text>

  <!-- restrained caption on photo side -->
  <text x="944" y="642" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600"
        letter-spacing="1.6"
        text-anchor="end"
        fill="#FFFFFF"
        opacity="0.72">
    MODERN OPERATING MODEL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not place text directly over the photo; the technique depends on the solid diagonal panel guaranteeing legibility.
- ❌ Do not use `<mask>` to create the diagonal split; use an editable `<path>` polygon instead.
- ❌ Do not apply `clip-path` to the diagonal panel or other vector shapes; clipping is only reliable on `<image>`.
- ❌ Do not use a vertical 50/50 split unless the diagonal motion is intentionally removed; it will lose the premium editorial feel.
- ❌ Do not omit `width` on `<text>` elements, or PowerPoint text boxes may render with incorrect wrapping.

## Composition notes
- Keep the left panel dominant: roughly 65% of the top edge and 45% of the bottom edge creates a strong diagonal without crowding the photo.
- Place all key typography inside the safe left zone, with generous margins around 75–90 px.
- Use one restrained accent color, such as champagne gold, for the kicker and diagonal slash.
- Choose a hero photo with visual interest on the right side; avoid busy faces or objects behind the diagonal edge.