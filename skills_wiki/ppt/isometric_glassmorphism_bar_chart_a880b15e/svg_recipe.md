# SVG Recipe — Isometric Glassmorphism Bar Chart

## Visual mechanism
Build each bar as a fake 3D isometric prism using separate vector faces: two vertical side faces, a diamond top cap, and a semi-transparent highlight slice. Place the bars on a layered cylindrical stage over a dark atmospheric gradient, then add translucent UI panels and glow/shadow filters for a premium glassmorphism dashboard look.

## SVG primitives needed
- 1× `<rect>` for the full-slide atmospheric gradient background
- 2× `<circle>` for blurred radial color glows behind the chart
- 3× `<path>` for abstract background wave silhouettes
- 2× `<rect>` for the floating glass UI panel and its header chip
- 6× `<line>` for subtle panel grid ticks and connector accents
- 1× `<path>` for the mini line chart inside the glass panel
- 2× `<ellipse>` + 1× `<rect>` for the layered cylindrical stage
- 16× `<path>` for four isometric bars: left face, right face, top diamond, and glass highlight per bar
- 4× `<ellipse>` for soft contact shadows under the pillars
- 10× `<text>` labels for title, KPI panel, bar values, and category labels; every text element includes `width`
- Multiple `<linearGradient>` definitions for background, stage, bar faces, top caps, and glass fills
- 2× `<radialGradient>` definitions for ambient light blooms
- 2× `<filter>` definitions: one soft shadow and one glow, applied only to rect/path/ellipse/text elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A0B2E"/>
      <stop offset="55%" stop-color="#0B132B"/>
      <stop offset="100%" stop-color="#050816"/>
    </linearGradient>
    <radialGradient id="cyanBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#36F4FF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#36F4FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="magentaBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF4FD8" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#FF4FD8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#8DDCFF" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="stageTop" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#233B75"/>
      <stop offset="55%" stop-color="#13224A"/>
      <stop offset="100%" stop-color="#090E24"/>
    </linearGradient>
    <linearGradient id="stageSide" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#17285A"/>
      <stop offset="100%" stop-color="#070A19"/>
    </linearGradient>
    <linearGradient id="orangeFace" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FFD36B"/><stop offset="100%" stop-color="#F05A28"/></linearGradient>
    <linearGradient id="orangeDark" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FF9D3D"/><stop offset="100%" stop-color="#9D2A20"/></linearGradient>
    <linearGradient id="cyanFace" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#65FFF2"/><stop offset="100%" stop-color="#158CFF"/></linearGradient>
    <linearGradient id="cyanDark" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#20BEEB"/><stop offset="100%" stop-color="#0E3A94"/></linearGradient>
    <linearGradient id="pinkFace" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FF8DF3"/><stop offset="100%" stop-color="#8B4DFF"/></linearGradient>
    <linearGradient id="pinkDark" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#C35BFF"/><stop offset="100%" stop-color="#431B96"/></linearGradient>
    <linearGradient id="limeFace" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#D9FF72"/><stop offset="100%" stop-color="#12D6A1"/></linearGradient>
    <linearGradient id="limeDark" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#79E96A"/><stop offset="100%" stop-color="#087D6A"/></linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="18"/><feGaussianBlur stdDeviation="18"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <circle cx="880" cy="225" r="290" fill="url(#cyanBloom)" filter="url(#glow)"/>
  <circle cx="440" cy="520" r="260" fill="url(#magentaBloom)" filter="url(#glow)"/>
  <path d="M0 610 C190 535 300 585 455 520 C650 438 810 542 980 475 C1120 420 1195 455 1280 395 L1280 720 L0 720 Z" fill="#111B3C" opacity="0.55"/>
  <path d="M0 690 C220 595 360 655 560 585 C750 520 940 610 1280 500 L1280 720 L0 720 Z" fill="#081126" opacity="0.82"/>
  <path d="M750 120 C855 75 1005 92 1088 150 C1008 132 875 147 750 120 Z" fill="#FFFFFF" opacity="0.08"/>

  <rect x="78" y="92" width="355" height="430" rx="32" fill="url(#glass)" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5" filter="url(#shadow)"/>
  <rect x="106" y="124" width="126" height="34" rx="17" fill="#FFFFFF" opacity="0.12"/>
  <text x="124" y="147" width="180" fill="#BCEFFF" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700">LIVE METRICS</text>
  <text x="108" y="212" width="290" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700">Sales velocity</text>
  <text x="110" y="250" width="280" fill="#A7B3D7" font-family="Segoe UI, Microsoft YaHei" font-size="17">Glassmorphic isometric bars for executive KPI storytelling.</text>
  <line x1="115" y1="330" x2="380" y2="330" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="115" y1="382" x2="380" y2="382" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="115" y1="434" x2="380" y2="434" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <path d="M120 432 C155 396 178 415 210 374 C244 329 270 358 304 315 C330 282 352 296 382 262" fill="none" stroke="#5AF7FF" stroke-width="5" stroke-linecap="round" filter="url(#glow)"/>
  <text x="108" y="485" width="130" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700">+38%</text>
  <text x="226" y="482" width="150" fill="#A7B3D7" font-family="Segoe UI, Microsoft YaHei" font-size="15">QoQ growth index</text>

  <text x="585" y="92" width="520" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" letter-spacing="2">SALES REPORT</text>
  <text x="590" y="128" width="420" fill="#8EA5D8" font-family="Segoe UI, Microsoft YaHei" font-size="18">volumetric performance by region</text>

  <ellipse cx="825" cy="598" rx="390" ry="84" fill="#030510" opacity="0.55"/>
  <rect x="435" y="548" width="780" height="72" fill="url(#stageSide)"/>
  <ellipse cx="825" cy="548" rx="390" ry="84" fill="url(#stageTop)" stroke="#78E6FF" stroke-opacity="0.18" stroke-width="2" filter="url(#shadow)"/>
  <ellipse cx="825" cy="546" rx="310" ry="54" fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="2" stroke-dasharray="10 12"/>

  <ellipse cx="610" cy="566" rx="76" ry="24" fill="#000000" opacity="0.28"/>
  <path d="M560 280 L610 304 L610 580 L560 556 Z" fill="url(#orangeDark)"/>
  <path d="M660 280 L610 304 L610 580 L660 556 Z" fill="url(#orangeFace)" filter="url(#shadow)"/>
  <path d="M610 232 L660 280 L610 304 L560 280 Z" fill="#FFD36B" filter="url(#glow)"/>
  <path d="M628 294 L660 280 L660 556 L628 570 Z" fill="#FFFFFF" opacity="0.16"/>

  <ellipse cx="760" cy="566" rx="80" ry="25" fill="#000000" opacity="0.30"/>
  <path d="M708 345 L760 370 L760 580 L708 555 Z" fill="url(#cyanDark)"/>
  <path d="M812 345 L760 370 L760 580 L812 555 Z" fill="url(#cyanFace)" filter="url(#shadow)"/>
  <path d="M760 296 L812 345 L760 370 L708 345 Z" fill="#65FFF2" filter="url(#glow)"/>
  <path d="M778 360 L812 345 L812 555 L778 570 Z" fill="#FFFFFF" opacity="0.18"/>

  <ellipse cx="915" cy="566" rx="84" ry="26" fill="#000000" opacity="0.31"/>
  <path d="M860 210 L915 236 L915 580 L860 554 Z" fill="url(#pinkDark)"/>
  <path d="M970 210 L915 236 L915 580 L970 554 Z" fill="url(#pinkFace)" filter="url(#shadow)"/>
  <path d="M915 158 L970 210 L915 236 L860 210 Z" fill="#FF8DF3" filter="url(#glow)"/>
  <path d="M936 228 L970 210 L970 554 L936 570 Z" fill="#FFFFFF" opacity="0.17"/>

  <ellipse cx="1072" cy="566" rx="78" ry="24" fill="#000000" opacity="0.27"/>
  <path d="M1020 385 L1072 410 L1072 580 L1020 555 Z" fill="url(#limeDark)"/>
  <path d="M1124 385 L1072 410 L1072 580 L1124 555 Z" fill="url(#limeFace)" filter="url(#shadow)"/>
  <path d="M1072 336 L1124 385 L1072 410 L1020 385 Z" fill="#D9FF72" filter="url(#glow)"/>
  <path d="M1090 400 L1124 385 L1124 555 L1090 570 Z" fill="#FFFFFF" opacity="0.15"/>

  <text x="570" y="206" width="90" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700">72</text>
  <text x="720" y="270" width="90" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700">54</text>
  <text x="876" y="132" width="90" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700">91</text>
  <text x="1032" y="312" width="90" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700">43</text>
  <text x="555" y="647" width="110" fill="#96A6CF" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600">NORTH</text>
  <text x="708" y="647" width="110" fill="#96A6CF" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600">WEST</text>
  <text x="865" y="647" width="110" fill="#96A6CF" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600">APAC</text>
  <text x="1022" y="647" width="110" fill="#96A6CF" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600">EMEA</text>
</svg>
```

## Avoid in this skill
- ❌ Native PowerPoint chart objects; the effect depends on manually drawn vector prisms, not chart engines.
- ❌ `<polygon>` for the bar faces if your SVG-to-PPT path handling is more reliable; use explicit `<path d="... Z">` faces instead.
- ❌ `skewX`, `skewY`, or `matrix(...)` transforms to fake isometric projection; calculate the diamond and side-face coordinates directly.
- ❌ Filters on `<line>` grid marks; use opacity-only lines, and apply glow/shadow only to paths, rects, ellipses, circles, or text.
- ❌ Masked vector highlights; use semi-transparent white `<path>` overlays for the glass reflection strips.

## Composition notes
- Keep the volumetric bars right-of-center and reserve the left third for a floating glass KPI panel; this creates asymmetrical executive-slide balance.
- Use a dark navy/purple background so neon gradients and translucent white highlights read as luminous glass.
- The stage should occupy the lower 25–30% of the slide, with bars rising from it and value labels floating just above each top diamond.
- Limit categories to 3–5 bars; the technique is meant for hero metrics, not dense analytical comparisons.