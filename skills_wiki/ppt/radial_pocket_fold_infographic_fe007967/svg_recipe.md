# SVG Recipe — Radial Pocket-Fold Infographic

## Visual mechanism
A large gradient hub sits at the center of a radial layout, partially covered by a background-colored “paper pocket” shape whose shadow makes the hub appear tucked underneath. Dashed spokes radiate outward to compact text cards, turning a bullet list into a tactile, layered executive infographic.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× decorative `<path>` blobs for soft premium background accents
- 6× rounded `<rect>` cards for the surrounding agenda / pillar blocks
- 6× `<line>` dashed radial connectors from the hub to the cards
- 6× small `<path>` chevrons for manual arrowhead terminals
- 1× `<circle>` for the central gradient hub
- 1× custom `<path>` for the white pocket-fold overlay
- 9× `<text>` elements with explicit `width` attributes for title, body, card copy, and hub label
- 1× `<linearGradient>` for the central hub fill
- 1× `<linearGradient>` for soft decorative accent fills
- 2× `<filter>` definitions: one soft shadow for cards / hub, one stronger offset shadow for the pocket-fold edge

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="hubGrad" x1="780" y1="235" x2="1015" y2="485" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#47C99D"/>
      <stop offset="0.55" stop-color="#9FE8CE"/>
      <stop offset="1" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#47C99D" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#E65F5C" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="foldShadow" x="-35%" y="-35%" width="180%" height="180%">
      <feOffset dx="10" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <path d="M1080 28 C1188 48 1240 118 1224 214 C1208 309 1125 345 1052 292 C979 239 980 79 1080 28 Z"
        fill="url(#accentGrad)"/>
  <path d="M42 548 C112 505 206 528 237 602 C268 676 180 726 91 704 C8 684 -28 591 42 548 Z"
        fill="#47C99D" opacity="0.08"/>

  <text x="78" y="122" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700" letter-spacing="2">
    RADIAL AGENDA
  </text>
  <text x="78" y="176" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="48" fill="#282828" font-weight="700">
    <tspan x="78" dy="0">Pocket-fold</tspan>
    <tspan x="78" dy="56">infographic</tspan>
  </text>
  <text x="80" y="320" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#6B6B6B">
    <tspan x="80" dy="0">Use this layout to frame a central theme</tspan>
    <tspan x="80" dy="26">with six supporting decisions, pillars, or</tspan>
    <tspan x="80" dy="26">meeting topics. The fold adds depth while</tspan>
    <tspan x="80" dy="26">keeping the diagram clean and editable.</tspan>
  </text>

  <rect x="770" y="46" width="260" height="88" rx="22" fill="#FFFFFF" stroke="#EEEEEE" filter="url(#softShadow)"/>
  <rect x="1046" y="162" width="208" height="92" rx="22" fill="#FFFFFF" stroke="#EEEEEE" filter="url(#softShadow)"/>
  <rect x="1046" y="468" width="208" height="92" rx="22" fill="#FFFFFF" stroke="#EEEEEE" filter="url(#softShadow)"/>
  <rect x="770" y="586" width="260" height="88" rx="22" fill="#FFFFFF" stroke="#EEEEEE" filter="url(#softShadow)"/>
  <rect x="544" y="468" width="210" height="92" rx="22" fill="#FFFFFF" stroke="#EEEEEE" filter="url(#softShadow)"/>
  <rect x="544" y="162" width="210" height="92" rx="22" fill="#FFFFFF" stroke="#EEEEEE" filter="url(#softShadow)"/>

  <line x1="900" y1="235" x2="900" y2="145" stroke="#A0A0A0" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="1010" y1="286" x2="1038" y2="214" stroke="#A0A0A0" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="1010" y1="434" x2="1038" y2="506" stroke="#A0A0A0" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="900" y1="485" x2="900" y2="575" stroke="#A0A0A0" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="790" y1="434" x2="758" y2="506" stroke="#A0A0A0" stroke-width="2" stroke-dasharray="7 8"/>
  <line x1="790" y1="286" x2="758" y2="214" stroke="#A0A0A0" stroke-width="2" stroke-dasharray="7 8"/>

  <path d="M891 157 L900 143 L909 157" fill="none" stroke="#A0A0A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1026 209 L1040 213 L1034 226" fill="none" stroke="#A0A0A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1026 511 L1040 507 L1034 494" fill="none" stroke="#A0A0A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M891 563 L900 577 L909 563" fill="none" stroke="#A0A0A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M770 511 L756 507 L762 494" fill="none" stroke="#A0A0A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M770 209 L756 213 L762 226" fill="none" stroke="#A0A0A0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="900" cy="360" r="132" fill="url(#hubGrad)" stroke="#FFFFFF" stroke-width="7" filter="url(#softShadow)"/>

  <path d="M744 210 C790 184 846 183 902 198 L946 212 C907 244 879 292 879 356 C836 347 792 323 758 288 C732 262 728 226 744 210 Z"
        fill="#FFFFFF" filter="url(#foldShadow)"/>

  <text x="838" y="344" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="46" fill="#282828" font-weight="800" text-anchor="middle">
    <tspan x="900" dy="0">CORE</tspan>
    <tspan x="900" dy="34" font-size="15" fill="#5C5C5C" font-weight="600" letter-spacing="1.5">THEME</tspan>
  </text>

  <text x="900" y="78" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700" text-anchor="middle">
    01 Strategic intent
    <tspan x="900" dy="26" font-size="12.5" fill="#666666" font-weight="400">Define the priority and</tspan>
    <tspan x="900" dy="18" font-size="12.5" fill="#666666" font-weight="400">success metric.</tspan>
  </text>

  <text x="1066" y="192" width="166" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700">
    02 Insight
    <tspan x="1066" dy="26" font-size="12.5" fill="#666666" font-weight="400">Surface the evidence</tspan>
    <tspan x="1066" dy="18" font-size="12.5" fill="#666666" font-weight="400">behind the choice.</tspan>
  </text>

  <text x="1066" y="498" width="166" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700">
    03 Execution
    <tspan x="1066" dy="26" font-size="12.5" fill="#666666" font-weight="400">Translate the idea into</tspan>
    <tspan x="1066" dy="18" font-size="12.5" fill="#666666" font-weight="400">workable actions.</tspan>
  </text>

  <text x="900" y="618" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700" text-anchor="middle">
    04 Governance
    <tspan x="900" dy="26" font-size="12.5" fill="#666666" font-weight="400">Clarify ownership and</tspan>
    <tspan x="900" dy="18" font-size="12.5" fill="#666666" font-weight="400">decision cadence.</tspan>
  </text>

  <text x="734" y="498" width="166" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700" text-anchor="end">
    05 Capability
    <tspan x="734" dy="26" font-size="12.5" fill="#666666" font-weight="400">Identify resources and</tspan>
    <tspan x="734" dy="18" font-size="12.5" fill="#666666" font-weight="400">skills required.</tspan>
  </text>

  <text x="734" y="192" width="166" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E65F5C" font-weight="700" text-anchor="end">
    06 Momentum
    <tspan x="734" dy="26" font-size="12.5" fill="#666666" font-weight="400">Create visibility with</tspan>
    <tspan x="734" dy="18" font-size="12.5" fill="#666666" font-weight="400">short feedback loops.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` or `mask="url(...)"` to create the pocket effect; use a background-colored `<path>` overlay instead.
- ❌ Do not apply `filter` to dashed `<line>` connectors; shadows on lines are dropped. Keep shadows on cards, circles, or paths.
- ❌ Do not use `<use>` to duplicate arrowheads. Draw each chevron as its own small `<path>` so it remains editable.
- ❌ Do not rely on `marker-end` on `<path>` connectors. If arrowheads are needed, use `<line>` connectors plus manual chevron paths.
- ❌ Do not clip the central hub with `clip-path`; clipping on non-image shapes is ignored by the translator.

## Composition notes
- Reserve the left 35% of the slide for the narrative title and explanatory copy; keep the radial diagram in the right 65%.
- Place the hub slightly right of center, around `cx=900`, so the left-side copy and the radial system feel balanced.
- Keep the pocket-fold shape the same color as the background; the illusion comes from its offset shadow, not from a visible fill.
- Use coral only for labels and key accents, green only for the hub, and neutral gray for connector logic and body text.