# SVG Recipe — Centered Quote Panel

## Visual mechanism
A calm executive quote slide built around one elevated central card, with oversized translucent quote marks and restrained accent lines to make the testimonial feel editorial and premium. The background uses soft gradient lighting and blurred organic shapes so the centered quote panel has depth without competing with the message.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× `<circle>` for blurred ambient light pools behind the quote card
- 1× `<rect>` for the central rounded quote panel with shadow
- 1× `<rect>` for a subtle inner panel highlight / border treatment
- 2× `<path>` for decorative organic corner flourishes
- 2× `<text>` for oversized translucent quotation marks
- 1× `<text>` for the optional headline
- 1× `<text>` with nested `<tspan>` lines for the main quote
- 1× `<text>` for the author / attribution
- 2× `<rect>` for small accent rules around the author
- 1× `<filter id="cardShadow">` applied to the panel
- 1× `<filter id="softGlow">` applied to background circles and decorative paths
- 2× `<linearGradient>` for background and panel fills
- 1× `<radialGradient>` for ambient glow color

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7F2EA"/>
      <stop offset="0.48" stop-color="#EEF3F7"/>
      <stop offset="1" stop-color="#E7EEF5"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="360" y1="150" x2="920" y2="565" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F8FAFC"/>
    </linearGradient>

    <linearGradient id="inkGrad" x1="410" y1="250" x2="870" y2="450" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172033"/>
      <stop offset="1" stop-color="#34445C"/>
    </linearGradient>

    <radialGradient id="glowGold" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#F7C66A" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#F7C66A" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="270" cy="170" r="180" fill="url(#glowGold)" filter="url(#softGlow)" opacity="0.55"/>
  <circle cx="1010" cy="570" r="230" fill="#9EC7D8" filter="url(#softGlow)" opacity="0.28"/>
  <circle cx="1120" cy="110" r="140" fill="#D7C6FF" filter="url(#softGlow)" opacity="0.25"/>

  <path d="M88 612 C168 560, 236 610, 308 548 C346 515, 380 520, 424 548 C352 644, 220 674, 88 612 Z"
        fill="#FFFFFF" opacity="0.38" filter="url(#softGlow)"/>
  <path d="M1046 92 C1110 44, 1208 64, 1238 136 C1198 166, 1138 156, 1088 196 C1048 228, 1002 218, 976 178 C998 144, 1012 118, 1046 92 Z"
        fill="#D8E8F0" opacity="0.48" filter="url(#softGlow)"/>

  <text x="640" y="88" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="600"
        letter-spacing="2.6" fill="#506176" opacity="0.9">
    CUSTOMER PERSPECTIVE
  </text>

  <rect x="312" y="145" width="656" height="430" rx="34"
        fill="url(#panelGrad)" filter="url(#cardShadow)" opacity="0.98"/>
  <rect x="330" y="163" width="620" height="394" rx="26"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.9"/>

  <text x="365" y="286" width="130"
        font-family="Georgia, 'Times New Roman', serif" font-size="150" font-weight="700"
        fill="#D7A94F" opacity="0.18">
    “
  </text>
  <text x="820" y="535" width="130"
        font-family="Georgia, 'Times New Roman', serif" font-size="150" font-weight="700"
        fill="#7AA8BE" opacity="0.16">
    ”
  </text>

  <text x="640" y="258" width="540" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="600"
        fill="url(#inkGrad)">
    <tspan x="640" dy="0">The team translated complexity</tspan>
    <tspan x="640" dy="48">into a simple operating story</tspan>
    <tspan x="640" dy="48">our executives could act on.</tspan>
  </text>

  <rect x="478" y="448" width="88" height="2.5" rx="1.25" fill="#D7A94F" opacity="0.85"/>
  <rect x="714" y="448" width="88" height="2.5" rx="1.25" fill="#D7A94F" opacity="0.85"/>

  <text x="640" y="459" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        fill="#27364A">
    Maya Chen
  </text>
  <text x="640" y="488" width="360" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="400"
        letter-spacing="0.4" fill="#6D7C8F">
    Chief Strategy Officer, Northstar Group
  </text>

  <rect x="618" y="527" width="44" height="4" rx="2" fill="#D7A94F"/>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on automatic text wrapping; split the quote into explicit `<tspan>` lines so the centered panel remains balanced in PowerPoint.
- ❌ Do not use `<foreignObject>` for quote text or HTML-style rich text; it will not translate into editable PPT text.
- ❌ Do not apply `filter` to `<line>` elements for accent rules; use thin rounded `<rect>` elements instead.
- ❌ Do not use `<mask>` for the glass-card effect; use gradients, opacity, strokes, and shadows that translate cleanly.
- ❌ Avoid dense backgrounds or busy photos directly behind the quote unless heavily softened, because the quote must remain the visual priority.

## Composition notes
- Keep the main card centered and occupy roughly 50–60% of slide width; this creates a ceremonial quote moment rather than a cramped text box.
- Reserve the top 80–110 px for a small headline or section label, not a large title competing with the quotation.
- Use oversized quotation marks as decorative atmosphere, with low opacity so they frame the quote without reducing readability.
- Maintain generous vertical spacing: quote in the upper-middle of the panel, author below, and a small accent mark near the bottom for closure.