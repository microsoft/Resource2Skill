# SVG Recipe — Orbital Motion & Path Dynamics

## Visual mechanism
A deep-space stage uses visible dashed trajectories, ghosted object positions, and directional streaks to imply continuous motion paths without requiring SVG animation. A bold tilted title banner, orbiting app/system icons, and a rocket following a curved path make the slide read as an energetic “motion paths” keynote cover.

## SVG primitives needed
- 1× `<rect>` for the orange outer frame
- 1× `<rect>` for the deep-space slide background
- 1× `<image>` for a nebula/space photo background
- 1× `<image>` clipped by a circular `<clipPath>` for the planet/earth crop
- 20+× `<circle>` for stars, logo dots, porthole rings, and glow accents
- 2× `<ellipse>` for orbit paths and planet glows
- 2× `<path>` for dashed curved motion trajectories
- 4× small `<path>` arrowheads to show direction along motion paths
- 1× tilted `<rect>` for the bright title banner
- 3× `<text>` elements with explicit `width` for title, subtitle label, and logo text
- 6× `<rect>` for Microsoft-style tile icon and PowerPoint card elements
- 12+× `<path>` for rocket body, fins, nose cone, shadows, flame, and orbiting ghost marks
- 3× `<linearGradient>` for space tinting, rocket metal, and flame
- 2× `<radialGradient>` for sun/planet glows
- 2× `<filter>` using blur/shadow for premium glow and depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="spaceTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#140018" stop-opacity="0.55"/>
      <stop offset="48%" stop-color="#09132f" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#020610" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="bannerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f4ff13"/>
      <stop offset="100%" stop-color="#ffff00"/>
    </linearGradient>
    <linearGradient id="rocketMetal" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#e9e9e9"/>
      <stop offset="100%" stop-color="#bdbdbd"/>
    </linearGradient>
    <linearGradient id="flameGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff36a"/>
      <stop offset="45%" stop-color="#ff4b1f"/>
      <stop offset="100%" stop-color="#ff004c"/>
    </linearGradient>
    <radialGradient id="planetGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#79f4ff" stop-opacity="0.75"/>
      <stop offset="55%" stop-color="#2e8dff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sunGrad" cx="45%" cy="40%" r="65%">
      <stop offset="0%" stop-color="#ff9b5d"/>
      <stop offset="55%" stop-color="#ff4c1a"/>
      <stop offset="100%" stop-color="#c41d00"/>
    </radialGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="7" dy="9"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="earthClip"><circle cx="934" cy="452" r="96"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ff8a22"/>
  <rect x="24" y="22" width="1232" height="676" fill="#070b1d"/>
  <image x="24" y="22" width="1232" height="676" preserveAspectRatio="xMidYMid slice" href="https://images.example.com/deep-nebula-starfield-for-motion-paths.jpg"/>
  <rect x="24" y="22" width="1232" height="676" fill="url(#spaceTint)"/>

  <circle cx="210" cy="84" r="2" fill="#ffffff" opacity="0.65"/><circle cx="420" cy="28" r="1.8" fill="#ffd7ff" opacity="0.55"/>
  <circle cx="570" cy="98" r="2.2" fill="#ffffff" opacity="0.7"/><circle cx="742" cy="55" r="1.4" fill="#7fdcff" opacity="0.7"/>
  <circle cx="1050" cy="108" r="2.4" fill="#ffffff" opacity="0.65"/><circle cx="1134" cy="286" r="2" fill="#56e8ff" opacity="0.65"/>
  <circle cx="82" cy="312" r="1.5" fill="#ffffff" opacity="0.5"/><circle cx="490" cy="350" r="2.4" fill="#ffffff" opacity="0.75"/>
  <circle cx="682" cy="292" r="1.7" fill="#ffb36b" opacity="0.7"/><circle cx="829" cy="642" r="2.2" fill="#ffffff" opacity="0.6"/>

  <path d="M120 520 C330 390 520 650 704 492 C820 392 944 250 1098 180" fill="none" stroke="#ffffff" stroke-width="3" stroke-opacity="0.42" stroke-dasharray="14 16"/>
  <path d="M676 500 C792 594 944 588 1088 470" fill="none" stroke="#fffd73" stroke-width="4" stroke-opacity="0.7" stroke-dasharray="18 14"/>
  <path d="M1090 179 l-25 4 l15 -21 z" fill="#ffffff" opacity="0.55"/>
  <path d="M1088 470 l-24 -8 l21 -15 z" fill="#fffd73" opacity="0.75"/>

  <g transform="rotate(-2 512 190)">
    <rect x="48" y="100" width="928" height="184" rx="25" fill="url(#bannerGrad)" filter="url(#softShadow)"/>
    <text x="78" y="242" width="860" font-family="Segoe UI, Microsoft YaHei" font-size="118" font-weight="800" fill="#5d00e8" stroke="#ffffff" stroke-width="2">Motion Paths</text>
  </g>

  <ellipse cx="610" cy="525" rx="190" ry="86" fill="none" stroke="#7bdcff" stroke-width="2" stroke-opacity="0.45" stroke-dasharray="10 11"/>
  <ellipse cx="610" cy="525" rx="260" ry="124" fill="none" stroke="#ffffff" stroke-width="2" stroke-opacity="0.22" stroke-dasharray="7 12"/>
  <circle cx="616" cy="516" r="112" fill="url(#sunGrad)" opacity="0.96"/>
  <path d="M616 404 A112 112 0 0 1 728 516 L616 516 Z" fill="#ffb07b" opacity="0.55"/>
  <path d="M616 516 L728 516 A112 112 0 0 1 616 628 Z" fill="#d81f00" opacity="0.45"/>

  <g filter="url(#softShadow)">
    <rect x="462" y="452" width="142" height="142" rx="10" fill="#f1370b"/>
    <rect x="476" y="463" width="132" height="132" rx="10" fill="#b62308" opacity="0.42"/>
    <text x="504" y="568" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="92" font-weight="800" fill="#ffffff">P</text>
  </g>

  <g transform="translate(86 438) rotate(-1)">
    <rect x="0" y="0" width="98" height="98" fill="#f25022"/>
    <rect x="106" y="-4" width="98" height="102" fill="#7fba00"/>
    <rect x="2" y="106" width="98" height="98" fill="#00a4ef"/>
    <rect x="110" y="106" width="98" height="98" fill="#ffb900"/>
  </g>

  <ellipse cx="934" cy="452" rx="120" ry="120" fill="url(#planetGlow)" filter="url(#glow)"/>
  <image x="838" y="356" width="192" height="192" preserveAspectRatio="xMidYMid slice" clip-path="url(#earthClip)" href="https://images.example.com/blue-earth-planet-from-space.jpg"/>
  <circle cx="934" cy="452" r="96" fill="none" stroke="#79f4ff" stroke-width="2" opacity="0.45"/>

  <g transform="translate(935 102)" filter="url(#softShadow)">
    <path d="M94 0 C145 58 176 168 168 292 C164 352 146 412 118 456 L70 462 C38 420 17 358 12 295 C3 170 35 58 94 0 Z" fill="url(#rocketMetal)" stroke="#050505" stroke-width="6"/>
    <path d="M94 0 C124 35 145 70 160 102 L29 104 C45 66 66 31 94 0 Z" fill="#ff0000" stroke="#050505" stroke-width="6"/>
    <path d="M28 300 C-12 320 -22 374 -16 430 C-2 390 18 364 42 360 Z" fill="#ff0000" stroke="#050505" stroke-width="6"/>
    <path d="M158 300 C199 316 214 370 205 428 C190 390 169 362 144 358 Z" fill="#ff0000" stroke="#050505" stroke-width="6"/>
    <circle cx="94" cy="205" r="42" fill="#c8c8c8" stroke="#050505" stroke-width="6"/>
    <circle cx="94" cy="205" r="28" fill="#e9fbff" stroke="#050505" stroke-width="5"/>
    <path d="M78 221 L110 189" stroke="#46dfff" stroke-width="8" stroke-linecap="round"/>
    <path d="M60 354 L130 348 L118 395 L72 397 Z" fill="#9e9e9e" stroke="#050505" stroke-width="6"/>
    <path d="M84 350 L96 470 M113 342 L121 478" stroke="#050505" stroke-width="7"/>
    <path d="M88 462 C70 493 76 520 93 546 C115 520 120 493 104 462 Z" fill="url(#flameGrad)" stroke="#ff1d22" stroke-width="5"/>
    <path d="M94 500 C86 516 88 529 95 541 C104 527 105 516 100 500 Z" fill="#fff36a"/>
  </g>

  <g transform="translate(1103 46)">
    <circle cx="66" cy="66" r="66" fill="#43d4e9" stroke="#070707" stroke-width="4"/>
    <path d="M6 68 C32 36 70 29 126 61" fill="none" stroke="#ffffff" stroke-width="18" opacity="0.35" stroke-dasharray="3 9"/>
    <text x="18" y="96" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="63" font-weight="900" font-style="italic" fill="#ffffff" stroke="#050505" stroke-width="3">TM</text>
  </g>

  <text x="54" y="675" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#b8c9ff" opacity="0.9">DASHED TRAJECTORIES + GHOST POSITIONS COMMUNICATE CONTINUOUS MOTION</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateMotion>`; PPT-Master will not translate these into editable PowerPoint animations.
- ❌ `<textPath>` for labels following the orbit; use ordinary rotated `<text>` blocks with explicit `width` instead.
- ❌ `marker-end` arrowheads on curved paths; draw arrowheads manually as small `<path>` triangles.
- ❌ Applying `filter` to `<line>` elements; use `<path>` or shape strokes for glowing trajectories.
- ❌ Clipping dashed orbit shapes; only apply `clip-path` to `<image>` elements if a circular or rounded photo crop is needed.

## Composition notes
- Keep the title in the upper-left/top band and tilt it slightly; the center and right side should remain available for the path system and rocket.
- Use a dark photographic or gradient space background so bright paths, yellow banners, and red rocket details pop.
- Show motion statically with dashed curves, orbit ellipses, arrowhead triangles, and repeated/ghosted positions rather than actual SVG animation.
- Balance the visual rhythm with one large kinetic hero object on the right, one circular system hub near the lower center, and small app/process icons orbiting or anchoring the left side.