# SVG Recipe — Diagram with Sidebar

## Visual mechanism
A narrow narrative sidebar anchors the slide on the left while a large, shadowed diagram canvas dominates the right. The right panel can hold a clipped screenshot or architectural image, with editable SVG overlays and a highlighted callout that draws attention to the key insight.

## SVG primitives needed
- 3× `<rect>` for the full-slide background, sidebar panel, and main diagram card
- 1× `<image>` for the primary diagram/screenshot, clipped to a rounded rectangle
- 1× `<clipPath>` with rounded `<rect>` for the diagram image crop
- 2× `<linearGradient>` for the dark background and sidebar surface
- 1× `<radialGradient>` for subtle ambient glow behind the diagram
- 2× `<filter>` definitions: one soft card shadow and one accent glow
- 8× `<line>` for editable network connectors and sidebar separators
- 6× `<circle>` for diagram nodes and status indicators
- 6× `<path>` for decorative blobs, arrowheads, callout notch, and small technical glyphs
- 10× `<text>` with explicit `width` attributes for headline, subtitle, detail copy, labels, and callout text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.55" stop-color="#0E1730"/>
      <stop offset="1" stop-color="#08101D"/>
    </linearGradient>
    <linearGradient id="sideGrad" x1="48" y1="52" x2="376" y2="668" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172642"/>
      <stop offset="1" stop-color="#0F1A2F"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="80" y1="530" x2="314" y2="626" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#31D5FF"/>
      <stop offset="1" stop-color="#7C5CFF"/>
    </linearGradient>
    <radialGradient id="diagramGlow" cx="0.58" cy="0.34" r="0.7">
      <stop offset="0" stop-color="#3DE2FF" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#3DE2FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blueGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <clipPath id="diagramClip">
      <rect x="433" y="78" width="779" height="486" rx="24" ry="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="860" cy="250" r="360" fill="url(#diagramGlow)"/>
  <path d="M1020,38 C1110,6 1227,50 1245,128 C1263,207 1158,239 1080,214 C1000,188 930,70 1020,38 Z" fill="#243B72" opacity="0.22"/>

  <rect x="48" y="52" width="328" height="616" rx="30" fill="url(#sideGrad)" stroke="#2C3B5F" stroke-width="1"/>
  <rect x="48" y="52" width="8" height="616" rx="4" fill="url(#accentGrad)"/>
  <text x="82" y="104" width="248" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2.4" fill="#58D8FF">SYSTEM MAP</text>
  <text x="82" y="166" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#F6FAFF">
    <tspan x="82" dy="0">Diagram with</tspan>
    <tspan x="82" dy="42">executive</tspan>
    <tspan x="82" dy="42">sidebar</tspan>
  </text>
  <text x="82" y="322" width="242" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#AEBBD4">
    <tspan x="82" dy="0">Use the left rail for context,</tspan>
    <tspan x="82" dy="24">decision framing, assumptions,</tspan>
    <tspan x="82" dy="24">or the business implication of</tspan>
    <tspan x="82" dy="24">a dense technical diagram.</tspan>
  </text>
  <line x1="82" y1="438" x2="322" y2="438" stroke="#314263" stroke-width="1"/>
  <circle cx="92" cy="482" r="6" fill="#37D7FF"/>
  <text x="112" y="489" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDE7F5">Primary system boundary</text>
  <circle cx="92" cy="520" r="6" fill="#A882FF"/>
  <text x="112" y="527" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDE7F5">Integration dependencies</text>
  <circle cx="92" cy="558" r="6" fill="#FFCA58"/>
  <text x="112" y="565" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDE7F5">Risk or opportunity zone</text>
  <rect x="82" y="598" width="236" height="40" rx="20" fill="#102844" stroke="#2E9BFF" stroke-width="1"/>
  <text x="106" y="623" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#70DBFF">READ LEFT → RIGHT</text>

  <rect x="415" y="58" width="815" height="604" rx="34" fill="#F8FBFF" filter="url(#softShadow)"/>
  <rect x="433" y="78" width="779" height="486" rx="24" fill="#EAF1FA"/>
  <image x="433" y="78" width="779" height="486" clip-path="url(#diagramClip)" preserveAspectRatio="xMidYMid slice" href="https://images.example.com/technical-cloud-infrastructure-diagram-screenshot.png"/>
  <rect x="433" y="78" width="779" height="486" rx="24" fill="#0A1630" opacity="0.18"/>

  <line x1="592" y1="242" x2="782" y2="170" stroke="#72E5FF" stroke-width="3" opacity="0.85"/>
  <line x1="782" y1="170" x2="973" y2="238" stroke="#72E5FF" stroke-width="3" opacity="0.85"/>
  <line x1="592" y1="242" x2="760" y2="350" stroke="#72E5FF" stroke-width="3" stroke-dasharray="10 8" opacity="0.85"/>
  <line x1="760" y1="350" x2="973" y2="238" stroke="#72E5FF" stroke-width="3" opacity="0.85"/>
  <line x1="973" y1="238" x2="1064" y2="391" stroke="#FFCA58" stroke-width="4" stroke-dasharray="8 7"/>
  <line x1="760" y1="350" x2="1064" y2="391" stroke="#72E5FF" stroke-width="3" opacity="0.85"/>

  <circle cx="592" cy="242" r="35" fill="#142B4D" stroke="#6DE6FF" stroke-width="3"/>
  <path d="M576,241 L589,228 L609,248 L621,236 L621,261 L596,261 L608,249 L589,268 Z" fill="#6DE6FF" opacity="0.95"/>
  <circle cx="782" cy="170" r="38" fill="#18264F" stroke="#A882FF" stroke-width="3"/>
  <path d="M762,172 C762,158 773,147 787,147 C801,147 812,158 812,172 C812,186 801,197 787,197 C773,197 762,186 762,172 Z M776,172 L798,172 M787,161 L787,183" stroke="#CBB9FF" stroke-width="4" fill="none"/>
  <circle cx="973" cy="238" r="42" fill="#12304F" stroke="#37D7FF" stroke-width="3"/>
  <path d="M950,234 L973,215 L997,234 L997,263 L950,263 Z M962,263 L962,244 L985,244 L985,263" fill="#65E4FF"/>
  <circle cx="760" cy="350" r="45" fill="#152B42" stroke="#67F0B2" stroke-width="3"/>
  <path d="M738,350 C738,335 747,326 760,326 C773,326 782,335 782,350 C782,365 773,374 760,374 C747,374 738,365 738,350 Z M727,350 L793,350 M760,317 L760,383" stroke="#7EF2BD" stroke-width="4" fill="none"/>
  <circle cx="1064" cy="391" r="48" fill="#3A2B12" stroke="#FFCA58" stroke-width="4" filter="url(#blueGlow)"/>
  <text x="1035" y="398" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" text-anchor="middle" fill="#FFE7A3">!</text>

  <rect x="458" y="590" width="292" height="44" rx="22" fill="#EFF5FC" stroke="#D6E2F1" stroke-width="1"/>
  <text x="484" y="618" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#253655">Live architecture diagram / editable overlays</text>
  <path d="M820,580 L1174,580 C1197,580 1214,597 1214,620 L1214,628 C1214,646 1200,660 1182,660 L852,660 C834,660 820,646 820,628 Z" fill="#111C33" stroke="#49D8FF" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M852,580 L878,548 L904,580 Z" fill="#111C33" stroke="#49D8FF" stroke-width="2"/>
  <text x="850" y="613" width="322" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Highlight the one dependency that changes the decision.</text>
  <text x="850" y="642" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FDFFF">Keep the callout short; let the diagram carry the evidence.</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to groups, rectangles, or callout shapes; use clipping only on the `<image>` crop.
- ❌ Using a full-slide screenshot without editable overlays; add native lines, nodes, labels, and callouts so the slide remains customizable.
- ❌ Dense sidebar paragraphs that compete with the diagram; the sidebar should summarize, not duplicate the visual.
- ❌ `marker-end` on `<path>` connectors; if arrows are required, use `<line>` plus small editable `<path>` arrowheads.

## Composition notes
- Reserve roughly 25–30% of the slide width for the sidebar and 65–70% for the diagram canvas.
- Keep the sidebar dark and text-led; let the diagram panel be brighter, larger, and more visually detailed.
- Use one accent color consistently across the sidebar stripe, active connectors, and callout border.
- Place the callout inside or just below the diagram area, anchored to a visually meaningful node rather than floating randomly.