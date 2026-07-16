# SVG Recipe — UI Card Depth & Lighting (Dual-Mode Design)

## Visual mechanism
Create two side-by-side UI cards that demonstrate the same component in light and dark mode, using a neutral split canvas, rounded surfaces, subtle borders, top-edge highlights, and layered soft shadows to simulate CSS-like depth and lighting.

## SVG primitives needed
- 2× `<rect>` for the left light-mode and right dark-mode canvas backgrounds
- 2× `<rect>` for the main rounded card surfaces
- 2× `<rect>` for thin top-edge “light catch” highlights on each card
- 2× `<circle>` for circular status/icon badges
- 2× `<path>` for checkmark icons inside the badges
- 5× `<text>` for the large title, mode labels, and small explanatory captions
- 4× `<linearGradient>` for background atmosphere and card surface lighting
- 2× `<filter>` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft card shadows
- 1× `<filter>` using `feGaussianBlur` for a subtle icon glow/accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="lightCanvas" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#eeeeee"/>
      <stop offset="100%" stop-color="#d4d4d4"/>
    </linearGradient>

    <linearGradient id="darkCanvas" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#050505"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>

    <linearGradient id="lightCard" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#f4f4f4"/>
      <stop offset="100%" stop-color="#ececec"/>
    </linearGradient>

    <linearGradient id="darkCard" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#242424"/>
      <stop offset="55%" stop-color="#1b1b1b"/>
      <stop offset="100%" stop-color="#131313"/>
    </linearGradient>

    <filter id="shadowLight" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="offset1"/>
      <feGaussianBlur in="offset1" stdDeviation="18" result="blur1"/>
      <feOffset dx="0" dy="5" result="offset2"/>
      <feGaussianBlur in="offset2" stdDeviation="6" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur1"/>
        <feMergeNode in="blur2"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadowDark" x="-16%" y="-16%" width="132%" height="142%">
      <feOffset dx="0" dy="14" result="offset1"/>
      <feGaussianBlur in="offset1" stdDeviation="20" result="blur1"/>
      <feOffset dx="0" dy="2" result="offset2"/>
      <feGaussianBlur in="offset2" stdDeviation="4" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur1"/>
        <feMergeNode in="blur2"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="badgeGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <!-- dual-mode canvas -->
  <rect x="0" y="0" width="640" height="720" fill="url(#lightCanvas)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#darkCanvas)"/>

  <!-- title with explicit dual-color letters -->
  <text x="316" y="178" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="160" font-weight="800" letter-spacing="8">
    <tspan fill="#080808">COL</tspan><tspan fill="#f2f2f2">ORS</tspan>
  </text>

  <!-- light-mode card -->
  <rect x="98" y="252" width="438" height="365" rx="36" ry="36"
        fill="url(#lightCard)" stroke="#ffffff" stroke-width="1.2" filter="url(#shadowLight)"/>
  <rect x="131" y="253" width="372" height="2" rx="1" ry="1" fill="#ffffff" opacity="0.95"/>
  <rect x="121" y="589" width="390" height="1" fill="#d8d8d8" opacity="0.55"/>

  <circle cx="318" cy="370" r="50" fill="#5a7ee6" filter="url(#badgeGlow)" opacity="0.16"/>
  <circle cx="318" cy="370" r="49" fill="#557be7"/>
  <path d="M295 368 L311 384 L341 353" fill="none" stroke="#ffffff"
        stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="219" y="529" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="78" font-weight="650" fill="#333333">Light</text>
  <text x="151" y="570" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#767676" text-anchor="middle">
    raised surface · white top highlight
  </text>

  <!-- dark-mode card -->
  <rect x="743" y="252" width="438" height="365" rx="36" ry="36"
        fill="url(#darkCard)" stroke="#3d3d3d" stroke-width="1.2" filter="url(#shadowDark)"/>
  <rect x="776" y="253" width="372" height="2" rx="1" ry="1" fill="#8f8f8f" opacity="0.42"/>
  <rect x="767" y="589" width="390" height="1" fill="#0a0a0a" opacity="0.9"/>

  <circle cx="961" cy="370" r="50" fill="#f2df4a" filter="url(#badgeGlow)" opacity="0.12"/>
  <circle cx="961" cy="370" r="49" fill="#f1dd49"/>
  <path d="M938 368 L954 384 L984 353" fill="none" stroke="#222222"
        stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="875" y="529" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="78" font-weight="650" fill="#d7d7d7">Dark</text>
  <text x="797" y="570" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#8a8a8a" text-anchor="middle">
    recessed surface · muted edge contrast
  </text>

  <!-- small design-system annotation -->
  <text x="486" y="678" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="500" fill="#8f8f8f" text-anchor="middle">
    same component geometry, inverted neutral lightness scale
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on a standard PowerPoint rectangle border alone; it creates an even outline and misses the CSS-like top-edge highlight.
- ❌ Do not put shadows on `<line>` elements; use shadow filters on the rounded card `<rect>` instead.
- ❌ Do not use `<mask>` to split light/dark title coloring; use separate `<tspan>` fills or separate text elements.
- ❌ Do not over-saturate the card surfaces; the premium UI look depends on neutral HSL steps and restrained contrast.

## Composition notes
- Keep the canvas split exactly in half so the same card geometry can be compared across light and dark modes.
- Put the cards below a large, high-contrast title; the visual focus should be the card lighting and shadows, not dense copy.
- Use generous internal padding: icon near the upper center, label below, and any caption small and muted.
- Let shadows extend downward more than upward to imply a soft overhead light source.