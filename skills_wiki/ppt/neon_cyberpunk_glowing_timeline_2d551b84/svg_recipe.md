# SVG Recipe — Neon Cyberpunk Glowing Timeline

## Visual mechanism
A dark void-like slide is cut by a razor-thin luminous horizontal axis, with alternating milestone nodes above and below it. Each milestone uses a bright inner neon core, a larger hollow ring, vertical connector stems, and tight date/description text to create a premium cyberpunk roadmap aesthetic.

## SVG primitives needed
- 1× `<rect>` for the full dark background
- 1× `<radialGradient>` for subtle center illumination behind the timeline
- 1× `<linearGradient>` for the white/cyan/purple glowing timeline axis
- 5× `<linearGradient>` fills for colored vertical connector stems
- 5× `<filter>` glow effects for red, yellow, cyan, green, and purple milestone nodes
- 1× `<filter>` for soft white title glow
- 1× `<filter>` for the main axis glow
- 1× `<rect>` for the horizontal timeline axis
- 5× `<rect>` for vertical stems connecting nodes to text groups
- 10× `<circle>` for milestone nodes: 5 inner cores and 5 outer hollow rings
- Multiple low-opacity `<line>` and `<path>` elements for cyberpunk HUD/grid/circuit decoration
- 16× `<text>` elements for title, subtitle, years, labels, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="48%" r="70%">
      <stop offset="0%" stop-color="#263044"/>
      <stop offset="42%" stop-color="#161820"/>
      <stop offset="100%" stop-color="#0B0C10"/>
    </radialGradient>

    <linearGradient id="axisGrad" x1="120" y1="0" x2="1160" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#33CCFF" stop-opacity="0.15"/>
      <stop offset="16%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="84%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#AF52DE" stop-opacity="0.15"/>
    </linearGradient>

    <linearGradient id="stemRed" x1="0" y1="250" x2="0" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF3B30" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#FF3B30"/>
    </linearGradient>
    <linearGradient id="stemYellow" x1="0" y1="360" x2="0" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFCC00"/>
      <stop offset="100%" stop-color="#FFCC00" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="stemCyan" x1="0" y1="250" x2="0" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#33CCFF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#33CCFF"/>
    </linearGradient>
    <linearGradient id="stemGreen" x1="0" y1="360" x2="0" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#34C759"/>
      <stop offset="100%" stop-color="#34C759" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="stemPurple" x1="0" y1="250" x2="0" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#AF52DE" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#AF52DE"/>
    </linearGradient>

    <filter id="axisGlow" x="-30%" y="-900%" width="160%" height="1900%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="whiteGlow" x="-40%" y="-120%" width="180%" height="340%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glowRed" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowYellow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowCyan" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowGreen" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowPurple" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <line x1="80" y1="120" x2="1200" y2="120" stroke="#33CCFF" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="80" y1="600" x2="1200" y2="600" stroke="#AF52DE" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="180" y1="90" x2="180" y2="630" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1" stroke-dasharray="8 14"/>
  <line x1="410" y1="90" x2="410" y2="630" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1" stroke-dasharray="8 14"/>
  <line x1="640" y1="90" x2="640" y2="630" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1" stroke-dasharray="8 14"/>
  <line x1="870" y1="90" x2="870" y2="630" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1" stroke-dasharray="8 14"/>
  <line x1="1100" y1="90" x2="1100" y2="630" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1" stroke-dasharray="8 14"/>

  <path d="M60 205 H190 L225 170 H365" fill="none" stroke="#33CCFF" stroke-width="1.5" stroke-opacity="0.22"/>
  <path d="M1210 520 H1040 L1000 560 H870" fill="none" stroke="#AF52DE" stroke-width="1.5" stroke-opacity="0.22"/>
  <path d="M90 505 H245 L285 545 H420" fill="none" stroke="#FF3B30" stroke-width="1.2" stroke-opacity="0.15"/>
  <path d="M1190 210 H1000 L960 250 H835" fill="none" stroke="#34C759" stroke-width="1.2" stroke-opacity="0.15"/>

  <text x="640" y="70" width="780" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" letter-spacing="7" fill="#FFFFFF" filter="url(#whiteGlow)">CYBER ROADMAP</text>
  <text x="640" y="104" width="620" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#B9C7D6">SECURE PLATFORM EVOLUTION · 2019—2023</text>

  <rect x="120" y="358" width="1040" height="4" rx="2" fill="url(#axisGrad)" filter="url(#axisGlow)"/>

  <rect x="178.5" y="250" width="3" height="110" fill="url(#stemRed)"/>
  <rect x="408.5" y="360" width="3" height="110" fill="url(#stemYellow)"/>
  <rect x="638.5" y="250" width="3" height="110" fill="url(#stemCyan)"/>
  <rect x="868.5" y="360" width="3" height="110" fill="url(#stemGreen)"/>
  <rect x="1098.5" y="250" width="3" height="110" fill="url(#stemPurple)"/>

  <circle cx="180" cy="360" r="26" fill="none" stroke="#FF3B30" stroke-width="2.4" filter="url(#glowRed)"/>
  <circle cx="180" cy="360" r="9" fill="#FF3B30" filter="url(#glowRed)"/>
  <circle cx="410" cy="360" r="26" fill="none" stroke="#FFCC00" stroke-width="2.4" filter="url(#glowYellow)"/>
  <circle cx="410" cy="360" r="9" fill="#FFCC00" filter="url(#glowYellow)"/>
  <circle cx="640" cy="360" r="26" fill="none" stroke="#33CCFF" stroke-width="2.4" filter="url(#glowCyan)"/>
  <circle cx="640" cy="360" r="9" fill="#33CCFF" filter="url(#glowCyan)"/>
  <circle cx="870" cy="360" r="26" fill="none" stroke="#34C759" stroke-width="2.4" filter="url(#glowGreen)"/>
  <circle cx="870" cy="360" r="9" fill="#34C759" filter="url(#glowGreen)"/>
  <circle cx="1100" cy="360" r="26" fill="none" stroke="#AF52DE" stroke-width="2.4" filter="url(#glowPurple)"/>
  <circle cx="1100" cy="360" r="9" fill="#AF52DE" filter="url(#glowPurple)"/>

  <text x="180" y="204" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FF3B30" filter="url(#glowRed)">2019</text>
  <text x="180" y="230" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">ZERO TRUST KICKOFF</text>
  <text x="180" y="250" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9D1DA">Identity perimeter established<tspan x="180" dy="16">across all cloud workloads.</tspan></text>

  <text x="410" y="506" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFCC00" filter="url(#glowYellow)">2020</text>
  <text x="410" y="532" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">AUTOMATION CORE</text>
  <text x="410" y="552" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9D1DA">Policy engines reduced<tspan x="410" dy="16">manual response time by 62%.</tspan></text>

  <text x="640" y="204" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#33CCFF" filter="url(#glowCyan)">2021</text>
  <text x="640" y="230" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">AI DETECTION LAYER</text>
  <text x="640" y="250" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9D1DA">Behavioral models began<tspan x="640" dy="16">classifying anomalous traffic.</tspan></text>

  <text x="870" y="506" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#34C759" filter="url(#glowGreen)">2022</text>
  <text x="870" y="532" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">GLOBAL SCALEOUT</text>
  <text x="870" y="552" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9D1DA">Edge nodes deployed in<tspan x="870" dy="16">18 regions with live telemetry.</tspan></text>

  <text x="1100" y="204" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#AF52DE" filter="url(#glowPurple)">2023</text>
  <text x="1100" y="230" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">QUANTUM READY</text>
  <text x="1100" y="250" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9D1DA">Post-quantum encryption<tspan x="1100" dy="16">piloted for sensitive data flows.</tspan></text>

  <text x="72" y="674" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="2" fill="#6C7784">SYSTEM STATUS: SYNCHRONIZED</text>
  <text x="1025" y="674" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="2" fill="#6C7784">CONFIDENTIAL ROADMAP</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<filter>` on `<line>` elements for neon strokes; line filters are dropped. Use thin glowing `<rect>` elements for the main axis and stems when glow is needed.
- ❌ Do not use `<marker-end>` for arrows on circuit traces; cyberpunk details should be plain `<path>` or `<line>` strokes.
- ❌ Do not use `<pattern>` for the grid background; create sparse low-opacity lines manually so the slide remains editable.
- ❌ Do not use `<mask>` for fade effects around nodes; use gradients, opacity, and glow filters instead.
- ❌ Do not crowd every milestone with long body copy; the neon aesthetic depends on strong negative space.

## Composition notes
- Keep the main timeline axis exactly near vertical center, around `y=360`, so top and bottom milestone groups feel balanced.
- Use five evenly spaced nodes across roughly 80% of slide width; the first and last nodes should not touch the slide edges.
- Alternate milestone labels strictly above/below the axis to preserve rhythm and avoid text collisions.
- Let neon color appear only on nodes, dates, and stems; keep body copy white or pale gray so the accents feel premium rather than chaotic.