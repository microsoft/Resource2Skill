# SVG Recipe — High-Contrast Branching Process Diagram

## Visual mechanism
Use dark teal flowchart nodes with thick white “sticker” outlines on a pale cyan background, then drive the reading order with thick orange arrow connectors. The diagram branches from a central decision hub into three parallel tracks and merges back into a single end state.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft gradient background.
- 2× `<ellipse>` for START and END terminals.
- 5× `<rect>` for process/action nodes and merge steps.
- 1× `<circle>` for the central branching decision hub.
- 9× `<line>` for direct arrow connectors, each with its own `marker-end`.
- Multiple `<text>` elements for centered labels; every text element includes an explicit `width`.
- 1× `<linearGradient>` for the subtle cyan-to-white background.
- 1× `<marker>` for the orange triangle arrowhead.

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgCyan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#d6f0f2"/>
      <stop offset="55%" stop-color="#fbfefe"/>
      <stop offset="100%" stop-color="#e3f6f7"/>
    </linearGradient>
    <marker id="arrowOrange" viewBox="0 0 10 10" refX="10" refY="5"
            markerWidth="10" markerHeight="10" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#f39c12"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgCyan)"/>

  <text x="70" y="62" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="700" fill="#333333">
    HIGH-CONTRAST PROCESS FLOW
  </text>

  <!-- Connectors behind nodes -->
  <line x1="180" y1="360" x2="280" y2="360" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="440" y1="360" x2="520" y2="360" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="620" y1="330" x2="720" y2="205" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="625" y1="360" x2="720" y2="360" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="620" y1="390" x2="720" y2="515" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="900" y1="205" x2="990" y2="330" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="900" y1="360" x2="990" y2="360" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="900" y1="515" x2="990" y2="390" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>
  <line x1="1110" y1="360" x2="1175" y2="360" stroke="#f39c12" stroke-width="6"
        stroke-linecap="round" marker-end="url(#arrowOrange)"/>

  <!-- Nodes -->
  <ellipse cx="120" cy="360" rx="70" ry="48" fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>
  <rect x="280" y="310" width="160" height="100" rx="16" ry="16"
        fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>
  <circle cx="570" cy="360" r="62" fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>

  <rect x="720" y="155" width="180" height="100" rx="14" ry="14"
        fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>
  <rect x="720" y="310" width="180" height="100" rx="14" ry="14"
        fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>
  <rect x="720" y="465" width="180" height="100" rx="14" ry="14"
        fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>

  <rect x="990" y="310" width="120" height="100" rx="14" ry="14"
        fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>
  <ellipse cx="1210" cy="360" rx="62" ry="48" fill="#1e8e8e" stroke="#ffffff" stroke-width="5"/>

  <!-- Node labels -->
  <text x="120" y="369" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" fill="#ffffff">START</text>

  <text x="360" y="349" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">VALIDATE</text>
  <text x="360" y="374" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">REQUEST</text>

  <text x="570" y="351" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">ROUTE</text>
  <text x="570" y="376" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">BY TYPE</text>

  <text x="810" y="199" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">PROCESS A</text>
  <text x="810" y="224" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#ffffff">FAST TRACK</text>

  <text x="810" y="354" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">PROCESS B</text>
  <text x="810" y="379" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#ffffff">STANDARD</text>

  <text x="810" y="509" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#ffffff">PROCESS C</text>
  <text x="810" y="534" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#ffffff">ESCALATE</text>

  <text x="1050" y="354" width="110" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#ffffff">MERGE</text>
  <text x="1050" y="379" width="110" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#ffffff">RESULTS</text>

  <text x="1210" y="369" width="110" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" fill="#ffffff">END</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path>` for the decision diamond, parallelograms, or elbow connectors; those will not remain clean editable PowerPoint shapes in this restricted subset.
- ❌ Do not put `marker-end` on a parent `<g>`; every `<line>` must carry its own arrowhead attribute.
- ❌ Do not apply filters to text, nodes, or arrows; filtered subtrees may rasterize and lose editability.
- ❌ Do not rely on rotated rectangles for diamonds or slanted process boxes; only `translate(x y)` transforms are safe.

## Composition notes
- Keep the main flow centered vertically, with the branching hub near the middle and three evenly spaced tracks above, center, and below it.
- Use high contrast: dark teal nodes, white outlines/text, and orange arrows; avoid adding many secondary colors.
- Leave generous negative space around the branch tracks so the orange connectors remain visually dominant.
- Place the title in the upper-left and keep it separate from the diagram grid to preserve a clean operational-dashboard feel.