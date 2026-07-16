# SVG Recipe — Dynamic Concentric Arc Gauge

## Visual mechanism
A premium HUD-style metric chart built from nested semi-circular annular paths anchored to the bottom edge. Each ring has a muted full-track arc plus a bright data arc sweeping left-to-right, with vertical connector lines tying arc endpoints to floating percentage labels.

## SVG primitives needed
- 1× `<rect>` for the deep navy slide background
- 1× `<radialGradient>` for a subtle spotlight behind the gauge
- 4× `<path>` for muted concentric half-circle track arcs
- 4× `<path>` for filled data arcs, each using annular arc geometry
- 4× `<linearGradient>` fills for neon arc coloring and dimensionality
- 1× `<filter id="softGlow">` applied to bright arc paths and endpoint dots
- 4× `<line>` for vertical connector/drop lines from arc tips to labels
- 8× `<circle>` for endpoint dots and subtle halo markers
- Multiple `<text>` elements with explicit `width` for title, description, metric values, and subtitles
- Optional decorative `<path>` strokes for faint HUD guide rings and background rhythm

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="78%" cy="72%" r="58%">
      <stop offset="0%" stop-color="#12328F" stop-opacity="0.65"/>
      <stop offset="48%" stop-color="#07164F" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#050A3C" stop-opacity="1"/>
    </radialGradient>

    <linearGradient id="cyanArc" x1="520" y1="705" x2="1244" y2="543" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00A8FF"/>
      <stop offset="62%" stop-color="#00E5FF"/>
      <stop offset="100%" stop-color="#8FF7FF"/>
    </linearGradient>
    <linearGradient id="mintArc" x1="574" y1="705" x2="1066" y2="424" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00C76A"/>
      <stop offset="68%" stop-color="#00FF85"/>
      <stop offset="100%" stop-color="#B7FFD8"/>
    </linearGradient>
    <linearGradient id="blueArc" x1="628" y1="705" x2="917" y2="434" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#366BFF"/>
      <stop offset="65%" stop-color="#64C8FF"/>
      <stop offset="100%" stop-color="#D2F1FF"/>
    </linearGradient>
    <linearGradient id="violetArc" x1="682" y1="705" x2="820" y2="502" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7C4DFF"/>
      <stop offset="65%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#F0D5FF"/>
    </linearGradient>

    <filter id="softGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#050A3C" opacity="0.42"/>

  <path d="M 470 705 A 430 430 0 0 1 1330 705" fill="none" stroke="#223A7A" stroke-width="1.2" stroke-dasharray="4 10" opacity="0.45"/>
  <path d="M 620 705 A 280 280 0 0 1 1180 705" fill="none" stroke="#3150A7" stroke-width="1" stroke-dasharray="2 8" opacity="0.35"/>

  <text x="84" y="236" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" letter-spacing="3" fill="#69D7FF" opacity="0.9">FY26 EXECUTIVE DASHBOARD</text>
  <text x="82" y="304" width="430" font-family="Georgia, 'Times New Roman', serif" font-size="56" font-weight="600" fill="#FFFFFF">Dynamic</text>
  <text x="82" y="365" width="430" font-family="Georgia, 'Times New Roman', serif" font-size="56" font-weight="600" fill="#FFFFFF">Arc Gauge</text>
  <text x="86" y="414" width="385" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#B8C5F5" opacity="0.86">
    Four priority signals rendered as nested semi-circular indicators with endpoint callouts.
  </text>
  <line x1="86" y1="456" x2="268" y2="456" stroke="#00E5FF" stroke-width="3"/>
  <text x="86" y="489" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#8EA0D6" opacity="0.9">Native editable vector arcs; duplicate slides to Morph from 0% to final state.</text>

  <!-- muted full tracks -->
  <path d="M 520 705 A 380 380 0 0 1 1280 705 L 1246 705 A 346 346 0 0 0 554 705 Z" fill="#050A3C" stroke="#2C478D" stroke-width="1.2" opacity="0.95"/>
  <path d="M 574 705 A 326 326 0 0 1 1226 705 L 1192 705 A 292 292 0 0 0 608 705 Z" fill="#050A3C" stroke="#2C478D" stroke-width="1.2" opacity="0.95"/>
  <path d="M 628 705 A 272 272 0 0 1 1172 705 L 1138 705 A 238 238 0 0 0 662 705 Z" fill="#050A3C" stroke="#2C478D" stroke-width="1.2" opacity="0.95"/>
  <path d="M 682 705 A 218 218 0 0 1 1118 705 L 1084 705 A 184 184 0 0 0 716 705 Z" fill="#050A3C" stroke="#2C478D" stroke-width="1.2" opacity="0.95"/>

  <!-- completed data arcs -->
  <path d="M 520 705 A 380 380 0 0 1 1244 543 L 1213 558 A 346 346 0 0 0 554 705 Z" fill="url(#cyanArc)" filter="url(#softGlow)"/>
  <path d="M 574 705 A 326 326 0 0 1 1066 424 L 1049 454 A 292 292 0 0 0 608 705 Z" fill="url(#mintArc)" filter="url(#softGlow)"/>
  <path d="M 628 705 A 272 272 0 0 1 917 434 L 915 468 A 238 238 0 0 0 662 705 Z" fill="url(#blueArc)" filter="url(#softGlow)"/>
  <path d="M 682 705 A 218 218 0 0 1 820 502 L 832 534 A 184 184 0 0 0 716 705 Z" fill="url(#violetArc)" filter="url(#softGlow)"/>

  <!-- connector lines and endpoint markers -->
  <line x1="1229" y1="551" x2="1229" y2="292" stroke="#00E5FF" stroke-width="1.4"/>
  <circle cx="1229" cy="551" r="13" fill="#00E5FF" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="1229" cy="551" r="5.5" fill="#B9FBFF"/>

  <line x1="1057" y1="439" x2="1057" y2="214" stroke="#00FF85" stroke-width="1.4"/>
  <circle cx="1057" cy="439" r="13" fill="#00FF85" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="1057" cy="439" r="5.5" fill="#C8FFE0"/>

  <line x1="916" y1="451" x2="916" y2="178" stroke="#64C8FF" stroke-width="1.4"/>
  <circle cx="916" cy="451" r="13" fill="#64C8FF" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="916" cy="451" r="5.5" fill="#D9F4FF"/>

  <line x1="826" y1="518" x2="826" y2="270" stroke="#C084FC" stroke-width="1.4"/>
  <circle cx="826" cy="518" r="13" fill="#C084FC" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="826" cy="518" r="5.5" fill="#F3D9FF"/>

  <!-- floating labels -->
  <text x="1158" y="268" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#FFFFFF">86%</text>
  <text x="1158" y="292" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" letter-spacing="1.8" fill="#00E5FF">ADOPTION</text>

  <text x="986" y="190" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#FFFFFF">67%</text>
  <text x="986" y="214" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" letter-spacing="1.8" fill="#00FF85">RETENTION</text>

  <text x="845" y="154" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#FFFFFF">52%</text>
  <text x="845" y="178" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" letter-spacing="1.8" fill="#64C8FF">VELOCITY</text>

  <text x="755" y="246" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#FFFFFF">38%</text>
  <text x="755" y="270" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" letter-spacing="1.8" fill="#C084FC">PIPELINE</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<marker>` arrowheads for connector lines; endpoint dots are safer and remain editable.
- ❌ Simulating progress with `stroke-dashoffset` on a single stroked circle; use filled annular `<path>` segments for reliable PowerPoint geometry.
- ❌ Applying `filter` to `<line>` connectors; PowerPoint translation drops line filters, so glow should be on circles or arc paths.
- ❌ Using `<mask>` or clipping non-image shapes to create the arcs; construct the annular arc directly as a closed path.
- ❌ Relying on `skewX`, `skewY`, or matrix transforms for perspective HUD effects; keep the gauge geometry explicit.

## Composition notes
- Place explanatory copy on the left 35–40% of the slide; reserve the right 60% for the gauge so the arcs can feel large and cinematic.
- Anchor the gauge center below or near the bottom edge so only the upper semicircles are visible, creating a strong dashboard base.
- Keep ring thickness and gaps consistent; this is what makes the nested arcs feel engineered rather than decorative.
- Use bright gradients only for the active arcs and labels; keep tracks, guide rings, and background details muted to preserve hierarchy.