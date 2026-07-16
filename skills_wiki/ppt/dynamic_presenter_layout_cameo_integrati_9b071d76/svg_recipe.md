# SVG Recipe — Dynamic Presenter Layout (Cameo Integration Mockup)

## Visual mechanism
A dark executive data slide is split between a declining revenue chart and a “live presenter” cameo clipped into a dramatic downward arrow. The presenter shape is integrated into the narrative with a hot red-orange glow, crisp border, and semi-transparent lower-third name tag.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 1× `<radialGradient>` for subtle background illumination behind the presenter
- 1× `<linearGradient>` for chart area tinting
- 1× `<clipPath>` with a custom `<path>` for the arrow-shaped presenter crop
- 1× `<image>` for the presenter portrait clipped to the arrow geometry
- 3× duplicate `<path>` shapes for presenter glow, dark underlay, and border
- 1× `<filter id="orangeGlow">` applied to the arrow silhouette
- 1× `<filter id="softShadow">` applied to cards and name tag
- Multiple `<line>` elements for chart axes, gridlines, and tick marks
- 1× `<path>` for the declining revenue line
- 1× `<circle>` for the highlighted final data point
- Several `<rect>` elements for chart panel, label pills, and translucent name tag
- Multiple `<text>` elements with explicit `width` attributes for title, labels, axis values, presenter name, role, and footer copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="78%" cy="45%" r="48%">
      <stop offset="0%" stop-color="#3a1010" stop-opacity="0.70"/>
      <stop offset="45%" stop-color="#151923" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#11151f" stop-opacity="1"/>
    </radialGradient>

    <linearGradient id="chartPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#202637" stop-opacity="0.90"/>
      <stop offset="100%" stop-color="#11151f" stop-opacity="0.35"/>
    </linearGradient>

    <linearGradient id="orangeLine" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffb347"/>
      <stop offset="55%" stop-color="#ff8c00"/>
      <stop offset="100%" stop-color="#ff4500"/>
    </linearGradient>

    <filter id="orangeGlow" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="18" result="blur1"/>
      <feGaussianBlur in="SourceAlpha" stdDeviation="34" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="presenterArrowClip">
      <path d="M940 146 H1118 Q1156 146 1156 184 V384 H1218 L1030 568 L842 384 H904 V184 Q904 146 940 146 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <text x="640" y="64" width="920" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800"
        letter-spacing="3" fill="#ffffff">REVENUE UPDATE</text>

  <text x="640" y="104" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        letter-spacing="1.6" fill="#9da6b8">Q3 PERFORMANCE SNAPSHOT · EXECUTIVE BRIEFING</text>

  <rect x="58" y="138" width="730" height="468" rx="26" fill="url(#chartPanel)" stroke="#2f384a" stroke-width="1.5" filter="url(#softShadow)"/>
  <rect x="86" y="164" width="174" height="34" rx="17" fill="#ff8c00" opacity="0.14" stroke="#ff8c00" stroke-opacity="0.45"/>
  <text x="104" y="187" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#ffb15c">MONTHLY REVENUE</text>

  <line x1="145" y1="520" x2="720" y2="520" stroke="#6b7280" stroke-width="1"/>
  <line x1="145" y1="218" x2="145" y2="520" stroke="#6b7280" stroke-width="1"/>
  <line x1="145" y1="460" x2="720" y2="460" stroke="#333b4d" stroke-width="1"/>
  <line x1="145" y1="400" x2="720" y2="400" stroke="#333b4d" stroke-width="1"/>
  <line x1="145" y1="340" x2="720" y2="340" stroke="#333b4d" stroke-width="1"/>
  <line x1="145" y1="280" x2="720" y2="280" stroke="#333b4d" stroke-width="1"/>
  <line x1="145" y1="220" x2="720" y2="220" stroke="#333b4d" stroke-width="1"/>

  <text x="82" y="525" width="52" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#9aa3b5">$0M</text>
  <text x="82" y="465" width="52" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#9aa3b5">$20M</text>
  <text x="82" y="405" width="52" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#9aa3b5">$40M</text>
  <text x="82" y="345" width="52" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#9aa3b5">$60M</text>
  <text x="82" y="285" width="52" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#9aa3b5">$80M</text>

  <path d="M145 255 C210 260 238 270 300 278 C350 286 382 318 430 385 C472 442 514 456 560 470 C614 486 660 498 720 510"
        fill="none" stroke="url(#orangeLine)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M145 255 C210 260 238 270 300 278 C350 286 382 318 430 385 C472 442 514 456 560 470 C614 486 660 498 720 510"
        fill="none" stroke="#ff8c00" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" opacity="0.12"/>

  <circle cx="720" cy="510" r="11" fill="#ff4500" stroke="#ffd0bb" stroke-width="4"/>
  <circle cx="720" cy="510" r="24" fill="#ff4500" opacity="0.16"/>

  <text x="125" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8d96a8">FEB</text>
  <text x="225" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8d96a8">MAR</text>
  <text x="325" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8d96a8">APR</text>
  <text x="425" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8d96a8">MAY</text>
  <text x="525" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8d96a8">JUN</text>
  <text x="625" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8d96a8">JUL</text>
  <text x="715" y="556" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#ffb15c">AUG</text>

  <rect x="548" y="236" width="164" height="54" rx="12" fill="#11151f" opacity="0.78" stroke="#ff8c00" stroke-opacity="0.35"/>
  <text x="566" y="257" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#aab3c4">Latest readout</text>
  <text x="566" y="281" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#ffffff">−64% YoY</text>

  <path d="M940 146 H1118 Q1156 146 1156 184 V384 H1218 L1030 568 L842 384 H904 V184 Q904 146 940 146 Z"
        fill="#ff4500" opacity="0.82" filter="url(#orangeGlow)"/>
  <path d="M940 146 H1118 Q1156 146 1156 184 V384 H1218 L1030 568 L842 384 H904 V184 Q904 146 940 146 Z"
        fill="#090b10" opacity="0.78"/>

  <image x="842" y="126" width="376" height="470"
         href="https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&amp;w=900&amp;auto=format&amp;fit=crop"
         clip-path="url(#presenterArrowClip)" preserveAspectRatio="xMidYMid slice"/>

  <path d="M940 146 H1118 Q1156 146 1156 184 V384 H1218 L1030 568 L842 384 H904 V184 Q904 146 940 146 Z"
        fill="none" stroke="#ff7448" stroke-width="5" stroke-linejoin="round"/>
  <path d="M940 146 H1118 Q1156 146 1156 184 V384 H1218 L1030 568 L842 384 H904 V184 Q904 146 940 146 Z"
        fill="none" stroke="#ffd1c2" stroke-opacity="0.45" stroke-width="1.5" stroke-linejoin="round"/>

  <rect x="878" y="514" width="304" height="84" rx="18" fill="#11151f" opacity="0.82" stroke="#ffffff" stroke-opacity="0.14" filter="url(#softShadow)"/>
  <rect x="900" y="532" width="58" height="24" rx="12" fill="#ff4500"/>
  <text x="916" y="550" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="800" fill="#ffffff">LIVE</text>
  <text x="972" y="553" width="188" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#ffffff">Kevin Stratvert</text>
  <text x="972" y="578" width="188" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#b7bfce">Chief Revenue Officer</text>

  <text x="640" y="660" width="960" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#c3c8d4">
    Revenue plummeted due to declining sales. We need to pivot our strategy before the next quarter closes.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the presenter crop; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not place `clip-path` on a `<g>` or on the arrow `<path>` expecting it to affect child shapes; apply it directly to the presenter `<image>`.
- ❌ Do not use `<foreignObject>` for video or HTML-style name tags; recreate the Cameo mockup with editable SVG shapes and text.
- ❌ Do not apply filters to chart `<line>` elements; use a thicker translucent duplicate `<path>` behind the data line for a glow-like emphasis.
- ❌ Do not rely on PowerPoint-only live Cameo behavior; this recipe is a static, editable visual mockup that suggests an integrated camera feed.

## Composition notes
- Keep the chart on the left 55–60% of the canvas and reserve the right 30% for the presenter, so the human figure feels embedded rather than pasted on.
- Use a dark navy background with warm orange/red accents; the chart line and presenter glow should share the same urgency color family.
- Let the arrow shape overlap the chart’s vertical midpoint and extend downward to reinforce the “decline” story.
- Place the name tag across the lower portion of the presenter shape, not below it, to make the cameo feel like a broadcast overlay.