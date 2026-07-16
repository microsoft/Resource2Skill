# SVG Recipe — Perspective Photo Timeline

## Visual mechanism
A diagonal chain of photo-filled quadrilateral cards shrinks and rises across a dark stage, creating the illusion of a 3D roadmap receding into depth. Shadows, rim highlights, reflections, and perspective-shaped image clips make each milestone feel like a tangible floating object rather than a flat thumbnail.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark radial-gradient background
- 6× `<clipPath>` with `<path>` silhouettes to crop each timeline photo into a perspective card
- 6× `<image>` elements for the milestone photos, each clipped to its card shape
- 6× `<path>` elements for dark card bases / depth plates behind the photos
- 6× `<path>` elements for bright beveled rim strokes around each card
- 6× `<path>` elements with gradient fills for soft floor reflections
- 6× `<text>` elements for large year labels placed on or near the cards
- 6× `<text>` elements for short milestone captions
- 1× `<line>` dashed perspective guide running through the card sequence
- 2× `<filter>` definitions: one for card shadows and one for soft glow accents
- Multiple `<linearGradient>` and `<radialGradient>` definitions for background, reflections, bevels, and atmospheric lighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="52%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#1e335f"/>
      <stop offset="48%" stop-color="#111b38"/>
      <stop offset="100%" stop-color="#060914"/>
    </radialGradient>

    <linearGradient id="cardBevel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.88"/>
      <stop offset="42%" stop-color="#9fd6ff" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#1c5cff" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="reflection" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#79baff" stop-opacity="0.24"/>
      <stop offset="58%" stop-color="#234c8e" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#050913" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="guideGlow" x1="100" y1="560" x2="1110" y2="205">
      <stop offset="0%" stop-color="#3be7ff" stop-opacity="0.1"/>
      <stop offset="45%" stop-color="#9ed7ff" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="clip2019"><path d="M95 335 L310 285 L345 520 L120 585 Z"/></clipPath>
    <clipPath id="clip2020"><path d="M282 283 L470 246 L498 450 L304 505 Z"/></clipPath>
    <clipPath id="clip2021"><path d="M455 239 L620 210 L641 382 L474 432 Z"/></clipPath>
    <clipPath id="clip2022"><path d="M610 204 L755 184 L770 330 L626 374 Z"/></clipPath>
    <clipPath id="clip2023"><path d="M748 180 L875 166 L887 288 L762 326 Z"/></clipPath>
    <clipPath id="clip2024"><path d="M868 162 L980 153 L989 254 L881 286 Z"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <circle cx="855" cy="180" r="250" fill="#2a70ff" opacity="0.12" filter="url(#softGlow)"/>
  <circle cx="225" cy="520" r="180" fill="#00d7ff" opacity="0.10" filter="url(#softGlow)"/>

  <text x="72" y="96" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#ffffff">
    Product evolution timeline
  </text>
  <text x="74" y="130" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#a9bddc">
    Perspective photo cards create depth, sequence, and momentum across milestones.
  </text>

  <line x1="115" y1="560" x2="1080" y2="208" stroke="url(#guideGlow)" stroke-width="3" stroke-dasharray="9 14"/>

  <path d="M95 335 L310 285 L345 520 L120 585 Z" fill="#07101f" opacity="0.85" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="82" y="270" width="290" height="330" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2019)"/>
  <path d="M95 335 L310 285 L345 520 L120 585 Z" fill="none" stroke="url(#cardBevel)" stroke-width="4"/>
  <path d="M126 592 L348 526 L420 588 L184 662 Z" fill="url(#reflection)" opacity="0.75"/>
  <text x="130" y="389" width="170" transform="rotate(-13 130 389)" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#ffffff">2019</text>
  <text x="136" y="436" width="160" transform="rotate(-13 136 436)" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#d9ecff">Foundation</text>

  <path d="M282 283 L470 246 L498 450 L304 505 Z" fill="#07101f" opacity="0.82" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="270" y="228" width="248" height="292" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2020)"/>
  <path d="M282 283 L470 246 L498 450 L304 505 Z" fill="none" stroke="url(#cardBevel)" stroke-width="3.5"/>
  <path d="M306 512 L500 456 L560 506 L354 570 Z" fill="url(#reflection)" opacity="0.58"/>
  <text x="316" y="331" width="150" transform="rotate(-12 316 331)" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#ffffff">2020</text>
  <text x="321" y="371" width="150" transform="rotate(-12 321 371)" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#d9ecff">First launch</text>

  <path d="M455 239 L620 210 L641 382 L474 432 Z" fill="#07101f" opacity="0.8" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="442" y="196" width="218" height="250" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2021)"/>
  <path d="M455 239 L620 210 L641 382 L474 432 Z" fill="none" stroke="url(#cardBevel)" stroke-width="3"/>
  <path d="M476 438 L642 388 L695 431 L520 486 Z" fill="url(#reflection)" opacity="0.46"/>
  <text x="485" y="281" width="135" transform="rotate(-10 485 281)" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#ffffff">2021</text>
  <text x="489" y="316" width="130" transform="rotate(-10 489 316)" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#d9ecff">Scale-up</text>

  <path d="M610 204 L755 184 L770 330 L626 374 Z" fill="#07101f" opacity="0.78" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="598" y="174" width="190" height="210" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2022)"/>
  <path d="M610 204 L755 184 L770 330 L626 374 Z" fill="none" stroke="url(#cardBevel)" stroke-width="2.8"/>
  <path d="M628 380 L771 336 L815 372 L666 420 Z" fill="url(#reflection)" opacity="0.36"/>
  <text x="636" y="239" width="120" transform="rotate(-8 636 239)" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#ffffff">2022</text>
  <text x="639" y="270" width="116" transform="rotate(-8 639 270)" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#d9ecff">New markets</text>

  <path d="M748 180 L875 166 L887 288 L762 326 Z" fill="#07101f" opacity="0.76" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="736" y="155" width="168" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2023)"/>
  <path d="M748 180 L875 166 L887 288 L762 326 Z" fill="none" stroke="url(#cardBevel)" stroke-width="2.4"/>
  <path d="M764 331 L888 293 L924 323 L796 364 Z" fill="url(#reflection)" opacity="0.28"/>
  <text x="772" y="211" width="105" transform="rotate(-6 772 211)" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" fill="#ffffff">2023</text>
  <text x="774" y="238" width="102" transform="rotate(-6 774 238)" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#d9ecff">AI platform</text>

  <path d="M868 162 L980 153 L989 254 L881 286 Z" fill="#07101f" opacity="0.74" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="856" y="143" width="150" height="152" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2024)"/>
  <path d="M868 162 L980 153 L989 254 L881 286 Z" fill="none" stroke="url(#cardBevel)" stroke-width="2.2"/>
  <path d="M883 291 L990 260 L1020 285 L910 319 Z" fill="url(#reflection)" opacity="0.22"/>
  <text x="890" y="189" width="92" transform="rotate(-5 890 189)" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#ffffff">2024</text>
  <text x="892" y="213" width="88" transform="rotate(-5 892 213)" font-family="Segoe UI, Microsoft YaHei" font-size="10" font-weight="600" fill="#d9ecff">Global suite</text>

  <text x="865" y="626" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#8fa9cf">
    Cards get smaller, higher, and tighter as they recede.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` transforms to fake perspective; those transforms are not reliably translated.
- ❌ Do not apply `clip-path` to `<g>`, `<path>`, or `<rect>` elements; only clip the `<image>` elements.
- ❌ Do not use `<mask>` for reflection fades; use semi-transparent gradient-filled paths instead.
- ❌ Do not rely on PowerPoint-native 3D rotation metadata; build the perspective illusion directly with editable SVG paths.
- ❌ Do not use `marker-end` arrows for the timeline path; use a plain dashed `<line>` or custom path geometry.

## Composition notes
- Keep the card sequence inside the central 70–80% of the canvas, moving from lower-left foreground to upper-right background.
- Foreground cards should be larger, lower, brighter, and more widely spaced; distant cards should shrink, rise, and compress.
- Use a dark atmospheric background so photo edges, bevel strokes, and white date labels read clearly.
- Leave negative space above-left for the title and below-right for a short explanatory note or legend.