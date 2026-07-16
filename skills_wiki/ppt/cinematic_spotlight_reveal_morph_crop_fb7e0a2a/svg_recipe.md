# SVG Recipe — Cinematic Spotlight Reveal (Morph & Crop)

## Visual mechanism
A dimmed monochrome full-slide image establishes context, while the identical full-color image is clipped to an elliptical “spotlight” window above it. Across Morph slides, keep the image layers identical and move/resize only the spotlight crop plus nearby annotation text, creating a cinematic roaming-reveal effect.

## SVG primitives needed
- 2× `<image>` for the identical scene: one pre-desaturated/dimmed background, one full-color foreground clipped to the spotlight
- 1× `<clipPath>` with an `<ellipse>` for the editable oval crop window on the foreground image
- 3× `<rect>` for global darkening/vignette overlays and a translucent text card
- 2× `<ellipse>` for the spotlight rim and soft halo/glow
- 2× `<path>` for premium editorial annotation shapes and the small arrowhead pointer
- 2× `<line>` for the thin callout leader from text to spotlight
- 3× `<text>` with explicit `width` attributes for headline, subject label, and body copy
- 1× `<radialGradient>` for the cinematic edge vignette
- 2× `<linearGradient>` for text-card glass fill and cyan spotlight stroke
- 2× `<filter>` using blur/offset/shadow for spotlight glow and text-card depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="spotlightClip">
      <ellipse cx="805" cy="336" rx="190" ry="148"/>
    </clipPath>

    <radialGradient id="edgeVignette" cx="55%" cy="48%" r="78%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <linearGradient id="glassPanel" x1="120" y1="180" x2="520" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#07131F" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#01050A" stop-opacity="0.58"/>
    </linearGradient>

    <linearGradient id="cyanStroke" x1="615" y1="185" x2="995" y2="485" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8BEAFF"/>
      <stop offset="45%" stop-color="#00BFFF"/>
      <stop offset="100%" stop-color="#126CFF"/>
    </linearGradient>

    <filter id="spotlightGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Slide-wide desaturated/dimmed context image. Use a preprocessed grayscale asset. -->
  <image id="BackgroundScene"
         href="https://images.example.com/cinematic-spotlight/team-workshop-desaturated-dimmed-16x9.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Additional cinematic dark wash; keeps typography readable. -->
  <rect x="0" y="0" width="1280" height="720" fill="#03070D" opacity="0.22"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <!-- Full-color copy of the same image, clipped to the moving spotlight. -->
  <image id="SpotlightColorImage"
         href="https://images.example.com/cinematic-spotlight/team-workshop-full-color-16x9.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#spotlightClip)"/>

  <!-- Spotlight glow and editorial rim. Keep these aligned with the clip ellipse. -->
  <ellipse id="SpotlightHalo" cx="805" cy="336" rx="205" ry="162"
           fill="none" stroke="#00BFFF" stroke-opacity="0.42" stroke-width="18"
           filter="url(#spotlightGlow)"/>
  <ellipse id="SpotlightRim" cx="805" cy="336" rx="190" ry="148"
           fill="none" stroke="url(#cyanStroke)" stroke-width="4"/>

  <!-- Thin orbital accent to make the crop feel like a lens, not just a cutout. -->
  <path d="M655 244 C690 196, 785 172, 866 195 C934 214, 983 260, 1002 313"
        fill="none" stroke="#B8F5FF" stroke-opacity="0.62" stroke-width="2"
        stroke-dasharray="8 10"/>

  <!-- Annotation panel floats opposite the spotlight. -->
  <rect id="AnnotationCard" x="118" y="174" width="394" height="310" rx="28"
        fill="url(#glassPanel)" stroke="#FFFFFF" stroke-opacity="0.12"
        filter="url(#cardShadow)"/>

  <path d="M118 204 Q118 174 148 174 L255 174 Q220 190 196 224 Q162 272 118 286 Z"
        fill="#00BFFF" opacity="0.14"/>

  <text x="150" y="232" width="320"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="2.6"
        fill="#00BFFF">SPOTLIGHT 02</text>

  <text x="150" y="282" width="335"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700"
        fill="#FFFFFF">
    <tspan x="150" dy="0">Product Strategy</tspan>
    <tspan x="150" dy="44" fill="#BDEFFF">Lead</tspan>
  </text>

  <text x="150" y="382" width="320"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#EAF7FF" opacity="0.92">
    <tspan x="150" dy="0">The scene stays visible, but the</tspan>
    <tspan x="150" dy="30">color crop pulls attention to one</tspan>
    <tspan x="150" dy="30">person, feature, or decision point.</tspan>
  </text>

  <!-- Callout leader: use line plus a small path arrowhead, not marker-end. -->
  <line x1="512" y1="330" x2="628" y2="330" stroke="#00BFFF" stroke-width="2" stroke-opacity="0.85"/>
  <line x1="628" y1="330" x2="662" y2="318" stroke="#00BFFF" stroke-width="2" stroke-opacity="0.85"/>
  <path d="M672 314 L654 308 L660 326 Z" fill="#00BFFF" opacity="0.9"/>

  <!-- Small cinematic frame bars. -->
  <rect x="0" y="0" width="1280" height="42" fill="#000000" opacity="0.62"/>
  <rect x="0" y="678" width="1280" height="42" fill="#000000" opacity="0.62"/>
</svg>
```

## Avoid in this skill
- ❌ Applying SVG grayscale filters directly to the background image; use a preprocessed desaturated/dimmed image asset instead for reliable PowerPoint translation.
- ❌ Using `<mask>` to reveal the spotlight; use `clipPath` on the foreground `<image>` only.
- ❌ Putting `clip-path` on rectangles, groups, or decorative shapes; the supported crop mechanism here is an image clipped by an ellipse.
- ❌ Using `marker-end` on a `<path>` for the callout arrow; draw the arrowhead as a small standalone `<path>`.
- ❌ Letting text auto-size implicitly; every `<text>` needs an explicit `width` attribute.

## Composition notes
- Build each Morph keyframe with identical layer order: dimmed background image, dark/vignette overlays, clipped color image, spotlight rim, then annotation text.
- Keep the spotlight radius around 20–28% of slide height; too small feels like a cursor, too large loses the reveal effect.
- Place the text card on the opposite side of the spotlight with a short leader line; preserve at least 80–120 px of negative space around both.
- For animation in PowerPoint, duplicate the slide, keep equivalent objects named/structured consistently, then move the clip ellipse, rim, halo, and annotation panel together before applying Morph.