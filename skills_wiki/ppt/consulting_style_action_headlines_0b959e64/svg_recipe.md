# SVG Recipe — Consulting-Style Action Headlines

## Visual mechanism
Use the top title area as a complete “so what” sentence that states the conclusion before the audience reads the evidence. A smaller descriptive subtitle and a thin separator line create a clean consulting-style hierarchy above the chart or content body.

## SVG primitives needed
- 9× `<rect>` for the slide background, chart panel, plot area, bars, legend chip, and insight callout
- 5× `<line>` for the title separator and chart gridlines
- 5× `<circle>` for growth-rate markers and legend marker
- 28× `<text>` for the action headline, subtitle, chart labels, values, callout, and source note
- 3× `<g>` for grouping the title block, chart body, and right-side insight callout

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <g font-family="Segoe UI, Microsoft YaHei, sans-serif">
    <text x="60" y="58" width="1120" font-size="30" font-weight="700" fill="#262626">
      Hospitals are now the largest and fastest-growing healthcare segment
    </text>
    <text x="60" y="92" width="1120" font-size="17" font-weight="400" fill="#808080">
      Industry segments by annual turnover and five-year CAGR
    </text>
    <line x1="60" y1="120" x2="1220" y2="120" stroke="#c8c8c8" stroke-width="1"/>
  </g>

  <g transform="translate(70 155)" font-family="Segoe UI, Microsoft YaHei, sans-serif">
    <text x="0" y="0" width="820" font-size="18" font-weight="600" fill="#404040">
      Segment turnover, 2024
    </text>

    <rect x="0" y="24" width="820" height="420" fill="#fafafa" stroke="#e6e6e6" stroke-width="1"/>
    <rect x="64" y="64" width="700" height="300" fill="#ffffff" stroke="#eeeeee" stroke-width="1"/>

    <line x1="64" y1="64" x2="764" y2="64" stroke="#e0e0e0" stroke-width="1"/>
    <line x1="64" y1="164" x2="764" y2="164" stroke="#e0e0e0" stroke-width="1"/>
    <line x1="64" y1="264" x2="764" y2="264" stroke="#e0e0e0" stroke-width="1"/>
    <line x1="64" y1="364" x2="764" y2="364" stroke="#bfbfbf" stroke-width="1"/>

    <text x="8" y="68" width="46" font-size="12" fill="#8a8a8a">600</text>
    <text x="8" y="168" width="46" font-size="12" fill="#8a8a8a">400</text>
    <text x="8" y="268" width="46" font-size="12" fill="#8a8a8a">200</text>
    <text x="8" y="368" width="46" font-size="12" fill="#8a8a8a">0</text>
    <text x="8" y="48" width="160" font-size="12" fill="#8a8a8a">Annual turnover, $B</text>

    <rect x="120" y="94" width="72" height="270" fill="#1f77b4"/>
    <rect x="275" y="184" width="72" height="180" fill="#b8c0c8"/>
    <rect x="430" y="224" width="72" height="140" fill="#b8c0c8"/>
    <rect x="585" y="274" width="72" height="90" fill="#b8c0c8"/>

    <circle cx="156" cy="124" r="8" fill="#ffffff" stroke="#1f77b4" stroke-width="3"/>
    <circle cx="311" cy="264" r="8" fill="#ffffff" stroke="#7f8c99" stroke-width="3"/>
    <circle cx="466" cy="284" r="8" fill="#ffffff" stroke="#7f8c99" stroke-width="3"/>
    <circle cx="621" cy="164" r="8" fill="#ffffff" stroke="#7f8c99" stroke-width="3"/>

    <text x="103" y="388" width="110" font-size="13" font-weight="600" fill="#404040">Hospitals</text>
    <text x="258" y="388" width="110" font-size="13" fill="#606060">Pharma</text>
    <text x="413" y="388" width="110" font-size="13" fill="#606060">Devices</text>
    <text x="568" y="388" width="120" font-size="13" fill="#606060">Digital care</text>

    <text x="112" y="86" width="95" font-size="13" font-weight="700" fill="#1f77b4">$540B</text>
    <text x="270" y="176" width="95" font-size="13" fill="#606060">$360B</text>
    <text x="425" y="216" width="95" font-size="13" fill="#606060">$280B</text>
    <text x="580" y="266" width="95" font-size="13" fill="#606060">$180B</text>

    <text x="170" y="128" width="82" font-size="12" font-weight="700" fill="#1f77b4">12% CAGR</text>
    <text x="325" y="268" width="72" font-size="12" fill="#606060">5% CAGR</text>
    <text x="480" y="288" width="72" font-size="12" fill="#606060">4% CAGR</text>
    <text x="635" y="168" width="82" font-size="12" fill="#606060">10% CAGR</text>

    <rect x="562" y="36" width="20" height="10" fill="#1f77b4"/>
    <text x="590" y="46" width="100" font-size="12" fill="#606060">Turnover</text>
    <circle cx="690" cy="41" r="6" fill="#ffffff" stroke="#1f77b4" stroke-width="2"/>
    <text x="704" y="46" width="90" font-size="12" fill="#606060">Growth</text>
  </g>

  <g transform="translate(940 210)" font-family="Segoe UI, Microsoft YaHei, sans-serif">
    <rect x="0" y="0" width="270" height="230" fill="#f5f8fb" stroke="#d9e3ec" stroke-width="1"/>
    <rect x="0" y="0" width="7" height="230" fill="#1f77b4"/>
    <text x="24" y="42" width="220" font-size="18" font-weight="700" fill="#262626">Implication</text>
    <text x="24" y="82" width="220" font-size="15" fill="#4d4d4d">Prioritize hospital</text>
    <text x="24" y="106" width="220" font-size="15" fill="#4d4d4d">partnerships in the</text>
    <text x="24" y="130" width="220" font-size="15" fill="#4d4d4d">next commercial cycle.</text>
    <text x="24" y="170" width="220" font-size="13" fill="#808080">Largest revenue pool plus</text>
    <text x="24" y="190" width="220" font-size="13" fill="#808080">strongest growth trajectory.</text>
  </g>

  <text x="70" y="690" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#8a8a8a">
    Source: Slide Science analysis; company filings; market interviews
  </text>
</svg>
```

## Avoid in this skill
- ❌ Descriptive noun-phrase titles like “Market Share by Segment” when the slide should state the conclusion.
- ❌ Centered or decorative titles; consulting action headlines should usually be left-aligned and sentence-like.
- ❌ Overlong headlines that wrap into three or more lines and consume the chart area.
- ❌ Applying filters or shadows to the title block; keep text native and editable in PowerPoint.
- ❌ Omitting explicit `width` on text elements, which can cause text frames to drift when rendered in PowerPoint.

## Composition notes
- Keep the title block in the top 10–15% of the slide: action headline first, descriptive subtitle second, separator line third.
- Use the body area only for evidence that supports the action headline; the chart should not compete typographically with the title.
- Maintain a strong left margin, typically 50–70 px on a 1280×720 canvas, so title, chart, and source align cleanly.
- Use one accent color to connect the headline’s key claim with the supporting evidence in the chart.