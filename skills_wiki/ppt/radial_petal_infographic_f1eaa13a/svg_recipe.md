# SVG Recipe — Radial Petal Infographic

## Visual mechanism
Eight curved, overlapping “petals” radiate from a central hub, forming a flower-like system diagram where each concept has equal visual weight. A secondary curved overlay on each petal creates an interwoven transparency effect, while numbered outer caps make the eight ideas easy to reference.

## SVG primitives needed
- 1× `<rect>` for the full-slide radial gradient background
- 2× `<ellipse>` for soft ambient background highlights
- 16× `<path>` for the eight primary petals plus eight lighter overlap facets
- 8× `<circle>` for numbered outer caps
- 2× `<circle>` for the central hub and inner ring
- 17× `<text>` for eight cap numbers, eight petal labels, and the central theme label
- 1× `<radialGradient>` for the executive-style neutral background
- 1× `<filter id="softShadow">` applied to petals, caps, and hub elements
- 1× `<filter id="mist">` applied to background highlight ellipses

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bg" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F3F5F8"/>
      <stop offset="100%" stop-color="#D9DEE7"/>
    </radialGradient>

    <filter id="softShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset in="SourceAlpha" dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="mist" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <ellipse cx="330" cy="155" rx="210" ry="80" fill="#FFFFFF" opacity="0.55" filter="url(#mist)"/>
  <ellipse cx="1005" cy="565" rx="260" ry="90" fill="#C9D8FF" opacity="0.28" filter="url(#mist)"/>

  <!-- Primary petal layer -->
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#00B0F0" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#00B050" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(45 640 360)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#7030A0" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(90 640 360)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#E6007E" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(135 640 360)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#FF8000" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(180 640 360)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#7F7F7F" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(225 640 360)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#404040" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(270 640 360)"/>
  <path d="M603 326 C581 285 586 214 620 122 C628 100 652 100 660 122 C694 214 699 285 677 326 C661 356 619 356 603 326 Z" fill="#26A69A" stroke="#FFFFFF" stroke-width="2" filter="url(#softShadow)" transform="rotate(315 640 360)"/>

  <!-- Lighter overlap facets, placed above primaries to simulate woven petals -->
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#33C6F4" stroke="#FFFFFF" stroke-width="1.5"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#33C978" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(45 640 360)"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#8C5AB5" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(90 640 360)"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#EC4DA0" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(135 640 360)"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#FF9A33" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(180 640 360)"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#9A9A9A" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(225 640 360)"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#666666" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(270 640 360)"/>
  <path d="M642 344 C672 311 682 244 658 128 C691 178 714 254 700 314 C692 348 666 363 642 344 Z" fill="#55BDB2" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(315 640 360)"/>

  <!-- Outer numbered caps -->
  <circle cx="640" cy="96" r="31" fill="#00B0F0" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="827" cy="173" r="31" fill="#00B050" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="904" cy="360" r="31" fill="#7030A0" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="827" cy="547" r="31" fill="#E6007E" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="640" cy="624" r="31" fill="#FF8000" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="453" cy="547" r="31" fill="#7F7F7F" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="376" cy="360" r="31" fill="#404040" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="453" cy="173" r="31" fill="#26A69A" stroke="#FFFFFF" stroke-width="4" filter="url(#softShadow)"/>

  <!-- Central hub -->
  <circle cx="640" cy="360" r="96" fill="#FFFFFF" stroke="#E5EAF2" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="640" cy="360" r="72" fill="none" stroke="#D7DEE9" stroke-width="2"/>

  <!-- Cap numbers -->
  <text x="640" y="107" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">1</text>
  <text x="827" y="184" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">2</text>
  <text x="904" y="371" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">3</text>
  <text x="827" y="558" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">4</text>
  <text x="640" y="635" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">5</text>
  <text x="453" y="558" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">6</text>
  <text x="376" y="371" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">7</text>
  <text x="453" y="184" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">8</text>

  <!-- Petal labels kept horizontal for readability -->
  <text x="640" y="220" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Research</tspan><tspan x="640" dy="21">Signals</tspan>
  </text>
  <text x="758" y="254" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="758" dy="0">Customer</tspan><tspan x="758" dy="21">Lens</tspan>
  </text>
  <text x="792" y="367" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="792" dy="0">Value</tspan><tspan x="792" dy="21">Story</tspan>
  </text>
  <text x="758" y="482" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="758" dy="0">Channel</tspan><tspan x="758" dy="21">Mix</tspan>
  </text>
  <text x="640" y="514" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Operating</tspan><tspan x="640" dy="21">Model</tspan>
  </text>
  <text x="522" y="482" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="522" dy="0">Talent</tspan><tspan x="522" dy="21">System</tspan>
  </text>
  <text x="488" y="367" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="488" dy="0">Risk</tspan><tspan x="488" dy="21">Controls</tspan>
  </text>
  <text x="522" y="254" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="522" dy="0">Growth</tspan><tspan x="522" dy="21">Metrics</tspan>
  </text>

  <text x="640" y="344" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" fill="#273142">
    <tspan x="640" font-size="22" font-weight="700">CENTRAL</tspan>
    <tspan x="640" dy="30" font-size="22" font-weight="700">THEME</tspan>
    <tspan x="640" dy="25" font-size="13" font-weight="600" fill="#7B8794">8 connected facets</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` to clone the petal shape; repeat the `<path>` elements directly so the PPTX remains editable and does not hard-fail.
- ❌ Do not apply a filter to a parent `<g>`; apply `filter="url(#softShadow)"` directly to each petal path, cap circle, or hub circle.
- ❌ Do not use `<textPath>` for curved labels around the flower; it will not translate reliably. Use positioned `<text>` blocks with explicit `width`.
- ❌ Do not rely on masks or clipping for the petal overlap effect; create the woven illusion with visible layered paths instead.

## Composition notes
- Keep the radial graphic centered and sized to roughly 70–80% of the slide height, leaving calm margins around the flower.
- Use the central hub for the unifying theme only; avoid cramming body copy into the center.
- Place short two-word labels inside petals and keep numbers large inside the outer caps for quick audience reference.
- Use a vivid eight-color palette, but soften the background with pale neutrals so the radial structure remains the visual focus.