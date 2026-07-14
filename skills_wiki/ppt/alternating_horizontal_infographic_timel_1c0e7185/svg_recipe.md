# SVG Recipe — Alternating Horizontal Infographic Timeline

## Visual mechanism
A single horizontal axis runs through the center of the slide, with milestone nodes evenly spaced along it. Each milestone owns a floating content card that alternates above and below the axis, connected back to its node with a thin dashed vertical stem.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× decorative `<path>` blobs for premium depth behind the timeline
- 2× `<linearGradient>` for the background and central track
- 1× `<radialGradient>` for subtle node halo effects
- 2× `<filter>` definitions: soft card shadow and node glow
- 2× `<rect>` for the main horizontal timeline track and highlight
- 5× dashed `<line>` stems connecting nodes to milestone cards
- 5× card `<rect>` containers with rounded corners and shadow
- 5× thin accent `<rect>` bars inside cards
- 15× `<circle>` node parts for outer rings, colored centers, and white inner dots
- Multiple editable `<text>` elements with explicit `width` attributes for dates, titles, descriptions, and slide header

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#F3F6FA"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="trackGrad" x1="150" y1="0" x2="1130" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#D7DEE8"/>
      <stop offset="50%" stop-color="#C7D1DD"/>
      <stop offset="100%" stop-color="#D7DEE8"/>
    </linearGradient>

    <radialGradient id="nodeHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="65%" stop-color="#FFFFFF" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="nodeGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <path d="M-70,170 C70,40 240,30 350,115 C460,200 405,330 230,335 C55,340 -125,295 -70,170 Z"
        fill="#DFF7FF" opacity="0.65"/>
  <path d="M1005,520 C1110,420 1270,425 1345,545 C1420,665 1250,760 1090,710 C950,665 900,620 1005,520 Z"
        fill="#EFE5FF" opacity="0.75"/>

  <text x="86" y="74" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#1F2937">
    Product Roadmap Momentum
  </text>
  <text x="88" y="112" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#6B7280">
    Five strategic milestones showing how the platform matures from launch to global scale.
  </text>

  <rect x="136" y="374" width="1008" height="14" rx="7" fill="url(#trackGrad)"/>
  <rect x="151" y="378" width="978" height="3" rx="1.5" fill="#FFFFFF" opacity="0.65"/>

  <!-- Connector stems -->
  <line x1="190" y1="366" x2="190" y2="330" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="415" y1="394" x2="415" y2="430" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="640" y1="366" x2="640" y2="330" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="865" y1="394" x2="865" y2="430" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="1090" y1="366" x2="1090" y2="330" stroke="#94A3B8" stroke-width="2" stroke-dasharray="5 7"/>

  <!-- Top card 1 -->
  <rect x="82" y="178" width="216" height="152" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="82" y="202" width="6" height="88" rx="3" fill="#00B8D9"/>
  <text x="108" y="220" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#00B8D9">2021</text>
  <text x="108" y="254" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">Market Launch</text>
  <text x="108" y="285" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">
    <tspan x="108" dy="0">Released the first platform</tspan>
    <tspan x="108" dy="17">and secured lighthouse</tspan>
    <tspan x="108" dy="17">enterprise customers.</tspan>
  </text>

  <!-- Bottom card 2 -->
  <rect x="307" y="430" width="216" height="152" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="307" y="454" width="6" height="88" rx="3" fill="#7C3AED"/>
  <text x="333" y="472" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#7C3AED">2022</text>
  <text x="333" y="506" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">Scale Engine</text>
  <text x="333" y="537" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">
    <tspan x="333" dy="0">Expanded sales operations</tspan>
    <tspan x="333" dy="17">and doubled recurring</tspan>
    <tspan x="333" dy="17">revenue year over year.</tspan>
  </text>

  <!-- Top card 3 -->
  <rect x="532" y="178" width="216" height="152" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="532" y="202" width="6" height="88" rx="3" fill="#F97316"/>
  <text x="558" y="220" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#F97316">2023</text>
  <text x="558" y="254" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">AI Foundation</text>
  <text x="558" y="285" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">
    <tspan x="558" dy="0">Integrated predictive</tspan>
    <tspan x="558" dy="17">models into workflows</tspan>
    <tspan x="558" dy="17">for faster decisions.</tspan>
  </text>

  <!-- Bottom card 4 -->
  <rect x="757" y="430" width="216" height="152" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="757" y="454" width="6" height="88" rx="3" fill="#10B981"/>
  <text x="783" y="472" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#10B981">2024</text>
  <text x="783" y="506" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">Global Rollout</text>
  <text x="783" y="537" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">
    <tspan x="783" dy="0">Opened regional hubs</tspan>
    <tspan x="783" dy="17">and localized customer</tspan>
    <tspan x="783" dy="17">success operations.</tspan>
  </text>

  <!-- Top card 5 -->
  <rect x="982" y="178" width="216" height="152" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="982" y="202" width="6" height="88" rx="3" fill="#EC4899"/>
  <text x="1008" y="220" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#EC4899">2025</text>
  <text x="1008" y="254" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#111827">Category Leader</text>
  <text x="1008" y="285" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">
    <tspan x="1008" dy="0">Positioned the platform</tspan>
    <tspan x="1008" dy="17">as the operating layer</tspan>
    <tspan x="1008" dy="17">for modern teams.</tspan>
  </text>

  <!-- Nodes -->
  <circle cx="190" cy="381" r="38" fill="url(#nodeHalo)" filter="url(#nodeGlow)"/>
  <circle cx="190" cy="381" r="23" fill="#FFFFFF"/>
  <circle cx="190" cy="381" r="14" fill="#00B8D9"/>
  <circle cx="190" cy="381" r="5" fill="#FFFFFF"/>

  <circle cx="415" cy="381" r="38" fill="url(#nodeHalo)" filter="url(#nodeGlow)"/>
  <circle cx="415" cy="381" r="23" fill="#FFFFFF"/>
  <circle cx="415" cy="381" r="14" fill="#7C3AED"/>
  <circle cx="415" cy="381" r="5" fill="#FFFFFF"/>

  <circle cx="640" cy="381" r="38" fill="url(#nodeHalo)" filter="url(#nodeGlow)"/>
  <circle cx="640" cy="381" r="23" fill="#FFFFFF"/>
  <circle cx="640" cy="381" r="14" fill="#F97316"/>
  <circle cx="640" cy="381" r="5" fill="#FFFFFF"/>

  <circle cx="865" cy="381" r="38" fill="url(#nodeHalo)" filter="url(#nodeGlow)"/>
  <circle cx="865" cy="381" r="23" fill="#FFFFFF"/>
  <circle cx="865" cy="381" r="14" fill="#10B981"/>
  <circle cx="865" cy="381" r="5" fill="#FFFFFF"/>

  <circle cx="1090" cy="381" r="38" fill="url(#nodeHalo)" filter="url(#nodeGlow)"/>
  <circle cx="1090" cy="381" r="23" fill="#FFFFFF"/>
  <circle cx="1090" cy="381" r="14" fill="#EC4899"/>
  <circle cx="1090" cy="381" r="5" fill="#FFFFFF"/>
</svg>
```

## Avoid in this skill
- ❌ Putting all milestone cards on one side of the axis; it loses the alternating rhythm and creates cramped text.
- ❌ Using `marker-end` arrows on the timeline path; if directional arrows are needed, use a native `<line>` with endpoint decoration built from circles or paths.
- ❌ Applying filters to the dashed connector `<line>` elements; shadows and glows on lines may be dropped.
- ❌ Using clip paths on the card rectangles; clipping is reliable for `<image>` crops, not for non-image shapes.
- ❌ Overloading the slide with more than 6 milestones; the alternating structure becomes too dense and the cards lose hierarchy.

## Composition notes
- Keep the timeline axis near the vertical midpoint, usually around `y=360–400`, leaving enough room for a title above and bottom cards below.
- Use equal horizontal spacing between nodes; uneven spacing should only be used when the timeline needs to communicate elapsed time accurately.
- Alternate card placement consistently: top, bottom, top, bottom, top. This creates a visual cadence and prevents text collisions.
- Use one accent color per milestone, repeated in the date, card accent bar, and node center for fast association.