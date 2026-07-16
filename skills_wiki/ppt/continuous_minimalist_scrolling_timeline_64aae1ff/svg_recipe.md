# SVG Recipe — Continuous Minimalist Scrolling Timeline

## Visual mechanism
A centered, full-bleed horizontal axis creates the illusion that the viewer is panning across one long timeline canvas. Sparse alternating milestone blocks, edge-overlapping abstract ink clouds, and partial off-slide elements make adjacent slides feel stitched together during a native PowerPoint Push transition.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 1× `<line>` for the full-bleed continuous timeline axis
- 4× `<line>` for vertical milestone connector stems
- 6× `<circle>` for main nodes plus partial edge-continuation nodes
- 8× `<circle>` for node halos and micro accent dots
- 10–16× blurred `<circle>` for abstract powder / ink cloud particles at slide edges
- 4–6× blurred organic `<path>` shapes for premium edge splashes
- 4× small `<path>` diamond ticks for milestone emphasis
- 10× `<text>` elements for title, subtitle, milestone years, and multiline descriptions; every text element must include `width`
- 1× `<linearGradient>` for a subtle metallic-gray axis stroke
- 1× `<radialGradient>` for ink-cloud depth
- 2× `<filter>` definitions: one soft blur for powder shapes and one subtle shadow for milestone node halos

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="axisGrad" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E7E5E5"/>
      <stop offset="0.18" stop-color="#D0CECE"/>
      <stop offset="0.82" stop-color="#D0CECE"/>
      <stop offset="1" stop-color="#E7E5E5"/>
    </linearGradient>

    <radialGradient id="inkGrad" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#262626" stop-opacity="0.38"/>
      <stop offset="0.58" stop-color="#3B3B3B" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#262626" stop-opacity="0"/>
    </radialGradient>

    <filter id="powderBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <filter id="nodeShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="72" y="78" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="3.5" fill="#262626">
    PRODUCT EVOLUTION
  </text>
  <text x="72" y="108" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="400" letter-spacing="0.8" fill="#777777">
    A continuous roadmap designed to flow slide-to-slide with a horizontal push transition
  </text>

  <!-- left edge powder cloud: duplicate the matching right-side half on the previous slide -->
  <circle cx="-18" cy="348" r="104" fill="url(#inkGrad)" filter="url(#powderBlur)" opacity="0.85"/>
  <circle cx="36" cy="394" r="74" fill="url(#inkGrad)" filter="url(#powderBlur)" opacity="0.42"/>
  <circle cx="78" cy="316" r="38" fill="#262626" filter="url(#powderBlur)" opacity="0.14"/>
  <path d="M-70 314 C-24 246, 64 258, 92 318 C118 374, 50 430, -26 404 C-86 384, -114 350, -70 314 Z"
        fill="#2B2B2B" filter="url(#powderBlur)" opacity="0.18"/>
  <path d="M14 250 C42 238, 76 254, 84 286 C92 318, 56 336, 28 318 C0 300, -10 266, 14 250 Z"
        fill="#3B3B3B" filter="url(#powderBlur)" opacity="0.16"/>

  <!-- right edge powder cloud: carry this same shape onto the next slide's left edge -->
  <circle cx="1296" cy="365" r="118" fill="url(#inkGrad)" filter="url(#powderBlur)" opacity="0.82"/>
  <circle cx="1238" cy="310" r="68" fill="url(#inkGrad)" filter="url(#powderBlur)" opacity="0.38"/>
  <circle cx="1192" cy="414" r="44" fill="#262626" filter="url(#powderBlur)" opacity="0.13"/>
  <path d="M1208 302 C1260 236, 1348 270, 1372 340 C1392 398, 1322 448, 1244 416 C1184 392, 1164 356, 1208 302 Z"
        fill="#252525" filter="url(#powderBlur)" opacity="0.18"/>
  <path d="M1172 382 C1202 360, 1242 372, 1252 406 C1262 440, 1226 466, 1192 450 C1158 434, 1144 404, 1172 382 Z"
        fill="#3B3B3B" filter="url(#powderBlur)" opacity="0.14"/>

  <!-- full-bleed continuous axis -->
  <line x1="-80" y1="360" x2="1360" y2="360" stroke="url(#axisGrad)" stroke-width="3"/>

  <!-- partial edge nodes imply the timeline continues beyond the slide -->
  <circle cx="-36" cy="360" r="8" fill="#FFFFFF" stroke="#D0CECE" stroke-width="2"/>
  <circle cx="1316" cy="360" r="8" fill="#FFFFFF" stroke="#D0CECE" stroke-width="2"/>

  <!-- milestone stems -->
  <line x1="175" y1="360" x2="175" y2="238" stroke="#D0CECE" stroke-width="2"/>
  <line x1="485" y1="360" x2="485" y2="486" stroke="#D0CECE" stroke-width="2"/>
  <line x1="795" y1="360" x2="795" y2="238" stroke="#D0CECE" stroke-width="2"/>
  <line x1="1105" y1="360" x2="1105" y2="486" stroke="#D0CECE" stroke-width="2"/>

  <!-- main nodes -->
  <circle cx="175" cy="360" r="17" fill="#FFFFFF" stroke="#D0CECE" stroke-width="2.5" filter="url(#nodeShadow)"/>
  <circle cx="175" cy="360" r="7" fill="#262626"/>
  <circle cx="485" cy="360" r="17" fill="#FFFFFF" stroke="#D0CECE" stroke-width="2.5" filter="url(#nodeShadow)"/>
  <circle cx="485" cy="360" r="7" fill="#262626"/>
  <circle cx="795" cy="360" r="17" fill="#FFFFFF" stroke="#D0CECE" stroke-width="2.5" filter="url(#nodeShadow)"/>
  <circle cx="795" cy="360" r="7" fill="#262626"/>
  <circle cx="1105" cy="360" r="17" fill="#FFFFFF" stroke="#D0CECE" stroke-width="2.5" filter="url(#nodeShadow)"/>
  <circle cx="1105" cy="360" r="7" fill="#262626"/>

  <!-- small diamond ticks -->
  <path d="M175 226 L181 232 L175 238 L169 232 Z" fill="#262626"/>
  <path d="M485 498 L491 504 L485 510 L479 504 Z" fill="#262626"/>
  <path d="M795 226 L801 232 L795 238 L789 232 Z" fill="#262626"/>
  <path d="M1105 498 L1111 504 L1105 510 L1099 504 Z" fill="#262626"/>

  <!-- milestone 1 -->
  <text x="72" y="177" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#262626">
    2016
  </text>
  <text x="72" y="205" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" font-weight="400" fill="#3B3B3B">
    <tspan x="72" dy="0">Prototype validated with</tspan>
    <tspan x="72" dy="18">founding customers and</tspan>
    <tspan x="72" dy="18">first platform architecture.</tspan>
  </text>

  <!-- milestone 2 -->
  <text x="382" y="551" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#262626">
    2018
  </text>
  <text x="382" y="579" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" font-weight="400" fill="#3B3B3B">
    <tspan x="382" dy="0">Public launch, commercial</tspan>
    <tspan x="382" dy="18">packaging, and first wave</tspan>
    <tspan x="382" dy="18">of enterprise adoption.</tspan>
  </text>

  <!-- milestone 3 -->
  <text x="692" y="177" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#262626">
    2021
  </text>
  <text x="692" y="205" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" font-weight="400" fill="#3B3B3B">
    <tspan x="692" dy="0">Global expansion begins;</tspan>
    <tspan x="692" dy="18">infrastructure is rebuilt</tspan>
    <tspan x="692" dy="18">for scale and resilience.</tspan>
  </text>

  <!-- milestone 4 -->
  <text x="1002" y="551" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#262626">
    2024
  </text>
  <text x="1002" y="579" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" font-weight="400" fill="#3B3B3B">
    <tspan x="1002" dy="0">AI-native product suite</tspan>
    <tspan x="1002" dy="18">unifies analytics, workflow,</tspan>
    <tspan x="1002" dy="18">and customer intelligence.</tspan>
  </text>

  <!-- restrained powder speckles -->
  <circle cx="115" cy="300" r="3" fill="#262626" opacity="0.22"/>
  <circle cx="1038" cy="425" r="2.5" fill="#262626" opacity="0.18"/>
  <circle cx="1224" cy="266" r="3.5" fill="#262626" opacity="0.16"/>
  <circle cx="48" cy="448" r="2.5" fill="#262626" opacity="0.18"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the timeline at the slide edges; use full-bleed lines and off-canvas shapes instead.
- ❌ Do not use `<use>` or `<symbol>` to repeat milestone nodes; duplicate the editable circles and lines directly.
- ❌ Do not apply filters to `<line>` elements; shadows and blur should be reserved for circles, paths, rects, or text.
- ❌ Do not use `marker-end` arrows on the timeline axis; this pattern should feel continuous, not directional or finite.
- ❌ Do not omit `width` on `<text>` elements, or PowerPoint text layout will be unreliable.
- ❌ Do not overcrowd the slide with too many milestones; the scrolling illusion depends on whitespace and pacing.

## Composition notes
- Keep the timeline axis exactly centered vertically around `y=360`, extending past both slide edges to support the Push-transition illusion.
- Use 3–4 milestones per slide, alternating above and below the axis; leave generous negative space between text blocks.
- Place abstract ink or powder shapes partially off the left and right edges; repeat the opposite half on neighboring slides for seamless continuity.
- Maintain a monochrome rhythm: charcoal for emphasis, mid-gray for structure, white for breathing room.