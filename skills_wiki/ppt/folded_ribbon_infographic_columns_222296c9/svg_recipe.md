# SVG Recipe — Folded Ribbon Infographic Columns

## Visual mechanism
A row of elevated white cards is punctuated by bright horizontal ribbons that overhang the left edge of each card. The “fold” illusion comes from placing a darker triangular flap beneath each ribbon, making the accent feel wrapped around the card edge.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft gray background
- 4× `<rect>` for white infographic cards with borders and shadows
- 4× `<rect>` for vivid front-facing ribbon banners
- 4× `<path>` for darker triangular ribbon folds tucked under the banners
- 4× `<circle>` for pale icon medallions inside the cards
- 8× `<path>` for simple editable line-style icons inside the medallions
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to cards
- 4× `<linearGradient>` fills for subtle premium ribbon lighting
- Multiple `<text>` elements with explicit `width` for title, numbers, headings, body copy, and small metrics

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="13" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="goldRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFD84A"/>
      <stop offset="1" stop-color="#FFC000"/>
    </linearGradient>
    <linearGradient id="blueRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#27A7FF"/>
      <stop offset="1" stop-color="#0070C0"/>
    </linearGradient>
    <linearGradient id="greenRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22D879"/>
      <stop offset="1" stop-color="#00A651"/>
    </linearGradient>
    <linearGradient id="purpleRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#9A66D9"/>
      <stop offset="1" stop-color="#7030A0"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F5F7"/>
  <path d="M-40 122 C170 54 283 88 455 28" fill="none" stroke="#E6E9EF" stroke-width="26" stroke-linecap="round"/>
  <path d="M858 690 C1035 610 1124 635 1328 566" fill="none" stroke="#E9ECF2" stroke-width="34" stroke-linecap="round"/>

  <text x="90" y="80" width="1100" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#252A31">Folded Ribbon Infographic Columns</text>
  <text x="92" y="116" width="880" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">Use equal-weight cards when four ideas need clear separation, sequence, and visual parity.</text>

  <g>
    <rect x="120" y="160" width="230" height="440" rx="6" fill="#FFFFFF" stroke="#D9DDE4" stroke-width="2" filter="url(#cardShadow)"/>
    <path d="M94 266 L120 266 L120 293 Z" fill="#B78400"/>
    <rect x="94" y="210" width="124" height="56" rx="2" fill="url(#goldRibbon)"/>
    <text x="115" y="249" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF" text-anchor="middle">01</text>
    <circle cx="235" cy="332" r="42" fill="#FFF6D9"/>
    <path d="M218 329 C218 318 225 311 235 311 C245 311 252 318 252 329 C252 338 247 343 242 348 L228 348 C223 343 218 338 218 329 Z" fill="none" stroke="#FFC000" stroke-width="5" stroke-linejoin="round"/>
    <path d="M228 360 L242 360 M230 369 L240 369" fill="none" stroke="#FFC000" stroke-width="5" stroke-linecap="round"/>
    <text x="145" y="416" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#2E3440" text-anchor="middle">RESEARCH</text>
    <text x="148" y="455" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280" text-anchor="middle">
      <tspan x="235" dy="0">Map customer needs,</tspan>
      <tspan x="235" dy="22">market signals, and</tspan>
      <tspan x="235" dy="22">opportunity spaces.</tspan>
    </text>
    <line x1="164" y1="532" x2="306" y2="532" stroke="#ECEFF4" stroke-width="2"/>
    <text x="160" y="565" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFC000" text-anchor="middle">INSIGHT SCORE 92%</text>
  </g>

  <g>
    <rect x="390" y="160" width="230" height="440" rx="6" fill="#FFFFFF" stroke="#D9DDE4" stroke-width="2" filter="url(#cardShadow)"/>
    <path d="M364 266 L390 266 L390 293 Z" fill="#004E86"/>
    <rect x="364" y="210" width="124" height="56" rx="2" fill="url(#blueRibbon)"/>
    <text x="385" y="249" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF" text-anchor="middle">02</text>
    <circle cx="505" cy="332" r="42" fill="#E4F3FF"/>
    <path d="M483 344 L483 321 C483 316 487 312 492 312 L518 312 C523 312 527 316 527 321 L527 344 Z" fill="none" stroke="#0070C0" stroke-width="5" stroke-linejoin="round"/>
    <path d="M496 312 L496 304 L514 304 L514 312 M483 329 L527 329" fill="none" stroke="#0070C0" stroke-width="5" stroke-linecap="round"/>
    <text x="415" y="416" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#2E3440" text-anchor="middle">EXPERIENCE</text>
    <text x="418" y="455" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280" text-anchor="middle">
      <tspan x="505" dy="0">Shape a frictionless</tspan>
      <tspan x="505" dy="22">journey across key</tspan>
      <tspan x="505" dy="22">decision moments.</tspan>
    </text>
    <line x1="434" y1="532" x2="576" y2="532" stroke="#ECEFF4" stroke-width="2"/>
    <text x="430" y="565" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#0070C0" text-anchor="middle">NPS LIFT +18</text>
  </g>

  <g>
    <rect x="660" y="160" width="230" height="440" rx="6" fill="#FFFFFF" stroke="#D9DDE4" stroke-width="2" filter="url(#cardShadow)"/>
    <path d="M634 266 L660 266 L660 293 Z" fill="#00763A"/>
    <rect x="634" y="210" width="124" height="56" rx="2" fill="url(#greenRibbon)"/>
    <text x="655" y="249" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF" text-anchor="middle">03</text>
    <circle cx="775" cy="332" r="42" fill="#E4F9ED"/>
    <path d="M755 308 L792 308 L792 357 L755 357 Z" fill="none" stroke="#00A651" stroke-width="5" stroke-linejoin="round"/>
    <path d="M764 323 L784 323 M764 335 L784 335 M764 347 L777 347" fill="none" stroke="#00A651" stroke-width="5" stroke-linecap="round"/>
    <text x="685" y="416" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#2E3440" text-anchor="middle">PLANNING</text>
    <text x="688" y="455" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280" text-anchor="middle">
      <tspan x="775" dy="0">Prioritize initiatives,</tspan>
      <tspan x="775" dy="22">owners, milestones,</tspan>
      <tspan x="775" dy="22">and investment gates.</tspan>
    </text>
    <line x1="704" y1="532" x2="846" y2="532" stroke="#ECEFF4" stroke-width="2"/>
    <text x="700" y="565" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#00A651" text-anchor="middle">ROADMAP 12 WKS</text>
  </g>

  <g>
    <rect x="930" y="160" width="230" height="440" rx="6" fill="#FFFFFF" stroke="#D9DDE4" stroke-width="2" filter="url(#cardShadow)"/>
    <path d="M904 266 L930 266 L930 293 Z" fill="#4E2170"/>
    <rect x="904" y="210" width="124" height="56" rx="2" fill="url(#purpleRibbon)"/>
    <text x="925" y="249" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF" text-anchor="middle">04</text>
    <circle cx="1045" cy="332" r="42" fill="#F0E7FA"/>
    <path d="M1032 354 C1044 330 1054 319 1071 309 C1063 327 1052 339 1032 354 Z" fill="none" stroke="#7030A0" stroke-width="5" stroke-linejoin="round"/>
    <path d="M1027 345 L1019 361 M1046 326 L1029 309 M1057 319 L1065 327" fill="none" stroke="#7030A0" stroke-width="5" stroke-linecap="round"/>
    <text x="955" y="416" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#2E3440" text-anchor="middle">EXECUTION</text>
    <text x="958" y="455" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280" text-anchor="middle">
      <tspan x="1045" dy="0">Launch, measure,</tspan>
      <tspan x="1045" dy="22">optimize, and scale</tspan>
      <tspan x="1045" dy="22">what proves value.</tspan>
    </text>
    <line x1="974" y1="532" x2="1116" y2="532" stroke="#ECEFF4" stroke-width="2"/>
    <text x="970" y="565" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7030A0" text-anchor="middle">ROI TARGET 3.4×</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using only flat rectangles without the darker triangular fold; the ribbon will look like a label, not a wrapped paper element.
- ❌ Applying `clip-path` or masks to card rectangles for shadows or folds; use normal paths and rects so every element remains editable.
- ❌ Putting `filter` on separator lines; shadows/glows on `<line>` may be dropped, so keep filters on cards or paths.
- ❌ Making the ribbons too wide or centered on the card; the effect depends on a visible left overhang and a tight fold triangle.

## Composition notes
- Keep the card grid symmetrical: four cards should have equal width, equal vertical position, and generous gutters.
- The ribbon should sit in the upper third of each card, overlapping the card’s left edge by roughly 10–15% of card width.
- Use bright accent colors only on the ribbon, number, icon, and small metric; keep card interiors mostly white for contrast.
- Leave negative space above the cards for a title/subtitle and below the content for small data callouts or status labels.