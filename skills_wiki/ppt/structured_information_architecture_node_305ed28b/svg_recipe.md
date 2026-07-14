# SVG Recipe — Structured Information Architecture (Node-Based Hierarchy Diagram)

## Visual mechanism
Transform dense bullet information into a spatial logic tree: one dominant root node branches into category nodes, then into lightweight detail nodes. Use strict alignment, color-coded hierarchy, thin connectors, and subtle shadows to make relationships instantly scannable while retaining an executive keynote feel.

## SVG primitives needed
- 1× `<rect>` for the dark slide background
- 4× large blurred `<path>` shapes for premium powder-like atmospheric color fields
- 1× `<text>` title group using nested `<tspan>` for mixed Chinese/Latin headline styling
- 1× `<rect>` for the root node
- 3× `<rect>` for level-2 category nodes
- 7× `<rect>` for level-3 detail nodes
- 16× `<line>` for editable hierarchy connectors and elbow joints
- 7× small `<circle>` anchor dots at branch junctions
- 1× `<linearGradient>` for the root node fill
- 3× `<linearGradient>` / `<radialGradient>` fills for background glow and accent nodes
- 1× `<filter id="softShadow">` applied to node rectangles
- 1× `<filter id="powderBlur">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="rootGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A3768"/>
      <stop offset="100%" stop-color="#07182F"/>
    </linearGradient>

    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D5FF"/>
      <stop offset="100%" stop-color="#0077B6"/>
    </linearGradient>

    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFB347"/>
      <stop offset="100%" stop-color="#E85D04"/>
    </linearGradient>

    <radialGradient id="tealPowder" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.42"/>
      <stop offset="65%" stop-color="#008FA3" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="amberPowder" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#FFB000" stop-opacity="0.36"/>
      <stop offset="70%" stop-color="#B13A00" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .28 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="powderBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#05070B"/>

  <path d="M-40,5 C120,-40 240,10 325,95 C405,176 395,285 305,345 C190,423 58,345 -20,260 Z"
        fill="url(#amberPowder)" filter="url(#powderBlur)"/>
  <path d="M500,90 C650,12 760,80 805,210 C855,352 755,460 615,450 C470,440 390,300 430,185 Z"
        fill="url(#tealPowder)" filter="url(#powderBlur)"/>
  <path d="M795,305 C930,225 1085,265 1130,390 C1188,552 1030,632 875,585 C735,542 690,395 795,305 Z"
        fill="url(#tealPowder)" filter="url(#powderBlur)"/>
  <path d="M160,520 C285,455 390,470 455,550 C510,620 440,695 292,690 C145,684 60,610 160,520 Z"
        fill="#7A1E00" opacity="0.20" filter="url(#powderBlur)"/>

  <text x="72" y="76" width="620" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF">
    <tspan x="72" dy="0" font-size="22" font-weight="400" opacity="0.72">内容要清晰</tspan>
    <tspan x="72" dy="46" font-size="38" font-weight="800">PPT结构化思维</tspan>
  </text>

  <text x="900" y="86" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#B8C7D9" text-anchor="start">
    从“文字堆叠”到“空间化架构”
  </text>

  <!-- connectors: root to category trunk -->
  <line x1="274" y1="360" x2="352" y2="360" stroke="#6F849E" stroke-width="2"/>
  <line x1="352" y1="228" x2="352" y2="492" stroke="#6F849E" stroke-width="2"/>
  <line x1="352" y1="228" x2="438" y2="228" stroke="#6F849E" stroke-width="2"/>
  <line x1="352" y1="360" x2="438" y2="360" stroke="#6F849E" stroke-width="2"/>
  <line x1="352" y1="492" x2="438" y2="492" stroke="#6F849E" stroke-width="2"/>

  <!-- connectors: category to details -->
  <line x1="642" y1="228" x2="712" y2="228" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="188" x2="712" y2="268" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="188" x2="760" y2="188" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="268" x2="760" y2="268" stroke="#4F657C" stroke-width="2"/>

  <line x1="642" y1="360" x2="712" y2="360" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="320" x2="712" y2="400" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="320" x2="760" y2="320" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="400" x2="760" y2="400" stroke="#4F657C" stroke-width="2"/>

  <line x1="642" y1="492" x2="712" y2="492" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="452" x2="712" y2="532" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="452" x2="760" y2="452" stroke="#4F657C" stroke-width="2"/>
  <line x1="712" y1="532" x2="760" y2="532" stroke="#4F657C" stroke-width="2"/>

  <circle cx="352" cy="228" r="5" fill="#00D5FF"/>
  <circle cx="352" cy="360" r="5" fill="#00D5FF"/>
  <circle cx="352" cy="492" r="5" fill="#00D5FF"/>
  <circle cx="712" cy="188" r="4" fill="#B8C7D9"/>
  <circle cx="712" cy="320" r="4" fill="#B8C7D9"/>
  <circle cx="712" cy="452" r="4" fill="#B8C7D9"/>
  <circle cx="712" cy="532" r="4" fill="#B8C7D9"/>

  <!-- root node -->
  <rect x="92" y="294" width="182" height="132" rx="28" fill="url(#rootGrad)" filter="url(#softShadow)"/>
  <text x="122" y="340" width="122" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF" text-anchor="middle">
    <tspan x="183" font-size="18" font-weight="400" opacity="0.78">Root</tspan>
    <tspan x="183" dy="34" font-size="24" font-weight="800">核心目标</tspan>
  </text>

  <!-- level 2 category nodes -->
  <rect x="438" y="180" width="204" height="96" rx="22" fill="url(#cyanGrad)" filter="url(#softShadow)"/>
  <text x="466" y="220" width="148" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF" text-anchor="middle">
    <tspan x="540" font-size="19" font-weight="800">战略层</tspan>
    <tspan x="540" dy="25" font-size="13" opacity="0.82">Why / Direction</tspan>
  </text>

  <rect x="438" y="312" width="204" height="96" rx="22" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <text x="466" y="352" width="148" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF" text-anchor="middle">
    <tspan x="540" font-size="19" font-weight="800">结构层</tspan>
    <tspan x="540" dy="25" font-size="13" opacity="0.82">How / Modules</tspan>
  </text>

  <rect x="438" y="444" width="204" height="96" rx="22" fill="#20354F" filter="url(#softShadow)"/>
  <text x="466" y="484" width="148" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF" text-anchor="middle">
    <tspan x="540" font-size="19" font-weight="800">执行层</tspan>
    <tspan x="540" dy="25" font-size="13" opacity="0.82">What / Actions</tspan>
  </text>

  <!-- level 3 detail nodes -->
  <rect x="760" y="154" width="192" height="68" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="784" y="194" width="144" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#18304E" text-anchor="middle">用户价值主张</text>

  <rect x="760" y="234" width="192" height="68" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="784" y="274" width="144" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#18304E" text-anchor="middle">商业优先级</text>

  <rect x="760" y="286" width="192" height="68" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="784" y="326" width="144" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#18304E" text-anchor="middle">模块分组</text>

  <rect x="760" y="366" width="192" height="68" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="784" y="406" width="144" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#18304E" text-anchor="middle">逻辑顺序</text>

  <rect x="760" y="418" width="192" height="68" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="784" y="458" width="144" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#18304E" text-anchor="middle">关键任务</text>

  <rect x="760" y="498" width="192" height="68" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="784" y="538" width="144" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#18304E" text-anchor="middle">度量指标</text>

  <rect x="994" y="286" width="178" height="148" rx="24" fill="#0E1724" stroke="#2D435E" stroke-width="1.5" filter="url(#softShadow)"/>
  <text x="1022" y="326" width="122" font-family="Segoe UI, Microsoft YaHei" fill="#FFFFFF" text-anchor="middle">
    <tspan x="1083" font-size="16" font-weight="800">输出结果</tspan>
    <tspan x="1083" dy="30" font-size="13" opacity="0.72">清晰结论</tspan>
    <tspan x="1083" dy="23" font-size="13" opacity="0.72">可执行路径</tspan>
    <tspan x="1083" dy="23" font-size="13" opacity="0.72">一致叙事</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Avoid SmartArt-like `<use>` duplication; duplicate each node explicitly so PowerPoint receives fully editable independent shapes.
- ❌ Avoid `marker-end` arrowheads on `<path>` connectors; use plain `<line>` connectors or separate small triangle paths if arrows are essential.
- ❌ Avoid putting filters on connector lines; shadows on lines are dropped, so keep connectors thin and clean.
- ❌ Avoid auto-sized text assumptions; every `<text>` must include an explicit `width` so labels do not reflow unpredictably in PowerPoint.
- ❌ Avoid overloading each node with long sentences; the diagram works best when nodes contain compact noun phrases.

## Composition notes
- Keep the hierarchy inside the central 80% of the canvas, with a strong root node on the left and increasingly lighter detail nodes toward the right.
- Use hierarchy-driven color: dark/navy for the root, saturated accents for level 2, white or outline cards for level 3.
- Let connectors be visually secondary: 1.5–2 px muted strokes are enough to communicate structure without competing with node labels.
- Add atmospheric background color only around the edges or behind empty space; do not place high-contrast texture directly behind small node text.