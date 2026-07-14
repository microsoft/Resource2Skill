# SVG Recipe — Dynamic Flowchart with Anchored Connectors

## Visual mechanism
A clean top-down flowchart where every connector endpoint lands precisely on a node’s connection site: top, right, bottom, or left. The diagram remains readable because connectors are drawn behind white-filled nodes, while decision outcomes use strong semantic colors for fast branch scanning.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 2× decorative `<path>` blobs for subtle executive-style depth
- 5× `<rect>` for process/action nodes and section labels
- 1× `<path>` for the decision diamond
- 2× `<ellipse>` for Yes/No semantic branch nodes
- 14× `<line>` for connector segments, including elbow-style routes made from multiple native lines
- 1× `<marker>` arrowhead definition applied directly to each final `<line>` segment
- 1× `<filter id="softShadow">` applied to nodes for subtle elevation
- 1× `<linearGradient>` for the background
- 1× `<linearGradient>` for the decision diamond fill
- Multiple `<text>` elements with explicit `width` attributes for editable PowerPoint text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="diamondFill" x1="0" y1="210" x2="0" y2="370">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F7FB"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <marker id="arrowBlack" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 12 6 L 0 12 Z" fill="#1F2937"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M -40 620 C 160 540, 220 710, 420 650 C 560 610, 610 700, 780 660 L 780 760 L -40 760 Z"
        fill="#DDEBFF" opacity="0.45"/>
  <path d="M 930 -80 C 1120 -10, 1170 120, 1320 70 L 1320 -90 Z"
        fill="#D7F5E6" opacity="0.55"/>

  <text x="70" y="62" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111827">
    Dynamic Native Flowchart
  </text>
  <text x="72" y="96" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    Connectors terminate at shape edges so the logic remains visually intact when nodes are edited.
  </text>

  <!-- Connector layer: draw all connectors before nodes so white nodes obscure crossing lines -->
  <line x1="640" y1="145" x2="640" y2="222" stroke="#1F2937" stroke-width="2.2" marker-end="url(#arrowBlack)"/>

  <line x1="548" y1="295" x2="450" y2="295" stroke="#1F2937" stroke-width="2.2" marker-end="url(#arrowBlack)"/>
  <line x1="732" y1="295" x2="830" y2="295" stroke="#1F2937" stroke-width="2.2" marker-end="url(#arrowBlack)"/>

  <line x1="410" y1="335" x2="410" y2="390" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="410" y1="390" x2="315" y2="390" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="315" y1="390" x2="315" y2="435" stroke="#1F2937" stroke-width="2.2" marker-end="url(#arrowBlack)"/>

  <line x1="870" y1="335" x2="870" y2="390" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="870" y1="390" x2="965" y2="390" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="965" y1="390" x2="965" y2="435" stroke="#1F2937" stroke-width="2.2" marker-end="url(#arrowBlack)"/>

  <line x1="315" y1="525" x2="315" y2="580" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="315" y1="580" x2="640" y2="580" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="965" y1="525" x2="965" y2="580" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="965" y1="580" x2="640" y2="580" stroke="#1F2937" stroke-width="2.2"/>
  <line x1="640" y1="580" x2="640" y2="622" stroke="#1F2937" stroke-width="2.2" marker-end="url(#arrowBlack)"/>

  <!-- Start node -->
  <rect x="500" y="80" width="280" height="65" rx="16" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="500" y="119" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#111827">
    Start from home
  </text>

  <!-- Decision diamond -->
  <path d="M 640 215 L 740 295 L 640 375 L 540 295 Z" fill="url(#diamondFill)" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="550" y="288" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#111827">
    Before
  </text>
  <text x="550" y="316" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#111827">
    7 AM?
  </text>

  <!-- Semantic branch badges -->
  <ellipse cx="410" cy="295" rx="42" ry="42" fill="#EB5353" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="368" y="302" width="84" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">
    No
  </text>

  <ellipse cx="870" cy="295" rx="42" ry="42" fill="#3CB371" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="828" y="302" width="84" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">
    Yes
  </text>

  <!-- Branch process nodes -->
  <rect x="185" y="435" width="260" height="90" rx="18" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="205" y="471" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#111827">
    Take expressway
  </text>
  <text x="205" y="498" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">
    Higher traffic risk
  </text>

  <rect x="835" y="435" width="260" height="90" rx="18" fill="#FFFFFF" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="855" y="471" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#111827">
    Take shortcut
  </text>
  <text x="855" y="498" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">
    Lower congestion risk
  </text>

  <!-- Converged end node -->
  <rect x="500" y="622" width="280" height="64" rx="16" fill="#111827" stroke="#111827" stroke-width="2" filter="url(#softShadow)"/>
  <text x="500" y="661" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    Arrive at office
  </text>

  <!-- Small caption blocks -->
  <rect x="82" y="632" width="270" height="34" rx="17" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="102" y="654" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    Red branch = negative condition
  </text>

  <rect x="928" y="632" width="270" height="34" rx="17" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="948" y="654" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    Green branch = positive condition
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<path>` connectors with `marker-end`; arrowheads may disappear. Use `<line>` segments and apply `marker-end` directly to the final line segment.
- ❌ Drawing connectors above nodes; overlapping lines will make the flowchart look messy and reduce editability.
- ❌ Using `<g marker-end="...">` to inherit arrowheads; place `marker-end` on each arrow-bearing `<line>` directly.
- ❌ Relying on diagonal freeform connector paths for elbow routing; build elbows from horizontal and vertical native `<line>` segments.
- ❌ Omitting explicit `width` on `<text>`; PowerPoint text boxes need a defined width for reliable rendering.

## Composition notes
- Keep the main decision diamond on the vertical center axis; branch badges should sit horizontally aligned with the diamond midpoint.
- Draw connectors first, then nodes, so white-filled shapes visually “cut” the connector lines at clean connection sites.
- Use semantic color sparingly: red and green should identify branch meaning, while process nodes stay neutral and white.
- Preserve generous negative space around branches so users can move or edit nodes without immediately crowding the diagram.