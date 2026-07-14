# SVG Recipe — Premium Industrial Dark Grid (Grayscale & Gold)

## Visual mechanism
A premium editorial layout built from a dark slate canvas, strict grayscale industrial photography, and mustard-gold structural accents. The key is to remove color from imagery and reintroduce color only through precise geometric UI blocks, dividers, and metric highlights.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark slate background
- 1× `<radialGradient>` for a subtle vignette glow behind the typography area
- 1× `<linearGradient>` for gold pedestal blocks and accent bars
- 3× `<image>` for pre-grayscaled industrial / architecture portrait photos
- 3× `<clipPath>` with rectangular crops applied to the images
- 3× `<rect>` for gold pedestal blocks under each image card
- 3× `<rect>` for dark metric strips inside the gold pedestals
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` for premium card depth
- 1× `<filter id="softGlow">` using `feGaussianBlur` for a muted gold glow accent
- Multiple `<rect>` hairlines for grid dividers, header rules, and architectural alignment marks
- Multiple `<text>` elements with explicit `width` attributes for headline, subtitle, labels, metrics, and body copy
- Several `<path>` elements for bracket-like gold corner accents and angular industrial decoration

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2f2f2f"/>
      <stop offset="65%" stop-color="#393939"/>
      <stop offset="100%" stop-color="#242424"/>
    </linearGradient>

    <radialGradient id="rightGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#6a5a2b" stop-opacity="0.32"/>
      <stop offset="55%" stop-color="#6a5a2b" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#6a5a2b" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f0c85c"/>
      <stop offset="45%" stop-color="#dab03c"/>
      <stop offset="100%" stop-color="#a77d20"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="145%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="13" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="photoCropA">
      <rect x="70" y="185" width="220" height="300"/>
    </clipPath>
    <clipPath id="photoCropB">
      <rect x="318" y="185" width="220" height="300"/>
    </clipPath>
    <clipPath id="photoCropC">
      <rect x="566" y="185" width="220" height="300"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="1015" cy="365" rx="310" ry="250" fill="url(#rightGlow)"/>

  <rect x="48" y="48" width="1184" height="1.5" fill="#767676" opacity="0.42"/>
  <rect x="48" y="672" width="1184" height="1.5" fill="#767676" opacity="0.28"/>
  <rect x="836" y="92" width="1.5" height="532" fill="#d4d4d4" opacity="0.18"/>
  <rect x="70" y="154" width="716" height="1.5" fill="#d4d4d4" opacity="0.34"/>

  <text x="70" y="96" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff" letter-spacing="2">
    INDUSTRIAL GROWTH INDEX
  </text>
  <text x="70" y="128" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#dab03c" letter-spacing="1.4">
    GRAYSCALE ASSETS · GOLD STRUCTURAL HIERARCHY
  </text>

  <rect x="640" y="88" width="146" height="34" fill="url(#goldGrad)"/>
  <text x="656" y="110" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#282828" letter-spacing="1">
    FY 2026
  </text>

  <g filter="url(#cardShadow)">
    <image x="70" y="185" width="220" height="300" preserveAspectRatio="xMidYMid slice"
      clip-path="url(#photoCropA)"
      href="https://images.example.com/grayscale-industrial-architecture-tower-portrait-01.jpg"/>
    <rect x="70" y="485" width="220" height="104" fill="url(#goldGrad)"/>
    <rect x="70" y="555" width="220" height="34" fill="#252525" opacity="0.92"/>
  </g>

  <g filter="url(#cardShadow)">
    <image x="318" y="185" width="220" height="300" preserveAspectRatio="xMidYMid slice"
      clip-path="url(#photoCropB)"
      href="https://images.example.com/grayscale-factory-steel-beams-portrait-02.jpg"/>
    <rect x="318" y="485" width="220" height="104" fill="url(#goldGrad)"/>
    <rect x="318" y="555" width="220" height="34" fill="#252525" opacity="0.92"/>
  </g>

  <g filter="url(#cardShadow)">
    <image x="566" y="185" width="220" height="300" preserveAspectRatio="xMidYMid slice"
      clip-path="url(#photoCropC)"
      href="https://images.example.com/grayscale-urban-construction-crane-portrait-03.jpg"/>
    <rect x="566" y="485" width="220" height="104" fill="url(#goldGrad)"/>
    <rect x="566" y="555" width="220" height="34" fill="#252525" opacity="0.92"/>
  </g>

  <text x="88" y="520" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#282828" letter-spacing="0.8">
    MATERIALS
  </text>
  <text x="88" y="546" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3a321e">
    Supply resilience
  </text>
  <text x="88" y="578" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#ffffff">
    +18.4%
  </text>
  <text x="180" y="578" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#cfcfcf">
    YoY delta
  </text>

  <text x="336" y="520" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#282828" letter-spacing="0.8">
    CAPACITY
  </text>
  <text x="336" y="546" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3a321e">
    Utilization lift
  </text>
  <text x="336" y="578" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#ffffff">
    82.7%
  </text>
  <text x="428" y="578" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#cfcfcf">
    active load
  </text>

  <text x="584" y="520" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#282828" letter-spacing="0.8">
    EXPANSION
  </text>
  <text x="584" y="546" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#3a321e">
    New asset pipeline
  </text>
  <text x="584" y="578" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#ffffff">
    14
  </text>
  <text x="676" y="578" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#cfcfcf">
    sites live
  </text>

  <rect x="870" y="150" width="76" height="6" fill="url(#goldGrad)"/>
  <text x="870" y="216" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#ffffff" letter-spacing="-0.8">
    Top quality
  </text>
  <text x="870" y="270" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#ffffff" letter-spacing="-0.8">
    industrial design
  </text>
  <text x="872" y="314" width="278" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#dab03c" letter-spacing="1.2">
    EXECUTIVE OPERATIONS SNAPSHOT
  </text>

  <text x="872" y="365" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#d8d8d8">
    <tspan x="872" dy="0">A controlled grayscale image system keeps</tspan>
    <tspan x="872" dy="24">mixed-source photography visually unified.</tspan>
    <tspan x="872" dy="24">Gold blocks carry hierarchy, metrics, and</tspan>
    <tspan x="872" dy="24">navigation without competing with the image grid.</tspan>
  </text>

  <rect x="872" y="493" width="94" height="94" fill="#2b2b2b" stroke="#dab03c" stroke-width="1.5"/>
  <text x="895" y="536" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff">
    3×
  </text>
  <text x="887" y="565" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#dab03c" letter-spacing="1">
    GRID CARDS
  </text>

  <rect x="988" y="493" width="194" height="94" fill="#2b2b2b" stroke="#5f5f5f" stroke-width="1"/>
  <text x="1010" y="528" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ffffff" letter-spacing="0.7">
    COLOR RULE
  </text>
  <text x="1010" y="558" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#bdbdbd">
    Only gold accents carry saturation.
  </text>

  <path d="M54 178 L54 144 L88 144" fill="none" stroke="#dab03c" stroke-width="3"/>
  <path d="M802 610 L802 642 L770 642" fill="none" stroke="#dab03c" stroke-width="3"/>
  <path d="M1188 142 L1220 142 L1220 174" fill="none" stroke="#dab03c" stroke-width="3"/>
  <path d="M1058 646 L1182 646 L1208 620" fill="none" stroke="#dab03c" stroke-width="2" opacity="0.7"/>

  <circle cx="830" cy="154" r="5" fill="#dab03c" filter="url(#softGlow)"/>
  <circle cx="830" cy="154" r="3" fill="#f0c85c"/>
</svg>
```

## Avoid in this skill
- ❌ SVG filter-based grayscale conversion such as `feColorMatrix`; instead, use already-grayscaled image assets before insertion.
- ❌ Colorful photos that compete with the mustard accent system.
- ❌ Rounded, playful cards or soft pastel backgrounds; this style depends on hard-edged industrial geometry.
- ❌ Loose spacing between image and pedestal blocks; the photo must sit flush on the gold block to create a single architectural unit.
- ❌ Applying `clip-path` to rectangles or groups; apply clips only to `<image>` elements for reliable PowerPoint translation.

## Composition notes
- Keep the left 60–65% of the slide as the dense image/data grid; reserve the right 35–40% for large typography and narrative copy.
- Use dark slate as the dominant field, grayscale images as texture, and gold only for hierarchy, labels, rules, and metric pedestals.
- Align photo widths exactly to their gold blocks; avoid padding at the seam between image and pedestal.
- Add thin gray dividers and small gold bracket paths to make the layout feel engineered, architectural, and executive.