# SVG Recipe — Architecture Evolution

## Visual mechanism
A three-stage horizontal evolution timeline shows structure becoming more modular from left to right: a single contained block, then separated layers, then a constellation of independently deployable services. Use repeated cards, directional connectors, and increasing internal fragmentation to communicate architectural maturity and complexity.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× large rounded `<rect>` cards for the three architecture phases
- 20+ smaller `<rect>` modules for monolith layers, platform components, and microservices
- 10+ `<circle>` / `<ellipse>` nodes for databases, events, and service endpoints
- 8× `<line>` elements for timeline arrows and service connections
- 6× `<path>` elements for glow accents, arrowheads, database silhouettes, and decorative architecture traces
- Multiple `<text>` elements with explicit `width` for headline, stage labels, captions, and component names
- 2× `<linearGradient>` definitions for background and card/module fills
- 1× `<radialGradient>` for ambient glow behind the final distributed phase
- 2× `<filter>` definitions for soft shadows and neon glow applied to cards, paths, and selected nodes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="48%" stop-color="#0B1C30"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#172A44"/>
      <stop offset="100%" stop-color="#0D1728"/>
    </linearGradient>
    <linearGradient id="moduleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#33D6FF"/>
      <stop offset="100%" stop-color="#6C5CE7"/>
    </linearGradient>
    <radialGradient id="serviceGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#2FE6C8" stop-opacity="0.34"/>
      <stop offset="70%" stop-color="#2FE6C8" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#2FE6C8" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M60 610 C250 520, 340 650, 520 560 S830 475, 1210 585" fill="none" stroke="#244567" stroke-width="2" stroke-dasharray="8 14" opacity="0.5"/>
  <path d="M130 116 C340 64, 560 92, 720 58 S1030 70, 1180 130" fill="none" stroke="#1AD9FF" stroke-width="3" opacity="0.18" filter="url(#glow)"/>

  <text x="80" y="68" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F3F8FF">Architecture Evolution</text>
  <text x="82" y="104" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#9FB3C9">From tightly coupled delivery to layered capabilities to autonomous, composable services.</text>

  <rect x="80" y="166" width="320" height="420" rx="28" fill="url(#cardGrad)" stroke="#28445F" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="480" y="166" width="320" height="420" rx="28" fill="url(#cardGrad)" stroke="#28445F" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="880" y="166" width="320" height="420" rx="28" fill="url(#cardGrad)" stroke="#2A5B63" stroke-width="1.5" filter="url(#shadow)"/>
  <ellipse cx="1040" cy="360" rx="210" ry="190" fill="url(#serviceGlow)"/>

  <line x1="410" y1="376" x2="462" y2="376" stroke="#55D6FF" stroke-width="3"/>
  <path d="M462 376 L448 367 L448 385 Z" fill="#55D6FF"/>
  <line x1="810" y1="376" x2="862" y2="376" stroke="#55D6FF" stroke-width="3"/>
  <path d="M862 376 L848 367 L848 385 Z" fill="#55D6FF"/>

  <text x="110" y="218" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">1. Monolith</text>
  <text x="110" y="244" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB3C9">One deployable unit, one release train.</text>
  <rect x="126" y="284" width="228" height="202" rx="20" fill="#0C1525" stroke="#3E5876" stroke-width="2"/>
  <rect x="146" y="310" width="188" height="42" rx="10" fill="#1D88FF" opacity="0.95"/>
  <rect x="146" y="362" width="188" height="42" rx="10" fill="#5B6CFF" opacity="0.95"/>
  <rect x="146" y="414" width="188" height="42" rx="10" fill="#8F5CFF" opacity="0.95"/>
  <text x="166" y="337" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#FFFFFF">UI + API</text>
  <text x="166" y="389" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#FFFFFF">Business Logic</text>
  <text x="166" y="441" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#FFFFFF">Data Access</text>
  <ellipse cx="240" cy="502" rx="80" ry="18" fill="#16263A" stroke="#517090"/>
  <path d="M160 502 L160 532 C160 542, 320 542, 320 532 L320 502 C320 512, 160 512, 160 502 Z" fill="#101C2E" stroke="#517090"/>
  <text x="190" y="530" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#BFD2E6">Shared DB</text>

  <text x="510" y="218" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">2. Modular Platform</text>
  <text x="510" y="244" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB3C9">Capabilities split, still coordinated centrally.</text>
  <rect x="532" y="292" width="216" height="54" rx="14" fill="#172235" stroke="#50C7FF"/>
  <rect x="532" y="368" width="216" height="54" rx="14" fill="#172235" stroke="#8977FF"/>
  <rect x="532" y="444" width="216" height="54" rx="14" fill="#172235" stroke="#2FE6C8"/>
  <rect x="550" y="306" width="52" height="26" rx="7" fill="#1D88FF"/>
  <rect x="614" y="306" width="52" height="26" rx="7" fill="#1D88FF" opacity="0.7"/>
  <rect x="678" y="306" width="52" height="26" rx="7" fill="#1D88FF" opacity="0.45"/>
  <rect x="550" y="382" width="82" height="26" rx="7" fill="#7167FF"/>
  <rect x="646" y="382" width="82" height="26" rx="7" fill="#7167FF" opacity="0.65"/>
  <rect x="550" y="458" width="178" height="26" rx="7" fill="#2FE6C8" opacity="0.86"/>
  <text x="550" y="275" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#DDEBFA">Separated application layers</text>
  <text x="552" y="333" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#EAF7FF">Experience modules</text>
  <text x="552" y="409" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#EAF7FF">Domain services</text>
  <text x="552" y="485" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#082522">Platform data layer</text>
  <line x1="640" y1="346" x2="640" y2="368" stroke="#5B7898" stroke-width="2" stroke-dasharray="5 5"/>
  <line x1="640" y1="422" x2="640" y2="444" stroke="#5B7898" stroke-width="2" stroke-dasharray="5 5"/>

  <text x="910" y="218" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">3. Distributed Services</text>
  <text x="910" y="244" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB3C9">Autonomous teams, contracts, events, and independent scaling.</text>
  <line x1="1017" y1="326" x2="948" y2="366" stroke="#466B87" stroke-width="2"/>
  <line x1="1017" y1="326" x2="1096" y2="360" stroke="#466B87" stroke-width="2"/>
  <line x1="948" y1="366" x2="1002" y2="438" stroke="#466B87" stroke-width="2"/>
  <line x1="1096" y1="360" x2="1078" y2="454" stroke="#466B87" stroke-width="2"/>
  <line x1="1002" y1="438" x2="1078" y2="454" stroke="#466B87" stroke-width="2"/>
  <rect x="962" y="292" width="110" height="68" rx="18" fill="url(#moduleGrad)" filter="url(#glow)"/>
  <rect x="906" y="346" width="88" height="58" rx="16" fill="#192B42" stroke="#36D6FF" stroke-width="2"/>
  <rect x="1054" y="340" width="92" height="60" rx="16" fill="#192B42" stroke="#2FE6C8" stroke-width="2"/>
  <rect x="952" y="416" width="100" height="64" rx="16" fill="#192B42" stroke="#8C7BFF" stroke-width="2"/>
  <rect x="1040" y="434" width="96" height="62" rx="16" fill="#192B42" stroke="#FFB86B" stroke-width="2"/>
  <circle cx="1138" cy="292" r="18" fill="#2FE6C8" opacity="0.9"/>
  <circle cx="930" cy="474" r="16" fill="#55D6FF" opacity="0.8"/>
  <circle cx="1118" cy="520" r="12" fill="#FFB86B" opacity="0.8"/>
  <text x="984" y="333" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">API Edge</text>
  <text x="928" y="380" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#EAF7FF">Billing</text>
  <text x="1074" y="376" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#EAF7FF">Identity</text>
  <text x="974" y="454" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#EAF7FF">Orders</text>
  <text x="1062" y="472" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#EAF7FF">Events</text>

  <text x="120" y="626" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8FA6BF">Coupling: high · Deployment: single</text>
  <text x="520" y="626" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8FA6BF">Coupling: managed · Delivery: coordinated</text>
  <text x="920" y="626" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8FA6BF">Coupling: low · Delivery: independent</text>
</svg>
```

## Avoid in this skill
- ❌ Do not represent the three phases as identical boxes; the internal structure must visibly increase in modularity from left to right.
- ❌ Do not use `marker-end` on `<path>` connectors; use `<line>` plus editable triangular `<path>` arrowheads.
- ❌ Do not rely on non-editable screenshots of architecture diagrams; build the system blocks as native SVG shapes.
- ❌ Do not place dense labels inside every microservice node; too much text destroys the “evolution at a glance” read.

## Composition notes
- Keep the three phase cards aligned on a single horizontal axis, with generous gutters for directional arrows.
- Reserve the top 15–18% of the slide for headline and framing sentence; the diagram should dominate the middle.
- Use increasingly fragmented internals: one large stack, then layered modules, then a network of small services.
- Let the final phase carry the brightest glow/accent color so the eye reads the evolution as forward progress.