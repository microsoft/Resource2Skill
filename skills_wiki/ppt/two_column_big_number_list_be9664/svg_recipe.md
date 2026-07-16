# SVG Recipe — Two Column Big Number List

## Visual mechanism
A balanced two-column list uses oversized ordinal or metric numerals as the visual anchors, with compact explanatory copy aligned beside each number inside premium card bands. A subtle central spine, gradient accents, and soft shadowed panels make the list feel editorial and executive rather than like a plain table.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× large decorative `<path>` shapes for soft abstract background energy
- 1× `<text>` headline with nested `<tspan>` for inline emphasis
- 1× `<text>` subtitle / context line
- 1× `<line>` for the vertical center divider
- 8× rounded `<rect>` card panels for the list items
- 8× narrow `<rect>` accent bars to color-code each item
- 8× large `<text>` numerals for the big-number anchors
- 8× `<text>` item headings
- 8× `<text>` item descriptions
- 8× small `<circle>` nodes on the central divider for rhythm and alignment
- 3× `<linearGradient>` definitions for background, accent bars, and number fills
- 1× `<filter id="cardShadow">` applied to card rectangles
- 1× `<filter id="softGlow">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.58" stop-color="#0D1E33"/>
      <stop offset="1" stop-color="#122B46"/>
    </linearGradient>
    <linearGradient id="numberGrad" x1="0" y1="0" x2="140" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7DD3FC"/>
      <stop offset="0.52" stop-color="#38BDF8"/>
      <stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="0" y2="96" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FDE68A"/>
      <stop offset="1" stop-color="#F97316"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80,130 C105,32 243,74 331,160 C413,240 328,326 175,316 C40,307 -50,250 -80,130 Z"
        fill="#2563EB" opacity="0.22" filter="url(#softGlow)"/>
  <path d="M1002,504 C1128,424 1285,452 1356,552 C1427,653 1322,747 1165,728 C1037,713 926,611 1002,504 Z"
        fill="#14B8A6" opacity="0.18" filter="url(#softGlow)"/>

  <text x="80" y="72" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#FFFFFF">
    <tspan>Operating priorities for </tspan><tspan fill="#7DD3FC">next quarter</tspan>
  </text>
  <text x="82" y="108" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#B9C7D8">
    Eight high-leverage moves, split into two executive workstreams.
  </text>

  <line x1="640" y1="146" x2="640" y2="650" stroke="#35506B" stroke-width="2" stroke-dasharray="6 12"/>
  <circle cx="640" cy="185" r="5" fill="#7DD3FC"/>
  <circle cx="640" cy="305" r="5" fill="#7DD3FC"/>
  <circle cx="640" cy="425" r="5" fill="#7DD3FC"/>
  <circle cx="640" cy="545" r="5" fill="#7DD3FC"/>

  <g transform="translate(80 150)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">01</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Win the renewal moment</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Prioritize accounts with expansion signals and near-term decision windows.</text>
  </g>

  <g transform="translate(80 270)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">02</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Compress cycle time</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Remove handoff friction across pricing, legal, and implementation teams.</text>
  </g>

  <g transform="translate(80 390)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">03</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Reprice strategic bundles</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Package premium capabilities around measurable business outcomes.</text>
  </g>

  <g transform="translate(80 510)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">04</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Instrument leading signals</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Track usage quality, risk flags, and conversion intent before lagging metrics move.</text>
  </g>

  <g transform="translate(680 150)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">05</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Elevate partner coverage</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Activate ecosystem sellers where local trust accelerates enterprise adoption.</text>
  </g>

  <g transform="translate(680 270)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">06</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Tighten success playbooks</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Standardize onboarding milestones and executive value reviews.</text>
  </g>

  <g transform="translate(680 390)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">07</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Fund the automation layer</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Redirect manual service load into scalable workflow and AI-assisted operations.</text>
  </g>

  <g transform="translate(680 510)">
    <rect x="0" y="0" width="520" height="96" rx="22" fill="#10243A" opacity="0.94" filter="url(#cardShadow)"/>
    <rect x="0" y="18" width="7" height="60" rx="4" fill="url(#accentGrad)"/>
    <text x="26" y="64" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="url(#numberGrad)">08</text>
    <text x="150" y="36" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Publish one scorecard</text>
    <text x="150" y="64" width="332" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#AFC1D4">Align leadership around fewer metrics with clear owners and weekly cadence.</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Plain spreadsheet-like rows with only small text; the technique depends on oversized numerals as the scanning structure.
- ❌ More than five items per column; the big numbers need vertical breathing room.
- ❌ Center-aligning all content inside cards; keep numbers and text left-aligned for executive readability.
- ❌ Using `<marker-end>` arrows or connector paths; if directional cues are needed, use simple `<line>` elements or small shapes.
- ❌ Clipping or masking non-image elements for the card effects; use rounded rectangles, gradients, and filters instead.

## Composition notes
- Keep the headline in the upper-left 15% of the slide and let the two-column list occupy the main body from roughly y=150 to y=610.
- Use a central divider or rhythm dots to make the two columns feel intentionally paired rather than like two unrelated lists.
- Reserve about 110–130 px inside each card for the big number, then align heading and body copy consistently to its right.
- Use a dark or quiet background with bright gradient numerals; the numbers should be the primary visual focus, while descriptions stay secondary.