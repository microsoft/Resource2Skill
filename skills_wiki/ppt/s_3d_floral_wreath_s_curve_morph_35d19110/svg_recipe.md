# SVG Recipe — 3D Floral Wreath S-Curve Morph

## Visual mechanism
A chain of plump, gradient-filled leaf shapes overlaps along two opposing arcs to form an elegant “S” curve, with each leaf casting a soft shadow onto the next for a layered 3D floral-wreath effect. The middle of the S is intentionally interrupted by a title capsule, turning the negative space into the slide’s focal frame.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 24× `<path>` for the repeated leaf/petal shapes following the S-curve
- 1× `<linearGradient id="leafGradient">` for the dark-to-bright green leaf fill
- 1× `<radialGradient id="backgroundGlow">` for a subtle premium stage glow
- 1× `<filter id="leafShadow">` applied to every leaf path for stacked 3D depth
- 1× `<filter id="cardShadow">` applied to the central title capsule
- 1× `<rect>` for the central white title capsule
- 4× `<line>` for clean horizontal connector rules
- 8× `<text>` blocks with explicit `width` attributes for title, option labels, and supporting copy
- 2× small `<circle>` accents for option callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="backgroundGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#F7FAF4"/>
      <stop offset="100%" stop-color="#EEF4EA"/>
    </radialGradient>

    <linearGradient id="leafGradient" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#063808"/>
      <stop offset="48%" stop-color="#087E15"/>
      <stop offset="100%" stop-color="#00A51A"/>
    </linearGradient>

    <filter id="leafShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="8" dy="9" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="7" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0.08
                0 0 0 0 0.02
                0 0 0 0.42 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-20%" y="-35%" width="140%" height="170%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0.12
                0 0 0 0 0.03
                0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#backgroundGlow)"/>

  <text x="86" y="132" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2.5" fill="#6A7B63">OPTION 01</text>
  <text x="86" y="178" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#16351C">Current Model</text>
  <text x="88" y="218" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#5C6B58">Map the existing process, expose friction, and identify where growth stalls.</text>
  <circle cx="96" cy="270" r="7" fill="#009A16"/>
  <text x="116" y="276" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#2B4C2B">Baseline performance</text>
  <line x1="374" y1="248" x2="478" y2="248" stroke="#B7C8B1" stroke-width="2"/>
  <line x1="430" y1="248" x2="478" y2="236" stroke="#D5E2D1" stroke-width="2"/>

  <text x="896" y="456" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2.5" fill="#6A7B63">OPTION 02</text>
  <text x="896" y="502" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#16351C">Future System</text>
  <text x="898" y="542" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#5C6B58">Reframe the path forward with compounding improvements and visible momentum.</text>
  <circle cx="906" cy="594" r="7" fill="#009A16"/>
  <text x="926" y="600" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#2B4C2B">Accelerated adoption</text>
  <line x1="802" y1="470" x2="906" y2="470" stroke="#B7C8B1" stroke-width="2"/>
  <line x1="802" y1="482" x2="856" y2="470" stroke="#D5E2D1" stroke-width="2"/>

  <g>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(790 150) rotate(-140)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(760 122) rotate(-155)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(720 101) rotate(-170)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(675 92) rotate(180)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(630 96) rotate(165)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(585 114) rotate(145)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(545 145) rotate(125)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(512 187) rotate(102)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(492 236) rotate(78)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(492 288) rotate(54)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(515 337) rotate(30)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(558 372) rotate(10)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>

    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(722 348) rotate(-170)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(770 376) rotate(-145)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(800 422) rotate(-116)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(812 475) rotate(-92)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(797 528) rotate(-66)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(760 574) rotate(-42)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(710 608) rotate(-18)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(650 620) rotate(0)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(590 610) rotate(22)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(538 580) rotate(48)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(505 535) rotate(76)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
    <path d="M -74 0 C -45 -44 45 -44 74 0 C 45 44 -45 44 -74 0 Z" transform="translate(500 480) rotate(104)" fill="url(#leafGradient)" stroke="#0A5E12" stroke-width="1" filter="url(#leafShadow)"/>
  </g>

  <rect x="532" y="314" width="216" height="96" rx="48" fill="#FFFFFF" stroke="#E3EBDD" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="570" y="354" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" text-anchor="middle" fill="#6A7B63">STRATEGIC</text>
  <text x="640" y="389" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" text-anchor="middle" fill="#0D3513">S-CURVE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to repeat the leaf; duplicate the editable `<path>` leaf shapes directly.
- ❌ Do not rasterize the wreath into one `<image>` if editability is required; the premium effect comes from editable layered paths and native shadows.
- ❌ Do not apply `clip-path` or `mask` to the leaf paths; clipping on non-image shapes will not translate reliably.
- ❌ Do not rely on `marker-end` for arrows around the wreath; use plain connector `<line>` elements or custom triangular paths if arrowheads are needed.
- ❌ Do not use skew or matrix transforms to bend leaves; rotate and translate each path along the S-curve instead.

## Composition notes
- Keep the wreath in the central 45–55% of the canvas, with the top lobe slightly above center and the lower lobe dipping toward the bottom-right.
- Leave generous left and right negative space for two option narratives; the S-curve should visually guide from Option 01 to Option 02.
- Use a central white pill or compact title card to cover the intentional break between arcs and make the gap feel designed, not accidental.
- Maintain a tight green palette: dark leaf bases, bright green tips, muted sage connector lines, and off-white background for executive polish.