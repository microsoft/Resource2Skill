# SVG Recipe — Radial Origami Infographic Pivot

## Visual mechanism
A tilted white presentation card carries a central origami-like circular hub made from overlapping gradient folds, then dotted radial connectors pivot outward to five labeled option nodes. Soft shadows, seafoam gradients, black dot anchors, and red title accents create a premium keynote-style “core-and-spoke” infographic.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep red gradient background.
- 2× large `<text>` elements for the keynote-style title treatment.
- 1× rotated `<rect>` for the white infographic card.
- 1× `<circle>` for the dark teal base hub.
- 4× `<line>` for subtle hub grid seams.
- 3× `<path>` for overlapping origami fold segments and folded flap geometry.
- 1× `<circle>` for the glowing inner hub disk.
- 1× large `<text>` for the central number.
- 5× dashed `<line>` connectors with direct `marker-end` arrowheads.
- 5× small `<circle>` anchor dots at the hub perimeter.
- 5× icon clusters made from `<line>`, `<circle>`, `<path>`, and small `<text>`.
- 5× option title `<text>` elements and 5× body copy `<text>` elements.
- 1× bottom-left card title `<text>` and 1× supporting paragraph `<text>`.
- 4× `<linearGradient>` / `<radialGradient>` definitions for background, card, hub, and folds.
- 3× `<filter>` definitions for card shadow, text shadow, and hub glow/shadow.
- 1× `<marker>` definition for dashed radial line arrowheads, applied directly to each `<line>`.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="bgRed" cx="50%" cy="38%" r="75%">
      <stop offset="0%" stop-color="#c61f23"/>
      <stop offset="58%" stop-color="#8c071d"/>
      <stop offset="100%" stop-color="#370013"/>
    </radialGradient>

    <linearGradient id="cardFill" x1="0" y1="250" x2="0" y2="650">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f2f2f2"/>
    </linearGradient>

    <linearGradient id="foldGreen" x1="510" y1="350" x2="700" y2="535">
      <stop offset="0%" stop-color="#dffbf0"/>
      <stop offset="45%" stop-color="#58d8aa"/>
      <stop offset="100%" stop-color="#239d85"/>
    </linearGradient>

    <linearGradient id="flapGrad" x1="520" y1="405" x2="620" y2="490">
      <stop offset="0%" stop-color="#f5fff9"/>
      <stop offset="100%" stop-color="#57cfa7"/>
    </linearGradient>

    <radialGradient id="hubGlow" cx="44%" cy="34%" r="70%">
      <stop offset="0%" stop-color="#e8fff8"/>
      <stop offset="45%" stop-color="#6be0b6"/>
      <stop offset="100%" stop-color="#2b6071"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-10%" y="-10%" width="130%" height="150%">
      <feOffset dx="0" dy="13"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softHubShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="9"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <marker id="dotArrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#202020"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRed)"/>

  <text x="42" y="138" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="148" font-weight="900" fill="#ffffff" letter-spacing="-7" filter="url(#textShadow)">BEST</text>
  <text x="42" y="250" width="900" font-family="Segoe UI, Microsoft YaHei" font-size="118" font-weight="900" fill="#ffffff" letter-spacing="-5" filter="url(#textShadow)">PowerPoint</text>

  <g transform="rotate(-18 560 450)">
    <rect x="128" y="245" width="855" height="400" rx="14" fill="url(#cardFill)" filter="url(#cardShadow)"/>

    <text x="230" y="582" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="300" fill="#e33a1f" letter-spacing="1">YOUR TITLE</text>
    <text x="235" y="618" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#333333">
      <tspan x="235" dy="0">Lorem ipsum dolor sit amet, consectetur</tspan>
      <tspan x="235" dy="17">adipiscing elit. Maecenas porttitor congue</tspan>
      <tspan x="235" dy="17">massa. Fusce posuere, magna sed pulvinar.</tspan>
    </text>

    <circle cx="610" cy="440" r="112" fill="#2b6071" filter="url(#softHubShadow)"/>
    <line x1="498" y1="440" x2="722" y2="440" stroke="#1f4b5b" stroke-width="2"/>
    <line x1="531" y1="361" x2="689" y2="519" stroke="#1f4b5b" stroke-width="2"/>
    <line x1="610" y1="328" x2="610" y2="552" stroke="#1f4b5b" stroke-width="2"/>
    <line x1="531" y1="519" x2="689" y2="361" stroke="#1f4b5b" stroke-width="2"/>

    <path d="M500 455 A112 112 0 0 1 706 377 Q662 417 628 456 Q590 501 565 548 Q525 520 510 490 Q500 470 500 455 Z" fill="url(#foldGreen)" filter="url(#softHubShadow)"/>
    <path d="M538 420 L596 397 L615 456 L558 478 Z" fill="url(#flapGrad)" filter="url(#softHubShadow)"/>
    <path d="M665 354 Q711 391 722 440 Q690 426 652 435 Q670 397 665 354 Z" fill="#eafdf6" opacity="0.85" filter="url(#softHubShadow)"/>

    <circle cx="610" cy="440" r="72" fill="url(#hubGlow)" opacity="0.88"/>
    <text x="570" y="490" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="92" font-weight="900" fill="#ffffff" transform="rotate(-16 610 450)">5</text>

    <circle cx="510" cy="440" r="5" fill="#202020"/>
    <circle cx="548" cy="358" r="5" fill="#202020"/>
    <circle cx="610" cy="328" r="5" fill="#202020"/>
    <circle cx="676" cy="360" r="5" fill="#202020"/>
    <circle cx="718" cy="440" r="5" fill="#202020"/>

    <line x1="510" y1="440" x2="365" y2="390" stroke="#202020" stroke-width="1.4" stroke-dasharray="5 5" marker-end="url(#dotArrow)"/>
    <line x1="548" y1="358" x2="500" y2="278" stroke="#202020" stroke-width="1.4" stroke-dasharray="5 5" marker-end="url(#dotArrow)"/>
    <line x1="610" y1="328" x2="610" y2="238" stroke="#202020" stroke-width="1.4" stroke-dasharray="5 5" marker-end="url(#dotArrow)"/>
    <line x1="676" y1="360" x2="760" y2="286" stroke="#202020" stroke-width="1.4" stroke-dasharray="5 5" marker-end="url(#dotArrow)"/>
    <line x1="718" y1="440" x2="848" y2="420" stroke="#202020" stroke-width="1.4" stroke-dasharray="5 5" marker-end="url(#dotArrow)"/>

    <circle cx="300" cy="346" r="13" fill="none" stroke="#202020" stroke-width="1.4"/>
    <circle cx="326" cy="370" r="13" fill="none" stroke="#202020" stroke-width="1.4"/>
    <line x1="311" y1="356" x2="316" y2="361" stroke="#202020" stroke-width="1.4"/>
    <text x="272" y="410" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#111111">OPTION 1</text>
    <text x="276" y="432" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="8.5" fill="#333333">
      <tspan x="276" dy="0">Lorem ipsum dolor sit amet,</tspan><tspan x="276" dy="11">consectetur adipiscing elit.</tspan><tspan x="276" dy="11">Maecenas porttitor congue.</tspan>
    </text>

    <path d="M447 268 L458 259 M447 259 L458 268 M431 284 L420 293 M420 284 L431 293 M439 253 L439 239 M452 285 L466 285 M427 253 L417 243 M461 276 L471 286" fill="none" stroke="#202020" stroke-width="1.5"/>
    <text x="420" y="323" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#111111">OPTION 2</text>
    <text x="424" y="345" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="8.5" fill="#333333">
      <tspan x="424" dy="0">Lorem ipsum dolor sit amet,</tspan><tspan x="424" dy="11">consectetur adipiscing elit.</tspan><tspan x="424" dy="11">Maecenas porttitor congue.</tspan>
    </text>

    <text x="585" y="235" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#202020">1010</text>
    <text x="585" y="255" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#202020">1010</text>
    <text x="585" y="275" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#202020">1010</text>
    <text x="570" y="308" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#111111">OPTION 3</text>
    <text x="574" y="330" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="8.5" fill="#333333">
      <tspan x="574" dy="0">Lorem ipsum dolor sit amet,</tspan><tspan x="574" dy="11">consectetur adipiscing elit.</tspan><tspan x="574" dy="11">Maecenas porttitor congue.</tspan>
    </text>

    <path d="M792 251 L775 300 L790 292 L798 310 L805 306 L797 288 L813 286 Z" fill="none" stroke="#202020" stroke-width="1.5"/>
    <text x="750" y="335" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#111111">OPTION 4</text>
    <text x="754" y="357" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="8.5" fill="#333333">
      <tspan x="754" dy="0">Lorem ipsum dolor sit amet,</tspan><tspan x="754" dy="11">consectetur adipiscing elit.</tspan><tspan x="754" dy="11">Maecenas porttitor congue.</tspan>
    </text>

    <text x="860" y="384" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="42" fill="#202020">₿</text>
    <text x="842" y="463" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#111111">OPTION 5</text>
    <text x="846" y="485" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="8.5" fill="#333333">
      <tspan x="846" dy="0">Lorem ipsum dolor sit amet,</tspan><tspan x="846" dy="11">consectetur adipiscing elit.</tspan><tspan x="846" dy="11">Maecenas porttitor congue.</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the origami hub shapes; use explicit circular/arc paths instead because clipping non-image elements may be ignored.
- ❌ Using `<path marker-end="...">` for arrow connectors; keep arrowheads on individual `<line>` elements only.
- ❌ Building the fold effect as one flattened image; separate editable circles and paths preserve PowerPoint editability.
- ❌ Overcrowding all five nodes equally around a full circle; this technique works best as a controlled upper semicircle or fan so the title area remains readable.
- ❌ Hard black shadows; use blurred offset filters with low visual weight for a premium paper-and-glass feel.

## Composition notes
- Keep the hub near the center of the card, not the slide; the surrounding slide can hold a bold title or brand color field.
- Reserve the lower-left card quadrant for the main title and paragraph so the radial nodes can breathe above and around the hub.
- Use black dots at hub contact points to make dashed connectors feel intentionally “pinned” to the central pivot.
- Limit the palette to deep teal, seafoam, white, charcoal, and one warm accent red/orange for a polished executive look.