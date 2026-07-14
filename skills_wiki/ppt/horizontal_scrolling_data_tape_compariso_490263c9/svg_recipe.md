# SVG Recipe — Horizontal Scrolling Data Tape (Comparison Ticker)

## Visual mechanism
A long horizontal strip of repeated comparison cards extends beyond the right edge of the slide, creating the illusion of a scrolling data tape. A fixed dark title panel sits on top at the right edge, hiding incoming cards and framing the comparison like a social-video ticker.

## SVG primitives needed
- 3× `<rect>` for the horizontal background track bands: value zone, label zone, image zone.
- 8× `<path>` for red-orange downward ribbon flags holding the key metric.
- 8× `<rect>` for label plates and image-card frames.
- 8× `<image>` clipped into rounded square crops for subject photos.
- 8× `<clipPath>` with rounded `<rect>` for editable rounded image crops.
- 1× `<rect>` for the fixed right-side overlay/mask panel.
- 2× `<circle>` for the timer/progress indicator on the overlay panel.
- Multiple `<text>` elements with explicit `width` for values, labels, ranks, and panel copy.
- 2× `<linearGradient>` for premium background/panel depth.
- 1× `<filter id="softShadow">` applied to cards and the overlay panel.
- 1× `<filter id="glow">` applied to the active progress ring accent.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="topBand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#252B33"/>
      <stop offset="55%" stop-color="#333A45"/>
      <stop offset="100%" stop-color="#222831"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#202832"/>
      <stop offset="100%" stop-color="#11161C"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
    <clipPath id="photoClip1"><rect x="60" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip2"><rect x="250" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip3"><rect x="440" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip4"><rect x="630" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip5"><rect x="820" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip6"><rect x="1010" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip7"><rect x="1200" y="468" width="150" height="150" rx="18"/></clipPath>
    <clipPath id="photoClip8"><rect x="1390" y="468" width="150" height="150" rx="18"/></clipPath>
  </defs>

  <!-- fixed track background -->
  <rect x="0" y="0" width="1280" height="330" fill="url(#topBand)"/>
  <rect x="0" y="330" width="1280" height="118" fill="#A0A4A8"/>
  <rect x="0" y="448" width="1280" height="272" fill="#4E555D"/>
  <rect x="0" y="329" width="1280" height="2" fill="#C8CDD2" opacity="0.35"/>
  <rect x="0" y="447" width="1280" height="2" fill="#1B2026" opacity="0.55"/>

  <!-- moving tape: group this in PowerPoint and apply a constant-speed left motion path -->
  <g id="data-tape">
    <path d="M60 52 H210 V210 L135 252 L60 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="76" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="135">10B</tspan><tspan x="135" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="60" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="73" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Nova Labs</text>
    <rect x="56" y="464" width="158" height="158" rx="22" fill="#20242A" filter="url(#softShadow)"/>
    <image href="https://images.example.com/comparison-ticker/clean-tech-startup-founder.jpg" x="60" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip1)"/>
    <text x="60" y="650" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D5DAE0" text-anchor="middle">#8</text>

    <path d="M250 52 H400 V210 L325 252 L250 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="266" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="325">12B</tspan><tspan x="325" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="250" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="263" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Orbit AI</text>
    <rect x="246" y="464" width="158" height="158" rx="22" fill="#20242A" filter="url(#softShadow)"/>
    <image href="https://images.example.com/comparison-ticker/futuristic-ai-product-photo.jpg" x="250" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip2)"/>
    <text x="250" y="650" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D5DAE0" text-anchor="middle">#7</text>

    <path d="M440 52 H590 V210 L515 252 L440 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="456" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="515">15B</tspan><tspan x="515" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="440" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="453" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Aster Bank</text>
    <rect x="436" y="464" width="158" height="158" rx="22" fill="#20242A" filter="url(#softShadow)"/>
    <image href="https://images.example.com/comparison-ticker/modern-bank-headquarters.jpg" x="440" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip3)"/>
    <text x="440" y="650" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D5DAE0" text-anchor="middle">#6</text>

    <path d="M630 52 H780 V210 L705 252 L630 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="646" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="705">22B</tspan><tspan x="705" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="630" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="643" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Helio Grid</text>
    <rect x="626" y="464" width="158" height="158" rx="22" fill="#20242A" filter="url(#softShadow)"/>
    <image href="https://images.example.com/comparison-ticker/solar-energy-field.jpg" x="630" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip4)"/>
    <text x="630" y="650" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D5DAE0" text-anchor="middle">#5</text>

    <path d="M820 52 H970 V210 L895 252 L820 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="836" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="895">35B</tspan><tspan x="895" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="820" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="833" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">BluePeak</text>
    <rect x="816" y="464" width="158" height="158" rx="22" fill="#20242A" filter="url(#softShadow)"/>
    <image href="https://images.example.com/comparison-ticker/cloud-computing-data-center.jpg" x="820" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip5)"/>
    <text x="820" y="650" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#D5DAE0" text-anchor="middle">#4</text>

    <path d="M1010 52 H1160 V210 L1085 252 L1010 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="1026" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="1085">41B</tspan><tspan x="1085" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="1010" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="1023" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Zenith EV</text>
    <rect x="1006" y="464" width="158" height="158" rx="22" fill="#20242A" filter="url(#softShadow)"/>
    <image href="https://images.example.com/comparison-ticker/electric-vehicle-showroom.jpg" x="1010" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip6)"/>

    <path d="M1200 52 H1350 V210 L1275 252 L1200 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="1216" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="1275">50B</tspan><tspan x="1275" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="1200" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="1213" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Quantum</text>
    <image href="https://images.example.com/comparison-ticker/quantum-computer-lab.jpg" x="1200" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip7)"/>

    <path d="M1390 52 H1540 V210 L1465 252 L1390 210 Z" fill="#DC3220" filter="url(#softShadow)"/>
    <text x="1406" y="112" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF" text-anchor="middle"><tspan x="1465">75B</tspan><tspan x="1465" dy="34" font-size="20" font-weight="600">USD</tspan></text>
    <rect x="1390" y="348" width="150" height="74" rx="12" fill="#F1F3F5"/>
    <text x="1403" y="391" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#252B33" text-anchor="middle">Titan Bio</text>
    <image href="https://images.example.com/comparison-ticker/biotech-lab-researcher.jpg" x="1390" y="468" width="150" height="150" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip8)"/>
  </g>

  <!-- stationary right overlay / visual mask -->
  <rect x="960" y="0" width="320" height="720" fill="url(#panelGrad)" filter="url(#softShadow)"/>
  <rect x="960" y="0" width="4" height="720" fill="#FFFFFF" opacity="0.12"/>
  <text x="995" y="92" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#FFFFFF">Top Market Cap</text>
  <text x="995" y="145" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#AEB7C2">Comparison Ticker</text>
  <text x="995" y="224" width="225" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#78838F">Group the tape, then animate left with linear timing for a scrolling reveal.</text>
  <circle cx="1120" cy="430" r="82" fill="none" stroke="#37424E" stroke-width="18"/>
  <circle cx="1120" cy="430" r="82" fill="none" stroke="#FF4A2F" stroke-width="18" stroke-linecap="round" stroke-dasharray="360 515" transform="rotate(-90 1120 430)" filter="url(#glow)"/>
  <text x="1058" y="423" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF" text-anchor="middle">08</text>
  <text x="1058" y="464" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#B7C0CA" text-anchor="middle">ITEMS</text>
  <rect x="995" y="585" width="220" height="54" rx="27" fill="#FF4A2F"/>
  <text x="1020" y="620" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">NEXT →</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the scroll; create the layout in SVG, then apply the left motion path in PowerPoint.
- ❌ `<mask>` to hide the incoming tape; use an opaque overlay panel as the visual mask instead.
- ❌ `clip-path` on grouped card shapes; only apply clipping to `<image>` elements.
- ❌ `marker-end` arrows for motion cues; use text like `NEXT →` or simple editable shapes.
- ❌ A tape that stops at the slide boundary; the key effect requires cards placed far beyond `x=1280`.

## Composition notes
- Keep the moving data tape roughly 75% of the slide width and reserve the rightmost 25% for the fixed overlay panel.
- Use three strong horizontal bands so every card has a predictable value, label, and image zone.
- Let at least two cards overflow beyond the right edge to communicate “more items are coming.”
- Use one high-energy accent color for all value ribbons and progress graphics; keep the track neutral so the numbers dominate.