# SVG Recipe — Shape-Driven Styled Gantt Chart

## Visual mechanism
Render the Gantt as a composed infographic: each date range becomes an independent rounded rectangle mapped onto a timeline grid, then styled with gradients, soft shadows, milestone diamonds, and subtle background atmosphere. The result looks like a premium SaaS roadmap rather than a native chart.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× blurred `<ellipse>` elements for soft ambient color behind the chart
- 1× large rounded `<rect>` for the chart card/container
- 7× `<line>` for vertical month gridlines
- 6× `<line>` for row separators
- 6× `<text>` for month labels
- 5× `<text>` for task/category labels
- 5× gradient-filled rounded `<rect>` elements for task bars
- 5× small highlight `<rect>` elements layered on task bars for glossy depth
- 2× `<path>` diamond shapes for milestones
- 2× dashed `<line>` elements for dependency/phase connectors
- 4× `<linearGradient>` definitions for bar and milestone fills
- 1× `<radialGradient>` for ambient glow
- 2× `<filter>` definitions: one soft drop shadow for bars/card, one blur glow for ambient shapes
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, labels, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealTitle" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2596BE"/>
      <stop offset="100%" stop-color="#41C7B9"/>
    </linearGradient>

    <linearGradient id="gradPurpleBlue" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E0C3FC"/>
      <stop offset="100%" stop-color="#8EC5FC"/>
    </linearGradient>
    <linearGradient id="gradCoralOrange" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF9A9E"/>
      <stop offset="100%" stop-color="#FAD0C4"/>
    </linearGradient>
    <linearGradient id="gradMint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#84FAB0"/>
      <stop offset="100%" stop-color="#8FD3F4"/>
    </linearGradient>
    <linearGradient id="gradIndigo" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#667EEA"/>
      <stop offset="100%" stop-color="#764BA2"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8EC5FC" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#8EC5FC" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <ellipse cx="1080" cy="170" rx="210" ry="130" fill="url(#ambientGlow)" filter="url(#blurGlow)"/>
  <ellipse cx="145" cy="590" rx="240" ry="120" fill="#E0C3FC" opacity="0.22" filter="url(#blurGlow)"/>

  <text x="640" y="66" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="url(#tealTitle)">
    Project schedule and milestones
  </text>
  <text x="640" y="108" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#787878">
    Shape-built Gantt chart with gradient phase bars, milestone diamonds, and editable timeline geometry
  </text>

  <rect x="72" y="164" width="1136" height="476" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="72" y="164" width="1136" height="476" rx="30" fill="none" stroke="#EEF3F7" stroke-width="1.5"/>

  <text x="108" y="214" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A8793">
    WORKSTREAM
  </text>
  <text x="310" y="214" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A8793">
    Q1–Q2 2024
  </text>

  <line x1="292" y1="240" x2="292" y2="584" stroke="#E8EEF3" stroke-width="1.5"/>
  <line x1="310" y1="250" x2="310" y2="584" stroke="#DDE6EE" stroke-width="1"/>
  <line x1="453" y1="250" x2="453" y2="584" stroke="#E9EEF3" stroke-width="1"/>
  <line x1="596" y1="250" x2="596" y2="584" stroke="#E9EEF3" stroke-width="1"/>
  <line x1="740" y1="250" x2="740" y2="584" stroke="#E9EEF3" stroke-width="1"/>
  <line x1="883" y1="250" x2="883" y2="584" stroke="#E9EEF3" stroke-width="1"/>
  <line x1="1026" y1="250" x2="1026" y2="584" stroke="#E9EEF3" stroke-width="1"/>
  <line x1="1170" y1="250" x2="1170" y2="584" stroke="#DDE6EE" stroke-width="1"/>

  <text x="310" y="244" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Jan</text>
  <text x="453" y="244" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Feb</text>
  <text x="596" y="244" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Mar</text>
  <text x="740" y="244" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Apr</text>
  <text x="883" y="244" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">May</text>
  <text x="1026" y="244" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Jun</text>

  <line x1="108" y1="293" x2="1170" y2="293" stroke="#F0F3F6" stroke-width="1"/>
  <line x1="108" y1="351" x2="1170" y2="351" stroke="#F0F3F6" stroke-width="1"/>
  <line x1="108" y1="409" x2="1170" y2="409" stroke="#F0F3F6" stroke-width="1"/>
  <line x1="108" y1="467" x2="1170" y2="467" stroke="#F0F3F6" stroke-width="1"/>
  <line x1="108" y1="525" x2="1170" y2="525" stroke="#F0F3F6" stroke-width="1"/>
  <line x1="108" y1="584" x2="1170" y2="584" stroke="#E8EEF3" stroke-width="1.5"/>

  <text x="108" y="282" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#374151">Concept planning</text>
  <text x="108" y="340" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#374151">UX research</text>
  <text x="108" y="398" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#374151">Prototype build</text>
  <text x="108" y="456" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#374151">Engineering sprint</text>
  <text x="108" y="514" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#374151">Beta launch</text>

  <rect x="310" y="264" width="191" height="28" rx="14" fill="url(#gradPurpleBlue)" filter="url(#softShadow)"/>
  <rect x="377" y="322" width="286" height="28" rx="14" fill="url(#gradCoralOrange)" filter="url(#softShadow)"/>
  <rect x="550" y="380" width="286" height="28" rx="14" fill="url(#gradMint)" filter="url(#softShadow)"/>
  <rect x="641" y="438" width="462" height="28" rx="14" fill="url(#gradIndigo)" filter="url(#softShadow)"/>
  <rect x="911" y="496" width="259" height="28" rx="14" fill="url(#gradPurpleBlue)" filter="url(#softShadow)"/>

  <rect x="322" y="269" width="120" height="5" rx="2.5" fill="#FFFFFF" opacity="0.42"/>
  <rect x="389" y="327" width="170" height="5" rx="2.5" fill="#FFFFFF" opacity="0.36"/>
  <rect x="562" y="385" width="160" height="5" rx="2.5" fill="#FFFFFF" opacity="0.40"/>
  <rect x="653" y="443" width="250" height="5" rx="2.5" fill="#FFFFFF" opacity="0.28"/>
  <rect x="923" y="501" width="150" height="5" rx="2.5" fill="#FFFFFF" opacity="0.42"/>

  <line x1="501" y1="278" x2="550" y2="394" stroke="#B9C6D2" stroke-width="1.5" stroke-dasharray="5 5"/>
  <line x1="836" y1="394" x2="911" y2="510" stroke="#B9C6D2" stroke-width="1.5" stroke-dasharray="5 5"/>

  <path d="M740 358 L756 374 L740 390 L724 374 Z" fill="url(#gradIndigo)" filter="url(#softShadow)"/>
  <path d="M1026 474 L1042 490 L1026 506 L1010 490 Z" fill="url(#gradCoralOrange)" filter="url(#softShadow)"/>

  <text x="764" y="378" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#596877">Design freeze</text>
  <text x="1050" y="494" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#596877">Beta gate</text>

  <rect x="102" y="602" width="12" height="12" rx="6" fill="#8EC5FC"/>
  <text x="122" y="613" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Phase duration</text>
  <path d="M285 596 L297 608 L285 620 L273 608 Z" fill="#667EEA"/>
  <text x="307" y="613" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">Milestone</text>
</svg>
```

## Avoid in this skill
- ❌ Native chart-like assumptions: do not use a single chart object or rely on automatic axes; each bar should be an editable shape.
- ❌ `<marker-end>` arrowheads for dependencies; if arrows are needed, use `<line>` plus a separate triangle/path arrowhead.
- ❌ Applying filters to `<line>` elements; shadows/glows should be applied to bars, cards, milestone paths, or ambient ellipses.
- ❌ Clipping or masking non-image shapes; rounded bars should be real rounded `<rect>` elements, not masked rectangles.
- ❌ Overcrowding rows with tiny text; premium Gantt slides need generous vertical spacing and readable labels.

## Composition notes
- Keep the chart card in the lower 65% of the slide, leaving a calm executive-style title and subtitle zone above.
- Reserve roughly 20% of the chart width for task labels and 75% for the timeline; use a clean vertical divider to separate them.
- Use pale gridlines and neutral labels so the gradient bars become the visual focus.
- Add subtle atmosphere with blurred background ellipses, but keep opacity low so the slide still reads as crisp and data-driven.