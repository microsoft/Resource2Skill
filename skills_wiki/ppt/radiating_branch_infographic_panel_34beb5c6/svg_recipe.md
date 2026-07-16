# SVG Recipe — Radiating Branch Infographic Panel

## Visual mechanism
A large central hub anchors the idea while five colored, ribbon-like branches radiate outward and resolve into stacked rounded content panels. The branch geometry starts as a tight trunk behind the hub, then fans vertically into separate tracks, creating a polished “single source to multiple outcomes” hierarchy.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× decorative `<path>` shapes for subtle background arcs and ambient motion
- 5× filled `<path>` ribbon branches, each using a curved polygon-like path
- 5× `<rect>` rounded content panels aligned on the right
- 1× large `<circle>` central hub with shadow
- 5× small `<circle>` icon nodes overlapping the panels
- 10× small `<path>` icon strokes inside the nodes
- 1× soft halo `<circle>` behind the hub
- 1× `<filter id="shadow">` for hub, panels, and nodes
- 1× `<filter id="softGlow">` for the ambient hub glow
- 5× `<linearGradient>` fills for the branch/panel color progression
- Multiple `<text>` elements with explicit `width` attributes for hub, panel titles, body copy, numbers, and small labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="g1" x1="300" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#154B54"/><stop offset="1" stop-color="#1A535C"/>
    </linearGradient>
    <linearGradient id="g2" x1="300" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#246F70"/><stop offset="1" stop-color="#2E817B"/>
    </linearGradient>
    <linearGradient id="g3" x1="300" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#3AA68F"/><stop offset="1" stop-color="#44B59C"/>
    </linearGradient>
    <linearGradient id="g4" x1="300" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#66B983"/><stop offset="1" stop-color="#76C893"/>
    </linearGradient>
    <linearGradient id="g5" x1="300" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#89CD76"/><stop offset="1" stop-color="#99D98C"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F8F6"/>
  <path d="M-40 120 C170 40 300 80 455 170 C620 266 755 238 910 130 C1045 36 1168 18 1320 70"
        fill="none" stroke="#DDEBE6" stroke-width="34" opacity="0.45"/>
  <path d="M-30 640 C150 560 310 600 480 640 C680 688 800 620 960 540 C1110 464 1200 470 1320 520"
        fill="none" stroke="#E7F1E7" stroke-width="44" opacity="0.65"/>
  <path d="M1010 70 C1110 10 1205 34 1248 112 C1298 204 1232 310 1128 310 C1028 310 945 216 972 126 C978 104 991 84 1010 70 Z"
        fill="#EAF4EF" opacity="0.72"/>

  <circle cx="335" cy="360" r="190" fill="#BDE8D5" opacity="0.38" filter="url(#softGlow)"/>

  <path d="M300 270 L470 270 C540 268 595 140 718 140 L718 212 C600 212 535 296 470 296 L300 296 Z"
        fill="url(#g1)" opacity="0.98"/>
  <path d="M300 305 L470 305 C550 306 602 232 718 232 L718 304 C602 304 550 331 470 331 L300 331 Z"
        fill="url(#g2)" opacity="0.98"/>
  <path d="M300 340 L470 340 C555 340 606 324 718 324 L718 396 C606 396 555 366 470 366 L300 366 Z"
        fill="url(#g3)" opacity="0.98"/>
  <path d="M300 375 L470 375 C550 374 602 488 718 488 L718 416 C602 416 550 401 470 401 L300 401 Z"
        fill="url(#g4)" opacity="0.98"/>
  <path d="M300 410 L470 410 C535 414 600 580 718 580 L718 508 C595 508 540 436 470 436 L300 436 Z"
        fill="url(#g5)" opacity="0.98"/>

  <rect x="690" y="140" width="470" height="72" rx="26" fill="url(#g1)" filter="url(#shadow)"/>
  <rect x="690" y="232" width="470" height="72" rx="26" fill="url(#g2)" filter="url(#shadow)"/>
  <rect x="690" y="324" width="470" height="72" rx="26" fill="url(#g3)" filter="url(#shadow)"/>
  <rect x="690" y="416" width="470" height="72" rx="26" fill="url(#g4)" filter="url(#shadow)"/>
  <rect x="690" y="508" width="470" height="72" rx="26" fill="url(#g5)" filter="url(#shadow)"/>

  <circle cx="335" cy="360" r="156" fill="#FFFFFF" filter="url(#shadow)"/>
  <circle cx="335" cy="360" r="132" fill="none" stroke="#E8F1EE" stroke-width="2"/>
  <text x="335" y="320" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#183D43">
    <tspan x="335" dy="0">CORE</tspan>
    <tspan x="335" dy="34">OPERATING</tspan>
    <tspan x="335" dy="34">MODEL</tspan>
  </text>
  <text x="335" y="432" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6C7E7B">
    Five connected workstreams from one strategic center
  </text>

  <circle cx="702" cy="176" r="34" fill="#FFFFFF" filter="url(#shadow)"/>
  <circle cx="702" cy="268" r="34" fill="#FFFFFF" filter="url(#shadow)"/>
  <circle cx="702" cy="360" r="34" fill="#FFFFFF" filter="url(#shadow)"/>
  <circle cx="702" cy="452" r="34" fill="#FFFFFF" filter="url(#shadow)"/>
  <circle cx="702" cy="544" r="34" fill="#FFFFFF" filter="url(#shadow)"/>

  <path d="M690 176 C694 166 710 166 714 176 C710 186 694 186 690 176 Z" fill="none" stroke="#1A535C" stroke-width="3"/>
  <circle cx="702" cy="176" r="5" fill="#1A535C"/>
  <path d="M689 278 L699 258 L707 272 L715 254" fill="none" stroke="#2E817B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M688 360 L698 370 L718 350" fill="none" stroke="#44B59C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M702 432 L718 440 L715 462 C712 470 708 474 702 478 C696 474 692 470 689 462 L686 440 Z" fill="none" stroke="#76C893" stroke-width="3" stroke-linejoin="round"/>
  <path d="M706 524 L688 550 L702 550 L698 566 L718 538 L704 538 Z" fill="#99D98C"/>

  <text x="760" y="167" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">01  Market Signal</text>
  <text x="760" y="191" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDF2EE">Capture demand shifts, weak signals, and customer intent before competitors react.</text>
  <text x="760" y="259" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">02  Capability Build</text>
  <text x="760" y="283" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#E2F4F1">Convert strategy into talent, tooling, governance, and repeatable execution rituals.</text>
  <text x="760" y="351" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">03  Process Flow</text>
  <text x="760" y="375" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ECFAF5">Design handoffs that reduce friction and keep cross-functional teams synchronized.</text>
  <text x="760" y="443" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">04  Risk Control</text>
  <text x="760" y="467" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#F2FFF5">Embed checkpoints, ownership, and escalation paths without slowing momentum.</text>
  <text x="760" y="535" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">05  Growth Loop</text>
  <text x="760" y="559" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#F7FFF4">Feed learnings back into the hub so each cycle improves speed, quality, and scale.</text>

  <text x="72" y="78" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#5C7773">STRATEGIC BREAKDOWN</text>
</svg>
```

## Avoid in this skill
- ❌ Using straight connector lines instead of filled curved branch paths; the premium effect depends on broad ribbons that visibly fan out.
- ❌ Applying `marker-end` arrowheads to paths; if directional arrows are needed, use separate `<line>` elements with direct marker attributes, but this layout usually does not need arrows.
- ❌ Clipping non-image elements; branch geometry should be drawn directly as paths rather than relying on masks or clips.
- ❌ Overcrowding the central hub with long text; keep the hub to 2–4 short words and place details in the right panels.
- ❌ Drawing all branches in the same color; the sequential palette is what makes the hierarchy scannable.

## Composition notes
- Keep the hub left-of-center, around 25–30% of slide width, with enough radius to cover the compressed branch trunks.
- Reserve the right half for stacked panels; consistent panel height and vertical gaps make the fan geometry feel intentional.
- Draw branches first, then panels, then hub and icon nodes on top so seams are hidden and the composition feels layered.
- Use a dark-to-light analogous palette from top to bottom; pair it with a quiet off-white background and subtle shadows for keynote-level polish.