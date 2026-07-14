# SVG Recipe — Geometric Image Masking & Composition

## Visual mechanism
Crop photography into a clean geometric boundary — here, a perfect circle — and place it against a saturated gradient field with oversized translucent geometry. The contrast between crisp masked image edges, soft background rings, and minimal white typography creates a polished tutorial/title-slide composition.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background.
- 5× `<circle>` for oversized translucent background rings and the circular photo shadow/base.
- 1× `<image>` for the hero photograph, clipped into a circle.
- 1× `<clipPath id="photoCircleClip">` with a `<circle>` to crop the image.
- 1× `<linearGradient>` for the purple-to-orange background wash.
- 1× `<radialGradient>` for subtle glow behind the circular photo.
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for image-card depth.
- 2× `<text>` elements for editable title hierarchy.
- 1× `<path>` for a translucent diagonal color overlay that adds motion and depth.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#5F39C8"/>
      <stop offset="0.45" stop-color="#A6388E"/>
      <stop offset="1" stop-color="#F04A1A"/>
    </linearGradient>

    <radialGradient id="photoGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#38D6FF" stop-opacity="0.34"/>
      <stop offset="0.55" stop-color="#1A7BCB" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#001A2A" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoCircleClip" clipPathUnits="userSpaceOnUse">
      <circle cx="1038" cy="460" r="270"/>
    </clipPath>
  </defs>

  <!-- Full-bleed gradient field -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <!-- Large translucent geometry: oversized rings that echo the crop shape -->
  <circle cx="318" cy="438" r="315" fill="#FFFFFF" opacity="0.13"/>
  <circle cx="460" cy="445" r="250" fill="#3B0F62" opacity="0.18"/>
  <circle cx="452" cy="425" r="124" fill="#FFFFFF" opacity="0.12"/>
  <circle cx="382" cy="398" r="620" fill="none" stroke="#FFFFFF" stroke-width="120" opacity="0.08"/>

  <!-- Subtle diagonal overlay to keep the composition energetic -->
  <path d="M548 0 L768 0 C872 88 950 198 1002 332 C1054 468 1052 600 1004 720 L832 720 C878 592 872 470 812 350 C752 230 658 112 548 0 Z"
        fill="#FFFFFF" opacity="0.08"/>

  <!-- Glow and shadow foundation behind circular image -->
  <circle cx="1038" cy="460" r="292" fill="url(#photoGlow)" opacity="0.9"/>
  <circle cx="1038" cy="460" r="270" fill="#061C2B" filter="url(#softShadow)"/>

  <!-- Circularly masked image; preserveAspectRatio slices the photo without distortion -->
  <image x="768" y="190" width="540" height="540"
         href="https://images.example.com/ocean-sea-turtle-aquarium-hero-photo.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoCircleClip)"/>

  <!-- Optional dark edge overlay for better contrast against bright backgrounds -->
  <circle cx="1038" cy="460" r="270" fill="none" stroke="#06253A" stroke-width="2" opacity="0.55"/>

  <!-- Editable typography -->
  <text x="100" y="390" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="60" font-weight="300"
        fill="#FFFFFF" opacity="0.95">
    PowerPoint Tutorial
  </text>

  <text x="100" y="468" width="660"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="60" font-weight="700"
        fill="#FFFFFF">
    Crop Image to Shape
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<rect>` or `<circle>` as a pseudo-mask; clipping should be applied directly to the `<image>`.
- ❌ Using `<mask>` for image reveals; it may hard-fail or be ignored by the PPT translator.
- ❌ Using `<pattern>` fills to simulate photo texture; use a real `<image>` with a geometric `clipPath`.
- ❌ Cropping by stretching the image to fit the shape; use `preserveAspectRatio="xMidYMid slice"` so the photo remains natural.
- ❌ Adding arrow markers or line filters around the mask; use simple editable strokes or shadowed backing shapes instead.

## Composition notes
- Keep the masked photo large enough to feel intentional: about 38–45% of slide width works well for title slides.
- Place text in the negative space opposite the image, aligned to the visual centerline of the circular crop.
- Repeat the mask geometry subtly in the background using low-opacity circles or rings to unify the layout.
- Use a vivid photo against a dark or saturated gradient; the crisp crop edge should be one of the main focal points.