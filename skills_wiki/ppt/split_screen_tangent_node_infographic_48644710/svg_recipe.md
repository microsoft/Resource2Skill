# SVG Recipe — Split-Screen Tangent Node Infographic

## Visual mechanism
A 50/50 vertical split background is unified by a central white axis, with numbered badges sitting on the divide. Circular photo nodes sit tangent to branching connector lines; each node uses a larger white circle behind a slightly offset circular image crop to create a premium crescent-frame “cut-out” effect.

## SVG primitives needed
- 2× `<rect>` for the exact left/right split-screen background panels.
- 1× `<ellipse>` for the white title arch emerging from the top edge.
- 1× `<line>` for the continuous central vertical axis.
- 4× `<line>` for tangent connector branches from center badges to node rings.
- 4× large `<circle>` for white outer node rings / crescent frames.
- 4× slightly smaller clipped `<image>` elements for circular photo content inside each node.
- 4× `<clipPath>` definitions using `<circle>` for editable circular photo crops.
- 2× central badge `<circle>` elements for category numbers.
- 4× small `<circle>` elements for branch junction dots on the central axis.
- 1× `<filter id="nodeShadow">` applied to photo node circles and badges for depth.
- 2× `<linearGradient>` fills for richer red and navy background panels.
- Multiple `<text>` elements with nested `<tspan>` for title, badge numbers, labels, and supporting copy.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="redPanel" x1="0" y1="0" x2="640" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff5138"/>
      <stop offset="1" stop-color="#d92c22"/>
    </linearGradient>
    <linearGradient id="darkPanel" x1="640" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#343c48"/>
      <stop offset="1" stop-color="#202630"/>
    </linearGradient>
    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipLeftTop"><circle cx="364" cy="230" r="68"/></clipPath>
    <clipPath id="clipLeftBottom"><circle cx="300" cy="516" r="64"/></clipPath>
    <clipPath id="clipRightTop"><circle cx="982" cy="196" r="64"/></clipPath>
    <clipPath id="clipRightBottom"><circle cx="908" cy="500" r="68"/></clipPath>
  </defs>

  <!-- split background -->
  <rect x="0" y="0" width="640" height="720" fill="url(#redPanel)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#darkPanel)"/>

  <!-- title arch -->
  <ellipse cx="640" cy="-36" rx="270" ry="132" fill="#ffffff"/>
  <text x="430" y="38" width="420" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="700" fill="#2b323c">
    SPLIT STRATEGY MAP
  </text>
  <text x="485" y="68" width="310" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="600" letter-spacing="2" fill="#ee3b24">
    COMPARISON FRAMEWORK
  </text>

  <!-- central axis -->
  <line x1="640" y1="86" x2="640" y2="720" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>

  <!-- tangent branch connectors -->
  <line x1="592" y1="210" x2="440" y2="230" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
  <line x1="592" y1="474" x2="374" y2="500" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
  <line x1="688" y1="246" x2="918" y2="196" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
  <line x1="688" y1="510" x2="832" y2="500" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>

  <!-- branch junction dots -->
  <circle cx="640" cy="210" r="9" fill="#ee3b24" stroke="#ffffff" stroke-width="5"/>
  <circle cx="640" cy="246" r="9" fill="#2b323c" stroke="#ffffff" stroke-width="5"/>
  <circle cx="640" cy="474" r="9" fill="#ee3b24" stroke="#ffffff" stroke-width="5"/>
  <circle cx="640" cy="510" r="9" fill="#2b323c" stroke="#ffffff" stroke-width="5"/>

  <!-- left top crescent photo node -->
  <circle cx="364" cy="230" r="84" fill="#ffffff" filter="url(#nodeShadow)"/>
  <image href="https://images.example.com/executive-workshop-team-planning.jpg"
         x="296" y="162" width="136" height="136" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipLeftTop)"/>

  <!-- left bottom crescent photo node -->
  <circle cx="300" cy="500" r="74" fill="#ffffff" filter="url(#nodeShadow)"/>
  <image href="https://images.example.com/industrial-product-detail-red-lighting.jpg"
         x="236" y="452" width="128" height="128" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipLeftBottom)"/>

  <!-- right top crescent photo node -->
  <circle cx="982" cy="196" r="74" fill="#ffffff" filter="url(#nodeShadow)"/>
  <image href="https://images.example.com/analytics-dashboard-blue-glow.jpg"
         x="918" y="132" width="128" height="128" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipRightTop)"/>

  <!-- right bottom crescent photo node -->
  <circle cx="908" cy="500" r="84" fill="#ffffff" filter="url(#nodeShadow)"/>
  <image href="https://images.example.com/city-night-operations-control-room.jpg"
         x="840" y="432" width="136" height="136" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipRightBottom)"/>

  <!-- central numbered badges -->
  <circle cx="640" cy="228" r="48" fill="#ffffff" filter="url(#nodeShadow)"/>
  <text x="592" y="243" width="96" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800" fill="#ee3b24">01</text>

  <circle cx="640" cy="492" r="48" fill="#ffffff" filter="url(#nodeShadow)"/>
  <text x="592" y="507" width="96" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800" fill="#2b323c">02</text>

  <!-- left content -->
  <text x="64" y="176" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="1.5" fill="#ffffff">
    MARKET ENTRY
  </text>
  <text x="64" y="210" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="800" fill="#ffffff">
    <tspan x="64" dy="0">Launch</tspan>
    <tspan x="64" dy="35">Readiness</tspan>
  </text>
  <text x="64" y="292" width="265"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#ffe2dc">
    <tspan x="64" dy="0">Validate the offer, align field teams,</tspan>
    <tspan x="64" dy="24">and sequence customer proof points.</tspan>
  </text>

  <text x="82" y="610" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#ffffff">
    Operational Scale-Up
  </text>
  <text x="82" y="642" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#ffe2dc">
    <tspan x="82" dy="0">Automate repeatable motions and protect</tspan>
    <tspan x="82" dy="23">capacity before demand accelerates.</tspan>
  </text>

  <!-- right content -->
  <text x="1010" y="106" width="210" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="1.5" fill="#ee3b24">
    PLATFORM SIGNALS
  </text>
  <text x="1010" y="140" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="800" fill="#ffffff">
    <tspan x="1010" dy="0">Data-Led</tspan>
    <tspan x="1010" dy="35">Decisions</tspan>
  </text>
  <text x="1010" y="222" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#cfd6df">
    <tspan x="1010" dy="0">Turn fragmented insight streams</tspan>
    <tspan x="1010" dy="24">into a single executive rhythm.</tspan>
  </text>

  <text x="990" y="528" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#ffffff">
    Future Operating Model
  </text>
  <text x="990" y="560" width="235"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#cfd6df">
    <tspan x="990" dy="0">Define ownership, decision rights,</tspan>
    <tspan x="990" dy="23">and control-tower governance.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using SVG `<mask>` to subtract crescents; create the crescent illusion with white circles behind offset circular images instead.
- ❌ Applying `clip-path` to circles or groups; only clip the `<image>` elements.
- ❌ Putting arrow markers on branch paths; this design relies on clean tangent lines, not arrows.
- ❌ Using `<textPath>` for curved labels around nodes; PowerPoint translation will drop it.
- ❌ Filtering connector lines; shadows/glows should be applied to circles or badges only.

## Composition notes
- Keep the split exactly centered at `x=640`; the central vertical axis is the visual spine and should read as continuous.
- Branch lines should terminate at the outer circle’s tangent point, usually the leftmost or rightmost edge of the white node ring.
- Let the left side descend and the right side rise or mirror it; the opposing diagonals make the comparison feel dynamic.
- Use white as the unifying layer: axis, branch lines, node rings, title arch, and badges should all share the same white fill/stroke.