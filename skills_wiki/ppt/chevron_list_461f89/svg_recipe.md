# SVG Recipe — Chevron List

## Visual mechanism
A vertical agenda list where each item is anchored by a bold left chevron that overlaps a rounded information card, creating a directional process-flow feel. Subtle gradients, shadows, and technical guide lines make the shell feel engineered and executive rather than like a plain bullet list.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark technical background
- 2× `<linearGradient>` for the background wash and card surface
- 4× `<linearGradient>` for chevron color accents by row
- 1× `<filter id="softShadow">` applied to rounded cards and chevrons
- 1× `<filter id="chevronGlow">` applied to chevrons for a premium neon edge
- 8× `<line>` for subtle technical grid / alignment guides
- 4× `<rect>` for rounded item cards
- 4× `<path>` for large filled chevron tabs
- 4× `<path>` for smaller inner chevron highlight facets
- 4× `<circle>` for numbered step badges inside chevrons
- 4× `<text>` for step numbers
- 4× `<text>` with nested `<tspan>` for item heading and supporting line
- 1× `<text>` for the headline
- 1× `<path>` for a thin decorative circuit trace on the right side

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="55%" stop-color="#0B1E32"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="230" y1="0" x2="1120" y2="0">
      <stop offset="0%" stop-color="#17283B"/>
      <stop offset="70%" stop-color="#101B2A"/>
      <stop offset="100%" stop-color="#0B1320"/>
    </linearGradient>

    <linearGradient id="cyanChevron" x1="120" y1="0" x2="250" y2="0">
      <stop offset="0%" stop-color="#11D5FF"/>
      <stop offset="100%" stop-color="#0877FF"/>
    </linearGradient>
    <linearGradient id="blueChevron" x1="120" y1="0" x2="250" y2="0">
      <stop offset="0%" stop-color="#6F8CFF"/>
      <stop offset="100%" stop-color="#3157E8"/>
    </linearGradient>
    <linearGradient id="violetChevron" x1="120" y1="0" x2="250" y2="0">
      <stop offset="0%" stop-color="#B76CFF"/>
      <stop offset="100%" stop-color="#7435D9"/>
    </linearGradient>
    <linearGradient id="amberChevron" x1="120" y1="0" x2="250" y2="0">
      <stop offset="0%" stop-color="#FFD166"/>
      <stop offset="100%" stop-color="#FF8A3D"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="chevronGlow" x="-30%" y="-40%" width="160%" height="190%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <line x1="88" y1="120" x2="1188" y2="120" stroke="#24425E" stroke-width="1" stroke-dasharray="6 10" opacity="0.42"/>
  <line x1="88" y1="615" x2="1188" y2="615" stroke="#24425E" stroke-width="1" stroke-dasharray="6 10" opacity="0.32"/>
  <line x1="125" y1="86" x2="125" y2="646" stroke="#24425E" stroke-width="1" stroke-dasharray="5 12" opacity="0.30"/>
  <line x1="248" y1="86" x2="248" y2="646" stroke="#24425E" stroke-width="1" stroke-dasharray="5 12" opacity="0.24"/>
  <line x1="1132" y1="86" x2="1132" y2="646" stroke="#24425E" stroke-width="1" stroke-dasharray="5 12" opacity="0.30"/>
  <line x1="1176" y1="155" x2="1176" y2="548" stroke="#35C7FF" stroke-width="2" opacity="0.18"/>
  <line x1="1052" y1="214" x2="1176" y2="214" stroke="#35C7FF" stroke-width="2" opacity="0.16"/>
  <line x1="1052" y1="506" x2="1176" y2="506" stroke="#35C7FF" stroke-width="2" opacity="0.16"/>

  <text x="125" y="82" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#F5FAFF" letter-spacing="0.2">
    Product Launch Operating Plan
  </text>
  <text x="126" y="112" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#7FA4C7" letter-spacing="2.6">
    FOUR-PHASE CHEVRON AGENDA
  </text>

  <path d="M1088 175 L1150 175 L1150 214 L1182 214 L1182 287 L1146 287 L1146 361 L1182 361 L1182 434 L1150 434 L1150 548 L1088 548"
        fill="none" stroke="#1B91C9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.42"/>

  <g>
    <rect x="228" y="158" width="890" height="92" rx="24" fill="url(#cardFill)" stroke="#28435C" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M122 158 L230 158 L282 204 L230 250 L122 250 L174 204 Z" fill="url(#cyanChevron)" filter="url(#chevronGlow)"/>
    <path d="M146 171 L223 171 L258 204 L223 237 L146 237 L181 204 Z" fill="#FFFFFF" opacity="0.16"/>
    <circle cx="191" cy="204" r="25" fill="#07111F" opacity="0.72" stroke="#C7F5FF" stroke-width="1.5"/>
    <text x="176" y="214" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#E9FCFF">01</text>
    <text x="315" y="195" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#F3F8FF">
      Market signal scan
      <tspan x="315" dy="27" font-size="15" font-weight="400" fill="#A8BBD0">Validate customer demand, risk triggers, and early adoption indicators.</tspan>
    </text>
  </g>

  <g>
    <rect x="248" y="274" width="870" height="92" rx="24" fill="url(#cardFill)" stroke="#28435C" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M142 274 L250 274 L302 320 L250 366 L142 366 L194 320 Z" fill="url(#blueChevron)" filter="url(#chevronGlow)"/>
    <path d="M166 287 L243 287 L278 320 L243 353 L166 353 L201 320 Z" fill="#FFFFFF" opacity="0.15"/>
    <circle cx="211" cy="320" r="25" fill="#07111F" opacity="0.72" stroke="#D9E0FF" stroke-width="1.5"/>
    <text x="196" y="330" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#F0F3FF">02</text>
    <text x="335" y="311" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#F3F8FF">
      Offer architecture
      <tspan x="335" dy="27" font-size="15" font-weight="400" fill="#A8BBD0">Package the roadmap, commercial model, and proof points into one narrative.</tspan>
    </text>
  </g>

  <g>
    <rect x="228" y="390" width="890" height="92" rx="24" fill="url(#cardFill)" stroke="#28435C" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M122 390 L230 390 L282 436 L230 482 L122 482 L174 436 Z" fill="url(#violetChevron)" filter="url(#chevronGlow)"/>
    <path d="M146 403 L223 403 L258 436 L223 469 L146 469 L181 436 Z" fill="#FFFFFF" opacity="0.15"/>
    <circle cx="191" cy="436" r="25" fill="#07111F" opacity="0.72" stroke="#E8D1FF" stroke-width="1.5"/>
    <text x="176" y="446" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#F7EEFF">03</text>
    <text x="315" y="427" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#F3F8FF">
      Launch execution
      <tspan x="315" dy="27" font-size="15" font-weight="400" fill="#A8BBD0">Coordinate content, sales enablement, partner motion, and launch governance.</tspan>
    </text>
  </g>

  <g>
    <rect x="248" y="506" width="870" height="92" rx="24" fill="url(#cardFill)" stroke="#28435C" stroke-width="1.5" filter="url(#softShadow)"/>
    <path d="M142 506 L250 506 L302 552 L250 598 L142 598 L194 552 Z" fill="url(#amberChevron)" filter="url(#chevronGlow)"/>
    <path d="M166 519 L243 519 L278 552 L243 585 L166 585 L201 552 Z" fill="#FFFFFF" opacity="0.18"/>
    <circle cx="211" cy="552" r="25" fill="#07111F" opacity="0.72" stroke="#FFE6A6" stroke-width="1.5"/>
    <text x="196" y="562" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#FFF6DD">04</text>
    <text x="335" y="543" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#F3F8FF">
      Scale and optimize
      <tspan x="335" dy="27" font-size="15" font-weight="400" fill="#A8BBD0">Review telemetry, remove friction, and prioritize the next growth experiments.</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` on chevron connector paths; if arrows are needed, draw arrowheads as explicit `<path>` shapes.
- ❌ Applying `filter` to `<line>` guide marks; shadows and glows should be on cards, chevrons, paths, or text only.
- ❌ Building chevrons from `<polygon>` if the target pipeline is strict; use editable `<path d="...">` chevron geometry instead.
- ❌ Letting text auto-size or omit `width`; every `<text>` needs a fixed width so PowerPoint preserves the layout.
- ❌ Making all four rows identical x-positions; slight alternating offsets add depth while preserving a clean vertical reading path.

## Composition notes
- Keep the chevrons on the left third of the slide and let them overlap the rounded cards by 35–60 px to create a locked-together process structure.
- Use a dark, low-contrast background with dashed technical guide lines; the chevrons should carry the saturated color rhythm.
- The main card text should start well after the chevron point, typically around x=315–340, leaving clear breathing room.
- Four items fit best at 90–96 px height with 20–26 px vertical gaps; for three items, increase row height and spacing rather than stretching text.