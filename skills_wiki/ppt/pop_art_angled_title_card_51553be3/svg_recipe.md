# SVG Recipe — Pop-Art Angled Title Card

## Visual mechanism
A hot split-color background is interrupted by a tilted stack of oversized flat cards, making the title feel like a physical poster slapped onto the slide. The headline gets comic-book depth through many duplicated, offset text layers that create a hard magenta extrusion instead of a blurry shadow.

## SVG primitives needed
- 1× `<rect>` for the full electric-purple background base
- 1× `<path>` for the hot-pink diagonal background split
- 2× `<path>` for extra angular cyan and navy background wedges
- 24× `<circle>` for hand-placed halftone dot clusters
- 2× `<path>` for pop-art lightning / burst accent shapes
- 2× `<rect>` for the tilted white back card and yellow front card
- 4× `<rect>` for tilted black edge strips, label tags, and small graphic accents
- 11× `<text>` for the dense magenta extrusion layers
- 1× `<text>` for the white headline face
- 2× `<text>` for small supporting label copy
- 1× `<filter id="softLift">` applied to the rear card for a subtle editable lift shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softLift" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="10" dy="12" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- split pop-art background -->
  <rect x="0" y="0" width="1280" height="720" fill="#411EE1"/>
  <path d="M0 0 H895 L306 720 H0 Z" fill="#FF0066"/>
  <path d="M925 0 H1280 V190 L1038 244 Z" fill="#00D9FF" opacity="0.95"/>
  <path d="M0 548 L385 500 L338 720 H0 Z" fill="#1A125F" opacity="0.75"/>

  <!-- halftone dots, individually drawn instead of pattern fills -->
  <circle cx="995" cy="312" r="16" fill="#FF0066" opacity="0.45"/>
  <circle cx="1044" cy="292" r="14" fill="#FF0066" opacity="0.42"/>
  <circle cx="1090" cy="272" r="12" fill="#FF0066" opacity="0.38"/>
  <circle cx="1134" cy="254" r="10" fill="#FF0066" opacity="0.34"/>
  <circle cx="1180" cy="236" r="8" fill="#FF0066" opacity="0.30"/>
  <circle cx="1018" cy="370" r="14" fill="#FF0066" opacity="0.40"/>
  <circle cx="1065" cy="350" r="12" fill="#FF0066" opacity="0.36"/>
  <circle cx="1110" cy="331" r="10" fill="#FF0066" opacity="0.32"/>
  <circle cx="1152" cy="313" r="8" fill="#FF0066" opacity="0.28"/>
  <circle cx="1195" cy="296" r="6" fill="#FF0066" opacity="0.24"/>

  <circle cx="94" cy="102" r="15" fill="#FFF000" opacity="0.45"/>
  <circle cx="146" cy="116" r="13" fill="#FFF000" opacity="0.40"/>
  <circle cx="199" cy="130" r="11" fill="#FFF000" opacity="0.35"/>
  <circle cx="252" cy="144" r="9" fill="#FFF000" opacity="0.30"/>
  <circle cx="118" cy="164" r="13" fill="#FFF000" opacity="0.38"/>
  <circle cx="171" cy="178" r="11" fill="#FFF000" opacity="0.33"/>
  <circle cx="224" cy="192" r="9" fill="#FFF000" opacity="0.28"/>
  <circle cx="278" cy="206" r="7" fill="#FFF000" opacity="0.24"/>

  <circle cx="1095" cy="610" r="18" fill="#00D9FF" opacity="0.40"/>
  <circle cx="1146" cy="592" r="15" fill="#00D9FF" opacity="0.34"/>
  <circle cx="1193" cy="574" r="12" fill="#00D9FF" opacity="0.29"/>
  <circle cx="1234" cy="558" r="9" fill="#00D9FF" opacity="0.24"/>
  <circle cx="1122" cy="666" r="14" fill="#00D9FF" opacity="0.30"/>
  <circle cx="1170" cy="648" r="10" fill="#00D9FF" opacity="0.24"/>

  <!-- comic accents -->
  <path d="M91 455 L132 432 L121 382 L160 415 L207 391 L184 441 L222 474 L168 468 L148 518 L132 468 Z"
        fill="#FFF000" stroke="#111111" stroke-width="6"/>
  <path d="M1110 92 L1162 66 L1142 119 L1198 126 L1147 153 L1166 206 L1119 169 L1074 205 L1088 150 L1040 123 L1096 117 Z"
        fill="#FF0066" stroke="#FFFFFF" stroke-width="6"/>

  <!-- tilted card system -->
  <g transform="rotate(-4 640 360)">
    <rect x="204" y="126" width="902" height="496" fill="#FFFFFF" filter="url(#softLift)"/>
    <rect x="172" y="94" width="902" height="496" fill="#FFF000"/>
    <rect x="172" y="570" width="902" height="20" fill="#111111" opacity="0.95"/>
    <rect x="1054" y="94" width="20" height="496" fill="#111111" opacity="0.95"/>

    <!-- small editorial label -->
    <rect x="224" y="132" width="232" height="42" fill="#111111"/>
    <text x="244" y="160" width="190" fill="#FFF000"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" letter-spacing="2">
      RETRO PULSE
    </text>

    <!-- magenta solid extrusion: duplicated editable text layers -->
    <text x="258" y="286" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="258" dy="0">How was your</tspan><tspan x="258" dy="96">onboarding?</tspan>
    </text>
    <text x="262" y="290" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="262" dy="0">How was your</tspan><tspan x="262" dy="96">onboarding?</tspan>
    </text>
    <text x="266" y="294" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="266" dy="0">How was your</tspan><tspan x="266" dy="96">onboarding?</tspan>
    </text>
    <text x="270" y="298" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="270" dy="0">How was your</tspan><tspan x="270" dy="96">onboarding?</tspan>
    </text>
    <text x="274" y="302" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="274" dy="0">How was your</tspan><tspan x="274" dy="96">onboarding?</tspan>
    </text>
    <text x="278" y="306" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="278" dy="0">How was your</tspan><tspan x="278" dy="96">onboarding?</tspan>
    </text>
    <text x="282" y="310" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="282" dy="0">How was your</tspan><tspan x="282" dy="96">onboarding?</tspan>
    </text>
    <text x="286" y="314" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="286" dy="0">How was your</tspan><tspan x="286" dy="96">onboarding?</tspan>
    </text>
    <text x="290" y="318" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="290" dy="0">How was your</tspan><tspan x="290" dy="96">onboarding?</tspan>
    </text>
    <text x="294" y="322" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="294" dy="0">How was your</tspan><tspan x="294" dy="96">onboarding?</tspan>
    </text>
    <text x="298" y="326" width="795" fill="#DC146E"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="298" dy="0">How was your</tspan><tspan x="298" dy="96">onboarding?</tspan>
    </text>

    <!-- headline face -->
    <text x="246" y="274" width="795" fill="#FFFFFF" stroke="#111111" stroke-width="2"
          font-family="Arial Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900">
      <tspan x="246" dy="0">How was your</tspan><tspan x="246" dy="96">onboarding?</tspan>
    </text>

    <rect x="760" y="512" width="255" height="44" fill="#111111"/>
    <text x="782" y="542" width="215" fill="#FFFFFF"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" letter-spacing="1.5">
      TEAM CHECK-IN
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<pattern>` for halftone dots; draw individual editable circles so the dots survive as PowerPoint shapes.
- ❌ Do not use a blurred PowerPoint-style shadow for the title extrusion; duplicate text layers with small offsets to keep the comic-book block effect sharp.
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` to fake the angled card; use `rotate(angle cx cy)` on the card group.
- ❌ Do not use `<textPath>` for energetic typography; keep the title as standard `<text>` / `<tspan>` so it remains editable.
- ❌ Do not rely on clipping or masks for the background split; use direct polygon-like `<path>` shapes.

## Composition notes
- Keep the tilted card stack at roughly 70–75% of slide width, centered, with enough background visible to make the diagonal split feel intentional.
- Use extreme saturation: hot pink, electric purple, bright yellow, white, black, and one optional cyan accent. Avoid muted corporate palettes.
- The title should dominate the slide; supporting labels are tiny editorial details, not competing content.
- Rotate the card and all text together by only 3–6 degrees. Larger angles reduce legibility and make the design feel chaotic rather than punchy.