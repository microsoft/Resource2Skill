# SVG Recipe — Data-Driven Block Arrow Timeline

## Visual mechanism
Use tall, bottom-aligned block-arrow shapes as both data bars and directional symbols: height encodes magnitude while the upward arrowhead communicates growth. Each arrow contains its own KPI value and label, creating a self-contained timeline without needing a separate legend or heavy chart axis.

## SVG primitives needed
- 2× `<rect>` for the slide background and title accent bar.
- 3× `<path>` for editable upward block arrows with data-driven heights.
- 2× `<path>` for small right-facing chevrons between timeline periods.
- 1× `<path>` for a subtle decorative growth sparkline near the title.
- 7× `<line>` for the baseline axis, tick marks, and faint horizontal guide rules.
- 3× `<circle>` for timeline nodes beneath each arrow.
- Multiple `<text>` elements with explicit `width` for title, subtitle, KPI values, arrow labels, guide labels, and period labels.
- 1× `<linearGradient id="growthGrad">` for premium green arrow fills.
- 1× `<linearGradient id="bgGrad">` for a soft executive-style background.
- 1× `<filter id="softShadow">` applied to the arrow paths and chevrons.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="64%" stop-color="#F6F8F4"/>
      <stop offset="100%" stop-color="#EDF4E8"/>
    </linearGradient>

    <linearGradient id="growthGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#B9E878"/>
      <stop offset="48%" stop-color="#9CCC65"/>
      <stop offset="100%" stop-color="#72A93D"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- Left title system -->
  <rect x="72" y="78" width="8" height="112" rx="4" fill="#9CCC65"/>
  <text x="98" y="104" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="38" fill="#9A9A9A" font-weight="300">
    Transition of
  </text>
  <text x="98" y="150" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="36" fill="#252A2D" font-weight="700">
    Annual Advertising
  </text>
  <text x="98" y="194" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="36" fill="#252A2D" font-weight="700">
    Expenditures
  </text>
  <text x="98" y="236" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6F7772">
    Data values are embedded inside each growth arrow to create a compact timeline narrative.
  </text>

  <!-- Decorative growth sparkline -->
  <path d="M100 304 C145 294, 168 306, 208 282 C244 260, 286 266, 326 225"
        fill="none" stroke="#9CCC65" stroke-width="5" stroke-linecap="round"/>
  <circle cx="326" cy="225" r="8" fill="#9CCC65"/>
  <text x="98" y="340" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8A928B" letter-spacing="1.8">
    GROWTH STORYLINE
  </text>

  <!-- Faint guide rules behind data region -->
  <line x1="485" y1="195" x2="1158" y2="195" stroke="#DDE7D6" stroke-width="1" stroke-dasharray="7 9"/>
  <line x1="485" y1="340" x2="1158" y2="340" stroke="#DDE7D6" stroke-width="1" stroke-dasharray="7 9"/>
  <line x1="485" y1="485" x2="1158" y2="485" stroke="#DDE7D6" stroke-width="1" stroke-dasharray="7 9"/>
  <text x="432" y="199" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A1AAA2" text-anchor="end">High</text>
  <text x="432" y="344" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A1AAA2" text-anchor="end">Mid</text>
  <text x="432" y="489" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A1AAA2" text-anchor="end">Low</text>

  <!-- Baseline axis -->
  <line x1="470" y1="625" x2="1170" y2="625" stroke="#C7D0C4" stroke-width="2"/>
  <line x1="598" y1="612" x2="598" y2="638" stroke="#C7D0C4" stroke-width="2"/>
  <line x1="818" y1="612" x2="818" y2="638" stroke="#C7D0C4" stroke-width="2"/>
  <line x1="1038" y1="612" x2="1038" y2="638" stroke="#C7D0C4" stroke-width="2"/>

  <!-- Data-driven block arrows: bottom aligned at y=625 -->
  <path filter="url(#softShadow)" fill="url(#growthGrad)" stroke="#7EAF46" stroke-width="1.5"
        d="M598 395 L675 463 L638 463 L638 625 L557 625 L557 463 L520 463 Z"/>
  <path filter="url(#softShadow)" fill="url(#growthGrad)" stroke="#7EAF46" stroke-width="1.5"
        d="M818 270 L895 352 L858 352 L858 625 L777 625 L777 352 L740 352 Z"/>
  <path filter="url(#softShadow)" fill="url(#growthGrad)" stroke="#7EAF46" stroke-width="1.5"
        d="M1038 125 L1115 221 L1078 221 L1078 625 L997 625 L997 221 L960 221 Z"/>

  <!-- Inter-period chevrons -->
  <path filter="url(#softShadow)" d="M700 513 L720 493 L720 505 L744 505 L744 521 L720 521 L720 533 Z"
        fill="#AFC79D"/>
  <path filter="url(#softShadow)" d="M920 438 L940 418 L940 430 L964 430 L964 446 L940 446 L940 458 Z"
        fill="#AFC79D"/>

  <!-- KPI text inside arrows -->
  <text x="536" y="505" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800"
        fill="#FFFFFF" text-anchor="middle">
    <tspan x="598">$5B</tspan>
  </text>
  <text x="536" y="544" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#F7FFF0" text-anchor="middle">
    <tspan x="598">Internet</tspan>
    <tspan x="598" dy="19">Advertising</tspan>
    <tspan x="598" dy="19">Display</tspan>
  </text>

  <text x="756" y="408" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800"
        fill="#FFFFFF" text-anchor="middle">
    <tspan x="818">$30B</tspan>
  </text>
  <text x="756" y="448" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#F7FFF0" text-anchor="middle">
    <tspan x="818">Search</tspan>
    <tspan x="818" dy="19">and Online</tspan>
    <tspan x="818" dy="19">Performance</tspan>
  </text>

  <text x="976" y="292" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800"
        fill="#FFFFFF" text-anchor="middle">
    <tspan x="1038">$35B+</tspan>
  </text>
  <text x="976" y="334" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#F7FFF0" text-anchor="middle">
    <tspan x="1038">Call</tspan>
    <tspan x="1038" dy="19">Advertising</tspan>
    <tspan x="1038" dy="19">Models</tspan>
  </text>

  <!-- Timeline nodes and period labels -->
  <circle cx="598" cy="625" r="7" fill="#FFFFFF" stroke="#7EAF46" stroke-width="3"/>
  <circle cx="818" cy="625" r="7" fill="#FFFFFF" stroke="#7EAF46" stroke-width="3"/>
  <circle cx="1038" cy="625" r="7" fill="#FFFFFF" stroke="#7EAF46" stroke-width="3"/>

  <text x="518" y="666" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6E766F"
        text-anchor="middle">1995–2000</text>
  <text x="738" y="666" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6E766F"
        text-anchor="middle">2000–2010</text>
  <text x="958" y="666" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6E766F"
        text-anchor="middle">2010+</text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` on `<path>` for arrowheads; build chevrons or arrows as editable `<path>` geometry instead.
- ❌ Applying filters to `<line>` elements for the axis or guide rules; shadows on lines are dropped.
- ❌ Drawing the timeline as a screenshot or flattened image; the value of this pattern is fully editable arrow geometry and text.
- ❌ Placing labels in separate legends far from the arrows; the data should live inside the arrow containers.
- ❌ Forgetting `width` on `<text>` elements; PowerPoint text layout will otherwise be unreliable.

## Composition notes
- Keep all arrows bottom-aligned to a shared baseline so the audience reads them as a timeline and a bar chart simultaneously.
- Reserve the left third of the slide for a strong typographic title; place the data sequence in the right two-thirds.
- Use one dominant growth color with subtle gradients and shadows; avoid rainbow palettes because they weaken the progression story.
- Increase arrow height by data ratio, but keep arrow width consistent so magnitude is read vertically rather than by area.