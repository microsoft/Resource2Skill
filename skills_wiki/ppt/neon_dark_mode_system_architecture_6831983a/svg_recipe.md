# SVG Recipe — Neon Dark-Mode System Architecture

## Visual mechanism
A deep slate canvas turns the diagram into a cinematic dark-mode surface, while rounded neon “pill” nodes divide the architecture into ingestion, core processing, and delivery layers. Thin glowing connector lines, subtle radial backlights, and small technical labels create a premium developer-keynote feel without sacrificing diagram clarity.

## SVG primitives needed
- 1× `<rect>` for the full-slide near-black background.
- 1× `<linearGradient>` for the background vignette wash.
- 3× `<radialGradient>` for ambient neon glows behind the main architecture zones.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for blurred neon backlights.
- 1× `<filter id="nodeShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for elevated node depth.
- 1× `<marker>` arrowhead definition used directly on each `<line>`.
- 10× `<rect>` for rounded architecture nodes, labels, and status chips.
- 12× `<line>` for editable connector arrows between architecture components.
- 10× `<circle>` / `<ellipse>` for endpoint lights, database cylinders, and ambient technical details.
- 8× `<path>` for database cylinder curves, minimal icons, and decorative circuit traces.
- Multiple `<text>` elements with explicit `width` attributes for title, section labels, node names, and metadata.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101216"/>
      <stop offset="55%" stop-color="#151A21"/>
      <stop offset="100%" stop-color="#090B0F"/>
    </linearGradient>

    <radialGradient id="cyanAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BCD4" stop-opacity="0.55"/>
      <stop offset="50%" stop-color="#00BCD4" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00BCD4" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blueAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2980B9" stop-opacity="0.45"/>
      <stop offset="60%" stop-color="#2980B9" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#2980B9" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="greenAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#27AE60" stop-opacity="0.42"/>
      <stop offset="60%" stop-color="#27AE60" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#27AE60" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="producerFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3498DB"/>
      <stop offset="100%" stop-color="#1B5F9E"/>
    </linearGradient>
    <linearGradient id="brokerFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#19E6F4"/>
      <stop offset="100%" stop-color="#008CA3"/>
    </linearGradient>
    <linearGradient id="consumerFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4BE38B"/>
      <stop offset="100%" stop-color="#138A4D"/>
    </linearGradient>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <filter id="nodeShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <marker id="arrowCyan" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="#7DEBFF"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="42" y="58" width="8" height="68" rx="4" fill="#69E6BE"/>
  <text x="72" y="105" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#FFFFFF">Event-Driven Architecture</text>
  <text x="74" y="142" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#AEB8C4">Decoupling services with real-time streams, durable queues, and scalable consumers</text>

  <path d="M1012 64 C1084 48 1162 72 1218 118" fill="none" stroke="#1F3942" stroke-width="2" stroke-dasharray="7 8"/>
  <path d="M1038 102 C1106 90 1168 116 1218 166" fill="none" stroke="#203F35" stroke-width="2" stroke-dasharray="4 9"/>
  <circle cx="1188" cy="116" r="5" fill="#00BCD4"/>
  <circle cx="1134" cy="86" r="3" fill="#27AE60"/>

  <ellipse cx="252" cy="408" rx="260" ry="210" fill="url(#blueAura)" filter="url(#softGlow)"/>
  <ellipse cx="640" cy="396" rx="310" ry="240" fill="url(#cyanAura)" filter="url(#softGlow)"/>
  <ellipse cx="1024" cy="408" rx="260" ry="210" fill="url(#greenAura)" filter="url(#softGlow)"/>

  <rect x="54" y="200" width="320" height="402" rx="28" fill="#111821" stroke="#243240" stroke-width="1.5"/>
  <rect x="480" y="196" width="320" height="410" rx="30" fill="#101C24" stroke="#1F5060" stroke-width="1.5"/>
  <rect x="906" y="200" width="320" height="402" rx="28" fill="#111A18" stroke="#254033" stroke-width="1.5"/>

  <text x="82" y="238" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#79CFFF">PRODUCERS</text>
  <text x="510" y="234" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#7DEBFF">CORE MESSAGE FABRIC</text>
  <text x="936" y="238" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#7FF0A8">CONSUMERS</text>

  <line x1="306" y1="324" x2="508" y2="356" stroke="#7DEBFF" stroke-width="2" stroke-opacity="0.72" marker-end="url(#arrowCyan)"/>
  <line x1="306" y1="444" x2="508" y2="430" stroke="#7DEBFF" stroke-width="2" stroke-opacity="0.72" marker-end="url(#arrowCyan)"/>
  <line x1="772" y1="356" x2="960" y2="322" stroke="#7DEBFF" stroke-width="2" stroke-opacity="0.72" marker-end="url(#arrowCyan)"/>
  <line x1="772" y1="430" x2="960" y2="448" stroke="#7DEBFF" stroke-width="2" stroke-opacity="0.72" marker-end="url(#arrowCyan)"/>
  <line x1="640" y1="344" x2="640" y2="292" stroke="#7DEBFF" stroke-width="2" stroke-opacity="0.6" marker-end="url(#arrowCyan)"/>
  <line x1="640" y1="456" x2="640" y2="522" stroke="#7DEBFF" stroke-width="2" stroke-opacity="0.6" marker-end="url(#arrowCyan)"/>

  <rect x="96" y="280" width="210" height="88" rx="44" fill="url(#producerFill)" filter="url(#nodeShadow)"/>
  <text x="128" y="316" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Web Apps</text>
  <text x="128" y="344" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#E6F4FF">clickstream events</text>

  <rect x="96" y="400" width="210" height="88" rx="44" fill="url(#producerFill)" filter="url(#nodeShadow)"/>
  <text x="128" y="436" width="158" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">IoT Devices</text>
  <text x="128" y="464" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#E6F4FF">telemetry streams</text>

  <rect x="508" y="344" width="264" height="112" rx="56" fill="url(#brokerFill)" filter="url(#nodeShadow)"/>
  <text x="560" y="388" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">Message Broker</text>
  <text x="566" y="421" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#D7FBFF">Kafka · Pulsar · NATS</text>

  <rect x="528" y="244" width="224" height="56" rx="28" fill="#152A33" stroke="#1CBBD0" stroke-width="1.5"/>
  <text x="574" y="278" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#A9F7FF">Schema Registry</text>

  <rect x="528" y="522" width="224" height="56" rx="28" fill="#152A33" stroke="#1CBBD0" stroke-width="1.5"/>
  <text x="574" y="556" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#A9F7FF">Dead-letter Queue</text>

  <rect x="960" y="278" width="210" height="88" rx="44" fill="url(#consumerFill)" filter="url(#nodeShadow)"/>
  <text x="994" y="314" width="148" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Analytics API</text>
  <text x="994" y="342" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#E9FFF0">real-time insights</text>

  <rect x="960" y="404" width="210" height="88" rx="44" fill="url(#consumerFill)" filter="url(#nodeShadow)"/>
  <text x="994" y="440" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Data Lake</text>
  <text x="994" y="468" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#E9FFF0">batch enrichment</text>

  <circle cx="306" cy="324" r="5" fill="#7DEBFF"/>
  <circle cx="306" cy="444" r="5" fill="#7DEBFF"/>
  <circle cx="508" cy="356" r="5" fill="#7DEBFF"/>
  <circle cx="508" cy="430" r="5" fill="#7DEBFF"/>
  <circle cx="772" cy="356" r="5" fill="#7DEBFF"/>
  <circle cx="772" cy="430" r="5" fill="#7DEBFF"/>

  <ellipse cx="201" cy="552" rx="55" ry="14" fill="#071016" stroke="#79CFFF" stroke-width="2"/>
  <path d="M146 552 L146 584 C146 592 170 600 201 600 C232 600 256 592 256 584 L256 552" fill="none" stroke="#79CFFF" stroke-width="2"/>
  <path d="M146 584 C146 592 170 600 201 600 C232 600 256 592 256 584" fill="none" stroke="#79CFFF" stroke-width="2"/>
  <text x="168" y="578" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#AEE7FF">Source DB</text>

  <ellipse cx="1065" cy="552" rx="55" ry="14" fill="#07130E" stroke="#7FF0A8" stroke-width="2"/>
  <path d="M1010 552 L1010 584 C1010 592 1034 600 1065 600 C1096 600 1120 592 1120 584 L1120 552" fill="none" stroke="#7FF0A8" stroke-width="2"/>
  <path d="M1010 584 C1010 592 1034 600 1065 600 C1096 600 1120 592 1120 584" fill="none" stroke="#7FF0A8" stroke-width="2"/>
  <text x="1034" y="578" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BFFFD4">Warehouse</text>

  <rect x="76" y="640" width="1128" height="32" rx="16" fill="#0C1117" stroke="#22313D"/>
  <text x="104" y="662" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7F8D9B">SLO: 99.95% delivery</text>
  <text x="436" y="662" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7F8D9B">Latency target: &lt; 200ms</text>
  <text x="760" y="662" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7F8D9B">Autoscaling consumers · encrypted topics · replayable logs</text>
</svg>
```

## Avoid in this skill
- ❌ Putting arrowheads on `<path>` connectors; use `<line marker-end="url(#arrowCyan)">` on each connector directly.
- ❌ Applying filters to connector `<line>` elements; use opacity, color, and nearby glow shapes instead.
- ❌ Overloading the canvas with too many equal-weight nodes; reserve the strongest glow and brightest fill for the core broker or orchestrator.
- ❌ Using pure saturated neon on every element; balance bright fills with dark cards, muted strokes, and gray metadata text.
- ❌ Omitting `width` on text elements; every label needs explicit width for clean editable PowerPoint rendering.

## Composition notes
- Keep the diagram in a three-column architecture flow: producers on the left, core message fabric in the center, consumers on the right.
- Allocate the brightest glow to the central system node so the audience understands the control plane or broker is the focal point.
- Use generous dark negative space around connectors; the premium look comes from clean routing, not dense linework.
- Repeat cyan as the connector color, then reserve blue and green fills for semantic grouping of inputs and outputs.