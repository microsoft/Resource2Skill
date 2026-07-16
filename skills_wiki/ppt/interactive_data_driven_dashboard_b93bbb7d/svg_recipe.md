# SVG Recipe — Modern KPI Dashboard

## Visual mechanism
A dark executive dashboard is built from softly rounded modular panels, each containing a distinct KPI visualization: oversized numeric cards, donut progress, compact bar charts, a gauge, and a wide Gantt timeline. High-contrast cyan, gold, green, and red accents sit on charcoal surfaces to make data feel live, structured, and immediately scannable.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 6× `<rect>` for rounded dashboard panels with subtle gradient fills
- Multiple `<rect>` for KPI icon chips, progress tracks, bar charts, Gantt rows, status pills, and timeline blocks
- Multiple `<circle>` for donut charts, KPI icon dots, gauge hub, and small status indicators
- Multiple `<path>` for gauge arc segments and small decorative trend sparklines
- Multiple `<line>` for chart axes, tick marks, and gauge needle
- Multiple `<text>` with explicit `width` for title, KPI values, labels, percentages, legends, axes, and annotations
- 2× `<linearGradient>` for the slide background and panel surface treatment
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` for soft card depth
- 1× `<filter id="cyanGlow">` using `feGaussianBlur` for subtle accent glow on active KPI elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#202327"/>
      <stop offset="55%" stop-color="#2D3033"/>
      <stop offset="100%" stop-color="#181B1F"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3D4248"/>
      <stop offset="100%" stop-color="#32363B"/>
    </linearGradient>
    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="44" y="42" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="700" fill="#F4F7FA">Project Performance Dashboard</text>
  <text x="44" y="70" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9EA8B3">Executive snapshot · Q3 delivery portfolio · Updated 09:30</text>
  <rect x="1030" y="32" width="200" height="34" rx="17" fill="#263038" stroke="#49525B"/>
  <circle cx="1052" cy="49" r="5" fill="#35D07F"/>
  <text x="1066" y="54" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#DCE7EF">Live data snapshot</text>

  <rect x="40" y="100" width="205" height="125" rx="20" fill="url(#panelGrad)" filter="url(#panelShadow)"/>
  <rect x="60" y="120" width="38" height="38" rx="12" fill="#123A4A"/>
  <circle cx="79" cy="139" r="10" fill="#00B0F0" filter="url(#cyanGlow)"/>
  <text x="112" y="134" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AAB4BF">Completion</text>
  <text x="60" y="190" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF">78%</text>
  <text x="160" y="192" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#35D07F">▲ 6.4%</text>

  <rect x="40" y="245" width="205" height="125" rx="20" fill="url(#panelGrad)" filter="url(#panelShadow)"/>
  <rect x="60" y="265" width="38" height="38" rx="12" fill="#3F3021"/>
  <circle cx="79" cy="284" r="10" fill="#FFC000"/>
  <text x="112" y="279" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AAB4BF">Open Risks</text>
  <text x="60" y="335" width="115" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF">14</text>
  <text x="146" y="337" width="75" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FF6B6B">● 3 critical</text>

  <rect x="270" y="100" width="285" height="270" rx="22" fill="url(#panelGrad)" filter="url(#panelShadow)"/>
  <text x="295" y="134" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#F4F7FA">Budget utilization</text>
  <text x="295" y="155" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA8B3">Spend vs approved allocation</text>
  <circle cx="412" cy="240" r="74" fill="none" stroke="#242A30" stroke-width="24"/>
  <circle cx="412" cy="240" r="74" fill="none" stroke="#00B0F0" stroke-width="24" stroke-linecap="round" stroke-dasharray="344 465" transform="rotate(-90 412 240)" filter="url(#cyanGlow)"/>
  <circle cx="412" cy="240" r="43" fill="#32363B"/>
  <text x="365" y="246" width="94" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF" text-anchor="middle">74%</text>
  <text x="330" y="305" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#BAC4CC" text-anchor="middle">$2.8M of $3.8M committed</text>
  <rect x="313" y="330" width="22" height="8" rx="4" fill="#00B0F0"/>
  <text x="342" y="338" width="75" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AAB4BF">Spent</text>
  <rect x="420" y="330" width="22" height="8" rx="4" fill="#242A30"/>
  <text x="449" y="338" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AAB4BF">Remaining</text>

  <rect x="575" y="100" width="330" height="270" rx="22" fill="url(#panelGrad)" filter="url(#panelShadow)"/>
  <text x="600" y="134" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#F4F7FA">Workload by team</text>
  <text x="600" y="155" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA8B3">Capacity consumed this sprint</text>
  <line x1="640" y1="315" x2="850" y2="315" stroke="#59616A" stroke-width="1"/>
  <text x="600" y="200" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CED6DD">Design</text>
  <rect x="670" y="187" width="170" height="18" rx="9" fill="#242A30"/>
  <rect x="670" y="187" width="126" height="18" rx="9" fill="#00B0F0"/>
  <text x="850" y="201" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#F4F7FA">74%</text>
  <text x="600" y="238" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CED6DD">Build</text>
  <rect x="670" y="225" width="170" height="18" rx="9" fill="#242A30"/>
  <rect x="670" y="225" width="151" height="18" rx="9" fill="#35D07F"/>
  <text x="850" y="239" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#F4F7FA">89%</text>
  <text x="600" y="276" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CED6DD">QA</text>
  <rect x="670" y="263" width="170" height="18" rx="9" fill="#242A30"/>
  <rect x="670" y="263" width="94" height="18" rx="9" fill="#FFC000"/>
  <text x="850" y="277" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#F4F7FA">55%</text>
  <text x="600" y="338" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA8B3">Peak pressure in engineering; QA buffer remains available.</text>

  <rect x="925" y="100" width="315" height="270" rx="22" fill="url(#panelGrad)" filter="url(#panelShadow)"/>
  <text x="950" y="134" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#F4F7FA">Delivery confidence</text>
  <text x="950" y="155" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA8B3">Composite risk-adjusted gauge</text>
  <path d="M 982 265 A 94 94 0 0 1 1009 198" fill="none" stroke="#00B0F0" stroke-width="24" stroke-linecap="round"/>
  <path d="M 1009 198 A 94 94 0 0 1 1083 171" fill="none" stroke="#35D07F" stroke-width="24" stroke-linecap="round"/>
  <path d="M 1083 171 A 94 94 0 0 1 1157 198" fill="none" stroke="#FFC000" stroke-width="24" stroke-linecap="round"/>
  <path d="M 1157 198 A 94 94 0 0 1 1184 265" fill="none" stroke="#FF4E50" stroke-width="24" stroke-linecap="round"/>
  <line x1="1083" y1="265" x2="1136" y2="205" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <circle cx="1083" cy="265" r="12" fill="#FFFFFF"/>
  <text x="1044" y="310" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">68</text>
  <text x="1050" y="337" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#AAB4BF" text-anchor="middle">moderate</text>

  <rect x="40" y="395" width="1200" height="280" rx="24" fill="url(#panelGrad)" filter="url(#panelShadow)"/>
  <text x="70" y="430" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F4F7FA">Milestone timeline</text>
  <text x="70" y="452" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9EA8B3">Stacked Gantt view with current-date marker and risk tags</text>
  <line x1="250" y1="490" x2="1160" y2="490" stroke="#59616A" stroke-width="1"/>
  <line x1="250" y1="490" x2="250" y2="630" stroke="#59616A" stroke-width="1"/>
  <text x="245" y="474" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AAB4BF">Jul</text>
  <text x="475" y="474" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AAB4BF">Aug</text>
  <text x="705" y="474" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AAB4BF">Sep</text>
  <text x="935" y="474" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AAB4BF">Oct</text>
  <line x1="790" y1="478" x2="790" y2="640" stroke="#00B0F0" stroke-width="2" stroke-dasharray="5 7"/>
  <text x="800" y="645" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#00B0F0">Today</text>
  <text x="70" y="515" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7EF">Discovery</text>
  <rect x="265" y="502" width="225" height="18" rx="9" fill="#00B0F0"/>
  <rect x="500" y="502" width="64" height="18" rx="9" fill="#35D07F"/>
  <text x="70" y="555" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7EF">Platform build</text>
  <rect x="390" y="542" width="390" height="18" rx="9" fill="#00B0F0"/>
  <rect x="792" y="542" width="86" height="18" rx="9" fill="#FFC000"/>
  <text x="70" y="595" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7EF">Pilot rollout</text>
  <rect x="690" y="582" width="270" height="18" rx="9" fill="#35D07F"/>
  <rect x="970" y="582" width="72" height="18" rx="9" fill="#FF4E50"/>
  <text x="70" y="635" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7EF">Executive launch</text>
  <rect x="930" y="622" width="190" height="18" rx="9" fill="#00B0F0"/>
  <rect x="1128" y="618" width="54" height="26" rx="13" fill="#3F3021" stroke="#FFC000"/>
  <text x="1140" y="636" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFC000">RISK</text>
</svg>
```

## Avoid in this skill
- ❌ Embedding bitmap screenshots of charts when the same effect can be built from editable SVG rectangles, circles, paths, and text
- ❌ Using `<foreignObject>` for tables or KPI cards; it will hard-fail and also prevents native PowerPoint editing
- ❌ Applying `filter` to `<line>` elements for glowing axes or needles; use glow on nearby circles/paths/rectangles instead
- ❌ Using `marker-end` on Gantt connectors or arrows; if arrows are needed, draw them manually with `<line>` plus small triangular `<path>`
- ❌ Overloading the dashboard with too many chart panels; the premium look depends on generous padding and clear module hierarchy

## Composition notes
- Keep the slide on a strict modular grid: small KPI cards at left/top, analytical widgets across the top row, and one wide narrative chart along the bottom.
- Use charcoal panels with 20–24 px corner radius; reserve saturated colors only for data marks, status tags, and key percentages.
- KPI numbers should be oversized and high-contrast, while chart labels stay compact and muted to avoid visual noise.
- Leave consistent internal padding inside every panel, especially around donut and gauge charts, so the dashboard feels executive rather than cramped.