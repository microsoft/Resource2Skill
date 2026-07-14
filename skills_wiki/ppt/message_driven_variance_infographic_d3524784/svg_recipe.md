# SVG Recipe — Message-Driven Variance Infographic

## Visual mechanism
Replace a complex comparison chart with a purpose-built horizontal bar infographic: actual values are shown as large, clean bars, while the “so what?” variance is elevated into small semantic badges placed immediately after each bar. The audience reads the conclusion first, then scans the rows for volume and variance without doing mental math.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× decorative `<path>` for a subtle executive-style background wash
- 1× thin `<rect>` divider below the headline
- 3× `<rect>` for actual-volume horizontal bars
- 3× `<rect>` for faint budget target ticks
- 3× rounded `<rect>` for variance badges
- 3× small `<path>` arrow/triangle icons inside variance badges
- Multiple `<text>` elements for title, subtitle, row labels, values, headers, and badge numbers
- 2× `<linearGradient>` fills for premium green and neutral bar styling
- 1× `<filter id="badgeShadow">` applied to variance badges for subtle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="greenBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#78B84A"/>
      <stop offset="100%" stop-color="#5FA33F"/>
    </linearGradient>
    <linearGradient id="greyBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#B7B7B7"/>
      <stop offset="100%" stop-color="#9E9E9E"/>
    </linearGradient>
    <filter id="badgeShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M0,0 L520,0 C455,82 371,117 248,120 C139,123 70,163 0,232 Z" fill="#F3FAEF"/>

  <text x="80" y="66" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="2" fill="#6E9F4A">
    PERFORMANCE UPDATE
  </text>
  <text x="80" y="114" width="960" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="600" fill="#404040">
    <tspan>Production volume </tspan><tspan fill="#70AD47">ahead of budget</tspan><tspan fill="#404040"> by 30 tons</tspan>
  </text>
  <text x="82" y="146" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#7A7A7A">
    Actual output is concentrated in Europe; variance callouts show the message directly.
  </text>
  <rect x="80" y="169" width="1120" height="2" fill="#E6E6E6"/>

  <text x="330" y="215" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#8A8A8A">
    ACTUAL VOLUME, TONS
  </text>
  <text x="970" y="215" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#8A8A8A">
    VARIANCE VS BUDGET
  </text>
  <text x="804" y="244" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6F6F6F">
    Budget marker
  </text>

  <!-- Row 1: Europe -->
  <text x="282" y="305" width="190" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#595959">
    Europe
  </text>
  <rect x="817" y="258" width="4" height="76" rx="2" fill="#404040" opacity="0.45"/>
  <rect x="330" y="268" width="620" height="56" rx="0" fill="url(#greenBar)"/>
  <text x="928" y="304" width="100" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">
    330
  </text>
  <rect x="970" y="263" width="128" height="66" rx="16" fill="#E2EFDA" filter="url(#badgeShadow)"/>
  <path d="M994 289 L1005 275 L1016 289 Z" fill="#548235"/>
  <text x="1034" y="293" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#548235">
    +70
  </text>
  <text x="1001" y="316" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#548235">
    vs budget
  </text>

  <!-- Row 2: US -->
  <text x="282" y="419" width="190" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#595959">
    US
  </text>
  <rect x="610" y="372" width="4" height="76" rx="2" fill="#404040" opacity="0.45"/>
  <rect x="330" y="382" width="310" height="56" rx="0" fill="url(#greyBar)"/>
  <text x="620" y="418" width="80" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">
    165
  </text>
  <rect x="660" y="377" width="118" height="66" rx="16" fill="#E2EFDA" filter="url(#badgeShadow)"/>
  <path d="M684 403 L695 389 L706 403 Z" fill="#548235"/>
  <text x="724" y="407" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#548235">
    +15
  </text>
  <text x="691" y="430" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#548235">
    vs budget
  </text>

  <!-- Row 3: Asia -->
  <text x="282" y="533" width="190" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#595959">
    Asia
  </text>
  <rect x="553" y="486" width="4" height="76" rx="2" fill="#404040" opacity="0.45"/>
  <rect x="330" y="496" width="122" height="56" rx="0" fill="url(#greyBar)"/>
  <text x="472" y="532" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#595959">
    65
  </text>
  <rect x="502" y="491" width="118" height="66" rx="16" fill="#FCE4D6" filter="url(#badgeShadow)"/>
  <path d="M526 519 L537 533 L548 519 Z" fill="#C00000"/>
  <text x="566" y="521" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#C00000">
    -55
  </text>
  <text x="533" y="544" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#C00000">
    vs budget
  </text>

  <rect x="330" y="605" width="18" height="18" rx="3" fill="#70AD47"/>
  <text x="358" y="620" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    Highlighted region driving the outperformance
  </text>
  <rect x="650" y="605" width="18" height="18" rx="3" fill="#A6A6A6"/>
  <text x="678" y="620" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    Neutral actual-volume bars
  </text>
</svg>
```

## Avoid in this skill
- ❌ Default chart axes, gridlines, legends, and clustered bars; they make the viewer calculate variance instead of reading it.
- ❌ Placing variance labels far from the corresponding bar; the badge should sit immediately beside the actual value.
- ❌ Using only red/green text without a filled badge; the variance should feel like a deliberate semantic object.
- ❌ Over-scaling small categories until they look equal to large categories; preserve honest bar lengths and place short values outside the bar if needed.
- ❌ Applying `filter` effects to `<line>` elements for budget ticks; use thin `<rect>` elements instead.

## Composition notes
- Keep the title declarative and message-led; the headline should state the conclusion before the audience reaches the data.
- Reserve the left 20–25% of the slide for right-aligned category labels, then start every bar on the same x-coordinate.
- Use the brightest bar color only for the row that supports the main message; keep other actual bars neutral grey.
- Variance badges should be compact, rounded, and high-contrast, forming a second visual column that reads faster than a legend.