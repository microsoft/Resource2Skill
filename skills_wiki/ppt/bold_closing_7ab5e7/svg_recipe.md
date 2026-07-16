# SVG Recipe — Bold Closing

## Visual mechanism
A full-bleed saturated background creates instant finality, while one oversized centered headline becomes the sole focal point. Subtle folded-paper geometry, vignette glow, and faint diagonal highlights add keynote polish without competing with the closing message.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<radialGradient>` for center glow and edge vignette depth
- 2× `<linearGradient>` for diagonal accent folds and highlight panels
- 5× `<path>` for oversized folded-paper / spotlight geometry
- 1× `<rect>` for a soft central headline glow panel
- 1× `<filter id="softShadow">` applied to fold geometry
- 1× `<filter id="titleGlow">` applied to the headline text
- 1× `<text>` with nested `<tspan>` for the centered closing headline
- 2× `<line>` for fine metallic accent rules near the headline

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#141B5D"/>
      <stop offset="0.45" stop-color="#5330C9"/>
      <stop offset="1" stop-color="#F0448A"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="48%" r="54%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="50%" r="70%">
      <stop offset="0" stop-color="#080A2A" stop-opacity="0"/>
      <stop offset="0.72" stop-color="#080A2A" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#080A2A" stop-opacity="0.55"/>
    </radialGradient>

    <linearGradient id="foldLight" x1="120" y1="120" x2="1160" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="0.52" stop-color="#FFFFFF" stop-opacity="0.09"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="foldDark" x1="0" y1="720" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#050620" stop-opacity="0.35"/>
      <stop offset="0.55" stop-color="#050620" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#050620" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ruleGradient" x1="350" y1="0" x2="930" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-15%" y="-35%" width="130%" height="170%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <path d="M-120 95 L440 -40 L1180 720 L720 760 Z"
        fill="url(#foldLight)" opacity="0.55"/>
  <path d="M860 -80 L1340 0 L1010 720 L620 720 Z"
        fill="url(#foldDark)" opacity="0.48"/>
  <path d="M-80 640 L325 365 L1280 580 L1280 760 L-80 760 Z"
        fill="#FFFFFF" opacity="0.07"/>
  <path d="M0 0 L260 0 L0 255 Z"
        fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <path d="M1280 720 L1018 720 L1280 470 Z"
        fill="#050620" opacity="0.20" filter="url(#softShadow)"/>

  <rect x="250" y="245" width="780" height="230" rx="38"
        fill="#FFFFFF" opacity="0.055"/>

  <line x1="348" y1="284" x2="932" y2="284"
        stroke="url(#ruleGradient)" stroke-width="2"/>
  <line x1="348" y1="438" x2="932" y2="438"
        stroke="url(#ruleGradient)" stroke-width="2"/>

  <text x="640" y="377" width="960"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92"
        font-weight="800"
        letter-spacing="5"
        fill="#FFFFFF"
        filter="url(#titleGlow)">
    <tspan x="640" dy="0">THANK YOU</tspan>
  </text>

  <text x="640" y="420" width="760"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22"
        font-weight="500"
        letter-spacing="3"
        fill="#FFFFFF"
        opacity="0.78">
    <tspan x="640" dy="0">LET’S BUILD WHAT’S NEXT</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Multiple competing content blocks; the closing slide should have one dominant message
- ❌ Thin low-contrast headline text on a saturated background
- ❌ Busy dashboards, icons, or charts that dilute the final emotional beat
- ❌ `<mask>` or clipped non-image shapes for the fold effect; use native paths with opacity and gradients instead
- ❌ Small text placed near the slide edges, where vignette and projection cropping can reduce readability

## Composition notes
- Keep the headline centered both horizontally and optically; the safest title zone is roughly x=250–1030 and y=260–430.
- Use a full-bleed bold accent background, but add center glow so white text remains crisp.
- Decorative folds should live mostly in corners and diagonals, never crossing the headline at high opacity.
- Limit copy to a short closing phrase; if a secondary line is needed, keep it small, widely tracked, and directly beneath the main headline.