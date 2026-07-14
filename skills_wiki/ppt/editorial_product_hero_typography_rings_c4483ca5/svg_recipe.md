# SVG Recipe — Editorial Product Hero & Typography Rings

## Visual mechanism
A premium editorial cover composition: oversized display typography bleeds across the slide, then a large product cutout floats in front to interrupt the word shape and create depth. A circular typography badge, built from individually rotated letters, adds the crafted “brand seal” detail without relying on unsupported SVG text paths.

## SVG primitives needed
- 1× `<rect>` for the full-slide vibrant/atmospheric background.
- 2× `<linearGradient>` for the moody background and screen-bottom editorial fade.
- 1× huge `<text>` for the screen-spanning headline behind the product.
- 1× blurred `<rect>` with `<filter id="softShadow">` for the floating product/tablet shadow.
- 2× rounded `<rect>` for the tablet body and bezel highlight.
- 1× `<clipPath>` with rounded `<rect>` applied to the tablet screen `<image>`.
- 1× `<image>` for the tablet screen hero visual.
- 2× transparent PNG `<image>` elements for foreground hands/product interaction cutouts.
- Several small `<text>` and `<line>` elements for screen UI details.
- 2× `<circle>` for the circular typography badge structure.
- 36× individually positioned `<text>` elements for the circular type ring.
- 1× centered `<text>` inside the badge for the short seal label.
- 1× `<path>` decorative sweep/accent behind the badge for editorial motion.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#24323A"/>
      <stop offset="55%" stop-color="#277A97"/>
      <stop offset="100%" stop-color="#0E2028"/>
    </linearGradient>
    <linearGradient id="screenFade" x1="0" y1="350" x2="0" y2="650">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="70%" stop-color="#000000" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.82"/>
    </linearGradient>
    <linearGradient id="badgeGrad" x1="980" y1="100" x2="1120" y2="250">
      <stop offset="0%" stop-color="#FFF8EA"/>
      <stop offset="100%" stop-color="#FFD56A"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="26"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="badgeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
    <clipPath id="screenClip">
      <rect x="174" y="158" width="932" height="522" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="54" y="132" width="1190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="142" font-weight="800" fill="#F7F6F2" letter-spacing="-6">
    2025 Inspiration
  </text>
  <line x1="285" y1="140" x2="1100" y2="140" stroke="#F7F6F2" stroke-width="5" opacity="0.92"/>

  <path d="M945,118 C1028,92 1115,108 1160,176 C1086,158 1026,176 972,236 C962,197 952,158 945,118 Z"
        fill="#FF6B4A" opacity="0.55" filter="url(#badgeGlow)"/>

  <rect x="188" y="184" width="910" height="500" rx="28" fill="#071014" opacity="0.75" filter="url(#softShadow)"/>
  <rect x="150" y="138" width="980" height="566" rx="32" fill="#040608"/>
  <rect x="154" y="142" width="972" height="558" rx="28" fill="none" stroke="#F5F7F6" stroke-width="3"/>

  <image x="174" y="158" width="932" height="522" clip-path="url(#screenClip)"
         href="https://images.example.com/editorial-tablet-screen-red-bull-racing-workforce-hero.jpg"/>
  <rect x="174" y="416" width="932" height="264" fill="url(#screenFade)" opacity="0.96"/>

  <text x="222" y="216" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="27" font-weight="800" fill="#22313A">Citrix</text>
  <text x="968" y="211" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9" font-weight="700" fill="#51636B" letter-spacing="2">SOUND</text>
  <line x1="1045" y1="198" x2="1068" y2="198" stroke="#30444F" stroke-width="4"/>
  <line x1="1045" y1="206" x2="1068" y2="206" stroke="#30444F" stroke-width="4"/>
  <line x1="1045" y1="214" x2="1068" y2="214" stroke="#30444F" stroke-width="4"/>

  <text x="226" y="494" width="735" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="300" fill="#F8F8F4" letter-spacing="3">
    HOW DO YOU POWER
  </text>
  <text x="226" y="550" width="830" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="300" fill="#F8F8F4" letter-spacing="3">
    THE NEW MOBILE WORKFORCE?
  </text>
  <text x="502" y="620" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="400" fill="#DCE5E5" opacity="0.82">
    Citrix is helping racing teams reimagine how work moves from track to factory to everywhere in between.
  </text>

  <image x="-4" y="344" width="294" height="386"
         href="https://images.example.com/transparent-left-hand-holding-tablet-cutout.png"/>
  <image x="1012" y="330" width="272" height="400"
         href="https://images.example.com/transparent-right-hand-holding-tablet-cutout.png"/>

  <circle cx="1048" cy="190" r="74" fill="url(#badgeGrad)" stroke="#17242C" stroke-width="3"/>
  <circle cx="1048" cy="190" r="48" fill="#17242C" opacity="0.93"/>
  <text x="1024" y="199" width="54" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#FFF8EA" letter-spacing="1">AI</text>

  <g font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="800"
     fill="#17242C" text-anchor="middle" dominant-baseline="middle">
    <text x="1048" y="90" width="20" transform="rotate(0 1048 190)">P</text>
    <text x="1048" y="90" width="20" transform="rotate(10 1048 190)">O</text>
    <text x="1048" y="90" width="20" transform="rotate(20 1048 190)">W</text>
    <text x="1048" y="90" width="20" transform="rotate(30 1048 190)">E</text>
    <text x="1048" y="90" width="20" transform="rotate(40 1048 190)">R</text>
    <text x="1048" y="90" width="20" transform="rotate(50 1048 190)">•</text>
    <text x="1048" y="90" width="20" transform="rotate(60 1048 190)">M</text>
    <text x="1048" y="90" width="20" transform="rotate(70 1048 190)">O</text>
    <text x="1048" y="90" width="20" transform="rotate(80 1048 190)">B</text>
    <text x="1048" y="90" width="20" transform="rotate(90 1048 190)">I</text>
    <text x="1048" y="90" width="20" transform="rotate(100 1048 190)">L</text>
    <text x="1048" y="90" width="20" transform="rotate(110 1048 190)">E</text>
    <text x="1048" y="90" width="20" transform="rotate(120 1048 190)">•</text>
    <text x="1048" y="90" width="20" transform="rotate(130 1048 190)">W</text>
    <text x="1048" y="90" width="20" transform="rotate(140 1048 190)">O</text>
    <text x="1048" y="90" width="20" transform="rotate(150 1048 190)">R</text>
    <text x="1048" y="90" width="20" transform="rotate(160 1048 190)">K</text>
    <text x="1048" y="90" width="20" transform="rotate(170 1048 190)">F</text>
    <text x="1048" y="90" width="20" transform="rotate(180 1048 190)">O</text>
    <text x="1048" y="90" width="20" transform="rotate(190 1048 190)">R</text>
    <text x="1048" y="90" width="20" transform="rotate(200 1048 190)">C</text>
    <text x="1048" y="90" width="20" transform="rotate(210 1048 190)">E</text>
    <text x="1048" y="90" width="20" transform="rotate(220 1048 190)">•</text>
    <text x="1048" y="90" width="20" transform="rotate(230 1048 190)">2</text>
    <text x="1048" y="90" width="20" transform="rotate(240 1048 190)">0</text>
    <text x="1048" y="90" width="20" transform="rotate(250 1048 190)">2</text>
    <text x="1048" y="90" width="20" transform="rotate(260 1048 190)">5</text>
    <text x="1048" y="90" width="20" transform="rotate(270 1048 190)">•</text>
    <text x="1048" y="90" width="20" transform="rotate(280 1048 190)">A</text>
    <text x="1048" y="90" width="20" transform="rotate(290 1048 190)">I</text>
    <text x="1048" y="90" width="20" transform="rotate(300 1048 190)">•</text>
    <text x="1048" y="90" width="20" transform="rotate(310 1048 190)">P</text>
    <text x="1048" y="90" width="20" transform="rotate(320 1048 190)">O</text>
    <text x="1048" y="90" width="20" transform="rotate(330 1048 190)">W</text>
    <text x="1048" y="90" width="20" transform="rotate(340 1048 190)">E</text>
    <text x="1048" y="90" width="20" transform="rotate(350 1048 190)">R</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<textPath>` for the circular badge; PPT translation drops it. Build the ring from individual rotated `<text>` elements.
- ❌ Do not use `<mask>` to cut the product out of typography; layer the product image above the giant text instead.
- ❌ Do not apply `clip-path` to text or shapes for text-interruption effects; it is only reliable on `<image>`.
- ❌ Do not put shadows on `<line>` elements; use filtered `<rect>`, `<circle>`, or `<path>` shadows.
- ❌ Do not rely on a photo with a non-transparent background for the foreground hands/product cutout unless you intentionally want a rectangular image card.

## Composition notes
- Keep the display headline huge and partially hidden: it should read like a masthead, not a normal title box.
- Place the product/tablet in the central 70–80% of the canvas and let it overlap the headline to create instant foreground depth.
- Use the circular typography badge asymmetrically, usually near a product corner or crossing the headline/product boundary.
- Maintain strong color contrast: moody or vibrant background, off-white display type, and a high-energy accent badge.