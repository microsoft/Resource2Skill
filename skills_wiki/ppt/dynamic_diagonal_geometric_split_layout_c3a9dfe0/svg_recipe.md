# SVG Recipe — Dynamic Diagonal Geometric Split Layout

## Visual mechanism
A full-bleed photo is carved by parallel diagonal polygon slices, then partially covered with bold red-orange and peach geometric blocks. The consistent forward-leaning angles create motion while reserving clean white/red zones for editorial typography and supporting copy.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm red base/background.
- 1× `<image>` for the hero photo, clipped into a diagonal polygonal window.
- 1× `<clipPath>` with a `<path>` applied only to the hero `<image>`.
- 6× `<path>` for the large red wedge, peach slash, cream sliver, dark accent slice, white content panel, and soft panel shadow.
- 2× `<linearGradient>` for premium red background depth and subtle peach accent variation.
- 1× `<filter id="softShadow">` applied to editable polygon panels for depth.
- 1× `<rect>` for the crisp horizontal divider rule.
- 5× `<text>` blocks with explicit `width` for title, subtitle, section heading, body bullets, and photo label.
- 3× simple icon primitives (`<path>`, `<rect>`, `<circle>`) for an editable camera/image-placeholder mark.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="redDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f05a34"/>
      <stop offset="58%" stop-color="#da492d"/>
      <stop offset="100%" stop-color="#b93624"/>
    </linearGradient>

    <linearGradient id="peachSlash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffc2a5"/>
      <stop offset="45%" stop-color="#ff9178"/>
      <stop offset="100%" stop-color="#ef765f"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoDiagonalClip">
      <path d="M520 0 H1280 V430 H386 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#redDepth)"/>

  <image
    href="https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1600&auto=format&fit=crop"
    xlink:href="https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=1600&auto=format&fit=crop"
    x="386" y="0" width="894" height="430"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoDiagonalClip)"/>

  <path d="M0 0 H575 L405 720 H0 Z" fill="#df3f22"/>
  <path d="M168 0 H305 L668 720 H532 Z" fill="url(#peachSlash)"/>
  <path d="M486 0 H530 L357 720 H315 Z" fill="#ffd1b5"/>
  <path d="M760 0 H930 L742 430 H594 Z" fill="#d9361e" opacity="0.95"/>

  <path d="M306 430 H1280 V720 H230 Z" fill="#000000" opacity="0.20" filter="url(#softShadow)"/>
  <path d="M300 430 H1280 V720 H230 Z" fill="#f4f4f2"/>
  <rect x="0" y="430" width="1280" height="4" fill="#ffffff" opacity="0.85"/>

  <path d="M1088 0 H1280 V220 H1195 Z" fill="#ff947c"/>
  <path d="M1126 0 H1172 L1280 184 V242 Z" fill="#ffd1b5"/>
  <path d="M1044 0 H1125 L1280 278 V346 Z" fill="#ff8f76"/>

  <path d="M40 472 H390 L315 720 H0 V505 Z" fill="#cf3b24" opacity="0.88"/>
  <path d="M40 472 H385 L373 510 H30 Z" fill="#f16c4a" opacity="0.55"/>

  <text x="452" y="492" width="740"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="40" font-weight="800" fill="#d94427" letter-spacing="1">
    Engineer Haroon Mentor
  </text>

  <text x="458" y="535" width="640"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#9c5b4c" letter-spacing="12">
    GEOMETRIC GRAPHIC DESIGN
  </text>

  <text x="48" y="510" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#ffd6c8" letter-spacing="1">
    TITLE OF YOUR SLIDE
  </text>

  <text x="48" y="545" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#fff0e8">
    <tspan x="48" dy="0">• Welcome to a high-impact section</tspan>
    <tspan x="48" dy="22">  opener with editable diagonal shapes.</tspan>
    <tspan x="48" dy="26">• Use the red field for short copy,</tspan>
    <tspan x="48" dy="22">  bullets, or a compact data callout.</tspan>
    <tspan x="48" dy="26">• Keep all edges parallel for a</tspan>
    <tspan x="48" dy="22">  fast, premium keynote rhythm.</tspan>
  </text>

  <text x="785" y="610" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="800" fill="#d94427">
    TITLE OF YOUR SECTION
  </text>

  <text x="785" y="642" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#b97867" letter-spacing="7">
    FORWARD MOTION LAYOUT
  </text>

  <rect x="608" y="36" width="54" height="42" rx="6" fill="#111111"/>
  <path d="M620 36 L628 20 H645 L653 36 Z" fill="#111111"/>
  <circle cx="635" cy="57" r="14" fill="#e9eef2"/>
  <circle cx="635" cy="57" r="8" fill="#111111"/>
  <path d="M590 52 H604 V38 H616 V52 H630 V64 H616 V78 H604 V64 H590 Z" fill="#111111"/>
  <text x="604" y="97" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800" fill="#111111">
    Image Placeholder
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut the photo; use a `<clipPath>` on the `<image>` or simply cover the image with editable polygons.
- ❌ Do not place `clip-path` on polygon/text shapes; PowerPoint translation only preserves clipping reliably for images.
- ❌ Do not use `<pattern>` fills for diagonal texture; use real polygon strips or gradients instead.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to create slants; draw the final trapezoid/parallelogram coordinates directly.
- ❌ Do not rely on `marker-end` arrows for motion cues; the diagonal geometry itself should create the sense of speed.

## Composition notes
- Keep all major diagonal edges parallel, usually leaning from upper-left to lower-right, to make the irregular split feel intentional.
- Reserve one clean text zone: either a solid red left wedge or a white bottom band; avoid placing body copy over detailed photography.
- Use a three-color rhythm: dominant red-orange, secondary peach, and neutral white/off-white.
- Let the photo occupy roughly the upper-right half of the slide, while diagonal overlays hide its rectangular boundaries.