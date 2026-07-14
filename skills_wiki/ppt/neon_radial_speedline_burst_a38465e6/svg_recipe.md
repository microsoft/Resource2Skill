# SVG Recipe — Neon Radial Speedline Burst

## Visual mechanism
A dark cinematic slide background is filled with glowing rounded capsules that radiate outward from a central vanishing point, creating a hyperspeed tunnel effect. The middle is deliberately cleared and darkened so oversized title typography sits in a protected focal zone.

## SVG primitives needed
- 1× `<rect>` for the midnight navy/purple background
- 1× `<radialGradient>` for the central safe-zone vignette
- 1× `<linearGradient>` for subtle background depth
- 2× `<filter>`: one neon glow for speedline capsules, one soft shadow/glow for headline text
- 32–48× `<rect>` for capsule-shaped radial speedlines, using `rx` and `transform="rotate(angle cx cy)"`
- 8–16× `<circle>` for tiny star/spark accents near the burst edges
- 3× `<text>` for kicker, main title, and subtitle; each must include explicit `width=`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDepth" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#050313"/>
      <stop offset="45%" stop-color="#0B0718"/>
      <stop offset="100%" stop-color="#180725"/>
    </linearGradient>

    <radialGradient id="centerVignette" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#070415" stop-opacity="1"/>
      <stop offset="48%" stop-color="#070415" stop-opacity="0.96"/>
      <stop offset="72%" stop-color="#070415" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#070415" stop-opacity="0"/>
    </radialGradient>

    <filter id="neonGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDepth)"/>

  <g opacity="0.96" filter="url(#neonGlow)">
    <rect x="840" y="350" width="720" height="18" rx="9" fill="#00FFFF" transform="rotate(0 640 360)"/>
    <rect x="770" y="307" width="560" height="28" rx="14" fill="#FF0080" transform="rotate(-12 640 360)"/>
    <rect x="820" y="405" width="680" height="22" rx="11" fill="#8A2BE2" transform="rotate(15 640 360)"/>
    <rect x="780" y="265" width="470" height="14" rx="7" fill="#FFFFFF" transform="rotate(-24 640 360)"/>
    <rect x="790" y="455" width="620" height="34" rx="17" fill="#00FFFF" transform="rotate(30 640 360)"/>
    <rect x="810" y="205" width="760" height="26" rx="13" fill="#FF0080" transform="rotate(-38 640 360)"/>
    <rect x="740" y="512" width="510" height="16" rx="8" fill="#FFFFFF" transform="rotate(43 640 360)"/>
    <rect x="785" y="150" width="680" height="38" rx="19" fill="#8A2BE2" transform="rotate(-52 640 360)"/>

    <rect x="820" y="346" width="690" height="20" rx="10" fill="#FF0080" transform="rotate(180 640 360)"/>
    <rect x="790" y="307" width="590" height="30" rx="15" fill="#00FFFF" transform="rotate(168 640 360)"/>
    <rect x="810" y="404" width="610" height="18" rx="9" fill="#FFFFFF" transform="rotate(194 640 360)"/>
    <rect x="770" y="260" width="540" height="40" rx="20" fill="#8A2BE2" transform="rotate(154 640 360)"/>
    <rect x="800" y="468" width="760" height="24" rx="12" fill="#FF0080" transform="rotate(212 640 360)"/>
    <rect x="745" y="196" width="520" height="16" rx="8" fill="#FFFFFF" transform="rotate(140 640 360)"/>
    <rect x="815" y="525" width="720" height="36" rx="18" fill="#00FFFF" transform="rotate(228 640 360)"/>
    <rect x="770" y="128" width="600" height="22" rx="11" fill="#FF0080" transform="rotate(128 640 360)"/>

    <rect x="805" y="345" width="650" height="16" rx="8" fill="#00FFFF" transform="rotate(88 640 360)"/>
    <rect x="760" y="300" width="470" height="32" rx="16" fill="#FFFFFF" transform="rotate(74 640 360)"/>
    <rect x="825" y="392" width="740" height="26" rx="13" fill="#FF0080" transform="rotate(103 640 360)"/>
    <rect x="790" y="245" width="610" height="20" rx="10" fill="#8A2BE2" transform="rotate(61 640 360)"/>
    <rect x="760" y="462" width="500" height="14" rx="7" fill="#FFFFFF" transform="rotate(118 640 360)"/>
    <rect x="820" y="180" width="760" height="36" rx="18" fill="#00FFFF" transform="rotate(49 640 360)"/>
    <rect x="780" y="532" width="620" height="28" rx="14" fill="#8A2BE2" transform="rotate(132 640 360)"/>

    <rect x="810" y="348" width="720" height="24" rx="12" fill="#FF0080" transform="rotate(270 640 360)"/>
    <rect x="755" y="304" width="540" height="18" rx="9" fill="#00FFFF" transform="rotate(254 640 360)"/>
    <rect x="820" y="410" width="690" height="38" rx="19" fill="#8A2BE2" transform="rotate(287 640 360)"/>
    <rect x="780" y="238" width="560" height="14" rx="7" fill="#FFFFFF" transform="rotate(240 640 360)"/>
    <rect x="805" y="486" width="650" height="22" rx="11" fill="#00FFFF" transform="rotate(303 640 360)"/>
    <rect x="770" y="168" width="620" height="30" rx="15" fill="#FF0080" transform="rotate(226 640 360)"/>
    <rect x="815" y="555" width="760" height="16" rx="8" fill="#FFFFFF" transform="rotate(318 640 360)"/>
  </g>

  <g opacity="0.72">
    <circle cx="1110" cy="104" r="3" fill="#00FFFF"/>
    <circle cx="1012" cy="642" r="4" fill="#FF0080"/>
    <circle cx="170" cy="115" r="3" fill="#FFFFFF"/>
    <circle cx="96" cy="574" r="5" fill="#8A2BE2"/>
    <circle cx="1192" cy="412" r="3" fill="#FFFFFF"/>
    <circle cx="238" cy="665" r="4" fill="#00FFFF"/>
    <circle cx="1050" cy="280" r="2.5" fill="#FF0080"/>
    <circle cx="300" cy="224" r="2.5" fill="#FFFFFF"/>
  </g>

  <circle cx="640" cy="360" r="310" fill="url(#centerVignette)"/>

  <g filter="url(#titleShadow)">
    <text x="640" y="238" width="720" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="800"
          letter-spacing="8" fill="#FFFFFF">THE BEST</text>

    <text x="640" y="374" width="1180" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="128" font-weight="900"
          letter-spacing="-4" fill="#FFFFFF">MOCKUP</text>

    <text x="640" y="464" width="780" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="800"
          letter-spacing="10" fill="#00FFFF">TOOLS</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` to `<line>` elements; glow filters on lines are silently dropped, so use rounded `<rect>` capsules instead.
- ❌ Using `marker-end` for radial streaks or arrows; this effect should be pure speedlines, not arrowheads.
- ❌ Using `<mask>` to clear the center; draw a dark radial-gradient circle over the burst instead.
- ❌ Using `skewX`, `skewY`, or matrix transforms for dynamic perspective; rotate capsules around the center point with `transform="rotate(angle 640 360)"`.
- ❌ Crowding the focal zone with lines; leave a radius of roughly 200–300 px around the center for text readability.

## Composition notes
- Keep the vanishing point at or very near the exact center of the 1280×720 canvas; all capsules should visually radiate from that point.
- Reserve the central 40–45% of slide width for headline typography and protect it with a dark radial vignette.
- Use 3–4 neon colors repeatedly, not a rainbow; cyan, magenta, purple, and white create a coherent futuristic palette.
- Let many speedlines extend beyond the slide bounds to imply motion continuing off-canvas.