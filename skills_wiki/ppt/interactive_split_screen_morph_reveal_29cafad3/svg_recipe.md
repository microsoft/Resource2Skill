# SVG Recipe — Interactive Split-Screen Morph Reveal

## Visual mechanism
A cinematic 50/50 split-screen menu uses two full-slide photos clipped into opposing halves, with centered editorial typography and glassy “Explore” buttons. The interaction is reproduced in PowerPoint by duplicating this slide, expanding the selected image to full canvas for a Morph transition, then pushing into a detail slide.

## SVG primitives needed
- 2× `<image>` for full-canvas theme photos, each clipped to a left or right half so the same image can later Morph to full-screen
- 2× `<clipPath>` with `<rect>` for the initial half-screen crops
- 2× `<rect>` for dark translucent photo readability overlays
- 2× `<linearGradient>` for subtle cool/warm atmospheric color washes
- 1× `<rect>` for the luminous vertical split divider
- 2× `<rect>` for frosted-glass button cards
- 4× `<text>` blocks for option titles, descriptions, and button labels
- 2× `<path>` for decorative directional chevrons inside the buttons
- 1× `<filter id="softShadow">` applied to buttons and text panels
- 1× `<filter id="seamGlow">` applied to the center divider
- Optional duplicate slides outside SVG: same image IDs/positions, but adjusted clip dimensions to create Morph targets

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="clipLeft">
      <rect x="0" y="0" width="640" height="720"/>
    </clipPath>
    <clipPath id="clipRight">
      <rect x="640" y="0" width="640" height="720"/>
    </clipPath>

    <linearGradient id="coolWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#dff6ff" stop-opacity="0.28"/>
      <stop offset="55%" stop-color="#10243f" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#020816" stop-opacity="0.42"/>
    </linearGradient>
    <linearGradient id="warmWash" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffdd9b" stop-opacity="0.32"/>
      <stop offset="55%" stop-color="#7a3f17" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#150804" stop-opacity="0.46"/>
    </linearGradient>
    <linearGradient id="glassFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.44"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.16"/>
    </linearGradient>
    <linearGradient id="dividerGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="20%" stop-color="#ffffff" stop-opacity="0.65"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="80%" stop-color="#ffffff" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="seamGlow" x="-200%" y="-20%" width="500%" height="140%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0a0d12"/>

  <image id="themeSnowImage" href="https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?auto=format&amp;fit=crop&amp;w=1600&amp;q=80"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipLeft)"/>
  <image id="themeDesertImage" href="https://images.unsplash.com/photo-1509316785289-025f5b846b35?auto=format&amp;fit=crop&amp;w=1600&amp;q=80"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipRight)"/>

  <rect x="0" y="0" width="640" height="720" fill="url(#coolWash)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#warmWash)"/>
  <rect x="0" y="0" width="640" height="720" fill="#001429" opacity="0.16"/>
  <rect x="640" y="0" width="640" height="720" fill="#2a1000" opacity="0.14"/>

  <rect x="638.5" y="70" width="3" height="580" rx="1.5" fill="url(#dividerGrad)" filter="url(#seamGlow)"/>
  <rect x="639.5" y="0" width="1" height="720" fill="#ffffff" opacity="0.45"/>

  <text x="90" y="92" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" letter-spacing="4"
        fill="#e9f8ff" opacity="0.86">CHOOSE YOUR PATH</text>
  <text x="730" y="92" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" letter-spacing="4"
        fill="#fff1db" opacity="0.86">CHOOSE YOUR PATH</text>

  <text x="80" y="285" width="480" font-family="Georgia, Garamond, serif" font-size="62" letter-spacing="7"
        fill="#ffffff" text-anchor="middle" transform="translate(240 0)" filter="url(#softShadow)">ARCTIC</text>
  <text x="80" y="345" width="480" font-family="Georgia, Garamond, serif" font-size="62" letter-spacing="7"
        fill="#ffffff" text-anchor="middle" transform="translate(240 0)" filter="url(#softShadow)">EDGE</text>

  <text x="155" y="398" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#edf8ff" text-anchor="middle" opacity="0.92">
    <tspan x="320" dy="0">A precision route for teams that need</tspan>
    <tspan x="320" dy="28">clarity, resilience, and clean execution.</tspan>
  </text>

  <rect x="220" y="468" width="200" height="54" rx="27" fill="url(#glassFill)" stroke="#ffffff" stroke-opacity="0.72"
        stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="250" y="502" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        font-weight="700" letter-spacing="2" fill="#ffffff">EXPLORE</text>
  <path d="M378 486 L394 495 L378 504" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="720" y="285" width="480" font-family="Georgia, Garamond, serif" font-size="62" letter-spacing="7"
        fill="#ffffff" text-anchor="middle" transform="translate(240 0)" filter="url(#softShadow)">DESERT</text>
  <text x="720" y="345" width="480" font-family="Georgia, Garamond, serif" font-size="62" letter-spacing="7"
        fill="#ffffff" text-anchor="middle" transform="translate(240 0)" filter="url(#softShadow)">SIGNAL</text>

  <text x="795" y="398" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#fff3df" text-anchor="middle" opacity="0.92">
    <tspan x="960" dy="0">A bold route for brands seeking scale,</tspan>
    <tspan x="960" dy="28">momentum, and market heat.</tspan>
  </text>

  <rect x="860" y="468" width="200" height="54" rx="27" fill="url(#glassFill)" stroke="#ffffff" stroke-opacity="0.72"
        stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="890" y="502" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        font-weight="700" letter-spacing="2" fill="#ffffff">EXPLORE</text>
  <path d="M1018 486 L1034 495 L1018 504" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="470" y="666" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12"
        fill="#ffffff" opacity="0.68" text-anchor="middle" transform="translate(170 0)">
    Select a path to expand the scene
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the reveal; create the motion with PowerPoint Morph/Push transitions between duplicated slides instead
- ❌ `<mask>` for photo fades; use clipped images plus translucent gradient rectangles
- ❌ Applying `clip-path` to text, groups, or decorative shapes; keep clipping only on `<image>` elements
- ❌ `<use>` or `<symbol>` for repeated buttons/icons; duplicate the actual SVG primitives
- ❌ Arrow markers on paths for button chevrons; draw chevrons as simple stroked `<path>` geometry
- ❌ Filters on `<line>` elements; use thin `<rect>` elements for glowing dividers

## Composition notes
- Keep the first slide perfectly symmetrical: each theme owns exactly 640 px of the 1280 px canvas, with titles centered inside each half.
- For Morph targets, duplicate the slide and keep the selected image at `x=0 y=0 width=1280 height=720`; change its clip to full canvas while reducing the other image crop to zero width or moving it fully off-canvas.
- Buttons should sit below the description, not at the bottom edge, so users perceive them as interactive choices rather than footer navigation.
- Use color washes sampled from each photo: cool blue/black on one side, amber/brown on the other, with a bright central seam to dramatize the split.