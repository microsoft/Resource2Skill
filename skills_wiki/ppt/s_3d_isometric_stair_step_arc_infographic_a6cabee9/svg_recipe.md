# SVG Recipe — 3D Isometric Stair-Step Arc Infographic

## Visual mechanism
A 270-degree annular arc is split into six elliptical wedge segments, then each segment receives a darker offset side wall with progressively larger depth to create an isometric “stair-step” extrusion. Floating white numbers sit on the top faces, while peripheral labels explain each step without competing with the central 3D hero form.

## SVG primitives needed
- 6× `<path>` for the colored top annular arc segments
- 6× `<path>` for the darker outer extrusion walls, each with a different down/right offset
- 1× `<ellipse>` for the soft ground shadow below the full 3D structure
- 6× `<linearGradient>` fills for teal-to-navy top-face lighting
- 1× `<filter id="softShadow">` applied to the ground shadow / optional text emphasis
- 6× `<text>` for floating white step numbers on the arc surfaces
- 6× `<line>` for thin connector rules from arc to labels
- 12× `<text>` for title/body labels around the infographic
- 1× `<text>` for the main slide title and 1× subtitle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="g1" x1="430" y1="240" x2="850" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#32d7c7"/><stop offset="1" stop-color="#1db3a6"/>
    </linearGradient>
    <linearGradient id="g2" x1="400" y1="240" x2="850" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#24c8bb"/><stop offset="1" stop-color="#18968c"/>
    </linearGradient>
    <linearGradient id="g3" x1="390" y1="210" x2="850" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2aa8bd"/><stop offset="1" stop-color="#1a7e92"/>
    </linearGradient>
    <linearGradient id="g4" x1="430" y1="190" x2="890" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#237b9b"/><stop offset="1" stop-color="#165f7d"/>
    </linearGradient>
    <linearGradient id="g5" x1="500" y1="180" x2="930" y2="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2b5f88"/><stop offset="1" stop-color="#214365"/>
    </linearGradient>
    <linearGradient id="g6" x1="560" y1="190" x2="940" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#243f61"/><stop offset="1" stop-color="#1c304a"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="18"/>
      <feOffset dx="18" dy="28"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="numGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
      <feOffset dx="0" dy="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f5f8fb"/>
  <text x="70" y="70" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#263241">Six-Step Growth Architecture</text>
  <text x="72" y="105" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7a8794">Isometric stair-step arc for process progression, maturity models, and phased strategy roadmaps.</text>

  <ellipse cx="670" cy="442" rx="325" ry="95" fill="#26384d" opacity="0.18" filter="url(#softShadow)"/>

  <!-- progressively deeper outer side walls -->
  <path d="M630 490 A260 130 0 0 1 446.2 451.9 L462.2 481.9 A260 130 0 0 0 646 520 Z" fill="#128477"/>
  <path d="M446.2 451.9 A260 130 0 0 1 370 360 L388 404 A260 130 0 0 0 464.2 495.9 Z" fill="#116f72"/>
  <path d="M370 360 A260 130 0 0 1 446.2 268.1 L466.2 326.1 A260 130 0 0 0 390 418 Z" fill="#135d70"/>
  <path d="M446.2 268.1 A260 130 0 0 1 630 230 L652 302 A260 130 0 0 0 468.2 340.1 Z" fill="#104b67"/>
  <path d="M630 230 A260 130 0 0 1 813.8 268.1 L837.8 354.1 A260 130 0 0 0 654 316 Z" fill="#18344f"/>
  <path d="M813.8 268.1 A260 130 0 0 1 890 360 L916 460 A260 130 0 0 0 839.8 368.1 Z" fill="#14283f"/>

  <!-- top annular arc segments -->
  <path d="M630 490 A260 130 0 0 1 446.2 451.9 L527.5 411.3 A145 72.5 0 0 0 630 432.5 Z" fill="url(#g1)" stroke="#ffffff" stroke-width="2"/>
  <path d="M446.2 451.9 A260 130 0 0 1 370 360 L485 360 A145 72.5 0 0 0 527.5 411.3 Z" fill="url(#g2)" stroke="#ffffff" stroke-width="2"/>
  <path d="M370 360 A260 130 0 0 1 446.2 268.1 L527.5 308.7 A145 72.5 0 0 0 485 360 Z" fill="url(#g3)" stroke="#ffffff" stroke-width="2"/>
  <path d="M446.2 268.1 A260 130 0 0 1 630 230 L630 287.5 A145 72.5 0 0 0 527.5 308.7 Z" fill="url(#g4)" stroke="#ffffff" stroke-width="2"/>
  <path d="M630 230 A260 130 0 0 1 813.8 268.1 L732.5 308.7 A145 72.5 0 0 0 630 287.5 Z" fill="url(#g5)" stroke="#ffffff" stroke-width="2"/>
  <path d="M813.8 268.1 A260 130 0 0 1 890 360 L775 360 A145 72.5 0 0 0 732.5 308.7 Z" fill="url(#g6)" stroke="#ffffff" stroke-width="2"/>

  <!-- floating numbers -->
  <text x="548" y="462" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff" filter="url(#numGlow)">01</text>
  <text x="421" y="407" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff" filter="url(#numGlow)">02</text>
  <text x="420" y="330" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff" filter="url(#numGlow)">03</text>
  <text x="548" y="275" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff" filter="url(#numGlow)">04</text>
  <text x="704" y="275" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff" filter="url(#numGlow)">05</text>
  <text x="810" y="330" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff" filter="url(#numGlow)">06</text>

  <!-- label connectors -->
  <line x1="540" y1="456" x2="250" y2="555" stroke="#9fb3c3" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="430" y1="398" x2="220" y2="410" stroke="#9fb3c3" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="430" y1="322" x2="250" y2="235" stroke="#9fb3c3" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="568" y1="262" x2="930" y2="175" stroke="#9fb3c3" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="720" y1="262" x2="1015" y2="315" stroke="#9fb3c3" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="825" y1="325" x2="1010" y2="505" stroke="#9fb3c3" stroke-width="1.5" stroke-dasharray="5 5"/>

  <!-- peripheral labels -->
  <text x="78" y="555" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1db3a6">Discover</text>
  <text x="78" y="580" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667685">Map the opportunity space and align on customer needs.</text>

  <text x="70" y="405" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#18968c">Prioritize</text>
  <text x="70" y="430" width="275" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667685">Score initiatives by impact, readiness, and strategic fit.</text>

  <text x="105" y="225" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1a7e92">Design</text>
  <text x="105" y="250" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667685">Translate the strategy into a measurable operating blueprint.</text>

  <text x="930" y="165" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#165f7d">Build</text>
  <text x="930" y="190" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667685">Create the first scalable version with clear ownership.</text>

  <text x="1015" y="305" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#214365">Scale</text>
  <text x="1015" y="330" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667685">Extend the model across teams, channels, and regions.</text>

  <text x="1010" y="505" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1c304a">Optimize</text>
  <text x="1010" y="530" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#667685">Use feedback loops to compound gains and remove friction.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on PowerPoint-only 3D extrusion tags; approximate depth with editable SVG paths instead.
- ❌ Do not use `<mask>` for the donut hole; build each annular slice as a real compound-looking path.
- ❌ Do not use `marker-end` on connector paths; if arrows are needed, draw arrowheads manually with small paths.
- ❌ Do not apply `filter` to `<line>` connectors; shadows on lines are dropped by the translator.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for isometric perspective; precompute the elliptical arc coordinates directly.

## Composition notes
- Keep the 3D arc centered and slightly below midline so the extrusion has room to descend into the soft ground shadow.
- Reserve the outer left and right thirds for labels; the central 50% should remain dominated by the isometric stair form.
- Use a single analogous palette from bright teal to dark navy so the sequence reads as both ordered and premium.
- Put numbers directly on the top faces, but keep explanatory text outside the chart to preserve the clean architectural geometry.