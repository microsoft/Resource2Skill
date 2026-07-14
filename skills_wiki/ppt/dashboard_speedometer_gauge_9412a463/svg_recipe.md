# SVG Recipe — Dashboard Speedometer Gauge

## Visual mechanism
A thick semi-circular doughnut arc uses a semantic red→yellow→green gradient to encode range quality, while a pivot-mounted triangular needle points to the current KPI value. The gauge is framed as a premium dashboard card with subtle shadow, tick labels, and a dominant percentage readout.

## SVG primitives needed
- 2× `<rect>` for the slide background and elevated dashboard card
- 1× `<linearGradient>` for the page background
- 1× `<linearGradient>` for the red/yellow/green gauge arc
- 1× `<radialGradient>` for the metallic pivot hub
- 2× `<filter>` for soft card shadow and gauge/needle glow
- 1× `<path>` for the full pale semicircle track
- 1× `<path>` for the filled KPI arc segment
- 1× `<path>` for a glossy highlight over the arc
- 1× `<path>` for the triangular speedometer needle
- 2× `<circle>` for the pivot hub and inner cap
- 1× `<line>` for the horizontal baseline through the pivot
- 5× `<line>` for radial tick marks
- 12× `<text>` for title, subtitle, tick labels, percentage, status, and supporting dashboard labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>

    <linearGradient id="gaugeGradient" x1="360" y1="0" x2="920" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF1300"/>
      <stop offset="38%" stop-color="#FF9A00"/>
      <stop offset="54%" stop-color="#FFF500"/>
      <stop offset="78%" stop-color="#7DE02C"/>
      <stop offset="100%" stop-color="#16B85C"/>
    </linearGradient>

    <radialGradient id="hubGradient" cx="42%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#1F2937"/>
      <stop offset="65%" stop-color="#050505"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>
  <rect x="86" y="42" width="1108" height="636" rx="34" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="86" y="42" width="1108" height="636" rx="34" fill="none" stroke="#E6ECF3" stroke-width="2"/>

  <text x="640" y="96" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">
    Project Health Metric
  </text>
  <text x="640" y="130" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6B7280">
    Risk-weighted delivery confidence across budget, scope, velocity, and stakeholder sentiment
  </text>

  <rect x="232" y="166" width="168" height="42" rx="21" fill="#F3F6FA" stroke="#E4E9F0"/>
  <text x="316" y="194" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#6B7280">
    Q3 TARGET
  </text>

  <rect x="884" y="166" width="164" height="42" rx="21" fill="#ECFDF5" stroke="#B7F0D2"/>
  <text x="966" y="194" width="140" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#059669">
    ON TRACK
  </text>

  <!-- Full gauge track: center=(640,420), outerR=280, innerR=200 -->
  <path d="M 360 420
           A 280 280 0 0 1 920 420
           L 840 420
           A 200 200 0 0 0 440 420
           Z"
        fill="#E9EEF5"/>

  <!-- Filled KPI arc at 75%: start angle 180°, end angle 315° -->
  <path d="M 360 420
           A 280 280 0 0 1 838 222
           L 781 279
           A 200 200 0 0 0 440 420
           Z"
        fill="url(#gaugeGradient)" filter="url(#softGlow)"/>

  <!-- Gloss highlight along the upper center of the colored band -->
  <path d="M 388 414
           A 252 252 0 0 1 816 240"
        fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity="0.22"/>

  <!-- Baseline through pivot -->
  <line x1="278" y1="420" x2="1002" y2="420" stroke="#111827" stroke-width="1.4" opacity="0.75"/>

  <!-- Tick marks -->
  <line x1="348" y1="420" x2="382" y2="420" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <line x1="426" y1="206" x2="451" y2="231" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <line x1="640" y1="126" x2="640" y2="162" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <line x1="854" y1="206" x2="829" y2="231" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <line x1="932" y1="420" x2="898" y2="420" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>

  <text x="320" y="462" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#6B7280">0</text>
  <text x="410" y="246" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#6B7280">25</text>
  <text x="640" y="116" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#6B7280">50</text>
  <text x="870" y="246" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#6B7280">75</text>
  <text x="960" y="462" width="80" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#6B7280">100</text>

  <!-- Needle aimed at 75% -->
  <path d="M 653 433
           L 806 254
           L 627 407
           Z"
        fill="#050505" filter="url(#softGlow)"/>
  <circle cx="640" cy="420" r="34" fill="url(#hubGradient)"/>
  <circle cx="640" cy="420" r="10" fill="#FFFFFF"/>

  <text x="855" y="124" width="190" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" fill="#050505">
    75%
  </text>

  <text x="640" y="548" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#050505">
    75%
  </text>
  <text x="640" y="588" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#16A34A">
    DELIVERY CONFIDENCE SCORE
  </text>

  <text x="206" y="630" width="260" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9CA3AF">
    Low confidence
  </text>
  <text x="816" y="630" width="260" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#9CA3AF">
    High confidence
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to cut the doughnut hole; build the gauge as a compound `<path>` instead.
- ❌ Applying `filter` to `<line>` tick marks or baselines; filters on lines are dropped, so reserve shadows/glows for paths, circles, rectangles, or text.
- ❌ Rendering the whole gauge as a flat PNG unless you specifically need a photo-realistic texture; editable SVG paths make the arc, needle, and labels easier to recolor in PowerPoint.
- ❌ Using `marker-end` for the needle; draw the pointer as a filled triangular `<path>` so it remains editable and visually sharp.
- ❌ Forgetting `width` on `<text>` elements; PPT translation relies on explicit text box width for clean layout.

## Composition notes
- Place the pivot exactly on the horizontal diameter of the semicircle; this makes the needle read as physically anchored rather than floating.
- Reserve the upper half of the card for the arc and needle, and the lower third for the dominant KPI number and status label.
- Use a pale full-range track behind the colored value arc when the dashboard needs to show remaining headroom; omit it for a cleaner “animated speedometer” look.
- Keep the red/yellow/green rhythm left-to-right and avoid adding competing colors near the gauge, so status is decoded instantly.