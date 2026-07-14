# SVG Recipe — Hierarchical Network Topology Diagram

## Visual mechanism
A structured top-down infrastructure map uses distinct device icons for core hub, distribution switches, and endpoint workstations. Orthogonal elbow connectors create clean routing lanes so relationships read like an engineered network schematic rather than a loose mind map.

## SVG primitives needed
- 1× `<rect>` for the white slide background.
- 1× subtle `<rect>` band for the title/header area.
- 10× rounded `<rect>` node cards behind devices to visually group icons and labels.
- 4× switch/router icon assemblies made from `<rect>`, `<path>`, `<circle>`, and `<line>` for chassis, ports, LEDs, and antennas.
- 9× workstation icon assemblies made from `<rect>`, `<path>`, `<ellipse>`, and `<line>` for monitors, towers, bases, keyboards, and mice.
- 12× `<path>` orthogonal elbow connectors using `M / V / H / V` commands.
- 1× `<linearGradient>` for router and switch face highlights.
- 1× `<linearGradient>` for workstation screen fills.
- 1× `<filter id="softShadow">` applied to icon/card rectangles and paths for editable depth.
- Multiple `<text width="...">` labels for title, tier captions, and node names.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="coreBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2FA7F7"/>
      <stop offset="100%" stop-color="#1E5F93"/>
    </linearGradient>
    <linearGradient id="switchSlate" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3D5269"/>
      <stop offset="100%" stop-color="#223140"/>
    </linearGradient>
    <linearGradient id="screenBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#72C8FF"/>
      <stop offset="55%" stop-color="#2378BD"/>
      <stop offset="100%" stop-color="#134875"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="86" fill="#F7FAFC"/>
  <text x="640" y="43" width="760" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="28" font-weight="700" fill="#243447">Enterprise 10Base‑T Star Network Topology</text>
  <text x="640" y="68" width="680" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="13" fill="#6B7C8F">Core hub routes traffic to distribution switches and endpoint workstations through orthogonal cable lanes</text>

  <text x="64" y="133" width="150" font-family="Verdana, Segoe UI" font-size="11" font-weight="700" fill="#8AA0B6">CORE</text>
  <text x="64" y="310" width="150" font-family="Verdana, Segoe UI" font-size="11" font-weight="700" fill="#8AA0B6">DISTRIBUTION</text>
  <text x="64" y="552" width="150" font-family="Verdana, Segoe UI" font-size="11" font-weight="700" fill="#8AA0B6">ENDPOINTS</text>
  <line x1="132" y1="129" x2="1210" y2="129" stroke="#E6EEF5" stroke-width="1"/>
  <line x1="174" y1="306" x2="1210" y2="306" stroke="#E6EEF5" stroke-width="1"/>
  <line x1="156" y1="548" x2="1210" y2="548" stroke="#E6EEF5" stroke-width="1"/>

  <!-- Orthogonal backbone connectors -->
  <path d="M640 154 V202 H330 V248" fill="none" stroke="#5F7FA3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640 154 V202 H950 V248" fill="none" stroke="#5F7FA3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640 154 V332 H640 V382" fill="none" stroke="#5F7FA3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M330 326 V398 H164 V470" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M330 326 V398 H330 V470" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M330 326 V398 H496 V470" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M950 326 V398 H818 V470" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M950 326 V398 H982 V470" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M950 326 V398 H1144 V470" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640 458 V506 H500 V548" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640 458 V506 H640 V548" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640 458 V506 H780 V548" fill="none" stroke="#88A3BD" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Core router -->
  <g transform="translate(570 92)">
    <rect x="-10" y="-8" width="160" height="94" rx="18" fill="#FFFFFF" stroke="#E8EEF5" filter="url(#softShadow)"/>
    <line x1="24" y1="24" x2="6" y2="-4" stroke="#2C3E50" stroke-width="5" stroke-linecap="round"/>
    <line x1="116" y1="24" x2="134" y2="-4" stroke="#2C3E50" stroke-width="5" stroke-linecap="round"/>
    <rect x="10" y="20" width="120" height="50" rx="11" fill="url(#coreBlue)" stroke="#1B5C89" stroke-width="2.5"/>
    <circle cx="52" cy="45" r="4" fill="#2ECC71"/>
    <circle cx="68" cy="45" r="4" fill="#2ECC71"/>
    <circle cx="84" cy="45" r="4" fill="#2ECC71"/>
    <text x="70" y="101" width="150" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="13" font-weight="700" fill="#12619A">Core Hub</text>
  </g>

  <!-- Distribution switches -->
  <g transform="translate(255 248)">
    <rect x="-16" y="-14" width="182" height="112" rx="16" fill="#FFFFFF" stroke="#E8EEF5" filter="url(#softShadow)"/>
    <path d="M10 10 L145 10 L154 26 L0 26 Z" fill="#34495E"/>
    <rect x="0" y="26" width="154" height="42" rx="4" fill="url(#switchSlate)" stroke="#1C2733" stroke-width="2"/>
    <rect x="22" y="39" width="10" height="11" fill="#2ECC71"/><rect x="40" y="39" width="10" height="11" fill="#2ECC71"/><rect x="58" y="39" width="10" height="11" fill="#2ECC71"/><rect x="76" y="39" width="10" height="11" fill="#2ECC71"/><rect x="94" y="39" width="10" height="11" fill="#2ECC71"/><rect x="112" y="39" width="10" height="11" fill="#2ECC71"/>
    <text x="77" y="93" width="160" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="13" fill="#176CA8">Switch A</text>
  </g>
  <g transform="translate(875 248)">
    <rect x="-16" y="-14" width="182" height="112" rx="16" fill="#FFFFFF" stroke="#E8EEF5" filter="url(#softShadow)"/>
    <path d="M10 10 L145 10 L154 26 L0 26 Z" fill="#34495E"/>
    <rect x="0" y="26" width="154" height="42" rx="4" fill="url(#switchSlate)" stroke="#1C2733" stroke-width="2"/>
    <rect x="22" y="39" width="10" height="11" fill="#2ECC71"/><rect x="40" y="39" width="10" height="11" fill="#2ECC71"/><rect x="58" y="39" width="10" height="11" fill="#2ECC71"/><rect x="76" y="39" width="10" height="11" fill="#2ECC71"/><rect x="94" y="39" width="10" height="11" fill="#2ECC71"/><rect x="112" y="39" width="10" height="11" fill="#2ECC71"/>
    <text x="77" y="93" width="160" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="13" fill="#176CA8">Switch B</text>
  </g>
  <g transform="translate(565 380)">
    <rect x="-16" y="-14" width="182" height="112" rx="16" fill="#FFFFFF" stroke="#E8EEF5" filter="url(#softShadow)"/>
    <path d="M10 10 L145 10 L154 26 L0 26 Z" fill="#34495E"/>
    <rect x="0" y="26" width="154" height="42" rx="4" fill="url(#switchSlate)" stroke="#1C2733" stroke-width="2"/>
    <rect x="22" y="39" width="10" height="11" fill="#2ECC71"/><rect x="40" y="39" width="10" height="11" fill="#2ECC71"/><rect x="58" y="39" width="10" height="11" fill="#2ECC71"/><rect x="76" y="39" width="10" height="11" fill="#2ECC71"/><rect x="94" y="39" width="10" height="11" fill="#2ECC71"/><rect x="112" y="39" width="10" height="11" fill="#2ECC71"/>
    <text x="77" y="93" width="160" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="13" fill="#176CA8">Switch C</text>
  </g>

  <!-- Workstations -->
  <g transform="translate(124 470)">
    <rect x="-30" y="-20" width="140" height="116" rx="16" fill="#FFFFFF" stroke="#E9EEF4" filter="url(#softShadow)"/>
    <rect x="8" y="0" width="76" height="58" rx="5" fill="#9AA7B0" stroke="#6F7D86" stroke-width="2"/><rect x="14" y="7" width="64" height="42" fill="url(#screenBlue)"/>
    <rect x="40" y="58" width="12" height="18" fill="#7A8790"/><rect x="24" y="76" width="44" height="7" rx="3" fill="#7A8790"/>
    <rect x="78" y="55" width="33" height="24" rx="4" fill="#2D3339"/><ellipse cx="118" cy="78" rx="8" ry="4" fill="#536E78"/>
    <text x="40" y="107" width="120" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="12" fill="#176CA8">Workstation</text>
  </g>
  <g transform="translate(290 470)">
    <rect x="-30" y="-20" width="140" height="116" rx="16" fill="#FFFFFF" stroke="#E9EEF4" filter="url(#softShadow)"/>
    <rect x="8" y="0" width="76" height="58" rx="5" fill="#9AA7B0" stroke="#6F7D86" stroke-width="2"/><rect x="14" y="7" width="64" height="42" fill="url(#screenBlue)"/>
    <rect x="40" y="58" width="12" height="18" fill="#7A8790"/><rect x="24" y="76" width="44" height="7" rx="3" fill="#7A8790"/>
    <rect x="78" y="55" width="33" height="24" rx="4" fill="#2D3339"/><ellipse cx="118" cy="78" rx="8" ry="4" fill="#536E78"/>
    <text x="40" y="107" width="120" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="12" fill="#176CA8">Workstation</text>
  </g>
  <g transform="translate(456 470)">
    <rect x="-30" y="-20" width="140" height="116" rx="16" fill="#FFFFFF" stroke="#E9EEF4" filter="url(#softShadow)"/>
    <rect x="8" y="0" width="76" height="58" rx="5" fill="#9AA7B0" stroke="#6F7D86" stroke-width="2"/><rect x="14" y="7" width="64" height="42" fill="url(#screenBlue)"/>
    <rect x="40" y="58" width="12" height="18" fill="#7A8790"/><rect x="24" y="76" width="44" height="7" rx="3" fill="#7A8790"/>
    <rect x="78" y="55" width="33" height="24" rx="4" fill="#2D3339"/><ellipse cx="118" cy="78" rx="8" ry="4" fill="#536E78"/>
    <text x="40" y="107" width="120" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="12" fill="#176CA8">Workstation</text>
  </g>
  <g transform="translate(778 470)">
    <rect x="-30" y="-20" width="140" height="116" rx="16" fill="#FFFFFF" stroke="#E9EEF4" filter="url(#softShadow)"/>
    <rect x="8" y="0" width="76" height="58" rx="5" fill="#9AA7B0" stroke="#6F7D86" stroke-width="2"/><rect x="14" y="7" width="64" height="42" fill="url(#screenBlue)"/>
    <rect x="40" y="58" width="12" height="18" fill="#7A8790"/><rect x="24" y="76" width="44" height="7" rx="3" fill="#7A8790"/>
    <rect x="78" y="55" width="33" height="24" rx="4" fill="#2D3339"/><ellipse cx="118" cy="78" rx="8" ry="4" fill="#536E78"/>
    <text x="40" y="107" width="120" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="12" fill="#176CA8">Workstation</text>
  </g>
  <g transform="translate(942 470)">
    <rect x="-30" y="-20" width="140" height="116" rx="16" fill="#FFFFFF" stroke="#E9EEF4" filter="url(#softShadow)"/>
    <rect x="8" y="0" width="76" height="58" rx="5" fill="#9AA7B0" stroke="#6F7D86" stroke-width="2"/><rect x="14" y="7" width="64" height="42" fill="url(#screenBlue)"/>
    <rect x="40" y="58" width="12" height="18" fill="#7A8790"/><rect x="24" y="76" width="44" height="7" rx="3" fill="#7A8790"/>
    <rect x="78" y="55" width="33" height="24" rx="4" fill="#2D3339"/><ellipse cx="118" cy="78" rx="8" ry="4" fill="#536E78"/>
    <text x="40" y="107" width="120" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="12" fill="#176CA8">Workstation</text>
  </g>
  <g transform="translate(1104 470)">
    <rect x="-30" y="-20" width="140" height="116" rx="16" fill="#FFFFFF" stroke="#E9EEF4" filter="url(#softShadow)"/>
    <rect x="8" y="0" width="76" height="58" rx="5" fill="#9AA7B0" stroke="#6F7D86" stroke-width="2"/><rect x="14" y="7" width="64" height="42" fill="url(#screenBlue)"/>
    <rect x="40" y="58" width="12" height="18" fill="#7A8790"/><rect x="24" y="76" width="44" height="7" rx="3" fill="#7A8790"/>
    <rect x="78" y="55" width="33" height="24" rx="4" fill="#2D3339"/><ellipse cx="118" cy="78" rx="8" ry="4" fill="#536E78"/>
    <text x="40" y="107" width="120" text-anchor="middle" font-family="Verdana, Segoe UI" font-size="12" fill="#176CA8">Workstation</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` on connector paths; arrowheads on paths may disappear, so keep topology links as clean stroked elbow paths or use explicit shapes for arrows if required.
- ❌ Diagonal direct links between hierarchy levels; they quickly create visual clutter and weaken the engineered schematic style.
- ❌ `<use>` for repeated workstation or switch icons; duplicate the editable primitives directly so the PPTX remains safe.
- ❌ `skewX`, `skewY`, or `matrix()` transforms for pseudo-3D hardware; use simple polygon `<path>` top faces instead.
- ❌ Applying `filter` to `<line>` elements; use shadows on cards, device bodies, or paths, not lines.

## Composition notes
- Keep the root device centered in the upper third, distribution devices in the middle band, and endpoints along the lower band.
- Route connectors through shared vertical and horizontal “lanes” with consistent stroke widths; avoid crossings whenever possible.
- Use blue for the primary/core layer, dark slate for switching hardware, green for ports/status lights, and muted blue-gray for cables.
- Leave generous white space between clusters so the eye can trace each parent-child relationship without competing labels.