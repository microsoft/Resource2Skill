# SVG Recipe — Animated Geometric Alternating Timeline

## Visual mechanism
A light horizontal spine carries a sequence of technical dial-like nodes, each built from an accent dot, a background-filled hollow circle, and a rotated partial arc. Thin branch lines alternate upward and downward to connect each node to its year and milestone copy, creating rhythm while preventing text collisions.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 1× `<linearGradient>` for a subtle premium background wash
- 1× `<filter id="softShadow">` applied to text cards and node rings for gentle depth
- 1× `<line>` for the main horizontal timeline axis
- 5× `<line>` for alternating vertical branch connectors
- 5× `<path>` for colored outer arc segments around each node
- 5× `<circle>` for background-filled hollow node rings that mask the axis/branch intersections
- 5× `<circle>` for solid inner node dots
- 5× `<rect>` for soft milestone text cards
- 10× `<text>` for year labels and descriptions
- 6× decorative `<path>`/`<circle>` elements for faint geometric background accents and small endpoint ticks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.55" stop-color="#f5f5f5"/>
      <stop offset="1" stop-color="#eceff3"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M58 140 L176 76 L292 142 L174 207 Z" fill="#ffffff" opacity="0.45"/>
  <path d="M1005 94 L1194 94 L1124 188 Z" fill="#dfe8f1" opacity="0.38"/>
  <circle cx="1135" cy="610" r="88" fill="#ffffff" opacity="0.42"/>
  <circle cx="114" cy="570" r="58" fill="#dfe8f1" opacity="0.34"/>

  <text x="0" y="74" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31"
        font-weight="600" fill="#34383f">T I M E L I N E&nbsp;&nbsp; S L I D E</text>
  <text x="0" y="106" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        fill="#8a929b">alternating milestones with geometric focus nodes</text>

  <line x1="88" y1="360" x2="1192" y2="360" stroke="#c9cdd2" stroke-width="2"/>

  <line x1="150" y1="360" x2="150" y2="238" stroke="#c9cdd2" stroke-width="2"/>
  <line x1="395" y1="360" x2="395" y2="486" stroke="#c9cdd2" stroke-width="2"/>
  <line x1="640" y1="360" x2="640" y2="238" stroke="#c9cdd2" stroke-width="2"/>
  <line x1="885" y1="360" x2="885" y2="486" stroke="#c9cdd2" stroke-width="2"/>
  <line x1="1130" y1="360" x2="1130" y2="238" stroke="#c9cdd2" stroke-width="2"/>

  <path d="M132 238 L168 238" stroke="#3498db" stroke-width="3" stroke-linecap="round"/>
  <path d="M377 486 L413 486" stroke="#e67e22" stroke-width="3" stroke-linecap="round"/>
  <path d="M622 238 L658 238" stroke="#e74c3c" stroke-width="3" stroke-linecap="round"/>
  <path d="M867 486 L903 486" stroke="#2980b9" stroke-width="3" stroke-linecap="round"/>
  <path d="M1112 238 L1148 238" stroke="#27ae60" stroke-width="3" stroke-linecap="round"/>

  <rect x="64" y="150" width="172" height="78" rx="18" fill="#ffffff" opacity="0.82" filter="url(#softShadow)"/>
  <text x="64" y="188" width="172" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#3498db">2019</text>
  <text x="82" y="211" width="136" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8b9299">Market validation and first customer pilots</text>

  <rect x="309" y="496" width="172" height="78" rx="18" fill="#ffffff" opacity="0.82" filter="url(#softShadow)"/>
  <text x="309" y="534" width="172" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#e67e22">2020</text>
  <text x="327" y="557" width="136" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8b9299">Platform buildout and operational scale-up</text>

  <rect x="554" y="150" width="172" height="78" rx="18" fill="#ffffff" opacity="0.82" filter="url(#softShadow)"/>
  <text x="554" y="188" width="172" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#e74c3c">2021</text>
  <text x="572" y="211" width="136" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8b9299">Global launch with integrated partner ecosystem</text>

  <rect x="799" y="496" width="172" height="78" rx="18" fill="#ffffff" opacity="0.82" filter="url(#softShadow)"/>
  <text x="799" y="534" width="172" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#2980b9">2022</text>
  <text x="817" y="557" width="136" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8b9299">Automation layer released across all core workflows</text>

  <rect x="1044" y="150" width="172" height="78" rx="18" fill="#ffffff" opacity="0.82" filter="url(#softShadow)"/>
  <text x="1044" y="188" width="172" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#27ae60">2023</text>
  <text x="1062" y="211" width="136" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8b9299">Expansion milestone and enterprise adoption</text>

  <path d="M150 321 A39 39 0 1 1 121 386" fill="none" stroke="#3498db" stroke-width="4" stroke-linecap="round"/>
  <circle cx="150" cy="360" r="25" fill="#f5f5f5" stroke="#3498db" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="150" cy="360" r="9" fill="#3498db"/>

  <path d="M423 333 A39 39 0 1 1 367 387" fill="none" stroke="#e67e22" stroke-width="4" stroke-linecap="round"/>
  <circle cx="395" cy="360" r="25" fill="#f5f5f5" stroke="#e67e22" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="395" cy="360" r="9" fill="#e67e22"/>

  <path d="M640 399 A39 39 0 1 1 671 335" fill="none" stroke="#e74c3c" stroke-width="4" stroke-linecap="round"/>
  <circle cx="640" cy="360" r="25" fill="#f5f5f5" stroke="#e74c3c" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="640" cy="360" r="9" fill="#e74c3c"/>

  <path d="M857 386 A39 39 0 1 1 913 333" fill="none" stroke="#2980b9" stroke-width="4" stroke-linecap="round"/>
  <circle cx="885" cy="360" r="25" fill="#f5f5f5" stroke="#2980b9" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="885" cy="360" r="9" fill="#2980b9"/>

  <path d="M1130 321 A39 39 0 1 1 1100 386" fill="none" stroke="#27ae60" stroke-width="4" stroke-linecap="round"/>
  <circle cx="1130" cy="360" r="25" fill="#f5f5f5" stroke="#27ae60" stroke-width="4" filter="url(#softShadow)"/>
  <circle cx="1130" cy="360" r="9" fill="#27ae60"/>
</svg>
```

## Avoid in this skill
- ❌ SVG animation tags such as `<animate>` or `<animateTransform>`; represent the “animated” look with staged geometry, then add PowerPoint animations manually if needed.
- ❌ `marker-end` arrowheads on paths for the timeline axis; if arrows are required, draw them with separate `<line>` and `<path>` geometry.
- ❌ Masking or clipping non-image elements to cut the axis behind nodes; instead, use the background-filled hollow circle on top of the line.
- ❌ Applying filters to `<line>` connectors; PowerPoint translation drops line filters, so keep connector lines clean and flat.
- ❌ Overcrowding the centerline with long labels; the node ring should remain visually pristine.

## Composition notes
- Keep the axis near the vertical midpoint, with 120–135 px branch height so top and bottom text blocks have equal breathing room.
- Draw connectors first, then node arcs/rings/dots last; the background-filled ring is the masking layer that cleans up line intersections.
- Use one accent color per milestone and repeat it consistently across arc, ring stroke, dot, year, and branch cap.
- Leave generous negative space above the title and around the outermost milestones; the technique looks premium when the centerline feels airy rather than packed.