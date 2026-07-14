# SVG Recipe — Monochrome Corporate Node Panels

## Visual mechanism
A restrained taupe canvas carries a low-contrast world map silhouette, overlaid with three oversized circular “node panels.” The center node is emphasized as a dark active hub with concentric rings, a white status dot, and a label, while pale side nodes imply inactive regions.

## SVG primitives needed
- 2× `<rect>` for the warm monochrome background and dark footer band
- 10–14× `<path>` for abstract continent silhouettes and decorative map fragments
- 6× `<circle>` for large node panels, status dots, concentric active-node rings, and the footer page tab
- 1× `<line>` for the small title divider
- 4× `<text>` for title, subtitle, center-node label, and footer page number
- 2× `<filter>` with `feOffset` + `feGaussianBlur` + `feMerge` for subtle node depth
- 1× `<radialGradient>` for the active center node fill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="activeNode" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#25252b"/>
      <stop offset="70%" stop-color="#181820"/>
      <stop offset="100%" stop-color="#101017"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="microGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- warm monochrome base -->
  <rect x="0" y="0" width="1280" height="720" fill="#d8d1c8"/>

  <!-- abstract world map silhouette -->
  <g fill="#b8ad96" opacity="0.78">
    <path d="M90 225 L120 218 L170 230 L215 220 L255 230 L275 255 L248 272 L205 263 L180 282 L130 268 L100 285 L112 262 L88 257 L112 244 Z"/>
    <path d="M310 162 L362 140 L418 145 L397 168 L363 166 L345 184 L322 176 L338 164 Z"/>
    <path d="M395 146 L487 137 L565 148 L542 190 L515 244 L475 276 L450 224 L416 195 L386 182 Z"/>
    <path d="M222 188 L245 180 L255 192 L275 184 L290 203 L250 211 L230 205 Z"/>
    <path d="M450 465 L522 492 L509 552 L475 565 L432 545 L420 500 Z"/>
    <path d="M430 548 L418 625 L396 650 L405 682 L390 673 L377 638 L383 586 Z"/>
    <path d="M775 214 L795 190 L820 184 L803 203 L805 225 Z"/>
    <path d="M838 210 L895 211 L925 186 L940 181 L938 205 L1015 207 L1070 214 L1120 210 L1188 230 L1192 266 L1140 256 L1112 278 L1076 264 L1030 286 L985 275 L930 283 L885 265 L846 270 Z"/>
    <path d="M646 474 L707 492 L736 530 L723 587 L690 604 L671 560 L648 540 Z"/>
    <path d="M748 539 L766 528 L761 559 L747 572 Z"/>
    <path d="M972 559 L1005 542 L1055 558 L1080 600 L1052 615 L1005 594 L964 613 Z"/>
    <path d="M1138 642 L1163 613 L1182 620 L1158 648 Z"/>
  </g>

  <!-- header typography -->
  <text x="640" y="93" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="300"
        fill="#54514f">Our global reach</text>
  <text x="640" y="127" width="320" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="300"
        fill="#706b68">overview</text>
  <line x1="594" y1="146" x2="686" y2="146" stroke="#4b4b55" stroke-width="5"/>

  <!-- left inactive node -->
  <circle cx="292" cy="370" r="160" fill="#f7f6f2" opacity="0.86" filter="url(#softShadow)"/>
  <g fill="#ffffff" opacity="0.35">
    <path d="M162 272 L216 245 L276 257 L318 290 L304 326 L246 324 L226 350 L177 338 Z"/>
    <path d="M315 390 L352 407 L373 443 L338 467 L302 447 Z"/>
    <path d="M220 440 L265 458 L275 506 L245 518 L218 487 Z"/>
  </g>
  <circle cx="292" cy="294" r="29" fill="#9da0a7"/>

  <!-- center active node -->
  <circle cx="640" cy="371" r="168" fill="#292930" opacity="0.96" filter="url(#softShadow)"/>
  <circle cx="640" cy="371" r="151" fill="url(#activeNode)" stroke="#30303a" stroke-width="12"/>
  <g fill="#313139" opacity="0.62">
    <path d="M545 275 L592 248 L642 252 L680 266 L710 258 L728 274 L693 300 L642 294 L616 322 L568 318 Z"/>
    <path d="M514 336 L566 312 L608 330 L612 374 L578 401 L526 388 Z"/>
    <path d="M617 392 L660 382 L706 399 L718 440 L693 472 L646 470 L628 437 Z"/>
    <path d="M716 336 L752 346 L771 376 L749 404 L711 392 Z"/>
    <path d="M558 452 L606 460 L640 494 L602 500 L560 486 Z"/>
  </g>
  <circle cx="640" cy="294" r="29" fill="#ffffff" filter="url(#microGlow)"/>
  <text x="640" y="366" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="400"
        letter-spacing="1" fill="#ffffff">CONTACT</text>

  <!-- right inactive node -->
  <circle cx="988" cy="370" r="160" fill="#f7f6f2" opacity="0.86" filter="url(#softShadow)"/>
  <g fill="#ffffff" opacity="0.35">
    <path d="M907 280 L958 255 L1010 270 L1037 308 L1006 332 L951 319 Z"/>
    <path d="M1015 365 L1058 376 L1083 414 L1051 448 L1008 431 Z"/>
    <path d="M905 438 L944 462 L948 500 L915 512 L890 478 Z"/>
    <path d="M1070 470 L1112 492 L1092 523 L1052 505 Z"/>
  </g>
  <circle cx="984" cy="294" r="29" fill="#9da0a7"/>

  <!-- bottom footer and centered page node -->
  <rect x="0" y="692" width="1280" height="28" fill="#26262d"/>
  <circle cx="640" cy="704" r="48" fill="#26262d"/>
  <text x="640" y="692" width="80" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#ffffff">13</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for the world map texture; draw simplified editable `<path>` silhouettes instead.
- ❌ Do not use clipping or masks on circles to crop map shapes; the translator ignores `clip-path` on non-image elements.
- ❌ Do not overuse saturated color accents; the premium effect depends on taupe, charcoal, white, and gray restraint.
- ❌ Do not place heavy explanatory body copy inside the circles; this layout works best as a navigation, reach, or node-status visual.

## Composition notes
- Keep the title centered in the top 15–20% of the slide with generous letter spacing and a thin divider.
- Let the world map sit behind the nodes at low contrast; it should provide context, not compete with the circles.
- Make the center node the only dark, high-contrast object so the viewer immediately reads it as the active selection.
- Use the bottom footer band and small centered tab as a grounding device; it balances the large circular geometry above.