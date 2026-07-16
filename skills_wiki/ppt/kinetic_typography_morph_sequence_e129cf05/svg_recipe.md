# SVG Recipe — Kinetic Typography Morph Sequence

## Visual mechanism
Treat words as heavyweight physical blocks: oversized condensed text, rotated 90° in some columns, packed into a tight central typographic wall. The “animation” is authored as multiple SVG/PPT keyframes with the same object IDs/names, then PowerPoint Morph interpolates each word’s position, scale, and rotation.

## SVG primitives needed
- 1× `<rect>` for the clean full-slide background
- 1× `<rect>` for the elevated white poster/card surface
- 2× off-canvas `<rect>` shutters for a later Morph close transition
- 3× translucent `<path>` motion swashes behind the type wall
- 4× `<line>` registration/energy ticks framing the typographic lockup
- 11× `<text>` objects for the packed kinetic words and small sequence labels
- 1× `<linearGradient>` for the poster edge highlight
- 1× `<radialGradient>` for the subtle stage glow
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` applied to the poster card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="stageGlow" cx="50%" cy="45%" r="62%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#f7fafc"/>
      <stop offset="100%" stop-color="#e9eef5"/>
    </radialGradient>

    <linearGradient id="cardEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="54%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#eef2f7"/>
    </linearGradient>

    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="20" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect id="bg" x="0" y="0" width="1280" height="720" fill="url(#stageGlow)"/>

  <path id="motion_orange" d="M160,192 C310,92 475,104 642,168 C774,218 902,199 1060,118 L1096,168 C923,267 763,286 606,226 C450,166 309,165 186,252 Z"
        fill="#f4722b" opacity="0.10"/>
  <path id="motion_cyan" d="M198,562 C352,474 486,472 650,536 C794,592 936,574 1105,486 L1134,538 C950,650 784,660 612,596 C458,538 335,540 220,616 Z"
        fill="#03a9f4" opacity="0.11"/>
  <path id="motion_purple" d="M252,366 C396,260 586,250 746,342 C888,424 1002,405 1138,310 L1160,366 C1005,484 858,508 706,414 C558,322 416,324 280,420 Z"
        fill="#9c27b0" opacity="0.08"/>

  <rect id="poster_card" x="168" y="70" width="944" height="580" rx="34"
        fill="url(#cardEdge)" filter="url(#cardShadow)"/>

  <line id="tick_top_left" x1="218" y1="116" x2="312" y2="116" stroke="#212b36" stroke-width="5" stroke-linecap="round"/>
  <line id="tick_top_right" x1="968" y1="116" x2="1062" y2="116" stroke="#212b36" stroke-width="5" stroke-linecap="round"/>
  <line id="tick_bot_left" x1="218" y1="606" x2="312" y2="606" stroke="#212b36" stroke-width="5" stroke-linecap="round"/>
  <line id="tick_bot_right" x1="968" y1="606" x2="1062" y2="606" stroke="#212b36" stroke-width="5" stroke-linecap="round"/>

  <text id="seq_label" x="218" y="102" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="2" fill="#5d6976">KEYFRAME 03 · LOCKED WALL</text>

  <text id="morph_note" x="772" y="102" width="295"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600"
        text-anchor="end" fill="#7a8794">same IDs across slides → Morph</text>

  <text id="word_USING" x="0" y="0" width="355"
        transform="translate(302 568) rotate(-90)"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="116" font-weight="900"
        letter-spacing="-3" fill="#03a9f4">USING</text>

  <text id="word_FAST" x="0" y="0" width="300"
        transform="translate(386 568) rotate(-90)"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="104" font-weight="900"
        letter-spacing="-3" fill="#8bc34a">FAST</text>

  <text id="word_EASY" x="0" y="0" width="298"
        transform="translate(244 568) rotate(-90)"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="96" font-weight="900"
        letter-spacing="-3" fill="#e91e63">EASY</text>

  <text id="word_FUN" x="0" y="0" width="210"
        transform="translate(420 348) rotate(-90)"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="94" font-weight="900"
        letter-spacing="-2" fill="#9c27b0">FUN</text>

  <text id="word_STUNNING" x="452" y="208" width="600"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="108" font-weight="900"
        letter-spacing="-4" fill="#f4722b">STUNNING</text>

  <text id="word_TITLES" x="452" y="328" width="520"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="136" font-weight="900"
        letter-spacing="-5" fill="#212b36">TITLES</text>

  <text id="word_POWERPOINT" x="456" y="406" width="610"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="900"
        letter-spacing="-2" fill="#009688">POWERPOINT</text>

  <text id="word_ANIMATION" x="456" y="508" width="420"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="92" font-weight="900"
        letter-spacing="-3" fill="#9c27b0">ANIMATION</text>

  <text id="word_EFFECT" x="838" y="508" width="250"
        font-family="Impact, Segoe UI, Microsoft YaHei, sans-serif" font-size="92" font-weight="900"
        letter-spacing="-3" fill="#e91e63">EFFECT</text>

  <rect id="morph_TopShutter_offscreen" x="0" y="-372" width="1280" height="360" fill="#212b36"/>
  <rect id="morph_BottomShutter_offscreen" x="0" y="732" width="1280" height="360" fill="#212b36"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>`; PowerPoint Morph should create the motion between duplicate slide/keyframe states.
- ❌ Do not convert words to outlined `<path>` shapes unless the text must be non-editable; editable text is the point of this technique.
- ❌ Do not rely on SVG word wrapping. Keep every word in its own `<text width="...">` object with large explicit bounds.
- ❌ Do not use `<textPath>` for curved kinetic type; it will not translate reliably.
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` transforms for fake perspective; use only translate, rotate, and scale.
- ❌ Do not place filters on `<line>` elements; use filters only on rect/path/text/circle/ellipse if needed.

## Composition notes
- Build the sequence as 3–5 duplicate slides: scatter words off-canvas or at tiny scale in slide 1, partially assemble in slide 2, lock the packed wall in slide 3, then move the shutter rectangles on-canvas in slide 4.
- Keep the same word IDs/names across every keyframe; after import into PowerPoint, name corresponding shapes consistently, ideally with PowerPoint’s Morph-tracking convention such as `!!word_STUNNING`.
- The central type wall should occupy roughly 65–75% of slide width, with tight gaps between word blocks and generous clean space around the poster card.
- Use one dark neutral word as the visual anchor, then distribute saturated accent colors so the viewer’s eye scans vertically and horizontally through the lockup.