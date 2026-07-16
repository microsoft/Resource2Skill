# SVG Recipe — 3D Segmented Donut Chart Infographic

## Visual mechanism
A flat SVG annular chart is made to feel “3D” by drawing each donut segment as an elliptical arc, then adding darker offset side-wall paths underneath and a soft ambient shadow below. Around the object, balanced label cards connect to slices with clean leader lines, creating an executive-style exploded infographic.

## SVG primitives needed
- 1× `<rect>` for the pale executive-slide background
- 1× `<ellipse>` with blur filter for the ambient floor shadow
- 5× darker `<path>` side-wall shapes for the donut extrusion illusion
- 5× brighter `<path>` top-face annular segments for the segmented donut
- 2× `<ellipse>` for the central hub top face and subtle bevel/depth
- 5× `<line>` for straight editable connector leaders
- 5× small `<circle>` endpoint dots on slice anchors
- 5× `<rect>` label cards with rounded corners and soft shadow
- 6× `<text>` blocks with explicit `width` attributes for title, center hub text, and labels
- Multiple `<linearGradient>` definitions for premium segment shading
- 2× `<filter>` definitions: one blurred ambient shadow, one soft card shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#F8FAFD"/>
      <stop offset="1" stop-color="#E8EEF5"/>
    </linearGradient>

    <linearGradient id="redTop" x1="600" y1="260" x2="840" y2="390">
      <stop offset="0" stop-color="#FF6A63"/>
      <stop offset="1" stop-color="#D92323"/>
    </linearGradient>
    <linearGradient id="blueTop" x1="760" y1="330" x2="900" y2="500">
      <stop offset="0" stop-color="#55D6FF"/>
      <stop offset="1" stop-color="#269FD9"/>
    </linearGradient>
    <linearGradient id="greenTop" x1="500" y1="500" x2="800" y2="440">
      <stop offset="0" stop-color="#98C85F"/>
      <stop offset="1" stop-color="#456734"/>
    </linearGradient>
    <linearGradient id="goldTop" x1="380" y1="360" x2="560" y2="500">
      <stop offset="0" stop-color="#FFD766"/>
      <stop offset="1" stop-color="#E58A22"/>
    </linearGradient>
    <linearGradient id="violetTop" x1="400" y1="340" x2="650" y2="260">
      <stop offset="0" stop-color="#B987FF"/>
      <stop offset="1" stop-color="#6D42C7"/>
    </linearGradient>

    <linearGradient id="wallBlue" x1="820" y1="350" x2="820" y2="530">
      <stop offset="0" stop-color="#1E87BB"/>
      <stop offset="1" stop-color="#126087"/>
    </linearGradient>
    <linearGradient id="wallGreen" x1="640" y1="480" x2="640" y2="540">
      <stop offset="0" stop-color="#38572A"/>
      <stop offset="1" stop-color="#263C1D"/>
    </linearGradient>
    <linearGradient id="wallGold" x1="430" y1="370" x2="430" y2="530">
      <stop offset="0" stop-color="#B96B18"/>
      <stop offset="1" stop-color="#7F4810"/>
    </linearGradient>
    <linearGradient id="wallRed" x1="760" y1="270" x2="760" y2="390">
      <stop offset="0" stop-color="#B51E1E"/>
      <stop offset="1" stop-color="#7F1414"/>
    </linearGradient>
    <linearGradient id="wallViolet" x1="500" y1="260" x2="500" y2="380">
      <stop offset="0" stop-color="#5634A3"/>
      <stop offset="1" stop-color="#3D247A"/>
    </linearGradient>

    <filter id="ambientBlur" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
    <filter id="cardShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <text x="340" y="70" width="600" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#222B36">
    3D Segmented Donut Chart
  </text>
  <text x="340" y="105" width="600" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6D7785">
    Five equal strategic pillars around one central operating model
  </text>

  <ellipse cx="640" cy="452" rx="300" ry="76" fill="#111827" opacity="0.22" filter="url(#ambientBlur)"/>

  <!-- Extruded side walls, drawn first so top faces sit above them -->
  <path d="M640 265 A265 125 0 0 1 880 337 L880 375 A265 125 0 0 0 640 303 Z"
        fill="url(#wallRed)" opacity="0.82"/>
  <path d="M893 353 A265 125 0 0 1 817 483 L817 521 A265 125 0 0 0 893 391 Z"
        fill="url(#wallBlue)"/>
  <path d="M788 494 A265 125 0 0 1 504 496 L504 534 A265 125 0 0 0 788 532 Z"
        fill="url(#wallGreen)"/>
  <path d="M473 487 A265 125 0 0 1 383 360 L383 398 A265 125 0 0 0 473 525 Z"
        fill="url(#wallGold)" opacity="0.9"/>
  <path d="M394 343 A265 125 0 0 1 626 265 L626 303 A265 125 0 0 0 394 381 Z"
        fill="url(#wallViolet)" opacity="0.78"/>

  <!-- Top annular segments -->
  <path d="M640 265 A265 125 0 0 1 880 337 L747 366 A118 56 0 0 0 640 334 Z"
        fill="url(#redTop)" stroke="#F7FAFD" stroke-width="5"/>
  <path d="M893 353 A265 125 0 0 1 817 483 L719 432 A118 56 0 0 0 753 374 Z"
        fill="url(#blueTop)" stroke="#F7FAFD" stroke-width="5"/>
  <path d="M788 494 A265 125 0 0 1 504 496 L579 438 A118 56 0 0 0 706 436 Z"
        fill="url(#greenTop)" stroke="#F7FAFD" stroke-width="5"/>
  <path d="M473 487 A265 125 0 0 1 383 360 L526 376 A118 56 0 0 0 566 434 Z"
        fill="url(#goldTop)" stroke="#F7FAFD" stroke-width="5"/>
  <path d="M394 343 A265 125 0 0 1 626 265 L634 334 A118 56 0 0 0 531 369 Z"
        fill="url(#violetTop)" stroke="#F7FAFD" stroke-width="5"/>

  <!-- Central flush hub -->
  <ellipse cx="640" cy="407" rx="124" ry="60" fill="#AEB8C4" opacity="0.55"/>
  <ellipse cx="640" cy="390" rx="120" ry="58" fill="#FFFFFF" stroke="#D9E1EA" stroke-width="4"/>
  <text x="540" y="380" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#293241">
    <tspan x="640" dy="0">CORE</tspan>
    <tspan x="640" dy="22" font-size="15" font-weight="500" fill="#7A8696">STRATEGY</tspan>
  </text>

  <!-- Connectors -->
  <line x1="760" y1="307" x2="902" y2="206" stroke="#AAB5C2" stroke-width="2"/>
  <line x1="844" y1="410" x2="930" y2="350" stroke="#AAB5C2" stroke-width="2"/>
  <line x1="652" y1="505" x2="642" y2="585" stroke="#AAB5C2" stroke-width="2"/>
  <line x1="445" y1="428" x2="350" y2="492" stroke="#AAB5C2" stroke-width="2"/>
  <line x1="500" y1="310" x2="350" y2="242" stroke="#AAB5C2" stroke-width="2"/>

  <circle cx="760" cy="307" r="7" fill="#D92323" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="844" cy="410" r="7" fill="#269FD9" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="652" cy="505" r="7" fill="#456734" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="445" cy="428" r="7" fill="#E58A22" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="500" cy="310" r="7" fill="#6D42C7" stroke="#FFFFFF" stroke-width="3"/>

  <!-- Label cards -->
  <rect x="905" y="162" width="250" height="88" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="930" y="195" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#D92323">
    01 Discover
    <tspan x="930" dy="24" font-size="13" font-weight="400" fill="#657282">Map needs, signals, and stakeholder expectations.</tspan>
  </text>

  <rect x="930" y="306" width="250" height="88" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="955" y="339" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#269FD9">
    02 Design
    <tspan x="955" dy="24" font-size="13" font-weight="400" fill="#657282">Translate insights into a clear operating blueprint.</tspan>
  </text>

  <rect x="520" y="585" width="250" height="88" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="545" y="618" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#456734">
    03 Activate
    <tspan x="545" dy="24" font-size="13" font-weight="400" fill="#657282">Launch workstreams with owners and measurable cadence.</tspan>
  </text>

  <rect x="100" y="456" width="250" height="88" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="125" y="489" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#E58A22">
    04 Scale
    <tspan x="125" dy="24" font-size="13" font-weight="400" fill="#657282">Expand proven practices across teams and regions.</tspan>
  </text>

  <rect x="100" y="194" width="250" height="88" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="125" y="227" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#6D42C7">
    05 Improve
    <tspan x="125" dy="24" font-size="13" font-weight="400" fill="#657282">Review outcomes and feed learning back into the cycle.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on real SVG/PPT 3D transforms, perspective matrices, or `skewX/skewY`; simulate depth with editable offset paths instead.
- ❌ Do not use `marker-end` arrowheads on connector paths; use plain `<line>` connectors plus small endpoint `<circle>` dots.
- ❌ Do not apply filters to `<line>` connectors; shadows/glows should only be applied to cards, ellipses, paths, or text.
- ❌ Do not use `<mask>` or clip non-image objects to create the donut hole; build each slice as an annular `<path>` with outer and inner arcs.
- ❌ Do not use `<use>` to repeat slices or cards; duplicate the editable shapes directly.

## Composition notes
- Keep the donut centered slightly below mid-slide so the title breathes and the bottom label can fit without crowding.
- Use equal angular slice spans for conceptual frameworks; reserve unequal spans only when the visual is meant to show quantitative data.
- Draw side-wall paths before top faces, then add the central hub last so it appears flush and unified.
- Place labels in a left/right/top/bottom orbit with generous negative space; connector lines should be short, straight, and visually subordinate.