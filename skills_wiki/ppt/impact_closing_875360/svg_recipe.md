# SVG Recipe — Impact Closing

## Visual mechanism
A full-bleed accent-color field is used as the entire slide, with one oversized centered closing phrase rendered in the “background” color for maximum inversion and impact. Subtle gradient lighting, diagonal paper-fold planes, and a restrained micro-caption add premium depth without distracting from the final word.

## SVG primitives needed
- 3× `<rect>` for full-slide accent background, soft radial spotlight overlay, and short closing underline
- 5× `<path>` for diagonal paper-fold facets and edge highlights
- 3× `<text>` for small setup caption, massive closing message, and tiny footer cue
- 1× `<linearGradient id="accentBg">` for the inverted accent background
- 1× `<radialGradient id="centerLight">` for the central illumination behind the word
- 3× `<linearGradient>` for fold highlight and shadow fills
- 1× `<filter id="wordGlow">` applied to the massive text
- 1× `<filter id="foldShadow">` applied to folded-paper facets

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentBg" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0B3B8F"/>
      <stop offset="0.46" stop-color="#1257D8"/>
      <stop offset="1" stop-color="#4A1FD6"/>
    </linearGradient>

    <radialGradient id="centerLight" cx="50%" cy="49%" r="58%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="0.48" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="foldLight" x1="80" y1="40" x2="520" y2="420" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.02"/>
    </linearGradient>

    <linearGradient id="foldDark" x1="760" y1="120" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#050B28" stop-opacity="0.00"/>
      <stop offset="1" stop-color="#050B28" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="edgeShine" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.36"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="wordGlow" x="-10%" y="-35%" width="120%" height="170%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="8" result="blur"/>
      <feOffset in="blur" dx="0" dy="8" result="offsetBlur"/>
      <feMerge>
        <feMergeNode in="offsetBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="foldShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#accentBg)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerLight)"/>

  <path d="M0,0 L392,0 C316,84 238,168 158,252 C104,309 52,363 0,413 Z"
        fill="url(#foldLight)" opacity="0.88" filter="url(#foldShadow)"/>

  <path d="M1280,720 L872,720 C938,636 1008,558 1080,486 C1148,418 1215,363 1280,320 Z"
        fill="url(#foldDark)" opacity="0.86" filter="url(#foldShadow)"/>

  <path d="M0,518 C170,440 292,342 420,190 C469,132 521,70 590,0 L682,0 C580,121 499,221 425,303 C300,442 170,542 0,616 Z"
        fill="#FFFFFF" opacity="0.055"/>

  <path d="M690,720 C802,604 912,502 1048,414 C1130,361 1206,327 1280,304 L1280,396 C1188,430 1102,480 1018,548 C950,603 886,662 826,720 Z"
        fill="#050B28" opacity="0.12"/>

  <path d="M178,547 C394,442 572,292 754,74"
        fill="none" stroke="url(#edgeShine)" stroke-width="2.5" stroke-linecap="round" opacity="0.42"/>

  <text x="640" y="214" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" letter-spacing="4"
        text-anchor="middle" fill="#F8FBFF" opacity="0.78">
    THIS IS WHERE WE
  </text>

  <text x="640" y="394" width="1120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="800" letter-spacing="-4"
        text-anchor="middle" fill="#F8FBFF" filter="url(#wordGlow)">
    MAKE IT REAL
  </text>

  <rect x="520" y="444" width="240" height="6" rx="3" fill="#F8FBFF" opacity="0.72"/>

  <text x="640" y="522" width="680"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" letter-spacing="1.6"
        text-anchor="middle" fill="#F8FBFF" opacity="0.62">
    THANK YOU
  </text>
</svg>
```

## Avoid in this skill
- ❌ Adding multiple content blocks, charts, or icons; the technique depends on one dominant closing phrase.
- ❌ Low-contrast text over the accent background; the closing message should use near-white or the deck background color.
- ❌ Busy photo backgrounds unless heavily simplified; visual noise weakens the impact of the final word.
- ❌ Using `<textPath>` for dramatic typography; keep the message as normal editable `<text>`.

## Composition notes
- Keep the main phrase centered and enormous, occupying roughly 55–70% of slide width.
- Use negative space generously; the background and folds should feel cinematic, not decorative-heavy.
- Place any setup caption above the word and any closing cue below it at low opacity.
- Let diagonal folds frame the message from corners, creating motion toward the center without competing with the text.