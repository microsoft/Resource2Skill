# SVG Recipe — Corporate Process Timeline

## Visual mechanism
A clean vertical axis on the right organizes sequential process steps, with numbered circular nodes acting as anchors for concise text blocks. A sculptural segmented ring in the lower-left balances the composition and adds a premium corporate accent without competing with the timeline.

## SVG primitives needed
- 1× `<rect>` for the white slide background.
- 1× narrow `<rect>` for the vertical timeline axis.
- 4× `<circle>` for dark numbered process nodes.
- 4× `<circle>` for small red accent dots on the axis.
- 4× `<rect>` for subtle rounded content cards behind each process item.
- 4× `<line>` for fine connector rules from text cards to the timeline.
- 4× `<text>` for numbered node labels.
- 4× `<text>` with nested `<tspan>` for step headings and descriptions.
- 1× `<text>` for the main title.
- 10× `<path>` for the segmented 3D ring: blue/red arc segments, depth offsets, and angular cap pieces.
- 2× `<linearGradient>` for polished blue and red ring surfaces.
- 1× `<radialGradient>` for the soft background glow behind the ring.
- 2× `<filter>` definitions: soft drop shadow for cards/nodes/ring and a blur glow for the decorative base.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueSurface" x1="60" y1="430" x2="300" y2="675" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#49A0FF"/>
      <stop offset="0.48" stop-color="#2162DE"/>
      <stop offset="1" stop-color="#123E9A"/>
    </linearGradient>
    <linearGradient id="redSurface" x1="65" y1="445" x2="245" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF6B6B"/>
      <stop offset="0.55" stop-color="#ED1C24"/>
      <stop offset="1" stop-color="#A90F17"/>
    </linearGradient>
    <radialGradient id="ringGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#2162DE" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#2162DE" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <ellipse cx="178" cy="560" rx="170" ry="110" fill="url(#ringGlow)" filter="url(#glow)"/>

  <path d="M92 600 A122 122 0 0 1 80 493" fill="none" stroke="#102D73" stroke-width="50" stroke-linecap="butt" opacity="0.45"/>
  <path d="M111 444 A122 122 0 0 1 207 409" fill="none" stroke="#102D73" stroke-width="50" stroke-linecap="butt" opacity="0.45"/>
  <path d="M259 438 A122 122 0 0 1 299 527" fill="none" stroke="#102D73" stroke-width="50" stroke-linecap="butt" opacity="0.45"/>
  <path d="M274 594 A122 122 0 0 1 180 660" fill="none" stroke="#102D73" stroke-width="50" stroke-linecap="butt" opacity="0.45"/>

  <path d="M75 584 A122 122 0 0 1 63 477" fill="none" stroke="url(#redSurface)" stroke-width="50" stroke-linecap="butt" filter="url(#softShadow)"/>
  <path d="M94 428 A122 122 0 0 1 190 393" fill="none" stroke="url(#blueSurface)" stroke-width="50" stroke-linecap="butt" filter="url(#softShadow)"/>
  <path d="M242 422 A122 122 0 0 1 282 511" fill="none" stroke="url(#blueSurface)" stroke-width="50" stroke-linecap="butt" filter="url(#softShadow)"/>
  <path d="M257 578 A122 122 0 0 1 163 644" fill="none" stroke="url(#blueSurface)" stroke-width="50" stroke-linecap="butt" filter="url(#softShadow)"/>
  <path d="M51 477 L76 459 L111 488 L84 508 Z" fill="#B9151C"/>
  <path d="M52 587 L83 573 L109 610 L75 626 Z" fill="#D71920"/>

  <text x="144" y="96" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800" fill="#333333" letter-spacing="2">WHY US</text>
  <rect x="144" y="116" width="78" height="5" rx="2.5" fill="#ED1C24"/>
  <text x="144" y="152" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#6B6B6B">
    A clear operating model for confident delivery.
  </text>

  <rect x="910" y="128" width="3" height="450" rx="1.5" fill="#595959"/>
  <circle cx="911.5" cy="128" r="5" fill="#595959"/>
  <circle cx="911.5" cy="578" r="5" fill="#595959"/>

  <rect x="418" y="145" width="410" height="70" rx="18" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <line x1="828" y1="180" x2="880" y2="180" stroke="#BDBDBD" stroke-width="1.5"/>
  <circle cx="911.5" cy="180" r="31" fill="#404040" filter="url(#softShadow)"/>
  <circle cx="880" cy="180" r="6" fill="#ED1C24"/>
  <text x="894" y="191" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">1</text>
  <text x="446" y="173" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#555555">
    <tspan x="446" dy="0" font-weight="700" fill="#333333">Deep presentation craft</tspan>
    <tspan x="446" dy="24">Experienced design team for executive-ready slides.</tspan>
  </text>

  <rect x="418" y="255" width="410" height="70" rx="18" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <line x1="828" y1="290" x2="880" y2="290" stroke="#BDBDBD" stroke-width="1.5"/>
  <circle cx="911.5" cy="290" r="31" fill="#404040" filter="url(#softShadow)"/>
  <circle cx="880" cy="290" r="6" fill="#ED1C24"/>
  <text x="894" y="301" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">2</text>
  <text x="446" y="283" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#555555">
    <tspan x="446" dy="0" font-weight="700" fill="#333333">Fast turnaround rhythm</tspan>
    <tspan x="446" dy="24">Structured reviews keep delivery moving quickly.</tspan>
  </text>

  <rect x="418" y="365" width="410" height="70" rx="18" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <line x1="828" y1="400" x2="880" y2="400" stroke="#BDBDBD" stroke-width="1.5"/>
  <circle cx="911.5" cy="400" r="31" fill="#404040" filter="url(#softShadow)"/>
  <circle cx="880" cy="400" r="6" fill="#ED1C24"/>
  <text x="894" y="411" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">3</text>
  <text x="446" y="393" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#555555">
    <tspan x="446" dy="0" font-weight="700" fill="#333333">Satisfaction guarantee</tspan>
    <tspan x="446" dy="24">Clear checkpoints ensure the final deck lands.</tspan>
  </text>

  <rect x="418" y="475" width="410" height="70" rx="18" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <line x1="828" y1="510" x2="880" y2="510" stroke="#BDBDBD" stroke-width="1.5"/>
  <circle cx="911.5" cy="510" r="31" fill="#404040" filter="url(#softShadow)"/>
  <circle cx="880" cy="510" r="6" fill="#ED1C24"/>
  <text x="894" y="521" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">4</text>
  <text x="446" y="503" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#555555">
    <tspan x="446" dy="0" font-weight="700" fill="#333333">Motion-ready storytelling</tspan>
    <tspan x="446" dy="24">Slides can be enhanced with transitions and video.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the timeline with grouped arrow markers; `marker-end` on paths is unreliable, and this layout does not need arrowheads.
- ❌ Do not use `<mask>` to fake the segmented ring; use explicit stroked `<path>` arc segments instead.
- ❌ Do not place text without `width`; timeline copy will reflow unpredictably in PowerPoint.
- ❌ Do not clip non-image shapes for the cards or ring; clipping only translates reliably on `<image>` elements.
- ❌ Avoid overly dense step text. The technique works best with short, executive-summary phrasing.

## Composition notes
- Keep the vertical axis around 70–72% of slide width, leaving the central-left area for step copy and the far-left lower corner for the decorative ring.
- Use one strong accent color, usually red, only for small dots, title underline, and one ring segment.
- Preserve generous white space above and around the timeline; the thin axis should feel precise, not crowded.
- The decorative ring should be visually heavy but peripheral, balancing the timeline rather than becoming the main reading path.