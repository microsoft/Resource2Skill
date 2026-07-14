# SVG Recipe — Full Bleed Image Cover

## Visual mechanism
A single edge-to-edge hero image fills the entire 16:9 canvas, with layered editorial scrims and vignettes to guarantee headline contrast without visibly boxing in the photo. The optional centered headline floats over the image with a subtle glass panel, small accent rule, and soft shadow for a premium cover-slide feel.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph, scaled to cover the entire slide
- 2× `<rect>` for full-slide gradient overlays that improve contrast and create cinematic depth
- 1× `<rect>` for a translucent rounded headline backing panel
- 1× `<rect>` for a small accent rule above the headline
- 2× `<path>` for soft organic dark scrim shapes behind the headline and along the lower edge
- 3× `<text>` elements for optional eyebrow, main headline, and subtitle; each with explicit `width`
- 2× `<linearGradient>` for top/bottom editorial shading and accent color
- 1× `<radialGradient>` for center-focused vignette depth
- 2× `<filter>` definitions: one soft shadow for text/panel, one blur for atmospheric background scrims

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoDarken" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#06101C" stop-opacity="0.42"/>
      <stop offset="0.38" stop-color="#06101C" stop-opacity="0.08"/>
      <stop offset="0.72" stop-color="#06101C" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#06101C" stop-opacity="0.70"/>
    </linearGradient>

    <linearGradient id="accentGold" x1="474" y1="288" x2="806" y2="288" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D7B46A" stop-opacity="0"/>
      <stop offset="0.18" stop-color="#D7B46A" stop-opacity="0.95"/>
      <stop offset="0.82" stop-color="#F2D99C" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#F2D99C" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="centerVignette" cx="50%" cy="46%" r="58%">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="0.55" stop-color="#000000" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.48"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="atmosphericBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
  </defs>

  <image
    x="0" y="0" width="1280" height="720"
    href="https://images.example.com/full-bleed-cover/misty-mountain-sunrise-executive-keynote.jpg"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#photoDarken)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerVignette)"/>

  <path
    d="M116 -42 C260 22 300 120 435 151 C568 181 640 107 750 142 C860 177 870 290 1020 304 C1128 314 1205 263 1320 305 L1320 -60 Z"
    fill="#06101C"
    opacity="0.26"
    filter="url(#atmosphericBlur)"/>

  <path
    d="M-80 670 C120 600 240 635 398 664 C565 695 650 722 814 682 C976 643 1073 578 1360 638 L1360 780 L-80 780 Z"
    fill="#000814"
    opacity="0.42"
    filter="url(#atmosphericBlur)"/>

  <rect
    x="260" y="218" width="760" height="280" rx="34"
    fill="#07111F"
    opacity="0.32"
    filter="url(#softShadow)"/>

  <rect
    x="474" y="286" width="332" height="3.5" rx="1.75"
    fill="url(#accentGold)"/>

  <text
    x="340" y="268"
    width="600"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16"
    font-weight="700"
    letter-spacing="4"
    fill="#F5E9CF"
    opacity="0.92">
    STRATEGIC OUTLOOK
  </text>

  <text
    x="640" y="356"
    width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="58"
    font-weight="700"
    letter-spacing="-1.4"
    fill="#FFFFFF"
    filter="url(#softShadow)">
    <tspan x="640" dy="0">Signals Beyond</tspan>
    <tspan x="640" dy="66">the Horizon</tspan>
  </text>

  <text
    x="640" y="475"
    width="620"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="21"
    font-weight="400"
    fill="#DDE7F3"
    opacity="0.88">
    A concise executive briefing for the next market cycle
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not crop the hero image with `<mask>`; use full-canvas `<image>` sizing or an `<image>` with an allowed `<clipPath>` only if a non-rectangular crop is truly needed.
- ❌ Do not place headline text directly on a busy photo without gradient scrims or a translucent backing layer; contrast will fail on many images.
- ❌ Do not use `<foreignObject>` for multiline title layout; use separate `<tspan>` lines inside editable SVG `<text>`.
- ❌ Do not apply filters to `<line>` elements for accent rules; use a thin rounded `<rect>` instead.

## Composition notes
- Keep the image truly full bleed: no margins, frames, or visible crop edges.
- Put the headline near optical center, slightly above the vertical midpoint when a subtitle is present.
- Reserve the darkest overlay area behind the headline; let brighter photographic detail live toward corners or edges.
- Use one restrained accent color, usually sampled from the image warmth, to avoid competing with the photo.