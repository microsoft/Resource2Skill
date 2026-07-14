# SVG Recipe — Cinematic Spatial Morph Timeline

## Visual mechanism
Create the illusion of a camera panning across one vast horizontal timeline: the current event is centered while previous and next events remain partially or fully off-canvas. Across slides, keep the same objects and shift their x-positions so PowerPoint Morph preserves spatial continuity.

## SVG primitives needed
- 1× `<rect>` for the pure black stage background
- 1× `<image>` for a dim archival / documentary photo texture
- 1× `<rect>` overlay for darkening the image into the background
- 1× `<radialGradient>` for a cinematic vignette wash
- 1× `<linearGradient>` for a faint gold timeline glow
- 1× `<filter id="softShadow">` applied to text panels / plaques
- 1× `<filter id="nodeGlow">` applied to timeline nodes
- 1× `<clipPath>` with rounded rect for the archival image crop
- 1× long `<line>` for the continuous timeline spine extending off-slide
- 4× `<circle>` for timeline nodes, including off-canvas nodes
- 3× `<rect>` for translucent text plaques around events
- 9× `<text>` blocks for dates, titles, descriptions, and cinematic chapter labeling
- 2× `<path>` for subtle decorative cinematic flourishes / dust scratches

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="archiveCrop">
      <rect x="0" y="0" width="1280" height="300" rx="0"/>
    </clipPath>

    <radialGradient id="vignette" cx="50%" cy="46%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.92"/>
    </radialGradient>

    <linearGradient id="timelineGlow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="20%" stop-color="#d6c2a1" stop-opacity="0.36"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="1"/>
      <stop offset="80%" stop-color="#d6c2a1" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="nodeGlow" x="-250%" y="-250%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <!-- cinematic black stage -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <!-- dim archival memory band; can be removed on pure timeline slides -->
  <image href="https://images.example.com/archival-roman-stone-city-panorama.jpg"
         x="0" y="0" width="1280" height="300" preserveAspectRatio="xMidYMid slice"
         opacity="0.32" clip-path="url(#archiveCrop)"/>
  <rect x="0" y="0" width="1280" height="300" fill="#000000" opacity="0.68"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- subtle film scratches / dust -->
  <path d="M118 83 C174 70, 216 91, 278 78 S397 61, 468 74"
        fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="0.7"/>
  <path d="M1012 42 C1048 86, 1038 139, 1078 188 S1138 254, 1121 306"
        fill="none" stroke="#d6c2a1" stroke-opacity="0.09" stroke-width="0.8"/>

  <!-- chapter label -->
  <text x="72" y="86" width="520" fill="#d6c2a1"
        font-family="Georgia, 'Times New Roman', serif" font-size="13"
        letter-spacing="5" opacity="0.86">CHAPTER II  ·  THE TURNING POINT</text>

  <text x="72" y="128" width="680" fill="#ffffff"
        font-family="Georgia, 'Times New Roman', serif" font-size="34"
        letter-spacing="7" opacity="0.92">A CONTINUOUS HISTORY</text>

  <!-- the spatial world: previous, current, and next nodes occupy one huge canvas -->
  <g id="spatial-timeline-world">
    <!-- timeline spine extends far beyond the 1280px viewport -->
    <line x1="-820" y1="360" x2="2140" y2="360"
          stroke="url(#timelineGlow)" stroke-width="1.25"/>

    <!-- previous event, intentionally off-canvas left for Morph continuity -->
    <circle id="node-753bce-glow" cx="-380" cy="360" r="13" fill="#ffffff" opacity="0.22" filter="url(#nodeGlow)"/>
    <circle id="node-753bce" cx="-380" cy="360" r="5.5" fill="#ffffff"/>
    <text id="date-753bce" x="-520" y="322" width="280" fill="#d6c2a1"
          font-family="Georgia, 'Times New Roman', serif" font-size="18"
          letter-spacing="2">753 BCE</text>
    <text id="title-753bce" x="-520" y="400" width="320" fill="#ffffff"
          font-family="Georgia, 'Times New Roman', serif" font-size="27">ROME IS FOUNDED</text>

    <!-- centered current event -->
    <circle id="node-509bce-glow" cx="640" cy="360" r="22" fill="#ffffff" opacity="0.22" filter="url(#nodeGlow)"/>
    <circle id="node-509bce" cx="640" cy="360" r="7" fill="#ffffff"/>

    <rect id="panel-509bce" x="432" y="408" width="416" height="164" rx="18"
          fill="#090807" stroke="#d6c2a1" stroke-opacity="0.24" filter="url(#softShadow)" opacity="0.96"/>
    <text id="date-509bce" x="474" y="456" width="330" fill="#d6c2a1"
          font-family="Georgia, 'Times New Roman', serif" font-size="20"
          letter-spacing="3">509 BCE</text>
    <text id="title-509bce" x="474" y="496" width="330" fill="#ffffff"
          font-family="Georgia, 'Times New Roman', serif" font-size="28"
          letter-spacing="1">THE REPUBLIC RISES</text>
    <text id="desc-509bce" x="474" y="532" width="335" fill="#cfc7bb"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" opacity="0.86">
      <tspan x="474" dy="0">Power shifts from kings to elected offices,</tspan>
      <tspan x="474" dy="22">establishing a civic structure that will</tspan>
      <tspan x="474" dy="22">shape centuries of expansion.</tspan>
    </text>

    <!-- next event, staged off-canvas right so Morph can pull it into frame -->
    <circle id="node-27bce-glow" cx="1660" cy="360" r="13" fill="#ffffff" opacity="0.22" filter="url(#nodeGlow)"/>
    <circle id="node-27bce" cx="1660" cy="360" r="5.5" fill="#ffffff"/>
    <rect id="panel-27bce-preview" x="1506" y="174" width="360" height="118" rx="16"
          fill="#080706" stroke="#ffffff" stroke-opacity="0.14" opacity="0.78"/>
    <text id="date-27bce" x="1540" y="224" width="280" fill="#d6c2a1"
          font-family="Georgia, 'Times New Roman', serif" font-size="18"
          letter-spacing="3">27 BCE</text>
    <text id="title-27bce" x="1540" y="260" width="310" fill="#ffffff"
          font-family="Georgia, 'Times New Roman', serif" font-size="26">EMPIRE BEGINS</text>

    <!-- far-future node as a faint promise beyond the next slide -->
    <circle id="node-117ce" cx="2140" cy="360" r="4.5" fill="#ffffff" opacity="0.42"/>
  </g>

  <!-- bottom caption / direction cue -->
  <text x="470" y="654" width="340" fill="#ffffff"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12"
        letter-spacing="4" text-anchor="middle" opacity="0.44">THE CAMERA CONTINUES EAST</text>
  <line x1="675" y1="650" x2="810" y2="650" stroke="#ffffff" stroke-width="1" opacity="0.32"/>
</svg>
```

## Avoid in this skill
- ❌ Treating each slide as a separate timeline layout; the Morph illusion depends on preserving one continuous horizontal world.
- ❌ Rebuilding nodes as new objects on each slide; keep matching IDs/object names and only change their positions.
- ❌ Using `marker-end` on paths for directional arrows; if needed, draw arrows with editable `<line>` elements and separate triangle/path heads.
- ❌ Applying filters to `<line>` timeline spines; glows/shadows on lines may be dropped, so use gradient strokes or nearby blurred circles instead.
- ❌ Clipping text or shapes; only use `clipPath` on `<image>` elements.
- ❌ Filling the slide with dense labels; the premium cinematic feel comes from sparse information and deep black negative space.

## Composition notes
- Keep the timeline spine near vertical center, with the active node exactly around x=640; previous and next nodes should sit far off-canvas so Morph feels like a camera pan.
- Use large black negative space and only one fully readable event per slide; adjacent events can be partial previews.
- Maintain a restrained palette: black, white, muted sand/gold, and faint archival imagery.
- For a sequence, export one SVG per slide with the same objects shifted left by a constant distance; apply PowerPoint Morph between slides for spatial continuity.