# SVG Recipe — Geometric Hex-Masked "Spotlight" Layout

## Visual mechanism
A centered geometric portrait uses a point-up hexagonal image crop with a bold cyan frame, turning a standard headshot into a branded spotlight badge. Thin radiating lines and large all-caps typography create a polished executive keynote feel while keeping the slide symmetrical and easy to scan.

## SVG primitives needed
- 1× `<rect>` for the full-slide muted slate-blue background
- 1× `<radialGradient>` for subtle center illumination behind the subject
- 1× `<linearGradient>` for the cyan hexagon frame fill
- 1× `<clipPath>` with a hexagonal `<path>` for cropping the portrait image
- 2× `<path>` for the outer cyan hexagon frame and a faint inner highlight edge
- 1× `<image>` for the portrait photo, clipped into the hexagon
- 6× `<line>` for thin white sunburst rays projecting from the hexagon vertices
- 3× `<text>` blocks for name, job title, and the large “EMPLOYEE SPOTLIGHT” footer
- 1× `<filter id="titleShadow">` applied to the large footer text for subtle depth
- 1× `<filter id="hexShadow">` applied to the hexagon frame for soft separation from the background

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="38%" cy="34%" r="72%">
      <stop offset="0%" stop-color="#6690B4"/>
      <stop offset="58%" stop-color="#5E809D"/>
      <stop offset="100%" stop-color="#557895"/>
    </radialGradient>

    <linearGradient id="cyanFrame" x1="310" y1="45" x2="610" y2="390" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8AF5F3"/>
      <stop offset="45%" stop-color="#72D3E3"/>
      <stop offset="100%" stop-color="#58BFD4"/>
    </linearGradient>

    <filter id="titleShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="hexShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="hexPhotoClip" clipPathUnits="userSpaceOnUse">
      <path d="M452 46 L605 134 L605 310 L452 398 L299 310 L299 134 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <!-- Subtle radiating spotlight rays -->
  <line x1="452" y1="24" x2="452" y2="0" stroke="#FFFFFF" stroke-width="2" opacity="0.28"/>
  <line x1="622" y1="119" x2="663" y2="96" stroke="#FFFFFF" stroke-width="2" opacity="0.28"/>
  <line x1="622" y1="314" x2="660" y2="337" stroke="#FFFFFF" stroke-width="2" opacity="0.22"/>
  <line x1="452" y1="410" x2="452" y2="446" stroke="#FFFFFF" stroke-width="2" opacity="0.18"/>
  <line x1="282" y1="314" x2="244" y2="337" stroke="#FFFFFF" stroke-width="2" opacity="0.22"/>
  <line x1="282" y1="119" x2="241" y2="96" stroke="#FFFFFF" stroke-width="2" opacity="0.28"/>

  <!-- Hexagon frame -->
  <path d="M452 20 L627 121 L627 323 L452 424 L277 323 L277 121 Z"
        fill="url(#cyanFrame)" filter="url(#hexShadow)"/>
  <path d="M452 29 L619 126 L619 318 L452 414 L285 318 L285 126 Z"
        fill="none" stroke="#A9FFFF" stroke-width="6" opacity="0.48"/>

  <!-- Portrait clipped into hexagon -->
  <image x="292" y="39" width="326" height="368"
         href="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?crop=faces&amp;fit=crop&amp;w=700&amp;h=700&amp;q=80"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#hexPhotoClip)"/>

  <!-- Right-side identity text -->
  <text x="674" y="174" width="500"
        font-family="Segoe UI Light, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="300" letter-spacing="4"
        fill="#FFFFFF">
    CASEY SADLER
  </text>

  <text x="676" y="224" width="520"
        font-family="Segoe UI Semilight, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="300" letter-spacing="1.5"
        fill="#FFFFFF">
    <tspan x="676" dy="0">SENIOR MANAGER OF</tspan>
    <tspan x="676" dy="44">PROFESSIONAL DEVELOPMENT</tspan>
  </text>

  <!-- Large footer headline -->
  <text x="640" y="558" width="820"
        text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="116" font-weight="900" letter-spacing="-2"
        fill="#FFFFFF" filter="url(#titleShadow)">
    <tspan x="640" dy="0">EMPLOYEE</tspan>
    <tspan x="640" dy="118">SPOTLIGHT</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the portrait crop; use a `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to the cyan frame path or to a parent `<g>`; the crop should only affect the photo image.
- ❌ Do not use `<use>` to duplicate hexagon geometry; repeat the hexagonal path explicitly for frame, highlight, and clip definition.
- ❌ Do not rely on `marker-end` or filtered `<line>` elements for the sunburst rays; keep them as plain thin vector lines.
- ❌ Do not use ultra-condensed web fonts that may be unavailable in PowerPoint; approximate the look with Segoe UI weights, letter spacing, and large type.

## Composition notes
- Keep the hexagon in the upper-left/center zone, around 30% of slide height, leaving room for the large footer headline.
- Place the name and role to the right of the hexagon, vertically aligned with the portrait center for a balanced spotlight card.
- Use a muted blue background with cyan only on the geometric frame; this keeps attention on the portrait and typography.
- The footer headline should dominate the lower third, with a subtle shadow so the white type feels grounded rather than flat.