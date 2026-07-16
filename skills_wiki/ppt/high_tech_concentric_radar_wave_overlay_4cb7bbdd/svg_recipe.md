# SVG Recipe — High-Tech Concentric Radar Wave Overlay

## Visual mechanism
A dark cyber-HUD canvas is energized by dense neon concentric radar rings radiating from a left-of-center focal point, with glowing orange target nodes and a central product cutout layered above the waves. The right side stays structured and typographic, turning technical specs into a premium “detection interface” rather than a static chart.

## SVG primitives needed
- 1× `<rect>` for the near-black full-slide background
- 1× `<rect>` with radial/linear gradient overlays for subtle vignette and atmospheric depth
- 24× `<circle>` for concentric radar rings with decaying opacity
- 4× `<line>` for crosshair axes around the radar origin
- 4× glowing target marker groups, each using blurred `<circle>` halo + solid `<circle>` core + small ring
- 1× `<image>` for the central transparent product / hardware cutout
- 1× `<rect>` for the right-side translucent information panel
- Multiple `<text>` elements with explicit `width` for title, subtitle, metric labels, and values
- 6× `<path>` for angular HUD brackets, scan ticks, and decorative circuit accents
- 2× `<linearGradient>` for panel and accent fills
- 1× `<radialGradient>` for background glow behind the radar
- 3× `<filter>` definitions: cyan glow, orange target glow, soft panel shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="34%" cy="54%" r="58%">
      <stop offset="0%" stop-color="#07352b" stop-opacity="0.85"/>
      <stop offset="45%" stop-color="#031512" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#050507" stop-opacity="1"/>
    </radialGradient>
    <linearGradient id="panelGrad" x1="840" y1="90" x2="1220" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#10201e" stop-opacity="0.86"/>
      <stop offset="100%" stop-color="#050707" stop-opacity="0.72"/>
    </linearGradient>
    <linearGradient id="cyanLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00ff99"/>
      <stop offset="100%" stop-color="#00d8ff"/>
    </linearGradient>
    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="orangeGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#050507"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <circle cx="430" cy="395" r="32" fill="none" stroke="#00ff99" stroke-width="2.4" opacity="0.95" filter="url(#cyanGlow)"/>
  <circle cx="430" cy="395" r="52" fill="none" stroke="#00ff99" stroke-width="2.2" opacity="0.88"/>
  <circle cx="430" cy="395" r="74" fill="none" stroke="#00ff99" stroke-width="2.1" opacity="0.80"/>
  <circle cx="430" cy="395" r="98" fill="none" stroke="#00ff99" stroke-width="2" opacity="0.72"/>
  <circle cx="430" cy="395" r="123" fill="none" stroke="#00ff99" stroke-width="1.9" opacity="0.64"/>
  <circle cx="430" cy="395" r="149" fill="none" stroke="#00ff99" stroke-width="1.8" opacity="0.57"/>
  <circle cx="430" cy="395" r="176" fill="none" stroke="#00ff99" stroke-width="1.7" opacity="0.50"/>
  <circle cx="430" cy="395" r="203" fill="none" stroke="#00ff99" stroke-width="1.6" opacity="0.44"/>
  <circle cx="430" cy="395" r="231" fill="none" stroke="#00ff99" stroke-width="1.5" opacity="0.38"/>
  <circle cx="430" cy="395" r="259" fill="none" stroke="#00ff99" stroke-width="1.45" opacity="0.33"/>
  <circle cx="430" cy="395" r="287" fill="none" stroke="#00ff99" stroke-width="1.35" opacity="0.28"/>
  <circle cx="430" cy="395" r="315" fill="none" stroke="#00ff99" stroke-width="1.25" opacity="0.23"/>
  <circle cx="430" cy="395" r="343" fill="none" stroke="#00ff99" stroke-width="1.15" opacity="0.19"/>
  <circle cx="430" cy="395" r="371" fill="none" stroke="#00ff99" stroke-width="1.05" opacity="0.15"/>
  <circle cx="430" cy="395" r="399" fill="none" stroke="#00ff99" stroke-width="1" opacity="0.12"/>

  <line x1="90" y1="395" x2="770" y2="395" stroke="#00ff99" stroke-width="1.2" opacity="0.18" stroke-dasharray="7 12"/>
  <line x1="430" y1="65" x2="430" y2="690" stroke="#00ff99" stroke-width="1.2" opacity="0.18" stroke-dasharray="7 12"/>
  <line x1="190" y1="155" x2="670" y2="635" stroke="#00ff99" stroke-width="1" opacity="0.11" stroke-dasharray="5 16"/>
  <line x1="675" y1="145" x2="185" y2="635" stroke="#00ff99" stroke-width="1" opacity="0.11" stroke-dasharray="5 16"/>

  <path d="M184 138 L244 138 L244 150 M184 138 L184 198" fill="none" stroke="url(#cyanLine)" stroke-width="2" opacity="0.75"/>
  <path d="M690 138 L630 138 L630 150 M690 138 L690 198" fill="none" stroke="url(#cyanLine)" stroke-width="2" opacity="0.65"/>
  <path d="M160 618 L220 618 L220 606 M160 618 L160 558" fill="none" stroke="url(#cyanLine)" stroke-width="2" opacity="0.55"/>
  <path d="M716 610 L656 610 L656 598 M716 610 L716 550" fill="none" stroke="url(#cyanLine)" stroke-width="2" opacity="0.45"/>

  <circle cx="270" cy="515" r="36" fill="#ff6600" opacity="0.22" filter="url(#orangeGlow)"/>
  <circle cx="270" cy="515" r="13" fill="#ff6600"/>
  <circle cx="270" cy="515" r="25" fill="none" stroke="#ff9a3d" stroke-width="1.6" opacity="0.75"/>
  <circle cx="575" cy="455" r="32" fill="#ff6600" opacity="0.20" filter="url(#orangeGlow)"/>
  <circle cx="575" cy="455" r="11" fill="#ff6600"/>
  <circle cx="575" cy="455" r="23" fill="none" stroke="#ff9a3d" stroke-width="1.4" opacity="0.72"/>
  <circle cx="342" cy="250" r="28" fill="#ff6600" opacity="0.17" filter="url(#orangeGlow)"/>
  <circle cx="342" cy="250" r="9" fill="#ff6600"/>
  <circle cx="342" cy="250" r="20" fill="none" stroke="#ff9a3d" stroke-width="1.2" opacity="0.68"/>

  <image x="228" y="214" width="430" height="260" href="https://images.example.com/transparent-cutout-autonomous-radar-drone.png" preserveAspectRatio="xMidYMid meet"/>

  <rect x="820" y="76" width="390" height="568" rx="28" fill="url(#panelGrad)" stroke="#00ff99" stroke-width="1.2" opacity="0.96" filter="url(#panelShadow)"/>
  <path d="M848 116 L892 116 M848 116 L848 160" fill="none" stroke="#00ff99" stroke-width="2.2" opacity="0.85"/>
  <path d="M1182 604 L1138 604 M1182 604 L1182 560" fill="none" stroke="#00ff99" stroke-width="2.2" opacity="0.65"/>
  <text x="860" y="145" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#ffffff">高性能雷达探测</text>
  <text x="862" y="178" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2.2" fill="#00ff99">HIGH-PERFORMANCE RADAR DETECTION</text>
  <line x1="862" y1="205" x2="1156" y2="205" stroke="#00ff99" stroke-width="1.2" opacity="0.35"/>

  <text x="862" y="257" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#8ea3a0">SCAN RADIUS</text>
  <text x="1040" y="260" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#00ff99">12.8km</text>
  <text x="862" y="326" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#8ea3a0">TARGET LOCK</text>
  <text x="1040" y="329" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ff8a2a">98.6%</text>
  <text x="862" y="395" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#8ea3a0">LATENCY</text>
  <text x="1040" y="398" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff">14ms</text>

  <rect x="862" y="444" width="294" height="76" rx="14" fill="#071412" stroke="#00ff99" stroke-width="1" opacity="0.86"/>
  <text x="884" y="475" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#dcefeb">Adaptive pulse compression and multi-node fusion maintain precision under high-noise conditions.</text>
  <text x="862" y="578" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="1.6" fill="#5effc2">SYSTEM STATUS / ACTIVE MONITORING</text>
  <line x1="862" y1="596" x2="1156" y2="596" stroke="#00ff99" stroke-width="4" opacity="0.85"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<pattern>` to generate the rings; create individual editable `<circle>` rings instead.
- ❌ Applying `filter` to `<line>` crosshairs; line filters are dropped, so use low opacity and dashed strokes instead.
- ❌ Using `<mask>` for the radar fade; translate the fade with per-ring opacity.
- ❌ Using `<use>` or `<symbol>` to duplicate rings or target nodes; explicitly draw each element.
- ❌ Putting `clip-path` on circles, paths, or groups; only use clipping on `<image>` if a shaped photo crop is required.

## Composition notes
- Keep the radar origin left-of-center, occupying roughly 60% of the slide; let outer rings bleed toward the edges for scale.
- Place structured metrics in a right-side translucent panel so the high-energy wave field does not compete with text legibility.
- Use cyan/green for sensing, precision, and system state; reserve orange only for target locks or alert markers.
- Layer order matters: dark background → radar rings/crosshairs → glowing nodes → product cutout → typography and panel.