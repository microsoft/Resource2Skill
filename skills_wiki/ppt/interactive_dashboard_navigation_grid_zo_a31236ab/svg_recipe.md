# SVG Recipe — Interactive Dashboard Navigation Grid (Zoom Menu Style)

## Visual mechanism
A presentation “hub” slide uses a premium two-zone layout: a calm agenda panel on the left and a 2×2 grid of clickable slide-preview cards on the right. Each card looks like a mini section cover, with a clipped 16:9 photo thumbnail, soft elevation, a color-coded title block, and an invisible hit-area rectangle that can receive a PowerPoint hyperlink.

## SVG primitives needed
- 1× full-canvas `<rect>` for the slate executive background.
- 2× decorative `<path>` strokes for subtle app-like navigation motion in the background.
- 4× `<rect>` card bases with rounded corners and shadow filter for elevated thumbnail tiles.
- 4× `<image>` elements clipped by rounded `<clipPath>` rectangles for 16:9 section previews.
- 4× brand-colored `<rect>` title pills overlapping the bottom of the thumbnails.
- 4× `<circle>` number badges to reinforce menu ordering.
- 4× nearly transparent `<rect>` hit targets placed above the cards for later PowerPoint hyperlink assignment.
- 1× `<linearGradient>` for the background and 1× `<radialGradient>` for ambient glow.
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for editable card depth.
- Multiple `<text>` elements with explicit `width` attributes for title, agenda list, card labels, and microcopy.
- 1× `<line>` divider for the agenda column.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5F6B77"/>
      <stop offset="55%" stop-color="#6A737D"/>
      <stop offset="100%" stop-color="#4F5964"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="72%" cy="42%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="58%" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipOverview">
      <rect x="500" y="112" width="330" height="186" rx="18"/>
    </clipPath>
    <clipPath id="clipStrategy">
      <rect x="875" y="112" width="330" height="186" rx="18"/>
    </clipPath>
    <clipPath id="clipOperations">
      <rect x="500" y="392" width="330" height="186" rx="18"/>
    </clipPath>
    <clipPath id="clipMarketing">
      <rect x="875" y="392" width="330" height="186" rx="18"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#ambientGlow)"/>

  <path d="M430 86 C520 44, 626 60, 700 122 S875 225, 1000 156 S1185 92, 1254 158"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="2" stroke-dasharray="8 12"/>
  <path d="M445 650 C565 596, 660 630, 765 576 S966 474, 1216 520"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="2" stroke-dasharray="3 11"/>
  <circle cx="1178" cy="84" r="58" fill="#FFFFFF" opacity="0.05"/>
  <circle cx="468" cy="620" r="92" fill="#FFFFFF" opacity="0.04"/>

  <text x="80" y="128" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600"
        letter-spacing="4" fill="#DDE4EA" opacity="0.78">ZOOM MENU</text>
  <text x="80" y="184" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="800"
        fill="#FFFFFF">MEETING<tspan x="80" dy="46">AGENDA</tspan></text>
  <line x1="80" y1="254" x2="350" y2="254" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>

  <text x="80" y="310" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    <tspan x="80" dy="0" fill="#E59E3F">01</tspan><tspan dx="18" fill="#FFFFFF">Business Overview</tspan>
    <tspan x="80" dy="44" fill="#48A67B">02</tspan><tspan dx="18" fill="#FFFFFF">Strategy</tspan>
    <tspan x="80" dy="44" fill="#3D5A80">03</tspan><tspan dx="18" fill="#FFFFFF">Operations</tspan>
    <tspan x="80" dy="44" fill="#C25953">04</tspan><tspan dx="18" fill="#FFFFFF">Marketing</tspan>
  </text>

  <text x="80" y="552" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" line-height="1.4"
        fill="#E8EDF1" opacity="0.82">
    Select a topic card to jump directly into that section. Return to this hub between modules to preserve the audience’s mental map.
  </text>

  <rect x="500" y="112" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&amp;fit=crop&amp;w=900&amp;q=80"
         x="500" y="112" width="330" height="186" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipOverview)"/>
  <rect x="518" y="236" width="242" height="46" rx="10" fill="#E59E3F"/>
  <circle cx="790" cy="135" r="22" fill="#E59E3F"/>
  <text x="782" y="143" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">1</text>
  <text x="536" y="265" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">BUSINESS OVERVIEW</text>

  <rect x="875" y="112" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1529699211952-734e80c4d42b?auto=format&amp;fit=crop&amp;w=900&amp;q=80"
         x="875" y="112" width="330" height="186" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipStrategy)"/>
  <rect x="893" y="236" width="168" height="46" rx="10" fill="#48A67B"/>
  <circle cx="1165" cy="135" r="22" fill="#48A67B"/>
  <text x="1157" y="143" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">2</text>
  <text x="911" y="265" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">STRATEGY</text>

  <rect x="500" y="392" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&amp;fit=crop&amp;w=900&amp;q=80"
         x="500" y="392" width="330" height="186" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipOperations)"/>
  <rect x="518" y="516" width="190" height="46" rx="10" fill="#3D5A80"/>
  <circle cx="790" cy="415" r="22" fill="#3D5A80"/>
  <text x="782" y="423" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">3</text>
  <text x="536" y="545" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">OPERATIONS</text>

  <rect x="875" y="392" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&amp;fit=crop&amp;w=900&amp;q=80"
         x="875" y="392" width="330" height="186" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMarketing)"/>
  <rect x="893" y="516" width="184" height="46" rx="10" fill="#C25953"/>
  <circle cx="1165" cy="415" r="22" fill="#C25953"/>
  <text x="1157" y="423" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">4</text>
  <text x="911" y="545" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">MARKETING</text>

  <rect id="link-hit-overview" x="500" y="112" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.01"/>
  <rect id="link-hit-strategy" x="875" y="112" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.01"/>
  <rect id="link-hit-operations" x="500" y="392" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.01"/>
  <rect id="link-hit-marketing" x="875" y="392" width="330" height="186" rx="18" fill="#FFFFFF" opacity="0.01"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<a href="...">` links as the interaction mechanism; instead, import the SVG as editable shapes and assign PowerPoint hyperlinks to the transparent hit-target rectangles.
- ❌ Do not use `<use>` or `<symbol>` to duplicate cards; repeated native shapes are safer and remain editable.
- ❌ Do not apply `clip-path` to the whole card group or to colored rectangles; only clip the `<image>` thumbnails.
- ❌ Do not rely on PowerPoint’s proprietary Section Zoom XML inside SVG. Recreate the visual zoom menu and attach slide hyperlinks after import.
- ❌ Do not use filter effects on `<line>` elements; keep shadows on card rectangles only.

## Composition notes
- Reserve the left 32–35% of the canvas for orientation: title, divider, agenda list, and presenter guidance copy.
- Keep the right 65% for the 2×2 thumbnail grid; each card should remain a true 16:9 preview so it feels like a slide miniature.
- Use one saturated accent color per section and repeat it in both the agenda list and the card title block for fast scanning.
- Place transparent hit rectangles as the topmost objects over each card so the entire thumbnail behaves like a clean PowerPoint navigation button.