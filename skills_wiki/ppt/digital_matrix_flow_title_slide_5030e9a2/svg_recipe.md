# SVG Recipe — Digital Matrix Flow Title Slide

## Visual mechanism
A deep navy-black stage is pierced by blurred vertical cyan light columns, then overlaid with a rigid matrix of squares that dissolves from large, solid white blocks on the left into smaller, translucent blue artifacts on the right. Bottom-left typography sits in the densest, highest-contrast area, making the slide feel like a frozen frame of data streaming through an architecture grid.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 5× blurred `<rect>` vertical bands for volumetric server-rack/data-stream glow
- 8× low-opacity `<line>` elements for subtle structural grid guides
- 4× `<path>` elements for faint circuit/data-flow traces crossing the field
- 45–60× `<rect>` elements for the degrading square matrix, mixing filled and outlined blocks
- 1× translucent rounded `<rect>` behind the title for readability and executive polish
- 2× `<text>` elements with explicit `width` attributes for title and subtitle
- 2× `<linearGradient>` definitions for background and light-band color
- 2× `<filter>` definitions: one Gaussian blur for glow columns, one soft shadow for the text plate

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgNavy" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#05070D"/>
      <stop offset="48%" stop-color="#08101A"/>
      <stop offset="100%" stop-color="#020308"/>
    </linearGradient>

    <linearGradient id="cyanColumn" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0048FF" stop-opacity="0.15"/>
      <stop offset="45%" stop-color="#00F0FF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0070FF" stop-opacity="0.12"/>
    </linearGradient>

    <filter id="deepBlur" x="-80%" y="-20%" width="260%" height="140%">
      <feGaussianBlur stdDeviation="44"/>
    </filter>

    <filter id="plateShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgNavy)"/>

  <!-- blurred vertical data-light columns -->
  <rect x="170" y="-40" width="80" height="800" fill="url(#cyanColumn)" opacity="0.45" filter="url(#deepBlur)"/>
  <rect x="355" y="-40" width="54" height="800" fill="#00B8FF" opacity="0.34" filter="url(#deepBlur)"/>
  <rect x="575" y="-40" width="96" height="800" fill="#0078FF" opacity="0.27" filter="url(#deepBlur)"/>
  <rect x="830" y="-40" width="70" height="800" fill="#00FFFF" opacity="0.22" filter="url(#deepBlur)"/>
  <rect x="1045" y="-40" width="120" height="800" fill="#0055FF" opacity="0.18" filter="url(#deepBlur)"/>

  <!-- faint rigid grid scaffold -->
  <line x1="70" y1="80" x2="1180" y2="80" stroke="#4DEBFF" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="70" y1="200" x2="1180" y2="200" stroke="#4DEBFF" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="70" y1="320" x2="1180" y2="320" stroke="#4DEBFF" stroke-opacity="0.07" stroke-width="1"/>
  <line x1="70" y1="440" x2="1180" y2="440" stroke="#4DEBFF" stroke-opacity="0.06" stroke-width="1"/>
  <line x1="70" y1="560" x2="1180" y2="560" stroke="#4DEBFF" stroke-opacity="0.05" stroke-width="1"/>
  <line x1="160" y1="55" x2="160" y2="610" stroke="#4DEBFF" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="400" y1="55" x2="400" y2="610" stroke="#4DEBFF" stroke-opacity="0.07" stroke-width="1"/>
  <line x1="760" y1="55" x2="760" y2="610" stroke="#4DEBFF" stroke-opacity="0.05" stroke-width="1"/>

  <!-- subtle circuit-like flow traces -->
  <path d="M95 150 H210 V205 H315 H420 V260 H535" fill="none" stroke="#00F0FF" stroke-opacity="0.20" stroke-width="2"/>
  <path d="M150 405 H265 V350 H390 H520 V305 H650" fill="none" stroke="#7DF9FF" stroke-opacity="0.14" stroke-width="2"/>
  <path d="M500 128 H630 V178 H770 H900" fill="none" stroke="#007CFF" stroke-opacity="0.18" stroke-width="2" stroke-dasharray="14 12"/>
  <path d="M735 525 H850 V475 H990 H1120" fill="none" stroke="#00E5FF" stroke-opacity="0.10" stroke-width="2" stroke-dasharray="8 14"/>

  <!-- degrading square matrix: large white blocks left, fading cyan artifacts right -->
  <rect x="82" y="82" width="48" height="48" fill="#FFFFFF" opacity="0.94"/>
  <rect x="82" y="202" width="48" height="48" fill="#FFFFFF" opacity="0.88"/>
  <rect x="82" y="322" width="48" height="48" fill="#FFFFFF" opacity="0.82"/>
  <rect x="82" y="442" width="48" height="48" fill="#FFFFFF" opacity="0.70"/>
  <rect x="82" y="562" width="48" height="48" fill="#FFFFFF" opacity="0.50"/>

  <rect x="198" y="96" width="42" height="42" fill="#F4FCFF" opacity="0.82"/>
  <rect x="198" y="216" width="42" height="42" fill="#F4FCFF" opacity="0.76"/>
  <rect x="198" y="336" width="42" height="42" fill="#F4FCFF" opacity="0.68"/>
  <rect x="198" y="456" width="42" height="42" fill="#F4FCFF" opacity="0.52"/>

  <rect x="315" y="108" width="38" height="38" fill="#DFFBFF" opacity="0.72"/>
  <rect x="315" y="228" width="38" height="38" fill="none" stroke="#DFFBFF" stroke-width="3" opacity="0.66"/>
  <rect x="315" y="348" width="38" height="38" fill="#DFFBFF" opacity="0.52"/>
  <rect x="315" y="468" width="38" height="38" fill="#DFFBFF" opacity="0.38"/>

  <rect x="432" y="120" width="34" height="34" fill="#BFF7FF" opacity="0.58"/>
  <rect x="432" y="240" width="34" height="34" fill="#BFF7FF" opacity="0.50"/>
  <rect x="432" y="360" width="34" height="34" fill="none" stroke="#BFF7FF" stroke-width="3" opacity="0.43"/>
  <rect x="432" y="480" width="34" height="34" fill="#BFF7FF" opacity="0.30"/>

  <rect x="552" y="132" width="29" height="29" fill="#79EDFF" opacity="0.44"/>
  <rect x="552" y="252" width="29" height="29" fill="#79EDFF" opacity="0.38"/>
  <rect x="552" y="372" width="29" height="29" fill="#79EDFF" opacity="0.28"/>
  <rect x="552" y="492" width="29" height="29" fill="none" stroke="#79EDFF" stroke-width="2" opacity="0.25"/>

  <rect x="672" y="144" width="24" height="24" fill="#35DCFF" opacity="0.32"/>
  <rect x="672" y="264" width="24" height="24" fill="none" stroke="#35DCFF" stroke-width="2" opacity="0.28"/>
  <rect x="672" y="384" width="24" height="24" fill="#35DCFF" opacity="0.22"/>

  <rect x="792" y="156" width="20" height="20" fill="#00CFFF" opacity="0.24"/>
  <rect x="792" y="276" width="20" height="20" fill="#00CFFF" opacity="0.20"/>
  <rect x="792" y="516" width="20" height="20" fill="none" stroke="#00CFFF" stroke-width="2" opacity="0.16"/>

  <rect x="912" y="168" width="16" height="16" fill="#009CFF" opacity="0.18"/>
  <rect x="912" y="408" width="16" height="16" fill="#009CFF" opacity="0.14"/>
  <rect x="1032" y="288" width="13" height="13" fill="#38E8FF" opacity="0.12"/>
  <rect x="1138" y="528" width="10" height="10" fill="#38E8FF" opacity="0.10"/>

  <!-- title plate and typography -->
  <rect x="72" y="498" width="610" height="142" rx="24" fill="#020714" opacity="0.72" filter="url(#plateShadow)"/>
  <text x="104" y="555" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#FFFFFF" letter-spacing="-1">
    <tspan x="104" dy="0">Software Architecture</tspan>
    <tspan x="104" dy="48" fill="#C9F8FF">Matrix Flow</tspan>
  </text>
  <text x="106" y="623" width="540" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400" fill="#7EEBFF" opacity="0.88" letter-spacing="1.8">
    DIAGRAMMING TOOLS  ·  CLOUD SYSTEMS  ·  DATA MOVEMENT
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` fills for the matrix; repeated patterns will translate poorly and remove the left-to-right degradation logic.
- ❌ Do not blur `<line>` elements for the vertical streaks; filters on lines are dropped. Use blurred `<rect>` bands instead.
- ❌ Do not use `<mask>` for fading the grid; vary each square’s opacity, size, and color directly.
- ❌ Do not use `<use>` or `<symbol>` to duplicate squares; write explicit `<rect>` elements so every block remains editable in PowerPoint.
- ❌ Do not place the title over the thinnest right-side artifacts; the text must sit over the dark/dense left area for contrast.

## Composition notes
- Keep the heaviest grid density on the left third, then let squares shrink and fade toward the right to imply digital motion.
- Put title text in the lower-left quadrant, preferably on a semi-transparent dark plate so the white/cyan typography stays crisp.
- Use the vertical glow columns behind the matrix, not above it; the sharp squares should feel like data blocks floating in front of atmospheric light.
- Reserve the right half as negative space with only faint artifacts, making the slide suitable for premium keynote openings rather than busy dashboards.