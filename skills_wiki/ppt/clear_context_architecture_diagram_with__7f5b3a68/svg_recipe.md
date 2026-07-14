# SVG Recipe — Clear-Context Architecture Diagram with Grouping & Legends

## Visual mechanism
A complex system is made legible by placing editable architecture nodes inside dashed contextual zones, then connecting them with clean orthogonal flows and semantic labels. A compact legend decodes shape meanings, line styles, and alert colors so non-technical viewers can follow the story without needing the presenter to explain every symbol.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 3× dashed rounded `<rect>` for contextual grouping boundaries
- 6× filled rounded `<rect>` for process/service nodes
- 2× database cylinder groups made from `<rect>`, `<ellipse>`, and `<path>`
- 1× decision diamond made from `<path>`
- 10× `<line>` for straight connector segments with arrowheads applied directly
- 6× small `<path>` icons inside nodes and legend items
- 1× `<filter id="softShadow">` applied to nodes and legend panel
- 1× `<linearGradient>` for premium node fills
- 1× `<radialGradient>` for subtle background emphasis
- Multiple `<text>` elements with explicit `width` attributes for titles, node labels, connector labels, zone captions, and legend text
- 1× `<marker>` in `<defs>` used only on `<line>` connectors

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="nodeFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="100%" stop-color="#E3EEF8"/>
    </linearGradient>
    <linearGradient id="accentFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EEF7FF"/>
      <stop offset="100%" stop-color="#D6E9FA"/>
    </linearGradient>
    <radialGradient id="bgGlow" cx="48%" cy="38%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F7FB"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrowBlue" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#2F5D8C"/>
    </marker>
    <marker id="arrowRed" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#D94A4A"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <text x="54" y="56" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#1E2A36">Story-Driven Reference Architecture</text>
  <text x="56" y="88" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#657487">Grouping boundaries, standard shapes, and an explicit legend reduce cognitive load.</text>

  <rect x="54" y="128" width="295" height="380" rx="24" fill="none" stroke="#AEB9C5" stroke-width="2.5" stroke-dasharray="10 8"/>
  <text x="78" y="158" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#71808F">SOURCE SYSTEMS</text>

  <rect x="394" y="128" width="464" height="380" rx="24" fill="none" stroke="#AEB9C5" stroke-width="2.5" stroke-dasharray="10 8"/>
  <text x="418" y="158" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#71808F">CORE PROCESSING GROUP</text>

  <rect x="902" y="128" width="324" height="380" rx="24" fill="none" stroke="#AEB9C5" stroke-width="2.5" stroke-dasharray="10 8"/>
  <text x="926" y="158" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#71808F">SERVING & OBSERVABILITY</text>

  <g filter="url(#softShadow)">
    <rect x="98" y="205" width="178" height="82" rx="18" fill="url(#nodeFill)" stroke="#2F5D8C" stroke-width="2"/>
    <path d="M125 246 h24 v-24 h-24 z M154 222 h24 v24 h-24 z M183 222 h24 v24 h-24 z M125 252 h82 v10 h-82 z" fill="#7DA9D4"/>
    <text x="118" y="276" width="138" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">CRM + Orders</text>
  </g>

  <g filter="url(#softShadow)">
    <rect x="116" y="360" width="142" height="74" fill="#E6F1FA" stroke="#2F5D8C" stroke-width="2"/>
    <ellipse cx="187" cy="360" rx="71" ry="18" fill="#F7FBFF" stroke="#2F5D8C" stroke-width="2"/>
    <path d="M116 360 C116 384 258 384 258 360" fill="none" stroke="#2F5D8C" stroke-width="2"/>
    <ellipse cx="187" cy="434" rx="71" ry="18" fill="#DDECF8" stroke="#2F5D8C" stroke-width="2"/>
    <text x="137" y="405" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Data Lake</text>
  </g>

  <g filter="url(#softShadow)">
    <rect x="434" y="218" width="168" height="86" rx="18" fill="url(#accentFill)" stroke="#2F5D8C" stroke-width="2"/>
    <path d="M474 262 C486 238 510 238 522 262 C534 238 558 238 570 262" fill="none" stroke="#7DA9D4" stroke-width="5" stroke-linecap="round"/>
    <text x="458" y="290" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Event Bus</text>
  </g>

  <g filter="url(#softShadow)">
    <path d="M682 196 L766 263 L682 330 L598 263 Z" fill="#FFF7E6" stroke="#B77E22" stroke-width="2.5"/>
    <text x="626" y="258" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Policy</text>
    <text x="626" y="277" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Decision?</text>
  </g>

  <g filter="url(#softShadow)">
    <rect x="458" y="386" width="160" height="76" rx="18" fill="url(#nodeFill)" stroke="#2F5D8C" stroke-width="2"/>
    <path d="M496 424 l28 -22 l28 22 l-28 22 z" fill="#7DA9D4"/>
    <text x="478" y="453" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Scoring Model</text>
  </g>

  <g filter="url(#softShadow)">
    <rect x="694" y="386" width="132" height="76" fill="#E6F1FA" stroke="#2F5D8C" stroke-width="2"/>
    <ellipse cx="760" cy="386" rx="66" ry="16" fill="#F7FBFF" stroke="#2F5D8C" stroke-width="2"/>
    <ellipse cx="760" cy="462" rx="66" ry="16" fill="#DDECF8" stroke="#2F5D8C" stroke-width="2"/>
    <text x="714" y="429" width="92" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Rules DB</text>
  </g>

  <g filter="url(#softShadow)">
    <rect x="956" y="222" width="176" height="82" rx="18" fill="url(#nodeFill)" stroke="#2F5D8C" stroke-width="2"/>
    <path d="M1004 264 h80 M1044 224 v80 M1018 244 l-14 20 l14 20 M1070 244 l14 20 l-14 20" fill="none" stroke="#7DA9D4" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="984" y="292" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">API Gateway</text>
  </g>

  <g filter="url(#softShadow)">
    <rect x="956" y="382" width="176" height="82" rx="18" fill="#FFF1F1" stroke="#D94A4A" stroke-width="2"/>
    <path d="M1030 402 h28 l-6 36 h-16 z M1034 448 h20" fill="#F06B6B"/>
    <text x="982" y="454" width="124" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E2A36">Manual Review</text>
  </g>

  <line x1="276" y1="246" x2="434" y2="246" stroke="#2F5D8C" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <line x1="258" y1="397" x2="458" y2="424" stroke="#2F5D8C" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <line x1="602" y1="263" x2="598" y2="263" stroke="#2F5D8C" stroke-width="2.5"/>
  <line x1="602" y1="263" x2="598" y2="263" stroke="#2F5D8C" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <line x1="682" y1="330" x2="682" y2="424" stroke="#2F5D8C" stroke-width="2.5"/>
  <line x1="682" y1="424" x2="694" y2="424" stroke="#2F5D8C" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <line x1="766" y1="263" x2="956" y2="263" stroke="#2F5D8C" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
  <line x1="682" y1="196" x2="682" y2="178" stroke="#D94A4A" stroke-width="2.5"/>
  <line x1="682" y1="178" x2="1044" y2="178" stroke="#D94A4A" stroke-width="2.5"/>
  <line x1="1044" y1="178" x2="1044" y2="382" stroke="#D94A4A" stroke-width="2.5" marker-end="url(#arrowRed)"/>

  <text x="326" y="232" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-style="italic" fill="#2F5D8C">events</text>
  <text x="704" y="361" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-style="italic" fill="#2F5D8C">lookup</text>
  <text x="828" y="247" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-style="italic" fill="#2F5D8C">approved</text>
  <text x="864" y="164" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-style="italic" fill="#D94A4A">exception path</text>

  <g filter="url(#softShadow)">
    <rect x="88" y="560" width="1104" height="92" rx="22" fill="#FFFFFF" stroke="#DDE5ED"/>
  </g>
  <text x="116" y="594" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1E2A36">Legend</text>
  <rect x="220" y="574" width="56" height="34" rx="9" fill="url(#nodeFill)" stroke="#2F5D8C" stroke-width="1.6"/>
  <text x="288" y="596" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#435466">Process / service</text>
  <path d="M478 572 L512 591 L478 610 L444 591 Z" fill="#FFF7E6" stroke="#B77E22" stroke-width="1.6"/>
  <text x="526" y="596" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#435466">Decision point</text>
  <ellipse cx="690" cy="578" rx="33" ry="9" fill="#F7FBFF" stroke="#2F5D8C" stroke-width="1.5"/>
  <rect x="657" y="578" width="66" height="26" fill="#E6F1FA" stroke="#2F5D8C" stroke-width="1.5"/>
  <ellipse cx="690" cy="604" rx="33" ry="9" fill="#DDECF8" stroke="#2F5D8C" stroke-width="1.5"/>
  <text x="738" y="596" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#435466">Data store</text>
  <line x1="874" y1="590" x2="940" y2="590" stroke="#2F5D8C" stroke-width="2.2" marker-end="url(#arrowBlue)"/>
  <text x="952" y="596" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#435466">Primary flow</text>
  <line x1="1070" y1="590" x2="1136" y2="590" stroke="#D94A4A" stroke-width="2.2" marker-end="url(#arrowRed)"/>
  <text x="1146" y="596" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#435466">Exception</text>
</svg>
```

## Avoid in this skill
- ❌ Unlabeled box-and-arrow diagrams with no grouping zones; the technique depends on context boundaries.
- ❌ Connectors drawn as complex `<path>` arrows with `marker-end`; use `<line>` segments and apply `marker-end` directly to each line.
- ❌ Applying filters to connector lines; shadows should be reserved for nodes, panels, and major containers.
- ❌ Dense crossing connectors; route flows orthogonally with generous whitespace and label decision branches.
- ❌ Legends that use different miniature symbols than the diagram itself; the legend must visually match the actual node language.

## Composition notes
- Keep the main story left-to-right: sources on the left, processing in the center, serving/exception outcomes on the right.
- Use dashed rounded rectangles as quiet “context containers”; draw them behind nodes and give them enough padding so they read as zones, not decoration.
- Reserve the bottom 15–18% of the slide for a legend strip; this makes the diagram self-explanatory for executives and mixed audiences.
- Use one calm primary color for normal architecture flow and one semantic alert color for exceptions, failures, or manual review paths.