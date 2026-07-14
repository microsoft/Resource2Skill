# SVG Recipe — Centered Metric Card

## Visual mechanism
A single oversized metric sits inside a centered, premium card with a warm gradient border, soft shadow, and subtle ambient glow. The value and unit are separated typographically so the number dominates while the unit reads as a supporting label.

## SVG primitives needed
- 3× `<linearGradient>` for the slide background, card surface, and warm border/accent treatments
- 2× `<radialGradient>` for ambient glow behind the metric card
- 2× `<filter>` using blur/offset for the card shadow and soft accent glow
- 4× `<rect>` for the full-slide background, main card body, inset highlight border, and small status pill
- 2× `<circle>` for small status/accent dots
- 7× `<path>` for abstract background blobs, decorative card swooshes, corner brackets, and a small sparkline
- 1× `<line>` for a quiet divider beneath the metric
- 6× `<text>` elements for headline, eyebrow label, metric value, unit, explanatory caption, and source note
- Nested `<tspan>` inside the caption for inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#171A24"/>
      <stop offset="55%" stop-color="#24202A"/>
      <stop offset="100%" stop-color="#3B241C"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="400" y1="160" x2="880" y2="570">
      <stop offset="0%" stop-color="#FFF9F1"/>
      <stop offset="46%" stop-color="#FFF4E5"/>
      <stop offset="100%" stop-color="#FFE8CA"/>
    </linearGradient>

    <linearGradient id="borderGrad" x1="360" y1="130" x2="920" y2="590">
      <stop offset="0%" stop-color="#FFE4A3"/>
      <stop offset="42%" stop-color="#FF9E43"/>
      <stop offset="100%" stop-color="#D75E2A"/>
    </linearGradient>

    <linearGradient id="metricGrad" x1="420" y1="300" x2="860" y2="420">
      <stop offset="0%" stop-color="#231B17"/>
      <stop offset="55%" stop-color="#5D2B18"/>
      <stop offset="100%" stop-color="#B45A22"/>
    </linearGradient>

    <radialGradient id="haloA" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFB45F" stop-opacity="0.48"/>
      <stop offset="52%" stop-color="#FF8F3D" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FF8F3D" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="haloB" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F7D58A" stop-opacity="0.38"/>
      <stop offset="70%" stop-color="#F7D58A" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#F7D58A" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="26"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80,190 C120,60 240,115 330,25 C420,-65 570,-25 610,85 C650,195 520,260 365,255 C210,250 80,350 -80,300 Z"
        fill="url(#haloB)" opacity="0.58"/>
  <path d="M960,40 C1095,5 1245,80 1328,198 L1328,420 C1220,350 1085,386 1015,300 C945,214 850,70 960,40 Z"
        fill="url(#haloA)" opacity="0.52"/>
  <circle cx="640" cy="374" r="250" fill="url(#haloA)" opacity="0.42" filter="url(#softGlow)"/>
  <circle cx="410" cy="520" r="7" fill="#FFC26F" opacity="0.9"/>

  <rect x="350" y="136" width="580" height="438" rx="42"
        fill="url(#borderGrad)" opacity="0.95" filter="url(#cardShadow)"/>
  <rect x="356" y="142" width="568" height="426" rx="37"
        fill="url(#cardGrad)"/>
  <rect x="378" y="164" width="524" height="382" rx="28"
        fill="none" stroke="#FFFFFF" stroke-width="2.4" opacity="0.68"/>

  <path d="M396,212 C500,170 602,190 704,164 C778,145 844,158 902,184"
        fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.34"/>
  <path d="M394,504 C476,466 570,485 656,462 C760,434 825,455 888,510"
        fill="none" stroke="#F29B4B" stroke-width="10" stroke-linecap="round" opacity="0.20"/>

  <path d="M397,203 L397,181 L421,181"
        fill="none" stroke="#A85222" stroke-width="3" stroke-linecap="round" opacity="0.50"/>
  <path d="M883,181 L907,181 L907,203"
        fill="none" stroke="#A85222" stroke-width="3" stroke-linecap="round" opacity="0.50"/>
  <path d="M397,507 L397,531 L421,531"
        fill="none" stroke="#A85222" stroke-width="3" stroke-linecap="round" opacity="0.38"/>
  <path d="M883,531 L907,531 L907,507"
        fill="none" stroke="#A85222" stroke-width="3" stroke-linecap="round" opacity="0.38"/>

  <text x="160" y="86" width="960" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700"
        fill="#FFF4E8" opacity="0.96">FY26 Operating Momentum</text>

  <rect x="535" y="214" width="210" height="36" rx="18" fill="#2A211D" opacity="0.92"/>
  <circle cx="561" cy="232" r="5.5" fill="#FFB45F"/>
  <text x="583" y="238" width="142"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700"
        letter-spacing="1.5" fill="#FFE5BF">NET RETENTION</text>

  <text x="640" y="386" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="116" font-weight="800"
        fill="url(#metricGrad)">124</text>
  <text x="790" y="377" width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="750"
        fill="#8A3E1F">%</text>

  <line x1="480" y1="420" x2="800" y2="420" stroke="#B76533" stroke-width="1.6" opacity="0.32"/>

  <text x="440" y="462" width="400" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="500"
        fill="#5C4235">
    <tspan fill="#8A3E1F" font-weight="750">+18 pts</tspan><tspan> vs. prior year cohort baseline</tspan>
  </text>

  <path d="M535,500 L570,486 L604,493 L638,470 L672,478 L708,447 L745,456"
        fill="none" stroke="#C9692F" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="640" y="619" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="500"
        fill="#FFE7D0" opacity="0.66">Trailing twelve months • Enterprise segment • Constant currency</text>
</svg>
```

## Avoid in this skill
- ❌ Don’t create a busy dashboard grid; the power of this shell comes from one metric owning the slide.
- ❌ Don’t use multiple competing chart marks around the number; decorative paths should support the focal card, not explain a second story.
- ❌ Don’t rely on `filter` effects for `<line>` elements; apply shadows/glows to card rectangles, paths, or circles instead.
- ❌ Don’t put the value and unit in one unstyled text run if the unit should feel secondary; separate text elements give stronger typographic control.
- ❌ Don’t use masks or clipped non-image shapes for the card treatment; use editable rounded rectangles, gradients, paths, and opacity.

## Composition notes
- Keep the card centered and large: roughly 45% of slide width and 60% of slide height, with generous negative space around it.
- The headline should sit above the card, not inside the metric zone, so the number remains the visual anchor.
- Use warm accent color sparingly on the border, pill, unit, and tiny sparkline to create rhythm without distracting from the value.
- Preserve a clear hierarchy: eyebrow label → oversized metric → small contextual caption → quiet source note.