# SVG Recipe — Morph-Driven Concept Splitting (Divergent Deconstruction)

## Visual mechanism
A single composite idea appears to deconstruct into multiple constituent labels that fan outward from a shared origin, with the final frame preserving the split as bold, separated text slabs. For a PowerPoint-native Morph build, create two slides: first with the slabs stacked at the origin, second with the same shapes spread into their final positions.

## SVG primitives needed
- 1× `<rect>` for the clean white background
- 1× `<path>` for the stylized PowerPoint red door/block silhouette
- 1× `<rect>` with stroke only for the PowerPoint slide-outline icon
- 3× `<path>` / `<circle>` combinations for the pie-chart motif inside the PowerPoint icon
- 3× `<rect>` for the yellow split-text bars
- 3× `<text>` elements for the red slab typography labels
- 3× `<line>` for subtle divergent guide trails from the origin toward each split bar
- 1× `<filter id="softShadow">` applied to yellow slabs for editable depth
- 1× `<linearGradient id="pptRed">` for the PowerPoint icon fill
- 1× `<linearGradient id="goldBar">` for the yellow split bars

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pptRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#e34721"/>
      <stop offset="100%" stop-color="#c9341a"/>
    </linearGradient>

    <linearGradient id="goldBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffd400"/>
      <stop offset="55%" stop-color="#ffdf19"/>
      <stop offset="100%" stop-color="#ffd000"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Large editable PowerPoint-inspired source object -->
  <path d="M0,102 L292,50 L334,50 L334,116 L570,116
           Q590,116 590,138 L590,570
           Q590,590 570,590 L334,590 L334,670
           L292,670 L0,618 Z"
        fill="url(#pptRed)"/>

  <rect x="334" y="126" width="236" height="452" rx="10"
        fill="none" stroke="#cf3b1e" stroke-width="18"/>

  <path d="M334,206 L382,198 L382,278 L462,278
           Q456,224 418,198 Q386,176 334,184 Z"
        fill="#d94220"/>

  <path d="M384,184
           A100,100 0 0 1 484,284
           L384,284 Z"
        fill="#d94220"/>

  <path d="M464,294
           A114,114 0 0 1 334,420
           L334,350 L464,350 Z"
        fill="#d94220"/>

  <rect x="334" y="420" width="170" height="30" fill="#d94220"/>
  <rect x="334" y="484" width="170" height="30" fill="#d94220"/>

  <text x="76" y="466" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="250" font-weight="900"
        fill="#ffffff">P</text>

  <!-- Divergent origin cue: where the bars are assumed to be stacked on slide 1 -->
  <circle cx="628" cy="360" r="7" fill="#ffcc00"/>
  <line x1="635" y1="360" x2="742" y2="128"
        stroke="#f2c200" stroke-width="4" stroke-dasharray="10 12" opacity="0.45"/>
  <line x1="635" y1="360" x2="690" y2="326"
        stroke="#f2c200" stroke-width="4" stroke-dasharray="10 12" opacity="0.35"/>
  <line x1="635" y1="360" x2="660" y2="526"
        stroke="#f2c200" stroke-width="4" stroke-dasharray="10 12" opacity="0.45"/>

  <!-- Final split state: three independently editable concept slabs -->
  <rect x="704" y="56" width="504" height="142" rx="0"
        fill="url(#goldBar)" filter="url(#softShadow)"/>
  <rect x="648" y="247" width="606" height="154" rx="0"
        fill="url(#goldBar)" filter="url(#softShadow)"/>
  <rect x="620" y="457" width="640" height="140" rx="0"
        fill="url(#goldBar)" filter="url(#softShadow)"/>

  <text x="792" y="169" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="88" font-weight="900"
        letter-spacing="2"
        fill="#ed0000">SPLIT</text>

  <text x="820" y="363" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="900"
        letter-spacing="1"
        fill="#ed0000">TEXT</text>

  <text x="762" y="572" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="900"
        letter-spacing="0"
        fill="#ed0000">EFFECT</text>

  <!-- Small split seams to imply the bars have been pulled apart -->
  <rect x="952" y="56" width="4" height="142" fill="#ffe65a" opacity="0.55"/>
  <rect x="784" y="247" width="4" height="154" fill="#ffe65a" opacity="0.35"/>
  <rect x="977" y="457" width="4" height="140" fill="#ffe65a" opacity="0.45"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; PowerPoint Morph should handle the motion between two slides instead.
- ❌ `<textPath>` for curved trajectory labels; keep labels as normal editable `<text>`.
- ❌ `marker-end` on paths for arrows; if directional arrows are needed, use editable `<line>` plus a separate triangle `<path>`.
- ❌ Clipping text or bars with non-image clip paths; use direct editable rectangles and text so the final deck remains easy to modify.
- ❌ Overly thin decorative strokes on the yellow bars; they can shimmer during Morph and weaken the bold thumbnail-like effect.

## Composition notes
- Keep the left 45% of the canvas reserved for the large source object; it reads as the “whole” before decomposition.
- Place the final split labels in the right 55%, vertically staggered with generous gaps so Morph movement is visually legible.
- For the start slide, duplicate this SVG layout but move all three yellow bars and red text labels to the same origin point near `cx=628, cy=360`; on the final slide, restore the spread positions shown above.
- Use high-saturation red/yellow for the split slabs and a white background for tutorial-thumbnail clarity; for executive decks, the same structure can be recolored to dark navy with neon accent trails.