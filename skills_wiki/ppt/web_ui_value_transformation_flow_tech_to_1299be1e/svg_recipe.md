# SVG Recipe — Web-UI Value Transformation Flow (Tech-to-Revenue)

## Visual mechanism
A clean SaaS-style process graphic shows stacked “technology input” UI cards on the left transforming through a central directional connector into a golden “revenue outcome” card on the right. The transformation is reinforced with depth, shadows, blue-to-gold color contrast, small UI details, and icon-like vector illustrations.

## SVG primitives needed
- 1× full-slide `<rect>` for the pale app-like background
- 2× decorative blurred `<path>` blobs for soft blue/gold ambient depth
- 5× `<linearGradient>` definitions for background tint, blue UI cards, gold UI cards, arrow accent, and chips
- 2× `<filter>` definitions: one soft drop shadow for cards, one glow for ambient blobs/accent elements
- 5× rounded `<rect>` for the overlapping left input card stack and inner UI panels
- 4× rounded `<rect>` for the right revenue card, inner dashboard panel, CTA pill, and metric strip
- 1× `<line>` for the main connector shaft
- 1× triangular `<path>` for the arrowhead, instead of relying on marker-end
- 8× small `<circle>` elements for data particles and decorative UI status dots
- 6× `<path>` elements for editable vector icons: AI chip, circuit traces, coin stack, revenue bag, sparkle, and upward graph line
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, card labels, values, and microcopy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFD"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="blueCard" x1="250" y1="230" x2="520" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2B7CFF"/>
      <stop offset="100%" stop-color="#0D52D6"/>
    </linearGradient>
    <linearGradient id="blueDark" x1="220" y1="210" x2="475" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1C66E8"/>
      <stop offset="100%" stop-color="#083B9E"/>
    </linearGradient>
    <linearGradient id="goldCard" x1="760" y1="220" x2="1045" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFD66B"/>
      <stop offset="100%" stop-color="#FFAB00"/>
    </linearGradient>
    <linearGradient id="arrowGrad" x1="560" y1="360" x2="720" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8FA3B8"/>
      <stop offset="100%" stop-color="#FFB72A"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.04 0 0 0 0 0.10 0 0 0 0 0.18 0 0 0 0.20 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M70,120 C170,40 295,60 330,150 C365,242 255,300 160,275 C63,250 0,198 70,120 Z" fill="#DDEBFF" opacity="0.75" filter="url(#softGlow)"/>
  <path d="M1000,110 C1130,50 1248,115 1240,235 C1230,360 1080,366 990,300 C900,235 890,162 1000,110 Z" fill="#FFE4A7" opacity="0.70" filter="url(#softGlow)"/>

  <text x="120" y="82" width="1040" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800" fill="#1E2832">
    Turn AI Workflows into Revenue Engines
  </text>
  <text x="120" y="124" width="1040" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#657280">
    From one-click generation to commercial monetization — a simple input/output value story.
  </text>

  <rect x="236" y="236" width="252" height="246" rx="30" fill="url(#blueDark)" opacity="0.92" filter="url(#cardShadow)"/>
  <rect x="274" y="266" width="260" height="252" rx="32" fill="url(#blueCard)" filter="url(#cardShadow)"/>
  <rect x="306" y="300" width="196" height="34" rx="17" fill="#FFFFFF" opacity="0.18"/>
  <circle cx="328" cy="317" r="6" fill="#B9D7FF"/>
  <circle cx="348" cy="317" r="6" fill="#B9D7FF" opacity="0.75"/>
  <circle cx="368" cy="317" r="6" fill="#B9D7FF" opacity="0.55"/>

  <rect x="318" y="360" width="148" height="112" rx="24" fill="#FFFFFF" opacity="0.16"/>
  <path d="M360,380 H424 Q434,380 434,390 V442 Q434,452 424,452 H360 Q350,452 350,442 V390 Q350,380 360,380 Z" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.94"/>
  <path d="M372,398 H412 M372,418 H412 M392,384 V370 M392,462 V478 M346,416 H330 M454,416 H470" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.94"/>
  <text x="296" y="560" width="235" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#1E2832">INPUT</text>
  <text x="296" y="590" width="235" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#0D52D6">AI + Web UI</text>

  <rect x="558" y="332" width="164" height="56" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <line x1="578" y1="360" x2="688" y2="360" stroke="url(#arrowGrad)" stroke-width="10" stroke-linecap="round"/>
  <path d="M690,342 L724,360 L690,378 Z" fill="#FFB72A"/>
  <circle cx="592" cy="326" r="5" fill="#0D52D6" opacity="0.65"/>
  <circle cx="624" cy="400" r="4" fill="#8FA3B8" opacity="0.70"/>
  <circle cx="680" cy="318" r="6" fill="#FFAB00" opacity="0.80"/>
  <text x="534" y="430" width="212" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#7B8794">TRANSFORM</text>

  <rect x="764" y="238" width="282" height="280" rx="36" fill="url(#goldCard)" filter="url(#cardShadow)"/>
  <rect x="796" y="276" width="218" height="70" rx="20" fill="#FFFFFF" opacity="0.30"/>
  <text x="820" y="309" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#4B3300">Revenue Kit</text>
  <text x="820" y="334" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6E4A00">Products · Courses · Services</text>

  <path d="M848,402 C848,380 880,378 884,402 C896,395 918,403 914,426 C910,450 848,450 842,426 C838,413 840,407 848,402 Z" fill="#FFFFFF" opacity="0.95"/>
  <path d="M868,382 C884,368 896,368 912,382" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.95"/>
  <text x="846" y="435" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="900" fill="#FFAB00">$</text>

  <ellipse cx="970" cy="404" rx="32" ry="10" fill="#FFFFFF" opacity="0.95"/>
  <path d="M938,404 V432 C938,438 952,444 970,444 C988,444 1002,438 1002,432 V404" fill="#FFFFFF" opacity="0.95"/>
  <ellipse cx="970" cy="432" rx="32" ry="10" fill="#FFF2C7" opacity="0.95"/>
  <path d="M956,466 L956,448 L976,448 L976,428 L1004,428" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>

  <rect x="812" y="474" width="186" height="28" rx="14" fill="#1E2832" opacity="0.88"/>
  <text x="832" y="494" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">+ Commercial Output</text>

  <text x="788" y="560" width="235" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#1E2832">OUTPUT</text>
  <text x="788" y="590" width="235" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#C77700">Monetization</text>

  <path d="M1116,254 L1125,274 L1146,282 L1125,290 L1116,310 L1107,290 L1086,282 L1107,274 Z" fill="#FFD66B" opacity="0.9"/>
  <path d="M177,472 L184,488 L201,494 L184,500 L177,516 L170,500 L153,494 L170,488 Z" fill="#A9CBFF" opacity="0.9"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade cards or arrows; masks on shapes are not reliable in the PPT translation path.
- ❌ Do not put `marker-end` on a `<path>` for the arrow; create the arrow with a `<line>` shaft plus a triangular `<path>` arrowhead.
- ❌ Do not apply `filter` to the connector `<line>`; line filters are dropped, so keep shadows/glows on cards, paths, circles, or text only.
- ❌ Do not use `<foreignObject>` for HTML-like UI cards; build the web-UI panels from editable SVG rectangles, text, circles, and paths.
- ❌ Do not rely on clipped non-image elements for card interiors; clip paths should be reserved for `<image>` crops only.

## Composition notes
- Keep the slide split into a 40 / 20 / 40 rhythm: left input stack, central transformation arrow, right revenue outcome card.
- Reserve the top 20% for a concise headline and subtitle; the main visual should occupy the middle 55–60% of the canvas.
- Use blue only on the technology/input side and gold only on the value/output side; the connector may blend gray into gold to imply conversion.
- Shadows should be broad and soft, not dark; the goal is modern SaaS depth rather than heavy 3D realism.