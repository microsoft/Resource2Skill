# SVG Recipe — Semi-Circular Data Progress Arcs

## Visual mechanism
A row of four half-donut progress indicators converts percentages into quick visual comparisons: each metric has a pale gray semi-circular track with a colored arc overlay showing completion. The percentage, label, and descriptive copy sit directly beneath the arc, using matched color to bind each KPI into a compact vertical module.

## SVG primitives needed
- 8× `<path>` for the semi-circular arcs: 4 pale gray background tracks and 4 colored progress arcs.
- 13× `<text>` for the title, subtitle, four percentages, four metric labels, and four multiline descriptions.
- Optional 1× `<rect>` for a clean white slide background.
- No images are needed; the technique should remain fully editable vector geometry.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Global title -->
  <text x="640" y="84" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="700" letter-spacing="14"
        fill="#9E9E9E">PERCENTAGES</text>

  <text x="640" y="124" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#9E9E9E">
    <tspan x="640" dy="0">This is a demo text you may write a brief text here to explain the title or if you think you do</tspan>
    <tspan x="640" dy="26">not need this you may consider to delete the text box.</tspan>
  </text>

  <!-- Shared arc style: radius 119, stroke 25, flat caps -->
  <!-- Column 1: 60% -->
  <path d="M 66 386 A 119 119 0 0 1 304 386"
        fill="none" stroke="#F1F1F1" stroke-width="25" stroke-linecap="butt"/>
  <path d="M 66 386 A 119 119 0 0 1 222 273"
        fill="none" stroke="#E91E63" stroke-width="25" stroke-linecap="butt"/>

  <text x="185" y="401" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#E91E63">60%</text>
  <text x="185" y="445" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29" font-weight="800" fill="#E91E63">GRAPHIC DESIGN</text>
  <text x="185" y="486" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" fill="#9E9E9E">
    <tspan x="185" dy="0">Here You Should Add</tspan>
    <tspan x="185" dy="32">Some Brief Text to Explain</tspan>
    <tspan x="185" dy="32">Main Title</tspan>
  </text>

  <!-- Column 2: 70% -->
  <path d="M 371 386 A 119 119 0 0 1 609 386"
        fill="none" stroke="#F1F1F1" stroke-width="25" stroke-linecap="butt"/>
  <path d="M 371 386 A 119 119 0 0 1 560 290"
        fill="none" stroke="#009688" stroke-width="25" stroke-linecap="butt"/>

  <text x="490" y="401" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#009688">70%</text>
  <text x="490" y="445" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29" font-weight="800" fill="#009688">WEB DESIGN</text>
  <text x="490" y="486" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" fill="#9E9E9E">
    <tspan x="490" dy="0">Here You Should Add</tspan>
    <tspan x="490" dy="32">Some Brief Text to Explain</tspan>
    <tspan x="490" dy="32">Main Title</tspan>
  </text>

  <!-- Column 3: 50% -->
  <path d="M 676 386 A 119 119 0 0 1 914 386"
        fill="none" stroke="#F1F1F1" stroke-width="25" stroke-linecap="butt"/>
  <path d="M 676 386 A 119 119 0 0 1 795 267"
        fill="none" stroke="#8BC34A" stroke-width="25" stroke-linecap="butt"/>

  <text x="795" y="401" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#8BC34A">50%</text>
  <text x="795" y="445" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29" font-weight="800" fill="#8BC34A">VIDEO EDITING</text>
  <text x="795" y="486" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" fill="#9E9E9E">
    <tspan x="795" dy="0">Here You Should Add</tspan>
    <tspan x="795" dy="32">Some Brief Text to Explain</tspan>
    <tspan x="795" dy="32">Main Title</tspan>
  </text>

  <!-- Column 4: 90% -->
  <path d="M 981 386 A 119 119 0 0 1 1219 386"
        fill="none" stroke="#F1F1F1" stroke-width="25" stroke-linecap="butt"/>
  <path d="M 981 386 A 119 119 0 0 1 1213 349"
        fill="none" stroke="#1F7CB5" stroke-width="25" stroke-linecap="butt"/>

  <text x="1100" y="401" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#1F7CB5">90%</text>
  <text x="1100" y="445" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29" font-weight="800" fill="#1F7CB5">UX DESIGN</text>
  <text x="1100" y="486" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" fill="#9E9E9E">
    <tspan x="1100" dy="0">Here You Should Add</tspan>
    <tspan x="1100" dy="32">Some Brief Text to Explain</tspan>
    <tspan x="1100" dy="32">Main Title</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rasterizing the arcs as PNGs; use editable `<path>` arc strokes instead.
- ❌ `stroke-linecap="round"` if you want the clean tutorial-style flat arc ends.
- ❌ Full donut charts; the key value of this technique is saving vertical space with semi-circles.
- ❌ Overcrowding each module with legends or axes; the color and percentage already explain the data.
- ❌ Using `<mask>`, `<clipPath>` on non-image shapes, or `<textPath>` for curved labels; these are unnecessary and may not translate cleanly.

## Composition notes
- Keep the four arc centers evenly spaced across the slide, with generous side margins and equal column widths.
- Reserve the top 20–25% of the canvas for the spaced uppercase title and muted subtitle.
- Place the percentage inside the open lower half of each arc, then stack the category label and description beneath it.
- Use a light gray track and saturated accent colors; repeat each accent color in both the arc and its text label for instant grouping.