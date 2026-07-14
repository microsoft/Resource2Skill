# SVG Recipe — Cinematic 3D Recap & Scrolling Credits (电影回顾式3D致谢页)

## Visual mechanism
A dark cinematic stage pairs a left-side perspective “recap screen” with a soft floor reflection, while the right side uses strict dual-column movie credits typography. The slide feels like an executive keynote closing sequence: spatial, solemn, and appreciative.

## SVG primitives needed
- 1× full-slide `<rect>` for the deep radial-gradient background
- 2× large `<ellipse>` for atmospheric cyan/blue light blooms
- 18× tiny `<circle>` for distant cinematic particles/stars
- 2× `<clipPath>` with polygon shapes for the tilted screen crop and reflection crop
- 2× `<image>` using the same recap screenshot/photo source: one main screen, one faint reflection
- 5× `<path>` for the perspective screen frame, side thickness, bottom bevel, glass overlay, and reflection fade
- 8× `<line>` for floor perspective grid lines and subtle screen UI accents
- 1× `<filter id="softShadow">` for the floating screen shadow
- 1× `<filter id="cyanGlow">` for premium neon glows on key frame elements
- Multiple `<linearGradient>` / `<radialGradient>` fills for background, glass, metallic edges, strokes, and reflection fade
- 15× `<text>` blocks with explicit `width` for title, subtitle, screen label, and dual-column credits

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="48%" cy="44%" r="78%">
      <stop offset="0%" stop-color="#162744"/>
      <stop offset="45%" stop-color="#081321"/>
      <stop offset="100%" stop-color="#020509"/>
    </radialGradient>

    <radialGradient id="cyanBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#24d8ff" stop-opacity="0.28"/>
      <stop offset="70%" stop-color="#0b6a9b" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="screenStroke" x1="90" y1="140" x2="710" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#72f4ff"/>
      <stop offset="45%" stop-color="#1fa4ff"/>
      <stop offset="100%" stop-color="#725cff"/>
    </linearGradient>

    <linearGradient id="glassOverlay" x1="120" y1="160" x2="650" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="38%" stop-color="#62dfff" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.22"/>
    </linearGradient>

    <linearGradient id="edgeMetal" x1="650" y1="150" x2="735" y2="460" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#3c5e86"/>
      <stop offset="55%" stop-color="#10233c"/>
      <stop offset="100%" stop-color="#050912"/>
    </linearGradient>

    <linearGradient id="reflectionFade" x1="410" y1="460" x2="410" y2="675" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#52d9ff" stop-opacity="0.22"/>
      <stop offset="38%" stop-color="#153456" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#020509" stop-opacity="0.92"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="18" dy="24" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="screenClip" clipPathUnits="userSpaceOnUse">
      <polygon points="92,180 640,134 704,431 135,506"/>
    </clipPath>

    <clipPath id="reflectionClip" clipPathUnits="userSpaceOnUse">
      <polygon points="138,520 704,448 645,620 184,666"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <ellipse cx="465" cy="354" rx="445" ry="285" fill="url(#cyanBloom)"/>
  <ellipse cx="930" cy="342" rx="300" ry="260" fill="#182844" opacity="0.26"/>

  <g opacity="0.55">
    <circle cx="86" cy="82" r="1.4" fill="#9eefff"/><circle cx="204" cy="132" r="1.1" fill="#7fb7ff"/>
    <circle cx="342" cy="58" r="1.3" fill="#d9fbff"/><circle cx="612" cy="72" r="1.2" fill="#7de7ff"/>
    <circle cx="758" cy="112" r="1.1" fill="#96c8ff"/><circle cx="1136" cy="88" r="1.5" fill="#cdfaff"/>
    <circle cx="1210" cy="220" r="1.1" fill="#7de7ff"/><circle cx="1044" cy="610" r="1.2" fill="#9eefff"/>
    <circle cx="782" cy="650" r="1.0" fill="#8fbfff"/><circle cx="502" cy="628" r="1.2" fill="#d9fbff"/>
    <circle cx="248" cy="590" r="1.1" fill="#7de7ff"/><circle cx="74" cy="466" r="1.3" fill="#9eefff"/>
    <circle cx="914" cy="156" r="1.1" fill="#d9fbff"/><circle cx="1010" cy="268" r="1.2" fill="#7de7ff"/>
    <circle cx="1170" cy="480" r="1.1" fill="#96c8ff"/><circle cx="690" cy="540" r="1.0" fill="#cdfaff"/>
    <circle cx="428" cy="112" r="1.0" fill="#7fb7ff"/><circle cx="180" cy="310" r="1.1" fill="#d9fbff"/>
  </g>

  <g opacity="0.22">
    <line x1="0" y1="650" x2="1280" y2="610" stroke="#2fdcff" stroke-width="1"/>
    <line x1="0" y1="694" x2="1280" y2="646" stroke="#2fdcff" stroke-width="1"/>
    <line x1="122" y1="720" x2="522" y2="430" stroke="#1c8cc2" stroke-width="1"/>
    <line x1="360" y1="720" x2="582" y2="430" stroke="#1c8cc2" stroke-width="1"/>
    <line x1="650" y1="720" x2="650" y2="430" stroke="#1c8cc2" stroke-width="1"/>
    <line x1="920" y1="720" x2="720" y2="430" stroke="#1c8cc2" stroke-width="1"/>
  </g>

  <g id="tilted-recap-screen">
    <path d="M92 180 L640 134 L704 431 L135 506 Z" fill="#00040a" opacity="0.55" filter="url(#softShadow)"/>
    <image href="https://images.example.com/executive-keynote-recap-dashboard-screenshot.jpg"
           x="88" y="132" width="620" height="382" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#screenClip)"/>
    <path d="M92 180 L640 134 L704 431 L135 506 Z" fill="url(#glassOverlay)"/>
    <path d="M640 134 L704 431 L734 455 L668 154 Z" fill="url(#edgeMetal)" opacity="0.92"/>
    <path d="M135 506 L704 431 L734 455 L154 536 Z" fill="#07111e" opacity="0.95"/>
    <path d="M92 180 L640 134 L704 431 L135 506 Z" fill="none" stroke="url(#screenStroke)" stroke-width="4" filter="url(#cyanGlow)"/>
    <line x1="145" y1="226" x2="585" y2="190" stroke="#81f7ff" stroke-width="1.5" opacity="0.55"/>
    <line x1="180" y1="426" x2="640" y2="372" stroke="#35ffc7" stroke-width="2" opacity="0.38"/>
    <text x="160" y="264" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#ffffff" opacity="0.88">Q4 IMPACT RECAP</text>
    <text x="160" y="294" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9deeff" opacity="0.82">presentation highlights · metrics · milestones</text>
  </g>

  <g id="floor-reflection">
    <image href="https://images.example.com/executive-keynote-recap-dashboard-screenshot.jpg"
           x="116" y="444" width="610" height="236" preserveAspectRatio="xMidYMid slice"
           opacity="0.14" clip-path="url(#reflectionClip)"/>
    <path d="M138 520 L704 448 L645 620 L184 666 Z" fill="url(#reflectionFade)"/>
    <path d="M172 555 L650 492" stroke="#6beeff" stroke-width="1.3" opacity="0.12"/>
    <path d="M205 604 L608 548" stroke="#35ffc7" stroke-width="1.1" opacity="0.10"/>
  </g>

  <g id="credits">
    <text x="820" y="116" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#ffffff">THANK YOU</text>
    <text x="823" y="151" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#8fdcff" opacity="0.88">特别致谢 · END CREDITS</text>
    <line x1="930" y1="194" x2="930" y2="574" stroke="#2fdcff" stroke-width="1.5" opacity="0.34"/>

    <text x="902" y="220" width="205" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#96c8dc">Special Thanks</text>
    <text x="958" y="220" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">All Attendees</text>

    <text x="902" y="270" width="205" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#96c8dc">Content Strategy</text>
    <text x="958" y="270" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Product Team</text>

    <text x="902" y="320" width="205" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#96c8dc">Data Analysis</text>
    <text x="958" y="320" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Data Science Dept</text>

    <text x="902" y="370" width="205" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#96c8dc">Slide Design</text>
    <text x="958" y="370" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Creative Studio</text>

    <text x="902" y="420" width="205" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#96c8dc">Review &amp; QA</text>
    <text x="958" y="420" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Management Board</text>

    <text x="902" y="470" width="205" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#96c8dc">Final Production</text>
    <text x="958" y="470" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">Media Group</text>

    <text x="823" y="610" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7faec2" opacity="0.75">Static layout; add native PowerPoint upward motion to this credits group for a scrolling-credit finale.</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `transform="matrix(...)"` or `skewX/skewY` to force true perspective; these transforms are dropped by the PPT translator.
- ❌ Do not use SVG `<mask>` to fade the reflection. Use a semi-transparent reflection image plus a gradient-filled `<path>` overlay instead.
- ❌ Do not apply `clip-path` to a whole `<g>` or to vector shapes; only apply polygon clip paths directly to `<image>`.
- ❌ Do not use `<animate>` for scrolling credits. Build the static layout in SVG, then add PowerPoint motion animation afterward if needed.
- ❌ Do not put filters on `<line>` elements. Use glow/shadow filters on `<path>`, `<rect>`, `<ellipse>`, or `<text>` only.

## Composition notes
- Keep the tilted recap screen in the left 55% of the canvas, with the right edge pointing toward the credits column to create depth.
- Reserve the right 35–40% for credits; use a fixed vertical divider and aligned role/name columns for the movie-credit feeling.
- Use cyan sparingly: frame strokes, grid lines, small labels, and atmospheric glow. Names should remain crisp white for hierarchy.
- The reflection should be visible but subdued; it supports the cinematic floor illusion without competing with the main recap screen.