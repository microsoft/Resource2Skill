# SVG Recipe — Centered Section Divider

## Visual mechanism
A low-density transition slide built around a strict vertical centerline: optional hero medallion, oversized headline, thick accent divider, and concise subtitle. Subtle gradient blobs and a soft photo crop add polish while keeping the viewer’s attention locked on the new section title.

## SVG primitives needed
- 1× `<rect>` for the full-slide background wash
- 2× `<path>` for large soft organic corner blobs that frame the centered content
- 1× `<image>` clipped to a circular medallion for an optional section visual
- 1× `<clipPath>` with `<circle>` applied only to the hero image
- 2× `<circle>` for the medallion backing and accent ring
- 1× `<rect>` for the thick rounded accent divider under the headline
- 1× `<text>` for the small section eyebrow
- 1× `<text>` for the main centered headline
- 1× `<text>` for the subtitle
- 2× `<linearGradient>` for background and accent divider color
- 1× `<radialGradient>` for the medallion glow
- 2× `<filter>` definitions: one soft shadow for the medallion, one blur glow for decorative blobs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="48%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F7FF"/>
    </linearGradient>

    <linearGradient id="accentBar" x1="440" y1="0" x2="840" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#6C5CE7"/>
      <stop offset="45%" stop-color="#00B8D9"/>
      <stop offset="100%" stop-color="#2ED573"/>
    </linearGradient>

    <radialGradient id="medallionGlow" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#EEF5FF"/>
      <stop offset="100%" stop-color="#DDE8FF"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blobGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="heroCircleClip">
      <circle cx="640" cy="190" r="62"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-90,98 C52,18 145,42 232,116 C318,190 291,310 184,344 C76,379 -41,324 -93,230 C-137,151 -128,120 -90,98 Z"
        fill="#DCEBFF" opacity="0.62" filter="url(#blobGlow)"/>

  <path d="M1132,500 C1218,414 1367,448 1398,563 C1429,678 1285,765 1171,724 C1058,684 1035,596 1132,500 Z"
        fill="#E9DFFF" opacity="0.58" filter="url(#blobGlow)"/>

  <circle cx="640" cy="190" r="86" fill="url(#medallionGlow)" filter="url(#softShadow)"/>
  <circle cx="640" cy="190" r="74" fill="none" stroke="#FFFFFF" stroke-width="8"/>
  <circle cx="640" cy="190" r="78" fill="none" stroke="#6C5CE7" stroke-width="2.5" opacity="0.38"/>

  <image x="578" y="128" width="124" height="124"
         href="https://images.example.com/hero/abstract-team-strategy-photo.jpg"
         clip-path="url(#heroCircleClip)" preserveAspectRatio="xMidYMid slice"/>

  <text x="640" y="318" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="4"
        fill="#6C5CE7">
    SECTION 03
  </text>

  <text x="640" y="387" width="960" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#121826">
    Customer Growth Engine
  </text>

  <rect x="488" y="424" width="304" height="14" rx="7" fill="url(#accentBar)"/>

  <text x="640" y="486" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#596174">
    How we turn insight, product adoption, and retention into a repeatable operating system
  </text>

  <path d="M428,553 C493,582 574,590 640,590 C706,590 787,582 852,553"
        fill="none" stroke="#D7DDEA" stroke-width="2" stroke-dasharray="5 12" opacity="0.95"/>

  <circle cx="640" cy="590" r="4.5" fill="#6C5CE7"/>
  <circle cx="610" cy="588" r="3" fill="#00B8D9" opacity="0.75"/>
  <circle cx="670" cy="588" r="3" fill="#2ED573" opacity="0.75"/>
</svg>
```

## Avoid in this skill
- ❌ Do not overfill the slide with charts, cards, or multiple columns; this divider depends on low density and a single center axis.
- ❌ Do not apply `clip-path` to decorative circles or paths; only clip the `<image>` medallion.
- ❌ Do not use `<textPath>` for curved subtitle or section labels; keep all text as normal centered `<text>` with explicit `width`.
- ❌ Do not create arrow embellishments with `marker-end`; this layout does not need directional flow.

## Composition notes
- Keep all meaningful content within the central 55–65% of the canvas width; the outer edges are reserved for soft atmospheric decoration.
- The headline should be the dominant object, with the divider bar close beneath it to act like a visual underline.
- Use the hero medallion only when the section needs an emotional or thematic cue; otherwise replace it with a simple icon-like path or remove it and move text upward.
- Maintain generous negative space above and below the center stack so the slide reads instantly as a transition, not a content slide.