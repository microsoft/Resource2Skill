# SVG Recipe — Panoramic Chevron Reveal Slide

## Visual mechanism
A widescreen slide is divided by nested, full-height chevron ribbons that all share the same forward-pointing slope, creating momentum and depth. A clipped panoramic photo sits inside the central chevron, while bright accent bands, a white reveal panel, and a bold blue arrow title block create an executive keynote-style reveal.

## SVG primitives needed
- 1× `<rect>` for the deep navy full-slide background
- 6× `<path>` for layered chevron ribbons, accent bands, white reveal panel, and hero arrow
- 1× `<image>` clipped into a custom chevron photo crop
- 1× `<clipPath>` with a `<path>` for the panoramic chevron image crop
- 2× `<linearGradient>` for premium background and hero-arrow fills
- 1× `<filter id="ribbonShadow">` with offset blur shadow applied to major chevron paths
- 3× `<text>` elements with explicit `width` attributes for title, subtitle, and small eyebrow label
- 2× decorative dashed `<path>` strokes following the same chevron slope rhythm

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="55%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="blueArrow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="52%" stop-color="#0ea5e9"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <linearGradient id="yellowBand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fde047"/>
      <stop offset="100%" stop-color="#facc15"/>
    </linearGradient>

    <filter id="ribbonShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="16" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoChevron">
      <path d="M410 0 L910 0 L1170 360 L910 720 L410 720 L670 360 Z"/>
    </clipPath>
  </defs>

  <!-- base canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- deep left structural chevron -->
  <path d="M-80 0 L395 0 L655 360 L395 720 L-80 720 Z"
        fill="#1e293b" opacity="0.95"/>

  <!-- darker inner depth fold -->
  <path d="M270 0 L355 0 L615 360 L355 720 L270 720 L530 360 Z"
        fill="#0f172a" opacity="0.88"/>

  <!-- bright reveal accent band -->
  <path d="M350 0 L435 0 L695 360 L435 720 L350 720 L610 360 Z"
        fill="url(#yellowBand)" filter="url(#ribbonShadow)"/>

  <!-- photo chevron shadow, then clipped panoramic photo -->
  <path d="M410 0 L910 0 L1170 360 L910 720 L410 720 L670 360 Z"
        fill="#000000" opacity="0.32" filter="url(#ribbonShadow)"/>

  <image x="360" y="-20" width="880" height="760"
         href="https://images.example.com/panoramic-modern-city-architecture-blue-hour.jpg"
         xlink:href="https://images.example.com/panoramic-modern-city-architecture-blue-hour.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoChevron)"/>

  <!-- subtle blue glaze over the photo shape for palette unity -->
  <path d="M410 0 L910 0 L1170 360 L910 720 L410 720 L670 360 Z"
        fill="#0284c7" opacity="0.16"/>

  <!-- white reveal block on the right, sharing identical chevron slope -->
  <path d="M860 0 L1280 0 L1280 720 L860 720 L1120 360 Z"
        fill="#ffffff" filter="url(#ribbonShadow)"/>

  <!-- hero title arrow sitting on the white reveal panel -->
  <path d="M755 130 L1055 130 L1195 360 L1055 590 L755 590 L895 360 Z"
        fill="url(#blueArrow)" filter="url(#ribbonShadow)"/>

  <!-- slope-following editorial guide accents -->
  <path d="M300 58 L558 360 L300 662"
        fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="8 12" opacity="0.55"/>
  <path d="M468 42 L728 360 L468 678"
        fill="none" stroke="#ffffff" stroke-width="2" stroke-dasharray="10 14" opacity="0.42"/>

  <!-- left eyebrow label -->
  <text x="58" y="86" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3"
        fill="#f8fafc" opacity="0.92">
    STRATEGY FORWARD
  </text>

  <!-- main title inside arrow -->
  <text x="975" y="388" width="340"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="800"
        fill="#ffffff">
    2026
  </text>

  <!-- subtitle on clean white reveal field -->
  <text x="905" y="638" width="300"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" letter-spacing="2.5"
        fill="#0f172a">
    GLOBAL VISION &amp; STRATEGY
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the chevron photo crop; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not clip groups or colored `<path>` elements; PPT-Master only preserves clipping reliably for images.
- ❌ Do not use `marker-end` for directional arrows; the chevron geometry itself should communicate motion.
- ❌ Do not mix different slant angles across layers; the premium look depends on strict parallelism.
- ❌ Do not flatten the whole composition into one bitmap; keep ribbons, text, and chevrons editable.

## Composition notes
- Keep the strongest visual mass on the right two-thirds: panoramic photo, white reveal block, and blue title arrow.
- Reserve the left edge for dark negative space and a small label so the chevrons feel like they are launching from off-canvas.
- Use one vivid warm accent band and one cool hero arrow; too many saturated bands will weaken the hierarchy.
- Make every major chevron share the same slope delta, e.g. top edge to point to bottom edge uses a consistent 260px horizontal shift.