# SVG Recipe — Tabbed Content Panel Infographic

## Visual mechanism
A large floating white rounded panel is divided into a left-side content list and a right-side vertical stack of saturated index tabs. Each row title, icon, and tab share the same color, creating a file-folder/navigation metaphor that turns 5–7 related points into a scannable executive infographic.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark neutral background
- 2× translucent decorative `<circle>` elements for premium depth behind the panel
- 1× `<rect>` for the main rounded white content panel
- 1× `<filter id="panelShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for the floating-card shadow
- 1× `<linearGradient>` for subtle background depth
- 5× `<path>` for the right-side colored index tabs with rounded outer corners
- 5× `<line>` for horizontal row separators in the content area
- 5× `<circle>` icon badges, color-matched to the tabs
- 5× small icon `<path>` drawings inside the badges
- 16× `<text>` blocks for title, subtitle, row labels, body copy, and tab labels; every text element includes an explicit `width`
- Optional translucent `<path>` accent on the panel for a soft folder-like overlay

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#777777"/>
      <stop offset="55%" stop-color="#858585"/>
      <stop offset="100%" stop-color="#666666"/>
    </linearGradient>

    <filter id="panelShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1090" cy="120" r="210" fill="#ffffff" opacity="0.07"/>
  <circle cx="120" cy="650" r="260" fill="#000000" opacity="0.08"/>

  <rect x="76" y="68" width="1128" height="584" rx="34" fill="#FFFFFF" filter="url(#panelShadow)"/>

  <path d="M96 99 C260 72 395 86 526 120 C438 143 324 154 182 142 C138 138 108 124 96 99Z"
        fill="#F3F5F8" opacity="0.9"/>

  <text x="126" y="134" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="800" letter-spacing="2" fill="#3F3F3F">INFOGRAPHIC</text>
  <text x="130" y="170" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#777777">Five connected priorities organized as a tabbed content panel</text>

  <path d="M895 134 H1172 Q1206 134 1206 168 V206 Q1206 240 1172 240 H895 Z" fill="#FFC000"/>
  <path d="M895 242 H1172 Q1206 242 1206 276 V314 Q1206 348 1172 348 H895 Z" fill="#92D050"/>
  <path d="M895 350 H1172 Q1206 350 1206 384 V422 Q1206 456 1172 456 H895 Z" fill="#00B0F0"/>
  <path d="M895 458 H1172 Q1206 458 1206 492 V530 Q1206 564 1172 564 H895 Z" fill="#7030A0"/>
  <path d="M895 566 H1172 Q1206 566 1206 600 V616 Q1206 650 1172 650 H895 Z" fill="#F47026"/>

  <text x="945" y="178" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#FFFFFF">OPTION 01</text>
  <text x="945" y="286" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#FFFFFF">OPTION 02</text>
  <text x="945" y="394" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#FFFFFF">OPTION 03</text>
  <text x="945" y="502" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#FFFFFF">OPTION 04</text>
  <text x="945" y="610" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#FFFFFF">OPTION 05</text>

  <line x1="128" y1="236" x2="866" y2="236" stroke="#E4E7EB" stroke-width="2"/>
  <line x1="128" y1="344" x2="866" y2="344" stroke="#E4E7EB" stroke-width="2"/>
  <line x1="128" y1="452" x2="866" y2="452" stroke="#E4E7EB" stroke-width="2"/>
  <line x1="128" y1="560" x2="866" y2="560" stroke="#E4E7EB" stroke-width="2"/>
  <line x1="128" y1="632" x2="866" y2="632" stroke="#E4E7EB" stroke-width="2"/>

  <circle cx="164" cy="204" r="28" fill="#FFF4CC"/>
  <path d="M152 204 L161 213 L178 191" fill="none" stroke="#FFC000" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="214" y="197" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#D8A100">Strategic Focus</text>
  <text x="214" y="226" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#595959">Clarify the highest-value initiatives and align stakeholders around the main objective.</text>

  <circle cx="164" cy="312" r="28" fill="#EEF9E5"/>
  <path d="M152 315 C157 297 176 296 181 312 C172 309 164 318 164 329 C159 321 153 318 152 315Z" fill="#92D050"/>
  <text x="214" y="305" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#6EAA39">Growth Engine</text>
  <text x="214" y="334" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#595959">Identify scalable channels, repeatable motions, and measurable expansion opportunities.</text>

  <circle cx="164" cy="420" r="28" fill="#E1F7FE"/>
  <path d="M150 421 H178 M164 407 V435 M154 411 L174 431 M174 411 L154 431" stroke="#00B0F0" stroke-width="5" stroke-linecap="round"/>
  <text x="214" y="413" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#0098D4">Digital Enablement</text>
  <text x="214" y="442" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#595959">Connect platforms, analytics, and automation into a cohesive operating capability.</text>

  <circle cx="164" cy="528" r="28" fill="#EEE6F6"/>
  <path d="M150 528 C150 518 158 510 168 510 C178 510 184 517 184 526 C184 541 166 546 154 536"
        fill="none" stroke="#7030A0" stroke-width="5" stroke-linecap="round"/>
  <text x="214" y="521" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#7030A0">Customer Journey</text>
  <text x="214" y="550" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#595959">Map touchpoints, remove friction, and design experiences that increase loyalty.</text>

  <circle cx="164" cy="612" r="28" fill="#FDE9DF"/>
  <path d="M151 617 L164 592 L177 617 Z M158 617 H170 V626 H158 Z" fill="#F47026"/>
  <text x="214" y="605" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" fill="#F47026">Execution Roadmap</text>
  <text x="214" y="634" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#595959">Translate priorities into owners, milestones, decision gates, and measurable outcomes.</text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain table grid; the technique depends on a floating folder-panel metaphor, not spreadsheet structure
- ❌ Applying `clip-path` to tab shapes or panel shapes; clipping is only reliable on `<image>` elements
- ❌ Using `<use>` to duplicate icon artwork; duplicate or redraw each icon path directly
- ❌ Putting a shadow filter on separator `<line>` elements; filters on lines may be dropped
- ❌ Overcrowding the right tabs with long copy; tabs should remain short navigational labels

## Composition notes
- Keep the white panel large, centered, and dominant: about 85–90% slide width and 75–85% slide height.
- Reserve roughly 70% of the panel for detailed content and 30% for the colored tab index.
- Use strong color repetition: tab color = row title color = icon accent color.
- Maintain generous horizontal breathing room between icons, row titles, body text, and the tab column; the premium feel comes from spacing and alignment.