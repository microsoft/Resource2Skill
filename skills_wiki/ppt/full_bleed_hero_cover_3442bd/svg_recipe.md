# SVG Recipe — Full Bleed Hero Cover

## Visual mechanism
A full-bleed photographic hero image fills the entire slide, then dark gradient scrims and subtle editorial geometry create a clean reading zone for an oversized headline. The slide feels premium because the typography is massive, sparse, and anchored against cinematic image contrast rather than boxed into a card.

## SVG primitives needed
- 1× `<image>` for the full-slide hero photograph
- 3× `<rect>` for full-bleed darkening, side readability gradient, and bottom vignette
- 3× `<path>` for translucent diagonal editorial shards that add depth without blocking the image
- 3× `<linearGradient>` for cinematic overlay, left-side text scrim, and warm accent geometry
- 1× `<filter id="softTextShadow">` with blur/offset/merge for headline legibility
- 2× `<line>` for small editorial accent rules near the title block
- 3× `<text>` for eyebrow, headline, and subtitle; every text element has an explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaScrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.42"/>
      <stop offset="48%" stop-color="#020617" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="leftReadability" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.88"/>
      <stop offset="42%" stop-color="#020617" stop-opacity="0.58"/>
      <stop offset="72%" stop-color="#020617" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="accentGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8D47A" stop-opacity="0.86"/>
      <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.26"/>
    </linearGradient>

    <linearGradient id="coolGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.02"/>
    </linearGradient>

    <filter id="softTextShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.example.com/hero-photo-modern-city-skyline-at-blue-hour.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaScrim)"/>
  <rect x="0" y="0" width="920" height="720" fill="url(#leftReadability)"/>
  <rect x="0" y="500" width="1280" height="220" fill="#020617" opacity="0.18"/>

  <path
    d="M930 -40 L1280 -40 L1280 720 L1105 720 L1012 402 Z"
    fill="#020617"
    opacity="0.34"/>

  <path
    d="M1040 0 L1280 0 L1280 350 L1152 288 Z"
    fill="url(#coolGlass)"
    opacity="0.9"/>

  <path
    d="M794 720 L931 720 L806 510 L690 510 Z"
    fill="url(#accentGold)"
    opacity="0.72"/>

  <line
    x1="92" y1="250" x2="174" y2="250"
    stroke="#F8D47A"
    stroke-width="5"
    stroke-linecap="round"/>

  <text
    x="190" y="258"
    width="480"
    fill="#F8FAFC"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="700"
    letter-spacing="4">
    2026 STRATEGY BRIEFING
  </text>

  <text
    x="88" y="398"
    width="850"
    fill="#FFFFFF"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="92"
    font-weight="800"
    letter-spacing="-3"
    filter="url(#softTextShadow)">
    <tspan x="88" dy="0">URBAN</tspan>
    <tspan x="88" dy="96">FUTURES</tspan>
  </text>

  <line
    x1="92" y1="596" x2="92" y2="646"
    stroke="#F8D47A"
    stroke-width="4"
    stroke-linecap="round"/>

  <text
    x="120" y="603"
    width="660"
    fill="#DDE7F5"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="25"
    font-weight="400"
    letter-spacing="0.2">
    Designing resilient growth across infrastructure, climate, and digital mobility.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not place the headline inside an opaque rectangular card; it weakens the full-bleed photographic impact.
- ❌ Do not rely on a bright hero image without a gradient scrim; title legibility will collapse on busy areas.
- ❌ Do not use `mask` or clip paths on non-image shapes for the vignette; use gradient-filled `<rect>` and `<path>` overlays instead.
- ❌ Do not make the headline small or centered like a normal title slide; the technique depends on oversized editorial typography.

## Composition notes
- Keep the main text block on the darkest third of the image, usually left or lower-left, with 80–110 px slide margins.
- Use the photo as atmosphere, not information density; choose images with one broad dark area suitable for type.
- Reserve 55–65% of the slide for visual immersion and 35–45% for the title zone.
- Add one warm accent line or shard to create brand energy, but keep overlays translucent so the hero image remains dominant.