# SVG Recipe — Immersive Typographic Quote Poster

## Visual mechanism
A full-bleed abstract image is darkened and color-washed, then overlaid with oversized editorial typography. The signature effect is a massive hollow word in outline-only text paired with dense solid quote lines, making the words feel like part of the poster artwork rather than a normal slide title.

## SVG primitives needed
- 1× `<image>` for the full-bleed abstract or moody photographic background.
- 3× `<rect>` for the base darkness overlay, left-side readability vignette, and small accent rule.
- 3× `<ellipse>` for blurred neon atmosphere glows layered over the background.
- 2× `<path>` for organic decorative light streaks / poster texture accents.
- 3× `<text>` blocks for the hollow hook word, solid quote body, and tracked attribution.
- 1× `<linearGradient>` for the dark readability wash.
- 2× `<radialGradient>` for neon purple/cyan glow fills.
- 2× `<filter>` using `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for atmospheric blur and soft text shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftDarkWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#02030A" stop-opacity="0.92"/>
      <stop offset="48%" stop-color="#02030A" stop-opacity="0.72"/>
      <stop offset="78%" stop-color="#02030A" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#02030A" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="purpleGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#BA55D3" stop-opacity="0.90"/>
      <stop offset="45%" stop-color="#7B2CFF" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#7B2CFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00FFFF" stop-opacity="0.72"/>
      <stop offset="52%" stop-color="#00AEEF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#00AEEF" stop-opacity="0"/>
    </radialGradient>

    <filter id="atmosphericBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="softPosterShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.example.com/abstract-dark-holographic-texture-with-purple-cyan-light.jpg"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#03040B" opacity="0.44"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftDarkWash)"/>

  <ellipse cx="1030" cy="130" rx="270" ry="155" fill="url(#purpleGlow)" filter="url(#atmosphericBlur)" opacity="0.78"/>
  <ellipse cx="1060" cy="610" rx="360" ry="120" fill="url(#cyanGlow)" filter="url(#atmosphericBlur)" opacity="0.62"/>
  <ellipse cx="360" cy="95" rx="220" ry="80" fill="url(#purpleGlow)" filter="url(#atmosphericBlur)" opacity="0.36"/>

  <path d="M810 52 C930 88 980 150 1135 134 C1194 128 1234 108 1280 86 L1280 178 C1212 208 1132 220 1038 198 C934 174 880 128 782 116 Z"
        fill="#FFFFFF" opacity="0.055"/>
  <path d="M822 588 C934 548 1018 552 1114 602 C1174 634 1224 642 1280 626 L1280 720 L846 720 C798 675 780 623 822 588 Z"
        fill="#00FFFF" opacity="0.075"/>

  <text x="92" y="156" width="1050"
        font-family="Segoe UI, Microsoft YaHei, Arial Black, sans-serif"
        font-size="112" font-weight="900" letter-spacing="-3"
        fill="none" stroke="#FFFFFF" stroke-width="2.8" opacity="0.92">
    CREATIVITY
  </text>

  <text x="96" y="256" width="820"
        font-family="Segoe UI, Microsoft YaHei, Arial Black, sans-serif"
        font-size="60" font-weight="900" letter-spacing="-1.4"
        fill="#FFFFFF" filter="url(#softPosterShadow)">
    <tspan x="96" dy="0">IS INVENTING,</tspan>
    <tspan x="96" dy="68">EXPERIMENTING,</tspan>
    <tspan x="96" dy="68">GROWING,</tspan>
    <tspan x="96" dy="68">TAKING RISKS,</tspan>
    <tspan x="96" dy="68">BREAKING RULES,</tspan>
    <tspan x="96" dy="68">AND HAVING FUN.</tspan>
  </text>

  <rect x="99" y="652" width="92" height="5" rx="2.5" fill="#00FFFF"/>
  <text x="216" y="660" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="5.5"
        fill="#BA55D3">
    ANGELO BREWING
  </text>

  <text x="958" y="396" width="250"
        font-family="Segoe UI, Microsoft YaHei, Arial Black, sans-serif"
        font-size="190" font-weight="900"
        fill="#FFFFFF" opacity="0.065" transform="rotate(-8 958 396)">
    “
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create hollow text; use native SVG text with `fill="none"` and `stroke` instead.
- ❌ Do not rely on `<textPath>` for editorial curves; it will not translate reliably.
- ❌ Do not apply `clip-path` to text or decorative shapes; clipping is only safe for `<image>` elements.
- ❌ Do not make the background too bright behind the solid body copy; the effect depends on strong contrast.
- ❌ Do not use thin outline fonts for the hollow headline; use a heavy font with a visible stroke so it survives PowerPoint editing.

## Composition notes
- Keep the main typography block left-aligned and oversized, occupying roughly 55–65% of slide width and 70–80% of slide height.
- Use the right side for atmospheric glow, abstract texture, and negative space; avoid competing readable content there.
- The hollow headline should sit above the solid quote body and feel like a poster masthead, not a normal title.
- Use one neon accent color repeatedly in small doses: glow, rule, attribution, or a few outlined strokes.