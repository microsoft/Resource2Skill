# SVG Recipe — Hero Image Cover

## Visual mechanism
A low-density cover slide with a large, emotionally immediate hero image centered under a bold headline. The image is treated as the main object of attention, supported by a cinematic gradient background, soft glow, oversized decorative geometry, and generous negative space.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<rect>` for translucent top/bottom atmospheric overlays
- 6× `<circle>` for spotlight glows, image halo, and subtle decorative dots
- 4× `<path>` for organic background ribbons and energetic swooshes around the hero image
- 1× `<image>` for the central hero photograph, clipped into a large circle
- 1× `<clipPath>` with `<circle>` applied to the hero `<image>`
- 3× `<linearGradient>` for background, title accent, and decorative ribbons
- 2× `<radialGradient>` for spotlight and halo lighting
- 2× `<filter>` definitions: one soft shadow for hero/decorative shapes, one glow for title accents
- 3× `<text>` elements with explicit `width` attributes for title, kicker, and small caption
- Nested `<tspan>` inside the headline for inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.48" stop-color="#102B3A"/>
      <stop offset="1" stop-color="#103D2C"/>
    </linearGradient>

    <linearGradient id="headlineGradient" x1="150" y1="60" x2="980" y2="150" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.58" stop-color="#EAF7FF"/>
      <stop offset="1" stop-color="#A7F3D0"/>
    </linearGradient>

    <linearGradient id="ribbonGradient" x1="170" y1="230" x2="1110" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22D3EE" stop-opacity="0.12"/>
      <stop offset="0.55" stop-color="#A3E635" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#FDE047" stop-opacity="0.10"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="52%" r="52%">
      <stop offset="0" stop-color="#D9F99D" stop-opacity="0.42"/>
      <stop offset="0.42" stop-color="#34D399" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#07111F" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="imageHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.35"/>
      <stop offset="0.72" stop-color="#86EFAC" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#86EFAC" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.05  0 0 0 0 0.08  0 0 0 0.42 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroCircleClip">
      <circle cx="640" cy="425" r="205"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>
  <rect x="0" y="0" width="1280" height="230" fill="#FFFFFF" opacity="0.035"/>
  <rect x="0" y="530" width="1280" height="190" fill="#000000" opacity="0.18"/>

  <circle cx="640" cy="430" r="430" fill="url(#centerGlow)"/>
  <circle cx="640" cy="425" r="270" fill="url(#imageHalo)" filter="url(#softGlow)"/>

  <path d="M-80,516 C160,380 315,656 548,522 C755,403 892,206 1360,295 L1360,720 L-80,720 Z"
        fill="url(#ribbonGradient)" opacity="0.78"/>
  <path d="M92,286 C260,182 425,217 560,326 C690,430 833,452 1042,330 C1128,280 1210,270 1305,300"
        fill="none" stroke="#67E8F9" stroke-width="3" stroke-linecap="round" opacity="0.34"/>
  <path d="M155,570 C320,486 456,536 570,594 C724,672 885,660 1094,518"
        fill="none" stroke="#BEF264" stroke-width="5" stroke-linecap="round" opacity="0.22"/>
  <path d="M308,412 C382,268 542,211 690,250 C820,284 902,393 901,527 C810,482 733,456 626,470 C508,486 410,456 308,412 Z"
        fill="#FFFFFF" opacity="0.045"/>

  <circle cx="180" cy="184" r="5" fill="#A7F3D0" opacity="0.75"/>
  <circle cx="1090" cy="154" r="8" fill="#67E8F9" opacity="0.45"/>
  <circle cx="1138" cy="514" r="4" fill="#FDE047" opacity="0.75"/>
  <circle cx="236" cy="612" r="10" fill="#FFFFFF" opacity="0.14"/>

  <circle cx="640" cy="425" r="226" fill="#FFFFFF" opacity="0.12" filter="url(#softShadow)"/>
  <circle cx="640" cy="425" r="215" fill="#0B1724" opacity="0.9"/>

  <image x="410" y="195" width="460" height="460"
         href="https://images.example.com/hero/soccer-ball-action-photo-on-green-pitch.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroCircleClip)"/>

  <circle cx="640" cy="425" r="206" fill="none" stroke="#FFFFFF" stroke-width="7" opacity="0.92"/>
  <circle cx="640" cy="425" r="222" fill="none" stroke="#A7F3D0" stroke-width="2" opacity="0.55"/>
  <circle cx="640" cy="425" r="246" fill="none" stroke="#67E8F9" stroke-width="1.5" stroke-dasharray="10 14" opacity="0.35"/>

  <text x="90" y="70" width="1100"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3"
        fill="#A7F3D0" opacity="0.95">
    SEASON OPENING KEYNOTE
  </text>

  <text x="88" y="142" width="1104"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="68" font-weight="800" letter-spacing="-2"
        fill="url(#headlineGradient)" filter="url(#softGlow)">
    <tspan>Own the </tspan><tspan fill="#BEF264">Moment</tspan>
  </text>

  <text x="250" y="672" width="780"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="500"
        text-anchor="middle"
        fill="#EAF7FF" opacity="0.78"
        transform="translate(390 0)">
    A bold hero image cover for launches, sports stories, campaigns, and keynote openings.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the hero image; use a clipped `<image>` plus editable overlay shapes instead.
- ❌ Do not apply `clip-path` to decorative circles or paths; clipping is only reliable here on the `<image>`.
- ❌ Do not build the cover as many small tiled rectangles; the technique depends on one dominant image and large atmospheric shapes.
- ❌ Do not place the title directly over a busy photo unless you add a strong gradient veil or reposition the image lower.

## Composition notes
- Keep the headline in the upper 20–25% of the slide; the hero image should dominate the center and lower middle.
- Use generous negative space around the title so it reads instantly as a cover, not a content slide.
- Let decorative paths orbit or cradle the hero image rather than compete with it.
- Maintain a tight color rhythm: dark cinematic base, one bright accent, and white headline contrast.