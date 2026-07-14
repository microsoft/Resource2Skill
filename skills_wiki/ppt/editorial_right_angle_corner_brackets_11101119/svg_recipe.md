# SVG Recipe — Editorial Right-Angle Corner Brackets

## Visual mechanism
Minimal 90-degree corner brackets define an implied frame around centered typography, creating editorial structure without covering the photograph. A full-bleed image, dark overlay, and restrained white linework make the text feel anchored, intentional, and magazine-like.

## SVG primitives needed
- 1× `<image>` for the full-bleed thematic photo background
- 2× `<rect>` for translucent darkening overlays / vignette wash
- 4× `<path>` for the disconnected L-shaped corner brackets
- 2× `<line>` for subtle editorial guide ticks near the subtitle
- 3× `<text>` for large title, subtitle, and small deck label
- 1× `<linearGradient>` for a left-to-right photographic readability overlay
- 1× `<radialGradient>` for soft center focus / edge darkening
- 1× `<filter id="softShadow">` applied to brackets and text for subtle separation
- 1× `<filter id="titleGlow">` applied to the main title for gentle photo-background legibility

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="readabilityWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="42%" stop-color="#000000" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.48"/>
    </linearGradient>

    <radialGradient id="centerLift" cx="50%" cy="48%" r="62%">
      <stop offset="0%" stop-color="#1F3F2A" stop-opacity="0.05"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.44"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="2.4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1515823064-d6e0c04616a7?auto=format&amp;fit=crop&amp;w=1920&amp;q=85"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#readabilityWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerLift)"/>

  <text x="72" y="70" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="3"
        fill="#FFFFFF" opacity="0.78">
    ORIGIN / TERROIR
  </text>

  <line x1="515" y1="505" x2="590" y2="505"
        stroke="#FFFFFF" stroke-width="1.4" stroke-opacity="0.55"/>
  <line x1="690" y1="505" x2="765" y2="505"
        stroke="#FFFFFF" stroke-width="1.4" stroke-opacity="0.55"/>

  <text x="640" y="334" width="700"
        text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="118" font-weight="700"
        letter-spacing="18"
        fill="#FFFFFF"
        filter="url(#titleGlow)">
    抹 茶
  </text>

  <text x="640" y="454" width="560"
        text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="24" font-weight="400"
        letter-spacing="13"
        fill="#E9E6DA" opacity="0.92"
        filter="url(#softShadow)">
    三 大 產 地
  </text>

  <path d="M 424 258 L 424 202 L 492 202"
        fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="square" stroke-linejoin="miter"
        filter="url(#softShadow)"/>

  <path d="M 856 258 L 856 202 L 788 202"
        fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="square" stroke-linejoin="miter"
        filter="url(#softShadow)"/>

  <path d="M 424 430 L 424 486 L 492 486"
        fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="square" stroke-linejoin="miter"
        filter="url(#softShadow)"/>

  <path d="M 856 430 L 856 486 L 788 486"
        fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="square" stroke-linejoin="miter"
        filter="url(#softShadow)"/>

  <text x="640" y="622" width="420"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="500"
        letter-spacing="2.5"
        fill="#FFFFFF" opacity="0.55">
    AN EDITORIAL FIELD GUIDE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Drawing a complete rectangle around the text; the premium effect depends on implied boundaries and open negative space.
- ❌ Using `<marker-end>` or arrow shapes for the brackets; use direct L-shaped `<path>` geometry instead.
- ❌ Applying `clip-path` or masks to bracket paths; clipping is only reliable on `<image>` elements.
- ❌ Heavy opaque backing boxes behind the title; they defeat the “floating editorial frame” feel.
- ❌ Very long bracket arms; keep each arm roughly 15–25% of the implied frame width/height.

## Composition notes
- Keep the bracket frame wider and taller than the title block, leaving generous breathing room on all sides.
- Use a full-bleed photo with darker, low-detail space behind the typography; add a subtle overlay rather than a solid panel.
- Place the main title near optical center, with the subtitle close enough to read as one editorial unit.
- Use white or warm off-white brackets/text; let the photograph provide the color richness while the frame stays minimal.