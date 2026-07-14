# SVG Recipe — Sleek Process Flow Diagram

## Visual mechanism
A premium flowchart is built from teal geometric nodes with thick white outlines and soft shadows, connected by crisp orange orthogonal routes with arrowheads. The layout reads left-to-right, splits into three parallel process lanes, then converges into a final action and end state.

## SVG primitives needed
- 2× `<rect>` for the soft full-slide background and the white title banner
- 1× `<radialGradient>` for a subtle spotlight background wash
- 1× `<linearGradient>` for dimensional teal node fills
- 1× `<filter id="nodeShadow">` applied to all process nodes for lift
- 2× `<circle>` for START and END nodes
- 3× `<rect rx>` for rounded PROCESS nodes
- 2× `<path>` for the DECISION diamond and ACTION parallelogram
- 13× `<line>` for straight and orthogonal orange connector segments
- 8× small `<path>` triangles for custom arrowheads instead of SVG markers
- 8× `<text>` labels, each with explicit `width` for clean PowerPoint rendering

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#F8FCFC"/>
      <stop offset="48%" stop-color="#DFF4F2"/>
      <stop offset="100%" stop-color="#B7E4E1"/>
    </radialGradient>

    <linearGradient id="tealNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#09908B"/>
      <stop offset="100%" stop-color="#00756F"/>
    </linearGradient>

    <filter id="nodeShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
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
  </defs>

  <!-- Background and title band -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <rect x="0" y="18" width="1280" height="74" fill="#FFFFFF" opacity="0.96"/>

  <text x="640" y="74" width="1080" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="52"
        font-weight="700" letter-spacing="2" fill="#141926">
    FLOWCHART/PROCESS FLOW DIAGRAM
  </text>

  <!-- Orange connectors, routed underneath nodes -->
  <g stroke="#F29A13" stroke-width="4" stroke-linecap="square" fill="none">
    <line x1="256" y1="360" x2="338" y2="360"/>
    <line x1="486" y1="360" x2="532" y2="360"/>
    <line x1="728" y1="360" x2="804" y2="360"/>
    <line x1="1002" y1="360" x2="1120" y2="360"/>

    <line x1="427" y1="302" x2="427" y2="164"/>
    <line x1="427" y1="164" x2="548" y2="164"/>

    <line x1="427" y1="418" x2="427" y2="558"/>
    <line x1="427" y1="558" x2="548" y2="558"/>

    <line x1="730" y1="164" x2="782" y2="164"/>
    <line x1="782" y1="164" x2="782" y2="558"/>
    <line x1="730" y1="558" x2="782" y2="558"/>

    <line x1="782" y1="360" x2="804" y2="360"/>
  </g>

  <!-- Custom arrowheads; use paths, not marker-end on paths -->
  <g fill="#F29A13" stroke="none">
    <path d="M338 360 L320 350 L320 370 Z"/>
    <path d="M532 360 L514 350 L514 370 Z"/>
    <path d="M548 164 L530 154 L530 174 Z"/>
    <path d="M548 558 L530 548 L530 568 Z"/>
    <path d="M804 360 L786 350 L786 370 Z"/>
    <path d="M1120 360 L1102 350 L1102 370 Z"/>
  </g>

  <!-- Nodes -->
  <circle cx="208" cy="360" r="48" fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="208" y="367" width="92" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" fill="#FFFFFF">
    START
  </text>

  <path d="M427 303 L485 360 L427 417 L369 360 Z"
        fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="427" y="367" width="118" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" fill="#FFFFFF">
    DECISION
  </text>

  <rect x="550" y="128" width="180" height="72" rx="14" ry="14"
        fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="640" y="170" width="160" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" fill="#FFFFFF">
    PROCESS 1
  </text>

  <rect x="550" y="324" width="180" height="72" rx="14" ry="14"
        fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="640" y="366" width="160" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" fill="#FFFFFF">
    PROCESS 2
  </text>

  <rect x="550" y="522" width="180" height="72" rx="14" ry="14"
        fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="640" y="564" width="160" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" fill="#FFFFFF">
    PROCESS 3
  </text>

  <path d="M846 324 L1006 324 L986 396 L826 396 Z"
        fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="916" y="367" width="150" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="700" fill="#FFFFFF">
    ACTION
  </text>

  <circle cx="1176" cy="360" r="48" fill="url(#tealNode)" stroke="#FFFFFF" stroke-width="4" filter="url(#nodeShadow)"/>
  <text x="1176" y="367" width="92" text-anchor="middle"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" fill="#FFFFFF">
    END
  </text>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` on `<path>` connectors; custom triangle arrowheads or direct `<line marker-end>` are safer, and triangle paths are easiest to edit visually.
- ❌ Thin black connector strokes; the style depends on bold orange routing with clear 90-degree turns.
- ❌ Mixed node colors or default flowchart outlines; keep teal fills and thick white borders for a unified premium look.
- ❌ Freeform diagonal connector routing except where the node geometry itself demands it; the process logic should feel grid-aligned and operationally precise.
- ❌ Applying filters to `<line>` connectors; shadows should be reserved for nodes because line filters may be dropped.

## Composition notes
- Keep the main logic centered vertically, with START, DECISION, PROCESS 2, ACTION, and END sharing the same horizontal axis.
- Use the upper and lower lanes only for parallel branches; leave generous negative space between PROCESS 1, PROCESS 2, and PROCESS 3.
- Put connectors behind nodes so white node borders visually “cut” the orange lines cleanly.
- Use a calm cyan background and white title band to let the teal/orange diagram carry the visual energy.