# SVG Recipe — Proportional Split Bar

## Visual mechanism
A single horizontal bar is split into adjacent segments whose widths represent each segment’s share of the total, with labels embedded in the colored blocks and a bottom bracket spanning the full bar to reinforce the summed total. The technique works best when values can be parsed from segment titles, then normalized into proportional widths.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 2× decorative `<path>` shapes for soft executive-style backdrop geometry
- 3× segment shapes: 2× rounded-end `<path>` for the first/last segments and 1× `<rect>` for the middle segment
- 2× `<line>` for internal segment dividers
- 3× dashed `<line>` guides from segment boundaries down to the total bracket
- 1× bracket `<path>` spanning the total width
- 1× subtle base `<rect>` behind the bar for depth
- 8× `<text>` elements for headline, subtitle, segment labels, percentages, and total annotation
- 4× `<linearGradient>` fills for background and segment color harmony
- 1× `<filter id="softShadow">` applied to the bar base and colored segments

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="segA" x1="150" y1="340" x2="738" y2="424" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2554D8"/>
      <stop offset="100%" stop-color="#2E7BFF"/>
    </linearGradient>

    <linearGradient id="segB" x1="738" y1="340" x2="1032" y2="424" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#20A4B8"/>
      <stop offset="100%" stop-color="#36D1C4"/>
    </linearGradient>

    <linearGradient id="segC" x1="1032" y1="340" x2="1130" y2="424" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F2A23A"/>
      <stop offset="100%" stop-color="#FFC857"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-35%" width="120%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05  0 0 0 0 0.10  0 0 0 0 0.18  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M905 62 C1055 20 1198 78 1268 186 L1268 0 L905 0 Z" fill="#DCE8F7" opacity="0.62"/>
  <path d="M-28 612 C118 548 260 592 370 720 L0 720 Z" fill="#E9D8FF" opacity="0.48"/>

  <text x="150" y="112" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#102033">
    FY25 Revenue Mix by Business Line
  </text>
  <text x="150" y="154" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#627084">
    Segment widths are normalized from the values in each label: 60 + 30 + 10 = 100.
  </text>

  <text x="150" y="258" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#6A7484" letter-spacing="1.2">
    PROPORTIONAL SPLIT
  </text>
  <text x="150" y="292" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="600" fill="#172436">
    Total addressable portfolio allocation
  </text>

  <rect x="142" y="332" width="996" height="100" rx="30" fill="#D5DEE9" opacity="0.55" filter="url(#softShadow)"/>

  <!-- Total bar width = 980. Values: Cloud 60, Services 30, Hardware 10. Segment widths: 588, 294, 98. -->
  <path d="M174 340 H738 V424 H174 Q150 424 150 400 V364 Q150 340 174 340 Z" fill="url(#segA)" filter="url(#softShadow)"/>
  <rect x="738" y="340" width="294" height="84" fill="url(#segB)" filter="url(#softShadow)"/>
  <path d="M1032 340 H1106 Q1130 340 1130 364 V400 Q1130 424 1106 424 H1032 Z" fill="url(#segC)" filter="url(#softShadow)"/>

  <line x1="738" y1="348" x2="738" y2="416" stroke="#FFFFFF" stroke-width="3" opacity="0.72"/>
  <line x1="1032" y1="348" x2="1032" y2="416" stroke="#FFFFFF" stroke-width="3" opacity="0.72"/>

  <text x="184" y="374" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#FFFFFF">
    Cloud platform
  </text>
  <text x="184" y="405" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#FFFFFF">
    60%
  </text>

  <text x="766" y="374" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#FFFFFF">
    Advisory services
  </text>
  <text x="766" y="405" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#FFFFFF">
    30%
  </text>

  <text x="1048" y="374" width="76" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#3C2800">
    HW
  </text>
  <text x="1048" y="405" width="76" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#3C2800">
    10%
  </text>

  <line x1="150" y1="444" x2="150" y2="493" stroke="#8793A3" stroke-width="1.5" stroke-dasharray="5 7"/>
  <line x1="738" y1="444" x2="738" y2="493" stroke="#8793A3" stroke-width="1.5" stroke-dasharray="5 7"/>
  <line x1="1032" y1="444" x2="1032" y2="493" stroke="#8793A3" stroke-width="1.5" stroke-dasharray="5 7"/>

  <path d="M150 488 V516 H1130 V488" fill="none" stroke="#263445" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="470" y="560" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#263445" text-anchor="middle">
    Total portfolio = 100%
  </text>
  <text x="470" y="590" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#687586" text-anchor="middle">
    Bracket spans the full normalized bar width
  </text>

  <rect x="905" y="548" width="225" height="56" rx="18" fill="#FFFFFF" opacity="0.82"/>
  <text x="930" y="582" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#506071">
    Formula: value ÷ total
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not fake proportions with equal-width blocks; the visual promise depends on segment widths matching parsed values.
- ❌ Do not use `clip-path` on non-image shapes to create rounded segment ends; draw rounded first/last segments directly as `<path>`.
- ❌ Do not put shadows on divider `<line>` elements; filters on lines may be dropped.
- ❌ Do not use arrow markers for the bracket; draw the bracket as a simple stroked `<path>`.
- ❌ Do not overcrowd small segments with long labels; use abbreviations or external callouts when a segment falls below ~12% width.

## Composition notes
- Keep the split bar as the dominant object, usually spanning 70–80% of slide width and sitting slightly below vertical center.
- Reserve the upper-left quadrant for the headline and explanatory subtitle; keep the bar area visually clean.
- Use a harmonious gradient sequence across segments, with thin white dividers to clarify boundaries without breaking proportional continuity.
- Place the total bracket below the bar with enough vertical breathing room so it reads as a summarizing annotation, not another data series.