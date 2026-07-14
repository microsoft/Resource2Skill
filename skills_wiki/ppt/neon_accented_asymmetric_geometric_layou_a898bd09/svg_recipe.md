# SVG Recipe — Tech Neon Asymmetric Layout

## Visual mechanism
A deep slate canvas is split asymmetrically: oversized left-aligned typography anchors the negative space while the right side stacks neon geometric blocks and a clipped technology photo. The signature move is a “diagonal rounded rectangle” shape where only the top-left and bottom-right corners are rounded, creating a futuristic, engineered feel.

## SVG primitives needed
- 1× full-canvas `<rect>` for the dark navy/slate background
- 2× `<linearGradient>` for subtle background depth and neon photo overlays
- 2× `<filter>` definitions for soft shadow and neon glow on editable shapes/text
- 1× `<clipPath>` with a custom `<path>` for the asymmetric rounded photo crop
- 4× large `<path>` shapes for asymmetric neon blocks and photo backing plates
- 1× `<image>` clipped to the asymmetric hero shape
- 1× compound `<path>` with `fill-rule="evenodd"` for a cyan donut/ring accent
- 6× thin `<line>` elements for minimal tech-circuit accents
- 3× small `<circle>` nodes for glowing interface dots
- 4× `<text>` blocks with explicit `width` attributes for title, subtitle, label, and meta copy
- Nested `<tspan>` elements for split-line title styling and neon emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#24252C"/>
      <stop offset="58%" stop-color="#2C2D35"/>
      <stop offset="100%" stop-color="#1E2028"/>
    </linearGradient>

    <linearGradient id="photoTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D0C5" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#C4F042" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <path d="M711 176 H1145 V454 Q1145 536 1063 536 H635 V258 Q635 176 711 176 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDepth)"/>

  <path d="M818 72 H1168 V300 Q1168 368 1100 368 H748 V142 Q748 72 818 72 Z"
        fill="#C4F042" filter="url(#neonGlow)"/>

  <path d="M704 126 H1120 V394 Q1120 462 1052 462 H636 V194 Q636 126 704 126 Z"
        fill="#20222B" opacity="0.75" filter="url(#softShadow)"/>

  <path d="M711 176 H1145 V454 Q1145 536 1063 536 H635 V258 Q635 176 711 176 Z"
        fill="#11141C" filter="url(#softShadow)"/>

  <image x="635" y="176" width="510" height="360"
         href="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&amp;fit=crop&amp;w=1200&amp;q=80"
         clip-path="url(#heroClip)" preserveAspectRatio="xMidYMid slice"/>

  <path d="M711 176 H1145 V454 Q1145 536 1063 536 H635 V258 Q635 176 711 176 Z"
        fill="url(#photoTint)" opacity="0.9"/>

  <path d="M650 505
           A96 96 0 1 0 842 505
           A96 96 0 1 0 650 505
           M706 505
           A40 40 0 1 1 786 505
           A40 40 0 1 1 706 505"
        fill="#00D0C5" fill-rule="evenodd" filter="url(#neonGlow)"/>

  <path d="M1040 508 H1210 V602 Q1210 638 1174 638 H1004 V544 Q1004 508 1040 508 Z"
        fill="#C4F042"/>

  <path d="M116 88 H228 V146 Q228 166 208 166 H96 V108 Q96 88 116 88 Z"
        fill="#C4F042"/>

  <path d="M114 104 L154 104 L174 127 L154 150 L114 150 L134 127 Z"
        fill="#2C2D35"/>

  <line x1="870" y1="94" x2="936" y2="94" stroke="#2C2D35" stroke-width="4" opacity="0.55"/>
  <line x1="962" y1="94" x2="1034" y2="94" stroke="#2C2D35" stroke-width="4" opacity="0.55"/>
  <line x1="104" y1="602" x2="248" y2="602" stroke="#00D0C5" stroke-width="2" stroke-dasharray="8 10" opacity="0.7"/>
  <line x1="248" y1="602" x2="292" y2="558" stroke="#00D0C5" stroke-width="2" stroke-dasharray="8 10" opacity="0.7"/>
  <line x1="292" y1="558" x2="374" y2="558" stroke="#00D0C5" stroke-width="2" stroke-dasharray="8 10" opacity="0.7"/>
  <line x1="1115" y1="626" x2="1190" y2="626" stroke="#2C2D35" stroke-width="4" opacity="0.55"/>

  <circle cx="104" cy="602" r="5" fill="#00D0C5" filter="url(#neonGlow)"/>
  <circle cx="374" cy="558" r="5" fill="#00D0C5" filter="url(#neonGlow)"/>
  <circle cx="1190" cy="626" r="5" fill="#2C2D35"/>

  <text x="96" y="236" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="74" font-weight="800"
        letter-spacing="-2" fill="#FFFFFF">
    <tspan x="96" dy="0">IT PRODUCT</tspan>
    <tspan x="96" dy="82" fill="#B4B4B4">PRESENTATION</tspan>
  </text>

  <text x="100" y="405" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400"
        fill="#B8BBC7">
    <tspan x="100">Secure cloud platforms, real-time analytics,</tspan>
    <tspan x="100" dy="32">and infrastructure intelligence for modern teams.</tspan>
  </text>

  <text x="100" y="494" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700"
        letter-spacing="3" fill="#C4F042">
    NEXT-GEN SYSTEMS
  </text>

  <text x="1018" y="586" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800"
        letter-spacing="1.5" fill="#2C2D35">
    2026 / CYBER OPS
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `mask` to create the asymmetric photo crop; use a `<clipPath>` applied directly to the `<image>`.
- ❌ Do not build the diagonal rounded rectangle from multiple overlapping rectangles and circles; use a single editable `<path>` so the shape stays clean.
- ❌ Do not center all content symmetrically; the style depends on a strong left text field and a heavier right visual cluster.
- ❌ Do not use muted accent colors; the neon lime and cyan need high contrast against the dark background.
- ❌ Do not apply filters to `<line>` elements; use glow filters only on paths, circles, rectangles, ellipses, or text.

## Composition notes
- Keep the left 40–45% of the slide mostly empty except for large typography and a short subtitle; this negative space makes the neon geometry feel premium.
- Stack the right-side shapes in layers: neon backing block, dark shadow plate, clipped photo, then foreground cyan ring or small lime tag.
- Use lime green as the dominant accent and cyan as the secondary “circuit” accent; avoid distributing both colors evenly across the slide.
- The hero image should feel technical: circuit boards, server racks, code screens, cybersecurity operations, robotics, or abstract data infrastructure.