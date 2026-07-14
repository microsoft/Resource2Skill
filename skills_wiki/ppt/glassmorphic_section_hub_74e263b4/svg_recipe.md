# SVG Recipe — Glassmorphic Section Hub

## Visual mechanism
A sharp cinematic background is covered by circular “frosted glass” lenses: each lens uses a full-slide blurred copy of the same background clipped to a circle, then adds translucent white gloss, rim highlights, and editable white section labels. The lenses are arranged as a staggered section-navigation hub that feels like an interactive premium keynote interface.

## SVG primitives needed
- 1× `<image>` for the sharp full-slide architectural/interior background
- 9× `<clipPath>` with `<circle>` for localized circular image crops
- 9× `<image>` for the blurred duplicate background, each clipped to a lens circle
- 9× `<circle>` for translucent glass tint overlays
- 9× `<circle>` for crisp semi-transparent white rims
- 9× `<circle>` for small icon badges on the glass lenses
- 9× `<path>` or `<line>` icon marks inside the badges
- 9× `<text>` section labels with explicit `width`
- 1× `<text>` main title with explicit `width`
- 1× `<linearGradient>` for the dark cinematic slide overlay
- 2× `<radialGradient>` for lens frost and highlight behavior
- 2× `<filter>` definitions: one soft drop shadow for bubbles and one glow for badge highlights

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#000000" stop-opacity="0.48"/>
      <stop offset="0.45" stop-color="#18230f" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.58"/>
    </linearGradient>

    <radialGradient id="glassFrost" cx="34%" cy="24%" r="72%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.48"/>
      <stop offset="0.32" stop-color="#ffffff" stop-opacity="0.20"/>
      <stop offset="0.72" stop-color="#d8ffd0" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.30"/>
    </radialGradient>

    <radialGradient id="badgeFill" cx="32%" cy="24%" r="74%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.82"/>
      <stop offset="0.52" stop-color="#ffffff" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.16"/>
    </radialGradient>

    <filter id="bubbleShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="13"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="badgeGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>

    <clipPath id="clipMission"><circle cx="150" cy="365" r="72"/></clipPath>
    <clipPath id="clipSolution"><circle cx="300" cy="318" r="72"/></clipPath>
    <clipPath id="clipModel"><circle cx="455" cy="306" r="72"/></clipPath>
    <clipPath id="clipCompetition"><circle cx="610" cy="298" r="72"/></clipPath>
    <clipPath id="clipTeam"><circle cx="760" cy="318" r="72"/></clipPath>
    <clipPath id="clipProblem"><circle cx="225" cy="500" r="72"/></clipPath>
    <clipPath id="clipMarket"><circle cx="380" cy="475" r="72"/></clipPath>
    <clipPath id="clipGrowth"><circle cx="535" cy="465" r="72"/></clipPath>
    <clipPath id="clipFinancials"><circle cx="690" cy="500" r="72"/></clipPath>
  </defs>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-1280x720.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaShade)"/>

  <text x="96" y="92" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700" fill="#ffffff" letter-spacing="-1.2">
    Table of<tspan x="96" dy="40">Contents</tspan>
  </text>
  <line x1="96" y1="152" x2="250" y2="152" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2"/>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMission)"/>
  <circle cx="150" cy="365" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="150" cy="365" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="122" cy="306" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M116 306 L121 311 L130 300" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="102" y="358" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#ffffff">Our<tspan x="150" dy="22">Mission</tspan></text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipSolution)"/>
  <circle cx="300" cy="318" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="300" cy="318" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="284" cy="254" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M275 254 L283 262 L295 246" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="252" y="322" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#ffffff">Solution</text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipModel)"/>
  <circle cx="455" cy="306" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="455" cy="306" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="455" cy="238" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M447 238 h16 M455 230 v16 M449 244 l12 -12" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round"/>
  <text x="407" y="292" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#ffffff">Business<tspan x="455" dy="22">Model</tspan></text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCompetition)"/>
  <circle cx="610" cy="298" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="610" cy="298" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="626" cy="234" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M617 239 c6 -16 18 -16 18 0 M621 239 h10 M626 224 v9" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round"/>
  <text x="562" y="304" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#ffffff">Competition</text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipTeam)"/>
  <circle cx="760" cy="318" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="760" cy="318" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="782" cy="258" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M776 264 c2 -8 10 -8 12 0 M778 253 a5 5 0 1 0 8 0" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round"/>
  <text x="712" y="323" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#ffffff">Our Team</text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipProblem)"/>
  <circle cx="225" cy="500" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="225" cy="500" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="225" cy="568" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M225 557 l10 18 h-20 z M225 563 v5" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="177" y="506" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#ffffff">Problem</text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMarket)"/>
  <circle cx="380" cy="475" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="380" cy="475" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="396" cy="541" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <circle cx="396" cy="541" r="9" fill="none" stroke="#ffffff" stroke-width="2.1"/>
  <line x1="396" y1="532" x2="396" y2="550" stroke="#ffffff" stroke-width="2.1"/>
  <text x="332" y="461" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#ffffff">Market<tspan x="380" dy="22">Potential</tspan></text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipGrowth)"/>
  <circle cx="535" cy="465" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="535" cy="465" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="535" cy="533" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M525 540 L532 532 L538 536 L547 524 M542 524 h5 v5" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="487" y="451" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#ffffff">Growth<tspan x="535" dy="22">Strategy</tspan></text>

  <image href="https://images.example.com/luxury-modern-villa-interior-with-green-garden-BLURRED-1280x720.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipFinancials)"/>
  <circle cx="690" cy="500" r="72" fill="url(#glassFrost)" filter="url(#bubbleShadow)"/>
  <circle cx="690" cy="500" r="72" fill="none" stroke="#ffffff" stroke-opacity="0.76" stroke-width="2.3"/>
  <circle cx="713" cy="562" r="20" fill="url(#badgeFill)" stroke="#ffffff" stroke-opacity="0.8" filter="url(#badgeGlow)"/>
  <path d="M713 551 v22 M706 557 c0 -5 14 -5 14 0 c0 6 -14 4 -14 10 c0 6 14 6 14 0" fill="none" stroke="#ffffff" stroke-width="2.1" stroke-linecap="round"/>
  <text x="642" y="506" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#ffffff">Financials</text>

  <rect x="930" y="160" width="250" height="340" rx="34" fill="#ffffff" fill-opacity="0.07" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1.5"/>
  <text x="960" y="220" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700" fill="#ffffff">Section Hub</text>
  <text x="960" y="264" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#ffffff" fill-opacity="0.76">Click a glass lens to jump into the matching chapter.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the glass lenses; use `<clipPath>` applied directly to each `<image>`.
- ❌ Do not apply `clip-path` to circles, groups, or text for the lens effect; the reliable editable workflow is clipped images plus editable overlay shapes.
- ❌ Do not rely on SVG `filter` blur on `<image>` for the frosted crop; provide a separate pre-blurred version of the same background image.
- ❌ Do not use `<use>` to duplicate bubbles; repeat the shapes explicitly so each bubble remains independently editable in PowerPoint.
- ❌ Do not omit `width` on text labels; PowerPoint translation needs explicit text box width.

## Composition notes
- Keep the title in the upper-left or upper-center with generous breathing room; the glass bubbles should occupy the middle 55–65% of slide height.
- Arrange bubbles in a staggered 5-over-4 grid, with row two offset horizontally to create a dashboard rhythm rather than a static table.
- Use a complex, high-contrast background image; glassmorphism works best when the blurred crop has visible greens, warm lights, windows, or architectural lines.
- Maintain white text, white translucent rims, and soft shadows consistently so the hub reads as one premium interactive system.