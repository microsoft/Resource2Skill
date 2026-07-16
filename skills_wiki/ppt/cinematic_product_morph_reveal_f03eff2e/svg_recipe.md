# SVG Recipe — Cinematic Product Morph Reveal

## Visual mechanism
A persistent hero product sits on the compositional seam while large background panels repartition the slide from a full cinematic stage into an editorial split-screen. The Morph-ready illusion comes from keeping the product and key text as stable named objects while changing panel widths, product scale/position, and inverted typography between slides.

## SVG primitives needed
- 2× `<rect>` for the split-screen background panels: dark cinematic product zone and light specs zone.
- 3× `<rect>` for translucent spec cards and small editorial label chips.
- 1× `<image>` for the transparent-background hero product render, positioned to overlap the panel boundary.
- 5× `<path>` for premium lighting sweeps, road shadow, accent chevron, and optional editable product-highlight glints.
- 3× `<circle>` / `<ellipse>` for radial glow accents and ground reflections behind the product.
- 1× `<linearGradient>` for the dark studio panel.
- 1× `<radialGradient>` for the product halo / studio light.
- 1× `<filter id="softShadow">` for card and product-area depth.
- 1× `<filter id="glow">` for cinematic accent light.
- Multiple `<text>` elements with explicit `width` attributes for tracked title, compact specs, and editorial annotations.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="studioDark" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#111113"/>
      <stop offset="58%" stop-color="#1E1E1E"/>
      <stop offset="100%" stop-color="#09090A"/>
    </linearGradient>

    <linearGradient id="paperLight" x1="640" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#ECECEC"/>
    </linearGradient>

    <radialGradient id="halo" cx="50%" cy="48%" r="62%">
      <stop offset="0%" stop-color="#FFD74D" stop-opacity="0.32"/>
      <stop offset="45%" stop-color="#FFD74D" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFD74D" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="metalLine" x1="260" y1="0" x2="990" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <!-- Morph keyframe: Deep-dive split state. On the previous slide, make this dark panel full width. -->
  <rect id="morphBgDark" x="0" y="0" width="640" height="720" fill="url(#studioDark)"/>
  <rect id="morphBgLight" x="640" y="0" width="640" height="720" fill="url(#paperLight)"/>

  <!-- Cinematic lighting behind the persistent product -->
  <ellipse cx="525" cy="375" rx="430" ry="245" fill="url(#halo)" filter="url(#glow)"/>
  <path d="M72 484 C214 430, 415 414, 623 428 C790 439, 929 478, 1062 560"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.09" stroke-width="2"/>
  <path d="M165 512 C362 475, 653 472, 912 525 C955 534, 991 546, 1030 560"
        fill="none" stroke="#D8B437" stroke-opacity="0.35" stroke-width="3"/>

  <!-- Boundary accent: shows the morphing partition line -->
  <rect x="636" y="0" width="8" height="720" fill="#DDBA2A"/>
  <path d="M644 256 L682 286 L644 316 Z" fill="#DDBA2A"/>

  <!-- Hero product: use a transparent PNG/WebP render. Keep the same id and asset across morph slides. -->
  <ellipse id="morphProductShadow" cx="548" cy="563" rx="350" ry="34" fill="#000000" opacity="0.42" filter="url(#softShadow)"/>
  <image id="morphProduct"
         href="https://images.example.com/products/transparent-silver-sports-car-side-profile.png"
         x="172" y="278" width="740" height="278"
         preserveAspectRatio="xMidYMid meet"/>

  <!-- Editable fallback glints that can sit above the product render -->
  <path d="M267 389 C391 344, 561 338, 731 377"
        fill="none" stroke="url(#metalLine)" stroke-width="5" stroke-linecap="round" opacity="0.62"/>
  <path d="M291 444 C438 468, 616 468, 796 438"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2" stroke-linecap="round"/>

  <!-- Left-side cinematic title block -->
  <text x="64" y="82" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#DDBA2A" letter-spacing="4">LAUNCH SEQUENCE 02</text>
  <text id="morphTitle" x="60" y="145" width="560" font-family="Segoe UI, Microsoft YaHei"
        font-size="45" font-weight="700" fill="#FFFFFF" letter-spacing="5">CARRERA S</text>
  <text x="64" y="185" width="445" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#B8B8B8">A persistent hero object crosses the moving seam while the environment transforms around it.</text>

  <!-- Right-side editorial spec system -->
  <text x="720" y="108" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#777777" letter-spacing="3">PERFORMANCE PROFILE</text>
  <text x="718" y="164" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="42"
        font-weight="700" fill="#161616">Engineered for the reveal moment.</text>

  <rect x="718" y="242" width="190" height="118" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="742" y="286" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="38"
        font-weight="700" fill="#151515">379</text>
  <text x="742" y="318" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#777777" letter-spacing="2">HORSEPOWER</text>
  <path d="M878 265 L893 280 L878 295" fill="none" stroke="#DDBA2A" stroke-width="3" stroke-linecap="round"/>

  <rect x="938" y="242" width="190" height="118" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="962" y="286" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="38"
        font-weight="700" fill="#151515">4.0s</text>
  <text x="962" y="318" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#777777" letter-spacing="2">0–60 MPH</text>
  <path d="M1098 265 L1113 280 L1098 295" fill="none" stroke="#DDBA2A" stroke-width="3" stroke-linecap="round"/>

  <rect x="718" y="398" width="410" height="122" rx="24" fill="#171717"/>
  <text x="746" y="439" width="348" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#FFFFFF">Morph construction</text>
  <text x="746" y="472" width="342" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#BEBEBE">Duplicate this slide. On slide one, expand the dark panel to full width, center the title, and scale the product larger.</text>

  <line x1="718" y1="570" x2="1128" y2="570" stroke="#161616" stroke-width="1" stroke-dasharray="5 9"/>
  <text x="718" y="612" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        fill="#777777">Keep IDs/names stable for Morph: product, dark panel, light panel, title, and spec group.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the motion should be created by PowerPoint Morph between two editable slide states.
- ❌ Do not rely on `<mask>` for product reveal wipes; use moving rect panels behind a persistent transparent product image instead.
- ❌ Do not put filters on `<line>` elements for the split seam or dashed guides; use filters only on rect/path/text/ellipse shapes.
- ❌ Do not use `marker-end` on paths for chevrons or callouts; draw arrowheads as small editable `<path>` shapes.
- ❌ Do not crop the product image with `clip-path` unless it is intentionally a photo-card crop; the hero product should remain transparent and free-floating.

## Composition notes
- Place the product so it overlaps the vertical panel boundary by 20–35% of its width; this makes the panel morph feel like it moves behind the object.
- Reserve the dark side for emotional brand copy and the light side for compact specs, so text color can invert cleanly between keyframes.
- Use one warm accent color only: seam line, chevrons, product glow, and small labels should share the same gold/yellow hue.
- For the opening slide, use the same SVG objects but expand the dark panel to `width="1280"`, reduce or hide the light/spec area, center the title, and enlarge the product to create the cinematic hook before Morphing into this split view.