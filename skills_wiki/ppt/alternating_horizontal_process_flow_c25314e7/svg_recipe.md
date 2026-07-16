# SVG Recipe — Alternating Process Flow

## Visual mechanism
A horizontal process spine runs across the slide with milestone nodes placed evenly along it; information cards branch alternately above and below the spine to create a zig-zag reading rhythm. Each card uses a dark header plus light body, subtle drop shadow, and short connector line to make the sequence feel structured, premium, and executive-ready.

## SVG primitives needed
- 1× `<rect>` full-slide background using a cool white-to-grey gradient
- 1× `<rect>` top accent bar to anchor the industrial / strategic theme
- 1× `<line>` central horizontal spine with `marker-end` arrowhead
- 6× `<circle>` milestone nodes on the central spine
- 6× `<line>` vertical connector stems from nodes to alternating cards
- 12× `<rect>` card containers: one shadowed white rounded body and one dark header per step
- 6× `<circle>` numbered badges layered on card headers
- 6× `<text>` card headers, 6× `<text>` numbered badges, and 6× `<text>` card body descriptions
- 2× `<path>` decorative background arcs / industrial geometry accents
- 1× `<filter id="cardShadow">` applied to the white card bodies
- 1× `<linearGradient id="bgGrad">` for the background
- 1× `<radialGradient id="nodeGrad">` for raised milestone nodes
- 1× `<marker id="arrowHead">` for the central spine arrowhead, applied directly to the `<line>`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f2f6f7"/>
    </linearGradient>
    <radialGradient id="nodeGrad" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="38%" stop-color="#d9edf1"/>
      <stop offset="100%" stop-color="#264048"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrowHead" markerWidth="14" markerHeight="14" refX="12" refY="7" orient="auto">
      <path d="M2,2 L12,7 L2,12 Z" fill="#6f8f9a"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="10" fill="#264048"/>
  <path d="M850 72 C970 10 1110 28 1214 138 C1270 198 1288 282 1232 345" fill="none" stroke="#d9e5e8" stroke-width="3"/>
  <path d="M48 640 C210 590 332 640 480 604 C584 578 670 520 804 548" fill="none" stroke="#e2ebee" stroke-width="4"/>

  <text x="70" y="62" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#264048">Manufacturing Roadmap: From Plan to Scale</text>
  <text x="70" y="100" width="900" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#65777e">Six alternating workstreams show how production moves from early planning through commercial launch while preserving enough space for detailed notes.</text>

  <line x1="86" y1="395" x2="1196" y2="395" stroke="#9fb4be" stroke-width="5" stroke-linecap="round" marker-end="url(#arrowHead)"/>
  <text x="1032" y="378" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#6f8f9a">TIME</text>

  <!-- Step 1: top -->
  <line x1="150" y1="395" x2="150" y2="332" stroke="#9fb4be" stroke-width="2.5" stroke-dasharray="5 6"/>
  <circle cx="150" cy="395" r="18" fill="url(#nodeGrad)" stroke="#264048" stroke-width="3"/>
  <rect x="60" y="178" width="180" height="154" rx="16" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="60" y="178" width="180" height="48" rx="16" fill="#264048"/>
  <rect x="60" y="210" width="180" height="20" fill="#264048"/>
  <circle cx="86" cy="202" r="18" fill="#7ec9d4"/>
  <text x="78" y="208" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">1</text>
  <text x="112" y="208" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">Plan Demand</text>
  <text x="78" y="254" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#44555b">
    <tspan x="78" dy="0">• Forecast capacity</tspan>
    <tspan x="78" dy="20">• Lock supply inputs</tspan>
    <tspan x="78" dy="20">• Confirm budget gates</tspan>
  </text>

  <!-- Step 2: bottom -->
  <line x1="330" y1="395" x2="330" y2="455" stroke="#9fb4be" stroke-width="2.5" stroke-dasharray="5 6"/>
  <circle cx="330" cy="395" r="18" fill="url(#nodeGrad)" stroke="#264048" stroke-width="3"/>
  <rect x="240" y="455" width="180" height="154" rx="16" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="240" y="455" width="180" height="48" rx="16" fill="#264048"/>
  <rect x="240" y="487" width="180" height="20" fill="#264048"/>
  <circle cx="266" cy="479" r="18" fill="#7ec9d4"/>
  <text x="258" y="485" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">2</text>
  <text x="292" y="485" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">Design Line</text>
  <text x="258" y="531" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#44555b">
    <tspan x="258" dy="0">• Map process cells</tspan>
    <tspan x="258" dy="20">• Specify tooling</tspan>
    <tspan x="258" dy="20">• Model cycle time</tspan>
  </text>

  <!-- Step 3: top -->
  <line x1="510" y1="395" x2="510" y2="332" stroke="#9fb4be" stroke-width="2.5" stroke-dasharray="5 6"/>
  <circle cx="510" cy="395" r="18" fill="url(#nodeGrad)" stroke="#264048" stroke-width="3"/>
  <rect x="420" y="178" width="180" height="154" rx="16" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="420" y="178" width="180" height="48" rx="16" fill="#264048"/>
  <rect x="420" y="210" width="180" height="20" fill="#264048"/>
  <circle cx="446" cy="202" r="18" fill="#7ec9d4"/>
  <text x="438" y="208" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">3</text>
  <text x="472" y="208" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">Prototype</text>
  <text x="438" y="254" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#44555b">
    <tspan x="438" dy="0">• Build pilot batch</tspan>
    <tspan x="438" dy="20">• Capture defects</tspan>
    <tspan x="438" dy="20">• Tune parameters</tspan>
  </text>

  <!-- Step 4: bottom -->
  <line x1="690" y1="395" x2="690" y2="455" stroke="#9fb4be" stroke-width="2.5" stroke-dasharray="5 6"/>
  <circle cx="690" cy="395" r="18" fill="url(#nodeGrad)" stroke="#264048" stroke-width="3"/>
  <rect x="600" y="455" width="180" height="154" rx="16" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="600" y="455" width="180" height="48" rx="16" fill="#264048"/>
  <rect x="600" y="487" width="180" height="20" fill="#264048"/>
  <circle cx="626" cy="479" r="18" fill="#7ec9d4"/>
  <text x="618" y="485" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">4</text>
  <text x="652" y="485" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">Validate</text>
  <text x="618" y="531" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#44555b">
    <tspan x="618" dy="0">• Run quality checks</tspan>
    <tspan x="618" dy="20">• Certify safety</tspan>
    <tspan x="618" dy="20">• Approve SOPs</tspan>
  </text>

  <!-- Step 5: top -->
  <line x1="870" y1="395" x2="870" y2="332" stroke="#9fb4be" stroke-width="2.5" stroke-dasharray="5 6"/>
  <circle cx="870" cy="395" r="18" fill="url(#nodeGrad)" stroke="#264048" stroke-width="3"/>
  <rect x="780" y="178" width="180" height="154" rx="16" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="780" y="178" width="180" height="48" rx="16" fill="#264048"/>
  <rect x="780" y="210" width="180" height="20" fill="#264048"/>
  <circle cx="806" cy="202" r="18" fill="#7ec9d4"/>
  <text x="798" y="208" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">5</text>
  <text x="832" y="208" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">Ramp Output</text>
  <text x="798" y="254" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#44555b">
    <tspan x="798" dy="0">• Train operators</tspan>
    <tspan x="798" dy="20">• Balance shifts</tspan>
    <tspan x="798" dy="20">• Stabilize yield</tspan>
  </text>

  <!-- Step 6: bottom -->
  <line x1="1050" y1="395" x2="1050" y2="455" stroke="#9fb4be" stroke-width="2.5" stroke-dasharray="5 6"/>
  <circle cx="1050" cy="395" r="18" fill="url(#nodeGrad)" stroke="#264048" stroke-width="3"/>
  <rect x="960" y="455" width="180" height="154" rx="16" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="960" y="455" width="180" height="48" rx="16" fill="#264048"/>
  <rect x="960" y="487" width="180" height="20" fill="#264048"/>
  <circle cx="986" cy="479" r="18" fill="#7ec9d4"/>
  <text x="978" y="485" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">6</text>
  <text x="1012" y="485" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">Launch</text>
  <text x="978" y="531" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#44555b">
    <tspan x="978" dy="0">• Release inventory</tspan>
    <tspan x="978" dy="20">• Monitor service</tspan>
    <tspan x="978" dy="20">• Report ROI</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path marker-end="...">` for the main arrow spine; arrowheads on paths may disappear. Use a `<line>` with `marker-end` applied directly.
- ❌ Do not put shadows on connector `<line>` elements; filters on lines are silently dropped. Apply shadows only to card `<rect>` elements.
- ❌ Do not compress cards into a uniform grid; the technique depends on the alternating up/down rhythm around the central spine.
- ❌ Do not use clip paths on card rectangles or groups; only use `clip-path` on `<image>` if adding a themed photo.
- ❌ Do not omit `width` on text elements; PowerPoint translation needs explicit text widths for clean editable rendering.

## Composition notes
- Keep the spine around 52–57% of slide height so upper cards fit beneath the title and lower cards do not collide with the bottom margin.
- Use 4–7 steps maximum; beyond 7, reduce body text or switch to a two-row roadmap.
- Alternate cards strictly above / below the spine, but keep all card widths identical for a disciplined consulting-slide feel.
- Use one dark structural color for headers, nodes, and title; reserve a brighter accent only for numbered badges or selected milestone emphasis.