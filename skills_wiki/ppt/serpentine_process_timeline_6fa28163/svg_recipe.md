# SVG Recipe — Serpentine Process Timeline

## Visual mechanism
A sequence of stage cards is anchored on a central horizontal axis and connected by alternating upper/lower cubic arcs, creating a smooth S-shaped journey. Each stage owns a distinct color that repeats across its connector, icon frame, label, and title block to make the flow feel continuous but still segmented.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 5× thick `<path>` connector arcs for the serpentine spine
- 5× thin dashed `<path>` overlays to imply direction and movement along the spine
- 6× rounded `<rect>` icon containers with colored strokes
- 6× solid `<rect>` bottom labels inside the icon containers
- 6× rounded `<rect>` title blocks, alternating above and below the timeline
- 6× rounded `<rect>` description cards behind body copy
- 6× `<circle>` number badges on the stage containers
- Multiple `<path>`, `<circle>`, and `<line>` primitives for simple editable icons
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, stage labels, numbers, and descriptions
- 1× `<filter id="softShadow">` applied to cards and containers
- 1× `<filter id="pathGlow">` applied to connector paths
- 1× `<linearGradient>` for the subtle executive-style background

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFD"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="pathGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-20 625 C210 570 320 705 510 650 C725 588 880 670 1320 560" fill="none" stroke="#DCE8F5" stroke-width="34" opacity="0.55"/>
  <path d="M1010 80 C1120 115 1175 65 1295 120" fill="none" stroke="#E7ECF6" stroke-width="42" opacity="0.75"/>

  <text x="640" y="58" width="900" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#26384A">Customer Onboarding Roadmap</text>
  <text x="640" y="92" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7785">A six-stage serpentine process that guides the audience from discovery to measurable value</text>

  <!-- serpentine connector spine, drawn behind the stage cards -->
  <path d="M165 350 C225 500 295 500 355 350" fill="none" stroke="#2E3D49" stroke-width="18" stroke-linecap="round" opacity="0.78" filter="url(#pathGlow)"/>
  <path d="M355 350 C415 205 485 205 545 350" fill="none" stroke="#2E75B6" stroke-width="18" stroke-linecap="round" opacity="0.78" filter="url(#pathGlow)"/>
  <path d="M545 350 C605 500 675 500 735 350" fill="none" stroke="#70AD47" stroke-width="18" stroke-linecap="round" opacity="0.78" filter="url(#pathGlow)"/>
  <path d="M735 350 C795 205 865 205 925 350" fill="none" stroke="#FFC000" stroke-width="18" stroke-linecap="round" opacity="0.78" filter="url(#pathGlow)"/>
  <path d="M925 350 C985 500 1055 500 1115 350" fill="none" stroke="#C00000" stroke-width="18" stroke-linecap="round" opacity="0.78" filter="url(#pathGlow)"/>

  <path d="M165 350 C225 500 295 500 355 350" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="10 15" stroke-linecap="round" opacity="0.9"/>
  <path d="M355 350 C415 205 485 205 545 350" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="10 15" stroke-linecap="round" opacity="0.9"/>
  <path d="M545 350 C605 500 675 500 735 350" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="10 15" stroke-linecap="round" opacity="0.9"/>
  <path d="M735 350 C795 205 865 205 925 350" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="10 15" stroke-linecap="round" opacity="0.9"/>
  <path d="M925 350 C985 500 1055 500 1115 350" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="10 15" stroke-linecap="round" opacity="0.9"/>

  <!-- Stage 1 -->
  <rect x="85" y="178" width="160" height="40" rx="12" fill="#2E3D49" filter="url(#softShadow)"/>
  <text x="165" y="204" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Discover</text>
  <rect x="75" y="226" width="180" height="62" rx="14" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="92" y="250" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#344255">Map needs, goals, stakeholders, and decision criteria.</text>
  <rect x="90" y="305" width="150" height="90" rx="20" fill="#FFFFFF" stroke="#2E3D49" stroke-width="5" filter="url(#softShadow)"/>
  <rect x="90" y="365" width="150" height="30" rx="0" fill="#2E3D49"/>
  <text x="165" y="385" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">INTAKE</text>
  <circle cx="105" cy="318" r="15" fill="#2E3D49"/>
  <text x="105" y="323" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">1</text>
  <circle cx="156" cy="337" r="15" fill="none" stroke="#2E3D49" stroke-width="4"/>
  <path d="M168 349 L184 365" fill="none" stroke="#2E3D49" stroke-width="4" stroke-linecap="round"/>

  <!-- Stage 2 -->
  <rect x="265" y="445" width="180" height="40" rx="12" fill="#2E75B6" filter="url(#softShadow)"/>
  <text x="355" y="471" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Design</text>
  <rect x="265" y="493" width="180" height="66" rx="14" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="282" y="518" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#344255">Translate insights into a clear onboarding blueprint.</text>
  <rect x="280" y="305" width="150" height="90" rx="20" fill="#FFFFFF" stroke="#2E75B6" stroke-width="5" filter="url(#softShadow)"/>
  <rect x="280" y="365" width="150" height="30" rx="0" fill="#2E75B6"/>
  <text x="355" y="385" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">BLUEPRINT</text>
  <circle cx="295" cy="318" r="15" fill="#2E75B6"/>
  <text x="295" y="323" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">2</text>
  <path d="M335 335 L375 322 L375 360 L335 372 Z" fill="none" stroke="#2E75B6" stroke-width="4" stroke-linejoin="round"/>
  <path d="M335 335 L355 350 L375 322" fill="none" stroke="#2E75B6" stroke-width="3"/>

  <!-- Stage 3 -->
  <rect x="465" y="178" width="160" height="40" rx="12" fill="#70AD47" filter="url(#softShadow)"/>
  <text x="545" y="204" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Configure</text>
  <rect x="455" y="226" width="180" height="62" rx="14" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="472" y="250" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#344255">Set up workflows, access, data rules, and integrations.</text>
  <rect x="470" y="305" width="150" height="90" rx="20" fill="#FFFFFF" stroke="#70AD47" stroke-width="5" filter="url(#softShadow)"/>
  <rect x="470" y="365" width="150" height="30" rx="0" fill="#70AD47"/>
  <text x="545" y="385" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">SETUP</text>
  <circle cx="485" cy="318" r="15" fill="#70AD47"/>
  <text x="485" y="323" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">3</text>
  <circle cx="545" cy="350" r="20" fill="none" stroke="#70AD47" stroke-width="4"/>
  <path d="M545 326 L545 337 M545 363 L545 374 M521 350 L532 350 M558 350 L569 350 M528 333 L536 341 M554 359 L562 367 M528 367 L536 359 M554 341 L562 333" stroke="#70AD47" stroke-width="3" stroke-linecap="round"/>

  <!-- Stage 4 -->
  <rect x="645" y="445" width="180" height="40" rx="12" fill="#FFC000" filter="url(#softShadow)"/>
  <text x="735" y="471" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Validate</text>
  <rect x="645" y="493" width="180" height="66" rx="14" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="662" y="518" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#344255">Run pilots, review edge cases, and confirm readiness.</text>
  <rect x="660" y="305" width="150" height="90" rx="20" fill="#FFFFFF" stroke="#FFC000" stroke-width="5" filter="url(#softShadow)"/>
  <rect x="660" y="365" width="150" height="30" rx="0" fill="#FFC000"/>
  <text x="735" y="385" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">PILOT</text>
  <circle cx="675" cy="318" r="15" fill="#FFC000"/>
  <text x="675" y="323" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">4</text>
  <path d="M710 348 L727 365 L762 327" fill="none" stroke="#D99B00" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Stage 5 -->
  <rect x="845" y="178" width="160" height="40" rx="12" fill="#C00000" filter="url(#softShadow)"/>
  <text x="925" y="204" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Launch</text>
  <rect x="835" y="226" width="180" height="62" rx="14" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="852" y="250" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#344255">Activate users, training paths, and executive comms.</text>
  <rect x="850" y="305" width="150" height="90" rx="20" fill="#FFFFFF" stroke="#C00000" stroke-width="5" filter="url(#softShadow)"/>
  <rect x="850" y="365" width="150" height="30" rx="0" fill="#C00000"/>
  <text x="925" y="385" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">GO LIVE</text>
  <circle cx="865" cy="318" r="15" fill="#C00000"/>
  <text x="865" y="323" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">5</text>
  <path d="M925 324 C940 337 943 355 930 370 C910 362 902 348 911 331 Z" fill="none" stroke="#C00000" stroke-width="4" stroke-linejoin="round"/>
  <path d="M912 365 L900 377 M920 371 L912 385" stroke="#C00000" stroke-width="3" stroke-linecap="round"/>

  <!-- Stage 6 -->
  <rect x="1025" y="445" width="180" height="40" rx="12" fill="#7030A0" filter="url(#softShadow)"/>
  <text x="1115" y="471" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Optimize</text>
  <rect x="1025" y="493" width="180" height="66" rx="14" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="1042" y="518" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#344255">Measure adoption, refine plays, and scale best practices.</text>
  <rect x="1040" y="305" width="150" height="90" rx="20" fill="#FFFFFF" stroke="#7030A0" stroke-width="5" filter="url(#softShadow)"/>
  <rect x="1040" y="365" width="150" height="30" rx="0" fill="#7030A0"/>
  <text x="1115" y="385" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">SCALE</text>
  <circle cx="1055" cy="318" r="15" fill="#7030A0"/>
  <text x="1055" y="323" width="30" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">6</text>
  <path d="M1090 365 L1090 345 L1108 345 L1108 365 Z M1113 365 L1113 333 L1131 333 L1131 365 Z M1136 365 L1136 322 L1154 322 L1154 365 Z" fill="none" stroke="#7030A0" stroke-width="4" stroke-linejoin="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` arrowheads on curved `<path>` connectors; they will disappear. Use numbered badges or dashed overlays to imply direction instead.
- ❌ Do not build the serpentine with many short `<line>` segments; the visual mechanism depends on smooth cubic `<path>` continuity.
- ❌ Do not apply `clip-path` to cards, arcs, or text; clipping should only be used on `<image>` elements if adding photos.
- ❌ Do not use `<mask>` to hide connector sections behind cards; simply draw connector paths first, then layer the stage containers above them.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for angled labels; keep transforms to translate, rotate, or scale only.

## Composition notes
- Keep the central icon containers on one horizontal axis; the sense of motion comes from the alternating connector arcs and alternating content blocks.
- Reserve the upper and lower thirds for titles/descriptions so the central serpentine path remains visually clean.
- Repeat each stage color across connector, title block, badge, and label to reinforce stage ownership.
- Use generous horizontal spacing; if stages are too close, the S-curve becomes cramped and reads like decoration rather than navigation.