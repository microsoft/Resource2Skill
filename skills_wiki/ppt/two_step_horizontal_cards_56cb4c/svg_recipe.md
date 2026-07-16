# SVG Recipe — Two Step Horizontal Cards

## Visual mechanism
Two wide rounded cards are stacked vertically, each anchored by an oversized overlapping numbered circle and finished with a colored ribbon tab. The layout creates a simple two-step sequence with strong left-to-right reading flow, generous whitespace, and premium depth from shadows, gradients, and small fold details.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<rect>` for the main rounded horizontal cards
- 2× `<path>` for right-side ribbon tabs with angled notches
- 2× `<path>` for small folded ribbon shadow accents
- 4× `<circle>` for overlapping step badges and inner highlights
- 2× `<line>` for subtle card divider rules
- 6× `<path>` for decorative abstract background arcs, bullet icons, and arrowhead accents
- Multiple `<text>` elements with explicit `width` for title, step numbers, card headings, and supporting copy
- 3× `<linearGradient>` for background, card surface, and ribbon/badge color treatments
- 1× `<radialGradient>` for soft badge highlight
- 1× `<filter id="cardShadow">` applied to cards and badges
- 1× `<filter id="softGlow">` applied to decorative background shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#F9FBFF"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F7FF"/>
    </linearGradient>

    <linearGradient id="blueRibbon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2E7BFF"/>
      <stop offset="100%" stop-color="#173DCC"/>
    </linearGradient>

    <linearGradient id="coralRibbon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF8A4C"/>
      <stop offset="100%" stop-color="#EF3F6B"/>
    </linearGradient>

    <radialGradient id="badgeLight" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.06  0 0 0 0 0.12  0 0 0 0 0.25  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M1020 35 C1130 75 1195 145 1224 250 C1167 221 1091 206 1009 216 C1053 155 1055 91 1020 35Z"
        fill="#C9DCFF" opacity="0.55" filter="url(#softGlow)"/>
  <path d="M84 604 C173 552 286 560 360 633 C260 652 172 681 92 714 C73 681 70 645 84 604Z"
        fill="#FFD6C8" opacity="0.6" filter="url(#softGlow)"/>
  <path d="M988 636 C1040 594 1110 586 1184 612 C1138 642 1111 677 1102 719 C1051 701 1015 674 988 636Z"
        fill="#D9E7FF" opacity="0.9"/>

  <text x="96" y="82" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#15233D">Two-step horizontal process</text>
  <text x="98" y="120" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#62708A">Use oversized step markers, ribbon tabs, and calm spacing to make two ideas feel connected but distinct.</text>

  <g id="step-one">
    <rect x="178" y="178" width="920" height="168" rx="30" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
    <path d="M1018 178 L1148 178 Q1170 178 1170 200 L1170 324 Q1170 346 1148 346 L1018 346 L1050 262 Z"
          fill="url(#blueRibbon)" filter="url(#cardShadow)"/>
    <path d="M1018 346 L1050 314 L1050 346 Z" fill="#0E2EA5" opacity="0.55"/>

    <circle cx="178" cy="262" r="72" fill="url(#blueRibbon)" filter="url(#cardShadow)"/>
    <circle cx="178" cy="262" r="72" fill="url(#badgeLight)"/>
    <circle cx="178" cy="262" r="48" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.65"/>
    <text x="136" y="279" width="84" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="48" font-weight="800" text-anchor="middle" fill="#FFFFFF">01</text>

    <text x="292" y="230" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="25" font-weight="700" fill="#16243B">Frame the decision</text>
    <text x="292" y="267" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="17" fill="#60708C">Clarify the problem, success metric, and constraints before the team debates solutions.</text>
    <line x1="292" y1="294" x2="880" y2="294" stroke="#DCE6F7" stroke-width="2"/>
    <path d="M304 319 C304 313 308 309 314 309 C320 309 324 313 324 319 C324 325 320 329 314 329 C308 329 304 325 304 319Z"
          fill="#2E7BFF"/>
    <text x="338" y="325" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="15" fill="#566680">Align stakeholders on the highest-leverage question.</text>
    <text x="1062" y="272" width="76" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="16" font-weight="700" text-anchor="middle" fill="#FFFFFF">DEFINE</text>
  </g>

  <g id="step-two">
    <rect x="178" y="402" width="920" height="168" rx="30" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
    <path d="M1018 402 L1148 402 Q1170 402 1170 424 L1170 548 Q1170 570 1148 570 L1018 570 L1050 486 Z"
          fill="url(#coralRibbon)" filter="url(#cardShadow)"/>
    <path d="M1018 570 L1050 538 L1050 570 Z" fill="#B7224B" opacity="0.55"/>

    <circle cx="178" cy="486" r="72" fill="url(#coralRibbon)" filter="url(#cardShadow)"/>
    <circle cx="178" cy="486" r="72" fill="url(#badgeLight)"/>
    <circle cx="178" cy="486" r="48" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.65"/>
    <text x="136" y="503" width="84" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="48" font-weight="800" text-anchor="middle" fill="#FFFFFF">02</text>

    <text x="292" y="454" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="25" font-weight="700" fill="#16243B">Run the focused sprint</text>
    <text x="292" y="491" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="17" fill="#60708C">Prototype quickly, pressure-test assumptions, then move the best option into execution.</text>
    <line x1="292" y1="518" x2="880" y2="518" stroke="#DCE6F7" stroke-width="2"/>
    <path d="M304 543 C304 537 308 533 314 533 C320 533 324 537 324 543 C324 549 320 553 314 553 C308 553 304 549 304 543Z"
          fill="#FF6B5E"/>
    <text x="338" y="549" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="15" fill="#566680">Convert learning into one clear owner, timeline, and next action.</text>
    <text x="1062" y="496" width="76" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="16" font-weight="700" text-anchor="middle" fill="#FFFFFF">EXECUTE</text>
  </g>

  <line x1="178" y1="334" x2="178" y2="414" stroke="#B9C7E6" stroke-width="3" stroke-dasharray="8 10"/>
  <path d="M178 432 L162 408 L194 408 Z" fill="#B9C7E6"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` for the card overlap or badge cutouts; use layered circles and paths instead.
- ❌ Applying `filter` to the dashed connector `<line>`; line filters are dropped, so keep the connector flat.
- ❌ Using `marker-end` on a `<path>` for the process arrow; draw the arrowhead as a small standalone `<path>`.
- ❌ Building the ribbon with `<use>` duplicates; repeat explicit `<path>` elements so PowerPoint keeps everything editable.
- ❌ Putting text inside auto-sized boxes without `width`; every `<text>` needs an explicit width for stable PPT rendering.

## Composition notes
- Keep the two cards centered in the middle 60% of the slide, with the title occupying the upper-left and ample negative space around it.
- Let the numbered badges overlap the left edge of each card by roughly half their diameter; this is the signature visual hook.
- Use one dominant accent color per step, repeated on the badge, ribbon, bullet dot, and label to create a clear sequence rhythm.
- Reserve the right ribbon for short action labels only; the main explanatory copy should stay inside the white card body.