# SVG Recipe — Icon-Stacked Bar Chart

## Visual mechanism
Use repeated thematic icons as the “fill” of each horizontal bar, where each icon represents one unit or a fixed quantity. The chart keeps axes minimal so the audience reads the bar length through recognizable objects rather than abstract rectangles.

## SVG primitives needed
- 2× `<rect>` for the slide background and rounded chart card
- 1× `<linearGradient>` for the warm stage background
- 1× `<radialGradient>` for dimensional basketball icon fills
- 1× `<filter id="softShadow">` applied to the chart card and selected callout elements
- 5× `<line>` for subtle row guide rails behind the icon stacks
- 29× basketball icon groups, each made from:
  - 1× `<circle>` for the ball body
  - 3× `<path>` for basketball seam curves
- 10× `<text>` for title, subtitle, category labels, value labels, and source note
- 1× decorative `<path>` accent behind the title for premium editorial styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF7EF"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F5F7FB"/>
    </linearGradient>
    <radialGradient id="ballGrad" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#FFB15E"/>
      <stop offset="58%" stop-color="#F47A23"/>
      <stop offset="100%" stop-color="#C65014"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M94,94 C155,44 252,54 306,98 C238,122 166,134 94,118 Z" fill="#FFE1C2" opacity="0.75"/>
  <text x="92" y="84" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#1F2937">City Recreation Assets</text>
  <text x="94" y="119" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#6B7280">Basketball courts by district — each ball represents one court</text>

  <rect x="86" y="156" width="1108" height="480" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="1014" y="116" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#D97706">ICON = 1 COURT</text>

  <line x1="302" y1="230" x2="1054" y2="230" stroke="#E5E7EB" stroke-width="2"/>
  <line x1="302" y1="310" x2="1054" y2="310" stroke="#E5E7EB" stroke-width="2"/>
  <line x1="302" y1="390" x2="1054" y2="390" stroke="#E5E7EB" stroke-width="2"/>
  <line x1="302" y1="470" x2="1054" y2="470" stroke="#E5E7EB" stroke-width="2"/>
  <line x1="302" y1="550" x2="1054" y2="550" stroke="#E5E7EB" stroke-width="2"/>

  <text x="128" y="237" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#374151">Northside</text>
  <text x="128" y="317" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#374151">Central</text>
  <text x="128" y="397" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#374151">Riverside</text>
  <text x="128" y="477" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#374151">East End</text>
  <text x="128" y="557" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#374151">Old Town</text>

  <g transform="translate(322 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(376 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(430 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(484 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(538 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(592 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(646 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(700 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(754 206)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <text x="830" y="237" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#111827">9</text>

  <g transform="translate(322 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(376 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(430 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(484 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(538 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(592 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(646 286)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <text x="722" y="317" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#111827">7</text>

  <g transform="translate(322 366)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(376 366)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(430 366)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(484 366)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(538 366)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(592 366)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <text x="668" y="397" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#111827">6</text>

  <g transform="translate(322 446)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(376 446)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(430 446)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(484 446)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <text x="560" y="477" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#111827">4</text>

  <g transform="translate(322 526)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(376 526)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <g transform="translate(430 526)"><circle cx="24" cy="24" r="22" fill="url(#ballGrad)" stroke="#7A2E12" stroke-width="2"/><path d="M4,24 C15,15 33,15 44,24" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C17,14 17,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/><path d="M24,2 C31,14 31,34 24,46" fill="none" stroke="#6E2B12" stroke-width="3"/></g>
  <text x="506" y="557" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#111827">3</text>

  <text x="92" y="674" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9CA3AF">Source: Parks & Recreation inventory, FY2026 planning cut.</text>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` fills for icon tiling; PowerPoint translation may drop pattern fills, so manually repeat editable icon shapes instead.
- ❌ `<use href="#icon">` to duplicate the icon; it can hard-fail the slide, even though it would be convenient.
- ❌ Stretching one large image to fill a bar; it loses the “one icon = one unit” reading.
- ❌ Heavy axes, tick marks, and gridlines; they compete with the pictorial bar mechanism.
- ❌ Applying `clip-path` to vector icon groups; clipping is only reliable on `<image>` elements.

## Composition notes
- Keep category labels in a fixed left column and begin all icon stacks on the same x-position for clean bar-chart comparison.
- Use generous row spacing; pictorial bars need breathing room so each icon remains recognizable.
- Place value labels immediately after the final icon, not at the far right edge, to reinforce that length equals count.
- Derive the accent palette from the icon color, then keep the card, gridlines, and typography neutral.