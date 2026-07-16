# SVG Recipe — Geometric Chevron Cover

## Visual mechanism
A clean cover slide built from a dark negative-space title field and an oversized layered chevron wedge that cuts in from the right. The chevron is made from angular polygon paths with gradients, shadows, and subtle facet overlays to create a premium corporate section-divider feel.

## SVG primitives needed
- 2× `<rect>` for the full-slide dark background and a soft left-side title field tint
- 6× `<path>` for the large chevron body, inner facets, highlight planes, and diagonal accent slashes
- 5× `<line>` for fine architectural guide lines and title underline accents
- 4× `<text>` blocks for section label, headline, subtitle, and footer metadata
- 4× `<linearGradient>` fills for background depth and chevron facet lighting
- 1× `<filter id="chevronShadow">` applied to the main chevron body for depth
- 1× `<filter id="softGlow">` applied to the cyan highlight facet

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#081326"/>
      <stop offset="0.55" stop-color="#0E1C33"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="leftWash" x1="0" y1="0" x2="560" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172A46" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#172A46" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="chevronMain" x1="650" y1="40" x2="1280" y2="690" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1947D2"/>
      <stop offset="0.48" stop-color="#0A7FD8"/>
      <stop offset="1" stop-color="#13C5D8"/>
    </linearGradient>

    <linearGradient id="chevronFacet" x1="770" y1="0" x2="1270" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#6BE4FF" stop-opacity="0.86"/>
      <stop offset="0.55" stop-color="#19B6E9" stop-opacity="0.7"/>
      <stop offset="1" stop-color="#0876C8" stop-opacity="0.25"/>
    </linearGradient>

    <linearGradient id="deepFacet" x1="800" y1="720" x2="1280" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#061A3A" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#0E5FBF" stop-opacity="0.18"/>
    </linearGradient>

    <filter id="chevronShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-16" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="620" height="720" fill="url(#leftWash)"/>

  <path d="M 720 -40 L 1280 -40 L 1280 760 L 720 760 L 1015 360 Z"
        fill="url(#chevronMain)" filter="url(#chevronShadow)"/>

  <path d="M 720 -40 L 1015 360 L 720 760 L 598 760 L 892 360 L 598 -40 Z"
        fill="#07152A" fill-opacity="0.58"/>

  <path d="M 756 0 L 1280 0 L 1280 192 L 1015 360 Z"
        fill="url(#chevronFacet)"/>

  <path d="M 1015 360 L 1280 528 L 1280 720 L 756 720 Z"
        fill="url(#deepFacet)"/>

  <path d="M 920 0 L 1280 0 L 1280 72 L 1056 292 Z"
        fill="#FFFFFF" fill-opacity="0.12"/>

  <path d="M 1122 352 L 1280 252 L 1280 468 Z"
        fill="#00E0FF" fill-opacity="0.38" filter="url(#softGlow)"/>

  <path d="M 642 92 L 694 92 L 442 628 L 390 628 Z"
        fill="#2AE7FF" fill-opacity="0.08"/>

  <path d="M 592 126 L 620 126 L 386 594 L 358 594 Z"
        fill="#FFFFFF" fill-opacity="0.05"/>

  <line x1="92" y1="128" x2="214" y2="128" stroke="#19D3F3" stroke-width="4"/>
  <line x1="92" y1="140" x2="162" y2="140" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.26"/>
  <line x1="90" y1="516" x2="350" y2="516" stroke="#19D3F3" stroke-width="3"/>
  <line x1="376" y1="516" x2="432" y2="516" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.24"/>
  <line x1="1050" y1="66" x2="1192" y2="66" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.35"/>

  <text x="92" y="112" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3"
        fill="#7EEBFF">SECTION 01</text>

  <text x="88" y="242" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="68" font-weight="800"
        fill="#FFFFFF">
    <tspan x="88" dy="0">Strategy,</tspan>
    <tspan x="88" dy="78" fill="#D9F7FF">Simplified</tspan>
  </text>

  <text x="92" y="390" width="480"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400"
        fill="#B8C7D9">
    <tspan x="92" dy="0">A geometric cover system for bold</tspan>
    <tspan x="92" dy="34">executive narratives and section breaks.</tspan>
  </text>

  <text x="92" y="638" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="1.2"
        fill="#7B8FA8">2026 ENTERPRISE PLANNING · CONFIDENTIAL</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<polygon>` plus `<use>` clones for repeated chevrons; duplicate editable `<path>` shapes directly instead.
- ❌ Applying `skewX`, `skewY`, or `matrix(...)` transforms to create the angled geometry; draw the final angled paths explicitly.
- ❌ Overcrowding the left text area with icons, charts, or photos; the power of this cover comes from strong negative space.
- ❌ Using a filter on `<line>` accents; shadows/glows should be applied only to paths, rects, circles, ellipses, or text.

## Composition notes
- Keep the headline on the left 40–45% of the canvas, with generous top and side margins.
- Let the chevron occupy the right half and extend beyond the canvas edges so it feels cropped, architectural, and energetic.
- Use one bright cyan highlight facet sparingly; most depth should come from darker blue planes and soft shadow.
- Align small labels, underlines, and footer metadata to the same left margin to reinforce the minimal corporate grid.