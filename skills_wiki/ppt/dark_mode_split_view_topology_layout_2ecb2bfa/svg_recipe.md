# SVG Recipe — Dark Mode Split-View Topology Layout

## Visual mechanism
A premium developer-dark canvas is split into three zones: a left vertical navigation rail, a floating code-editor panel, and a right-side topology output diagram. The visual story comes from placing syntax-highlighted code beside the architecture it generates, with neon accents, soft glows, and high-contrast dark surfaces.

## SVG primitives needed
- 1× `<rect>` for the full dark charcoal slide background
- 1× `<path>` for a subtle radial/neon ambience blob behind the topology area
- 5× `<rect>` for pill-shaped sidebar navigation items
- 1× `<rect>` for the active navigation accent pill
- 1× `<rect>` for the floating terminal/editor body with shadow
- 1× `<rect>` for the terminal title bar
- 3× `<circle>` for terminal traffic-light buttons
- Multiple `<text>` blocks with explicit `width` for nav labels, title, code, annotations, and node labels
- Multiple `<tspan>` elements inside code `<text>` blocks for syntax highlighting
- 4× `<rect>` for topology service cards/nodes
- 4× `<circle>` for node icons and small status accents
- Several `<line>` elements for diagram connectors
- Several small `<path>` triangles for arrowheads, avoiding fragile path markers
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` for floating panels
- 1× `<filter id="neonGlow">` using `feGaussianBlur` for accent glows
- 2× `<linearGradient>` fills for active UI elements and diagram nodes
- 1× `<radialGradient>` for the background glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="purpleAccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#9D4EDD"/>
      <stop offset="100%" stop-color="#5A2BEF"/>
    </linearGradient>
    <linearGradient id="nodeFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#202436"/>
      <stop offset="100%" stop-color="#11131D"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#7B2FF7" stop-opacity="0.32"/>
      <stop offset="48%" stop-color="#00D4FF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#262629" stop-opacity="0"/>
    </radialGradient>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neonGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#262629"/>
  <path d="M680,92 C818,34 1066,40 1190,178 C1324,328 1240,579 1048,654 C862,727 659,634 614,476 C569,318 538,151 680,92 Z" fill="url(#ambientGlow)"/>

  <text x="52" y="72" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#F3F3F5">Topology Lab</text>
  <text x="52" y="101" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8C8C96">code → architecture</text>

  <rect x="42" y="154" width="176" height="48" rx="24" fill="#3C3C41"/>
  <text x="70" y="184" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#A6A6AF">Diagrams</text>
  <rect x="42" y="218" width="176" height="48" rx="24" fill="url(#purpleAccent)" filter="url(#neonGlow)"/>
  <rect x="42" y="218" width="176" height="48" rx="24" fill="url(#purpleAccent)"/>
  <text x="70" y="248" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Go diagrams</text>
  <rect x="42" y="282" width="176" height="48" rx="24" fill="#3C3C41"/>
  <text x="70" y="312" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#A6A6AF">Mermaid</text>
  <rect x="42" y="346" width="176" height="48" rx="24" fill="#3C3C41"/>
  <text x="70" y="376" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#A6A6AF">PlantUML</text>
  <rect x="42" y="410" width="176" height="48" rx="24" fill="#3C3C41"/>
  <text x="70" y="440" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#A6A6AF">ASCII editors</text>

  <rect x="270" y="88" width="430" height="556" rx="22" fill="#0F0F10" filter="url(#panelShadow)"/>
  <rect x="270" y="88" width="430" height="56" rx="22" fill="#18191D"/>
  <rect x="270" y="122" width="430" height="22" fill="#18191D"/>
  <circle cx="302" cy="116" r="7" fill="#FF5F57"/>
  <circle cx="326" cy="116" r="7" fill="#FFBD2E"/>
  <circle cx="350" cy="116" r="7" fill="#28C840"/>
  <text x="382" y="121" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8B8B95">infra/web_services.go</text>

  <text x="302" y="180" width="365" font-family="Consolas, Courier New, monospace" font-size="16" fill="#B8B8C0">
    <tspan x="302" dy="0" fill="#C678DD">package</tspan><tspan fill="#E6E6E8"> main</tspan>
    <tspan x="302" dy="30" fill="#C678DD">func</tspan><tspan fill="#61AFEF"> BuildTopology</tspan><tspan fill="#E6E6E8">() {</tspan>
    <tspan x="326" dy="30" fill="#E5C07B">dns</tspan><tspan fill="#E6E6E8"> := Route53(</tspan><tspan fill="#98C379">"dns"</tspan><tspan fill="#E6E6E8">)</tspan>
    <tspan x="326" dy="30" fill="#E5C07B">edge</tspan><tspan fill="#E6E6E8"> := CloudFront(</tspan><tspan fill="#98C379">"edge"</tspan><tspan fill="#E6E6E8">)</tspan>
    <tspan x="326" dy="30" fill="#E5C07B">api</tspan><tspan fill="#E6E6E8"> := Lambda(</tspan><tspan fill="#98C379">"api"</tspan><tspan fill="#E6E6E8">)</tspan>
    <tspan x="326" dy="30" fill="#E5C07B">db</tspan><tspan fill="#E6E6E8"> := DynamoDB(</tspan><tspan fill="#98C379">"state"</tspan><tspan fill="#E6E6E8">)</tspan>
    <tspan x="326" dy="42" fill="#ABB2BF">dns</tspan><tspan fill="#56B6C2"> &gt;&gt; </tspan><tspan fill="#ABB2BF">edge</tspan><tspan fill="#56B6C2"> &gt;&gt; </tspan><tspan fill="#ABB2BF">api</tspan><tspan fill="#56B6C2"> &gt;&gt; </tspan><tspan fill="#ABB2BF">db</tspan>
    <tspan x="302" dy="30" fill="#E6E6E8">}</tspan>
  </text>

  <rect x="302" y="534" width="354" height="66" rx="14" fill="#171922" stroke="#2C2E3A"/>
  <circle cx="328" cy="567" r="9" fill="#2ECC71" filter="url(#neonGlow)"/>
  <circle cx="328" cy="567" r="5" fill="#2ECC71"/>
  <text x="350" y="561" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#F4F4F6">Preview compiled successfully</text>
  <text x="350" y="584" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8E929D">4 resources · 3 directed edges · 0 warnings</text>

  <text x="752" y="100" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Generated service topology</text>
  <text x="754" y="130" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A7A7B1">Live architecture output rendered from the code block.</text>

  <rect x="766" y="178" width="168" height="92" rx="18" fill="url(#nodeFill)" stroke="#7B2FF7" stroke-width="1.5" filter="url(#panelShadow)"/>
  <circle cx="804" cy="224" r="19" fill="#7B2FF7"/>
  <path d="M793,225 C799,211 816,211 821,225 C814,220 801,220 793,225 Z" fill="#FFFFFF"/>
  <text x="834" y="218" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Route53</text>
  <text x="834" y="240" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA2AF">dns</text>

  <rect x="1000" y="178" width="168" height="92" rx="18" fill="url(#nodeFill)" stroke="#00D4FF" stroke-width="1.5" filter="url(#panelShadow)"/>
  <circle cx="1038" cy="224" r="19" fill="#00D4FF"/>
  <path d="M1026,224 L1038,211 L1050,224 L1038,237 Z" fill="#071019"/>
  <text x="1068" y="218" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">CloudFront</text>
  <text x="1068" y="240" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA2AF">edge</text>

  <rect x="766" y="396" width="168" height="92" rx="18" fill="url(#nodeFill)" stroke="#FFB000" stroke-width="1.5" filter="url(#panelShadow)"/>
  <circle cx="804" cy="442" r="19" fill="#FFB000"/>
  <path d="M797,430 L814,442 L797,454 Z" fill="#17120A"/>
  <text x="834" y="436" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Lambda</text>
  <text x="834" y="458" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA2AF">api</text>

  <rect x="1000" y="396" width="168" height="92" rx="18" fill="url(#nodeFill)" stroke="#2ECC71" stroke-width="1.5" filter="url(#panelShadow)"/>
  <circle cx="1038" cy="442" r="19" fill="#2ECC71"/>
  <path d="M1026,435 C1026,426 1050,426 1050,435 L1050,450 C1050,459 1026,459 1026,450 Z" fill="#07140D"/>
  <text x="1068" y="436" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">DynamoDB</text>
  <text x="1068" y="458" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA2AF">state</text>

  <line x1="934" y1="224" x2="991" y2="224" stroke="#7C8194" stroke-width="2.4"/>
  <path d="M991,224 L980,218 L980,230 Z" fill="#7C8194"/>
  <line x1="1084" y1="270" x2="1084" y2="388" stroke="#7C8194" stroke-width="2.4" stroke-dasharray="7 7"/>
  <path d="M1084,388 L1078,377 L1090,377 Z" fill="#7C8194"/>
  <line x1="1000" y1="442" x2="943" y2="442" stroke="#7C8194" stroke-width="2.4"/>
  <path d="M943,442 L954,436 L954,448 Z" fill="#7C8194"/>
  <line x1="850" y1="270" x2="850" y2="388" stroke="#7C8194" stroke-width="2.4" stroke-dasharray="7 7"/>
  <path d="M850,388 L844,377 L856,377 Z" fill="#7C8194"/>

  <rect x="756" y="558" width="420" height="48" rx="24" fill="#171922" stroke="#303341"/>
  <text x="782" y="588" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#C6C8D2">Directed edges mirror the operator chain in the source file.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path marker-end="...">` for arrows; draw connectors with `<line>` plus small editable `<path>` triangle arrowheads.
- ❌ Do not omit `width` on code or navigation `<text>` elements; terminal layouts depend on fixed text boxes.
- ❌ Do not apply filters to `<line>` connectors; use glow/shadow only on panels, nodes, icons, or text.
- ❌ Do not overfill the topology area with too many nodes; the split-view concept needs breathing room and clear code-to-output correspondence.
- ❌ Do not use `<foreignObject>` for code blocks; build syntax highlighting with native `<text>` and nested `<tspan>`.

## Composition notes
- Keep the left navigation rail narrow, around 15–18% of the canvas, so it reads as product UI rather than main content.
- The terminal should occupy the visual center-left and feel like a floating IDE window, with a deep black fill and soft shadow.
- Reserve the right half for the topology output; use fewer, larger nodes with generous spacing instead of a dense system map.
- Use one dominant neon accent for active navigation, then secondary accents on diagram nodes to create a polished developer-tool color rhythm.