# SVG Recipe — Frosted Glassmorphism Reveal Panel

## Visual mechanism
A frosted reveal panel is built by placing a pre-blurred, brightened duplicate of the same background image exactly over the original image, then clipping it to a rounded rectangle. A transparent foreground subject breaks the panel boundary, while crisp typography sits on the softened glass surface.

## SVG primitives needed
- 3× `<image>` for the base vivid background, the aligned pre-blurred background duplicate inside the glass panel, and the transparent foreground bird cutout
- 5× `<rect>` for the laptop body/screen, glass shadow plate, frosted wash, glass border, and PowerPoint logo tile
- 2× `<circle>` for the PowerPoint logo disc and inner color split
- 3× `<path>` for the laptop base, curved pink annotation arrow, and decorative glass highlight streak
- 1× `<ellipse>` for a soft subject shadow behind the bird
- 5× `<text>` for panel headline, paragraph copy, logo letter, and large “GLASS EFFECT” callout
- 3× `<linearGradient>` for screen depth, frosted panel wash, and pink headline/callout styling
- 2× `<filter>` with blur/shadow for panel depth, laptop depth, subject shadow, and glowing text
- 2× `<clipPath>` with rounded rectangles applied only to `<image>` elements for screen and glass crops

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="screenBezel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#11131f"/>
      <stop offset="55%" stop-color="#05060b"/>
      <stop offset="100%" stop-color="#25293a"/>
    </linearGradient>

    <linearGradient id="glassWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#ff78bb" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#5fb7ff" stop-opacity="0.25"/>
    </linearGradient>

    <linearGradient id="pinkGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff1fb"/>
      <stop offset="45%" stop-color="#ff79cf"/>
      <stop offset="100%" stop-color="#ff3fae"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pinkTextGlow" x="-15%" y="-15%" width="130%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="screenClip">
      <rect x="230" y="78" width="820" height="462" rx="8" ry="8"/>
    </clipPath>

    <clipPath id="glassClip">
      <rect x="352" y="150" width="660" height="330" rx="48" ry="48"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#080910"/>
  <rect x="0" y="0" width="1280" height="720" fill="#131827" opacity="0.45"/>
  <ellipse cx="650" cy="675" rx="600" ry="70" fill="#000000" opacity="0.52" filter="url(#softShadow)"/>

  <rect x="205" y="50" width="870" height="555" rx="28" ry="28" fill="url(#screenBezel)" filter="url(#softShadow)"/>
  <rect x="222" y="67" width="836" height="488" rx="17" ry="17" fill="#02030a"/>
  <image href="https://images.example.com/vibrant-neon-leaf-veins-background-1920x1080.jpg"
         x="230" y="78" width="820" height="462" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#screenClip)"/>
  <rect x="230" y="78" width="820" height="462" fill="#000000" opacity="0.18"/>

  <path d="M170 600 C250 586 365 586 455 594 L825 594 C930 586 1042 586 1110 600 L1148 640 C1010 656 797 661 640 660 C475 660 278 655 132 640 Z"
        fill="#24283a" filter="url(#softShadow)"/>
  <path d="M260 584 L1020 584 L1084 617 C900 629 396 629 196 617 Z" fill="#111423"/>
  <rect x="500" y="594" width="280" height="14" rx="7" fill="#35394c" opacity="0.75"/>

  <rect x="352" y="150" width="660" height="330" rx="48" ry="48" fill="#000000" opacity="0.22" filter="url(#softShadow)"/>
  <image href="https://images.example.com/vibrant-neon-leaf-veins-background-1920x1080-preblurred.jpg"
         x="230" y="78" width="820" height="462" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#glassClip)"/>
  <rect x="352" y="150" width="660" height="330" rx="48" ry="48" fill="url(#glassWash)"/>
  <path d="M394 166 C515 144 696 154 858 164 C742 184 536 194 394 166 Z"
        fill="#ffffff" opacity="0.17"/>
  <rect x="353.5" y="151.5" width="657" height="327" rx="46" ry="46"
        fill="none" stroke="#ffffff" stroke-opacity="0.48" stroke-width="2"/>
  <rect x="356" y="154" width="653" height="323" rx="44" ry="44"
        fill="none" stroke="#9fe2ff" stroke-opacity="0.16" stroke-width="1"/>

  <ellipse cx="450" cy="398" rx="150" ry="36" fill="#000000" opacity="0.25" filter="url(#softShadow)"/>
  <image href="https://images.example.com/transparent-png-kingfisher-bird-wings-open.png"
         x="260" y="106" width="420" height="350" preserveAspectRatio="xMidYMid meet"/>

  <text x="670" y="242" width="300" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" letter-spacing="5">
    <tspan x="670" dy="0">The Masterclass of</tspan>
    <tspan x="670" dy="24">Evolutionary Precision</tspan>
  </text>

  <text x="670" y="322" width="315" fill="#ffffff" opacity="0.92"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11.5" font-weight="500">
    <tspan x="670" dy="0">In the natural world, survival is the ultimate designer. The</tspan>
    <tspan x="670" dy="15">Kingfisher is a living testament to this, having evolved into a</tspan>
    <tspan x="670" dy="15">biological marvel of aerodynamics and intent. Its specialized</tspan>
    <tspan x="670" dy="15">feathers minimize turbulence, while its unique ocular structure</tspan>
    <tspan x="670" dy="15">allows it to adjust for light refraction as it transitions from air</tspan>
    <tspan x="670" dy="15">to water in a split second. The glass panel preserves the energy</tspan>
    <tspan x="670" dy="15">of the image while giving the story a calm, readable stage.</tspan>
  </text>

  <circle cx="1160" cy="151" r="91" fill="#ff835f"/>
  <path d="M1069 151 A91 91 0 0 0 1160 242 L1160 151 Z" fill="#d84b2d" opacity="0.8"/>
  <rect x="1060" y="102" width="103" height="100" rx="8" fill="#d93c16" filter="url(#softShadow)"/>
  <rect x="1052" y="102" width="96" height="96" rx="8" fill="#e34b20"/>
  <text x="1082" y="180" width="60" fill="#ffffff" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="700">P</text>

  <path d="M1198 257 C1242 313 1248 382 1199 434 C1166 469 1123 480 1077 476
           L1088 515 L1026 463 L1086 414 L1088 452 C1131 452 1165 437 1185 410
           C1217 367 1214 310 1187 262 Z"
        fill="#ff7be4" filter="url(#softShadow)"/>

  <text x="845" y="596" width="380" fill="url(#pinkGlow)" font-family="Georgia, 'Times New Roman', serif"
        font-size="75" font-weight="700" letter-spacing="2" filter="url(#pinkTextGlow)">GLASS</text>
  <text x="825" y="678" width="410" fill="url(#pinkGlow)" font-family="Georgia, 'Times New Roman', serif"
        font-size="75" font-weight="700" letter-spacing="1" filter="url(#pinkTextGlow)">EFFECT</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on `filter="url(#blur)"` applied to an `<image>` for the frosted crop; use a pre-blurred duplicate image clipped to the panel area for reliable PowerPoint translation.
- ❌ Do not use SVG `<mask>` for rounded glass corners; use `<clipPath>` applied only to the blurred `<image>`, then place editable rounded `<rect>` overlays above it.
- ❌ Do not clip the frosted wash `<rect>` itself; clip only the image layer, and make all overlay rectangles the exact same rounded size.
- ❌ Do not use `marker-end` for the curved annotation arrow; draw the arrow as a filled `<path>` so the arrowhead survives translation.
- ❌ Do not let text auto-size; every `<text>` element needs an explicit `width` so PowerPoint preserves the intended typography.

## Composition notes
- Keep the glass panel large, centered, and calm: roughly 55–70% of slide width and 40–50% of slide height.
- The background should remain vivid and high contrast, while the glass panel should be brighter, blurrier, and less saturated to make text readable.
- Place the cutout subject so it crosses the glass edge; this boundary break is what sells the dimensional reveal.
- Use small white typography inside the panel and reserve saturated accent color, glow, or large display text for the outside callout area.