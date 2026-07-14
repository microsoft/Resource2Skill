# SVG Recipe — Declarative Title Slide

## Visual mechanism
A single oversized, high-contrast typographic statement is centered on a deep, uninterrupted color field. A small label above the statement creates hierarchy, while subtle tonal geometry keeps the slide premium without competing with the message.

## SVG primitives needed
- 1× `<rect>` for the full-slide saturated background field
- 2× `<path>` for barely visible oversized corner contour shapes / atmosphere
- 1× `<line>` for a restrained divider between label and message
- 3× `<text>` for label, declarative headline, and optional small chapter footer
- 1× `<linearGradient id="bg">` for a near-solid executive background with slight depth
- 1× `<linearGradient id="accent">` for the thin divider line
- 1× `<filter id="textShadow">` applied to headline text for subtle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#101B35"/>
      <stop offset="0.55" stop-color="#1B2B4B"/>
      <stop offset="1" stop-color="#14233F"/>
    </linearGradient>

    <linearGradient id="accent" x1="490" y1="0" x2="790" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Deep uninterrupted field -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <!-- Tonal atmosphere: keep these extremely quiet -->
  <path d="M990,-70
           C1108,-42 1192,28 1260,128
           C1324,223 1322,348 1268,444
           C1208,551 1089,603 969,582
           C850,561 760,474 728,360
           C694,240 740,118 838,41
           C882,6 933,-84 990,-70Z"
        fill="#FFFFFF" opacity="0.035"/>

  <path d="M-112,520
           C-48,444 52,408 148,431
           C246,454 326,526 347,624
           C368,724 302,808 210,845
           C118,882 5,856 -62,781
           C-132,703 -181,603 -112,520Z"
        fill="#46B9AA" opacity="0.09"/>

  <!-- Small label: authoritative but secondary -->
  <text x="640" y="200"
        width="960"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="68"
        font-weight="800"
        letter-spacing="2"
        fill="#FFFFFF">
    #1
  </text>

  <!-- Fine divider gives the centered block a premium editorial feel -->
  <line x1="490" y1="236" x2="790" y2="236"
        stroke="url(#accent)"
        stroke-width="2"/>

  <!-- Main declarative statement -->
  <text x="640" y="334"
        width="1120"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="88"
        font-weight="900"
        letter-spacing="-1"
        fill="#FFFFFF"
        filter="url(#textShadow)">
    <tspan x="640" dy="0">GOOD PRESENTATION</tspan>
    <tspan x="640" dy="98">SLIDES ARE CLEAR</tspan>
  </text>

  <!-- Optional restrained footer for chapter context -->
  <text x="640" y="635"
        width="900"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
        font-size="20"
        font-weight="700"
        letter-spacing="4"
        fill="#FFFFFF"
        opacity="0.58">
    CHAPTER 01 · THE PRINCIPLE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Adding icons, charts, screenshots, or decorative illustrations that dilute the single-message focus
- ❌ Using multiple competing font weights, colors, or alignments; the power comes from strict hierarchy
- ❌ Centering each line independently with inconsistent widths; keep all `<text>` elements on the same center axis
- ❌ Applying filters to `<line>` elements for divider glow; use a simple gradient stroke instead
- ❌ Using `<textPath>`, `<foreignObject>`, or HTML text layout for multiline headlines

## Composition notes
- Keep the headline block centered both horizontally and vertically; the main message should occupy roughly the central 50–60% of slide width.
- Use a dark saturated background and white typography for maximum signal-to-noise ratio.
- Decorative paths should stay below 10% opacity so they read as atmosphere, not content.
- The label, divider, and footer are optional; remove the footer for the most austere executive keynote version.