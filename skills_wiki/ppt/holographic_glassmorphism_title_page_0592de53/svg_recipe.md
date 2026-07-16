# SVG Recipe — Holographic Glassmorphism Title Page

## Visual mechanism
A dark digital canvas is energized with large blurred cyan, violet, and yellow-green aurora blobs, then stabilized by a centered translucent “glass” panel. Crisp white typography and thin wireframe geometry float above the soft background, creating a premium high-tech title-page effect.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark base background
- 5× blurred `<ellipse>` for the holographic aurora / mesh-gradient color fields
- 1× large translucent `<rect>` for the central frosted glass title panel
- 2× subtle translucent `<rect>` overlays for inner sheen and panel highlight
- 3× `<linearGradient>` for background depth, glass fill, and glass border sheen
- 2× `<radialGradient>` for soft glow hotspots
- 2× `<filter>` with `feGaussianBlur` for aurora diffusion and title halo
- 1× `<filter>` with `feOffset + feGaussianBlur + feMerge` for the glass panel shadow
- 4× `<path>` for wireframe triangles and angular holographic accents
- 8× `<line>` for fine technical guide lines and dotted accent rules
- 6× `<circle>` for small endpoint nodes and floating light particles
- 3× `<text>` blocks with explicit `width` for title, subtitle, and small metadata label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="spaceBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07131f"/>
      <stop offset="45%" stop-color="#13213a"/>
      <stop offset="100%" stop-color="#070914"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="42%" stop-color="#111827" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.54"/>
    </linearGradient>

    <linearGradient id="glassStroke" x1="260" y1="240" x2="1020" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.78"/>
      <stop offset="38%" stop-color="#7df9ff" stop-opacity="0.24"/>
      <stop offset="72%" stop-color="#c6a8ff" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.16"/>
    </linearGradient>

    <radialGradient id="cyanCore" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.95"/>
      <stop offset="60%" stop-color="#00a8b8" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#00a8b8" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetCore" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#9b6cff" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#6546d8" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#6546d8" stop-opacity="0"/>
    </radialGradient>

    <filter id="auroraBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="62"/>
    </filter>

    <filter id="panelShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softTextGlow" x="-10%" y="-40%" width="120%" height="180%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#spaceBase)"/>

  <ellipse cx="260" cy="190" rx="350" ry="230" fill="url(#cyanCore)" filter="url(#auroraBlur)" opacity="0.92"/>
  <ellipse cx="920" cy="170" rx="420" ry="260" fill="url(#violetCore)" filter="url(#auroraBlur)" opacity="0.86"/>
  <ellipse cx="710" cy="585" rx="460" ry="230" fill="#d7f56a" filter="url(#auroraBlur)" opacity="0.34"/>
  <ellipse cx="1130" cy="560" rx="320" ry="250" fill="#00d2b8" filter="url(#auroraBlur)" opacity="0.38"/>
  <ellipse cx="150" cy="610" rx="360" ry="210" fill="#435cff" filter="url(#auroraBlur)" opacity="0.34"/>

  <rect x="0" y="0" width="1280" height="720" fill="#020510" opacity="0.28"/>
  <rect x="0" y="0" width="1280" height="720" fill="none" stroke="#ffffff" stroke-opacity="0.06" stroke-width="1"/>

  <line x1="95" y1="132" x2="330" y2="92" stroke="#ffffff" stroke-opacity="0.35" stroke-width="1.2" stroke-dasharray="2 9"/>
  <line x1="936" y1="101" x2="1174" y2="185" stroke="#ffffff" stroke-opacity="0.42" stroke-width="1.2" stroke-dasharray="8 10"/>
  <line x1="145" y1="590" x2="370" y2="530" stroke="#7df9ff" stroke-opacity="0.42" stroke-width="1"/>
  <line x1="905" y1="584" x2="1118" y2="508" stroke="#ffffff" stroke-opacity="0.32" stroke-width="1" stroke-dasharray="3 7"/>

  <path d="M175 200 L260 72 L333 230 Z" fill="none" stroke="#ffffff" stroke-opacity="0.48" stroke-width="1.4" transform="rotate(-14 254 168)"/>
  <path d="M1024 256 L1132 128 L1195 316 Z" fill="none" stroke="#ffffff" stroke-opacity="0.34" stroke-width="1.2" transform="rotate(12 1110 238)"/>
  <path d="M130 475 L216 410 L283 516 Z" fill="none" stroke="#b8f7ff" stroke-opacity="0.36" stroke-width="1.1" transform="rotate(18 207 467)"/>
  <path d="M1005 484 L1088 430 L1158 535 Z" fill="none" stroke="#e6ddff" stroke-opacity="0.32" stroke-width="1.1" transform="rotate(-10 1082 484)"/>

  <circle cx="95" cy="132" r="4" fill="#ffffff" opacity="0.7"/>
  <circle cx="330" cy="92" r="3" fill="#7df9ff" opacity="0.8"/>
  <circle cx="936" cy="101" r="3.5" fill="#ffffff" opacity="0.75"/>
  <circle cx="1174" cy="185" r="4.5" fill="#c6a8ff" opacity="0.78"/>
  <circle cx="370" cy="530" r="3.5" fill="#7df9ff" opacity="0.65"/>
  <circle cx="1118" cy="508" r="3.5" fill="#ffffff" opacity="0.6"/>

  <rect x="278" y="244" width="724" height="218" rx="26" fill="#000000" opacity="0.26" filter="url(#panelShadow)"/>
  <rect x="278" y="244" width="724" height="218" rx="26" fill="url(#glassFill)" stroke="url(#glassStroke)" stroke-width="1.4"/>
  <rect x="306" y="264" width="668" height="56" rx="18" fill="#ffffff" opacity="0.08"/>
  <rect x="306" y="424" width="668" height="1.2" fill="#ffffff" opacity="0.18"/>

  <text x="640" y="332" width="724" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="700"
        letter-spacing="8" fill="#ffffff" opacity="0.30" filter="url(#softTextGlow)">HOLOGRAPHIC</text>

  <text x="640" y="330" width="724" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="700"
        letter-spacing="8" fill="#ffffff">HOLOGRAPHIC</text>

  <text x="640" y="386" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400"
        letter-spacing="3" fill="#dcecff" opacity="0.9">
    GLASSMORPHISM TITLE SYSTEM
  </text>

  <text x="640" y="430" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#ffffff" opacity="0.72">
    <tspan x="640" dy="0">汇报人：清风　　部门：数字体验中心</tspan>
    <tspan x="640" dy="25">Executive Keynote / Product Launch / Training Deck</tspan>
  </text>

  <line x1="378" y1="350" x2="465" y2="350" stroke="#ffffff" stroke-opacity="0.42" stroke-width="1"/>
  <line x1="815" y1="350" x2="902" y2="350" stroke="#ffffff" stroke-opacity="0.42" stroke-width="1"/>
  <line x1="416" y1="452" x2="864" y2="452" stroke="#7df9ff" stroke-opacity="0.34" stroke-width="1" stroke-dasharray="1 10"/>
  <line x1="538" y1="244" x2="742" y2="244" stroke="#ffffff" stroke-opacity="0.36" stroke-width="1.2"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; PowerPoint will not reproduce true background blur behind the glass panel. Simulate it with translucent fills, gradients, shadows, and blurred background blobs.
- ❌ Do not put a `filter` on a `<g>` or `<line>` for glowing guide lines; apply blur filters only to supported shapes like `<ellipse>`, `<rect>`, `<path>`, or `<text>`.
- ❌ Do not use `<mask>` to create frosted-glass cutouts; masks are not safe for this workflow.
- ❌ Do not rely on `<pattern>` fills for noise texture; use subtle translucent rectangles and gradients instead.
- ❌ Do not use `<use>` or `<symbol>` for repeated triangle accents; duplicate editable `<path>` elements directly.

## Composition notes
- Keep the glass panel centered and sized around 55–60% of slide width and 25–32% of slide height; it should feel like a premium UI card floating in space.
- Place the brightest aurora colors away from the exact title baseline so the text remains crisp; use a dark overlay if the background becomes too loud.
- Use white geometry sparingly: thin triangles, dashed rules, and small node dots should frame the title rather than compete with it.
- Maintain generous negative space above and below the panel; the atmosphere is created by depth and glow, not by filling every corner.