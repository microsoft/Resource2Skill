# SVG Recipe — Glassmorphism Reveal Panel

## Visual mechanism
A sharp full-bleed photo is overlaid with a rounded “glass” panel that contains a clipped duplicate of the same photo in a pre-blurred version, creating a frosted-window illusion. Semi-transparent fills, luminous borders, soft shadow, and white typography make the panel feel like a floating reveal surface that can be animated with Morph by moving the panel between slides.

## SVG primitives needed
- 1× `<image>` for the full-slide sharp background photo
- 1× `<image>` for the pre-blurred duplicate photo clipped inside the glass panel
- 1× `<clipPath>` with rounded `<rect>` for the blurred image crop inside the panel
- 2× `<rect>` for global dark/blue overlays that improve contrast
- 1× `<rect>` for the glass panel translucent wash
- 1× `<rect>` for the luminous glass border
- 1× `<filter id="panelShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for floating depth
- 1× `<linearGradient>` for the panel’s milky highlight fill
- 1× `<linearGradient>` for the glass rim stroke
- 2× `<circle>` for soft decorative light blooms
- 1× `<path>` for a subtle diagonal specular highlight across the panel
- 4× `<text>` elements for label, title, body copy, and small metadata
- 1× `<line>` plus 1× `<path>` triangle for a simple motion cue without SVG markers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sceneTint" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#08111F" stop-opacity="0.10"/>
      <stop offset="0.55" stop-color="#102A48" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#000814" stop-opacity="0.54"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="430" y1="210" x2="900" y2="510" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="0.45" stop-color="#DDEBFF" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="glassStroke" x1="410" y1="194" x2="930" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="0.36" stop-color="#BFE6FF" stop-opacity="0.46"/>
      <stop offset="0.72" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.72"/>
    </linearGradient>

    <radialGradient id="bloomA" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#7DD3FC" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#7DD3FC" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="bloomB" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#F0ABFC" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#F0ABFC" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="20" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="glassClip">
      <rect x="420" y="218" width="500" height="284" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/hero-night-city-rain-glass-sharp.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#sceneTint)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#020617" opacity="0.18"/>

  <circle cx="1040" cy="150" r="180" fill="url(#bloomA)" filter="url(#softGlow)"/>
  <circle cx="160" cy="600" r="210" fill="url(#bloomB)" filter="url(#softGlow)"/>

  <line x1="266" y1="360" x2="370" y2="360" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="2" stroke-dasharray="8 10"/>
  <path d="M372 360 L354 350 L354 370 Z" fill="#FFFFFF" opacity="0.38"/>

  <rect x="420" y="218" width="500" height="284" rx="34" ry="34"
        fill="#000000" opacity="0.20" filter="url(#panelShadow)"/>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/hero-night-city-rain-glass-preblurred-50px.jpg"
         clip-path="url(#glassClip)"/>

  <rect x="420" y="218" width="500" height="284" rx="34" ry="34"
        fill="url(#glassFill)" opacity="1"/>

  <path d="M458 240 C560 224 708 230 884 270 L884 310 C698 270 548 264 458 284 Z"
        fill="#FFFFFF" opacity="0.12"/>

  <rect x="420" y="218" width="500" height="284" rx="34" ry="34"
        fill="none" stroke="url(#glassStroke)" stroke-width="2.4"/>

  <rect x="439" y="237" width="462" height="246" rx="24" ry="24"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1"/>

  <text x="466" y="282" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.8"
        fill="#D9F3FF" opacity="0.92">LIVE REVEAL PANEL</text>

  <text x="466" y="344" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="750"
        fill="#FFFFFF">Glassmorphic</text>

  <text x="468" y="389" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#EAF6FF" opacity="0.88">
    <tspan x="468" dy="0">Move the panel with Morph to reveal</tspan>
    <tspan x="468" dy="28">a softened version of the scene below.</tspan>
  </text>

  <text x="468" y="461" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="1.4"
        fill="#FFFFFF" opacity="0.58">DUPLICATE SLIDE → SHIFT PANEL → MORPH</text>
</svg>
```

## Avoid in this skill
- ❌ `backdrop-filter: blur(...)`; PowerPoint will not preserve CSS backdrop blur as editable shapes.
- ❌ Applying `filter="url(#blur)"` directly to the `<image>` and expecting reliable native blur; use a pre-blurred duplicate image asset clipped to the panel.
- ❌ `clip-path` on the glass `<rect>` itself; only clip the blurred `<image>`, then place translucent rounded rectangles above it.
- ❌ `<mask>` for the frosted area; masks are not safe for this pipeline.
- ❌ `marker-end` for motion arrows; draw arrowheads manually with a small `<path>` triangle.

## Composition notes
- Keep the panel large enough for text but not full-width: about 38–45% of slide width and 35–45% of slide height works well.
- Use a busy, high-contrast photo background; the glass effect is most visible when the clipped blurred crop sits over recognizable detail.
- Place the panel slightly off-center for a keynote feel, leaving negative space and visible background context around it.
- For animation, create two slides with the same background and panel construction, then change the panel’s x/y position and use PowerPoint Morph.