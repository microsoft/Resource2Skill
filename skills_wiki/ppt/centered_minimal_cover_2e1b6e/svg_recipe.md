# SVG Recipe — Centered Minimal Cover

## Visual mechanism
A quiet, high-end title slide built around a perfectly centered headline stack, with generous negative space and only subtle atmospheric decoration. The premium feel comes from restrained typography, soft gradient lighting, and a tiny accent rule rather than heavy framing.

## SVG primitives needed
- 1× `<rect>` for the full-slide background wash
- 2× `<radialGradient>` for soft corner illumination
- 1× `<linearGradient>` for the headline/accent color system
- 3× `<circle>` for blurred ambient light pools
- 2× `<path>` for barely visible organic editorial shapes
- 1× `<rect>` for the centered accent rule beneath the headline
- 3× `<text>` elements for eyebrow, headline, and subtitle
- 1× `<filter id="softBlur">` applied to ambient circles and decorative paths
- 1× `<filter id="titleShadow">` applied subtly to the headline text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="48%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <radialGradient id="coolGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#BFD7FF" stop-opacity="0.58"/>
      <stop offset="55%" stop-color="#BFD7FF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#BFD7FF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="warmGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F3D6B1" stop-opacity="0.42"/>
      <stop offset="62%" stop-color="#F3D6B1" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#F3D6B1" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="inkAccent" x1="390" y1="0" x2="890" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#172033"/>
      <stop offset="62%" stop-color="#243B63"/>
      <stop offset="100%" stop-color="#3166A5"/>
    </linearGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="titleShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="12"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.08  0 0 0 0 0.12  0 0 0 0 0.18  0 0 0 0.16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <circle cx="170" cy="90" r="190" fill="url(#coolGlow)" filter="url(#softBlur)" opacity="0.82"/>
  <circle cx="1135" cy="640" r="230" fill="url(#warmGlow)" filter="url(#softBlur)" opacity="0.74"/>
  <circle cx="1030" cy="120" r="120" fill="#DDEAFE" filter="url(#softBlur)" opacity="0.28"/>

  <path d="M1040 35
           C1115 8 1205 34 1238 95
           C1274 161 1235 231 1152 230
           C1067 229 1010 172 1008 109
           C1007 76 1016 46 1040 35Z"
        fill="#E7EEF9" opacity="0.38" filter="url(#softBlur)"/>

  <path d="M43 594
           C106 542 190 541 242 594
           C292 645 267 705 184 718
           C104 731 36 699 22 657
           C14 631 21 612 43 594Z"
        fill="#F1E6D8" opacity="0.38" filter="url(#softBlur)"/>

  <path d="M265 154 C393 106 521 105 649 154"
        fill="none" stroke="#C9D5E6" stroke-width="1.2" stroke-linecap="round" opacity="0.55"/>
  <path d="M631 566 C761 615 890 614 1019 566"
        fill="none" stroke="#D9C9B8" stroke-width="1.2" stroke-linecap="round" opacity="0.5"/>

  <g transform="translate(0 0)">
    <text x="640" y="224" width="520"
          text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="16"
          font-weight="700"
          letter-spacing="4"
          fill="#6B7A90">
      2026 STRATEGY BRIEF
    </text>

    <text x="640" y="324" width="920"
          text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="70"
          font-weight="750"
          letter-spacing="-2.2"
          fill="url(#inkAccent)"
          filter="url(#titleShadow)">
      <tspan x="640" dy="0">Centered Minimal</tspan>
      <tspan x="640" dy="78">Cover System</tspan>
    </text>

    <rect x="590" y="472" width="100" height="4" rx="2" fill="#3166A5" opacity="0.92"/>

    <text x="640" y="526" width="760"
          text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22"
          font-weight="400"
          line-height="1.35"
          fill="#536173">
      <tspan x="640" dy="0">A calm opening slide for executive narratives,</tspan>
      <tspan x="640" dy="32">section breaks, and concise strategic framing.</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Dense grids, cards, charts, or icon clusters; they break the low-density cover-shell purpose
- ❌ Large photo backgrounds unless the deck specifically requires a photographic editorial cover
- ❌ Heavy borders, boxed title panels, or centered rectangles that make the slide feel like a template
- ❌ More than one strong accent color; the look depends on restraint and quiet hierarchy
- ❌ Tiny subtitles under 18px or long subtitles beyond two lines, which weaken the centered focal point

## Composition notes
- Keep the title stack centered both horizontally and optically vertically, usually around y=300–390 on a 1280×720 canvas.
- Reserve at least 35–45% of the slide as clean negative space; decoration should sit at the corners or edges.
- Use the brightest or highest-contrast element only for the headline and the small accent rule.
- If the subtitle is omitted, move the accent rule slightly lower or increase spacing below the headline so the cover still feels intentional.