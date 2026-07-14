# SVG Recipe — Programmatic Linear Flowchart (SmartArt Alternative)

## Visual mechanism
A premium linear flowchart uses evenly spaced rounded-rectangle nodes connected by directional chevrons, creating an unmistakable left-to-right sequence. The polish comes from mathematical alignment, restrained contrast, soft shadows, numbered badges, and a subtle background track that keeps the process visually unified.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<rect>` for the translucent flowchart rail behind the process
- 5× `<rect>` for primary rounded process nodes
- 5× `<circle>` for numbered step badges
- 4× `<path>` for block-arrow / chevron connectors between nodes
- 2× decorative `<path>` elements for soft executive-keynote background ribbons
- 1× `<line>` for a dashed alignment guide running through the flow
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, step labels, step numbers, and supporting captions
- 3× `<linearGradient>` definitions for background, node fills, and connector fills
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for editable shape shadows
- 1× `<filter id="nodeGlow">` using `feGaussianBlur` for a subtle premium glow on the active/final node

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF4FB"/>
      <stop offset="100%" stop-color="#E6EDF7"/>
    </linearGradient>

    <linearGradient id="nodeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2462A7"/>
      <stop offset="100%" stop-color="#173E73"/>
    </linearGradient>

    <linearGradient id="finalNodeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1F7A8C"/>
      <stop offset="100%" stop-color="#0F4C5C"/>
    </linearGradient>

    <linearGradient id="arrowGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#B7C1CC"/>
      <stop offset="100%" stop-color="#8795A3"/>
    </linearGradient>

    <linearGradient id="railGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.45"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0.08  0 0 0 0 0.18  0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="nodeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="7" flood-color="#39A3B5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40 112 C175 38 315 42 478 95 C646 151 775 146 930 86 C1075 31 1194 33 1325 81 L1325 0 L-40 0 Z"
        fill="#DCE9F7" opacity="0.78"/>
  <path d="M-55 650 C178 571 338 586 505 626 C670 666 793 690 981 616 C1112 565 1216 560 1336 596 L1336 720 L-55 720 Z"
        fill="#D8E6F3" opacity="0.72"/>

  <text x="640" y="82" width="880" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#14233B">
    Product Launch Operating Flow
  </text>
  <text x="640" y="122" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#5B6675">
    Replace static SmartArt with editable SVG geometry: consistent spacing, directional logic, and slide-ready polish.
  </text>

  <rect x="64" y="276" width="1152" height="188" rx="42"
        fill="url(#railGrad)" stroke="#D9E3EF" stroke-width="1.5" filter="url(#softShadow)"/>
  <line x1="118" y1="370" x2="1162" y2="370"
        stroke="#BAC6D3" stroke-width="3" stroke-dasharray="8 12" opacity="0.62"/>

  <path d="M278 338 L296 338 L296 322 L318 370 L296 418 L296 402 L278 402 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>
  <path d="M506 338 L524 338 L524 322 L546 370 L524 418 L524 402 L506 402 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>
  <path d="M734 338 L752 338 L752 322 L774 370 L752 418 L752 402 L734 402 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>
  <path d="M962 338 L980 338 L980 322 L1002 370 L980 418 L980 402 L962 402 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>

  <rect x="90" y="312" width="176" height="116" rx="22" fill="url(#nodeGrad)" filter="url(#softShadow)"/>
  <circle cx="126" cy="316" r="22" fill="#FFFFFF" stroke="#2462A7" stroke-width="4"/>
  <text x="126" y="324" width="40" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2462A7">1</text>
  <text x="178" y="359" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">
    <tspan x="178" dy="0">Discover</tspan>
    <tspan x="178" dy="25" font-size="13" font-weight="500" fill="#DCEBFA">market signal</tspan>
  </text>

  <rect x="318" y="312" width="176" height="116" rx="22" fill="url(#nodeGrad)" filter="url(#softShadow)"/>
  <circle cx="354" cy="316" r="22" fill="#FFFFFF" stroke="#2462A7" stroke-width="4"/>
  <text x="354" y="324" width="40" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2462A7">2</text>
  <text x="406" y="359" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">
    <tspan x="406" dy="0">Prioritize</tspan>
    <tspan x="406" dy="25" font-size="13" font-weight="500" fill="#DCEBFA">value drivers</tspan>
  </text>

  <rect x="546" y="312" width="176" height="116" rx="22" fill="url(#nodeGrad)" filter="url(#softShadow)"/>
  <circle cx="582" cy="316" r="22" fill="#FFFFFF" stroke="#2462A7" stroke-width="4"/>
  <text x="582" y="324" width="40" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2462A7">3</text>
  <text x="634" y="359" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">
    <tspan x="634" dy="0">Build</tspan>
    <tspan x="634" dy="25" font-size="13" font-weight="500" fill="#DCEBFA">release candidate</tspan>
  </text>

  <rect x="774" y="312" width="176" height="116" rx="22" fill="url(#nodeGrad)" filter="url(#softShadow)"/>
  <circle cx="810" cy="316" r="22" fill="#FFFFFF" stroke="#2462A7" stroke-width="4"/>
  <text x="810" y="324" width="40" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2462A7">4</text>
  <text x="862" y="359" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">
    <tspan x="862" dy="0">Validate</tspan>
    <tspan x="862" dy="25" font-size="13" font-weight="500" fill="#DCEBFA">pilot feedback</tspan>
  </text>

  <rect x="1002" y="312" width="176" height="116" rx="22" fill="url(#finalNodeGrad)" filter="url(#nodeGlow)"/>
  <circle cx="1038" cy="316" r="22" fill="#FFFFFF" stroke="#1F7A8C" stroke-width="4"/>
  <text x="1038" y="324" width="40" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#1F7A8C">5</text>
  <text x="1090" y="359" width="132" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">
    <tspan x="1090" dy="0">Launch</tspan>
    <tspan x="1090" dy="25" font-size="13" font-weight="500" fill="#D9FAFF">scale globally</tspan>
  </text>

  <text x="640" y="514" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#657385">
    Each node and connector is an editable PowerPoint shape; update labels, colors, or spacing without relying on SmartArt.
  </text>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` arrowheads on `<path>` connectors; they may disappear. Use editable block-arrow `<path>` shapes or direct `<line>` arrows instead.
- ❌ `<use>` or `<symbol>` for repeated nodes; duplicate each node group explicitly so the slide remains editable and translator-safe.
- ❌ Omitting `width` on `<text>` elements; PowerPoint will not auto-fit text reliably without explicit widths.
- ❌ Overcrowding with more than 6–7 horizontal nodes on one slide; either reduce label length, wrap into two rows, or switch to a vertical/segmented process.
- ❌ Applying filters to `<line>` elements; use shadows on node rectangles and connector paths instead.

## Composition notes
- Keep the flowchart centered slightly below the title area, with a single horizontal rail occupying the middle third of the slide.
- Use equal node widths and equal connector gaps; the visual credibility of this technique depends on mathematical spacing.
- Make nodes the strongest color, connectors neutral gray, and the final/current step a distinct accent color.
- Reserve generous negative space above and below the flow so labels remain readable and the process feels executive, not diagram-heavy.