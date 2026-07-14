# SVG Recipe — Organic Dual-Tone Wave Layout

## Visual mechanism
A full-bleed emotional photo is partially covered by two oversized, overlapping Bezier wave shapes: a mustard-gold accent wave peeks out behind a dominant slate wave that holds the title and body copy. The curved boundary replaces rigid split-screen geometry and creates a premium corporate divider/title-slide feel.

## SVG primitives needed
- 1× `<image>` for the full-bleed photographic background
- 1× `<rect>` for darkening the photo and improving contrast
- 1× `<path>` for the rear mustard-gold organic wave
- 1× `<path>` for the foreground slate organic wave
- 2× `<path>` for subtle decorative curved highlight strokes
- 1× `<linearGradient id="slateGrad">` for depth on the main slate wave
- 1× `<linearGradient id="goldGrad">` for depth on the gold accent wave
- 1× `<filter id="softShadow">` applied to the slate wave for light dimensional separation
- 3× `<circle>` for small executive-style icon/accent nodes
- 3× `<path>` for simple editable line icons inside the accent nodes
- 3× `<line>` for horizontal accent rules and metadata separators
- 6× `<text>` elements with explicit `width` attributes for editable PowerPoint typography

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="slateGrad" x1="440" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#343545"/>
      <stop offset="58%" stop-color="#414150"/>
      <stop offset="100%" stop-color="#292A36"/>
    </linearGradient>

    <linearGradient id="goldGrad" x1="290" y1="0" x2="690" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#E0BD67"/>
      <stop offset="45%" stop-color="#C8A050"/>
      <stop offset="100%" stop-color="#A97D32"/>
    </linearGradient>

    <filter id="softShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="-8" dy="0" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed emotional corporate background -->
  <image
    href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1600&amp;q=80"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Photo contrast overlay -->
  <rect x="0" y="0" width="1280" height="720" fill="#05070B" opacity="0.34"/>

  <!-- Rear accent wave: visible as a gold ribbon between photo and slate -->
  <path
    d="M 418 -80
       C 318 42 306 154 378 286
       C 455 428 421 556 288 780
       L 1360 780
       L 1360 -80
       Z"
    fill="url(#goldGrad)"/>

  <!-- Foreground organic slate wave: large editable Bezier shape -->
  <path
    d="M 505 -90
       C 384 50 400 171 487 306
       C 574 441 527 566 395 780
       L 1360 780
       L 1360 -90
       Z"
    fill="url(#slateGrad)"
    filter="url(#softShadow)"/>

  <!-- Thin internal curve highlights for premium keynote polish -->
  <path
    d="M 608 80
       C 536 184 555 278 627 382
       C 683 463 658 562 578 682"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="2"
    stroke-opacity="0.13"/>

  <path
    d="M 470 12
       C 382 118 378 215 446 338
       C 513 459 483 566 362 720"
    fill="none"
    stroke="#D7AD59"
    stroke-width="6"
    stroke-opacity="0.75"/>

  <!-- Small section label -->
  <line x1="725" y1="128" x2="803" y2="128" stroke="#C8A050" stroke-width="4"/>
  <text x="818" y="136" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="3"
        fill="#D9C38F">CORPORATE OVERVIEW</text>

  <!-- Main title -->
  <text x="720" y="236" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="700"
        fill="#FFFFFF">
    <tspan x="720" dy="0">Company</tspan>
    <tspan x="720" dy="68">Profile</tspan>
  </text>

  <!-- Body copy -->
  <text x="724" y="356" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" line-height="1.45"
        fill="#E8E9EF" opacity="0.92">
    <tspan x="724" dy="0">A modern operating model built for</tspan>
    <tspan x="724" dy="31">growth, resilience, and measurable</tspan>
    <tspan x="724" dy="31">enterprise impact.</tspan>
  </text>

  <!-- Metadata rule -->
  <line x1="724" y1="470" x2="1045" y2="470" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.2"/>
  <line x1="724" y1="492" x2="880" y2="492" stroke="#C8A050" stroke-width="3"/>

  <!-- Three editable icon nodes -->
  <circle cx="746" cy="568" r="28" fill="#C8A050"/>
  <path d="M 733 568 C 733 559 739 552 746 552 C 753 552 759 559 759 568 C 759 577 753 584 746 584 C 739 584 733 577 733 568 Z"
        fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M 746 552 C 740 559 740 577 746 584 C 752 577 752 559 746 552 Z"
        fill="none" stroke="#FFFFFF" stroke-width="2"/>

  <circle cx="872" cy="568" r="28" fill="#FFFFFF" opacity="0.12"/>
  <path d="M 858 575 L 869 554 L 886 584 L 873 578 L 864 584 Z"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>

  <circle cx="998" cy="568" r="28" fill="#FFFFFF" opacity="0.12"/>
  <path d="M 984 570 L 994 580 L 1014 555"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Icon captions -->
  <text x="724" y="628" width="86"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600"
        fill="#FFFFFF">Global</text>
  <text x="846" y="628" width="100"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600"
        fill="#FFFFFF">Agile</text>
  <text x="970" y="628" width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600"
        fill="#FFFFFF">Trusted</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut the photo into a wave; instead, place editable wave `<path>` shapes above the image.
- ❌ Do not make the waves with many straight polygon points; the premium effect depends on large, smooth cubic Bezier curves.
- ❌ Do not apply `clip-path` to the slate or gold shapes; clipping non-image elements is ignored by the translator.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake the swoosh; draw the wave directly as a path.
- ❌ Do not rely on drop shadows on `<line>` elements; if depth is needed, apply filters only to `<path>`, `<rect>`, `<circle>`, `<ellipse>`, or `<text>`.

## Composition notes
- Keep the photo full-bleed and let the wave shapes define the split; the image should occupy roughly the left 45–55% visually.
- The gold wave should sit behind the slate wave and protrude as a narrow curved ribbon, not a large competing panel.
- Place the main title and body copy inside the darkest, calmest part of the slate field, usually right-center.
- Use gold sparingly for rules, labels, and icon accents so the dual-tone rhythm feels disciplined and executive.