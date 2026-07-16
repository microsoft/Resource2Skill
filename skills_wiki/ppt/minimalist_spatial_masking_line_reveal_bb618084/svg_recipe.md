# SVG Recipe — Minimalist Spatial Masking & Line Reveal

## Visual mechanism
A bold text lockup is placed beneath a moving “matte” layer, with a thin accent line sitting exactly on the matte’s leading edge. When the matte and line slide together, the line appears to cut open the space and reveal the typography with a premium editorial wipe effect.

## SVG primitives needed
- 2× `<image>` for the cinematic background: one full-slide hero photo, one clipped duplicate used as the spatial mask over text
- 1× `<clipPath>` with `<rect>` for the moving image-mask region
- 5× `<rect>` for black base, dark cinematic overlays, accent reveal line, mask darkening veil, and tilted presentation-card panels
- 4× `<text>` for the large title typography and the small “P” inside the presentation icon
- 2× `<path>` for simplified PowerPoint/document icon details
- 1× `<linearGradient>` for top-to-bottom cinematic darkening
- 1× `<radialGradient>` for edge vignette depth
- 2× `<filter>` definitions for soft title/card shadows applied to text and rectangles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinematicShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#020305" stop-opacity="0.88"/>
      <stop offset="42%" stop-color="#121722" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#020305" stop-opacity="0.82"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="72%" stop-color="#000000" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <filter id="titleShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Animate this rect and the orange line together in PowerPoint for the reveal. -->
    <clipPath id="wipePhotoClip">
      <rect x="970" y="92" width="310" height="250"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <image
    href="https://images.example.com/cinematic-snow-mountain-night-sky.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#cinematicShade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <!-- Bottom layer: typography that will be revealed. -->
  <text x="145" y="198" width="1000"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="800" letter-spacing="2"
        fill="#ffffff" filter="url(#titleShadow)">REVEAL TEXT</text>

  <text x="142" y="318" width="1080"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="102" font-weight="900" letter-spacing="5"
        fill="#c94621" stroke="#ffffff" stroke-width="5"
        filter="url(#titleShadow)">ON CLICK</text>

  <!-- Middle layer: clipped duplicate background, parked just after the revealed title.
       Move this clipped image region left/right with the line for a true spatial wipe. -->
  <image
    href="https://images.example.com/cinematic-snow-mountain-night-sky.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#wipePhotoClip)"/>

  <!-- Dark veil matching the global grade inside the mask zone; keep aligned with clip rect. -->
  <rect x="970" y="92" width="310" height="250" fill="#05070b" opacity="0.46"/>

  <!-- Top layer: the reveal blade / anchor line. -->
  <rect x="960" y="90" width="8" height="258" rx="4" fill="#d96a22"/>

  <!-- Presentation icon card, echoing the reference thumbnail style. -->
  <g transform="rotate(6 610 510)">
    <rect x="505" y="395" width="210" height="176" rx="2"
          fill="#ffffff" filter="url(#cardShadow)"/>
    <rect x="520" y="410" width="180" height="146" rx="1"
          fill="#d84b25"/>

    <rect x="558" y="446" width="76" height="72" rx="2" fill="#ffffff"/>
    <text x="582" y="497" width="42"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="38" font-weight="800"
          fill="#d84b25">P</text>

    <path d="M628 456 L670 466 L670 510 L628 520 Z"
          fill="none" stroke="#ffffff" stroke-width="7" stroke-linejoin="round"/>
    <path d="M646 473 C658 473 664 481 664 489 C664 499 657 505 646 505
             L646 493 C651 493 654 491 654 488 C654 485 651 483 646 483 Z"
          fill="#ffffff"/>
  </g>

  <!-- Optional tiny construction cue; remove for final cinematic use. -->
  <text x="145" y="606" width="720"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="600" letter-spacing="1.5"
        fill="#ffffff" opacity="0.58">LINE + MASK MOVE TOGETHER</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<mask>` or `mask="url(#...)"`; use physical layering or a clipped duplicate image instead
- ❌ Applying `clip-path` to text or rectangles; PPT-Master only preserves clip paths reliably on `<image>`
- ❌ Relying on native PowerPoint “Wipe” as the visual mechanism; the premium effect comes from moving the matte and line as objects
- ❌ Putting a filter on the accent `<line>` or using `<line>` with shadow; use a thin `<rect>` for the reveal blade
- ❌ Using a photo background with only a flat-color mask unless the slide background is also flat; for image backgrounds, duplicate and clip the photo so the mask visually matches

## Composition notes
- Keep the text large and left-weighted, with enough negative space on the right for the mask to park offstage.
- The accent line should be slightly taller than the text block and sit exactly on the mask’s leading edge.
- For photo backgrounds, darken the whole image first, then duplicate the same image inside the mask area so the covered text disappears cleanly.
- Use one strong accent color only; the line and any highlighted word/icon should share that hue for a polished keynote rhythm.