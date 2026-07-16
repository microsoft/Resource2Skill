# SVG Recipe — Circular Node Morph Reveal Layout

## Visual mechanism
Minimal numbered circles sit exactly on top of circular photo crops, so each node can later “morph” in PowerPoint by shrinking the white number circle while zoom-growing the image beneath it. The static SVG builds the perfectly registered before/after layers; the reveal timing is added in PowerPoint after translation.

## SVG primitives needed
- 1× full-slide `<image>` for the atmospheric photographic background
- 1× `<rect>` with vertical `<linearGradient>` overlay for darkening the photo and improving text contrast
- 3× `<clipPath>` with `<circle>` for circular reveal-image crops
- 3× circular `<image>` elements clipped by those clip paths, one per node
- 3× soft halo `<circle>` elements behind each reveal node for premium depth and color rhythm
- 3× white “before state” `<circle>` elements stacked directly over the reveal images
- 3× numbered `<text>` elements centered on the white circles
- 3× caption `<text>` elements below the nodes
- 2× title `<text>` blocks using `<tspan>` for hierarchy and line breaks
- 1× `<filter id="softShadow">` for circle/text depth
- 1× `<filter id="titleShadow">` for readable title typography over the photo background
- Optional decorative `<path>` strokes for subtle motion arcs connecting the nodes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#06172A" stop-opacity="0.58"/>
      <stop offset="48%" stop-color="#0A2842" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#020B14" stop-opacity="0.62"/>
    </linearGradient>

    <radialGradient id="goldHalo" cx="50%" cy="50%" r="58%">
      <stop offset="0%" stop-color="#FFD36A" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#FF9900" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blueHalo" cx="50%" cy="50%" r="58%">
      <stop offset="0%" stop-color="#61D6FF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0096FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="redHalo" cx="50%" cy="50%" r="58%">
      <stop offset="0%" stop-color="#FF6E88" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#DC143C" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleShadow" x="-10%" y="-10%" width="120%" height="140%">
      <feOffset dx="0" dy="4" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipNode1">
      <circle cx="328" cy="394" r="70"/>
    </clipPath>
    <clipPath id="clipNode2">
      <circle cx="640" cy="394" r="70"/>
    </clipPath>
    <clipPath id="clipNode3">
      <circle cx="952" cy="394" r="70"/>
    </clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/minimal-ocean-horizon-sunset-wide.jpg"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgShade)"/>

  <path d="M330 394 C430 326, 536 326, 638 394 S848 462, 950 394"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="2.5"
        stroke-dasharray="9 14"/>

  <text x="640" y="88" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="4" fill="#D7F4FF" opacity="0.95" filter="url(#titleShadow)">
    THREE MOMENTS THAT MATTER
  </text>

  <text x="640" y="154" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        fill="#FFFFFF" filter="url(#titleShadow)">
    <tspan x="640" dy="0">WHAT WE DO IS</tspan>
    <tspan x="640" dy="66" fill="#FFF0B3">GORGEOUS</tspan>
  </text>

  <!-- Node 1: before state. The white circle fully covers the photo underneath. -->
  <circle cx="328" cy="394" r="104" fill="url(#goldHalo)"/>
  <image x="258" y="324" width="140" height="140"
         href="https://images.example.com/founder-with-laptop-warm-yellow-square.jpg"
         clip-path="url(#clipNode1)"/>
  <circle cx="328" cy="394" r="70" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="328" y="417" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        fill="#FF9F00">1</text>
  <text x="328" y="505" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        fill="#FFFFFF" filter="url(#titleShadow)">Good Idea</text>

  <!-- Node 2: mid-morph preview. In production, this smaller circle starts full size, then shrinks. -->
  <circle cx="640" cy="394" r="104" fill="url(#blueHalo)"/>
  <image x="570" y="324" width="140" height="140"
         href="https://images.example.com/minimal-blue-clock-interface-square.jpg"
         clip-path="url(#clipNode2)"/>
  <circle cx="640" cy="394" r="42" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="640" y="411" width="110" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="800"
        fill="#0096FF">2</text>
  <text x="640" y="505" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        fill="#FFFFFF" filter="url(#titleShadow)">Good Timing</text>

  <!-- Node 3: revealed state. The white circle layer has disappeared, leaving only the image. -->
  <circle cx="952" cy="394" r="104" fill="url(#redHalo)"/>
  <image x="882" y="324" width="140" height="140"
         href="https://images.example.com/business-team-celebrating-success-square.jpg"
         clip-path="url(#clipNode3)"/>
  <circle cx="952" cy="394" r="72" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.92"/>
  <text x="952" y="505" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        fill="#FFFFFF" filter="url(#titleShadow)">Good Result</text>

  <text x="640" y="618" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600"
        fill="#EAF8FF" opacity="0.84">
    Build each node as two perfectly overlapping layers: circular photo below, numbered white circle above.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the morph; PowerPoint animations should be applied after SVG-to-PPT translation.
- ❌ Do not use `<mask>` for the circular photo crop; use `<clipPath>` applied directly to each `<image>`.
- ❌ Do not place `clip-path` on a `<g>`, `<circle>`, or `<rect>` expecting it to crop everything; for this workflow, apply it only to the photo `<image>`.
- ❌ Do not use `<use>` or `<symbol>` to duplicate nodes; create each node explicitly so every circle/image/text layer remains individually editable in PowerPoint.
- ❌ Do not rely on a filter on `<line>` for connector shadows; filters on lines may be dropped. Use subtle dashed paths or plain lines instead.

## Composition notes
- Keep the top 35–40% of the slide for the title; place morph nodes slightly below vertical center so the reveal feels like a staged keynote moment, not a dense diagram.
- Each node’s white circle and circular image must share the exact same center and diameter for the morph illusion to work cleanly.
- Use colored halos behind the nodes to foreshadow the image reveal and create rhythm across the horizontal sequence.
- In PowerPoint, animate each node as: grow emphasis on white circle → zoom/shrink exit on white circle → zoom/grow entrance on photo underneath.