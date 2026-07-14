# SVG Recipe — Native Data-Driven Clustered Column Chart

## Visual mechanism
A clean clustered column chart is built from structured data arrays: category labels drive x-axis positions, series values drive bar heights, and a shared max value drives y-axis scaling. The surrounding slide uses a presentation-thumbnail layout: bold instructional headline, dark green field, and a white chart canvas that keeps the chart fully editable as individual PowerPoint shapes.

## SVG primitives needed
- 1× `<rect>` for the full-slide green background
- 1× `<linearGradient>` for the orange footer strip on the chart card
- 1× `<filter id="cardShadow">` for soft depth under the chart card
- 1× `<rect>` for the main white chart card
- 1× `<rect>` for the orange footer accent on the chart card
- 1× `<line>` for the title divider inside the chart card
- 8× `<line>` for horizontal value gridlines and axis baseline
- 5× `<rect>` for data-driven orange clustered columns
- 5× `<text>` for x-axis category labels
- 8× `<text>` for y-axis value labels
- 1× `<rect>` plus 1× `<text>` for the legend key and label
- Multiple `<text>` elements for slide headline, chart title, axis/title labels, and source URL
- 1× decorative `<path>` for an Excel-like data ribbon accent, replacing any presenter/face imagery

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="orangeFooter" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c95f18"/>
      <stop offset="55%" stop-color="#e57b1c"/>
      <stop offset="100%" stop-color="#b94f12"/>
    </linearGradient>
    <linearGradient id="barFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f39a20"/>
      <stop offset="100%" stop-color="#e77f12"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#1f7948"/>

  <text x="112" y="90" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700" fill="#ffffff">
    <tspan x="112" dy="0">Excel</tspan>
    <tspan x="112" dy="70">Chart</tspan>
    <tspan x="112" dy="70">Tips</tspan>
  </text>

  <text x="326" y="90" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#fff200">
    <tspan x="326" dy="0">Tip #5: Create a graph in</tspan>
    <tspan x="326" dy="70">PowerPoint using data from</tspan>
    <tspan x="326" dy="70">Excel</tspan>
  </text>

  <path d="M91 562 L91 520 C121 496 158 484 203 484 C249 484 286 496 316 520 L316 568 L91 568 Z"
        fill="#125a38" opacity="0.65"/>
  <rect x="113" y="340" width="183" height="134" rx="12" fill="#ffffff" opacity="0.12"/>
  <rect x="132" y="360" width="145" height="24" rx="4" fill="#2fbf71"/>
  <rect x="132" y="396" width="145" height="12" rx="3" fill="#ffffff" opacity="0.55"/>
  <rect x="132" y="422" width="106" height="12" rx="3" fill="#ffffff" opacity="0.45"/>
  <rect x="132" y="448" width="126" height="12" rx="3" fill="#ffffff" opacity="0.45"/>
  <text x="145" y="381" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">DATA</text>

  <g filter="url(#cardShadow)">
    <rect x="474" y="253" width="638" height="359" fill="#ffffff"/>
    <rect x="474" y="585" width="638" height="27" fill="url(#orangeFooter)"/>
  </g>

  <text x="536" y="333" width="530" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="300" fill="#555555">
    Chart created in PowerPoint
  </text>
  <line x1="536" y1="345" x2="1060" y2="345" stroke="#c8c8c8" stroke-width="2"/>

  <text x="780" y="378" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="700" fill="#666666">Units</text>

  <!-- Data model: categories = Region A..E; values = 24, 65, 36, 48, 51; yMax = 70 -->
  <line x1="600" y1="538" x2="1000" y2="538" stroke="#e2e2e2" stroke-width="1.2"/>
  <line x1="600" y1="517" x2="1000" y2="517" stroke="#e8e8e8" stroke-width="1"/>
  <line x1="600" y1="496" x2="1000" y2="496" stroke="#e8e8e8" stroke-width="1"/>
  <line x1="600" y1="475" x2="1000" y2="475" stroke="#e8e8e8" stroke-width="1"/>
  <line x1="600" y1="454" x2="1000" y2="454" stroke="#e8e8e8" stroke-width="1"/>
  <line x1="600" y1="433" x2="1000" y2="433" stroke="#e8e8e8" stroke-width="1"/>
  <line x1="600" y1="412" x2="1000" y2="412" stroke="#e8e8e8" stroke-width="1"/>
  <line x1="600" y1="391" x2="1000" y2="391" stroke="#e8e8e8" stroke-width="1"/>

  <text x="584" y="542" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">0</text>
  <text x="582" y="521" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">10</text>
  <text x="582" y="500" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">20</text>
  <text x="582" y="479" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">30</text>
  <text x="582" y="458" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">40</text>
  <text x="582" y="437" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">50</text>
  <text x="582" y="416" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">60</text>
  <text x="582" y="395" width="22" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#666666">70</text>

  <rect x="628" y="487" width="26" height="51" fill="url(#barFill)"/>
  <rect x="708" y="401" width="26" height="137" fill="url(#barFill)"/>
  <rect x="788" y="462" width="26" height="76" fill="url(#barFill)"/>
  <rect x="868" y="437" width="26" height="101" fill="url(#barFill)"/>
  <rect x="948" y="430" width="26" height="108" fill="url(#barFill)"/>

  <text x="625" y="552" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="7" fill="#333333">Region A</text>
  <text x="705" y="552" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="7" fill="#333333">Region B</text>
  <text x="785" y="552" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="7" fill="#333333">Region C</text>
  <text x="865" y="552" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="7" fill="#333333">Region D</text>
  <text x="945" y="552" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="7" fill="#333333">Region E</text>

  <rect x="785" y="565" width="7" height="7" fill="#e77f12"/>
  <text x="798" y="572" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#333333">Units</text>

  <text x="372" y="685" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff">
    www.ExcelChartTips.com
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rendering the chart as a single screenshot; use editable rectangles, lines, and text so each bar and label remains PowerPoint-editable.
- ❌ Using `<foreignObject>` for an HTML chart/table; it will hard-fail translation.
- ❌ Using `<pattern>` fills for plot backgrounds; use simple gridline `<line>` elements instead.
- ❌ Applying `filter` to gridlines or axes; filters on `<line>` are dropped, so keep axes crisp and unfiltered.
- ❌ Depending on automatic text wrapping; every `<text>` needs an explicit `width` attribute for stable PPTX rendering.

## Composition notes
- Reserve the upper third for the bold instructional headline; keep the chart card slightly right of center to match a tutorial-thumbnail feel.
- Use the green background as a high-contrast stage, then let the white chart card act as the analytical focal point.
- Scale bar heights from a declared `yMax` so updates to values remain visually proportional; keep gridlines light gray and bars Office-orange.
- Replace presenter imagery with a neutral data/accent motif when faces are blurred or unavailable; the chart should remain the primary subject.