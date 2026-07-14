# SVG Recipe — Corporate Split-Pane Data Storytelling

## Visual mechanism
A clean 60/40 vertical split pairs a stripped-down horizontal bar chart with a concise “Key Highlights” narrative pane. The highest-priority data point is emphasized with a dark corporate color while secondary bars recede, letting the viewer immediately connect the ranked data to business implications.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× `<rect>` for subtle pane cards behind the chart and insight area
- 6× `<rect>` for horizontal chart bars with rounded ends
- 6× `<text>` for category labels on the left of the bars
- 6× `<text>` for direct value labels inside the bars
- 6× small `<circle>` / `<rect>` accents for country or rank markers
- 2× `<line>` for dark-blue section dividers
- 1× `<path>` for a faint decorative corporate background curve
- 1× `<linearGradient>` for the muted background accent
- 1× `<filter id="softShadow">` applied to pane cards
- Multiple `<text>` elements with explicit `width` attributes for title, headers, notes, and bullet narratives
- 4× colored `<rect>` squares for custom insight bullets

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="iceWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="60%" stop-color="#EEF4FC"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M830,0 C1010,70 1050,190 1280,165 L1280,0 Z" fill="url(#iceWash)"/>

  <text x="64" y="58" width="930" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#505050">
    <tspan x="64" dy="0">The US market is the most significant, accounting for over</tspan>
    <tspan fill="#14235A"> 30% of total revenue</tspan>
    <tspan x="64" dy="42">in 2021</tspan>
  </text>

  <text x="64" y="142" width="590" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7A7A7A">
    Revenue by country, USD millions; direct labels remove the need for axes or legends.
  </text>

  <rect x="50" y="174" width="690" height="488" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="770" y="174" width="455" height="488" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="82" y="218" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#505050" text-anchor="middle">
    <tspan x="395">Top 6 Countries by Revenue in $ millions</tspan>
  </text>
  <line x1="82" y1="242" x2="708" y2="242" stroke="#14235A" stroke-width="2"/>

  <text x="818" y="218" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#505050" text-anchor="middle">
    <tspan x="998">Key Highlights</tspan>
  </text>
  <line x1="818" y1="242" x2="1178" y2="242" stroke="#14235A" stroke-width="2"/>

  <text x="92" y="284" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">United States</text>
  <circle cx="226" cy="277" r="6" fill="#14235A"/>
  <rect x="246" y="260" width="430" height="34" rx="7" fill="#14235A"/>
  <text x="608" y="283" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">13,010</text>

  <text x="92" y="344" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">Mexico</text>
  <circle cx="226" cy="337" r="6" fill="#8EAFE1"/>
  <rect x="246" y="320" width="283" height="34" rx="7" fill="#8EAFE1"/>
  <text x="471" y="343" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">8,556</text>

  <text x="92" y="404" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">United Kingdom</text>
  <circle cx="226" cy="397" r="6" fill="#8EAFE1"/>
  <rect x="246" y="380" width="251" height="34" rx="7" fill="#8EAFE1"/>
  <text x="439" y="403" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">7,589</text>

  <text x="92" y="464" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">Canada</text>
  <circle cx="226" cy="457" r="6" fill="#8EAFE1"/>
  <rect x="246" y="440" width="243" height="34" rx="7" fill="#8EAFE1"/>
  <text x="431" y="463" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">7,358</text>

  <text x="92" y="524" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">Japan</text>
  <circle cx="226" cy="517" r="6" fill="#8EAFE1"/>
  <rect x="246" y="500" width="179" height="34" rx="7" fill="#8EAFE1"/>
  <text x="367" y="523" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">5,428</text>

  <text x="92" y="584" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">Brazil</text>
  <circle cx="226" cy="577" r="6" fill="#8EAFE1"/>
  <rect x="246" y="560" width="178" height="34" rx="7" fill="#8EAFE1"/>
  <text x="366" y="583" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">5,401</text>

  <rect x="818" y="276" width="13" height="13" rx="2" fill="#14235A"/>
  <text x="850" y="288" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#505050">
    <tspan x="850">US is the clear revenue anchor</tspan>
  </text>
  <text x="850" y="316" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#626262">
    <tspan x="850">At $13.0B, the US is 52% larger than Mexico</tspan>
    <tspan x="850" dy="22">and contributes more than one-third of the total.</tspan>
  </text>

  <rect x="818" y="382" width="13" height="13" rx="2" fill="#8EAFE1"/>
  <text x="850" y="394" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#505050">
    <tspan x="850">Secondary markets form a tight cluster</tspan>
  </text>
  <text x="850" y="422" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#626262">
    <tspan x="850">Mexico, UK, and Canada sit within a narrow</tspan>
    <tspan x="850" dy="22">performance band, suggesting similar maturity.</tspan>
  </text>

  <rect x="818" y="488" width="13" height="13" rx="2" fill="#8EAFE1"/>
  <text x="850" y="500" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#505050">
    <tspan x="850">Portfolio concentration needs attention</tspan>
  </text>
  <text x="850" y="528" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#626262">
    <tspan x="850">Growth planning should balance US investment</tspan>
    <tspan x="850" dy="22">with risk mitigation across other regions.</tspan>
  </text>

  <rect x="818" y="598" width="135" height="32" rx="16" fill="#EEF4FC"/>
  <text x="837" y="620" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#14235A">2022 focus area</text>
</svg>
```

## Avoid in this skill
- ❌ Full chart axes, gridlines, tick marks, and legends; they dilute the executive-summary feel.
- ❌ Using `<marker-end>` for arrows between panes; if arrows are required, use native `<line>` with direct styling and no inherited markers.
- ❌ Clipping or masking chart bars; keep bars as editable `<rect>` shapes.
- ❌ Dense paragraphs in the right pane; insights should be short, scannable, and aligned to colored square bullets.
- ❌ Low-contrast value labels inside light bars; keep the secondary tint dark enough for white labels or move labels outside.

## Composition notes
- Use a 55–60% left pane for the chart and a 35–40% right pane for highlights, with a generous gutter between them.
- Keep the title area large and quiet; it should state the insight, not merely describe the chart.
- The visual focal point is the top dark-blue bar; all other bars should recede in a lighter tint.
- Align section headers, divider lines, and pane cards precisely so the slide feels structured and consulting-grade.