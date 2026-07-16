# SVG Recipe — Product Feature "Magnifying Glass" Callout

## Visual mechanism
A full-bleed product/context image is dimmed, then the same image is reused at a larger scale inside a circular clip to create a floating “magnified” detail window. A crisp origin marker, connector line, bold ring, and editorial text label explain exactly where the detail comes from and why it matters.

## SVG primitives needed
- 2× `<image>` for the base product/context photo and the enlarged copy clipped into the magnifier
- 1× `<clipPath>` with `<circle>` for the circular zoom crop applied only to the magnified image
- 2× `<rect>` for the darkening overlay and glassy caption panel
- 3× `<circle>` for the magnifier shadow disk, magnifier border ring, and source-location marker
- 1× `<line>` for the connector from original feature point to zoom circle
- 3× `<path>` for premium accent glints, cursor/detail pointer, and decorative focus ticks
- 1× `<linearGradient>` for the subtle photo-dimming vignette
- 1× `<linearGradient>` for the translucent caption panel
- 1× `<filter id="softShadow">` applied to circular and panel shapes
- 4× `<text>` with explicit `width` attributes for callout title, description, eyebrow, and micro-label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="zoomCircle">
      <circle cx="910" cy="282" r="150"/>
    </clipPath>

    <linearGradient id="dimVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#06131d" stop-opacity="0.18"/>
      <stop offset="48%" stop-color="#06131d" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#02060a" stop-opacity="0.68"/>
    </linearGradient>

    <linearGradient id="captionGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.23"/>
      <stop offset="100%" stop-color="#77d6ff" stop-opacity="0.11"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ringGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed context image -->
  <image
    href="https://source.unsplash.com/1280x720/?premium-camera-lens-product-detail"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Dimming layer pushes the context photo back -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#dimVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.18"/>

  <!-- Source point and connector; keep line native, no filter -->
  <circle cx="505" cy="415" r="9" fill="#ff4f64"/>
  <circle cx="505" cy="415" r="25" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.88"/>
  <line x1="525" y1="402" x2="775" y2="318" stroke="#ffffff" stroke-width="2.5" opacity="0.92"/>

  <!-- Subtle focus ticks around the source feature -->
  <path d="M470 385 L456 371 M540 445 L555 460 M468 446 L452 461 M542 384 L557 369"
        fill="none" stroke="#ff4f64" stroke-width="3" stroke-linecap="round" opacity="0.95"/>

  <!-- Magnifier shadow disk -->
  <circle cx="910" cy="282" r="154" fill="#000000" opacity="0.28" filter="url(#softShadow)"/>

  <!-- Enlarged copy of the same image, translated so the source point appears at the circle center -->
  <image
    href="https://source.unsplash.com/1280x720/?premium-camera-lens-product-detail"
    x="-100" y="-585" width="2688" height="1512"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#zoomCircle)"/>

  <!-- Premium red magnifier ring -->
  <circle cx="910" cy="282" r="151" fill="none" stroke="#c94356" stroke-width="20" filter="url(#ringGlow)"/>
  <circle cx="910" cy="282" r="138" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.82"/>

  <!-- Inner pointer detail, useful for software/UI or tiny hardware feature callouts -->
  <path d="M938 230 L938 294 L956 276 L970 309 L986 302 L972 270 L998 270 Z"
        fill="#ffffff" stroke="#1b2730" stroke-width="3" stroke-linejoin="round" opacity="0.96"/>

  <!-- Specular glints to make the zoom circle feel like a lens -->
  <path d="M815 185 C852 155 907 144 954 158"
        fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.42"/>
  <path d="M1004 365 C975 398 926 415 878 404"
        fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.28"/>

  <!-- Caption panel in negative space -->
  <rect x="116" y="96" width="430" height="194" rx="22"
        fill="url(#captionGlass)" stroke="#ffffff" stroke-width="1.4"
        opacity="0.95" filter="url(#softShadow)"/>

  <text x="146" y="137" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="3"
        fill="#9ee8ff" opacity="0.95">
    PRODUCT DETAIL
  </text>

  <text x="146" y="182" width="370"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700"
        fill="#ffffff">
    Precision Craftsmanship
  </text>

  <text x="146" y="222" width="355"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="400"
        fill="#d9eef6" opacity="0.92">
    <tspan x="146" dy="0">The knurled control ring is enlarged</tspan>
    <tspan x="146" dy="25">to show tactile machining, material</tspan>
    <tspan x="146" dy="25">finish, and edge tolerance in context.</tspan>
  </text>

  <!-- Small technical label near source point -->
  <rect x="365" y="462" width="214" height="34" rx="17" fill="#071018" opacity="0.72"/>
  <text x="386" y="485" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600"
        fill="#ffffff" opacity="0.92">
    2.1× enlarged detail
  </text>

  <!-- Fine grain editorial rule -->
  <line x1="116" y1="322" x2="546" y2="322" stroke="#ffffff" stroke-width="1" opacity="0.28"/>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<g>`, `<rect>`, or `<circle>` for the magnifier; use the circular `clipPath` only on the enlarged `<image>`.
- ❌ Using SVG `<mask>` for the dimmed background or circular crop; masks are not reliable for PPT translation.
- ❌ Putting a filter on the connector `<line>`; PowerPoint translation drops line filters, so keep the line clean and native.
- ❌ Using `marker-end` for arrows; if an arrow is needed, draw a small triangular `<path>` manually.
- ❌ Overloading the slide with multiple magnifiers; this technique is strongest with one hero detail and one clear story.

## Composition notes
- Place the magnifier in negative space, usually upper-right or lower-right, so it does not cover the product’s main silhouette.
- Keep the source point visibly anchored with a small dot/ring, but make the zoom circle the dominant visual object.
- Darken the full image enough that the clipped zoom feels brighter and more premium, but do not obscure the product context.
- Use a thick high-contrast ring color, such as white, coral, or brand accent red, and repeat that accent once at the source marker for visual rhythm.