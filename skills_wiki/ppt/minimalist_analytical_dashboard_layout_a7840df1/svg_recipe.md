# SVG Recipe — Minimalist Analytical Dashboard Layout

## Visual mechanism
A presentation slide is styled like a premium BI dashboard: a sparse KPI ribbon at the top, a large contextual hero image in the middle, and three stripped-down analytical charts along the bottom. The look depends on generous whitespace, very light dividers, no chart axes, and one muted accent color used consistently for emphasis.

## SVG primitives needed
- 1× full-slide `<rect>` for the off-white dashboard background.
- 4× rounded `<rect>` for the year slicer tabs, with one active dark tab.
- 8× `<text>` for KPI values and uppercase KPI labels.
- 3× thin `<line>` for horizontal zoning/dividers.
- 1× `<image>` for the central transparent-background hero product photo.
- 2× `<path>` for left/right navigation chevrons around the hero image.
- 3× rounded `<rect>` for bottom chart cards/panels.
- 7× `<rect>` for minimalist horizontal bars and column bars.
- 3× stroked `<circle>` for the donut chart rings/segments.
- 1× `<path>` for a small trend sparkline.
- 1× `<filter id="softShadow">` applied to chart cards and the hero image container.
- 1× `<linearGradient>` for subtle accent fills in chart bars.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5A9696"/>
      <stop offset="100%" stop-color="#8DB8B8"/>
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

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#F8F9FA"/>

  <!-- Header -->
  <text x="56" y="52" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#333333">Sales Dashboard</text>
  <text x="56" y="78" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A8A8A">EXECUTIVE PERFORMANCE SNAPSHOT</text>

  <!-- Year slicer -->
  <rect x="905" y="32" width="68" height="32" rx="16" fill="#F8F9FA" stroke="#CFCFCF"/>
  <text x="939" y="53" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A8A8A">2019</text>

  <rect x="984" y="32" width="68" height="32" rx="16" fill="#F8F9FA" stroke="#CFCFCF"/>
  <text x="1018" y="53" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A8A8A">2020</text>

  <rect x="1063" y="32" width="68" height="32" rx="16" fill="#F8F9FA" stroke="#CFCFCF"/>
  <text x="1097" y="53" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A8A8A">2021</text>

  <rect x="1142" y="32" width="68" height="32" rx="16" fill="#333333" stroke="#333333"/>
  <text x="1176" y="53" width="68" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">2022</text>

  <!-- KPI ribbon -->
  <text x="210" y="126" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#333333">746K</text>
  <text x="210" y="154" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A8A8A">SALE</text>

  <text x="440" y="126" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#333333">21.4%</text>
  <text x="440" y="154" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A8A8A">GROWTH</text>

  <text x="670" y="126" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#333333">614K</text>
  <text x="670" y="154" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A8A8A">PRE SALE</text>

  <text x="900" y="126" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#333333">473K</text>
  <text x="900" y="154" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#8A8A8A">BUDGET</text>

  <line x1="96" y1="178" x2="1184" y2="178" stroke="#E1E1E1" stroke-width="1"/>

  <!-- Hero zone -->
  <ellipse cx="640" cy="382" rx="250" ry="22" fill="#DDE4E4" opacity="0.55"/>
  <image x="392" y="210" width="496" height="210" filter="url(#softShadow)"
         href="https://images.example.com/transparent-premium-electric-car-side-view.png"/>

  <path d="M168 320 L146 346 L168 372" fill="none" stroke="#B8B8B8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1112 320 L1134 346 L1112 372" fill="none" stroke="#B8B8B8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="640" y="448" width="520" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">Model mix performance · current year selection</text>
  <line x1="96" y1="480" x2="1184" y2="480" stroke="#E6E6E6" stroke-width="1"/>

  <!-- Bottom chart cards -->
  <rect x="78" y="512" width="332" height="150" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="474" y="512" width="332" height="150" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="870" y="512" width="332" height="150" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>

  <!-- Chart 1: minimalist horizontal bars -->
  <text x="104" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">Regional Sales</text>
  <text x="104" y="570" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A8A8A">TOP MARKETS</text>

  <rect x="104" y="590" width="190" height="9" rx="5" fill="#E3E3E3"/>
  <rect x="104" y="590" width="146" height="9" rx="5" fill="url(#tealFade)"/>
  <text x="318" y="599" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">38%</text>

  <rect x="104" y="616" width="190" height="9" rx="5" fill="#E3E3E3"/>
  <rect x="104" y="616" width="102" height="9" rx="5" fill="#AFCACA"/>
  <text x="318" y="625" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">27%</text>

  <rect x="104" y="642" width="190" height="9" rx="5" fill="#E3E3E3"/>
  <rect x="104" y="642" width="72" height="9" rx="5" fill="#C8DADA"/>
  <text x="318" y="651" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#555555">19%</text>

  <!-- Chart 2: donut -->
  <text x="500" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">Channel Split</text>
  <text x="500" y="570" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A8A8A">DIRECT VS PARTNER</text>

  <circle cx="640" cy="613" r="40" fill="none" stroke="#E6E6E6" stroke-width="13"/>
  <circle cx="640" cy="613" r="40" fill="none" stroke="#5A9696" stroke-width="13" stroke-dasharray="162 252" stroke-linecap="round" transform="rotate(-90 640 613)"/>
  <circle cx="640" cy="613" r="40" fill="none" stroke="#333333" stroke-width="13" stroke-dasharray="62 252" stroke-linecap="round" transform="rotate(142 640 613)"/>
  <text x="640" y="609" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#333333">64%</text>
  <text x="640" y="627" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A8A8A">DIRECT</text>

  <!-- Chart 3: columns and sparkline -->
  <text x="896" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#333333">Monthly Trend</text>
  <text x="896" y="570" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8A8A8A">LAST 6 MONTHS</text>

  <rect x="906" y="628" width="26" height="24" rx="5" fill="#D9D9D9"/>
  <rect x="948" y="612" width="26" height="40" rx="5" fill="#CFCFCF"/>
  <rect x="990" y="596" width="26" height="56" rx="5" fill="#AFCACA"/>
  <rect x="1032" y="604" width="26" height="48" rx="5" fill="#C8DADA"/>
  <rect x="1074" y="578" width="26" height="74" rx="5" fill="#5A9696"/>
  <rect x="1116" y="588" width="26" height="64" rx="5" fill="#333333"/>

  <path d="M906 602 C930 594, 948 584, 970 588 C1006 594, 1020 570, 1048 572 C1082 574, 1100 558, 1142 562"
        fill="none" stroke="#5A9696" stroke-width="3" stroke-linecap="round"/>

  <line x1="906" y1="652" x2="1152" y2="652" stroke="#E6E6E6" stroke-width="1"/>
</svg>
```

## Avoid in this skill
- ❌ Default-looking chart furniture: axes, tick labels, gridlines, legends, and heavy chart borders undermine the “executive dashboard” feel.
- ❌ Dense tables or many tiny labels; this layout works because each chart is reduced to one immediate takeaway.
- ❌ Bright multi-color palettes; keep nearly everything gray and reserve one muted accent color for the main data signal.
- ❌ Applying `filter` to `<line>` dividers or arrows; use shadows only on cards, images, paths, circles, or rectangles.
- ❌ Masking chart elements to fake donut segments; use stroked circles with `stroke-dasharray` instead.

## Composition notes
- Keep the top 25% for title, slicer, KPI ribbon, and one thin divider; KPI numbers should feel large but not boxed in.
- Reserve the middle as the emotional anchor: one transparent-background product or context image, centered with large negative space around it.
- Place the bottom analytical ribbon in three equal panels; charts should be readable at a glance and should avoid axes.
- Use a strict color rhythm: off-white background, dark charcoal text, light gray structure, and one muted teal accent for priority data.