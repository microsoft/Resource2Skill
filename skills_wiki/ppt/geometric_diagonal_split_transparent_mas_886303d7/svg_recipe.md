# SVG Recipe — Geometric Diagonal Split & Transparent Masking

## Visual mechanism
A full-bleed photo is partially covered by a large diagonal brand-color panel, creating a safe content zone on the left while preserving the image on the right. Parallel translucent diagonal stripes extend from the panel edge to create a progressive “masked fade” rather than a single hard cut.

## SVG primitives needed
- 1× `<image>` for the full-slide photographic background
- 1× `<rect>` for a subtle darkening veil over the photo
- 1× `<path>` for the main solid diagonal content block
- 3–5× `<path>` for parallel translucent diagonal masking stripes
- 1× `<linearGradient>` for a premium blue panel fill with slight tonal depth
- 1× `<filter id="softShadow">` applied to selected text or small logo shapes for depth
- 4× `<rect>` for a simple editable geometric logo mark
- 6× `<text>` for super-title, main title lines, divider label, and body copy
- 1× `<line>` for a thin accent divider under the title

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="brandBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1560A1"/>
      <stop offset="58%" stop-color="#0F558F"/>
      <stop offset="100%" stop-color="#0A477A"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed corporate photo -->
  <image
    href="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Subtle photo control layer so the transparent stripes feel intentional -->
  <rect x="0" y="0" width="1280" height="720" fill="#07192A" opacity="0.16"/>

  <!-- Main diagonal solid content field -->
  <path d="M 0 0 L 835 0 L 510 720 L 0 720 Z"
        fill="url(#brandBlue)"/>

  <!-- Transparent geometric masking stripes -->
  <path d="M 850 0 L 930 0 L 604 720 L 524 720 Z"
        fill="#1560A1" opacity="0.78"/>
  <path d="M 948 0 L 998 0 L 672 720 L 622 720 Z"
        fill="#1560A1" opacity="0.48"/>
  <path d="M 1017 0 L 1044 0 L 718 720 L 691 720 Z"
        fill="#1560A1" opacity="0.28"/>
  <path d="M 1062 0 L 1075 0 L 749 720 L 736 720 Z"
        fill="#FFC000" opacity="0.52"/>

  <!-- Top-left geometric logo -->
  <rect x="78" y="68" width="18" height="18" rx="2" fill="#FFFFFF" opacity="0.95" filter="url(#softShadow)"/>
  <rect x="101" y="68" width="18" height="18" rx="2" fill="#FFC000" opacity="0.95"/>
  <rect x="78" y="91" width="18" height="18" rx="2" fill="#FFC000" opacity="0.95"/>
  <rect x="101" y="91" width="18" height="18" rx="2" fill="#FFFFFF" opacity="0.95"/>

  <text x="138" y="85" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="2.6"
        fill="#FFFFFF">
    POWERPOINT SHOW
  </text>

  <!-- Editorial title stack -->
  <text x="78" y="232" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="78" font-weight="800" letter-spacing="-2"
        fill="#FFFFFF" filter="url(#softShadow)">
    BUSINESS
  </text>

  <text x="78" y="314" width="580"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" letter-spacing="-2"
        fill="#FFC000" filter="url(#softShadow)">
    PRESENTATION
  </text>

  <line x1="80" y1="356" x2="430" y2="356"
        stroke="#FFC000" stroke-width="4" opacity="0.9"/>

  <text x="80" y="397" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" letter-spacing="1.8"
        fill="#FFFFFF">
    STRATEGY • GROWTH • IMPACT
  </text>

  <text x="82" y="462" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="400"
        fill="#DCEBFA">
    <tspan x="82" dy="0">A modern executive summary layout using a</tspan>
    <tspan x="82" dy="25">diagonal brand field, transparent geometric</tspan>
    <tspan x="82" dy="25">masking, and high-contrast typography to</tspan>
    <tspan x="82" dy="25">balance message clarity with photographic</tspan>
    <tspan x="82" dy="25">context and momentum.</tspan>
  </text>

  <!-- Small right-side caption integrated into the photo zone -->
  <text x="936" y="644" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="1.4"
        fill="#FFFFFF" opacity="0.82">
    2026 EXECUTIVE KEYNOTE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using an SVG `<mask>` to reveal the photo; PPT translation may fail or ignore it. Simulate masking with translucent editable `<path>` overlays instead.
- ❌ Applying `clip-path` to the diagonal color panels; clipping is reliable for `<image>` crops only, not normal shapes.
- ❌ Building the diagonal edge from rotated rectangles with skew or matrix transforms; use direct polygon-like `<path>` coordinates for reliable editable geometry.
- ❌ Placing text over the photo side unless the photo is heavily darkened; the solid diagonal panel exists to guarantee legibility.
- ❌ Using only one hard diagonal block with no transparent stripes; the premium look depends on the layered fade transition.

## Composition notes
- Keep all important copy inside the left 40–45% safe zone, well away from the diagonal edge.
- The main diagonal should intersect near 63–68% width at the top and around 38–42% width at the bottom.
- Use one dominant brand color for the panel and repeated translucent versions of that color for the masking stripes.
- Reserve the far-right third for the photo subject; avoid covering faces or key objects with the opaque panel.