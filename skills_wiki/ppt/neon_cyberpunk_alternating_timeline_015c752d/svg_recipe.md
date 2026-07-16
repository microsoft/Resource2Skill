# SVG Recipe — Neon Cyberpunk Alternating Timeline

## Visual mechanism
A dark, high-contrast horizontal timeline is energized with alternating vertical branches, glowing neon node cores, and crisp concentric rings. Each milestone uses a distinct cyberpunk accent color, tying year, branch, node, and caption rule into one visual unit.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 2× `<ellipse>` for subtle atmospheric neon haze behind the timeline
- 1× `<rect>` for the central horizontal axis
- 10× thin `<rect>` for vertical milestone branches and caption divider rules
- 5× solid `<circle>` for glowing node cores on the central axis
- 10× stroked `<circle>` for concentric hollow node rings
- 5× small `<circle>` for glowing branch endpoint dots
- 6× `<text>` for title and year labels
- 5× multiline `<text>` blocks with nested `<tspan>` for milestone captions
- 6× `<filter>` definitions for white title glow and neon color glows
- 1× `<linearGradient>` for the charcoal background
- 2× `<radialGradient>` definitions for ambient cyberpunk haze

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#282828"/>
      <stop offset="55%" stop-color="#202123"/>
      <stop offset="100%" stop-color="#17181B"/>
    </linearGradient>

    <radialGradient id="cyanHaze" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00C7BE" stop-opacity="0.18"/>
      <stop offset="70%" stop-color="#00C7BE" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#00C7BE" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="violetHaze" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5856D6" stop-opacity="0.16"/>
      <stop offset="75%" stop-color="#5856D6" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#5856D6" stop-opacity="0"/>
    </radialGradient>

    <filter id="whiteGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="redGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="yellowGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="cyanGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="greenGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="goldGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="380" cy="390" rx="360" ry="210" fill="url(#cyanHaze)" opacity="0.45"/>
  <ellipse cx="910" cy="335" rx="330" ry="190" fill="url(#violetHaze)" opacity="0.38"/>

  <text x="640" y="78" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="800" letter-spacing="12" fill="#FFFFFF" filter="url(#whiteGlow)">TIMELINE SLIDE</text>

  <circle cx="570" cy="118" r="9" fill="#FF2D20" filter="url(#redGlow)"/>
  <circle cx="605" cy="118" r="9" fill="#FFF000" filter="url(#yellowGlow)"/>
  <circle cx="640" cy="118" r="9" fill="#40E0E0" filter="url(#cyanGlow)"/>
  <circle cx="675" cy="118" r="9" fill="#34C759" filter="url(#greenGlow)"/>
  <circle cx="710" cy="118" r="9" fill="#FFC400" filter="url(#goldGlow)"/>

  <rect x="0" y="414" width="1280" height="3" rx="1.5" fill="#F2F2F2" opacity="0.92"/>

  <!-- 2019: lower red branch -->
  <rect x="235" y="414" width="3" height="164" rx="1.5" fill="#FF3B30" filter="url(#redGlow)"/>
  <circle cx="236" cy="416" r="23" fill="none" stroke="#FF3B30" stroke-width="3" filter="url(#redGlow)"/>
  <circle cx="236" cy="416" r="15" fill="none" stroke="#FF3B30" stroke-width="2"/>
  <circle cx="236" cy="416" r="9" fill="#FF3B30" filter="url(#redGlow)"/>
  <circle cx="236" cy="578" r="7" fill="#FF3B30" filter="url(#redGlow)"/>
  <text x="236" y="362" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FF3B30">2019</text>
  <text x="101" y="632" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#FFFFFF">
    <tspan x="101" dy="0">Prototype launch with a</tspan>
    <tspan x="101" dy="22">secure cloud foundation.</tspan>
  </text>
  <rect x="101" y="671" width="272" height="3" rx="1.5" fill="#FF3B30" filter="url(#redGlow)"/>

  <!-- 2020: upper yellow branch -->
  <rect x="437" y="253" width="3" height="163" rx="1.5" fill="#FFF000" filter="url(#yellowGlow)"/>
  <circle cx="439" cy="416" r="23" fill="none" stroke="#FFF000" stroke-width="3" filter="url(#yellowGlow)"/>
  <circle cx="439" cy="416" r="15" fill="none" stroke="#FFF000" stroke-width="2"/>
  <circle cx="439" cy="416" r="9" fill="#FFF000" filter="url(#yellowGlow)"/>
  <circle cx="439" cy="252" r="7" fill="#FFF000" filter="url(#yellowGlow)"/>
  <text x="439" y="497" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFF000">2020</text>
  <rect x="303" y="162" width="272" height="3" rx="1.5" fill="#FFF000" filter="url(#yellowGlow)"/>
  <text x="303" y="196" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#FFFFFF">
    <tspan x="303" dy="0">AI workflow automation</tspan>
    <tspan x="303" dy="22">moved from beta to scale.</tspan>
  </text>

  <!-- 2021: lower cyan branch -->
  <rect x="638" y="414" width="3" height="164" rx="1.5" fill="#40E0E0" filter="url(#cyanGlow)"/>
  <circle cx="640" cy="416" r="23" fill="none" stroke="#40E0E0" stroke-width="3" filter="url(#cyanGlow)"/>
  <circle cx="640" cy="416" r="15" fill="none" stroke="#40E0E0" stroke-width="2"/>
  <circle cx="640" cy="416" r="9" fill="#40E0E0" filter="url(#cyanGlow)"/>
  <circle cx="640" cy="578" r="7" fill="#40E0E0" filter="url(#cyanGlow)"/>
  <text x="640" y="362" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#40E0E0">2021</text>
  <text x="505" y="632" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#FFFFFF">
    <tspan x="505" dy="0">Unified data layer enabled</tspan>
    <tspan x="505" dy="22">real-time product analytics.</tspan>
  </text>
  <rect x="505" y="671" width="272" height="3" rx="1.5" fill="#40E0E0" filter="url(#cyanGlow)"/>

  <!-- 2022: upper green branch -->
  <rect x="840" y="253" width="3" height="163" rx="1.5" fill="#34C759" filter="url(#greenGlow)"/>
  <circle cx="842" cy="416" r="23" fill="none" stroke="#34C759" stroke-width="3" filter="url(#greenGlow)"/>
  <circle cx="842" cy="416" r="15" fill="none" stroke="#34C759" stroke-width="2"/>
  <circle cx="842" cy="416" r="9" fill="#34C759" filter="url(#greenGlow)"/>
  <circle cx="842" cy="252" r="7" fill="#34C759" filter="url(#greenGlow)"/>
  <text x="842" y="497" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#34C759">2022</text>
  <rect x="710" y="162" width="272" height="3" rx="1.5" fill="#34C759" filter="url(#greenGlow)"/>
  <text x="710" y="196" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#FFFFFF">
    <tspan x="710" dy="0">Enterprise platform released</tspan>
    <tspan x="710" dy="22">with global compliance built in.</tspan>
  </text>

  <!-- 2023: lower gold branch -->
  <rect x="1041" y="414" width="3" height="164" rx="1.5" fill="#FFC400" filter="url(#goldGlow)"/>
  <circle cx="1043" cy="416" r="23" fill="none" stroke="#FFC400" stroke-width="3" filter="url(#goldGlow)"/>
  <circle cx="1043" cy="416" r="15" fill="none" stroke="#FFC400" stroke-width="2"/>
  <circle cx="1043" cy="416" r="9" fill="#FFC400" filter="url(#goldGlow)"/>
  <circle cx="1043" cy="578" r="7" fill="#FFC400" filter="url(#goldGlow)"/>
  <text x="1043" y="362" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFC400">2023</text>
  <text x="910" y="632" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#FFFFFF">
    <tspan x="910" dy="0">Next-generation release</tspan>
    <tspan x="910" dy="22">prepared for public launch.</tspan>
  </text>
  <rect x="910" y="671" width="272" height="3" rx="1.5" fill="#FFC400" filter="url(#goldGlow)"/>
</svg>
```

## Avoid in this skill
- ❌ Applying glow filters to `<line>` elements; use thin `<rect>` elements for neon branches and rules instead.
- ❌ Using `<marker>` arrowheads on the timeline axis; this style is node-driven, not arrow-driven.
- ❌ Putting filters on parent `<g>` groups; apply the glow filter directly to each editable circle, rect, or text object.
- ❌ Using masks for glow halos; blurred filtered circles translate more reliably.
- ❌ Overcrowding with more than 5–7 milestones; the alternating branch rhythm needs breathing room.

## Composition notes
- Keep the central axis exactly around the vertical midpoint; reserve the top 20% for the title and decorative neon dots.
- Alternate captions above and below the axis so each milestone owns a clear vertical lane.
- Use one accent color per milestone across year, node, branch, endpoint dot, and caption rule for instant association.
- Leave wide negative space between caption blocks; the neon glow reads as premium only when the dark field remains uncluttered.