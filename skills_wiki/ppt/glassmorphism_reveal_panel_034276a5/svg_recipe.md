# SVG Recipe — Glassmorphism Reveal Panel

## Visual mechanism
A vibrant gradient-and-typography background is duplicated as a pre-blurred full-slide image, then clipped to a rounded rectangle to create a frosted “reveal” pane. A translucent fill, gradient rim stroke, soft shadow, and crisp foreground metrics make the panel feel like floating glass over a high-energy backdrop.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 4× `<circle>` / `<ellipse>` for large blurred color orbs that create a mesh-gradient atmosphere
- 1× large `<text>` for ambient background typography
- 1× clipped `<image>` for the blurred composite background visible only inside the glass panel
- 1× `<clipPath>` with rounded `<rect>` for cropping the blurred image to the panel shape
- 2× `<rect>` for the glass panel body and subtle inner highlight
- 2× `<linearGradient>` for the background and glass rim stroke
- 1× `<radialGradient>` for ambient glow accents
- 2× `<filter>`: one Gaussian blur for color orbs, one offset blur shadow for the floating glass panel
- Multiple `<text>` elements with explicit `width` for headline, metric values, labels, and small UI captions
- 3× `<line>` for fine dividers inside the panel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="720" x2="1280" y2="0">
      <stop offset="0%" stop-color="#070711"/>
      <stop offset="42%" stop-color="#132B9B"/>
      <stop offset="73%" stop-color="#651E96"/>
      <stop offset="100%" stop-color="#110A1E"/>
    </linearGradient>

    <linearGradient id="glassRim" x1="330" y1="190" x2="950" y2="555">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.82"/>
      <stop offset="38%" stop-color="#BFD7FF" stop-opacity="0.42"/>
      <stop offset="72%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="softSpot" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="orbBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="46"/>
    </filter>

    <filter id="panelShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="26"/>
      <feGaussianBlur stdDeviation="28"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="panelClip">
      <rect x="284" y="204" width="712" height="346" rx="38" ry="38"/>
    </clipPath>
  </defs>

  <!-- vibrant base atmosphere -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="132" cy="540" r="245" fill="#245CFF" opacity="0.78" filter="url(#orbBlur)"/>
  <circle cx="1015" cy="112" r="260" fill="#A52BFF" opacity="0.58" filter="url(#orbBlur)"/>
  <ellipse cx="728" cy="644" rx="360" ry="150" fill="#00B8FF" opacity="0.18" filter="url(#orbBlur)"/>
  <circle cx="555" cy="180" r="145" fill="#FF5AC8" opacity="0.20" filter="url(#orbBlur)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#02030B" opacity="0.18"/>

  <!-- clear background title, intentionally oversized and decorative -->
  <text x="640" y="162" width="1180" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif" font-size="108"
        font-style="italic" letter-spacing="-4" fill="#FFFFFF" opacity="0.92">
    Future of design
  </text>
  <text x="640" y="214" width="1000" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15"
        letter-spacing="5" fill="#D8E7FF" opacity="0.52">
    SIGNALS · SYSTEMS · SCALE
  </text>

  <!-- clipped blurred layer: use a pre-rendered blurred version of the full background + title -->
  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/glassmorphism/blurred-gradient-title-future-of-design.png"
         clip-path="url(#panelClip)" opacity="0.92"/>

  <!-- glass pane body -->
  <rect x="284" y="204" width="712" height="346" rx="38" ry="38"
        fill="#FFFFFF" opacity="0.145" filter="url(#panelShadow)"/>
  <rect x="284" y="204" width="712" height="346" rx="38" ry="38"
        fill="none" stroke="url(#glassRim)" stroke-width="2"/>
  <rect x="306" y="226" width="668" height="302" rx="28" ry="28"
        fill="url(#softSpot)" opacity="0.52"/>

  <!-- top label and title inside glass -->
  <text x="340" y="262" width="280"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="700" letter-spacing="3" fill="#DDEBFF" opacity="0.78">
    PRODUCT INTELLIGENCE
  </text>
  <text x="340" y="308" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34"
        font-weight="700" fill="#FFFFFF">
    Adoption momentum is compounding
  </text>
  <text x="342" y="338" width="530"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16"
        fill="#DCE6F7" opacity="0.76">
    The new workspace experience is driving deeper engagement across enterprise teams.
  </text>

  <!-- metric dividers -->
  <line x1="340" y1="386" x2="940" y2="386" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1"/>
  <line x1="540" y1="414" x2="540" y2="502" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="740" y1="414" x2="740" y2="502" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>

  <!-- metric column 1 -->
  <text x="340" y="452" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54"
        font-weight="700" fill="#FFFFFF" letter-spacing="-2">
    84%
  </text>
  <text x="344" y="486" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#D6E2F8" opacity="0.72">
    weekly active teams
  </text>

  <!-- metric column 2 -->
  <text x="574" y="452" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54"
        font-weight="700" fill="#FFFFFF" letter-spacing="-2">
    3.8×
  </text>
  <text x="578" y="486" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#D6E2F8" opacity="0.72">
    faster review cycles
  </text>

  <!-- metric column 3 -->
  <text x="774" y="452" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54"
        font-weight="700" fill="#FFFFFF" letter-spacing="-2">
    $12M
  </text>
  <text x="778" y="486" width="160"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#D6E2F8" opacity="0.72">
    projected annual value
  </text>

  <!-- subtle status chip -->
  <rect x="814" y="244" width="132" height="34" rx="17" ry="17"
        fill="#FFFFFF" opacity="0.13" stroke="#FFFFFF" stroke-opacity="0.22"/>
  <circle cx="836" cy="261" r="5" fill="#7CFFCB"/>
  <text x="852" y="266" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="600" fill="#F4FAFF" opacity="0.88">
    LIVE DATA
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on CSS `backdrop-filter`; it will not translate into editable PowerPoint glass.
- ❌ Do not apply `clip-path` to groups, rectangles, or text for the frosted area; use `clipPath` only on the blurred `<image>`.
- ❌ Do not use `<mask>` to create the panel reveal; masks are unsafe for this workflow.
- ❌ Do not put blur filters on `<line>` dividers; line filters are dropped.
- ❌ Do not use placeholder-only flat rectangles; the effect depends on a rich background plus a clipped blurred duplicate layer.

## Composition notes
- Keep the glass panel centered and large, roughly 55–65% of slide width, so the frosted area becomes the main visual object.
- Place oversized ambient typography behind the panel; it should be legible outside the glass and softly abstracted inside the clipped blur.
- Use high-contrast white foreground text inside the panel, with muted blue-gray labels to preserve the premium glass feel.
- Maintain generous internal padding; the panel should feel like a calm readable island over a vibrant, complex background.