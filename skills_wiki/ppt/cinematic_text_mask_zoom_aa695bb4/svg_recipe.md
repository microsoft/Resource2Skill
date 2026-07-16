# SVG Recipe — Cinematic Text Mask Zoom

## Visual mechanism
A dramatic black slide uses oversized letterforms as a stencil window into a vivid full-bleed photograph. In PowerPoint, duplicate this slide, replace the stencil state with the same photo full-screen, and apply Morph to create the cinematic “zoom through the word” reveal.

## SVG primitives needed
- 1× `<rect>` for the black stage background
- 1× `<radialGradient>` for a subtle cinematic vignette on the stage
- 1× `<image>` for a dim, atmospheric full-slide photo underlay
- 1× `<clipPath>` containing a compound `<path>` shaped like bold block lettering
- 1× clipped `<image>` for the photo visible only inside the letter stencil
- 2× `<path>` duplicates of the letter geometry for glow, outline, and bevel-like edge definition
- 1× `<filter id="letterGlow">` with `feGaussianBlur` for soft light around the stencil
- 1× `<filter id="softShadow">` with `feOffset`, `feGaussianBlur`, and `feMerge` for caption depth
- 3× `<text>` elements with explicit `width` for small cinematic metadata/caption typography

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="stageVignette" cx="50%" cy="47%" r="72%">
      <stop offset="0%" stop-color="#151a22"/>
      <stop offset="52%" stop-color="#05070b"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="edgeLight" x1="130" y1="245" x2="1150" y2="475" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#b9f3ff"/>
      <stop offset="48%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#6fb7ff"/>
    </linearGradient>

    <filter id="letterGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="wordClip">
      <path d="
        M130 245 H310 V287 H172 V339 H304 V381 H172 V433 H310 V475 H130 V433 H268 V381 H130 V245 Z
        M340 245 H382 V337 H478 V245 H520 V475 H478 V379 H382 V475 H340 V245 Z
        M550 245 H730 V287 H661 V433 H730 V475 H550 V433 H619 V287 H550 V245 Z
        M760 245 H940 V287 H802 V342 H928 V384 H802 V475 H760 V245 Z
        M970 245 H1150 V287 H1081 V475 H1039 V287 H970 V245 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#stageVignette)"/>

  <image
    href="https://images.example.com/cinematic-night-city-mountains-blue-orange-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    opacity="0.16"/>

  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.38"/>

  <path
    d="
      M130 245 H310 V287 H172 V339 H304 V381 H172 V433 H310 V475 H130 V433 H268 V381 H130 V245 Z
      M340 245 H382 V337 H478 V245 H520 V475 H478 V379 H382 V475 H340 V245 Z
      M550 245 H730 V287 H661 V433 H730 V475 H550 V433 H619 V287 H550 V245 Z
      M760 245 H940 V287 H802 V342 H928 V384 H802 V475 H760 V245 Z
      M970 245 H1150 V287 H1081 V475 H1039 V287 H970 V245 Z"
    fill="#06101b"
    opacity="0.52"
    filter="url(#letterGlow)"/>

  <image
    href="https://images.example.com/cinematic-night-city-mountains-blue-orange-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#wordClip)"/>

  <path
    d="
      M130 245 H310 V287 H172 V339 H304 V381 H172 V433 H310 V475 H130 V433 H268 V381 H130 V245 Z
      M340 245 H382 V337 H478 V245 H520 V475 H478 V379 H382 V475 H340 V245 Z
      M550 245 H730 V287 H661 V433 H730 V475 H550 V433 H619 V287 H550 V245 Z
      M760 245 H940 V287 H802 V342 H928 V384 H802 V475 H760 V245 Z
      M970 245 H1150 V287 H1081 V475 H1039 V287 H970 V245 Z"
    fill="none"
    stroke="#02050a"
    stroke-width="10"
    opacity="0.78"/>

  <path
    d="
      M130 245 H310 V287 H172 V339 H304 V381 H172 V433 H310 V475 H130 V433 H268 V381 H130 V245 Z
      M340 245 H382 V337 H478 V245 H520 V475 H478 V379 H382 V475 H340 V245 Z
      M550 245 H730 V287 H661 V433 H730 V475 H550 V433 H619 V287 H550 V245 Z
      M760 245 H940 V287 H802 V342 H928 V384 H802 V475 H760 V245 Z
      M970 245 H1150 V287 H1081 V475 H1039 V287 H970 V245 Z"
    fill="none"
    stroke="url(#edgeLight)"
    stroke-width="3"
    opacity="0.92"
    filter="url(#letterGlow)"/>

  <text x="132" y="158" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" letter-spacing="5" fill="#8ea7bd" opacity="0.88">
    OPENING SEQUENCE
  </text>

  <text x="130" y="548" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="600" fill="#f1f7ff" filter="url(#softShadow)">
    Zoom through the message to reveal the world behind it
  </text>

  <text x="130" y="582" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#8fa3b8" opacity="0.9">
    Duplicate this slide, remove the black stencil layer, place the same image full bleed, then apply PowerPoint Morph.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; PowerPoint Morph should create the motion, not SVG animation
- ❌ `<mask>` for the text reveal; use `clipPath` applied directly to the `<image>`
- ❌ `<pattern>` image fills for the text; pattern fills are not reliable in the translator
- ❌ `<textPath>` or live SVG text as a clipping shape; convert the headline word into bold compound letter paths for the stencil
- ❌ `<use href="#...">` to reuse the letter geometry; duplicate the path data explicitly instead

## Composition notes
- Keep the word huge, centered, and wide enough to occupy roughly 75–85% of slide width; the effect depends on large letter windows.
- Use a nearly black stage around the letters so the photo-filled typography feels like a bright portal.
- The second Morph slide should use the exact same image, full-bleed, in the same crop/aspect ratio for a smooth zoom illusion.
- Short supporting text belongs below the stencil or in a corner; avoid competing with the central word.