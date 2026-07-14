# SVG Recipe — Cinematic Horizontal Stepper Layout

## Visual mechanism
A premium dark-mode slide uses a blurred/tinted cinematic photo as atmosphere, then overlays a fixed top navigation bar and a precise horizontal stepper. The active chapter is emphasized by a bright white node and a vertical drop-line that anchors the viewer’s eye to the focused content block below.

## SVG primitives needed
- 1× `<image>` for the full-slide blurred cinematic background photo
- 3× `<rect>` for dark overlays, top separator, and content glass panel
- 2× `<linearGradient>` for background vignette and subtle content panel fill
- 1× `<radialGradient>` for the active-node glow
- 2× `<filter>` definitions: one soft shadow for panels, one glow for active geometry
- 5× `<circle>` for stepper nodes
- 2× highlighted `<circle>` overlays for the active node and its halo
- 6× `<line>` for top separator, horizontal navigation track segments, and active vertical drop-line
- 3× decorative `<path>` elements for cinematic diagonal light streaks / abstract depth
- Multiple `<text>` elements with explicit `width` for logo, global traits, step numbers, step labels, content heading, and body bullets

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0A0E15" stop-opacity="0.88"/>
      <stop offset="48%" stop-color="#141A24" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#05070B" stop-opacity="0.92"/>
    </linearGradient>

    <linearGradient id="glassPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="55%" stop-color="#9FB1C5" stop-opacity="0.055"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.025"/>
    </linearGradient>

    <radialGradient id="nodeGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.75"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <image href="https://images.example.com/blurred-night-city-architecture-cinematic-1920x1080.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#darkWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#101820" opacity="0.42"/>

  <path d="M-80 650 C210 555 350 560 610 450 C820 360 1020 310 1370 280"
        fill="none" stroke="#8BA1B7" stroke-width="1.2" opacity="0.16"/>
  <path d="M850 -40 C900 120 980 225 1125 350 C1195 410 1235 510 1288 735"
        fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.10"/>
  <path d="M-20 180 C190 120 310 135 490 95 C675 55 790 38 1010 70"
        fill="none" stroke="#6D8095" stroke-width="1" opacity="0.12"/>

  <line x1="0" y1="120" x2="1280" y2="120" stroke="#647382" stroke-width="1" opacity="0.6"/>

  <text x="64" y="44" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#FFFFFF" letter-spacing="1.4">
    PERSONAL
    <tspan x="64" dy="30">CV/RESUME</tspan>
  </text>

  <text x="555" y="68" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#E8EEF5" text-anchor="end" letter-spacing="0.6">
    Adaptability    |    Responsibility    |    Passion    |    Self-control
  </text>

  <text x="64" y="156" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#8EA0B3" letter-spacing="3">
    EXECUTIVE PROFILE MAP
  </text>

  <line x1="250" y1="250" x2="445" y2="250" stroke="#667789" stroke-width="2" opacity="0.85"/>
  <line x1="445" y1="250" x2="640" y2="250" stroke="#667789" stroke-width="2" opacity="0.85"/>
  <line x1="640" y1="250" x2="835" y2="250" stroke="#667789" stroke-width="2" opacity="0.85"/>
  <line x1="835" y1="250" x2="1030" y2="250" stroke="#667789" stroke-width="2" opacity="0.85"/>

  <circle cx="250" cy="250" r="7" fill="#647382"/>
  <circle cx="445" cy="250" r="34" fill="url(#nodeGlow)" filter="url(#softGlow)" opacity="0.9"/>
  <circle cx="445" cy="250" r="13" fill="#FFFFFF" filter="url(#softGlow)"/>
  <circle cx="640" cy="250" r="7" fill="#647382"/>
  <circle cx="835" cy="250" r="7" fill="#647382"/>
  <circle cx="1030" cy="250" r="7" fill="#647382"/>

  <line x1="445" y1="270" x2="445" y2="430" stroke="#FFFFFF" stroke-width="2" opacity="0.96"/>

  <text x="218" y="206" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="700" fill="#728396" text-anchor="middle">01</text>
  <text x="250" y="286" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#9CAEC1" text-anchor="middle" letter-spacing="2">EDUCATION</text>

  <text x="413" y="206" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">02</text>
  <text x="445" y="286" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="2">WORK</text>

  <text x="608" y="206" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="700" fill="#728396" text-anchor="middle">03</text>
  <text x="640" y="286" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#9CAEC1" text-anchor="middle" letter-spacing="2">SKILLS</text>

  <text x="803" y="206" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="700" fill="#728396" text-anchor="middle">04</text>
  <text x="835" y="286" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#9CAEC1" text-anchor="middle" letter-spacing="2">ABOUT</text>

  <text x="998" y="206" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="700" fill="#728396" text-anchor="middle">05</text>
  <text x="1030" y="286" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#9CAEC1" text-anchor="middle" letter-spacing="2">PORTFOLIO</text>

  <rect x="392" y="430" width="510" height="214" rx="22" fill="url(#glassPanel)"
        stroke="#CBD6E2" stroke-opacity="0.18" filter="url(#panelShadow)"/>

  <text x="430" y="482" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">Work Experience</text>
  <text x="432" y="516" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#9EADBD" letter-spacing="2.2">SELECTED PROFESSIONAL CHAPTER</text>

  <text x="430" y="558" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#E7EEF6">
    • Senior Manager at WESTIN Group · 2013–2014
    <tspan x="430" dy="28">• Led cross-functional teams in luxury hospitality</tspan>
    <tspan x="430" dy="28">• Product Manager for digital transformation programs</tspan>
  </text>

  <text x="950" y="632" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#7F91A5" text-anchor="end" letter-spacing="2">ACTIVE SECTION 02 / 05</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` blur directly to the `<image>` if you need guaranteed PPT editability; use a pre-blurred photo asset instead.
- ❌ Using `<mask>` for the dark cinematic overlay; stack semi-transparent `<rect>` overlays and gradients instead.
- ❌ Using `marker-end` arrows for the active drop-line; draw a plain `<line>` and reinforce it with a bright active node.
- ❌ Omitting `width` on any `<text>` element; the PowerPoint translator depends on explicit text widths.
- ❌ Overcrowding the bottom content area with full paragraphs; the stepper aesthetic works best with concise chapter content.

## Composition notes
- Keep the top 15–18% as a fixed global header: logo/title on the left, global traits or navigation metadata on the right.
- Center the horizontal stepper in the upper-middle band, roughly y=230–290, with generous spacing between nodes.
- Use the active node’s vertical drop-line as the organizing spine for the lower content block.
- Maintain a restrained palette: dark blue-black background, muted steel inactive UI, pure white active state, and light slate secondary text.