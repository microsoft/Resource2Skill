# SVG Recipe — Split-Panel Edge-Bleed Agenda

## Visual mechanism
A full-height image panel bleeds off the left edge while agenda nodes sit precisely on the vertical seam between photo and white space. Thin horizontal connectors extend from each seam node into the clean text field, creating an editorial bridge between emotional imagery and structured agenda content.

## SVG primitives needed
- 1× `<image>` for the full-height edge-bleed hero/photo panel
- 1× `<clipPath>` with `<rect>` for cropping the photo to the left panel
- 2× `<rect>` for the right content background and dark translucent title overlay
- 1× `<linearGradient>` for a subtle right-panel paper-like background
- 1× `<filter id="nodeShadow">` applied to agenda nodes for a soft premium lift
- 5× `<circle>` for colored seam agenda nodes with thick white strokes
- 5× `<line>` for thin horizontal agenda connectors
- 10× `<text>` for agenda headers and descriptions
- 1× large `<text>` for the image-panel slide title
- 1× small `<text>` for an eyebrow label / meeting context
- Optional decorative `<path>` accents on the photo panel for editorial polish

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoClip">
      <rect x="0" y="0" width="448" height="720"/>
    </clipPath>

    <linearGradient id="rightPaper" x1="448" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.58" stop-color="#F7F8FA"/>
      <stop offset="1" stop-color="#EEF1F5"/>
    </linearGradient>

    <linearGradient id="photoShade" x1="0" y1="0" x2="448" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F" stop-opacity="0.05"/>
      <stop offset="0.55" stop-color="#07111F" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#07111F" stop-opacity="0.45"/>
    </linearGradient>

    <filter id="nodeShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Left edge-bleed image panel -->
  <image x="0" y="0" width="448" height="720"
         href="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1100&auto=format&fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoClip)"/>
  <rect x="0" y="0" width="448" height="720" fill="url(#photoShade)"/>

  <!-- Right negative-space panel -->
  <rect x="448" y="0" width="832" height="720" fill="url(#rightPaper)"/>
  <rect x="447" y="0" width="2" height="720" fill="#FFFFFF" opacity="0.9"/>

  <!-- Subtle editorial photo accents -->
  <path d="M34 0 L72 0 L420 720 L382 720 Z" fill="#FFFFFF" opacity="0.08"/>
  <path d="M0 572 L448 438 L448 720 L0 720 Z" fill="#000000" opacity="0.18"/>

  <!-- Title block over image -->
  <rect x="0" y="438" width="448" height="132" fill="#000000" opacity="0.66"/>
  <text x="48" y="491" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="600" fill="#BFD7FF" letter-spacing="2">EXECUTIVE SESSION</text>
  <text x="48" y="546" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#FFFFFF">Agenda</text>

  <!-- Right panel heading -->
  <text x="548" y="80" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#7C8794" letter-spacing="2">TODAY'S DISCUSSION FLOW</text>
  <text x="548" y="122" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#1E2732">Meeting agenda</text>

  <!-- Agenda item 01 -->
  <line x1="482" y1="176" x2="1110" y2="176" stroke="#D9DEE7" stroke-width="2"/>
  <circle cx="448" cy="176" r="22" fill="#592B91" stroke="#FFFFFF" stroke-width="8" filter="url(#nodeShadow)"/>
  <text x="438" y="183" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#FFFFFF">01</text>
  <text x="548" y="162" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#592B91">Organization Structure</text>
  <text x="548" y="201" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#5D6673">Review team alignment, reporting lines, and operating rhythm for the next quarter.</text>

  <!-- Agenda item 02 -->
  <line x1="482" y1="268" x2="1110" y2="268" stroke="#D9DEE7" stroke-width="2"/>
  <circle cx="448" cy="268" r="22" fill="#3465A4" stroke="#FFFFFF" stroke-width="8" filter="url(#nodeShadow)"/>
  <text x="438" y="275" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#FFFFFF">02</text>
  <text x="548" y="254" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#3465A4">Action Items</text>
  <text x="548" y="293" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#5D6673">Confirm owners, timing, and dependencies for open deliverables from the last session.</text>

  <!-- Agenda item 03 -->
  <line x1="482" y1="360" x2="1110" y2="360" stroke="#D9DEE7" stroke-width="2"/>
  <circle cx="448" cy="360" r="22" fill="#73D216" stroke="#FFFFFF" stroke-width="8" filter="url(#nodeShadow)"/>
  <text x="438" y="367" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#FFFFFF">03</text>
  <text x="548" y="346" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#4F9F10">Key Updates</text>
  <text x="548" y="385" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#5D6673">Share recent product launches, customer signals, and market movement since Q2 close.</text>

  <!-- Agenda item 04 -->
  <line x1="482" y1="452" x2="1110" y2="452" stroke="#D9DEE7" stroke-width="2"/>
  <circle cx="448" cy="452" r="22" fill="#CC0000" stroke="#FFFFFF" stroke-width="8" filter="url(#nodeShadow)"/>
  <text x="438" y="459" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#FFFFFF">04</text>
  <text x="548" y="438" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#CC0000">Head Count</text>
  <text x="548" y="477" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#5D6673">Review current capacity, critical role coverage, and approved hiring priorities.</text>

  <!-- Agenda item 05 -->
  <line x1="482" y1="544" x2="1110" y2="544" stroke="#D9DEE7" stroke-width="2"/>
  <circle cx="448" cy="544" r="22" fill="#ED7D31" stroke="#FFFFFF" stroke-width="8" filter="url(#nodeShadow)"/>
  <text x="438" y="551" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#FFFFFF">05</text>
  <text x="548" y="530" width="530" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#ED7D31">Project Updates</text>
  <text x="548" y="569" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#5D6673">Status review for Alpha, Beta, and Gamma initiatives with next milestone decisions.</text>

  <!-- Footer cue -->
  <text x="548" y="650" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#98A1AD">Nodes are centered exactly on the image seam for the edge-bleed effect.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place agenda nodes entirely inside the right panel; the premium effect depends on circles straddling the image/content seam.
- ❌ Do not use heavy boxed agenda cards; they fight the airy editorial split-panel layout.
- ❌ Do not apply `clip-path` to rectangles or groups for the overlay; use a correctly sized `<rect>` instead.
- ❌ Do not use `<mask>` for image darkening; use translucent rectangles or gradients layered above the photo.
- ❌ Do not put shadows on `<line>` connectors; filters on lines may be dropped.

## Composition notes
- Keep the image panel at roughly 34–36% of the slide width; in a 1280×720 canvas, the seam works well around `x=448`.
- Center each node exactly on the seam, with a white stroke thick enough to create a cutout against both the photo and the white panel.
- Use the right 60% as calm negative space: thin lines, short headers, and one-sentence descriptions.
- Let the photo carry the drama and the agenda area carry clarity; avoid over-coloring the right panel beyond the five node accents.