# SVG Recipe — Impact Milestone Reveal with Floating Badge

## Visual mechanism
A cinematic full-bleed photo is muted by a dark translucent horizontal band, creating a high-contrast stage for oversized uppercase typography. A vivid circular badge floats across the band’s bottom edge, breaking the grid and turning the key milestone into the focal point.

## SVG primitives needed
- 1× `<image>` for the full-bleed contextual background photo
- 2× full-slide `<rect>` overlays for global darkening and vignette depth
- 1× wide translucent `<rect>` for the central letterbox band
- 1× small accent `<rect>` line above the headline
- 1× `<circle>` for the floating milestone badge
- 1× subtle outer `<circle>` ring for badge polish
- 5× `<text>` elements for eyebrow, headline, badge date, badge year, and badge label
- 1× `<radialGradient>` for the vignette overlay
- 1× `<linearGradient>` for the translucent band
- 1× `<filter id="badgeShadow">` applied to the badge circle
- 1× `<filter id="softShadow">` applied to the letterbox band

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.70"/>
    </radialGradient>

    <linearGradient id="bandFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#111216" stop-opacity="0.72"/>
      <stop offset="45%" stop-color="#1B1C21" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#111216" stop-opacity="0.72"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-40%" width="120%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="badgeShadow" x="-45%" y="-45%" width="190%" height="190%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed cinematic background -->
  <image
    href="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Muting layers keep text readable over busy photography -->
  <rect x="0" y="0" width="1280" height="720" fill="#101217" opacity="0.34"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- Translucent horizontal letterbox band -->
  <rect x="0" y="205" width="1280" height="250" fill="url(#bandFill)" filter="url(#softShadow)"/>

  <!-- Small executive-style accent line -->
  <rect x="565" y="248" width="150" height="6" rx="3" fill="#F4B004"/>

  <!-- Eyebrow label -->
  <text x="640" y="292" width="720"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="700"
        letter-spacing="4"
        fill="#F4B004">
    GLOBAL PRODUCT ROLLOUT
  </text>

  <!-- Main impact headline -->
  <text x="640" y="368" width="1180"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="78"
        font-weight="800"
        letter-spacing="7"
        fill="#FFFFFF">
    LAUNCHING DATE
  </text>

  <!-- Floating badge: center aligns exactly with bottom edge of band at y=455 -->
  <circle cx="640" cy="455" r="122" fill="#F4B004" filter="url(#badgeShadow)"/>
  <circle cx="640" cy="455" r="109" fill="none" stroke="#FFD968" stroke-width="3" opacity="0.75"/>

  <!-- Badge text stack -->
  <text x="640" y="414" width="210"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28"
        font-weight="800"
        letter-spacing="2"
        fill="#252525">
    05 DEC
  </text>

  <text x="640" y="483" width="230"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64"
        font-weight="900"
        letter-spacing="-1"
        fill="#1E1E1E">
    2024
  </text>

  <text x="640" y="523" width="210"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="700"
        letter-spacing="3"
        fill="#38301A">
    GO-LIVE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a mask to darken or crop the background; use translucent rectangles and gradients instead.
- ❌ Do not place the badge fully inside the band; the badge center should align with the band’s bottom edge for the “floating” reveal.
- ❌ Do not use low-contrast badge text; dark charcoal on yellow/orange keeps the metric readable.
- ❌ Do not apply filters to lines; use a small rounded rectangle for the accent rule if shadow or polish is needed.
- ❌ Do not overcrowd the photo with labels outside the band; the band and badge should carry the message.

## Composition notes
- Keep the band in the vertical middle third, occupying roughly 35% of slide height; this creates a cinematic letterbox feel.
- Center the badge horizontally and set its center point on the band’s bottom edge so it visibly overlaps both the band and the photo.
- Use a dark, high-opacity band over a moody photo, then reserve one vivid accent color for both the badge and the small headline rule.
- Leave the top and bottom of the slide mostly photographic and quiet; the viewer’s eye should travel from accent line → headline → floating badge.