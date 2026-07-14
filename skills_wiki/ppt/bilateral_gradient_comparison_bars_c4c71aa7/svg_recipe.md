# SVG Recipe — Bilateral Gradient Comparison Bars

## Visual mechanism
A central column of metric labels anchors the chart while paired pill bars grow outward to the left and right, creating an immediate “push-pull” comparison. Directional gradients darken near the center axis and brighten toward the bar tips, emphasizing expansion and making percentage endpoints easy to scan.

## SVG primitives needed
- 1× `<rect>` for the full dark slide background
- 2× translucent `<circle>` / `<ellipse>` for soft background color halos
- 1× `<path>` for an abstract decorative wave accent behind the chart
- 2× `<linearGradient>` for left/right data bar fills with opposite directional color logic
- 1× `<linearGradient>` for the subtle central metric-pill fill
- 1× `<filter id="softShadow">` applied to central metric pills and header badges
- 1× `<filter id="barGlow">` applied to the colored comparison bars
- 10× muted `<rect>` track pills showing each side’s full possible range
- 10× colored `<rect>` data pill bars, anchored to the center and expanding outward
- 5× elevated center `<rect>` metric pills layered above the bar roots
- 2× `<circle>` product badges for the left and right comparison entities
- Multiple `<text>` elements with explicit `width` attributes for title, headers, metric labels, and embedded values
- 1× `<line>` for a subtle vertical center spine behind the metric labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1B2230"/>
      <stop offset="100%" stop-color="#101622"/>
    </linearGradient>

    <linearGradient id="leftBarGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#74F0A7"/>
      <stop offset="58%" stop-color="#38A169"/>
      <stop offset="100%" stop-color="#1F5C45"/>
    </linearGradient>

    <linearGradient id="rightBarGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#245CA8"/>
      <stop offset="54%" stop-color="#3182CE"/>
      <stop offset="100%" stop-color="#7DD3FC"/>
    </linearGradient>

    <linearGradient id="centerPillGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3A465C"/>
      <stop offset="100%" stop-color="#273244"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="barGlow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="120" cy="130" r="190" fill="#38A169" opacity="0.10"/>
  <ellipse cx="1160" cy="590" rx="250" ry="190" fill="#3182CE" opacity="0.12"/>
  <path d="M-20 650 C180 570 315 705 495 620 C670 538 780 600 960 520 C1090 463 1190 475 1310 405 L1310 720 L-20 720 Z" fill="#FFFFFF" opacity="0.035"/>

  <text x="72" y="66" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">
    Product Comparison: A vs. B
  </text>
  <text x="72" y="101" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#AAB6C7">
    Bilateral gradient bars reveal relative strength across shared business metrics
  </text>

  <circle cx="260" cy="138" r="28" fill="#2F855A" filter="url(#softShadow)"/>
  <text x="249" y="148" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">A</text>
  <text x="305" y="145" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#D8FBE5">
    Product Alpha
  </text>

  <circle cx="1020" cy="138" r="28" fill="#2B6CB0" filter="url(#softShadow)"/>
  <text x="1009" y="148" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">B</text>
  <text x="710" y="145" width="265" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" text-anchor="end" fill="#D8EEFF">
    Product Beta
  </text>

  <line x1="640" y1="170" x2="640" y2="620" stroke="#5D6A7F" stroke-width="1" opacity="0.45"/>

  <!-- Row 1 -->
  <rect x="190" y="202" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="690" y="202" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="390" y="202" width="200" height="42" rx="21" fill="url(#leftBarGrad)" filter="url(#barGlow)"/>
  <rect x="690" y="202" width="380" height="42" rx="21" fill="url(#rightBarGrad)" filter="url(#barGlow)"/>
  <rect x="490" y="196" width="300" height="54" rx="27" fill="url(#centerPillGrad)" filter="url(#softShadow)"/>
  <text x="405" y="229" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">50%</text>
  <text x="1012" y="229" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">95%</text>
  <text x="515" y="229" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#FFFFFF">Target Market Penetration</text>

  <!-- Row 2 -->
  <rect x="190" y="284" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="690" y="284" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="290" y="284" width="300" height="42" rx="21" fill="url(#leftBarGrad)" filter="url(#barGlow)"/>
  <rect x="690" y="284" width="260" height="42" rx="21" fill="url(#rightBarGrad)" filter="url(#barGlow)"/>
  <rect x="490" y="278" width="300" height="54" rx="27" fill="url(#centerPillGrad)" filter="url(#softShadow)"/>
  <text x="305" y="311" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">75%</text>
  <text x="892" y="311" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">65%</text>
  <text x="515" y="311" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#FFFFFF">Market Share</text>

  <!-- Row 3 -->
  <rect x="190" y="366" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="690" y="366" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="190" y="366" width="400" height="42" rx="21" fill="url(#leftBarGrad)" filter="url(#barGlow)"/>
  <rect x="690" y="366" width="200" height="42" rx="21" fill="url(#rightBarGrad)" filter="url(#barGlow)"/>
  <rect x="490" y="360" width="300" height="54" rx="27" fill="url(#centerPillGrad)" filter="url(#softShadow)"/>
  <text x="205" y="393" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">100%</text>
  <text x="832" y="393" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">50%</text>
  <text x="515" y="393" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#FFFFFF">Customer Acquisition Cost</text>

  <!-- Row 4 -->
  <rect x="190" y="448" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="690" y="448" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="430" y="448" width="160" height="42" rx="21" fill="url(#leftBarGrad)" filter="url(#barGlow)"/>
  <rect x="690" y="448" width="200" height="42" rx="21" fill="url(#rightBarGrad)" filter="url(#barGlow)"/>
  <rect x="490" y="442" width="300" height="54" rx="27" fill="url(#centerPillGrad)" filter="url(#softShadow)"/>
  <text x="445" y="475" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">40%</text>
  <text x="832" y="475" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">50%</text>
  <text x="515" y="475" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#FFFFFF">Average Revenue Per User</text>

  <!-- Row 5 -->
  <rect x="190" y="530" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="690" y="530" width="400" height="42" rx="21" fill="#FFFFFF" opacity="0.075"/>
  <rect x="250" y="530" width="340" height="42" rx="21" fill="url(#leftBarGrad)" filter="url(#barGlow)"/>
  <rect x="690" y="530" width="400" height="42" rx="21" fill="url(#rightBarGrad)" filter="url(#barGlow)"/>
  <rect x="490" y="524" width="300" height="54" rx="27" fill="url(#centerPillGrad)" filter="url(#softShadow)"/>
  <text x="265" y="557" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">85%</text>
  <text x="1024" y="557" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">100%</text>
  <text x="515" y="557" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#FFFFFF">Customer Lifetime Value</text>

  <text x="72" y="662" width="1140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7F8CA3">
    Reading guide: bars originate beneath the central metric labels; brighter endpoints indicate the achieved magnitude on each side.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using ordinary squared bars; the pill geometry is essential to the premium SaaS-dashboard feel.
- ❌ Reversing the gradient directions accidentally; the darker color should sit near the center axis and the brighter color should sit toward the outer endpoints.
- ❌ Placing metric labels at the far left; the technique depends on the reader scanning one central metric column.
- ❌ Applying shadows to `<line>` elements; use shadows on the center pill `<rect>` elements instead.
- ❌ Using `<mask>` or clipping non-image elements to fake bar lengths; just draw each rounded `<rect>` at its computed width.

## Composition notes
- Keep the center metric column visually dominant but narrow: roughly 23–25% of slide width, with left and right bar fields balanced around it.
- Layer order matters: draw muted tracks first, colored data bars second, then central metric pills on top so the bars appear to tuck underneath.
- Use a dark neutral background with low-opacity halos so green/blue gradients feel luminous without reducing readability.
- Put percentage labels near the bright outer tips of each bar; this reinforces outward motion and makes the endpoints scannable.