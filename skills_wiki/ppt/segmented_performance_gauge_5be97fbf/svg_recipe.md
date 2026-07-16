# SVG Recipe — Segmented Performance Gauge

## Visual mechanism
A semi-circular speedometer gauge is built from closed donut-slice `<path>` segments, each filled with a performance color. A custom triangular needle pivots from the center toward the metric value, while soft blur shadows and subtle highlights make the gauge feel like a premium, physical dashboard object.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 1× `<radialGradient>` for a soft focal glow behind the gauge.
- 1× `<circle>` for the background glow field.
- 1× `<ellipse>` with blur filter for the centered ambient shadow under the gauge.
- 5× closed `<path>` donut-slice segments for the colored performance bands.
- 1× stroked `<path>` for a subtle glossy highlight across the top of the arc.
- 6× `<line>` for small boundary ticks around the gauge scale.
- 1× triangular `<path>` for the needle pointer.
- 3× `<circle>` for the needle hub, hub rim, and central cap.
- 2× `<filter>` definitions: one blur for the gauge shadow and one offset blur for the needle depth.
- Multiple `<text>` labels with explicit `width` attributes for title, KPI value, scale labels, and category captions.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="58%" r="48%">
      <stop offset="0%" stop-color="#EAF4FF"/>
      <stop offset="58%" stop-color="#F7FAFD"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </radialGradient>

    <linearGradient id="hubGrad" x1="600" y1="430" x2="680" y2="520">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#D8E1EA"/>
    </linearGradient>

    <filter id="ambientBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="needleShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="640" cy="450" r="330" fill="#FFFFFF" opacity="0.42"/>

  <text x="80" y="82" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1D2B3A">
    Customer Experience Index
  </text>
  <text x="82" y="116" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#718096">
    Segmented performance gauge · current quarter
  </text>

  <ellipse cx="640" cy="505" rx="335" ry="132" fill="#0B1F33" opacity="0.14" filter="url(#ambientBlur)"/>

  <!-- Segmented semi-circular gauge: outer radius 250, inner radius 150, center 640,480 -->
  <path d="M 390 480 A 250 250 0 0 1 433 340 L 516 396 A 150 150 0 0 0 490 480 Z"
        fill="#C84A4A"/>
  <path d="M 438 333 A 250 250 0 0 1 554 245 L 589 339 A 150 150 0 0 0 519 392 Z"
        fill="#F2994A"/>
  <path d="M 563 242 A 250 250 0 0 1 709 240 L 681 336 A 150 150 0 0 0 594 337 Z"
        fill="#F2C94C"/>
  <path d="M 717 242 A 250 250 0 0 1 837 326 L 758 388 A 150 150 0 0 0 686 337 Z"
        fill="#56B870"/>
  <path d="M 842 333 A 250 250 0 0 1 890 471 L 790 475 A 150 150 0 0 0 761 392 Z"
        fill="#2F80ED"/>

  <!-- Soft gloss riding across the arc -->
  <path d="M 412 462 A 228 228 0 0 1 868 462"
        fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.35"/>

  <!-- Boundary ticks -->
  <line x1="380" y1="480" x2="356" y2="480" stroke="#8A97A6" stroke-width="3" stroke-linecap="round"/>
  <line x1="430" y1="327" x2="415" y2="316" stroke="#8A97A6" stroke-width="3" stroke-linecap="round"/>
  <line x1="560" y1="233" x2="552" y2="210" stroke="#8A97A6" stroke-width="3" stroke-linecap="round"/>
  <line x1="720" y1="233" x2="728" y2="210" stroke="#8A97A6" stroke-width="3" stroke-linecap="round"/>
  <line x1="850" y1="327" x2="865" y2="316" stroke="#8A97A6" stroke-width="3" stroke-linecap="round"/>
  <line x1="900" y1="480" x2="924" y2="480" stroke="#8A97A6" stroke-width="3" stroke-linecap="round"/>

  <!-- Needle at 68%: angle = 180 + 0.68 * 180 = 302.4 degrees -->
  <path d="M 750 307 L 650 486 L 640 497 L 630 475 Z"
        fill="#3E4650" filter="url(#needleShadow)"/>
  <circle cx="640" cy="480" r="43" fill="#FFFFFF" opacity="0.96"/>
  <circle cx="640" cy="480" r="34" fill="url(#hubGrad)" stroke="#B8C4D1" stroke-width="2"/>
  <circle cx="640" cy="480" r="11" fill="#3E4650"/>

  <!-- Metric readout -->
  <text x="640" y="552" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#1D2B3A">
    68%
  </text>
  <text x="640" y="586" width="300" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#5B6775">
    Above target performance
  </text>

  <!-- Scale labels -->
  <text x="348" y="516" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6775">0</text>
  <text x="404" y="294" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6775">20</text>
  <text x="550" y="197" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6775">40</text>
  <text x="730" y="197" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6775">60</text>
  <text x="876" y="294" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6775">80</text>
  <text x="932" y="516" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6775">100</text>

  <!-- Category captions -->
  <text x="420" y="632" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#C84A4A">Critical</text>
  <text x="530" y="632" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#F2994A">Watch</text>
  <text x="640" y="632" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#B08A1D">Stable</text>
  <text x="750" y="632" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#3D9B5B">Strong</text>
  <text x="860" y="632" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#2F80ED">Leading</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path marker-end="...">` for the needle; marker arrowheads on paths may disappear. Build the needle as a filled triangular `<path>`.
- ❌ Do not rely on a thick stroked arc with `stroke-dasharray` as the main gauge body if you need editable, individually recolorable segments; use closed donut-slice paths instead.
- ❌ Do not apply `filter` to tick `<line>` elements; line filters are dropped. Put depth on ellipses, circles, or paths.
- ❌ Do not use `<mask>` to cut out the inner hole of the gauge; create each segment as a closed compound-looking path with outer and inner arc edges.
- ❌ Do not omit `width` on any `<text>` label, including small scale numbers.

## Composition notes
- Keep the gauge centered horizontally and slightly below mid-slide so the top title area has clean breathing room.
- Use 5 segments maximum for executive readability; more segments make the speedometer feel noisy.
- The needle should stop just inside the colored arc, not on top of the labels.
- Use a single warm-to-cool or red-to-blue progression; reserve the darkest neutral color for the needle and value text.