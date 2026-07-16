# SVG Recipe — Offset Diagonal-Corner Process Cards

## Visual mechanism
Three elongated process cards use a custom diagonal-corner silhouette: rounded top-left and bottom-right, sharp top-right and bottom-left. Each bright neon foreground card is paired with a darker duplicate offset down-left, creating crisp pseudo-3D depth against a dark “tech keynote” canvas.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background.
- 3× `<ellipse>` for soft colored ambient glow behind each card cluster.
- 6× `<path>` for the diagonal-corner cards: 3 darker offset backing cards and 3 neon foreground cards.
- 3× `<path>` for thin inner highlight strokes on the foreground cards.
- 8× `<line>` for subtle background circuit/grid accents.
- 1× `<text>` for the slide eyebrow label.
- 1× `<text>` for the main title.
- 3× `<text>` for oversized step numbers.
- 3× `<text>` for card titles.
- 3× `<text>` for card descriptions.
- 3× `<linearGradient>` for neon foreground fills.
- 3× `<linearGradient>` for darker offset backing fills.
- 1× `<filter id="softGlow">` applied to ambient ellipses.
- 1× `<filter id="cardGlow">` applied to foreground card paths for a restrained neon edge glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="greenFront" x1="260" y1="110" x2="1060" y2="240" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#00ff9d"/>
      <stop offset="0.55" stop-color="#31ffbf"/>
      <stop offset="1" stop-color="#00d46f"/>
    </linearGradient>
    <linearGradient id="blueFront" x1="310" y1="300" x2="1110" y2="430" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#3d7cff"/>
      <stop offset="0.55" stop-color="#52a0ff"/>
      <stop offset="1" stop-color="#1d43ff"/>
    </linearGradient>
    <linearGradient id="redFront" x1="260" y1="490" x2="1060" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff4343"/>
      <stop offset="0.55" stop-color="#ff6b58"/>
      <stop offset="1" stop-color="#df1f2f"/>
    </linearGradient>

    <linearGradient id="greenBack" x1="235" y1="128" x2="1035" y2="258" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#005c34"/>
      <stop offset="1" stop-color="#002d20"/>
    </linearGradient>
    <linearGradient id="blueBack" x1="285" y1="318" x2="1085" y2="448" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172b87"/>
      <stop offset="1" stop-color="#091447"/>
    </linearGradient>
    <linearGradient id="redBack" x1="235" y1="508" x2="1035" y2="638" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7a151e"/>
      <stop offset="1" stop-color="#3a0710"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <filter id="cardGlow" x="-8%" y="-18%" width="116%" height="136%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0b0b10"/>

  <line x1="84" y1="118" x2="210" y2="118" stroke="#202636" stroke-width="2"/>
  <line x1="84" y1="118" x2="84" y2="228" stroke="#202636" stroke-width="2"/>
  <line x1="1108" y1="92" x2="1192" y2="92" stroke="#202636" stroke-width="2"/>
  <line x1="1192" y1="92" x2="1192" y2="190" stroke="#202636" stroke-width="2"/>
  <line x1="86" y1="618" x2="190" y2="618" stroke="#202636" stroke-width="2"/>
  <line x1="190" y1="618" x2="190" y2="662" stroke="#202636" stroke-width="2"/>
  <line x1="1110" y1="604" x2="1210" y2="604" stroke="#202636" stroke-width="2"/>
  <line x1="1110" y1="604" x2="1110" y2="650" stroke="#202636" stroke-width="2"/>

  <ellipse cx="630" cy="180" rx="430" ry="88" fill="#00ff9d" opacity="0.12" filter="url(#softGlow)"/>
  <ellipse cx="680" cy="370" rx="430" ry="88" fill="#3d7cff" opacity="0.13" filter="url(#softGlow)"/>
  <ellipse cx="630" cy="560" rx="430" ry="88" fill="#ff4343" opacity="0.11" filter="url(#softGlow)"/>

  <text x="112" y="70" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="3" fill="#7f8aa3">PROCESS MAP / DARK MODE</text>
  <text x="112" y="116" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#f4f7ff">Launch sequence in three moves</text>

  <path d="M 286 150 H 1060 V 236 Q 1060 276 1020 276 H 246 V 190 Q 246 150 286 150 Z" fill="url(#greenBack)"/>
  <path d="M 312 126 H 1086 V 212 Q 1086 252 1046 252 H 272 V 166 Q 272 126 312 126 Z" fill="url(#greenFront)" filter="url(#cardGlow)"/>
  <path d="M 334 146 H 1054 V 205 Q 1054 228 1031 228 H 295" fill="none" stroke="#d8fff0" stroke-width="2" opacity="0.55"/>

  <text x="310" y="218" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="80" font-weight="900" fill="#06110d" opacity="0.42">01.</text>
  <text x="505" y="172" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#07110d">Discover the signal</text>
  <text x="506" y="207" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="500" fill="#082018" opacity="0.9">Capture customer intent, technical constraints, and success metrics before committing to the build path.</text>

  <path d="M 336 340 H 1110 V 426 Q 1110 466 1070 466 H 296 V 380 Q 296 340 336 340 Z" fill="url(#blueBack)"/>
  <path d="M 362 316 H 1136 V 402 Q 1136 442 1096 442 H 322 V 356 Q 322 316 362 316 Z" fill="url(#blueFront)" filter="url(#cardGlow)"/>
  <path d="M 384 336 H 1104 V 395 Q 1104 418 1081 418 H 345" fill="none" stroke="#e6f0ff" stroke-width="2" opacity="0.5"/>

  <text x="360" y="408" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="80" font-weight="900" fill="#06102e" opacity="0.42">02.</text>
  <text x="555" y="362" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#06102e">Engineer the system</text>
  <text x="556" y="397" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="500" fill="#081a45" opacity="0.9">Convert the strategy into modular workflows, automated checkpoints, and a resilient operating model.</text>

  <path d="M 286 530 H 1060 V 616 Q 1060 656 1020 656 H 246 V 570 Q 246 530 286 530 Z" fill="url(#redBack)"/>
  <path d="M 312 506 H 1086 V 592 Q 1086 632 1046 632 H 272 V 546 Q 272 506 312 506 Z" fill="url(#redFront)" filter="url(#cardGlow)"/>
  <path d="M 334 526 H 1054 V 585 Q 1054 608 1031 608 H 295" fill="none" stroke="#ffe0dd" stroke-width="2" opacity="0.48"/>

  <text x="310" y="598" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="80" font-weight="900" fill="#2b0508" opacity="0.42">03.</text>
  <text x="505" y="552" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#270608">Scale the impact</text>
  <text x="506" y="587" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="500" fill="#3a080b" opacity="0.88">Roll out the operating cadence, measure adoption, and amplify the winning motions across teams.</text>
</svg>
```

## Avoid in this skill
- ❌ Using normal rounded `<rect>` cards only; the diagonal-corner silhouette is the signature of the technique, so build cards with `<path>`.
- ❌ Applying `filter` to `<line>` elements for glowing connectors; line filters are dropped, so keep circuit accents flat or use thin `<path>` shapes if glow is required.
- ❌ Using `<clipPath>` on card paths to fake corners; clipping non-image elements is ignored. Draw the card silhouette directly as a path.
- ❌ Overusing blur shadows under the cards; the style depends on crisp offset duplicate shapes, not soft generic drop shadows.
- ❌ Placing all cards perfectly aligned if you want more energy; a slight horizontal stagger between the middle card and the outer cards strengthens motion.

## Composition notes
- Keep the process stack centered vertically, with each card occupying about 60–70% of slide width and 16–18% of slide height.
- Reserve the left 20–25% of each card for the oversized number; put title and body copy in the remaining right zone.
- Use a dark off-black background with sparse circuit-line accents so the neon cards remain the visual focus.
- Repeat the same card geometry for every step, but vary neon color and slight horizontal offset to create rhythm without sacrificing readability.