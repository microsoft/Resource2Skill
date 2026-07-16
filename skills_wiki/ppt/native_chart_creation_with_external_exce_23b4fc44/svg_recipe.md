# SVG Recipe — Native Chart Creation with External Excel Data

## Visual mechanism
Render a clean, PowerPoint-editable clustered column chart by converting spreadsheet categories and values into SVG bars, gridlines, axis labels, and chart annotations. The premium look comes from a large white chart card, precise data-scaled columns, subtle shadows, and a small “Excel data source” cue that explains the chart was driven by external data.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<linearGradient>` for the slide background and orange bar fills
- 1× `<filter id="cardShadow">` applied to the chart card
- 1× `<filter id="softShadow">` applied to data bars and the source badge
- 1× `<rect>` for the main chart card
- 1× `<rect>` for the Excel/source-data badge
- 1× `<path>` for the decorative data-flow curve from source badge toward chart
- 8× `<line>` for horizontal value-axis gridlines
- 1× `<line>` for the x-axis baseline
- 5× `<rect>` for data columns generated from external Excel values
- 5× `<text>` for bar value labels
- 5× `<text>` for x-axis category labels
- 8× `<text>` for y-axis tick labels
- Multiple `<text>` elements with explicit `width` for slide title, chart title, captions, and source metadata
- 4× small `<rect>` elements inside the badge to suggest an embedded Excel data table

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F9FC"/>
      <stop offset="60%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#E8EEF5"/>
    </linearGradient>

    <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFB15C"/>
      <stop offset="52%" stop-color="#F47A20"/>
      <stop offset="100%" stop-color="#D85F11"/>
    </linearGradient>

    <linearGradient id="excelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#29B36A"/>
      <stop offset="100%" stop-color="#0B7A3B"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.08  0 0 0 0 0.12  0 0 0 0 0.18  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.10  0 0 0 0 0.08  0 0 0 0 0.05  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="76" y="72" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#172033">
    Chart created in PowerPoint
  </text>
  <text x="78" y="106" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#697386">
    External Excel data converted into fully editable chart shapes
  </text>

  <rect x="80" y="135" width="1120" height="520" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="108" y="158" width="214" height="86" rx="18" fill="url(#excelGrad)" filter="url(#softShadow)"/>
  <text x="132" y="190" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">
    Excel Data
  </text>
  <text x="132" y="214" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DDF7E8">
    categories + values
  </text>

  <rect x="132" y="225" width="34" height="6" rx="3" fill="#BFF2D2"/>
  <rect x="172" y="225" width="34" height="6" rx="3" fill="#BFF2D2"/>
  <rect x="212" y="225" width="34" height="6" rx="3" fill="#BFF2D2"/>
  <rect x="252" y="225" width="34" height="6" rx="3" fill="#BFF2D2"/>

  <path d="M322 200 C385 185, 418 148, 500 158 C565 166, 604 185, 655 178"
        fill="none" stroke="#96A3B8" stroke-width="3" stroke-dasharray="8 8" opacity="0.6"/>

  <text x="405" y="190" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#1F2A44">
    Units
  </text>
  <text x="405" y="218" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#778195">
    Clustered column chart generated from spreadsheet rows
  </text>

  <line x1="210" y1="185" x2="1050" y2="185" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="240" x2="1050" y2="240" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="295" x2="1050" y2="295" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="350" x2="1050" y2="350" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="405" x2="1050" y2="405" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="460" x2="1050" y2="460" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="515" x2="1050" y2="515" stroke="#E3E8EF" stroke-width="1"/>
  <line x1="210" y1="570" x2="1050" y2="570" stroke="#AEB7C5" stroke-width="1.4"/>

  <text x="164" y="190" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">70</text>
  <text x="164" y="245" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">60</text>
  <text x="164" y="300" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">50</text>
  <text x="164" y="355" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">40</text>
  <text x="164" y="410" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">30</text>
  <text x="164" y="465" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">20</text>
  <text x="164" y="520" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">10</text>
  <text x="164" y="575" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" text-anchor="end" fill="#7C8798">0</text>

  <rect x="285" y="438" width="76" height="132" rx="9" fill="url(#barGrad)" filter="url(#softShadow)"/>
  <rect x="425" y="212.5" width="76" height="357.5" rx="9" fill="url(#barGrad)" filter="url(#softShadow)"/>
  <rect x="565" y="372" width="76" height="198" rx="9" fill="url(#barGrad)" filter="url(#softShadow)"/>
  <rect x="705" y="306" width="76" height="264" rx="9" fill="url(#barGrad)" filter="url(#softShadow)"/>
  <rect x="845" y="289.5" width="76" height="280.5" rx="9" fill="url(#barGrad)" filter="url(#softShadow)"/>

  <text x="285" y="425" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#1F2A44">24</text>
  <text x="425" y="199" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#1F2A44">65</text>
  <text x="565" y="359" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#1F2A44">36</text>
  <text x="705" y="293" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#1F2A44">48</text>
  <text x="845" y="276" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#1F2A44">51</text>

  <text x="268" y="604" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#5D687A">Region A</text>
  <text x="408" y="604" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#5D687A">Region B</text>
  <text x="548" y="604" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#5D687A">Region C</text>
  <text x="688" y="604" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#5D687A">Region D</text>
  <text x="828" y="604" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#5D687A">Region E</text>

  <rect x="980" y="182" width="126" height="34" rx="17" fill="#FFF3E8"/>
  <circle cx="1000" cy="199" r="6" fill="#F47A20"/>
  <text x="1014" y="204" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#B65312">
    Units
  </text>

  <text x="960" y="617" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8B95A5">
    Data range: Sheet1!A1:B6
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<foreignObject>` to embed an HTML table as the Excel source; it will hard-fail translation.
- ❌ Do not use `<pattern>` fills for chart grid backgrounds; use simple editable `<line>` gridlines instead.
- ❌ Do not use `marker-end` on a `<path>` for the data-flow arrow; use a dashed `<path>` without an arrowhead or draw a small triangle manually if needed.
- ❌ Do not omit `width` on chart labels, tick labels, or titles; PowerPoint text boxes need explicit widths.
- ❌ Do not rely on SVG animation to “grow” the bars; create final editable bar rectangles only.

## Composition notes
- Keep the chart card large and central; reserve about 70–80% of the slide width for the plot so the chart reads as the main object.
- Put the external data cue near the upper-left of the chart card, but keep it secondary so it explains the workflow without competing with the bars.
- Use one strong accent color for the series when there is only one data series; remove or minimize the legend unless it clarifies the data.
- Compute bar heights from the external data using a fixed chart scale, then render each bar as an editable `<rect>` with value labels above.