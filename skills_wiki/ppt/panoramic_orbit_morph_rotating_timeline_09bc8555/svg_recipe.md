# SVG Recipe — Panoramic Orbit Morph (Rotating Timeline)

## Visual mechanism
A wide cinematic background pans horizontally while a fixed left-side “planet” anchors a large rotating orbit ring with dated nodes. Across Morph-linked slides, keep the same objects in the same order, but shift the panorama and rotate/recalculate the orbit nodes so the next milestone swings into the active focus zone.

## SVG primitives needed
- 1× wide `<image>` for the panoramic background, positioned wider than the slide so it can pan between slides
- 1× full-slide `<rect>` for the dark readability overlay
- 1× large `<circle>` for the warm planet/pivot on the far left
- 2× large `<circle>` for the orbit track and secondary faint orbital guide
- 6× small `<circle>` for timeline nodes placed along the orbit circumference
- 6× `<text>` labels for node captions such as PART 01 / PART 02
- 1× highlighted node `<circle>` plus glow filter to indicate the active stage
- 2× decorative `<path>` arc strokes for cinematic orbital motion accents
- 1× right-side translucent `<rect>` content panel
- Multiple `<text>` elements with explicit `width` attributes for title, stage heading, metadata, and body copy
- 1× `<linearGradient>` for the planet fill
- 1× `<radialGradient>` for active node highlight
- 2× `<filter>` definitions for shadow and glow applied to editable shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="planetGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4D0A6"/>
      <stop offset="48%" stop-color="#D6AF8C"/>
      <stop offset="100%" stop-color="#8B5E49"/>
    </linearGradient>

    <radialGradient id="nodeHot" cx="35%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="42%" stop-color="#F5C98E"/>
      <stop offset="100%" stop-color="#D6AF8C"/>
    </radialGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#151A22" stop-opacity="0.80"/>
      <stop offset="100%" stop-color="#030507" stop-opacity="0.35"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="18" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="warmGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="12" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Panoramic background: for later Morph states, change x to -280, -520, etc. -->
  <image href="https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=2200&q=80"
         x="-160" y="0" width="1700" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Contrast veil -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.62"/>
  <rect x="0" y="0" width="1280" height="720" fill="#0B1020" opacity="0.18"/>

  <!-- Fixed planet pivot -->
  <circle cx="70" cy="360" r="285" fill="url(#planetGrad)" opacity="0.95" filter="url(#softShadow)"/>
  <circle cx="70" cy="360" r="235" fill="none" stroke="#FFE7C8" stroke-width="1.5" opacity="0.20"/>
  <circle cx="-4" cy="270" r="78" fill="#FFFFFF" opacity="0.06"/>

  <!-- Orbit system: rotate this group between slides, or recompute each node position with trig. -->
  <g id="orbit-state-02">
    <circle cx="70" cy="360" r="430" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.34"/>
    <circle cx="70" cy="360" r="378" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.12" stroke-dasharray="8 16"/>

    <path d="M 330 18 C 430 78, 502 180, 520 292"
          fill="none" stroke="#F5C98E" stroke-width="4" opacity="0.58" stroke-linecap="round"/>
    <path d="M 430 580 C 498 506, 528 426, 520 332"
          fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.18" stroke-dasharray="10 14" stroke-linecap="round"/>

    <!-- Nodes along the orbit, roughly 20 degrees apart -->
    <circle cx="217" cy="-44" r="7" fill="#FFFFFF" opacity="0.44"/>
    <text x="242" y="-40" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.50">PART 01</text>

    <circle cx="346" cy="31" r="8" fill="#FFFFFF" opacity="0.58"/>
    <text x="371" y="36" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.62">PART 02</text>

    <circle cx="442" cy="145" r="9" fill="#FFFFFF" opacity="0.70"/>
    <text x="467" y="150" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.72">PART 03</text>

    <circle cx="494" cy="285" r="19" fill="url(#nodeHot)" filter="url(#warmGlow)"/>
    <circle cx="494" cy="285" r="34" fill="none" stroke="#F5C98E" stroke-width="2" opacity="0.55"/>
    <text x="528" y="290" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#F8D3A2">PART 04 · ACTIVE</text>

    <circle cx="494" cy="435" r="8" fill="#FFFFFF" opacity="0.54"/>
    <text x="528" y="440" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.58">PART 05</text>

    <circle cx="442" cy="575" r="7" fill="#FFFFFF" opacity="0.40"/>
    <text x="467" y="580" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.44">PART 06</text>
  </g>

  <!-- Right narrative panel -->
  <rect x="650" y="112" width="500" height="472" rx="28" fill="url(#panelGrad)" stroke="#FFFFFF" stroke-width="1" opacity="0.96"/>
  <rect x="680" y="142" width="92" height="28" rx="14" fill="#D6AF8C" opacity="0.92"/>
  <text x="700" y="162" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#17110D">STEP 04</text>

  <text x="680" y="224" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="50" font-weight="700" fill="#FFFFFF">
    Orbit Morph
  </text>
  <text x="680" y="274" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="50" font-weight="300" fill="#D6AF8C">
    Prototype
  </text>

  <line x1="682" y1="312" x2="1038" y2="312" stroke="#FFFFFF" stroke-width="1" opacity="0.24"/>

  <text x="680" y="356" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#EAEAEA">
    <tspan x="680" dy="0">The rotating timeline brings the next milestone into</tspan>
    <tspan x="680" dy="30">focus while the city panorama pans in the opposite</tspan>
    <tspan x="680" dy="30">direction, creating a continuous sense of forward</tspan>
    <tspan x="680" dy="30">motion through strategy, design, and launch.</tspan>
  </text>

  <text x="680" y="512" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF" opacity="0.58">
    MORPH CUE: keep object order identical; change image x-position and rotate the orbit state by -20° per slide.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG animation tags such as `<animate>` or `<animateTransform>`; PowerPoint Morph should create the motion, not SVG animation
- ❌ `<use>` or `<symbol>` for repeated nodes; duplicate each node as real editable circles/text so Morph can track them reliably
- ❌ `marker-end` arrowheads on orbit paths; use plain arc strokes or separate small path chevrons if directional cues are needed
- ❌ Applying `clip-path` to non-image orbit elements; if you need cropped photos, clip only the `<image>`
- ❌ Reordering timeline nodes between Morph slides; preserve identical object sequence and only change positions/rotation

## Composition notes
- Keep the planet center slightly off-canvas on the left so the orbit feels enormous and mechanical rather than like a small diagram.
- Reserve the right 45–50% of the slide for the active stage title and body copy; the orbit should point toward this panel but not collide with it.
- Use a dark overlay over the panorama at roughly 55–65% opacity so the background remains cinematic without competing with text.
- For a multi-slide sequence, pan the background left by 200–300 px per slide and rotate the orbit/nodes by about 20° per step to create the panoramic time-travel effect.