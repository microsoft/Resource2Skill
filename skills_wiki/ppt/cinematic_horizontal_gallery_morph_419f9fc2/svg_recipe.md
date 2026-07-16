# SVG Recipe — Cinematic Horizontal Gallery Morph

## Visual mechanism
A full-bleed cinematic hero image dominates the upper two-thirds of the slide, while a deep-color bottom panel contains a horizontally scrolling thumbnail filmstrip. A circular play button sits in a smooth concave cutout at the panel boundary, making the composition feel like a premium media app; duplicate the slide and shift the filmstrip left to create the Morph animation.

## SVG primitives needed
- 1× `<image>` for the full-slide hero photograph
- 1× `<rect>` with gradient fill for the dark readability overlay on the hero
- 1× `<path>` for the bottom panel with a semicircular concave cutout
- 5× `<image>` for horizontal gallery thumbnails
- 5× `<clipPath>` with rounded `<rect>` crops applied to thumbnail images
- 5× `<rect>` thumbnail border/highlight overlays
- 1× `<circle>` for the floating play button
- 1× `<path>` for the play triangle icon
- 2× `<text>` blocks for the cinematic headline and supporting copy
- 1× `<filter id="softShadow">` applied to panel/button/card shapes
- 1× `<filter id="titleGlow">` applied to large title text
- 2× `<linearGradient>` definitions for hero vignette and active-thumbnail sheen

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#050614" stop-opacity="0.30"/>
      <stop offset="48%" stop-color="#050614" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#050614" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="thumbSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-15%" y="-15%" width="130%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipThumb01"><rect x="456" y="532" width="228" height="128" rx="18"/></clipPath>
    <clipPath id="clipThumb02"><rect x="710" y="532" width="228" height="128" rx="18"/></clipPath>
    <clipPath id="clipThumb03"><rect x="964" y="532" width="228" height="128" rx="18"/></clipPath>
    <clipPath id="clipThumb04"><rect x="1218" y="532" width="228" height="128" rx="18"/></clipPath>
    <clipPath id="clipThumb05"><rect x="1472" y="532" width="228" height="128" rx="18"/></clipPath>
  </defs>

  <!-- Hero layer: change this href on the next Morph slide to match the newly active thumbnail -->
  <image x="0" y="0" width="1280" height="720"
         href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1920&amp;h=1080&amp;fit=crop"
         preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="520" fill="url(#heroVignette)"/>

  <!-- Cinematic headline -->
  <text x="640" y="205" width="980"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="114"
        font-weight="800"
        letter-spacing="10"
        fill="#FFFFFF"
        filter="url(#titleGlow)">TRAVEL</text>

  <text x="640" y="272" width="560"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20"
        font-weight="400"
        fill="#FFFFFF"
        opacity="0.88">
    <tspan x="640" dy="0">Four cinematic routes through wild coastlines, alpine air,</tspan>
    <tspan x="640" dy="28">golden deserts, and forest lodges.</tspan>
  </text>

  <!-- Bottom panel with concave circular cutout for the play button -->
  <path d="M0 470 H246
           A74 74 0 0 1 394 470
           H1280 V720 H0 Z"
        fill="#24225B"
        filter="url(#softShadow)"/>

  <!-- Small metadata in lower panel -->
  <text x="78" y="580" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="700"
        letter-spacing="2"
        fill="#A8A7D8">EPISODE 01</text>
  <text x="78" y="616" width="275"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31"
        font-weight="700"
        fill="#FFFFFF">Alpine Dawn</text>
  <text x="78" y="648" width="280"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        fill="#C8C7EA">Swipe the gallery with Morph.</text>

  <!-- Floating play button -->
  <circle cx="320" cy="470" r="52" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="320" cy="470" r="43" fill="#FFFFFF" stroke="#E9E8FF" stroke-width="2"/>
  <path d="M305 444 L305 496 L350 470 Z" fill="#24225B"/>

  <!-- Filmstrip: on the next slide, translate this group left by 254px -->
  <g id="filmstrip_state_01">
    <rect x="446" y="522" width="248" height="148" rx="24" fill="#11103E" opacity="0.34" filter="url(#softShadow)"/>
    <image x="456" y="532" width="228" height="128"
           href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800&amp;h=450&amp;fit=crop"
           preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb01)"/>
    <rect x="456" y="532" width="228" height="128" rx="18" fill="url(#thumbSheen)"/>
    <rect x="456" y="532" width="228" height="128" rx="18" fill="none" stroke="#FFFFFF" stroke-width="4"/>

    <image x="710" y="532" width="228" height="128"
           href="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&amp;h=450&amp;fit=crop"
           preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb02)"/>
    <rect x="710" y="532" width="228" height="128" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>

    <image x="964" y="532" width="228" height="128"
           href="https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&amp;h=450&amp;fit=crop"
           preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb03)"/>
    <rect x="964" y="532" width="228" height="128" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>

    <image x="1218" y="532" width="228" height="128"
           href="https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800&amp;h=450&amp;fit=crop"
           preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb04)"/>
    <rect x="1218" y="532" width="228" height="128" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>

    <image x="1472" y="532" width="228" height="128"
           href="https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800&amp;h=450&amp;fit=crop"
           preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb05)"/>
    <rect x="1472" y="532" width="228" height="128" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to subtract the play-button cutout; build the bottom panel as a single editable `<path>` with an arc.
- ❌ Do not apply `clip-path` to thumbnail border rectangles; apply clips only to the `<image>` elements, then draw editable rounded `<rect>` borders above them.
- ❌ Do not use `<animate>` or `<animateTransform>` for the gallery motion; create two PowerPoint slides and use PowerPoint Morph.
- ❌ Do not use `<use>` for repeated thumbnail cards; duplicate the editable shapes so Morph can interpolate positions reliably.
- ❌ Do not use `marker-end` arrows for navigation cues; if arrows are needed, draw them as editable `<line>` plus `<path>` triangle shapes.

## Composition notes
- Keep the hero image dominant: roughly the top 65–70% of the slide should feel photographic, emotional, and uncluttered.
- The bottom panel should occupy about one-third of the slide and use a saturated dark color that contrasts strongly with the hero image.
- For Morph, duplicate the slide, preserve the same filmstrip objects, then shift every thumbnail and border left by one card pitch, e.g. `254px`; update the hero image to the newly active thumbnail.
- Place the play button on the split line, centered in the panel cutout, so it visually bridges the cinematic image and the interactive gallery.