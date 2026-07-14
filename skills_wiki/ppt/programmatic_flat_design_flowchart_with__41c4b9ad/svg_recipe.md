# SVG Recipe — Programmatic Flat-Design Flowchart with Retro Accents

## Visual mechanism
A perfectly distributed horizontal process flow uses bold teal circular nodes connected by thick white lines, set against a saturated terracotta field. Retro footer stripes and small geometric accents give the otherwise clean flat-design chart a warm keynote-template personality.

## SVG primitives needed
- 1× `<rect>` for the full-slide terracotta background
- 4× `<rect>` for stacked retro footer stripes
- 4× `<line>` for weighted white node connectors and short decorative footer ticks
- 4× `<circle>` for the primary flowchart nodes
- 4× `<circle>` for small numbered badges inside each node
- 8× `<text>` for title, subtitle, node numbers, and step labels; every text element needs an explicit `width`
- 6× `<path>` for directional chevrons and retro decorative corner motifs
- 1× `<filter id="softShadow">` applied to the circular nodes for editable depth
- 1× `<linearGradient>` for a subtle title highlight or accent fill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="warmHighlight" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE6A7"/>
      <stop offset="100%" stop-color="#FFB84C"/>
    </linearGradient>
  </defs>

  <!-- saturated flat background -->
  <rect x="0" y="0" width="1280" height="720" fill="#D65846"/>

  <!-- retro corner geometry -->
  <circle cx="1148" cy="92" r="74" fill="#C94E3E" opacity="0.55"/>
  <circle cx="1190" cy="54" r="16" fill="#FFC107" opacity="0.95"/>
  <path d="M1018 132 C1056 94, 1102 94, 1140 132" fill="none" stroke="#F6D36B" stroke-width="10" stroke-linecap="round" opacity="0.9"/>
  <path d="M1038 162 C1070 136, 1112 136, 1144 162" fill="none" stroke="#2A3039" stroke-width="8" stroke-linecap="round" opacity="0.75"/>
  <path d="M74 124 L112 88 L150 124 L112 160 Z" fill="#B93736" opacity="0.42"/>

  <!-- title block -->
  <text x="80" y="72" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#FFFFFF">
    Program Launch Flow
  </text>
  <text x="82" y="112" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#FFE7DF" opacity="0.92">
    Four aligned stages, generated with consistent spacing and editable PowerPoint geometry
  </text>

  <!-- baseline connector track behind nodes -->
  <line x1="266" y1="356" x2="414" y2="356" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
  <line x1="566" y1="356" x2="714" y2="356" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
  <line x1="866" y1="356" x2="1014" y2="356" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>

  <!-- directional chevrons; use paths instead of marker-end -->
  <path d="M336 330 L364 356 L336 382" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M636 330 L664 356 L636 382" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M936 330 L964 356 L936 382" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- node 1 -->
  <circle cx="190" cy="356" r="76" fill="#26A69A" filter="url(#softShadow)"/>
  <circle cx="190" cy="310" r="24" fill="#1F827A"/>
  <text x="190" y="318" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#FFFFFF">01</text>
  <text x="190" y="360" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#FFFFFF">
    <tspan x="190" dy="0">Initiate</tspan>
    <tspan x="190" dy="26" font-size="14" font-weight="600" fill="#D9FFFA">define scope</tspan>
  </text>

  <!-- node 2 -->
  <circle cx="490" cy="356" r="76" fill="#26A69A" filter="url(#softShadow)"/>
  <circle cx="490" cy="310" r="24" fill="#1F827A"/>
  <text x="490" y="318" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#FFFFFF">02</text>
  <text x="490" y="360" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#FFFFFF">
    <tspan x="490" dy="0">Build</tspan>
    <tspan x="490" dy="26" font-size="14" font-weight="600" fill="#D9FFFA">create assets</tspan>
  </text>

  <!-- node 3 -->
  <circle cx="790" cy="356" r="76" fill="#26A69A" filter="url(#softShadow)"/>
  <circle cx="790" cy="310" r="24" fill="#1F827A"/>
  <text x="790" y="318" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#FFFFFF">03</text>
  <text x="790" y="360" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#FFFFFF">
    <tspan x="790" dy="0">Review</tspan>
    <tspan x="790" dy="26" font-size="14" font-weight="600" fill="#D9FFFA">test quality</tspan>
  </text>

  <!-- node 4 -->
  <circle cx="1090" cy="356" r="76" fill="#26A69A" filter="url(#softShadow)"/>
  <circle cx="1090" cy="310" r="24" fill="#1F827A"/>
  <text x="1090" y="318" width="48" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#FFFFFF">04</text>
  <text x="1090" y="360" width="126" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#FFFFFF">
    <tspan x="1090" dy="0">Deploy</tspan>
    <tspan x="1090" dy="26" font-size="14" font-weight="600" fill="#D9FFFA">go live</tspan>
  </text>

  <!-- small retro caption card -->
  <rect x="80" y="520" width="330" height="54" rx="18" fill="#B9473C" opacity="0.7"/>
  <circle cx="108" cy="547" r="8" fill="url(#warmHighlight)"/>
  <text x="128" y="553" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#FFFFFF">Morph-ready editable flow</text>

  <!-- footer stripe stack -->
  <rect x="0" y="660" width="1280" height="15" fill="#222831"/>
  <rect x="0" y="675" width="1280" height="15" fill="#FFC107"/>
  <rect x="0" y="690" width="1280" height="15" fill="#8E2828"/>
  <rect x="0" y="705" width="1280" height="15" fill="#EB7E3D"/>
  <line x1="930" y1="682" x2="1002" y2="682" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.75"/>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` arrowheads on connector paths; they may disappear. Use explicit chevron `<path>` shapes or simple `<line>` connectors.
- ❌ Relying on `<text>` without `width`; PowerPoint may clip or lay out text unpredictably.
- ❌ `<pattern>` or noise textures for retro grain; use editable flat shapes, translucent circles, and accent paths instead.
- ❌ Applying filters to `<line>` connector strokes; shadows/glows on lines are dropped, so keep connector lines clean and flat.

## Composition notes
- Keep the flowchart on the horizontal midline, with circles evenly distributed and connectors starting/ending at circle edges.
- Reserve the upper-left quadrant for the title; keep it clear so the chart remains the visual focus.
- Use a warm terracotta field with teal nodes and white connectors for strong contrast, then repeat navy/gold/maroon/orange only in the footer.
- Decorative retro elements should stay secondary: corner arcs, muted diamonds, or small accent cards should not compete with the process nodes.