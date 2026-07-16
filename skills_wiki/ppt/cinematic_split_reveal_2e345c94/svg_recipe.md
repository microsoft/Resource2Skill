# SVG Recipe — Cinematic Split-Reveal

## Visual mechanism
A dramatic horizontal “curtain split” reveals a vivid cinematic image bar, with the title rendered as a photo-filled cutout through a dark central plaque. The composition feels like a film trailer opener: black letterbox fields, glowing edge highlights, and a single monumental word tied directly to the revealed imagery.

## SVG primitives needed
- 1× `<rect>` for the black cinematic background.
- 2× `<rect>` for the top and bottom curtain panels / letterbox fields.
- 1× `<rect>` for the semi-transparent dark title plaque across the image.
- 2× `<image>` using the same photo: one for the revealed horizontal hero bar, one clipped into the title letterforms.
- 1× `<clipPath>` with `<rect>` for cropping the hero image into a wide central bar.
- 1× `<clipPath>` with a combined `<path>` for the photo-filled block-letter title.
- 2× `<path>` using the same letterform path for the title shadow and subtle highlight outline.
- 3× `<linearGradient>` / `<radialGradient>` for background glow, plaque sheen, and curtain edge atmosphere.
- 2× `<filter>` definitions: one soft shadow for the plaque/title depth, one glow for cinematic rim light.
- 4× `<line>` for fine reveal-edge highlights at the curtain boundaries.
- 3× `<text>` elements with explicit `width` attributes for small cinematic metadata and subtitle copy.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="48%" r="62%">
      <stop offset="0%" stop-color="#1c2630"/>
      <stop offset="42%" stop-color="#07090c"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="plaqueSheen" x1="0" y1="285" x2="0" y2="438" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#111820" stop-opacity="0.82"/>
      <stop offset="42%" stop-color="#020305" stop-opacity="0.70"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.86"/>
    </linearGradient>

    <linearGradient id="edgeGlow" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00d8ff" stop-opacity="0"/>
      <stop offset="18%" stop-color="#00d8ff" stop-opacity="0.38"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.72"/>
      <stop offset="82%" stop-color="#ffcf8a" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#ffcf8a" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="rimGlow" x="-20%" y="-60%" width="140%" height="220%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <clipPath id="barClip">
      <rect x="0" y="218" width="1280" height="284"/>
    </clipPath>

    <clipPath id="titleClip">
      <path d="M255 415 L255 305 L274 305 L294 368 L314 305 L333 305 L333 415 L314 415 L314 352 L294 412 L274 352 L274 415 Z
               M353 415 L386 305 L405 305 L372 415 Z M421 415 L388 305 L407 305 L440 415 Z M376 376 L417 376 L422 394 L371 394 Z
               M460 305 L480 305 L480 397 L530 397 L530 415 L460 415 Z
               M550 305 L570 305 L570 415 L550 415 Z M570 305 L608 305 L608 323 L570 323 Z M570 397 L608 397 L608 415 L570 415 Z M608 323 C632 326 642 342 642 360 C642 378 632 394 608 397 L608 377 C618 374 622 368 622 360 C622 352 618 346 608 343 Z
               M662 305 L734 305 L734 323 L708 323 L708 397 L734 397 L734 415 L662 415 L662 397 L688 397 L688 323 L662 323 Z
               M754 305 L775 305 L796 415 L776 415 Z M831 305 L852 305 L830 415 L810 415 Z
               M872 305 L945 305 L945 324 L892 324 L892 350 L938 350 L938 369 L892 369 L892 396 L947 396 L947 415 L872 415 Z
               M970 305 L1046 305 L1046 324 L990 324 L990 349 L1040 349 L1040 415 L970 415 L970 396 L1020 396 L1020 369 L970 369 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <image href="https://images.pexels.com/photos/3889855/pexels-photo-3889855.jpeg"
         x="0" y="190" width="1280" height="340" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#barClip)"/>

  <rect x="0" y="0" width="1280" height="218" fill="#000000"/>
  <rect x="0" y="502" width="1280" height="218" fill="#000000"/>

  <line x1="0" y1="218" x2="1280" y2="218" stroke="url(#edgeGlow)" stroke-width="2"/>
  <line x1="0" y1="502" x2="1280" y2="502" stroke="url(#edgeGlow)" stroke-width="2"/>
  <line x1="0" y1="224" x2="1280" y2="224" stroke="#ffffff" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="0" y1="496" x2="1280" y2="496" stroke="#ffffff" stroke-opacity="0.10" stroke-width="1"/>

  <rect x="164" y="282" width="952" height="156" rx="10" fill="url(#plaqueSheen)" filter="url(#softShadow)"/>

  <path transform="translate(7 9)"
        d="M255 415 L255 305 L274 305 L294 368 L314 305 L333 305 L333 415 L314 415 L314 352 L294 412 L274 352 L274 415 Z M353 415 L386 305 L405 305 L372 415 Z M421 415 L388 305 L407 305 L440 415 Z M376 376 L417 376 L422 394 L371 394 Z M460 305 L480 305 L480 397 L530 397 L530 415 L460 415 Z M550 305 L570 305 L570 415 L550 415 Z M570 305 L608 305 L608 323 L570 323 Z M570 397 L608 397 L608 415 L570 415 Z M608 323 C632 326 642 342 642 360 C642 378 632 394 608 397 L608 377 C618 374 622 368 622 360 C622 352 618 346 608 343 Z M662 305 L734 305 L734 323 L708 323 L708 397 L734 397 L734 415 L662 415 L662 397 L688 397 L688 323 L662 323 Z M754 305 L775 305 L796 415 L776 415 Z M831 305 L852 305 L830 415 L810 415 Z M872 305 L945 305 L945 324 L892 324 L892 350 L938 350 L938 369 L892 369 L892 396 L947 396 L947 415 L872 415 Z M970 305 L1046 305 L1046 324 L990 324 L990 349 L1040 349 L1040 415 L970 415 L970 396 L1020 396 L1020 369 L970 369 Z"
        fill="#000000" opacity="0.58" filter="url(#softShadow)"/>

  <image href="https://images.pexels.com/photos/3889855/pexels-photo-3889855.jpeg"
         x="0" y="190" width="1280" height="340" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#titleClip)"/>

  <path d="M255 415 L255 305 L274 305 L294 368 L314 305 L333 305 L333 415 L314 415 L314 352 L294 412 L274 352 L274 415 Z M353 415 L386 305 L405 305 L372 415 Z M421 415 L388 305 L407 305 L440 415 Z M376 376 L417 376 L422 394 L371 394 Z M460 305 L480 305 L480 397 L530 397 L530 415 L460 415 Z M550 305 L570 305 L570 415 L550 415 Z M570 305 L608 305 L608 323 L570 323 Z M570 397 L608 397 L608 415 L570 415 Z M608 323 C632 326 642 342 642 360 C642 378 632 394 608 397 L608 377 C618 374 622 368 622 360 C622 352 618 346 608 343 Z M662 305 L734 305 L734 323 L708 323 L708 397 L734 397 L734 415 L662 415 L662 397 L688 397 L688 323 L662 323 Z M754 305 L775 305 L796 415 L776 415 Z M831 305 L852 305 L830 415 L810 415 Z M872 305 L945 305 L945 324 L892 324 L892 350 L938 350 L938 369 L892 369 L892 396 L947 396 L947 415 L872 415 Z M970 305 L1046 305 L1046 324 L990 324 L990 349 L1040 349 L1040 415 L970 415 L970 396 L1020 396 L1020 369 L970 369 Z"
        fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="2"/>

  <text x="70" y="78" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" letter-spacing="4" fill="#aeb8c2">SECTION 01 / REVEAL</text>
  <text x="70" y="642" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" letter-spacing="3" fill="#ffffff" opacity="0.72">CINEMATIC DESTINATION OPENER</text>
  <text x="820" y="642" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" letter-spacing="3" text-anchor="end" fill="#ffffff" opacity="0.56">MOTION PATH: SPLIT CURTAINS</text>

  <rect x="164" y="282" width="952" height="156" rx="10" fill="none" stroke="#ffffff" stroke-opacity="0.10"/>
  <rect x="196" y="292" width="888" height="1.5" fill="#ffffff" opacity="0.18" filter="url(#rimGlow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; create the two curtain rectangles as editable objects, then apply PowerPoint motion paths after translation.
- ❌ Do not use `<mask>` to create the text cutout; masks are not safe for the translator. Use an `<image>` clipped by a letterform `<clipPath>` instead.
- ❌ Do not use `<pattern>` fills for image-in-text; pattern fills are silently dropped. Duplicate the same image and clip it into the title shape.
- ❌ Do not apply `clip-path` to the dark plaque or other non-image shapes; clipping is only reliable on `<image>`.
- ❌ Do not rely on normal SVG text for the main photo-filled title if you need the image-window effect; use block letter paths as the image clip.

## Composition notes
- Keep the hero content constrained to a central horizontal band occupying roughly 35–40% of slide height; the black top and bottom fields create the cinematic letterbox.
- The main word should be oversized, centered, and short enough to read instantly; one powerful destination, brand, product, or event name works best.
- Use the same photo for both the central bar and clipped title image so the letters feel like transparent windows through the title plaque.
- For the reveal animation in PowerPoint, start the top curtain and bottom curtain meeting near the slide center, then animate them upward and downward respectively over 2.0–2.5 seconds.