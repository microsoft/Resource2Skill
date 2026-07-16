# SVG Recipe — Narrative-Driven Highlighted Chart

## Visual mechanism
A decluttered column chart uses muted bars for context and one saturated accent bar for the narrative focal point. Direct value labels, a small annotation, and a bottom “Key Takeaway” panel tell the audience exactly what to notice without requiring them to decode axes or legends.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 2× `<rect>` for the elevated chart panel and takeaway panel
- 12× `<rect>` for monthly column bars, with one highlighted bar
- 12× `<text>` for direct data labels above bars
- 12× `<text>` for month labels along the baseline
- 4× `<text>` for title, subtitle, annotation, and takeaway copy
- 2× `<line>` for the chart baseline and the annotation connector
- 1× `<path>` for the custom arrowhead pointing to the highlighted bar
- 2× `<linearGradient>` for muted bar fills and the focal alert bar
- 2× `<filter>` using blur/offset/merge for panel shadow and focal glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f4f7fb"/>
    </linearGradient>

    <linearGradient id="mutedBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c7d7ee"/>
      <stop offset="100%" stop-color="#aebfda"/>
    </linearGradient>

    <linearGradient id="alertBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ff6b7d"/>
      <stop offset="100%" stop-color="#dc3545"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-15%" width="120%" height="140%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="redGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="80" y="66" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#222831">
    Monthly Sales Analysis
  </text>
  <text x="82" y="96" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#697386">
    Context is muted; the single point that explains the story is highlighted.
  </text>

  <rect x="70" y="118" width="1140" height="442" rx="24" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="100" y="154" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#3c4858">
    Sales revenue by month
  </text>
  <text x="1080" y="154" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8a94a6" text-anchor="end">
    USD, thousands
  </text>

  <line x1="115" y1="510" x2="1165" y2="510" stroke="#d9dee8" stroke-width="2"/>

  <rect x="135" y="291" width="56" height="219" rx="8" fill="url(#mutedBar)"/>
  <rect x="219" y="284" width="56" height="226" rx="8" fill="url(#mutedBar)"/>
  <rect x="303" y="268" width="56" height="242" rx="8" fill="url(#mutedBar)"/>
  <rect x="387" y="272" width="56" height="238" rx="8" fill="url(#mutedBar)"/>
  <rect x="471" y="241" width="56" height="269" rx="8" fill="url(#mutedBar)"/>
  <rect x="555" y="217" width="56" height="293" rx="8" fill="url(#mutedBar)"/>
  <rect x="639" y="362" width="56" height="148" rx="8" fill="url(#alertBar)" filter="url(#redGlow)"/>
  <rect x="723" y="256" width="56" height="254" rx="8" fill="url(#mutedBar)"/>
  <rect x="807" y="245" width="56" height="265" rx="8" fill="url(#mutedBar)"/>
  <rect x="891" y="233" width="56" height="277" rx="8" fill="url(#mutedBar)"/>
  <rect x="975" y="206" width="56" height="304" rx="8" fill="url(#mutedBar)"/>
  <rect x="1059" y="190" width="56" height="320" rx="8" fill="url(#mutedBar)"/>

  <text x="163" y="278" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$560K</text>
  <text x="247" y="271" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$580K</text>
  <text x="331" y="255" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$620K</text>
  <text x="415" y="259" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$610K</text>
  <text x="499" y="228" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$690K</text>
  <text x="583" y="204" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$750K</text>
  <text x="667" y="344" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#dc3545" text-anchor="middle">$380K</text>
  <text x="751" y="243" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$650K</text>
  <text x="835" y="232" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$680K</text>
  <text x="919" y="220" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$710K</text>
  <text x="1003" y="193" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$780K</text>
  <text x="1087" y="177" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#697386" text-anchor="middle">$820K</text>

  <text x="163" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Jan</text>
  <text x="247" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Feb</text>
  <text x="331" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Mar</text>
  <text x="415" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Apr</text>
  <text x="499" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">May</text>
  <text x="583" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Jun</text>
  <text x="667" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#dc3545" text-anchor="middle">Jul</text>
  <text x="751" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Aug</text>
  <text x="835" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Sep</text>
  <text x="919" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Oct</text>
  <text x="1003" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Nov</text>
  <text x="1087" y="538" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7788" text-anchor="middle">Dec</text>

  <line x1="750" y1="322" x2="697" y2="370" stroke="#dc3545" stroke-width="2.5"/>
  <path d="M692 374 L704 368 L699 381 Z" fill="#dc3545"/>
  <rect x="754" y="270" width="245" height="62" rx="14" fill="#fff5f6" stroke="#f1b8bf" stroke-width="1.5"/>
  <text x="774" y="295" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#dc3545">
    July breaks the trend
  </text>
  <text x="774" y="316" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#5f6775">
    Only month below the $500K operating threshold.
  </text>

  <rect x="80" y="600" width="1120" height="86" rx="18" fill="#ffffff" stroke="#dc3545" stroke-width="2.5" filter="url(#softShadow)"/>
  <text x="112" y="628" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#dc3545">
    KEY TAKEAWAY
  </text>
  <text x="112" y="660" width="1010" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#252b36">
    The July sales drop was the only material deviation; recovery began immediately in August.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Full chart furniture: legends, dense gridlines, tick-heavy Y-axes, and secondary axes dilute the intended story.
- ❌ Coloring every bar differently; the hierarchy should be “quiet context” plus one unmistakable focal point.
- ❌ Using transparent overlays to simulate muted data if export fidelity is uncertain; use lighter solid colors instead.
- ❌ Applying `marker-end` to paths for annotation arrows; use a `<line>` plus a small editable `<path>` arrowhead.

## Composition notes
- Keep the chart in the upper 70–75% of the slide, with generous side margins so the bars feel executive rather than cramped.
- Place the takeaway panel as a strong bottom anchor; tie its border or label color to the highlighted chart bar.
- Use direct labels above bars so the audience never needs to read across to an axis.
- Preserve negative space around the highlighted bar and annotation so the focal point is obvious within one glance.