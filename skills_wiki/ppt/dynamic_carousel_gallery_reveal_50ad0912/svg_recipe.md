# SVG Recipe — Dynamic Carousel Gallery Reveal

## Visual mechanism
A premium horizontal carousel freezes on one enlarged, high-contrast center card while neighboring cards shrink, dim, and recede to imply motion and depth. Duplicate the slide and move the same card IDs to new positions/sizes so PowerPoint Morph creates the “gallery reveal” transition between focal entities.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 2× `<path>` for soft ambient glow shapes behind the carousel
- 5× `<image>` for portrait/product/gallery visuals, each clipped into a rounded card crop
- 5× `<clipPath>` using rounded `<rect>` geometry for editable rounded image crops
- 5× `<rect>` for card backing plates / frames with rounded corners
- 4× `<rect>` for semi-transparent inactive-card dim overlays
- 1× `<rect>` for the active cyan label tag overlapping the hero card
- 3× `<text>` blocks for title, active name, and active role
- 4× small `<text>` captions for inactive carousel previews
- 5× `<circle>` pagination dots
- 2× `<path>` chevrons for carousel navigation hints
- 1× `<linearGradient>` for the active card frame
- 1× `<radialGradient>` for ambient background glow
- 2× `<filter>` definitions: one soft shadow for cards, one blur glow for background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="activeFrameGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35D7FF"/>
      <stop offset="48%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#00A6FF"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.42"/>
      <stop offset="65%" stop-color="#176BFF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#0E1016" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="clip-card-01"><rect x="106" y="292" width="132" height="176" rx="28"/></clipPath>
    <clipPath id="clip-card-02"><rect x="276" y="250" width="164" height="218" rx="32"/></clipPath>
    <clipPath id="clip-card-03"><rect x="488" y="126" width="304" height="406" rx="46"/></clipPath>
    <clipPath id="clip-card-04"><rect x="840" y="250" width="164" height="218" rx="32"/></clipPath>
    <clipPath id="clip-card-05"><rect x="1042" y="292" width="132" height="176" rx="28"/></clipPath>
  </defs>

  <rect id="bg-charcoal" x="0" y="0" width="1280" height="720" fill="#25272D"/>

  <path id="glow-left" d="M180,210 C250,120 360,128 420,205 C475,276 418,390 305,395 C186,400 112,305 180,210 Z"
        fill="url(#ambientGlow)" filter="url(#softGlow)" opacity="0.78"/>
  <path id="glow-right" d="M915,160 C1045,84 1185,147 1208,274 C1236,429 1070,504 956,442 C850,384 810,221 915,160 Z"
        fill="url(#ambientGlow)" filter="url(#softGlow)" opacity="0.58"/>

  <text id="eyebrow" x="72" y="74" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="600" fill="#7FE7FF" letter-spacing="2.4">FEATURED LEADERSHIP</text>
  <text id="title" x="72" y="118" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="38"
        font-weight="700" fill="#FFFFFF">Dynamic Carousel Gallery Reveal</text>

  <rect id="card-01-frame" x="106" y="292" width="132" height="176" rx="28" fill="#343842" filter="url(#cardShadow)"/>
  <image id="card-01-image" href="https://images.example.com/portrait-strategist-warm-studio.jpg"
         x="106" y="292" width="132" height="176" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-01)"/>
  <rect id="card-01-dim" x="106" y="292" width="132" height="176" rx="28" fill="#05070A" opacity="0.42"/>
  <text id="card-01-label" x="82" y="506" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="600" fill="#B8C0CC" text-anchor="middle">Strategy</text>

  <rect id="card-02-frame" x="276" y="250" width="164" height="218" rx="32" fill="#3A3F4A" filter="url(#cardShadow)"/>
  <image id="card-02-image" href="https://images.example.com/portrait-designer-blue-background.jpg"
         x="276" y="250" width="164" height="218" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-02)"/>
  <rect id="card-02-dim" x="276" y="250" width="164" height="218" rx="32" fill="#05070A" opacity="0.30"/>
  <text id="card-02-label" x="358" y="506" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="600" fill="#D3DAE5" text-anchor="middle">Design</text>

  <rect id="card-03-active-frame" x="478" y="116" width="324" height="426" rx="52"
        fill="url(#activeFrameGrad)" filter="url(#cardShadow)"/>
  <rect id="card-03-inner-mat" x="488" y="126" width="304" height="406" rx="46" fill="#11151D"/>
  <image id="card-03-image" href="https://images.example.com/executive-portrait-confident-cyan-light.jpg"
         x="488" y="126" width="304" height="406" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-03)"/>

  <rect id="active-tag" x="455" y="494" width="370" height="86" rx="22" fill="#00BFFF" filter="url(#cardShadow)"/>
  <text id="active-name" x="484" y="529" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="28"
        font-weight="800" fill="#03131B">Maya Chen</text>
  <text id="active-role" x="484" y="557" width="315" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="600" fill="#053447" letter-spacing="1.2">CHIEF PRODUCT OFFICER</text>

  <rect id="card-04-frame" x="840" y="250" width="164" height="218" rx="32" fill="#3A3F4A" filter="url(#cardShadow)"/>
  <image id="card-04-image" href="https://images.example.com/portrait-engineer-green-background.jpg"
         x="840" y="250" width="164" height="218" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-04)"/>
  <rect id="card-04-dim" x="840" y="250" width="164" height="218" rx="32" fill="#05070A" opacity="0.30"/>
  <text id="card-04-label" x="922" y="506" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="600" fill="#D3DAE5" text-anchor="middle">Engineering</text>

  <rect id="card-05-frame" x="1042" y="292" width="132" height="176" rx="28" fill="#343842" filter="url(#cardShadow)"/>
  <image id="card-05-image" href="https://images.example.com/portrait-operator-purple-background.jpg"
         x="1042" y="292" width="132" height="176" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-05)"/>
  <rect id="card-05-dim" x="1042" y="292" width="132" height="176" rx="28" fill="#05070A" opacity="0.42"/>
  <text id="card-05-label" x="1108" y="506" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="600" fill="#B8C0CC" text-anchor="middle">Operations</text>

  <path id="nav-left" d="M54,357 L34,377 L54,397" fill="none" stroke="#8B96A8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path id="nav-right" d="M1226,357 L1246,377 L1226,397" fill="none" stroke="#8B96A8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <circle id="dot-01" cx="588" cy="642" r="5" fill="#606978"/>
  <circle id="dot-02" cx="614" cy="642" r="5" fill="#606978"/>
  <circle id="dot-03" cx="640" cy="642" r="7" fill="#00BFFF"/>
  <circle id="dot-04" cx="666" cy="642" r="5" fill="#606978"/>
  <circle id="dot-05" cx="692" cy="642" r="5" fill="#606978"/>

  <text id="morph-note" x="424" y="686" width="432" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        font-weight="500" fill="#8E98A8" text-anchor="middle">Duplicate slide → move the same card IDs → apply PowerPoint Morph.</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` / `<animateTransform>` for the carousel motion; create separate Morph keyframes as separate slides instead.
- ❌ `<use href="#card">` clones for repeated cards; duplicated instances may fail translation and prevent editable output.
- ❌ Applying `clip-path` to card frames, overlays, or groups; only apply clipping to the `<image>` elements.
- ❌ `marker-end` arrows on paths; use explicit chevron `<path>` shapes or `<line>` arrows with direct marker settings if needed.
- ❌ Skew or matrix transforms for perspective; create depth through actual x/y/width/height changes and opacity instead.

## Composition notes
- Keep the active card centered and 2–3× larger than side cards; the tag should overlap the lower edge so the focal identity feels attached to the image.
- Side cards should remain visible but dimmed, giving preview/context without competing with the hero portrait.
- For Morph, duplicate the slide and preserve the same element IDs/order; move the next card into the center geometry and resize the previous active card into a side slot.
- Use a dark neutral background with one vivid accent color, then repeat that accent in the active frame, tag, and pagination dot for a clear visual rhythm.