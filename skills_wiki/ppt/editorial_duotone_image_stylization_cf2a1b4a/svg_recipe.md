# SVG Recipe — Duotone Image Stylization

## Visual mechanism
A full-bleed or side-anchored photograph is reduced to a two-color editorial palette: deep shadow purple plus warm peach highlight. Large typographic forms sit in the open highlight field, creating a branded title-slide look where the image feels integrated rather than decorative.

## SVG primitives needed
- 1× `<rect>` for the warm peach base background
- 1× `<image>` for a preprocessed duotone portrait/photo asset, clipped to the left side of the slide
- 1× `<clipPath>` using a `<rect>` to crop the photo cleanly without distorting it
- 2× `<linearGradient>` for subtle brand wash and tonal chip overlays
- 3× translucent `<rect>` overlays for highlight haze, edge vignette, and duotone color sample
- 1× `<rect>` with rounded corners for the app/logo-style badge
- 4× `<text>` elements for the main title, subtitle, badge letters, and small editorial label
- 1× `<filter id="softShadow">` applied to the badge for a premium floating feel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="leftPhotoCrop">
      <rect x="0" y="0" width="560" height="720"/>
    </clipPath>

    <linearGradient id="creamWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2f1747" stop-opacity="0.16"/>
      <stop offset="42%" stop-color="#f8d7a6" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#f8d7a6" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="toneChip" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5b285d" stop-opacity="0.88"/>
      <stop offset="55%" stop-color="#8b5b74" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#f0c296" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="leftVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2b1244" stop-opacity="0.34"/>
      <stop offset="62%" stop-color="#2b1244" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#2b1244" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Warm highlight field: the light half of the duotone palette -->
  <rect x="0" y="0" width="1280" height="720" fill="#f6d4a3"/>

  <!-- Use a photo that has already been gradient-mapped to purple shadows and peach highlights. -->
  <image
    x="-50" y="0" width="650" height="720"
    href="https://images.example.com/duotone-purple-peach-side-profile-fashion-portrait.png"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#leftPhotoCrop)"/>

  <!-- Brand tint layers that help the photo melt into the peach field. -->
  <rect x="0" y="0" width="720" height="720" fill="url(#creamWash)"/>
  <rect x="0" y="0" width="430" height="720" fill="url(#leftVignette)"/>

  <!-- Editorial tone chip: visually demonstrates the shadow-to-highlight color ramp. -->
  <rect x="134" y="122" width="202" height="284" fill="url(#toneChip)" opacity="0.92"/>

  <!-- Small product/app badge in the upper-right corner. -->
  <rect x="1089" y="47" width="135" height="132" rx="24" fill="#5b285d" filter="url(#softShadow)"/>
  <text x="1115" y="140" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="800" fill="#ffe0a8">Ps</text>

  <!-- Main editorial headline. Keep the right half open and calm. -->
  <text x="565" y="350" width="675" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="128" font-weight="800" letter-spacing="4" fill="#5b285d">DUOTONE</text>

  <text x="568" y="463" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="122" font-weight="300" letter-spacing="14" fill="#5b285d">COLORING</text>

  <!-- Optional small deck label; remove for cleaner title slides. -->
  <text x="573" y="548" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="600" letter-spacing="3" fill="#7a4468" opacity="0.72">
    EDITORIAL IMAGE SYSTEM
  </text>

  <!-- Subtle bottom grounding band, using the same shadow hue at very low opacity. -->
  <rect x="0" y="676" width="1280" height="44" fill="#3c164f" opacity="0.08"/>
</svg>
```

## Avoid in this skill
- ❌ SVG blend modes such as `mix-blend-mode`, `background-blend-mode`, or CSS filters for duotone mapping; these are unlikely to translate into editable PowerPoint reliably.
- ❌ `<feColorMatrix>` or complex SVG filter chains for true pixel-level duotone conversion; preprocess the photo or use a prepared duotone image asset instead.
- ❌ Applying `clip-path` to colored rectangles or text; only clip the `<image>` crop.
- ❌ Low-contrast typography over the detailed photo area; place headline text over the clean highlight field or add a dark vignette behind it.
- ❌ Using three or more competing accent colors; the effect depends on strict two-color discipline.

## Composition notes
- Keep the photo subject anchored to the left third, leaving the right half mostly open for oversized typography.
- Use the highlight color as the slide background, not pure white; this makes the photo and negative space feel like one continuous duotone treatment.
- Let the shadow color drive all typography, badges, and accents for palette consistency.
- If text must cross the image, add a semi-transparent shadow-color vignette behind it rather than a hard opaque box.