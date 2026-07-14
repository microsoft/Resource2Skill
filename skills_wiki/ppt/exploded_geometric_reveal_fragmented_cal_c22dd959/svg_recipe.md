# SVG Recipe — Exploded Geometric Reveal (Fragmented Callout)

## Visual mechanism
A complete circle is visually “broken” by clipping a photo into a 270° pie sector, then offsetting the missing 90° quadrant as a bright floating accent piece. The exploded fragment creates directional tension and naturally points toward the large metric callout.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 2× `<ellipse>` for soft ambient glow fields behind the composition
- 1× `<clipPath>` with a 270° `<path>` for cropping the hero image into the main circle fragment
- 1× `<image>` for the photo-filled main fragment
- 4× `<path>` for the main sector shadow, main rim, exploded accent quadrant, and ghost outline of the missing quadrant
- 1× `<linearGradient>` for the background wash
- 1× `<linearGradient>` for the cyan accent fragment
- 1× `<linearGradient>` for a subtle photo-tint overlay
- 2× `<filter>` using `feOffset`, `feGaussianBlur`, and `feMerge` for fragment shadows and glow depth
- 1× `<line>` for a thin connector from the fragment to the callout text
- 5× `<circle>` for decorative data dots and orbit markers
- 5× `<rect>` for small KPI chips / mini data bars
- Multiple `<text>` elements with explicit `width` for metric, title, body copy, and labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0D111C"/>
      <stop offset="58%" stop-color="#101827"/>
      <stop offset="100%" stop-color="#070A12"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="335" y1="110" x2="585" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#54E6FF"/>
      <stop offset="58%" stop-color="#00BFFF"/>
      <stop offset="100%" stop-color="#006DFF"/>
    </linearGradient>

    <linearGradient id="photoTint" x1="85" y1="110" x2="585" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.10"/>
      <stop offset="52%" stop-color="#0D111C" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset in="SourceAlpha" dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="16" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="mainSectorClip" clipPathUnits="userSpaceOnUse">
      <path d="M335 360 L585 360 A250 250 0 1 1 335 110 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <ellipse cx="325" cy="380" rx="360" ry="300" fill="#00BFFF" opacity="0.10" filter="url(#accentGlow)"/>
  <ellipse cx="1030" cy="145" rx="260" ry="180" fill="#7C3AED" opacity="0.12" filter="url(#accentGlow)"/>

  <circle cx="335" cy="360" r="292" fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1.5" stroke-dasharray="4 12"/>
  <circle cx="335" cy="360" r="222" fill="none" stroke="#00BFFF" stroke-opacity="0.15" stroke-width="1" stroke-dasharray="18 14"/>
  <circle cx="132" cy="201" r="5" fill="#00BFFF" opacity="0.65"/>
  <circle cx="568" cy="555" r="4" fill="#FFFFFF" opacity="0.35"/>
  <circle cx="502" cy="136" r="7" fill="#00BFFF" opacity="0.28"/>

  <path d="M335 360 L585 360 A250 250 0 1 1 335 110 Z" fill="#000000" opacity="0.45" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-photo/business-architecture-glass-towers-square.jpg"
         x="85" y="110" width="500" height="500" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#mainSectorClip)"/>
  <path d="M335 360 L585 360 A250 250 0 1 1 335 110 Z" fill="url(#photoTint)"/>
  <path d="M335 360 L585 360 A250 250 0 1 1 335 110 Z" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>

  <path d="M335 360 L335 110 A250 250 0 0 1 585 360 Z"
        fill="none" stroke="#00BFFF" stroke-width="2" stroke-opacity="0.22" stroke-dasharray="10 10"/>

  <path d="M335 360 L335 110 A250 250 0 0 1 585 360 Z"
        transform="translate(48 -48)" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <path d="M335 360 L335 110 A250 250 0 0 1 585 360 Z"
        transform="translate(48 -48)" fill="none" stroke="#B9F7FF" stroke-width="3" stroke-opacity="0.7"/>
  <path d="M383 312 L383 110 A250 250 0 0 1 585 312"
        transform="translate(48 -48)" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.42"/>

  <line x1="620" y1="246" x2="690" y2="246" stroke="#00BFFF" stroke-width="2.5" stroke-opacity="0.85"/>
  <circle cx="690" cy="246" r="5" fill="#00BFFF"/>

  <text x="706" y="215" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700"
        letter-spacing="3" fill="#54E6FF">EXPANSION FOCUS</text>

  <text x="700" y="315" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="112" font-weight="800"
        fill="#FFFFFF">25%</text>

  <text x="710" y="370" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700"
        fill="#FFFFFF">Market Expansion</text>

  <text x="712" y="415" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="400"
        fill="#B8C2D6">
    <tspan x="712" dy="0">The highlighted segment isolates the</tspan>
    <tspan x="712" dy="28">new sector opportunity while the photo</tspan>
    <tspan x="712" dy="28">fragment preserves the larger market context.</tspan>
  </text>

  <rect x="712" y="530" width="122" height="48" rx="14" fill="#FFFFFF" opacity="0.07"/>
  <rect x="854" y="530" width="122" height="48" rx="14" fill="#FFFFFF" opacity="0.07"/>
  <rect x="996" y="530" width="122" height="48" rx="14" fill="#FFFFFF" opacity="0.07"/>

  <rect x="728" y="562" width="72" height="5" rx="2.5" fill="#00BFFF"/>
  <rect x="870" y="562" width="49" height="5" rx="2.5" fill="#FFB020"/>
  <rect x="1012" y="562" width="86" height="5" rx="2.5" fill="#7CFFB2"/>

  <text x="728" y="552" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#EAF2FF">TAM</text>
  <text x="870" y="552" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#EAF2FF">PIPELINE</text>
  <text x="1012" y="552" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#EAF2FF">MARGIN</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to subtract the missing quadrant; use a `<clipPath>` on the `<image>` and explicit pie-sector `<path>` shapes instead.
- ❌ Applying `clip-path` to a `<g>` or decorative `<path>`; PPT translation only preserves clipping reliably on `<image>`.
- ❌ Building the exploded quadrant with `<use href="#...">`; duplicate the sector path directly.
- ❌ Using `marker-end` arrowheads for the connector; draw a simple `<line>` and optional `<circle>` endpoint.
- ❌ Relying on `skewX`, `skewY`, or matrix transforms to fake perspective; offset the fragment with `translate(x y)` only.

## Composition notes
- Keep the fragmented circle large and left-weighted, occupying roughly 40–45% of slide width.
- Offset the accent quadrant diagonally upward/right by about 8–12% of the circle radius so the circle still feels psychologically complete.
- Place the metric immediately to the right of the exploded fragment; the connector should feel like a continuation of the fragment’s outward motion.
- Use a dark background, one vivid accent color, and restrained white/blue-gray typography to preserve executive-keynote polish.