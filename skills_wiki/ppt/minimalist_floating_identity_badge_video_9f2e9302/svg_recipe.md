# SVG Recipe — Minimalist Floating Identity Badge (Video Documentary Style)

## Visual mechanism
A full-bleed documentary-style portrait frame is softened with cinematic vignettes, then overlaid with a compact translucent rounded badge in the lower-left quadrant. The badge behaves like a broadcast lower-third: bright, legible, tightly padded, and lifted from the image with a soft shadow.

## SVG primitives needed
- 1× `<image>` for the full-bleed portrait/video-frame background
- 2× `<rect>` for dark cinematic gradient overlays that improve text contrast
- 1× `<rect>` for the semi-transparent rounded identity badge
- 1× `<filter id="badgeShadow">` applied to the badge for a soft floating drop shadow
- 1× `<filter id="textShadow">` applied to the subtitle and small video UI text
- 2× `<linearGradient>` for bottom and left vignettes over the photo
- 1× `<radialGradient>` for subtle center light bloom / lens softness
- 1× `<ellipse>` for the soft bloom layer
- 4× `<text>` for name, role line, timestamp, and closing prompt
- 1× `<circle>` for a minimal recording/status dot
- 2× `<line>` for small documentary-frame corner marks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bottomVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.58"/>
    </linearGradient>

    <linearGradient id="leftVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.48"/>
      <stop offset="36%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="softBloom" cx="54%" cy="38%" r="54%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="badgeShadow" x="-20%" y="-45%" width="150%" height="210%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 0.24 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-10%" y="-30%" width="130%" height="170%">
      <feOffset dx="0" dy="2"/>
      <feGaussianBlur stdDeviation="3"/>
      <feColorMatrix type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 0.55 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#252A2F"/>

  <image
    href="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <ellipse cx="720" cy="255" rx="520" ry="330" fill="url(#softBloom)" opacity="0.75"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftVignette)"/>

  <line x1="62" y1="54" x2="130" y2="54" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>
  <line x1="62" y1="54" x2="62" y2="122" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>

  <circle cx="1076" cy="64" r="6" fill="#FF4D4D"/>
  <text x="1094" y="70" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600" letter-spacing="2"
        fill="#FFFFFF" opacity="0.86" filter="url(#textShadow)">REC</text>

  <text x="1012" y="675" width="210"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500" letter-spacing="1.6"
        fill="#FFFFFF" opacity="0.64" text-anchor="end"
        filter="url(#textShadow)">00:18:42 / FINAL TAKE</text>

  <g transform="translate(118, 438)">
    <rect x="0" y="0" width="438" height="92" rx="24" ry="24"
          fill="#F8F9FA" fill-opacity="0.92"
          filter="url(#badgeShadow)"/>

    <text x="34" y="58" width="370"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="41" font-weight="700"
          fill="#151C24" letter-spacing="-0.8">Karen Walter</text>
  </g>

  <text x="124" y="568" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700"
        letter-spacing="2.8"
        fill="#FFFFFF" filter="url(#textShadow)">PRESENTATION EXPERT · EXECUTIVE STORYTELLING</text>

  <text x="124" y="628" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="500"
        fill="#FFFFFF" opacity="0.88"
        filter="url(#textShadow)">Thank you for watching.</text>
</svg>
```

## Avoid in this skill
- ❌ Full-width opaque lower-third bars; they make the design feel like a TV news template instead of a premium documentary overlay
- ❌ Placing dark text directly on the photo without a badge; photo contrast will vary and reduce legibility
- ❌ Heavy outlines around the badge; rely on translucency and shadow instead
- ❌ Using `<mask>` for the background fade; use gradient-filled `<rect>` overlays instead
- ❌ Applying `filter` to `<line>` elements for camera-frame marks; filters on lines may be dropped

## Composition notes
- Keep the badge in the lower-left or mid-lower-left area, roughly 9–12% from the left edge and 60–65% from the top.
- Size the badge to wrap the name closely with generous horizontal padding; avoid stretching it across the whole slide.
- Use dark vignettes over the photo only where text sits, preserving the subject’s face and key visual details.
- Pair the bright badge with a white all-caps role line underneath for a polished broadcast/documentary hierarchy.