# SVG Recipe — Modular Project Portfolio Dashboard

## Visual mechanism
A premium PMO dashboard built from repeated horizontal project modules: each row combines a colored project identity block, a summary panel, and three standardized donut KPI cells. A right-hand sidebar compresses portfolio-wide metrics into large numeric tiles, creating a fast executive scan path from project-level health to aggregate totals.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 1× `<linearGradient>` for the soft dashboard background wash.
- 1× `<linearGradient>` for the sidebar panel fill.
- 1× `<filter id="cardShadow">` applied to row cards and sidebar for subtle elevation.
- 1× `<filter id="softGlow">` applied to accent circles for a premium ambient glow.
- 3× large row `<rect>` cards for project modules.
- 3× colored `<rect>` project identity blocks.
- 9× KPI cell `<rect>` panels for status, risk, and resources.
- 18× `<circle>` elements for donut charts: one muted track and one colored progress ring per KPI.
- 3× `<rect>` progress bars in summary cells for mini timeline/budget cues.
- Multiple `<text>` elements with explicit `width` attributes for title, labels, summaries, percentages, and sidebar numbers.
- 2× decorative `<circle>` glow accents in the background/sidebar.
- 1× decorative `<path>` accent curve behind the sidebar to avoid a flat spreadsheet look.
- 4× sidebar metric `<rect>` tiles with large number typography.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF3FF"/>
    </linearGradient>
    <linearGradient id="sidebarFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#182033"/>
      <stop offset="100%" stop-color="#101624"/>
    </linearGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <circle cx="1030" cy="92" r="80" fill="#DDE7FF" opacity="0.42" filter="url(#softGlow)"/>
  <circle cx="1190" cy="630" r="96" fill="#BEEAF3" opacity="0.30" filter="url(#softGlow)"/>
  <path d="M1010,88 C1080,20 1198,28 1262,118 L1262,292 C1192,218 1100,222 1018,286 Z" fill="#FFFFFF" opacity="0.26"/>

  <text x="52" y="58" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#212529">Project KPI Dashboard</text>
  <text x="54" y="88" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C757D">Portfolio health, delivery confidence, risk exposure, and resource utilization across active strategic programs</text>

  <rect x="1000" y="106" width="226" height="548" rx="28" fill="url(#sidebarFill)" filter="url(#cardShadow)"/>
  <text x="1030" y="148" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#A9B7D0">PORTFOLIO SNAPSHOT</text>
  <rect x="1030" y="178" width="166" height="82" rx="16" fill="#FFFFFF" opacity="0.08"/>
  <text x="1050" y="215" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">08</text>
  <text x="1050" y="240" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A9B7D0">Ongoing Projects</text>
  <rect x="1030" y="278" width="166" height="82" rx="16" fill="#FFFFFF" opacity="0.08"/>
  <text x="1050" y="315" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">$25.3M</text>
  <text x="1050" y="340" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A9B7D0">Allocated Budget</text>
  <rect x="1030" y="378" width="166" height="82" rx="16" fill="#FFFFFF" opacity="0.08"/>
  <text x="1050" y="415" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">50</text>
  <text x="1050" y="440" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A9B7D0">Team Members</text>
  <rect x="1030" y="478" width="166" height="82" rx="16" fill="#FFFFFF" opacity="0.08"/>
  <text x="1050" y="515" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">102</text>
  <text x="1050" y="540" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A9B7D0">Tasks Pending</text>
  <text x="1030" y="612" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F8DA8">Updated today · PMO weekly review</text>

  <g transform="translate(52 120)">
    <rect x="0" y="0" width="908" height="154" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="132" height="154" rx="22" fill="#5872FF"/>
    <rect x="100" y="0" width="32" height="154" fill="#5872FF"/>
    <text x="66" y="66" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">Project A</text>
    <text x="66" y="91" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#E8ECFF">Q3 Launch</text>
    <text x="158" y="36" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#6C757D">SUMMARY</text>
    <text x="158" y="62" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#212529">
      <tspan x="158" dy="0">On track for Q3 launch.</tspan><tspan x="158" dy="19">UI/UX milestones completed;</tspan><tspan x="158" dy="19">vendor testing starts next week.</tspan>
    </text>
    <rect x="158" y="119" width="218" height="8" rx="4" fill="#E9ECEF"/>
    <rect x="158" y="119" width="142" height="8" rx="4" fill="#5872FF"/>
    <rect x="420" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="489" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">STATUS TRACK</text>
    <circle cx="489" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="489" cy="86" r="30" fill="none" stroke="#FFC107" stroke-width="11" stroke-linecap="round" stroke-dasharray="94 189" transform="rotate(-90 489 86)"/>
    <text x="489" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">50%</text>
    <rect x="576" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="645" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">RISK ANALYSIS</text>
    <circle cx="645" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="645" cy="86" r="30" fill="none" stroke="#FD7E14" stroke-width="11" stroke-linecap="round" stroke-dasharray="57 189" transform="rotate(-90 645 86)"/>
    <text x="645" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">30%</text>
    <rect x="732" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="801" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">RESOURCES</text>
    <circle cx="801" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="801" cy="86" r="30" fill="none" stroke="#DC3545" stroke-width="11" stroke-linecap="round" stroke-dasharray="170 189" transform="rotate(-90 801 86)"/>
    <text x="801" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">90%</text>
  </g>

  <g transform="translate(52 296)">
    <rect x="0" y="0" width="908" height="154" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="132" height="154" rx="22" fill="#28A745"/>
    <rect x="100" y="0" width="32" height="154" fill="#28A745"/>
    <text x="66" y="66" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">Project B</text>
    <text x="66" y="91" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#E6F6EA">Platform Core</text>
    <text x="158" y="36" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#6C757D">SUMMARY</text>
    <text x="158" y="62" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#212529">
      <tspan x="158" dy="0">Budget review pending.</tspan><tspan x="158" dy="19">Minor backend integration delay;</tspan><tspan x="158" dy="19">scope remains under control.</tspan>
    </text>
    <rect x="158" y="119" width="218" height="8" rx="4" fill="#E9ECEF"/>
    <rect x="158" y="119" width="164" height="8" rx="4" fill="#28A745"/>
    <rect x="420" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="489" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">STATUS TRACK</text>
    <circle cx="489" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="489" cy="86" r="30" fill="none" stroke="#FFC107" stroke-width="11" stroke-linecap="round" stroke-dasharray="132 189" transform="rotate(-90 489 86)"/>
    <text x="489" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">70%</text>
    <rect x="576" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="645" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">RISK ANALYSIS</text>
    <circle cx="645" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="645" cy="86" r="30" fill="none" stroke="#FD7E14" stroke-width="11" stroke-linecap="round" stroke-dasharray="94 189" transform="rotate(-90 645 86)"/>
    <text x="645" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">50%</text>
    <rect x="732" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="801" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">RESOURCES</text>
    <circle cx="801" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="801" cy="86" r="30" fill="none" stroke="#DC3545" stroke-width="11" stroke-linecap="round" stroke-dasharray="170 189" transform="rotate(-90 801 86)"/>
    <text x="801" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">90%</text>
  </g>

  <g transform="translate(52 472)">
    <rect x="0" y="0" width="908" height="154" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="132" height="154" rx="22" fill="#17A2B8"/>
    <rect x="100" y="0" width="32" height="154" fill="#17A2B8"/>
    <text x="66" y="66" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">Project C</text>
    <text x="66" y="91" width="104" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#E4F8FB">Client Rollout</text>
    <text x="158" y="36" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#6C757D">SUMMARY</text>
    <text x="158" y="62" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#212529">
      <tspan x="158" dy="0">Awaiting stakeholder feedback.</tspan><tspan x="158" dy="19">Development is 90% complete;</tspan><tspan x="158" dy="19">release readiness is high.</tspan>
    </text>
    <rect x="158" y="119" width="218" height="8" rx="4" fill="#E9ECEF"/>
    <rect x="158" y="119" width="196" height="8" rx="4" fill="#17A2B8"/>
    <rect x="420" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="489" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">STATUS TRACK</text>
    <circle cx="489" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="489" cy="86" r="30" fill="none" stroke="#FFC107" stroke-width="11" stroke-linecap="round" stroke-dasharray="170 189" transform="rotate(-90 489 86)"/>
    <text x="489" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">90%</text>
    <rect x="576" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="645" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">RISK ANALYSIS</text>
    <circle cx="645" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="645" cy="86" r="30" fill="none" stroke="#FD7E14" stroke-width="11" stroke-linecap="round" stroke-dasharray="28 189" transform="rotate(-90 645 86)"/>
    <text x="645" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">15%</text>
    <rect x="732" y="20" width="138" height="114" rx="18" fill="#F8F9FA"/>
    <text x="801" y="42" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#6C757D">RESOURCES</text>
    <circle cx="801" cy="86" r="30" fill="none" stroke="#E9ECEF" stroke-width="11"/>
    <circle cx="801" cy="86" r="30" fill="none" stroke="#DC3545" stroke-width="11" stroke-linecap="round" stroke-dasharray="170 189" transform="rotate(-90 801 86)"/>
    <text x="801" y="94" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#212529">90%</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Rendering donut charts as PNGs; use editable SVG circles with `stroke-dasharray` so the rings remain native PowerPoint shapes.
- ❌ Using `<mask>` or clipping non-image shapes to create card reveals; rounded `<rect>` panels are safer and translate cleanly.
- ❌ Putting `filter` on divider `<line>` elements; if shadows are needed, apply them only to cards, circles, paths, or text.
- ❌ Overloading every cell with equal-weight typography; the dashboard becomes unreadable if labels, percentages, and summaries all compete visually.
- ❌ Inheriting arrow markers or unsupported markers from parent groups; this dashboard does not need arrows, and marker behavior can be unreliable.

## Composition notes
- Keep the left 75% of the slide for project rows and reserve the right 18–20% for portfolio totals; this preserves a clear comparison zone plus an executive summary zone.
- Use one strong project color per row, but keep KPI colors consistent across rows: yellow for status, orange for risk, red for resources.
- Donut cells should be visually identical in size and spacing so differences in percentages are read instantly without layout noise.
- Preserve generous gutters between rows; the white space is what makes the dense project data feel executive rather than spreadsheet-like.