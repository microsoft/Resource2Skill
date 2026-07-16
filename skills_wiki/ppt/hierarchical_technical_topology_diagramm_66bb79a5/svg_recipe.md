# SVG Recipe — Hierarchical Technical Topology Diagramming

## Visual mechanism
Use nested, semantically styled containers to encode infrastructure hierarchy: region, network, availability domains, and subnets. Place standardized service nodes inside the correct boundary and connect them with disciplined orthogonal routing so the diagram reads like an engineered blueprint rather than a loose flowchart.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a subtle executive title band
- 1× `<rect>` for the outer cloud region boundary with solid dark-gray stroke
- 1× `<rect>` for the virtual cloud network boundary with brick-red dashed stroke
- 2× `<rect>` for availability domain boundaries with light-gray dashed stroke and faint fill
- 4× `<rect>` for subnet boundaries with brick-red dotted stroke
- 8× `<rect>` for service-node cards with rounded corners and soft shadows
- 10× `<path>` for editable monoline service icons and small arrowhead triangles
- 7× `<line>` for topology connectors, routed horizontally/vertically
- 1× `<filter id="nodeShadow">` applied to service-node cards
- 1× `<filter id="softGlow">` applied to the outer region boundary
- 2× `<linearGradient>` fills for the title band and selected node accents
- Multiple `<text>` labels with explicit `width` attributes for all hierarchy labels, node names, and legend annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="titleBand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="accentNode" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7FAFD"/>
    </linearGradient>
    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-4%" y="-4%" width="108%" height="108%">
      <feGaussianBlur stdDeviation="2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="78" fill="url(#titleBand)"/>
  <text x="54" y="46" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="700" fill="#263238">Cloud Architecture Topology</text>
  <text x="965" y="45" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Production reference blueprint</text>

  <rect x="52" y="112" width="1176" height="548" rx="8" fill="#FFFFFF" stroke="#505050" stroke-width="2.2" filter="url(#softGlow)"/>
  <text x="76" y="105" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#505050">CLOUD REGION — us-phoenix-1</text>

  <rect x="92" y="154" width="1096" height="470" rx="8" fill="#FFFDFB" stroke="#C74634" stroke-width="2" stroke-dasharray="9 6"/>
  <text x="115" y="147" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#C74634">VCN 10.0.0.0/16</text>

  <rect x="122" y="196" width="500" height="390" rx="8" fill="#F8F8F8" stroke="#9B9B9B" stroke-width="1.8" stroke-dasharray="12 8"/>
  <text x="145" y="189" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#7D7D7D">Availability Domain 1</text>

  <rect x="658" y="196" width="500" height="390" rx="8" fill="#F8F8F8" stroke="#9B9B9B" stroke-width="1.8" stroke-dasharray="12 8"/>
  <text x="681" y="189" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#7D7D7D">Availability Domain 2</text>

  <rect x="152" y="238" width="440" height="132" rx="6" fill="#FFFFFF" stroke="#C74634" stroke-width="1.7" stroke-dasharray="2 6"/>
  <text x="173" y="232" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C74634">Public Subnet — 10.0.1.0/24</text>

  <rect x="152" y="410" width="440" height="132" rx="6" fill="#FFFFFF" stroke="#C74634" stroke-width="1.7" stroke-dasharray="2 6"/>
  <text x="173" y="404" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C74634">Private App Subnet — 10.0.2.0/24</text>

  <rect x="688" y="238" width="440" height="132" rx="6" fill="#FFFFFF" stroke="#C74634" stroke-width="1.7" stroke-dasharray="2 6"/>
  <text x="709" y="232" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C74634">Private App Subnet — 10.0.3.0/24</text>

  <rect x="688" y="410" width="440" height="132" rx="6" fill="#FFFFFF" stroke="#C74634" stroke-width="1.7" stroke-dasharray="2 6"/>
  <text x="709" y="404" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C74634">Data Subnet — 10.0.4.0/24</text>

  <rect x="88" y="292" width="78" height="58" rx="14" fill="url(#accentNode)" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M111 320 C111 309 122 309 123 319 C130 317 137 321 137 329 C137 337 130 341 121 341 L109 341 C101 341 96 337 96 330 C96 323 102 319 111 320Z" fill="none" stroke="#39424E" stroke-width="2"/>
  <text x="74" y="371" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">Internet</text>

  <rect x="230" y="276" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M259 299 L283 299 M259 310 L307 310 M259 321 L293 321" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="230" y="363" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">Load Balancer</text>

  <rect x="408" y="276" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M452 292 L494 292 L494 330 L452 330Z M459 300 L487 300 M459 310 L487 310 M459 320 L476 320" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="408" y="363" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">API Gateway</text>

  <rect x="230" y="448" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M263 471 L301 471 L301 505 L263 505Z M271 480 L293 480 M271 489 L293 489 M271 498 L286 498" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="230" y="535" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">App VM Pool A</text>

  <rect x="776" y="276" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M809 471" stroke="#39424E" stroke-width="2" fill="none"/>
  <path d="M809 299 L847 299 L847 333 L809 333Z M817 308 L839 308 M817 317 L839 317 M817 326 L832 326" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="776" y="363" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">App VM Pool B</text>

  <rect x="954" y="276" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M987 301 C987 294 1051 294 1051 301 L1051 327 C1051 335 987 335 987 327Z M987 301 C987 309 1051 309 1051 301 M987 315 C987 323 1051 323 1051 315" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="954" y="363" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">Cache Cluster</text>

  <rect x="776" y="448" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M809 473 C809 465 873 465 873 473 L873 500 C873 508 809 508 809 500Z M809 473 C809 481 873 481 873 473 M809 487 C809 495 873 495 873 487" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="776" y="535" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">Primary DB</text>

  <rect x="954" y="448" width="130" height="70" rx="10" fill="#FFFFFF" stroke="#39424E" stroke-width="1.2" filter="url(#nodeShadow)"/>
  <path d="M987 473 C987 465 1051 465 1051 473 L1051 500 C1051 508 987 508 987 500Z M987 473 C987 481 1051 481 1051 473 M987 487 C987 495 1051 495 1051 487" stroke="#39424E" stroke-width="2" fill="none"/>
  <text x="954" y="535" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" text-anchor="middle" fill="#39424E">Standby DB</text>

  <line x1="166" y1="321" x2="230" y2="321" stroke="#2563EB" stroke-width="2"/>
  <path d="M230 321 L220 316 L220 326Z" fill="#2563EB"/>
  <line x1="360" y1="311" x2="408" y2="311" stroke="#2563EB" stroke-width="2"/>
  <path d="M408 311 L398 306 L398 316Z" fill="#2563EB"/>
  <line x1="473" y1="346" x2="473" y2="431" stroke="#2563EB" stroke-width="2"/>
  <line x1="473" y1="431" x2="360" y2="483" stroke="#2563EB" stroke-width="2"/>
  <path d="M360 483 L371 483 L367 473Z" fill="#2563EB"/>
  <line x1="360" y1="483" x2="776" y2="311" stroke="#2563EB" stroke-width="2"/>
  <path d="M776 311 L766 309 L771 319Z" fill="#2563EB"/>
  <line x1="906" y1="311" x2="954" y2="311" stroke="#2563EB" stroke-width="2"/>
  <path d="M954 311 L944 306 L944 316Z" fill="#2563EB"/>
  <line x1="841" y1="346" x2="841" y2="448" stroke="#2563EB" stroke-width="2"/>
  <path d="M841 448 L836 438 L846 438Z" fill="#2563EB"/>
  <line x1="906" y1="483" x2="954" y2="483" stroke="#7C3AED" stroke-width="2" stroke-dasharray="7 5"/>
  <path d="M954 483 L944 478 L944 488Z" fill="#7C3AED"/>

  <rect x="930" y="596" width="214" height="42" rx="8" fill="#FFFFFF" stroke="#D6DADF" stroke-width="1"/>
  <line x1="952" y1="617" x2="1002" y2="617" stroke="#C74634" stroke-width="2" stroke-dasharray="2 6"/>
  <text x="1016" y="622" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#59636E">Subnet boundary</text>
</svg>
```

## Avoid in this skill
- ❌ Using random icon placement; topology diagrams need grid alignment and clear containment.
- ❌ Applying `clip-path` or masks to container rectangles; clipping is only reliable for images.
- ❌ Heavy filled boxes for every hierarchy level; it reduces nesting clarity and makes the diagram feel crowded.
- ❌ Arrowheads on `<path>` connectors; use `<line>` connectors and explicit triangle `<path>` arrowheads instead.
- ❌ Missing `width` on labels; every `<text>` needs an explicit width for clean PowerPoint translation.

## Composition notes
- Keep the outer region large, with 30–50 px of internal margin before the next hierarchy level.
- Use label color to match container stroke color: dark gray for physical boundaries, brick red for logical network boundaries.
- Service nodes should be small, consistent cards with icons; the hierarchy boxes carry the structure, nodes carry the meaning.
- Reserve the bottom-right corner for a compact legend or routing note, not for primary architecture elements.