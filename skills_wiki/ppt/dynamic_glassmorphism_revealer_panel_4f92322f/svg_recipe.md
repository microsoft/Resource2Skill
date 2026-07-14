# SVG Recipe — Dynamic Glassmorphism Revealer Panel

## Visual mechanism
A sharp full-slide hero image sits above a perfectly aligned blurred duplicate that is visible only through a large rounded “glass” panel. Semi-transparent gradient borders, glossy highlights, soft shadows, and subtle motion ghosts make the panel feel like a draggable frosted revealer moving across the scene.

## SVG primitives needed
- 1× full-slide `<image>` for the sharp hero background
- 1× clipped full-slide `<image>` for the blurred version revealed only inside the glass panel
- 1× `<clipPath>` with rounded `<rect>` defining the frosted panel crop
- 3× translucent `<rect>` for offset motion-ghost panels behind the main revealer
- 2× large `<rect>` overlays for dark vignette and contrast management
- 1× main rounded `<rect>` with gradient stroke/fill for the glass surface
- 3× thin rounded `<rect>` highlights for glossy top/side reflections
- 1× `<filter id="panelShadow">` applied to rounded rectangles for premium depth
- 1× `<filter id="textShadow">` applied to text for legibility over the blur
- 1× `<linearGradient>` for the glass edge highlight
- 1× `<radialGradient>` for subtle environmental glow overlays
- 4× `<text>` elements with explicit `width` attributes for title, eyebrow, body copy, and small UI label
- 2× `<circle>` UI dots and 1× `<rect>` drag pill to imply interactive movement
- 1× `<path>` chevron/arrow glyph drawn manually, avoiding marker-based arrows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="glassClip">
      <rect x="260" y="130" width="760" height="430" rx="44" ry="44"/>
    </clipPath>

    <linearGradient id="darkVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.10"/>
      <stop offset="55%" stop-color="#020617" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.48"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="260" y1="130" x2="1020" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="38%" stop-color="#FFFFFF" stop-opacity="0.12"/>
      <stop offset="72%" stop-color="#BDEBFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.20"/>
    </linearGradient>

    <linearGradient id="glassStroke" x1="260" y1="130" x2="1020" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="20%" stop-color="#FFFFFF" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#8AE5FF" stop-opacity="0.16"/>
      <stop offset="82%" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.72"/>
    </linearGradient>

    <radialGradient id="panelGlow" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#9BE7FF" stop-opacity="0.26"/>
      <stop offset="58%" stop-color="#7C3AED" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-25%" width="140%" height="150%">
      <feOffset dx="0" dy="26" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>

    <filter id="textShadow" x="-8%" y="-20%" width="116%" height="150%">
      <feOffset dx="0" dy="3" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#07111F"/>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/abstract-dark-flowing-neon-glass-background-sharp.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkVignette)"/>
  <ellipse cx="930" cy="150" rx="300" ry="210" fill="url(#panelGlow)" filter="url(#softGlow)" opacity="0.75"/>
  <ellipse cx="290" cy="585" rx="260" ry="150" fill="#00E5FF" opacity="0.09" filter="url(#softGlow)"/>

  <rect x="220" y="166" width="760" height="430" rx="44" ry="44"
        fill="#FFFFFF" opacity="0.055" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1.2"/>
  <rect x="240" y="148" width="760" height="430" rx="44" ry="44"
        fill="#FFFFFF" opacity="0.075" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.2"/>
  <rect x="255" y="134" width="760" height="430" rx="44" ry="44"
        fill="#FFFFFF" opacity="0.10" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="1.2"/>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/abstract-dark-flowing-neon-glass-background-blurred-35px.jpg"
         clip-path="url(#glassClip)"/>

  <rect x="260" y="130" width="760" height="430" rx="44" ry="44"
        fill="url(#glassFill)" stroke="url(#glassStroke)" stroke-width="2.4" filter="url(#panelShadow)"/>

  <rect x="287" y="154" width="706" height="2.8" rx="1.4" fill="#FFFFFF" opacity="0.58"/>
  <rect x="287" y="158" width="270" height="1.4" rx="0.7" fill="#FFFFFF" opacity="0.24"/>
  <rect x="287" y="168" width="2.4" height="350" rx="1.2" fill="#FFFFFF" opacity="0.22"/>
  <rect x="969" y="188" width="2.2" height="180" rx="1.1" fill="#B7F6FF" opacity="0.28"/>

  <rect x="300" y="168" width="112" height="32" rx="16" fill="#020617" opacity="0.30" stroke="#FFFFFF" stroke-opacity="0.22"/>
  <circle cx="325" cy="184" r="5.5" fill="#70F0FF" opacity="0.95"/>
  <circle cx="347" cy="184" r="5.5" fill="#FFFFFF" opacity="0.55"/>
  <text x="370" y="190" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" letter-spacing="1.8" fill="#FFFFFF" opacity="0.78">LIVE REVEAL</text>

  <text x="330" y="284" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3.5" fill="#C8F7FF" opacity="0.92" filter="url(#textShadow)">
    DYNAMIC GLASS PANEL
  </text>

  <text x="330" y="352" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64" font-weight="750" fill="#FFFFFF" filter="url(#textShadow)">
    Reveal the signal
  </text>

  <text x="334" y="405" width="575" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" line-height="1.25" fill="#EAF8FF" opacity="0.88" filter="url(#textShadow)">
    Frosted blur follows the panel, suppressing background noise while preserving color depth and premium motion.
  </text>

  <rect x="784" y="480" width="172" height="44" rx="22" fill="#FFFFFF" opacity="0.16" stroke="#FFFFFF" stroke-opacity="0.32"/>
  <text x="812" y="508" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#FFFFFF" opacity="0.92">DRAG PANEL</text>
  <path d="M928 495 L944 502 L928 509 L932 503 L900 503 L900 501 L932 501 Z"
        fill="#FFFFFF" opacity="0.88"/>

  <text x="60" y="660" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="500" fill="#FFFFFF" opacity="0.45">
    Use the blurred duplicate only inside the panel crop; keep it perfectly aligned with the sharp background.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the revealer motion; create motion ghosts or duplicate slides instead.
- ❌ `<mask>` for the frosted panel crop; use `clipPath` applied only to the blurred `<image>`.
- ❌ Applying `filter` blur directly to an `<image>`; use a pre-blurred duplicate image asset for reliable PowerPoint translation.
- ❌ `clip-path` on the glass `<rect>` or text; clipping is only reliable here on the blurred image layer.
- ❌ `marker-end` arrows for the drag cue; draw arrowheads manually with a small `<path>`.

## Composition notes
- Keep the glass panel large, about 60–70% of slide width, so the blur reads as a deliberate reveal rather than a small overlay.
- The sharp background should remain visible around all panel edges; this contrast is what sells the frosted-glass illusion.
- Put the strongest text in the center-left of the panel, leaving the right side for interaction cues, highlights, or UI metadata.
- Use mostly white, cyan, and very low-opacity fills; the background image should provide the real color complexity.