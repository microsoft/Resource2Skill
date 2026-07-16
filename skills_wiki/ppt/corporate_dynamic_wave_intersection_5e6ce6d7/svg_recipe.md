# SVG Recipe — Corporate Dynamic Wave Intersection

## Visual mechanism
A full-bleed corporate photograph is intersected by large, smooth, overlapping brand-color waves that sweep upward from the lower right. The main wave creates a clean high-contrast typography zone, while secondary purple and cyan curves add depth, motion, and executive polish.

## SVG primitives needed
- 1× `<image>` for the full-bleed corporate background photo
- 1× `<rect>` for a subtle dark/blue photo wash that improves foreground contrast
- 3× `<path>` for the oversized intersecting wave blocks: purple shadow wave, primary blue text wave, cyan highlight swoosh
- 1× `<linearGradient>` for the photo wash
- 2× `<linearGradient>` fills for dimensional blue and purple wave surfaces
- 1× `<filter id="waveShadow">` applied to the main wave for soft depth
- 3× `<path>` strokes for thin decorative data-curve accents inside the wave
- 5× `<circle>` for small node markers on the data-curve accents
- 4× `<text>` elements for eyebrow, main title, subtitle, and date/context label
- 1× `<line>` for a small editorial divider beside the metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071B34" stop-opacity="0.10"/>
      <stop offset="55%" stop-color="#071B34" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#071B34" stop-opacity="0.38"/>
    </linearGradient>

    <linearGradient id="purpleWave" x1="0" y1="0.4" x2="1" y2="1">
      <stop offset="0%" stop-color="#5B2A88"/>
      <stop offset="62%" stop-color="#562B85"/>
      <stop offset="100%" stop-color="#3D1E67"/>
    </linearGradient>

    <linearGradient id="blueWave" x1="0.15" y1="0.2" x2="1" y2="1">
      <stop offset="0%" stop-color="#166DBA"/>
      <stop offset="55%" stop-color="#125DA8"/>
      <stop offset="100%" stop-color="#083E78"/>
    </linearGradient>

    <linearGradient id="cyanSwoosh" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#00AEEF"/>
      <stop offset="100%" stop-color="#3AD7FF"/>
    </linearGradient>

    <filter id="waveShadow" x="-10%" y="-20%" width="130%" height="150%">
      <feOffset dx="-10" dy="-12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoWash)"/>

  <path d="M0,720 L1280,720 L1280,214
           C1135,242 1043,296 948,383
           C829,492 717,603 532,628
           C355,652 183,575 0,535 Z"
        fill="url(#purpleWave)" opacity="0.98"/>

  <path d="M0,720 L1280,720 L1280,292
           C1132,318 1033,372 938,462
           C794,599 612,680 370,650
           C223,632 105,587 0,565 Z"
        fill="url(#blueWave)" filter="url(#waveShadow)"/>

  <path d="M0,720 L0,624
           C70,628 130,654 184,720 Z"
        fill="url(#cyanSwoosh)"/>

  <path d="M879,601
           C943,558 1009,548 1073,575
           C1124,596 1166,593 1213,558"
        fill="none" stroke="#61D9FF" stroke-width="3" stroke-opacity="0.46"/>

  <path d="M727,647
           C808,612 861,615 922,650
           C977,681 1046,674 1125,627"
        fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.22"/>

  <path d="M997,512
           C1041,484 1084,484 1134,507
           C1178,528 1214,520 1260,488"
        fill="none" stroke="#FFC000" stroke-width="2.5" stroke-opacity="0.55"/>

  <circle cx="879" cy="601" r="5" fill="#61D9FF" opacity="0.90"/>
  <circle cx="1073" cy="575" r="5" fill="#61D9FF" opacity="0.80"/>
  <circle cx="922" cy="650" r="4" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="997" cy="512" r="4.5" fill="#FFC000" opacity="0.90"/>
  <circle cx="1134" cy="507" r="4.5" fill="#FFC000" opacity="0.90"/>

  <line x1="744" y1="410" x2="744" y2="463"
        stroke="#00AEEF" stroke-width="5" stroke-linecap="round"/>

  <text x="770" y="423" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3"
        fill="#BFEAFF">FY2026 EXECUTIVE BRIEFING</text>

  <text x="735" y="515" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800" letter-spacing="-1.5"
        fill="#FFFFFF">PERFORMANCE</text>

  <text x="741" y="575" width="490"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="43" font-weight="700"
        fill="#FFC000">Review</text>

  <text x="975" y="643" width="235"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        fill="#D8F4FF" text-anchor="end">Global Sales Operations  ·  Q4</text>
</svg>
```

## Avoid in this skill
- ❌ Rectangular opaque title boxes; they destroy the fluid corporate-wave mechanism.
- ❌ Text directly over the photo without a solid wave behind it; readability becomes unreliable.
- ❌ Hard-edged polygons for the main overlay; use smooth Bézier paths or oversized ellipse-like curves.
- ❌ Applying `clip-path` or `mask` to the wave shapes; keep waves as native editable filled paths.
- ❌ Overusing decorative data curves; they should be subtle texture, not compete with the title.

## Composition notes
- Keep the photograph dominant in the upper-left 55–65% of the slide; avoid placing important faces or objects where the wave will cover them.
- Let the primary blue wave occupy the lower-right 40–50% and place all major typography fully inside it.
- Use the purple wave as a visible offset shadow above/behind the blue wave; it should read as depth, not as a second text area.
- Reserve cyan and gold for small accents only: node markers, dividers, subtitle, or thin curve strokes.