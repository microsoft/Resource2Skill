# SVG Recipe — Illuminated Trendline Chart

## Visual mechanism
Layer a soft, translucent gradient-filled area under a precise bright trendline, then add a blurred duplicate stroke behind the line to create an illuminated “data glow.” Place the chart on a dark atmospheric background with restrained gridlines so the trend becomes the slide’s visual centerpiece.

## SVG primitives needed
- 1× `<image>` for the dark atmospheric background photo
- 2× `<rect>` for the dark overlay wash and chart panel vignette
- 1× `<linearGradient>` for the slide background overlay
- 1× `<linearGradient>` for the under-curve area fill fading from yellow to green/transparent
- 1× `<radialGradient>` for highlighted data point fills
- 2× `<filter>`: one glow filter for trendline/points, one shadow filter for the title card
- 6× `<line>` for subtle horizontal gridlines and the x-axis baseline
- 2× `<path>` for the filled area and the crisp illuminated trendline
- 1× `<path>` duplicate for the blurred halo behind the trendline
- 9× `<circle>` for editable data point markers
- 20× `<text>` for title, subtitle, axis labels, value callouts, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050818" stop-opacity="0.92"/>
      <stop offset="55%" stop-color="#0B1032" stop-opacity="0.86"/>
      <stop offset="100%" stop-color="#02040D" stop-opacity="0.96"/>
    </linearGradient>

    <linearGradient id="areaGlow" x1="0" y1="190" x2="0" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFE64D" stop-opacity="0.72"/>
      <stop offset="38%" stop-color="#B9FF54" stop-opacity="0.34"/>
      <stop offset="72%" stop-color="#2AC36A" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#2AC36A" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="pointCore" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="38%" stop-color="#FFF176"/>
      <stop offset="100%" stop-color="#FFCC00"/>
    </radialGradient>

    <filter id="trendGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?auto=format&fit=crop&w=1600&q=80"
         x="0" y="0" width="1280" height="720" opacity="0.72"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="74" y="104" width="1132" height="540" rx="30" fill="#071027" opacity="0.58" filter="url(#softShadow)"/>

  <text x="96" y="72" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#FFFFFF">
    Metaverse Market Potential
  </text>
  <text x="98" y="104" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#AAB6D6">
    Forecast market size, 2022–2030 · USD trillions
  </text>
  <text x="990" y="74" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFEB65" text-anchor="end">
    CAGR acceleration signal
  </text>

  <line x1="130" y1="195" x2="1170" y2="195" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="130" y1="273" x2="1170" y2="273" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="130" y1="351" x2="1170" y2="351" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="130" y1="429" x2="1170" y2="429" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="130" y1="507" x2="1170" y2="507" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="130" y1="585" x2="1170" y2="585" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="1.5"/>

  <text x="86" y="200" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B7C1DF" text-anchor="end">$5T</text>
  <text x="86" y="278" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B7C1DF" text-anchor="end">$4T</text>
  <text x="86" y="356" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B7C1DF" text-anchor="end">$3T</text>
  <text x="86" y="434" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B7C1DF" text-anchor="end">$2T</text>
  <text x="86" y="512" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B7C1DF" text-anchor="end">$1T</text>

  <path d="M130 569
           C178 566 214 565 260 563
           C310 560 346 555 390 550
           C442 544 475 535 520 533
           C574 528 604 508 650 508
           C704 502 735 475 780 470
           C836 463 864 419 910 414
           C965 407 995 338 1040 330
           C1098 319 1124 224 1170 206
           L1170 585 L130 585 Z"
        fill="url(#areaGlow)" stroke="none"/>

  <path d="M130 569
           C178 566 214 565 260 563
           C310 560 346 555 390 550
           C442 544 475 535 520 533
           C574 528 604 508 650 508
           C704 502 735 475 780 470
           C836 463 864 419 910 414
           C965 407 995 338 1040 330
           C1098 319 1124 224 1170 206"
        fill="none" stroke="#FFE100" stroke-width="18" stroke-opacity="0.28"
        stroke-linecap="round" stroke-linejoin="round" filter="url(#trendGlow)"/>

  <path d="M130 569
           C178 566 214 565 260 563
           C310 560 346 555 390 550
           C442 544 475 535 520 533
           C574 528 604 508 650 508
           C704 502 735 475 780 470
           C836 463 864 419 910 414
           C965 407 995 338 1040 330
           C1098 319 1124 224 1170 206"
        fill="none" stroke="#FFE64D" stroke-width="5"
        stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="130" cy="569" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="260" cy="563" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="390" cy="550" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="520" cy="533" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="650" cy="508" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="780" cy="470" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="910" cy="414" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="1040" cy="330" r="6" fill="url(#pointCore)" filter="url(#trendGlow)"/>
  <circle cx="1170" cy="206" r="8" fill="url(#pointCore)" filter="url(#trendGlow)"/>

  <text x="130" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2022</text>
  <text x="260" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2023</text>
  <text x="390" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2024</text>
  <text x="520" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2025</text>
  <text x="650" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2026</text>
  <text x="780" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2027</text>
  <text x="910" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2028</text>
  <text x="1040" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEF7" text-anchor="middle">2029</text>
  <text x="1170" y="620" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" text-anchor="middle">2030</text>

  <text x="144" y="542" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AAB6D6">Initial market</text>
  <text x="1102" y="176" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="end">$4.86T</text>
  <text x="1088" y="200" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFEB65" text-anchor="end">projected by 2030</text>
</svg>
```

## Avoid in this skill
- ❌ Native PowerPoint chart objects if the goal is a custom illuminated look; draw the trend as editable SVG paths instead.
- ❌ Applying `filter` to `<line>` gridlines or axes; filters on lines are dropped, so keep gridlines flat and subtle.
- ❌ Using `<mask>` to fade the area fill; use a vertical `linearGradient` with stop opacity instead.
- ❌ Clipping the area or line paths with `clip-path`; clipping is only reliable for `<image>` elements in this workflow.
- ❌ Overloading the chart with legends, dense tick labels, or many competing series; the effect works best with one dominant glowing trend.

## Composition notes
- Keep the chart large: roughly 80–85% slide width and 60% slide height, with the title above and only compact annotations inside the plot.
- Use a dark background and very low-opacity gridlines so the yellow/green illuminated data path carries the visual energy.
- The filled area should be softer than the line: translucent gradient below, thick blurred halo behind, crisp 4–6 px stroke on top.
- Put the most important callout near the final data point; the eye naturally follows the glowing trendline to the upper-right endpoint.