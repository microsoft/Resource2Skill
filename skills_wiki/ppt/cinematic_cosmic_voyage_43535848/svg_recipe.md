# SVG Recipe — Cinematic Cosmic Voyage

## Visual mechanism
Build a deep-space title slide as separated parallax-ready layers: nebula background, distant planet, midground moon, foreground spacecraft, sharp futuristic typography, and diagonal meteor streaks. The SVG itself is static, but each visual layer is kept as editable/independent objects so PowerPoint motion paths, spin, and staggered entrance timing can be added after import.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark cosmic base color
- 1× full-slide `<image>` for the nebula/starfield background
- 2× overlay `<rect>` with gradient fills for cinematic vignette and atmospheric color wash
- 2× clipped `<image>` elements for Earth and moon image crops
- 3× `<circle>` for planet atmosphere, moon rim glow, and orbital emphasis
- 1× `<image>` for the spacecraft foreground element
- 2× `<path>` for spacecraft exhaust plumes and angular title brackets
- 10× narrow rounded `<rect>` for meteor streaks with white-to-transparent gradient fills
- 2× `<text>` objects for the glowing main title and crisp foreground title; each has explicit `width`
- 1× `<text>` subtitle with nested `<tspan>` accents; explicit `width`
- 2× `<linearGradient>` for meteor trails and title accent strokes
- 3× `<radialGradient>` for vignette, nebula bloom, and planetary atmosphere
- 2× `<filter>` definitions for soft glow and shadow applied to shapes/text/images where supported
- 2× `<clipPath>` definitions applied only to `<image>` elements for circular celestial crops

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#101846" stop-opacity="0"/>
      <stop offset="68%" stop-color="#070919" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#02030B" stop-opacity="0.95"/>
    </radialGradient>

    <radialGradient id="magentaBloom" cx="73%" cy="36%" r="58%">
      <stop offset="0%" stop-color="#F04BFF" stop-opacity="0.28"/>
      <stop offset="42%" stop-color="#6B35FF" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#050718" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="earthAtmosphere" cx="45%" cy="42%" r="58%">
      <stop offset="58%" stop-color="#1D8CFF" stop-opacity="0"/>
      <stop offset="78%" stop-color="#2FD6FF" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#B8F5FF" stop-opacity="0.58"/>
    </radialGradient>

    <linearGradient id="meteorFade" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="34%" stop-color="#BEEBFF" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>
    </linearGradient>

    <linearGradient id="hotExhaust" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#FF3FB7" stop-opacity="0"/>
      <stop offset="52%" stop-color="#FF7A2A" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#FFF2A6" stop-opacity="0.95"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cinemaShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="earthClip">
      <circle cx="155" cy="430" r="245"/>
    </clipPath>

    <clipPath id="moonClip">
      <circle cx="1004" cy="188" r="79"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#050715"/>
  <image href="https://images.example.com/deep-blue-magenta-nebula-starfield.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.92"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#magentaBloom)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <g id="distant-earth-layer">
    <image href="https://images.example.com/realistic-earth-from-space.png" x="-90" y="185" width="490" height="490" preserveAspectRatio="xMidYMid slice" clip-path="url(#earthClip)" filter="url(#cinemaShadow)"/>
    <circle cx="155" cy="430" r="247" fill="url(#earthAtmosphere)" filter="url(#softGlow)"/>
    <circle cx="155" cy="430" r="274" fill="none" stroke="#39D7FF" stroke-opacity="0.18" stroke-width="2" stroke-dasharray="18 18"/>
    <circle cx="155" cy="430" r="312" fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1" stroke-dasharray="5 16"/>
  </g>

  <g id="midground-moon-layer">
    <image href="https://images.example.com/cratered-moon-asteroid-round.png" x="925" y="109" width="158" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#moonClip)" filter="url(#cinemaShadow)"/>
    <circle cx="1004" cy="188" r="83" fill="none" stroke="#DDEBFF" stroke-opacity="0.45" stroke-width="2" filter="url(#softGlow)"/>
    <path d="M890 262 C946 304 1048 298 1112 248" fill="none" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1.5" stroke-dasharray="8 13"/>
  </g>

  <g id="spacecraft-layer" transform="rotate(-13 840 472)">
    <path d="M705 493 C657 506 615 526 574 552 C628 547 675 534 724 510 Z" fill="url(#hotExhaust)" filter="url(#softGlow)" opacity="0.9"/>
    <path d="M728 477 C687 476 653 482 620 493 C660 501 697 501 735 491 Z" fill="#67D6FF" opacity="0.28" filter="url(#softGlow)"/>
    <image href="https://images.example.com/sleek-futuristic-spaceship-transparent.png" x="720" y="390" width="250" height="128" preserveAspectRatio="xMidYMid meet" filter="url(#cinemaShadow)"/>
  </g>

  <g id="title-architecture">
    <path d="M492 238 L548 205 L765 205 L744 220 L568 220 L516 252 Z" fill="#35E8FF" opacity="0.28"/>
    <path d="M845 355 L1008 355 L1044 332 L1064 338 L1018 374 L848 374 Z" fill="#FF4CDB" opacity="0.25"/>
    <line x1="518" y1="392" x2="824" y2="392" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="2"/>
    <line x1="842" y1="392" x2="975" y2="392" stroke="#37E7FF" stroke-opacity="0.8" stroke-width="2"/>
  </g>

  <text x="510" y="320" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="800" letter-spacing="5" fill="#54E7FF" opacity="0.55" filter="url(#softGlow)">穿梭蔚蓝</text>
  <text x="510" y="318" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="800" letter-spacing="5" fill="#FFFFFF">穿梭蔚蓝</text>
  <text x="520" y="430" width="535" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="400" letter-spacing="1.2" fill="#DCEBFF">
    <tspan fill="#7DEBFF" font-weight="600">COSMIC VOYAGE</tspan>
    <tspan fill="#FFFFFF" opacity="0.78">  ·  穿越浩瀚星空，抵达下一代蓝色星球</tspan>
  </text>

  <g id="meteor-shower-overlay" opacity="0.92">
    <rect x="982" y="42" width="188" height="5" rx="2.5" fill="url(#meteorFade)" transform="rotate(27 982 42)" filter="url(#softGlow)"/>
    <rect x="1082" y="104" width="132" height="4" rx="2" fill="url(#meteorFade)" transform="rotate(27 1082 104)" opacity="0.72"/>
    <rect x="838" y="78" width="96" height="3" rx="1.5" fill="url(#meteorFade)" transform="rotate(27 838 78)" opacity="0.6"/>
    <rect x="1050" y="304" width="210" height="6" rx="3" fill="url(#meteorFade)" transform="rotate(27 1050 304)" filter="url(#softGlow)"/>
    <rect x="910" y="440" width="150" height="4" rx="2" fill="url(#meteorFade)" transform="rotate(27 910 440)" opacity="0.78"/>
    <rect x="590" y="95" width="118" height="4" rx="2" fill="url(#meteorFade)" transform="rotate(27 590 95)" opacity="0.68"/>
    <rect x="250" y="92" width="86" height="3" rx="1.5" fill="url(#meteorFade)" transform="rotate(27 250 92)" opacity="0.48"/>
    <rect x="1120" y="560" width="130" height="4" rx="2" fill="url(#meteorFade)" transform="rotate(27 1120 560)" opacity="0.62"/>
    <rect x="690" y="585" width="174" height="5" rx="2.5" fill="url(#meteorFade)" transform="rotate(27 690 585)" filter="url(#softGlow)"/>
    <rect x="420" y="512" width="104" height="3" rx="1.5" fill="url(#meteorFade)" transform="rotate(27 420 512)" opacity="0.54"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the voyage motion; create the slide as separated layers, then add PowerPoint motion paths/spin after import.
- ❌ `<mask>` for planet shadows or title reveals; use gradients, opacity, and clipped images instead.
- ❌ `clip-path` on circles/paths/text; clipping is reliable here only when applied to `<image>`.
- ❌ `marker-end` arrowheads for flight direction; use meteor streak rectangles or simple `<line>` elements instead.
- ❌ `<filter>` on `<line>` objects; apply glow to paths, rects, circles, or text instead.

## Composition notes
- Keep the massive Earth cropped off the left edge to create scale; it should occupy roughly the left third while leaving the title area open.
- Put the title in the right-center safe zone, aligned around x=500–1060, with decorative angular paths behind it rather than boxed panels.
- Use diagonal meteor streaks from upper-left to lower-right as the motion rhythm; vary length, opacity, and position so they feel staggered.
- Preserve layer independence: background, Earth, moon, spacecraft, title, and meteors should remain separate groups for later parallax animation in PowerPoint.