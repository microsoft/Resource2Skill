# SVG Recipe — Editorial Grid & Layered Profile

## Visual mechanism
A strict editorial construction grid sits on top of oversized typographic blocks, making the slide feel like a magazine layout in progress. The hierarchy comes from extreme scale contrast: massive yellow headline type dominates the left grid, while a compact cyan subtitle locks into the right column.

## SVG primitives needed
- 1× `<rect>` for the saturated blue slide background
- 1× `<linearGradient>` for a subtle premium blue background variation
- 2× large `<text>` elements for the stacked oversized headline
- 1× multi-line `<text>` with nested `<tspan>` for the right-side subtitle
- 1× `<rect>` for the thin outer editorial frame
- 11× `<line>` elements for dashed vertical, horizontal, and diagonal construction guides
- 4× short `<line>` elements for a small grid intersection crosshair accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueField" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0617E8"/>
      <stop offset="55%" stop-color="#0714D9"/>
      <stop offset="100%" stop-color="#0710C8"/>
    </linearGradient>
  </defs>

  <!-- Saturated editorial background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#blueField)"/>

  <!-- Giant editorial headline locked to the left grid -->
  <text x="108" y="328" width="720"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="182" font-weight="900"
        letter-spacing="-8"
        fill="#FFC20A">
    DESIGN
  </text>

  <text x="108" y="580" width="730"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="184" font-weight="900"
        letter-spacing="-8"
        fill="#FFC20A">
    LAYOUT
  </text>

  <!-- Compact right-column profile/subtitle block -->
  <text x="860" y="210" width="360"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="70" font-weight="900"
        letter-spacing="-2"
        fill="#23BFEA">
    <tspan x="860" dy="0">IN 5 SIMPLE</tspan>
    <tspan x="860" dy="88">STEPS</tspan>
  </text>

  <!-- Thin outer construction frame -->
  <rect x="30" y="30" width="1220" height="660"
        fill="none"
        stroke="#EAFBFF"
        stroke-width="2"/>

  <!-- Horizontal modular guides -->
  <line x1="30" y1="125" x2="1250" y2="125"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>
  <line x1="30" y1="329" x2="1250" y2="329"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>
  <line x1="30" y1="580" x2="1250" y2="580"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>

  <!-- Vertical modular guides -->
  <line x1="110" y1="30" x2="110" y2="690"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>
  <line x1="818" y1="30" x2="818" y2="690"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>
  <line x1="863" y1="30" x2="863" y2="690"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>

  <!-- Right-side diagonal construction guide -->
  <line x1="865" y1="690" x2="1250" y2="306"
        stroke="#EAFBFF" stroke-width="2"
        stroke-dasharray="12 12"/>

  <!-- Small editorial crosshair at the main grid intersection -->
  <line x1="808" y1="125" x2="828" y2="125"
        stroke="#EAFBFF" stroke-width="2"/>
  <line x1="818" y1="115" x2="818" y2="135"
        stroke="#EAFBFF" stroke-width="2"/>
  <line x1="853" y1="125" x2="873" y2="125"
        stroke="#EAFBFF" stroke-width="2"/>
  <line x1="863" y1="115" x2="863" y2="135"
        stroke="#EAFBFF" stroke-width="2"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the dashed construction grid as a raster image; use editable `<line>` elements with `stroke-dasharray`.
- ❌ Do not use `<pattern>` for the grid, because pattern fills may be dropped or flattened.
- ❌ Do not use `textPath`, skew transforms, or matrix transforms to fake editorial type perspective.
- ❌ Do not rely on automatic text fitting; every `<text>` element must have an explicit `width`.
- ❌ Do not place the grid behind the headline if you want the “layout blueprint” effect; the dashed lines should sit above the typography.

## Composition notes
- Keep the left 65% of the slide dominated by the oversized headline; let the letters nearly collide with the grid lines.
- Use the right third as a compact secondary information zone, aligned to the same horizontal guides.
- The white dashed grid should be visible but not thicker than the typography; it is a construction overlay, not the main message.
- Limit the palette to electric blue, yellow, cyan, and white for a bold keynote/editorial rhythm.