# SVG Recipe — Isometric Glassmorphism UI Stack

## Visual mechanism
A dark neon product slide where multiple translucent UI panels are drawn as manually projected isometric parallelograms, stacked with small depth offsets and soft glows. The glass layers partially reveal a darker “device” layer beneath, creating a premium floating dashboard / mobile-app render without relying on PowerPoint 3D.

## SVG primitives needed
- 1× `<rect>` for the deep navy slide background
- 2× blurred `<circle>` elements for ambient magenta and cyan light orbs
- 5× `<path>` elements for the isometric phone chassis, screen face, and side-depth faces
- 4× translucent `<path>` elements for floating glass UI panels
- 8× small `<path>` elements for projected UI cards, mini charts, and button tiles
- 3× stroked `<path>` elements for curved progress rings and line-chart traces
- 5× `<ellipse>` elements for projected circular controls / data nodes
- 1× `<line>` for the right-side headline accent
- 8× `<text>` elements with explicit `width` attributes for UI labels, metrics, and slide copy
- 2× `<linearGradient>` definitions for glass and device surfaces
- 2× `<radialGradient>` definitions for neon orb color
- 2× `<filter>` definitions: one Gaussian blur for glow, one offset+blur+merge shadow for floating depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="orbMagenta" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff0080" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#ff0080" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#ff0080" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orbCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.85"/>
      <stop offset="60%" stop-color="#00e5ff" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#00e5ff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="phoneFace" x1="220" y1="100" x2="770" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#252839"/>
      <stop offset="55%" stop-color="#171b2b"/>
      <stop offset="100%" stop-color="#0d111c"/>
    </linearGradient>
    <linearGradient id="glassFill" x1="250" y1="40" x2="720" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.26"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#9eefff" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <filter id="floatShadow" x="-30%" y="-30%" width="170%" height="170%">
      <feOffset dx="18" dy="26"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0d111c"/>
  <circle cx="250" cy="70" r="250" fill="url(#orbMagenta)" filter="url(#softGlow)" opacity="0.82"/>
  <circle cx="715" cy="560" r="290" fill="url(#orbCyan)" filter="url(#softGlow)" opacity="0.76"/>
  <circle cx="1025" cy="140" r="190" fill="url(#orbMagenta)" filter="url(#softGlow)" opacity="0.28"/>

  <path d="M230 182 L610 92 L800 430 L420 575 L230 182 Z" fill="#090b12" opacity="0.65" filter="url(#floatShadow)"/>
  <path d="M610 92 L800 430 L833 478 L642 136 Z" fill="#111522"/>
  <path d="M420 575 L800 430 L833 478 L448 622 Z" fill="#0a0d16"/>
  <path d="M230 182 L610 92 L800 430 L420 575 Z" fill="url(#phoneFace)" stroke="#555d70" stroke-width="3"/>
  <path d="M332 201 L566 145 L610 222 L376 280 Z" fill="#070912" opacity="0.95"/>

  <path d="M410 314 C425 252 472 202 526 192 C584 183 628 219 626 275" fill="none" stroke="#00e5ff" stroke-width="18" stroke-linecap="round"/>
  <path d="M626 275 C623 328 580 382 522 398 C469 412 421 385 410 314" fill="none" stroke="#31354a" stroke-width="18" stroke-linecap="round"/>
  <text x="474" y="292" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff" transform="rotate(-18 474 292)">5678</text>
  <text x="492" y="330" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#aab0c5" transform="rotate(-18 492 330)">STEPS</text>

  <path d="M342 385 L488 348 L545 447 L397 487 Z" fill="#1d2032" stroke="#343a52" stroke-width="2"/>
  <path d="M542 337 L688 300 L746 398 L598 441 Z" fill="#1d2032" stroke="#343a52" stroke-width="2"/>
  <ellipse cx="418" cy="413" rx="28" ry="18" fill="#ff0080" opacity="0.9"/>
  <ellipse cx="620" cy="367" rx="28" ry="18" fill="#00e5ff" opacity="0.9"/>
  <text x="456" y="415" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" transform="rotate(-18 456 415)">HEART</text>
  <text x="657" y="369" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" transform="rotate(-18 657 369)">WATER</text>

  <path d="M260 118 L594 38 L735 292 L400 380 Z" fill="url(#glassFill)" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2.5" filter="url(#floatShadow)"/>
  <path d="M302 146 L410 120 L442 177 L334 204 Z" fill="#ffffff" opacity="0.16" stroke="#ffffff" stroke-opacity="0.35"/>
  <path d="M455 108 L610 70 L644 130 L489 169 Z" fill="#00e5ff" opacity="0.13" stroke="#8ff6ff" stroke-opacity="0.45"/>
  <path d="M352 255 C398 214 449 245 490 207 C530 170 584 188 638 146" fill="none" stroke="#00e5ff" stroke-width="6" stroke-linecap="round" opacity="0.9"/>
  <ellipse cx="352" cy="255" rx="10" ry="7" fill="#00e5ff"/>
  <ellipse cx="490" cy="207" rx="10" ry="7" fill="#ffffff"/>
  <ellipse cx="638" cy="146" rx="10" ry="7" fill="#ff0080"/>

  <path d="M330 58 L620 -10 L710 152 L420 228 Z" fill="url(#glassFill)" stroke="#ffffff" stroke-opacity="0.48" stroke-width="2" opacity="0.92" filter="url(#floatShadow)"/>
  <path d="M382 72 L505 42 L526 80 L403 111 Z" fill="#ffffff" opacity="0.18"/>
  <path d="M536 35 L635 11 L658 51 L558 77 Z" fill="#ff0080" opacity="0.22"/>

  <path d="M285 430 L536 350 L665 568 L411 660 Z" fill="url(#glassFill)" stroke="#ffffff" stroke-opacity="0.44" stroke-width="2" filter="url(#floatShadow)"/>
  <path d="M346 475 L464 436 L500 497 L382 538 Z" fill="#ffffff" opacity="0.13"/>
  <path d="M499 424 L593 393 L629 453 L535 486 Z" fill="#00e5ff" opacity="0.16"/>
  <text x="392" y="505" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff" transform="rotate(-19 392 505)">84%</text>
  <text x="530" y="452" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#cfd7e6" transform="rotate(-19 530 452)">GOAL</text>

  <line x1="858" y1="214" x2="938" y2="214" stroke="#00e5ff" stroke-width="4" stroke-linecap="round"/>
  <text x="858" y="300" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="800" fill="#ffffff">FITNESS</text>
  <text x="858" y="362" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="800" fill="#00e5ff">OS</text>
  <text x="862" y="420" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#aab0c5">Layered health analytics with glass panels, live metrics, and premium dark-mode depth.</text>
  <text x="862" y="492" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ff4dac">DOWNLOAD TODAY</text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to create the isometric view; manually draw projected parallelogram paths instead.
- ❌ Applying `filter` to `<line>` elements for glow; use filtered circles/paths nearby or glowing strokes on `<path>`.
- ❌ Using `<mask>` or clip paths on non-image shapes to fake glass blur; PowerPoint translation will not preserve it reliably.
- ❌ Relying on real backdrop blur through transparent glass; simulate it with translucent gradient fills, bright borders, and softened glow objects.
- ❌ Arrow markers or inherited `marker-end`; if callouts are needed, draw simple `<line>` objects without markers or use small path triangles manually.

## Composition notes
- Keep the isometric stack in the left 60% of the slide, angled upward toward the center so it feels like a product reveal rather than a flat chart.
- Use a dark navy background with two or three oversized blurred neon orbs; the glass panels need visible color beneath them to feel translucent.
- Separate each floating layer by a consistent diagonal offset, usually up-left for higher layers and down-right for cast shadows.
- Reserve the right 35–40% for bold flat typography; this contrast makes the 3D/glass object feel more premium and intentional.