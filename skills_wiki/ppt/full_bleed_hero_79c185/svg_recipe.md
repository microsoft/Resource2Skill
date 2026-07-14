# SVG Recipe — Full Bleed Hero

## Visual mechanism
A cinematic full-bleed photograph fills the entire 16:9 canvas, with layered dark-to-transparent gradients creating a readable lower-third text zone. Subtle warm light leaks, vignette shading, and restrained editorial typography make the slide feel like a premium keynote cover or section divider.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph, set to cover the entire canvas
- 4–6× `<rect>` for full-slide tonal overlays, bottom readability gradients, and small editorial label backing
- 1–2× `<path>` for warm organic light-leak shapes that add cinematic atmosphere
- 1× `<ellipse>` or `<circle>` for a soft radial highlight / lens glow
- 1× `<line>` for a thin accent rule anchoring the lower-third typography
- 3× `<text>` for eyebrow label, headline, and subtitle; every text element must include `width`
- 2–3× `<linearGradient>` for dark vignette and lower-third legibility overlays
- 1× `<radialGradient>` for warm photo glow
- 1–2× `<filter>` with blur/shadow for atmospheric glow and text separation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bottomFade" x1="0" y1="720" x2="0" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#050403" stop-opacity="0.92"/>
      <stop offset="0.48" stop-color="#080605" stop-opacity="0.66"/>
      <stop offset="1" stop-color="#080605" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="leftFade" x1="0" y1="360" x2="760" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#060504" stop-opacity="0.58"/>
      <stop offset="0.52" stop-color="#060504" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#060504" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="topVignette" x1="0" y1="0" x2="0" y2="230" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="warmLeak" x1="780" y1="540" x2="1180" y2="150" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F4A259" stop-opacity="0"/>
      <stop offset="0.42" stop-color="#F4A259" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#FFE1A8" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="lensGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFD39A" stop-opacity="0.34"/>
      <stop offset="0.46" stop-color="#E88645" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#E88645" stop-opacity="0"/>
    </radialGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>

    <filter id="textShadow" x="-15%" y="-30%" width="130%" height="170%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.example.com/hero-photo-cinematic-warm-architecture-at-dusk.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.14"/>
  <rect x="0" y="0" width="1280" height="260" fill="url(#topVignette)"/>
  <rect x="0" y="0" width="860" height="720" fill="url(#leftFade)"/>
  <rect x="0" y="230" width="1280" height="490" fill="url(#bottomFade)"/>

  <path
    d="M905 720 C950 622 1018 580 1115 526 C1225 465 1284 360 1280 220 L1280 720 Z"
    fill="url(#warmLeak)"
    filter="url(#softGlow)"
    opacity="0.95"/>

  <ellipse
    cx="1035" cy="430" rx="255" ry="160"
    fill="url(#lensGlow)"
    filter="url(#softGlow)"
    opacity="0.82"/>

  <path
    d="M0 640 C172 596 302 620 444 654 C612 694 806 704 1010 654 C1126 626 1215 598 1280 566 L1280 720 L0 720 Z"
    fill="#080605"
    opacity="0.32"/>

  <rect
    x="80" y="424" width="232" height="34" rx="17"
    fill="#11100E"
    opacity="0.58"/>

  <line
    x1="82" y1="486" x2="176" y2="486"
    stroke="#F0B36A"
    stroke-width="4"
    stroke-linecap="round"/>

  <text
    x="102" y="447"
    width="190"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="700"
    letter-spacing="2.8"
    fill="#F7E8D0"
    opacity="0.96">
    2026 STRATEGY
  </text>

  <text
    x="80" y="552"
    width="820"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="66"
    font-weight="700"
    letter-spacing="-1.8"
    fill="#FFFFFF"
    filter="url(#textShadow)">
    <tspan x="80" dy="0">Designing the</tspan>
    <tspan x="80" dy="73">next growth era</tspan>
  </text>

  <text
    x="82" y="660"
    width="720"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="22"
    font-weight="400"
    fill="#E8DED2"
    opacity="0.92"
    filter="url(#textShadow)">
    A full-bleed editorial opener for bold section breaks and executive keynote covers.
  </text>

  <text
    x="1040" y="648"
    width="160"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="600"
    letter-spacing="2.2"
    text-anchor="end"
    fill="#F5D7AF"
    opacity="0.72">
    CONFIDENTIAL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Placing type directly on a bright or busy photo area without a dark gradient overlay; PowerPoint text remains editable but readability will fail.
- ❌ Using `<mask>` for vignette effects; use stacked gradient-filled `<rect>` elements instead.
- ❌ Applying `clip-path` to overlay shapes; only use clipping on `<image>` if a shaped photo crop is required.
- ❌ Building the hero from many small image tiles or patterns; use one full-bleed `<image>` and simple editable overlays.
- ❌ Overcrowding the lower third with bullets, charts, or multiple callouts; this technique works best as a low-density cover/divider.

## Composition notes
- Keep the hero image full canvas, with the main subject preferably on the right or upper middle so the lower-left text zone stays clean.
- Reserve the lower 35–45% of the slide for title and subtitle; use a bottom fade strong enough to make white text reliable.
- Use one warm accent color from the photo for the rule, glow, or eyebrow label to create a unified editorial palette.
- Maintain large negative space around the headline; the visual focus should be the photograph first, then the lower-third message.