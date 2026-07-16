# SVG Recipe — Intervention Point Timeline Chart

## Visual mechanism
A time-series line chart is split by a prominent vertical intervention marker, with the “before” trend and “after” trend drawn as separate color-coded series. The marker creates a clear narrative hinge: performance before a strategic action versus performance after it.

## SVG primitives needed
- 1× full-slide `<rect>` with gradient fill for the dark executive background
- 1× rounded `<rect>` chart panel with subtle shadow for the plotting surface
- 6× horizontal `<line>` gridlines plus 1× vertical axis and 1× horizontal axis
- 2× filled `<path>` areas under the before/after lines for subtle trend emphasis
- 2× stroked `<path>` line series for before and after performance
- 17× `<circle>` data point markers, split into before/after colors
- 1× narrow glowing `<rect>` for the intervention point
- 1× rounded `<rect>` intervention label badge
- 1× rounded `<rect>` insight callout card with connector `<line>`
- Multiple `<text>` labels for title, subtitle, axes, ticks, legend, intervention label, and annotation; every text element includes `width`
- 2× `<filter>` effects: one soft shadow for panels/cards and one orange glow for the intervention marker
- 4× `<linearGradient>` definitions for background, panel, intervention marker, and after-impact area

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E3D72"/>
      <stop offset="55%" stop-color="#2F5597"/>
      <stop offset="100%" stop-color="#17315F"/>
    </linearGradient>
    <linearGradient id="panelFill" x1="0" y1="120" x2="0" y2="580" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>
    <linearGradient id="afterArea" x1="645" y1="150" x2="645" y2="550" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF2E2E" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FF2E2E" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="interventionGrad" x1="0" y1="150" x2="0" y2="550" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFE0C2"/>
      <stop offset="45%" stop-color="#F4B084"/>
      <stop offset="100%" stop-color="#D96926"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="orangeGlow" x="-300%" y="-30%" width="700%" height="160%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M1045,30 C1165,45 1225,120 1260,230 C1180,210 1108,180 1052,115 C1022,80 1018,54 1045,30 Z" fill="#FFFFFF" opacity="0.06"/>
  <path d="M0,610 C120,560 250,578 370,640 C250,712 95,735 0,700 Z" fill="#000000" opacity="0.12"/>

  <text x="70" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">
    Before-and-After Improvement Comparison
  </text>
  <text x="70" y="92" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#DDE8FF">
    Defect rate fell sharply after the process intervention on Feb 10
  </text>

  <rect x="96" y="122" width="1090" height="500" rx="28" fill="url(#panelFill)" stroke="#FFFFFF" stroke-opacity="0.22" filter="url(#softShadow)"/>

  <text x="58" y="388" width="230" transform="rotate(-90 58 388)" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#FFFFFF" opacity="0.9">
    Defect Rate %
  </text>

  <line x1="150" y1="550" x2="1140" y2="550" stroke="#FFFFFF" stroke-width="1.6" opacity="0.75"/>
  <line x1="150" y1="150" x2="150" y2="550" stroke="#FFFFFF" stroke-width="1.6" opacity="0.75"/>

  <line x1="150" y1="550" x2="1140" y2="550" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="150" y1="459" x2="1140" y2="459" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="150" y1="368" x2="1140" y2="368" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="150" y1="277" x2="1140" y2="277" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="150" y1="186" x2="1140" y2="186" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="150" y1="150" x2="1140" y2="150" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>

  <text x="114" y="556" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" text-anchor="end">0</text>
  <text x="114" y="465" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" text-anchor="end">5</text>
  <text x="114" y="374" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" text-anchor="end">10</text>
  <text x="114" y="283" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" text-anchor="end">15</text>
  <text x="114" y="192" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" text-anchor="end">20</text>
  <text x="114" y="156" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" text-anchor="end">22</text>

  <rect x="637" y="145" width="16" height="410" rx="8" fill="url(#interventionGrad)" opacity="0.95" filter="url(#orangeGlow)"/>
  <rect x="596" y="125" width="98" height="28" rx="14" fill="#F4B084"/>
  <text x="608" y="145" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1D2743" text-anchor="middle">
    INTERVENTION
  </text>

  <path d="M150,186 L212,223 L274,168 L336,205 L398,186 L459,259 L521,205 L583,277 L583,550 L150,550 Z"
        fill="#000000" opacity="0.12"/>
  <path d="M645,368 L707,377 L769,386 L831,396 L893,386 L954,405 L1016,423 L1078,414 L1140,423 L1140,550 L645,550 Z"
        fill="url(#afterArea)"/>

  <path d="M150,186 L212,223 L274,168 L336,205 L398,186 L459,259 L521,205 L583,277"
        fill="none" stroke="#111827" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M645,368 L707,377 L769,386 L831,396 L893,386 L954,405 L1016,423 L1078,414 L1140,423"
        fill="none" stroke="#FF3030" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="150" cy="186" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="212" cy="223" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="274" cy="168" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="336" cy="205" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="398" cy="186" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="459" cy="259" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="521" cy="205" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="583" cy="277" r="6" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="645" cy="368" r="7" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="707" cy="377" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="769" cy="386" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="831" cy="396" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="893" cy="386" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="954" cy="405" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="1016" cy="423" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="1078" cy="414" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="1140" cy="423" r="6" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>

  <text x="138" y="586" width="70" transform="rotate(-35 138 586)" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDE8FF">Feb 2</text>
  <text x="385" y="586" width="70" transform="rotate(-35 385 586)" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDE8FF">Feb 6</text>
  <text x="632" y="586" width="80" transform="rotate(-35 632 586)" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF" font-weight="700">Feb 10</text>
  <text x="879" y="586" width="80" transform="rotate(-35 879 586)" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDE8FF">Feb 14</text>
  <text x="1126" y="586" width="80" transform="rotate(-35 1126 586)" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDE8FF">Feb 18</text>

  <rect x="895" y="158" width="230" height="94" rx="18" fill="#102B55" stroke="#FFFFFF" stroke-opacity="0.18" filter="url(#softShadow)"/>
  <text x="917" y="188" width="188" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">
    Step-change visible
  </text>
  <text x="917" y="216" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDE8FF">
    Average defect rate dropped from 18.5% before to 8.3% after launch.
  </text>
  <line x1="895" y1="245" x2="653" y2="368" stroke="#F4B084" stroke-width="2" stroke-dasharray="6 6"/>

  <circle cx="858" cy="86" r="7" fill="#111827" stroke="#FFFFFF" stroke-width="2"/>
  <text x="874" y="91" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">Before</text>
  <circle cx="958" cy="86" r="7" fill="#FF3030" stroke="#FFFFFF" stroke-width="2"/>
  <text x="974" y="91" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">After</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on native PowerPoint chart objects; draw the chart with editable SVG paths, lines, circles, and text.
- ❌ Do not use `<polyline>` or `<polygon>` for the trend; use `<path>` so curved/segmented trend styling remains broadly editable.
- ❌ Do not put `filter` on gridline `<line>` elements; line filters are dropped. Apply glow/shadow only to `<rect>`, `<path>`, `<circle>`, `<ellipse>`, or `<text>`.
- ❌ Do not use `marker-end` for callout arrows; if a pointer is needed, use a plain `<line>` or draw a small arrowhead manually as a `<path>`.
- ❌ Do not use clip paths or masks on chart shapes; clipping is only reliable for `<image>` elements.

## Composition notes
- Keep the chart panel dominant, occupying roughly 75–80% of the slide width and 65–70% of the slide height.
- Place the intervention marker slightly right of center when telling an “improvement after action” story; it leaves room for the post-intervention recovery trend.
- Use high contrast: subdued dark/black before line, saturated red or green after line, and a warm orange intervention marker.
- Reserve the upper-right quadrant for a concise insight callout so the audience sees both the data change and the interpretation immediately.