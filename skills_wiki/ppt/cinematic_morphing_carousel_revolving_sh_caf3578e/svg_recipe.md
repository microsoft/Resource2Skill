# SVG Recipe — Cinematic Morphing Carousel

## Visual mechanism
A premium carousel is built as a sequence of near-identical slides where the same named product cards change position, scale, depth, and opacity; PowerPoint Morph turns those static layout states into a fluid revolving showcase. The foreground card is large, sharp, and centered, while neighboring cards recede toward the edges with smaller scale, lower opacity, and stronger atmospheric depth.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark cinematic background
- 2× `<radialGradient>` fills for soft colored atmosphere behind the carousel
- 1× `<linearGradient>` for the floor reflection fade/ambient stage
- 1× `<filter id="softShadow">` applied to card backing rectangles
- 1× `<filter id="glowBlur">` applied to decorative glow paths/circles
- 3× rounded `<clipPath>` definitions for portrait product image crops
- 3× `<image>` elements for the carousel hero visuals, each clipped to a rounded rectangle
- 6× rounded `<rect>` elements for card shadow plates and crisp card borders
- 3× translucent reflected `<image>` elements, vertically flipped and faded, to imply a glossy stage
- 2× curved `<path>` elements for the implied orbital track / depth guide
- 5× small `<circle>` elements for carousel progress indicators and luminous particles
- Multiple `<text>` elements with explicit `width` for slide title, product label, metadata, and navigation hints

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="cyanAtmosphere" cx="42%" cy="38%" r="58%">
      <stop offset="0%" stop-color="#00D5FF" stop-opacity="0.32"/>
      <stop offset="45%" stop-color="#224BFF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#080A13" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="coralAtmosphere" cx="76%" cy="42%" r="55%">
      <stop offset="0%" stop-color="#FF7A59" stop-opacity="0.26"/>
      <stop offset="48%" stop-color="#8A2EFF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#080A13" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="stageFade" x1="0" y1="420" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="45%" stop-color="#1D2335" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#03040A" stop-opacity="0.86"/>
    </linearGradient>
    <linearGradient id="cardRim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.75"/>
      <stop offset="40%" stop-color="#9EEBFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-25%" width="160%" height="160%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glowBlur" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <clipPath id="clipPosterA">
      <rect x="446" y="90" width="388" height="520" rx="34"/>
    </clipPath>
    <clipPath id="clipPosterB">
      <rect x="112" y="188" width="244" height="330" rx="26"/>
    </clipPath>
    <clipPath id="clipPosterC">
      <rect x="924" y="188" width="244" height="330" rx="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#070914"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cyanAtmosphere)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#coralAtmosphere)"/>
  <rect x="0" y="420" width="1280" height="300" fill="url(#stageFade)"/>

  <path d="M145 462 C330 350, 505 315, 640 315 C775 315, 950 350, 1135 462"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="2" stroke-dasharray="10 16"/>
  <path d="M245 530 C405 610, 875 610, 1035 530"
        fill="none" stroke="#00D5FF" stroke-opacity="0.16" stroke-width="3"/>

  <circle cx="280" cy="155" r="76" fill="#00D5FF" opacity="0.20" filter="url(#glowBlur)"/>
  <circle cx="1010" cy="145" r="92" fill="#FF7A59" opacity="0.16" filter="url(#glowBlur)"/>
  <circle cx="650" cy="622" r="210" fill="#274CFF" opacity="0.10" filter="url(#glowBlur)"/>

  <text x="70" y="72" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#B9C4D8" letter-spacing="2">
    REVOLVING PRODUCT SHOWCASE
  </text>
  <text x="70" y="118" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF">
    Cinematic Morphing Carousel
  </text>
  <text x="70" y="154" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#8F9BB2">
    Duplicate this slide, keep the same object IDs, then swap which card is centered for a seamless Morph transition.
  </text>

  <g id="!!PosterB_Left">
    <rect x="104" y="180" width="260" height="346" rx="31" fill="#000000" opacity="0.36" filter="url(#softShadow)"/>
    <image href="https://images.example.com/carousel/minimal-orange-smartwatch-poster.jpg"
           x="112" y="188" width="244" height="330" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipPosterB)" opacity="0.62"/>
    <rect x="112" y="188" width="244" height="330" rx="26" fill="none" stroke="url(#cardRim)" stroke-width="2" opacity="0.55"/>
    <image href="https://images.example.com/carousel/minimal-orange-smartwatch-poster.jpg"
           x="112" y="-844" width="244" height="330" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipPosterB)" transform="scale(1 -1)" opacity="0.11"/>
    <text x="132" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#DDE5F7" opacity="0.55">
      Watch OS / Day 02
    </text>
  </g>

  <g id="!!PosterC_Right">
    <rect x="916" y="180" width="260" height="346" rx="31" fill="#000000" opacity="0.36" filter="url(#softShadow)"/>
    <image href="https://images.example.com/carousel/yellow-modular-camera-poster.jpg"
           x="924" y="188" width="244" height="330" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipPosterC)" opacity="0.62"/>
    <rect x="924" y="188" width="244" height="330" rx="26" fill="none" stroke="url(#cardRim)" stroke-width="2" opacity="0.55"/>
    <image href="https://images.example.com/carousel/yellow-modular-camera-poster.jpg"
           x="924" y="-844" width="244" height="330" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipPosterC)" transform="scale(1 -1)" opacity="0.11"/>
    <text x="944" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#DDE5F7" opacity="0.55">
      Camera Kit / Day 03
    </text>
  </g>

  <g id="!!PosterA_Center">
    <rect x="430" y="74" width="420" height="552" rx="42" fill="#000000" opacity="0.54" filter="url(#softShadow)"/>
    <rect x="438" y="82" width="404" height="536" rx="39" fill="#101827" stroke="#4FE7FF" stroke-opacity="0.28" stroke-width="1.5"/>
    <image href="https://images.example.com/carousel/neon-blue-headphones-hero-poster.jpg"
           x="446" y="90" width="388" height="520" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipPosterA)"/>
    <rect x="446" y="90" width="388" height="520" rx="34" fill="none" stroke="url(#cardRim)" stroke-width="3"/>
    <path d="M470 548 C545 586, 735 586, 810 548" fill="none" stroke="#00D5FF" stroke-width="4" stroke-opacity="0.55"/>
    <image href="https://images.example.com/carousel/neon-blue-headphones-hero-poster.jpg"
           x="446" y="-1138" width="388" height="520" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#clipPosterA)" transform="scale(1 -1)" opacity="0.13"/>
  </g>

  <rect x="492" y="486" width="296" height="88" rx="24" fill="#030712" opacity="0.62"/>
  <text x="520" y="522" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#8CEEFF" letter-spacing="1.5">
    FEATURED DROP 01
  </text>
  <text x="520" y="554" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">
    Audio Halo
  </text>

  <circle cx="592" cy="662" r="5" fill="#FFFFFF" opacity="0.28"/>
  <circle cx="616" cy="662" r="5" fill="#FFFFFF" opacity="0.28"/>
  <circle cx="640" cy="662" r="7" fill="#00D5FF"/>
  <circle cx="664" cy="662" r="5" fill="#FFFFFF" opacity="0.28"/>
  <circle cx="688" cy="662" r="5" fill="#FFFFFF" opacity="0.28"/>
  <text x="995" y="664" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8F9BB2" text-anchor="end">
    Morph: by object · medium speed
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not try to create the carousel motion inside SVG with `<animate>` or `<animateTransform>`; build separate static SVG slide states and use PowerPoint Morph.
- ❌ Do not use `<use>` / `<symbol>` for repeated cards; duplicate the actual editable shapes so each card can keep a stable morph identity.
- ❌ Do not apply `clip-path` to groups or rectangles for card cropping; use `clipPath` only on the `<image>` elements.
- ❌ Do not place shadows on `<line>` elements or rely on marker arrows; carousel depth should come from blurred shape shadows, scale, opacity, and Z-order.
- ❌ Do not change object IDs between slides. The visual trick depends on stable names such as `!!PosterA_Center`, `!!PosterB_Left`, and `!!PosterC_Right`.

## Composition notes
- Keep the active card at roughly 55–70% of slide height, centered horizontally, and highest in Z-order; side cards should be 35–45% of slide height and partially subordinated with opacity.
- Use a dark neutral background with two or three colored atmospheric glows that echo the product artwork, creating a cinematic stage rather than a flat gallery.
- Reserve the top-left for stable explanatory text; the viewer’s eye should track the moving cards, not chase changing headers.
- For the morph sequence, duplicate the slide and rotate positions: center card moves left, right card moves center, left card exits or moves right, while retaining the same SVG/PPT object IDs across slides.