# SVG Recipe — Morphing Text Photo Reveal

## Visual mechanism
A large, heavy word becomes the window through which a cinematic photograph is revealed. For the PowerPoint “Morph” effect, create two near-identical slides: slide 1 uses the same clipped image oversized and translated for a close-up crop, while slide 2 uses the full photo position so the image appears to zoom out inside the letterforms.

## SVG primitives needed
- 1× `<rect>` for the warm editorial background
- 2× blurred `<ellipse>` shapes for soft atmospheric color washes
- 1× `<clipPath>` made from custom `<path>` letterforms to create the image-filled word
- 1× large `<image>` clipped to the letterform path for the main photo reveal
- 2× `<image>` thumbnails clipped by rounded `<rect>` clipPaths to explain the morph start/end states
- 2× `<rect>` thumbnail frames with soft shadows
- 3× `<path>` roles for letter shadow, letter outline, and small arrowhead
- 1× `<line>` for the thumbnail transition connector
- 3× `<text>` elements with explicit `width` for subtitle, micro-labels, and transition notes
- 1× `<filter id="softShadow">` applied to letter/thumbnail shapes
- 1× `<filter id="blurGlow">` applied to atmospheric ellipses
- 2× gradients for background depth and warm spotlight accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff7ef"/>
      <stop offset="58%" stop-color="#fff0e4"/>
      <stop offset="100%" stop-color="#f7dfd0"/>
    </linearGradient>

    <radialGradient id="sunsetGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff9b69" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#ff9b69" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="seaGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4bb8c8" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#4bb8c8" stop-opacity="0"/>
    </radialGradient>

    <filter id="blurGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="38"/>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- The word VISTA is built as editable geometric paths, then used as an image clip. -->
    <clipPath id="vistaClip">
      <path d="
        M110 230 L180 230 L230 410 L280 230 L350 230 L260 490 L200 490 Z
        M380 230 H460 V490 H380 Z
        M680 230 H515 Q500 230 500 245 V330 Q500 345 515 345 H620 V382 H515 Q500 382 500 397 V475 Q500 490 515 490 H680 V435 H555 V397 H665 Q680 397 680 382 V330 Q680 315 665 315 H555 V285 H680 Z
        M710 230 H920 V290 H845 V490 H785 V290 H710 Z
        M930 490 L1025 230 H1085 L990 490 Z
        M1055 230 H1115 L1190 490 H1128 Z
        M1005 386 H1112 L1130 438 H988 Z"/>
    </clipPath>

    <clipPath id="thumbZoomClip">
      <rect x="946" y="562" width="112" height="64" rx="12"/>
    </clipPath>

    <clipPath id="thumbFullClip">
      <rect x="1112" y="562" width="112" height="64" rx="12"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <ellipse cx="210" cy="118" rx="250" ry="120" fill="url(#sunsetGlow)" filter="url(#blurGlow)"/>
  <ellipse cx="1110" cy="612" rx="280" ry="130" fill="url(#seaGlow)" filter="url(#blurGlow)"/>

  <!-- Letter shadow: duplicate of the word geometry, offset slightly for depth. -->
  <path transform="translate(0 14)" opacity="0.22" fill="#5d2d20" filter="url(#softShadow)" d="
    M110 230 L180 230 L230 410 L280 230 L350 230 L260 490 L200 490 Z
    M380 230 H460 V490 H380 Z
    M680 230 H515 Q500 230 500 245 V330 Q500 345 515 345 H620 V382 H515 Q500 382 500 397 V475 Q500 490 515 490 H680 V435 H555 V397 H665 Q680 397 680 382 V330 Q680 315 665 315 H555 V285 H680 Z
    M710 230 H920 V290 H845 V490 H785 V290 H710 Z
    M930 490 L1025 230 H1085 L990 490 Z
    M1055 230 H1115 L1190 490 H1128 Z
    M1005 386 H1112 L1130 438 H988 Z"/>

  <!-- END / reveal state: full photograph aligned behind the clipped word. -->
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
         x="0" y="0" width="1280" height="720"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#vistaClip)"/>

  <!-- Crisp editorial outline to make the photo-filled letters read on pale backgrounds. -->
  <path fill="none" stroke="#ffffff" stroke-width="2.2" stroke-opacity="0.82" d="
    M110 230 L180 230 L230 410 L280 230 L350 230 L260 490 L200 490 Z
    M380 230 H460 V490 H380 Z
    M680 230 H515 Q500 230 500 245 V330 Q500 345 515 345 H620 V382 H515 Q500 382 500 397 V475 Q500 490 515 490 H680 V435 H555 V397 H665 Q680 397 680 382 V330 Q680 315 665 315 H555 V285 H680 Z
    M710 230 H920 V290 H845 V490 H785 V290 H710 Z
    M930 490 L1025 230 H1085 L990 490 Z
    M1055 230 H1115 L1190 490 H1128 Z
    M1005 386 H1112 L1130 438 H988 Z"/>

  <text x="112" y="156" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="4" fill="#8f6b5d">
    CINEMATIC SECTION OPENER
  </text>

  <text x="114" y="548" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="400" fill="#6e4b3f">
    One photograph. Two crops. Morph turns the title into a reveal.
  </text>

  <!-- Small morph-state guide: close crop thumbnail to full panorama thumbnail. -->
  <rect x="936" y="552" width="132" height="84" rx="18" fill="#ffffff" opacity="0.76" filter="url(#softShadow)"/>
  <rect x="1102" y="552" width="132" height="84" rx="18" fill="#ffffff" opacity="0.76" filter="url(#softShadow)"/>

  <!-- START state thumbnail: same photo oversized and translated, representing slide 1 crop. -->
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
         x="900" y="520" width="230" height="130"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#thumbZoomClip)"/>

  <!-- END state thumbnail: same photo at full composition, representing slide 2 crop. -->
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1600&amp;q=90"
         x="1112" y="562" width="112" height="64"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#thumbFullClip)"/>

  <line x1="1078" y1="594" x2="1098" y2="594" stroke="#8f6b5d" stroke-width="2"/>
  <path d="M1098 594 L1090 589 L1090 599 Z" fill="#8f6b5d"/>

  <text x="948" y="654" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.4" fill="#8f6b5d">
    SLIDE 1 CROP
  </text>
  <text x="1114" y="654" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.4" fill="#8f6b5d">
    SLIDE 2 FULL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to create the text-photo effect; masks are a hard fail for this workflow.
- ❌ Do not rely on live SVG animation such as `<animate>` or `<animateTransform>`; create two PowerPoint slides and use the native Morph transition.
- ❌ Do not use `<textPath>` or pattern fills for the letter interiors; they will not translate reliably.
- ❌ Do not place `clip-path` on a `<text>` or `<path>` expecting it to work as a mask; apply the clipPath to the `<image>` only.
- ❌ Do not use `marker-end` for the thumbnail arrow; draw the arrowhead as a small editable `<path>`.

## Composition notes
- Keep the image-filled word huge, centered, and dominant; it should occupy roughly 70–85% of slide width.
- Use a quiet warm background so the photograph inside the letters carries the color energy.
- For Morph, duplicate the slide: on slide 1, keep the same clipped word but make the photo much larger and shifted; on slide 2, restore the photo to the full-slide composition.
- Choose short, heavy words with wide letter surfaces; thin fonts will not reveal enough photographic detail.