# SVG Recipe — Cinematic Full-Bleed Impact Slide

## Visual mechanism
A full-bleed cinematic photo becomes a dark atmospheric canvas through a semi-transparent black overlay, vignette, and subtle color haze. Large left-aligned typography carries the message, with a few key phrases highlighted in a vivid accent color to create instant visual focus.

## SVG primitives needed
- 1× `<image>` for the full-canvas photographic background
- 2× `<rect>` for the dark dimming overlay and directional readability gradient
- 2× `<ellipse>` for blurred cinematic color blooms over the photo
- 1× `<path>` for a soft abstract accent sweep in the lower-right background
- 1× `<radialGradient>` for the vignette overlay
- 1× `<linearGradient>` for the left-to-right readability shade
- 2× `<filter>` using `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for haze and text shadow
- 3× `<text>` blocks for the small kicker, the main impact statement, and the closing label
- Multiple nested `<tspan>` elements for inline accent-color highlighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="readabilityShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.72"/>
      <stop offset="48%" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.10"/>
    </linearGradient>

    <radialGradient id="vignette" cx="50%" cy="48%" r="75%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="68%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.68"/>
    </radialGradient>

    <linearGradient id="accentSweep" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFC000" stop-opacity="0.28"/>
      <stop offset="52%" stop-color="#FF5A00" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#6A2DFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>

    <filter id="typeShadow" x="-10%" y="-10%" width="120%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.example.com/cinematic-abstract-colorful-powder-splash-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.46"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#readabilityShade)"/>

  <ellipse cx="1085" cy="155" rx="260" ry="170" fill="#7B2CFF" opacity="0.22" filter="url(#softBlur)"/>
  <ellipse cx="1015" cy="590" rx="340" ry="120" fill="#FFC000" opacity="0.14" filter="url(#softBlur)"/>

  <path
    d="M815,720 C900,640 1000,625 1090,565 C1172,510 1235,428 1280,338 L1280,720 Z"
    fill="url(#accentSweep)"
    opacity="0.78"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <text
    x="154" y="138"
    width="760"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="700"
    letter-spacing="3"
    fill="#FFC000"
    opacity="0.95">
    EXECUTIVE IMPACT / 2026
  </text>

  <text
    x="150" y="250"
    width="940"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="62"
    font-weight="800"
    line-height="1.08"
    fill="#FFFFFF"
    filter="url(#typeShadow)">
    <tspan x="150" dy="0">By combining a template,</tspan>
    <tspan x="150" dy="72">custom colors, a high-quality</tspan>
    <tspan x="150" dy="72">image, and a modern font,</tspan>
    <tspan x="150" dy="72">we create </tspan>
    <tspan fill="#FFC000">real impact</tspan>
    <tspan fill="#FFFFFF">.</tspan>
  </text>

  <text
    x="154" y="642"
    width="680"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="22"
    font-weight="500"
    fill="#FFFFFF"
    opacity="0.74">
    Less slide. More signal.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a bright, undimmed image behind the typography; it destroys legibility.
- ❌ Putting the headline inside a visible box or card; this weakens the cinematic full-bleed feel.
- ❌ Highlighting too many words; reserve the accent color for one or two decisive phrases.
- ❌ Center-aligning long headline copy; left alignment feels more editorial and is easier to read.
- ❌ Using low-contrast accent colors such as muted blue or gray against a dark photo.

## Composition notes
- Keep the text block in the left 70–75% of the slide with a generous 12–15% left margin.
- Vertically center the headline mass; allow the photo to breathe around the text.
- Use black overlays and vignette gradients to make the image cinematic, not merely dark.
- Let the accent color appear in only two places: the highlighted phrase and a small kicker/detail.