# SVG Recipe — Standard Chart Slide

## Visual mechanism
A disciplined executive chart shell: a strong headline anchors the top, while a large rounded chart canvas occupies almost the full slide width with clear chart title, subtitle, legend, grid, data marks, and footer separated by a fine hairline. The visual style is minimal but premium through subtle shadows, restrained blue accents, soft gridlines, and editable SVG-built chart elements.

## SVG primitives needed
- 2× `<rect>` for full-slide background and main chart card
- 1× `<rect>` for a thin top accent rule
- 1× `<rect>` for a highlighted forecast / focus band inside the plot
- 12× `<line>` for chart gridlines, axes, target rule, and footer hairline
- 12× `<rect>` for editable vertical bars and legend swatches
- 2× `<path>` for the filled trend area and trend line overlay
- 7× `<circle>` for editable data points and legend marker
- 18× `<text>` for slide headline, chart title, subtitle, axis labels, legend, annotation, and footer
- 3× `<linearGradient>` for background, bar fills, and trend area
- 1× `<filter id="cardShadow">` applied to the main chart card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2F80ED"/>
      <stop offset="100%" stop-color="#1B5FB8"/>
    </linearGradient>

    <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#26A6FF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#26A6FF" stop-opacity="0.02"/>
    </linearGradient>

    <filter id="cardShadow" x="-5%" y="-8%" width="110%" height="120%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05  0 0 0 0 0.12  0 0 0 0 0.22  0 0 0 0.16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>
  <rect x="0" y="0" width="1280" height="6" fill="#1F6FEB"/>

  <text x="64" y="68" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#172033">
    Revenue growth is broadening across enterprise segments
  </text>
  <text x="1040" y="66" width="176" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" text-anchor="end" fill="#7B8794">
    Q4 Board Update
  </text>

  <rect x="64" y="116" width="1152" height="522" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="64" y="116" width="1152" height="522" rx="22" fill="none" stroke="#E5ECF3" stroke-width="1"/>

  <text x="96" y="162" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#182235">
    Net revenue by quarter, indexed to Q1 FY22
  </text>
  <text x="96" y="190" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#697586">
    Current portfolio outpaces target from Q2 onward; shaded area indicates management forecast window.
  </text>

  <rect x="912" y="145" width="14" height="14" rx="3" fill="url(#barGradient)"/>
  <text x="934" y="157" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#4B5565">Actual revenue</text>
  <circle cx="1050" cy="152" r="5" fill="#26A6FF"/>
  <text x="1062" y="157" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#4B5565">Run-rate index</text>

  <rect x="892" y="242" width="260" height="314" fill="#EAF5FF" opacity="0.72"/>

  <line x1="128" y1="556" x2="1152" y2="556" stroke="#D9E2EC" stroke-width="1"/>
  <line x1="128" y1="493" x2="1152" y2="493" stroke="#E8EEF5" stroke-width="1"/>
  <line x1="128" y1="430" x2="1152" y2="430" stroke="#E8EEF5" stroke-width="1"/>
  <line x1="128" y1="367" x2="1152" y2="367" stroke="#E8EEF5" stroke-width="1"/>
  <line x1="128" y1="304" x2="1152" y2="304" stroke="#E8EEF5" stroke-width="1"/>
  <line x1="128" y1="242" x2="1152" y2="242" stroke="#E8EEF5" stroke-width="1"/>

  <line x1="128" y1="556" x2="128" y2="242" stroke="#B8C4D2" stroke-width="1.2"/>
  <line x1="128" y1="556" x2="1152" y2="556" stroke="#B8C4D2" stroke-width="1.2"/>
  <line x1="128" y1="350" x2="1152" y2="350" stroke="#9AA8BA" stroke-width="1.2" stroke-dasharray="6 6"/>
  <text x="1048" y="340" width="104" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="600" text-anchor="end" fill="#667085">
    FY target line
  </text>

  <text x="82" y="560" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#7B8794">100</text>
  <text x="82" y="497" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#7B8794">120</text>
  <text x="82" y="434" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#7B8794">140</text>
  <text x="82" y="371" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#7B8794">160</text>
  <text x="82" y="308" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#7B8794">180</text>
  <text x="82" y="246" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#7B8794">200</text>

  <rect x="172" y="487" width="44" height="69" rx="6" fill="url(#barGradient)"/>
  <rect x="278" y="464" width="44" height="92" rx="6" fill="url(#barGradient)"/>
  <rect x="384" y="430" width="44" height="126" rx="6" fill="url(#barGradient)"/>
  <rect x="490" y="401" width="44" height="155" rx="6" fill="url(#barGradient)"/>
  <rect x="596" y="374" width="44" height="182" rx="6" fill="url(#barGradient)"/>
  <rect x="702" y="335" width="44" height="221" rx="6" fill="url(#barGradient)"/>
  <rect x="808" y="310" width="44" height="246" rx="6" fill="url(#barGradient)"/>
  <rect x="914" y="284" width="44" height="272" rx="6" fill="#75B7FF"/>
  <rect x="1020" y="262" width="44" height="294" rx="6" fill="#75B7FF"/>
  <rect x="1126" y="247" width="26" height="309" rx="6" fill="#75B7FF"/>

  <path d="M194 474 C300 448, 406 416, 512 388 C618 354, 724 318, 830 296 C936 270, 1042 248, 1152 230 L1152 556 L194 556 Z" fill="url(#areaGradient)"/>
  <path d="M194 474 C300 448, 406 416, 512 388 C618 354, 724 318, 830 296 C936 270, 1042 248, 1152 230" fill="none" stroke="#26A6FF" stroke-width="4" stroke-linecap="round"/>

  <circle cx="194" cy="474" r="6" fill="#FFFFFF" stroke="#26A6FF" stroke-width="3"/>
  <circle cx="406" cy="416" r="6" fill="#FFFFFF" stroke="#26A6FF" stroke-width="3"/>
  <circle cx="618" cy="354" r="6" fill="#FFFFFF" stroke="#26A6FF" stroke-width="3"/>
  <circle cx="830" cy="296" r="6" fill="#FFFFFF" stroke="#26A6FF" stroke-width="3"/>
  <circle cx="1042" cy="248" r="6" fill="#FFFFFF" stroke="#26A6FF" stroke-width="3"/>
  <circle cx="1152" cy="230" r="6" fill="#26A6FF" stroke="#FFFFFF" stroke-width="3"/>

  <text x="172" y="586" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="middle" fill="#7B8794">Q1 FY22</text>
  <text x="384" y="586" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="middle" fill="#7B8794">Q3 FY22</text>
  <text x="596" y="586" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="middle" fill="#7B8794">Q1 FY23</text>
  <text x="808" y="586" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="middle" fill="#7B8794">Q3 FY23</text>
  <text x="1020" y="586" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="middle" fill="#7B8794">Q1 FY24</text>
  <text x="1138" y="586" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="middle" fill="#7B8794">Q2 FY24F</text>

  <text x="934" y="276" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#1864AB">
    Forecast window
  </text>
  <text x="934" y="296" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#52616F">
    Consensus range narrows as renewal cohort matures.
  </text>

  <line x1="64" y1="666" x2="1216" y2="666" stroke="#D7DEE8" stroke-width="1"/>
  <text x="64" y="690" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#7B8794">
    Source: Finance data mart; indexed revenue, Q1 FY22 = 100. Forecasts reflect current management plan.
  </text>
  <text x="1216" y="690" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" text-anchor="end" fill="#9AA8BA">
    Confidential · Strategy Office
  </text>
</svg>
```

## Avoid in this skill
- ❌ Exporting the chart as a single raster image; the bars, line, labels, and grid should remain editable PowerPoint shapes.
- ❌ Overloading the card with dense callouts; this shell is for one primary chart, not a multi-panel dashboard.
- ❌ Applying filters to gridlines or axis lines; shadows/glows on thin lines are dropped or create visual noise.
- ❌ Using `marker-end` arrowheads on paths for trend annotations; use plain lines or small editable paths if arrows are required.
- ❌ Relying on clipping for chart elements; keep bars, bands, and paths manually inside the plot area.

## Composition notes
- Keep the headline in the top 90 px and the chart card from roughly y=115 to y=640, giving the chart maximum horizontal breathing room.
- Reserve the first 70–90 px inside the card for chart title, subtitle, and legend; begin the plot below that to prevent label collisions.
- Use one dominant accent color for the primary data series, with softer tints for forecast or secondary regions.
- Footer content should sit below a fine hairline and stay visually quiet so it supports provenance without competing with the chart.