# SVG Recipe — Hub-and-Spoke Infrastructure Architecture Visualization

## Visual mechanism
A central office “hub” is drawn as a clustered set of Cisco-style infrastructure icons, with branch locations radiating outward as spokes via crisp dark connector lines. The diagram relies on recognizable symbolic geometry—blue routers, cyan buildings, charcoal server racks, and a yellow internet cloud—to make infrastructure relationships instantly legible.

## SVG primitives needed
- 1× `<rect>` full-slide background plus subtle panel/card rectangles for the clean architecture canvas
- 10–20× `<line>` for hub-and-spoke network links, branch access lines, and small icon details
- 20–40× `<rect>` for buildings, windows, server racks, ports, vents, and device faces
- 8–12× `<ellipse>` for router cylinders, cloud lobes, and device top/bottom faces
- 12–18× `<path>` for Cisco-style cloud outline, isometric device sides, arrows, server symbols, and decorative icon glyphs
- 8–12× `<circle>` for LEDs, status points, and hub emphasis dots
- 1× `<filter id="softShadow">` applied to major icon bodies and node cards
- 4× `<linearGradient>` fills for premium blue hardware, cyan buildings, yellow cloud, and dark rack depth
- Multiple `<text>` elements with explicit `width` attributes for title, node labels, link labels, and zone callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="100%" stop-color="#EAF2F8"/>
    </linearGradient>
    <linearGradient id="routerBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#37B8E8"/>
      <stop offset="100%" stop-color="#008FC9"/>
    </linearGradient>
    <linearGradient id="buildingCyan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B8EAFF"/>
      <stop offset="100%" stop-color="#62BDE8"/>
    </linearGradient>
    <linearGradient id="rackDark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#555B62"/>
      <stop offset="100%" stop-color="#22272D"/>
    </linearGradient>
    <linearGradient id="cloudGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE173"/>
      <stop offset="100%" stop-color="#FFC400"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <rect x="58" y="54" width="1164" height="606" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="58" y="54" width="1164" height="88" rx="28" fill="#F4FAFE"/>
  <line x1="88" y1="142" x2="1192" y2="142" stroke="#CFE1EC" stroke-width="2"/>

  <text x="96" y="104" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#075E78">
    Hub-and-Spoke Infrastructure Architecture
  </text>
  <text x="930" y="104" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6B75" text-anchor="end">
    WAN / Internet / Data Center topology
  </text>

  <!-- topology links -->
  <line x1="640" y1="292" x2="304" y2="492" stroke="#253746" stroke-width="5" stroke-linecap="round"/>
  <line x1="640" y1="292" x2="640" y2="506" stroke="#253746" stroke-width="5" stroke-linecap="round"/>
  <line x1="640" y1="292" x2="972" y2="492" stroke="#253746" stroke-width="5" stroke-linecap="round"/>
  <line x1="640" y1="292" x2="310" y2="218" stroke="#253746" stroke-width="4" stroke-linecap="round" stroke-dasharray="12 10"/>
  <line x1="702" y1="250" x2="930" y2="242" stroke="#253746" stroke-width="5" stroke-linecap="round"/>
  <line x1="702" y1="250" x2="930" y2="318" stroke="#253746" stroke-width="4" stroke-linecap="round"/>

  <text x="418" y="370" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#324957" text-anchor="middle">
    MPLS link
  </text>
  <text x="724" y="430" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#324957" text-anchor="middle">
    SD-WAN tunnel
  </text>
  <text x="420" y="242" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#324957" text-anchor="middle">
    Internet breakout
  </text>

  <!-- internet cloud -->
  <g transform="translate(170 164)">
    <path d="M42 72 C18 72 6 55 16 38 C24 24 38 21 50 27 C59 8 83 2 101 15 C113 2 138 9 145 29 C167 28 181 43 177 62 C173 82 154 87 136 84 L45 84 C44 84 43 84 42 84 Z"
          fill="url(#cloudGold)" stroke="#CF9F00" stroke-width="3" filter="url(#softShadow)"/>
    <text x="28" y="64" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#6A5100" text-anchor="middle">
      Internet
    </text>
  </g>

  <!-- central office node card -->
  <rect x="494" y="166" width="292" height="190" rx="22" fill="#F8FCFF" stroke="#BFD8E8" stroke-width="2" filter="url(#softShadow)"/>
  <text x="540" y="334" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#143B52" text-anchor="middle">
    Central Office
  </text>

  <!-- central building -->
  <g transform="translate(520 180)">
    <rect x="18" y="14" width="82" height="112" fill="url(#buildingCyan)" stroke="#3A9FCB" stroke-width="3"/>
    <path d="M100 14 L126 30 L126 142 L100 126 Z" fill="#4AAAD2" stroke="#2E89AE" stroke-width="3"/>
    <path d="M18 126 L100 126 L126 142 L44 142 Z" fill="#85D7F5" stroke="#3A9FCB" stroke-width="3"/>
    <rect x="34" y="30" width="14" height="16" fill="#FFFFFF" opacity="0.9"/>
    <rect x="62" y="30" width="14" height="16" fill="#FFFFFF" opacity="0.9"/>
    <rect x="34" y="60" width="14" height="16" fill="#FFFFFF" opacity="0.9"/>
    <rect x="62" y="60" width="14" height="16" fill="#FFFFFF" opacity="0.9"/>
    <rect x="34" y="90" width="14" height="16" fill="#FFFFFF" opacity="0.9"/>
    <rect x="62" y="90" width="14" height="16" fill="#FFFFFF" opacity="0.9"/>
  </g>

  <!-- central router -->
  <g transform="translate(620 200)">
    <ellipse cx="62" cy="84" rx="62" ry="22" fill="#0079AD"/>
    <rect x="0" y="36" width="124" height="48" fill="url(#routerBlue)"/>
    <ellipse cx="62" cy="36" rx="62" ry="22" fill="#54C9F2" stroke="#0079AD" stroke-width="3"/>
    <path d="M62 21 L72 32 L65 32 L65 50 L59 50 L59 32 L52 32 Z" fill="#FFFFFF"/>
    <path d="M62 51 L72 40 L65 40 L65 26 L59 26 L59 40 L52 40 Z" fill="#FFFFFF"/>
    <path d="M40 36 L51 28 L51 34 L73 34 L73 38 L51 38 L51 44 Z" fill="#FFFFFF"/>
    <path d="M84 36 L73 28 L73 34 L51 34 L51 38 L73 38 L73 44 Z" fill="#FFFFFF"/>
  </g>

  <!-- data center racks -->
  <g transform="translate(936 184)">
    <rect x="0" y="0" width="178" height="154" rx="12" fill="#F6FAFC" stroke="#BCD5E4" stroke-width="2" filter="url(#softShadow)"/>
    <text x="88" y="136" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#143B52" text-anchor="middle">
      Data Center
    </text>
    <rect x="30" y="22" width="118" height="22" fill="url(#rackDark)" stroke="#161A1E" stroke-width="2"/>
    <rect x="30" y="50" width="118" height="22" fill="url(#rackDark)" stroke="#161A1E" stroke-width="2"/>
    <rect x="30" y="78" width="118" height="22" fill="url(#rackDark)" stroke="#161A1E" stroke-width="2"/>
    <line x1="48" y1="30" x2="86" y2="30" stroke="#111" stroke-width="3"/>
    <line x1="48" y1="58" x2="86" y2="58" stroke="#111" stroke-width="3"/>
    <line x1="48" y1="86" x2="86" y2="86" stroke="#111" stroke-width="3"/>
    <circle cx="125" cy="33" r="5" fill="#2BFF57"/>
    <circle cx="125" cy="61" r="5" fill="#2BFF57"/>
    <circle cx="125" cy="89" r="5" fill="#2BFF57"/>
  </g>

  <!-- reusable-looking but manually drawn branch nodes -->
  <g transform="translate(176 462)">
    <rect x="0" y="0" width="256" height="124" rx="20" fill="#FFFFFF" stroke="#C8DCE8" stroke-width="2" filter="url(#softShadow)"/>
    <rect x="32" y="24" width="58" height="66" fill="url(#buildingCyan)" stroke="#3A9FCB" stroke-width="3"/>
    <rect x="45" y="38" width="10" height="12" fill="#FFFFFF"/>
    <rect x="68" y="38" width="10" height="12" fill="#FFFFFF"/>
    <rect x="45" y="62" width="10" height="12" fill="#FFFFFF"/>
    <rect x="68" y="62" width="10" height="12" fill="#FFFFFF"/>
    <ellipse cx="142" cy="76" rx="46" ry="16" fill="#0079AD"/>
    <rect x="96" y="44" width="92" height="32" fill="url(#routerBlue)"/>
    <ellipse cx="142" cy="44" rx="46" ry="16" fill="#54C9F2" stroke="#0079AD" stroke-width="2"/>
    <path d="M142 34 L150 42 L145 42 L145 54 L139 54 L139 42 L134 42 Z" fill="#FFFFFF"/>
    <text x="128" y="108" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#143B52" text-anchor="middle">
      Branch Office 1
    </text>
  </g>

  <g transform="translate(512 510)">
    <rect x="0" y="0" width="256" height="124" rx="20" fill="#FFFFFF" stroke="#C8DCE8" stroke-width="2" filter="url(#softShadow)"/>
    <rect x="32" y="24" width="58" height="66" fill="url(#buildingCyan)" stroke="#3A9FCB" stroke-width="3"/>
    <rect x="45" y="38" width="10" height="12" fill="#FFFFFF"/>
    <rect x="68" y="38" width="10" height="12" fill="#FFFFFF"/>
    <rect x="45" y="62" width="10" height="12" fill="#FFFFFF"/>
    <rect x="68" y="62" width="10" height="12" fill="#FFFFFF"/>
    <ellipse cx="142" cy="76" rx="46" ry="16" fill="#0079AD"/>
    <rect x="96" y="44" width="92" height="32" fill="url(#routerBlue)"/>
    <ellipse cx="142" cy="44" rx="46" ry="16" fill="#54C9F2" stroke="#0079AD" stroke-width="2"/>
    <path d="M120 44 L132 36 L132 42 L164 42 L164 46 L132 46 L132 52 Z" fill="#FFFFFF"/>
    <text x="128" y="108" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#143B52" text-anchor="middle">
      Branch Office 2
    </text>
  </g>

  <g transform="translate(848 462)">
    <rect x="0" y="0" width="256" height="124" rx="20" fill="#FFFFFF" stroke="#C8DCE8" stroke-width="2" filter="url(#softShadow)"/>
    <rect x="32" y="24" width="58" height="66" fill="url(#buildingCyan)" stroke="#3A9FCB" stroke-width="3"/>
    <rect x="45" y="38" width="10" height="12" fill="#FFFFFF"/>
    <rect x="68" y="38" width="10" height="12" fill="#FFFFFF"/>
    <rect x="45" y="62" width="10" height="12" fill="#FFFFFF"/>
    <rect x="68" y="62" width="10" height="12" fill="#FFFFFF"/>
    <ellipse cx="142" cy="76" rx="46" ry="16" fill="#0079AD"/>
    <rect x="96" y="44" width="92" height="32" fill="url(#routerBlue)"/>
    <ellipse cx="142" cy="44" rx="46" ry="16" fill="#54C9F2" stroke="#0079AD" stroke-width="2"/>
    <path d="M142 34 L150 42 L145 42 L145 54 L139 54 L139 42 L134 42 Z" fill="#FFFFFF"/>
    <path d="M122 44 L134 36 L134 42 L162 42 L162 46 L134 46 L134 52 Z" fill="#FFFFFF"/>
    <text x="128" y="108" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#143B52" text-anchor="middle">
      Regional Office
    </text>
  </g>

  <circle cx="640" cy="292" r="8" fill="#FF5D2E" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="304" cy="492" r="6" fill="#FF5D2E" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="640" cy="506" r="6" fill="#FF5D2E" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="972" cy="492" r="6" fill="#FF5D2E" stroke="#FFFFFF" stroke-width="2"/>

  <text x="94" y="632" width="1090" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7B86">
    Visual convention: cyan buildings indicate physical sites, blue cylinders indicate routers / WAN gateways, charcoal racks indicate server infrastructure, and yellow cloud indicates public internet dependency.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<use>` or `<symbol>` to repeat router/building icons; manually duplicate the editable SVG geometry instead.
- ❌ Applying `marker-end` to `<path>` connectors; if arrowheads are required, use `<line marker-end="...">` directly or draw arrowheads as small editable `<path>` triangles.
- ❌ Rendering the entire topology as one screenshot image; keep buildings, routers, labels, and links as separate editable SVG primitives.
- ❌ Putting shadows or glows on connector `<line>` elements; filters on lines are dropped, so reserve shadows for node cards and icon bodies.
- ❌ Overly decorative curved links that obscure topology; architecture audiences need clear hub-to-branch relationship lines.

## Composition notes
- Place the central office slightly above the slide midpoint, with branch cards forming a wide lower triangle; this makes the hub-and-spoke topology readable at a glance.
- Keep connectors behind node cards/icons and use a dark slate stroke so links remain visible against the pale executive-style canvas.
- Use a limited, symbolic color palette: blue for network hardware, cyan for physical sites, charcoal for servers, yellow for internet/cloud.
- Reserve the top band for title and context; keep the main topology in the central 70% of the canvas with generous negative space around each node.