# SVG Recipe — Layered Crescent Infographic

## Visual mechanism
A vertical process list is transformed into a tactile paper-cut composition: three thick crescent bands overlap slightly, each casting a soft shadow onto the layer beneath it. Large step letters, simple icons, and right-side text blocks reinforce the sequential A–B–C reading path.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 1× `<path>` for the subtle angled background plane behind the crescent stack
- 1× `<filter id="planeShadow">` applied to the background plane for a soft floor shadow
- 1× `<filter id="layerShadow">` applied to each crescent for the stacked paper-cut shadow
- 3× `<linearGradient>` fills for the pink, blue, and green crescent surfaces
- 3× compound-like `<path>` crescent silhouettes, each shaped as a thick semi-circular block arc
- 3× smaller translucent `<path>` highlights on the upper-left edge of each crescent
- 3× icon groups built from editable `<path>`, `<circle>`, and `<line>` primitives
- 3× large `<text>` labels for A, B, and C
- 3× header/body `<text>` blocks with nested `<tspan>` for hierarchy and inline color
- Several decorative `<circle>` accents for premium polish and color rhythm

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="planeGrad" x1="180" y1="120" x2="760" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#E9ECEF"/>
    </linearGradient>

    <linearGradient id="pinkGrad" x1="250" y1="60" x2="470" y2="290" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#EBC0BE"/>
      <stop offset="1" stop-color="#DA9694"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="250" y1="220" x2="470" y2="450" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7FA6C4"/>
      <stop offset="1" stop-color="#5985A9"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="250" y1="390" x2="470" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B5C6A9"/>
      <stop offset="1" stop-color="#92AC86"/>
    </linearGradient>

    <filter id="planeShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="22" dy="24" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="layerShadow" x="-20%" y="-20%" width="160%" height="160%">
      <feOffset dx="12" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F5F1"/>

  <circle cx="1055" cy="106" r="5" fill="#DA9694" opacity="0.55"/>
  <circle cx="1090" cy="132" r="3" fill="#5985A9" opacity="0.45"/>
  <circle cx="1028" cy="158" r="4" fill="#92AC86" opacity="0.45"/>

  <path d="M178 124 L610 84 L758 640 L244 656 Z" fill="url(#planeGrad)" opacity="0.82" filter="url(#planeShadow)"/>
  <path d="M204 168 L568 132 L690 602 L266 620 Z" fill="none" stroke="#D6D9DD" stroke-width="2" stroke-dasharray="7 10" opacity="0.55"/>

  <!-- Bottom layer first -->
  <path d="M286 398
           C404 398 470 482 470 494
           C470 506 404 590 286 590
           L286 534
           C350 534 386 510 386 494
           C386 478 350 454 286 454 Z"
        fill="url(#greenGrad)" filter="url(#layerShadow)"/>
  <path d="M306 416 C380 420 430 468 438 494" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.22"/>

  <!-- Middle layer -->
  <path d="M286 234
           C404 234 470 318 470 330
           C470 342 404 426 286 426
           L286 370
           C350 370 386 346 386 330
           C386 314 350 290 286 290 Z"
        fill="url(#blueGrad)" filter="url(#layerShadow)"/>
  <path d="M306 252 C380 256 430 304 438 330" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.22"/>

  <!-- Top layer -->
  <path d="M286 70
           C404 70 470 154 470 166
           C470 178 404 262 286 262
           L286 206
           C350 206 386 182 386 166
           C386 150 350 126 286 126 Z"
        fill="url(#pinkGrad)" filter="url(#layerShadow)"/>
  <path d="M306 88 C380 92 430 140 438 166" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.25"/>

  <!-- Step letters -->
  <text x="135" y="178" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="700" fill="#595959">A</text>
  <text x="135" y="342" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="700" fill="#595959">B</text>
  <text x="137" y="506" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="700" fill="#595959">C</text>

  <!-- Icons in crescent hollows -->
  <circle cx="333" cy="166" r="28" fill="#FFFFFF" opacity="0.88"/>
  <path d="M320 170 L330 180 L349 151" fill="none" stroke="#DA9694" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="333" cy="330" r="28" fill="#FFFFFF" opacity="0.88"/>
  <path d="M318 342 L318 321 L333 310 L348 321 L348 342 Z" fill="none" stroke="#5985A9" stroke-width="5" stroke-linejoin="round"/>
  <line x1="333" y1="310" x2="333" y2="342" stroke="#5985A9" stroke-width="5" stroke-linecap="round"/>
  <circle cx="333" cy="494" r="28" fill="#FFFFFF" opacity="0.88"/>
  <path d="M333 516 C333 492 350 484 357 464 C339 467 322 478 318 497 C315 508 321 515 333 516 Z" fill="none" stroke="#92AC86" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Title -->
  <text x="535" y="86" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#3F3F3F">
    Layered Crescent Infographic
  </text>
  <text x="536" y="121" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#8A8A8A" letter-spacing="1.6">
    THREE STEP EXECUTIVE PROCESS
  </text>

  <!-- Text block A -->
  <text x="535" y="180" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#595959">
    <tspan x="535" dy="0" font-size="15" font-weight="700" fill="#DA9694" letter-spacing="1.3">OPTION 01</tspan>
    <tspan x="535" dy="30" font-size="25" font-weight="700" fill="#3E3E3E">Discover the opportunity</tspan>
    <tspan x="535" dy="31" font-size="16" fill="#6C6C6C">Frame the business question, isolate the key audience need,</tspan>
    <tspan x="535" dy="23" font-size="16" fill="#6C6C6C">and define the measurable outcome before execution begins.</tspan>
  </text>

  <!-- Text block B -->
  <text x="535" y="344" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#595959">
    <tspan x="535" dy="0" font-size="15" font-weight="700" fill="#5985A9" letter-spacing="1.3">OPTION 02</tspan>
    <tspan x="535" dy="30" font-size="25" font-weight="700" fill="#3E3E3E">Build the operating model</tspan>
    <tspan x="535" dy="31" font-size="16" fill="#6C6C6C">Translate the strategy into workflows, ownership, and milestone</tspan>
    <tspan x="535" dy="23" font-size="16" fill="#6C6C6C">checkpoints that keep the initiative moving with confidence.</tspan>
  </text>

  <!-- Text block C -->
  <text x="535" y="508" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#595959">
    <tspan x="535" dy="0" font-size="15" font-weight="700" fill="#92AC86" letter-spacing="1.3">OPTION 03</tspan>
    <tspan x="535" dy="30" font-size="25" font-weight="700" fill="#3E3E3E">Scale the impact</tspan>
    <tspan x="535" dy="31" font-size="16" fill="#6C6C6C">Measure adoption, codify what works, and expand the playbook</tspan>
    <tspan x="535" dy="23" font-size="16" fill="#6C6C6C">into a repeatable system for future teams and regions.</tspan>
  </text>

  <circle cx="1135" cy="606" r="42" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="1135" cy="606" r="25" fill="#E6E0D8" opacity="0.55"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut the crescent holes; build the crescent as a single editable path silhouette instead.
- ❌ Do not use `<use>` or `<symbol>` for repeated crescents or icons; duplicate the editable paths directly.
- ❌ Do not apply filters to `<line>` icon strokes; line filters are dropped, so keep shadows on the main crescent `<path>` elements only.
- ❌ Do not rely on `marker-end` arrows for process flow; the stacked crescents already imply direction, and SVG path arrowheads may disappear.
- ❌ Do not use `clip-path` on the crescent shapes; clipping is only reliable for images in this workflow.

## Composition notes
- Keep the crescent stack in the left 35–40% of the canvas, with the text column beginning around x=520–550.
- Draw the lowest crescent first, then the middle, then the top so each upper layer’s shadow visually falls onto the layer beneath it.
- Use muted accent colors and matching header text to tie each crescent to its corresponding content block.
- Preserve generous right-side negative space; the crescents are visually heavy, so body text should remain clean, short, and aligned.