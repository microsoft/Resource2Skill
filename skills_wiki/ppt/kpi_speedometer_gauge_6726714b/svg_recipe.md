# SVG Recipe — KPI Speedometer Gauge

## Visual mechanism
A single KPI is mapped to a 180° speedometer dial: the value determines both a prominent needle angle and a colored progress sweep, while the numeric percentage remains centered below the pivot for instant executive readability.

## SVG primitives needed
- 2× `<rect>` for the slide background and rounded dashboard card
- 1× `<path>` for the main cream-colored semicircular gauge body
- 3× `<path>` for thin red / amber / green threshold bands
- 2× `<path>` for the dark progress track and bright KPI progress sweep
- 1× `<path>` for the triangular needle
- 5× `<line>` for major gauge divider ticks
- 2× `<circle>` for the metallic pivot hub
- 12× `<text>` for title, KPI value, subtitle, end labels, and tick labels
- 4× `<linearGradient>` for background, card, gauge sheen, and progress color
- 1× `<radialGradient>` for the pivot hub
- 2× `<filter>` with blur / offset for card shadow, needle depth, and glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="slideBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#DDE7F1"/>
    </linearGradient>

    <linearGradient id="cardBg" x1="230" y1="105" x2="1050" y2="625" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2F527A"/>
      <stop offset="58%" stop-color="#214A79"/>
      <stop offset="100%" stop-color="#1C4477"/>
    </linearGradient>

    <linearGradient id="arcSheen" x1="390" y1="235" x2="890" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FBFAF0"/>
      <stop offset="62%" stop-color="#EEECE1"/>
      <stop offset="100%" stop-color="#DAD7C9"/>
    </linearGradient>

    <linearGradient id="progressGrad" x1="430" y1="500" x2="800" y2="355" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4AA3FF"/>
      <stop offset="50%" stop-color="#66D1FF"/>
      <stop offset="100%" stop-color="#8AF0C8"/>
    </linearGradient>

    <radialGradient id="hubMetal" cx="42%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="40%" stop-color="#B7C3CD"/>
      <stop offset="100%" stop-color="#4A5662"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#slideBg)"/>

  <text x="90" y="70" width="1100" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#3E4A56">
    Sales Performance Dashboard
  </text>
  <text x="92" y="105" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#728091">
    KPI speedometer gauge for quarterly target attainment
  </text>

  <rect x="230" y="105" width="820" height="520" rx="36" fill="url(#cardBg)" filter="url(#shadow)"/>
  <path d="M270 155 C370 120 510 122 640 150 C770 122 910 120 1010 155"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.16"/>

  <text x="285" y="175" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" opacity="0.92">
    TARGET ACHIEVEMENT
  </text>
  <text x="285" y="202" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#C9D6E6">
    Current run-rate versus committed quarterly goal
  </text>

  <!-- Thin outer threshold ribbon: red 0–50, amber 50–80, green 80–100 -->
  <path d="M370 500 A270 270 0 0 1 640 230 L640 247 A253 253 0 0 0 387 500 Z"
        fill="#E85C5C" opacity="0.98"/>
  <path d="M640 230 A270 270 0 0 1 858 341 L844 351 A253 253 0 0 0 640 247 Z"
        fill="#F5C84C" opacity="0.98"/>
  <path d="M858 341 A270 270 0 0 1 910 500 L893 500 A253 253 0 0 0 844 351 Z"
        fill="#49D18F" opacity="0.98"/>

  <!-- Main cream dial body -->
  <path d="M390 500 A250 250 0 0 1 890 500 L815 500 A175 175 0 0 0 465 500 Z"
        fill="url(#arcSheen)" filter="url(#shadow)"/>

  <!-- Inner progress track and current progress sweep: 76% -->
  <path d="M435 500 A205 205 0 0 1 845 500"
        fill="none" stroke="#183A60" stroke-width="18" stroke-linecap="round" opacity="0.75"/>
  <path d="M435 500 A205 205 0 0 1 789 360"
        fill="none" stroke="url(#progressGrad)" stroke-width="18" stroke-linecap="round" filter="url(#softGlow)"/>

  <!-- Major divider ticks -->
  <line x1="370" y1="500" x2="415" y2="500" stroke="#595959" stroke-width="4" stroke-linecap="round"/>
  <line x1="449" y1="309" x2="487" y2="347" stroke="#595959" stroke-width="4" stroke-linecap="round"/>
  <line x1="640" y1="230" x2="640" y2="282" stroke="#595959" stroke-width="4" stroke-linecap="round"/>
  <line x1="831" y1="309" x2="793" y2="347" stroke="#595959" stroke-width="4" stroke-linecap="round"/>
  <line x1="910" y1="500" x2="865" y2="500" stroke="#595959" stroke-width="4" stroke-linecap="round"/>

  <!-- Tick labels -->
  <text x="323" y="526" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">0%</text>
  <text x="424" y="294" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">25%</text>
  <text x="640" y="214" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">50%</text>
  <text x="856" y="294" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">75%</text>
  <text x="957" y="526" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">100%</text>

  <!-- Needle for 76%: angle = 180 - 76*1.8 = 43.2 degrees -->
  <path d="M808 342 L634 523 L616 504 Z"
        fill="#40464D" stroke="#2B3035" stroke-width="2" filter="url(#shadow)"/>
  <path d="M808 342 L642 509"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.22" stroke-linecap="round"/>

  <circle cx="640" cy="500" r="38" fill="#273647" opacity="0.95"/>
  <circle cx="640" cy="500" r="27" fill="url(#hubMetal)" stroke="#1D2630" stroke-width="3"/>

  <text x="570" y="584" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    76%
  </text>
  <text x="500" y="617" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#BFD0E3" text-anchor="middle">
    of quarterly sales target
  </text>

  <text x="855" y="178" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8AF0C8" text-anchor="end">
    STATUS: ON TRACK
  </text>
  <text x="855" y="202" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF" text-anchor="end">
    +11 pts
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` for the gauge needle; create the pointer as a triangular `<path>` so it remains editable.
- ❌ Do not apply `filter` to `<line>` tick marks; shadows/glows on lines may be dropped.
- ❌ Do not use `<textPath>` to curve labels around the dial; place each label as normal editable `<text>`.
- ❌ Do not use clipping or masks to cut the gauge ring; build annular arcs directly with filled `<path>` geometry.

## Composition notes
- Keep the pivot near the lower center of the card, leaving the upper semicircle as the main visual arena.
- Reserve the lower center for the large KPI value; it should be readable even if the audience ignores the tick labels.
- Use a dark card with a light dial for strong contrast, then add a narrow red/amber/green ribbon to communicate performance zones.
- The needle should be the topmost object, with a subtle shadow and metallic hub to make the gauge feel dimensional.