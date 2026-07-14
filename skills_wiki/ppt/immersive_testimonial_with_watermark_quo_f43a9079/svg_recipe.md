# SVG Recipe — Watermark Quote Testimonial Slide

## Visual mechanism
A full-bleed emotional photograph is darkened with layered translucent overlays, then treated as a cinematic canvas for a large white testimonial. The signature device is an oversized semi-transparent quote mark placed behind the copy as an editorial watermark, creating depth without sacrificing readability.

## SVG primitives needed
- 1× `<image>` for the full-bleed background photograph
- 1× `<rect>` for a dark fallback base behind the photo
- 2× `<rect>` overlays for global darkening and left-side readability gradient
- 1× `<linearGradient>` for the side-to-side vignette over the photo
- 1× `<radialGradient>` for subtle atmospheric highlight around the subject area
- 2× `<text>` elements for oversized translucent quote watermark marks
- 4× `<text>` elements for the main quote, attribution, role/company, and quiet brand mark
- 1× `<line>` for the attribution separator accent
- 1× `<filter id="softTextShadow">` applied to foreground text for legibility
- 1× `<filter id="logoGlow">` applied to the small brand mark
- Optional decorative `<path>` strokes for subtle editorial contour/wave accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftReadability" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.78"/>
      <stop offset="42%" stop-color="#000000" stop-opacity="0.52"/>
      <stop offset="72%" stop-color="#000000" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.50"/>
    </linearGradient>

    <radialGradient id="coolAtmosphere" cx="63%" cy="36%" r="62%">
      <stop offset="0%" stop-color="#15F2C8" stop-opacity="0.18"/>
      <stop offset="38%" stop-color="#0B8F84" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="softTextShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="3" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="logoGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Deep fallback color in case the remote photo is unavailable -->
  <rect x="0" y="0" width="1280" height="720" fill="#091011"/>

  <!-- Full-bleed emotional background photo -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/customer-success-couple-modern-home-evening.jpg"/>

  <!-- Dark cinematic treatment over the image -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.32"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftReadability)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#coolAtmosphere)"/>

  <!-- Subtle editorial contour accents -->
  <path d="M-20,586 C145,542 258,623 420,580 C584,537 730,580 895,548 C1040,520 1158,542 1304,506"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.12"/>
  <path d="M-10,610 C150,570 274,646 438,603 C598,562 738,607 905,575 C1060,545 1165,566 1300,532"
        fill="none" stroke="#10E0C0" stroke-width="3" opacity="0.10"/>

  <!-- Giant watermark quotation marks -->
  <text x="78" y="285" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="260" font-weight="900" fill="#FFFFFF" opacity="0.24">“</text>
  <text x="900" y="620" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="230" font-weight="900" fill="#FFFFFF" opacity="0.14">”</text>

  <!-- Quiet brand mark in the top right -->
  <text x="1010" y="72" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#FFFFFF" opacity="0.90" filter="url(#logoGlow)">
    HOMEFLOW
  </text>
  <text x="1010" y="96" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="10" font-weight="500" letter-spacing="1.8" fill="#FFFFFF" opacity="0.58">
    CUSTOMER STORIES
  </text>

  <!-- Main testimonial quote -->
  <text x="118" y="250" width="790" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="900" fill="#FFFFFF" filter="url(#softTextShadow)">
    <tspan x="118" dy="0">HomeFlow transformed our</tspan>
    <tspan x="118" dy="58">move from overwhelming to</tspan>
    <tspan x="118" dy="58">effortless — every detail felt</tspan>
    <tspan x="118" dy="58">personal, calm, and expertly led.</tspan>
  </text>

  <!-- Attribution block -->
  <line x1="122" y1="542" x2="206" y2="542" stroke="#FFFFFF" stroke-width="4" opacity="0.92"/>
  <text x="122" y="590" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#FFFFFF" filter="url(#softTextShadow)">
    Patricia &amp; Michael Kiernan
  </text>
  <text x="122" y="622" width="640" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-style="italic" fill="#FFFFFF" opacity="0.78">
    First-time buyers · Dublin, Ireland
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to darken or fade the background; use editable translucent `<rect>` overlays and gradients instead.
- ❌ Do not put `clip-path` on quote text or overlay rectangles; clipping is only reliable for `<image>` elements.
- ❌ Do not rely on a pale or busy photo without a dark overlay; the heavy white testimonial text needs strong contrast.
- ❌ Do not make the watermark quote fully opaque; it should read as texture behind the testimonial, not compete with it.
- ❌ Do not use `marker-end` for decorative arrows or quote accents; if needed, build arrows with `<line>` and simple shapes.

## Composition notes
- Anchor the main quote in the middle-left 60–70% of the slide, leaving the right side mostly photographic and atmospheric.
- Keep the watermark quote large enough to crop visually into the layout; it should feel oversized and editorial.
- Use white typography almost exclusively, with only a very subtle brand accent or atmospheric tint from the photo.
- Place attribution below the quote with a short horizontal rule so the testimonial has a clear speaker hierarchy.