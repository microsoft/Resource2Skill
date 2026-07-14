# SVG Recipe — Realistic Typewriter Rhythm Morph (Frame-by-Frame Transition)

## Visual mechanism
A typewriter-photo hero frame is held constant while the typed headline changes one frame at a time, including blinking cursor states, typo frames, backspace frames, and uneven pauses. SVG supplies the editable visual frame; the realism comes from exporting many nearly identical slides with only the text state and cursor visibility changed.

## SVG primitives needed
- 1× `<rect>` for the off-white canvas background.
- 1× `<image>` for the cropped typewriter hero photo occupying the lower half of the slide.
- 1× `<clipPath>` with `<rect>` for the typewriter photo crop.
- 2× `<linearGradient>` for the paper fade and subtle lower vignette.
- 1× `<filter id="softShadow">` applied to logo and foreground cards.
- 1× `<filter id="inkSoftness">` applied to headline text for slightly softened typewriter ink edges.
- 3× `<text>` for the typed headline lines and PowerPoint “P” mark; every text element includes explicit `width`.
- 1× `<rect>` for the cursor bar, toggled on/off per animation frame.
- 2× `<circle>` and 2× `<rect>` for the decorative PowerPoint badge in the lower-right.
- 4× `<path>` for paper edge shadows, typewriter metal accents, and subtle mechanical silhouettes.
- 6× `<line>` for small typewriter ruler / tick details.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="typewriterCrop">
      <rect x="0" y="320" width="1280" height="400"/>
    </clipPath>

    <linearGradient id="paperFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#eef1f2"/>
    </linearGradient>

    <linearGradient id="lowerVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#111111" stop-opacity="0.18"/>
    </linearGradient>

    <linearGradient id="pptBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff7b55"/>
      <stop offset="100%" stop-color="#d44a27"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="5" dy="7"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="inkSoftness" x="-5%" y="-5%" width="110%" height="120%">
      <feGaussianBlur stdDeviation="0.35"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#fbfbf8"/>

  <image
    x="0" y="285" width="1280" height="470"
    href="https://images.example.com/hero/vintage-typewriter-paper-closeup.jpg"
    clip-path="url(#typewriterCrop)"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="420" fill="url(#paperFade)"/>

  <path d="M0 410 C180 406 305 414 445 408 C540 404 650 396 780 406 C955 420 1100 404 1280 411 L1280 455 L0 455 Z"
        fill="#d9dddc" opacity="0.42"/>
  <path d="M0 419 C170 417 315 425 445 418 C610 410 730 408 890 418 C1035 427 1160 414 1280 421 L1280 454 L0 454 Z"
        fill="#191919" opacity="0.16"/>

  <path d="M468 392 C510 348 530 318 555 318 C580 318 602 354 645 392"
        fill="none" stroke="#191b1c" stroke-width="7" stroke-linecap="round" opacity="0.86"/>
  <path d="M260 398 C330 384 405 382 475 392 L452 448 C390 446 315 440 244 430 Z"
        fill="#111111" opacity="0.88"/>
  <path d="M610 392 C688 380 768 381 845 396 L827 432 C748 440 674 438 598 426 Z"
        fill="#111111" opacity="0.88"/>
  <path d="M472 423 C505 407 588 407 620 424 L617 486 C581 497 510 497 475 486 Z"
        fill="#d9d9d4" stroke="#777a76" stroke-width="2"/>

  <line x1="410" y1="392" x2="410" y2="406" stroke="#f5f5f2" stroke-width="3"/>
  <line x1="422" y1="392" x2="422" y2="407" stroke="#f5f5f2" stroke-width="3"/>
  <line x1="434" y1="391" x2="434" y2="407" stroke="#f5f5f2" stroke-width="3"/>
  <line x1="647" y1="392" x2="647" y2="407" stroke="#f5f5f2" stroke-width="3"/>
  <line x1="660" y1="392" x2="660" y2="408" stroke="#f5f5f2" stroke-width="3"/>
  <line x1="673" y1="392" x2="673" y2="408" stroke="#f5f5f2" stroke-width="3"/>

  <text x="42" y="142" width="1160"
        font-family="Consolas, 'Courier New', monospace"
        font-size="108" font-weight="700" letter-spacing="19"
        fill="#030303" filter="url(#inkSoftness)">REALISTIC TYPING</text>

  <text x="42" y="294" width="770"
        font-family="Consolas, 'Courier New', monospace"
        font-size="108" font-weight="700" letter-spacing="14"
        fill="#030303" filter="url(#inkSoftness)">ANIMATION</text>

  <rect x="690" y="179" width="8" height="138" rx="2" fill="#030303"/>

  <circle cx="1090" cy="560" r="102" fill="url(#pptBadge)" opacity="0.94"/>
  <path d="M1090 458 A102 102 0 0 1 1192 560 L1090 560 Z" fill="#ff8b69" opacity="0.72"/>
  <path d="M1090 560 L1192 560 A102 102 0 0 1 1090 662 Z" fill="#bf361d" opacity="0.42"/>
  <rect x="978" y="504" width="110" height="112" rx="9" fill="#af321c" opacity="0.45" filter="url(#softShadow)"/>
  <rect x="970" y="504" width="110" height="112" rx="9" fill="#cf3d1f" filter="url(#softShadow)"/>
  <text x="1004" y="590" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="700" fill="#ffffff">P</text>

  <rect x="0" y="560" width="1280" height="160" fill="url(#lowerVignette)" opacity="0.3"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for typing; create separate slides/frames instead.
- ❌ Do not rely on PowerPoint “appear by letter” animations; the robotic cadence defeats the technique.
- ❌ Do not use `<textPath>` for the typed headline; keep each text state as normal editable `<text>`.
- ❌ Do not apply `clip-path` to text or decorative shapes; use clipping only on the typewriter `<image>`.
- ❌ Do not use `<pattern>` for paper grain or typewriter texture; use a real cropped photo plus gradients.

## Composition notes
- Keep the upper 40–45% of the slide as clean paper whitespace; this is where the typed message changes frame by frame.
- The typewriter photo should anchor the lower half and remain identical across every frame so the transition feels like true typing, not a layout jump.
- Use a monospace face, large tracking, and a simple vertical cursor rectangle; toggle the cursor by including/removing or hiding that rectangle on alternate frames.
- Build the transition sequence as many slides: initial cursor blinks, uneven character additions, occasional wrong-character frames, backspace frames, final blink, then a long hold.