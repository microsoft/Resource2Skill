# SVG Recipe — Sequential Vertical Node Timeline (Agenda Reveal)

## Visual mechanism
A standard agenda is converted into a guided vertical journey: numbered circular nodes sit on a central spine, with each agenda item revealed as a clean text card to the right. The strong contrast between a saturated modern background, white connectors, dark nodes, and bright typography creates a keynote-style structure that is easy to animate step by step.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× decorative `<path>` blobs for premium depth and directional movement
- 1× `<rect>` for the title accent bar
- 1× `<text>` for the agenda title
- 4× `<line>` for vertical connector segments between nodes
- 5× `<circle>` for dark numbered timeline nodes
- 5× `<text>` for node numbers
- 5× rounded `<rect>` agenda cards behind labels
- 5× `<text>` agenda label groups using nested `<tspan>` for title/subtitle styling
- 1× `<linearGradient>` for the teal background
- 1× `<radialGradient>` for subtle ambient glow
- 1× `<filter id="softShadow">` applied to node circles and agenda cards
- 1× `<filter id="titleGlow">` applied to the title accent and title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgTeal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1BC8B7"/>
      <stop offset="55%" stop-color="#18AFA8"/>
      <stop offset="100%" stop-color="#0B6F78"/>
    </linearGradient>
    <radialGradient id="ambientGlow" cx="78%" cy="18%" r="62%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="48%" stop-color="#7FF7EA" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#00616C" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02 0 0 0 0 0.16 0 0 0 0 0.18 0 0 0 0.24 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="titleGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgTeal)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambientGlow)"/>

  <path d="M-80,608 C90,520 160,600 260,508 C352,424 456,470 536,384 C594,320 654,304 724,330 L724,720 L-80,720 Z"
        fill="#FFFFFF" opacity="0.07"/>
  <path d="M1040,-80 C1130,42 1284,36 1348,158 C1398,254 1320,334 1392,442 L1392,-80 Z"
        fill="#063F49" opacity="0.22"/>

  <rect x="110" y="170" width="8" height="108" rx="4" fill="#FFFFFF" opacity="0.95" filter="url(#titleGlow)"/>
  <text x="140" y="219" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="800" fill="#FFFFFF" letter-spacing="2" filter="url(#titleGlow)">AGENDA</text>
  <text x="142" y="256" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500" fill="#D9FFFB" letter-spacing="1.5">TODAY’S STRATEGIC FLOW</text>

  <line x1="560" y1="134" x2="560" y2="238" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.82"/>
  <line x1="560" y1="238" x2="560" y2="342" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.82"/>
  <line x1="560" y1="342" x2="560" y2="446" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.82"/>
  <line x1="560" y1="446" x2="560" y2="550" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.82"/>

  <g id="step-01">
    <circle cx="560" cy="134" r="38" fill="#34383C" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
    <text x="526" y="145" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" font-weight="800" fill="#FFFFFF">01</text>
    <rect x="625" y="101" width="430" height="66" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
    <text x="653" y="127" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#243A3E">
      <tspan x="653" y="127" font-size="22" font-weight="800">Opening Context</tspan>
      <tspan x="653" y="151" font-size="13" font-weight="500" fill="#5B7478">Frame the opportunity and meeting objectives</tspan>
    </text>
  </g>

  <g id="step-02">
    <circle cx="560" cy="238" r="38" fill="#34383C" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
    <text x="526" y="249" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" font-weight="800" fill="#FFFFFF">02</text>
    <rect x="625" y="205" width="430" height="66" rx="18" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
    <text x="653" y="231" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#243A3E">
      <tspan x="653" y="231" font-size="22" font-weight="800">Market Signals</tspan>
      <tspan x="653" y="255" font-size="13" font-weight="500" fill="#5B7478">Key shifts, risks, and competitive movement</tspan>
    </text>
  </g>

  <g id="step-03">
    <circle cx="560" cy="342" r="38" fill="#34383C" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
    <text x="526" y="353" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" font-weight="800" fill="#FFFFFF">03</text>
    <rect x="625" y="309" width="430" height="66" rx="18" fill="#FFFFFF" opacity="0.88" filter="url(#softShadow)"/>
    <text x="653" y="335" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#243A3E">
      <tspan x="653" y="335" font-size="22" font-weight="800">Strategic Options</tspan>
      <tspan x="653" y="359" font-size="13" font-weight="500" fill="#5B7478">Compare the paths available to leadership</tspan>
    </text>
  </g>

  <g id="step-04">
    <circle cx="560" cy="446" r="38" fill="#34383C" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
    <text x="526" y="457" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" font-weight="800" fill="#FFFFFF">04</text>
    <rect x="625" y="413" width="430" height="66" rx="18" fill="#FFFFFF" opacity="0.84" filter="url(#softShadow)"/>
    <text x="653" y="439" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#243A3E">
      <tspan x="653" y="439" font-size="22" font-weight="800">Execution Roadmap</tspan>
      <tspan x="653" y="463" font-size="13" font-weight="500" fill="#5B7478">Milestones, owners, and operating cadence</tspan>
    </text>
  </g>

  <g id="step-05">
    <circle cx="560" cy="550" r="38" fill="#34383C" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
    <text x="526" y="561" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" font-weight="800" fill="#FFFFFF">05</text>
    <rect x="625" y="517" width="430" height="66" rx="18" fill="#FFFFFF" opacity="0.80" filter="url(#softShadow)"/>
    <text x="653" y="543" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#243A3E">
      <tspan x="653" y="543" font-size="22" font-weight="800">Decision & Next Steps</tspan>
      <tspan x="653" y="567" font-size="13" font-weight="500" fill="#5B7478">Confirm priorities and immediate commitments</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using one long connector line if you want sequential reveal animation; separate line segments make step-by-step wipes easier in PowerPoint.
- ❌ Placing text labels on both sides unless there is a strong reason; it weakens the simple left-to-right reading rhythm.
- ❌ Applying filters to `<line>` connector segments; shadows/glows on lines may be dropped, so keep connectors flat.
- ❌ Using tiny node numbers or low-contrast outlines; the node is the visual anchor and must remain legible from the back of the room.
- ❌ Building the timeline as a single raster image; keep nodes, lines, and labels editable for animation and agenda updates.

## Composition notes
- Keep the title block on the left third and the timeline spine slightly right of center, leaving generous label space on the right.
- Use equal vertical spacing between nodes; the precision is what makes the agenda feel structured and executive.
- Put connector lines behind the circles so nodes feel like “stations” on the path rather than dots pasted over a line.
- For animation, reveal each group in order: node zoom, connector wipe downward, card/text fade or wipe from left.