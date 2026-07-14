# SVG Recipe — Focal Spotlight Title

## Visual mechanism
A full-bleed atmospheric photo is dimmed with subtle edge vignettes, then a large centered soft-edged dark circle creates a readable “spotlight” container for the title. White centered typography sits inside the circle, producing a cinematic chapter-divider or keynote title slide.

## SVG primitives needed
- 1× `<image>` for the full-slide background photograph.
- 2× full-canvas `<rect>` overlays for global darkening and top/bottom cinematic shading.
- 1× `<circle>` with radial gradient fill for the central semi-transparent spotlight.
- 1× `<filter id="spotlightBlur">` with `feGaussianBlur` applied to the circle for feathered edges.
- 1× `<filter id="textGlow">` with blur/merge applied to title text for subtle readability lift.
- 2× `<text>` elements for subtitle and main title, both centered and with explicit `width`.
- 2× decorative `<line>` elements for understated divider ticks around the subtitle.
- 1× small `<circle>` accent dot to reinforce the centered focal axis.
- Multiple `<linearGradient>` / `<radialGradient>` definitions for vignette, spotlight fade, and cinematic shading.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.58"/>
      <stop offset="22%" stop-color="#000000" stop-opacity="0.12"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.55"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="50%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.58"/>
    </radialGradient>

    <radialGradient id="spotlightFade" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.74"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.70"/>
      <stop offset="82%" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="spotlightBlur" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>

    <filter id="textGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2.5" result="blur"/>
      <feOffset in="blur" dx="0" dy="2" result="offsetBlur"/>
      <feMerge>
        <feMergeNode in="offsetBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#071018" opacity="0.18"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaShade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <circle
    cx="640" cy="360" r="238"
    fill="url(#spotlightFade)"
    filter="url(#spotlightBlur)"/>

  <circle
    cx="640" cy="360" r="151"
    fill="#000000"
    opacity="0.18"/>

  <line x1="468" y1="294" x2="552" y2="294"
        stroke="#FFFFFF" stroke-opacity="0.58" stroke-width="1.4"/>
  <line x1="728" y1="294" x2="812" y2="294"
        stroke="#FFFFFF" stroke-opacity="0.58" stroke-width="1.4"/>
  <circle cx="640" cy="294" r="3.5" fill="#FFFFFF" opacity="0.75"/>

  <text
    x="340" y="300"
    width="600"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="600"
    letter-spacing="3.2"
    fill="#FFFFFF"
    opacity="0.92">
    <tspan x="640">FOUR PRINCIPLES OF TYPOGRAPHY</tspan>
  </text>

  <text
    x="240" y="378"
    width="800"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="58"
    font-weight="800"
    letter-spacing="-1.4"
    fill="#FFFFFF"
    filter="url(#textGlow)">
    <tspan x="640">Alignment</tspan>
    <tspan x="640" dy="66">Principle</tspan>
  </text>

  <text
    x="390" y="506"
    width="500"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="17"
    font-weight="400"
    fill="#FFFFFF"
    opacity="0.78">
    <tspan x="640">Create order by connecting every element to a clear visual axis.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not blur or darken the background by rasterizing it into a precomposited image; keep the photo and overlays editable as separate SVG/PPT layers.
- ❌ Do not use `<mask>` to create the spotlight fade; use a radial gradient fill and/or Gaussian blur on a circle.
- ❌ Do not place text directly on the photo without the dark circular container; the technique depends on high-contrast readability.
- ❌ Do not use `clip-path` on the circle or text; clipping is only reliable for `<image>` elements in this workflow.
- ❌ Do not use tiny body text inside the spotlight; the design is for large section-title hierarchy, not dense content.

## Composition notes
- Keep the spotlight centered; its diameter should be roughly 50–60% of slide height for a premium title-card feel.
- Choose a background image with mood and texture, but avoid a busy central subject competing with the text.
- Let the title occupy the visual center, with subtitle above and optional one-line descriptor below.
- Use white typography, restrained letter spacing, and subtle divider lines to create ceremony without clutter.