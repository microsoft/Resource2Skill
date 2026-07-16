# SVG Recipe — Modern Data-Driven Profile & Dashboard Layout

## Visual mechanism
A dark executive dashboard slide combines a large circular hero portrait with floating glass-like metric cards and bright progress rings. The composition feels like a premium product UI: editorial profile on the right, concise story and data widgets on the left, with cyan and magenta accents guiding attention.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 2× `<radialGradient>` / `<linearGradient>` definitions for subtle atmospheric glow and card surfaces
- 2× `<path>` for abstract background glow blobs and decorative dashboard contours
- 1× `<clipPath>` with `<circle>` to crop the hero photo into a perfect circular portrait
- 1× `<image>` for the circular hero/profile photograph
- 1× `<circle>` behind the hero image for shadow/depth
- 6× `<rect>` for floating rounded dashboard cards, stat pills, and micro chart containers
- 6× `<circle>` for doughnut/progress-ring tracks and colored progress strokes
- 4× `<line>` for mini bar-chart ticks and connector accents
- 8× `<text>` elements with explicit `width` for title, subtitle, numbers, labels, and card annotations
- 2× `<filter>` definitions: one soft shadow for cards/portrait, one glow for accent rings

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#252B38"/>
      <stop offset="100%" stop-color="#161B26"/>
    </linearGradient>
    <radialGradient id="cyanAtmosphere" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.35"/>
      <stop offset="70%" stop-color="#00E5FF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="magentaAtmosphere" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF3296" stop-opacity="0.30"/>
      <stop offset="75%" stop-color="#FF3296" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#FF3296" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="heroCircle">
      <circle cx="955" cy="305" r="214"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#141821"/>
  <path d="M785 42 C910 -18 1110 14 1202 142 C1298 276 1258 471 1138 555 C1020 638 821 601 753 470 C683 336 657 105 785 42 Z" fill="url(#cyanAtmosphere)"/>
  <path d="M-70 505 C68 430 205 461 257 570 C315 692 179 774 28 751 C-95 731 -175 626 -70 505 Z" fill="url(#magentaAtmosphere)"/>

  <text x="84" y="108" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="3" fill="#00E5FF">PROFILE DASHBOARD</text>
  <text x="82" y="184" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="55" font-weight="800" fill="#FFFFFF">
    Modern Data<tspan x="82" dy="62">Driven Overview</tspan>
  </text>
  <text x="86" y="308" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#B7BDCA">
    Real-time performance, leadership profile, and strategic signals combined into one executive-ready visual system.
  </text>

  <rect x="82" y="372" width="178" height="96" rx="26" fill="url(#cardGrad)" stroke="#343B4B" stroke-width="1.5" filter="url(#softShadow)"/>
  <text x="112" y="414" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">92%</text>
  <text x="112" y="445" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8F98AA">Team velocity</text>
  <circle cx="224" cy="420" r="23" fill="none" stroke="#323741" stroke-width="8"/>
  <circle cx="224" cy="420" r="23" fill="none" stroke="#00E5FF" stroke-width="8" stroke-linecap="round" stroke-dasharray="122 145" transform="rotate(-90 224 420)" filter="url(#accentGlow)"/>

  <rect x="286" y="372" width="178" height="96" rx="26" fill="url(#cardGrad)" stroke="#343B4B" stroke-width="1.5" filter="url(#softShadow)"/>
  <text x="316" y="414" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">68%</text>
  <text x="316" y="445" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8F98AA">Market reach</text>
  <circle cx="428" cy="420" r="23" fill="none" stroke="#323741" stroke-width="8"/>
  <circle cx="428" cy="420" r="23" fill="none" stroke="#FF3296" stroke-width="8" stroke-linecap="round" stroke-dasharray="94 145" transform="rotate(-90 428 420)" filter="url(#accentGlow)"/>

  <rect x="86" y="515" width="378" height="96" rx="28" fill="#1A202C" stroke="#2D3545" stroke-width="1.5"/>
  <text x="118" y="552" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Quarterly signal</text>
  <text x="118" y="580" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8F98AA">Momentum remains above target</text>
  <line x1="318" y1="584" x2="318" y2="548" stroke="#00E5FF" stroke-width="10" stroke-linecap="round"/>
  <line x1="348" y1="584" x2="348" y2="526" stroke="#FF3296" stroke-width="10" stroke-linecap="round"/>
  <line x1="378" y1="584" x2="378" y2="558" stroke="#00E5FF" stroke-width="10" stroke-linecap="round"/>
  <line x1="408" y1="584" x2="408" y2="536" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="10" stroke-linecap="round"/>

  <circle cx="955" cy="305" r="226" fill="#0E121A" filter="url(#softShadow)"/>
  <image x="741" y="91" width="428" height="428" href="https://images.example.com/executive-portrait-tech-dashboard-hero.jpg" clip-path="url(#heroCircle)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="955" cy="305" r="214" fill="none" stroke="#00E5FF" stroke-opacity="0.75" stroke-width="4"/>
  <circle cx="955" cy="305" r="232" fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1.5" stroke-dasharray="8 14"/>

  <rect x="742" y="470" width="276" height="126" rx="30" fill="url(#cardGrad)" stroke="#394154" stroke-width="1.4" filter="url(#softShadow)"/>
  <text x="776" y="510" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Engagement index</text>
  <text x="776" y="560" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#00E5FF">8.7</text>
  <text x="858" y="560" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#8F98AA">/ 10</text>
  <path d="M775 574 C810 548 837 586 870 558 C900 532 926 548 958 523" fill="none" stroke="#FF3296" stroke-width="4" stroke-linecap="round"/>

  <rect x="1012" y="166" width="178" height="92" rx="26" fill="#1B2130" stroke="#00E5FF" stroke-opacity="0.55" stroke-width="1.5" filter="url(#softShadow)"/>
  <text x="1042" y="205" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">24K</text>
  <text x="1042" y="232" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FA8BA">active users</text>

  <path d="M642 126 C685 112 700 167 666 187 C633 207 594 177 604 148 C608 136 622 130 642 126 Z" fill="#00E5FF" opacity="0.16"/>
  <path d="M1152 548 C1195 522 1246 560 1236 608 C1227 653 1164 655 1134 624 C1106 594 1116 570 1152 548 Z" fill="#FF3296" opacity="0.16"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the circular portrait; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to dashboard cards or other non-image elements; it will be ignored by the translator.
- ❌ Do not build progress rings with `marker-end` arrows or line markers; use stroked `<circle>` elements with `stroke-dasharray`.
- ❌ Do not use `<foreignObject>` for UI widgets; keep all cards, charts, labels, and numbers as native SVG shapes/text.
- ❌ Do not apply filters to `<line>` mini-chart bars; use filters only on cards, circles, paths, or text.

## Composition notes
- Keep the left half for narrative and metric widgets; reserve the right half for the large circular portrait and overlapping UI cards.
- Use a dark navy background with restrained atmospheric glows so cyan and magenta accents feel intentional, not decorative clutter.
- Let the hero circle dominate the slide visually, then break its edge with one floating card to create depth.
- Use large numeric typography inside cards and rings; labels should stay small, muted, and UI-like.