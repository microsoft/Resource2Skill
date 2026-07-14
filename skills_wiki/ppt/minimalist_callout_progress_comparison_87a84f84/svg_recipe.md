# SVG Recipe — Minimalist Callout Progress Comparison

## Visual mechanism
A stripped-down comparison chart uses long, quiet horizontal tracks and short bursts of saturated color to show progress. The signature detail is a floating geometric callout bubble pinned to each bar endpoint, making the percentage feel physically attached to the metric.

## SVG primitives needed
- 1× `<rect>` for the pure white slide background
- 1× `<rect>` for a very pale right-column chart panel
- 3× `<rect>` for light-gray rounded progress tracks
- 3× `<rect>` for colored rounded progress fills
- 15× `<line>` for subtle segment ticks across the tracks
- 3× `<path>` for merged speech-bubble callouts with triangular pointers
- 11× `<text>` for title, subtitle, row labels, row descriptions, and percentage values
- 3× `<linearGradient>` for polished colored bar/callout fills
- 1× `<filter id="bubbleShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for soft depth on callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E9575F"/>
      <stop offset="100%" stop-color="#D63B41"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#65C4AA"/>
      <stop offset="100%" stop-color="#4BAC8F"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5FA3DA"/>
      <stop offset="100%" stop-color="#3F88C5"/>
    </linearGradient>
    <filter id="bubbleShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="440" y="178" width="760" height="410" rx="28" fill="#FAFAFA"/>

  <text x="0" y="70" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" letter-spacing="1.5" fill="#323232">
    MINIMALIST PROGRESS COMPARISON
  </text>
  <text x="0" y="112" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#969696">
    Clean callout labels attached directly to each progress endpoint
  </text>

  <!-- Row 1 left copy -->
  <text x="94" y="252" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" letter-spacing="1" fill="#D63B41">
    MARKET READINESS
  </text>
  <text x="94" y="286" width="305" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    <tspan x="94" dy="0">Core launch assets are complete,</tspan>
    <tspan x="94" dy="22">with final regional adaptations</tspan>
    <tspan x="94" dy="22">now entering approval.</tspan>
  </text>

  <!-- Row 1 track -->
  <rect x="500" y="286" width="660" height="14" rx="7" fill="#EDEDED"/>
  <rect x="500" y="286" width="541" height="14" rx="7" fill="url(#redGrad)"/>
  <line x1="632" y1="279" x2="632" y2="307" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="764" y1="279" x2="764" y2="307" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="896" y1="279" x2="896" y2="307" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="1028" y1="279" x2="1028" y2="307" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="1160" y1="279" x2="1160" y2="307" stroke="#D4D4D4" stroke-width="1"/>
  <path filter="url(#bubbleShadow)" fill="url(#redGrad)" d="M995 224 H1087 Q1097 224 1097 234 V264 Q1097 274 1087 274 H1059 L1041 292 L1023 274 H995 Q985 274 985 264 V234 Q985 224 995 224 Z"/>
  <text x="985" y="257" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">82%</text>

  <!-- Row 2 left copy -->
  <text x="94" y="376" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" letter-spacing="1" fill="#4BAC8F">
    PRODUCT QUALITY
  </text>
  <text x="94" y="410" width="305" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    <tspan x="94" dy="0">Customer validation is trending</tspan>
    <tspan x="94" dy="22">positive, while defect burn-down</tspan>
    <tspan x="94" dy="22">continues across priority flows.</tspan>
  </text>

  <!-- Row 2 track -->
  <rect x="500" y="410" width="660" height="14" rx="7" fill="#EDEDED"/>
  <rect x="500" y="410" width="363" height="14" rx="7" fill="url(#tealGrad)"/>
  <line x1="632" y1="403" x2="632" y2="431" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="764" y1="403" x2="764" y2="431" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="896" y1="403" x2="896" y2="431" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="1028" y1="403" x2="1028" y2="431" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="1160" y1="403" x2="1160" y2="431" stroke="#D4D4D4" stroke-width="1"/>
  <path filter="url(#bubbleShadow)" fill="url(#tealGrad)" d="M817 348 H909 Q919 348 919 358 V388 Q919 398 909 398 H881 L863 416 L845 398 H817 Q807 398 807 388 V358 Q807 348 817 348 Z"/>
  <text x="807" y="381" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">55%</text>

  <!-- Row 3 left copy -->
  <text x="94" y="500" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" letter-spacing="1" fill="#3F88C5">
    SALES ENABLEMENT
  </text>
  <text x="94" y="534" width="305" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    <tspan x="94" dy="0">Training content is drafted,</tspan>
    <tspan x="94" dy="22">but field readiness depends on</tspan>
    <tspan x="94" dy="22">final demo environment access.</tspan>
  </text>

  <!-- Row 3 track -->
  <rect x="500" y="534" width="660" height="14" rx="7" fill="#EDEDED"/>
  <rect x="500" y="534" width="251" height="14" rx="7" fill="url(#blueGrad)"/>
  <line x1="632" y1="527" x2="632" y2="555" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="764" y1="527" x2="764" y2="555" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="896" y1="527" x2="896" y2="555" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="1028" y1="527" x2="1028" y2="555" stroke="#D4D4D4" stroke-width="1"/>
  <line x1="1160" y1="527" x2="1160" y2="555" stroke="#D4D4D4" stroke-width="1"/>
  <path filter="url(#bubbleShadow)" fill="url(#blueGrad)" d="M705 472 H797 Q807 472 807 482 V512 Q807 522 797 522 H769 L751 540 L733 522 H705 Q695 522 695 512 V482 Q695 472 705 472 Z"/>
  <text x="695" y="505" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">38%</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy chart furniture such as axes, legends, grid boxes, or numeric scales; the callout endpoint should carry the value.
- ❌ `<marker-end>` arrowheads for indicating progress direction; they are unnecessary and may disappear in translation.
- ❌ Applying filters to tick `<line>` elements; keep shadows only on the callout `<path>` shapes.
- ❌ Clipping or masking non-image shapes to create the callout; use a single editable `<path>` instead.
- ❌ Too many rows; this style works best with 3–5 metrics so the bars have enough horizontal runway.

## Composition notes
- Reserve roughly the left third for metric names and explanatory copy; reserve the right two-thirds for long progress tracks.
- Keep the background mostly white, with only a very pale chart panel if extra separation is needed.
- Align each callout’s triangular pointer to the exact end of the colored bar for visual credibility.
- Use one vivid accent per row, repeated in the row title, bar fill, and callout bubble for fast visual association.