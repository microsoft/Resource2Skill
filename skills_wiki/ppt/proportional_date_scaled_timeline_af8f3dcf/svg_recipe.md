# SVG Recipe — Proportional Date-Scaled Timeline

## Visual mechanism
A horizontal timeline axis maps each event’s x-position from its real calendar date, so clusters and long gaps are visible at a glance. Alternating callout cards above and below the axis keep labels readable while thin connector lines preserve the exact date anchor.

## SVG primitives needed
- 1× `<rect>` full-slide background with a subtle premium gradient
- 1× `<text>` title and 1× `<text>` subtitle / formula note
- 1× rounded `<rect>` for the main horizontal time axis
- 10–12× `<line>` for month/quarter tick marks and tick labels
- 6× `<circle>` event markers placed at date-scaled x-coordinates
- 6× rounded `<rect>` callout cards, alternating above/below the axis
- 6× `<line>` or simple `<path>` connectors from marker to callout
- 12× `<text>` elements for dates and event descriptions inside callouts
- 1–2× decorative `<path>` elements for subtle emphasis on long elapsed gaps
- 1× `<filter id="cardShadow">` applied to callout rectangles
- 1× `<filter id="markerGlow">` applied to key marker circles
- 2–3× `<linearGradient>` definitions for background, axis, and accent fills

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFD"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF6FA"/>
    </linearGradient>

    <linearGradient id="axisGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#D2D9DE"/>
      <stop offset="50%" stop-color="#BFC9CF"/>
      <stop offset="100%" stop-color="#D2D9DE"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#59C7E8"/>
      <stop offset="100%" stop-color="#1F8FB8"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="markerGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <text x="70" y="68" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#26323A">
    Proportional Date-Scaled Timeline
  </text>
  <text x="72" y="101" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#66737C">
    X-position = start + ((event date − first date) ÷ total days) × timeline width
  </text>

  <text x="1030" y="67" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#228CB3" text-anchor="end">
    Jun 2023 → Apr 2024
  </text>

  <!-- Main proportional axis: start x=140, end x=1140, axis y=380 -->
  <rect x="130" y="374" width="1020" height="12" rx="6" fill="url(#axisGrad)"/>

  <!-- Quarter / month ticks give the viewer a true scale reference -->
  <line x1="140" y1="354" x2="140" y2="406" stroke="#AAB5BC" stroke-width="1.5"/>
  <line x1="236" y1="364" x2="236" y2="396" stroke="#CDD5DA" stroke-width="1"/>
  <line x1="335" y1="364" x2="335" y2="396" stroke="#CDD5DA" stroke-width="1"/>
  <line x1="433" y1="354" x2="433" y2="406" stroke="#AAB5BC" stroke-width="1.5"/>
  <line x1="532" y1="364" x2="532" y2="396" stroke="#CDD5DA" stroke-width="1"/>
  <line x1="630" y1="364" x2="630" y2="396" stroke="#CDD5DA" stroke-width="1"/>
  <line x1="729" y1="354" x2="729" y2="406" stroke="#AAB5BC" stroke-width="1.5"/>
  <line x1="827" y1="364" x2="827" y2="396" stroke="#CDD5DA" stroke-width="1"/>
  <line x1="929" y1="364" x2="929" y2="396" stroke="#CDD5DA" stroke-width="1"/>
  <line x1="1021" y1="354" x2="1021" y2="406" stroke="#AAB5BC" stroke-width="1.5"/>
  <line x1="1140" y1="354" x2="1140" y2="406" stroke="#AAB5BC" stroke-width="1.5"/>

  <text x="140" y="430" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7C8991" text-anchor="middle">Jun</text>
  <text x="433" y="430" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7C8991" text-anchor="middle">Sep</text>
  <text x="729" y="430" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7C8991" text-anchor="middle">Dec</text>
  <text x="1021" y="430" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7C8991" text-anchor="middle">Mar</text>
  <text x="1140" y="430" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7C8991" text-anchor="middle">Apr</text>

  <!-- Subtle long-delay emphasis: this span visually explains why proportional spacing matters -->
  <path d="M456 348 C610 316, 850 316, 1038 348" fill="none" stroke="#D8EEF6" stroke-width="10" stroke-linecap="round"/>
  <text x="650" y="316" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#59AFCB" text-anchor="middle">
    6+ month execution gap is visible
  </text>

  <!-- Connectors -->
  <line x1="140" y1="374" x2="140" y2="258" stroke="#44ACD6" stroke-width="1.6" stroke-dasharray="4 6"/>
  <line x1="280" y1="386" x2="280" y2="478" stroke="#44ACD6" stroke-width="1.6" stroke-dasharray="4 6"/>
  <line x1="312" y1="374" x2="312" y2="238" stroke="#44ACD6" stroke-width="1.6" stroke-dasharray="4 6"/>
  <line x1="433" y1="386" x2="433" y2="503" stroke="#44ACD6" stroke-width="1.6" stroke-dasharray="4 6"/>
  <line x1="1057" y1="374" x2="1057" y2="240" stroke="#44ACD6" stroke-width="1.6" stroke-dasharray="4 6"/>
  <line x1="1140" y1="386" x2="1140" y2="487" stroke="#44ACD6" stroke-width="1.6" stroke-dasharray="4 6"/>

  <!-- Event markers: x values are proportional to actual days elapsed across a 314-day span -->
  <circle cx="140" cy="380" r="11" fill="url(#accentGrad)" stroke="#FFFFFF" stroke-width="3" filter="url(#markerGlow)"/>
  <circle cx="280" cy="380" r="9" fill="url(#accentGrad)" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="312" cy="380" r="9" fill="url(#accentGrad)" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="433" cy="380" r="9" fill="url(#accentGrad)" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="1057" cy="380" r="10" fill="url(#accentGrad)" stroke="#FFFFFF" stroke-width="3" filter="url(#markerGlow)"/>
  <circle cx="1140" cy="380" r="9" fill="url(#accentGrad)" stroke="#FFFFFF" stroke-width="3"/>

  <!-- Alternating callout cards -->
  <rect x="52" y="170" width="215" height="88" rx="16" fill="#FFFFFF" stroke="#DCE6EB" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="75" y="202" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1F8FB8">Jun 1, 2023</text>
  <text x="75" y="229" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35424B">Project conception</text>

  <rect x="186" y="478" width="200" height="88" rx="16" fill="#FFFFFF" stroke="#DCE6EB" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="209" y="510" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1F8FB8">Jul 15, 2023</text>
  <text x="209" y="537" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35424B">Core team assembled</text>

  <rect x="302" y="150" width="220" height="88" rx="16" fill="#FFFFFF" stroke="#DCE6EB" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="325" y="182" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1F8FB8">Jul 25, 2023</text>
  <text x="325" y="209" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35424B">Scope &amp; budget approved</text>

  <rect x="397" y="503" width="215" height="88" rx="16" fill="#FFFFFF" stroke="#DCE6EB" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="420" y="535" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1F8FB8">Sep 1, 2023</text>
  <text x="420" y="562" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35424B">Execution phase begins</text>

  <rect x="946" y="152" width="230" height="88" rx="16" fill="#FFFFFF" stroke="#DCE6EB" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="969" y="184" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1F8FB8">Mar 15, 2024</text>
  <text x="969" y="211" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35424B">Final deployment</text>

  <rect x="1008" y="487" width="220" height="88" rx="16" fill="#FFFFFF" stroke="#DCE6EB" stroke-width="1.2" filter="url(#cardShadow)"/>
  <text x="1031" y="519" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#1F8FB8">Apr 10, 2024</text>
  <text x="1031" y="546" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#35424B">Wrap-up &amp; retrospective</text>

  <text x="70" y="665" width="1040" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A8790">
    Notice how July events cluster tightly while the deployment gap occupies most of the visual width — this is the core advantage over evenly spaced timelines.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Evenly distributing markers with identical gaps; that defeats the purpose of a date-scaled timeline.
- ❌ Letting dense event clusters force overlapping callout cards; nudge cards horizontally if needed, but keep the marker anchored to the exact date.
- ❌ Using chart-only elements or non-editable screenshots when the axis, markers, labels, and connectors can remain native editable SVG shapes.
- ❌ Applying `filter` to `<line>` connectors; shadows/glows on lines may be dropped, so keep connector styling simple.
- ❌ Using `marker-end` on paths for arrows; this technique does not need arrowheads, and they may disappear in translation.

## Composition notes
- Keep the timeline axis across roughly 80–85% of slide width, with generous left/right margins so the first and last callouts do not feel clipped.
- Place the axis slightly below vertical center; this leaves enough room for a strong title and top-row callouts.
- Alternate callouts above and below the axis, but allow small manual x-offsets for clustered dates while preserving exact marker positions.
- Use a restrained gray axis and ticks, then reserve the accent color for markers, dates, and key explanatory annotations.