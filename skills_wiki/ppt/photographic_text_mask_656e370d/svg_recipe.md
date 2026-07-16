# SVG Recipe — Photographic Text Mask

## Visual mechanism
A bold word is converted into vector letter outlines and used as a clipping shape for a high-impact photograph, making the image visible only inside the typography. The surrounding slide stays restrained so the photo-filled letters become the hero graphic.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background.
- 1× `<clipPath>` containing 1 compound `<path>` for the outlined word stencil.
- 1× clipped `<image>` for the photograph revealed inside the letters.
- 3× duplicate compound `<path>` shapes for shadow, rim highlight, and subtle glass sheen over the photographic text.
- 4× decorative `<path>` wave/contour strokes in the background to echo the photo theme.
- 2× `<text>` elements with explicit `width` for small editable supporting copy.
- 2× `<linearGradient>` for the background and highlight sheen.
- 2× `<radialGradient>` for soft ambient color blooms.
- 2× `<filter>` definitions: one drop shadow and one soft glow, applied only to paths.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07131F"/>
      <stop offset="48%" stop-color="#0B2030"/>
      <stop offset="100%" stop-color="#02070C"/>
    </linearGradient>

    <radialGradient id="aquaBloom" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#1FE3FF" stop-opacity="0.22"/>
      <stop offset="60%" stop-color="#0E7FA6" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0E7FA6" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetBloom" cx="82%" cy="20%" r="45%">
      <stop offset="0%" stop-color="#7C5CFF" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#7C5CFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="sheen" x1="0" y1="220" x2="0" y2="465">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="38%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="wordShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="rimGlow" x="-8%" y="-12%" width="116%" height="130%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <clipPath id="wordClip" clipPathUnits="userSpaceOnUse">
      <path fill-rule="evenodd" d="M175 218 C112 218 76 266 76 340 C76 414 112 462 175 462 C238 462 274 414 274 340 C274 266 238 218 175 218 Z M175 266 C210 266 229 294 229 340 C229 386 210 414 175 414 C140 414 121 386 121 340 C121 294 140 266 175 266 Z M498 255 C463 228 431 216 391 220 C324 226 282 275 282 340 C282 409 327 462 395 466 C439 469 475 455 502 428 L470 389 C448 409 427 419 399 417 C354 414 324 382 324 341 C324 299 352 267 396 264 C425 262 448 272 471 293 Z M545 225 H705 V270 H596 V316 H688 V359 H596 V412 H710 V457 H545 Z M737 457 L823 225 H875 L963 457 H908 L891 413 H807 L790 457 Z M822 371 H875 L848 293 Z M1000 457 V225 H1052 L1140 369 V225 H1192 V457 H1141 L1052 312 V457 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#aquaBloom)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#violetBloom)"/>

  <path d="M-40 560 C150 515 270 610 450 565 C635 518 760 500 920 545 C1075 588 1160 570 1320 525" fill="none" stroke="#2AD4FF" stroke-width="2" stroke-opacity="0.22"/>
  <path d="M-20 604 C170 565 290 650 470 610 C640 572 770 548 940 590 C1090 626 1195 612 1320 575" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.12"/>
  <path d="M790 105 C875 70 960 70 1045 108 C1120 141 1188 133 1265 92" fill="none" stroke="#7C5CFF" stroke-width="2" stroke-opacity="0.22"/>
  <path d="M35 138 C125 100 218 110 305 150 C378 184 445 175 520 126" fill="none" stroke="#2AD4FF" stroke-width="2" stroke-opacity="0.15"/>

  <text x="92" y="108" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" letter-spacing="4" fill="#8FEAFF">
    BLUE ECONOMY 2026
  </text>

  <path transform="translate(0 0)" filter="url(#wordShadow)" fill="#000000" fill-opacity="0.58" fill-rule="evenodd" d="M175 218 C112 218 76 266 76 340 C76 414 112 462 175 462 C238 462 274 414 274 340 C274 266 238 218 175 218 Z M175 266 C210 266 229 294 229 340 C229 386 210 414 175 414 C140 414 121 386 121 340 C121 294 140 266 175 266 Z M498 255 C463 228 431 216 391 220 C324 226 282 275 282 340 C282 409 327 462 395 466 C439 469 475 455 502 428 L470 389 C448 409 427 419 399 417 C354 414 324 382 324 341 C324 299 352 267 396 264 C425 262 448 272 471 293 Z M545 225 H705 V270 H596 V316 H688 V359 H596 V412 H710 V457 H545 Z M737 457 L823 225 H875 L963 457 H908 L891 413 H807 L790 457 Z M822 371 H875 L848 293 Z M1000 457 V225 H1052 L1140 369 V225 H1192 V457 H1141 L1052 312 V457 Z"/>

  <image x="58" y="180" width="1168" height="360" preserveAspectRatio="xMidYMid slice" clip-path="url(#wordClip)"
         href="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&amp;fit=crop&amp;w=1800&amp;q=85"/>

  <path fill="url(#sheen)" fill-rule="evenodd" opacity="0.55" d="M175 218 C112 218 76 266 76 340 C76 414 112 462 175 462 C238 462 274 414 274 340 C274 266 238 218 175 218 Z M175 266 C210 266 229 294 229 340 C229 386 210 414 175 414 C140 414 121 386 121 340 C121 294 140 266 175 266 Z M498 255 C463 228 431 216 391 220 C324 226 282 275 282 340 C282 409 327 462 395 466 C439 469 475 455 502 428 L470 389 C448 409 427 419 399 417 C354 414 324 382 324 341 C324 299 352 267 396 264 C425 262 448 272 471 293 Z M545 225 H705 V270 H596 V316 H688 V359 H596 V412 H710 V457 H545 Z M737 457 L823 225 H875 L963 457 H908 L891 413 H807 L790 457 Z M822 371 H875 L848 293 Z M1000 457 V225 H1052 L1140 369 V225 H1192 V457 H1141 L1052 312 V457 Z"/>

  <path filter="url(#rimGlow)" fill="none" stroke="#A8F4FF" stroke-width="3" stroke-opacity="0.55" fill-rule="evenodd" d="M175 218 C112 218 76 266 76 340 C76 414 112 462 175 462 C238 462 274 414 274 340 C274 266 238 218 175 218 Z M175 266 C210 266 229 294 229 340 C229 386 210 414 175 414 C140 414 121 386 121 340 C121 294 140 266 175 266 Z M498 255 C463 228 431 216 391 220 C324 226 282 275 282 340 C282 409 327 462 395 466 C439 469 475 455 502 428 L470 389 C448 409 427 419 399 417 C354 414 324 382 324 341 C324 299 352 267 396 264 C425 262 448 272 471 293 Z M545 225 H705 V270 H596 V316 H688 V359 H596 V412 H710 V457 H545 Z M737 457 L823 225 H875 L963 457 H908 L891 413 H807 L790 457 Z M822 371 H875 L848 293 Z M1000 457 V225 H1052 L1140 369 V225 H1192 V457 H1141 L1052 312 V457 Z"/>

  <text x="92" y="610" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="400" fill="#D7F7FF" opacity="0.88">
    Where marine intelligence, capital, and climate strategy converge.
  </text>

  <circle cx="1112" cy="595" r="4" fill="#8FEAFF"/>
  <circle cx="1134" cy="595" r="4" fill="#8FEAFF" opacity="0.55"/>
  <circle cx="1156" cy="595" r="4" fill="#8FEAFF" opacity="0.30"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<text>` with `fill="url(#image)"` or `<pattern>` image fills; image patterns are not reliable for editable PowerPoint translation.
- ❌ Do not apply `clip-path` to the text itself. Apply the letter-shaped `clipPath` only to the `<image>`.
- ❌ Do not place live `<text>` inside the `clipPath`; convert the headline word to vector `<path>` outlines first.
- ❌ Avoid thin fonts or narrow letterforms; too little photographic detail will be visible.
- ❌ Avoid `<mask>` for text knockout effects; masks hard-fail or translate poorly compared with clipped images.

## Composition notes
- Keep the photographic word very large, usually 65–80% of slide width, with generous negative space around it.
- Use a dark or neutral background so the photo texture inside the letters carries the full color story.
- Choose a photo with strong contrast and recognizable texture; wide landscapes, city lights, foliage, waves, and machinery work especially well.
- Supporting copy should be small and quiet, positioned outside the main word so it does not compete with the masked typography.