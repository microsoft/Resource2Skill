# SVG Recipe — Neon Glow Data Dashboard

## Visual mechanism
A dark radial-gradient “deep space” canvas supports a strict grid of translucent KPI cards, while high-value numbers, sparklines, and active navigation elements emit cyan/yellow/magenta neon glows. The dashboard feels premium because the data is ordered and executive-readable, but the lighting, gradients, and holographic accents make it feel futuristic.

## SVG primitives needed
- 1× `<rect>` full-slide background filled by a dark `<radialGradient>`
- 1× sidebar `<rect>` plus 1× active-state rounded `<rect>` for navigation structure
- 6× rounded `<rect>` KPI cards with translucent fills, thin neon borders, and soft shadow/glow filters
- 6× large `<text>` KPI values with yellow neon glow filters
- 12–18× supporting `<text>` labels for titles, deltas, captions, and navigation
- 6× `<path>` filled sparkline/area charts using cyan, purple, and magenta gradients
- 6× `<path>` stroked sparkline traces layered over the filled areas
- 8–12× small `<rect>` bars for compact comparative bar charts
- 3× `<circle>` progress rings / status indicators using `stroke-dasharray`
- 4–6× simple `<path>` icons in the sidebar and header
- 3× `<filter>` definitions: card shadow, yellow text glow, cyan/magenta chart glow
- 4–6× `<linearGradient>` / `<radialGradient>` definitions for background, card fills, chart fills, and neon strokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="bgRadial" cx="55%" cy="42%" r="80%">
      <stop offset="0%" stop-color="#2B1B56"/>
      <stop offset="55%" stop-color="#160A3E"/>
      <stop offset="100%" stop-color="#0B0427"/>
    </radialGradient>

    <linearGradient id="cardFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#25245B" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#11122E" stop-opacity="0.76"/>
    </linearGradient>

    <linearGradient id="cyanArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#46C8D2" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#46C8D2" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="magentaArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E84BFF" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#7748D4" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="yellowStroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FDD550"/>
      <stop offset="100%" stop-color="#FF8D3A"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.20  0 0 0 0 0.12  0 0 0 0 0.65  0 0 0 0.45 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="yellowGlow" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="1 0 0 0 0.99  0 1 0 0 0.83  0 0 1 0 0.31  0 0 0 0.75 0" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-25%" y="-40%" width="150%" height="180%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.27  0 0 0 0 0.78  0 0 0 0 0.82  0 0 0 0.70 0" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <path d="M245 0 L290 720" fill="none" stroke="#46C8D2" stroke-width="1" opacity="0.10"/>
  <path d="M0 615 C260 560 410 690 680 620 C915 558 1030 612 1280 540" fill="none" stroke="#7748D4" stroke-width="2" opacity="0.18"/>
  <path d="M755 70 C850 18 985 26 1085 88" fill="none" stroke="#46C8D2" stroke-width="2" opacity="0.16"/>

  <rect x="0" y="0" width="224" height="720" fill="#09051D" opacity="0.74"/>
  <text x="34" y="54" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">NEXUS BI</text>
  <text x="34" y="80" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="2" fill="#8F8BB6">EXECUTIVE VIEW</text>

  <rect x="24" y="132" width="176" height="48" rx="14" fill="#1B1B3F" stroke="#46C8D2" stroke-width="1.4" filter="url(#cyanGlow)"/>
  <path d="M48 146 L64 146 L64 162 L48 162 Z M70 146 L86 146 L86 170 L70 170 Z" fill="#46C8D2"/>
  <text x="100" y="162" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFFFFF">Overview</text>

  <path d="M52 224 L84 224 M52 238 L74 238 M52 252 L88 252" stroke="#7D789F" stroke-width="3" stroke-linecap="round"/>
  <text x="100" y="242" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A7A3C7">Revenue</text>
  <path d="M54 298 C60 286 78 286 84 298 C78 310 60 310 54 298 Z" fill="none" stroke="#7D789F" stroke-width="3"/>
  <circle cx="69" cy="298" r="4" fill="#7D789F"/>
  <text x="100" y="303" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A7A3C7">Pipeline</text>
  <path d="M54 365 L69 350 L84 365 L69 380 Z" fill="none" stroke="#7D789F" stroke-width="3"/>
  <text x="100" y="370" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A7A3C7">Forecast</text>

  <text x="268" y="54" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">Sales Performance Dashboard</text>
  <text x="270" y="82" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9B4DE">Q4 live metrics · refreshed 09:45 UTC · global revenue operations</text>
  <rect x="1060" y="38" width="150" height="36" rx="18" fill="#1B1B3F" stroke="#FDD550" stroke-opacity="0.55"/>
  <circle cx="1083" cy="56" r="5" fill="#FDD550" filter="url(#yellowGlow)"/>
  <text x="1100" y="61" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#FFFFFF">LIVE SIGNAL</text>

  <rect x="258" y="122" width="300" height="232" rx="24" fill="url(#cardFill)" stroke="#7B5CFF" stroke-opacity="0.48" filter="url(#cardShadow)"/>
  <text x="286" y="158" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">SALES TOTAL</text>
  <text x="286" y="214" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FDD550" filter="url(#yellowGlow)">$8.42M</text>
  <text x="292" y="244" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A7F6FF">▲ 18.6% vs prior quarter</text>
  <path d="M286 317 L286 278 C313 284 338 246 365 255 C393 265 414 300 444 283 C472 267 493 238 530 248 L530 317 Z" fill="url(#cyanArea)"/>
  <path d="M286 278 C313 284 338 246 365 255 C393 265 414 300 444 283 C472 267 493 238 530 248" fill="none" stroke="#46C8D2" stroke-width="3" stroke-linecap="round" filter="url(#cyanGlow)"/>

  <rect x="590" y="122" width="300" height="232" rx="24" fill="url(#cardFill)" stroke="#7B5CFF" stroke-opacity="0.48" filter="url(#cardShadow)"/>
  <text x="618" y="158" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">PIPELINE VALUE</text>
  <text x="618" y="214" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FDD550" filter="url(#yellowGlow)">$21.7M</text>
  <text x="624" y="244" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFB8FF">▲ 9.2% expansion</text>
  <rect x="625" y="313" width="22" height="30" rx="5" fill="#46C8D2"/>
  <rect x="659" y="288" width="22" height="55" rx="5" fill="#7748D4"/>
  <rect x="693" y="270" width="22" height="73" rx="5" fill="#E84BFF" filter="url(#cyanGlow)"/>
  <rect x="727" y="300" width="22" height="43" rx="5" fill="#46C8D2"/>
  <rect x="761" y="252" width="22" height="91" rx="5" fill="#FDD550"/>
  <text x="806" y="326" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#B9B4DE">5-region weighted view</text>

  <rect x="922" y="122" width="300" height="232" rx="24" fill="url(#cardFill)" stroke="#7B5CFF" stroke-opacity="0.48" filter="url(#cardShadow)"/>
  <text x="950" y="158" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">CONVERSION RATE</text>
  <text x="950" y="214" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FDD550" filter="url(#yellowGlow)">42.8%</text>
  <circle cx="1074" cy="292" r="48" fill="none" stroke="#2A2859" stroke-width="14"/>
  <circle cx="1074" cy="292" r="48" fill="none" stroke="url(#yellowStroke)" stroke-width="14" stroke-linecap="round" stroke-dasharray="220 302" transform="rotate(-90 1074 292)" filter="url(#yellowGlow)"/>
  <text x="1046" y="298" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">+6.1</text>
  <text x="958" y="332" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9B4DE">Lead-to-opportunity lift</text>

  <rect x="258" y="384" width="300" height="232" rx="24" fill="url(#cardFill)" stroke="#7B5CFF" stroke-opacity="0.48" filter="url(#cardShadow)"/>
  <text x="286" y="420" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">NET RETENTION</text>
  <text x="286" y="476" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FDD550" filter="url(#yellowGlow)">116%</text>
  <text x="292" y="506" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A7F6FF">Best enterprise cohort</text>
  <path d="M288 580 L288 552 C322 532 345 568 372 544 C401 519 424 529 451 500 C479 470 501 494 532 462 L532 580 Z" fill="url(#magentaArea)"/>
  <path d="M288 552 C322 532 345 568 372 544 C401 519 424 529 451 500 C479 470 501 494 532 462" fill="none" stroke="#E84BFF" stroke-width="3" stroke-linecap="round" filter="url(#cyanGlow)"/>

  <rect x="590" y="384" width="300" height="232" rx="24" fill="url(#cardFill)" stroke="#7B5CFF" stroke-opacity="0.48" filter="url(#cardShadow)"/>
  <text x="618" y="420" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">CUSTOMER HEALTH</text>
  <text x="618" y="476" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FDD550" filter="url(#yellowGlow)">91.4</text>
  <circle cx="670" cy="554" r="34" fill="none" stroke="#2A2859" stroke-width="10"/>
  <circle cx="670" cy="554" r="34" fill="none" stroke="#46C8D2" stroke-width="10" stroke-linecap="round" stroke-dasharray="176 214" transform="rotate(-90 670 554)" filter="url(#cyanGlow)"/>
  <circle cx="757" cy="554" r="34" fill="none" stroke="#2A2859" stroke-width="10"/>
  <circle cx="757" cy="554" r="34" fill="none" stroke="#E84BFF" stroke-width="10" stroke-linecap="round" stroke-dasharray="142 214" transform="rotate(-90 757 554)" filter="url(#cyanGlow)"/>
  <text x="805" y="548" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#B9B4DE">NPS + SLA composite</text>

  <rect x="922" y="384" width="300" height="232" rx="24" fill="url(#cardFill)" stroke="#7B5CFF" stroke-opacity="0.48" filter="url(#cardShadow)"/>
  <text x="950" y="420" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.8" fill="#FFFFFF">FORECAST INDEX</text>
  <text x="950" y="476" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FDD550" filter="url(#yellowGlow)">1.32×</text>
  <text x="956" y="506" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFB8FF">Coverage above target</text>
  <path d="M954 582 L954 545 C990 556 1018 508 1049 518 C1081 529 1097 562 1126 546 C1157 529 1174 503 1196 512 L1196 582 Z" fill="url(#cyanArea)"/>
  <path d="M954 545 C990 556 1018 508 1049 518 C1081 529 1097 562 1126 546 C1157 529 1174 503 1196 512" fill="none" stroke="#46C8D2" stroke-width="3" stroke-linecap="round" filter="url(#cyanGlow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the glow haze; use `filter` with `feGaussianBlur` on text, paths, circles, and card rectangles instead.
- ❌ Do not put `filter` on `<line>` elements for glowing grid lines; use thin `<path>` strokes or apply glow only to supported shapes.
- ❌ Do not rely on `<foreignObject>` for dashboard widgets or HTML-style cards; build every card from native SVG rectangles, text, paths, circles, and gradients.
- ❌ Do not use `clip-path` on cards or chart paths; clipping is reliable only for `<image>` crops, and this dashboard can be built without clipped non-image elements.
- ❌ Do not create arrowheads with `marker-end` on paths; if directional indicators are needed, draw simple triangle/chevron paths manually.

## Composition notes
- Keep the left sidebar around 17–18% of the canvas width; it provides orientation but should remain darker and quieter than the KPI grid.
- Use a 3×2 card grid with generous gutters, rounded corners, and consistent title/value/chart zones so the slide scans like a premium BI cockpit.
- Make only the primary KPI values bright yellow; reserve cyan and magenta for trends, progress rings, and active navigation so the color rhythm stays disciplined.
- Preserve negative space inside each card: title at top, large value in the upper middle, supporting delta below, chart/progress visual anchored in the lower third.