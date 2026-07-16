# SVG Recipe — Dynamic 2.5D Cutout Spotlight

## Visual mechanism
A cinematic 2.5D hero slide built from layered depth: a bright spotlight/ray background, oversized angled headline typography with offset shadow extrusion, and foreground cutout objects/screens that overlap the scene like a product launch frame. The trick is to separate background atmosphere, midground text, and foreground cutouts with shadows, scale contrast, and partial overlap.

## SVG primitives needed
- 1× `<rect>` for the full-slide aqua gradient background
- 8× `<path>` for subtle radial spotlight rays
- 18–25× `<circle>` for floating particle/snow highlights
- 4× `<text>` for duplicated headline/subtitle shadow + foreground typography
- 10× `<rect>` for product/device bodies, screens, highlight panels, and small UI bars
- 6× `<path>` for 2.5D product boxes and device stands/bases
- 4× `<image>` for clipped screenshot/photo content inside monitor, laptop, tablet, and phone screens
- 4× `<clipPath>` using rounded `<rect>` crops for editable device-screen image windows
- 3× `<linearGradient>` for background, product-box faces, and metallic device frames
- 1× `<radialGradient>` for the central spotlight glow
- 2× `<filter>` definitions using `feOffset`, `feGaussianBlur`, and `feMerge` for deep object shadows and bold text shadows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgAqua" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#9de9e2"/>
      <stop offset="55%" stop-color="#78d8d2"/>
      <stop offset="100%" stop-color="#47bbb9"/>
    </linearGradient>
    <radialGradient id="spotlight" cx="48%" cy="42%" r="70%">
      <stop offset="0%" stop-color="#d8fff7" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="#9be9e0" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#39aaa9" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="boxFace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1e3244"/>
      <stop offset="100%" stop-color="#071320"/>
    </linearGradient>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e7ecef"/>
      <stop offset="50%" stop-color="#8f969b"/>
      <stop offset="100%" stop-color="#d9dddf"/>
    </linearGradient>
    <filter id="deepShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="10" dy="14"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="typeShadow" x="-15%" y="-15%" width="140%" height="140%">
      <feOffset dx="8" dy="10"/>
      <feGaussianBlur stdDeviation="1.2"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .02  0 0 0 0 .11  0 0 0 0 .22  0 0 0 .95 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="clipMonitor"><rect x="774" y="264" width="300" height="168" rx="8"/></clipPath>
    <clipPath id="clipLaptop"><rect x="585" y="383" width="302" height="170" rx="7"/></clipPath>
    <clipPath id="clipTablet"><rect x="1063" y="344" width="112" height="170" rx="10"/></clipPath>
    <clipPath id="clipPhone"><rect x="1176" y="405" width="50" height="102" rx="10"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgAqua)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>

  <path d="M0 720 L500 382 L80 0 L0 0 Z" fill="#ffffff" opacity="0.10"/>
  <path d="M0 720 L548 390 L335 0 L245 0 Z" fill="#ffffff" opacity="0.08"/>
  <path d="M0 720 L598 398 L650 0 L530 0 Z" fill="#ffffff" opacity="0.09"/>
  <path d="M0 720 L650 405 L1010 0 L880 0 Z" fill="#ffffff" opacity="0.08"/>
  <path d="M0 720 L704 416 L1280 68 L1280 0 L1210 0 Z" fill="#ffffff" opacity="0.10"/>
  <path d="M0 720 L560 500 L1280 520 L1280 654 Z" fill="#36b9b7" opacity="0.15"/>
  <path d="M0 720 L470 430 L0 300 Z" fill="#ffffff" opacity="0.07"/>
  <path d="M0 720 L770 430 L1280 275 L1280 365 Z" fill="#ffffff" opacity="0.06"/>

  <circle cx="98" cy="126" r="2.4" fill="#ffffff" opacity=".42"/>
  <circle cx="205" cy="312" r="1.8" fill="#ffffff" opacity=".35"/>
  <circle cx="332" cy="84" r="2.2" fill="#ffffff" opacity=".30"/>
  <circle cx="474" cy="214" r="1.7" fill="#ffffff" opacity=".40"/>
  <circle cx="632" cy="128" r="2.6" fill="#ffffff" opacity=".28"/>
  <circle cx="790" cy="92" r="1.6" fill="#ffffff" opacity=".45"/>
  <circle cx="928" cy="182" r="2.1" fill="#ffffff" opacity=".38"/>
  <circle cx="1138" cy="104" r="2.7" fill="#ffffff" opacity=".34"/>
  <circle cx="1184" cy="310" r="1.8" fill="#ffffff" opacity=".35"/>
  <circle cx="1010" cy="612" r="2.4" fill="#ffffff" opacity=".24"/>
  <circle cx="690" cy="610" r="1.9" fill="#ffffff" opacity=".30"/>
  <circle cx="396" cy="575" r="2.0" fill="#ffffff" opacity=".25"/>

  <g transform="rotate(-7 265 160)">
    <text x="52" y="145" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="74" font-weight="900" letter-spacing="-3" fill="#072948" opacity=".95">LEVIDIO 5</text>
    <text x="43" y="134" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="74" font-weight="900" letter-spacing="-3" fill="#d60018" filter="url(#typeShadow)">LEVIDIO 5</text>
    <text x="68" y="218" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="900" font-style="italic" letter-spacing="-2" fill="#0a2447" opacity=".72">QUICK TESTIMONIAL</text>
    <text x="57" y="207" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="900" font-style="italic" letter-spacing="-2" fill="#153a70">QUICK TESTIMONIAL</text>
  </g>

  <g filter="url(#deepShadow)">
    <path d="M80 444 L188 420 L188 665 L80 635 Z" fill="#0a1524"/>
    <path d="M188 420 L292 455 L292 690 L188 665 Z" fill="#13263b"/>
    <path d="M80 444 L188 420 L292 455 L183 480 Z" fill="#24374a"/>
    <text x="101" y="515" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#c7d4df">LEVIDIO</text>

    <path d="M198 382 L386 412 L386 696 L198 650 Z" fill="url(#boxFace)"/>
    <path d="M386 412 L482 462 L482 692 L386 696 Z" fill="#102033"/>
    <path d="M198 382 L303 342 L482 386 L386 412 Z" fill="#253a4e"/>
    <text x="278" y="532" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="600" fill="#d9eef5">LEVIDIO</text>
    <path d="M402 528 l16 8 l-16 8 z" fill="#ef1630"/>

    <path d="M455 432 L572 452 L572 673 L455 646 Z" fill="#16293b"/>
    <path d="M572 452 L630 482 L630 665 L572 673 Z" fill="#0c1827"/>
    <text x="485" y="536" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#d7e4ec">LEVIDIO</text>
  </g>

  <g filter="url(#deepShadow)">
    <rect x="748" y="235" width="352" height="225" rx="18" fill="url(#metal)"/>
    <rect x="764" y="252" width="320" height="197" rx="10" fill="#1b1f25"/>
    <image href="https://images.example.com/screenshots/video-editor-dashboard-hero.jpg" x="774" y="264" width="300" height="168" clip-path="url(#clipMonitor)"/>
    <path d="M895 460 L960 460 L982 564 L872 564 Z" fill="#b6bec4"/>
    <rect x="835" y="560" width="185" height="18" rx="9" fill="#d8dddf"/>

    <path d="M558 372 L900 372 L926 582 L532 582 Z" fill="#e9eef0"/>
    <rect x="574" y="386" width="326" height="181" rx="12" fill="#171b20"/>
    <image href="https://images.example.com/screenshots/webpage-testimonial-builder.jpg" x="585" y="383" width="302" height="170" clip-path="url(#clipLaptop)"/>
    <path d="M502 584 L956 584 L1012 634 L448 634 Z" fill="#b8c0c5"/>
    <path d="M448 634 L1012 634 L956 660 L504 660 Z" fill="#8d969c"/>

    <rect x="1048" y="322" width="144" height="218" rx="18" fill="#2d3338"/>
    <rect x="1058" y="335" width="124" height="192" rx="14" fill="#11161b"/>
    <image href="https://images.example.com/screenshots/course-cover-green-mountains.jpg" x="1063" y="344" width="112" height="170" clip-path="url(#clipTablet)"/>

    <rect x="1163" y="388" width="76" height="140" rx="17" fill="#263039"/>
    <rect x="1173" y="400" width="58" height="116" rx="12" fill="#0d1217"/>
    <image href="https://images.example.com/screenshots/mobile-sales-page.jpg" x="1176" y="405" width="50" height="102" clip-path="url(#clipPhone)"/>
  </g>

  <rect x="0" y="0" width="1280" height="720" fill="none" stroke="#000000" stroke-width="0"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to isolate the foreground cutout; use transparent PNG `<image>` assets or editable vector `<path>` silhouettes instead.
- ❌ Do not apply `clip-path` to groups, rectangles, or paths for device mockups; only clip the `<image>` screenshots.
- ❌ Do not use `<use>` to repeat particles or product-box geometry; duplicate simple circles/paths directly so PowerPoint receives editable shapes.
- ❌ Do not rely on `marker-end` for angled callouts or motion arrows; if arrows are needed, build them from `<line>` plus small triangle `<path>`.
- ❌ Avoid tiny text inside screenshot mockups as live SVG text; use clipped screenshots for believable UI detail and reserve editable text for the main message.

## Composition notes
- Keep the largest headline in the upper-left third, rotated slightly upward for kinetic energy; duplicate it behind with a dark offset to create the chunky 2.5D extrusion.
- Anchor the foreground cutout/product cluster along the bottom edge and let it overlap the background rays; shadows should be strongest here to sell depth.
- Use aqua/cyan as the atmospheric field, then introduce one aggressive accent color such as red, yellow, or electric blue for the headline.
- Leave the top-right relatively open so rays, particles, and device silhouettes can breathe without competing with the main title.