# SVG Recipe — Automated Cloud Architecture Visualization (Hierarchical Node-Link Diagram)

## Visual mechanism
A cloud system is clarified through nested, lightly tinted boundary boxes: a large virtual network contains subnet tiers, and each tier contains uniform service nodes. Directional arrows run left-to-right to show traffic flow, while small service badges and labels make the architecture scannable without flattening it into a generic flowchart.

## SVG primitives needed
- 1× `<rect>` full-slide background with a subtle gradient
- 1× `<rect>` for the main cloud/VNet boundary with dashed stroke
- 4× `<rect>` for subnet/tier boundaries with pastel fills and dashed strokes
- 8× `<rect>` for service node cards with rounded corners and soft shadows
- 8× `<circle>` / `<ellipse>` for icon backplates, status dots, and database cylinders
- 10× `<path>` for editable cloud/service glyphs inside the node cards
- 8× `<line>` for directed connectors, each with its own `marker-end`
- 1× `<marker>` arrowhead definition used only on `<line>` elements
- 1× `<filter id="cardShadow">` applied to node cards and the main boundary
- 1× `<filter id="softGlow">` applied to the highlighted ingress node
- 3× `<linearGradient>` for premium background, boundary, and node accents
- Multiple `<text>` elements with explicit `width` attributes for title, tier labels, node names, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="55%" stop-color="#EEF6FF"/>
      <stop offset="100%" stop-color="#F9FAFB"/>
    </linearGradient>
    <linearGradient id="vnetFill" x1="0" y1="82" x2="0" y2="650">
      <stop offset="0%" stop-color="#EAF5FF"/>
      <stop offset="100%" stop-color="#F8FCFF"/>
    </linearGradient>
    <linearGradient id="accentBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00A6FF"/>
      <stop offset="100%" stop-color="#0067B8"/>
    </linearGradient>
    <linearGradient id="accentGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38D996"/>
      <stop offset="100%" stop-color="#008A5B"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <marker id="arrowBlue" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#2563EB"/>
    </marker>
    <marker id="arrowGray" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#64748B"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <text x="56" y="52" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" fill="#172033">Contoso Cloud Architecture</text>
  <text x="58" y="82" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Hierarchical node-link view: internet ingress, application tiers, private data plane, and operations services</text>

  <rect x="238" y="118" width="964" height="536" rx="30" fill="url(#vnetFill)" stroke="#2B7BBB" stroke-width="2" stroke-dasharray="10 7" filter="url(#cardShadow)"/>
  <text x="268" y="151" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1D5F99">Virtual Network: contoso-prod-vnet / 10.24.0.0/16</text>

  <rect x="270" y="184" width="205" height="392" rx="22" fill="#F1F8FF" stroke="#4A90C2" stroke-width="1.5" stroke-dasharray="7 6"/>
  <rect x="500" y="184" width="230" height="392" rx="22" fill="#F4F8FF" stroke="#5E81D1" stroke-width="1.5" stroke-dasharray="7 6"/>
  <rect x="755" y="184" width="220" height="392" rx="22" fill="#F3FBF7" stroke="#31A66A" stroke-width="1.5" stroke-dasharray="7 6"/>
  <rect x="1000" y="184" width="170" height="392" rx="22" fill="#FFF8EE" stroke="#D97706" stroke-width="1.5" stroke-dasharray="7 6"/>

  <text x="294" y="214" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2563EB">Ingress subnet</text>
  <text x="526" y="214" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#4F46E5">Application subnet</text>
  <text x="780" y="214" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#059669">Data subnet</text>
  <text x="1022" y="214" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B45309">Ops subnet</text>

  <line x1="156" y1="362" x2="286" y2="362" stroke="#2563EB" stroke-width="3" marker-end="url(#arrowBlue)"/>
  <line x1="415" y1="362" x2="526" y2="300" stroke="#2563EB" stroke-width="3" marker-end="url(#arrowBlue)"/>
  <line x1="415" y1="362" x2="526" y2="424" stroke="#2563EB" stroke-width="3" marker-end="url(#arrowBlue)"/>
  <line x1="655" y1="300" x2="782" y2="300" stroke="#2563EB" stroke-width="3" marker-end="url(#arrowBlue)"/>
  <line x1="655" y1="424" x2="782" y2="424" stroke="#2563EB" stroke-width="3" marker-end="url(#arrowBlue)"/>
  <line x1="900" y1="300" x2="1040" y2="300" stroke="#64748B" stroke-width="2.5" stroke-dasharray="8 7" marker-end="url(#arrowGray)"/>
  <line x1="900" y1="424" x2="1040" y2="424" stroke="#64748B" stroke-width="2.5" stroke-dasharray="8 7" marker-end="url(#arrowGray)"/>
  <line x1="585" y1="488" x2="1040" y2="488" stroke="#64748B" stroke-width="2.5" stroke-dasharray="8 7" marker-end="url(#arrowGray)"/>

  <rect x="52" y="300" width="106" height="124" rx="22" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#cardShadow)"/>
  <circle cx="105" cy="346" r="27" fill="#F1F5F9" stroke="#64748B"/>
  <path d="M92 346 C92 336 98 329 105 329 C113 329 119 336 119 346 C119 356 113 363 105 363 C98 363 92 356 92 346 Z M78 389 C82 373 91 367 105 367 C119 367 128 373 132 389 Z" fill="#475569"/>
  <text x="71" y="404" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#334155">Users</text>

  <rect x="300" y="296" width="128" height="132" rx="24" fill="#FFFFFF" stroke="#BBD7F0" filter="url(#cardShadow)"/>
  <circle cx="364" cy="348" r="33" fill="url(#accentBlue)" filter="url(#softGlow)"/>
  <path d="M334 353 C335 339 345 333 356 336 C361 323 382 323 388 339 C399 339 407 346 407 356 C407 366 399 374 388 374 L348 374 C339 374 333 365 334 353 Z" fill="#FFFFFF"/>
  <text x="315" y="405" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#1E3A8A">Front Door</text>

  <rect x="540" y="234" width="128" height="132" rx="24" fill="#FFFFFF" stroke="#C7D2FE" filter="url(#cardShadow)"/>
  <rect x="578" y="269" width="54" height="46" rx="10" fill="#EEF2FF" stroke="#4F46E5" stroke-width="2"/>
  <path d="M588 303 L599 288 L609 299 L617 282 L627 303 Z" fill="#4F46E5"/>
  <circle cx="624" cy="277" r="4" fill="#4F46E5"/>
  <text x="554" y="343" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#3730A3">Web App</text>

  <rect x="540" y="358" width="128" height="132" rx="24" fill="#FFFFFF" stroke="#DDD6FE" filter="url(#cardShadow)"/>
  <rect x="574" y="391" width="62" height="50" rx="12" fill="#F5F3FF" stroke="#7C3AED" stroke-width="2"/>
  <path d="M588 423 L598 406 L605 418 L612 406 L626 423" fill="none" stroke="#7C3AED" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="554" y="467" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#5B21B6">API Service</text>

  <rect x="794" y="234" width="128" height="132" rx="24" fill="#FFFFFF" stroke="#BBF7D0" filter="url(#cardShadow)"/>
  <ellipse cx="858" cy="279" rx="33" ry="13" fill="#DCFCE7" stroke="#059669" stroke-width="2"/>
  <path d="M825 279 L825 316 C825 323 840 329 858 329 C876 329 891 323 891 316 L891 279" fill="#DCFCE7" stroke="#059669" stroke-width="2"/>
  <ellipse cx="858" cy="316" rx="33" ry="13" fill="#BBF7D0" stroke="#059669" stroke-width="2"/>
  <text x="810" y="343" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#047857">SQL DB</text>

  <rect x="794" y="358" width="128" height="132" rx="24" fill="#FFFFFF" stroke="#A7F3D0" filter="url(#cardShadow)"/>
  <circle cx="858" cy="418" r="32" fill="url(#accentGreen)"/>
  <path d="M839 420 C849 407 860 407 877 420 M839 420 C849 433 860 433 877 420 M858 389 L858 447 M830 418 L886 418" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="810" y="467" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#047857">Cache</text>

  <rect x="1036" y="234" width="100" height="132" rx="22" fill="#FFFFFF" stroke="#FED7AA" filter="url(#cardShadow)"/>
  <circle cx="1086" cy="294" r="30" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
  <path d="M1067 296 L1079 308 L1105 280" fill="none" stroke="#EA580C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1050" y="343" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#9A3412">Monitor</text>

  <rect x="1036" y="422" width="100" height="132" rx="22" fill="#FFFFFF" stroke="#FED7AA" filter="url(#cardShadow)"/>
  <rect x="1060" y="457" width="52" height="44" rx="9" fill="#FFF7ED" stroke="#EA580C" stroke-width="2"/>
  <path d="M1069 469 L1103 469 M1069 481 L1094 481 M1069 493 L1100 493" stroke="#EA580C" stroke-width="4" stroke-linecap="round"/>
  <text x="1050" y="531" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" text-anchor="middle" fill="#9A3412">Logs</text>

  <rect x="292" y="606" width="850" height="28" rx="14" fill="#FFFFFF" stroke="#CBD5E1"/>
  <circle cx="314" cy="620" r="5" fill="#22C55E"/>
  <text x="330" y="625" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#475569">Private endpoints and managed identity keep database traffic inside the VNet; dashed gray links indicate telemetry and operational replication.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not flatten the whole architecture into a screenshot; build boundaries, nodes, labels, and connectors as editable SVG shapes.
- ❌ Do not put `marker-end` on a parent `<g>` or on a `<path>` connector; put it directly on every `<line>` that needs an arrow.
- ❌ Do not apply filters to connector `<line>` elements; shadows/glows should stay on cards, boundaries, or icon shapes.
- ❌ Do not use `<use>` / `<symbol>` for repeated service cards, even though architecture diagrams repeat components; duplicate the editable shapes instead.
- ❌ Do not use masks or clip paths on non-image elements for subnet effects; use rounded rectangles, gradients, transparency, and dashed strokes.

## Composition notes
- Keep the largest boundary box to roughly 75–85% of the slide width, leaving room on the left for external users or internet sources.
- Use strict horizontal tiering: ingress on the left, application in the middle, data to the right, operations as a sidecar lane.
- Give every subnet generous internal padding so the dashed boundary reads as a logical security zone, not as a cramped container.
- Use one dominant traffic color for primary request flow and a quieter dashed gray for observability, replication, or control-plane dependencies.