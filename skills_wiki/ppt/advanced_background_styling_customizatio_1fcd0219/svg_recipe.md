# SVG Recipe — Advanced Background Styling & Customization

## Visual mechanism
Create a full-bleed custom slide environment by stacking editable gradient fills, low-opacity picture texture, simulated pattern marks, and translucent “aurora” shapes behind the content. The background itself becomes the design system: color, depth, texture, and focal lighting all guide the viewer toward a central message.

## SVG primitives needed
- 1× full-slide `<rect>` for the primary multi-stop radial gradient background
- 1× `<image>` for full-bleed photographic or paper/fabric texture overlay
- 1× `<clipPath>` with a full-slide `<rect>` applied to the texture image
- 2× `<radialGradient>` for spotlight-style background lighting and center glow
- 3× `<linearGradient>` for aurora ribbons, glass cards, and accent bars
- 3× large organic `<path>` shapes for premium abstract background customization
- 1× repeated-shape pattern layer using editable `<circle>` and `<line>` elements instead of SVG `<pattern>`
- 1× frosted-glass `<rect>` content panel with shadow
- 1× accent ribbon `<path>` for a branded foreground motif
- 2× `<filter>` definitions: one soft shadow and one glow applied to editable shapes
- 3× `<text>` elements with explicit `width` attributes for title, subtitle, and label copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="47%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#FFF48A"/>
      <stop offset="20%" stop-color="#3EE3D6"/>
      <stop offset="58%" stop-color="#087D83"/>
      <stop offset="100%" stop-color="#06252E"/>
    </radialGradient>

    <radialGradient id="centerGlow" cx="50%" cy="45%" r="46%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="42%" stop-color="#8AF5E8" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#0B2D36" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="auroraA" x1="130" y1="120" x2="1120" y2="610">
      <stop offset="0%" stop-color="#72FFE4" stop-opacity="0.62"/>
      <stop offset="48%" stop-color="#3775FF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#1B104B" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="auroraB" x1="1150" y1="80" x2="150" y2="690">
      <stop offset="0%" stop-color="#FF5A8A" stop-opacity="0.55"/>
      <stop offset="52%" stop-color="#FFC857" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#00B6B8" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="320" y1="230" x2="960" y2="520">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#E9FFFA" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.07"/>
    </linearGradient>

    <linearGradient id="accentFill" x1="410" y1="194" x2="875" y2="194">
      <stop offset="0%" stop-color="#FF315F"/>
      <stop offset="48%" stop-color="#FF8A3D"/>
      <stop offset="100%" stop-color="#FFE166"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>

    <clipPath id="slideClip">
      <rect x="0" y="0" width="1280" height="720"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/subtle-fibers-paper-texture-dark-teal.jpg"
         clip-path="url(#slideClip)" opacity="0.18" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <path d="M-80,208 C120,70 310,88 498,178 C662,256 790,246 938,154 C1060,78 1190,56 1360,118 L1360,318 C1168,250 1054,250 910,332 C720,440 524,398 338,286 C194,198 78,238 -80,350 Z"
        fill="url(#auroraA)" opacity="0.72" filter="url(#softGlow)"/>

  <path d="M1370,515 C1165,610 1000,646 820,590 C642,535 572,408 390,402 C220,396 86,514 -70,630 L-70,760 L1370,760 Z"
        fill="url(#auroraB)" opacity="0.62" filter="url(#softGlow)"/>

  <path d="M1010,-60 C1116,38 1160,130 1135,224 C1110,318 1002,365 914,316 C826,267 820,150 884,56 C910,18 956,-28 1010,-60 Z"
        fill="#FFFFFF" opacity="0.10"/>

  <g opacity="0.16" stroke="#D7FFF8" stroke-width="1.4">
    <line x1="70" y1="92" x2="320" y2="342" stroke-dasharray="3 12"/>
    <line x1="150" y1="70" x2="470" y2="390" stroke-dasharray="3 12"/>
    <line x1="1010" y1="120" x2="1225" y2="335" stroke-dasharray="3 12"/>
    <line x1="915" y1="600" x2="1220" y2="295" stroke-dasharray="4 14"/>
    <line x1="70" y1="650" x2="410" y2="310" stroke-dasharray="4 14"/>
  </g>

  <g opacity="0.24" fill="#DFFFF8">
    <circle cx="104" cy="122" r="3"/>
    <circle cx="164" cy="182" r="2.4"/>
    <circle cx="224" cy="242" r="3.2"/>
    <circle cx="284" cy="302" r="2.4"/>
    <circle cx="1110" cy="156" r="3"/>
    <circle cx="1170" cy="216" r="2.4"/>
    <circle cx="1230" cy="276" r="3.2"/>
    <circle cx="980" cy="626" r="2.8"/>
    <circle cx="1040" cy="566" r="2.4"/>
    <circle cx="1100" cy="506" r="3.2"/>
    <circle cx="206" cy="606" r="3"/>
    <circle cx="266" cy="546" r="2.4"/>
    <circle cx="326" cy="486" r="3.2"/>
  </g>

  <rect x="318" y="228" width="644" height="304" rx="36"
        fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.36" stroke-width="1.5"
        filter="url(#softShadow)"/>

  <path d="M405,190 L875,190 C902,190 924,212 924,239 L924,239 L875,276 L405,276 C378,276 356,254 356,227 C356,206 376,190 405,190 Z"
        fill="url(#accentFill)" opacity="0.96" filter="url(#softShadow)"/>

  <text x="640" y="225" width="420" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700"
        fill="#18222A" letter-spacing="2">
    ADVANCED BACKGROUND
  </text>

  <text x="640" y="352" width="570" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="800"
        fill="#FFFFFF">
    <tspan x="640" dy="0">Gradient · Texture</tspan>
    <tspan x="640" dy="64" fill="#DFFFF8">Pattern Styling</tspan>
  </text>

  <text x="640" y="472" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400"
        fill="#E9FFFA" opacity="0.92">
    Full-bleed visual systems for title slides, dividers, dashboards, and branded executive decks.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for repeating textures; simulate patterns with repeated editable `<circle>`, `<line>`, or `<path>` elements instead.
- ❌ Applying `clip-path` to gradient rectangles, paths, or groups; use clipping only on `<image>` elements.
- ❌ Relying on master-theme background graphics; build the full-bleed background directly in the SVG so it remains portable and editable.
- ❌ Heavy texture images without tinting or opacity control; they can overpower foreground content.
- ❌ Filters on `<line>` pattern strokes; glow and shadow filters should be applied to `<rect>`, `<path>`, `<circle>`, `<ellipse>`, or `<text>` only.

## Composition notes
- Keep the background full-bleed and reserve the brightest gradient area for the intended focal point, usually center or upper-center.
- Use texture at very low opacity, then layer translucent paths or gradients above it to preserve premium depth without visual noise.
- Simulated patterns work best when pushed to corners and edges, leaving the central content zone calm.
- Pair complex backgrounds with simple foreground typography: one glass panel, one accent ribbon, and high-contrast white or dark text.