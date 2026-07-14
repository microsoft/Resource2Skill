# SVG Recipe — Product Detail Magnifier (The "Loupe" Effect)

## Visual mechanism
A full-bleed product photo is darkened to become context, while the same photo is duplicated, enlarged, and clipped into a crisp circular “loupe” that reveals a bright close-up detail. Thin locator lines connect the magnified circle back to the original point, creating a premium inspection-style product callout.

## SVG primitives needed
- 2× `<image>` for the dimmed full-slide product photo and the enlarged bright duplicate inside the loupe
- 1× `<clipPath>` with `<circle>` for the circular loupe crop applied to the zoomed image
- 3× `<rect>` for the darkening overlay, text panel wash, and subtle bottom vignette
- 5× `<circle>` for loupe border, shadow/glow base, original-detail locator rings, and endpoint dots
- 2× `<line>` for connector rays from the original detail to the loupe
- 1× `<path>` for a small decorative precision bracket near the label
- 1× `<filter id="loupeShadow">` applied to the loupe support circle
- 1× `<filter id="softGlow">` applied to the original-detail locator ring
- 2× `<linearGradient>` for premium dark overlays and warm accent strokes
- 3× `<text>` blocks with explicit `width` for title, body, and micro-label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="loupeClip">
      <circle cx="875" cy="335" r="168"/>
    </clipPath>

    <linearGradient id="rightPanelFade" x1="620" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#05070A" stop-opacity="0"/>
      <stop offset="0.55" stop-color="#05070A" stop-opacity="0.54"/>
      <stop offset="1" stop-color="#05070A" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="bottomVignette" x1="0" y1="420" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="accentStroke" x1="710" y1="180" x2="1030" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.45" stop-color="#D8C49A"/>
      <stop offset="1" stop-color="#A88345"/>
    </linearGradient>

    <filter id="loupeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <!-- Full-bleed product context image -->
  <rect x="0" y="0" width="1280" height="720" fill="#05070A"/>
  <image
    href="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.48"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.30"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#rightPanelFade)"/>
  <rect x="0" y="420" width="1280" height="300" fill="url(#bottomVignette)"/>

  <!-- Original detail locator on the darkened background -->
  <circle cx="330" cy="485" r="34" fill="none" stroke="#D8C49A" stroke-width="2.5" opacity="0.92"/>
  <circle cx="330" cy="485" r="47" fill="none" stroke="#D8C49A" stroke-width="1.2" stroke-dasharray="6 8" opacity="0.62"/>
  <circle cx="330" cy="485" r="54" fill="none" stroke="#D8C49A" stroke-width="8" opacity="0.18" filter="url(#softGlow)"/>

  <!-- Connector rays: use line, not path, so arrow behavior remains editable -->
  <line x1="365" y1="468" x2="715" y2="270" stroke="#D8C49A" stroke-width="1.4" opacity="0.72"/>
  <line x1="368" y1="502" x2="716" y2="402" stroke="#D8C49A" stroke-width="1.4" opacity="0.52"/>
  <circle cx="330" cy="485" r="5" fill="#D8C49A"/>
  <circle cx="715" cy="270" r="4" fill="#D8C49A" opacity="0.9"/>
  <circle cx="716" cy="402" r="4" fill="#D8C49A" opacity="0.7"/>

  <!-- Loupe shadow/base -->
  <circle cx="875" cy="335" r="180" fill="#000000" opacity="0.55" filter="url(#loupeShadow)"/>

  <!-- Magnified duplicate image.
       Detail point in original: (330,485). Zoom: 2.25.
       Image placement formula: x = loupeCx - detailX*zoom; y = loupeCy - detailY*zoom. -->
  <image
    href="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="132.5" y="-756.25" width="2880" height="1620"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#loupeClip)"/>

  <!-- Loupe rim and inner highlight -->
  <circle cx="875" cy="335" r="168" fill="none" stroke="#FFFFFF" stroke-width="8"/>
  <circle cx="875" cy="335" r="174" fill="none" stroke="url(#accentStroke)" stroke-width="4"/>
  <circle cx="875" cy="335" r="150" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity="0.28"/>
  <path d="M755 233 C782 205, 824 188, 875 188" fill="none" stroke="#FFFFFF" stroke-width="2.2" opacity="0.46"/>

  <!-- Text system -->
  <path d="M715 555 L715 605 L762 605" fill="none" stroke="#D8C49A" stroke-width="2.5"/>
  <text x="740" y="575" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" letter-spacing="2.5" fill="#D8C49A">
    MATERIAL DETAIL / 2.25× MAGNIFICATION
  </text>

  <text x="740" y="625" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#FFFFFF">
    PREMIUM CRAFTSMANSHIP
  </text>

  <text x="740" y="664" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#D7DCE2">
    <tspan x="740" dy="0">The loupe isolates the stitching, texture, and seam</tspan>
    <tspan x="740" dy="25">alignment while preserving the full product context.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to dim everything except the loupe; use a duplicated clipped image instead.
- ❌ Do not apply `clip-path` to a `<g>` or `<rect>` for the loupe; apply the circular clip directly to the magnified `<image>`.
- ❌ Do not use `<path marker-end="...">` for connector arrows; use editable `<line>` elements and endpoint dots.
- ❌ Do not use `<filter>` on connector `<line>` elements; shadows and glows should sit on circles or paths.
- ❌ Do not rely on CSS `filter: brightness()` for the background image; use a dark overlay rectangle and image opacity for predictable PowerPoint translation.

## Composition notes
- Put the loupe opposite the original detail point to create a diagonal inspection path across the slide.
- Keep the full photo visible but subdued; the loupe should be the only bright, high-detail region.
- Size the loupe to roughly 30–40% of slide height so it feels intentional, not like a small annotation.
- Place title and body near the loupe, usually in the darker negative space, with a small accent label to reinforce technical precision.