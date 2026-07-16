# SVG Recipe — Dynamic Spotlight Series (Thematic Q&A Morph)

## Visual mechanism
A persistent stage spotlight in the upper-left casts a large translucent polygonal beam across the canvas, visually “illuminating” a featured person or Q&A topic. Across a series, duplicate the slide and slightly change the spotlight rotation plus beam path while keeping the same element IDs/names so PowerPoint Morph reads the beam sweep as one continuous object.

## SVG primitives needed
- 2× `<rect>` for the gradient background and deep navy title banner
- 2× `<path>` for the main white light beam and the darker beam overlay inside the banner
- 8–12× `<path>` / `<ellipse>` / `<line>` for the stylized editable spotlight illustration
- 1× `<image>` for the featured portrait, clipped to a clean photo card
- 1× `<clipPath>` with rounded `<rect>` for the portrait crop
- 1× `<filter id="softShadow">` applied to the portrait card and optional beam edges
- 2× `<linearGradient>` for the cool background and subtle beam intensity
- 4× `<text>` elements with explicit `width` for series title, role, first name, and surname

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgCool" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D2E1F0"/>
      <stop offset="0.55" stop-color="#EAF3FB"/>
      <stop offset="1" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="beamFade" x1="96" y1="86" x2="1180" y2="420" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.54"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.32"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.10"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitClip">
      <rect x="702" y="234" width="410" height="436" rx="0" ry="0"/>
    </clipPath>
  </defs>

  <!-- cool executive background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgCool)"/>

  <!-- persistent top banner -->
  <rect x="0" y="0" width="1280" height="186" fill="#0D4778"/>
  <rect x="0" y="0" width="1280" height="186" fill="#07508F" opacity="0.35"/>

  <!-- morph object: dark beam segment visible across banner -->
  <path id="morph_beam_banner"
        d="M 98 88 L 1280 212 L 1280 186 L 126 186 Z"
        fill="#2F79AE" opacity="0.46"/>

  <!-- morph object: main volumetric spotlight beam -->
  <path id="morph_beam_main"
        d="M 91 86 L 1280 212 L 1280 720 L 352 720 Z"
        fill="url(#beamFade)" opacity="0.95"/>

  <!-- spotlight icon, deliberately cropped at the top-left for scale -->
  <g id="morph_spotlight" transform="translate(-18 -10) rotate(22 90 78)">
    <path d="M 10 18 L 108 18 L 152 52 L 152 118 L 108 152 L 10 152 Z"
          fill="#0D4778" stroke="#AFCDE5" stroke-width="2.2"/>
    <path d="M 112 24 C 138 35 154 53 154 84 C 154 115 138 136 112 146
             C 83 130 76 101 83 74 C 88 51 96 35 112 24 Z"
          fill="#135B95" stroke="#BFD8EC" stroke-width="2.2"/>
    <ellipse cx="132" cy="85" rx="24" ry="43"
             fill="#0A3E6E" stroke="#C7DDEE" stroke-width="2.6"/>
    <ellipse cx="137" cy="85" rx="13" ry="35"
             fill="#D7E9F8" opacity="0.88"/>
    <path d="M 8 26 L 52 44" stroke="#BFD8EC" stroke-width="3" stroke-linecap="round"/>
    <path d="M 8 45 L 45 60" stroke="#BFD8EC" stroke-width="3" stroke-linecap="round"/>
    <path d="M 8 64 L 37 75" stroke="#BFD8EC" stroke-width="3" stroke-linecap="round"/>
    <path d="M 8 83 L 32 92" stroke="#BFD8EC" stroke-width="3" stroke-linecap="round"/>
    <line x1="46" y1="18" x2="46" y2="-18" stroke="#BFD8EC" stroke-width="2.5"/>
    <line x1="76" y1="18" x2="76" y2="-22" stroke="#BFD8EC" stroke-width="2.5"/>
    <path d="M 42 -18 L 82 -22" stroke="#BFD8EC" stroke-width="2.5"/>
    <circle cx="18" cy="142" r="5" fill="#BFD8EC"/>
  </g>

  <!-- large series title inside banner -->
  <text x="270" y="116" width="760"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="84" font-weight="600"
        fill="#FFFFFF" letter-spacing="0.5">
    Employee Spotlight
  </text>

  <!-- portrait card on the illuminated right third -->
  <rect x="700" y="232" width="414" height="440" fill="#FFFFFF" opacity="0.74" filter="url(#softShadow)"/>
  <rect x="702" y="234" width="410" height="436" fill="none" stroke="#0D4778" stroke-width="3.2"/>
  <image x="702" y="234" width="410" height="436"
         href="https://images.example.com/corporate-analyst-portrait-neutral-background.jpg"
         clip-path="url(#portraitClip)" preserveAspectRatio="xMidYMid slice"/>

  <!-- subject typography -->
  <text x="201" y="337" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="300"
        fill="#0D4778" letter-spacing="1">
    Financial Analyst
  </text>

  <text x="199" y="456" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="800"
        fill="#07508F">
    Jimmy
  </text>

  <text x="199" y="561" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="300"
        fill="#07508F">
    Pineda
  </text>

  <!-- faint floor wedge to echo the sweeping beam shape -->
  <path d="M 0 720 L 350 720 L 260 488 L 0 560 Z" fill="#FFFFFF" opacity="0.24"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` / `<animateTransform>`; create separate slides and use PowerPoint Morph instead.
- ❌ Replacing the beam with a raster image; use editable `<path>` polygons so the beam can morph cleanly.
- ❌ Applying `clip-path` to the beam or text; clipping should be reserved for the portrait `<image>`.
- ❌ Using a `<mask>` for the volumetric light fade; prefer alpha fills and gradients that translate reliably.
- ❌ Over-detailing the spotlight with tiny repeated elements; keep it bold enough to survive PPT editing and slide-scale viewing.

## Composition notes
- Keep the spotlight anchored partially off-canvas in the upper-left; this makes the beam feel like it is entering the stage from outside the slide.
- Reserve the upper 25% for the navy banner and series title; place the person/topic content in the illuminated lower field.
- Use a right-third portrait for intro slides, then remove it on topic slides and center the Q&A text within the beam.
- For a morph sequence, duplicate the slide and adjust only `morph_beam_main`, `morph_beam_banner`, and the spotlight `rotate(...)` angle while preserving their IDs/names.