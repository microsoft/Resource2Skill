# SVG Recipe — Interlocking Geometric Brackets Reveal

## Visual mechanism
Two mirrored custom polygon brackets, built from precise 45-degree cuts, interlock around a single oversized keyword. The brackets behave like engineered reveal doors: one energetic accent side and one dark neutral side compress the viewer’s attention into the center.

## SVG primitives needed
- 1× `<rect>` for the clean off-white slide background
- 2× large `<path>` polygons for the mirrored left/right interlocking bracket bodies
- 4× smaller `<path>` polygons for bevel/facet highlights that make the brackets feel machined rather than flat
- 2× `<line>` elements for thin alignment ticks near the central reveal zone
- 1× `<text>` for the massive uppercase keyword, with explicit `width`
- 1× optional small `<text>` for a technical subtitle/section label, with explicit `width`
- 2× `<linearGradient>` fills for orange and graphite bracket depth
- 1× `<filter id="bracketShadow">` using `feOffset + feGaussianBlur + feMerge` applied to the main bracket paths
- 1× `<filter id="textLift">` using `feGaussianBlur`/merge for subtle typographic lift

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="orangeMachined" x1="248" y1="158" x2="516" y2="562" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7A15D"/>
      <stop offset="0.52" stop-color="#ED7D31"/>
      <stop offset="1" stop-color="#C95F1F"/>
    </linearGradient>

    <linearGradient id="graphiteMachined" x1="764" y1="158" x2="1032" y2="562" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4B4B4B"/>
      <stop offset="0.55" stop-color="#262626"/>
      <stop offset="1" stop-color="#111111"/>
    </linearGradient>

    <linearGradient id="centerSheen" x1="320" y1="275" x2="960" y2="445" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="bracketShadow" x="-12%" y="-12%" width="124%" height="124%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 .20 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-4%" y="-20%" width="108%" height="140%">
      <feOffset dx="0" dy="3" in="SourceAlpha" result="txtOff"/>
      <feGaussianBlur in="txtOff" stdDeviation="3" result="txtBlur"/>
      <feMerge>
        <feMergeNode in="txtBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="#F8F9FA"/>

  <!-- faint central reveal sheen -->
  <path d="M328 300 L952 300 L914 420 L366 420 Z" fill="url(#centerSheen)" opacity="0.55"/>

  <!-- left interlocking bracket: outer 45-degree terminal, vertical spine, inner cut -->
  <path
    d="M421 158
       L248 331
       L248 562
       L315 562
       L315 359
       L516 158
       Z"
    fill="url(#orangeMachined)"
    filter="url(#bracketShadow)"/>

  <!-- right interlocking bracket: exact rotational counterpart -->
  <path
    d="M859 562
       L1032 389
       L1032 158
       L965 158
       L965 361
       L764 562
       Z"
    fill="url(#graphiteMachined)"
    filter="url(#bracketShadow)"/>

  <!-- orange bracket bevel facets -->
  <path d="M421 158 L516 158 L315 359 L315 314 Z" fill="#FFB174" opacity="0.46"/>
  <path d="M248 331 L315 359 L315 562 L248 562 Z" fill="#B94D17" opacity="0.22"/>

  <!-- graphite bracket bevel facets -->
  <path d="M859 562 L764 562 L965 361 L965 406 Z" fill="#5F5F5F" opacity="0.36"/>
  <path d="M1032 158 L965 158 L965 361 L1032 389 Z" fill="#000000" opacity="0.20"/>

  <!-- small precision ticks that reinforce the engineered reveal -->
  <line x1="535" y1="188" x2="585" y2="188" stroke="#ED7D31" stroke-width="5" stroke-linecap="square"/>
  <line x1="695" y1="532" x2="745" y2="532" stroke="#262626" stroke-width="5" stroke-linecap="square"/>

  <!-- central keyword -->
  <text
    x="640"
    y="385"
    width="690"
    text-anchor="middle"
    font-family="Segoe UI, Arial Black, Microsoft YaHei, sans-serif"
    font-size="104"
    font-weight="900"
    letter-spacing="-3"
    fill="#000000"
    filter="url(#textLift)">WELCOME</text>

  <!-- small supporting label -->
  <text
    x="640"
    y="448"
    width="520"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="20"
    font-weight="700"
    letter-spacing="4"
    fill="#6A6A6A">SYSTEM ACCESS REVEAL</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the brackets from rotated rectangles; tiny alignment errors make the 45-degree cuts look amateur and create visible seams.
- ❌ Do not use `<mask>` to simulate the reveal state; PPT translation will fail or ignore it. Show the resolved end-state instead.
- ❌ Do not put `clip-path` on the bracket paths; clipping non-image elements is ignored by the translator.
- ❌ Do not rely on `skewX`, `skewY`, or matrix transforms for the angled geometry; encode the angled cuts directly in the path coordinates.
- ❌ Do not add arrow markers to bracket edges; if directional accents are needed, use standalone `<line>` elements.

## Composition notes
- Keep the central keyword locked to the exact slide center; the brackets should feel mathematically mirrored around it.
- The bracket tips may tuck slightly behind the implied text box, but avoid covering the letters; the text must remain the dominant black anchor.
- Use a bright warm color on one side and a dark neutral on the other to create asymmetric energy while preserving geometric balance.
- Leave generous off-white negative space above and below so the interlocking mark reads like a premium logo reveal, not a chart frame.