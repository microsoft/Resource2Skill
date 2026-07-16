# SVG Recipe — Insight-Driven Ranked Bar Chart

## Visual mechanism
A ranked horizontal bar chart is paired with an action title and a focused callout so the slide makes an argument, not just a comparison. The bars are stripped of chart junk, sorted descending, and visually connected to a right-side insight card that explains the executive takeaway.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm white background
- 1× `<rect>` for a soft top accent band behind the title
- 10× `<rect>` for horizontal ranked bars
- 10× `<rect>` for compact country/logo badges beside labels
- 10× `<text>` for category labels
- 10× `<text>` for value labels at the bar ends
- 1× `<rect>` with dashed stroke for the top-two highlight callout box
- 1× `<line>` plus 1× small `<path>` triangle for the annotation arrow
- 1× `<rect>` for the right-side insight card, with shadow filter
- 4× `<text>` blocks for action title, chart subtitle, card headline, and source note
- Several decorative `<path>` shapes for subtle executive-style background arcs and card accent marks
- 3× `<linearGradient>` definitions for background, lead bars, and insight card
- 1× `<filter id="softShadow">` for the insight card
- 1× `<filter id="pinkGlow">` for the emphasis callout

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f6f8f8"/>
    </linearGradient>
    <linearGradient id="leadBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#01717A"/>
      <stop offset="100%" stop-color="#0FA3A8"/>
    </linearGradient>
    <linearGradient id="mutedBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#A8C8CA"/>
      <stop offset="100%" stop-color="#D6E7E8"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#edf5f5"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="pinkGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="128" fill="#F2F7F7"/>
  <path d="M980,20 C1090,58 1190,22 1280,78 L1280,0 L980,0 Z" fill="#DDEEEE" opacity="0.65"/>
  <path d="M1060,666 C1135,615 1210,635 1280,585 L1280,720 L1040,720 Z" fill="#E7F1F1" opacity="0.85"/>

  <text x="72" y="58" width="1080" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#111827">
    China and India produce over 60% of rice among leading producers —
    <tspan fill="#01717A"> nearly 400M tonnes combined</tspan>
  </text>
  <text x="74" y="100" width="820" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#647174">
    Ranked production by country, million tonnes, 2019
  </text>

  <text x="74" y="166" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#1F2937">
    Biggest rice producers
  </text>
  <text x="330" y="166" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#7B878A">
    Bar length shows annual rice production; sorted descending
  </text>

  <line x1="330" y1="190" x2="330" y2="590" stroke="#CDD6D8" stroke-width="1"/>
  <rect x="60" y="198" width="850" height="80" rx="16" fill="none" stroke="#E2ACAC" stroke-width="3" stroke-dasharray="8 7" filter="url(#pinkGlow)"/>
  <text x="684" y="220" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#B76F6F">
    top-two concentration
  </text>

  <rect x="80" y="212" width="34" height="22" rx="5" fill="#DE2910"/><circle cx="91" cy="223" r="4" fill="#FFDE00"/>
  <text x="128" y="229" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#1F2937">China</text>
  <rect x="330" y="211" width="560" height="24" rx="12" fill="url(#leadBar)"/>
  <text x="904" y="229" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#01717A">211</text>

  <rect x="80" y="250" width="34" height="22" rx="5" fill="#FF9933"/><rect x="80" y="257" width="34" height="8" fill="#FFFFFF"/><rect x="80" y="265" width="34" height="7" fill="#138808"/>
  <text x="128" y="267" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#1F2937">India</text>
  <rect x="330" y="249" width="473" height="24" rx="12" fill="url(#leadBar)" opacity="0.92"/>
  <text x="817" y="267" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#01717A">178</text>

  <rect x="80" y="288" width="34" height="22" rx="5" fill="#CE1126"/><rect x="80" y="299" width="34" height="11" fill="#FFFFFF"/>
  <text x="128" y="305" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Indonesia</text>
  <rect x="330" y="287" width="146" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="490" y="305" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">55</text>

  <rect x="80" y="326" width="34" height="22" rx="5" fill="#006A4E"/><circle cx="96" cy="337" r="7" fill="#F42A41"/>
  <text x="128" y="343" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Bangladesh</text>
  <rect x="330" y="325" width="146" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="490" y="343" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">55</text>

  <rect x="80" y="364" width="34" height="22" rx="5" fill="#DA251D"/><rect x="80" y="371" width="34" height="8" fill="#FFFF00"/>
  <text x="128" y="381" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Vietnam</text>
  <rect x="330" y="363" width="114" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="458" y="381" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">43</text>

  <rect x="80" y="402" width="34" height="22" rx="5" fill="#A51931"/><rect x="80" y="409" width="34" height="8" fill="#F4F5F8"/><rect x="80" y="414" width="34" height="4" fill="#2D2A4A"/>
  <text x="128" y="419" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Thailand</text>
  <rect x="330" y="401" width="74" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="418" y="419" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">28</text>

  <rect x="80" y="440" width="34" height="22" rx="5" fill="#FECB00"/><rect x="80" y="447" width="34" height="8" fill="#34B233"/><rect x="80" y="455" width="34" height="7" fill="#EA2839"/>
  <text x="128" y="457" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Myanmar</text>
  <rect x="330" y="439" width="69" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="413" y="457" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">26</text>

  <rect x="80" y="478" width="34" height="22" rx="5" fill="#0038A8"/><rect x="91" y="478" width="23" height="11" fill="#CE1126"/><rect x="91" y="489" width="23" height="11" fill="#FFFFFF"/>
  <text x="128" y="495" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Philippines</text>
  <rect x="330" y="477" width="50" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="394" y="495" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">19</text>

  <rect x="80" y="516" width="34" height="22" rx="5" fill="#01411C"/><rect x="80" y="516" width="10" height="22" fill="#FFFFFF"/>
  <text x="128" y="533" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Pakistan</text>
  <rect x="330" y="515" width="29" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="373" y="533" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">11</text>

  <rect x="80" y="554" width="34" height="22" rx="5" fill="#009B3A"/><path d="M97,558 L111,565 L97,572 L83,565 Z" fill="#FFDF00"/>
  <text x="128" y="571" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#344044">Brazil</text>
  <rect x="330" y="553" width="27" height="24" rx="12" fill="url(#mutedBar)"/>
  <text x="371" y="571" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#566366">10</text>

  <rect x="948" y="184" width="258" height="320" rx="24" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <path d="M948,206 C1008,178 1062,184 1112,215 C1152,240 1178,232 1206,210 L1206,184 L948,184 Z" fill="#D8ECEC"/>
  <text x="982" y="238" width="178" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#01717A" letter-spacing="1.2">EXECUTIVE INSIGHT</text>
  <text x="982" y="298" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#01717A">61%</text>
  <text x="982" y="338" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#1F2937">
    of top-10 output
  </text>
  <text x="982" y="378" width="184" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#5E6B6E">
    comes from China and India, creating a steep drop-off after the two leaders.
  </text>
  <line x1="948" y1="242" x2="916" y2="242" stroke="#E2ACAC" stroke-width="3"/>
  <path d="M916,242 L928,235 L928,249 Z" fill="#E2ACAC"/>

  <text x="74" y="650" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-style="italic" fill="#8A9497">
    Source: FAOSTAT, USDA. Values rounded to nearest million tonnes.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using an embedded chart object or screenshot; build bars, labels, and callouts as editable SVG shapes.
- ❌ Adding vertical gridlines, heavy axes, legends, or tick clutter that competes with the ranking.
- ❌ Using `<marker-end>` on a `<path>` for annotation arrows; use a `<line>` plus a small triangle `<path>` arrowhead.
- ❌ Placing labels inside short bars, where they will collide or become illegible.
- ❌ Applying `clip-path` to bar rectangles or callout boxes; clipping should be reserved for `<image>` elements only.

## Composition notes
- Reserve the top 15–18% of the slide for the action title; it should state the conclusion before the audience reads the chart.
- Keep the chart left-heavy: labels on the far left, bars starting on one clean vertical baseline, values just outside bar ends.
- Use one dominant accent color for the most important bars, then desaturate the remaining bars to reinforce ranking.
- The right-side card should not repeat the chart; it should explain the implication of the highlighted bars in one concise metric.