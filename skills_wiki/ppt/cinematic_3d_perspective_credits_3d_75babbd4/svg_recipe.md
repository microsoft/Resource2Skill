# SVG Recipe — Cinematic 3D Perspective Credits

## Visual mechanism
A dark cinematic stage holds a left-side “projection screen” drawn as a trapezoid with side extrusion, glow, and shadow to simulate 3D perspective. On the right, tightly aligned two-column credits mimic movie end titles, creating an elegant team-recognition finale instead of a plain thank-you slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide black/navy background
- 2× `<radialGradient>` / `<linearGradient>` for ambient glow and screen highlight
- 2× `<filter>` for soft bloom and screen drop shadow
- 1× `<clipPath>` with a perspective `<path>` applied to the screen `<image>`
- 1× `<image>` for the presentation/video still inside the angled screen
- 5× `<path>` for the 3D screen body, side extrusion, bottom bevel, glare, and perspective scan lines
- 1× `<ellipse>` for the blurred floor shadow under the screen
- Multiple small `<circle>` elements for cinematic dust/star particles
- Multiple `<rect>` elements for film-strip perforations and subtle UI details
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, roles, names, and closing line
- 1× `<line>` for the credits divider, without filters

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="46%" r="72%">
      <stop offset="0%" stop-color="#243553"/>
      <stop offset="42%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#020308"/>
    </radialGradient>

    <linearGradient id="screenFace" x1="120" y1="120" x2="610" y2="505" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1e2b42"/>
      <stop offset="52%" stop-color="#0b111d"/>
      <stop offset="100%" stop-color="#05070c"/>
    </linearGradient>

    <linearGradient id="screenEdge" x1="550" y1="160" x2="660" y2="490" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#3b4657"/>
      <stop offset="100%" stop-color="#111620"/>
    </linearGradient>

    <linearGradient id="glare" x1="130" y1="130" x2="540" y2="410" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.38"/>
      <stop offset="32%" stop-color="#8ec5ff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blueGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>

    <clipPath id="screenClip" clipPathUnits="userSpaceOnUse">
      <path d="M112 158 L552 100 L618 430 L150 520 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.18"/>

  <circle cx="116" cy="92" r="1.5" fill="#b8c7ff" opacity="0.45"/>
  <circle cx="278" cy="58" r="1.1" fill="#ffffff" opacity="0.32"/>
  <circle cx="506" cy="84" r="1.4" fill="#c7d2fe" opacity="0.28"/>
  <circle cx="688" cy="118" r="1.2" fill="#ffffff" opacity="0.25"/>
  <circle cx="1120" cy="74" r="1.5" fill="#e0e7ff" opacity="0.38"/>
  <circle cx="1038" cy="302" r="1" fill="#ffffff" opacity="0.26"/>
  <circle cx="1210" cy="520" r="1.2" fill="#94a3b8" opacity="0.26"/>

  <ellipse cx="372" cy="594" rx="330" ry="48" fill="#000000" opacity="0.55" filter="url(#blueGlow)"/>
  <ellipse cx="386" cy="586" rx="245" ry="20" fill="#2f5f9f" opacity="0.16" filter="url(#blueGlow)"/>

  <path d="M552 100 L642 153 L690 465 L618 430 Z" fill="url(#screenEdge)" opacity="0.92"/>
  <path d="M150 520 L618 430 L690 465 L222 558 Z" fill="#0c1018" opacity="0.95"/>
  <path d="M112 158 L552 100 L618 430 L150 520 Z" fill="url(#screenFace)" filter="url(#softShadow)"/>

  <image href="https://images.example.com/futuristic-presentation-video-frame-with-blue-interface.jpg"
         x="92" y="82" width="560" height="470"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#screenClip)"/>

  <path d="M112 158 L552 100 L618 430 L150 520 Z" fill="none" stroke="#9cc9ff" stroke-width="2.5" opacity="0.55"/>
  <path d="M128 174 L536 122 L596 416 L168 496 Z" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.18"/>
  <path d="M118 162 C235 126 410 118 548 104 L394 220 C292 198 190 188 118 162 Z" fill="url(#glare)" opacity="0.9"/>

  <path d="M126 232 L568 181" stroke="#8ab4ff" stroke-width="1" opacity="0.16"/>
  <path d="M134 292 L580 246" stroke="#8ab4ff" stroke-width="1" opacity="0.13"/>
  <path d="M143 354 L592 313" stroke="#8ab4ff" stroke-width="1" opacity="0.11"/>
  <path d="M151 418 L604 380" stroke="#8ab4ff" stroke-width="1" opacity="0.09"/>

  <rect x="132" y="178" width="9" height="18" rx="2" fill="#02050a" opacity="0.75"/>
  <rect x="139" y="228" width="9" height="18" rx="2" fill="#02050a" opacity="0.65"/>
  <rect x="147" y="278" width="9" height="18" rx="2" fill="#02050a" opacity="0.58"/>
  <rect x="155" y="328" width="9" height="18" rx="2" fill="#02050a" opacity="0.50"/>
  <rect x="163" y="378" width="9" height="18" rx="2" fill="#02050a" opacity="0.42"/>

  <text x="178" y="466" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#ffffff" opacity="0.92">
    Q4 STRATEGY FILM
  </text>
  <text x="178" y="492" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#b8c7ff" opacity="0.72" letter-spacing="2">
    FINAL CUT · EXECUTIVE PRESENTATION
  </text>

  <text x="720" y="86" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8" letter-spacing="4">
    PRESENTED BY THE PROJECT TEAM
  </text>
  <text x="720" y="132" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#ffffff" letter-spacing="1">
    END CREDITS
  </text>
  <text x="720" y="165" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#cbd5e1" opacity="0.78">
    A cinematic closing page for the people behind the work
  </text>

  <line x1="866" y1="206" x2="866" y2="528" stroke="#334155" stroke-width="1"/>
  <text x="846" y="234" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Executive Sponsor</text>
  <text x="894" y="234" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Maya Chen</text>

  <text x="846" y="278" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Topic Curation</text>
  <text x="894" y="278" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Sarah Jenkins</text>

  <text x="846" y="322" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Data Gathering</text>
  <text x="894" y="322" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Markus Doe</text>

  <text x="846" y="366" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Visual Design</text>
  <text x="894" y="366" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Alex Rivera</text>

  <text x="846" y="410" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Motion Direction</text>
  <text x="894" y="410" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Chris Wong</text>

  <text x="846" y="454" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Post Production</text>
  <text x="894" y="454" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Emma Stone</text>

  <text x="846" y="498" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94a3b8">Final Review</text>
  <text x="894" y="498" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">Dr. Alan Grant</text>

  <text x="720" y="590" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#e2e8f0">
    <tspan font-weight="700">Thank you</tspan><tspan fill="#94a3b8"> for watching the story unfold.</tspan>
  </text>
  <text x="720" y="626" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748b" letter-spacing="3">
    ADD POWERPOINT “CREDITS” ANIMATION TO SCROLL THIS COLUMN
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake perspective; those transforms are dropped. Draw the perspective screen directly as `<path>` quadrilaterals.
- ❌ Do not rely on PowerPoint 3D camera XML inside SVG. SVG should simulate the 3D look with trapezoid faces, bevel paths, gradients, and shadows.
- ❌ Do not apply `clip-path` to ordinary shapes for this technique; clipping is reliable for `<image>` only. Draw overlays as paths already matching the screen geometry.
- ❌ Do not use `<mask>` for fading credits. If a fade is needed, place translucent gradient-colored shapes or adjust text opacity manually.
- ❌ Do not put `filter` on `<line>` elements; use filters on paths, ellipses, rects, circles, or text only.

## Composition notes
- Keep the 3D screen on the left 45–50% of the canvas, tilted toward the credits so the eye flows from visual proof to team recognition.
- Reserve the right 38–42% for credits; use a narrow gray role column and a wider bold white name column for movie-title hierarchy.
- Use deep navy, black, slate gray, and small blue-white highlights to maintain a premium cinema atmosphere.
- Leave generous negative space above and around the credits so the layout feels like an ending sequence, not a dense staff directory.