# SVG Recipe — Winding Serpentine Roadmap

## Visual mechanism
A thick, editable SVG path snakes across the slide in a horizontal S-curve, styled as an asphalt road with a dashed center line. Numbered circular milestones sit directly on the road, while alternating text cards fill the negative space above and below the curves to create a journey-like timeline.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft background
- 3× `<path>` for decorative terrain / ambient blobs behind the roadmap
- 2× `<path>` copies of the same serpentine route: one thick dark road base, one dashed white center line
- 6× `<circle>` for milestone nodes placed along the road
- 6× `<text>` for milestone numbers inside nodes
- 6× `<line>` for dotted connectors from nodes to text cards
- 6× `<rect>` for rounded milestone description cards
- 12× `<text>` for milestone titles and short descriptions
- 2× `<text>` for slide title and subtitle
- 2× `<linearGradient>` for background and accent card fills
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for road, cards, and milestone nodes
- 1× `<filter id="blueGlow">` using `feGaussianBlur` for subtle accent glow around milestones

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#EEF6FF"/>
      <stop offset="100%" stop-color="#F7FAFC"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F8FF"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blueGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="7" result="glow"/>
      <feColorMatrix in="glow" type="matrix"
        values="0 0 0 0 0.035  0 0 0 0 0.52  0 0 0 0 0.89  0 0 0 .45 0" result="blue"/>
      <feMerge>
        <feMergeNode in="blue"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80 590 C160 500 250 700 470 610 C700 515 850 650 1080 565 C1190 525 1260 555 1360 510 L1360 760 L-80 760 Z"
        fill="#DDEEFF" opacity="0.55"/>
  <path d="M850 70 C1010 20 1110 65 1280 20 L1280 190 C1120 230 1025 175 880 225 C790 255 735 210 765 150 C780 118 810 88 850 70 Z"
        fill="#E8F4FF" opacity="0.8"/>
  <path d="M30 315 C145 255 255 330 365 275 C455 230 525 250 575 310 C410 355 235 365 30 315 Z"
        fill="#EAF7F0" opacity="0.9"/>

  <text x="72" y="56" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#1F2937">
    Strategic Roadmap
  </text>
  <text x="74" y="94" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#64748B">
    A winding journey from discovery to market scale, with clear decision points along the way.
  </text>

  <!-- Serpentine road: left-to-right, right-to-left, left-to-right -->
  <path d="M115 220 C270 165 410 165 560 220 C690 268 805 276 925 220 C1000 185 1110 205 1135 295 C1165 405 985 420 885 390 C735 345 600 345 455 390 C335 428 155 420 150 510 C145 608 315 615 460 570 C625 520 785 520 955 570 C1040 595 1120 600 1180 570"
        fill="none" stroke="#20242B" stroke-width="70" stroke-linecap="round" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M115 220 C270 165 410 165 560 220 C690 268 805 276 925 220 C1000 185 1110 205 1135 295 C1165 405 985 420 885 390 C735 345 600 345 455 390 C335 428 155 420 150 510 C145 608 315 615 460 570 C625 520 785 520 955 570 C1040 595 1120 600 1180 570"
        fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="28 24" opacity="0.95"/>

  <!-- Connectors -->
  <line x1="178" y1="199" x2="178" y2="140" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="420" y1="198" x2="420" y2="276" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="680" y1="252" x2="680" y2="160" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="1028" y1="237" x2="1028" y2="140" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="390" y1="414" x2="390" y2="486" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="820" y1="540" x2="820" y2="456" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>

  <!-- Text cards -->
  <rect x="82" y="112" width="195" height="86" rx="18" fill="url(#cardGrad)" stroke="#D8E6F7" filter="url(#softShadow)"/>
  <rect x="320" y="276" width="205" height="92" rx="18" fill="url(#cardGrad)" stroke="#D8E6F7" filter="url(#softShadow)"/>
  <rect x="575" y="112" width="215" height="94" rx="18" fill="url(#cardGrad)" stroke="#D8E6F7" filter="url(#softShadow)"/>
  <rect x="928" y="80" width="210" height="100" rx="18" fill="url(#cardGrad)" stroke="#D8E6F7" filter="url(#softShadow)"/>
  <rect x="282" y="486" width="215" height="96" rx="18" fill="url(#cardGrad)" stroke="#D8E6F7" filter="url(#softShadow)"/>
  <rect x="712" y="456" width="220" height="96" rx="18" fill="url(#cardGrad)" stroke="#D8E6F7" filter="url(#softShadow)"/>

  <text x="104" y="140" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0984E3">Discover</text>
  <text x="104" y="166" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Map needs, signals, and customer friction.</text>

  <text x="342" y="305" width="158" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0984E3">Define</text>
  <text x="342" y="331" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Prioritize the bets that deserve investment.</text>

  <text x="598" y="141" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0984E3">Prototype</text>
  <text x="598" y="167" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Build evidence through fast, testable concepts.</text>

  <text x="952" y="110" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0984E3">Validate</text>
  <text x="952" y="136" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Measure adoption risk before scaling delivery.</text>

  <text x="306" y="516" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0984E3">Launch</text>
  <text x="306" y="542" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Release the first market-ready experience.</text>

  <text x="736" y="486" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#0984E3">Scale</text>
  <text x="736" y="512" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Expand capability, coverage, and measurable impact.</text>

  <!-- Milestone nodes -->
  <circle cx="178" cy="199" r="32" fill="#FFFFFF" stroke="#0984E3" stroke-width="8" filter="url(#blueGlow)"/>
  <circle cx="420" cy="198" r="32" fill="#FFFFFF" stroke="#0984E3" stroke-width="8" filter="url(#blueGlow)"/>
  <circle cx="680" cy="252" r="32" fill="#FFFFFF" stroke="#0984E3" stroke-width="8" filter="url(#blueGlow)"/>
  <circle cx="1028" cy="237" r="32" fill="#FFFFFF" stroke="#0984E3" stroke-width="8" filter="url(#blueGlow)"/>
  <circle cx="390" cy="414" r="32" fill="#FFFFFF" stroke="#0984E3" stroke-width="8" filter="url(#blueGlow)"/>
  <circle cx="820" cy="540" r="32" fill="#FFFFFF" stroke="#0984E3" stroke-width="8" filter="url(#blueGlow)"/>

  <text x="161" y="209" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#1F2937" text-anchor="middle">1</text>
  <text x="403" y="208" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#1F2937" text-anchor="middle">2</text>
  <text x="663" y="262" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#1F2937" text-anchor="middle">3</text>
  <text x="1011" y="247" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#1F2937" text-anchor="middle">4</text>
  <text x="373" y="424" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#1F2937" text-anchor="middle">5</text>
  <text x="803" y="550" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#1F2937" text-anchor="middle">6</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the road from many separate rectangles or arcs; use one continuous `<path>` so the dashed center line aligns perfectly.
- ❌ Do not use `marker-end` arrows on the serpentine path; the journey direction should be implied by numbering and layout.
- ❌ Do not apply filters to `<line>` connectors; shadows on lines are dropped by the translator.
- ❌ Do not use `<textPath>` for labels along the road; place editable text cards near the milestones instead.
- ❌ Do not clip or mask non-image shapes to create the road; a stroked path is cleaner and translates better.

## Composition notes
- Keep the road as the dominant visual anchor, occupying roughly the middle 65% of slide height while leaving title space at the top.
- Alternate text cards above and below the road to exploit the negative spaces created by the curves.
- Place milestone circles directly on the path, not beside it, so they feel like checkpoints on the journey.
- Use a restrained palette: dark asphalt, white lane markings, one bright accent color for nodes and titles, and pale background terrain for depth.