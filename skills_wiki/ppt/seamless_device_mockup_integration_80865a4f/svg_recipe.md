# SVG Recipe — Seamless Device Mockup Integration

## Visual mechanism
Embed a digital product screenshot into a believable vector-built device frame, then ground it with soft shadows, desk props, and small branded collateral so the screen feels like a premium product photograph rather than a flat capture.

## SVG primitives needed
- 1× full-slide `<rect>` for the warm studio background
- 2× `<radialGradient>` / `<linearGradient>` fills for subtle tabletop lighting and metallic device parts
- 3× `<filter>` definitions for soft object shadows and screen glow
- 4× `<ellipse>` for blurred contact shadows under cards, monitor, keyboard, and mouse
- 2× rotated `<rect>` cards for floating stationery / brand collateral
- 5× `<path>` decorative curves and card edge details for premium branded print material
- 1× monitor bezel `<rect>` plus 1× inner screen `<rect>` for the device frame
- 1× `<clipPath>` with rounded `<rect>` applied to the website hero `<image>`
- 1× `<image>` for the screen’s hero photo, cropped inside the website layout
- Multiple small `<rect>` elements for website UI blocks, navigation, CTA panels, keyboard keys, and base details
- 4× `<path>` elements for metallic monitor stand, base, and angled product-shot geometry
- Several `<text>` elements with explicit `width` for brand labels, website copy, slide headline, and UI captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWarm" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f4dda3"/>
      <stop offset="55%" stop-color="#efd28f"/>
      <stop offset="100%" stop-color="#e7c374"/>
    </linearGradient>
    <radialGradient id="tableGlow" cx="50%" cy="54%" r="58%">
      <stop offset="0%" stop-color="#fff1c8" stop-opacity="0.52"/>
      <stop offset="70%" stop-color="#fff1c8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="34%" stop-color="#c9c9c9"/>
      <stop offset="68%" stop-color="#f5f5f5"/>
      <stop offset="100%" stop-color="#9e9e9e"/>
    </linearGradient>
    <linearGradient id="screenSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.20"/>
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.10"/>
    </linearGradient>
    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="contactBlur" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <filter id="screenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <clipPath id="heroCrop" clipPathUnits="userSpaceOnUse">
      <rect x="836" y="164" width="118" height="178" rx="3"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWarm)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#tableGlow)"/>

  <ellipse cx="332" cy="475" rx="190" ry="24" fill="#7a5b25" opacity="0.22" filter="url(#contactBlur)"/>
  <ellipse cx="874" cy="465" rx="210" ry="30" fill="#6e5424" opacity="0.23" filter="url(#contactBlur)"/>
  <ellipse cx="944" cy="515" rx="132" ry="13" fill="#6e5424" opacity="0.22" filter="url(#contactBlur)"/>
  <ellipse cx="1124" cy="500" rx="48" ry="13" fill="#6e5424" opacity="0.18" filter="url(#contactBlur)"/>

  <rect x="415" y="184" width="186" height="285" rx="2" fill="#fafafa" transform="rotate(14 508 326)" filter="url(#softShadow)"/>
  <rect x="211" y="196" width="186" height="285" rx="2" fill="#fbfbfb" transform="rotate(14 304 338)" filter="url(#softShadow)"/>

  <path d="M282 178 C268 245 323 330 387 291 C423 269 374 207 350 180" fill="none" stroke="#d5a04c" stroke-width="8" stroke-linecap="round" transform="rotate(14 304 338)"/>
  <path d="M254 285 C235 354 304 417 370 363 C411 329 382 274 331 302" fill="none" stroke="#c99039" stroke-width="8" stroke-linecap="round" transform="rotate(14 304 338)"/>
  <path d="M448 391 C479 350 560 367 565 430 C568 467 537 498 494 493" fill="none" stroke="#c99039" stroke-width="8" stroke-linecap="round" transform="rotate(14 508 326)"/>
  <path d="M424 449 C457 419 516 423 547 467" fill="none" stroke="#d5a04c" stroke-width="7" stroke-linecap="round" transform="rotate(14 508 326)"/>

  <text x="257" y="445" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#111111" transform="rotate(14 304 338)">Versus Co.</text>
  <text x="468" y="254" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600" fill="#111111" transform="rotate(14 508 326)">Miley Cortys</text>
  <text x="475" y="286" width="118" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="8" fill="#6b6b6b" transform="rotate(14 508 326)">+1-202-555-0133</text>
  <text x="468" y="304" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="8" fill="#6b6b6b" transform="rotate(14 508 326)">miley.core@versus.com</text>

  <g transform="rotate(3 840 282)">
    <path d="M726 426 L882 426 L866 457 L710 457 Z" fill="url(#chrome)" stroke="#8d8d8d" stroke-width="1"/>
    <path d="M841 421 L874 421 L911 330 L895 330 Z" fill="url(#chrome)" stroke="#6f6f6f" stroke-width="2"/>
    <path d="M747 420 L770 420 L815 331 L801 329 Z" fill="url(#chrome)" stroke="#6f6f6f" stroke-width="2"/>
    <path d="M706 452 L885 452 L914 468 L681 468 Z" fill="#d8d8d8" stroke="#9a9a9a" stroke-width="1"/>
    <rect x="680" y="120" width="304" height="286" rx="9" fill="#070707" filter="url(#softShadow)"/>
    <rect x="698" y="141" width="269" height="244" rx="2" fill="#f9f9f7"/>
    <rect x="698" y="141" width="269" height="244" rx="2" fill="url(#screenSheen)" opacity="0.65" filter="url(#screenGlow)"/>

    <rect x="698" y="141" width="36" height="24" fill="#121212"/>
    <text x="707" y="157" width="28" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="6" fill="#ffffff">STUDIO</text>
    <text x="760" y="155" width="38" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="5" fill="#777777">Collection</text>
    <text x="810" y="155" width="28" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="5" font-weight="700" fill="#111111">New</text>
    <text x="848" y="155" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="5" fill="#777777">Trending</text>
    <text x="895" y="155" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="5" fill="#777777">Projects</text>

    <text x="720" y="210" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600" fill="#101010">Van Gend</text>
    <text x="720" y="242" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600" fill="#101010">Residence</text>
    <text x="724" y="294" width="88" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="6" fill="#555555">Urban living meets a calm interior language: warm textures, soft daylight, and fresh botanical forms.</text>
    <text x="724" y="338" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="6" font-weight="700" fill="#111111">DETAILS +</text>

    <image href="https://images.example.com/interior-design-chair-plant-website-hero.jpg" x="836" y="164" width="118" height="178" preserveAspectRatio="xMidYMid slice" clip-path="url(#heroCrop)"/>
    <rect x="738" y="360" width="72" height="28" fill="#ffc400"/>
    <text x="762" y="377" width="38" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="6" font-weight="700" fill="#111111">GALLERY</text>
    <rect x="810" y="342" width="72" height="46" fill="#151515"/>
    <text x="820" y="374" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" fill="#ffffff">02</text>
    <line x1="850" y1="366" x2="873" y2="366" stroke="#ffffff" stroke-width="1"/>
    <text x="940" y="159" width="14" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="8" fill="#111111">×</text>
    <rect x="952" y="360" width="14" height="28" fill="#ffc400"/>
  </g>

  <g transform="rotate(3 944 509)">
    <path d="M828 493 L1034 493 L1078 513 L858 513 Z" fill="#dddddd" stroke="#9e9e9e" stroke-width="1"/>
    <path d="M853 497 L1028 497 L1054 507 L874 507 Z" fill="#4d4d4d"/>
    <line x1="875" y1="500" x2="1030" y2="500" stroke="#9a9a9a" stroke-width="1"/>
    <line x1="887" y1="504" x2="1044" y2="504" stroke="#9a9a9a" stroke-width="1"/>
    <line x1="912" y1="496" x2="924" y2="509" stroke="#777777" stroke-width="1"/>
    <line x1="956" y1="496" x2="966" y2="510" stroke="#777777" stroke-width="1"/>
    <line x1="1000" y1="496" x2="1008" y2="510" stroke="#777777" stroke-width="1"/>
  </g>

  <ellipse cx="1125" cy="486" rx="42" ry="17" fill="url(#chrome)" stroke="#a8a8a8" stroke-width="1" transform="rotate(3 1125 486)"/>
  <ellipse cx="1113" cy="481" rx="18" ry="6" fill="#ffffff" opacity="0.55" transform="rotate(3 1113 481)"/>

  <text x="88" y="105" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" letter-spacing="2" fill="#8b6d34" opacity="0.72">PRODUCT SHOWCASE</text>
  <text x="88" y="150" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700" fill="#2b2110">Digital work, placed in the real world.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a transparent PNG mockup for the entire device if the goal is editable PowerPoint; build the bezel, stand, base, and shadows as SVG shapes.
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` for perspective device angles; approximate depth with rotated groups, trapezoid `<path>` bases, and layered highlights.
- ❌ Do not apply `clip-path` to UI rectangles or monitor frames; use clipping only on the embedded `<image>` screenshot/photo.
- ❌ Do not use `<mask>` for rounded screen crops; use `<clipPath>` with a rounded rect applied directly to the `<image>`.
- ❌ Do not rely on tiny raster text inside the screenshot; recreate key UI labels with editable `<text>` where possible.

## Composition notes
- Put the hero device on the right 45–55% of the canvas and let it occupy roughly 55–65% of slide height so the embedded screen content remains readable.
- Use left-side negative space for a short launch headline, or replace it with branded cards/collateral when the device itself is the message.
- Ground every floating object with a wide blurred ellipse shadow; the shadow sells the physical integration more than the bezel detail.
- Keep the palette restrained: warm studio background, black/white device frame, one accent color from the product UI, and subtle chrome gradients for hardware.