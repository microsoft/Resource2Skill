# SVG Recipe — Animated Liquid Image Mask

## Visual mechanism
A full-bleed photograph sits underneath an oversized white compound shape whose center is cut out with an organic “liquid” Bezier contour, creating the illusion of an image revealed through a fluid window. Because SVG animation is not PowerPoint-editable, the SVG should build an animation-ready static keyframe with subtle motion echoes; after import, apply native PowerPoint Spin and Grow/Shrink animations to the white mask shape.

## SVG primitives needed
- 1× `<image>` for the full-slide photographic background revealed through the liquid opening
- 1× oversized compound `<path>` for the white mask frame, using an outer rectangle plus inner organic hole with `fill-rule="evenodd"`
- 1× `<path>` for a soft dark edge shadow around the liquid opening
- 3× `<path>` for faint rotated/scaled “motion echo” outlines that imply liquid movement
- 2× `<rect>` for the white canvas base and small editorial accent bars
- 2× `<circle>` for subtle decorative UI dots / brand details
- 4× `<text>` elements with explicit `width` attributes for logo, title, subtitle, and footer metadata
- 1× `<linearGradient>` for the accent bar
- 1× `<filter id="liquidEdgeBlur">` using `feGaussianBlur` for the soft inner edge depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="55%" stop-color="#6D5DFB"/>
      <stop offset="100%" stop-color="#00C2A8"/>
    </linearGradient>

    <filter id="liquidEdgeBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
  </defs>

  <!-- Bottom layer: full-screen photograph -->
  <rect x="0" y="0" width="1280" height="720" fill="#F7F7F4"/>
  <image
    href="https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&amp;fit=crop&amp;w=1800&amp;q=85"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Soft dark rim just inside the liquid opening -->
  <path
    d="M 346 145
       C 224 164 138 276 147 395
       C 158 550 293 623 430 589
       C 574 553 676 423 633 294
       C 601 198 481 124 346 145 Z"
    fill="none"
    stroke="#101828"
    stroke-width="30"
    opacity="0.22"
    filter="url(#liquidEdgeBlur)"/>

  <!-- Oversized white mask frame: outer rect + liquid hole. Import this as one editable shape. -->
  <path
    fill="#FFFFFF"
    fill-rule="evenodd"
    d="M -360 -260
       H 1640
       V 980
       H -360
       Z

       M 346 145
       C 224 164 138 276 147 395
       C 158 550 293 623 430 589
       C 574 553 676 423 633 294
       C 601 198 481 124 346 145
       Z"/>

  <!-- Motion echoes: static visual hint of the intended slow rotation / vertical pulse -->
  <path
    d="M 346 145
       C 224 164 138 276 147 395
       C 158 550 293 623 430 589
       C 574 553 676 423 633 294
       C 601 198 481 124 346 145 Z"
    fill="none"
    stroke="#D7DDE8"
    stroke-width="2.5"
    stroke-dasharray="12 14"
    opacity="0.72"
    transform="rotate(-7 395 365)"/>

  <path
    d="M 346 145
       C 224 164 138 276 147 395
       C 158 550 293 623 430 589
       C 574 553 676 423 633 294
       C 601 198 481 124 346 145 Z"
    fill="none"
    stroke="#E6EAF1"
    stroke-width="2"
    stroke-dasharray="4 12"
    opacity="0.95"
    transform="translate(395 365) scale(1.035 0.965) rotate(6) translate(-395 -365)"/>

  <path
    d="M 346 145
       C 224 164 138 276 147 395
       C 158 550 293 623 430 589
       C 574 553 676 423 633 294
       C 601 198 481 124 346 145 Z"
    fill="none"
    stroke="#CBD5E1"
    stroke-width="1.5"
    opacity="0.5"
    transform="translate(395 365) scale(0.965 1.04) rotate(12) translate(-395 -365)"/>

  <!-- Right-side editorial typography -->
  <rect x="760" y="162" width="108" height="6" rx="3" fill="url(#accentGrad)"/>
  <text x="760" y="215" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58"
        font-weight="800"
        letter-spacing="3"
        fill="#111827">
    <tspan x="760" dy="0">LIQUID</tspan>
    <tspan x="760" dy="66">IMAGE</tspan>
    <tspan x="760" dy="66">MASK</tspan>
  </text>

  <text x="764" y="454" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20"
        font-weight="400"
        fill="#4B5563">
    <tspan x="764" dy="0">A slow rotating organic window reveals</tspan>
    <tspan x="764" dy="30">the image beneath, giving a title slide</tspan>
    <tspan x="764" dy="30">premium motion-design energy.</tspan>
  </text>

  <rect x="764" y="568" width="174" height="42" rx="21" fill="#111827"/>
  <text x="790" y="595" width="126"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="700"
        letter-spacing="1.6"
        fill="#FFFFFF">SECTION 01</text>

  <!-- Small brand/navigation details -->
  <circle cx="1136" cy="72" r="5" fill="#111827"/>
  <circle cx="1156" cy="72" r="5" fill="#6D5DFB"/>
  <text x="960" y="78" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="700"
        letter-spacing="2"
        fill="#111827">FLUID LAB</text>

  <rect x="1040" y="646" width="62" height="2" fill="#111827" opacity="0.28"/>
  <text x="1118" y="652" width="86"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12"
        font-weight="600"
        letter-spacing="1.2"
        fill="#6B7280">2026</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; PowerPoint-editable output should be static, then animated with native PowerPoint effects after import.
- ❌ Do not use `<mask>` to punch the liquid hole; use a compound `<path>` with `fill-rule="evenodd"` instead.
- ❌ Do not place `clip-path` on the white overlay shape; if clipping is needed, apply `clip-path` only to an `<image>`.
- ❌ Do not use `<use href="#blob">` to duplicate the liquid outline; repeat the path data explicitly.
- ❌ Do not make the white mask frame only slide-sized if it will rotate later; it must be much larger than the canvas so corners never expose the photo during Spin animation.

## Composition notes
- Keep the liquid opening on the left 40–50% of the slide; reserve the right side as clean white negative space for title typography.
- Use an oversized white compound path so the frame can rotate slowly in PowerPoint without revealing edges.
- Add faint dashed echo contours around the hole to communicate fluid motion even before native animation is applied.
- For the true animated version, apply PowerPoint Spin to the white mask frame for ~20 seconds, then layer a subtle vertical Grow/Shrink pulse for ~5 seconds with auto-reverse.