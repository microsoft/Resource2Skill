# SVG Recipe — Bipartite Sliding Comparison

## Visual mechanism
Build a 2560px-wide “virtual stage” containing both comparison states, then crop it through the 1280×720 slide viewBox. A large laptop mockup straddles the seam between the two states, so duplicating the slide and translating the whole stage left by 1280px creates the illusion of a smooth horizontal push reveal.

## SVG primitives needed
- 1× large `<g id="stage">` for the 2560px-wide sliding canvas; duplicate the slide and change its transform to `translate(-1280 0)` for state 2.
- 2× topic content groups for left and right comparison narratives.
- 1× oversized laptop mockup built from `<rect>`, `<path>`, and gradients, centered on the seam between the two slides.
- 1× `<image>` for the shared thematic hero photo inside the laptop screen.
- 1× `<clipPath>` with rounded `<rect>` applied to the laptop screen image.
- 2× translucent `<rect>` color washes over the laptop screen image, one red and one blue, split at the slide seam.
- 8× KPI rows made from `<text>`, small `<rect>` metric pills, and mini bar indicators.
- 2× circular icon badges using `<circle>` plus simple `<path>` glyphs.
- 2× `<linearGradient>` fills for laptop metal and subtle background accents.
- 1× `<filter id="softShadow">` applied to laptop body and cards for premium depth.
- 1× `<filter id="glowRed">` and 1× `<filter id="glowBlue">` applied to accent halos behind the topic icons.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f7f7"/>
      <stop offset="100%" stop-color="#eceff4"/>
    </linearGradient>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f5f6f8"/>
      <stop offset="45%" stop-color="#cfd4db"/>
      <stop offset="100%" stop-color="#8f98a4"/>
    </linearGradient>
    <linearGradient id="bezel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#171a21"/>
      <stop offset="100%" stop-color="#05070b"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glowRed" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="glowBlue" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <clipPath id="screenClip">
      <rect x="835" y="142" width="890" height="458" rx="18"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Sliding stage: duplicate slide and change this transform to translate(-1280 0) for the second state -->
  <g id="stage" transform="translate(0 0)">
    <rect x="0" y="0" width="2560" height="720" fill="url(#bgWash)"/>

    <!-- LEFT TOPIC CONTENT -->
    <g id="legacyContent">
      <circle cx="118" cy="112" r="46" fill="#de0100" opacity="0.25" filter="url(#glowRed)"/>
      <circle cx="118" cy="112" r="38" fill="#333333"/>
      <path d="M96 119 C104 99,132 96,142 114 C147 124,140 135,128 137 C114 140,101 132,96 119 Z" fill="#ffffff"/>
      <path d="M111 94 L120 82 L128 95" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
      <text x="174" y="91" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#595959">CURRENT OPERATING MODEL</text>
      <text x="70" y="178" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="900" fill="#de0100" letter-spacing="-2">LEGACY STACK</text>
      <text x="74" y="218" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">Stable, familiar, but increasingly slow to adapt when the market shifts.</text>

      <g transform="translate(72 284)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#de0100">CYCLE TIME</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Manual handoffs create drag.</text>
        <rect x="348" y="21" width="92" height="28" rx="14" fill="#de0100"/>
        <text x="366" y="41" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#ffffff">42 DAYS</text>
      </g>

      <g transform="translate(72 374)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#de0100">COST TO SERVE</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Fragmented tooling inflates support.</text>
        <rect x="334" y="32" width="118" height="10" rx="5" fill="#f1c0c0"/>
        <rect x="334" y="32" width="96" height="10" rx="5" fill="#de0100"/>
      </g>

      <g transform="translate(72 464)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#de0100">DATA LATENCY</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Reports arrive after decisions are made.</text>
        <rect x="348" y="21" width="92" height="28" rx="14" fill="#de0100"/>
        <text x="367" y="41" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#ffffff">T+9</text>
      </g>

      <g transform="translate(72 554)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#de0100">EXPERIMENT RATE</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Low throughput limits learning.</text>
        <rect x="334" y="32" width="118" height="10" rx="5" fill="#f1c0c0"/>
        <rect x="334" y="32" width="38" height="10" rx="5" fill="#de0100"/>
      </g>
    </g>

    <!-- RIGHT TOPIC CONTENT, positioned one slide-width to the right -->
    <g id="futureContent" transform="translate(1280 0)">
      <circle cx="1162" cy="112" r="46" fill="#12338a" opacity="0.25" filter="url(#glowBlue)"/>
      <circle cx="1162" cy="112" r="38" fill="#333333"/>
      <path d="M1141 124 L1155 100 L1164 115 L1174 96 L1185 124 Z" fill="none" stroke="#ffffff" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>
      <text x="650" y="91" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#595959" text-anchor="end">TARGET OPERATING MODEL</text>
      <text x="650" y="178" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="900" fill="#12338a" letter-spacing="-2" text-anchor="start">FUTURE STACK</text>
      <text x="654" y="218" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">Automated, instrumented, and designed for fast strategic pivots.</text>

      <g transform="translate(720 284)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#12338a">CYCLE TIME</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Automated orchestration compresses flow.</text>
        <rect x="348" y="21" width="92" height="28" rx="14" fill="#12338a"/>
        <text x="371" y="41" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#ffffff">6 DAYS</text>
      </g>

      <g transform="translate(720 374)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#12338a">COST TO SERVE</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Shared services reduce duplicated effort.</text>
        <rect x="334" y="32" width="118" height="10" rx="5" fill="#ccd6f5"/>
        <rect x="334" y="32" width="52" height="10" rx="5" fill="#12338a"/>
      </g>

      <g transform="translate(720 464)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#12338a">DATA LATENCY</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Live instrumentation powers decisions.</text>
        <rect x="348" y="21" width="92" height="28" rx="14" fill="#12338a"/>
        <text x="365" y="41" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#ffffff">REALTIME</text>
      </g>

      <g transform="translate(720 554)">
        <rect x="0" y="0" width="490" height="70" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
        <text x="24" y="29" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#12338a">EXPERIMENT RATE</text>
        <text x="24" y="52" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#666666">Teams test, measure, and scale faster.</text>
        <rect x="334" y="32" width="118" height="10" rx="5" fill="#ccd6f5"/>
        <rect x="334" y="32" width="108" height="10" rx="5" fill="#12338a"/>
      </g>
    </g>

    <!-- LAPTOP MOCKUP STRADDLING THE SEAM AT x=1280 -->
    <g id="seamLaptop" filter="url(#softShadow)">
      <rect x="785" y="96" width="990" height="550" rx="34" fill="url(#bezel)"/>
      <rect x="818" y="128" width="924" height="500" rx="24" fill="#05070b"/>
      <image href="https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&amp;fit=crop&amp;w=1600&amp;q=80" x="835" y="142" width="890" height="458" preserveAspectRatio="xMidYMid slice" clip-path="url(#screenClip)"/>
      <rect x="835" y="142" width="445" height="458" fill="#de0100" opacity="0.46"/>
      <rect x="1280" y="142" width="445" height="458" fill="#12338a" opacity="0.50"/>
      <path d="M728 646 H1832 L1888 690 C1898 698,1888 712,1868 712 H692 C672 712,662 698,672 690 Z" fill="url(#metal)"/>
      <rect x="1186" y="658" width="188" height="16" rx="8" fill="#7f8790" opacity="0.7"/>
      <line x1="1280" y1="142" x2="1280" y2="600" stroke="#ffffff" stroke-width="2" stroke-opacity="0.45" stroke-dasharray="8 8"/>
    </g>
  </g>

  <text x="70" y="690" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8a8a8a">Slide 1 shows the left half. For Slide 2, translate the stage by -1280px and apply PowerPoint Push transition from right.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG animation; the slide-to-slide movement should be a PowerPoint Push transition, not `<animate>` or `<animateTransform>`.
- ❌ Do not use `<mask>` for the laptop screen; use a `<clipPath>` applied only to the `<image>`.
- ❌ Do not rely on `clip-path` for colored overlay rectangles; keep overlays exactly inside the screen bounds or let the bezel hide their edges.
- ❌ Do not use `<use>` to duplicate KPI cards or icons; repeat the shapes explicitly so PPT-Master converts them into editable objects.
- ❌ Do not use `marker-end` on paths for directional hints; if arrows are needed, build them from `<line>` plus small `<path>` arrowheads.

## Composition notes
- Treat the full composition as a 2560×720 stage: left topic occupies x=0–640, right topic occupies x=1920–2560, and the laptop is centered on the seam at x=1280.
- Keep the laptop oversized and partially off-slide in each state; the crop is what makes the comparison feel cinematic rather than like a basic two-column layout.
- Use one shared image inside the laptop so the two states feel connected, then split the mood with red and blue translucent washes.
- Leave generous negative space around the text columns; the laptop edge should dominate the opposite side and create anticipation for the pushed reveal.