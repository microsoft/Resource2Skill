# SVG Recipe — Mirrored Concentric Arc Comparison

## Visual mechanism
A bisected circular infographic uses mirrored concentric semi-rings to frame an A-versus-B comparison, with numbered data nodes placed along the outer orbit. The central dashed axis creates a clean visual split while left/right text blocks align outward from the circular structure.

## SVG primitives needed
- 1× `<rect>` for the subtle full-slide background wash
- 4× `<path>` for the left/right outer half-donut rings and inner solid semicircles
- 2× `<path>` for faint outer orbit guide arcs
- 1× `<line>` for the central dashed dividing axis
- 6× `<line>` for short node-to-text connector ticks
- 6× `<circle>` for colored numbered data nodes
- 6× `<circle>` for smaller glossy node highlights
- 19× `<text>` for the title, side labels, node numbers, and comparison descriptions
- 3× `<linearGradient>` for background and ring depth
- 1× `<radialGradient>` for node highlight styling
- 1× `<filter id="softShadow">` applied to arcs and nodes for keynote-style depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F6F8"/>
    </linearGradient>

    <linearGradient id="leftArc" x1="355" y1="115" x2="640" y2="685" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#B9DAF4"/>
      <stop offset="100%" stop-color="#78AEDB"/>
    </linearGradient>

    <linearGradient id="rightArc" x1="640" y1="115" x2="925" y2="685" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#D7D8DA"/>
      <stop offset="100%" stop-color="#8F9296"/>
    </linearGradient>

    <radialGradient id="nodeGloss" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.12"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.10  0 0 0 0 0.12  0 0 0 0 0.16  0 0 0 0.20 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="640" y="62" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#20242A">
    Mirrored Market Readiness Comparison
  </text>
  <text x="640" y="93" width="680" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7B828C">
    Two scenarios mapped to the same decision orbit for rapid executive contrast
  </text>

  <!-- Outer half-donut rings -->
  <path d="M 640 115 A 285 285 0 0 0 640 685 L 640 605 A 205 205 0 0 1 640 195 Z"
        fill="url(#leftArc)" filter="url(#softShadow)"/>
  <path d="M 640 115 A 285 285 0 0 1 640 685 L 640 605 A 205 205 0 0 0 640 195 Z"
        fill="url(#rightArc)" filter="url(#softShadow)"/>

  <!-- Inner solid semicircles -->
  <path d="M 640 275 A 125 125 0 0 0 640 525 Z"
        fill="#A7CEF0" opacity="0.95"/>
  <path d="M 640 275 A 125 125 0 0 1 640 525 Z"
        fill="#B8BABE" opacity="0.95"/>

  <!-- Subtle orbit guides -->
  <path d="M 640 100 A 300 300 0 0 0 640 700"
        fill="none" stroke="#D9E6F3" stroke-width="2" stroke-dasharray="4 10"/>
  <path d="M 640 100 A 300 300 0 0 1 640 700"
        fill="none" stroke="#E2E3E5" stroke-width="2" stroke-dasharray="4 10"/>

  <!-- Central split axis -->
  <line x1="640" y1="122" x2="640" y2="690"
        stroke="#62666B" stroke-width="2.5" stroke-dasharray="10 10"/>

  <!-- Core labels -->
  <text x="585" y="385" width="105" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#244A69">
    Scenario A
  </text>
  <text x="585" y="412" width="118" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4F7696">
    Expansion play
  </text>
  <text x="695" y="385" width="105" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#474A4F">
    Scenario B
  </text>
  <text x="695" y="412" width="118" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777B80">
    Efficiency play
  </text>

  <!-- Left connectors -->
  <line x1="424" y1="217" x2="304" y2="217" stroke="#B8C4CF" stroke-width="2"/>
  <line x1="355" y1="400" x2="286" y2="400" stroke="#B8C4CF" stroke-width="2"/>
  <line x1="424" y1="583" x2="304" y2="583" stroke="#B8C4CF" stroke-width="2"/>

  <!-- Right connectors -->
  <line x1="856" y1="217" x2="976" y2="217" stroke="#C3C5C8" stroke-width="2"/>
  <line x1="925" y1="400" x2="994" y2="400" stroke="#C3C5C8" stroke-width="2"/>
  <line x1="856" y1="583" x2="976" y2="583" stroke="#C3C5C8" stroke-width="2"/>

  <!-- Left nodes -->
  <circle cx="424" cy="217" r="24" fill="#F28C28" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="424" cy="217" r="24" fill="url(#nodeGloss)"/>
  <text x="424" y="225" width="44" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">1</text>

  <circle cx="355" cy="400" r="24" fill="#27AE60" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="355" cy="400" r="24" fill="url(#nodeGloss)"/>
  <text x="355" y="408" width="44" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">2</text>

  <circle cx="424" cy="583" r="24" fill="#2F80ED" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="424" cy="583" r="24" fill="url(#nodeGloss)"/>
  <text x="424" y="591" width="44" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">3</text>

  <!-- Right nodes -->
  <circle cx="856" cy="217" r="24" fill="#EB5757" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="856" cy="217" r="24" fill="url(#nodeGloss)"/>
  <text x="856" y="225" width="44" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">4</text>

  <circle cx="925" cy="400" r="24" fill="#9B51E0" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="925" cy="400" r="24" fill="url(#nodeGloss)"/>
  <text x="925" y="408" width="44" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">5</text>

  <circle cx="856" cy="583" r="24" fill="#F2C94C" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="856" cy="583" r="24" fill="url(#nodeGloss)"/>
  <text x="856" y="591" width="44" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#FFFFFF">6</text>

  <!-- Left comparison copy -->
  <text x="282" y="198" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2E3338">
    Faster adoption
  </text>
  <text x="282" y="223" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A828A">
    Existing demand signals reduce launch friction.
  </text>

  <text x="264" y="381" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2E3338">
    Higher upside
  </text>
  <text x="264" y="406" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A828A">
    Larger addressable base with premium attach.
  </text>

  <text x="282" y="564" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2E3338">
    Brand lift
  </text>
  <text x="282" y="589" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A828A">
    Creates visible momentum in new segments.
  </text>

  <!-- Right comparison copy -->
  <text x="998" y="198" width="220" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2E3338">
    Lower risk
  </text>
  <text x="998" y="223" width="220" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A828A">
    Uses proven channels and known operating model.
  </text>

  <text x="1016" y="381" width="220" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2E3338">
    Cost control
  </text>
  <text x="1016" y="406" width="220" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A828A">
    Savings compound through process automation.
  </text>

  <text x="998" y="564" width="220" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2E3338">
    Predictable ROI
  </text>
  <text x="998" y="589" width="220" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A828A">
    Shorter payback horizon and tighter variance.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to cut donut holes; build the half-donut directly as compound-looking arc paths instead.
- ❌ Applying `clip-path` to the ring paths; clipping is only reliable for images in this pipeline.
- ❌ Putting arrow markers on curved paths or connectors; use plain `<line>` connectors for dependable PowerPoint output.
- ❌ Creating the arcs as a raster screenshot unless a special texture is essential; editable SVG paths are cleaner and more flexible.
- ❌ Letting text auto-size implicitly; every `<text>` element needs a `width` attribute for stable PPT rendering.

## Composition notes
- Keep the circular structure centered slightly below the title; in a 1280×720 slide, `cx=640`, `cy≈400` leaves enough top space for a strong headline.
- Reserve the far left and far right thirds for short comparison copy; align left-side text rightward and right-side text leftward to reinforce symmetry.
- Use cool color on one half and neutral gray on the other, then make the numbered nodes bright accents so the reading sequence is obvious.
- The dashed vertical axis should run through both semicircles and extend beyond the ring to make the A/B division unmistakable.