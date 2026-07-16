# SVG Recipe — Action-Titled Decluttered Bar Chart

## Visual mechanism
A horizontal bar chart is stripped down to only the data-bearing marks: sorted thick bars, left-aligned category labels, and bold values placed directly inside each bar. The slide is led by an action title that states the takeaway before the audience reads the chart.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 1× `<rect>` for a subtle pale-blue title accent rail
- 1× `<text>` with nested `<tspan>` for the action title and emphasized insight phrase
- 1× `<text>` for the small subtitle/context line
- 8× `<text>` for category labels on the left
- 8× `<rect>` for thick horizontal bars, sorted descending
- 8× `<text>` for white percentage labels placed inside the right end of each bar
- 1× `<rect>` for a small source note pill
- 1× `<text>` for the source note
- 1× `<linearGradient>` for premium blue bar fills
- 1× `<filter id="softShadow">` applied lightly to bars for depth without chart clutter

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="barBlue" x1="330" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1D70B8"/>
      <stop offset="72%" stop-color="#2385D6"/>
      <stop offset="100%" stop-color="#40A6F2"/>
    </linearGradient>
    <linearGradient id="titleBlue" x1="0" y1="0" x2="650" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0F5594"/>
      <stop offset="100%" stop-color="#1D70B8"/>
    </linearGradient>
    <filter id="softShadow" x="-8%" y="-20%" width="116%" height="150%">
      <feOffset dx="0" dy="2"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="66" y="52" width="7" height="88" rx="3.5" fill="url(#titleBlue)"/>

  <text x="88" y="76" width="1040" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#202124">
    <tspan x="88" dy="0">Customers rate </tspan>
    <tspan fill="#1D70B8">cleanliness and safety highest</tspan>
    <tspan>, while education trails.</tspan>
  </text>
  <text x="90" y="123" width="940" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#6A717A">
    Sorted share of respondents rating each attribute “excellent” or “very good”
  </text>

  <text x="90" y="222" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Cleanliness</text>
  <rect x="330" y="190" width="756" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="1028" y="222" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">90%</text>

  <text x="90" y="285" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Safety</text>
  <rect x="330" y="253" width="756" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="1028" y="285" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">90%</text>

  <text x="90" y="348" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Welcoming</text>
  <rect x="330" y="316" width="739" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="1011" y="348" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">88%</text>

  <text x="90" y="411" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Accessibility</text>
  <rect x="330" y="379" width="739" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="1011" y="411" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">88%</text>

  <text x="90" y="474" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Value for Cost</text>
  <rect x="330" y="442" width="655" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="927" y="474" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">78%</text>

  <text x="90" y="537" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Overall Experience</text>
  <rect x="330" y="505" width="622" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="894" y="537" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">74%</text>

  <text x="90" y="600" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Easy to Navigate</text>
  <rect x="330" y="568" width="580" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="852" y="600" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">69%</text>

  <text x="90" y="663" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#333333">Educational</text>
  <rect x="330" y="631" width="563" height="48" rx="9" fill="url(#barBlue)" filter="url(#softShadow)"/>
  <text x="835" y="663" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" text-anchor="end" fill="#FFFFFF">67%</text>

  <rect x="1032" y="638" width="134" height="30" rx="15" fill="#EEF5FB"/>
  <text x="1050" y="658" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="600" fill="#51708B">n = 1,248</text>
</svg>
```

## Avoid in this skill
- ❌ Visible X/Y axes, tick marks, gridlines, legends, or chart frames; they undermine the decluttered premise.
- ❌ Putting data labels outside the bars unless bars are too short to hold the value legibly.
- ❌ Using many unrelated bar colors; this technique works best with one strong accent color and one clear narrative.
- ❌ Unsorted bars; random ordering forces the audience to work to find the takeaway.
- ❌ Thin bars with large gaps; the bars should feel substantial and easy to compare.

## Composition notes
- Keep the action title in the top 15–20% of the slide; it should read like the conclusion, not a neutral chart label.
- Reserve a fixed left column for category labels and align all bars to one clean vertical start line.
- Use thick bars with modest gaps so the chart feels authoritative and executive-ready.
- Keep negative space on the right side of shorter bars; the absence of axes makes the ranking visually immediate.