# SVG Recipe — Layered Chevron Title Layout

## Visual mechanism
A full-bleed city image is clipped into a broad right-pointing chevron, then stacked with oversized concave chevron bands in black and yellow to create forward momentum. Large title typography sits safely on the left over the photo, while the angled bands push the eye toward the right side of the slide.

## SVG primitives needed
- 1× `<rect>` for the dark navy slide background
- 1× `<image>` clipped to a custom chevron photo shape
- 1× `<clipPath>` with a `<path>` for the photo chevron crop
- 2× large `<path>` concave chevron bands for the black and yellow forward arrows
- 1× translucent `<path>` for the pale blue internal arrow overlay on top of the photo
- 1× semi-transparent `<rect>` for the lower title contrast strip
- 1× `<linearGradient>` for the yellow chevron highlight
- 1× `<linearGradient>` for the subtle navy background depth
- 2× `<filter>` shadows applied to chevron paths for dimensional layering
- 4× `<text>` elements for year, subtitle, and stacked section title

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#273342"/>
      <stop offset="55%" stop-color="#202a37"/>
      <stop offset="100%" stop-color="#16202d"/>
    </linearGradient>

    <linearGradient id="yellowSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffe25a"/>
      <stop offset="35%" stop-color="#ffd200"/>
      <stop offset="70%" stop-color="#f2c200"/>
      <stop offset="100%" stop-color="#c99700"/>
    </linearGradient>

    <linearGradient id="blackBand" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2c2c2c"/>
      <stop offset="45%" stop-color="#171717"/>
      <stop offset="100%" stop-color="#080808"/>
    </linearGradient>

    <filter id="softDropShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="14" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="deepChevronShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="-10" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoChevronClip">
      <path d="M0 0 L672 0 L930 360 L672 720 L0 720 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#navyDepth)"/>

  <image
    x="0" y="0" width="960" height="720"
    href="https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&amp;w=1600&amp;auto=format&amp;fit=crop"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoChevronClip)"/>

  <path d="M690 0 L862 0 L1268 360 L862 720 L690 720 L1096 360 Z"
        fill="url(#yellowSheen)"
        filter="url(#softDropShadow)"/>

  <path d="M520 0 L692 0 L1096 360 L692 720 L520 720 L924 360 Z"
        fill="url(#blackBand)"
        filter="url(#deepChevronShadow)"/>

  <path d="M16 86 L328 86 L328 30 L660 360 L328 690 L328 618 L16 618 Z"
        fill="#b8efff"
        opacity="0.58"/>

  <path d="M0 0 L520 0 L650 120 L650 0 Z"
        fill="#0014b8"
        opacity="0.72"/>

  <rect x="16" y="407" width="635" height="86" fill="#111111" opacity="0.42"/>

  <text x="64" y="255" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="158"
        font-weight="800"
        fill="#ffffff"
        letter-spacing="3">2019</text>

  <text x="93" y="364" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29"
        font-weight="500"
        fill="#111820">Enter your text here</text>

  <text x="58" y="492" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58"
        font-weight="800"
        fill="#ffffff"
        letter-spacing="2">TITLE SLIDE</text>

  <text x="58" y="579" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58"
        font-weight="800"
        fill="#ffffff"
        letter-spacing="2">INTRO</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the chevron photo crop; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not try to build the chevrons with skew transforms; draw the angled geometry directly with `<path d="...">`.
- ❌ Do not use `<pattern>` fills for the chevron bands; use solid fills or gradients so they remain editable.
- ❌ Do not apply filters to `<line>` elements; shadows should be applied to the large chevron `<path>` shapes.
- ❌ Do not rely on `<use>` or `<symbol>` to duplicate chevrons; duplicate the path geometry explicitly.

## Composition notes
- Keep the main title text inside the left 40–45% of the slide, where the photo is brightest and the chevron geometry is least busy.
- Let the black chevron overlap the photo edge; it acts as a strong separator between image and the yellow momentum band.
- The yellow band should extend nearly to the right edge, leaving only a slim dark navy field for contrast.
- Use a cool photo palette with cyan/blue highlights so the mustard yellow chevron becomes the dominant accent.