# SVG Recipe — Text Zoom-Reveal Morph

## Visual mechanism
A full-slide photograph sits underneath a dark cinematic overlay, while a giant word acts as a photo-filled “window” that appears to punch through the overlay. In PowerPoint, duplicate the slide and scale the same word-window group enormously; Morph makes the audience feel like they zoom through the letters into the revealed image.

## SVG primitives needed
- 2× `<image>` for the same hero photograph: one as the underlying reveal photo, one clipped into the word-window
- 1× `<rect>` for the full-slide dark overlay
- 1× `<clipPath>` containing chunky letter `<path>` geometry to simulate the transparent text cutout
- 1× `<image clip-path="url(#wordClip)">` for the visible photo inside the letters
- 1× `<linearGradient>` for a premium dark edge vignette over the photo
- 1× `<radialGradient>` for subtle warm highlight behind the word
- 2× `<filter>` definitions: one soft glow behind the clipped word image, one drop shadow for typography and callouts
- 6× `<path>` for large geometric block-letter shapes spelling the reveal word
- 4× `<text>` blocks with explicit `width` attributes for supporting editorial labels and Morph instructions
- 3× `<line>` elements for small guide marks / motion direction accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="edgeVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.38"/>
      <stop offset="45%" stop-color="#020617" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.52"/>
    </linearGradient>

    <radialGradient id="warmCore" cx="50%" cy="48%" r="58%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.23"/>
      <stop offset="48%" stop-color="#f59e0b" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="letterGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Chunky geometric text converted to paths.
         Use actual outlined paths for your chosen word; do not rely on SVG masks. -->
    <clipPath id="wordClip" clipPathUnits="userSpaceOnUse">
      <!-- Word: VISION, built as extra-bold geometric letterforms -->
      <path d="M170 214 L226 214 L278 431 L330 214 L386 214 L304 506 L252 506 Z"/>
      <path d="M420 214 L482 214 L482 506 L420 506 Z"/>
      <path d="M534 232 C559 216 591 207 630 207 C678 207 717 221 747 249 L713 291 C689 272 660 262 626 262 C604 262 587 266 575 274 C563 282 557 292 557 304 C557 317 564 327 578 333 C592 339 616 345 651 351 C686 357 713 367 733 383 C753 399 763 421 763 449 C763 487 748 516 717 536 C686 556 646 566 598 566 C542 566 496 551 460 521 L495 477 C526 501 561 513 600 513 C626 513 646 509 661 501 C676 493 684 482 684 468 C684 454 677 444 662 438 C647 432 623 426 590 420 C554 414 527 404 509 389 C491 374 482 352 482 323 C482 286 499 256 534 232 Z"/>
      <path d="M803 214 L865 214 L865 506 L803 506 Z"/>
      <path d="M940 249 C969 221 1006 207 1051 207 C1096 207 1133 221 1162 249 C1191 277 1206 314 1206 360 C1206 406 1191 443 1162 471 C1133 499 1096 513 1051 513 C1006 513 969 499 940 471 C911 443 896 406 896 360 C896 314 911 277 940 249 Z M984 433 C1001 451 1023 460 1051 460 C1079 460 1101 451 1118 433 C1135 415 1144 391 1144 360 C1144 329 1135 305 1118 287 C1101 269 1079 260 1051 260 C1023 260 1001 269 984 287 C967 305 958 329 958 360 C958 391 967 415 984 433 Z"/>
      <path d="M1228 214 L1280 214 L1280 506 L1228 506 Z M1148 214 L1203 214 L1272 353 L1272 506 L1222 506 L1148 363 Z"/>
    </clipPath>
  </defs>

  <!-- Underlying image that will be fully visible after the Morph zoom. -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/hero-photo-night-city-with-warm-lights-and-motion.jpg"/>

  <!-- Premium photo grading. -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmCore)"/>

  <!-- Dark mask layer. This is the visible overlay on the starting slide. -->
  <rect x="0" y="0" width="1280" height="720" fill="#05070d" opacity="0.88"/>

  <!-- Same image clipped into the word; visually reads as transparent text cutout. -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#wordClip)" filter="url(#letterGlow)"
         href="https://images.example.com/hero-photo-night-city-with-warm-lights-and-motion.jpg"/>

  <!-- Thin editorial frame, giving the start state a cinematic title-card quality. -->
  <rect x="58" y="52" width="1164" height="616" rx="26" fill="none" stroke="#ffffff" stroke-opacity="0.16" stroke-width="1.5"/>
  <rect x="82" y="76" width="1116" height="568" rx="20" fill="none" stroke="#f59e0b" stroke-opacity="0.22" stroke-width="1"/>

  <!-- Microcopy: keep small, secondary, and away from the zoom word. -->
  <text x="86" y="104" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" letter-spacing="3" fill="#f8fafc" opacity="0.78">
    KEYNOTE OPENING
  </text>

  <text x="86" y="624" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400" fill="#cbd5e1" opacity="0.82">
    The audience first sees the world only through the letters.
  </text>

  <text x="834" y="104" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" letter-spacing="2.5" fill="#f59e0b" opacity="0.9">
    MORPH: SCALE WORD GROUP 24×
  </text>

  <text x="794" y="624" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400" text-anchor="end" fill="#cbd5e1" opacity="0.82">
    Duplicate slide → enlarge the clipped-word layer until it exceeds the canvas.
  </text>

  <!-- Directional zoom accents; use lines, not path marker arrows. -->
  <line x1="604" y1="150" x2="640" y2="184" stroke="#f59e0b" stroke-width="2" stroke-opacity="0.55"/>
  <line x1="676" y1="150" x2="640" y2="184" stroke="#f59e0b" stroke-width="2" stroke-opacity="0.55"/>
  <line x1="640" y1="184" x2="640" y2="126" stroke="#f59e0b" stroke-width="2" stroke-opacity="0.38" stroke-dasharray="5 8"/>

  <!-- Optional designer-only end-state ghost: the huge scaled word boundary.
       In production, remove this from Slide 1 and create it on Slide 2 as the Morph target. -->
  <path d="M170 214 L226 214 L278 431 L330 214 L386 214 L304 506 L252 506 Z"
        transform="translate(640 360) scale(7.5) translate(-278 -360)"
        fill="none" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<mask>` or `mask="url(#...)"` for the text cutout; PPT translation will fail or ignore it.
- ❌ `<textPath>` or image `<pattern>` fills to put the photo inside typography; use outlined letter paths in a `<clipPath>` applied to an `<image>`.
- ❌ Depending on live editable `<text>` as the clipping geometry; convert the zoom word to chunky vector paths for reliable cropping.
- ❌ Scaling the background photo itself on the Morph target; keep the full-slide photo stable and scale only the word-window / clipped reveal layer.
- ❌ Tiny or thin fonts; the reveal must use ultra-bold, wide letterforms so the photo is legible through the word.

## Composition notes
- Center the word vertically and let it occupy roughly 75–90% of slide width on the first slide; the word is the entire focal mechanism.
- Use a dark overlay around 85–92% opacity so the photo is only visible through the letters at the start.
- For the Morph target slide, duplicate the slide and scale the clipped-word layer 20–30× around the slide center until the clipped photo fills the entire canvas.
- Keep all supporting labels small and peripheral; the animation should read as “word → world,” not as a busy title layout.