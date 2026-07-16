# SVG Recipe — Editable Speedometer Gauge Chart

## Visual mechanism
A thick semi-circular dial is divided into red, amber, and green performance bands, then overlaid with a triangular needle that pivots from the center. The KPI value is encoded both by the needle angle and by a large numeric readout beneath the cap.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× `<rect>` for the elevated dashboard card
- 1× `<path>` for the soft full semi-donut backing track
- 3× `<path>` for the editable red / amber / green gauge arc segments
- 1× `<path>` for the triangular needle
- 2× `<circle>` for the center pivot cap and inner highlight
- 7× `<line>` for major tick marks around the dial
- 8× `<text>` for title, subtitle, zone labels, KPI value, KPI label, and footnote
- 2× `<linearGradient>` for the card and needle polish
- 1× `<radialGradient>` for the metallic pivot cap
- 1× `<filter id="softShadow">` applied to the card, backing track, and pivot cap

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#E9EEF5"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="120" x2="0" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7FAFD"/>
    </linearGradient>

    <linearGradient id="needleGrad" x1="640" y1="500" x2="825" y2="282" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#121820"/>
      <stop offset="62%" stop-color="#2B2B2B"/>
      <stop offset="100%" stop-color="#05070A"/>
    </linearGradient>

    <radialGradient id="capGrad" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#D8DDE5"/>
      <stop offset="100%" stop-color="#6D7480"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="80" y="72" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#202631">
    Quarterly KPI Health
  </text>
  <text x="82" y="106" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6B7280">
    Editable SVG speedometer gauge for executive status reporting
  </text>

  <rect x="155" y="135" width="970" height="500" rx="34" fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="185" y="165" width="910" height="440" rx="26" fill="#FFFFFF" opacity="0.62"/>

  <!-- Soft backing semi-donut: center=(640,500), outer radius=310, inner radius=205 -->
  <path d="M 330 500 A 310 310 0 0 1 950 500 L 845 500 A 205 205 0 0 0 435 500 Z"
        fill="#EEF2F7" filter="url(#softShadow)"/>

  <!-- Red zone: 0-33 -->
  <path d="M 330 500 A 310 310 0 0 1 485 231.5 L 537.5 322.5 A 205 205 0 0 0 435 500 Z"
        fill="#E23E57" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>

  <!-- Amber zone: 34-66 -->
  <path d="M 485 231.5 A 310 310 0 0 1 795 231.5 L 742.5 322.5 A 205 205 0 0 0 537.5 322.5 Z"
        fill="#F4A42C" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>

  <!-- Green zone: 67-100 -->
  <path d="M 795 231.5 A 310 310 0 0 1 950 500 L 845 500 A 205 205 0 0 0 742.5 322.5 Z"
        fill="#519872" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>

  <!-- Major tick marks -->
  <line x1="288" y1="500" x2="323" y2="500" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.40"/>
  <line x1="337" y1="325" x2="367" y2="342" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.32"/>
  <line x1="465" y1="197" x2="483" y2="227" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.32"/>
  <line x1="640" y1="148" x2="640" y2="183" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.32"/>
  <line x1="815" y1="197" x2="797" y2="227" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.32"/>
  <line x1="943" y1="325" x2="913" y2="342" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.32"/>
  <line x1="992" y1="500" x2="957" y2="500" stroke="#2B2B2B" stroke-width="4" stroke-linecap="round" opacity="0.40"/>

  <!-- Needle for score 72.5: angle = 49.5 degrees -->
  <path d="M 825 282 L 626 488 L 654 512 Z"
        fill="url(#needleGrad)" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"/>

  <circle cx="640" cy="500" r="43" fill="url(#capGrad)" stroke="#FFFFFF" stroke-width="5" filter="url(#softShadow)"/>
  <circle cx="628" cy="486" r="12" fill="#FFFFFF" opacity="0.75"/>

  <text x="256" y="550" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#E23E57" text-anchor="middle">
    Poor
  </text>
  <text x="640" y="215" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#C47C14" text-anchor="middle">
    Monitor
  </text>
  <text x="1024" y="550" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#519872" text-anchor="middle">
    Healthy
  </text>

  <text x="640" y="585" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" fill="#202631" text-anchor="middle">
    72.5%
  </text>
  <text x="640" y="617" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#6B7280" text-anchor="middle">
    Customer success readiness
  </text>

  <text x="195" y="674" width="890" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8B93A1" text-anchor="middle">
    Gauge bands and needle are native editable vector shapes; update the needle path points to reflect a new score.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a raster screenshot of a gauge; it defeats the editable chart purpose.
- ❌ Do not build the dial with `<mask>` or clipped non-image shapes; masks and clip-paths on shapes will not translate reliably.
- ❌ Do not use `<use>` to repeat tick marks; duplicate explicit `<line>` elements instead.
- ❌ Do not rely on `marker-end` arrowheads for the needle; draw the needle as an editable triangular `<path>`.
- ❌ Do not use SVG arc strokes with complex dash patterns as the only gauge bands if the bands need to be recolored or edited individually in PowerPoint.

## Composition notes
- Keep the gauge horizontally centered and place the pivot slightly below the card midpoint so the semi-circle has room to breathe.
- Use a thick dial band: inner radius should be roughly 65–70% of outer radius for a premium, legible executive look.
- Put qualitative labels near the visual zones, not in a separate legend; this makes the chart instantly readable.
- Reserve the bottom center for the numeric KPI and metric name, aligned with the pivot to reinforce the single-value focus.