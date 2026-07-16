# SVG Recipe — Alternating Vertical Timeline

## Visual mechanism
A thin central spine anchors a sequence of numbered circular nodes, while content cards alternate left and right to create visual balance and a natural top-to-bottom reading path. Colored connector stems, accent bars, and subtle shadows make the diagram feel precise, corporate, and presentation-ready.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft background
- 2× `<path>` for faint organic corner accents that add depth without distracting
- 1× `<rect>` for the central vertical spine
- 1× narrow `<rect>` highlight on the spine for a polished beveled feel
- 5× `<rect>` for horizontal connector stems from the spine to each card
- 5× rounded `<rect>` for elevated milestone cards
- 5× narrow `<rect>` for colored accent bars on the cards
- 5× rounded `<rect>` for small phase/date pills
- 10× `<circle>` for node bases and colored node rings
- 17× `<text>` elements for title, subtitle, node numbers, phase labels, card titles, and body copy
- 1× `<linearGradient>` for the background wash
- 1× `<filter id="cardShadow">` for soft card elevation
- 1× `<filter id="nodeShadow">` for premium circular node depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#FAFAFA"/>
      <stop offset="100%" stop-color="#F1F5F7"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="nodeShadow" x="-40%" y="-40%" width="180%" height="190%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-80,96 C52,8 148,28 224,94 C292,154 366,160 420,124 C370,230 248,282 126,240 C24,205 -40,164 -80,96 Z"
        fill="#00A88F" opacity="0.055"/>
  <path d="M1390,602 C1266,714 1120,724 1034,650 C956,582 890,568 818,606 C886,500 1018,452 1146,486 C1256,516 1332,548 1390,602 Z"
        fill="#0072BC" opacity="0.06"/>

  <text x="640" y="54" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#323232">
    PROJECT ROADMAP
  </text>
  <text x="640" y="88" width="680" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="400" fill="#69747A">
    Five-step execution timeline with alternating milestone ownership
  </text>

  <rect x="637" y="132" width="6" height="500" rx="3" fill="#CED6DA"/>
  <rect x="639" y="132" width="2" height="500" rx="1" fill="#FFFFFF" opacity="0.68"/>

  <!-- Step 01: left -->
  <rect x="520" y="150" width="90" height="6" rx="3" fill="#00A88F"/>
  <rect x="118" y="110" width="402" height="92" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="509" y="126" width="8" height="60" rx="4" fill="#00A88F"/>
  <rect x="376" y="122" width="114" height="24" rx="12" fill="#E7F7F4"/>
  <text x="433" y="139" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#00A88F">PHASE 01</text>
  <text x="490" y="165" width="330" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#00A88F">Project Kickoff</text>
  <text x="490" y="186" width="340" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4E5B61">
    <tspan x="490" dy="0">Define vision, success metrics, and</tspan>
    <tspan x="490" dy="17">assemble the core delivery team.</tspan>
  </text>
  <circle cx="640" cy="153" r="34" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="640" cy="153" r="29" fill="#FFFFFF" stroke="#00A88F" stroke-width="7"/>
  <text x="640" y="164" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800" fill="#00A88F">01</text>

  <!-- Step 02: right -->
  <rect x="670" y="265" width="90" height="6" rx="3" fill="#F26C4F"/>
  <rect x="760" y="225" width="402" height="92" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="763" y="241" width="8" height="60" rx="4" fill="#F26C4F"/>
  <rect x="790" y="237" width="114" height="24" rx="12" fill="#FDEDE9"/>
  <text x="847" y="254" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#F26C4F">PHASE 02</text>
  <text x="790" y="280" width="330" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#F26C4F">Market Analysis</text>
  <text x="790" y="301" width="340" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4E5B61">
    <tspan x="790" dy="0">Map competitor moves and identify</tspan>
    <tspan x="790" dy="17">priority customer segments.</tspan>
  </text>
  <circle cx="640" cy="268" r="34" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="640" cy="268" r="29" fill="#FFFFFF" stroke="#F26C4F" stroke-width="7"/>
  <text x="640" y="279" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800" fill="#F26C4F">02</text>

  <!-- Step 03: left -->
  <rect x="520" y="380" width="90" height="6" rx="3" fill="#88C340"/>
  <rect x="118" y="340" width="402" height="92" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="509" y="356" width="8" height="60" rx="4" fill="#88C340"/>
  <rect x="376" y="352" width="114" height="24" rx="12" fill="#F1FAE8"/>
  <text x="433" y="369" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#6EA62D">PHASE 03</text>
  <text x="490" y="395" width="330" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#6EA62D">Product Development</text>
  <text x="490" y="416" width="340" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4E5B61">
    <tspan x="490" dy="0">Design, prototype, and engineer the</tspan>
    <tspan x="490" dy="17">minimum viable release package.</tspan>
  </text>
  <circle cx="640" cy="383" r="34" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="640" cy="383" r="29" fill="#FFFFFF" stroke="#88C340" stroke-width="7"/>
  <text x="640" y="394" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800" fill="#6EA62D">03</text>

  <!-- Step 04: right -->
  <rect x="670" y="495" width="90" height="6" rx="3" fill="#0072BC"/>
  <rect x="760" y="455" width="402" height="92" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="763" y="471" width="8" height="60" rx="4" fill="#0072BC"/>
  <rect x="790" y="467" width="114" height="24" rx="12" fill="#E8F2FA"/>
  <text x="847" y="484" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#0072BC">PHASE 04</text>
  <text x="790" y="510" width="330" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#0072BC">Beta Launch</text>
  <text x="790" y="531" width="340" text-anchor="start"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4E5B61">
    <tspan x="790" dy="0">Release to early adopters, monitor</tspan>
    <tspan x="790" dy="17">feedback, and resolve QA issues.</tspan>
  </text>
  <circle cx="640" cy="498" r="34" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="640" cy="498" r="29" fill="#FFFFFF" stroke="#0072BC" stroke-width="7"/>
  <text x="640" y="509" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800" fill="#0072BC">04</text>

  <!-- Step 05: left -->
  <rect x="520" y="610" width="90" height="6" rx="3" fill="#5B6DE8"/>
  <rect x="118" y="570" width="402" height="92" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="509" y="586" width="8" height="60" rx="4" fill="#5B6DE8"/>
  <rect x="376" y="582" width="114" height="24" rx="12" fill="#EEF0FF"/>
  <text x="433" y="599" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#5B6DE8">PHASE 05</text>
  <text x="490" y="625" width="330" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#5B6DE8">Scale Rollout</text>
  <text x="490" y="646" width="340" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#4E5B61">
    <tspan x="490" dy="0">Launch broadly, operationalize support,</tspan>
    <tspan x="490" dy="17">and track adoption KPIs.</tspan>
  </text>
  <circle cx="640" cy="613" r="34" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="640" cy="613" r="29" fill="#FFFFFF" stroke="#5B6DE8" stroke-width="7"/>
  <text x="640" y="624" width="70" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800" fill="#5B6DE8">05</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` to connector `<line>` elements; use slim rounded `<rect>` stems instead if you need polish.
- ❌ Using `marker-end` arrowheads on timeline connectors; they may disappear, and this technique should feel like a precise roadmap rather than a flowchart.
- ❌ Putting card text directly over the spine; maintain a clear gutter around the central axis.
- ❌ Omitting `width` on `<text>` elements; PowerPoint translation needs explicit text box widths for clean editable output.
- ❌ Using masks or clip paths on non-image elements for the cards; rounded `<rect>` shapes are cleaner and fully editable.

## Composition notes
- Keep the spine exactly centered and reserve a 120–150 px vertical gutter around it so nodes and stems remain visually dominant.
- Alternate card alignment: left-side cards use right-aligned text, right-side cards use left-aligned text, so copy “hugs” the timeline.
- Use one strong accent color per milestone; repeat it on the stem, node ring, card bar, phase pill, and title for cohesion.
- Leave generous whitespace above the first node for the title and below the last node so the timeline feels intentional rather than crowded.