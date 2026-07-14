# SVG Recipe — Split-Panel Geometric Agenda Slide

## Visual mechanism
A giant off-canvas circle creates a curved left title panel, while the right side stays bright and minimal for a vertically paced agenda list. Matching blue numbered bullets link the two halves and turn a plain table of contents into a clean executive keynote layout.

## SVG primitives needed
- 1× `<rect>` for the full-slide light background gradient
- 1× oversized `<ellipse>` for the clipped left geometric panel
- 2× translucent `<circle>` accents inside the blue panel
- 2× decorative `<path>` curve strokes on the left panel for subtle depth
- 1× `<line>` for the faint vertical rhythm guide behind the agenda bullets
- 5× `<circle>` for numbered agenda bullets
- 15× `<text>` blocks for title, date, intro, agenda titles, descriptions, and bullet numbers
- 1× `<linearGradient id="bgGrad">` for the white-to-light-gray slide background
- 1× `<linearGradient id="panelGrad">` for the premium blue panel fill
- 1× `<filter id="softShadow">` applied to the left panel and agenda bullets

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#ECEFF4"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="-560" y1="120" x2="390" y2="620">
      <stop offset="0%" stop-color="#2557B8"/>
      <stop offset="55%" stop-color="#4472C4"/>
      <stop offset="100%" stop-color="#5E8BE0"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.05  0 0 0 0 0.09  0 0 0 0 0.18  0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="-150" cy="360" rx="540" ry="540" fill="url(#panelGrad)" filter="url(#softShadow)"/>

  <circle cx="120" cy="112" r="82" fill="#FFFFFF" opacity="0.08"/>
  <circle cx="250" cy="630" r="130" fill="#FFFFFF" opacity="0.07"/>

  <path d="M-80 158 C40 92, 190 110, 318 206" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.16"/>
  <path d="M-40 582 C92 496, 190 500, 315 590" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.13"/>

  <text x="62" y="288" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700" fill="#FFFFFF">
    Agenda
  </text>
  <text x="66" y="326" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#DCE8FF" letter-spacing="1.2">
    12-SEP-202X
  </text>
  <text x="66" y="378" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF" opacity="0.92">
    <tspan x="66" dy="0">A focused walkthrough of the</tspan>
    <tspan x="66" dy="27">priorities, milestones, and</tspan>
    <tspan x="66" dy="27">decisions for today’s session.</tspan>
  </text>

  <text x="475" y="96" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#4472C4" letter-spacing="2">
    EXECUTIVE WORKSHOP
  </text>
  <text x="475" y="132" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#2F3542">
    Today’s discussion flow
  </text>

  <line x1="512" y1="190" x2="512" y2="615" stroke="#D9E1F2" stroke-width="3" stroke-dasharray="6 12"/>

  <g transform="translate(0 210)">
    <circle cx="512" cy="0" r="25" fill="#4472C4" filter="url(#softShadow)"/>
    <text x="512" y="8" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">01</text>
    <text x="565" y="-9" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#333844">Market context and key signals</text>
    <text x="565" y="22" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7A7F89">
      Review the external shifts, client needs, and performance patterns shaping the plan.
    </text>
  </g>

  <g transform="translate(0 300)">
    <circle cx="512" cy="0" r="25" fill="#4472C4" filter="url(#softShadow)"/>
    <text x="512" y="8" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">02</text>
    <text x="565" y="-9" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#333844">Strategic priorities</text>
    <text x="565" y="22" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7A7F89">
      Align on the few initiatives that will create the highest commercial and operational lift.
    </text>
  </g>

  <g transform="translate(0 390)">
    <circle cx="512" cy="0" r="25" fill="#4472C4" filter="url(#softShadow)"/>
    <text x="512" y="8" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">03</text>
    <text x="565" y="-9" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#333844">Operating model updates</text>
    <text x="565" y="22" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7A7F89">
      Identify ownership, governance cadence, and the support structure required to execute.
    </text>
  </g>

  <g transform="translate(0 480)">
    <circle cx="512" cy="0" r="25" fill="#4472C4" filter="url(#softShadow)"/>
    <text x="512" y="8" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">04</text>
    <text x="565" y="-9" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#333844">Milestones and dependencies</text>
    <text x="565" y="22" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7A7F89">
      Map the critical dates, cross-functional handoffs, and decision gates for the next quarter.
    </text>
  </g>

  <g transform="translate(0 570)">
    <circle cx="512" cy="0" r="25" fill="#4472C4" filter="url(#softShadow)"/>
    <text x="512" y="8" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">05</text>
    <text x="565" y="-9" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#333844">Decisions and next steps</text>
    <text x="565" y="22" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#7A7F89">
      Confirm open decisions, accountable owners, and the immediate actions after the meeting.
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using a clipped `<mask>` to create the left curve; instead, place an oversized ellipse partly off-canvas.
- ❌ Applying `filter` to the vertical guide `<line>`; line filters are dropped, so keep the guide simple.
- ❌ Building the agenda as one large multiline text box; separate editable text blocks give better PowerPoint control.
- ❌ Using `marker-end` for decorative arrows in the agenda flow; if arrows are needed, use native `<line>` elements with direct marker attributes only, or avoid arrows entirely.
- ❌ Placing text too close to the curved boundary; the panel edge is visually active and needs breathing room.

## Composition notes
- Keep the left panel around 35–40% of the slide visually, even though the ellipse itself extends far beyond the canvas.
- Place title text well inside the blue curve, around x=60–70, so it does not collide with the circular edge.
- The right agenda list should start around x=475–565, leaving a clean gutter between the curve and list copy.
- Use the accent blue only for the panel, bullets, and small section label; keep all body text charcoal/gray to preserve a premium rhythm.