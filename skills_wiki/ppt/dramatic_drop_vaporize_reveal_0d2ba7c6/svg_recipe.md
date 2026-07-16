# SVG Recipe — Dramatic Drop & Vaporize Reveal

## Visual mechanism
A heavy, centered headline appears to have dropped into frame, creating a luminous impact point and a soft smoke burst that expands behind it. The final SVG should read like the peak frame of the reveal: crisp premium text in front, vapor cloud and shockwave energy behind, dark cinematic atmosphere around it.

## SVG primitives needed
- 1× `<image>` for the atmospheric dark hero background / night-sky texture.
- 3× `<rect>` for the base fallback color wash, dark overlay, and vignette-like stage panel.
- 1× `<radialGradient>` for the central impact glow.
- 2× `<linearGradient>` for background depth and gold accent text.
- 3× `<filter>`: one soft smoke blur, one text drop shadow, one impact glow.
- 9–14× `<ellipse>` for editable vapor puffs behind the headline.
- 3–5× `<path>` for organic smoke wisps and impact fragments.
- 2× `<text>` elements with nested `<tspan>` for the main title and subtitle, each with explicit `width`.
- 4–6× `<line>` elements for subtle vertical “drop streaks” above the headline.
- 1× dashed `<ellipse>` for the expanding shockwave ring.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDepth" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#050914"/>
      <stop offset="0.48" stop-color="#0B1736"/>
      <stop offset="1" stop-color="#111A2F"/>
    </linearGradient>

    <radialGradient id="impactGlow" cx="640" cy="392" r="380" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFC400" stop-opacity="0.55"/>
      <stop offset="0.28" stop-color="#5BB7FF" stop-opacity="0.24"/>
      <stop offset="0.62" stop-color="#1A2B59" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#02040B" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="goldText" x1="520" y1="290" x2="760" y2="420" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF2A8"/>
      <stop offset="0.45" stop-color="#FFC400"/>
      <stop offset="1" stop-color="#FF8A00"/>
    </linearGradient>

    <filter id="smokeBlur" x="-30%" y="-40%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="textShadow" x="-15%" y="-35%" width="130%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="hotGlow" x="-40%" y="-60%" width="180%" height="220%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <!-- Background atmosphere -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDepth)"/>
  <image href="https://images.example.com/atmospheric-dark-night-sky-subtle-stars-1280x720.jpg"
         x="0" y="0" width="1280" height="720" opacity="0.38"/>
  <rect x="0" y="0" width="1280" height="720" fill="#02040B" opacity="0.28"/>
  <rect x="90" y="72" width="1100" height="576" rx="34" fill="#071126" opacity="0.36"/>

  <!-- Central impact bloom -->
  <ellipse cx="640" cy="394" rx="470" ry="230" fill="url(#impactGlow)"/>
  <ellipse cx="640" cy="418" rx="318" ry="48" fill="#42B7FF" opacity="0.10" filter="url(#hotGlow)"/>
  <ellipse cx="640" cy="416" rx="235" ry="25" fill="#FFC400" opacity="0.20" filter="url(#hotGlow)"/>

  <!-- Drop streaks: imply the headline fell from above -->
  <line x1="470" y1="105" x2="470" y2="228" stroke="#9BD7FF" stroke-width="2" opacity="0.16" stroke-dasharray="14 18"/>
  <line x1="540" y1="70" x2="540" y2="235" stroke="#FFFFFF" stroke-width="2" opacity="0.13" stroke-dasharray="20 22"/>
  <line x1="640" y1="48" x2="640" y2="238" stroke="#FFC400" stroke-width="3" opacity="0.20" stroke-dasharray="24 20"/>
  <line x1="748" y1="82" x2="748" y2="232" stroke="#FFFFFF" stroke-width="2" opacity="0.12" stroke-dasharray="18 22"/>
  <line x1="815" y1="122" x2="815" y2="225" stroke="#9BD7FF" stroke-width="2" opacity="0.14" stroke-dasharray="12 16"/>

  <!-- Vapor cloud, built from editable blurred ellipses and organic paths -->
  <ellipse cx="450" cy="376" rx="158" ry="58" fill="#DDEEFF" opacity="0.30" filter="url(#smokeBlur)"/>
  <ellipse cx="560" cy="345" rx="190" ry="72" fill="#FFFFFF" opacity="0.26" filter="url(#smokeBlur)"/>
  <ellipse cx="700" cy="354" rx="205" ry="78" fill="#CFE9FF" opacity="0.28" filter="url(#smokeBlur)"/>
  <ellipse cx="830" cy="386" rx="165" ry="60" fill="#FFFFFF" opacity="0.22" filter="url(#smokeBlur)"/>
  <ellipse cx="505" cy="432" rx="225" ry="66" fill="#9BD7FF" opacity="0.16" filter="url(#smokeBlur)"/>
  <ellipse cx="725" cy="440" rx="260" ry="76" fill="#FFFFFF" opacity="0.17" filter="url(#smokeBlur)"/>
  <ellipse cx="905" cy="438" rx="150" ry="45" fill="#C8E6FF" opacity="0.13" filter="url(#smokeBlur)"/>

  <path d="M305 390 C390 332, 475 333, 545 372 C604 405, 694 404, 775 360 C848 321, 948 342, 1010 394 C930 374, 852 389, 782 427 C697 473, 589 470, 510 430 C445 397, 374 390, 305 390 Z"
        fill="#FFFFFF" opacity="0.14" filter="url(#smokeBlur)"/>
  <path d="M368 455 C460 418, 532 438, 605 468 C686 503, 762 494, 842 451 C793 514, 702 542, 601 520 C505 499, 433 477, 368 455 Z"
        fill="#7FCBFF" opacity="0.11" filter="url(#smokeBlur)"/>
  <path d="M400 315 C482 275, 565 292, 614 331 C559 318, 501 321, 430 354 C405 365, 379 357, 400 315 Z"
        fill="#FFFFFF" opacity="0.10" filter="url(#smokeBlur)"/>

  <!-- Expanding shockwave ring -->
  <ellipse cx="640" cy="418" rx="365" ry="72" fill="none" stroke="#FFFFFF" stroke-width="2"
           opacity="0.30" stroke-dasharray="22 18"/>
  <ellipse cx="640" cy="418" rx="238" ry="38" fill="none" stroke="#FFC400" stroke-width="3"
           opacity="0.35" stroke-dasharray="34 18"/>

  <!-- Impact sparks and fractured energy at landing line -->
  <path d="M440 428 L475 416 L462 438 Z" fill="#FFC400" opacity="0.75"/>
  <path d="M835 421 L872 410 L854 438 Z" fill="#FFC400" opacity="0.68"/>
  <path d="M600 450 L626 438 L615 466 Z" fill="#FFFFFF" opacity="0.58"/>
  <path d="M690 452 L722 438 L710 468 Z" fill="#FFFFFF" opacity="0.52"/>

  <!-- Main reveal text -->
  <text x="640" y="380" width="980" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92" font-weight="900" letter-spacing="-2"
        fill="#FFFFFF" filter="url(#textShadow)">
    <tspan>超额完成 </tspan><tspan fill="url(#goldText)">154%</tspan>
  </text>

  <text x="640" y="458" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="600" letter-spacing="5"
        fill="#C9D8F2" opacity="0.88">
    <tspan>YEAR-END PERFORMANCE BREAKTHROUGH</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the drop/vaporize timing; represent the reveal as a premium keyframe in SVG, then add PowerPoint animations natively if needed.
- ❌ Do not use `<mask>` to fade the smoke. Build vapor with semi-transparent blurred ellipses and paths instead.
- ❌ Do not apply `filter` to `<line>` elements for falling streaks; line filters are dropped by the translator.
- ❌ Do not put smoke in a raster screenshot unless necessary. Editable ellipses and paths preserve recoloring and resizing in PowerPoint.
- ❌ Do not crowd the slide with secondary charts or icons; the technique depends on one dominant focal event.

## Composition notes
- Keep the headline centered horizontally and slightly below vertical center, around `y=360–390`, so it feels like it has “landed.”
- Smoke should occupy roughly 55–65% of slide width, sitting behind the text with low opacity and strong blur.
- Use a dark navy/black background with one warm gold accent; the color rhythm is cold atmosphere + hot impact.
- Preserve generous negative space around the cloud so the reveal feels cinematic rather than busy.