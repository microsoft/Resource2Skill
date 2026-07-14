# SVG Recipe — Numbered Feature Spotlight

## Visual mechanism
A sequential list is transformed into a premium process layout by pairing bold numbered accent squares with elevated white content cards. The strong color anchor tells the audience where to look first, while soft shadows, generous spacing, and consistent alignment make each feature feel important and easy to scan.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark navy background
- 2× decorative `<path>` shapes for subtle ambient background geometry
- 1× `<linearGradient>` for the accent number-card fill
- 1× `<radialGradient>` for the background glow
- 1× `<filter id="cardShadow">` applied to white text cards
- 1× `<filter id="softGlow">` applied to decorative background paths
- 5× `<rect>` for numbered accent squares
- 5× `<text>` for large centered numerals
- 5× `<rect>` for white rounded feature cards
- 5× small `<rect>` accents on the right side of each card for color rhythm
- 5× `<text>` blocks with nested `<tspan>` for feature title and supporting detail
- 4× `<line>` elements for subtle dashed vertical sequencing between number blocks
- 2× `<text>` elements for the slide title and subtitle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF9A3D"/>
      <stop offset="55%" stop-color="#F76B1C"/>
      <stop offset="100%" stop-color="#D84D12"/>
    </linearGradient>

    <radialGradient id="navyGlow" cx="70%" cy="28%" r="65%">
      <stop offset="0%" stop-color="#4B4A82" stop-opacity="0.70"/>
      <stop offset="60%" stop-color="#2D2D52" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#24243F" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-35%" width="145%" height="180%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 .28 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#2D2D52"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#navyGlow)"/>

  <path d="M930 55 C1040 20 1175 65 1242 152 C1305 235 1280 342 1205 391 C1126 443 998 414 933 340 C866 263 826 88 930 55 Z"
        fill="#FFFFFF" opacity="0.055" filter="url(#softGlow)"/>
  <path d="M-60 610 C60 525 175 545 242 625 C306 702 201 764 64 747 C-46 733 -151 674 -60 610 Z"
        fill="#F76B1C" opacity="0.11" filter="url(#softGlow)"/>

  <text x="96" y="78" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#FFFFFF">
    Numbered Feature Spotlight
  </text>
  <text x="98" y="116" width="820" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#C9CBE6">
    Use bold numeric anchors to turn a plain list into a structured executive narrative.
  </text>

  <line x1="220" y1="213" x2="220" y2="252" stroke="#F76B1C" stroke-width="3" stroke-opacity="0.45" stroke-dasharray="5 9"/>
  <line x1="220" y1="309" x2="220" y2="348" stroke="#F76B1C" stroke-width="3" stroke-opacity="0.45" stroke-dasharray="5 9"/>
  <line x1="220" y1="405" x2="220" y2="444" stroke="#F76B1C" stroke-width="3" stroke-opacity="0.45" stroke-dasharray="5 9"/>
  <line x1="220" y1="501" x2="220" y2="540" stroke="#F76B1C" stroke-width="3" stroke-opacity="0.45" stroke-dasharray="5 9"/>

  <g transform="translate(0 0)">
    <rect x="184" y="156" width="72" height="72" rx="7" fill="url(#accentGrad)"/>
    <text x="220" y="193" width="72" text-anchor="middle" dominant-baseline="central"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">1</text>
    <rect x="286" y="156" width="820" height="72" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="1078" y="176" width="8" height="32" rx="4" fill="#F76B1C" opacity="0.75"/>
    <text x="322" y="183" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#2B2B35">
      <tspan font-weight="700">Discover the audience need</tspan>
      <tspan x="322" dy="26" font-size="15" fill="#6B6F7A">Frame the decision, pain point, or opportunity before presenting the feature.</tspan>
    </text>
  </g>

  <g transform="translate(0 96)">
    <rect x="184" y="156" width="72" height="72" rx="7" fill="url(#accentGrad)"/>
    <text x="220" y="193" width="72" text-anchor="middle" dominant-baseline="central"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">2</text>
    <rect x="286" y="156" width="820" height="72" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="1078" y="176" width="8" height="32" rx="4" fill="#F76B1C" opacity="0.75"/>
    <text x="322" y="183" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#2B2B35">
      <tspan font-weight="700">Spotlight the core capability</tspan>
      <tspan x="322" dy="26" font-size="15" fill="#6B6F7A">State the feature in plain language and connect it to a measurable outcome.</tspan>
    </text>
  </g>

  <g transform="translate(0 192)">
    <rect x="184" y="156" width="72" height="72" rx="7" fill="url(#accentGrad)"/>
    <text x="220" y="193" width="72" text-anchor="middle" dominant-baseline="central"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">3</text>
    <rect x="286" y="156" width="820" height="72" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="1078" y="176" width="8" height="32" rx="4" fill="#F76B1C" opacity="0.75"/>
    <text x="322" y="183" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#2B2B35">
      <tspan font-weight="700">Show the proof point</tspan>
      <tspan x="322" dy="26" font-size="15" fill="#6B6F7A">Add a metric, customer quote, or brief example to make the claim credible.</tspan>
    </text>
  </g>

  <g transform="translate(0 288)">
    <rect x="184" y="156" width="72" height="72" rx="7" fill="url(#accentGrad)"/>
    <text x="220" y="193" width="72" text-anchor="middle" dominant-baseline="central"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">4</text>
    <rect x="286" y="156" width="820" height="72" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="1078" y="176" width="8" height="32" rx="4" fill="#F76B1C" opacity="0.75"/>
    <text x="322" y="183" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#2B2B35">
      <tspan font-weight="700">Guide the next action</tspan>
      <tspan x="322" dy="26" font-size="15" fill="#6B6F7A">Tell the audience exactly how to adopt, test, or evaluate the feature.</tspan>
    </text>
  </g>

  <g transform="translate(0 384)">
    <rect x="184" y="156" width="72" height="72" rx="7" fill="url(#accentGrad)"/>
    <text x="220" y="193" width="72" text-anchor="middle" dominant-baseline="central"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#FFFFFF">5</text>
    <rect x="286" y="156" width="820" height="72" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="1078" y="176" width="8" height="32" rx="4" fill="#F76B1C" opacity="0.75"/>
    <text x="322" y="183" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#2B2B35">
      <tspan font-weight="700">Close with business impact</tspan>
      <tspan x="322" dy="26" font-size="15" fill="#6B6F7A">Summarize the value in one crisp sentence the audience can repeat.</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using only plain bullets; the visual anchor must be the numbered accent square.
- ❌ Applying shadows to `<line>` connectors; PowerPoint translation drops line filters.
- ❌ Overcrowding the white cards with paragraphs; keep each card to one bold phrase plus one short support line.
- ❌ Using `<marker-end>` arrows for the sequence; if direction is needed, use simple editable `<line>` segments or small triangle `<path>` shapes.
- ❌ Low-contrast accent colors on the dark background; the number blocks should be immediately visible.

## Composition notes
- Keep the numbered column visually consistent: all number squares should share the same x-position, size, color, and vertical rhythm.
- Reserve the top 15–20% of the slide for title and framing; the list stack should begin below it with generous breathing room.
- Use the white cards as the primary reading surface and the orange squares as scanning anchors; avoid adding competing bright colors.
- Leave negative space on the right and around the stack so the shadow and rounded cards feel premium rather than cramped.