# SVG Recipe — Glassmorphic Concentric Pill Overlay

## Visual mechanism
A muted full-bleed photo is covered by a warm vertical gradient veil, then a centered stack of translucent rounded pills creates a glassy “touch target” CTA. Thin semi-transparent white rings radiate around a frosted inner button, making the closing action feel premium, tactile, and interactive.

## SVG primitives needed
- 1× `<image>` for the full-bleed atmospheric background photo.
- 1× `<rect>` for the full-slide dark-to-warm gradient overlay.
- 2× large blurred `<circle>` / `<path>` accents for soft ambient glow behind the CTA.
- 1× `<rect>` for the top hanging tab bleeding off the slide edge.
- 3× concentric rounded `<rect>` pill shapes for the outer ring, middle ring, and inner glass button.
- 1× subtle highlight `<path>` across the inner button to fake glossy glass reflection.
- 1× small `<circle>` icon container plus simple `<path>` arrow for the CTA glyph.
- 5× `<text>` elements for eyebrow, headline, URL, tab label, and microcopy; every text element includes `width`.
- 1× `<linearGradient>` for the background veil.
- 2× `<radialGradient>` definitions for warm/cool atmospheric light blooms.
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for floating pill depth.
- 1× `<filter id="haloBlur">` using `feGaussianBlur` for large diffused glow shapes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoVeil" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2E2E2E" stop-opacity="0.74"/>
      <stop offset="0.48" stop-color="#3D3230" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#CBAF8E" stop-opacity="0.46"/>
    </linearGradient>

    <linearGradient id="innerGlass" x1="420" y1="500" x2="860" y2="604" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="0.45" stop-color="#FFFFFF" stop-opacity="0.20"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.30"/>
    </linearGradient>

    <linearGradient id="tabGlass" x1="492" y1="-48" x2="788" y2="38" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.12"/>
    </linearGradient>

    <radialGradient id="warmBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFD4A5" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#FFD4A5" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="coolBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#9BC7FF" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#9BC7FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-40%" width="140%" height="200%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="haloBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1920&amp;q=85"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#photoVeil)"/>

  <circle cx="268" cy="610" r="230" fill="url(#warmBloom)" filter="url(#haloBlur)"/>
  <path d="M930,105 C1062,40 1190,84 1238,204 C1278,304 1210,415 1086,422 C952,430 842,354 828,242 C820,178 862,138 930,105 Z"
        fill="url(#coolBloom)" filter="url(#haloBlur)"/>

  <rect x="492" y="-48" width="296" height="92" rx="46"
        fill="url(#tabGlass)" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.4"/>
  <text x="640" y="20" width="240" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        letter-spacing="3" fill="#FFFFFF" fill-opacity="0.88">ACME STUDIO</text>

  <text x="640" y="178" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="5" fill="#FFFFFF" fill-opacity="0.76">LIMITED LAUNCH OFFER</text>

  <text x="640" y="305" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="900"
        letter-spacing="2" fill="#FFFFFF">ORDER NOW</text>

  <text x="640" y="364" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="500"
        fill="#FFFFFF" fill-opacity="0.78">Your next step is one click away</text>

  <rect x="348" y="462" width="584" height="128" rx="64"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.4"/>

  <rect x="378" y="482" width="524" height="88" rx="44"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.50" stroke-width="2.4"/>

  <rect x="420" y="500" width="440" height="54" rx="27"
        fill="url(#innerGlass)" stroke="#FFFFFF" stroke-opacity="0.26" stroke-width="1"
        filter="url(#softShadow)"/>

  <path d="M445,511 C520,497 615,504 704,515 C765,523 814,519 843,507
           L843,520 C795,535 729,534 653,523 C571,511 500,509 445,523 Z"
        fill="#FFFFFF" fill-opacity="0.13"/>

  <circle cx="458" cy="527" r="15" fill="#FFFFFF" fill-opacity="0.24"
          stroke="#FFFFFF" stroke-opacity="0.44" stroke-width="1"/>
  <path d="M454,519 L464,527 L454,535 Z" fill="#FFFFFF" fill-opacity="0.92"/>

  <text x="640" y="534" width="320" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700"
        letter-spacing="0.4" fill="#FFFFFF" text-decoration="underline">https://yourwebsite.com</text>

  <text x="640" y="650" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600"
        letter-spacing="2.2" fill="#FFFFFF" fill-opacity="0.62">SECURE CHECKOUT · INSTANT ACCESS · 24/7 SUPPORT</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; it will not translate to editable PowerPoint glass. Simulate glass with translucent fills, strokes, gradients, and shadows.
- ❌ Do not use `<mask>` to fade the background photo; use a normal full-slide gradient `<rect>` overlay instead.
- ❌ Do not clip non-image elements for pill shapes; use native rounded `<rect rx="...">` geometry.
- ❌ Do not put glow or shadow filters on `<line>` elements; use filtered `<rect>`, `<circle>`, or `<path>` elements only.
- ❌ Do not make the CTA from a raster button image; keep the concentric pills as editable SVG rectangles and text.

## Composition notes
- Keep the headline centered in the upper-middle third, leaving enough breathing room above the CTA pill so the slide feels like a closing keynote screen rather than a form.
- The concentric pill stack should occupy roughly 45% of slide width; too small loses the “touch target” effect, too large feels like a banner.
- Use a darkened, low-detail photo so the white glass rings remain legible; the gradient veil is part of the technique, not an optional decoration.
- Repeat white at multiple opacities—solid headline, translucent rings, faint tab, and soft microcopy—to create a refined glassmorphic rhythm.