# SVG Recipe — Focal Zoom & Fade Overlay (Contextual Magnification)

## Visual mechanism
Duplicate the same dense source image: keep the full version as muted context, then place a scaled-up, clipped duplicate of the region of interest on top with a strong border and shadow. The viewer sees both the macro context and the magnified detail in a single static “zoom climax” state.

## SVG primitives needed
- 2× `<image>` for the full background document and the enlarged duplicate used inside the zoom window
- 1× `<clipPath>` with rounded `<rect>` for cropping the enlarged duplicate image to the focal window
- 1× full-slide `<rect>` for the pale fade overlay that mutes the background
- 3× `<rect>` for the slide frame, original ROI locator, and zoom-window border
- 1× `<filter id="zoomShadow">` with `feOffset`, `feGaussianBlur`, and `feMerge` for lifted focal-card depth
- 2× `<line>` for subtle context connectors from the original ROI to the magnified overlay
- 3× `<text>` blocks with explicit `width` attributes for title, annotation label, and caption
- 1× `<linearGradient>` for the small dark caption plate

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="zoomShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="captionPlate" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <!-- Crop region for the enlarged image. Apply clip-path directly to the <image>. -->
    <clipPath id="zoomClip">
      <rect x="505" y="214" width="560" height="260" rx="4" ry="4"/>
    </clipPath>
  </defs>

  <!-- Dark stage and thin presentation frame -->
  <rect x="0" y="0" width="1280" height="720" fill="#050505"/>
  <rect x="34" y="48" width="1212" height="624" fill="#f7f7f4" stroke="#2f4154" stroke-width="5"/>

  <!-- Full contextual image -->
  <image
    href="https://image.pollinations.ai/prompt/dense%20newspaper%20page%20with%20three%20columns%20headline%20small%20photo%20and%20body%20text%20editorial%20layout%20monochrome%20paper?width=1600&amp;height=900&amp;nologo=true"
    x="42" y="56" width="1196" height="608"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Fade overlay: use white for newspaper/document contexts, black for UI screenshots or maps -->
  <rect x="42" y="56" width="1196" height="608" fill="#ffffff" opacity="0.68"/>

  <!-- Slide title remains crisp above the faded context -->
  <text x="70" y="104" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="39" font-weight="700" fill="#c2410c">
    Contextual
  </text>
  <text x="70" y="168" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="800" fill="#ffffff" stroke="#dc2626" stroke-width="4">
    Zoom
  </text>
  <text x="72" y="230" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#ffffff" stroke="#0284c7" stroke-width="3">
    Overlay
  </text>

  <!-- Original ROI locator on the faded background -->
  <rect x="705" y="222" width="295" height="138" fill="none" stroke="#dc2626" stroke-width="4"/>
  <rect x="705" y="222" width="295" height="138" fill="#dc2626" opacity="0.05"/>

  <!-- Connector lines preserve spatial relationship without overwhelming the focus -->
  <line x1="705" y1="222" x2="505" y2="214" stroke="#dc2626" stroke-width="2.5" opacity="0.75" stroke-dasharray="8 7"/>
  <line x1="1000" y1="360" x2="1065" y2="474" stroke="#dc2626" stroke-width="2.5" opacity="0.75" stroke-dasharray="8 7"/>

  <!-- Zoom card base: shadowed white plate plus clipped enlarged duplicate -->
  <rect x="505" y="214" width="560" height="260" rx="4" fill="#ffffff" filter="url(#zoomShadow)"/>

  <!-- Enlarged duplicate of the same source image.
       Coordinates are shifted so the ROI lands inside the zoom frame. -->
  <image
    href="https://image.pollinations.ai/prompt/dense%20newspaper%20page%20with%20three%20columns%20headline%20small%20photo%20and%20body%20text%20editorial%20layout%20monochrome%20paper?width=1600&amp;height=900&amp;nologo=true"
    x="-890" y="-360" width="2460" height="1250"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#zoomClip)"/>

  <!-- Crisp high-contrast focal border -->
  <rect x="505" y="214" width="560" height="260" rx="4" fill="none" stroke="#dc2626" stroke-width="5"/>

  <!-- Optional annotation label mounted to zoom frame -->
  <rect x="505" y="486" width="560" height="58" rx="6" fill="url(#captionPlate)" opacity="0.96"/>
  <text x="528" y="522" width="515" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="650" fill="#ffffff">
    Magnified evidence stays anchored to its original location
  </text>

  <!-- Small product-style note in lower left -->
  <rect x="70" y="582" width="362" height="46" rx="8" fill="#0f172a" opacity="0.88"/>
  <text x="92" y="612" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#cbd5e1">
    Full context is visible, but visually de-emphasized.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<g>` or `<rect>` for the zoom crop; apply the clip directly to the enlarged `<image>`
- ❌ Using `<mask>` to create the fade or spotlight; use a simple semi-transparent overlay rectangle instead
- ❌ Using `<foreignObject>` for the newspaper/document content; use a raster `<image>` or native SVG shapes
- ❌ Relying on PowerPoint animation primitives; this recipe shows the final “fully zoomed and faded” state
- ❌ Placing the zoom card so far from the source ROI that the viewer loses spatial context

## Composition notes
- Keep the full source image nearly full-bleed, then mute it with a 55–75% white overlay for documents or a 45–65% black overlay for dark product screenshots.
- Place the zoom window near the ROI’s original location when possible; if it must move, add subtle dashed connector lines.
- Use a thick accent border, usually red/orange/blue, around both the original ROI and enlarged crop to create a clear visual pairing.
- Reserve one edge or the bottom of the zoom card for a short annotation; the magnified content should remain the main focus.