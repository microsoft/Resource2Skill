# SVG Recipe — Interactive Accordion Drawers (Morph-Driven Pull-out Panels)

## Visual mechanism
Stack a set of colorful “drawer” cards on the left edge of the slide, with only their rounded tabs visible when collapsed and one panel pulled out horizontally to reveal content. In PowerPoint, duplicate the same SVG-derived shapes across slides, change only their x-positions, and apply Morph so the selected drawer glides open like a physical file drawer.

## SVG primitives needed
- 1× `<rect>` for the warm neutral slide background.
- 2× decorative `<path>` blobs for premium depth behind the interface.
- 6× large `<rect>` for drawer bodies and rounded tabs across three drawers.
- 6× `<rect>` for small content chips, status pills, and callout cards inside the open drawer.
- 6× `<circle>` for step dots, bullet accents, and small UI indicators.
- 5× `<path>` for chevrons, handle glyphs, and decorative drawer seams.
- Multiple `<text>` elements with explicit `width` for title, tab numbers, drawer labels, body copy, and interaction hints.
- 3× `<linearGradient>` for pastel drawer fills.
- 1× `<radialGradient>` for the soft background glow.
- 1× `<filter id="drawerShadow">` using `feOffset + feGaussianBlur + feMerge` applied directly to drawer rectangles.
- 1× `<filter id="softGlow">` using `feGaussianBlur` applied to decorative background paths.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cyanDrawer" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7FE2E8"/>
      <stop offset="100%" stop-color="#49AEB8"/>
    </linearGradient>
    <linearGradient id="peachDrawer" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFD1A7"/>
      <stop offset="100%" stop-color="#F08E55"/>
    </linearGradient>
    <linearGradient id="mintDrawer" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#BEECC8"/>
      <stop offset="100%" stop-color="#72B985"/>
    </linearGradient>
    <radialGradient id="bgGlow" cx="45%" cy="35%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#F5F3EA" stop-opacity="0"/>
    </radialGradient>
    <filter id="drawerShadow" x="-20%" y="-30%" width="150%" height="170%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .20 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F3EA"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <path d="M930,78 C1058,38 1176,92 1210,190 C1244,288 1168,358 1036,352 C904,346 810,272 824,180 C833,122 872,96 930,78 Z" fill="#FFFFFF" opacity="0.62" filter="url(#softGlow)"/>
  <path d="M80,560 C180,510 278,544 322,626 C238,688 132,704 42,660 C22,622 38,584 80,560 Z" fill="#E9E3D8" opacity="0.55" filter="url(#softGlow)"/>

  <text x="80" y="70" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#2E3135">Interactive Accordion Drawers</text>
  <text x="82" y="106" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6B6F73">Duplicate this slide, shift one drawer body to the right, then apply PowerPoint Morph for a pull-out interaction.</text>

  <g id="drawer-01-collapsed" transform="translate(58 158)">
    <rect x="-650" y="0" width="790" height="126" rx="30" fill="url(#cyanDrawer)" filter="url(#drawerShadow)"/>
    <rect x="0" y="0" width="146" height="126" rx="30" fill="url(#cyanDrawer)" filter="url(#drawerShadow)"/>
    <path d="M112 42 L126 63 L112 84" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>
    <text x="30" y="53" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">01</text>
    <text x="31" y="82" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#EFFFFF">SOURCE</text>
    <text x="-596" y="46" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Data Aggregation</text>
  </g>

  <g id="drawer-02-open" transform="translate(58 294)">
    <rect x="112" y="0" width="842" height="154" rx="34" fill="url(#peachDrawer)" filter="url(#drawerShadow)"/>
    <rect x="0" y="0" width="146" height="154" rx="34" fill="url(#peachDrawer)" filter="url(#drawerShadow)"/>
    <path d="M104 48 L123 77 L104 106" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="28" y="65" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#FFFFFF">02</text>
    <text x="30" y="98" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFF8F1">PATTERN</text>

    <text x="182" y="50" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#FFFFFF">Pattern Extraction</text>
    <text x="184" y="82" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFF8F1">Analyze composition, color rhythm, iconography, and typographic hierarchy before generating the final deck system.</text>

    <rect x="692" y="32" width="208" height="88" rx="22" fill="#FFFFFF" opacity="0.26"/>
    <circle cx="724" cy="62" r="9" fill="#FFFFFF"/>
    <circle cx="724" cy="91" r="9" fill="#FFFFFF" opacity="0.7"/>
    <text x="744" y="68" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Color logic</text>
    <text x="744" y="97" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Layout rules</text>

    <rect x="184" y="112" width="118" height="26" rx="13" fill="#FFFFFF" opacity="0.28"/>
    <rect x="316" y="112" width="140" height="26" rx="13" fill="#FFFFFF" opacity="0.22"/>
    <rect x="470" y="112" width="120" height="26" rx="13" fill="#FFFFFF" opacity="0.18"/>
    <text x="204" y="131" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Morph ready</text>
    <text x="338" y="131" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Editable SVG</text>
    <text x="493" y="131" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">By object</text>
  </g>

  <g id="drawer-03-collapsed" transform="translate(58 466)">
    <rect x="-650" y="0" width="790" height="126" rx="30" fill="url(#mintDrawer)" filter="url(#drawerShadow)"/>
    <rect x="0" y="0" width="146" height="126" rx="30" fill="url(#mintDrawer)" filter="url(#drawerShadow)"/>
    <path d="M112 42 L126 63 L112 84" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>
    <text x="30" y="53" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">03</text>
    <text x="31" y="82" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#F1FFF5">OUTPUT</text>
    <text x="-596" y="46" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Code Generation</text>
  </g>

  <rect x="1012" y="176" width="190" height="330" rx="28" fill="#FFFFFF" opacity="0.72" filter="url(#drawerShadow)"/>
  <text x="1042" y="224" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#31343A">Morph setup</text>
  <circle cx="1051" cy="266" r="6" fill="#49AEB8"/>
  <text x="1070" y="272" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5F646A">Same IDs</text>
  <circle cx="1051" cy="306" r="6" fill="#F08E55"/>
  <text x="1070" y="312" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5F646A">Shift x only</text>
  <circle cx="1051" cy="346" r="6" fill="#72B985"/>
  <text x="1070" y="352" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5F646A">Morph by object</text>
  <path d="M1043 402 C1082 382 1120 382 1159 402" fill="none" stroke="#D8D1C5" stroke-width="4" stroke-linecap="round"/>
  <text x="1042" y="444" width="128" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A7E83">Use one slide per open state for non-linear presenter navigation.</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; PowerPoint Morph should create the movement, not SVG animation.
- ❌ Changing element order, deleting drawers, or renaming IDs between states; Morph needs stable matching objects.
- ❌ Applying `filter` to `<line>` elements; use paths or rectangles for decorative strokes if shadows are needed.
- ❌ Using `clip-path` on drawer rectangles to fake reveal states; instead move the body off-canvas or alter x-positions across slides.
- ❌ `marker-end` on `<path>` for arrows; if directional arrows are needed, draw the arrowhead as a small editable `<path>`.

## Composition notes
- Keep the drawer stack on the left two-thirds of the slide, with tabs always visible near the left edge; reserve the right side for a small instruction card or presenter cue.
- Use one active drawer at full width and keep inactive drawers collapsed or mostly off-canvas to preserve focus.
- Maintain identical y-positions across Morph slides; only change x-positions for the selected drawer body/tab group to create a clean horizontal pull.
- Use saturated pastel fills with soft shadows on a warm neutral background so the interface feels tactile rather than dashboard-like.