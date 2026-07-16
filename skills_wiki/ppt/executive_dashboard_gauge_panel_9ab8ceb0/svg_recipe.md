# SVG Recipe — KPI Gauge Panel

## Visual mechanism
Analog speedometer gauges convert percentages into a fast-read executive dashboard: a segmented semicircular track shows capacity, a saturated arc shows progress, and a central needle creates a physical “where are we now?” cue. Arrange three gauges in equal-width cards so the viewer can compare KPI status at a glance.

## SVG primitives needed
- 1× full-slide `<rect>` for the clean executive dashboard background
- 3× rounded `<rect>` cards for individual KPI panels
- 3× small accent `<rect>` bars for card color coding
- 6× semicircle `<path>` arcs for pale background tracks and saturated progress arcs
- 3× multi-subpath `<path>` separator overlays to divide each gauge into 10 segments
- 3× triangular `<path>` needles pointing to the current KPI value
- 6× `<circle>` elements for each gauge’s center pin and inner cutout
- 1× `<filter id="cardShadow">` for soft card elevation
- 1× `<linearGradient id="pageWash">` for a subtle page background
- 3× `<linearGradient>` definitions for premium KPI color shading
- Multiple `<text>` elements with explicit `width` for title, labels, values, and small context notes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageWash" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F7FA"/>
    </linearGradient>

    <linearGradient id="blueGauge" x1="-120" y1="0" x2="120" y2="-120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#5FA6D8"/>
      <stop offset="100%" stop-color="#2F628D"/>
    </linearGradient>
    <linearGradient id="orangeGauge" x1="-120" y1="0" x2="120" y2="-120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#E4A071"/>
      <stop offset="100%" stop-color="#B96745"/>
    </linearGradient>
    <linearGradient id="greenGauge" x1="-120" y1="0" x2="120" y2="-120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#92C69A"/>
      <stop offset="100%" stop-color="#4D8C62"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageWash)"/>

  <text x="640" y="78" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#30343B">
    EXECUTIVE KPI GAUGE PANEL
  </text>
  <text x="640" y="116" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="500" fill="#7B8794">
    Performance against quarterly operating targets
  </text>

  <!-- Gauge card 1: Reach, 80% -->
  <g transform="translate(110 170)">
    <rect x="0" y="0" width="320" height="425" rx="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="38" y="28" width="244" height="7" rx="4" fill="url(#blueGauge)"/>
    <g transform="translate(160 188)">
      <path d="M -112 0 A 112 112 0 0 1 112 0" fill="none" stroke="#D7E7F3" stroke-width="42" stroke-linecap="butt"/>
      <path d="M -112 0 A 112 112 0 0 1 112 0" fill="none" stroke="url(#blueGauge)" stroke-width="42" stroke-linecap="butt" stroke-dasharray="282 352"/>
      <path d="M -83.7 -27.2 L -109.4 -35.5 M -71.2 -51.7 L -93 -67.6 M -51.7 -71.2 L -67.6 -93 M -27.2 -83.7 L -35.5 -109.4 M 0 -88 L 0 -115 M 27.2 -83.7 L 35.5 -109.4 M 51.7 -71.2 L 67.6 -93 M 71.2 -51.7 L 93 -67.6 M 83.7 -27.2 L 109.4 -35.5"
            fill="none" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M 74 -54 L 4.7 6.5 L -4.7 -6.5 Z" fill="#2F628D"/>
      <circle cx="0" cy="0" r="24" fill="#2F628D"/>
      <circle cx="0" cy="0" r="10" fill="#FFFFFF"/>
    </g>
    <text x="160" y="296" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="600" letter-spacing="2" fill="#35698F">REACH</text>
    <text x="160" y="356" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="300" fill="#35698F">80%</text>
    <text x="160" y="393" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#8CA3B5">TARGET 75%</text>
  </g>

  <!-- Gauge card 2: Engagement, 55% -->
  <g transform="translate(480 170)">
    <rect x="0" y="0" width="320" height="425" rx="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="38" y="28" width="244" height="7" rx="4" fill="url(#orangeGauge)"/>
    <g transform="translate(160 188)">
      <path d="M -112 0 A 112 112 0 0 1 112 0" fill="none" stroke="#F4DED2" stroke-width="42" stroke-linecap="butt"/>
      <path d="M -112 0 A 112 112 0 0 1 112 0" fill="none" stroke="url(#orangeGauge)" stroke-width="42" stroke-linecap="butt" stroke-dasharray="194 352"/>
      <path d="M -83.7 -27.2 L -109.4 -35.5 M -71.2 -51.7 L -93 -67.6 M -51.7 -71.2 L -67.6 -93 M -27.2 -83.7 L -35.5 -109.4 M 0 -88 L 0 -115 M 27.2 -83.7 L 35.5 -109.4 M 51.7 -71.2 L 67.6 -93 M 71.2 -51.7 L 93 -67.6 M 83.7 -27.2 L 109.4 -35.5"
            fill="none" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M 14 -91 L 7.9 1.3 L -7.9 -1.3 Z" fill="#B96745"/>
      <circle cx="0" cy="0" r="24" fill="#B96745"/>
      <circle cx="0" cy="0" r="10" fill="#FFFFFF"/>
    </g>
    <text x="160" y="296" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="600" letter-spacing="1.5" fill="#C87552">ENGAGEMENT</text>
    <text x="160" y="356" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="300" fill="#C87552">55%</text>
    <text x="160" y="393" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#B99A8D">TARGET 60%</text>
  </g>

  <!-- Gauge card 3: Awareness, 75% -->
  <g transform="translate(850 170)">
    <rect x="0" y="0" width="320" height="425" rx="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
    <rect x="38" y="28" width="244" height="7" rx="4" fill="url(#greenGauge)"/>
    <g transform="translate(160 188)">
      <path d="M -112 0 A 112 112 0 0 1 112 0" fill="none" stroke="#DDEEDF" stroke-width="42" stroke-linecap="butt"/>
      <path d="M -112 0 A 112 112 0 0 1 112 0" fill="none" stroke="url(#greenGauge)" stroke-width="42" stroke-linecap="butt" stroke-dasharray="264 352"/>
      <path d="M -83.7 -27.2 L -109.4 -35.5 M -71.2 -51.7 L -93 -67.6 M -51.7 -71.2 L -67.6 -93 M -27.2 -83.7 L -35.5 -109.4 M 0 -88 L 0 -115 M 27.2 -83.7 L 35.5 -109.4 M 51.7 -71.2 L 67.6 -93 M 71.2 -51.7 L 93 -67.6 M 83.7 -27.2 L 109.4 -35.5"
            fill="none" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M 65 -65 L 5.7 5.7 L -5.7 -5.7 Z" fill="#4D8C62"/>
      <circle cx="0" cy="0" r="24" fill="#4D8C62"/>
      <circle cx="0" cy="0" r="10" fill="#FFFFFF"/>
    </g>
    <text x="160" y="296" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="600" letter-spacing="1.5" fill="#5E9B6B">AWARENESS</text>
    <text x="160" y="356" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="300" fill="#5E9B6B">75%</text>
    <text x="160" y="393" width="320" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#89A98E">TARGET 70%</text>
  </g>

  <text x="640" y="654" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="500" fill="#9AA4AF">
    Gauge arcs show actual progress; needles create the analog dashboard read for senior stakeholders.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut the inner hole of the gauge; build gauges with stroked semicircle paths instead.
- ❌ Do not use `<use>` for repeating the gauge structure; duplicate the editable shapes directly.
- ❌ Do not put `filter` on separator `<line>` elements; use a multi-subpath `<path>` for separators or keep lines unfiltered.
- ❌ Do not use `marker-end` for the needle; create the needle as a triangular `<path>` so it remains editable.
- ❌ Do not omit `width` on KPI text, especially large percentages, because PowerPoint text boxes need explicit width for stable rendering.

## Composition notes
- Keep the three gauges in equal-width cards with generous white space; the cards should feel like premium SaaS dashboard modules, not dense spreadsheet widgets.
- Place each gauge in the upper half of its card, then stack label, large percentage, and target note below for a clear vertical reading path.
- Use muted professional colors with pale background tracks and saturated progress arcs; this preserves legibility while still making performance differences obvious.
- Leave a calm header band at the top and a small methodology/footer note at the bottom so the dashboard feels executive-ready rather than purely decorative.