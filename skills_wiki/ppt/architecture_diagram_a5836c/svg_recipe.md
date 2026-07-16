# SVG Recipe — Architecture Diagram

## Visual mechanism
A premium technical architecture slide built around a luminous three-layer center stack, flanked by optional capability sidebars. The visual hierarchy comes from large rounded platform bands, smaller module cards inside each band, and thin connector lines that imply data/control flow without overwhelming the slide.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark executive background
- 2× decorative `<path>` blobs for soft ambient color fields behind the diagram
- 3× large rounded `<rect>` for the central architecture layers
- 9× small rounded `<rect>` for editable module cards inside the layers
- 2× sidebar rounded `<rect>` panels for left and right capability groups
- 8× sidebar item `<rect>` rows for supporting services, users, governance, and operations
- Multiple `<line>` elements for cross-panel connectors and vertical flow rails
- Multiple `<circle>` elements for connector nodes and status dots
- Multiple `<path>` elements for simple editable icons and arrowheads
- 1× `<filter id="softShadow">` for elevated cards and panels
- 1× `<filter id="blueGlow">` for the central stack emphasis
- Several `<linearGradient>` and `<radialGradient>` definitions for premium layered fills
- Multiple `<text>` elements with explicit `width` attributes for titles, labels, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#08111F"/>
      <stop offset="55%" stop-color="#0B1730"/>
      <stop offset="100%" stop-color="#060A12"/>
    </linearGradient>
    <radialGradient id="orbBlue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2F80FF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#2F80FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orbViolet" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="layerTop" x1="280" y1="150" x2="1000" y2="150">
      <stop offset="0%" stop-color="#1E6BFF"/>
      <stop offset="100%" stop-color="#32D6FF"/>
    </linearGradient>
    <linearGradient id="layerMid" x1="280" y1="305" x2="1000" y2="305">
      <stop offset="0%" stop-color="#6D5DF6"/>
      <stop offset="100%" stop-color="#1CC7B7"/>
    </linearGradient>
    <linearGradient id="layerBot" x1="280" y1="460" x2="1000" y2="460">
      <stop offset="0%" stop-color="#34445E"/>
      <stop offset="100%" stop-color="#1C2B3E"/>
    </linearGradient>
    <linearGradient id="cardFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blueGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M-80,190 C130,20 280,70 370,180 C455,285 310,405 130,390 C-30,375 -170,300 -80,190 Z" fill="url(#orbBlue)"/>
  <path d="M1040,70 C1215,25 1345,150 1330,315 C1315,465 1160,515 1040,430 C925,350 880,115 1040,70 Z" fill="url(#orbViolet)"/>

  <text x="72" y="64" width="650" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700">
    AI Platform Reference Architecture
  </text>
  <text x="74" y="96" width="620" fill="#AAB7CF" font-family="Segoe UI, Microsoft YaHei" font-size="15">
    Three-layer stack with channel, service, and governance interfaces
  </text>

  <rect x="70" y="156" width="210" height="430" rx="24" fill="#0E1A2E" stroke="#263B5D" stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="96" y="198" width="158" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700">Experience Channels</text>
  <text x="96" y="224" width="150" fill="#89A0C2" font-family="Segoe UI, Microsoft YaHei" font-size="12">entry points</text>

  <rect x="94" y="258" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="118" cy="282" r="7" fill="#42D7FF"/>
  <text x="136" y="287" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Web portal</text>

  <rect x="94" y="324" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="118" cy="348" r="7" fill="#42D7FF"/>
  <text x="136" y="353" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Mobile app</text>

  <rect x="94" y="390" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="118" cy="414" r="7" fill="#42D7FF"/>
  <text x="136" y="419" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Partner API</text>

  <rect x="94" y="456" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="118" cy="480" r="7" fill="#42D7FF"/>
  <text x="136" y="485" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Analyst console</text>

  <rect x="300" y="140" width="680" height="118" rx="30" fill="url(#layerTop)" opacity="0.93" filter="url(#softShadow)"/>
  <rect x="300" y="140" width="680" height="118" rx="30" fill="none" stroke="#B8F2FF" stroke-opacity="0.45"/>
  <text x="330" y="179" width="240" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700">Presentation & API Layer</text>
  <text x="330" y="203" width="230" fill="#DDF7FF" font-family="Segoe UI, Microsoft YaHei" font-size="12">secure access, routing, experience logic</text>

  <rect x="570" y="166" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#DDF8FF" stroke-opacity="0.4"/>
  <path d="M607,189 L623,178 L639,189 L639,207 L607,207 Z" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="590" y="239" width="78" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Gateway</text>

  <rect x="704" y="166" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#DDF8FF" stroke-opacity="0.4"/>
  <path d="M744,184 C754,174 770,174 780,184 C790,194 790,210 780,220 L744,220 C734,210 734,194 744,184 Z" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="762" y="239" width="82" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Identity</text>

  <rect x="838" y="166" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#DDF8FF" stroke-opacity="0.4"/>
  <path d="M874,191 L896,178 L918,191 L896,204 Z M874,205 L896,218 L918,205" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="896" y="239" width="84" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Orchestration</text>

  <rect x="300" y="296" width="680" height="118" rx="30" fill="url(#layerMid)" opacity="0.94" filter="url(#softShadow)"/>
  <rect x="300" y="296" width="680" height="118" rx="30" fill="none" stroke="#C4FFF4" stroke-opacity="0.4"/>
  <text x="330" y="335" width="240" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700">AI Service Layer</text>
  <text x="330" y="359" width="230" fill="#E5FFFB" font-family="Segoe UI, Microsoft YaHei" font-size="12">models, tools, workflow services</text>

  <rect x="570" y="322" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#E1FFFA" stroke-opacity="0.4"/>
  <circle cx="628" cy="346" r="15" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M618,346 L628,336 L638,346 L628,356 Z" fill="#FFFFFF"/>
  <text x="628" y="395" width="88" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Model router</text>

  <rect x="704" y="322" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#E1FFFA" stroke-opacity="0.4"/>
  <path d="M742,346 C742,334 782,334 782,346 C782,358 742,358 742,346 Z M752,346 L752,366 M772,346 L772,366" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="762" y="395" width="84" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Vector search</text>

  <rect x="838" y="322" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#E1FFFA" stroke-opacity="0.4"/>
  <path d="M876,336 H916 V366 H876 Z M886,346 H906 M886,356 H906" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="896" y="395" width="84" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Tool services</text>

  <rect x="300" y="452" width="680" height="118" rx="30" fill="url(#layerBot)" opacity="0.97" filter="url(#softShadow)"/>
  <rect x="300" y="452" width="680" height="118" rx="30" fill="none" stroke="#6D87AA" stroke-opacity="0.55"/>
  <text x="330" y="491" width="250" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700">Data & Infrastructure Layer</text>
  <text x="330" y="515" width="245" fill="#B7C9E8" font-family="Segoe UI, Microsoft YaHei" font-size="12">governed data, runtime, cloud foundations</text>

  <rect x="570" y="478" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#B8C8E4" stroke-opacity="0.35"/>
  <path d="M606,494 C606,486 650,486 650,494 V520 C650,528 606,528 606,520 Z M606,494 C606,502 650,502 650,494" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="628" y="551" width="84" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Lakehouse</text>

  <rect x="704" y="478" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#B8C8E4" stroke-opacity="0.35"/>
  <path d="M744,498 L762,486 L780,498 V520 H744 Z M753,520 V506 H771 V520" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="762" y="551" width="84" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Runtime</text>

  <rect x="838" y="478" width="116" height="58" rx="16" fill="url(#cardFill)" stroke="#B8C8E4" stroke-opacity="0.35"/>
  <path d="M876,508 C876,496 886,488 896,488 C906,488 916,496 916,508 C916,520 906,528 896,528 C886,528 876,520 876,508 Z M896,488 V528 M876,508 H916" fill="none" stroke="#FFFFFF" stroke-width="2"/>
  <text x="896" y="551" width="84" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="middle">Cloud fabric</text>

  <line x1="640" y1="258" x2="640" y2="296" stroke="#8DF6FF" stroke-width="2" stroke-dasharray="5 6"/>
  <line x1="640" y1="414" x2="640" y2="452" stroke="#8DF6FF" stroke-width="2" stroke-dasharray="5 6"/>
  <circle cx="640" cy="276" r="5" fill="#8DF6FF"/>
  <circle cx="640" cy="432" r="5" fill="#8DF6FF"/>

  <line x1="256" y1="282" x2="300" y2="199" stroke="#395B85" stroke-width="2"/>
  <line x1="256" y1="414" x2="300" y2="355" stroke="#395B85" stroke-width="2"/>
  <path d="M294,199 L282,193 L284,207 Z" fill="#42D7FF"/>
  <path d="M294,355 L282,349 L284,363 Z" fill="#42D7FF"/>

  <rect x="1000" y="156" width="210" height="430" rx="24" fill="#0E1A2E" stroke="#263B5D" stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="1026" y="198" width="160" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700">Governance & Ops</text>
  <text x="1026" y="224" width="150" fill="#89A0C2" font-family="Segoe UI, Microsoft YaHei" font-size="12">controls across all layers</text>

  <rect x="1024" y="258" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="1048" cy="282" r="7" fill="#A78BFA"/>
  <text x="1066" y="287" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Policy guardrails</text>

  <rect x="1024" y="324" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="1048" cy="348" r="7" fill="#A78BFA"/>
  <text x="1066" y="353" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Observability</text>

  <rect x="1024" y="390" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="1048" cy="414" r="7" fill="#A78BFA"/>
  <text x="1066" y="419" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Cost controls</text>

  <rect x="1024" y="456" width="162" height="48" rx="14" fill="#13243D" stroke="#31507A"/>
  <circle cx="1048" cy="480" r="7" fill="#A78BFA"/>
  <text x="1066" y="485" width="96" fill="#DCE8FF" font-family="Segoe UI, Microsoft YaHei" font-size="13">Audit trail</text>

  <line x1="980" y1="199" x2="1024" y2="282" stroke="#4C3B78" stroke-width="2"/>
  <line x1="980" y1="355" x2="1024" y2="348" stroke="#4C3B78" stroke-width="2"/>
  <line x1="980" y1="511" x2="1024" y2="480" stroke="#4C3B78" stroke-width="2"/>
  <path d="M1018,282 L1006,276 L1008,290 Z" fill="#A78BFA"/>
  <path d="M1018,348 L1006,342 L1008,356 Z" fill="#A78BFA"/>
  <path d="M1018,480 L1006,474 L1008,488 Z" fill="#A78BFA"/>

  <rect x="300" y="612" width="680" height="42" rx="21" fill="#0D1729" stroke="#2B4264"/>
  <circle cx="332" cy="633" r="6" fill="#28E0B9"/>
  <text x="350" y="638" width="590" fill="#AAB7CF" font-family="Segoe UI, Microsoft YaHei" font-size="13">
    Principle: decouple experience channels from model services through governed APIs and shared telemetry.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to repeat module cards; duplicate editable SVG primitives directly so PPT shapes remain independent.
- ❌ Do not apply `filter` to connector `<line>` elements; filters on lines are dropped, so use unfiltered lines plus glowing nodes if emphasis is needed.
- ❌ Do not use `marker-end` on `<path>` connectors; draw arrowheads as small editable `<path>` triangles.
- ❌ Do not overpack labels inside module cards; PowerPoint no-autofit text needs explicit `width` and enough horizontal room.
- ❌ Do not rely on masks or clipping for non-image shapes; use layered rounded rectangles and paths instead.

## Composition notes
- Keep the center stack dominant: reserve roughly 55% of slide width for the three architecture layers, with sidebars acting as secondary context.
- Use strong color separation by layer: bright cyan for access/API, teal-violet for AI services, and slate for data/infrastructure.
- Leave clear vertical gaps between layers so dashed flow rails and node dots are readable.
- Put dense explanatory text in the footer ribbon, not inside the layer cards; module labels should stay short and scannable.