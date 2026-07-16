# SVG Recipe — Angled Split Cover

## Visual mechanism
A cover slide split by a steep diagonal edge: calm typography sits on a light editorial panel while a saturated photo or gradient field pushes in from the opposite side. Oversized angled color bands echo the split, creating motion without clutter.

## SVG primitives needed
- 2× `<rect>` for full-slide base color and subtle top/bottom framing
- 1× `<image>` for the right-side hero visual, clipped into an angled polygonal crop
- 1× `<clipPath>` with a `<path>` applied only to the hero `<image>`
- 5× `<path>` for the main angled panel, dark photo overlay, and decorative diagonal accent bands
- 2× `<linearGradient>` for background depth and accent-band color
- 1× `<radialGradient>` for a soft highlight behind the title area
- 2× `<filter>` definitions for soft shadow and glow applied to paths/rectangles/text
- 5× `<text>` elements with explicit `width` for eyebrow, headline, subtitle, section label, and date
- 1× `<line>` for a small editorial divider accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyDepth" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#071B36"/>
      <stop offset="0.55" stop-color="#0E2A4D"/>
      <stop offset="1" stop-color="#07111F"/>
    </linearGradient>

    <linearGradient id="accentHeat" x1="420" y1="90" x2="1120" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#30D5C8"/>
      <stop offset="0.48" stop-color="#3E7BFF"/>
      <stop offset="1" stop-color="#FF6B4A"/>
    </linearGradient>

    <radialGradient id="titleGlow" cx="270" cy="290" r="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="0.55" stop-color="#F4F8FC" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#E8EEF5" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="20"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="edgeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="photoAngle">
      <path d="M715 0 L1280 0 L1280 720 L555 720 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#navyDepth)"/>

  <image
    href="https://images.example.com/hero-photo-glass-tower-city-at-dusk.jpg"
    x="515" y="-30" width="820" height="800"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoAngle)"/>

  <path d="M700 0 L1280 0 L1280 720 L560 720 Z" fill="#061425" opacity="0.28"/>

  <path
    d="M0 0 L760 0 L602 720 L0 720 Z"
    fill="#F5F8FC"
    filter="url(#softShadow)"/>

  <path d="M0 0 L760 0 L602 720 L0 720 Z" fill="url(#titleGlow)"/>

  <path
    d="M805 -45 L900 -45 L676 765 L581 765 Z"
    fill="url(#accentHeat)"
    opacity="0.96"
    filter="url(#softShadow)"/>

  <path
    d="M928 -30 L958 -30 L734 750 L704 750 Z"
    fill="#FFFFFF"
    opacity="0.36"
    filter="url(#edgeGlow)"/>

  <path
    d="M1010 58 L1048 58 L902 570 L864 570 Z"
    fill="#FFB547"
    opacity="0.88"/>

  <path
    d="M112 94 L244 94 L220 118 L88 118 Z"
    fill="#30D5C8"
    opacity="0.95"/>

  <text x="92" y="82" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3"
        fill="#2A6F7E">
    STRATEGY BRIEFING
  </text>

  <text x="90" y="205" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="70" font-weight="800"
        fill="#071B36">
    <tspan x="90" dy="0">Angled</tspan>
    <tspan x="90" dy="78">Market</tspan>
    <tspan x="90" dy="78">Outlook</tspan>
  </text>

  <line x1="94" y1="475" x2="218" y2="475" stroke="#FF6B4A" stroke-width="6" stroke-linecap="round"/>

  <text x="92" y="520" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400"
        fill="#33445C">
    Three forces reshaping growth, margin resilience, and the next operating model.
  </text>

  <rect x="92" y="610" width="210" height="42" rx="21" fill="#071B36" opacity="0.96"/>

  <text x="118" y="638" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="1.6"
        fill="#FFFFFF">
    EXECUTIVE DECK
  </text>

  <text x="1050" y="648" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600"
        fill="#FFFFFF" opacity="0.88">
    2026 / Q2
  </text>

  <rect x="0" y="0" width="1280" height="12" fill="#30D5C8" opacity="0.9"/>
  <rect x="0" y="708" width="1280" height="12" fill="#FF6B4A" opacity="0.9"/>
</svg>
```

## Avoid in this skill
- ❌ Using `skewX`, `skewY`, or `matrix(...)` transforms for the angled split; draw the diagonal panels as explicit `<path>` polygons instead.
- ❌ Applying `clip-path` to colored shapes or text; keep clipping only on the `<image>` so it translates reliably.
- ❌ Building the split with dozens of thin repeated stripes; use a few large diagonal bands for a premium keynote look.
- ❌ Placing headline text over the busy photo area unless a strong dark overlay is added.

## Composition notes
- Keep the title panel roughly the left 55–60% of the canvas, with the diagonal edge cutting toward the lower center.
- Let the photo or dark visual field own the right side; it should feel energetic but not compete with the headline.
- Use one strong accent diagonal near the split, then one or two thinner supporting slashes for rhythm.
- Preserve generous negative space around the headline; this cover depends on bold geometry plus restrained typography.