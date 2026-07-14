# SVG Recipe — Clean & Modern KPI Dashboard

## Visual mechanism
A single-slide executive dashboard built from aligned KPI cards: each widget combines a large metric, a semicircular gauge, a status color, and small supporting breakdown bars. The design feels modern because it uses disciplined spacing, restrained color, soft card separation, and consistent typography.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 3× `<rect>` for elevated KPI card containers with rounded corners.
- 3× `<path>` for pale semicircular gauge tracks.
- 3× `<path>` for colored gauge progress arcs.
- 3× `<circle>` for status icon disks inside the gauges.
- Multiple `<ellipse>` and `<path>` elements for simple editable facial/status icons.
- 6× `<rect>` for compact target/status pill labels.
- 9× `<rect>` for segmented mini breakdown bars under each KPI.
- Multiple `<text>` elements with explicit `width` attributes for title, metric values, subtitles, labels, and annotations.
- 1× `<linearGradient>` for the soft page background.
- 1× `<linearGradient>` for the teal accent rule.
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge`, applied only to card rectangles.
- 1× `<filter id="softGlow">` using `feGaussianBlur`, applied to colored gauge paths for premium emphasis.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFC"/>
      <stop offset="100%" stop-color="#EEF5F6"/>
    </linearGradient>
    <linearGradient id="tealRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00A99D"/>
      <stop offset="100%" stop-color="#7ED321"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="58" y="83" width="1164" height="6" rx="3" fill="url(#tealRule)"/>
  <text x="60" y="54" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2E3438">Customer Satisfaction Dashboard</text>
  <text x="880" y="52" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#7A868C" text-anchor="end">Q3 Executive KPI Snapshot</text>

  <rect x="60" y="126" width="340" height="510" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="420" y="126" width="340" height="510" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="780" y="126" width="340" height="510" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <text x="92" y="172" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#4A4A4A">Net Promoter Score</text>
  <rect x="302" y="148" width="66" height="28" rx="14" fill="#D0021B"/>
  <text x="315" y="168" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">Alert</text>
  <text x="92" y="213" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#2E3438">NPS = 25</text>
  <text x="92" y="241" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8A9499">Target: greater than 50</text>
  <path d="M 110 358 A 120 120 0 0 1 350 358" fill="none" stroke="#E6EAED" stroke-width="30" stroke-linecap="round"/>
  <path d="M 110 358 A 120 120 0 0 1 145 273" fill="none" stroke="#D0021B" stroke-width="30" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="230" cy="340" r="55" fill="#D0021B"/>
  <ellipse cx="210" cy="325" rx="6" ry="8" fill="#FFFFFF"/>
  <ellipse cx="250" cy="325" rx="6" ry="8" fill="#FFFFFF"/>
  <path d="M 200 365 A 35 24 0 0 1 260 365" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <rect x="92" y="462" width="244" height="12" rx="6" fill="#EEF1F3"/>
  <rect x="92" y="462" width="62" height="12" rx="6" fill="#D0021B"/>
  <rect x="158" y="462" width="74" height="12" rx="6" fill="#F5A623"/>
  <rect x="236" y="462" width="100" height="12" rx="6" fill="#00A99D"/>
  <text x="92" y="505" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Detractors</text>
  <text x="184" y="505" width="75" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Passives</text>
  <text x="266" y="505" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Promoters</text>
  <text x="92" y="560" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#4A4A4A">Primary risk: low advocacy after support interactions.</text>

  <text x="452" y="172" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#4A4A4A">Customer Satisfaction</text>
  <rect x="662" y="148" width="66" height="28" rx="14" fill="#F5A623"/>
  <text x="695" y="168" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">Good</text>
  <text x="452" y="213" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#2E3438">CSAT 82%</text>
  <text x="452" y="241" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8A9499">Target: 80% or higher</text>
  <path d="M 470 358 A 120 120 0 0 1 710 358" fill="none" stroke="#E6EAED" stroke-width="30" stroke-linecap="round"/>
  <path d="M 470 358 A 120 120 0 0 1 691 294" fill="none" stroke="#F5A623" stroke-width="30" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="590" cy="340" r="55" fill="#F5A623"/>
  <ellipse cx="570" cy="325" rx="6" ry="8" fill="#FFFFFF"/>
  <ellipse cx="610" cy="325" rx="6" ry="8" fill="#FFFFFF"/>
  <path d="M 560 350 A 35 28 0 0 0 620 350" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <rect x="452" y="462" width="244" height="12" rx="6" fill="#EEF1F3"/>
  <rect x="452" y="462" width="200" height="12" rx="6" fill="#F5A623"/>
  <rect x="656" y="462" width="40" height="12" rx="6" fill="#D8DEE2"/>
  <text x="452" y="505" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Satisfied</text>
  <text x="566" y="505" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Neutral</text>
  <text x="640" y="505" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Unsatisfied</text>
  <text x="452" y="560" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#4A4A4A">Satisfaction remains above target with room to improve onboarding.</text>

  <text x="812" y="172" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#4A4A4A">Customer Effort Score</text>
  <rect x="1022" y="148" width="66" height="28" rx="14" fill="#7ED321"/>
  <text x="1055" y="168" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">On track</text>
  <text x="812" y="213" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#2E3438">CES 68</text>
  <text x="812" y="241" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8A9499">Target: less effort month-over-month</text>
  <path d="M 830 358 A 120 120 0 0 1 1070 358" fill="none" stroke="#E6EAED" stroke-width="30" stroke-linecap="round"/>
  <path d="M 830 358 A 120 120 0 0 1 1014 257" fill="none" stroke="#7ED321" stroke-width="30" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="950" cy="340" r="55" fill="#7ED321"/>
  <ellipse cx="930" cy="325" rx="6" ry="8" fill="#FFFFFF"/>
  <ellipse cx="970" cy="325" rx="6" ry="8" fill="#FFFFFF"/>
  <path d="M 920 352 L 980 352" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <rect x="812" y="462" width="244" height="12" rx="6" fill="#EEF1F3"/>
  <rect x="812" y="462" width="166" height="12" rx="6" fill="#7ED321"/>
  <rect x="982" y="462" width="74" height="12" rx="6" fill="#D8DEE2"/>
  <text x="812" y="505" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Easy</text>
  <text x="900" y="505" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Moderate</text>
  <text x="1002" y="505" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A868C">Hard</text>
  <text x="812" y="560" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#4A4A4A">Self-service improvements are reducing customer effort.</text>
</svg>
```

## Avoid in this skill
- ❌ Using standard pie charts or dense axes; the technique depends on fast-read KPI widgets, not analytical chart complexity.
- ❌ Applying filters to `<line>` elements; use shadows only on card `<rect>` or glow on gauge `<path>`.
- ❌ Building gauges as raster screenshots; editable `<path>` arcs translate better and allow later recoloring in PowerPoint.
- ❌ Relying on `<textPath>` for curved labels around gauges; keep labels as normal editable `<text>`.
- ❌ Overcrowding each card with too many numbers; each widget should have one hero value, one target/status cue, and one short insight.

## Composition notes
- Keep the layout in a strict three-column grid with equal card widths, equal gutters, and generous top/bottom margins.
- Put the dashboard title above the grid; reserve the card centers for gauges and the bottom third for short breakdown bars plus a concise interpretation.
- Use one dominant neutral text color, one light gray gauge track, and status colors only where they communicate performance.
- The strongest visual focus should be the three gauge centers and their large metric values; supporting labels should remain small and subdued.