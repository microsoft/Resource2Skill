# SVG Recipe — Data Spotlight Reveal via Morph

## Visual mechanism
A full-context chart stays static while a hollow, high-contrast spotlight ring moves and scales between two slides, using Morph to guide attention from the macro dataset to one decisive outlier. The visual works because the ring is the only object that changes position/size; everything else remains locked, making the motion feel intentional and cinematic.

## SVG primitives needed
- 1× `<rect>` full-slide background with deep navy gradient
- 1× `<linearGradient>` for the executive dark background
- 1× `<filter id="softShadow">` applied to annotation/card elements
- 1× `<filter id="goldGlow">` applied to the spotlight ring
- 5× translucent `<line>` horizontal gridlines for chart scale
- 1× `<line>` x-axis baseline
- 4× `<rect>` chart bars with rounded tops, one outlier emphasized
- 4× `<text>` category labels under bars
- 4× `<text>` value labels above bars
- 1× hollow `<circle>` spotlight ring, duplicated across slides with the same PowerPoint shape name such as `!!Spotlight`
- 1× dashed `<circle>` optional “previous position” ghost guide for authoring/debugging only
- 1× `<rect>` annotation card beside the spotlight
- 1× `<path>` connector from annotation card to focused bar
- 3× `<text>` blocks for title, subtitle, and insight callout
- Optional 1× translucent `<rect>` chart panel to separate the chart from the background

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgNavy" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#0D111C"/>
      <stop offset="55%" stop-color="#132238"/>
      <stop offset="100%" stop-color="#1E2D41"/>
    </linearGradient>

    <linearGradient id="barCyan" x1="0" y1="500" x2="0" y2="180">
      <stop offset="0%" stop-color="#0077B6"/>
      <stop offset="45%" stop-color="#00BFFF"/>
      <stop offset="100%" stop-color="#6FE8FF"/>
    </linearGradient>

    <linearGradient id="barGold" x1="0" y1="500" x2="0" y2="120">
      <stop offset="0%" stop-color="#B97800"/>
      <stop offset="45%" stop-color="#FFD700"/>
      <stop offset="100%" stop-color="#FFF1A6"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="14" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="goldGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="9" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgNavy)"/>

  <text x="78" y="74" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#FFFFFF">
    Quarterly Revenue Spotlight
  </text>
  <text x="80" y="108" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#AFC3D8">
    Morph the gold ring from context view to focus view while the chart remains perfectly static.
  </text>

  <rect x="72" y="150" width="850" height="470" rx="28" fill="#FFFFFF" opacity="0.045" stroke="#FFFFFF" stroke-opacity="0.10"/>

  <line x1="135" y1="520" x2="860" y2="520" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1"/>
  <line x1="135" y1="445" x2="860" y2="445" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="135" y1="370" x2="860" y2="370" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="135" y1="295" x2="860" y2="295" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="135" y1="220" x2="860" y2="220" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="135" y1="520" x2="860" y2="520" stroke="#8FA7BE" stroke-opacity="0.38" stroke-width="2"/>

  <rect x="175" y="326" width="104" height="194" rx="18" fill="url(#barCyan)"/>
  <rect x="337" y="410" width="104" height="110" rx="18" fill="url(#barCyan)" opacity="0.86"/>
  <rect x="499" y="367" width="104" height="153" rx="18" fill="url(#barCyan)" opacity="0.9"/>
  <rect x="661" y="214" width="104" height="306" rx="18" fill="url(#barGold)" filter="url(#softShadow)"/>

  <text x="188" y="555" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#C8D8E8" text-anchor="middle">Q1</text>
  <text x="350" y="555" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#C8D8E8" text-anchor="middle">Q2</text>
  <text x="512" y="555" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#C8D8E8" text-anchor="middle">Q3</text>
  <text x="674" y="555" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFE57A" text-anchor="middle">Q4</text>

  <text x="178" y="304" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#EAF9FF" text-anchor="middle">$4.3M</text>
  <text x="340" y="388" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#CFE8F3" text-anchor="middle">$2.5M</text>
  <text x="502" y="345" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#CFE8F3" text-anchor="middle">$3.5M</text>
  <text x="664" y="190" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFF1A6" text-anchor="middle">$6.8M</text>

  <!-- Authoring guide: slide 1 ring position. Delete or hide before presenting final slide. -->
  <circle cx="227" cy="326" r="55" fill="none" stroke="#FFD700" stroke-opacity="0.25" stroke-width="5" stroke-dasharray="10 12"/>

  <!-- Morph object: keep this same object/name on both slides, e.g. PowerPoint shape name !!Spotlight. -->
  <circle id="morph_spotlight" cx="713" cy="214" r="108" fill="none" stroke="#FFD700" stroke-width="12" filter="url(#goldGlow)"/>

  <path d="M810 210 C870 188, 905 182, 948 188" fill="none" stroke="#FFD700" stroke-width="3" stroke-linecap="round"/>

  <rect x="948" y="148" width="255" height="164" rx="24" fill="#101A2A" stroke="#FFD700" stroke-opacity="0.42" filter="url(#softShadow)"/>
  <text x="975" y="190" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFD700">
    OUTLIER REVEALED
  </text>
  <text x="975" y="226" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">
    +94% vs Q3
  </text>
  <text x="975" y="266" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#BFD1E4">
    Enterprise renewals drove the strongest quarterly revenue result of the year.
  </text>

  <text x="80" y="654" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7F93AA">
    Build as two slides: Slide 1 uses the small ring over Q1; Slide 2 uses this enlarged ring over Q4 with Morph → By Object.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not move or resize the chart between the two Morph slides; only the spotlight ring should change.
- ❌ Do not use `<mask>` to create a punched-out overlay; use a transparent-fill circle with thick stroke instead.
- ❌ Do not apply `filter` to `<line>` connector strokes; use filters only on supported shapes such as `<rect>`, `<circle>`, `<path>`, or `<text>`.
- ❌ Do not rely on `marker-end` for arrowheads on paths; if an arrow is needed, draw the arrowhead manually with a small `<path>` or use a direct `<line>` with marker support where allowed.
- ❌ Do not change the Morph object’s identity/name between slides; the spotlight must resolve to the same PowerPoint shape object, typically named `!!Spotlight`.

## Composition notes
- Keep the chart static and dominant, occupying roughly 65–75% of the slide width; reserve the right side for the focused insight card.
- Slide 1 should feel like a macro context view: smaller ring, no heavy annotation, broad negative space.
- Slide 2 should feel like a reveal: enlarge the ring to 2×–2.5×, place it around the outlier, and add a concise callout near the ring.
- Use cyan for normal data and gold only for the spotlight/outlier so the viewer instantly understands what changed.