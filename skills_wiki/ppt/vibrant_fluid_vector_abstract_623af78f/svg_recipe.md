# SVG Recipe — Vibrant Fluid Vector Abstract

## Visual mechanism
A saturated royal-purple field is cut by oversized, off-canvas Bezier waves in yellow, magenta, orange, and deep purple, creating the feeling of fluid vector motion. Large white typography sits in the calm upper-left negative space while the bright curves sweep diagonally upward from the lower edge.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark purple base.
- 6× large filled `<path>` elements for overlapping fluid waves and foreground color bands.
- 3× smaller `<path>` elements for glossy curved highlights and motion accents.
- 5× `<circle>` elements for small energetic dots/spark accents.
- 4× `<text>` elements with explicit `width` attributes for title, subtitle, label, and contact/footer copy.
- 3× `<linearGradient>` definitions for richer magenta/orange/yellow vector fills.
- 1× `<radialGradient>` definition for a soft purple glow.
- 2× `<filter>` definitions: one soft glow for accent paths/circles, one shadow for lifted text and foreground shapes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="yellowSweep" x1="70" y1="520" x2="520" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFE66D"/>
      <stop offset="0.55" stop-color="#F4D03F"/>
      <stop offset="1" stop-color="#F9A825"/>
    </linearGradient>

    <linearGradient id="magentaSweep" x1="760" y1="350" x2="1170" y2="710" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF4FA3"/>
      <stop offset="0.55" stop-color="#E91E63"/>
      <stop offset="1" stop-color="#9C1B7A"/>
    </linearGradient>

    <linearGradient id="orangeSweep" x1="860" y1="390" x2="1310" y2="700" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFB02E"/>
      <stop offset="0.45" stop-color="#FF5722"/>
      <stop offset="1" stop-color="#E53935"/>
    </linearGradient>

    <radialGradient id="purpleGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0" stop-color="#7B1FD1"/>
      <stop offset="0.45" stop-color="#4A148C"/>
      <stop offset="1" stop-color="#310A64"/>
    </radialGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="liftShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#purpleGlow)"/>

  <path d="M-80,720 C35,560 145,492 286,520 C430,548 510,632 650,720 Z"
        fill="url(#yellowSweep)"/>

  <path d="M640,720 C724,594 808,492 948,452 C1096,410 1224,460 1375,610 L1375,720 Z"
        fill="#310A64"/>

  <path d="M738,720 C810,594 908,502 1028,488 C1148,474 1242,538 1360,652 L1360,720 Z"
        fill="url(#magentaSweep)" filter="url(#liftShadow)"/>

  <path d="M842,720 C895,610 982,518 1103,492 C1204,471 1295,510 1395,590 L1395,720 Z"
        fill="url(#orangeSweep)"/>

  <path d="M990,720 C1030,646 1084,592 1160,585 C1227,579 1284,616 1348,676 L1348,720 Z"
        fill="#4A148C"/>

  <path d="M-40,605 C105,515 245,496 390,548 C477,579 548,633 612,720 L-40,720 Z"
        fill="#F4D03F" opacity="0.92"/>

  <path d="M850,372 C936,328 1023,322 1118,364 C1175,389 1222,428 1268,486"
        fill="none" stroke="#FF7AC0" stroke-width="18" stroke-linecap="round" opacity="0.5" filter="url(#softGlow)"/>

  <path d="M930,438 C1010,396 1100,394 1192,438 C1238,460 1277,492 1310,530"
        fill="none" stroke="#FFC23C" stroke-width="10" stroke-linecap="round" opacity="0.75"/>

  <path d="M114,510 C176,476 254,472 330,502"
        fill="none" stroke="#FFF4A8" stroke-width="9" stroke-linecap="round" opacity="0.6"/>

  <circle cx="1090" cy="188" r="8" fill="#FF5722" filter="url(#softGlow)"/>
  <circle cx="1143" cy="238" r="5" fill="#F4D03F"/>
  <circle cx="1015" cy="260" r="4" fill="#E91E63"/>
  <circle cx="1224" cy="318" r="7" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="706" cy="122" r="5" fill="#F4D03F" opacity="0.8"/>

  <text x="82" y="88" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4"
        fill="#F4D03F">CREATIVE AGENCY DECK</text>

  <text x="78" y="178" width="770"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="900" letter-spacing="-2"
        fill="#FFFFFF" filter="url(#liftShadow)">
    <tspan x="78" dy="0">CREATE</tspan>
    <tspan x="78" dy="88">THE FUTURE</tspan>
  </text>

  <text x="84" y="392" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="400" line-height="1.3"
        fill="#D7C8F5">
    <tspan x="84" dy="0">A vibrant abstract keynote system</tspan>
    <tspan x="84" dy="34">for launches, events, and bold ideas.</tspan>
  </text>

  <text x="88" y="596" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700"
        fill="#310A64">
    <tspan x="88" dy="0">hello@fluid.studio</tspan>
    <tspan x="88" dy="31" font-weight="500">www.fluid-studio.co</tspan>
    <tspan x="88" dy="31" font-weight="500">+1 555 0198 442</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rasterize the entire background as one flat image; use editable `<path>` waves so the colors and curves remain adjustable in PowerPoint.
- ❌ Do not rely only on simple stacked rectangles or circles; the premium look comes from large off-canvas Bezier curves.
- ❌ Do not place dense body copy over the orange/magenta curves; those regions are visually loud and reduce readability.
- ❌ Do not use `<mask>`, `<pattern>`, `<textPath>`, or skew/matrix transforms for the fluid shapes; keep the design in native paths, gradients, and standard transforms.
- ❌ Do not add filters to `<line>` elements; if accents need glow, make them stroked `<path>` elements instead.

## Composition notes
- Keep the upper-left 55–65% of the slide mostly dark purple for clean title readability.
- Anchor the strongest yellow shape in the lower-left and the magenta/orange waves in the lower-right to create a diagonal visual sweep.
- Use white for the main title, muted lavender for subtitle text, and dark purple text when copy sits on the yellow region.
- Let the waves extend beyond the slide edges; off-canvas geometry makes the background feel expansive rather than boxed in.