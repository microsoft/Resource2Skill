# SVG Recipe — Title and Full Image

## Visual mechanism
A single 16:9 image or diagram occupies the full slide as the primary visual field, while a compact top-left title block sits on a translucent “glass” panel for readability. Subtle gradient veils and technical accent lines make the slide feel premium without competing with the image.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero diagram or architecture visual
- 2× `<rect>` for dark readability veils over the image
- 1× `<rect>` for the translucent title card
- 1× `<rect>` for the small category / section pill
- 1× `<rect>` for a thin accent rule under the title card
- 5× `<path>` for decorative technical contour lines and corner accents
- 2× `<circle>` for soft luminous anchor dots
- 4× `<text>` for eyebrow label, headline, subtitle, and image caption
- 2× `<linearGradient>` for image overlays and accent fills
- 1× `<radialGradient>` for soft blue glow
- 1× `<filter id="cardShadow">` for the title card shadow
- 1× `<filter id="softGlow">` for luminous dots and accent paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftVeil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#06111F" stop-opacity="0.92"/>
      <stop offset="42%" stop-color="#06111F" stop-opacity="0.52"/>
      <stop offset="78%" stop-color="#06111F" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#06111F" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomVeil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#06111F" stop-opacity="0"/>
      <stop offset="100%" stop-color="#06111F" stop-opacity="0.62"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2AF3FF"/>
      <stop offset="55%" stop-color="#5B8CFF"/>
      <stop offset="100%" stop-color="#9B6CFF"/>
    </linearGradient>

    <radialGradient id="blueGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2AF3FF" stop-opacity="0.85"/>
      <stop offset="55%" stop-color="#2AF3FF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#2AF3FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#07111F"/>

  <image
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
    href="https://images.example.com/full-bleed-isometric-cloud-infrastructure-architecture-diagram-16x9.png"
    xlink:href="https://images.example.com/full-bleed-isometric-cloud-infrastructure-architecture-diagram-16x9.png"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#leftVeil)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomVeil)"/>

  <circle cx="1008" cy="142" r="116" fill="url(#blueGlow)" filter="url(#softGlow)" opacity="0.72"/>
  <circle cx="1136" cy="578" r="90" fill="url(#blueGlow)" filter="url(#softGlow)" opacity="0.42"/>

  <path d="M884 96 C948 56, 1048 58, 1112 104 C1180 154, 1210 228, 1192 302"
        fill="none" stroke="#59E6FF" stroke-width="1.4" stroke-opacity="0.42" stroke-dasharray="8 12"/>
  <path d="M916 128 C970 98, 1040 102, 1090 138 C1148 180, 1172 238, 1162 286"
        fill="none" stroke="#8D7CFF" stroke-width="1.1" stroke-opacity="0.36" stroke-dasharray="3 10"/>
  <path d="M1054 542 C1090 514, 1144 512, 1180 542 C1212 570, 1218 620, 1188 650"
        fill="none" stroke="#2AF3FF" stroke-width="1.3" stroke-opacity="0.38" stroke-dasharray="7 10"/>

  <rect x="64" y="64" width="504" height="292" rx="28" fill="#081423" fill-opacity="0.76" filter="url(#cardShadow)"/>
  <rect x="64" y="64" width="504" height="292" rx="28" fill="none" stroke="#FFFFFF" stroke-opacity="0.16"/>

  <rect x="96" y="96" width="164" height="30" rx="15" fill="#102A45" fill-opacity="0.9"/>
  <text x="116" y="117" width="124" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="1.4" fill="#7DEFFF">
    PLATFORM MAP
  </text>

  <text x="96" y="174" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#FFFFFF">
    Cloud Infrastructure Overview
  </text>

  <text x="98" y="236" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="400" fill="#C9D6E8">
    A full-slide architecture visual with a compact title system for executive walkthroughs and technical briefings.
  </text>

  <rect x="96" y="310" width="236" height="4" rx="2" fill="url(#accentGrad)"/>

  <path d="M64 384 L64 440 L120 440" fill="none" stroke="#2AF3FF" stroke-width="2" stroke-opacity="0.68"/>
  <path d="M568 384 L568 440 L512 440" fill="none" stroke="#8D7CFF" stroke-width="2" stroke-opacity="0.55"/>

  <text x="852" y="666" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#D8E6F8" opacity="0.78">
    Source visual: network zones, services, workloads, data paths
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not place the title as plain text directly over a busy image without a veil or glass panel; it will fail readability.
- ❌ Do not crop the image into many small tiles; the technique depends on one dominant full-slide visual.
- ❌ Do not use `<mask>` for the dark overlay; use transparent `<rect>` fills or gradients instead.
- ❌ Do not use `<textPath>` for decorative captions; keep all text as normal editable `<text>` with explicit `width`.

## Composition notes
- Keep the title block in the upper-left 35–45% of the slide width; the rest of the canvas should remain image-led.
- Use a dark left-to-right gradient veil when the image is detailed, especially for architecture diagrams.
- Let the full image touch all four slide edges for a cinematic feel; avoid heavy borders unless the image has a white background.
- Accent colors should echo the image palette: cyan/blue for technical diagrams, warm amber for product photography, or violet for AI/cloud themes.