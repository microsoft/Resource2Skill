# SVG Recipe — Minimalist High-Signal Data Dashboard (Data-Ink Optimization)

## Visual mechanism
A high-signal dashboard removes chart junk and lets whitespace, sorting, direct labels, and selective accent color do the work. The layout uses faint card boundaries, muted grayscale data, and one or two saturated highlights to make the key insight immediately visible.

## SVG primitives needed
- 1× `<rect>` for the faint off-white slide background
- 4× `<rect>` for white dashboard cards with ultra-light borders
- 3× `<rect>` for compact KPI accent rules and micro progress indicators
- 5× `<rect>` for sorted horizontal bar chart values
- 1× `<line>` for a barely visible bar-chart baseline
- 5× `<line>` for minimalist distribution ticks in the KPI card
- 2× `<path>` for editable line/sparkline charts with no axes
- 8× `<circle>` for line-chart data points and highlighted endpoints
- Multiple `<text>` elements with explicit `width` for title, subtitles, KPI values, direct data labels, and muted annotations
- 1× `<defs>` block for shared color-neutral styling if desired; no gradients or shadows are needed for this data-ink style

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
      .title { font-family: Segoe UI, Microsoft YaHei, sans-serif; fill:#3C3C3C; font-weight:700; }
      .label { font-family: Segoe UI, Microsoft YaHei, sans-serif; fill:#8C8C8C; }
      .dark { font-family: Segoe UI, Microsoft YaHei, sans-serif; fill:#3C3C3C; }
      .muted { font-family: Segoe UI, Microsoft YaHei, sans-serif; fill:#9A9A9A; }
      .smallbold { font-family: Segoe UI, Microsoft YaHei, sans-serif; fill:#555555; font-weight:700; }
    </style>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FAFAFA"/>

  <text x="64" y="64" width="640" font-size="30" class="title">Q3 Executive Dashboard</text>
  <text x="64" y="96" width="720" font-size="15" class="label">Performance overview sorted by impact; non-essential ink removed.</text>
  <text x="1052" y="67" width="164" font-size="13" class="muted" text-anchor="end">Updated Sep 30</text>

  <!-- KPI cards -->
  <rect x="64" y="128" width="258" height="132" rx="18" fill="#FFFFFF" stroke="#E8E8E8"/>
  <rect x="92" y="232" width="72" height="4" rx="2" fill="#0078D4"/>
  <text x="92" y="165" width="180" font-size="13" class="muted">Revenue</text>
  <text x="92" y="210" width="190" font-size="40" class="title">$2.72M</text>
  <text x="236" y="211" width="50" font-size="14" fill="#0078D4" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="700">+18%</text>
  <text x="92" y="247" width="170" font-size="12" class="label">vs. prior quarter</text>

  <rect x="346" y="128" width="258" height="132" rx="18" fill="#FFFFFF" stroke="#E8E8E8"/>
  <rect x="374" y="232" width="38" height="4" rx="2" fill="#BDBDBD"/>
  <text x="374" y="165" width="180" font-size="13" class="muted">Gross Margin</text>
  <text x="374" y="210" width="160" font-size="40" class="title">42.8%</text>
  <text x="523" y="211" width="50" font-size="14" class="muted" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="700">-1.2</text>
  <text x="374" y="247" width="170" font-size="12" class="label">stable range</text>

  <rect x="628" y="128" width="258" height="132" rx="18" fill="#FFFFFF" stroke="#E8E8E8"/>
  <text x="656" y="165" width="190" font-size="13" class="muted">At-risk Accounts</text>
  <text x="656" y="210" width="96" font-size="40" fill="#D2222D" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="700">17</text>
  <text x="746" y="211" width="70" font-size="14" fill="#D2222D" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="700">▲ 5</text>
  <line x1="658" y1="234" x2="658" y2="248" stroke="#D2222D" stroke-width="2"/>
  <line x1="690" y1="224" x2="690" y2="248" stroke="#BDBDBD" stroke-width="2"/>
  <line x1="722" y1="216" x2="722" y2="248" stroke="#BDBDBD" stroke-width="2"/>
  <line x1="754" y1="238" x2="754" y2="248" stroke="#BDBDBD" stroke-width="2"/>
  <line x1="786" y1="229" x2="786" y2="248" stroke="#BDBDBD" stroke-width="2"/>

  <rect x="910" y="128" width="306" height="132" rx="18" fill="#FFFFFF" stroke="#E8E8E8"/>
  <text x="938" y="165" width="200" font-size="13" class="muted">Pipeline Conversion</text>
  <text x="938" y="210" width="140" font-size="40" class="title">31.4%</text>
  <path d="M1088 224 C1110 205, 1128 214, 1148 196 S1190 184, 1196 158" fill="none" stroke="#0078D4" stroke-width="3" stroke-linecap="round"/>
  <circle cx="1196" cy="158" r="5" fill="#0078D4"/>
  <text x="1088" y="247" width="108" font-size="12" class="label">6-week trend</text>

  <!-- Main sorted bar chart card -->
  <rect x="64" y="292" width="640" height="348" rx="20" fill="#FFFFFF" stroke="#E8E8E8"/>
  <text x="96" y="337" width="310" font-size="20" class="title">Sales by category</text>
  <text x="96" y="363" width="430" font-size="13" class="label">Sorted descending; direct labels replace x-axis and gridlines.</text>
  <line x1="246" y1="404" x2="246" y2="580" stroke="#EDEDED" stroke-width="1"/>

  <text x="96" y="416" width="120" font-size="14" class="dark">Bikes</text>
  <rect x="246" y="400" width="372" height="24" rx="4" fill="#0078D4"/>
  <text x="632" y="418" width="60" font-size="13" class="smallbold">$1.25M</text>

  <text x="96" y="456" width="120" font-size="14" class="dark">Components</text>
  <rect x="246" y="440" width="253" height="24" rx="4" fill="#CFCFCF"/>
  <text x="512" y="458" width="60" font-size="13" class="smallbold">$850K</text>

  <text x="96" y="496" width="120" font-size="14" class="dark">Clothing</text>
  <rect x="246" y="480" width="125" height="24" rx="4" fill="#D8D8D8"/>
  <text x="384" y="498" width="60" font-size="13" class="smallbold">$420K</text>

  <text x="96" y="536" width="120" font-size="14" class="dark">Accessories</text>
  <rect x="246" y="520" width="45" height="24" rx="4" fill="#D8D8D8"/>
  <text x="304" y="538" width="60" font-size="13" class="smallbold">$150K</text>

  <text x="96" y="576" width="120" font-size="14" class="dark">Services</text>
  <rect x="246" y="560" width="15" height="24" rx="4" fill="#D8D8D8"/>
  <text x="274" y="578" width="60" font-size="13" class="smallbold">$50K</text>

  <!-- Secondary line chart card -->
  <rect x="736" y="292" width="480" height="348" rx="20" fill="#FFFFFF" stroke="#E8E8E8"/>
  <text x="768" y="337" width="300" font-size="20" class="title">Weekly active accounts</text>
  <text x="768" y="363" width="360" font-size="13" class="label">Only endpoints and the intervention week are emphasized.</text>
  <line x1="782" y1="520" x2="1182" y2="520" stroke="#EFEFEF" stroke-width="1"/>
  <path d="M790 510 C828 498, 855 492, 892 500 S966 522, 1002 486 S1074 430, 1114 404 S1160 376, 1180 348" fill="none" stroke="#C9C9C9" stroke-width="3" stroke-linecap="round"/>
  <path d="M1002 486 C1040 456, 1074 430, 1114 404 S1160 376, 1180 348" fill="none" stroke="#0078D4" stroke-width="4" stroke-linecap="round"/>
  <circle cx="790" cy="510" r="4" fill="#C9C9C9"/>
  <circle cx="892" cy="500" r="4" fill="#C9C9C9"/>
  <circle cx="1002" cy="486" r="6" fill="#FFFFFF" stroke="#0078D4" stroke-width="3"/>
  <circle cx="1114" cy="404" r="4" fill="#0078D4"/>
  <circle cx="1180" cy="348" r="7" fill="#0078D4"/>
  <text x="768" y="556" width="70" font-size="12" class="label">Week 1</text>
  <text x="968" y="556" width="120" font-size="12" fill="#0078D4" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="700">Pricing reset</text>
  <text x="1138" y="556" width="70" font-size="12" class="label">Week 12</text>
  <text x="1088" y="342" width="88" font-size="13" fill="#0078D4" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-weight="700">+24%</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy chart frames, dense gridlines, legends, axis tick clutter, or decorative borders; they contradict the data-ink optimization principle.
- ❌ Gradients, shadows, 3D bars, pictorial fills, and background textures; use flat color and whitespace instead.
- ❌ Separate legends when direct labeling can be placed next to the data mark.
- ❌ Equal emphasis on every series or category; the technique depends on muted context plus one high-contrast insight.
- ❌ Unsorted categorical bars; descending order is part of the visual mechanism.

## Composition notes
- Keep the slide background nearly white and use white cards with very light gray strokes so structure is implied, not shouted.
- Reserve saturated color for one primary finding and, if needed, one alert state; all other data should sit in gray.
- Replace axes and legends with direct labels positioned beside the marks, especially on bar charts.
- Use generous margins between cards; negative space should create hierarchy more than lines or boxes do.