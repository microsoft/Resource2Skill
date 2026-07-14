# SVG Recipe — Diagonal Kinetic Typography

## Visual mechanism
Large diagonal color fields slice the slide into a high-energy composition, with rotated typography aligned to the cuts so the words feel like they are moving through the canvas. Soft shadows, edge highlights, speed lines, and oversized display type create a layered “motion graphics title card” effect while remaining editable SVG/PPT shapes.

## SVG primitives needed
- 1× `<rect>` for the off-white full-slide background
- 2× `<path>` for the dominant diagonal red-orange and cyan paper-cut panels
- 4× `<path>` for subtle diagonal background ribbons and panel edge highlights
- 10× `<line>` for kinetic speed-line accents aligned with the diagonal axes
- 9× `<text>` for rotated headline, label, number, ampersand, and supporting typography
- 2× `<linearGradient>` for premium color depth on the two main panels
- 1× `<filter id="paperShadow">` using `feOffset + feGaussianBlur + feMerge` applied to the large diagonal panels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="redOrange" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF7148"/>
      <stop offset="58%" stop-color="#ED552A"/>
      <stop offset="100%" stop-color="#C93A1C"/>
    </linearGradient>

    <linearGradient id="cyanBlue" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#35D3F2"/>
      <stop offset="56%" stop-color="#1DACD6"/>
      <stop offset="100%" stop-color="#0E78A5"/>
    </linearGradient>

    <filter id="paperShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.30  0 0 0 0 0.30  0 0 0 0 0.30  0 0 0 0.35 0"
        result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F2F2F2"/>

  <!-- pale diagonal atmosphere ribbons -->
  <path d="M-80 92 L236 0 L330 0 L-20 132 Z" fill="#FFFFFF" opacity="0.70"/>
  <path d="M945 720 L1280 602 L1280 660 L1065 720 Z" fill="#FFFFFF" opacity="0.75"/>
  <path d="M424 0 L470 0 L270 720 L224 720 Z" fill="#E4E4E4" opacity="0.50"/>
  <path d="M842 0 L890 0 L1068 720 L1018 720 Z" fill="#E4E4E4" opacity="0.42"/>

  <!-- dominant diagonal color panels -->
  <path d="M-120 -60 L540 -60 L318 780 L-120 780 Z"
        fill="url(#redOrange)" filter="url(#paperShadow)"/>
  <path d="M738 -60 L1400 -60 L1400 780 L960 780 Z"
        fill="url(#cyanBlue)" filter="url(#paperShadow)"/>

  <!-- crisp inner cut highlights -->
  <path d="M522 -60 L546 -60 L324 780 L300 780 Z" fill="#FFFFFF" opacity="0.20"/>
  <path d="M718 -60 L742 -60 L966 780 L942 780 Z" fill="#FFFFFF" opacity="0.22"/>

  <!-- kinetic speed lines: left panel -->
  <line x1="58" y1="560" x2="248" y2="505" stroke="#FFFFFF" stroke-width="4" opacity="0.48"/>
  <line x1="92" y1="602" x2="300" y2="542" stroke="#FFFFFF" stroke-width="2.5" opacity="0.36"/>
  <line x1="130" y1="645" x2="346" y2="582" stroke="#FFFFFF" stroke-width="2" opacity="0.30"/>
  <line x1="54" y1="174" x2="212" y2="128" stroke="#FFFFFF" stroke-width="3" opacity="0.42"/>
  <line x1="84" y1="214" x2="244" y2="168" stroke="#FFFFFF" stroke-width="2" opacity="0.30"/>

  <!-- kinetic speed lines: right panel -->
  <line x1="930" y1="140" x2="1144" y2="202" stroke="#FFFFFF" stroke-width="4" opacity="0.48"/>
  <line x1="900" y1="178" x2="1110" y2="238" stroke="#FFFFFF" stroke-width="2.5" opacity="0.34"/>
  <line x1="974" y1="552" x2="1210" y2="620" stroke="#FFFFFF" stroke-width="3" opacity="0.42"/>
  <line x1="930" y1="506" x2="1138" y2="566" stroke="#FFFFFF" stroke-width="2" opacity="0.32"/>
  <line x1="1034" y1="94" x2="1220" y2="148" stroke="#FFFFFF" stroke-width="2" opacity="0.28"/>

  <!-- left-side rotated typography -->
  <text x="78" y="146" width="300" transform="rotate(-16 78 146)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4" fill="#FFE9E0" opacity="0.92">
    01 / MOMENTUM
  </text>

  <text x="82" y="272" width="520" transform="rotate(-16 82 272)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="800" letter-spacing="-3" fill="#FFFFFF">
    IGNITE
  </text>

  <text x="96" y="332" width="380" transform="rotate(-16 96 332)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="600" fill="#32110A" opacity="0.72">
    launch the narrative
  </text>

  <!-- central kinetic title stack -->
  <text x="470" y="260" width="360" transform="rotate(-10 470 260)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" letter-spacing="7" fill="#1F1F1F">
    DIAGONAL
  </text>

  <text x="448" y="342" width="420" transform="rotate(-10 448 342)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="800" letter-spacing="-2" fill="#1F1F1F">
    KINETIC
  </text>

  <text x="584" y="445" width="160" transform="rotate(-10 584 445)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="300" fill="#D8D8D8">
    &amp;
  </text>

  <!-- right-side rotated typography -->
  <text x="834" y="168" width="330" transform="rotate(16 834 168)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4" fill="#DFF8FF" opacity="0.94">
    02 / SIGNAL
  </text>

  <text x="800" y="314" width="520" transform="rotate(16 800 314)"
        font-family="Century Gothic, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="84" font-weight="800" letter-spacing="-3" fill="#FFFFFF">
    SCALE
  </text>

  <text x="826" y="378" width="390" transform="rotate(16 826 378)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="600" fill="#043344" opacity="0.76">
    accelerate attention
  </text>
</svg>
```

## Avoid in this skill
- ❌ `<animate>` or motion-path SVG animation; PPT-Master will hard-fail animated SVG, so imply motion with rotated text, ghosting, and speed lines instead
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)`; build diagonal geometry directly with `<path>` coordinates
- ❌ `marker-end` arrows on diagonal paths; use plain `<line>` speed accents instead
- ❌ Clipping or masking text/shapes; only use `clipPath` on `<image>` elements if you add a photo variant
- ❌ Text without `width`; every `<text>` needs an explicit `width` so PowerPoint preserves the intended layout

## Composition notes
- Keep the central channel mostly light and uncluttered; it is the breathing space that makes the diagonal typography readable.
- Let the colored diagonal panels dominate 75–85% of the slide area, with typography rotated parallel to the nearest panel edge.
- Use high-contrast white text on saturated panels, then darker charcoal text in the central off-white area.
- Speed lines should be thin and semi-transparent; they support motion but should not compete with the main words.