# SVG Recipe — Magazine Cut-out Collage Effect

## Visual mechanism
A foreground subject is treated like a physical magazine clipping by placing an irregular, slightly larger white paper silhouette behind it and adding a soft offset shadow. Rotated scraps, washi tape, bold mixed typography, and overlapping data callouts make the slide feel handmade, editorial, and tactile.

## SVG primitives needed
- 1× full-slide `<rect>` for the warm editorial background
- 3× decorative `<path>` blobs for background energy and paper scraps
- 1× large irregular white `<path>` for the main cut-out paper backing
- 1× `<image>` for the transparent-background hero subject placed over the backing
- 3× smaller irregular white `<path>` scraps for data callout cards
- 5× semi-transparent rotated `<rect>` elements for washi tape strips and label blocks
- 2× `<line>` elements for hand-drawn underlines / accent marks
- Multiple `<text>` elements with explicit `width` for ransom-note title, subtitle, and chart-data callouts
- 1× `<filter id="paperShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to paper backing paths
- 1× `<filter id="softGlow">` using `feGaussianBlur` applied to accent blobs
- 1× `<linearGradient>` for the background and 1× `<radialGradient>` for soft color bloom

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mustardBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7D94C"/>
      <stop offset="55%" stop-color="#F0BE38"/>
      <stop offset="100%" stop-color="#E7992F"/>
    </linearGradient>
    <radialGradient id="pinkBloom" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#FF6B9A" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#FF6B9A" stop-opacity="0"/>
    </radialGradient>
    <filter id="paperShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="10" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .30 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#mustardBg)"/>
  <circle cx="1040" cy="145" r="175" fill="url(#pinkBloom)" filter="url(#softGlow)"/>
  <path d="M95,580 C180,520 250,610 330,555 C390,515 455,560 510,620 L510,720 L70,720 C52,665 45,615 95,580 Z"
        fill="#263B8F" opacity="0.20"/>
  <path d="M1020,510 C1085,455 1200,470 1245,545 C1288,618 1218,690 1110,680 C1012,672 958,562 1020,510 Z"
        fill="#FFFFFF" opacity="0.18"/>

  <rect x="148" y="72" width="350" height="78" rx="8" fill="#FFFFFF" opacity="0.92" transform="rotate(-3 323 111)" filter="url(#paperShadow)"/>
  <text x="172" y="126" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="900"
        fill="#151515" letter-spacing="2" transform="rotate(-3 323 111)">MAGAZINE</text>
  <rect x="214" y="151" width="270" height="44" rx="4" fill="#151515" transform="rotate(2 349 173)"/>
  <text x="235" y="181" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        fill="#FFFFFF" letter-spacing="1.5" transform="rotate(2 349 173)">CUT-OUT DATA</text>

  <rect x="618" y="66" width="126" height="34" rx="5" fill="#F8E7A1" opacity="0.72" transform="rotate(8 681 83)"/>
  <rect x="870" y="88" width="132" height="34" rx="5" fill="#F8E7A1" opacity="0.62" transform="rotate(-10 936 105)"/>
  <rect x="560" y="535" width="160" height="38" rx="5" fill="#F8E7A1" opacity="0.68" transform="rotate(-7 640 554)"/>

  <path d="M623,117 C696,69 835,65 910,115 C991,170 1005,276 966,360 C929,442 843,488 740,477 C637,465 564,404 538,315 C511,222 545,168 623,117 Z"
        fill="#FFFFFF" filter="url(#paperShadow)" transform="rotate(4 760 275)"/>
  <image x="585" y="92" width="360" height="430"
         href="https://images.example.com/transparent-cutout-person-in-bright-jacket.png"
         transform="rotate(4 765 307)"/>

  <path d="M120,266 C172,238 274,240 312,282 C348,322 331,401 278,421 C221,444 130,424 102,374 C78,329 82,286 120,266 Z"
        fill="#FFFFFF" filter="url(#paperShadow)" transform="rotate(-8 210 336)"/>
  <text x="132" y="312" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        fill="#111111" transform="rotate(-8 210 336)">SOCIAL LIFT</text>
  <text x="139" y="374" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="900"
        fill="#E83F6F" transform="rotate(-8 210 336)">42%</text>
  <line x1="134" y1="392" x2="286" y2="381" stroke="#111111" stroke-width="5" stroke-linecap="round"
        transform="rotate(-8 210 336)"/>

  <path d="M904,382 C960,342 1075,358 1118,404 C1166,455 1132,535 1066,555 C993,579 902,548 872,491 C849,446 860,411 904,382 Z"
        fill="#FFFFFF" filter="url(#paperShadow)" transform="rotate(7 1000 468)"/>
  <text x="910" y="424" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800"
        fill="#111111" transform="rotate(7 1000 468)">NEW AUDIENCE</text>
  <text x="918" y="494" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="900"
        fill="#2457FF" transform="rotate(7 1000 468)">3.8×</text>
  <text x="934" y="526" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700"
        fill="#111111" opacity="0.8" transform="rotate(7 1000 468)">ENGAGEMENT</text>

  <path d="M392,458 C445,426 539,437 582,480 C625,523 605,600 548,625 C485,652 395,622 368,569 C346,524 350,484 392,458 Z"
        fill="#FFFFFF" filter="url(#paperShadow)" transform="rotate(-4 480 535)"/>
  <text x="392" y="500" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="900"
        fill="#111111" transform="rotate(-4 480 535)">TREND INDEX</text>
  <text x="407" y="565" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="900"
        fill="#00A878" transform="rotate(-4 480 535)">91</text>
  <line x1="405" y1="582" x2="556" y2="570" stroke="#E83F6F" stroke-width="5" stroke-linecap="round"
        transform="rotate(-4 480 535)"/>

  <rect x="101" y="246" width="132" height="30" rx="4" fill="#F8E7A1" opacity="0.72" transform="rotate(-18 167 261)"/>
  <rect x="968" y="360" width="146" height="32" rx="4" fill="#F8E7A1" opacity="0.66" transform="rotate(16 1041 376)"/>
  <text x="776" y="651" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#151515" opacity="0.82">Irregular white silhouettes + soft shadows turn chart callouts into tactile paper objects.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG `<mask>` to generate the white border from the image alpha; masks on shapes will not translate reliably.
- ❌ Do not apply `clip-path` to the white paper backing path; clipping is only safe on `<image>` elements.
- ❌ Do not use `<use>` to duplicate paper scraps or tape strips; draw each path/rect explicitly.
- ❌ Do not put shadows on `<line>` accents; filter effects on lines are dropped.
- ❌ Do not make the backing a perfect rounded rectangle unless the subject is rectangular; the effect depends on an organic, hand-cut silhouette.

## Composition notes
- Keep the main subject large and slightly off-axis; the white backing should extend 12–28 px beyond the visible subject contour.
- Use shadows only on the white paper layers, not on every foreground element, so depth feels like stacked paper.
- Surround the hero cut-out with 2–4 rotated data scraps; overlap them lightly to create a casual editorial rhythm.
- Use a saturated background and high-contrast black/white typography so the collage reads clearly even with playful rotations.