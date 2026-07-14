# SVG Recipe — Dark Split-Pane Analytics Dashboard

## Visual mechanism
A premium dark dashboard built from a strict 30/70 vertical split: the left pane acts as a branded narrative/CTA column over a teal-tinted photo, while the right pane becomes a spacious glassmorphism analytics canvas. Luminous cyan and yellow accents create a modern SaaS/QBR feel against deep navy photographic overlays.

## SVG primitives needed
- 2× `<image>` for cinematic background photography: one portrait/business image in the left pane and one wide abstract/office image on the right.
- 2× `<clipPath>` for image cropping to the left pane and full-slide background.
- 5× `<linearGradient>` for dark navy base, teal photo wash, right-pane vignette, glass card highlights, and CTA button fill.
- 2× `<filter>`: one shadow filter for floating cards/buttons and one cyan glow filter for active chart strokes.
- 8–12× `<rect>` for split panes, glass cards, CTA button, micro chart bars, and subtle UI chips.
- 6–8× `<circle>` for doughnut chart tracks, progress rings, and small status dots.
- 4–6× `<path>` for sparkline charts, decorative angled separators, and soft organic accent curves.
- 6–8× `<line>` for dashboard grid rules and axis ticks.
- Multiple `<text>` elements with explicit `width=` for title hierarchy, KPI values, labels, body copy, and chart annotations.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="leftClip"><rect x="0" y="0" width="384" height="720"/></clipPath>
    <clipPath id="rightClip"><rect x="384" y="0" width="896" height="720"/></clipPath>

    <linearGradient id="navyBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1320"/>
      <stop offset="55%" stop-color="#09111D"/>
      <stop offset="100%" stop-color="#050A12"/>
    </linearGradient>
    <linearGradient id="leftTealWash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#008B8B" stop-opacity="0.88"/>
      <stop offset="55%" stop-color="#004B5C" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#07131F" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="rightVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1320" stop-opacity="0.95"/>
      <stop offset="50%" stop-color="#0B1320" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#020610" stop-opacity="0.98"/>
    </linearGradient>
    <linearGradient id="glassFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#203144" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#0D1724" stop-opacity="0.76"/>
    </linearGradient>
    <linearGradient id="ctaGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFD45A"/>
      <stop offset="100%" stop-color="#FFB703"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#navyBase)"/>

  <image x="0" y="0" width="384" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portrait-executive-dark-office.jpg" clip-path="url(#leftClip)"/>
  <rect x="0" y="0" width="384" height="720" fill="url(#leftTealWash)"/>
  <path d="M315 0 L384 0 L384 720 L260 720 C330 535 330 275 315 0Z" fill="#06101A" opacity="0.34"/>

  <image x="384" y="0" width="896" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/abstract-city-data-center-night.jpg" clip-path="url(#rightClip)" opacity="0.42"/>
  <rect x="384" y="0" width="896" height="720" fill="url(#rightVignette)"/>

  <text x="54" y="72" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" fill="#BDEEF4">QBR DASHBOARD</text>
  <text x="54" y="143" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#FFFFFF">BUSINESS</text>
  <text x="54" y="196" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#FFFFFF">PRESENTATION</text>
  <line x1="54" y1="226" x2="180" y2="226" stroke="#00D4FF" stroke-width="4"/>
  <text x="54" y="274" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#C8D3DE">
    <tspan x="54" dy="0">Performance signals, pipeline</tspan>
    <tspan x="54" dy="25">momentum, and operating KPIs</tspan>
    <tspan x="54" dy="25">for the next growth cycle.</tspan>
  </text>
  <rect x="54" y="462" width="168" height="48" rx="24" fill="url(#ctaGrad)" filter="url(#cardShadow)"/>
  <text x="84" y="493" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#1A1A1A">VIEW REPORT</text>
  <text x="54" y="644" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#8FA7B8">FY2026 · NORTH AMERICA</text>

  <text x="438" y="74" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" letter-spacing="3" font-weight="700" fill="#7FDFF2">EXECUTIVE PERFORMANCE</text>
  <text x="438" y="119" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="750" fill="#FFFFFF">Revenue intelligence overview</text>
  <rect x="1052" y="52" width="146" height="36" rx="18" fill="#101D2B" stroke="#2A435A"/>
  <circle cx="1074" cy="70" r="5" fill="#00D4FF"/>
  <text x="1090" y="76" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#D8E8F2">LIVE DATA</text>

  <rect x="438" y="158" width="236" height="174" rx="26" fill="url(#glassFill)" stroke="#29465E" filter="url(#cardShadow)"/>
  <rect x="704" y="158" width="236" height="174" rx="26" fill="url(#glassFill)" stroke="#29465E" filter="url(#cardShadow)"/>
  <rect x="970" y="158" width="218" height="174" rx="26" fill="url(#glassFill)" stroke="#29465E" filter="url(#cardShadow)"/>

  <text x="466" y="198" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#9FB0BF">ARR GROWTH</text>
  <text x="466" y="253" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">32.8%</text>
  <path d="M468 292 C500 274 520 307 548 285 S603 260 642 276" fill="none" stroke="#00D4FF" stroke-width="4" stroke-linecap="round"/>
  <circle cx="642" cy="276" r="5" fill="#00D4FF" filter="url(#cyanGlow)"/>

  <text x="732" y="198" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#9FB0BF">PIPELINE</text>
  <text x="732" y="253" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">$18.4M</text>
  <rect x="735" y="288" width="24" height="24" rx="4" fill="#00D4FF"/>
  <rect x="771" y="270" width="24" height="42" rx="4" fill="#126E8A"/>
  <rect x="807" y="248" width="24" height="64" rx="4" fill="#00D4FF"/>
  <rect x="843" y="282" width="24" height="30" rx="4" fill="#126E8A"/>
  <rect x="879" y="230" width="24" height="82" rx="4" fill="#00D4FF"/>

  <text x="998" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#9FB0BF">RETENTION</text>
  <text x="998" y="253" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">91%</text>
  <text x="1000" y="300" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A0AFBE">+6.2 pts YoY</text>

  <rect x="438" y="366" width="470" height="250" rx="30" fill="url(#glassFill)" stroke="#29465E" filter="url(#cardShadow)"/>
  <text x="470" y="410" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" letter-spacing="2" font-weight="700" fill="#C6D8E4">REGIONAL MOMENTUM</text>
  <line x1="470" y1="555" x2="868" y2="555" stroke="#30465A" stroke-width="1"/>
  <line x1="470" y1="505" x2="868" y2="505" stroke="#30465A" stroke-width="1" stroke-dasharray="5 8"/>
  <line x1="470" y1="455" x2="868" y2="455" stroke="#30465A" stroke-width="1" stroke-dasharray="5 8"/>
  <path d="M480 538 C522 510 552 522 590 488 C626 456 658 470 696 438 C742 400 790 436 858 396" fill="none" stroke="#00D4FF" stroke-width="5" stroke-linecap="round"/>
  <path d="M480 565 C534 552 572 562 614 536 C665 505 702 528 752 498 C796 471 826 480 858 458" fill="none" stroke="#FFB703" stroke-width="4" stroke-linecap="round" opacity="0.92"/>
  <circle cx="858" cy="396" r="7" fill="#00D4FF" filter="url(#cyanGlow)"/>
  <circle cx="858" cy="458" r="6" fill="#FFB703"/>

  <rect x="940" y="366" width="248" height="250" rx="30" fill="url(#glassFill)" stroke="#29465E" filter="url(#cardShadow)"/>
  <text x="970" y="410" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" letter-spacing="2" font-weight="700" fill="#C6D8E4">CHANNEL MIX</text>
  <circle cx="1036" cy="498" r="52" fill="none" stroke="#263847" stroke-width="18"/>
  <circle cx="1036" cy="498" r="52" fill="none" stroke="#00D4FF" stroke-width="18" stroke-dasharray="246 80" stroke-linecap="round" transform="rotate(-90 1036 498)" filter="url(#cyanGlow)"/>
  <circle cx="1122" cy="498" r="52" fill="none" stroke="#263847" stroke-width="18"/>
  <circle cx="1122" cy="498" r="52" fill="none" stroke="#FFB703" stroke-width="18" stroke-dasharray="185 141" stroke-linecap="round" transform="rotate(-90 1122 498)"/>
  <text x="1008" y="505" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">76%</text>
  <text x="1095" y="505" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF">57%</text>
  <text x="988" y="578" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A5B7C6">Product-led</text>
  <text x="1080" y="578" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#A5B7C6">Enterprise</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for photo dimming; use clipped `<image>` plus semi-transparent gradient `<rect>` overlays instead.
- ❌ Do not rely on `<foreignObject>` for dashboard widgets or HTML tables; build cards, labels, and charts from native SVG shapes.
- ❌ Do not use `clip-path` on glass cards or chart shapes; clipping is only reliable here for `<image>` crops.
- ❌ Do not put filters on `<line>` grid rules; apply shadows/glows to cards, circles, paths, or text only.
- ❌ Do not use `marker-end` on curved chart paths; if arrows are needed, use explicit `<line>` arrows with `marker-end` directly on each line.

## Composition notes
- Keep the left pane exactly around 30% of slide width; it should feel like a branded presenter panel, not a data area.
- Put dense analytics on the right 70%, using large glass cards with generous gutters so the dashboard reads as premium rather than crowded.
- Reserve cyan for live/active data and yellow for the CTA or a single comparison series; overusing both accents weakens the hierarchy.
- Use photography only as atmosphere: dark overlays should suppress detail enough that white typography and chart strokes remain dominant.