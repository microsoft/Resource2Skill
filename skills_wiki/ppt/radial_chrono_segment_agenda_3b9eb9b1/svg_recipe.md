# SVG Recipe — Radial Chrono-Segment Agenda

## Visual mechanism
A minimalist clock face sits at the center of the slide, wrapped by four thick, color-coded radial time segments. Each segment visually maps to an agenda card positioned in its quadrant, turning a linear agenda into a time-aware circular schedule.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 1× `<radialGradient>` for a subtle central glow behind the clock
- 4× `<path>` for thick chrono arc segments around the clock
- 1× `<circle>` for the central clock face
- 1× `<circle>` for the inner clock hub
- 2× `<line>` for the clock hands
- 12× small `<line>` tick marks around the clock face
- 4× `<rect>` for agenda text cards
- 4× `<circle>` for color-coded agenda bullets
- 4× `<text>` numerals inside the bullets
- 1× `<text>` for the main slide title
- 4× `<text>` blocks with nested `<tspan>` for agenda title, time, and description
- 4× `<line>` connector strokes linking text cards toward the radial segments
- 1× `<filter id="softShadow">` applied to cards and clock elements
- 1× `<filter id="arcGlow">` applied to colored arc paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="centerGlow" cx="50%" cy="52%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#F4F7FA"/>
      <stop offset="100%" stop-color="#EEF1F5"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="arcGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="3" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F8FA"/>
  <circle cx="640" cy="382" r="315" fill="url(#centerGlow)" opacity="0.9"/>

  <text x="640" y="72" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#1E1E1E">
    Radial Chrono-Segment Agenda
  </text>
  <text x="640" y="108" width="600" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#667085">
    Time-boxed flow for a focused 90-minute working session
  </text>

  <!-- Agenda cards -->
  <rect x="82" y="158" width="330" height="128" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="82" y="158" width="7" height="128" rx="3.5" fill="#7030A0"/>
  <circle cx="385" cy="198" r="23" fill="#7030A0"/>
  <text x="385" y="207" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">1</text>
  <text x="356" y="194" width="250" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">
    <tspan x="356" dy="0">Opening Context</tspan>
    <tspan x="356" dy="25" font-size="14" font-weight="600" fill="#7030A0">09:00–09:20</tspan>
    <tspan x="356" dy="25" font-size="14" font-weight="400" fill="#667085">Align goals, success criteria,</tspan>
    <tspan x="356" dy="19" font-size="14" font-weight="400" fill="#667085">and operating principles.</tspan>
  </text>

  <rect x="82" y="454" width="330" height="128" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="82" y="454" width="7" height="128" rx="3.5" fill="#00B050"/>
  <circle cx="385" cy="494" r="23" fill="#00B050"/>
  <text x="385" y="503" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">4</text>
  <text x="356" y="490" width="250" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">
    <tspan x="356" dy="0">Decisions &amp; Actions</tspan>
    <tspan x="356" dy="25" font-size="14" font-weight="600" fill="#00B050">10:10–10:30</tspan>
    <tspan x="356" dy="25" font-size="14" font-weight="400" fill="#667085">Confirm owners, next steps,</tspan>
    <tspan x="356" dy="19" font-size="14" font-weight="400" fill="#667085">and follow-up cadence.</tspan>
  </text>

  <rect x="868" y="158" width="330" height="128" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="1191" y="158" width="7" height="128" rx="3.5" fill="#FFC000"/>
  <circle cx="895" cy="198" r="23" fill="#FFC000"/>
  <text x="895" y="207" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#1E1E1E">2</text>
  <text x="924" y="194" width="250" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">
    <tspan x="924" dy="0">Discovery Review</tspan>
    <tspan x="924" dy="25" font-size="14" font-weight="600" fill="#B57A00">09:20–09:45</tspan>
    <tspan x="924" dy="25" font-size="14" font-weight="400" fill="#667085">Surface insights, constraints,</tspan>
    <tspan x="924" dy="19" font-size="14" font-weight="400" fill="#667085">and stakeholder signals.</tspan>
  </text>

  <rect x="868" y="454" width="330" height="128" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="1191" y="454" width="7" height="128" rx="3.5" fill="#00B0F0"/>
  <circle cx="895" cy="494" r="23" fill="#00B0F0"/>
  <text x="895" y="503" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">3</text>
  <text x="924" y="490" width="250" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">
    <tspan x="924" dy="0">Prioritization Sprint</tspan>
    <tspan x="924" dy="25" font-size="14" font-weight="600" fill="#0078A8">09:45–10:10</tspan>
    <tspan x="924" dy="25" font-size="14" font-weight="400" fill="#667085">Rank opportunities by impact,</tspan>
    <tspan x="924" dy="19" font-size="14" font-weight="400" fill="#667085">urgency, and effort.</tspan>
  </text>

  <!-- Connectors -->
  <line x1="412" y1="222" x2="508" y2="308" stroke="#7030A0" stroke-width="3" stroke-linecap="round" opacity="0.65"/>
  <line x1="412" y1="518" x2="510" y2="458" stroke="#00B050" stroke-width="3" stroke-linecap="round" opacity="0.65"/>
  <line x1="868" y1="222" x2="772" y2="308" stroke="#FFC000" stroke-width="3" stroke-linecap="round" opacity="0.75"/>
  <line x1="868" y1="518" x2="770" y2="458" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" opacity="0.65"/>

  <!-- Radial chrono segments -->
  <path d="M 681.4 227.5 A 160 160 0 0 1 797.6 354.2"
        fill="none" stroke="#FFC000" stroke-width="34" stroke-linecap="butt" filter="url(#arcGlow)"/>
  <path d="M 797.6 409.8 A 160 160 0 0 1 667.8 539.6"
        fill="none" stroke="#00B0F0" stroke-width="34" stroke-linecap="butt" filter="url(#arcGlow)"/>
  <path d="M 612.2 539.6 A 160 160 0 0 1 482.4 409.8"
        fill="none" stroke="#00B050" stroke-width="34" stroke-linecap="butt" filter="url(#arcGlow)"/>
  <path d="M 482.4 354.2 A 160 160 0 0 1 612.2 224.4"
        fill="none" stroke="#7030A0" stroke-width="34" stroke-linecap="butt" filter="url(#arcGlow)"/>

  <!-- Clock body -->
  <circle cx="640" cy="382" r="108" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="13" filter="url(#softShadow)"/>
  <line x1="640" y1="274" x2="640" y2="292" stroke="#1E1E1E" stroke-width="4" stroke-linecap="round"/>
  <line x1="640" y1="472" x2="640" y2="490" stroke="#1E1E1E" stroke-width="4" stroke-linecap="round"/>
  <line x1="532" y1="382" x2="550" y2="382" stroke="#1E1E1E" stroke-width="4" stroke-linecap="round"/>
  <line x1="730" y1="382" x2="748" y2="382" stroke="#1E1E1E" stroke-width="4" stroke-linecap="round"/>
  <line x1="586" y1="288" x2="595" y2="304" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="694" y1="288" x2="685" y2="304" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="734" y1="328" x2="718" y2="337" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="734" y1="436" x2="718" y2="427" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="694" y1="476" x2="685" y2="460" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="586" y1="476" x2="595" y2="460" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="546" y1="436" x2="562" y2="427" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>
  <line x1="546" y1="328" x2="562" y2="337" stroke="#1E1E1E" stroke-width="3" stroke-linecap="round"/>

  <line x1="640" y1="382" x2="589" y2="319" stroke="#1E1E1E" stroke-width="10" stroke-linecap="round"/>
  <line x1="640" y1="382" x2="690" y2="438" stroke="#1E1E1E" stroke-width="13" stroke-linecap="round"/>
  <circle cx="640" cy="382" r="15" fill="#1E1E1E"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<marker-end>` for connector arrows; arrowheads may disappear, and the visual works better with clean radial connector lines.
- ❌ Applying a filter to `<line>` elements; keep glows/shadows on cards, paths, circles, or text only.
- ❌ Building the colored segments as raster images; use editable `<path>` arcs with thick strokes so users can recolor and resize them in PowerPoint.
- ❌ Placing all agenda text in the center; the method depends on perimeter text blocks leaving the clock as the focal anchor.
- ❌ Using `<textPath>` to curve labels around the clock; it will not translate reliably.

## Composition notes
- Keep the central clock and arc system within the middle 35–40% of the slide; the surrounding negative space is needed for readable agenda cards.
- Use quadrant logic: left-side cards should right-align toward the clock, while right-side cards should left-align toward the clock.
- Assign one strong accent color per segment and repeat it in the card bullet, card edge, and connector line for instant association.
- Leave visible gaps between arc segments so each time block reads as a discrete agenda module rather than a continuous ring.