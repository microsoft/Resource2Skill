# SVG Recipe — Flat Whiteboard Doodle Explainer Style

## Visual mechanism
A bright off-white “digital whiteboard” is framed by cinematic film-strip borders, then filled with oversized doodle-like typography, crossed-out pain-point bubbles, and a simple geometric explainer icon. The style uses stark black linework with red marker “X” strokes and green solution accents to make the narrative feel like a live whiteboard explanation.

## SVG primitives needed
- 1× `<rect>` for the off-white paper background
- 2× `<rect>` for the black film-strip bars
- 32× small `<rect>` for repeated white sprocket holes
- 2× rounded `<rect>` for crossed-out pain-point bubbles
- 4× rough `<path>` strokes for red marker X marks
- 6× `<text>` blocks with explicit `width` for pain labels, headline, subtitle, and step captions
- 5× decorative `<path>` doodles for underline, arrow, burst marks, and hand-drawn motion lines
- 1× large `<circle>` plus 5× smaller `<circle>` elements for the film-reel icon
- 1× `<path>` for the green play-button triangle
- 1× `<linearGradient>` for the green icon fill
- 1× `<filter id="softShadow">` applied to cards and the icon for subtle depth
- 1× `<filter id="markerGlow">` applied to red X strokes for marker emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="greenPop" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#78D66E"/>
      <stop offset="100%" stop-color="#3FAE46"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="markerGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="1.8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8F9FA"/>

  <!-- subtle whiteboard doodle texture -->
  <path d="M88 137 C155 112, 210 128, 270 104" fill="none" stroke="#E5E8EB" stroke-width="4" stroke-linecap="round"/>
  <path d="M960 160 C1014 124, 1086 132, 1138 101" fill="none" stroke="#E5E8EB" stroke-width="4" stroke-linecap="round"/>
  <path d="M160 580 C250 548, 346 590, 442 556" fill="none" stroke="#E5E8EB" stroke-width="4" stroke-linecap="round"/>
  <path d="M760 590 C840 552, 940 586, 1045 552" fill="none" stroke="#E5E8EB" stroke-width="4" stroke-linecap="round"/>

  <!-- film strip borders -->
  <rect x="0" y="0" width="1280" height="46" fill="#1E1E1E"/>
  <rect x="0" y="674" width="1280" height="46" fill="#1E1E1E"/>
  <rect x="24" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="96" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="168" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="240" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="312" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="384" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="456" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="528" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="600" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="672" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="744" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="816" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="888" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="960" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="1032" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="1104" y="13" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="24" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="96" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="168" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="240" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="312" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="384" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="456" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="528" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="600" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="672" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="744" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="816" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="888" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="960" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="1032" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>
  <rect x="1104" y="687" width="22" height="20" rx="3" fill="#FFFFFF"/>

  <!-- crossed-out pain points -->
  <rect x="105" y="102" width="220" height="78" rx="22" fill="#FFFFFF" stroke="#55AF4B" stroke-width="5" filter="url(#softShadow)"/>
  <text x="145" y="153" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#1E1E1E">不会拍摄</text>
  <path d="M286 104 L324 142" fill="none" stroke="#EB3232" stroke-width="12" stroke-linecap="round" filter="url(#markerGlow)"/>
  <path d="M323 105 L284 143" fill="none" stroke="#EB3232" stroke-width="12" stroke-linecap="round" filter="url(#markerGlow)"/>

  <rect x="365" y="102" width="220" height="78" rx="22" fill="#FFFFFF" stroke="#55AF4B" stroke-width="5" filter="url(#softShadow)"/>
  <text x="405" y="153" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#1E1E1E">不想出镜</text>
  <path d="M548 104 L586 142" fill="none" stroke="#EB3232" stroke-width="12" stroke-linecap="round" filter="url(#markerGlow)"/>
  <path d="M586 105 L546 143" fill="none" stroke="#EB3232" stroke-width="12" stroke-linecap="round" filter="url(#markerGlow)"/>

  <!-- headline block -->
  <text x="95" y="282" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="900" fill="#1E1E1E">
    用 <tspan fill="#55AF4B" font-size="72">PPT</tspan> 也能做出
  </text>
  <text x="95" y="374" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="86" font-weight="900" fill="#1E1E1E">好看的视频！</text>
  <path d="M110 397 C220 420, 365 414, 555 398" fill="none" stroke="#55AF4B" stroke-width="11" stroke-linecap="round"/>
  <text x="112" y="466" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#2E2E2E">不用露脸，不用拍摄，按步骤把想法讲清楚。</text>

  <!-- doodle step cards -->
  <path d="M118 518 C155 494, 203 496, 245 515 C218 548, 158 550, 118 518 Z" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="4"/>
  <text x="145" y="528" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#1E1E1E">脚本</text>
  <path d="M268 520 C305 494, 356 498, 398 518 C367 550, 306 552, 268 520 Z" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="4"/>
  <text x="294" y="529" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#1E1E1E">画面</text>
  <path d="M420 519 C458 493, 512 498, 550 517 C522 552, 459 550, 420 519 Z" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="4"/>
  <text x="445" y="529" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#1E1E1E">配音</text>

  <!-- right-side film reel / play icon -->
  <circle cx="936" cy="356" r="154" fill="url(#greenPop)" stroke="#1E1E1E" stroke-width="9" filter="url(#softShadow)"/>
  <circle cx="936" cy="356" r="54" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="7"/>
  <circle cx="936" cy="240" r="30" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="6"/>
  <circle cx="1047" cy="320" r="30" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="6"/>
  <circle cx="1005" cy="452" r="30" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="6"/>
  <circle cx="867" cy="452" r="30" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="6"/>
  <circle cx="825" cy="320" r="30" fill="#FFFFFF" stroke="#1E1E1E" stroke-width="6"/>
  <path d="M918 324 L918 389 L974 357 Z" fill="#1E1E1E"/>

  <!-- hand-drawn callout arrow and energy marks -->
  <path d="M650 405 C720 390, 746 360, 777 325" fill="none" stroke="#1E1E1E" stroke-width="6" stroke-linecap="round"/>
  <path d="M775 325 L758 328 L769 343 Z" fill="#1E1E1E"/>
  <text x="735" y="555" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="900" fill="#55AF4B">像讲故事一样做课件</text>
  <path d="M1112 214 L1150 183" fill="none" stroke="#EB3232" stroke-width="8" stroke-linecap="round"/>
  <path d="M1130 263 L1185 253" fill="none" stroke="#EB3232" stroke-width="8" stroke-linecap="round"/>
  <path d="M1087 176 L1094 126" fill="none" stroke="#EB3232" stroke-width="8" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for paper grain or film-strip repetition; make the texture and sprocket holes from explicit editable paths/rectangles.
- ❌ Do not use `marker-end` for doodle arrows; draw the arrow shaft as a path and the arrowhead as a separate filled path.
- ❌ Do not clip or mask text/shapes to create rough edges; use slightly irregular path geometry instead.
- ❌ Do not overuse photographic assets; the style should feel flat, diagrammatic, and whiteboard-native.
- ❌ Do not make all text small and uniform; this style depends on poster-like hierarchy and very large keywords.

## Composition notes
- Keep the left 55–60% for narrative text: pain points at the top, oversized promise in the middle, small supporting explanation below.
- Use the right 35–40% for one dominant doodle icon so the slide has a clear visual anchor.
- Reserve generous white space; the doodle aesthetic works best when each visual bite has breathing room.
- Use red only for “problem / strikeout / attention” and green only for “solution / progress / positive outcome.”