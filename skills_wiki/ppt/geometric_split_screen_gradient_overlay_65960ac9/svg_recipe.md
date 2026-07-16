# SVG Recipe — Geometric Split-Screen Image Overlay

## Visual mechanism
A full-bleed photograph is divided by a bold geometric color overlay, creating a tinted zone and an untreated image zone. A crisp white boundary line traces the split, while centered framed typography bridges both sides for a cinematic title-slide effect.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph.
- 1× `<rect>` for a subtle full-slide vignette to improve contrast.
- 1× `<path>` for the semi-transparent geometric overlay polygon.
- 1× `<path>` for the thick white split boundary line.
- 1× `<path>` for a thinner accent line parallel to the main split.
- 1× `<rect>` for the transparent central typography frame.
- 3× `<text>` for eyebrow label, main title, and subtitle.
- 1× `<linearGradient>` for the branded overlay tint.
- 1× `<radialGradient>` for the edge-darkening vignette.
- 1× `<filter id="softShadow">` applied to the text frame and typography.
- 1× `<filter id="titleGlow">` applied to the main title for subtle premium glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyMagentaTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071426" stop-opacity="0.88"/>
      <stop offset="52%" stop-color="#142B4B" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#B73572" stop-opacity="0.58"/>
    </linearGradient>

    <radialGradient id="cinematicVignette" cx="50%" cy="44%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.48"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-15%" y="-25%" width="130%" height="150%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1920&h=1080&fit=crop"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#cinematicVignette)"/>

  <path
    d="M 0 0 L 480 0 L 735 720 L 0 720 Z"
    fill="url(#navyMagentaTint)"/>

  <path
    d="M 480 0 L 735 720"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="9"
    stroke-linecap="square"/>

  <path
    d="M 520 0 L 775 720"
    fill="none"
    stroke="#FFFFFF"
    stroke-opacity="0.38"
    stroke-width="2.5"
    stroke-linecap="square"/>

  <rect
    x="290" y="238" width="700" height="244"
    rx="0" ry="0"
    fill="#FFFFFF"
    fill-opacity="0.035"
    stroke="#FFFFFF"
    stroke-width="5"
    filter="url(#softShadow)"/>

  <rect
    x="315" y="263" width="650" height="194"
    fill="none"
    stroke="#FFFFFF"
    stroke-opacity="0.42"
    stroke-width="1.4"/>

  <text
    x="640" y="303"
    width="620"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="17"
    font-weight="600"
    letter-spacing="6"
    fill="#FFFFFF"
    fill-opacity="0.88">
    EXECUTIVE FIELD NOTES
  </text>

  <text
    x="640" y="380"
    width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="66"
    font-weight="800"
    letter-spacing="10"
    fill="#FFFFFF"
    filter="url(#titleGlow)">
    THANK YOU
  </text>

  <text
    x="640" y="428"
    width="560"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="20"
    font-weight="400"
    letter-spacing="2.5"
    fill="#FFFFFF"
    fill-opacity="0.82">
    partnership • clarity • momentum
  </text>

  <line
    x1="500" y1="518" x2="780" y2="518"
    stroke="#FFFFFF"
    stroke-opacity="0.74"
    stroke-width="2"/>

  <text
    x="640" y="552"
    width="520"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="600"
    letter-spacing="3"
    fill="#FFFFFF"
    fill-opacity="0.68">
    2026 STRATEGIC REVIEW
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the tinted side; use a filled `<path>` polygon instead.
- ❌ Do not apply `clip-path` to the overlay shape; clip paths should only be used on `<image>` elements for reliable PowerPoint translation.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the diagonal split; draw the actual polygon points.
- ❌ Do not put shadows or filters on `<line>` elements; use a stroked `<path>` if the boundary needs filtering.
- ❌ Do not rely on transparent PNG overlays when the geometry can be native SVG paths; native paths remain editable in PowerPoint.

## Composition notes
- Keep the photo full bleed, then reserve one 45–60% side of the slide for the tinted geometric overlay.
- Place the title frame near exact center so it visually bridges the raw photo and the tinted zone.
- Use a thick white split line as the main visual anchor; optional thinner parallel lines can add editorial polish.
- Choose high-contrast photography with clear subject separation; landscapes, architecture, and dramatic portraits work especially well.