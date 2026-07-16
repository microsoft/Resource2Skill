# SVG Recipe — macOS UI Card with Dynamic Callout

## Visual mechanism
A dimensional macOS-style UI card floats in the center of a dark atmospheric desktop scene, while an oversized executive callout headline dominates the top and small tilted UI widgets orbit the hero card. Soft shadows, glow halos, traffic-light controls, hand-drawn arrows, and rotated cards create a premium “software tutorial thumbnail” energy while remaining editable SVG/PPT shapes.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark atmospheric background
- 2× `<radialGradient>` / `<linearGradient>` for vignette, card lighting, and yellow macOS header glow
- 3× `<filter>` definitions for soft card shadow, neon glow, and text drop shadow
- 1× large rounded `<rect>` for the central macOS UI card body
- 1× rounded `<rect>` for the yellow top header / app-icon cap
- 12× small `<circle>` elements for macOS traffic-light / toolbar dot details
- 4× thin `<rect>` elements for muted UI content lines inside the card
- 2× large `<text>` elements for the stacked callout headline
- 6× small rotated widget groups made from `<rect>`, `<circle>`, `<text>`, and simple glyph paths
- 8× curved `<path>` strokes for hand-drawn motion arrows
- 8× small filled `<path>` arrowheads because `marker-end` should not be used
- Several decorative `<path>` glyphs for music, phone, waveform, fingerprint, folder, and link icons

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#292b2d"/>
      <stop offset="0.55" stop-color="#1f2022"/>
      <stop offset="1" stop-color="#151618"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="53%" r="45%">
      <stop offset="0" stop-color="#f5dc00" stop-opacity="0.42"/>
      <stop offset="0.35" stop-color="#f5dc00" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="yellowCap" x1="0" y1="270" x2="0" y2="385">
      <stop offset="0" stop-color="#fff700"/>
      <stop offset="1" stop-color="#ffd600"/>
    </linearGradient>
    <linearGradient id="cardWhite" x1="0" y1="350" x2="0" y2="620">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#eef0f1"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="9"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="yellowGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="17"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <text x="207" y="108" width="870" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900" letter-spacing="4" fill="#f7f7f7" filter="url(#textShadow)">YOU'RE USING IT</text>
  <text x="426" y="201" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="92" font-weight="900" letter-spacing="2" fill="#ff1111" filter="url(#textShadow)">WRONG</text>

  <rect x="474" y="271" width="350" height="90" rx="64" fill="#ffe900" opacity="0.62" filter="url(#yellowGlow)"/>
  <rect x="474" y="271" width="350" height="352" rx="72" fill="url(#cardWhite)" filter="url(#softShadow)" stroke="#d8dcde" stroke-width="1.5"/>
  <path d="M474 343 C474 302 504 271 557 271 L741 271 C794 271 824 302 824 343 L824 361 L474 361 Z" fill="url(#yellowCap)"/>
  <line x1="474" y1="361" x2="824" y2="361" stroke="#e6e1b8" stroke-width="1"/>
  <circle cx="495" cy="371" r="4.5" fill="#d6c779"/>
  <circle cx="517" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="539" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="561" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="583" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="605" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="627" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="649" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="671" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="693" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="715" cy="371" r="4.5" fill="#e2d17a"/>
  <circle cx="737" cy="371" r="4.5" fill="#e2d17a"/>
  <rect x="516" y="445" width="267" height="7" rx="3.5" fill="#d8d9da"/>
  <rect x="516" y="534" width="267" height="7" rx="3.5" fill="#d8d9da"/>

  <g transform="translate(52 278) rotate(11)">
    <rect x="0" y="0" width="238" height="68" rx="13" fill="#eef1f3" filter="url(#softShadow)" stroke="#cfd3d7"/>
    <text x="14" y="23" width="165" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#111">Take Me Back to London</text>
    <text x="14" y="43" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#555">Ed Sheeran</text>
    <circle cx="205" cy="34" r="19" fill="#ff1b2d"/>
    <path d="M199 24 L219 34 L199 44 Z" fill="#ffffff"/>
  </g>

  <g transform="translate(-35 433) rotate(-4)">
    <rect x="0" y="0" width="196" height="64" rx="8" fill="#f3f5f7" filter="url(#softShadow)" stroke="#d7dbe0"/>
    <text x="15" y="35" width="95" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#222">Finder Ever</text>
    <rect x="126" y="20" width="37" height="28" rx="4" fill="#13b8f1"/>
  </g>

  <g transform="translate(1065 288) rotate(-12)">
    <rect x="0" y="0" width="166" height="70" rx="15" fill="#e9ecef" filter="url(#softShadow)" stroke="#c9cdd2"/>
    <path d="M22 32 L22 45 M30 24 L30 50 M38 18 L38 53 M46 20 L46 51 M54 14 L54 55 M62 22 L62 48 M70 27 L70 43" stroke="#222" stroke-width="3" stroke-linecap="round" fill="none"/>
    <rect x="106" y="15" width="44" height="44" rx="12" fill="#19dd37"/>
    <path d="M120 27 C130 42 134 34 141 44" stroke="#fff" stroke-width="5" stroke-linecap="round" fill="none"/>
    <circle cx="150" cy="10" r="15" fill="#ff1010"/>
    <text x="145" y="15" width="20" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="900" fill="#fff">1</text>
  </g>

  <g transform="translate(945 489) rotate(-10)">
    <rect x="0" y="0" width="150" height="50" rx="22" fill="#f5f6f7" filter="url(#softShadow)" stroke="#d5d8dc"/>
    <path d="M23 18 L23 34 M29 14 L29 38 M35 20 L35 32 M41 16 L41 36" stroke="#333" stroke-width="2" stroke-linecap="round"/>
    <path d="M76 34 C63 28 71 12 82 18 C90 23 79 35 71 40" stroke="#555" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M117 14 C101 21 112 41 124 25 M110 33 C125 48 132 20 119 18" stroke="#555" stroke-width="3" fill="none" stroke-linecap="round"/>
  </g>

  <g transform="translate(1160 415) rotate(7)">
    <rect x="0" y="0" width="155" height="66" rx="12" fill="#f3f5f8" filter="url(#softShadow)" stroke="#d8dce1"/>
    <rect x="29" y="22" width="15" height="15" rx="3" fill="#ff1433"/>
    <rect x="68" y="18" width="70" height="31" rx="15" fill="#fff" stroke="#ffc8d1"/>
    <text x="82" y="38" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" fill="#ff6b82">Resume</text>
  </g>

  <g transform="translate(1085 576) rotate(-20)">
    <rect x="0" y="0" width="198" height="120" rx="16" fill="#f3f4f5" filter="url(#softShadow)" stroke="#d8dce0"/>
    <circle cx="39" cy="45" r="18" fill="#ff2ca8"/>
    <path d="M29 45 C29 32 49 32 49 45 M33 45 C33 37 45 37 45 45 M37 45 C37 42 41 42 41 45" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>
    <text x="27" y="76" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#111">Notes</text>
    <text x="27" y="96" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#333">Touch ID or enter the login password…</text>
  </g>

  <path d="M414 365 C380 350 359 377 333 357" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M332 357 L344 352 L342 365 Z" fill="#ffffff"/>
  <path d="M361 426 C313 425 280 455 234 446" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M233 446 L245 438 L245 452 Z" fill="#ffffff"/>
  <path d="M421 512 C392 525 368 531 330 519" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M329 519 L342 513 L340 527 Z" fill="#ffffff"/>
  <path d="M420 602 C389 618 356 635 329 648" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M329 648 L337 637 L342 650 Z" fill="#ffffff"/>
  <path d="M889 347 C923 365 969 331 1005 340" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M1005 340 L994 332 L992 346 Z" fill="#ffffff"/>
  <path d="M906 425 C944 395 970 430 1009 405 C1030 392 1039 395 1025 414 C1007 438 963 420 991 440 C1018 459 1054 434 1101 439" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M1101 439 L1089 432 L1089 446 Z" fill="#ffffff"/>
  <path d="M858 511 C878 516 891 507 912 513" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M912 513 L900 506 L900 520 Z" fill="#ffffff"/>
  <path d="M877 603 C913 641 970 627 1029 652" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M1029 652 L1015 646 L1018 660 Z" fill="#ffffff"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` for curved arrows; draw arrowheads manually with small filled `<path>` triangles.
- ❌ Do not apply filters to `<line>` elements; use shadows/glows on cards, text, circles, or paths instead.
- ❌ Do not use `<mask>` or clipping on vector shapes for the card; rounded rectangles and layered paths translate more reliably.
- ❌ Do not create reusable widgets with `<use>` or `<symbol>`; duplicate the editable primitives directly.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint text boxes need explicit widths.

## Composition notes
- Keep the top 25–30% of the slide reserved for the oversized callout headline; use white for the setup phrase and red/neon for the punch word.
- Center the macOS UI card slightly below the midpoint so it feels like the hero object under the headline.
- Surrounding mini-widgets should be tilted, partially cropped, and varied in scale to imply a busy desktop ecosystem without stealing focus.
- Use a dark vignette plus central yellow glow to separate the white card from the background and make the scene feel dimensional.