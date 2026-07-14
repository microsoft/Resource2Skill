# SVG Recipe — Cinematic Calligraphic Epilogue

## Visual mechanism
A full-bleed cinematic landscape is darkened with a subtle vignette, then overlaid with two oversized calligraphic quote lines staggered diagonally across the center. A small red seal stamp near the first line adds a traditional editorial finish and prevents the slide from feeling like a generic “thank you” page.

## SVG primitives needed
- 1× `<image>` for the full-bleed cinematic background photo
- 3× `<rect>` for dark contrast overlay, cinematic letterbox bars, and red seal stamp body
- 2× `<linearGradient>` for top/bottom cinematic shading and horizon-like contrast control
- 1× `<radialGradient>` for center-preserving vignette
- 2× `<filter>` definitions: one soft shadow for calligraphy text, one subtle glow/shadow for the red stamp
- 2× large `<text>` elements for the staggered calligraphic epilogue lines
- 1× small `<text>` element with nested `<tspan>` for the red seal characters
- 2× `<path>` elements for expressive brush-like underline/accent strokes
- 2× small `<text>` elements for optional quiet footer metadata or closing theme

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#020407" stop-opacity="0.68"/>
      <stop offset="26%" stop-color="#020407" stop-opacity="0.18"/>
      <stop offset="62%" stop-color="#020407" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#020407" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="leftDrama" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.56"/>
      <stop offset="42%" stop-color="#000000" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="vignette" cx="52%" cy="46%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.62"/>
    </radialGradient>

    <filter id="calligraphyShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="6" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="stampShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed cinematic landscape -->
  <image
    href="https://images.example.com/cinematic-empty-road-through-mountains-at-dusk-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Contrast system: cinematic bars + layered shade -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaShade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftDrama)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>
  <rect x="0" y="0" width="1280" height="48" fill="#000000" opacity="0.56"/>
  <rect x="0" y="672" width="1280" height="48" fill="#000000" opacity="0.56"/>

  <!-- Quiet cinematic context text -->
  <text x="86" y="94" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" letter-spacing="4"
        fill="#FFFFFF" opacity="0.54">
    EPILOGUE / THE ROAD AHEAD
  </text>

  <!-- First staggered calligraphic line -->
  <text x="298" y="302" width="560"
        font-family="STXingkai, 华文行楷, KaiTi, Microsoft YaHei, Segoe UI"
        font-size="104" font-weight="700"
        letter-spacing="8"
        fill="#FFFFFF"
        filter="url(#calligraphyShadow)"
        transform="rotate(-1.5 298 302)">
    道阻且长
  </text>

  <!-- Fine brush drag under first phrase -->
  <path d="M318 330 C 430 352, 572 347, 704 323"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="5"
        stroke-linecap="round"
        opacity="0.38"/>

  <!-- Red seal stamp, slightly tilted near the end of the first line -->
  <g transform="rotate(5 765 242)" filter="url(#stampShadow)">
    <rect x="737" y="204" width="58" height="72" rx="6"
          fill="#B50909" opacity="0.96"/>
    <rect x="743" y="210" width="46" height="60" rx="3"
          fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.82"/>
    <text x="754" y="235" width="34"
          font-family="KaiTi, Microsoft YaHei, Segoe UI"
          font-size="18" font-weight="700"
          fill="#FFFFFF">
      <tspan x="754" y="235">共</tspan>
      <tspan x="754" y="258">勉</tspan>
    </text>
  </g>

  <!-- Second staggered calligraphic line pushed lower and right -->
  <text x="548" y="476" width="560"
        font-family="STXingkai, 华文行楷, KaiTi, Microsoft YaHei, Segoe UI"
        font-size="104" font-weight="700"
        letter-spacing="8"
        fill="#FFFFFF"
        filter="url(#calligraphyShadow)"
        transform="rotate(1.2 548 476)">
    行则将至
  </text>

  <!-- Second brush accent, shorter and lower -->
  <path d="M574 507 C 664 523, 812 522, 994 490"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="4"
        stroke-linecap="round"
        opacity="0.28"/>

  <!-- Minimal closing attribution -->
  <text x="842" y="604" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17"
        fill="#FFFFFF"
        opacity="0.72">
    向远方，也向答案
  </text>
  <text x="842" y="632" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12"
        letter-spacing="3"
        fill="#FFFFFF"
        opacity="0.42">
    STRATEGY REVIEW · 2026
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the vignette; use layered semi-transparent `<rect>` elements with gradients instead.
- ❌ Do not place the quote in a centered two-line block; the effect depends on asymmetric diagonal staggering.
- ❌ Do not use plain system sans-serif for the main quote unless a calligraphic Chinese font is unavailable.
- ❌ Do not rely on tiny low-contrast text over a bright photo; always add dark overlays behind white calligraphy.
- ❌ Do not use `<animate>` for the brush-wipe reveal in SVG; add wipe animation later in PowerPoint if needed.

## Composition notes
- Keep the quote in the central 50–60% of the canvas, but offset line 1 left/up and line 2 right/down to create cinematic movement.
- Use the background as emotional atmosphere, not content; darken it enough that the white calligraphy dominates immediately.
- The red stamp should be small, imperfectly offset, and close to the first phrase end—an accent, not a logo.
- Maintain generous negative space around the quote; avoid adding charts, icons, or dense footer copy on this closing slide.