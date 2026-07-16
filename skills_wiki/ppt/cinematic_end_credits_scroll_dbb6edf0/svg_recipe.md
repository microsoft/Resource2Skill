# SVG Recipe — Cinematic End Credits Scroll

## Visual mechanism
A tall, centered column of white and grey attribution text is shown on a deep black cinematic viewport, with soft fade bands at the top and bottom to imply the text is continuously scrolling through the frame. In PowerPoint, animate the entire credits column upward with a linear motion path and zero smooth start/end.

## SVG primitives needed
- 1× `<rect>` for the full black cinema background
- 1× `<radialGradient>` on the background for a barely visible center glow
- 2× `<rect>` for top and bottom fade overlays using black-to-transparent gradients
- 2× `<path>` for subtle vertical film-edge framing lines
- 1× `<filter id="softGlow">` applied to the opening title text
- 24× `<text>` for centered credit roles, names, section labels, and closing dedication
- Optional 1× grouped credits column via `<g transform="translate(...)"` so the entire block can be selected and animated upward in PowerPoint

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="cinemaGlow" cx="50%" cy="46%" r="70%">
      <stop offset="0%" stop-color="#151820"/>
      <stop offset="52%" stop-color="#050609"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="topFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="1"/>
      <stop offset="60%" stop-color="#000000" stop-opacity=".78"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="1"/>
      <stop offset="58%" stop-color="#000000" stop-opacity=".84"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaGlow)"/>

  <path d="M142 40 C132 150 132 270 142 380 C152 500 152 610 142 690"
        fill="none" stroke="#1a1a1a" stroke-width="2" opacity=".55"/>
  <path d="M1138 40 C1148 150 1148 270 1138 380 C1128 500 1128 610 1138 690"
        fill="none" stroke="#1a1a1a" stroke-width="2" opacity=".55"/>

  <text x="640" y="88" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16"
        letter-spacing="4" fill="#8d8d8d">PROJECT FINALE</text>

  <g id="credits-column" transform="translate(0,-36)">
    <text x="640" y="165" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28"
          letter-spacing="6" fill="#ffffff" filter="url(#softGlow)">END CREDITS</text>

    <text x="640" y="222" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16"
          letter-spacing="3" fill="#9a9a9a">A TRANSFORMATION PROGRAM BY</text>
    <text x="640" y="256" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27"
          font-weight="700" fill="#ffffff">Northstar Strategy Office</text>

    <text x="640" y="322" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">EXECUTIVE SPONSORS</text>
    <text x="640" y="354" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24"
          font-weight="700" fill="#f5f5f5">Amelia Hart  ·  Victor Chen</text>

    <text x="640" y="414" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">PROGRAM DIRECTOR</text>
    <text x="640" y="446" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24"
          font-weight="700" fill="#f5f5f5">Maya Okafor</text>

    <text x="640" y="506" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">PRODUCT LEADS</text>
    <text x="640" y="538" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23"
          font-weight="700" fill="#ffffff">Jonas Meyer  ·  Priya Raman  ·  Elena Rossi</text>

    <text x="640" y="598" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">DESIGN & RESEARCH</text>
    <text x="640" y="630" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22"
          font-weight="700" fill="#f2f2f2">Noah Brooks  ·  Lina Park  ·  Sofia Alvarez</text>

    <text x="640" y="690" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">ENGINEERING</text>
    <text x="640" y="722" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22"
          font-weight="700" fill="#ffffff">Owen Patel  ·  Grace Kim  ·  Theo Laurent</text>

    <text x="640" y="782" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">DATA & ANALYTICS</text>
    <text x="640" y="814" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22"
          font-weight="700" fill="#f2f2f2">Hannah Wu  ·  Marcus Reed  ·  Samira El-Amin</text>

    <text x="640" y="874" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">CHANGE CHAMPIONS</text>
    <text x="640" y="906" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22"
          font-weight="700" fill="#ffffff">Avery Stone  ·  Daniel Ito  ·  Isabelle Moreau</text>

    <text x="640" y="974" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
          letter-spacing="3" fill="#858585">SPECIAL THANKS</text>
    <text x="640" y="1008" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21"
          font-weight="700" fill="#f6f6f6">Every teammate, partner, reviewer, and customer voice</text>

    <text x="640" y="1082" width="760" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
          letter-spacing="5" fill="#bdbdbd">THANK YOU</text>
  </g>

  <rect x="0" y="0" width="1280" height="150" fill="url(#topFade)"/>
  <rect x="0" y="560" width="1280" height="160" fill="url(#bottomFade)"/>

  <text x="640" y="685" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12"
        letter-spacing="3" fill="#4f4f4f">SET MOTION PATH: UP · LINEAR · NO SMOOTH START · NO SMOOTH END</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the scroll; they will not translate safely to editable PowerPoint.
- ❌ Do not use `<mask>` to fade the credits column; use black gradient overlay rectangles instead.
- ❌ Do not use `<textPath>` for curved credits or decorative typography; keep the credits mechanically centered and readable.
- ❌ Do not place hundreds of names in one giant SVG `<text>` without explicit `width`; use multiple editable text lines or grouped sections.
- ❌ Do not add easing, bounce, or cinematic zooms in PowerPoint; the end-credits illusion depends on constant-speed vertical movement.

## Composition notes
- Keep the credits column around 55–60% of slide width, centered, with generous black margins for a theatrical feel.
- Use grey, small, letter-spaced role labels above larger bright-white names to create hierarchy without breaking the end-credits convention.
- The top and bottom fade overlays should sit above the text so the column appears to enter and exit a viewport.
- For the real scroll, select/group the credits column, start it below the slide, animate upward past the top edge, set duration to 20–35 seconds, and set smooth start/end to zero.