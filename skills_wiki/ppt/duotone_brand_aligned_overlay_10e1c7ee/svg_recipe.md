# SVG Recipe — Duotone Brand-Aligned Overlay

## Visual mechanism
A pre-desaturated full-bleed photograph is unified by a semi-transparent brand-color overlay, creating a controlled pseudo-duotone image field. High-contrast white typography is anchored over the quieted photo, with oversized metrics or headlines becoming the dominant focal point.

## SVG primitives needed
- 1× `<image>` for the full-bleed grayscale or pre-desaturated photographic background
- 2× full-canvas `<rect>` overlays for brand tint and directional darkening
- 1× `<linearGradient>` for a left-to-right readability wash
- 1× `<radialGradient>` for edge vignette and focal contrast control
- 2–3× decorative `<path>` shapes for subtle editorial energy within the brand overlay
- 1× `<filter id="textShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for premium text separation
- 4–6× `<text>` elements with explicit `width` attributes for KPI, supporting copy, label, and footer note
- Optional thin `<line>` elements for small editorial rules or separators

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftReadabilityWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#102232" stop-opacity="0.82"/>
      <stop offset="42%" stop-color="#1E3A50" stop-opacity="0.56"/>
      <stop offset="75%" stop-color="#2C4C68" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#2C4C68" stop-opacity="0.04"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="34%" cy="48%" r="82%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="58%" stop-color="#0E2435" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#07131E" stop-opacity="0.45"/>
    </radialGradient>

    <linearGradient id="accentSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#79C7D3" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#2C4C68" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0A1824" stop-opacity="0"/>
    </linearGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Layer 1: pre-desaturated / grayscale photograph -->
  <image
    href="https://images.example.com/grayscale-recycling-facility-conveyor-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Layer 2: brand tint overlay -->
  <rect x="0" y="0" width="1280" height="720" fill="#2C4C68" opacity="0.68"/>

  <!-- Layer 3: contrast shaping overlays -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftReadabilityWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <!-- Subtle editorial color movement, still editable as vector paths -->
  <path
    d="M790,-40 C940,20 1020,130 1280,92 L1280,0 L790,0 Z"
    fill="url(#accentSheen)" opacity="0.72"/>

  <path
    d="M1010,720 C930,620 940,510 1080,438 C1160,397 1228,398 1280,414 L1280,720 Z"
    fill="#79C7D3" opacity="0.11"/>

  <path
    d="M-30,570 C130,520 225,555 322,650 C358,686 395,704 448,720 L-30,720 Z"
    fill="#06131E" opacity="0.24"/>

  <!-- Small editorial rule and label -->
  <line x1="124" y1="118" x2="214" y2="118" stroke="#FFFFFF" stroke-opacity="0.82" stroke-width="3"/>

  <text x="124" y="154" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        letter-spacing="3"
        fill="#D8EEF2" opacity="0.96">
    CIRCULARITY SNAPSHOT
  </text>

  <!-- Main content block -->
  <g filter="url(#textShadow)">
    <text x="118" y="263" width="420"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="42" font-weight="400"
          fill="#FFFFFF">
      Only
    </text>

    <text x="112" y="430" width="520"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="190" font-weight="800"
          letter-spacing="-8"
          fill="#FFFFFF">
      9%
    </text>

    <text x="124" y="493" width="520"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="42" font-weight="400"
          fill="#FFFFFF">
      gets recycled
    </text>
  </g>

  <!-- Supporting narrative -->
  <text x="124" y="565" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#D8EEF2" opacity="0.92">
    <tspan x="124" dy="0">A noisy stock image becomes an ownable</tspan>
    <tspan x="124" dy="32">brand moment once color is disciplined.</tspan>
  </text>

  <!-- Right-side quiet caption to balance the frame -->
  <rect x="918" y="562" width="238" height="1.5" fill="#FFFFFF" opacity="0.42"/>
  <text x="918" y="598" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500"
        letter-spacing="1.4"
        fill="#FFFFFF" opacity="0.72">
    SOURCE: GLOBAL MATERIAL FLOWS
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG `feColorMatrix` or CSS filters to grayscale the photo; use a pre-desaturated image asset for dependable PowerPoint output.
- ❌ Do not place the tint inside a `<mask>`; use editable semi-transparent `<rect>` overlays instead.
- ❌ Do not leave text without a `width` attribute; PowerPoint text boxes will not size predictably.
- ❌ Do not use a colorful, untreated stock photo under white text; the technique depends on suppressing the original palette.
- ❌ Avoid evenly transparent overlays only; add directional washes or vignettes so the text zone has stronger contrast than the decorative image zone.

## Composition notes
- Anchor the main text block around 9–12% from the left edge; this creates an editorial title-slide feel and leaves the photo visible on the right.
- Keep the overlay darkest behind the typography and lighter toward the image focal area so the slide still feels photographic.
- Use white for the primary metric/headline, then a pale tint of the brand color for labels and supporting copy.
- Let the KPI or title occupy roughly one-third of the slide height; the photo provides atmosphere, not the main hierarchy.