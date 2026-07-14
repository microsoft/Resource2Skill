# SVG Recipe — Cyclical Ecosystem Tri-Node Diagram

## Visual mechanism
A closed-loop ecosystem is shown as three translucent circular nodes arranged in an equilateral triangle, with separated curved arrows orbiting between them. The invisible larger circle creates momentum and continuity while the left-side narrative block explains the macro context.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× decorative `<circle>` / `<ellipse>` glows for atmospheric depth behind the diagram
- 3× large semi-transparent `<circle>` nodes for the ecosystem actors
- 3× `<path>` stroked arc segments for the directional cycle
- 3× small filled `<path>` triangle arrowheads, rotated manually at arc endpoints
- 1× faint dashed `<circle>` for the implied orbit guide
- 1× `<rect>` translucent information panel on the left
- Multiple `<text>` elements with explicit `width` for title, subtitle, node labels, and small annotations
- 2× `<linearGradient>` fills for background and node glass effect
- 1× `<radialGradient>` for soft highlight glow
- 2× `<filter>` effects: one soft shadow for nodes/panel, one Gaussian glow for background accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0.85" y2="1">
      <stop offset="0%" stop-color="#F05A48"/>
      <stop offset="45%" stop-color="#D72E2E"/>
      <stop offset="100%" stop-color="#8E151E"/>
    </linearGradient>

    <radialGradient id="hotGlow" cx="42%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#FFB067" stop-opacity="0.75"/>
      <stop offset="48%" stop-color="#F04A3D" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#7B1018" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="nodeFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF8A73" stop-opacity="0.78"/>
      <stop offset="55%" stop-color="#E33B35" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#B81824" stop-opacity="0.50"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="520" cy="130" rx="520" ry="260" fill="url(#hotGlow)" filter="url(#glow)"/>
  <circle cx="1050" cy="140" r="190" fill="#FF9075" opacity="0.12" filter="url(#glow)"/>
  <circle cx="1080" cy="640" r="260" fill="#6E0D17" opacity="0.20" filter="url(#glow)"/>

  <rect x="72" y="96" width="394" height="528" rx="34" fill="#FFFFFF" opacity="0.10" stroke="#FFFFFF" stroke-opacity="0.22" filter="url(#softShadow)"/>

  <text x="104" y="152" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#FFE6DE" letter-spacing="2">
    CLOSED-LOOP MODEL
  </text>
  <text x="104" y="222" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF">
    智慧手機生態圈
    <tspan x="104" dy="56" font-size="42" font-weight="600">Smart Phone APP</tspan>
  </text>
  <text x="106" y="358" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFE8E2" opacity="0.92">
    Three actors exchange value in a continuous orbit: users create demand, developers deliver services, and platforms scale the network.
  </text>

  <line x1="108" y1="432" x2="396" y2="432" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="1.5"/>
  <text x="106" y="478" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#FFFFFF" font-weight="600">
    System behavior
  </text>
  <text x="106" y="516" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#FFD5CC">
    Directional arcs indicate how each node reinforces the next, creating a self-sustaining ecosystem.
  </text>

  <circle cx="860" cy="360" r="250" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.18" stroke-dasharray="8 18"/>

  <path d="M 1003 155 A 250 250 0 0 1 1109 382" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.92"/>
  <path d="M 1003 565 A 250 250 0 0 1 717 565" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.92"/>
  <path d="M 611 382 A 250 250 0 0 1 717 155" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.92"/>

  <path d="M 0 -12 L 25 0 L 0 12 Z" fill="#FFFFFF" transform="translate(1109 382) rotate(95)"/>
  <path d="M 0 -12 L 25 0 L 0 12 Z" fill="#FFFFFF" transform="translate(717 565) rotate(215)"/>
  <path d="M 0 -12 L 25 0 L 0 12 Z" fill="#FFFFFF" transform="translate(717 155) rotate(-25)"/>

  <circle cx="860" cy="180" r="108" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="1016" cy="450" r="108" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="704" cy="450" r="108" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="2" filter="url(#softShadow)"/>

  <circle cx="826" cy="145" r="30" fill="#FFFFFF" opacity="0.12"/>
  <circle cx="982" cy="415" r="30" fill="#FFFFFF" opacity="0.12"/>
  <circle cx="670" cy="415" r="30" fill="#FFFFFF" opacity="0.12"/>

  <text x="760" y="164" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#FFFFFF">
    USERS
  </text>
  <text x="760" y="202" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFE6DF">
    demand · feedback · data
  </text>

  <text x="916" y="434" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#FFFFFF">
    PLATFORM
  </text>
  <text x="916" y="472" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFE6DF">
    scale · trust · distribution
  </text>

  <text x="604" y="434" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#FFFFFF">
    DEVELOPERS
  </text>
  <text x="604" y="472" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFE6DF">
    apps · services · innovation
  </text>

  <text x="760" y="354" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#FFD8D0" opacity="0.88">
    value circulates continuously
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` on curved `<path>` arcs; PowerPoint translation may drop the arrowheads. Draw arrowheads as separate small filled `<path>` triangles instead.
- ❌ Do not use `<animate>` or wheel/spin SVG animation; create the static end-state and add animation later inside PowerPoint if needed.
- ❌ Do not use `<mask>` to create glassy nodes; use semi-transparent fills, gradients, and strokes.
- ❌ Do not place text inside clipped groups or rely on auto-fit; every `<text>` needs an explicit `width`.

## Composition notes
- Reserve the left 30–35% of the slide for title, explanation, and system framing; keep the diagram dominant on the right.
- Place the three nodes around a shared center and keep arc radius slightly larger than node radius so arrows feel like an orbit, not connector lines.
- Use a warm monochrome background with white arcs and labels for high contrast; node transparency should feel like layered glass.
- Keep the center of the triangle mostly open so the circular flow remains readable and premium, not cluttered.