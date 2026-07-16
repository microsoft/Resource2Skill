# SVG Recipe — Radial Segmented Infographic Wheel

## Visual mechanism
A thick doughnut wheel is split into equal colored arc segments around a central hub, creating a balanced “all parts are equal” infographic. Dark gaps between wedges, inner icons, and segment-aligned labels make the wheel feel like a premium keynote diagram rather than a flat chart.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background.
- 1× `<ellipse>` with blur/shadow filter for the soft wheel shadow.
- 7× main `<path>` annular sectors for the colored wheel segments.
- 7× secondary `<path>` annular sectors for the darker outer rim band on each segment.
- 1× `<circle>` for the central hub.
- 7× small icon groups made from `<path>`, `<circle>`, `<rect>`, and `<line>`-like path strokes for white pictograms inside the ring.
- 8× `<text>` blocks: 1 central title and 7 segment labels, each with explicit `width`.
- 7× `<linearGradient>` fills for subtle segment depth.
- 1× `<filter id="wheelShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for a soft keynote-style shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="wheelShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="seg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffb12a"/><stop offset="1" stop-color="#ff7b1f"/></linearGradient>
    <linearGradient id="seg2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b345f"/><stop offset="1" stop-color="#5e274f"/></linearGradient>
    <linearGradient id="seg3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b54176"/><stop offset="1" stop-color="#8d315f"/></linearGradient>
    <linearGradient id="seg4" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#db3e64"/><stop offset="1" stop-color="#b52e55"/></linearGradient>
    <linearGradient id="seg5" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f03d56"/><stop offset="1" stop-color="#c92747"/></linearGradient>
    <linearGradient id="seg6" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff594d"/><stop offset="1" stop-color="#e23e3a"/></linearGradient>
    <linearGradient id="seg7" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a45"/><stop offset="1" stop-color="#ee5d32"/></linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#202b36"/>
  <ellipse cx="640" cy="390" rx="280" ry="270" fill="#101821" opacity="0.45" filter="url(#wheelShadow)"/>

  <!-- Seven equal annular sectors: outer radius 285, inner radius 105, centered at 640,360 -->
  <path d="M516.6 103.2 A285 285 0 0 1 763.4 103.2 L685.5 265.4 A105 105 0 0 0 594.5 265.4 Z" fill="url(#seg1)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>
  <path d="M763.4 103.2 A285 285 0 0 1 917.9 296.4 L742.4 336.6 A105 105 0 0 0 685.5 265.4 Z" fill="url(#seg2)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>
  <path d="M917.9 296.4 A285 285 0 0 1 862.9 537.8 L722.1 425.5 A105 105 0 0 0 742.4 336.6 Z" fill="url(#seg3)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>
  <path d="M862.9 537.8 A285 285 0 0 1 640 645 L640 465 A105 105 0 0 0 722.1 425.5 Z" fill="url(#seg4)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>
  <path d="M640 645 A285 285 0 0 1 417.1 537.8 L557.9 425.5 A105 105 0 0 0 640 465 Z" fill="url(#seg5)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>
  <path d="M417.1 537.8 A285 285 0 0 1 362.1 296.4 L537.6 336.6 A105 105 0 0 0 557.9 425.5 Z" fill="url(#seg6)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>
  <path d="M362.1 296.4 A285 285 0 0 1 516.6 103.2 L594.5 265.4 A105 105 0 0 0 537.6 336.6 Z" fill="url(#seg7)" stroke="#202b36" stroke-width="12" stroke-linejoin="round"/>

  <!-- Subtle outer bands add dimensionality without masks -->
  <path d="M516.6 103.2 A285 285 0 0 1 763.4 103.2 L750.4 130.2 A255 255 0 0 0 529.6 130.2 Z" fill="#0f1720" opacity="0.20"/>
  <path d="M763.4 103.2 A285 285 0 0 1 917.9 296.4 L888.6 303.1 A255 255 0 0 0 750.4 130.2 Z" fill="#0f1720" opacity="0.20"/>
  <path d="M917.9 296.4 A285 285 0 0 1 862.9 537.8 L839.4 519.1 A255 255 0 0 0 888.6 303.1 Z" fill="#0f1720" opacity="0.20"/>
  <path d="M862.9 537.8 A285 285 0 0 1 640 645 L640 615 A255 255 0 0 0 839.4 519.1 Z" fill="#0f1720" opacity="0.20"/>
  <path d="M640 645 A285 285 0 0 1 417.1 537.8 L440.6 519.1 A255 255 0 0 0 640 615 Z" fill="#0f1720" opacity="0.20"/>
  <path d="M417.1 537.8 A285 285 0 0 1 362.1 296.4 L391.4 303.1 A255 255 0 0 0 440.6 519.1 Z" fill="#0f1720" opacity="0.20"/>
  <path d="M362.1 296.4 A285 285 0 0 1 516.6 103.2 L529.6 130.2 A255 255 0 0 0 391.4 303.1 Z" fill="#0f1720" opacity="0.20"/>

  <circle cx="640" cy="360" r="105" fill="#202b36" stroke="#2e3b47" stroke-width="2"/>
  <text x="520" y="356" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-weight="700">
    <tspan x="640" font-size="24" fill="#e64c73" letter-spacing="1">7 OPTION</tspan>
    <tspan x="640" dy="30" font-size="25" fill="#ffffff" letter-spacing="1">INFOGRAPHIC</tspan>
  </text>

  <!-- Inner white pictograms, drawn as editable vector strokes -->
  <g stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.95">
    <path d="M630 225 C630 216 650 216 650 225 C650 231 646 234 646 239 L634 239 C634 234 630 231 630 225 Z"/><path d="M635 244 L645 244 M636 249 L644 249"/>
    <path d="M738 272 L746 264 L754 272 L746 280 Z"/><circle cx="746" cy="272" r="13"/><path d="M746 252 L746 260 M746 284 L746 292 M726 272 L734 272 M758 272 L766 272"/>
    <path d="M754 401 L754 379 M764 401 L764 369 M774 401 L774 388 M748 401 L780 401"/>
    <path d="M684 476 C694 460 712 460 722 476"/><path d="M690 476 L700 466 M704 476 L716 466"/>
    <rect x="572" y="471" width="22" height="22" rx="3" fill="none"/><path d="M577 471 L577 464 C577 455 589 455 589 464 L589 471"/><circle cx="583" cy="482" r="2"/>
    <path d="M492 388 L506 388 L506 400 L492 400 Z M510 379 L524 379 L524 391 L510 391 Z M518 395 L518 405"/><path d="M499 388 L510 385 M506 394 L518 395"/>
    <circle cx="532" cy="274" r="11"/><path d="M532 255 L532 262 M532 286 L532 293 M513 274 L520 274 M544 274 L551 274 M519 261 L524 266 M545 261 L540 266 M519 287 L524 282 M545 287 L540 282"/>
  </g>

  <!-- Segment labels orbit inside each wedge -->
  <text x="570" y="148" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="640" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="640" dy="13" font-size="8">Strategy pillar and focus area</tspan><tspan x="640" dy="10" font-size="8">for the next operating cycle.</tspan>
  </text>
  <text x="760" y="225" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="835" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="835" dy="13" font-size="8">Customer value expressed as</tspan><tspan x="835" dy="10" font-size="8">a measurable capability.</tspan>
  </text>
  <text x="776" y="394" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="851" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="851" dy="13" font-size="8">Operational lever that supports</tspan><tspan x="851" dy="10" font-size="8">scale and repeatability.</tspan>
  </text>
  <text x="648" y="531" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="723" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="723" dy="13" font-size="8">Governance principle linked to</tspan><tspan x="723" dy="10" font-size="8">performance outcomes.</tspan>
  </text>
  <text x="482" y="531" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="557" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="557" dy="13" font-size="8">Security, trust, and resilience</tspan><tspan x="557" dy="10" font-size="8">built into the system.</tspan>
  </text>
  <text x="355" y="394" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="430" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="430" dy="13" font-size="8">Delivery model designed for</tspan><tspan x="430" dy="10" font-size="8">clarity and speed.</tspan>
  </text>
  <text x="375" y="225" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#ffffff">
    <tspan x="450" font-size="15" font-weight="700">Lorem Ipsum</tspan><tspan x="450" dy="13" font-size="8">Market signal translated into</tspan><tspan x="450" dy="10" font-size="8">portfolio priorities.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut the center hole; build each wedge as an annular `<path>` instead.
- ❌ Do not use `<textPath>` for curved labels around the ring; PowerPoint editability and readability suffer.
- ❌ Do not use `<use>` to repeat icons or segments; duplicate the editable paths directly.
- ❌ Do not put `filter` on `<line>` elements; use path strokes or apply shadows to circles/ellipses/paths.
- ❌ Do not rely on a native chart object if the goal is fully editable custom geometry; arc paths give precise visual control.

## Composition notes
- Keep the wheel centered and let it occupy roughly 75–85% of slide height; this makes it the main visual anchor.
- Use a dark background so white wedge gaps, labels, and icons read crisply.
- Put the core concept in the center hub with two-line hierarchy: colored small descriptor above bold white main title.
- Keep all segment labels horizontally oriented; place them in the outer half of each wedge for readability while icons sit closer to the hub.