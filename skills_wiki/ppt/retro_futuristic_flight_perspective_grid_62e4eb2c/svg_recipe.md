# SVG Recipe — Retro-Futuristic Flight Perspective

## Visual mechanism
A low horizon, central vanishing point, and wireframe floor create the illusion of flying forward through a 3D retro grid. Layered silhouettes, oversized sticker typography, a hovering sci‑fi craft, and glowing accents make the slide feel like an energetic title frame from a futuristic motion sequence.

## SVG primitives needed
- 2× `<rect>` for the sky and neon-blue ground gradient planes
- 18–28× `<line>` for the perspective grid: radial vanishing lines plus compressed horizontal depth bands
- 2× `<path>` for distant mountain / city silhouettes at the horizon
- 1× `<path>` for the central sci‑fi flight craft silhouette
- 2× `<circle>` for the glowing engine core
- 5–7× `<ellipse>` for blurred cloud masses and the projected craft shadow
- 3× `<text>` groups for sticker-style “3D”, large title lettering, and the PowerPoint “P”
- 2× `<path>` for chunky forward-motion arrows on the grid
- 1× `<rect>` plus 1× `<path>` for the tilted PowerPoint-card icon
- 3× `<linearGradient>` for sky, ground, and 3D text fills
- 1× `<radialGradient>` for engine glow
- 3× `<filter>` using blur / offset blur / merge for shadows, cloud softness, and glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="432">
      <stop offset="0" stop-color="#b7d4df"/>
      <stop offset="0.55" stop-color="#e9eef0"/>
      <stop offset="1" stop-color="#f7ead6"/>
    </linearGradient>
    <linearGradient id="groundGrad" x1="0" y1="432" x2="0" y2="720">
      <stop offset="0" stop-color="#00136a"/>
      <stop offset="0.46" stop-color="#00369b"/>
      <stop offset="1" stop-color="#2388bf"/>
    </linearGradient>
    <linearGradient id="hillGradA" x1="0" y1="230" x2="0" y2="520">
      <stop offset="0" stop-color="#bde6c6"/>
      <stop offset="1" stop-color="#149ca3"/>
    </linearGradient>
    <linearGradient id="hillGradB" x1="780" y1="230" x2="980" y2="520">
      <stop offset="0" stop-color="#38b55e"/>
      <stop offset="1" stop-color="#188b73"/>
    </linearGradient>
    <linearGradient id="orange3d" x1="0" y1="80" x2="0" y2="220">
      <stop offset="0" stop-color="#ffd525"/>
      <stop offset="1" stop-color="#ff8e18"/>
    </linearGradient>
    <radialGradient id="engineGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#fff7ba"/>
      <stop offset="0.55" stop-color="#ffc72b"/>
      <stop offset="1" stop-color="#f27b00"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blurCloud" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="g"/>
      <feMerge>
        <feMergeNode in="g"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="432" fill="url(#skyGrad)"/>
  <rect x="0" y="432" width="1280" height="288" fill="url(#groundGrad)"/>

  <ellipse cx="965" cy="72" rx="170" ry="82" fill="#fff2dc" opacity="0.75" filter="url(#blurCloud)"/>
  <ellipse cx="1058" cy="138" rx="156" ry="104" fill="#fff7e8" opacity="0.68" filter="url(#blurCloud)"/>
  <ellipse cx="1120" cy="38" rx="115" ry="74" fill="#fff9ee" opacity="0.58" filter="url(#blurCloud)"/>

  <path d="M8 500 L8 376 C25 372 40 366 48 337 L62 245 L145 262 L162 312 L206 340 L229 447 L254 421 L333 418 L352 388 L385 396 L414 512 Z"
        fill="url(#hillGradA)" opacity="0.92"/>
  <path d="M690 444 L781 342 L868 304 L932 366 L990 423 L1030 430 L1075 407 L1122 430 L1210 430 L1220 510 L704 510 Z"
        fill="url(#hillGradB)" opacity="0.95"/>
  <line x1="0" y1="432" x2="1280" y2="432" stroke="#fff9b6" stroke-width="3" opacity="0.8"/>

  <line x1="640" y1="432" x2="-180" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="0" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="160" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="330" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="500" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="640" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.9"/>
  <line x1="640" y1="432" x2="780" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="950" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="1120" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="1280" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>
  <line x1="640" y1="432" x2="1460" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.86"/>

  <line x1="0" y1="438" x2="1280" y2="438" stroke="#ffffff" stroke-width="2" opacity="0.78"/>
  <line x1="0" y1="450" x2="1280" y2="450" stroke="#ffffff" stroke-width="2.3" opacity="0.82"/>
  <line x1="0" y1="468" x2="1280" y2="468" stroke="#ffffff" stroke-width="2.6" opacity="0.86"/>
  <line x1="0" y1="495" x2="1280" y2="495" stroke="#ffffff" stroke-width="3" opacity="0.9"/>
  <line x1="0" y1="535" x2="1280" y2="535" stroke="#ffffff" stroke-width="3.4" opacity="0.92"/>
  <line x1="0" y1="590" x2="1280" y2="590" stroke="#ffffff" stroke-width="3.6" opacity="0.95"/>
  <line x1="0" y1="660" x2="1280" y2="660" stroke="#ffffff" stroke-width="4" opacity="0.96"/>

  <ellipse cx="640" cy="492" rx="175" ry="24" fill="#000000" opacity="0.22" filter="url(#blurCloud)"/>

  <path d="M232 222 L535 162 L557 104 L568 151 L586 44 L600 150 L616 43 L629 150 L661 103 L690 157 L920 142 L986 82 L997 98 L934 166 L705 179 L676 207 L664 181 L630 212 L617 185 L592 198 L566 184 L555 207 L531 175 L236 234 Z"
        fill="#22242a" stroke="#050505" stroke-width="6" stroke-linejoin="round" filter="url(#softShadow)"/>
  <circle cx="618" cy="156" r="31" fill="#111217" stroke="#050505" stroke-width="5"/>
  <circle cx="618" cy="156" r="20" fill="url(#engineGlow)" filter="url(#glow)"/>

  <text x="84" y="192" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="132" font-weight="900"
        fill="#000000" stroke="#000000" stroke-width="16" transform="rotate(-8 210 150)" opacity="0.95">3D</text>
  <text x="76" y="176" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="132" font-weight="900"
        fill="url(#orange3d)" stroke="#ffffff" stroke-width="18" stroke-linejoin="round"
        transform="rotate(-8 210 150)" filter="url(#softShadow)">3D</text>
  <text x="76" y="176" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="132" font-weight="900"
        fill="url(#orange3d)" stroke="#050505" stroke-width="4" stroke-linejoin="round"
        transform="rotate(-8 210 150)">3D</text>

  <text x="305" y="397" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="142" font-weight="900"
        letter-spacing="8" fill="#ffffff" opacity="0.9">FLIGHT!</text>
  <text x="294" y="383" width="740" font-family="Segoe UI, Microsoft YaHei" font-size="142" font-weight="900"
        letter-spacing="8" fill="#ff585f">FLIGHT!</text>

  <path d="M452 486 L397 486 L322 563 L349 584 L317 584 L307 613 L390 607 L383 580 L412 579 L496 512 Q486 486 452 486 Z"
        fill="#ff5a60" stroke="#ffffff" stroke-width="12" stroke-linejoin="round" filter="url(#softShadow)"/>
  <path d="M826 486 L881 486 L956 563 L929 584 L961 584 L971 613 L888 607 L895 580 L866 579 L782 512 Q792 486 826 486 Z"
        fill="#ff5a60" stroke="#ffffff" stroke-width="12" stroke-linejoin="round" filter="url(#softShadow)"/>

  <g transform="rotate(14 1040 150)">
    <path d="M1005 84 L1170 124 L1170 270 L1015 236 Z" fill="#ffffff" stroke="#d93620" stroke-width="5"/>
    <rect x="982" y="70" width="136" height="178" fill="#d83b1f" filter="url(#softShadow)"/>
    <path d="M1118 124 L1162 136 L1162 264 L1118 252 Z M1130 165 L1152 170 M1130 198 L1152 204 M1130 228 L1152 235"
          fill="none" stroke="#d83b1f" stroke-width="8" stroke-linecap="round"/>
    <text x="1014" y="173" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="900" fill="#ffffff">P</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the looping grid; create the still frame in SVG, then add PowerPoint animations natively if needed.
- ❌ Do not bake the grid into a raster image; individual `<line>` elements keep the perspective floor editable.
- ❌ Do not use `marker-end` for arrows; use filled arrow `<path>` shapes so arrowheads survive translation.
- ❌ Do not apply filters to `<line>` grid elements; use opacity and stroke width instead, because line filters are dropped.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the faux-3D text; use rotation, layered strokes, and shadows.

## Composition notes
- Keep the vanishing point exactly centered on the horizon at about 60% slide height; all floor radials should converge there.
- Reserve the middle band for the oversized title, with the craft crossing above it to imply speed and depth.
- Use warm red/orange accents for title, arrows, and icon, contrasted against the cool blue grid and teal horizon silhouettes.
- Let the foreground grid occupy the bottom third to half of the slide; it needs enough height for the perspective illusion to read instantly.