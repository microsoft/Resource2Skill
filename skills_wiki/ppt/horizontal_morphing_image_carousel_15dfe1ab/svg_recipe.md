# SVG Recipe — Horizontal Morphing Image Carousel

## Visual mechanism
A clean horizontal row of circular photo crops creates a carousel: the active item sits centered, much larger, with bold title text and a crisp outline, while neighboring items shrink and fade into the sides. To reproduce the “morph” feeling in PowerPoint, create one SVG slide per carousel state and keep the same element IDs while changing only x/y/size/text emphasis between states.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 6× `<clipPath>` with `<circle>` for circular image cropping
- 6× `<image>` for topic photos clipped into circles
- 7× `<circle>` for active outline, inactive rims, and progress dots
- 1× `<line>` for the faint horizontal carousel axis
- 7× `<text>` for eyebrow labels, active title, inactive titles, and small instruction copy
- 1× `<filter id="activeShadow">` using `feOffset + feGaussianBlur + feMerge` for the active circle lift
- 1× `<filter id="softGlow">` using `feGaussianBlur` for the pale ambient halo behind the active item
- 1× `<linearGradient>` for subtle side-fade decorative discs behind peripheral items

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="activeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <linearGradient id="sideFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F1F3F5" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="#E9ECEF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#F1F3F5" stop-opacity="0.15"/>
    </linearGradient>

    <clipPath id="clipTopic01"><circle cx="80" cy="430" r="72"/></clipPath>
    <clipPath id="clipTopic02"><circle cx="270" cy="430" r="104"/></clipPath>
    <clipPath id="clipTopic03"><circle cx="640" cy="430" r="180"/></clipPath>
    <clipPath id="clipTopic04"><circle cx="1010" cy="430" r="104"/></clipPath>
    <clipPath id="clipTopic05"><circle cx="1200" cy="430" r="72"/></clipPath>
    <clipPath id="clipTopic06"><circle cx="1380" cy="430" r="58"/></clipPath>
  </defs>

  <rect id="slideBackground" x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text id="carouselKicker" x="80" y="72" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        letter-spacing="2.8" fill="#8A8F98">MORPHING CAROUSEL / NATURE EDITION</text>

  <text id="carouselHint" x="890" y="72" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        text-anchor="end" fill="#9AA0A6">Duplicate slide → move active item → apply Morph</text>

  <line id="carouselAxis" x1="70" y1="430" x2="1210" y2="430"
        stroke="#E6E8EB" stroke-width="2" stroke-dasharray="2 14"/>

  <circle id="ambientHalo" cx="640" cy="430" r="220" fill="#EDF2F7" opacity="0.75" filter="url(#softGlow)"/>
  <circle id="leftAmbientDisc" cx="270" cy="430" r="138" fill="url(#sideFade)"/>
  <circle id="rightAmbientDisc" cx="1010" cy="430" r="138" fill="url(#sideFade)"/>

  <image id="topic01Photo" x="8" y="358" width="144" height="144"
         href="https://images.unsplash.com/photo-1532822160912-78d12fc0c7cb?w=600&q=80"
         clip-path="url(#clipTopic01)" opacity="0.42"/>
  <circle id="topic01Rim" cx="80" cy="430" r="72" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.75"/>

  <image id="topic02Photo" x="166" y="326" width="208" height="208"
         href="https://images.unsplash.com/photo-1550236520-7050f3582da0?w=600&q=80"
         clip-path="url(#clipTopic02)" opacity="0.72"/>
  <circle id="topic02Rim" cx="270" cy="430" r="104" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.9"/>

  <circle id="topic03ShadowCarrier" cx="640" cy="430" r="183" fill="#FFFFFF" filter="url(#activeShadow)"/>
  <image id="topic03Photo" x="460" y="250" width="360" height="360"
         href="https://images.unsplash.com/photo-1484406593171-41b7938c9143?w=900&q=90"
         clip-path="url(#clipTopic03)"/>
  <circle id="topic03ActiveOutline" cx="640" cy="430" r="181" fill="none" stroke="#1B1B1B" stroke-width="3"/>

  <image id="topic04Photo" x="906" y="326" width="208" height="208"
         href="https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600&q=80"
         clip-path="url(#clipTopic04)" opacity="0.72"/>
  <circle id="topic04Rim" cx="1010" cy="430" r="104" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.9"/>

  <image id="topic05Photo" x="1128" y="358" width="144" height="144"
         href="https://images.unsplash.com/photo-1463319611694-4bf9eb5a6e72?w=600&q=80"
         clip-path="url(#clipTopic05)" opacity="0.42"/>
  <circle id="topic05Rim" cx="1200" cy="430" r="72" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.75"/>

  <image id="topic06Photo" x="1322" y="372" width="116" height="116"
         href="https://images.unsplash.com/photo-1552728089-57169264c70a?w=600&q=80"
         clip-path="url(#clipTopic06)" opacity="0.22"/>

  <text id="activeEyebrow" x="420" y="134" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        text-anchor="middle" letter-spacing="3.5" fill="#787878">TOPIC 03</text>
  <text id="activeTitle" x="360" y="180" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="39"
        font-weight="700" text-anchor="middle" fill="#1E1E1E">The Golden Hour Stag</text>

  <text id="topic02Title" x="150" y="608" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        text-anchor="middle" fill="#7C828A">Paper Kite Butterfly</text>
  <text id="topic04Title" x="890" y="608" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        text-anchor="middle" fill="#7C828A">Green Sprout</text>

  <circle id="dot01" cx="580" cy="666" r="4" fill="#CFD4DA"/>
  <circle id="dot02" cx="610" cy="666" r="4" fill="#CFD4DA"/>
  <circle id="dot03" cx="640" cy="666" r="6" fill="#1E1E1E"/>
  <circle id="dot04" cx="670" cy="666" r="4" fill="#CFD4DA"/>
  <circle id="dot05" cx="700" cy="666" r="4" fill="#CFD4DA"/>
</svg>
```

## Avoid in this skill
- ❌ Real SVG animation tags such as `<animate>` or `<animateTransform>`; use separate slides with PowerPoint Morph instead.
- ❌ Applying `clip-path` to circles or groups to create image crops; apply `clip-path` directly to each `<image>`.
- ❌ Using `<use>` to duplicate carousel items; duplicate the actual editable shapes so each item can morph independently.
- ❌ Arrowheads on paths for navigation controls; if arrows are needed, use `<line>` with direct `marker-end`, or build arrowheads from simple paths.
- ❌ Letting inactive images stretch from arbitrary aspect ratios; use square source crops or set equal image width/height inside circular clip paths.

## Composition notes
- Keep the active circle centered horizontally and placed slightly below mid-height, leaving generous space above for the active label and title.
- Peripheral circles should step down in both size and opacity as they approach the slide edges; this creates depth without needing complex 3D effects.
- For Morph slides, preserve the same IDs for each photo, rim, label, and dot, then change only their positions, radii, opacity, and text styling.
- Use a mostly white background with very pale grey axis/glow elements so the photo colors become the visual rhythm of the carousel.