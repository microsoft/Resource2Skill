# SVG Recipe — Intersecting Venn-Style Feature Cluster

## Visual mechanism
A clean Venn-like center cluster uses three transparent, overlapping circles as a structural metaphor for interconnected features, with bold accent icons sitting above each circle. Detailed explanations are pulled into flanking feature cards so the center remains geometric, symbolic, and uncluttered.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<path>` for the small angled accent mark beside the title
- 1× `<text>` for the page title
- 1× `<ellipse>` with radial gradient for a subtle central halo
- 3× `<circle>` for the intersecting Venn-style outlines
- 3× `<path>` for solid editable feature icons placed over the circles
- 6× `<line>` for faint hub-and-spoke connector guides
- 6× `<rect>` for three feature cards, each with a white body and colored header
- 9× `<text>` for card headers and multi-line body copy
- 1× `<linearGradient>` for premium mustard header fills
- 1× `<radialGradient>` for the soft background glow
- 1× `<filter id="softShadow">` applied to card bodies
- 1× `<filter id="iconGlow">` applied to icon paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mustardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFD34A"/>
      <stop offset="100%" stop-color="#FFC000"/>
    </linearGradient>

    <radialGradient id="centerHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFC000" stop-opacity="0.18"/>
      <stop offset="58%" stop-color="#FFC000" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="iconGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <path d="M62 76 L88 76 L75 122 L49 122 Z" fill="url(#mustardGrad)"/>
  <text x="118" y="98" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#404040">
    Unique Selling Points
  </text>
  <line x1="118" y1="122" x2="385" y2="122" stroke="#E7E7E7" stroke-width="2"/>

  <ellipse cx="640" cy="365" rx="245" ry="220" fill="url(#centerHalo)"/>

  <line x1="533" y1="304" x2="410" y2="292" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="6 8"/>
  <line x1="532" y1="420" x2="410" y2="403" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="6 8"/>
  <line x1="640" y1="277" x2="640" y2="164" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="6 8"/>
  <line x1="741" y1="360" x2="870" y2="250" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="6 8"/>
  <line x1="717" y1="436" x2="870" y2="480" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="6 8"/>
  <line x1="639" y1="485" x2="640" y2="585" stroke="#D6D6D6" stroke-width="1.5" stroke-dasharray="6 8"/>

  <circle cx="640" cy="300" r="112" fill="none" stroke="#C8C8C8" stroke-width="3"/>
  <circle cx="570" cy="420" r="112" fill="none" stroke="#C8C8C8" stroke-width="3"/>
  <circle cx="710" cy="420" r="112" fill="none" stroke="#C8C8C8" stroke-width="3"/>

  <path filter="url(#iconGlow)" d="M640 260 L682 300 L640 340 L598 300 Z" fill="#FFC000"/>
  <path filter="url(#iconGlow)" d="M588 376 L554 432 L582 432 L562 474 L624 408 L591 408 Z" fill="#FFC000"/>
  <path filter="url(#iconGlow)" d="M710 462 C666 430 646 401 665 377 C680 358 703 366 710 384 C717 366 740 358 755 377 C774 401 754 430 710 462 Z" fill="#FFC000"/>

  <rect x="78" y="235" width="340" height="190" rx="16" fill="#FFFFFF" stroke="#EFEFEF" stroke-width="1.5" filter="url(#softShadow)"/>
  <rect x="78" y="235" width="340" height="54" rx="16" fill="url(#mustardGrad)"/>
  <rect x="78" y="271" width="340" height="22" fill="url(#mustardGrad)"/>
  <text x="78" y="270" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="248">Adaptive Experience</tspan>
  </text>
  <text x="108" y="326" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#4A4A4A">
    <tspan x="108" dy="0">Personalized journeys respond</tspan>
    <tspan x="108" dy="26">to each user’s behavior, role,</tspan>
    <tspan x="108" dy="26">and context in real time.</tspan>
  </text>

  <rect x="862" y="170" width="340" height="180" rx="16" fill="#FFFFFF" stroke="#EFEFEF" stroke-width="1.5" filter="url(#softShadow)"/>
  <rect x="862" y="170" width="340" height="54" rx="16" fill="url(#mustardGrad)"/>
  <rect x="862" y="206" width="340" height="22" fill="url(#mustardGrad)"/>
  <text x="862" y="205" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="1032">Integrated Platform</tspan>
  </text>
  <text x="892" y="260" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#4A4A4A">
    <tspan x="892" dy="0">Core workflows, data sources,</tspan>
    <tspan x="892" dy="26">and teams are unified into</tspan>
    <tspan x="892" dy="26">one shared operating layer.</tspan>
  </text>

  <rect x="862" y="420" width="340" height="180" rx="16" fill="#FFFFFF" stroke="#EFEFEF" stroke-width="1.5" filter="url(#softShadow)"/>
  <rect x="862" y="420" width="340" height="54" rx="16" fill="url(#mustardGrad)"/>
  <rect x="862" y="456" width="340" height="22" fill="url(#mustardGrad)"/>
  <text x="862" y="455" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="1032">Measurable Outcomes</tspan>
  </text>
  <text x="892" y="510" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#4A4A4A">
    <tspan x="892" dy="0">Each feature maps directly to</tspan>
    <tspan x="892" dy="26">clear KPIs, making business</tspan>
    <tspan x="892" dy="26">impact visible and trackable.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Filled Venn intersections using masks or boolean clipping; keep circles transparent and let overlap be implied by strokes.
- ❌ Putting text inside the overlapping circle intersections; it clutters the central metaphor and reduces readability.
- ❌ Using `<use>` to repeat circles or icons; duplicate the native shapes directly.
- ❌ Applying filters to connector `<line>` elements; shadows/glows on lines may be dropped.
- ❌ Arrowheads via `marker-end` on paths; if directional connectors are needed, use simple `<line>` elements without markers.

## Composition notes
- Keep the Venn cluster in the middle 30–35% of the slide; it should read as the visual “hub,” not as a dense chart.
- Place detailed copy in flanking cards with generous margins, leaving the circle intersections visually clean.
- Use one strong accent color for headers and icons so the viewer connects the cards to the center instantly.
- Maintain a light background, pale connector lines, and thin gray circle strokes to preserve an executive, minimal tone.