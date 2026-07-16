# SVG Recipe — Animated Image-Fill Text Reveal

## Visual mechanism
Use oversized, extra-bold title lettering as a window into photography, then reveal a second photograph through the same letter shapes with a left-to-right wipe. In SVG/PPTX, represent the animation as two duplicated slides: slide 1 uses the “before” image fill, slide 2 swaps to the “after” image fill and receives a native PowerPoint wipe transition.

## SVG primitives needed
- 1× `<rect>` for the soft neutral slide background.
- 2× decorative `<ellipse>` elements with radial gradients for subtle atmospheric depth.
- 2× `<clipPath>` definitions made from `<path>` letter outlines: one for the revealed side of the title, one for the unrevealed side.
- 2× `<image>` elements, each clipped to a different set of title-letter paths to show a mid-reveal state.
- 1× large `<text>` shadow layer behind the clipped images for dimensional lift.
- 1× `<filter id="titleShadow">` using `feOffset + feGaussianBlur + feMerge` for the title shadow.
- 1× `<filter id="wipeGlow">` using `feGaussianBlur` for the luminous wipe edge.
- 2× `<rect>` elements for the wipe blade and its soft highlight.
- 2× `<text>` elements for subtitle and small transition cue, each with explicit `width`.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlowA" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#e7e7e7" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="bgGlowB" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#d8c7a3" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#e7e7e7" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="wipeBlade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#f7d77b" stop-opacity="0"/>
    </linearGradient>

    <filter id="titleShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="10" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="wipeGlow" x="-100%" y="-30%" width="300%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <!-- Revealed letters: W E L C -->
    <clipPath id="titleClipAfter" clipPathUnits="userSpaceOnUse">
      <path d="M116 250 L146 400 H184 L209 314 L234 400 H274 L304 250 H264 L251 348 L224 250 H194 L168 348 L156 250 Z"/>
      <path d="M322 250 H430 V284 H365 V307 H418 V340 H365 V366 H435 V400 H322 Z"/>
      <path d="M455 250 H497 V363 H570 V400 H455 Z"/>
      <path d="M606 250 H688 V286 H612 Q583 286 583 325 Q583 364 612 364 H688 V400 H606 Q536 400 536 325 Q536 250 606 250 Z"/>
    </clipPath>

    <!-- Unrevealed letters: O M E -->
    <clipPath id="titleClipBefore" clipPathUnits="userSpaceOnUse">
      <path fill-rule="evenodd" d="M738 250 H804 Q858 250 858 325 Q858 400 804 400 H738 Q684 400 684 325 Q684 250 738 250 Z M747 287 Q728 287 728 325 Q728 363 747 363 H795 Q814 363 814 325 Q814 287 795 287 Z"/>
      <path d="M880 400 V250 H927 L955 332 L984 250 H1032 V400 H991 V319 L966 389 H944 L919 319 V400 Z"/>
      <path d="M1054 250 H1166 V284 H1097 V307 H1152 V340 H1097 V366 H1169 V400 H1054 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#e7e7e7"/>
  <ellipse cx="270" cy="130" rx="420" ry="190" fill="url(#bgGlowA)"/>
  <ellipse cx="1040" cy="585" rx="360" ry="160" fill="url(#bgGlowB)"/>

  <!-- Soft typographic depth; the image-filled letter paths sit above it. -->
  <text x="640" y="398" width="1100" text-anchor="middle"
        font-family="Segoe UI, Arial Black, Microsoft YaHei, sans-serif"
        font-size="156" font-weight="900" letter-spacing="-6"
        fill="#1f2328" opacity="0.22" filter="url(#titleShadow)">WELCOME</text>

  <!-- Left side: the newly revealed image texture. -->
  <image x="70" y="150" width="1140" height="360" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1519996236531-f8a018a13a24?w=1600"
         clip-path="url(#titleClipAfter)"/>

  <!-- Right side: the original image texture still waiting to be wiped away. -->
  <image x="70" y="150" width="1140" height="360" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1444090542259-0af8fa96557e?w=1600"
         clip-path="url(#titleClipBefore)"/>

  <!-- Luminous wipe edge, positioned between C and O for this storyboard frame. -->
  <rect x="672" y="224" width="34" height="205" rx="17" fill="url(#wipeBlade)" filter="url(#wipeGlow)" opacity="0.9"/>
  <rect x="687" y="238" width="3" height="176" rx="1.5" fill="#ffffff" opacity="0.92"/>

  <text x="640" y="482" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="600" letter-spacing="9"
        fill="#654321">TO OUR PRESENTATION</text>

  <line x1="500" y1="535" x2="780" y2="535" stroke="#b9a987" stroke-width="1.5" stroke-dasharray="8 10"/>
  <text x="640" y="574" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#7b746a">
    Duplicate the slide, swap the image fill, then apply a native PowerPoint wipe from left.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; they will hard-fail or not translate. Use duplicate PPT slides plus a native wipe transition.
- ❌ Do not use `<mask>` to make the image-filled text. Use `<clipPath>` applied directly to `<image>`.
- ❌ Do not apply `clip-path` to `<text>` or `<g>` for this effect; clipping should be on the `<image>` element.
- ❌ Do not use `<pattern>` fills for photo typography; pattern fills are silently dropped.
- ❌ Do not rely on live font clipping if editability is critical. For robust image-filled typography, convert the hero word to letter outline `<path>` shapes inside the clipPath.

## Composition notes
- Keep the hero word enormous and centered; the technique works best when the letters are thick enough to show recognizable photographic detail.
- Use a quiet neutral background so the image-filled title remains the only dominant visual element.
- Place the subtitle close beneath the title with generous letter spacing; it should feel cinematic but not compete.
- For the animated version, make slide 1 entirely “before” image-filled text and slide 2 entirely “after” image-filled text, then apply a PowerPoint wipe transition from left to slide 2.