# SVG Recipe — Consulting-Style "High Data-to-Ink" Chart (Think-Cell Clone)

## Visual mechanism
A minimalist column chart removes axes, legends, borders, and grid clutter, placing values directly on bars and using one dark accent bar to focus the story. A floating bracket / difference arrow above the columns states the executive takeaway before the audience has to calculate it.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a thin title accent rule
- 7× `<rect>` for the chart columns, with one final column in navy accent
- 1× `<line>` for the only retained axis element: the x-axis baseline
- 1× `<path>` for the think-cell-style difference bracket
- 1× `<path>` for the custom geometric arrowhead at the target bar
- 1× `<rect>` for the floating insight label pill
- 1× `<filter id="softShadow">` applied to the insight label pill for subtle keynote polish
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, direct data labels, years, source note, and insight annotation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Executive title block -->
  <rect x="70" y="56" width="54" height="4" fill="#1F497D"/>
  <text x="70" y="104" width="920" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="700" fill="#333333">
    Net sales increased fivefold since 2015
  </text>
  <text x="70" y="142" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#666666">
    EUR mn, German Business Unit, 2015–2021
  </text>

  <!-- Small top-right context note -->
  <text x="930" y="92" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#8A8A8A" text-anchor="end">
    Illustrative management-report style
  </text>

  <!-- Chart baseline only: no y-axis, no gridlines, no legend -->
  <line x1="220" y1="600" x2="1030" y2="600" stroke="#B8B8B8" stroke-width="1.6"/>

  <!-- Bars: values 3, 5, 9, 12, 8, 13, 15; max height 280 -->
  <rect x="250" y="544" width="72" height="56" fill="#D9D9D9"/>
  <rect x="360" y="507" width="72" height="93" fill="#D9D9D9"/>
  <rect x="470" y="432" width="72" height="168" fill="#D9D9D9"/>
  <rect x="580" y="376" width="72" height="224" fill="#D9D9D9"/>
  <rect x="690" y="451" width="72" height="149" fill="#D9D9D9"/>
  <rect x="800" y="357" width="72" height="243" fill="#D9D9D9"/>
  <rect x="910" y="320" width="72" height="280" fill="#1F497D"/>

  <!-- Direct data labels above each bar -->
  <text x="286" y="532" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#404040">3</text>
  <text x="396" y="495" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#404040">5</text>
  <text x="506" y="420" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#404040">9</text>
  <text x="616" y="364" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#404040">12</text>
  <text x="726" y="439" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#404040">8</text>
  <text x="836" y="345" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#404040">13</text>
  <text x="946" y="308" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#1F497D">15</text>

  <!-- Category labels -->
  <text x="286" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2015</text>
  <text x="396" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2016</text>
  <text x="506" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2017</text>
  <text x="616" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2018</text>
  <text x="726" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2019</text>
  <text x="836" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#555555">2020</text>
  <text x="946" y="628" width="72" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#1F497D">2021</text>

  <!-- Think-cell-style difference bracket and arrow -->
  <path d="M286 516 L286 282 L946 282 L946 304"
        fill="none" stroke="#1F497D" stroke-width="2.4" stroke-linecap="square" stroke-linejoin="miter"/>
  <path d="M936 304 L956 304 L946 321 Z" fill="#1F497D"/>

  <!-- Floating insight pill -->
  <rect x="518" y="248" width="196" height="48" rx="4" fill="#1F497D" filter="url(#softShadow)"/>
  <text x="616" y="279" width="196" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">
    +400% growth
  </text>

  <!-- Minimal left-side chart descriptor instead of a y-axis -->
  <text x="220" y="244" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#404040">Net Sales</text>
  <text x="220" y="264" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#777777">EUR mn</text>

  <!-- Footer source note -->
  <text x="70" y="682" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#9A9A9A">
    Source: Internal BI Master Report; values rounded
  </text>
</svg>
```

## Avoid in this skill
- ❌ Full y-axis scaffolding, dense gridlines, legends, and chart borders; they defeat the high data-to-ink effect
- ❌ Native SVG `<marker>` arrowheads or `marker-end` on `<path>`; draw the arrowhead as a small editable `<path>` instead
- ❌ Overusing gradients, shadows, or 3D effects on columns; consulting charts should feel precise and analytical
- ❌ Labels placed far from their data marks; keep values directly above bars to eliminate visual lookup
- ❌ Multiple accent colors unless the business story truly requires multiple highlighted series

## Composition notes
- Reserve the top 25–35% of the slide for the title, subtitle, and difference arrow; the bars should sit lower with generous white space.
- Use muted gray for all context bars and a single navy or black accent for the focal bar and bracket annotation.
- Keep the chart horizontally centered and wide, with column gaps roughly 40–60% of bar width.
- Replace axes with direct labels: value above each bar, year below each bar, and only a tiny descriptor for units.