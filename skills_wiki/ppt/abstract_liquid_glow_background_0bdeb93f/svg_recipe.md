# SVG Recipe — Abstract Liquid Glow Background

## Visual mechanism
Deep dark canvas with oversized, blurred Bézier ribbons that sweep diagonally like liquified neon light. Layer broad magenta/purple ambient strokes first, then thinner orange/yellow “hot core” highlights and a few hairline streaks to imply motion while preserving dark negative space for title text.

## SVG primitives needed
- 2× `<rect>` for the deep base background and subtle vignette overlay.
- 7× `<path>` for liquid light ribbons: broad ambient waves, inner glow cores, and thin motion streaks.
- 3× `<ellipse>` for soft out-of-focus color blooms behind the waves.
- 4× `<linearGradient>` for ribbon strokes and typographic accent color.
- 2× `<radialGradient>` for background/vignette and diffuse bloom color.
- 3× `<filter>` using `feGaussianBlur` / `feMerge` for ambient blur, stronger neon glow, and soft text glow.
- 4× `<text>` elements for editable hero-slide sample typography; each includes explicit `width`.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgVignette" cx="38%" cy="45%" r="78%">
      <stop offset="0%" stop-color="#201047"/>
      <stop offset="48%" stop-color="#100927"/>
      <stop offset="100%" stop-color="#060612"/>
    </radialGradient>

    <radialGradient id="magentaBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff3aa8" stop-opacity="0.72"/>
      <stop offset="55%" stop-color="#9b1e8f" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#160030" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="ambientRibbon" x1="40" y1="640" x2="1180" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#3100ff" stop-opacity="0.28"/>
      <stop offset="26%" stop-color="#c016a9" stop-opacity="0.74"/>
      <stop offset="58%" stop-color="#ff3a88" stop-opacity="0.64"/>
      <stop offset="100%" stop-color="#5b1cff" stop-opacity="0.22"/>
    </linearGradient>

    <linearGradient id="hotCore" x1="170" y1="560" x2="1120" y2="170" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ff2f92" stop-opacity="0.2"/>
      <stop offset="18%" stop-color="#ffb22e"/>
      <stop offset="46%" stop-color="#ffe05a"/>
      <stop offset="68%" stop-color="#ff5c76"/>
      <stop offset="100%" stop-color="#8338ff" stop-opacity="0.15"/>
    </linearGradient>

    <linearGradient id="violetCounter" x1="0" y1="120" x2="1280" y2="680" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4425ff" stop-opacity="0.5"/>
      <stop offset="45%" stop-color="#b415c7" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#220a5d" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="accentText" x1="120" y1="0" x2="550" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffbc3f"/>
      <stop offset="50%" stop-color="#ff4fa3"/>
      <stop offset="100%" stop-color="#8d6bff"/>
    </linearGradient>

    <filter id="ambientBlur" x="-45%" y="-65%" width="190%" height="230%">
      <feGaussianBlur stdDeviation="46"/>
    </filter>

    <filter id="neonGlow" x="-55%" y="-75%" width="210%" height="250%">
      <feGaussianBlur stdDeviation="18" result="soft"/>
      <feGaussianBlur stdDeviation="5" result="sharp"/>
      <feMerge>
        <feMergeNode in="soft"/>
        <feMergeNode in="sharp"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textHalo" x="-10%" y="-20%" width="120%" height="150%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#080713"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgVignette)"/>

  <ellipse cx="255" cy="468" rx="310" ry="160" fill="url(#magentaBloom)" opacity="0.45" filter="url(#ambientBlur)" transform="rotate(-18 255 468)"/>
  <ellipse cx="720" cy="330" rx="460" ry="125" fill="#ff2b91" opacity="0.16" filter="url(#ambientBlur)" transform="rotate(-16 720 330)"/>
  <ellipse cx="980" cy="190" rx="330" ry="95" fill="#522aff" opacity="0.22" filter="url(#ambientBlur)" transform="rotate(-12 980 190)"/>

  <path d="M -170 610 C 80 468, 145 332, 310 365 C 500 402, 610 250, 810 232 C 1018 213, 1110 158, 1420 72"
        fill="none" stroke="url(#ambientRibbon)" stroke-width="150" stroke-linecap="round" stroke-linejoin="round"
        opacity="0.74" filter="url(#ambientBlur)"/>

  <path d="M -150 260 C 112 92, 266 178, 374 334 C 468 470, 642 448, 792 365 C 948 278, 1082 292, 1385 180"
        fill="none" stroke="url(#violetCounter)" stroke-width="116" stroke-linecap="round" stroke-linejoin="round"
        opacity="0.56" filter="url(#ambientBlur)"/>

  <path d="M 88 626 C 218 518, 278 406, 380 382 C 520 350, 640 314, 755 252 C 900 174, 1036 180, 1255 126"
        fill="none" stroke="#ff248f" stroke-width="66" stroke-linecap="round" stroke-linejoin="round"
        opacity="0.44" filter="url(#neonGlow)"/>

  <path d="M 154 548 C 230 452, 298 392, 368 374 C 518 336, 615 315, 762 258 C 886 210, 996 206, 1188 148"
        fill="none" stroke="url(#hotCore)" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"
        opacity="0.82" filter="url(#neonGlow)"/>

  <path d="M 198 154 C 276 266, 258 364, 198 433 C 282 376, 342 268, 394 94"
        fill="none" stroke="url(#hotCore)" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"
        opacity="0.62" filter="url(#neonGlow)"/>

  <path d="M 685 226 C 770 178, 838 162, 925 176"
        fill="none" stroke="#ffbe49" stroke-width="9" stroke-linecap="round"
        opacity="0.66" filter="url(#neonGlow)"/>

  <path d="M 918 395 C 1006 282, 1120 282, 1268 205"
        fill="none" stroke="#ff356d" stroke-width="8" stroke-linecap="round"
        opacity="0.52" filter="url(#neonGlow)"/>

  <path d="M 62 288 C 126 255, 186 264, 248 306"
        fill="none" stroke="#ffd04a" stroke-width="7" stroke-linecap="round"
        opacity="0.42" filter="url(#neonGlow)"/>

  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.18"/>

  <text x="96" y="104" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        letter-spacing="4" fill="url(#accentText)" font-weight="700">ABSTRACT SYSTEMS</text>

  <text x="92" y="322" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76"
        font-weight="800" fill="#ffffff" filter="url(#textHalo)">
    <tspan x="92" dy="0">LIQUID</tspan>
    <tspan x="92" dy="82">NEON</tspan>
  </text>

  <text x="98" y="498" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23"
        fill="#d7d3ea" opacity="0.92">
    Fluid glow backgrounds for premium dark-mode product launches.
  </text>

  <text x="98" y="602" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        fill="#9088b8" opacity="0.86">01 / Generative light field</text>
</svg>
```

## Avoid in this skill
- ❌ `filter` on `<line>` for neon streaks; use stroked `<path>` elements instead because path filters translate reliably.
- ❌ `mix-blend-mode`, SVG masks, or CSS background blending for glow accumulation; layer semi-transparent blurred paths directly.
- ❌ Hard-edged geometric waves without blur; the effect depends on feathered falloff and overlapping opacity.
- ❌ Putting bright ribbons behind body copy; reserve a dark negative-space zone for legible slide content.
- ❌ `<pattern>` noise fills for texture; if grain is needed, use sparse tiny editable circles instead, not a pattern.

## Composition notes
- Keep the brightest orange/yellow core crossing one diagonal third of the slide; avoid centering it exactly behind the headline.
- Use 60–70% dark negative space, typically on the left or lower-left, for title and subtitle.
- Build depth from back to front: dark base → blurred color blooms → huge soft ribbons → hot core → thin highlight streaks → typography.
- Color rhythm works best with a cool violet/purple base, saturated magenta body glow, and small warm yellow/orange accents.