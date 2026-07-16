# SVG Recipe — Color & Grayscale Split-Screen Divider

## Visual mechanism
A hard 50/50 vertical split pairs a saturated crimson color field with a cropped grayscale photograph, creating an editorial chapter-break moment. Three floating white circles bridge the seam and carry the section code, while left-side typography anchors the transition message.

## SVG primitives needed
- 1× `<rect>` for the full-slide crimson background on the left half
- 1× `<image>` for the grayscale photo filling the right half
- 1× `<clipPath>` with `<rect>` to constrain the photo exactly to the right half
- 3× `<circle>` for floating white section-code containers
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to the circles
- 2× `<linearGradient>` for subtle image-side darkening and crimson-side depth
- 3× `<rect>` overlays for vignette, seam highlight, and tonal wash
- 3× `<path>` for decorative angular crimson/white editorial accents
- 10× `<text>` elements with explicit `width` attributes for chapter code, title, subtitle, and small metadata
- 1× `<line>` for the crisp vertical split seam

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="rightPhotoClip">
      <rect x="640" y="0" width="640" height="720"/>
    </clipPath>

    <linearGradient id="crimsonDepth" x1="0" y1="0" x2="640" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F25A58"/>
      <stop offset="0.55" stop-color="#EE4D4D"/>
      <stop offset="1" stop-color="#C8323A"/>
    </linearGradient>

    <linearGradient id="photoVignette" x1="640" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.12"/>
      <stop offset="0.48" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="11" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Split-screen foundation -->
  <rect x="0" y="0" width="640" height="720" fill="url(#crimsonDepth)"/>

  <image x="640" y="0" width="640" height="720"
         href="https://images.example.com/grayscale-corporate-office-architecture.jpg"
         xlink:href="https://images.example.com/grayscale-corporate-office-architecture.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#rightPhotoClip)"/>

  <rect x="640" y="0" width="640" height="720" fill="url(#photoVignette)" opacity="0.95"/>
  <rect x="640" y="0" width="2" height="720" fill="#FFFFFF" opacity="0.34"/>
  <line x1="640" y1="0" x2="640" y2="720" stroke="#2B2B2B" stroke-width="1" opacity="0.18"/>

  <!-- Editorial geometric accents -->
  <path d="M0,0 L150,0 L0,150 Z" fill="#FFFFFF" opacity="0.12"/>
  <path d="M486,0 L640,0 L640,154 Z" fill="#B92D36" opacity="0.22"/>
  <path d="M104,720 L0,720 L0,616 Z" fill="#FFFFFF" opacity="0.10"/>

  <!-- Small metadata on crimson field -->
  <text x="64" y="74" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3" fill="#FFFFFF" opacity="0.82">
    STRATEGIC REPORT
  </text>

  <text x="64" y="104" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="400" letter-spacing="1.5" fill="#FFFFFF" opacity="0.62">
    Q4 BUSINESS REVIEW / SECTION DIVIDER
  </text>

  <!-- Floating circular chapter code -->
  <circle cx="429" cy="360" r="96" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="640" cy="360" r="104" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="851" cy="360" r="96" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="333" y="390" width="192" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" fill="#454545">
    C
  </text>

  <text x="536" y="393" width="208" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="800" fill="#454545">
    H
  </text>

  <text x="755" y="390" width="192" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" fill="#454545">
    1
  </text>

  <!-- Left-side chapter title block -->
  <text x="64" y="535" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" letter-spacing="1" fill="#FFFFFF">
    EXECUTIVE SUMMARY
  </text>

  <text x="66" y="574" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" letter-spacing="2.2" fill="#FFFFFF" opacity="0.78">
    MARKET POSITION / OPERATING PRIORITIES
  </text>

  <text x="66" y="614" width="485" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#FFFFFF" opacity="0.86">
    <tspan x="66" dy="0">This section frames the company’s current trajectory,</tspan>
    <tspan x="66" dy="25">key milestones, and the strategic choices ahead.</tspan>
  </text>

  <!-- Right-side quiet label for image half -->
  <text x="955" y="644" width="245" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2" fill="#FFFFFF" opacity="0.68">
    NEW CHAPTER BEGINS
  </text>

  <text x="955" y="670" width="245" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="400" fill="#FFFFFF" opacity="0.48">
    Use a true grayscale photo asset on this side.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG desaturation filters such as `feColorMatrix`; use an already-grayscale photo asset or grayscale image URL.
- ❌ Do not apply `clip-path` to rectangles or circles for the split; clipping should only be used on the `<image>`.
- ❌ Do not make the circles semi-transparent; their solid white fill is what creates the strong floating focal point.
- ❌ Do not soften the 50/50 split with a wide gradient blend; the power of the layout comes from the hard vertical contrast.
- ❌ Do not use `<mask>`, `<foreignObject>`, `<textPath>`, or `<pattern>` for the photo treatment or typography.

## Composition notes
- Keep the split exact: left color field from `x=0–640`, right image from `x=640–1280`.
- Center the largest circle directly on the split seam; the adjacent circles should sit symmetrically left and right.
- Place the main title in the lower-left quadrant with generous negative space above it.
- Use only one accent color family; let the grayscale image and white circles provide the contrast rhythm.