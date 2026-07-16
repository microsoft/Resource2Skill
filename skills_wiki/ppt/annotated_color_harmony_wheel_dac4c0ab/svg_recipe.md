# SVG Recipe — Annotated Color Harmony Wheel

## Visual mechanism
A segmented donut color wheel acts as the anchor while a semi-transparent wedge, outer arc, guide lines, and callout labels make a color-harmony relationship visually explicit. The layout pairs a concise theory explanation on the left with the annotated wheel on the right, creating a clean educational keynote slide.

## SVG primitives needed
- 24× `<path>` for individual editable annular color-wheel segments
- 1× `<path>` for the translucent highlighted harmony wedge
- 1× `<path>` for the outer annotation arc showing the angular range
- 1× `<circle>` for the wheel shadow plate
- 1× `<circle>` for the white center cutout
- 1× `<circle>` for the inner hub badge
- 3× `<circle>` for selected hue markers on the wheel
- 2× `<line>` for callout leader lines
- 6× `<rect>` for background panels, accent bars, label chips, and swatches
- Multiple `<text>` elements with explicit `width` for title, definitions, degree label, and annotations
- 1× `<linearGradient>` for the slide background
- 1× `<radialGradient>` for the center hub
- 1× `<filter id="softShadow">` applied to the wheel backing card
- 1× `<filter id="glow">` applied to hue markers and emphasis text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfaf7"/>
      <stop offset="55%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f3f0ea"/>
    </linearGradient>
    <radialGradient id="hubGrad" cx="50%" cy="42%" r="64%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="65%" stop-color="#f8f6f1"/>
      <stop offset="100%" stop-color="#e7e2d8"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="78" y="80" width="8" height="90" rx="4" fill="#d35400"/>
  <text x="104" y="95" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#d35400">COLOR THEORY / 色彩理论</text>
  <text x="104" y="136" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#333333">Analogous Harmony</text>
  <text x="106" y="190" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#5c5c5c">类似色：相差 60° 以内的色彩</text>

  <rect x="104" y="245" width="458" height="146" rx="24" fill="#ffffff" stroke="#eee7dd" stroke-width="1"/>
  <text x="134" y="284" width="395" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#333333">How to read the wheel</text>
  <text x="134" y="324" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#666666">
    <tspan x="134" dy="0">Choose hues that sit next to each other</tspan>
    <tspan x="134" dy="27">on the color wheel. The relationship feels</tspan>
    <tspan x="134" dy="27">cohesive because neighboring hues share</tspan>
    <tspan x="134" dy="27">visible color DNA.</tspan>
  </text>

  <rect x="104" y="430" width="32" height="32" rx="8" fill="#ff4000"/>
  <rect x="148" y="430" width="32" height="32" rx="8" fill="#ff8000"/>
  <rect x="192" y="430" width="32" height="32" rx="8" fill="#ffbf00"/>
  <text x="244" y="454" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#555555">Example palette: red-orange to amber</text>

  <rect x="104" y="520" width="330" height="54" rx="27" fill="#333333"/>
  <text x="134" y="554" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Recommended range: ±30°</text>

  <circle cx="900" cy="360" r="267" fill="#ffffff" filter="url(#softShadow)"/>
  <circle cx="900" cy="360" r="243" fill="none" stroke="#efe8dc" stroke-width="2"/>

  <path d="M 900 125 A 235 235 0 0 1 960.8 133 L 927.2 258.6 A 105 105 0 0 0 900 255 Z" fill="#ff0000" stroke="#ffffff" stroke-width="2"/>
  <path d="M 960.8 133 A 235 235 0 0 1 1017.5 156.5 L 952.5 269.1 A 105 105 0 0 0 927.2 258.6 Z" fill="#ff4000" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1017.5 156.5 A 235 235 0 0 1 1066.2 193.8 L 974.2 285.8 A 105 105 0 0 0 952.5 269.1 Z" fill="#ff8000" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1066.2 193.8 A 235 235 0 0 1 1103.5 242.5 L 990.9 307.5 A 105 105 0 0 0 974.2 285.8 Z" fill="#ffbf00" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1103.5 242.5 A 235 235 0 0 1 1127 299.2 L 1001.4 332.8 A 105 105 0 0 0 990.9 307.5 Z" fill="#ffff00" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1127 299.2 A 235 235 0 0 1 1135 360 L 1005 360 A 105 105 0 0 0 1001.4 332.8 Z" fill="#bfff00" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1135 360 A 235 235 0 0 1 1127 420.8 L 1001.4 387.2 A 105 105 0 0 0 1005 360 Z" fill="#80ff00" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1127 420.8 A 235 235 0 0 1 1103.5 477.5 L 990.9 412.5 A 105 105 0 0 0 1001.4 387.2 Z" fill="#40ff00" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1103.5 477.5 A 235 235 0 0 1 1066.2 526.2 L 974.2 434.2 A 105 105 0 0 0 990.9 412.5 Z" fill="#00ff00" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1066.2 526.2 A 235 235 0 0 1 1017.5 563.5 L 952.5 450.9 A 105 105 0 0 0 974.2 434.2 Z" fill="#00ff40" stroke="#ffffff" stroke-width="2"/>
  <path d="M 1017.5 563.5 A 235 235 0 0 1 960.8 587 L 927.2 461.4 A 105 105 0 0 0 952.5 450.9 Z" fill="#00ff80" stroke="#ffffff" stroke-width="2"/>
  <path d="M 960.8 587 A 235 235 0 0 1 900 595 L 900 465 A 105 105 0 0 0 927.2 461.4 Z" fill="#00ffbf" stroke="#ffffff" stroke-width="2"/>
  <path d="M 900 595 A 235 235 0 0 1 839.2 587 L 872.8 461.4 A 105 105 0 0 0 900 465 Z" fill="#00ffff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 839.2 587 A 235 235 0 0 1 782.5 563.5 L 847.5 450.9 A 105 105 0 0 0 872.8 461.4 Z" fill="#00bfff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 782.5 563.5 A 235 235 0 0 1 733.8 526.2 L 825.8 434.2 A 105 105 0 0 0 847.5 450.9 Z" fill="#0080ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 733.8 526.2 A 235 235 0 0 1 696.5 477.5 L 809.1 412.5 A 105 105 0 0 0 825.8 434.2 Z" fill="#0040ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 696.5 477.5 A 235 235 0 0 1 673 420.8 L 798.6 387.2 A 105 105 0 0 0 809.1 412.5 Z" fill="#0000ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 673 420.8 A 235 235 0 0 1 665 360 L 795 360 A 105 105 0 0 0 798.6 387.2 Z" fill="#4000ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 665 360 A 235 235 0 0 1 673 299.2 L 798.6 332.8 A 105 105 0 0 0 795 360 Z" fill="#8000ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 673 299.2 A 235 235 0 0 1 696.5 242.5 L 809.1 307.5 A 105 105 0 0 0 798.6 332.8 Z" fill="#bf00ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 696.5 242.5 A 235 235 0 0 1 733.8 193.8 L 825.8 285.8 A 105 105 0 0 0 809.1 307.5 Z" fill="#ff00ff" stroke="#ffffff" stroke-width="2"/>
  <path d="M 733.8 193.8 A 235 235 0 0 1 782.5 156.5 L 847.5 269.1 A 105 105 0 0 0 825.8 285.8 Z" fill="#ff00bf" stroke="#ffffff" stroke-width="2"/>
  <path d="M 782.5 156.5 A 235 235 0 0 1 839.2 133 L 872.8 258.6 A 105 105 0 0 0 847.5 269.1 Z" fill="#ff0080" stroke="#ffffff" stroke-width="2"/>
  <path d="M 839.2 133 A 235 235 0 0 1 900 125 L 900 255 A 105 105 0 0 0 872.8 258.6 Z" fill="#ff0040" stroke="#ffffff" stroke-width="2"/>

  <path d="M 960.8 133 A 235 235 0 0 1 1127 299.2 L 1001.4 332.8 A 105 105 0 0 0 927.2 258.6 Z" fill="#2f2f2f" opacity="0.2"/>
  <path d="M 969.9 99.2 A 270 270 0 0 1 1160.8 290.1" fill="none" stroke="#333333" stroke-width="7" stroke-linecap="round"/>
  <line x1="900" y1="360" x2="960.8" y2="133" stroke="#333333" stroke-width="2" stroke-dasharray="6 8"/>
  <line x1="900" y1="360" x2="1127" y2="299.2" stroke="#333333" stroke-width="2" stroke-dasharray="6 8"/>

  <circle cx="985" cy="212.8" r="15" fill="#ffffff" stroke="#333333" stroke-width="4" filter="url(#glow)"/>
  <circle cx="1020.2" cy="239.8" r="15" fill="#ffffff" stroke="#333333" stroke-width="4" filter="url(#glow)"/>
  <circle cx="1047.2" cy="275" r="15" fill="#ffffff" stroke="#333333" stroke-width="4" filter="url(#glow)"/>

  <circle cx="900" cy="360" r="104" fill="url(#hubGrad)" stroke="#ffffff" stroke-width="5"/>
  <text x="834" y="350" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" text-anchor="middle" fill="#333333" filter="url(#glow)">60°</text>
  <text x="820" y="386" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="17" text-anchor="middle" fill="#666666">shared hue family</text>

  <rect x="1044" y="102" width="160" height="44" rx="22" fill="#333333"/>
  <text x="1064" y="131" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#ffffff">selected arc</text>
  <line x1="1045" y1="148" x2="1017" y2="128" stroke="#333333" stroke-width="2"/>

  <rect x="1052" y="525" width="148" height="66" rx="18" fill="#ffffff" stroke="#e7ded0"/>
  <text x="1073" y="552" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#333333">Harmony cue</text>
  <text x="1073" y="575" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">neighboring hues</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` fills to create the wheel; use individual editable segment paths so each hue remains selectable in PowerPoint.
- ❌ Do not rely on `<mask>` to cut the donut hole; create the donut segments as annular paths and place a normal white center circle above them.
- ❌ Do not use `marker-end` arrowheads for callouts; use plain `<line>` elements and endpoint dots or label chips.
- ❌ Do not apply `filter` to `<line>` elements; shadows and glows should be on circles, rects, paths, or text only.
- ❌ Do not omit `width` on text labels, especially small wheel annotations, because PowerPoint text boxes will otherwise render unpredictably.

## Composition notes
- Keep the wheel large enough to be the visual anchor, typically 40–45% of slide width, with generous white space around it for callouts.
- Reserve the left third to half of the slide for the concept name, short bilingual definition, and palette example; avoid over-explaining near the wheel.
- Use neutral dark gray for annotation geometry so it reads over any hue without fighting the colors.
- Make the highlighted harmony range semi-transparent and add small white marker dots to show the exact chosen hues within the broader color relationship.