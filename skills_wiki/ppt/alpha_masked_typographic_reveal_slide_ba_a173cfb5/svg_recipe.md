# SVG Recipe — Alpha-Masked Typographic Reveal (Slide Background Fill Effect)

## Visual mechanism
A full-bleed hero photo is darkened by a left-heavy transparent gradient overlay, while a giant letter-shaped image crop sits above the overlay and visually “cuts through” it to reveal the untouched photograph beneath. The result mimics PowerPoint’s Slide Background Fill punch-out effect while staying editable through SVG primitives.

## SVG primitives needed
- 2× `<image>` for the same full-slide hero photo: one as the true background, one clipped into the giant letter reveal
- 1× `<clipPath>` with a custom `<path>` for the giant typographic letter crop
- 2× `<rect>` for the fallback base color and the dark gradient overlay
- 3× `<linearGradient>` for the dark alpha overlay, subtle title accent, and fine edge highlight
- 3× `<path>` for the letter silhouette, inner counter cover, and faint typographic edge highlight
- 1× `<filter id="softTextShadow">` applied to title and body copy for readability over photography
- 4× `<text>` blocks with explicit `width` for eyebrow, title, body, and metadata label
- 2× `<line>` elements for minimal editorial divider rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkRevealOverlay" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.96"/>
      <stop offset="35%" stop-color="#0F172A" stop-opacity="0.94"/>
      <stop offset="68%" stop-color="#0F172A" stop-opacity="0.48"/>
      <stop offset="88%" stop-color="#0F172A" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="letterEdgeLight" x1="140" y1="90" x2="565" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="670" y1="0" x2="830" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F6D365"/>
      <stop offset="100%" stop-color="#FDA085"/>
    </linearGradient>

    <filter id="softTextShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="letterAClip" clipPathUnits="userSpaceOnUse">
      <path d="M135 650 L264 70 L432 70 L565 650 L430 650 L405 525 L291 525 L266 650 Z
               M313 425 L383 425 L349 230 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#1E293B"/>

  <image
    href="https://images.example.com/hero/australia-coastline-aerial-golden-hour-1920x1080.jpg"
    xlink:href="https://images.example.com/hero/australia-coastline-aerial-golden-hour-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkRevealOverlay)"/>

  <image
    href="https://images.example.com/hero/australia-coastline-aerial-golden-hour-1920x1080.jpg"
    xlink:href="https://images.example.com/hero/australia-coastline-aerial-golden-hour-1920x1080.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#letterAClip)"/>

  <path d="M313 425 L383 425 L349 230 Z" fill="#0F172A" opacity="0.92"/>

  <path d="M135 650 L264 70 L432 70 L565 650 L430 650 L405 525 L291 525 L266 650 Z"
        fill="none" stroke="url(#letterEdgeLight)" stroke-width="3" opacity="0.7"/>

  <line x1="670" y1="222" x2="792" y2="222" stroke="url(#goldAccent)" stroke-width="4"/>
  <line x1="670" y1="594" x2="1130" y2="594" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>

  <text x="670" y="198" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="4"
        fill="#FDE68A" filter="url(#softTextShadow)">
    CHAPTER 04 · SOUTHERN HEMISPHERE
  </text>

  <text x="666" y="304" width="470"
        font-family="Georgia, Segoe UI, Microsoft YaHei, serif"
        font-size="64" font-weight="700"
        fill="#FFFFFF" filter="url(#softTextShadow)">
    Australia
  </text>

  <text x="672" y="358" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="400"
        fill="#E2E8F0" filter="url(#softTextShadow)">
    <tspan x="672" dy="0">A cinematic overview of coast, desert, and city</tspan>
    <tspan x="672" dy="31">systems — framed through one oversized initial</tspan>
    <tspan x="672" dy="31">that reveals the landscape beneath the surface.</tspan>
  </text>

  <text x="672" y="515" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2"
        fill="#CBD5E1" opacity="0.92">
    VISUAL TERRITORY · COASTAL / MINERAL / URBAN
  </text>

  <text x="1046" y="626" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" text-anchor="end"
        fill="#FFFFFF" opacity="0.58">
    35°18′S · 149°07′E
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to punch out the letter; masks are not reliable for this translation path.
- ❌ Do not use `<text>` as a clipping path or image fill; convert the giant letter to an editable `<path>` silhouette instead.
- ❌ Do not use `<pattern>` fills to place the image inside the letter; use a duplicated `<image>` with `clip-path`.
- ❌ Do not apply `clip-path` to regular shapes or text; only use it on the duplicated `<image>`.
- ❌ Do not rely on transparent text fill to create the cutout; PowerPoint will not treat it as a true background-fill reveal.

## Composition notes
- Keep the giant letter on the left 35–45% of the slide, tall enough to dominate the frame but cropped comfortably inside the canvas.
- Place title copy near the center-right, where the overlay is still dark enough for contrast but begins fading into the photo.
- Use the exact same hero image twice, aligned identically, so the clipped letter reveal matches the underlying photo perfectly.
- Reserve the far right and upper-right for negative space; the visual weight should come from the dark overlay and the oversized typographic window.