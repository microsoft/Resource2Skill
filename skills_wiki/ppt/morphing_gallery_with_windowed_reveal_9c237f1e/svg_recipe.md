# SVG Recipe — Morphing Gallery with Windowed Reveal

## Visual mechanism
A cinematic full-bleed image sits behind a dark readability gradient, while several tall rounded “window” crops reveal bright duplicate slices of the same image on the right. Across Morph-transition slides, keep the same object IDs/order but change the background image, window heights/positions, and active thumbnail size to create a fluid gallery reveal.

## SVG primitives needed
- 1× full-slide `<image>` for the base hero background.
- 6× rounded-rectangle `<clipPath>` definitions for vertical reveal windows.
- 6× clipped duplicate `<image>` elements for the bright window reveals.
- 6× `<rect>` elements behind/on top of windows for soft shadowed glass edges.
- 1× full-slide `<rect>` with `<linearGradient>` fill for the left-side dark readability overlay.
- 5× circular `<clipPath>` definitions for navigation thumbnails.
- 5× clipped thumbnail `<image>` elements for the gallery navigation rail.
- 5× `<circle>` elements for thumbnail rings, active-state emphasis, and soft shadows.
- 1× `<filter id="windowShadow">` for elevated window depth.
- 1× `<filter id="thumbShadow">` for floating circular thumbnails.
- 1× `<filter id="textGlow">` for subtle premium text separation from the photo.
- Multiple `<text>` and `<tspan>` elements with explicit `width` attributes for title, metadata, and body copy.
- 2× decorative `<path>` elements for fine-line editorial accents.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#02040A" stop-opacity="0.94"/>
      <stop offset="42%" stop-color="#02040A" stop-opacity="0.68"/>
      <stop offset="72%" stop-color="#02040A" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#02040A" stop-opacity="0"/>
    </linearGradient>

    <filter id="windowShadow" x="-30%" y="-20%" width="160%" height="140%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="thumbShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-10%" width="120%" height="140%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="win1"><rect x="548" y="118" width="86" height="438" rx="43"/></clipPath>
    <clipPath id="win2"><rect x="660" y="82" width="86" height="548" rx="43"/></clipPath>
    <clipPath id="win3"><rect x="772" y="154" width="86" height="386" rx="43"/></clipPath>
    <clipPath id="win4"><rect x="884" y="64" width="86" height="586" rx="43"/></clipPath>
    <clipPath id="win5"><rect x="996" y="132" width="86" height="454" rx="43"/></clipPath>
    <clipPath id="win6"><rect x="1108" y="190" width="86" height="326" rx="43"/></clipPath>

    <clipPath id="thumb1"><circle cx="92" cy="118" r="42"/></clipPath>
    <clipPath id="thumb2"><circle cx="92" cy="218" r="27"/></clipPath>
    <clipPath id="thumb3"><circle cx="92" cy="300" r="27"/></clipPath>
    <clipPath id="thumb4"><circle cx="92" cy="382" r="27"/></clipPath>
    <clipPath id="thumb5"><circle cx="92" cy="464" r="27"/></clipPath>
  </defs>

  <image id="bg_photo" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="548" y="118" width="86" height="438" rx="43" fill="#FFFFFF" opacity="0.08" filter="url(#windowShadow)"/>
  <rect x="660" y="82" width="86" height="548" rx="43" fill="#FFFFFF" opacity="0.08" filter="url(#windowShadow)"/>
  <rect x="772" y="154" width="86" height="386" rx="43" fill="#FFFFFF" opacity="0.08" filter="url(#windowShadow)"/>
  <rect x="884" y="64" width="86" height="586" rx="43" fill="#FFFFFF" opacity="0.08" filter="url(#windowShadow)"/>
  <rect x="996" y="132" width="86" height="454" rx="43" fill="#FFFFFF" opacity="0.08" filter="url(#windowShadow)"/>
  <rect x="1108" y="190" width="86" height="326" rx="43" fill="#FFFFFF" opacity="0.08" filter="url(#windowShadow)"/>

  <image id="reveal_01" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#win1)"/>
  <image id="reveal_02" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#win2)"/>
  <image id="reveal_03" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#win3)"/>
  <image id="reveal_04" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#win4)"/>
  <image id="reveal_05" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#win5)"/>
  <image id="reveal_06" href="https://images.example.com/gallery/arctic-glass-modern-architecture-wide.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#win6)"/>

  <rect x="548" y="118" width="86" height="438" rx="43" fill="none" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1.4"/>
  <rect x="660" y="82" width="86" height="548" rx="43" fill="none" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1.4"/>
  <rect x="772" y="154" width="86" height="386" rx="43" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1.4"/>
  <rect x="884" y="64" width="86" height="586" rx="43" fill="none" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1.4"/>
  <rect x="996" y="132" width="86" height="454" rx="43" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1.4"/>
  <rect x="1108" y="190" width="86" height="326" rx="43" fill="none" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="1.4"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#leftFade)"/>

  <circle cx="92" cy="118" r="46" fill="#FFFFFF" opacity="0.16" filter="url(#thumbShadow)"/>
  <image href="https://images.example.com/gallery/arctic-glass-modern-architecture-square.jpg" x="50" y="76" width="84" height="84" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumb1)"/>
  <circle cx="92" cy="118" r="43" fill="none" stroke="#FFFFFF" stroke-width="3.5"/>

  <circle cx="92" cy="218" r="29" fill="#FFFFFF" opacity="0.10" filter="url(#thumbShadow)"/>
  <image href="https://images.example.com/gallery/desert-solar-field-square.jpg" x="65" y="191" width="54" height="54" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumb2)"/>
  <circle cx="92" cy="300" r="29" fill="#FFFFFF" opacity="0.10" filter="url(#thumbShadow)"/>
  <image href="https://images.example.com/gallery/city-night-transport-square.jpg" x="65" y="273" width="54" height="54" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumb3)"/>
  <circle cx="92" cy="382" r="29" fill="#FFFFFF" opacity="0.10" filter="url(#thumbShadow)"/>
  <image href="https://images.example.com/gallery/forest-research-lab-square.jpg" x="65" y="355" width="54" height="54" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumb4)"/>
  <circle cx="92" cy="464" r="29" fill="#FFFFFF" opacity="0.10" filter="url(#thumbShadow)"/>
  <image href="https://images.example.com/gallery/ocean-wind-platform-square.jpg" x="65" y="437" width="54" height="54" preserveAspectRatio="xMidYMid slice" clip-path="url(#thumb5)"/>

  <path d="M154 116 C238 86 326 88 405 124" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.2"/>
  <path d="M154 578 C244 612 338 602 430 548" fill="none" stroke="#7DD3FC" stroke-opacity="0.30" stroke-width="1.2"/>

  <text x="154" y="120" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#A7F3D0" letter-spacing="2.6">GALLERY 01 / SPATIAL MEMORY</text>
  <text x="154" y="234" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="800" fill="#FFFFFF" filter="url(#textGlow)">
    <tspan x="154" dy="0">Windowed</tspan>
    <tspan x="154" dy="70">Reveal</tspan>
  </text>
  <text x="156" y="348" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" fill="#E5E7EB" opacity="0.92">
    <tspan x="156" dy="0">A morphing image sequence where</tspan>
    <tspan x="156" dy="29">vertical apertures resize between</tspan>
    <tspan x="156" dy="29">slides, exposing cinematic fragments</tspan>
    <tspan x="156" dy="29">of the scene behind the narrative.</tspan>
  </text>
  <text x="156" y="540" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#FFFFFF" opacity="0.62">KEEP IDS CONSTANT BETWEEN SLIDES · CHANGE WINDOW HEIGHTS · APPLY POWERPOINT MORPH</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; the motion must come from PowerPoint Morph between separate slides.
- ❌ `<mask>` for the reveal windows; use clipped duplicate `<image>` elements instead.
- ❌ Applying `clip-path` to `<rect>` or `<path>` for the window effect; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ `<use>` or `<symbol>` for repeated thumbnails/windows; duplicate the shapes explicitly so Morph can track them.
- ❌ `skewX`, `skewY`, or matrix transforms for angled gallery motion; use only translate/scale/rotate if you need variation.
- ❌ Filters on `<line>` elements; use filtered circles/rectangles/paths for shadows and glows.

## Composition notes
- Reserve the left 30–35% for navigation and copy; the dark gradient should be strongest there and fade before the reveal windows.
- The right 60% is the visual stage: stagger six rounded windows with varied heights so Morph has visible vertical motion between slides.
- For a multi-slide sequence, keep all object IDs, order, and approximate positions consistent; change each `clipPath` rectangle’s y/height, swap the image URLs, and enlarge the active thumbnail.
- Use bright window slices against a dimmed full-bleed base photo to create the illusion of “background-filled” PowerPoint windows while remaining SVG/PPTX editable.