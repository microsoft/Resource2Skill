# SVG Recipe — Programmatic Organic Fluid Vectors

## Visual mechanism
Stack several full-width, overlapping organic wave paths along the slide bottom, each with a distinct modern color, to create a fluid vector “terrain” that frames the content. Keep the typography in a calm negative-space field above the waves, with small geometric accents that echo the motion without competing with the title.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 3× large `<path>` shapes for the layered organic footer waves
- 3× `<linearGradient>` definitions for subtle dimensional color across the wave layers
- 1× `<filter id="waveShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for a soft lifted shadow on the foreground wave
- 1× `<rect>` for the coral title accent bar
- 2× `<text>` blocks for the main title and subtitle, with explicit `width` attributes
- 7× `<circle>` elements for floating decorative dots in cyan, coral, yellow, and navy
- 2× `<ellipse>` elements for soft orbital accent marks
- 2× thin `<path>` elements for small decorative swooshes in the negative space

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cyanWave" x1="0" y1="410" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A7DDDA"/>
      <stop offset="0.55" stop-color="#91CDCD"/>
      <stop offset="1" stop-color="#78BABB"/>
    </linearGradient>

    <linearGradient id="yellowWave" x1="0" y1="465" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFE17C"/>
      <stop offset="0.62" stop-color="#FCD269"/>
      <stop offset="1" stop-color="#F0B94F"/>
    </linearGradient>

    <linearGradient id="navyWave" x1="0" y1="520" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#50536C"/>
      <stop offset="0.5" stop-color="#3E4155"/>
      <stop offset="1" stop-color="#272A3C"/>
    </linearGradient>

    <filter id="waveShadow" x="-5%" y="-20%" width="110%" height="140%">
      <feOffset dx="0" dy="-8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.10  0 0 0 0 0.11  0 0 0 0 0.18  0 0 0 0.22 0"
        result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#F5F6F8"/>

  <!-- Floating organic accents -->
  <circle cx="1060" cy="112" r="7" fill="#F47460"/>
  <circle cx="1128" cy="168" r="4" fill="#91CDCD"/>
  <circle cx="1018" cy="220" r="3.5" fill="#FCD269"/>
  <circle cx="860" cy="88" r="5" fill="#3E4155" opacity="0.28"/>
  <circle cx="150" cy="570" r="5" fill="#91CDCD" opacity="0.45"/>
  <circle cx="230" cy="620" r="3.5" fill="#FCD269" opacity="0.8"/>
  <circle cx="1188" cy="420" r="6" fill="#F47460" opacity="0.7"/>

  <ellipse cx="1025" cy="292" rx="48" ry="11" fill="none" stroke="#91CDCD" stroke-width="2" opacity="0.5" transform="rotate(-18 1025 292)"/>
  <ellipse cx="1120" cy="342" rx="30" ry="7" fill="none" stroke="#FCD269" stroke-width="2" opacity="0.55" transform="rotate(21 1120 342)"/>

  <path d="M917 190 C944 164, 986 166, 1012 193" fill="none" stroke="#F47460" stroke-width="5" stroke-linecap="round" opacity="0.7"/>
  <path d="M980 246 C1012 232, 1048 237, 1078 260" fill="none" stroke="#3E4155" stroke-width="3" stroke-linecap="round" opacity="0.2"/>

  <!-- Title accent -->
  <rect x="92" y="142" width="86" height="9" rx="4.5" fill="#F47460"/>

  <!-- Typography -->
  <text x="88" y="220" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64" font-weight="800" letter-spacing="1.5" fill="#3E4155">
    <tspan x="88" dy="0">ORGANIC</tspan>
    <tspan x="88" dy="76">FLUID DESIGN</tspan>
  </text>

  <text x="92" y="404" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#6D7184">
    <tspan x="92" dy="0">Abstract mathematical geometry for modern presentations</tspan>
    <tspan x="92" dy="34" fill="#8A8EA0">Native editable vectors, built for premium transition screens.</tspan>
  </text>

  <!-- Back wave: high and calm -->
  <path d="
    M 0 440
    C 72 400, 136 391, 206 426
    C 292 468, 350 455, 430 410
    C 506 367, 588 374, 668 424
    C 746 473, 812 486, 884 445
    C 964 399, 1035 386, 1114 421
    C 1184 452, 1236 456, 1280 428
    L 1280 720
    L 0 720
    Z" fill="url(#cyanWave)"/>

  <!-- Middle wave: brighter, crossing the cyan wave -->
  <path d="
    M 0 520
    C 78 482, 145 466, 224 501
    C 306 537, 365 560, 450 512
    C 536 463, 602 451, 684 495
    C 762 536, 835 561, 914 527
    C 1008 486, 1068 454, 1154 491
    C 1210 515, 1252 523, 1280 505
    L 1280 720
    L 0 720
    Z" fill="url(#yellowWave)"/>

  <!-- Front wave: dark grounding layer -->
  <path filter="url(#waveShadow)" d="
    M 0 596
    C 66 558, 122 544, 204 574
    C 292 607, 354 628, 438 588
    C 520 549, 585 534, 670 574
    C 756 615, 820 647, 910 604
    C 1004 559, 1072 540, 1160 578
    C 1214 602, 1252 610, 1280 588
    L 1280 720
    L 0 720
    Z" fill="url(#navyWave)"/>

  <!-- Small foreground droplets embedded in the footer -->
  <circle cx="104" cy="664" r="8" fill="#FCD269" opacity="0.9"/>
  <circle cx="178" cy="690" r="4" fill="#91CDCD" opacity="0.95"/>
  <circle cx="1098" cy="648" r="6" fill="#F47460" opacity="0.95"/>
</svg>
```

## Avoid in this skill
- ❌ Do not render the waves as a single raster image; the value of this technique is editable, recolorable native vector geometry.
- ❌ Do not use `<pattern>` fills for the wave texture; PowerPoint translation will drop them and the fluid effect becomes flat or broken.
- ❌ Do not use `clip-path` on wave paths to trim the footer; clipping only translates reliably on `<image>` elements.
- ❌ Do not use `<mask>` for soft wave intersections; instead, layer opaque or semi-opaque paths directly.
- ❌ Do not overuse hundreds of tiny decorative dots; the visual should feel premium and spacious, not like confetti.
- ❌ Do not put filters on `<line>` elements; if accents need softness, use paths, circles, ellipses, or rects.

## Composition notes
- Keep the wave stack in the bottom 30–40% of the slide so the upper 60% remains clean for title content.
- Anchor the main title left, roughly x=80–100 and y=200–350, with a short coral accent bar above it.
- Use three wave layers with clear vertical separation: cyan highest/back, yellow middle, dark navy lowest/front.
- Scatter only a few small dots and orbital accents in the open space, preferably toward the right side, to imply motion without clutter.