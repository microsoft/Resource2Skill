# SVG Recipe — Compositional Grid Toolkit

## Visual mechanism
A premium keynote layout is built by snapping all visual weight to a compositional grid: a golden-ratio split creates the left visual anchor and right typography field, while faint spiral/grid guides make the geometry feel intentional and editorial. The slide uses a bold icon, oversized stacked typography, and a curved accent arrow to demonstrate how mathematical placement can produce dynamic balance.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 5× `<linearGradient>` for background, icon, text accent, card face, and arrow fills
- 3× `<filter>` for soft shadows on text, logo/card, and arrow
- 9× `<line>` for golden-ratio guide divisions and technical grid boundaries
- 5× `<path>` for golden spiral arcs
- 4× `<path>` for PowerPoint-style circular quadrant wedges
- 3× `<rect>` for the PowerPoint foreground card and its layered depth offsets
- 1× `<text>` for the PowerPoint “P” mark
- 3× `<text>` for the large stacked headline
- 1× `<path>` for the curved yellow directional arrow
- 2× `<circle>` for the main orange logo disc and its subtle highlight

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="720" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#e92a96"/>
      <stop offset="0.46" stop-color="#a75ac7"/>
      <stop offset="1" stop-color="#11a7df"/>
    </linearGradient>

    <linearGradient id="orangeDisc" x1="98" y1="32" x2="452" y2="404" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff7f54"/>
      <stop offset="1" stop-color="#c83e20"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="37" y1="120" x2="257" y2="338" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#df431e"/>
      <stop offset="1" stop-color="#b9341d"/>
    </linearGradient>

    <linearGradient id="goldText" x1="620" y1="270" x2="1188" y2="425" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffdf52"/>
      <stop offset="1" stop-color="#ffc333"/>
    </linearGradient>

    <linearGradient id="arrowGrad" x1="410" y1="590" x2="604" y2="464" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffd84d"/>
      <stop offset="1" stop-color="#ffc23c"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="8" dy="12"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .32 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-10%" y="-15%" width="130%" height="140%">
      <feOffset dx="5" dy="7"/>
      <feGaussianBlur stdDeviation="4"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="arrowShadow" x="-30%" y="-35%" width="170%" height="180%">
      <feOffset dx="8" dy="14"/>
      <feGaussianBlur stdDeviation="9"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.2  0 0 0 0 0.05  0 0 0 0 0.15  0 0 0 .42 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- Golden-ratio / rule-of-thirds construction overlay -->
  <line x1="488" y1="0" x2="488" y2="720" stroke="#ffffff" stroke-width="4" opacity="0.34"/>
  <line x1="0" y1="444" x2="488" y2="444" stroke="#ffffff" stroke-width="4" opacity="0.34"/>
  <line x1="302" y1="444" x2="302" y2="720" stroke="#ffffff" stroke-width="4" opacity="0.34"/>
  <line x1="302" y1="550" x2="488" y2="550" stroke="#ffffff" stroke-width="4" opacity="0.32"/>
  <line x1="372" y1="444" x2="372" y2="550" stroke="#ffffff" stroke-width="4" opacity="0.30"/>
  <line x1="302" y1="508" x2="372" y2="508" stroke="#ffffff" stroke-width="4" opacity="0.30"/>
  <line x1="345" y1="508" x2="345" y2="550" stroke="#ffffff" stroke-width="4" opacity="0.28"/>
  <line x1="427" y1="0" x2="427" y2="720" stroke="#ffffff" stroke-width="2" opacity="0.12"/>
  <line x1="853" y1="0" x2="853" y2="720" stroke="#ffffff" stroke-width="2" opacity="0.10"/>

  <path d="M 0 444 A 488 488 0 0 1 488 0" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.38"/>
  <path d="M 488 0 A 792 792 0 0 1 1280 720" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.35"/>
  <path d="M 0 720 A 302 302 0 0 1 302 444" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.32"/>
  <path d="M 302 720 A 186 186 0 0 1 488 550" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.30"/>
  <path d="M 302 550 A 70 70 0 0 1 372 508" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.28"/>

  <!-- Left visual anchor snapped to golden-ratio field -->
  <circle cx="264" cy="218" r="186" fill="url(#orangeDisc)" filter="url(#softShadow)"/>
  <path d="M264 32 A186 186 0 0 1 450 218 L264 218 Z" fill="#ff8a66" opacity="0.92"/>
  <path d="M264 218 L450 218 A186 186 0 0 1 264 404 Z" fill="#d64c2b" opacity="0.88"/>
  <path d="M264 218 L264 404 A186 186 0 0 1 78 218 Z" fill="#c84324" opacity="0.88"/>
  <path d="M264 32 L264 218 L78 218 A186 186 0 0 1 264 32 Z" fill="#f06443" opacity="0.90"/>
  <circle cx="264" cy="218" r="186" fill="none" stroke="#000000" stroke-width="1" opacity="0.08"/>

  <rect x="56" y="132" width="220" height="218" rx="16" fill="#6b2417" opacity="0.34"/>
  <rect x="46" y="126" width="220" height="218" rx="16" fill="#84291a" opacity="0.42"/>
  <rect x="37" y="120" width="220" height="218" rx="16" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <text x="98" y="290" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="166" font-weight="400" fill="#ffffff">P</text>

  <!-- Curved accent arrow follows the spiral movement toward the message -->
  <path d="M405 553
           C448 584 501 588 533 548
           C548 529 550 509 544 489
           L590 466
           C595 463 600 466 601 472
           L605 551
           C606 558 599 562 594 557
           L566 533
           C531 590 462 613 405 559
           C400 555 400 551 405 553 Z"
        fill="url(#arrowGrad)" filter="url(#arrowShadow)"/>

  <!-- Right typography field occupies the open 61.8% region -->
  <text x="502" y="235" width="715"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="168" font-weight="900" letter-spacing="2"
        fill="#ffffff" filter="url(#textShadow)">3 TIPS FOR</text>

  <text x="628" y="424" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="156" font-weight="900" letter-spacing="1"
        fill="url(#goldText)" filter="url(#textShadow)">PERFECT</text>

  <text x="744" y="612" width="480"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="150" font-weight="900" letter-spacing="2"
        fill="#ffffff" filter="url(#textShadow)">SLIDES</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place major objects “by eye”; calculate golden split positions such as `1280 × 0.382 ≈ 489` or `1280 × 0.618 ≈ 791`.
- ❌ Do not use `<marker-end>` for the curved arrow; build the arrow as a filled `<path>` so it remains editable.
- ❌ Do not rely on `<mask>` or clipping shapes for the golden spiral overlay; use editable `<line>` and stroked `<path>` elements.
- ❌ Do not make the construction grid too opaque; it should feel like a premium blueprint layer, not compete with the headline.
- ❌ Do not omit `width` on `<text>` elements; every text object needs an explicit width for clean PowerPoint translation.

## Composition notes
- Keep the main visual anchor inside the left golden-ratio field, roughly within the first 38% of the canvas; this leaves a clean editorial text stage on the right.
- Use the golden spiral arcs as both structure and decoration: low-opacity white lines create sophistication without overpowering the message.
- Place the largest headline blocks along the open side of the split, with strong vertical stacking and generous negative space around the letterforms.
- Use one warm accent color, such as gold, to emphasize the key word while the rest of the palette remains high-contrast white over a saturated gradient.