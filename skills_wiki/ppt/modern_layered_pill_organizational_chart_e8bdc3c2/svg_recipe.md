# SVG Recipe — Modern Layered-Pill Organizational Chart

## Visual mechanism
A hierarchical org chart is softened by replacing rigid boxes with layered pill cards: a full-width colored rounded rectangle sits underneath a slightly offset white pill, leaving a visible accent band on the left. Thin orthogonal connector lines and small joint dots keep the structure clear while soft shadows and a larger circular leader node create a premium, tactile keynote look.

## SVG primitives needed
- 1× `<rect>` for the pale slide background.
- 2× decorative `<path>` blobs for subtle depth behind the chart.
- 1× `<filter id="cardShadow">` applied to pill bases and the leader label card.
- 1× `<filter id="softGlow">` applied to the top circular leader node and background accents.
- 2× gradients: one background linear gradient and one circular leader-node radial gradient.
- 16× `<rect>` for 8 layered pill nodes: colored base pill + white foreground pill.
- 1× larger white `<rect>` pill for the CEO label beneath the circular avatar.
- 1× large `<circle>` for the top hierarchy node, plus smaller circles/paths for the avatar icon.
- 8× small `<circle>` avatar placeholders inside subordinate pill cards.
- Multiple `<line>` connectors for the hierarchy spine, branch bus, and vertical drops.
- Multiple small `<circle>` connector joints to make the tree feel engineered and intentional.
- 12× `<text>` elements with explicit `width` attributes for title, subtitle, CEO label, and node labels.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFD"/>
      <stop offset="100%" stop-color="#EAF0F6"/>
    </linearGradient>
    <radialGradient id="leaderGrad" cx="35%" cy="28%" r="75%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#DFF7F3"/>
      <stop offset="100%" stop-color="#009688"/>
    </radialGradient>
    <filter id="cardShadow" x="-25%" y="-35%" width="150%" height="180%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .16 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-40,650 C150,560 250,710 410,610 C560,515 650,575 790,520 C930,465 1040,500 1330,390 L1330,760 L-40,760 Z" fill="#DCEAF5" opacity="0.55"/>
  <path d="M870,45 C1010,-25 1180,35 1225,160 C1260,260 1165,340 1035,310 C910,280 775,210 785,125 C790,88 825,62 870,45 Z" fill="#E1F5FE" opacity="0.75" filter="url(#softGlow)"/>

  <text x="64" y="58" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#263238">Leadership Operating Model</text>
  <text x="64" y="88" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#607D8B">Color-banded pill nodes clarify ownership while preserving a calm executive aesthetic.</text>

  <line x1="640" y1="218" x2="640" y2="238" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="190" y1="238" x2="1090" y2="238" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="190" y1="238" x2="190" y2="272" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="490" y1="238" x2="490" y2="272" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="790" y1="238" x2="790" y2="272" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="1090" y1="238" x2="1090" y2="272" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="190" y1="342" x2="190" y2="448" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="490" y1="342" x2="490" y2="448" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="790" y1="342" x2="790" y2="448" stroke="#AAB7C4" stroke-width="2"/>
  <line x1="1090" y1="342" x2="1090" y2="448" stroke="#AAB7C4" stroke-width="2"/>
  <circle cx="640" cy="238" r="5" fill="#FFFFFF" stroke="#90A4AE" stroke-width="2"/>
  <circle cx="190" cy="238" r="4" fill="#FFFFFF" stroke="#90A4AE" stroke-width="2"/>
  <circle cx="490" cy="238" r="4" fill="#FFFFFF" stroke="#90A4AE" stroke-width="2"/>
  <circle cx="790" cy="238" r="4" fill="#FFFFFF" stroke="#90A4AE" stroke-width="2"/>
  <circle cx="1090" cy="238" r="4" fill="#FFFFFF" stroke="#90A4AE" stroke-width="2"/>

  <circle cx="640" cy="104" r="56" fill="url(#leaderGrad)" stroke="#FFFFFF" stroke-width="8" filter="url(#softGlow)"/>
  <circle cx="640" cy="92" r="19" fill="#FFFFFF" opacity="0.95"/>
  <path d="M607,136 C614,116 626,108 640,108 C654,108 666,116 673,136 Z" fill="#FFFFFF" opacity="0.95"/>
  <rect x="515" y="158" width="250" height="60" rx="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="555" y="182" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#263238">
    <tspan x="640" dy="0">MAYA CHEN</tspan><tspan x="640" dy="20" font-size="12" font-weight="400" fill="#78909C">Chief Executive Officer</tspan>
  </text>

  <g transform="translate(65 272)">
    <rect x="0" y="0" width="250" height="70" rx="35" fill="#009688" filter="url(#cardShadow)"/>
    <rect x="32" y="0" width="218" height="70" rx="35" fill="#FFFFFF"/>
    <circle cx="68" cy="35" r="22" fill="#DDF5F1"/>
    <text x="100" y="30" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#263238"><tspan x="100" dy="0">ALEX MORGAN</tspan><tspan x="100" dy="19" font-size="11" font-weight="400" fill="#78909C">Operations Lead</tspan></text>
  </g>
  <g transform="translate(365 272)">
    <rect x="0" y="0" width="250" height="70" rx="35" fill="#1976D2" filter="url(#cardShadow)"/>
    <rect x="32" y="0" width="218" height="70" rx="35" fill="#FFFFFF"/>
    <circle cx="68" cy="35" r="22" fill="#E3F2FD"/>
    <text x="100" y="30" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#263238"><tspan x="100" dy="0">PRIYA RAO</tspan><tspan x="100" dy="19" font-size="11" font-weight="400" fill="#78909C">Product Lead</tspan></text>
  </g>
  <g transform="translate(665 272)">
    <rect x="0" y="0" width="250" height="70" rx="35" fill="#D32F2F" filter="url(#cardShadow)"/>
    <rect x="32" y="0" width="218" height="70" rx="35" fill="#FFFFFF"/>
    <circle cx="68" cy="35" r="22" fill="#FFEBEE"/>
    <text x="100" y="30" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#263238"><tspan x="100" dy="0">JORDAN LEE</tspan><tspan x="100" dy="19" font-size="11" font-weight="400" fill="#78909C">Revenue Lead</tspan></text>
  </g>
  <g transform="translate(965 272)">
    <rect x="0" y="0" width="250" height="70" rx="35" fill="#F57C00" filter="url(#cardShadow)"/>
    <rect x="32" y="0" width="218" height="70" rx="35" fill="#FFFFFF"/>
    <circle cx="68" cy="35" r="22" fill="#FFF3E0"/>
    <text x="100" y="30" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#263238"><tspan x="100" dy="0">SOFIA MARTIN</tspan><tspan x="100" dy="19" font-size="11" font-weight="400" fill="#78909C">People Lead</tspan></text>
  </g>

  <g transform="translate(80 448)">
    <rect x="0" y="0" width="220" height="64" rx="32" fill="#009688" filter="url(#cardShadow)"/>
    <rect x="28" y="0" width="192" height="64" rx="32" fill="#FFFFFF"/>
    <circle cx="60" cy="32" r="19" fill="#DDF5F1"/>
    <text x="90" y="28" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#263238"><tspan x="90" dy="0">NOAH KIM</tspan><tspan x="90" dy="17" font-size="10" font-weight="400" fill="#78909C">Supply Chain</tspan></text>
  </g>
  <g transform="translate(380 448)">
    <rect x="0" y="0" width="220" height="64" rx="32" fill="#1976D2" filter="url(#cardShadow)"/>
    <rect x="28" y="0" width="192" height="64" rx="32" fill="#FFFFFF"/>
    <circle cx="60" cy="32" r="19" fill="#E3F2FD"/>
    <text x="90" y="28" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#263238"><tspan x="90" dy="0">EMMA WILSON</tspan><tspan x="90" dy="17" font-size="10" font-weight="400" fill="#78909C">Platform PM</tspan></text>
  </g>
  <g transform="translate(680 448)">
    <rect x="0" y="0" width="220" height="64" rx="32" fill="#D32F2F" filter="url(#cardShadow)"/>
    <rect x="28" y="0" width="192" height="64" rx="32" fill="#FFFFFF"/>
    <circle cx="60" cy="32" r="19" fill="#FFEBEE"/>
    <text x="90" y="28" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#263238"><tspan x="90" dy="0">LIAM EVANS</tspan><tspan x="90" dy="17" font-size="10" font-weight="400" fill="#78909C">Enterprise Sales</tspan></text>
  </g>
  <g transform="translate(980 448)">
    <rect x="0" y="0" width="220" height="64" rx="32" fill="#F57C00" filter="url(#cardShadow)"/>
    <rect x="28" y="0" width="192" height="64" rx="32" fill="#FFFFFF"/>
    <circle cx="60" cy="32" r="19" fill="#FFF3E0"/>
    <text x="90" y="28" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#263238"><tspan x="90" dy="0">AVA GARCIA</tspan><tspan x="90" dy="17" font-size="10" font-weight="400" fill="#78909C">Talent Partner</tspan></text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to reveal the accent band; layer two rounded `<rect>` elements instead.
- ❌ Do not apply drop-shadow filters to `<line>` connectors; PowerPoint translation drops filters on lines.
- ❌ Do not use `marker-end` arrowheads for hierarchy connectors; use clean lines and joint circles.
- ❌ Do not create the whole chart as one raster image; each pill, connector, and label should remain editable.
- ❌ Do not rely on `<use>` or `<symbol>` for repeated nodes; duplicate the SVG shapes directly or generate them as explicit groups.

## Composition notes
- Keep the top leader node centered, with the first-level branch bus directly beneath it; this makes the hierarchy instantly legible.
- Give each pill generous horizontal breathing room; the white card body should dominate while the accent band stays around 10–15% of node width.
- Use muted background blues/grays so white cards and department colors feel crisp but not loud.
- Keep connector lines thin and neutral; the color rhythm should come from the pill bands, not from the hierarchy scaffolding.