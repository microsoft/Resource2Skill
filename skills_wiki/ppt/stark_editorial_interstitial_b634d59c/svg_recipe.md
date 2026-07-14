# SVG Recipe — Stark Editorial Interstitial

## Visual mechanism
A full-bleed, heavily blurred architectural photograph is darkened into a cinematic backdrop, then overlaid with a stark left-aligned typographic block. The effect depends on extreme type contrast: tiny tracked uppercase text above and below a massive white title.

## SVG primitives needed
- 1× `<image>` for the full-slide blurred photographic background
- 3× `<rect>` for dark wash, editorial side shade, and soft vignette overlays
- 2× `<linearGradient>` for directional darkening and subtle side falloff
- 1× `<radialGradient>` for center-to-edge cinematic vignette
- 1× `<filter id="softGlow">` applied to decorative background paths
- 1× `<filter id="textLift">` applied to text for a barely perceptible editorial lift
- 3× `<path>` for blurred atmospheric light/shadow shapes over the photo
- 1× `<line>` for a thin structural editorial rule
- 4× `<text>` for section number, eyebrow, main title, and subtitle
- Nested `<tspan>` inside the title for optional stacked title styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050607" stop-opacity="0.82"/>
      <stop offset="42%" stop-color="#080A0D" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#020304" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="leftEditorialShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.62"/>
      <stop offset="38%" stop-color="#000000" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="vignette" cx="46%" cy="50%" r="72%">
      <stop offset="0%" stop-color="#10141A" stop-opacity="0"/>
      <stop offset="58%" stop-color="#06080B" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.68"/>
    </radialGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>

    <filter id="textLift" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="2" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#07090C"/>

  <image
    href="https://images.example.com/preblurred-dark-architecture-interior-glass-concrete-1920x1080.jpg"
    x="-18" y="-18" width="1316" height="756"
    preserveAspectRatio="xMidYMid slice"/>

  <path
    d="M-90,76 C160,2 272,94 410,46 C562,-6 705,-18 838,48 C640,86 482,160 344,236 C188,322 30,300 -90,238 Z"
    fill="#7A8CA5" opacity="0.16" filter="url(#softGlow)"/>

  <path
    d="M778,688 C928,544 1096,470 1378,500 L1378,808 L760,808 C706,766 716,742 778,688 Z"
    fill="#A48D72" opacity="0.12" filter="url(#softGlow)"/>

  <path
    d="M1060,-80 C1148,82 1180,208 1318,290 L1318,-80 Z"
    fill="#D4E0EA" opacity="0.10" filter="url(#softGlow)"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkWash)"/>
  <rect x="0" y="0" width="760" height="720" fill="url(#leftEditorialShade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <line
    x1="144" y1="246" x2="264" y2="246"
    stroke="#B8BCC2" stroke-width="1.2" opacity="0.46"/>

  <text
    x="144" y="226" width="180"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="12" font-weight="700"
    letter-spacing="5"
    fill="#B7BBC0" opacity="0.92">
    02
  </text>

  <text
    x="288" y="250" width="700"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="15" font-weight="700"
    letter-spacing="6"
    fill="#BABEC3" opacity="0.92">
    TYPICAL CLIENT MEETING
  </text>

  <text
    x="138" y="374" width="970"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="106" font-weight="800"
    letter-spacing="-2"
    fill="#FFFFFF"
    filter="url(#textLift)">
    <tspan x="138" dy="0">AGENDA</tspan>
  </text>

  <text
    x="144" y="434" width="850"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="14" font-weight="600"
    letter-spacing="3.6"
    fill="#D4D7DA" opacity="0.9">
    A GUIDE TO ENSURE YOU DON'T LEAVE ANY QUESTION UNANSWERED
  </text>

  <text
    x="1122" y="642" width="120"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="10" font-weight="600"
    letter-spacing="3"
    fill="#A9ADB2" opacity="0.46"
    text-anchor="end">
    STRATEGY DECK
  </text>
</svg>
```

## Avoid in this skill
- ❌ Relying on an SVG blur filter directly on the `<image>` if consistent PPT editability is required; use a pre-blurred image asset or data URI instead.
- ❌ Busy, high-contrast photography behind the title; the image should read as atmosphere, not content.
- ❌ Center-aligning the title block; the editorial feel comes from a strong left margin and architectural alignment.
- ❌ Large colored accents or decorative iconography; this style should remain monochrome, restrained, and cinematic.
- ❌ Missing `width` on `<text>` elements; PowerPoint text boxes will not render predictably without it.

## Composition notes
- Keep the typography block left-aligned around x=140–150, vertically centered slightly above the slide midpoint.
- Reserve the right half of the slide mostly as negative atmospheric space; do not fill it with secondary content.
- Use pure white only for the main title, with grey/off-white for eyebrow and subtitle to preserve hierarchy.
- The background should be dark enough that text feels like the only bright object on the slide.