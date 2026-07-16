# SVG Recipe — Seamless Background Mask Reveal

## Visual mechanism
A headline appears to emerge from inside the slide by placing it behind a “chameleon” mask: a duplicate crop of the background that perfectly covers the text’s starting area. In PowerPoint, animate the hidden text with a Fly In motion from the masked side so it seems to reveal from the background or from behind a foreground subject.

## SVG primitives needed
- 1× full-slide `<image>` for the photographic or textured background.
- 1× duplicate `<image>` clipped to a rectangular reveal-mask zone; this is the seamless cover that hides the starting text.
- 1× `<clipPath>` with `<rect>` for the background duplicate crop.
- 1× foreground `<image>` for a subject, product, or character placed above the mask to deepen the illusion.
- 2× `<text>` objects for the animated headline and small label; every text element has explicit `width`.
- 2× `<rect>` overlays for cinematic darkening and readability panels.
- 2× `<linearGradient>` definitions for atmosphere and text polish.
- 1× `<filter>` shadow applied to headline and foreground subject for depth.
- Several decorative `<path>` and `<circle>` elements for premium keynote styling and motion direction cues.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#050814" stop-opacity="0.82"/>
      <stop offset="45%" stop-color="#050814" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#050814" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="headlineFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="72%" stop-color="#EAF4FF"/>
      <stop offset="100%" stop-color="#A7D8FF"/>
    </linearGradient>

    <linearGradient id="accentGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#27F5FF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#6D5BFF" stop-opacity="0.45"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blueGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- This rectangle defines the exact zone that hides the incoming headline. -->
    <clipPath id="backgroundMaskZone">
      <rect x="760" y="0" width="520" height="720"/>
    </clipPath>
  </defs>

  <!-- Layer 1: background scene -->
  <image
    href="https://images.example.com/dark-premium-gym-interior-with-blue-rim-light.jpg"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Cinematic darkening. Keep this below the animated text. -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- Subtle premium atmosphere -->
  <circle cx="1020" cy="180" r="210" fill="#1F7DFF" opacity="0.14" filter="url(#blueGlow)"/>
  <circle cx="1120" cy="500" r="160" fill="#00E4FF" opacity="0.10" filter="url(#blueGlow)"/>
  <path d="M70 590 C240 520, 330 630, 520 555 S810 510, 960 590"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2" stroke-dasharray="8 14"/>

  <!-- Layer 2: the element that will receive Fly In from Right in PowerPoint -->
  <text x="82" y="328" width="710"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="74" font-weight="800" letter-spacing="-2"
        fill="url(#headlineFill)" filter="url(#softShadow)">
    Built for Peak Performance
  </text>

  <text x="88" y="384" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="600" letter-spacing="3.5"
        fill="#7EEBFF" opacity="0.95">
    SEAMLESS BACKGROUND MASK REVEAL
  </text>

  <!-- Optional end-position guide line / accent, also behind the mask. -->
  <rect x="88" y="414" width="250" height="4" rx="2" fill="url(#accentGlow)"/>

  <!-- Layer 3: chameleon mask.
       This is a duplicate of the background image clipped to the start zone.
       It must sit above the headline and be perfectly aligned with the original background. -->
  <image
    href="https://images.example.com/dark-premium-gym-interior-with-blue-rim-light.jpg"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
    clip-path="url(#backgroundMaskZone)"/>

  <!-- Recreate simple atmospheric elements that crossed into the mask zone so the cover remains seamless. -->
  <circle cx="1020" cy="180" r="210" fill="#1F7DFF" opacity="0.14" filter="url(#blueGlow)"/>
  <circle cx="1120" cy="500" r="160" fill="#00E4FF" opacity="0.10" filter="url(#blueGlow)"/>

  <!-- Layer 4: foreground anchor that sells the depth illusion. -->
  <image
    href="https://images.example.com/transparent-png-athlete-standing-with-kettlebell-blue-rim-light.png"
    x="762" y="118" width="360" height="520" preserveAspectRatio="xMidYMid meet"
    filter="url(#softShadow)"/>

  <!-- Premium foreground UI-like callout -->
  <rect x="858" y="560" width="250" height="72" rx="22" fill="#07111F" opacity="0.78"/>
  <rect x="858" y="560" width="250" height="72" rx="22" fill="none" stroke="#65E9FF" stroke-opacity="0.38" stroke-width="1.5"/>
  <text x="888" y="590" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        fill="#FFFFFF">
    Text starts hidden here
  </text>
  <text x="888" y="613" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="500"
        fill="#9EDFFF" opacity="0.9">
    Animate headline: Fly In → From Right
  </text>

  <!-- Small motion cue; remove for final production if not wanted. -->
  <path d="M735 360 C785 360, 820 360, 858 360"
        fill="none" stroke="#7EEBFF" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 10" opacity="0.65"/>
  <path d="M858 360 L838 348 L838 372 Z" fill="#7EEBFF" opacity="0.65"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(...)"`; it will not translate reliably and is unnecessary here.
- ❌ Do not apply `clip-path` to a normal `<rect>` or `<g>` for the chameleon cover; use it only on the duplicate `<image>`.
- ❌ Do not use `<animate>` or `<animateTransform>` in SVG. Create the visual layers in SVG, then add the PowerPoint Fly In animation to the headline after import.
- ❌ Do not rely on transparency alone for the mask; a semi-transparent rectangle will reveal the hidden text and break the illusion.
- ❌ Do not move or crop the duplicate background differently from the base background. Even a small mismatch makes the mask visible.

## Composition notes
- Keep the animated headline behind the mask layer, with its final resting position partly outside or just left of the masked region.
- The mask zone should be wider than the headline’s starting offset; for a right-side Fly In, reserve roughly the right 35–45% of the slide as the hidden launch area.
- A foreground subject overlapping the mask edge makes the reveal feel physically grounded, as if the title passes behind the subject.
- Use a dark or low-detail background in the mask region; seamless duplication works best when the crop alignment is exact and the texture is not overly busy.