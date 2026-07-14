# SVG Recipe — Consulting-Style Scenario Comparison Chart

## Visual mechanism
A premium consulting scenario chart contrasts “business as usual” against a proposed accelerated future using two line trajectories, a highlighted divergence point, and a persuasive annotation. The visual story is built around the widening delta: muted baseline, urgent dashed upside case, translucent gain area, and one callout explaining the intervention.

## SVG primitives needed
- 2× `<rect>` for slide background and white chart card
- 6× `<line>` for horizontal gridlines
- 6× `<line>` for vertical year tick guides
- 2× `<path>` for the BAU and acceleration scenario lines
- 1× `<path>` for the translucent impact / delta area between scenarios
- 3× `<circle>` for data emphasis points and divergence highlight
- 1× `<rect>` for the callout box with rounded corners
- 1× `<line>` for the callout leader pointing to the divergence point
- 1× `<line>` plus cap lines for the end-state delta bracket
- Multiple `<text>` elements with explicit `width` attributes for title, labels, legend, axis labels, callout, and KPI annotations
- 2× `<linearGradient>` for background polish and delta fill
- 2× `<filter>` for card shadow and line glow, applied only to supported shapes/paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>
    <linearGradient id="deltaGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#C00000" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#C00000" stop-opacity="0.22"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="redGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="8" fill="#0B1F3A"/>

  <text x="70" y="58" width="860" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111827">
    Acceleration scenario unlocks +50% outcome by 2026
  </text>
  <text x="72" y="88" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    Scenario comparison vs. business as usual; Y-axis starts at zero for decision-grade integrity
  </text>

  <rect x="64" y="112" width="1152" height="535" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="92" y="132" width="1096" height="35" rx="12" fill="#F8FAFC"/>

  <circle cx="840" cy="149" r="6" fill="#0070C0"/>
  <text x="855" y="154" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">BAU baseline</text>
  <line x1="1000" y1="149" x2="1042" y2="149" stroke="#C00000" stroke-width="4" stroke-dasharray="10 7"/>
  <text x="1052" y="154" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#334155">Acceleration</text>

  <!-- Chart grid -->
  <line x1="140" y1="565" x2="1100" y2="565" stroke="#CBD5E1" stroke-width="1.5"/>
  <line x1="140" y1="481" x2="1100" y2="481" stroke="#E5E7EB" stroke-width="1"/>
  <line x1="140" y1="397" x2="1100" y2="397" stroke="#E5E7EB" stroke-width="1"/>
  <line x1="140" y1="313" x2="1100" y2="313" stroke="#E5E7EB" stroke-width="1"/>
  <line x1="140" y1="229" x2="1100" y2="229" stroke="#E5E7EB" stroke-width="1"/>
  <line x1="140" y1="145" x2="1100" y2="145" stroke="#E5E7EB" stroke-width="1"/>

  <line x1="160" y1="145" x2="160" y2="565" stroke="#F1F5F9" stroke-width="1"/>
  <line x1="340" y1="145" x2="340" y2="565" stroke="#F1F5F9" stroke-width="1"/>
  <line x1="520" y1="145" x2="520" y2="565" stroke="#F1F5F9" stroke-width="1"/>
  <line x1="700" y1="145" x2="700" y2="565" stroke="#F1F5F9" stroke-width="1"/>
  <line x1="880" y1="145" x2="880" y2="565" stroke="#F1F5F9" stroke-width="1"/>
  <line x1="1060" y1="145" x2="1060" y2="565" stroke="#F1F5F9" stroke-width="1"/>

  <!-- Axis labels -->
  <text x="82" y="570" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="end">0</text>
  <text x="82" y="486" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="end">3K</text>
  <text x="82" y="402" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="end">6K</text>
  <text x="82" y="318" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="end">9K</text>
  <text x="82" y="234" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="end">12K</text>
  <text x="82" y="150" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="end">15K</text>

  <text x="142" y="602" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">2021</text>
  <text x="322" y="602" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">2022</text>
  <text x="502" y="602" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">2023</text>
  <text x="682" y="602" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">2024</text>
  <text x="862" y="602" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">2025</text>
  <text x="1042" y="602" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">2026</text>

  <!-- Impact area and trajectories -->
  <path d="M520 481 L700 257 L880 215 L1060 145 L1060 285 L880 285 L700 341 L520 481 Z" fill="url(#deltaGrad)"/>
  <path d="M160 523 L340 495 L520 481 L700 341 L880 285 L1060 285" fill="none" stroke="#0070C0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M520 481 L700 257 L880 215 L1060 145" fill="none" stroke="#C00000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="13 9" filter="url(#redGlow)"/>

  <!-- Data emphasis -->
  <circle cx="520" cy="481" r="9" fill="#FFFFFF" stroke="#111827" stroke-width="3"/>
  <circle cx="1060" cy="285" r="7" fill="#FFFFFF" stroke="#0070C0" stroke-width="3"/>
  <circle cx="1060" cy="145" r="8" fill="#FFFFFF" stroke="#C00000" stroke-width="3"/>

  <!-- Divergence callout -->
  <rect x="250" y="205" width="310" height="102" rx="16" fill="#FFF1F1" stroke="#F2B8B8" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="273" y="235" width="265" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#991B1B">
    Intervention begins in 2023
  </text>
  <text x="273" y="263" width="258" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7F1D1D">
    Additional $100K investment in product marketing shifts the growth curve.
  </text>
  <line x1="405" y1="307" x2="512" y2="472" stroke="#991B1B" stroke-width="2" stroke-dasharray="6 5"/>

  <!-- End-state delta bracket -->
  <line x1="1124" y1="145" x2="1124" y2="285" stroke="#C00000" stroke-width="2"/>
  <line x1="1108" y1="145" x2="1140" y2="145" stroke="#C00000" stroke-width="2"/>
  <line x1="1108" y1="285" x2="1140" y2="285" stroke="#C00000" stroke-width="2"/>
  <rect x="1148" y="186" width="74" height="52" rx="12" fill="#C00000"/>
  <text x="1160" y="208" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">+5K</text>
  <text x="1160" y="226" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#FEE2E2">impact</text>

  <text x="930" y="124" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#94A3B8" text-anchor="end">Units / revenue indexed</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use native `<marker>` arrowheads for the callout leader; marker-end on paths may disappear. Use a plain `<line>` or draw a small triangle manually if an arrow is essential.
- ❌ Do not apply filters to `<line>` elements; shadows/glows on lines are dropped. Apply glow to the scenario `<path>` instead.
- ❌ Do not crop or mask non-image elements for the delta area; use a closed `<path>` polygon for the impact region.
- ❌ Do not omit explicit `width` on chart labels and annotations; PowerPoint text rendering depends on these widths.
- ❌ Do not exaggerate the Y-axis by starting above zero; this chart’s persuasive credibility relies on honest axis scaling.

## Composition notes
- Give the chart 70–80% of the slide and keep title/subtitle compact; the comparison lines should be the hero.
- Place the callout near the divergence point, not at the end-state result, so the audience connects action to outcome.
- Use muted blue for the baseline and urgent red for the proposed scenario; reserve red fill/glow only for the acceleration story.
- Add a translucent delta region and end-state bracket to quantify the opportunity cost without cluttering the plot.