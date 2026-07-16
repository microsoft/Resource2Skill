# SVG Recipe — Morph-Driven Architecture Data Flow

## Visual mechanism
A dense dark “blueprint” architecture stays perfectly static while one neon data packet moves between nodes across duplicate slides. PowerPoint Morph supplies the motion: each slide uses the same SVG layout and changes only the packet’s position, creating a guided data-flow narrative through a complex system.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background.
- 12–20× thin `<line>` elements for blueprint grid/circuit structure and node connectors.
- 5–7× rounded `<rect>` elements for architecture nodes, grouped consistently across all morph frames.
- 5–7× `<text>` labels for system components; every text element must include `width`.
- 4–8× `<path>` elements for custom icons, small arrow chevrons, route highlights, and decorative circuit traces.
- 1× `<circle>` for the neon data packet, moved slide-to-slide with stable identity/position.
- 1–2× secondary `<circle>` elements for packet core/glow layering.
- 1× `<filter id="softShadow">` applied to node cards.
- 1× `<filter id="packetGlow">` applied to the moving data packet.
- 2–4× `<linearGradient>` / `<radialGradient>` definitions for premium dark panels, node fills, and packet glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#120f26"/>
      <stop offset="55%" stop-color="#151a34"/>
      <stop offset="100%" stop-color="#070b18"/>
    </linearGradient>

    <linearGradient id="nodeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#303a62"/>
      <stop offset="100%" stop-color="#202743"/>
    </linearGradient>

    <linearGradient id="hotRoute" x1="70" y1="350" x2="1130" y2="350">
      <stop offset="0%" stop-color="#00e5ff"/>
      <stop offset="45%" stop-color="#ffd84d"/>
      <stop offset="100%" stop-color="#7cffc4"/>
    </linearGradient>

    <radialGradient id="packetRadial" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#fff06a"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="packetGlow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- blueprint grid -->
  <g opacity="0.22" stroke="#7b86b8" stroke-width="1">
    <line x1="80" y1="80" x2="1200" y2="80"/>
    <line x1="80" y1="160" x2="1200" y2="160"/>
    <line x1="80" y1="240" x2="1200" y2="240"/>
    <line x1="80" y1="320" x2="1200" y2="320"/>
    <line x1="80" y1="400" x2="1200" y2="400"/>
    <line x1="80" y1="480" x2="1200" y2="480"/>
    <line x1="80" y1="560" x2="1200" y2="560"/>
    <line x1="160" y1="40" x2="160" y2="660"/>
    <line x1="320" y1="40" x2="320" y2="660"/>
    <line x1="480" y1="40" x2="480" y2="660"/>
    <line x1="640" y1="40" x2="640" y2="660"/>
    <line x1="800" y1="40" x2="800" y2="660"/>
    <line x1="960" y1="40" x2="960" y2="660"/>
    <line x1="1120" y1="40" x2="1120" y2="660"/>
  </g>

  <text x="70" y="54" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#f2f5ff">
    Morph-driven architecture data flow
  </text>
  <text x="72" y="84" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9da9d8" letter-spacing="1.5">
    STATIC BLUEPRINT + ONE MOVING PACKET + MORPH TRANSITION
  </text>

  <!-- static connectors -->
  <g stroke="#6e789f" stroke-width="3" stroke-linecap="round" opacity="0.78">
    <line x1="240" y1="355" x2="500" y2="225"/>
    <line x1="560" y1="250" x2="560" y2="470"/>
    <line x1="620" y1="225" x2="850" y2="355"/>
    <line x1="950" y1="355" x2="1095" y2="355"/>
  </g>

  <!-- highlighted route for the current explanation step -->
  <path d="M 85 355 L 240 355 L 560 225 L 560 470 L 560 225 L 900 355 L 1130 355"
        fill="none" stroke="url(#hotRoute)" stroke-width="5" stroke-linecap="round"
        stroke-linejoin="round" stroke-dasharray="16 14" opacity="0.78"/>

  <!-- manual chevrons instead of marker-end -->
  <g fill="#ffd84d" opacity="0.9">
    <path d="M 424 279 L 448 270 L 436 293 Z"/>
    <path d="M 569 379 L 560 405 L 551 379 Z"/>
    <path d="M 758 273 L 783 286 L 760 300 Z"/>
    <path d="M 1038 343 L 1064 355 L 1038 367 Z"/>
  </g>

  <!-- node: client -->
  <g id="node-client">
    <rect x="140" y="300" width="200" height="110" rx="22" fill="url(#nodeGrad)" stroke="#8d97c8" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M 203 337 h74 a10 10 0 0 1 10 10 v32 h-94 v-32 a10 10 0 0 1 10-10 Z M 214 350 h52 M 214 364 h38"
          fill="none" stroke="#a9b7ff" stroke-width="4" stroke-linecap="round"/>
    <text x="170" y="392" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#eef2ff" text-anchor="middle">Client App</text>
  </g>

  <!-- node: api gateway -->
  <g id="node-api">
    <rect x="460" y="170" width="200" height="110" rx="22" fill="url(#nodeGrad)" stroke="#8d97c8" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M 520 218 h80 M 520 238 h80 M 540 198 v60 M 580 198 v60"
          fill="none" stroke="#7de7ff" stroke-width="4" stroke-linecap="round"/>
    <text x="490" y="262" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#eef2ff" text-anchor="middle">API Gateway</text>
  </g>

  <!-- node: auth -->
  <g id="node-auth">
    <rect x="460" y="430" width="200" height="110" rx="22" fill="#222b4c" stroke="#6775a8" stroke-width="1.5"/>
    <path d="M 560 462 c-22 0-40 14-40 32 c0 26 40 44 40 44 s40-18 40-44 c0-18-18-32-40-32 Z"
          fill="none" stroke="#bba7ff" stroke-width="4"/>
    <text x="490" y="522" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#eef2ff" text-anchor="middle">Auth Service</text>
  </g>

  <!-- node: backend -->
  <g id="node-backend">
    <rect x="800" y="300" width="200" height="110" rx="22" fill="url(#nodeGrad)" stroke="#8d97c8" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M 860 333 h82 v44 h-82 Z M 872 345 h20 M 872 361 h45 M 934 345 v32"
          fill="none" stroke="#7cffc4" stroke-width="4" stroke-linecap="round"/>
    <text x="830" y="392" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#eef2ff" text-anchor="middle">Backend Core</text>
  </g>

  <!-- node: database -->
  <g id="node-db">
    <rect x="1055" y="300" width="170" height="110" rx="22" fill="#222b4c" stroke="#6775a8" stroke-width="1.5"/>
    <path d="M 1097 334 c0-12 86-12 86 0 v42 c0 12-86 12-86 0 Z M 1097 334 c0 12 86 12 86 0 M 1097 355 c0 12 86 12 86 0"
          fill="none" stroke="#ffd84d" stroke-width="4"/>
    <text x="1080" y="392" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#eef2ff" text-anchor="middle">Data Store</text>
  </g>

  <!-- moving actor: duplicate this slide and change only translate(x y) for Morph frames -->
  <g id="morph-data-packet" transform="translate(560 225)">
    <circle cx="0" cy="0" r="30" fill="#ffd84d" opacity="0.28" filter="url(#packetGlow)"/>
    <circle cx="0" cy="0" r="17" fill="url(#packetRadial)" stroke="#fff7b0" stroke-width="3" filter="url(#packetGlow)"/>
    <circle cx="6" cy="-6" r="4" fill="#ffffff"/>
  </g>

  <text x="70" y="655" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#aeb8e6">
    Frame 03 / 07 — packet entering API Gateway. Keep all blueprint objects locked; move only the packet group per Morph slide.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; the motion must come from PowerPoint Morph, not embedded SVG animation.
- ❌ Changing node positions, connector geometry, colors, or labels between frames; Morph works best when the background is perfectly identical.
- ❌ `marker-end` on `<path>` connectors; use manual chevron `<path>` shapes or simple `<line>` arrows instead.
- ❌ Filters on `<line>` elements; apply glow/shadow only to circles, rects, paths, or text.
- ❌ Missing `width` on `<text>` elements; PowerPoint translation may clip or mis-size labels.

## Composition notes
- Keep 80–90% of the slide as the locked blueprint; the only moving object should be the bright packet group.
- Place nodes on a clear left-to-right or looped journey so Morph reads as cause-and-effect, not random motion.
- Use a dark, low-contrast architecture layer and one saturated neon actor color to create instant focus.
- For the full effect, generate 6–10 duplicate slides with this same SVG structure and change only `transform="translate(x y)"` on `id="morph-data-packet"`, then apply a 0.4–0.6s Morph transition with automatic advance.