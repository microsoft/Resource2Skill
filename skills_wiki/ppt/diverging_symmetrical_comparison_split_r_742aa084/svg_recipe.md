# SVG Recipe — Diverging Symmetrical Comparison ("Split-Ring Before/After Infographic")

## Visual mechanism
A split-color donut ring anchors the slide center and visually binds two opposing columns into one transformation story. Symmetrical data cards on each side connect back to the ring through converging elbow lines, making “before” and “after” feel balanced but clearly contrasted.

## SVG primitives needed
- 1× `<rect>` for the slide background.
- 2× decorative `<path>` blobs for subtle warm/cool atmosphere behind each side.
- 8× `<path>` connector lines, drawn before the center ring so their convergence is hidden.
- 8× `<circle>` connector nodes at the card-side endpoints.
- 8× rounded `<rect>` content cards with soft fills.
- 8× rounded `<rect>` number badges/tabs attached to the cards.
- 2× thick stroked `<path>` arcs for the split-color central ring.
- 2× `<circle>` elements for the ring’s white center and subtle outer highlight.
- Multiple `<text>` elements with explicit `width` for title, side labels, numbers, headings, body copy, and center label.
- 2× `<linearGradient>` definitions for warm/cool decorative glows.
- 1× `<filter id="cardShadow">` for card depth.
- 1× `<filter id="ringGlow">` for the central focal glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="warmBlob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E74C3C" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#E74C3C" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="coolBlob" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3498DB" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#3498DB" stop-opacity="0"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode flood-color="#1F2D3D" flood-opacity="0.16"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="ringGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8FAFC"/>
  <path d="M0,130 C120,70 210,110 270,210 C330,310 260,420 120,430 C10,438 -60,350 0,130 Z" fill="url(#warmBlob)"/>
  <path d="M1280,120 C1160,60 1060,115 1010,220 C960,325 1035,438 1175,430 C1288,424 1345,300 1280,120 Z" fill="url(#coolBlob)"/>

  <text x="290" y="62" width="700" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#253243">Before And After</text>
  <text x="248" y="120" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" letter-spacing="3" fill="#E74C3C">BEFORE STATE</text>
  <text x="772" y="120" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" letter-spacing="3" fill="#3498DB">AFTER STATE</text>

  <!-- connectors sit behind the center split ring -->
  <path d="M500 190 L555 190 L640 380" fill="none" stroke="#E74C3C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M500 305 L555 305 L640 380" fill="none" stroke="#E74C3C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M500 420 L555 420 L640 380" fill="none" stroke="#E74C3C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M500 535 L555 535 L640 380" fill="none" stroke="#E74C3C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M780 190 L725 190 L640 380" fill="none" stroke="#3498DB" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M780 305 L725 305 L640 380" fill="none" stroke="#3498DB" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M780 420 L725 420 L640 380" fill="none" stroke="#3498DB" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M780 535 L725 535 L640 380" fill="none" stroke="#3498DB" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="500" cy="190" r="7" fill="#E74C3C"/>
  <circle cx="500" cy="305" r="7" fill="#E74C3C"/>
  <circle cx="500" cy="420" r="7" fill="#E74C3C"/>
  <circle cx="500" cy="535" r="7" fill="#E74C3C"/>
  <circle cx="780" cy="190" r="7" fill="#3498DB"/>
  <circle cx="780" cy="305" r="7" fill="#3498DB"/>
  <circle cx="780" cy="420" r="7" fill="#3498DB"/>
  <circle cx="780" cy="535" r="7" fill="#3498DB"/>

  <!-- left cards -->
  <rect x="90" y="155" width="410" height="70" rx="20" fill="#FDEDEC" filter="url(#cardShadow)"/>
  <rect x="90" y="155" width="76" height="70" rx="20" fill="#E74C3C"/>
  <text x="112" y="199" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">01</text>
  <text x="190" y="183" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Manual Intake</text>
  <text x="190" y="207" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Fragmented forms and slow handoffs</text>

  <rect x="90" y="270" width="410" height="70" rx="20" fill="#FDEDEC" filter="url(#cardShadow)"/>
  <rect x="90" y="270" width="76" height="70" rx="20" fill="#E74C3C"/>
  <text x="112" y="314" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">02</text>
  <text x="190" y="298" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Reactive Reporting</text>
  <text x="190" y="322" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Decisions made after issues appear</text>

  <rect x="90" y="385" width="410" height="70" rx="20" fill="#FDEDEC" filter="url(#cardShadow)"/>
  <rect x="90" y="385" width="76" height="70" rx="20" fill="#E74C3C"/>
  <text x="112" y="429" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">03</text>
  <text x="190" y="413" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Siloed Teams</text>
  <text x="190" y="437" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Local optimizations, limited visibility</text>

  <rect x="90" y="500" width="410" height="70" rx="20" fill="#FDEDEC" filter="url(#cardShadow)"/>
  <rect x="90" y="500" width="76" height="70" rx="20" fill="#E74C3C"/>
  <text x="112" y="544" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">04</text>
  <text x="190" y="528" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">High Friction</text>
  <text x="190" y="552" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Approvals depend on repeated follow-up</text>

  <!-- right cards -->
  <rect x="780" y="155" width="410" height="70" rx="20" fill="#EBF5FB" filter="url(#cardShadow)"/>
  <rect x="1114" y="155" width="76" height="70" rx="20" fill="#3498DB"/>
  <text x="1136" y="199" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">01</text>
  <text x="815" y="183" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Guided Intake</text>
  <text x="815" y="207" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Structured request paths and ownership</text>

  <rect x="780" y="270" width="410" height="70" rx="20" fill="#EBF5FB" filter="url(#cardShadow)"/>
  <rect x="1114" y="270" width="76" height="70" rx="20" fill="#3498DB"/>
  <text x="1136" y="314" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">02</text>
  <text x="815" y="298" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Predictive Signals</text>
  <text x="815" y="322" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Risks surfaced before they escalate</text>

  <rect x="780" y="385" width="410" height="70" rx="20" fill="#EBF5FB" filter="url(#cardShadow)"/>
  <rect x="1114" y="385" width="76" height="70" rx="20" fill="#3498DB"/>
  <text x="1136" y="429" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">03</text>
  <text x="815" y="413" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Shared Operating View</text>
  <text x="815" y="437" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">One source of truth across functions</text>

  <rect x="780" y="500" width="410" height="70" rx="20" fill="#EBF5FB" filter="url(#cardShadow)"/>
  <rect x="1114" y="500" width="76" height="70" rx="20" fill="#3498DB"/>
  <text x="1136" y="544" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">04</text>
  <text x="815" y="528" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#2C3E50">Low-Touch Flow</text>
  <text x="815" y="552" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Automated routing and clear next actions</text>

  <!-- split-ring focal node drawn last to hide connector convergence -->
  <circle cx="640" cy="380" r="112" fill="#FFFFFF" opacity="0.9" filter="url(#ringGlow)"/>
  <path d="M640 282 A98 98 0 0 0 640 478" fill="none" stroke="#E74C3C" stroke-width="32" stroke-linecap="butt"/>
  <path d="M640 282 A98 98 0 0 1 640 478" fill="none" stroke="#3498DB" stroke-width="32" stroke-linecap="butt"/>
  <circle cx="640" cy="380" r="58" fill="#FFFFFF"/>
  <text x="604" y="371" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#253243">VS</text>
  <text x="584" y="401" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" letter-spacing="1.5" fill="#6B7280">TRANSITION</text>
</svg>
```

## Avoid in this skill
- ❌ Do not create the split ring with `<mask>` or `mask="url(...)"`; masks will not translate reliably. Use two thick stroked arc `<path>` elements instead.
- ❌ Do not place connector arrowheads with `marker-end` on `<path>`; this comparison style does not need arrows, and path markers may disappear.
- ❌ Do not draw connector lines after the ring; the messy convergence point should be hidden underneath the central donut.
- ❌ Do not use one shared card group via `<use>`; duplicate the native shapes directly so every card remains editable in PowerPoint.
- ❌ Do not omit `width` on text elements; PowerPoint text boxes need explicit widths to avoid unexpected wrapping.

## Composition notes
- Keep the ring exactly on the vertical centerline; it should feel like the “hinge” between two states.
- Reserve the upper 15–18% of the slide for title and side labels, then stack four slim rows below.
- Use warm colors only on the left and cool colors only on the right; the split ring should repeat both colors to unify the story.
- Draw connectors first, cards second, and the ring last so the center node looks clean and intentional.