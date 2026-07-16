# SVG Recipe — Vertical Accordion Morph Panels

## Visual mechanism
A stack of full-height white panels is layered left-to-right, with each panel hiding half of the colored circle behind it so only a protruding semicircular tab remains visible. Soft left-cast shadows between panels create the illusion of physical accordion leaves, while the active front panel becomes a clean content canvas.

## SVG primitives needed
- 1× `<rect>` for the pale presentation background
- 5× colored `<circle>` elements for the protruding accordion tabs
- 5× full-height white `<rect>` elements for the stacked accordion panels
- 5× blurred gray `<rect>` elements behind panels for left-cast depth shadows
- 5× rotated `<text>` elements for vertical tab labels
- 3× rounded card groups using `<rect>`, `<path>`, `<circle>`, and `<text>` for active-panel process content
- 3× decorative `<path>` line icons for lightbulb-style step illustrations
- 2× `<filter>` definitions: one broad horizontal blur for panel separation, one vertical blur for floating card shadows
- Optional small `<circle>` / `<path>` accents for executive-keynote polish

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="leftPanelShadow" x="-60%" y="-10%" width="180%" height="120%">
      <feOffset in="SourceGraphic" dx="-18" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="13"/>
    </filter>
    <filter id="cardShadow" x="-30%" y="-20%" width="160%" height="160%">
      <feOffset in="SourceGraphic" dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12"/>
    </filter>
    <linearGradient id="panelWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f7f8fa"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f1f1f4"/>

  <!-- Accordion layer 1 -->
  <circle cx="88" cy="224" r="64" fill="#12a7ad"/>
  <rect x="88" y="-8" width="1220" height="736" fill="#92949b" opacity="0.32" filter="url(#leftPanelShadow)"/>
  <rect x="88" y="0" width="1195" height="720" fill="url(#panelWash)"/>
  <text x="49" y="224" width="130" transform="rotate(-90 49 224)" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="800" fill="#ffffff">follow</text>

  <!-- Accordion layer 2 -->
  <circle cx="144" cy="288" r="64" fill="#8bcf4a"/>
  <rect x="144" y="-8" width="1165" height="736" fill="#92949b" opacity="0.32" filter="url(#leftPanelShadow)"/>
  <rect x="144" y="0" width="1140" height="720" fill="url(#panelWash)"/>
  <text x="105" y="288" width="130" transform="rotate(-90 105 288)" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="800" fill="#ffffff">services</text>

  <!-- Accordion layer 3 -->
  <circle cx="200" cy="352" r="64" fill="#566b6f"/>
  <rect x="200" y="-8" width="1110" height="736" fill="#92949b" opacity="0.32" filter="url(#leftPanelShadow)"/>
  <rect x="200" y="0" width="1085" height="720" fill="url(#panelWash)"/>
  <text x="161" y="352" width="130" transform="rotate(-90 161 352)" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="800" fill="#ffffff">teams</text>

  <!-- Accordion layer 4 -->
  <circle cx="256" cy="416" r="64" fill="#ffc62e"/>
  <rect x="256" y="-8" width="1055" height="736" fill="#92949b" opacity="0.32" filter="url(#leftPanelShadow)"/>
  <rect x="256" y="0" width="1030" height="720" fill="url(#panelWash)"/>
  <text x="217" y="416" width="130" transform="rotate(-90 217 416)" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="800" fill="#ffffff">timeline</text>

  <!-- Active accordion layer -->
  <circle cx="312" cy="480" r="64" fill="#ef4e63"/>
  <rect x="312" y="-8" width="1000" height="736" fill="#92949b" opacity="0.34" filter="url(#leftPanelShadow)"/>
  <rect x="312" y="0" width="970" height="720" fill="#ffffff"/>
  <text x="273" y="480" width="130" transform="rotate(-90 273 480)" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="800" fill="#ffffff">about</text>

  <!-- Active panel header -->
  <text x="380" y="92" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#263238">
    Product launch path
  </text>
  <text x="382" y="126" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#8d98a0">
    Accordion panels behave like navigation, while the open leaf becomes a focused storytelling stage.
  </text>

  <!-- Floating process card 1 -->
  <rect x="392" y="188" width="180" height="332" rx="30" fill="#9a9a9a" opacity="0.32" filter="url(#cardShadow)"/>
  <rect x="392" y="174" width="180" height="348" rx="30" fill="#f8f8f8"/>
  <path d="M392 204 Q392 174 422 174 L542 174 Q572 174 572 204 L572 270 L392 270 Z" fill="#ef4e63"/>
  <circle cx="482" cy="270" r="50" fill="#ef4e63"/>
  <text x="482" y="222" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#ffffff">2010</text>
  <text x="482" y="288" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="800" fill="#ffffff">1</text>
  <text x="482" y="360" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#ef4e63">DISCOVER</text>
  <text x="482" y="389" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9a9a9a">Map customer</text>
  <text x="482" y="411" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9a9a9a">needs and gaps</text>
  <path d="M470 468 C452 446 468 426 482 426 C498 426 512 446 494 468 M470 468 L494 468 M474 478 L490 478 M476 487 L488 487 M482 416 L482 402 M456 424 L446 414 M508 424 L518 414 M445 450 L431 450 M519 450 L533 450"
        fill="none" stroke="#ef4e63" stroke-width="3" stroke-linecap="round"/>

  <!-- Floating process card 2 -->
  <rect x="656" y="188" width="180" height="332" rx="30" fill="#9a9a9a" opacity="0.32" filter="url(#cardShadow)"/>
  <rect x="656" y="174" width="180" height="348" rx="30" fill="#f8f8f8"/>
  <path d="M656 204 Q656 174 686 174 L806 174 Q836 174 836 204 L836 270 L656 270 Z" fill="#51c7bd"/>
  <circle cx="746" cy="270" r="50" fill="#51c7bd"/>
  <text x="746" y="222" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#ffffff">2014</text>
  <text x="746" y="288" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="800" fill="#ffffff">2</text>
  <text x="746" y="360" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#51c7bd">PROTOTYPE</text>
  <text x="746" y="389" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9a9a9a">Build the first</text>
  <text x="746" y="411" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9a9a9a">market story</text>
  <path d="M734 468 C716 446 732 426 746 426 C762 426 776 446 758 468 M734 468 L758 468 M738 478 L754 478 M740 487 L752 487 M746 416 L746 402 M720 424 L710 414 M772 424 L782 414 M709 450 L695 450 M783 450 L797 450"
        fill="none" stroke="#51c7bd" stroke-width="3" stroke-linecap="round"/>

  <!-- Floating process card 3 -->
  <rect x="920" y="188" width="180" height="332" rx="30" fill="#9a9a9a" opacity="0.32" filter="url(#cardShadow)"/>
  <rect x="920" y="174" width="180" height="348" rx="30" fill="#f8f8f8"/>
  <path d="M920 204 Q920 174 950 174 L1070 174 Q1100 174 1100 204 L1100 270 L920 270 Z" fill="#ffc62e"/>
  <circle cx="1010" cy="270" r="50" fill="#ffc62e"/>
  <text x="1010" y="222" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#ffffff">2018</text>
  <text x="1010" y="288" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="800" fill="#ffffff">3</text>
  <text x="1010" y="360" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#ffc62e">SCALE</text>
  <text x="1010" y="389" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9a9a9a">Expand across</text>
  <text x="1010" y="411" width="142" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9a9a9a">channels</text>
  <path d="M998 468 C980 446 996 426 1010 426 C1026 426 1040 446 1022 468 M998 468 L1022 468 M1002 478 L1018 478 M1004 487 L1016 487 M1010 416 L1010 402 M984 424 L974 414 M1036 424 L1046 414 M973 450 L959 450 M1047 450 L1061 450"
        fill="none" stroke="#ffc62e" stroke-width="3" stroke-linecap="round"/>

  <!-- Right-side hint tab to imply morphable continuation -->
  <circle cx="1216" cy="360" r="112" fill="#51c7bd"/>
  <text x="1195" y="360" width="190" transform="rotate(-90 1195 360)" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">history</text>
  <path d="M1152 355 C1162 339 1183 341 1190 358 C1197 375 1180 390 1165 382 M1165 382 L1165 394 M1160 394 L1174 394 M1162 403 L1172 403 M1140 364 L1128 364 M1145 344 L1136 335 M1170 332 L1170 318 M1194 344 L1203 335"
        fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.95"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG masks or boolean cutouts to create the semicircle tabs; layer full circles behind white panels instead.
- ❌ Do not apply `clip-path` to panel rectangles or tab circles; PPT translation only preserves clipping reliably for images.
- ❌ Do not use `<use>` / `<symbol>` for repeated cards or icons; duplicate editable shapes directly.
- ❌ Do not rely on `marker-end` arrowheads for process navigation; if arrows are needed, build them from `<line>` plus small `<path>` triangles.
- ❌ Do not omit `width` on rotated tab text; narrow PowerPoint text boxes can reflow unexpectedly after translation.

## Composition notes
- Keep the collapsed accordion stack in the left 20–25% of the slide; the active panel should own the remaining canvas.
- Use 5–6 saturated tab colors, but keep all panel faces white or near-white so the layout feels like a premium app interface.
- Shadows should cast leftward, not downward, to communicate overlapping vertical leaves.
- Place detailed content only on the foremost panel; earlier panels should read as navigation, not competing content areas.