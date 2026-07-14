# SVG Recipe — Modern Neumorphic Gantt Timeline

## Visual mechanism
A soft “track and fill” Gantt layout: each phase sits on a recessed, pale rounded track, while saturated pill bars show scheduled duration. The neumorphic feel comes from subtle gradients, paired highlights/shadows, and generous spacing rather than dense gridlines.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft background.
- 2× `<path>` for large blurred decorative corner blobs that make the slide feel premium without competing with the chart.
- 12× `<text>` for rotated month headers.
- 6× `<text>` for left-side phase names.
- 6× `<text>` for right-side status/date labels.
- 6× large rounded `<rect>` for recessed background tracks.
- 6× smaller rounded `<rect>` overlays for inner trough highlights.
- 6× colored pill `<rect>` for active Gantt durations.
- 6× tiny `<circle>` or `<ellipse>` status dots aligned to row labels.
- 11× vertical `<line>` elements for light month separators.
- 1× `<filter id="softShadow">` applied to tracks and cards.
- 1× `<filter id="barShadow">` applied to colored active bars.
- Multiple `<linearGradient>` definitions for background, tracks, and colored bars.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="55%" stop-color="#eef3f7"/>
      <stop offset="100%" stop-color="#e6edf3"/>
    </linearGradient>

    <linearGradient id="trackGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f8fbfd"/>
      <stop offset="50%" stop-color="#e9eef3"/>
      <stop offset="100%" stop-color="#dfe6ed"/>
    </linearGradient>

    <linearGradient id="troughGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#dbe3eb"/>
      <stop offset="100%" stop-color="#f7fafc"/>
    </linearGradient>

    <linearGradient id="amberBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f7c85f"/>
      <stop offset="100%" stop-color="#f29b38"/>
    </linearGradient>
    <linearGradient id="coralBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff8a6b"/>
      <stop offset="100%" stop-color="#e85050"/>
    </linearGradient>
    <linearGradient id="magentaBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c85d8f"/>
      <stop offset="100%" stop-color="#83305d"/>
    </linearGradient>
    <linearGradient id="blueBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#48a6d9"/>
      <stop offset="100%" stop-color="#1e5f89"/>
    </linearGradient>
    <linearGradient id="tealBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#54c6b3"/>
      <stop offset="100%" stop-color="#207f7a"/>
    </linearGradient>
    <linearGradient id="navyBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#44546a"/>
      <stop offset="100%" stop-color="#1f2937"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="5" dy="7"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="barShadow" x="-20%" y="-50%" width="140%" height="200%">
      <feOffset dx="0" dy="7"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurBlob" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M1050,-40 C1180,20 1240,110 1290,250 C1160,250 1080,205 1015,120 C970,62 978,10 1050,-40 Z" fill="#d8e9f5" opacity="0.65" filter="url(#blurBlob)"/>
  <path d="M-80,560 C70,495 185,535 270,665 C165,745 35,748 -90,705 C-128,650 -123,600 -80,560 Z" fill="#f4ded8" opacity="0.55" filter="url(#blurBlob)"/>

  <text x="86" y="72" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#26313f">Product Launch Roadmap</text>
  <text x="88" y="104" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7a8796">Modern neumorphic Gantt timeline · executive phase view</text>
  <rect x="1010" y="56" width="170" height="42" rx="21" fill="#f4f7fa" filter="url(#softShadow)"/>
  <circle cx="1034" cy="77" r="7" fill="#31b37c"/>
  <text x="1052" y="83" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#526071">FY 2026 PLAN</text>

  <text x="98" y="169" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#9aa6b2">WORKSTREAM</text>
  <text x="226" y="169" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#9aa6b2">TIMELINE</text>

  <line x1="230" y1="185" x2="230" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="305" y1="185" x2="305" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="380" y1="185" x2="380" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="455" y1="185" x2="455" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="530" y1="185" x2="530" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="605" y1="185" x2="605" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="680" y1="185" x2="680" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="755" y1="185" x2="755" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="830" y1="185" x2="830" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="905" y1="185" x2="905" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="980" y1="185" x2="980" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="1055" y1="185" x2="1055" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>
  <line x1="1130" y1="185" x2="1130" y2="628" stroke="#d8e0e8" stroke-width="1" stroke-dasharray="3 10"/>

  <text x="212" y="146" width="54" transform="rotate(-90 239 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">JAN</text>
  <text x="287" y="146" width="54" transform="rotate(-90 314 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">FEB</text>
  <text x="362" y="146" width="54" transform="rotate(-90 389 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">MAR</text>
  <text x="437" y="146" width="54" transform="rotate(-90 464 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">APR</text>
  <text x="512" y="146" width="54" transform="rotate(-90 539 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">MAY</text>
  <text x="587" y="146" width="54" transform="rotate(-90 614 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">JUN</text>
  <text x="662" y="146" width="54" transform="rotate(-90 689 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">JUL</text>
  <text x="737" y="146" width="54" transform="rotate(-90 764 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">AUG</text>
  <text x="812" y="146" width="54" transform="rotate(-90 839 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">SEP</text>
  <text x="887" y="146" width="54" transform="rotate(-90 914 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">OCT</text>
  <text x="962" y="146" width="54" transform="rotate(-90 989 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">NOV</text>
  <text x="1037" y="146" width="54" transform="rotate(-90 1064 146)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#546171">DEC</text>

  <circle cx="86" cy="226" r="6" fill="#f4b947"/><text x="104" y="232" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#334155">Discovery</text>
  <rect x="230" y="204" width="900" height="44" rx="22" fill="url(#trackGrad)" filter="url(#softShadow)"/><rect x="240" y="213" width="880" height="26" rx="13" fill="url(#troughGrad)" opacity="0.72"/><rect x="230" y="206" width="150" height="40" rx="20" fill="url(#amberBar)" filter="url(#barShadow)"/><text x="1148" y="232" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#8a96a3">JAN–FEB</text>

  <circle cx="86" cy="296" r="6" fill="#ef6c59"/><text x="104" y="302" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#334155">Strategy</text>
  <rect x="230" y="274" width="900" height="44" rx="22" fill="url(#trackGrad)" filter="url(#softShadow)"/><rect x="240" y="283" width="880" height="26" rx="13" fill="url(#troughGrad)" opacity="0.72"/><rect x="380" y="276" width="225" height="40" rx="20" fill="url(#coralBar)" filter="url(#barShadow)"/><text x="1148" y="302" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#8a96a3">MAR–MAY</text>

  <circle cx="86" cy="366" r="6" fill="#a94572"/><text x="104" y="372" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#334155">Design</text>
  <rect x="230" y="344" width="900" height="44" rx="22" fill="url(#trackGrad)" filter="url(#softShadow)"/><rect x="240" y="353" width="880" height="26" rx="13" fill="url(#troughGrad)" opacity="0.72"/><rect x="455" y="346" width="300" height="40" rx="20" fill="url(#magentaBar)" filter="url(#barShadow)"/><text x="1148" y="372" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#8a96a3">APR–JUL</text>

  <circle cx="86" cy="436" r="6" fill="#2e86ab"/><text x="104" y="442" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#334155">Build</text>
  <rect x="230" y="414" width="900" height="44" rx="22" fill="url(#trackGrad)" filter="url(#softShadow)"/><rect x="240" y="423" width="880" height="26" rx="13" fill="url(#troughGrad)" opacity="0.72"/><rect x="605" y="416" width="300" height="40" rx="20" fill="url(#blueBar)" filter="url(#barShadow)"/><text x="1148" y="442" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#8a96a3">JUN–SEP</text>

  <circle cx="86" cy="506" r="6" fill="#2f9e95"/><text x="104" y="512" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#334155">Launch</text>
  <rect x="230" y="484" width="900" height="44" rx="22" fill="url(#trackGrad)" filter="url(#softShadow)"/><rect x="240" y="493" width="880" height="26" rx="13" fill="url(#troughGrad)" opacity="0.72"/><rect x="830" y="486" width="225" height="40" rx="20" fill="url(#tealBar)" filter="url(#barShadow)"/><text x="1148" y="512" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#8a96a3">SEP–NOV</text>

  <circle cx="86" cy="576" r="6" fill="#334155"/><text x="104" y="582" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#334155">Scale</text>
  <rect x="230" y="554" width="900" height="44" rx="22" fill="url(#trackGrad)" filter="url(#softShadow)"/><rect x="240" y="563" width="880" height="26" rx="13" fill="url(#troughGrad)" opacity="0.72"/><rect x="980" y="556" width="150" height="40" rx="20" fill="url(#navyBar)" filter="url(#barShadow)"/><text x="1148" y="582" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#8a96a3">NOV–DEC</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` or `mask="url(#...)"` to create inner shadows; simulate recessed grooves with layered rounded rectangles, gradients, and soft shadows.
- ❌ Do not apply `filter` to `<line>` month separators; filters on lines are dropped.
- ❌ Do not use `marker-end` for milestone arrows; if arrows are needed, draw them as native `<line>` elements with direct attributes or use small triangle `<path>` shapes.
- ❌ Do not create a dense daily grid; this style works best as a high-level monthly or quarterly roadmap.
- ❌ Do not omit `width` on `<text>` elements, especially rotated month labels.

## Composition notes
- Keep the left label column compact, around 15–18% of slide width, so the colored bars dominate the visual field.
- Use generous vertical spacing: the gap between rows should feel almost as important as the bars themselves.
- Limit active bar colors to 4–6 saturated tones and keep all tracks pale gray-blue for a calm executive look.
- Place month labels above the chart and rotate them vertically to preserve horizontal room for long Gantt bars.