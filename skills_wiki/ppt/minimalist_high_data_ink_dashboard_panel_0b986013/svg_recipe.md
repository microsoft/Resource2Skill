# SVG Recipe — Minimalist "High Data-Ink" Dashboard Panel

## Visual mechanism
A quiet dashboard shell uses whitespace, crisp typography, and almost-invisible scaffolding so the viewer reads the data—not the container. The main chart removes spines, tick marks, borders, and heavy fills, leaving only pale horizontal reference lines and a strong accent data path.

## SVG primitives needed
- 2× `<rect>` for the light-gray slide canvas and white dashboard panel
- 1× `<filter id="panelShadow">` applied only to the main panel for a barely perceptible elevation
- 1× `<linearGradient id="areaFade">` for the subtle under-line chart fill
- 6× `<line>` for horizontal chart gridlines and the faint x-axis baseline
- 1× `<path>` for the low-opacity area under the time-series line
- 1× `<path>` for the primary editable time-series stroke
- 1× `<circle>` for the final highlighted data point
- 1× `<rect>` for the small latest-value callout chip
- 30+× `<text>` for dashboard title, KPI labels, KPI values, deltas, chart labels, and month labels
- 3× `<line>` for faint KPI column separators

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="areaFade" x1="0" y1="360" x2="0" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2B5B84" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#2B5B84" stop-opacity="0.00"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F6F8"/>
  <rect x="64" y="48" width="1152" height="624" rx="22" fill="#FFFFFF" filter="url(#panelShadow)"/>

  <text x="96" y="92" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#212529">Quarterly Performance Dashboard</text>
  <text x="96" y="121" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="500" fill="#6C757D">Executive summary · trailing twelve months · USD in thousands</text>
  <text x="1076" y="95" width="100" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#6C757D">FY 2026</text>
  <text x="1076" y="120" width="100" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#212529">Q4 Close</text>

  <text x="96" y="178" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" letter-spacing="1.3" fill="#6C757D">REVENUE</text>
  <text x="96" y="223" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#212529">$8.42M</text>
  <text x="96" y="253" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#28A745">▲ 18.2% vs last period</text>

  <line x1="354" y1="166" x2="354" y2="260" stroke="#EEF0F2" stroke-width="1"/>

  <text x="392" y="178" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" letter-spacing="1.3" fill="#6C757D">GROSS MARGIN</text>
  <text x="392" y="223" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#212529">64.8%</text>
  <text x="392" y="253" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#28A745">▲ 3.1 pts expansion</text>

  <line x1="650" y1="166" x2="650" y2="260" stroke="#EEF0F2" stroke-width="1"/>

  <text x="688" y="178" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" letter-spacing="1.3" fill="#6C757D">NET RETENTION</text>
  <text x="688" y="223" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#212529">119%</text>
  <text x="688" y="253" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#28A745">▲ 6 pts year over year</text>

  <line x1="946" y1="166" x2="946" y2="260" stroke="#EEF0F2" stroke-width="1"/>

  <text x="984" y="178" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" letter-spacing="1.3" fill="#6C757D">CAC PAYBACK</text>
  <text x="984" y="223" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#212529">9.4 mo</text>
  <text x="984" y="253" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#28A745">▼ 1.8 mo improvement</text>

  <text x="96" y="321" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#212529">Recurring revenue run-rate</text>
  <text x="96" y="344" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="500" fill="#6C757D">Minimal axis treatment: no chart border, no tick marks, no vertical grid.</text>

  <text x="92" y="382" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#9AA0A6">$900K</text>
  <line x1="150" y1="378" x2="1130" y2="378" stroke="#F0F2F4" stroke-width="1.2"/>

  <text x="92" y="432" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#9AA0A6">$800K</text>
  <line x1="150" y1="428" x2="1130" y2="428" stroke="#F0F2F4" stroke-width="1.2"/>

  <text x="92" y="482" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#9AA0A6">$700K</text>
  <line x1="150" y1="478" x2="1130" y2="478" stroke="#F0F2F4" stroke-width="1.2"/>

  <text x="92" y="532" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#9AA0A6">$600K</text>
  <line x1="150" y1="528" x2="1130" y2="528" stroke="#F0F2F4" stroke-width="1.2"/>

  <text x="92" y="582" width="48" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#9AA0A6">$500K</text>
  <line x1="150" y1="578" x2="1130" y2="578" stroke="#DDE1E5" stroke-width="1.4"/>

  <path d="M150 558 C190 548 220 540 238 536 C282 526 310 510 326 498 C366 468 398 492 414 478 C452 448 486 456 502 444 C544 414 574 430 590 416 C630 384 662 402 678 390 C718 358 750 374 766 362 C806 334 838 352 854 340 C896 310 926 330 942 318 C986 286 1022 302 1030 292 C1074 264 1102 286 1118 272 L1118 578 L150 578 Z" fill="url(#areaFade)"/>
  <path d="M150 558 C190 548 220 540 238 536 C282 526 310 510 326 498 C366 468 398 492 414 478 C452 448 486 456 502 444 C544 414 574 430 590 416 C630 384 662 402 678 390 C718 358 750 374 766 362 C806 334 838 352 854 340 C896 310 926 330 942 318 C986 286 1022 302 1030 292 C1074 264 1102 286 1118 272" fill="none" stroke="#2B5B84" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="1118" cy="272" r="6.5" fill="#2B5B84"/>
  <rect x="1048" y="232" width="92" height="28" rx="14" fill="#EDF4FA"/>
  <text x="1094" y="251" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" fill="#2B5B84">$842K</text>

  <text x="150" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Jan</text>
  <text x="238" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Feb</text>
  <text x="326" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Mar</text>
  <text x="414" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Apr</text>
  <text x="502" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">May</text>
  <text x="590" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Jun</text>
  <text x="678" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Jul</text>
  <text x="766" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Aug</text>
  <text x="854" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Sep</text>
  <text x="942" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Oct</text>
  <text x="1030" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Nov</text>
  <text x="1118" y="616" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A9097">Dec</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy panel borders, boxed chart areas, axis spines on all four sides, or visible tick marks; these lower the data-ink ratio.
- ❌ Decorative icons beside every KPI; they compete with the numeric hierarchy.
- ❌ Saturated multi-color palettes for a single-series dashboard; reserve one accent color for the actual data.
- ❌ Vertical gridlines unless they encode a meaningful interval; they usually add clutter without improving comprehension.
- ❌ Rasterized chart screenshots when editable SVG paths and text can preserve premium PowerPoint editability.

## Composition notes
- Keep the top third for KPI scanning and the lower half for one dominant chart; do not crowd the chart with legends or side panels.
- Use pale gray infrastructure: gridlines should be visible only after the main data line has been noticed.
- Let the accent blue appear in exactly three places: the line, its subtle area fill, and the latest-value callout.
- Maintain wide left/right margins and generous row spacing so the absence of decoration feels intentional, not unfinished.