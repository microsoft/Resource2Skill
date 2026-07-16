# SVG Recipe — Cinematic Vertical Morph Timeline

## Visual mechanism
A dark cinematic slide uses a vertical timeline axis on the left where the active event is enlarged, filled, and centered while surrounding events remain smaller, outlined, and dimmed. A large contextual photo occupies the right side and is blended into the black canvas using gradient overlay rectangles, creating a documentary-style fade without relying on masks.

## SVG primitives needed
- 1× `<rect>` for the deep charcoal slide background
- 1× `<image>` for the full-height cinematic event photo on the right
- 1× `<clipPath>` with rounded `<rect>` applied to the photo crop
- 4× `<rect>` overlays for left-to-right photo fade, right vignette, top/bottom darkening, and subtle text readability wash
- 1× `<path>` for an organic dark cinematic sweep over the photo edge
- 1× `<line>` for the continuous vertical timeline axis
- 7× inactive `<circle>` nodes with transparent fill and dim white stroke
- 1× active glow `<circle>` plus 1× active core `<circle>` for the focused node
- 7× year `<text>` labels with active/inactive scale and opacity hierarchy
- 4× main content `<text>` blocks for eyebrow, title, subtitle, and description
- 2× `<linearGradient>` fills for the photo fade and vignettes
- 1× `<radialGradient>` for the active node halo
- 2× `<filter>` definitions: one soft glow for the active node and one shadow for headline/photo depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoFadeLeft" x1="390" y1="0" x2="760" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#141414" stop-opacity="1"/>
      <stop offset="0.48" stop-color="#141414" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#141414" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rightVignette" x1="940" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#141414" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.46"/>
    </linearGradient>
    <linearGradient id="verticalVignette" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.62"/>
      <stop offset="0.22" stop-color="#000000" stop-opacity="0"/>
      <stop offset="0.78" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.70"/>
    </linearGradient>
    <radialGradient id="activeHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.42"/>
      <stop offset="0.42" stop-color="#ffffff" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="headlineShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoClip">
      <rect x="390" y="0" width="890" height="720" rx="0" ry="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#141414"/>

  <image x="390" y="-10" width="900" height="740"
         href="https://images.example.com/cinematic-ocean-liner-archive-photo.jpg"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip)"/>

  <rect x="390" y="0" width="450" height="720" fill="url(#photoFadeLeft)"/>
  <rect x="900" y="0" width="380" height="720" fill="url(#rightVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#verticalVignette)"/>
  <rect x="315" y="0" width="470" height="720" fill="#141414" opacity="0.18"/>

  <path d="M348,0 C435,112 404,226 482,338 C552,440 506,584 594,720 L330,720 L330,0 Z"
        fill="#141414" opacity="0.54"/>

  <line x1="180" y1="58" x2="180" y2="662" stroke="#ffffff" stroke-opacity="0.34" stroke-width="2"/>

  <g id="timeline-state-active-1912">
    <circle cx="180" cy="-60" r="12" fill="none" stroke="#ffffff" stroke-opacity="0.34" stroke-width="2"/>
    <text x="70" y="-52" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#888888" text-anchor="end">1876</text>

    <circle cx="180" cy="80" r="13" fill="none" stroke="#ffffff" stroke-opacity="0.42" stroke-width="2"/>
    <text x="70" y="88" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#9a9a9a" text-anchor="end">1899</text>

    <circle cx="180" cy="220" r="14" fill="none" stroke="#ffffff" stroke-opacity="0.58" stroke-width="2.2"/>
    <text x="70" y="229" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#b8b8b8" text-anchor="end">1907</text>

    <circle cx="180" cy="360" r="46" fill="url(#activeHalo)" filter="url(#softGlow)"/>
    <circle cx="180" cy="360" r="28" fill="#ffffff"/>
    <text x="62" y="376" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#ffffff" text-anchor="end">1912</text>

    <circle cx="180" cy="500" r="14" fill="none" stroke="#ffffff" stroke-opacity="0.52" stroke-width="2"/>
    <text x="70" y="508" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#9a9a9a" text-anchor="end">1920</text>

    <circle cx="180" cy="640" r="13" fill="none" stroke="#ffffff" stroke-opacity="0.38" stroke-width="2"/>
    <text x="70" y="648" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#858585" text-anchor="end">1932</text>

    <circle cx="180" cy="780" r="12" fill="none" stroke="#ffffff" stroke-opacity="0.24" stroke-width="2"/>
    <text x="70" y="788" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#707070" text-anchor="end">1948</text>
  </g>

  <text x="348" y="204" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700"
        letter-spacing="3" fill="#d7d7d7" opacity="0.82">CHAPTER 02  /  MAIDEN VOYAGE</text>

  <text x="344" y="312" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800"
        fill="#ffffff" filter="url(#headlineShadow)">TITANIC</text>

  <text x="350" y="360" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-style="italic"
        fill="#d0d0d0">April 10th | Great Britain</text>

  <text x="350" y="420" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#ededed" opacity="0.88">
    <tspan x="350" dy="0">A monumental launch sequence: 897 members boarded</tspan>
    <tspan x="350" dy="34">the vessel as the organization entered its most</tspan>
    <tspan x="350" dy="34">watched chapter across the Atlantic.</tspan>
  </text>

  <line x1="350" y1="548" x2="470" y2="548" stroke="#ffffff" stroke-opacity="0.48" stroke-width="2"/>
  <text x="350" y="584" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        letter-spacing="2" fill="#a8a8a8">DUPLICATE SLIDE · SHIFT GROUP · APPLY MORPH</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the vertical movement; create separate static slide states and use PowerPoint Morph instead.
- ❌ `<mask>` for fading the photo; use semi-transparent gradient overlay rectangles so the PPT result remains editable and reliable.
- ❌ `clip-path` on rectangles or paths; only apply clipping to the `<image>` if a crop is needed.
- ❌ Marker-based arrows or filter effects on `<line>` elements; the timeline axis should stay as a simple native line.
- ❌ Overcrowding the active event with many paragraphs; the cinematic hierarchy depends on one dominant headline and a short supporting description.

## Composition notes
- Keep the timeline axis in the left 18–22% of the slide; the active node should sit exactly at vertical center for strong Morph continuity.
- Place the main title block just right of the axis, roughly between x=340 and x=900, leaving the photo visible behind the far right side.
- Use white only for the active year, node, and title; dim all inactive years and nodes to preserve context without competing for attention.
- For a multi-slide sequence, duplicate this SVG layout, translate the entire timeline group vertically by one node spacing, then update which node is filled/enlarged before applying PowerPoint Morph.