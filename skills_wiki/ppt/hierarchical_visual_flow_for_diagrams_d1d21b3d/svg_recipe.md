# SVG Recipe — Hierarchical Visual Flow for Diagrams

## Visual mechanism
Use visual weight to encode hierarchy: the top node is dark and solid, mid-level nodes use lighter gradients, and detail nodes become pale or outline-only. Smooth curved connectors create an organic top-down flow so the viewer reads authority, dependency, or process order without heavy container boxes.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft background
- 2× `<path>` for large translucent decorative background flows
- 18× `<path>` for smooth curved hierarchy connectors, including a main trunk and branch lines
- 1× `<rect>` for the dominant Level 1 root node
- 1× `<rect>` for the Level 1/2 bridge node
- 7× `<rect>` for major department / category nodes
- 17× `<rect>` for lower-level role nodes with pale fills or outline styling
- 26× `<text>` for labels, all with explicit `width`
- 3× `<linearGradient>` for dark, medium, and pale hierarchical fills
- 1× `<radialGradient>` for a subtle spotlight behind the structure
- 1× `<filter id="softShadow">` applied to primary and secondary node rectangles
- 1× `<filter id="glow">` applied to the root node for keynote-style emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F3FBFA"/>
      <stop offset="100%" stop-color="#E8F2F1"/>
    </linearGradient>
    <radialGradient id="spotlight" cx="50%" cy="22%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rootGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0E7772"/>
      <stop offset="100%" stop-color="#074C4A"/>
    </linearGradient>
    <linearGradient id="midGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#39B3AD"/>
      <stop offset="100%" stop-color="#1D8C87"/>
    </linearGradient>
    <linearGradient id="softGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#DDF1EF"/>
      <stop offset="100%" stop-color="#B9DCDA"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02 0 0 0 0 0.16 0 0 0 0 0.15 0 0 0 0.18 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-30%" y="-45%" width="160%" height="190%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>
  <path d="M-40 620 C180 520 300 610 500 520 C760 400 880 500 1110 360 C1210 300 1300 290 1340 330 L1340 760 L-40 760 Z" fill="#B8DEDB" opacity="0.22"/>
  <path d="M930 -40 C1050 80 1000 170 1135 245 C1225 295 1300 282 1350 360 L1350 -40 Z" fill="#54B9B3" opacity="0.14"/>

  <text x="70" y="54" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#123E3C">Hierarchical Service Organization Flow</text>
  <text x="70" y="84" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5A7472">Visual weight, color depth, and connector curvature reveal level, authority, and dependency.</text>

  <path d="M640 128 C640 150 640 164 640 184" fill="none" stroke="#4C9F9A" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M640 248 C640 286 640 292 640 316" fill="none" stroke="#4C9F9A" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M640 248 C545 282 245 270 165 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M640 248 C570 282 300 285 260 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M640 248 C598 280 435 288 420 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M640 248 C620 280 540 290 580 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M640 248 C662 280 735 290 740 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M640 248 C700 280 890 285 900 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M640 248 C760 282 1040 272 1060 318" fill="none" stroke="#4C9F9A" stroke-width="2.5" stroke-linecap="round"/>

  <path d="M165 384 C165 412 92 414 92 442" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M165 384 C165 412 165 414 165 442" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M165 384 C165 412 238 414 238 442" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M420 384 C420 420 365 426 365 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M420 384 C420 420 475 426 475 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M580 384 C580 420 525 426 525 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M580 384 C580 420 635 426 635 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M900 384 C900 420 845 426 845 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M900 384 C900 420 955 426 955 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M1060 384 C1060 420 1005 426 1005 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>
  <path d="M1060 384 C1060 420 1115 426 1115 462" fill="none" stroke="#7DBBB7" stroke-width="2" stroke-dasharray="5 8" stroke-linecap="round"/>

  <rect x="520" y="62" width="240" height="66" rx="22" fill="url(#rootGrad)" filter="url(#glow)"/>
  <text x="640" y="91" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">General Manager</text>
  <text x="640" y="113" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D8F5F2">strategic ownership</text>

  <rect x="500" y="184" width="280" height="64" rx="19" fill="url(#midGrad)" filter="url(#softShadow)"/>
  <text x="640" y="211" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Operations Director</text>
  <text x="640" y="232" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#E7FFFD">coordinates cross-functional flow</text>

  <rect x="105" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>
  <rect x="200" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>
  <rect x="360" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>
  <rect x="520" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>
  <rect x="680" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>
  <rect x="840" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>
  <rect x="1000" y="318" width="120" height="66" rx="18" fill="url(#softGrad)" filter="url(#softShadow)"/>

  <text x="165" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">Finance</text>
  <text x="260" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">Engineering</text>
  <text x="420" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">People</text>
  <text x="580" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">Marketing</text>
  <text x="740" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">Security</text>
  <text x="900" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">Rooms</text>
  <text x="1060" y="357" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#115C59">Dining</text>

  <rect x="42" y="442" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="115" y="442" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="188" y="442" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="315" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="425" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="475" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="585" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="790" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="900" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="950" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>
  <rect x="1060" y="462" width="100" height="42" rx="14" fill="#FFFFFF" stroke="#76BDB8" stroke-width="2"/>

  <text x="92" y="468" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Accounting</text>
  <text x="165" y="468" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Cashier</text>
  <text x="238" y="468" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Procure</text>
  <text x="365" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Recruit</text>
  <text x="475" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Payroll</text>
  <text x="525" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Regional</text>
  <text x="635" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Digital</text>
  <text x="840" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Housekeep</text>
  <text x="950" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Front Desk</text>
  <text x="1000" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Kitchen</text>
  <text x="1110" y="488" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#274B49">Service</text>
</svg>
```

## Avoid in this skill
- ❌ Do not make every node the same fill, stroke, and font size; that destroys the hierarchy signal.
- ❌ Do not use rigid right-angle connectors everywhere when the diagram needs a softer executive look; curved `<path>` connectors are more readable and premium.
- ❌ Do not put arrowheads on curved `<path>` connectors with `marker-end`; if arrows are required, use separate `<line>` elements with `marker-end` directly on each line.
- ❌ Do not rely on container boxes around every subgroup; use proximity, color depth, and connector routing to imply grouping cleanly.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint translation depends on explicit text widths.

## Composition notes
- Keep the root node near the upper center with generous negative space so it feels like the clear source of authority or flow.
- Use darker, heavier fills only for the top 1–2 levels; lower levels should become lighter, smaller, or outline-only.
- Route connectors behind nodes first, then draw nodes and labels above them for a clean layered structure.
- Use a restrained monochromatic palette, then vary opacity, gradient depth, and stroke style to create hierarchy without visual noise.