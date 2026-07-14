# SVG Recipe — Dual-Scenario Waterfall Bridge

## Visual mechanism
Overlay two manually built waterfall paths on the same categorical axis, shifting the second scenario slightly to the right so both paths remain visible. Use darker bars for the base scenario and lighter bars for the stretch scenario, with the final bars emphasized to make the outcome delta easy to compare.

## SVG primitives needed
- 1× `<marker>` for the summary arrowhead.
- 1× `<line>` for the start-to-stretch-final comparison arrow; the line carries its own `marker-end`.
- 9× `<rect>` for waterfall bars: one shared start, three base increments, three stretch increments, and two final totals.
- 6× `<rect>` for baseline, subtle gridlines, and legend swatches.
- 20+× `<text>` for title, subtitle, labels, values, legend, and callout.
- Optional `<g>` groups for semantic layering only; avoid inherited arrow markers.

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowTip" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#595959"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <g id="title-block">
    <text x="70" y="70" width="1080" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111111">
      Stretch scenario adds $262M versus base budget
    </text>
    <text x="72" y="106" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#666666">
      Dual-scenario waterfall bridge for Sales Budget 20X2
    </text>
  </g>

  <g id="legend">
    <rect x="905" y="72" width="18" height="18" fill="#2F5496"/>
    <text x="932" y="87" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#333333">Base increments</text>
    <rect x="905" y="101" width="18" height="18" fill="#9BC2E6"/>
    <text x="932" y="116" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#333333">Stretch increments</text>
    <rect x="1080" y="72" width="18" height="18" fill="#808080"/>
    <text x="1107" y="87" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#333333">Base totals</text>
    <rect x="1080" y="101" width="18" height="18" fill="#D9D9D9"/>
    <text x="1107" y="116" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#333333">Stretch total</text>
  </g>

  <g id="chart-frame">
    <rect x="105" y="290" width="1070" height="1.5" fill="#E7E7E7"/>
    <rect x="105" y="370" width="1070" height="1.5" fill="#E7E7E7"/>
    <rect x="105" y="450" width="1070" height="1.5" fill="#E7E7E7"/>
    <rect x="105" y="530" width="1070" height="1.5" fill="#E7E7E7"/>
    <rect x="105" y="610" width="1070" height="2.5" fill="#BFBFBF"/>
    <text x="66" y="294" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#999999">2.0B</text>
    <text x="66" y="374" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#999999">1.5B</text>
    <text x="66" y="454" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#999999">1.0B</text>
    <text x="66" y="614" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#999999">0</text>
  </g>

  <g id="stretch-scenario-bars">
    <rect x="386" y="346" width="92" height="24" fill="#9BC2E6" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="606" y="312" width="92" height="34" fill="#9BC2E6" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="826" y="271" width="92" height="42" fill="#9BC2E6" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="1046" y="271" width="92" height="339" fill="#D9D9D9" stroke="#FFFFFF" stroke-width="1"/>
  </g>

  <g id="base-scenario-bars">
    <rect x="130" y="370" width="110" height="240" fill="#808080" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="360" y="357" width="92" height="13" fill="#2F5496" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="580" y="338" width="92" height="19" fill="#2F5496" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="800" y="312" width="92" height="26" fill="#2F5496" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="1020" y="312" width="92" height="298" fill="#A6A6A6" stroke="#FFFFFF" stroke-width="1"/>
  </g>

  <g id="summary-arrow">
    <line x1="236" y1="354" x2="1092" y2="270" stroke="#595959" stroke-width="3" marker-end="url(#arrowTip)"/>
    <text x="730" y="244" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#595959">
      Stretch path reaches $2,122M
    </text>
  </g>

  <g id="value-labels">
    <text x="142" y="500" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">1,500</text>
    <text x="406" y="342" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#6D9ED1" text-anchor="middle">+150</text>
    <text x="380" y="354" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2F5496" text-anchor="middle">+80</text>
    <text x="626" y="307" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#6D9ED1" text-anchor="middle">+210</text>
    <text x="600" y="333" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2F5496" text-anchor="middle">+120</text>
    <text x="846" y="265" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#6D9ED1" text-anchor="middle">+262</text>
    <text x="820" y="307" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2F5496" text-anchor="middle">+160</text>
    <text x="1065" y="292" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#333333" text-anchor="middle">2,122</text>
    <text x="1040" y="334" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">1,860</text>
  </g>

  <g id="category-labels">
    <text x="120" y="646" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333" text-anchor="middle">FC 20X1</text>
    <text x="340" y="646" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333" text-anchor="middle">New Products</text>
    <text x="560" y="646" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333" text-anchor="middle">M&amp;A</text>
    <text x="780" y="646" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333" text-anchor="middle">Online</text>
    <text x="1000" y="646" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333" text-anchor="middle">Budget 20X2</text>
  </g>

  <g id="final-delta-callout">
    <rect x="1015" y="206" width="180" height="44" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="1"/>
    <text x="1030" y="233" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#2F5496">
      Delta: +$262M
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Native SVG charting shortcuts such as `<path>` area traces or custom polygons for bars; use editable `<rect>` bars instead.
- ❌ Inheriting `marker-end` from a parent `<g>`; every arrow `<line>` must declare its own marker.
- ❌ Filters, masks, or clipping on chart bars or labels; they can cause rasterization or uneditable output.
- ❌ Rotated category labels; keep labels horizontal so PowerPoint text frames remain stable.
- ❌ Exact overlap between the two scenarios; use a small horizontal offset so both bars are readable.

## Composition notes
- Reserve the upper 20% of the slide for the takeaway title, subtitle, and compact legend.
- Keep the chart baseline low, around y=610, so tall final totals have enough vertical space.
- Draw the lighter stretch scenario first, shifted 20–30 px right, then draw the darker base scenario on top.
- Make the final category the visual focus with larger total bars, a delta callout, and one clean summary arrow.