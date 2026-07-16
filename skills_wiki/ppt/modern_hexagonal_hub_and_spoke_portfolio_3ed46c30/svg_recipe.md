# SVG Recipe — Modern Hexagonal Hub-and-Spoke Portfolio

## Visual mechanism
A central solid hexagonal hub anchors six satellite hexagons arranged on a precise radial orbit, with connector lines implying portfolio relationships. A faint honeycomb field, soft shadows, and mirrored detail-text alignment make the chart feel engineered, balanced, and executive-ready.

## SVG primitives needed
- 1× `<rect>` for the cool-gray slide background with a subtle radial glow
- 30× `<path>` for faint honeycomb background hex outlines
- 7× `<path>` for the main editable hexagons: 1 filled central hub and 6 bordered satellite nodes
- 6× `<line>` for hub-to-node spokes behind the hexagons
- 14× `<text>` for title, hub label, node labels, and outside detail annotations; every text element needs explicit `width`
- 1× `<linearGradient>` for the premium central hub fill
- 1× `<radialGradient>` for the background illumination
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge`, applied only to hexagon paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="64%" stop-color="#fcfcfe"/>
      <stop offset="100%" stop-color="#f3f4f8"/>
    </radialGradient>

    <linearGradient id="hubRed" x1="560" y1="292" x2="720" y2="458" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ff4b72"/>
      <stop offset="58%" stop-color="#db143c"/>
      <stop offset="100%" stop-color="#a90f2e"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset input="SourceAlpha" dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <g opacity="0.44" fill="none" stroke="#e6e7ee" stroke-width="2">
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(45 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(141 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(237 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(333 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(429 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(525 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(621 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(717 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(813 84)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(909 84)"/>

    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(93 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(189 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(285 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(381 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(477 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(573 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(669 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(765 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(861 188)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(957 188)"/>

    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(45 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(141 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(237 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(333 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(429 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(525 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(621 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(717 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(813 500)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(909 500)"/>
  </g>

  <text x="52" y="54" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#28282d">
    Corporate Ecosystem & Portfolio
  </text>
  <text x="54" y="84" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8b8f99">
    Hexagonal hub-and-spoke map showing portfolio brands connected to the core enterprise.
  </text>

  <g stroke="#c9ccd4" stroke-width="3" opacity="0.86">
    <line x1="640" y1="375" x2="640" y2="155"/>
    <line x1="640" y1="375" x2="839" y2="260"/>
    <line x1="640" y1="375" x2="839" y2="490"/>
    <line x1="640" y1="375" x2="640" y2="605"/>
    <line x1="640" y1="375" x2="441" y2="490"/>
    <line x1="640" y1="375" x2="441" y2="260"/>
  </g>

  <path d="M71 -41 L0 -82 L-71 -41 L-71 41 L0 82 L71 41 Z" transform="translate(640 375)" fill="url(#hubRed)" filter="url(#softShadow)"/>
  <text x="640" y="360" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#ffffff">
    <tspan x="640">CORE</tspan><tspan x="640" dy="30">HOLDING</tspan>
  </text>

  <g fill="#ffffff" stroke="#db143c" stroke-width="5" filter="url(#softShadow)">
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(640 155)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(839 260)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(839 490)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(640 605)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(441 490)"/>
    <path d="M52 -30 L0 -60 L-52 -30 L-52 30 L0 60 L52 30 Z" transform="translate(441 260)"/>
  </g>

  <text x="640" y="162" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#4a4a50">KNORR</text>
  <text x="839" y="267" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#4a4a50">LUX</text>
  <text x="839" y="497" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#4a4a50">LIPTON</text>
  <text x="640" y="612" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#4a4a50">SUNSILK</text>
  <text x="441" y="497" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#4a4a50">DOVE</text>
  <text x="441" y="267" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#4a4a50">REXONA</text>

  <text x="640" y="91" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8a8d96">
    <tspan x="640" font-weight="700" fill="#505057">Nutrition Scale</tspan><tspan x="640" dy="21">Food systems · Germany · 1838</tspan>
  </text>
  <text x="919" y="248" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8a8d96">
    <tspan x="919" font-weight="700" fill="#505057">Beauty Care</tspan><tspan x="919" dy="21">Soap & skincare · UK · 1925</tspan>
  </text>
  <text x="919" y="478" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8a8d96">
    <tspan x="919" font-weight="700" fill="#505057">Beverages</tspan><tspan x="919" dy="21">Tea platform · UK · 1890</tspan>
  </text>
  <text x="640" y="682" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8a8d96">
    <tspan x="640" font-weight="700" fill="#505057">Personal Care</tspan><tspan x="640" dy="21">Hair care · Global · 1954</tspan>
  </text>
  <text x="361" y="478" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8a8d96">
    <tspan x="361" font-weight="700" fill="#505057">Skin Health</tspan><tspan x="361" dy="21">Care rituals · US · 1957</tspan>
  </text>
  <text x="361" y="248" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8a8d96">
    <tspan x="361" font-weight="700" fill="#505057">Deodorants</tspan><tspan x="361" dy="21">Hygiene platform · AU · 1908</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the honeycomb background; draw faint editable hex paths instead
- ❌ `<use href="#hex">` to duplicate hexagons; it can hard-fail translation, so repeat explicit `<path>` elements
- ❌ `filter` on connector `<line>` elements; apply shadows only to hexagon paths
- ❌ `marker-end` arrowheads on spokes; this visual should use clean relationship lines, not arrows
- ❌ Clip paths or masks on non-image elements; the hexagons should be native editable paths

## Composition notes
- Keep the hub slightly below true vertical center if a title is present; this preserves breathing room at the top.
- Use mirrored detail alignment: right-side nodes get left-aligned text; left-side nodes get right-aligned text; top and bottom nodes use centered text.
- Make connector lines low-contrast and place them behind the hexagons so the nodes appear to float above the network.
- Let the background honeycomb be visible but quiet: pale gray strokes at low opacity support the theme without competing with the data.