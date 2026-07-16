# SVG Recipe — Swiss Brutalist Color & Grid System

## Visual mechanism
A strict Swiss grid turns color into a functional system: off-white creates breathing room, navy communicates, orange signals action, teal supports secondary flow, and gray anchors the structure. The slide feels like a modern product interface because every block, border, image, and CTA has a clearly assigned role.

## SVG primitives needed
- 1× `<rect>` for the neutral off-white canvas background
- 6–10× `<line>` for visible Swiss grid dividers and structural anchor rules
- 8–12× `<rect>` for functional panels, CTA button, hard shadow, metric cards, nav chips, and support blocks
- 1× `<image>` for an editorial product/architecture photo clipped into the right-side grid column
- 1× `<clipPath>` with rounded `<rect>` applied to the image crop
- 1× `<filter id="softShadow">` for subtle card depth on selected rectangular UI blocks
- 1× `<linearGradient>` for a quiet support-panel highlight without breaking the brutalist palette
- 1–2× `<path>` for angular UI accents or brutalist corner marks
- Multiple `<text>` elements with explicit `width` attributes for oversized headings, metadata, labels, and compact dashboard copy
- Optional `<tspan>` inside `<text>` for inline color emphasis in labels or captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealWash" x1="0" y1="560" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#77BAAD"/>
      <stop offset="1" stop-color="#9ED1C8"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="8" dy="8" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="0.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClip">
      <rect x="704" y="116" width="512" height="354" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <!-- Neutral canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#F6F4F1"/>

  <!-- Swiss structural grid: anchor lines -->
  <line x1="0" y1="82" x2="1280" y2="82" stroke="#B4B4B4" stroke-width="1"/>
  <line x1="640" y1="82" x2="640" y2="560" stroke="#B4B4B4" stroke-width="1"/>
  <line x1="0" y1="560" x2="1280" y2="560" stroke="#B4B4B4" stroke-width="1"/>
  <line x1="72" y1="82" x2="72" y2="560" stroke="#B4B4B4" stroke-width="1"/>
  <line x1="1216" y1="82" x2="1216" y2="560" stroke="#B4B4B4" stroke-width="1"/>
  <line x1="704" y1="116" x2="1216" y2="116" stroke="#B4B4B4" stroke-width="1"/>
  <line x1="704" y1="470" x2="1216" y2="470" stroke="#B4B4B4" stroke-width="1"/>

  <!-- Top navigation -->
  <text x="72" y="46" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#122638" letter-spacing="1.2">
    SATORI SYSTEM
  </text>
  <text x="400" y="46" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#122638">
    COLOR ROLES
  </text>
  <text x="540" y="46" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#122638">
    GRID / 12 COL
  </text>
  <rect x="1048" y="24" width="168" height="34" rx="17" fill="#122638"/>
  <text x="1072" y="47" width="128" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#F6F4F1">
    LIVE SYSTEM
  </text>

  <!-- Left communicator column -->
  <text x="72" y="164" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="800" fill="#122638" letter-spacing="-4">
    FUNCTIONAL
  </text>
  <text x="72" y="238" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="800" fill="#122638" letter-spacing="-4">
    COLOR
  </text>
  <text x="72" y="312" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="800" fill="#122638" letter-spacing="-4">
    MAPPING
  </text>

  <rect x="80" y="364" width="38" height="8" fill="#EB5E28"/>
  <text x="72" y="414" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" fill="#122638">
    A product-deck grid where each color has a job: communicate, support, stabilize, or trigger action.
  </text>

  <!-- Brutalist CTA with hard editable shadow -->
  <rect x="84" y="488" width="184" height="52" fill="#122638"/>
  <rect x="72" y="476" width="184" height="52" fill="#EB5E28" stroke="#122638" stroke-width="2"/>
  <text x="106" y="510" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="800" fill="#122638" letter-spacing="1.1">
    JOIN NOW
  </text>

  <!-- Micro functional legend -->
  <rect x="316" y="476" width="230" height="52" fill="none" stroke="#B4B4B4" stroke-width="1"/>
  <rect x="334" y="494" width="18" height="18" fill="#EB5E28"/>
  <text x="362" y="508" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#122638">
    ACTION ONLY
  </text>
  <text x="362" y="526" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#122638">
    Reserved for conversion.
  </text>

  <!-- Right editorial photo module -->
  <rect x="716" y="128" width="512" height="354" rx="18" fill="#122638" opacity="0.18"/>
  <image x="704" y="116" width="512" height="354" clip-path="url(#photoClip)"
         href="https://images.example.com/duotone-navy-offwhite-brutalist-architecture-product-interface.jpg"/>
  <rect x="704" y="116" width="512" height="354" rx="18" fill="none" stroke="#122638" stroke-width="2"/>

  <!-- Angular brutalist corner marks -->
  <path d="M704 116 L760 116 L704 172 Z" fill="#EB5E28"/>
  <path d="M1216 470 L1160 470 L1216 414 Z" fill="#77BAAD"/>

  <!-- Right-side metadata cards -->
  <rect x="704" y="494" width="156" height="46" fill="#F6F4F1" stroke="#B4B4B4" stroke-width="1"/>
  <text x="720" y="514" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#122638">
    COMMUNICATOR
  </text>
  <text x="720" y="535" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#122638">
    NAVY
  </text>

  <rect x="876" y="494" width="156" height="46" fill="#F6F4F1" stroke="#B4B4B4" stroke-width="1"/>
  <text x="892" y="514" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#122638">
    SUPPORT
  </text>
  <text x="892" y="535" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#77BAAD">
    TEAL
  </text>

  <rect x="1048" y="494" width="168" height="46" fill="#F6F4F1" stroke="#B4B4B4" stroke-width="1"/>
  <text x="1064" y="514" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#122638">
    ANCHOR
  </text>
  <text x="1064" y="535" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#B4B4B4">
    GRID
  </text>

  <!-- Bottom support row -->
  <rect x="0" y="560" width="1280" height="160" fill="url(#tealWash)"/>
  <line x1="320" y1="560" x2="320" y2="720" stroke="#122638" stroke-width="1"/>
  <line x1="640" y1="560" x2="640" y2="720" stroke="#122638" stroke-width="1"/>
  <line x1="960" y1="560" x2="960" y2="720" stroke="#122638" stroke-width="1"/>

  <text x="72" y="612" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#122638">
    01 / NEUTRAL
  </text>
  <text x="72" y="662" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#122638">
    REST
  </text>

  <text x="392" y="612" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#122638">
    02 / ANCHOR
  </text>
  <text x="392" y="662" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#122638">
    ALIGN
  </text>

  <text x="712" y="612" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#122638">
    03 / SUPPORT
  </text>
  <text x="712" y="662" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#122638">
    FLOW
  </text>

  <rect x="1028" y="604" width="150" height="48" fill="#EB5E28" stroke="#122638" stroke-width="2" filter="url(#softShadow)"/>
  <text x="1056" y="635" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#122638">
    ACT
  </text>
</svg>
```

## Avoid in this skill
- ❌ Random decorative color accents; every color must map to a functional role.
- ❌ Soft pastel gradients across the full slide; they weaken the Swiss/brutalist system.
- ❌ Applying `clip-path` to rectangles or text; use it only on the `<image>` crop.
- ❌ Using `<pattern>` for grid backgrounds; draw explicit editable `<line>` elements instead.
- ❌ Arrowheads with `marker-end` on paths; if directional UI is needed, use plain `<line>` plus separate editable shapes.

## Composition notes
- Keep the grid visible: top nav, center split, bottom support row, and outer margin rules should feel intentional rather than decorative.
- Reserve orange for one or two true action moments only; overusing it destroys the functional hierarchy.
- Let the huge navy headline dominate the left half while the right half carries the duotone image and compact system metadata.
- Use teal as the secondary flow zone, usually in the bottom row or a side panel, so the eye has a place to rest after the CTA.