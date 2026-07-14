# SVG Recipe — Parallax Glass Pane Reveal

## Visual mechanism
A cinematic full-bleed photo is fractured by several tall, angled “glass” panes that show slightly offset copies of the same image, creating a static parallax illusion. Soft shadows, translucent edge highlights, and a centered title corridor make the slide feel dimensional and premium even before adding optional PowerPoint motion.

## SVG primitives needed
- 1× full-slide `<image>` for the scenic background photo
- 1× `<rect>` with gradient fill for a dark cinematic overlay
- 4× `<clipPath>` with angled `<path>` shapes for the pane image windows
- 4× clipped `<image>` duplicates for the parallax pane reveals
- 4× shadow `<path>` shapes behind panes using `filter id="paneShadow"`
- 4× translucent glass `<path>` overlays for frosted tint and pane borders
- 4× narrow `<path>` highlight strokes for glossy pane edges
- 1× `<radialGradient>` vignette for center emphasis
- 1× `<linearGradient>` for darkening the background edges
- 1× `<filter>` for soft pane shadows
- 3× `<text>` elements for eyebrow, main title, and subtitle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.62"/>
      <stop offset="46%" stop-color="#07111f" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.74"/>
    </linearGradient>

    <radialGradient id="centerLift" cx="50%" cy="48%" r="58%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="58%" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.36"/>
    </radialGradient>

    <linearGradient id="glassTint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#7dd3fc" stop-opacity="0.14"/>
    </linearGradient>

    <filter id="paneShadow" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset dx="16" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <clipPath id="paneLeftWide" clipPathUnits="userSpaceOnUse">
      <path d="M170 -40 L425 -40 L260 760 L-10 760 Z"/>
    </clipPath>
    <clipPath id="paneLeftNarrow" clipPathUnits="userSpaceOnUse">
      <path d="M455 -40 L650 -40 L560 760 L345 760 Z"/>
    </clipPath>
    <clipPath id="paneRightNarrow" clipPathUnits="userSpaceOnUse">
      <path d="M720 -40 L915 -40 L820 760 L610 760 Z"/>
    </clipPath>
    <clipPath id="paneRightWide" clipPathUnits="userSpaceOnUse">
      <path d="M960 -40 L1220 -40 L1300 760 L1030 760 Z"/>
    </clipPath>
  </defs>

  <image href="https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=1600&amp;h=900&amp;fit=crop"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaShade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerLift)"/>

  <path d="M170 -40 L425 -40 L260 760 L-10 760 Z" fill="#000000" opacity="0.32" filter="url(#paneShadow)"/>
  <path d="M455 -40 L650 -40 L560 760 L345 760 Z" fill="#000000" opacity="0.26" filter="url(#paneShadow)"/>
  <path d="M720 -40 L915 -40 L820 760 L610 760 Z" fill="#000000" opacity="0.28" filter="url(#paneShadow)"/>
  <path d="M960 -40 L1220 -40 L1300 760 L1030 760 Z" fill="#000000" opacity="0.34" filter="url(#paneShadow)"/>

  <image href="https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=1600&amp;h=900&amp;fit=crop"
         x="-48" y="-18" width="1376" height="774" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#paneLeftWide)" opacity="0.98"/>
  <image href="https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=1600&amp;h=900&amp;fit=crop"
         x="18" y="-30" width="1328" height="747" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#paneLeftNarrow)" opacity="0.96"/>
  <image href="https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=1600&amp;h=900&amp;fit=crop"
         x="-18" y="24" width="1328" height="747" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#paneRightNarrow)" opacity="0.96"/>
  <image href="https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=1600&amp;h=900&amp;fit=crop"
         x="44" y="-16" width="1376" height="774" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#paneRightWide)" opacity="0.98"/>

  <path d="M170 -40 L425 -40 L260 760 L-10 760 Z" fill="url(#glassTint)" stroke="#ffffff" stroke-opacity="0.34" stroke-width="1.5"/>
  <path d="M455 -40 L650 -40 L560 760 L345 760 Z" fill="url(#glassTint)" stroke="#ffffff" stroke-opacity="0.26" stroke-width="1.25"/>
  <path d="M720 -40 L915 -40 L820 760 L610 760 Z" fill="url(#glassTint)" stroke="#ffffff" stroke-opacity="0.26" stroke-width="1.25"/>
  <path d="M960 -40 L1220 -40 L1300 760 L1030 760 Z" fill="url(#glassTint)" stroke="#ffffff" stroke-opacity="0.34" stroke-width="1.5"/>

  <path d="M424 -38 L259 758" fill="none" stroke="#ffffff" stroke-opacity="0.50" stroke-width="2.2"/>
  <path d="M650 -38 L560 758" fill="none" stroke="#dff8ff" stroke-opacity="0.34" stroke-width="1.6"/>
  <path d="M720 -38 L610 758" fill="none" stroke="#dff8ff" stroke-opacity="0.30" stroke-width="1.6"/>
  <path d="M960 -38 L1030 758" fill="none" stroke="#ffffff" stroke-opacity="0.48" stroke-width="2.2"/>

  <rect x="330" y="242" width="620" height="246" rx="30" fill="#020617" opacity="0.22"/>
  <text x="640" y="292" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" letter-spacing="5"
        fill="#bae6fd" opacity="0.96">WELCOME TO THE</text>
  <text x="640" y="376" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="800"
        letter-spacing="2" fill="#ffffff" filter="url(#titleGlow)">MOUNTAIN LAB</text>
  <text x="640" y="428" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24"
        fill="#e0f2fe" opacity="0.88">A premium launch experience built with depth, motion, and light</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the pane cutouts; use `<clipPath>` applied directly to duplicate `<image>` elements.
- ❌ Do not apply `clip-path` to glass tint `<path>` elements; clipping non-image elements may be ignored by the PPT translator.
- ❌ Do not rely on SVG animation tags for the parallax reveal; recreate the static look in SVG, then add PowerPoint motion paths or grow/shrink manually if needed.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to make panes; draw the parallelogram geometry directly with `<path>`.
- ❌ Do not place text too close to pane edges; the panes should frame the title, not compete with it.

## Composition notes
- Keep the title in the central 40–50% of the slide width, with panes forming a loose corridor around it.
- Use 3–5 panes maximum; vary their widths and image offsets so the background feels fragmented rather than tiled.
- Darken the base photo enough that white typography remains crisp, but let the clipped panes stay slightly brighter for the “reveal” effect.
- For optional PowerPoint animation, move the base background slowly one direction and the pane images slightly the opposite direction with auto-reverse.