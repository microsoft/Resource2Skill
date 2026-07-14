# SVG Recipe — Data Dashboard Pictogram Waffle Matrix

## Visual mechanism
A 10×10 matrix of repeated editable pictograms turns percentage data into a countable “waffle” area chart, where each icon represents 1%. Large percentage callouts sit beside the matrix and align vertically with the corresponding filled color bands.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark dashboard background.
- 1× `<rect>` for the elevated dashboard card.
- 1× translucent `<rect>` behind the active data block to create a soft color wash.
- 100× `<circle>` for pictogram heads.
- 100× rounded `<rect>` for pictogram bodies.
- 1× `<path>` for an abstract decorative dashboard accent.
- 6× `<text>` elements for title, subtitle, percentage callouts, labels, and chart caption.
- 1× `<linearGradient>` for the deep executive dashboard background.
- 1× `<linearGradient>` for the card fill.
- 1× `<radialGradient>` for ambient color glow.
- 1× `<filter id="cardShadow">` applied to the card rectangle.
- 1× `<filter id="softGlow">` applied to the active data wash rectangle.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="55%" stop-color="#141822"/>
      <stop offset="100%" stop-color="#0B1020"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="96" x2="0" y2="642">
      <stop offset="0%" stop-color="#202838"/>
      <stop offset="100%" stop-color="#151B27"/>
    </linearGradient>
    <radialGradient id="ambientCyan" cx="78%" cy="55%" r="52%">
      <stop offset="0%" stop-color="#2DE1C3" stop-opacity="0.28"/>
      <stop offset="60%" stop-color="#2DE1C3" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#2DE1C3" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="960" cy="390" rx="420" ry="300" fill="url(#ambientCyan)"/>
  <path d="M42,620 C170,560 232,682 374,612 C478,560 510,610 594,570" fill="none" stroke="#2DE1C3" stroke-width="2" stroke-opacity="0.22" stroke-dasharray="7 11"/>

  <rect x="58" y="82" width="1064" height="560" rx="34" fill="url(#cardGrad)" stroke="#2A3446" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="610" y="342" width="430" height="220" rx="28" fill="#2DE1C3" opacity="0.10" filter="url(#softGlow)"/>

  <text x="90" y="142" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#F5F7FA">Workforce adoption split</text>
  <text x="90" y="177" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9CA8BA">Each editable pictogram represents 1% of the measured employee base.</text>

  <text x="520" y="284" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#5D6878">42%</text>
  <text x="520" y="315" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#9CA8BA">not yet activated</text>

  <text x="520" y="452" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800" fill="#2DE1C3">58%</text>
  <text x="520" y="486" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D9FFF8">active platform users</text>

  <text x="840" y="130" width="430" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E6ECF5">10×10 pictogram waffle matrix</text>

  <g fill="#374150" stroke="#141822" stroke-width="1.2">
    <g transform="translate(640 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(960 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 160)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
    <g transform="translate(640 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(960 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 200)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
    <g transform="translate(640 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(960 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 240)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
    <g transform="translate(640 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(960 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 280)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
    <g transform="translate(960 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
  </g>

  <g fill="#2DE1C3" stroke="#141822" stroke-width="1.2">
    <g transform="translate(640 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 320)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
    <g transform="translate(640 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(960 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 360)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g>
    <g transform="translate(640 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(680 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(720 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(760 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(800 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(840 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(880 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(920 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(960 400)"><circle cx="14" cy="8" r="6"/><rect x="4" y="18" width="20" height="16" rx="5"/></g><g transform="translate(1000 400)"><circle cx="14"