# SVG Recipe — Cinematic Split Cover

## Visual mechanism
A wide central hero image is “letterboxed” between deep cinematic top and bottom bars, creating a film-frame effect for dramatic covers or section dividers. Minimal editorial typography sits inside the dark panels, while subtle gradients, edge glows, and frame markings make the slide feel like a premium keynote title card.

## SVG primitives needed
- 2× `<rect>` for the top and bottom black letterbox panels
- 1× `<image>` clipped to a wide horizontal hero band
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 4× `<rect>` for gradient overlays and image vignettes
- 3× `<line>` for thin cinematic divider rules and accent marks
- 2× `<path>` for atmospheric light-leak shapes over the hero image
- 5× `<text>` for kicker, headline, subtitle, frame label, and small metadata
- 3× `<linearGradient>` for image darkening, metallic divider highlights, and warm light leak
- 1× `<radialGradient>` for a soft center glow
- 1× `<filter id="softShadow">` applied to the hero image container
- 1× `<filter id="titleGlow">` applied to the main title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroClip">
      <rect x="44" y="126" width="1192" height="468" rx="18" ry="18"/>
    </clipPath>

    <linearGradient id="barGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#050608"/>
      <stop offset="45%" stop-color="#101217"/>
      <stop offset="100%" stop-color="#040507"/>
    </linearGradient>

    <linearGradient id="imageVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.72"/>
      <stop offset="22%" stop-color="#000000" stop-opacity="0.16"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="goldRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6d5934" stop-opacity="0"/>
      <stop offset="18%" stop-color="#d7b46a" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#fff0b8" stop-opacity="0.95"/>
      <stop offset="82%" stop-color="#d7b46a" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#6d5934" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="lightLeak" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffd27a" stop-opacity="0.55"/>
      <stop offset="44%" stop-color="#ff6a3d" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#1b0b32" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="50%" r="62%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="58%" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-10%" y="-15%" width="120%" height="130%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-8%" y="-30%" width="116%" height="160%">
      <feGaussianBlur stdDeviation="2.5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#050608"/>
  <rect x="0" y="0" width="1280" height="126" fill="url(#barGrad)"/>
  <rect x="0" y="594" width="1280" height="126" fill="url(#barGrad)"/>

  <rect x="44" y="126" width="1192" height="468" rx="18" fill="#11151c" filter="url(#softShadow)"/>

  <image
    x="44" y="126" width="1192" height="468"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroClip)"
    href="https://images.example.com/cinematic-night-city-coastal-road-hero.jpg"/>

  <rect x="44" y="126" width="1192" height="468" rx="18" fill="url(#imageVignette)" opacity="0.95"/>
  <rect x="44" y="126" width="1192" height="468" rx="18" fill="url(#centerGlow)" opacity="0.85"/>

  <path d="M895 126 C990 170 1044 258 1236 246 L1236 126 Z" fill="url(#lightLeak)" opacity="0.52"/>
  <path d="M44 512 C204 474 310 538 430 594 L44 594 Z" fill="#091b2a" opacity="0.48"/>

  <rect x="44" y="126" width="1192" height="54" rx="18" fill="#000000" opacity="0.26"/>
  <rect x="44" y="540" width="1192" height="54" rx="18" fill="#000000" opacity="0.34"/>

  <line x1="78" y1="126" x2="1202" y2="126" stroke="url(#goldRule)" stroke-width="1.2"/>
  <line x1="78" y1="594" x2="1202" y2="594" stroke="url(#goldRule)" stroke-width="1.2"/>
  <line x1="92" y1="66" x2="188" y2="66" stroke="#d7b46a" stroke-width="2.4"/>

  <text x="92" y="50" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="3.2" fill="#d7b46a">
    MARKET SIGNALS / 2026
  </text>

  <text x="92" y="672" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="700" letter-spacing="-1.6" fill="#f4f1e9" filter="url(#titleGlow)">
    CINEMATIC SPLIT COVER
  </text>

  <text x="92" y="704" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="400" fill="#aeb4bf">
    A dramatic letterbox shell for executive section dividers, launches, and high-stakes narrative openings.
  </text>

  <text x="1016" y="54" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="600" letter-spacing="2.4" fill="#777f8c" text-anchor="end">
    FRAME 01
  </text>

  <text x="1016" y="704" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="500" letter-spacing="1.8" fill="#6f7682" text-anchor="end">
    16:6 HERO IMAGE
  </text>

  <rect x="1112" y="38" width="74" height="28" rx="14" fill="#ffffff" opacity="0.08"/>
  <text x="1149" y="57" width="74" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#d7b46a" text-anchor="middle">
    COVER
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the vignette; use translucent gradient `<rect>` overlays instead.
- ❌ Do not clip text or decorative shapes; clipping is reliable only on `<image>` for this workflow.
- ❌ Do not use `<pattern>` for film grain; it will not translate reliably. Suggest texture through subtle gradients, glows, and small editable marks.
- ❌ Do not place dense body text over the hero image; the cinematic split cover works best as a low-density title or divider.
- ❌ Do not use `marker-end` on paths for arrows or timeline cues; this cover should rely on rules, labels, and framing.

## Composition notes
- Keep the hero image wide and shallow, roughly y=126 to y=594, so the top and bottom dark panels read as intentional letterbox bars.
- Place the kicker in the upper bar and the headline/subtitle in the lower bar; avoid competing with the image’s visual center.
- Use one warm accent color, such as muted gold, for divider rules and metadata to create a premium cinematic rhythm.
- Preserve generous negative space in both bars; the image should provide atmosphere, while typography provides authority.