# SVG Recipe — Continuous Scrolling Timeline

## Visual mechanism
A long horizontal timeline is treated as one oversized “world canvas,” while each slide is only a viewport into it. Repeating the same axis height, milestone spacing, and global x-positions across slides lets PowerPoint’s Push transition create the illusion of a single timeline scrolling continuously.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm neutral background
- 2× `<path>` for subtle decorative background ribbons that imply motion
- 1× `<path>` for the continuous timeline rail extending beyond the slide edges
- 7× `<circle>` for milestone halos and filled active/inactive markers
- 7× `<text>` for milestone numbers inside markers
- 6× `<rect>` for floating text cards paired with milestones
- 12× `<text>` for milestone titles and body copy, staggered above/below the axis
- 2× `<rect>` with linear-gradient fills for soft left/right viewport edge fades
- 1× `<linearGradient>` for the timeline rail
- 2× `<linearGradient>` for viewport fades
- 1× `<radialGradient>` for the active milestone glow
- 2× `<filter>` definitions for soft card shadows and active-marker glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="railGrad" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#d6d6d6"/>
      <stop offset="42%" stop-color="#ffc000"/>
      <stop offset="58%" stop-color="#ffc000"/>
      <stop offset="100%" stop-color="#d6d6d6"/>
    </linearGradient>

    <linearGradient id="fadeLeft" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f4f2ee"/>
      <stop offset="100%" stop-color="#f4f2ee" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="fadeRight" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#f4f2ee"/>
      <stop offset="100%" stop-color="#f4f2ee" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="activeGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#ffc000" stop-opacity="0.85"/>
      <stop offset="65%" stop-color="#ffc000" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#ffc000" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f4f2ee"/>

  <path d="M-40 146 C180 78, 300 120, 475 84 C710 36, 850 132, 1040 94 C1195 63, 1325 78, 1400 38"
        fill="none" stroke="#ffffff" stroke-width="44" stroke-opacity="0.6"/>
  <path d="M-60 610 C150 542, 330 602, 520 565 C720 526, 905 592, 1090 548 C1230 515, 1320 542, 1385 500"
        fill="none" stroke="#e8e3da" stroke-width="36" stroke-opacity="0.75"/>

  <text x="72" y="72" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#333333">
    GLOBAL ROLLOUT ROADMAP
  </text>
  <text x="72" y="104" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#77736c">
    Slide viewport 02 / 04 · use Push transition “From Right” on the following slide
  </text>

  <g id="scrolling-world" transform="translate(0 0)">
    <path d="M-260 360 L1540 360" fill="none" stroke="url(#railGrad)" stroke-width="8" stroke-linecap="round"/>

    <circle cx="-90" cy="360" r="25" fill="#f4f2ee" stroke="#a9a49b" stroke-width="3"/>
    <text x="-106" y="370" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" text-anchor="middle" fill="#a9a49b">1</text>

    <rect x="68" y="160" width="260" height="118" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
    <text x="92" y="198" width="212" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="1.5" fill="#333333">DISCOVERY</text>
    <text x="92" y="228" width="216" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#69645d">
      Validate customer segments, align executive sponsors, and define measurable launch criteria.
    </text>
    <circle cx="198" cy="360" r="28" fill="#f4f2ee" stroke="#333333" stroke-width="3"/>
    <circle cx="198" cy="360" r="13" fill="#ffc000"/>
    <text x="182" y="370" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" text-anchor="middle" fill="#333333">2</text>

    <rect x="356" y="446" width="260" height="118" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
    <text x="380" y="484" width="212" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="1.5" fill="#333333">PILOT BUILD</text>
    <text x="380" y="514" width="216" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#69645d">
      Prototype the operating model, test integrations, and capture early adoption signals.
    </text>
    <circle cx="486" cy="360" r="28" fill="#f4f2ee" stroke="#333333" stroke-width="3"/>
    <circle cx="486" cy="360" r="13" fill="#ffc000"/>
    <text x="470" y="370" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" text-anchor="middle" fill="#333333">3</text>

    <circle cx="774" cy="360" r="62" fill="url(#activeGlow)" filter="url(#softGlow)"/>
    <circle cx="774" cy="360" r="36" fill="#ffc000" stroke="#333333" stroke-width="3"/>
    <circle cx="774" cy="360" r="50" fill="none" stroke="#ffc000" stroke-width="3"/>
    <text x="758" y="372" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="900" text-anchor="middle" fill="#333333">4</text>
    <rect x="644" y="142" width="260" height="128" rx="24" fill="#fffaf0" filter="url(#cardShadow)"/>
    <text x="668" y="182" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="900" letter-spacing="1.5" fill="#333333">MARKET LAUNCH</text>
    <text x="668" y="213" width="216" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#5f594e">
      Activate priority regions with sales enablement, channel kits, and a command-center cadence.
    </text>

    <rect x="932" y="446" width="260" height="118" rx="22" fill="#ffffff" filter="url(#cardShadow)"/>
    <text x="956" y="484" width="212" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="1.5" fill="#333333">SCALE-UP</text>
    <text x="956" y="514" width="216" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#69645d">
      Expand the playbook, automate reporting, and convert learnings into repeatable motions.
    </text>
    <circle cx="1062" cy="360" r="28" fill="#f4f2ee" stroke="#333333" stroke-width="3"/>
    <circle cx="1062" cy="360" r="13" fill="#ffc000"/>
    <text x="1046" y="370" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" text-anchor="middle" fill="#333333">5</text>

    <circle cx="1350" cy="360" r="25" fill="#f4f2ee" stroke="#a9a49b" stroke-width="3"/>
    <text x="1334" y="370" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" text-anchor="middle" fill="#a9a49b">6</text>
  </g>

  <rect x="0" y="0" width="150" height="720" fill="url(#fadeLeft)"/>
  <rect x="1130" y="0" width="150" height="720" fill="url(#fadeRight)"/>

  <text x="72" y="664" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8a857d">
    Keep the axis y-position and milestone spacing identical on every slide.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not redraw each slide with “locally centered” milestones; calculate positions from one shared global timeline so the Push transition stays seamless.
- ❌ Do not use `marker-end` arrows on the timeline rail; arrowheads may disappear. If direction is needed, use small native `<path>` chevrons instead.
- ❌ Do not clip or mask shape groups to fake a viewport; the slide itself is the viewport. Let off-slide elements extend beyond x=0 and x=1280.
- ❌ Do not change the timeline axis y-value, rail thickness, or marker radius between slides; tiny mismatches become obvious during the transition.
- ❌ Do not rely on PowerPoint animations inside the SVG. The scrolling illusion comes from the manual slide transition, not SVG animation.

## Composition notes
- Keep the timeline rail locked to the same vertical center, usually y=360 on a 1280×720 canvas.
- Stagger cards above and below the rail to maintain rhythm and avoid crowding; reserve at least 120 px of open space near the slide edges for the incoming/outgoing motion.
- Use one active milestone per viewport with a brighter fill, halo, or glow, while adjacent milestones remain quieter for continuity.
- For multi-slide builds, shift the same global timeline left by a constant amount per slide, then apply PowerPoint Push → From Right to slides 2 onward.