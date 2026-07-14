# SVG Recipe — Rotational Fan-Out Morphing

## Visual mechanism
A stack of oversized rectangular panels rotates around a shared off-canvas pivot, opening like a deck of cards or turbine blades. For PowerPoint Morph, create a collapsed start slide and an expanded end slide with the same object IDs/names, changing only each panel’s rotation, position, and text placement.

## SVG primitives needed
- 1× `<rect>` for the full-slide turquoise background field
- 5× oversized `<rect>` for the colored fan panels, each rotated around the same bottom-right pivot
- 5× `<text>` groups for numbered agenda items aligned to the fan panel angles
- 1× large rotated `<text>` for the vertical “CONTENTS” label
- 1× `<text>` block for the small presentation eyebrow and title
- 3× `<path>` for subtle decorative pivot arcs and motion traces
- 1× `<circle>` for the visible pivot accent near the bottom-right corner
- 2× `<linearGradient>` for background depth and panel highlight accents
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` for layered depth on panels
- 1× `<filter id="softGlow">` using `feGaussianBlur` for the pivot glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#37C9E6"/>
      <stop offset="58%" stop-color="#2FB6DA"/>
      <stop offset="100%" stop-color="#1685B8"/>
    </linearGradient>

    <linearGradient id="panelSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="36%" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="panelShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="-8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="13" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <!-- Full-slide base; keep this identical on both Morph slides -->
  <rect id="bg" x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <!-- Motion/pivot traces; decorative only, not animated in SVG -->
  <path id="arc-01" d="M 902 654 C 982 584, 1086 550, 1200 558" fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="2"/>
  <path id="arc-02" d="M 820 604 C 936 486, 1072 426, 1232 420" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2" stroke-dasharray="10 12"/>
  <path id="arc-03" d="M 742 536 C 904 352, 1068 262, 1260 250" fill="none" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>

  <!-- Fan panels: same pivot point, different final rotations. 
       For the collapsed Morph slide, keep these IDs and set rotations close together/off-canvas. -->
  <rect id="fan-panel-01" x="500" y="-780" width="1450" height="1450" fill="#F46B45" filter="url(#panelShadow)" transform="rotate(42 1180 690)"/>
  <rect id="fan-panel-02" x="500" y="-780" width="1450" height="1450" fill="#7030A0" filter="url(#panelShadow)" transform="rotate(31 1180 690)"/>
  <rect id="fan-panel-03" x="500" y="-780" width="1450" height="1450" fill="#FFC000" filter="url(#panelShadow)" transform="rotate(21 1180 690)"/>
  <rect id="fan-panel-04" x="500" y="-780" width="1450" height="1450" fill="#00B0F0" filter="url(#panelShadow)" transform="rotate(10 1180 690)"/>
  <rect id="fan-panel-05" x="500" y="-780" width="1450" height="1450" fill="#F46B45" filter="url(#panelShadow)" transform="rotate(0 1180 690)"/>

  <!-- Subtle sheen overlays on top of each panel; preserve IDs for Morph pairing -->
  <rect id="fan-sheen-01" x="500" y="-780" width="1450" height="1450" fill="url(#panelSheen)" opacity="0.45" transform="rotate(42 1180 690)"/>
  <rect id="fan-sheen-02" x="500" y="-780" width="1450" height="1450" fill="url(#panelSheen)" opacity="0.35" transform="rotate(31 1180 690)"/>
  <rect id="fan-sheen-03" x="500" y="-780" width="1450" height="1450" fill="url(#panelSheen)" opacity="0.32" transform="rotate(21 1180 690)"/>
  <rect id="fan-sheen-04" x="500" y="-780" width="1450" height="1450" fill="url(#panelSheen)" opacity="0.32" transform="rotate(10 1180 690)"/>
  <rect id="fan-sheen-05" x="500" y="-780" width="1450" height="1450" fill="url(#panelSheen)" opacity="0.25" transform="rotate(0 1180 690)"/>

  <!-- Left-side content block -->
  <text id="eyebrow" x="68" y="80" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" letter-spacing="3" fill="#EAFBFF" opacity="0.86">
    STRATEGY BRIEFING
  </text>

  <text id="main-title" x="68" y="132" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">
    <tspan x="68" dy="0">Project Summary</tspan>
    <tspan x="68" dy="52">Report</tspan>
  </text>

  <text id="subtitle" x="72" y="258" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#DDF7FF" opacity="0.9">
    Five-part executive agenda revealed through a rotational fan-out Morph transition.
  </text>

  <text id="contents-vertical" x="112" y="642" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="800" letter-spacing="8" fill="#FFFFFF" opacity="0.22" transform="rotate(-90 112 642)">
    CONTENTS
  </text>

  <!-- Agenda labels: draw after panels so they remain visible; rotate each label to match its panel -->
  <text id="item-01" x="684" y="132" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF" transform="rotate(42 684 132)">
    <tspan font-size="44" font-weight="800">01</tspan><tspan dx="18" dy="-7">Project Introduction</tspan>
  </text>

  <text id="item-02" x="704" y="205" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF" transform="rotate(31 704 205)">
    <tspan font-size="44" font-weight="800">02</tspan><tspan dx="18" dy="-7">Goal Planning</tspan>
  </text>

  <text id="item-03" x="730" y="286" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF" transform="rotate(21 730 286)">
    <tspan font-size="44" font-weight="800">03</tspan><tspan dx="18" dy="-7">Results Showcase</tspan>
  </text>

  <text id="item-04" x="766" y="382" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF" transform="rotate(10 766 382)">
    <tspan font-size="44" font-weight="800">04</tspan><tspan dx="18" dy="-7">Risk &amp; Deficiencies</tspan>
  </text>

  <text id="item-05" x="806" y="504" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">
    <tspan font-size="44" font-weight="800">05</tspan><tspan dx="18" dy="-7">Future Planning</tspan>
  </text>

  <!-- Pivot accent: place near the common rotation anchor to make the fan logic legible -->
  <circle id="pivot-glow" cx="1180" cy="690" r="54" fill="#FFFFFF" opacity="0.22" filter="url(#softGlow)"/>
  <circle id="pivot-dot" cx="1180" cy="690" r="10" fill="#FFFFFF" opacity="0.86"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; PowerPoint Morph should create the motion, not SVG animation.
- ❌ `<use>` or `<symbol>` clones for repeated panels; each fan panel needs its own native editable shape for Morph pairing.
- ❌ `transform="matrix(...)"` or `skewX/skewY`; use only explicit `rotate(angle cx cy)` and simple translate/scale if needed.
- ❌ Applying `filter` to `<line>` elements for motion trails; use `<path>` strokes instead if glow/shadow is needed.
- ❌ `marker-end` arrows on paths; if arrows are required, build arrowheads from small editable paths.

## Composition notes
- Use a shared pivot slightly outside the bottom-right corner, around `(1180, 690)`, so the fan feels anchored but not mechanically centered.
- Keep the left 30–35% of the slide relatively calm for the title, vertical label, or speaker context.
- The fan panels should be much larger than the canvas; oversized rectangles prevent gaps during rotation and Morph interpolation.
- For the Morph setup, duplicate the slide: on the first slide collapse all `fan-panel-*`, `fan-sheen-*`, and `item-*` objects into a near-parallel/off-screen stack, then use this expanded SVG state as the second slide.