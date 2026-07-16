# SVG Recipe — Automated SmartArt-Style Process Flowchart

## Visual mechanism
A left-to-right sequence of brightly colored rounded step cards floats over a dark gradient stage, with semi-transparent arrow chevrons tucked behind the cards to create a continuous SmartArt-like process tube. Soft shadows, small numeric badges, and consistent typography make the flow feel polished and executive-ready while remaining fully editable.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 2× `<ellipse>` for soft ambient glow fields behind the flow
- 4× `<path>` for semi-transparent directional arrow connectors placed behind the step cards
- 5× `<rect>` for the primary rounded process nodes
- 5× `<rect>` for subtle top highlight strips on each node
- 5× `<circle>` for numbered step badges
- 10× `<text>` for step numbers, step labels, and short explanatory captions; every text element needs an explicit `width`
- 1× `<line>` for the dashed baseline guide running through the process
- 6× `<linearGradient>` for the background and node fills
- 1× `<radialGradient>` for ambient glow
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for depth on cards
- 1× `<filter id="softGlow">` using `feGaussianBlur` for background glow accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#1A2A3A"/>
      <stop offset="100%" stop-color="#0D1721"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.38"/>
      <stop offset="70%" stop-color="#38BDF8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="redGrad" x1="0" y1="280" x2="0" y2="440">
      <stop offset="0%" stop-color="#FF5A6A"/>
      <stop offset="100%" stop-color="#C62842"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0" y1="280" x2="0" y2="440">
      <stop offset="0%" stop-color="#FFB347"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="280" x2="0" y2="440">
      <stop offset="0%" stop-color="#4FE3FF"/>
      <stop offset="100%" stop-color="#0891B2"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="280" x2="0" y2="440">
      <stop offset="0%" stop-color="#5EEAD4"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="violetGrad" x1="0" y1="280" x2="0" y2="440">
      <stop offset="0%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#6D28D9"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="5" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="310" cy="365" rx="280" ry="130" fill="url(#ambientGlow)" filter="url(#softGlow)" opacity="0.55"/>
  <ellipse cx="960" cy="350" rx="300" ry="120" fill="url(#ambientGlow)" filter="url(#softGlow)" opacity="0.35"/>

  <text x="80" y="92" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">
    Automated Process Workflow
  </text>
  <text x="82" y="128" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#B8C7D9">
    A modern SmartArt-style sequence with editable cards, arrows, labels, and shadows.
  </text>

  <line x1="115" y1="360" x2="1165" y2="360" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="2" stroke-dasharray="7 10"/>

  <path d="M242 323 H302 L330 360 L302 397 H242 Z" fill="#FFFFFF" opacity="0.24"/>
  <path d="M462 323 H522 L550 360 L522 397 H462 Z" fill="#FFFFFF" opacity="0.24"/>
  <path d="M682 323 H742 L770 360 L742 397 H682 Z" fill="#FFFFFF" opacity="0.24"/>
  <path d="M902 323 H962 L990 360 L962 397 H902 Z" fill="#FFFFFF" opacity="0.24"/>

  <rect x="80" y="292" width="180" height="136" rx="24" fill="url(#redGrad)" filter="url(#cardShadow)"/>
  <rect x="300" y="292" width="180" height="136" rx="24" fill="url(#orangeGrad)" filter="url(#cardShadow)"/>
  <rect x="520" y="292" width="180" height="136" rx="24" fill="url(#cyanGrad)" filter="url(#cardShadow)"/>
  <rect x="740" y="292" width="180" height="136" rx="24" fill="url(#greenGrad)" filter="url(#cardShadow)"/>
  <rect x="960" y="292" width="180" height="136" rx="24" fill="url(#violetGrad)" filter="url(#cardShadow)"/>

  <rect x="98" y="308" width="144" height="15" rx="7" fill="#FFFFFF" opacity="0.22"/>
  <rect x="318" y="308" width="144" height="15" rx="7" fill="#FFFFFF" opacity="0.22"/>
  <rect x="538" y="308" width="144" height="15" rx="7" fill="#FFFFFF" opacity="0.22"/>
  <rect x="758" y="308" width="144" height="15" rx="7" fill="#FFFFFF" opacity="0.22"/>
  <rect x="978" y="308" width="144" height="15" rx="7" fill="#FFFFFF" opacity="0.22"/>

  <circle cx="170" cy="292" r="26" fill="#102033" stroke="#FFFFFF" stroke-opacity="0.50" stroke-width="2"/>
  <circle cx="390" cy="292" r="26" fill="#102033" stroke="#FFFFFF" stroke-opacity="0.50" stroke-width="2"/>
  <circle cx="610" cy="292" r="26" fill="#102033" stroke="#FFFFFF" stroke-opacity="0.50" stroke-width="2"/>
  <circle cx="830" cy="292" r="26" fill="#102033" stroke="#FFFFFF" stroke-opacity="0.50" stroke-width="2"/>
  <circle cx="1050" cy="292" r="26" fill="#102033" stroke="#FFFFFF" stroke-opacity="0.50" stroke-width="2"/>

  <text x="150" y="301" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">01</text>
  <text x="370" y="301" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">02</text>
  <text x="590" y="301" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">03</text>
  <text x="810" y="301" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">04</text>
  <text x="1030" y="301" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF" text-anchor="middle">05</text>

  <text x="105" y="360" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="170" dy="0">Discover</tspan><tspan x="170" dy="28" font-size="13" font-weight="500" fill="#FDE2E6">intake goals</tspan>
  </text>
  <text x="325" y="360" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="390" dy="0">Plan</tspan><tspan x="390" dy="28" font-size="13" font-weight="500" fill="#FFF1D6">scope work</tspan>
  </text>
  <text x="545" y="360" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="610" dy="0">Build</tspan><tspan x="610" dy="28" font-size="13" font-weight="500" fill="#D9FAFF">create assets</tspan>
  </text>
  <text x="765" y="360" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="830" dy="0">Launch</tspan><tspan x="830" dy="28" font-size="13" font-weight="500" fill="#D9FFF7">release value</tspan>
  </text>
  <text x="985" y="360" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="1050" dy="0">Review</tspan><tspan x="1050" dy="28" font-size="13" font-weight="500" fill="#ECE5FF">measure impact</tspan>
  </text>

  <text x="80" y="525" width="1120" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9FB1C7" text-anchor="middle">
    Repeatable operating model: every node is an editable rounded rectangle, every arrow is a separate editable shape, and each label can be changed in PowerPoint.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` on `<path>` connectors; arrowheads can disappear, so use filled `<path>` chevrons or `<line>` arrows with marker attributes applied directly to each line.
- ❌ Putting the arrows above the cards; this breaks the seamless SmartArt tube illusion. Draw connectors first, then draw cards on top.
- ❌ Using `<use>` or `<symbol>` to duplicate repeated cards; duplicate the actual SVG primitives so PPT-Master creates editable PowerPoint shapes.
- ❌ Applying `filter` to `<line>` elements; use shadows on the card rectangles or path connectors instead.
- ❌ Relying on text autofit; every `<text>` must include a `width` attribute and should be sized to fit its card.

## Composition notes
- Keep the process band centered vertically, occupying roughly 80–88% of slide width, with generous dark negative space above and below.
- Use vivid but distinct node gradients so each step is visually memorable; keep arrows semi-transparent white so they guide without competing.
- Let connectors overlap under the rounded cards by 10–20 px on each side to hide hard joins and create a continuous flow.
- Use a large title zone in the upper-left and a small explanatory note below the flow; the cards remain the primary visual focus.