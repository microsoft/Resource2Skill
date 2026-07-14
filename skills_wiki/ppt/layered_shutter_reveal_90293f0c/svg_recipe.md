# SVG Recipe — Layered Shutter Reveal

## Visual mechanism
A full-bleed hero image is duplicated into skewed vertical slices so the slices visually match the background beneath them, like shutters made from the photograph itself. Each shutter panel has a soft offset shadow and subtle glossy overlay, creating the illusion that the image is peeling open to reveal the central title.

## SVG primitives needed
- 1× full-slide `<image>` for the unobstructed hero background.
- 10× `<clipPath>` with `<path>` silhouettes for left/right parallelogram shutter slices.
- 10× clipped `<image>` elements, each using the same full-slide image and one clipPath so every panel aligns perfectly with the background.
- 10× `<path>` shadow silhouettes behind the panels, using a blur/offset filter.
- 10× `<path>` glossy overlays on top of the clipped images to add depth and premium shutter sheen.
- 10× `<path>` thin edge strokes to make each panel feel like a physical moving layer.
- 1× `<rect>` with a radial vignette gradient to darken the edges and focus attention toward center.
- 1× `<text>` title with nested `<tspan>` styling.
- 1× `<text>` subtitle/kicker.
- 2× `<filter>` definitions: one for panel shadows, one for text shadow/glow.
- 3× gradient definitions for vignette and left/right panel gloss.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.62"/>
    </radialGradient>

    <linearGradient id="glossLeft" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#06111F" stop-opacity="0.48"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="glossRight" x1="100%" y1="0%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#06111F" stop-opacity="0.48"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.28"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset in="SourceAlpha" dx="18" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset in="SourceAlpha" dx="0" dy="6" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipL1"><path d="M500 0 L650 0 L585 720 L435 720 Z"/></clipPath>
    <clipPath id="clipL2"><path d="M410 0 L560 0 L495 720 L345 720 Z"/></clipPath>
    <clipPath id="clipL3"><path d="M320 0 L470 0 L405 720 L255 720 Z"/></clipPath>
    <clipPath id="clipL4"><path d="M230 0 L380 0 L315 720 L165 720 Z"/></clipPath>
    <clipPath id="clipL5"><path d="M140 0 L290 0 L225 720 L75 720 Z"/></clipPath>
    <clipPath id="clipR1"><path d="M630 0 L780 0 L845 720 L695 720 Z"/></clipPath>
    <clipPath id="clipR2"><path d="M720 0 L870 0 L935 720 L785 720 Z"/></clipPath>
    <clipPath id="clipR3"><path d="M810 0 L960 0 L1025 720 L875 720 Z"/></clipPath>
    <clipPath id="clipR4"><path d="M900 0 L1050 0 L1115 720 L965 720 Z"/></clipPath>
    <clipPath id="clipR5"><path d="M990 0 L1140 0 L1205 720 L1055 720 Z"/></clipPath>
  </defs>

  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M140 0 L290 0 L225 720 L75 720 Z" fill="#000000" opacity="0.38" filter="url(#panelShadow)"/>
  <path d="M230 0 L380 0 L315 720 L165 720 Z" fill="#000000" opacity="0.35" filter="url(#panelShadow)"/>
  <path d="M320 0 L470 0 L405 720 L255 720 Z" fill="#000000" opacity="0.33" filter="url(#panelShadow)"/>
  <path d="M410 0 L560 0 L495 720 L345 720 Z" fill="#000000" opacity="0.31" filter="url(#panelShadow)"/>
  <path d="M500 0 L650 0 L585 720 L435 720 Z" fill="#000000" opacity="0.30" filter="url(#panelShadow)"/>
  <path d="M630 0 L780 0 L845 720 L695 720 Z" fill="#000000" opacity="0.30" filter="url(#panelShadow)"/>
  <path d="M720 0 L870 0 L935 720 L785 720 Z" fill="#000000" opacity="0.31" filter="url(#panelShadow)"/>
  <path d="M810 0 L960 0 L1025 720 L875 720 Z" fill="#000000" opacity="0.33" filter="url(#panelShadow)"/>
  <path d="M900 0 L1050 0 L1115 720 L965 720 Z" fill="#000000" opacity="0.35" filter="url(#panelShadow)"/>
  <path d="M990 0 L1140 0 L1205 720 L1055 720 Z" fill="#000000" opacity="0.38" filter="url(#panelShadow)"/>

  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipL5)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipL4)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipL3)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipL2)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipL1)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipR1)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipR2)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipR3)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipR4)"/>
  <image href="https://images.unsplash.com/photo-1549880181-56a44cf4a9a5?w=1600&amp;h=900&amp;fit=crop&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipR5)"/>

  <path d="M500 0 L650 0 L585 720 L435 720 Z" fill="url(#glossLeft)" opacity="0.45" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.5"/>
  <path d="M410 0 L560 0 L495 720 L345 720 Z" fill="url(#glossLeft)" opacity="0.38" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1.5"/>
  <path d="M320 0 L470 0 L405 720 L255 720 Z" fill="url(#glossLeft)" opacity="0.34" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1.5"/>
  <path d="M230 0 L380 0 L315 720 L165 720 Z" fill="url(#glossLeft)" opacity="0.31" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1.5"/>
  <path d="M140 0 L290 0 L225 720 L75 720 Z" fill="url(#glossLeft)" opacity="0.28" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1.5"/>
  <path d="M630 0 L780 0 L845 720 L695 720 Z" fill="url(#glossRight)" opacity="0.45" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.5"/>
  <path d="M720 0 L870 0 L935 720 L785 720 Z" fill="url(#glossRight)" opacity="0.38" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1.5"/>
  <path d="M810 0 L960 0 L1025 720 L875 720 Z" fill="url(#glossRight)" opacity="0.34" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1.5"/>
  <path d="M900 0 L1050 0 L1115 720 L965 720 Z" fill="url(#glossRight)" opacity="0.31" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1.5"/>
  <path d="M990 0 L1140 0 L1205 720 L1055 720 Z" fill="url(#glossRight)" opacity="0.28" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1.5"/>

  <text x="640" y="326" width="720" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="700" fill="#FFFFFF" letter-spacing="2" filter="url(#titleShadow)">
    <tspan x="640">UNVEILED</tspan>
    <tspan x="640" dy="84" font-size="48" font-weight="300" letter-spacing="12">FUTURE</tspan>
  </text>
  <text x="640" y="482" width="560" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#D9F2FF" letter-spacing="5" opacity="0.92">
    CINEMATIC PRODUCT REVEAL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; create the static editable panels, then apply PowerPoint Fly Out animations manually.
- ❌ Do not use `<mask>` to reveal the image; PPT translation can hard-fail or ignore it.
- ❌ Do not put `clip-path` on a `<g>` or `<path>`; for this technique, apply clip paths directly to the duplicated `<image>` elements only.
- ❌ Do not use `<use>` to duplicate panel shapes; repeat the paths explicitly so PPT-Master can convert them into editable shapes.
- ❌ Do not rely on `marker-end` or line filters for motion cues; if needed, use native PowerPoint animation directions instead.

## Composition notes
- Keep the title centered in the vertical reveal gap; the shutters should frame it without fully blocking legibility.
- Use 4–6 panels per side, with slight overlap and mirrored slants, to create a premium mechanical shutter rhythm.
- The same hero image must be used for the background and every clipped panel, all positioned at `x=0 y=0 width=1280 height=720`, so the image alignment is seamless.
- For the animated version in PowerPoint, send left-side panels Fly Out Left and right-side panels Fly Out Right, all “With Previous,” around 1.2–1.8 seconds.