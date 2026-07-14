# SVG Recipe — Hero with Top Accent

## Visual mechanism
A quiet left-side typography zone is balanced by a large clipped hero photo anchored bottom-right, while a bold organic accent shape spills in from the top-right corner. The accent establishes energy and brand color without competing with the headline.

## SVG primitives needed
- 1× `<rect>` for the soft full-slide background.
- 2× `<path>` for organic top-right accent shapes.
- 1× `<path>` for the hero-image halo / backing shape.
- 1× `<clipPath>` with a custom `<path>` for the irregular rounded hero-photo crop.
- 1× `<image>` clipped into the hero shape.
- 5× `<circle>` / `<ellipse>` for playful top accent dots and depth cues.
- 2× `<rect>` for small pill labels / UI-like accent chips.
- 3× `<text>` blocks with explicit `width` for eyebrow, headline, and subhead.
- 1× `<path>` for the hand-drawn underline stroke under the headline.
- 2× `<filter>` definitions: one soft shadow for raised objects, one glow for accent elements.
- 4× `<linearGradient>` / `<radialGradient>` definitions for background, accent, halo, and dots.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF8ED"/>
      <stop offset="54%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EEF5FF"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="850" y1="-30" x2="1280" y2="220" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFB84D"/>
      <stop offset="55%" stop-color="#FF6B4A"/>
      <stop offset="100%" stop-color="#E8347D"/>
    </linearGradient>

    <linearGradient id="heroHaloGrad" x1="730" y1="230" x2="1160" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFD867"/>
      <stop offset="48%" stop-color="#FF7C55"/>
      <stop offset="100%" stop-color="#7B61FF"/>
    </linearGradient>

    <radialGradient id="dotGrad" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.35"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.10  0 0 0 0 0.12  0 0 0 0 0.18  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <path d="M842 224 C936 175 1074 205 1131 310 C1199 436 1133 590 1000 637 C881 679 748 620 727 493 C703 348 750 272 842 224 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M872 0 H1280 V198 C1228 182 1199 145 1167 113 C1111 58 1044 88 995 73 C948 59 928 23 872 0 Z"
        fill="url(#accentGrad)" filter="url(#accentGlow)"/>

  <path d="M1030 0 C1085 42 1160 60 1280 54 V0 Z"
        fill="#FFFFFF" opacity="0.24"/>

  <circle cx="1128" cy="72" r="12" fill="url(#dotGrad)" opacity="0.95"/>
  <circle cx="1197" cy="128" r="7" fill="url(#dotGrad)" opacity="0.75"/>
  <circle cx="1062" cy="132" r="5" fill="#FFFFFF" opacity="0.68"/>
  <ellipse cx="1230" cy="42" rx="22" ry="9" fill="#FFFFFF" opacity="0.22" transform="rotate(-19 1230 42)"/>

  <rect x="104" y="102" width="148" height="34" rx="17" fill="#15213B" opacity="0.08"/>
  <text x="124" y="125" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.4" fill="#5E6B82">
    STRATEGY MOTION
  </text>

  <text x="104" y="226" width="555" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#18233E">
    <tspan x="104" dy="0">Motion Paths</tspan>
    <tspan x="104" dy="66">That Make</tspan>
    <tspan x="104" dy="66">Strategy Feel Alive</tspan>
  </text>

  <path d="M107 429 C172 415 248 418 319 410 C373 404 421 393 482 399"
        fill="none" stroke="#FF7A4F" stroke-width="10" stroke-linecap="round" opacity="0.92"/>

  <text x="108" y="486" width="485" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="400" fill="#536176">
    <tspan x="108" dy="0">Use one memorable visual action to introduce</tspan>
    <tspan x="108" dy="33">a section, keynote theme, or product story.</tspan>
  </text>

  <rect x="108" y="574" width="186" height="48" rx="24" fill="#18233E" filter="url(#softShadow)"/>
  <text x="137" y="605" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#FFFFFF">
    START THE STORY
  </text>

  <path d="M824 214 C926 154 1087 190 1152 298 C1230 428 1151 608 1008 662 C871 714 715 640 691 498 C666 346 724 274 824 214 Z"
        fill="url(#heroHaloGrad)" opacity="0.96" filter="url(#softShadow)"/>

  <image x="700" y="165" width="500" height="520"
         href="https://images.example.com/hero-speaker-with-colorful-motion-trails.jpg"
         clip-path="url(#heroClip)" preserveAspectRatio="xMidYMid slice"/>

  <path d="M755 256 C816 213 914 201 1010 230"
        fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.62"/>

  <circle cx="734" cy="592" r="38" fill="#FFFFFF" opacity="0.86" filter="url(#softShadow)"/>
  <circle cx="734" cy="592" r="18" fill="#FF7A4F"/>
  <circle cx="734" cy="592" r="7" fill="#FFFFFF"/>

  <rect x="914" y="603" width="206" height="54" rx="27" fill="#FFFFFF" opacity="0.94" filter="url(#softShadow)"/>
  <text x="943" y="637" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#24304B">
    01 / SECTION OPENER
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the hero image; use an image clipped by `<clipPath>` and separate translucent shapes instead.
- ❌ Do not apply `clip-path` to decorative paths or rectangles; clipping is reliable here only on the `<image>`.
- ❌ Do not rely on `marker-end` arrows for motion cues; use simple stroked paths or lines without markers.
- ❌ Do not overcrowd the left side with charts or cards; the technique depends on a clean editorial text zone.

## Composition notes
- Keep the headline left-aligned in the left 45–50% of the canvas, with generous line spacing and no competing imagery behind it.
- Let the hero image occupy the lower-right quadrant and slightly overlap the slide edge for a keynote-cover feel.
- The top-right accent should be large enough to be unmistakable but should not descend into the headline area.
- Repeat the accent color once or twice in small details, such as the underline, dot, or CTA, to unify the slide.