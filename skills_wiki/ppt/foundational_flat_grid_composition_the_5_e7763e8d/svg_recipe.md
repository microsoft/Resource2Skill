# SVG Recipe — Foundational Flat Grid Composition (The 5 Principles)

## Visual mechanism
A strict flat layout uses one dominant typographic block, generous empty space, and a visible modular grid made from dashed rectangles. The design demonstrates hierarchy through scale, alignment through shared left edges, repetition through identical stroke treatment, and contrast through charcoal text on a mustard field.

## SVG primitives needed
- 1× `<rect>` for the full-slide mustard background
- 3× `<text>` for the oversized two-line headline and small principle labels
- 1× `<rect>` for a flat subtitle highlight block
- 4× dashed `<rect>` for modular layout zones / placeholder grid structure
- 5× small `<circle>` for repeated principle markers
- 5× small `<text>` for the five principle names
- 2× `<line>` for subtle alignment guide accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
      .font { font-family: "Segoe UI", "Microsoft YaHei", sans-serif; }
      .charcoal { fill: #3F3D44; }
      .dashbox { fill: none; stroke: #3F3D44; stroke-width: 3; stroke-dasharray: 4 5; }
      .smallcap { font-size: 17px; font-weight: 800; letter-spacing: 2px; }
      .body { font-size: 18px; font-weight: 600; }
    </style>
  </defs>

  <!-- Flat color field -->
  <rect x="0" y="0" width="1280" height="720" fill="#F2C347"/>

  <!-- Invisible-grid headline: one left edge, two strong lines -->
  <text x="230" y="240" width="840" class="font charcoal"
        font-size="132" font-weight="900" letter-spacing="-5">
    Layout &amp;
  </text>
  <text x="226" y="405" width="910" class="font charcoal"
        font-size="132" font-weight="900" letter-spacing="-5">
    Composition
  </text>

  <!-- Flat highlight, reinforcing contrast and repetition -->
  <rect x="230" y="441" width="288" height="31" fill="#62CCB6"/>
  <text x="244" y="464" width="310" class="font charcoal smallcap">
    THE 5 PRINCIPLES
  </text>

  <!-- Modular grid zones: same stroke, same baseline logic -->
  <rect x="230" y="438" width="575" height="180" class="dashbox"/>
  <rect x="835" y="438" width="215" height="108" class="dashbox"/>
  <rect x="835" y="565" width="215" height="53" class="dashbox"/>

  <!-- Internal proximity group inside large module -->
  <text x="255" y="512" width="490" class="font charcoal"
        font-size="28" font-weight="850">
    Clear hierarchy starts with scale.
  </text>
  <text x="255" y="550" width="465" class="font charcoal"
        font-size="19" font-weight="500">
    Related elements sit close together; unrelated groups get more breathing room.
  </text>

  <!-- Small repeated principle chips -->
  <circle cx="260" cy="588" r="8" fill="#3F3D44"/>
  <text x="278" y="594" width="110" class="font charcoal body">Proximity</text>

  <circle cx="395" cy="588" r="8" fill="#3F3D44"/>
  <text x="413" y="594" width="130" class="font charcoal body">White Space</text>

  <circle cx="570" cy="588" r="8" fill="#3F3D44"/>
  <text x="588" y="594" width="120" class="font charcoal body">Alignment</text>

  <!-- Right modules: compact repeated blocks -->
  <circle cx="862" cy="477" r="18" fill="#62CCB6"/>
  <text x="895" y="486" width="125" class="font charcoal"
        font-size="24" font-weight="850">
    Contrast
  </text>
  <line x1="895" y1="501" x2="1015" y2="501" stroke="#3F3D44" stroke-width="3"/>

  <circle cx="862" cy="591" r="10" fill="#3F3D44"/>
  <text x="885" y="599" width="145" class="font charcoal"
        font-size="21" font-weight="800">
    Repetition
  </text>

  <!-- Alignment ticks: tiny, flat, non-decorative guides -->
  <line x1="230" y1="430" x2="518" y2="430" stroke="#3F3D44" stroke-width="3" stroke-dasharray="4 5"/>
  <line x1="835" y1="430" x2="1050" y2="430" stroke="#3F3D44" stroke-width="3" stroke-dasharray="4 5"/>
</svg>
```

## Avoid in this skill
- ❌ Gradients, glows, shadows, or glass effects; this technique depends on flat contrast and clean geometry.
- ❌ Centering every object independently; the layout should feel locked to a shared invisible grid.
- ❌ Equal spacing everywhere; proximity requires tight internal spacing and larger gaps between groups.
- ❌ Decorative icons that compete with the typographic hierarchy.
- ❌ Text without explicit `width`; PowerPoint needs fixed text box widths for predictable wrapping.

## Composition notes
- Keep the headline huge and heavy; it should occupy the upper half and establish the strongest visual hierarchy.
- Use one dominant left edge for the title, highlight, and main grid module to make alignment immediately visible.
- Leave large uninterrupted yellow space around the content; the negative space is part of the design, not an empty area to fill.
- Repeat the dashed stroke style and charcoal/yellow/teal palette so the slide feels systematic rather than decorative.