# SVG Recipe — Dark Mode Neon Glassmorphism Dashboard

## Visual mechanism
A deep navy canvas is energized by oversized blurred neon auras, then covered with semi-transparent rounded dashboard cards that feel like frosted glass. High-contrast white typography, cyan/magenta data strokes, glowing charts, and crisp low-opacity borders create a premium dark-mode SaaS interface.

## SVG primitives needed
- 1× full-slide `<rect>` for the deep dark base background
- 4× blurred `<circle>` / `<ellipse>` neon aura shapes for cyan, magenta, violet, and blue light fields
- 1× subtle `<linearGradient>` overlay for vignette/depth
- 4× large rounded `<rect>` glass cards with semi-transparent fills, thin borders, and soft shadows
- Multiple small `<rect>` elements for metric pills, progress bars, axis ticks, and micro UI blocks
- 3× `<path>` elements for the main glowing line chart, secondary chart fill, and decorative wave accents
- 3× `<circle>` / stroked donut elements for radial KPI visualization
- 1× `<clipPath>` with circular crop applied to a small `<image>` avatar/logo
- 2× `<filter>` definitions: heavy blur for neon auras and soft shadow/glow for cards and chart strokes
- Multiple `<text>` elements with explicit `width` attributes for title, labels, values, axis labels, and KPI callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#151827"/>
      <stop offset="55%" stop-color="#0A0B10"/>
      <stop offset="100%" stop-color="#05060A"/>
    </linearGradient>
    <linearGradient id="cardEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.32"/>
      <stop offset="45%" stop-color="#7B8194" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0.22"/>
    </linearGradient>
    <linearGradient id="chartStroke" x1="210" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="50%" stop-color="#9B5CFF"/>
      <stop offset="100%" stop-color="#FF0080"/>
    </linearGradient>
    <linearGradient id="chartFill" x1="0" y1="260" x2="0" y2="570" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0"/>
    </linearGradient>
    <filter id="neonBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="55"/>
    </filter>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="20"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="chartGlow" x="-20%" y="-60%" width="140%" height="220%">
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="avatarCrop">
      <circle cx="1162" cy="74" r="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgVignette)"/>
  <ellipse cx="145" cy="410" rx="255" ry="210" fill="#00E5FF" opacity="0.42" filter="url(#neonBlur)"/>
  <ellipse cx="1060" cy="150" rx="260" ry="190" fill="#FF0080" opacity="0.44" filter="url(#neonBlur)"/>
  <circle cx="660" cy="625" r="245" fill="#702DFF" opacity="0.34" filter="url(#neonBlur)"/>
  <ellipse cx="790" cy="260" rx="210" ry="130" fill="#224BFF" opacity="0.26" filter="url(#neonBlur)"/>

  <text x="70" y="76" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">Portfolio Overview</text>
  <text x="72" y="108" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#96A0B4">Live asset intelligence · dark mode executive dashboard</text>
  <rect x="1040" y="45" width="152" height="58" rx="29" fill="#1A1E29" fill-opacity="0.62" stroke="#5E6578" stroke-opacity="0.65"/>
  <image href="https://images.example.com/avatar-fintech-operator.jpg" x="1138" y="50" width="48" height="48" clip-path="url(#avatarCrop)"/>
  <text x="1060" y="69" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#96A0B4">Status</text>
  <text x="1060" y="88" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#53FFCF">Healthy</text>

  <rect x="70" y="138" width="704" height="500" rx="32" fill="#1A1E29" fill-opacity="0.82" stroke="url(#cardEdge)" stroke-width="1.4" filter="url(#softShadow)"/>
  <text x="112" y="195" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Total Portfolio Value</text>
  <text x="112" y="252" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="750" fill="#FFFFFF">$129,987.05</text>
  <text x="116" y="286" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#53FFCF">▲ +14.5% this quarter</text>
  <rect x="565" y="180" width="146" height="42" rx="21" fill="#00E5FF" fill-opacity="0.11" stroke="#00E5FF" stroke-opacity="0.45"/>
  <text x="589" y="207" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#BFF8FF">REAL-TIME</text>

  <line x1="126" y1="532" x2="704" y2="532" stroke="#546073" stroke-opacity="0.35"/>
  <line x1="126" y1="452" x2="704" y2="452" stroke="#546073" stroke-opacity="0.22"/>
  <line x1="126" y1="372" x2="704" y2="372" stroke="#546073" stroke-opacity="0.22"/>
  <line x1="126" y1="292" x2="704" y2="292" stroke="#546073" stroke-opacity="0.22"/>
  <path d="M126 532 C185 500, 210 462, 264 470 C330 480, 340 395, 402 398 C460 400, 478 325, 535 338 C602 354, 632 275, 704 246 L704 560 L126 560 Z" fill="url(#chartFill)"/>
  <path d="M126 532 C185 500, 210 462, 264 470 C330 480, 340 395, 402 398 C460 400, 478 325, 535 338 C602 354, 632 275, 704 246" fill="none" stroke="url(#chartStroke)" stroke-width="5.5" stroke-linecap="round" filter="url(#chartGlow)"/>
  <circle cx="704" cy="246" r="8" fill="#FF0080" stroke="#FFFFFF" stroke-width="3"/>
  <text x="125" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A8">Jan</text>
  <text x="258" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A8">Mar</text>
  <text x="393" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A8">May</text>
  <text x="529" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A8">Jul</text>
  <text x="665" y="590" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8792A8">Sep</text>

  <rect x="812" y="138" width="398" height="220" rx="30" fill="#1A1E29" fill-opacity="0.82" stroke="url(#cardEdge)" stroke-width="1.4" filter="url(#softShadow)"/>
  <text x="846" y="190" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Risk Exposure</text>
  <text x="846" y="235" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="750" fill="#FFFFFF">27%</text>
  <text x="846" y="265" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#96A0B4">Below target volatility</text>
  <circle cx="1110" cy="246" r="58" fill="none" stroke="#34394A" stroke-width="18"/>
  <circle cx="1110" cy="246" r="58" fill="none" stroke="#00E5FF" stroke-width="18" stroke-linecap="round" stroke-dasharray="98 266" transform="rotate(-90 1110 246)" filter="url(#chartGlow)"/>
  <text x="1082" y="254" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Low</text>

  <rect x="812" y="390" width="398" height="248" rx="30" fill="#1A1E29" fill-opacity="0.82" stroke="url(#cardEdge)" stroke-width="1.4" filter="url(#softShadow)"/>
  <text x="846" y="444" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Allocation Mix</text>
  <text x="846" y="479" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#96A0B4">Weighted by liquidity score</text>
  <rect x="846" y="520" width="280" height="12" rx="6" fill="#34394A"/>
  <rect x="846" y="520" width="188" height="12" rx="6" fill="#00E5FF"/>
  <text x="1142" y="533" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF">67%</text>
  <rect x="846" y="558" width="280" height="12" rx="6" fill="#34394A"/>
  <rect x="846" y="558" width="126" height="12" rx="6" fill="#9B5CFF"/>
  <text x="1142" y="571" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF">45%</text>
  <rect x="846" y="596" width="280" height="12" rx="6" fill="#34394A"/>
  <rect x="846" y="596" width="224" height="12" rx="6" fill="#FF0080"/>
  <text x="1142" y="609" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF">80%</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; PowerPoint will not preserve true background blur, so simulate glass with semi-transparent dark fills, glowing auras, and thin light borders.
- ❌ Do not apply `filter` to `<line>` elements; use filtered `<path>` for glowing chart strokes instead.
- ❌ Do not place `clip-path` on cards or chart shapes; only use clipping on `<image>` elements if adding avatars, logos, or screenshots.
- ❌ Do not rely on masks, patterns, or animated gradient movement for the neon atmosphere; use blurred SVG circles/ellipses and gradients.
- ❌ Avoid dense gridlines and small dashboard labels; dark-mode glass layouts need generous spacing and high contrast.

## Composition notes
- Keep the largest glass card on the left occupying roughly 55% of the slide width; this is the hero data story and should contain the most expressive chart.
- Use the right column for compact supporting widgets: one radial KPI card and one allocation/progress card keeps the dashboard executive-friendly.
- Place neon auras behind card clusters, not evenly across the slide; cyan behind the hero chart and magenta/violet behind the right cards creates depth.
- Maintain a disciplined palette: white for primary values, steel blue-gray for labels, and only 2–3 neon accents for data emphasis.