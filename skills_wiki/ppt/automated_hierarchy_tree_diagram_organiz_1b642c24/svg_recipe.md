# SVG Recipe — Automated Hierarchy Tree Diagram (Organizational Chart)

## Visual mechanism
A top-down hierarchy is rendered as stacked node levels connected by orthogonal elbow lines, making reporting or containment relationships instantly scannable. Premium styling comes from rounded gradient cards, subtle shadows, role-based color coding, and optional circular headshots embedded inside higher-level nodes.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for the large white chart canvas/card
- 1× `<path>` for a soft decorative background accent shape
- 14× `<rect>` for hierarchy nodes across root, manager, and department levels
- 21× `<line>` for editable orthogonal connector segments
- 6× `<image>` clipped into circular headshots for executive/manager nodes
- 6× `<circle>` for avatar border rings
- 14× `<text>` for node labels, each with explicit `width=`
- 2× `<text>` for slide title/subtitle, each with explicit `width=`
- 4× `<linearGradient>` for background, card/node fills, and level-based color depth
- 1× `<radialGradient>` for the ambient accent glow
- 1× `<filter id="softShadow">` applied to card and nodes
- 6× `<clipPath>` using `<circle>` applied only to `<image>` elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4F8FF"/>
      <stop offset="55%" stop-color="#EEF4FB"/>
      <stop offset="100%" stop-color="#E7EEF8"/>
    </linearGradient>
    <linearGradient id="rootGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2F5597"/>
      <stop offset="100%" stop-color="#163A72"/>
    </linearGradient>
    <linearGradient id="managerGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5B9BD5"/>
      <stop offset="100%" stop-color="#2F75B5"/>
    </linearGradient>
    <linearGradient id="deptGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F9FBFE"/>
      <stop offset="100%" stop-color="#DDEAF7"/>
    </linearGradient>
    <radialGradient id="accentGlow" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#7FC7FF" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#7FC7FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="clipCEO"><circle cx="578" cy="183" r="24"/></clipPath>
    <clipPath id="clipA"><circle cx="146" cy="331" r="20"/></clipPath>
    <clipPath id="clipB"><circle cx="354" cy="331" r="20"/></clipPath>
    <clipPath id="clipC"><circle cx="562" cy="331" r="20"/></clipPath>
    <clipPath id="clipD"><circle cx="770" cy="331" r="20"/></clipPath>
    <clipPath id="clipE"><circle cx="978" cy="331" r="20"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-80,610 C120,500 190,650 360,565 C520,485 620,565 760,500 C880,445 1000,420 1370,505 L1370,760 L-80,760 Z"
        fill="url(#accentGlow)" opacity="0.8"/>

  <text x="640" y="58" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#24364B">
    Company Organizational Structure
  </text>
  <text x="640" y="88" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7A90">
    Reporting lines, department ownership, and operating teams at a glance
  </text>

  <rect x="50" y="112" width="1180" height="555" rx="28" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.96"/>
  <rect x="78" y="140" width="1124" height="499" rx="22" fill="none" stroke="#D7E3F1" stroke-width="1.2"/>

  <!-- Root to manager level connectors -->
  <line x1="640" y1="221" x2="640" y2="264" stroke="#9AAEC6" stroke-width="2.4"/>
  <line x1="206" y1="264" x2="1038" y2="264" stroke="#9AAEC6" stroke-width="2.4"/>
  <line x1="206" y1="264" x2="206" y2="305" stroke="#9AAEC6" stroke-width="2.4"/>
  <line x1="414" y1="264" x2="414" y2="305" stroke="#9AAEC6" stroke-width="2.4"/>
  <line x1="622" y1="264" x2="622" y2="305" stroke="#9AAEC6" stroke-width="2.4"/>
  <line x1="830" y1="264" x2="830" y2="305" stroke="#9AAEC6" stroke-width="2.4"/>
  <line x1="1038" y1="264" x2="1038" y2="305" stroke="#9AAEC6" stroke-width="2.4"/>

  <!-- Department connectors -->
  <line x1="414" y1="381" x2="414" y2="424" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="388" y1="424" x2="494" y2="424" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="388" y1="424" x2="388" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="494" y1="424" x2="494" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="622" y1="381" x2="622" y2="424" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="562" y1="424" x2="682" y2="424" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="562" y1="424" x2="562" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="622" y1="424" x2="622" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="682" y1="424" x2="682" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="1038" y1="381" x2="1038" y2="424" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="978" y1="424" x2="1098" y2="424" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="978" y1="424" x2="978" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="1038" y1="424" x2="1038" y2="468" stroke="#B7C6D8" stroke-width="2"/>
  <line x1="1098" y1="424" x2="1098" y2="468" stroke="#B7C6D8" stroke-width="2"/>

  <!-- Root node -->
  <rect x="540" y="145" width="200" height="76" rx="16" fill="url(#rootGrad)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/headshots/confident-ceo-portrait.jpg" x="554" y="159" width="48" height="48" clip-path="url(#clipCEO)"/>
  <circle cx="578" cy="183" r="25" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <text x="616" y="179" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">General Manager</text>
  <text x="616" y="199" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#DCEBFF">Executive Office</text>

  <!-- Manager nodes -->
  <rect x="118" y="305" width="176" height="76" rx="14" fill="url(#managerGrad)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/headshots/executive-assistant.jpg" x="126" y="311" width="40" height="40" clip-path="url(#clipA)"/>
  <circle cx="146" cy="331" r="21" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="176" y="333" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">GM Assistant</text>
  <text x="176" y="352" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#EAF4FF">Coordination</text>

  <rect x="326" y="305" width="176" height="76" rx="14" fill="url(#managerGrad)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/headshots/rd-director.jpg" x="334" y="311" width="40" height="40" clip-path="url(#clipB)"/>
  <circle cx="354" cy="331" r="21" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="384" y="333" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">R&amp;D Dept</text>
  <text x="384" y="352" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#EAF4FF">Product Innovation</text>

  <rect x="534" y="305" width="176" height="76" rx="14" fill="url(#managerGrad)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/headshots/sales-director.jpg" x="542" y="311" width="40" height="40" clip-path="url(#clipC)"/>
  <circle cx="562" cy="331" r="21" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="592" y="333" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Sales Dept</text>
  <text x="592" y="352" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#EAF4FF">Revenue Growth</text>

  <rect x="742" y="305" width="176" height="76" rx="14" fill="url(#managerGrad)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/headshots/logistics-manager.jpg" x="750" y="311" width="40" height="40" clip-path="url(#clipD)"/>
  <circle cx="770" cy="331" r="21" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="800" y="333" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Logistics</text>
  <text x="800" y="352" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#EAF4FF">Supply Network</text>

  <rect x="950" y="305" width="176" height="76" rx="14" fill="url(#managerGrad)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/headshots/production-lead.jpg" x="958" y="311" width="40" height="40" clip-path="url(#clipE)"/>
  <circle cx="978" cy="331" r="21" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="1008" y="333" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Production</text>
  <text x="1008" y="352" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#EAF4FF">Manufacturing</text>

  <!-- Team nodes -->
  <rect x="334" y="468" width="108" height="52" rx="12" fill="url(#deptGrad)" stroke="#BFD3EA" stroke-width="1.2"/>
  <text x="388" y="500" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#30506F">R&amp;D 1</text>
  <rect x="440" y="468" width="108" height="52" rx="12" fill="url(#deptGrad)" stroke="#BFD3EA" stroke-width="1.2"/>
  <text x="494" y="500" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#30506F">R&amp;D 2</text>

  <rect x="508" y="468" width="108" height="52" rx="12" fill="url(#deptGrad)" stroke="#BFD3EA" stroke-width="1.2"/>
  <text x="562" y="500" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#30506F">Sales 1</text>
  <rect x="568" y="540" width="108" height="52" rx="12" fill="#FFF4EA" stroke="#F4B183" stroke-width="1.2"/>
  <text x="622" y="572" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8A4B16">Sales 2</text>
  <rect x="628" y="468" width="108" height="52" rx="12" fill="url(#deptGrad)" stroke="#BFD3EA" stroke-width="1.2"/>
  <text x="682" y="500" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#30506F">Sales 3</text>

  <rect x="924" y="468" width="108" height="52" rx="12" fill="url(#deptGrad)" stroke="#BFD3EA" stroke-width="1.2"/>
  <text x="978" y="500" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#30506F">Plant 1</text>
  <rect x="984" y="540" width="108" height="52" rx="12" fill="#FFF4EA" stroke="#F4B183" stroke-width="1.2"/>
  <text x="1038" y="572" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8A4B16">Plant 2</text>
  <rect x="1044" y="468" width="108" height="52" rx="12" fill="url(#deptGrad)" stroke="#BFD3EA" stroke-width="1.2"/>
  <text x="1098" y="500" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#30506F">Plant 3</text>
</svg>
```

## Avoid in this skill
- ❌ PowerPoint SmartArt assumptions; build the hierarchy from individual editable SVG shapes instead.
- ❌ `marker-end` arrowheads on connector paths; use plain `<line>` segments for every elbow connector.
- ❌ Applying shadows or filters to `<line>` connectors; connector filters are dropped, so keep lines clean.
- ❌ Clipping node rectangles or groups; only clip `<image>` elements for headshots.
- ❌ Overcrowding all leaf nodes into one row when departments have many children; stagger or wrap children to preserve label readability.

## Composition notes
- Keep the root node centered in the upper third, with each hierarchy level separated by generous vertical whitespace.
- Use horizontal spacing based on each branch’s total leaf count, not merely the number of immediate children.
- Reserve the strongest color for the root, medium color for managers, and pale fills for teams so the hierarchy reads instantly.
- For executive decks, add headshots only to the top two levels; lower-level nodes should stay simpler to avoid visual noise.