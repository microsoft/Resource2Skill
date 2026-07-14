# SVG Recipe — Immersive Data Slice

## Visual mechanism
A single data percentage is turned into a storytelling hero visual by placing a bold pie-slice shape over a large circular photo crop. The photo remains visible through the “uncovered” portion of the circle, making the statistic feel connected to a real-world context rather than like a standalone chart.

## SVG primitives needed
- 1× `<rect>` for the full-slide bright background.
- 1× `<radialGradient>` for subtle atmospheric background depth.
- 1× `<circle>` behind the image for editable soft shadow support.
- 1× `<image>` clipped into a large circle for the immersive thematic photo.
- 1× `<clipPath>` with `<circle>` to crop the image.
- 1× `<path>` for the dark data slice representing the percentage.
- 1× `<path>` for a thin accent arc around the image/data circle.
- 2× `<filter>` definitions: one soft shadow for the circle/slice and one glow accent.
- Several `<text>` elements with explicit `width` attributes for the percentage, label, headline, and footnote.
- 1× `<line>` for a simple editorial callout divider.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="30%" cy="46%" r="75%">
      <stop offset="0%" stop-color="#7FFAF3"/>
      <stop offset="48%" stop-color="#4FEBE3"/>
      <stop offset="100%" stop-color="#31D7D2"/>
    </radialGradient>

    <linearGradient id="sliceSheen" x1="160" y1="150" x2="420" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#062B62"/>
      <stop offset="70%" stop-color="#011F4B"/>
      <stop offset="100%" stop-color="#001632"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="orangeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoCircle">
      <circle cx="370" cy="360" r="250"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <circle cx="370" cy="360" r="252" fill="#0B315E" opacity="0.28" filter="url(#softShadow)"/>

  <image
    href="https://images.example.com/hero-photo-campfire-night-people-warm-storytelling.jpg"
    x="120" y="110" width="500" height="500"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoCircle)"/>

  <circle cx="370" cy="360" r="250" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.75"/>

  <path
    d="M 370 360 L 284.5 594.9 A 250 250 0 0 1 230.3 152.8 Z"
    fill="url(#sliceSheen)"
    filter="url(#softShadow)"/>

  <path
    d="M 614 304 A 250 250 0 0 1 560 522"
    fill="none"
    stroke="#FFA500"
    stroke-width="10"
    stroke-linecap="round"
    filter="url(#orangeGlow)"/>

  <text x="226" y="365" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="800"
        fill="#FFFFFF" letter-spacing="-4">
    35<tspan font-size="54" baseline-shift="super">%</tspan>
  </text>

  <text x="236" y="423" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700"
        fill="#A9FFF9" letter-spacing="2">
    DATA SLICE
  </text>

  <line x1="690" y1="204" x2="750" y2="204" stroke="#FFA500" stroke-width="7" stroke-linecap="round"/>

  <text x="690" y="185" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700"
        fill="#011F4B" letter-spacing="3">
    EXECUTIVE INSIGHT
  </text>

  <text x="690" y="275" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        fill="#011F4B" letter-spacing="-1">
    OF CAMPERS
  </text>

  <text x="690" y="345" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        fill="#011F4B" letter-spacing="-1">
    DON’T LIKE
  </text>

  <text x="690" y="418" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66" font-weight="900"
        fill="#FFA500" letter-spacing="-2">
    S’MORES*
  </text>

  <text x="694" y="485" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="500"
        fill="#06315F">
    A playful hero statistic paired with a contextual image makes the number feel memorable, emotional, and presentation-ready.
  </text>

  <text x="696" y="580" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600"
        fill="#06435C" opacity="0.8">
    *Illustrative sample data for visual technique demonstration.
  </text>

  <circle cx="1115" cy="120" r="44" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="1165" cy="168" r="16" fill="#FFA500" opacity="0.85"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to reveal the photo through the pie; use an `<image>` clipped by a circular `<clipPath>` instead.
- ❌ Do not apply `clip-path` to the pie slice or other non-image shapes; keep clipping only on the photo.
- ❌ Do not build the pie as a chart object or many tiny segments; use one clean `<path>` wedge for the hero statistic.
- ❌ Do not use `marker-end` on a curved `<path>` for callouts; use simple `<line>` elements if directional accents are needed.
- ❌ Do not omit `width` on text elements; PowerPoint text boxes need explicit width for stable rendering.

## Composition notes
- Keep the image/data circle on the left 40–50% of the slide and let it dominate the visual field.
- Place the large percentage inside the dark slice, not on the photo area, to preserve contrast.
- Reserve the right side for the explanatory headline with strong hierarchy: label, bold statement, accent word, footnote.
- Use a bright background, dark slice, white percentage, and one warm accent color to create a keynote-style color rhythm.