# SVG Recipe — Floating Panel KPI Dashboard

## Visual mechanism
A muted full-bleed background photo sits behind a large, softly shadowed “floating” dashboard panel. Inside the panel, KPI cards combine oversized numbers, small labels, linear gauges, semi-circle progress gauges, and compact bar charts with vivid accent colors for executive readability.

## SVG primitives needed
- 1× `<image>` for the full-slide photographic background
- 1× `<rect>` translucent overlay to darken/mute the background image
- 1× `<rect>` main floating panel with rounded corners and soft shadow
- 1× `<rect>` black header bar anchoring the dashboard title
- 4× `<rect>` KPI summary cards with shadows
- 3× `<rect>` lower widget cards for detailed charts
- Multiple `<text>` elements with explicit `width` attributes for dashboard title, KPI values, labels, chart labels, and annotations
- Multiple `<line>` elements for KPI dividers, axis ticks, and linear gauge tracks
- Multiple `<rect>` bars for mini bar charts and horizontal progress bars
- Multiple `<path>` arcs for semi-circle radial gauges
- 1× `<path>` custom upward arrow icon for performance status
- 2× `<linearGradient>` definitions for accent fills and panel sheen
- 1× `<filter id="panelShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for floating depth
- 1× `<filter id="softGlow">` using `feGaussianBlur` for subtle gauge glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelSheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f0f0f0"/>
    </linearGradient>
    <linearGradient id="magentaGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff4bb0"/>
      <stop offset="100%" stop-color="#da0080"/>
    </linearGradient>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/grayscale-city-office-background-for-executive-dashboard.jpg"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.58"/>

  <rect x="36" y="34" width="1208" height="652" rx="22" fill="url(#panelSheen)" filter="url(#panelShadow)"/>
  <rect x="36" y="34" width="1208" height="76" rx="22" fill="#000000"/>
  <rect x="36" y="88" width="1208" height="22" fill="#000000"/>
  <text x="72" y="82" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff">Executive KPI Dashboard</text>
  <text x="1010" y="78" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#d8d8d8">Q4 Performance</text>
  <circle cx="1196" cy="61" r="13" fill="#ed1c24"/>
  <path d="M1190 63 L1196 55 L1202 63 L1199 63 L1199 69 L1193 69 L1193 63 Z" fill="#ffffff"/>

  <rect x="72" y="136" width="262" height="126" rx="16" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="96" y="175" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#595959">Revenue</text>
  <text x="96" y="220" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111111">$12.8M</text>
  <text x="96" y="244" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8bc34a">▲ 18.4% vs target</text>

  <rect x="356" y="136" width="262" height="126" rx="16" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="380" y="175" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#595959">Pipeline Coverage</text>
  <text x="380" y="220" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111111">3.7×</text>
  <line x1="382" y1="238" x2="564" y2="238" stroke="#dddddd" stroke-width="9" stroke-linecap="round"/>
  <line x1="382" y1="238" x2="522" y2="238" stroke="#da0080" stroke-width="9" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="542" cy="238" r="7" fill="#8bc34a"/>

  <rect x="640" y="136" width="262" height="126" rx="16" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="664" y="175" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#595959">Customer NPS</text>
  <text x="664" y="220" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111111">72</text>
  <rect x="806" y="168" width="50" height="62" rx="8" fill="#ffd700"/>
  <text x="816" y="252" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#595959">Top quartile</text>

  <rect x="924" y="136" width="262" height="126" rx="16" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="948" y="175" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#595959">Risk Index</text>
  <text x="948" y="220" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111111">Low</text>
  <text x="948" y="244" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#595959">4 open escalations</text>

  <rect x="72" y="296" width="500" height="340" rx="18" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="104" y="340" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#222222">Regional Sales Mix</text>
  <text x="104" y="368" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">Contribution by territory, current quarter</text>
  <line x1="128" y1="582" x2="520" y2="582" stroke="#cfcfcf" stroke-width="2"/>
  <rect x="144" y="456" width="54" height="126" rx="7" fill="#ffd700"/>
  <rect x="222" y="408" width="54" height="174" rx="7" fill="#da0080"/>
  <rect x="300" y="476" width="54" height="106" rx="7" fill="#8bc34a"/>
  <rect x="378" y="430" width="54" height="152" rx="7" fill="#ed1c24"/>
  <rect x="456" y="390" width="54" height="192" rx="7" fill="#595959"/>
  <text x="143" y="612" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#595959">NA</text>
  <text x="221" y="612" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#595959">EU</text>
  <text x="299" y="612" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#595959">APAC</text>
  <text x="374" y="612" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#595959">LATAM</text>
  <text x="454" y="612" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#595959">MEA</text>

  <rect x="604" y="296" width="286" height="340" rx="18" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="634" y="340" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#222222">Forecast Attainment</text>
  <path d="M664 524 A82 82 0 0 1 828 524" fill="none" stroke="#e2e2e2" stroke-width="28" stroke-linecap="round"/>
  <path d="M664 524 A82 82 0 0 1 783 451" fill="none" stroke="url(#magentaGrad)" stroke-width="28" stroke-linecap="round" filter="url(#softGlow)"/>
  <text x="704" y="514" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#111111">73%</text>
  <text x="673" y="560" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">Against full-year plan</text>
  <line x1="640" y1="590" x2="854" y2="590" stroke="#dddddd" stroke-width="10" stroke-linecap="round"/>
  <line x1="640" y1="590" x2="796" y2="590" stroke="#8bc34a" stroke-width="10" stroke-linecap="round"/>

  <rect x="922" y="296" width="264" height="340" rx="18" fill="#ffffff" filter="url(#panelShadow)"/>
  <text x="952" y="340" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#222222">Delivery Health</text>
  <path d="M972 524 A82 82 0 0 1 1136 524" fill="none" stroke="#e2e2e2" stroke-width="28" stroke-linecap="round"/>
  <path d="M972 524 A82 82 0 0 1 1106 462" fill="none" stroke="#8bc34a" stroke-width="28" stroke-linecap="round" filter="url(#softGlow)"/>
  <text x="1014" y="514" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#111111">81%</text>
  <text x="978" y="560" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">Milestones on track</text>
  <rect x="956" y="588" width="184" height="18" rx="9" fill="#eeeeee"/>
  <rect x="956" y="588" width="149" height="18" rx="9" fill="#ffd700"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use real chart objects, `<foreignObject>`, or HTML tables; build KPI widgets from native SVG text, paths, rects, and lines.
- ❌ Do not use `<mask>` for dimming or cropping; use a translucent overlay rectangle for the background and `clipPath` only if cropping an `<image>`.
- ❌ Do not apply `filter` to `<line>` elements; use filters on panels, paths, rects, or text only.
- ❌ Do not use `marker-end` on curved gauge paths; draw arrows or status icons as explicit `<path>` shapes.
- ❌ Do not omit `width` on `<text>` elements, because PowerPoint translation needs explicit text box widths.

## Composition notes
- Keep the floating panel large, around 94–96% of slide width and 88–92% of slide height, so the background image frames the dashboard without competing.
- Use a strong top header bar, then a row of compact KPI cards, then larger analytical widgets below; this creates an executive scan path from summary to detail.
- Reserve vivid colors for data meaning: magenta for active progress, green for goal/healthy status, yellow for attention or contribution, red for alerts/icons.
- Maintain generous internal padding inside cards and avoid dense gridlines; the premium look comes from whitespace, soft shadows, and restrained typography.