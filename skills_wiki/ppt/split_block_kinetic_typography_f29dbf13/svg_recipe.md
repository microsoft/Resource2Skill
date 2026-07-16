# SVG Recipe — Split-Block Kinetic Typography

## Visual mechanism
Massive uppercase words are split into two independent text blocks that hug a central vertical seam: the left block is right-aligned, the right block is left-aligned. The result reads as one compact typographic brick while remaining structurally ready for opposing PowerPoint “Fly In” animations.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark matte background
- 1× `<linearGradient>` for a subtle premium charcoal background wash
- 1× `<filter id="typeShadow">` applied to large text for slight depth/blur
- 1× `<filter id="dropShadow">` applied to decorative icon shapes
- 4× large `<text>` elements for the split kinetic phrase lines
- 2× small translucent `<rect>` elements for motion-streak accents near the seam
- 5× `<circle>` elements for the stopwatch outer body, face, and rings
- 4× `<rect>` elements for stopwatch crown and side buttons
- 1× large `<text>` element for the stopwatch number
- 1× `<path>` for the PowerPoint front panel
- 1× `<rect>` for the PowerPoint rear slide frame
- 1× `<text>` element for the PowerPoint “P”
- 1× `<path>` plus 3× `<rect>` elements for the simplified chart marks inside the PowerPoint icon

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#302d31"/>
      <stop offset="0.55" stop-color="#1f1f22"/>
      <stop offset="1" stop-color="#151518"/>
    </linearGradient>

    <radialGradient id="stopwatchRed" cx="45%" cy="38%" r="68%">
      <stop offset="0" stop-color="#ff4568"/>
      <stop offset="1" stop-color="#ef214a"/>
    </radialGradient>

    <filter id="typeShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="0" dy="2" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="dropShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- matte keynote background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- subtle kinetic streaks that imply opposing entrance motion -->
  <rect x="413" y="299" width="210" height="8" rx="4" fill="#ffffff" opacity="0.08"/>
  <rect x="655" y="299" width="210" height="8" rx="4" fill="#ff0020" opacity="0.10"/>
  <rect x="448" y="484" width="175" height="8" rx="4" fill="#ffffff" opacity="0.06"/>
  <rect x="655" y="484" width="175" height="8" rx="4" fill="#ff0020" opacity="0.09"/>

  <!-- left kinetic block: right-aligned to the center seam -->
  <text x="626" y="346" width="560"
        text-anchor="end"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="116" font-weight="900" letter-spacing="4"
        fill="#ffffff" filter="url(#typeShadow)">WORK</text>

  <text x="626" y="532" width="560"
        text-anchor="end"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="116" font-weight="900" letter-spacing="4"
        fill="#ffffff" filter="url(#typeShadow)">HARD</text>

  <!-- right kinetic block: left-aligned to the center seam with a narrow gap -->
  <text x="658" y="346" width="560"
        text-anchor="start"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="116" font-weight="900" letter-spacing="4"
        fill="#f40018" filter="url(#typeShadow)">PLAY</text>

  <text x="658" y="532" width="560"
        text-anchor="start"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="116" font-weight="900" letter-spacing="4"
        fill="#f40018" filter="url(#typeShadow)">HARD</text>

  <!-- stopwatch accent, bottom left -->
  <rect x="132" y="371" width="60" height="27" rx="12" fill="#ffffff"/>
  <rect x="147" y="391" width="30" height="34" rx="3" fill="#ffffff"/>
  <rect x="38" y="430" width="44" height="18" rx="5" fill="#ffffff" transform="rotate(-45 60 439)"/>
  <rect x="238" y="430" width="44" height="18" rx="5" fill="#ffffff" transform="rotate(45 260 439)"/>

  <circle cx="160" cy="560" r="139" fill="#ffffff" filter="url(#dropShadow)"/>
  <circle cx="160" cy="560" r="116" fill="url(#stopwatchRed)"/>
  <circle cx="160" cy="560" r="104" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.95"/>
  <circle cx="160" cy="560" r="122" fill="none" stroke="#ffffff" stroke-width="8" opacity="0.98"/>

  <text x="160" y="614" width="210"
        text-anchor="middle"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="106" font-weight="900"
        fill="#ffffff">60</text>

  <!-- PowerPoint icon accent, top right -->
  <rect x="1090" y="49" width="168" height="169" rx="5"
        fill="none" stroke="#cf4b32" stroke-width="8" filter="url(#dropShadow)"/>
  <rect x="1159" y="54" width="82" height="58" fill="#ffffff"/>
  <path d="M1186 75 A36 36 0 0 1 1222 111 L1186 111 Z" fill="#cf4b32"/>
  <path d="M1184 116 L1223 116 A39 39 0 0 1 1184 149 Z" fill="#cf4b32"/>
  <rect x="1159" y="161" width="74" height="8" fill="#cf4b32"/>
  <rect x="1159" y="187" width="74" height="8" fill="#cf4b32"/>
  <rect x="1159" y="213" width="74" height="8" fill="#cf4b32"/>

  <path d="M1021 45 L1160 21 L1160 254 L1021 231 Z"
        fill="#d14931" filter="url(#dropShadow)"/>
  <text x="1061" y="178" width="92"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="108" font-weight="800"
        fill="#ffffff">P</text>
</svg>
```

## Avoid in this skill
- ❌ Putting the whole phrase in one centered `<text>` element; the kinetic effect depends on two independently selectable blocks.
- ❌ Measuring individual word widths and manually nudging letters; use opposing `text-anchor` alignment against a fixed seam instead.
- ❌ SVG `<animate>` or `<animateTransform>` for the fly-in motion; create the static layout, then add native PowerPoint entrance animations after translation.
- ❌ `marker-end` arrows or filtered `<line>` objects for motion cues; use simple translucent `<rect>` streaks or paths instead.
- ❌ Skew or matrix transforms for “speed” distortion; these are not reliably preserved.

## Composition notes
- Keep the center seam around `x=640`; place the left block’s anchor slightly left of it and the right block’s anchor slightly right of it to preserve a clean 24–36 px gap.
- Use two stacked lines with tight vertical spacing so the phrase reads as a dense typographic slab, not four separate labels.
- Reserve the largest visual weight for the typography; icons should sit in corners as energetic context, not compete with the central phrase.
- Use a dark matte background, white left-side text, and saturated red right-side text for maximum executive-keynote contrast.