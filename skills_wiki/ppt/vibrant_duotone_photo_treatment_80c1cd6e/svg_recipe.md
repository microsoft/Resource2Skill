# SVG Recipe — Vibrant Duotone Photo Treatment

## Visual mechanism
A full-bleed photograph is converted into a graphic two-color field: shadows become deep violet/magenta while highlights become electric green or yellow. Bold white typography and a saturated accent label sit on top, using the controlled duotone contrast to keep the slide legible and editorial.

## SVG primitives needed
- 1× `<image>` for the full-bleed pre-duotoned hero photograph
- 1× `<clipPath>` with `<rect>` for clean full-slide image cropping
- 3× `<rect>` for color-wash overlays that intensify the duotone palette and add text-safe dark zones
- 1× `<linearGradient>` for a left-side readability vignette
- 1× `<radialGradient>` for a neon color bloom
- 1× `<filter id="textShadow">` applied to headline and label text
- 1× `<filter id="softGlow">` applied to accent blocks / logo card
- 4× `<text>` for headline, subtitle, label, and small metadata
- 1× rounded `<rect>` plus 1× `<text>` for a software/app-style badge
- 2× decorative `<path>` shapes for energetic duotone streaks
- 1× dashed `<line>` for a subtle editorial guide mark

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="slideCrop">
      <rect x="0" y="0" width="1280" height="720"/>
    </clipPath>

    <linearGradient id="leftReadability" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#16002e" stop-opacity="0.62"/>
      <stop offset="42%" stop-color="#16002e" stop-opacity="0.22"/>
      <stop offset="76%" stop-color="#16002e" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="greenBloom" cx="23%" cy="22%" r="74%">
      <stop offset="0%" stop-color="#24ff00" stop-opacity="0.55"/>
      <stop offset="48%" stop-color="#24ff00" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#24ff00" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="magentaWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#16ff00" stop-opacity="0.10"/>
      <stop offset="58%" stop-color="#a30083" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#3b005e" stop-opacity="0.44"/>
    </linearGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/preprocessed-duotone-electric-green-magenta-portrait-hero.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#slideCrop)"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#magentaWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#greenBloom)"/>
  <rect x="0" y="0" width="760" height="720" fill="url(#leftReadability)"/>

  <path d="M-80,626 C150,555 246,618 390,558 C540,496 662,514 790,450"
        fill="none" stroke="#ec5be9" stroke-width="34" stroke-opacity="0.22"/>
  <path d="M875,-40 C945,122 1044,160 1210,112 C1292,88 1338,82 1390,102"
        fill="none" stroke="#39ff14" stroke-width="44" stroke-opacity="0.24"/>

  <text x="64" y="318" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="800" letter-spacing="-4"
        fill="#ffffff" filter="url(#textShadow)">Duotone</text>

  <text x="64" y="463" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="800" letter-spacing="-4"
        fill="#ffffff" filter="url(#textShadow)">Effect</text>

  <rect x="58" y="570" width="284" height="94" rx="0"
        fill="#ef64df" filter="url(#softGlow)" opacity="0.88"/>
  <rect x="58" y="570" width="284" height="94" rx="0"
        fill="#ef64df"/>

  <text x="86" y="635" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="300" letter-spacing="2"
        fill="#ffffff" filter="url(#textShadow)">HOW TO</text>

  <line x1="64" y1="528" x2="330" y2="528"
        stroke="#ffffff" stroke-width="3" stroke-opacity="0.55"
        stroke-dasharray="10 14"/>

  <rect x="1088" y="30" width="160" height="158" rx="26"
        fill="#001c38" filter="url(#textShadow)"/>
  <rect x="1088" y="30" width="160" height="158" rx="26"
        fill="#001f3d"/>

  <text x="1122" y="140" width="106"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="96" font-weight="700"
        fill="#35a8ff">Ps</text>

  <text x="914" y="656" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="4"
        fill="#ffffff" opacity="0.78">PHOTO / COLOR / BRAND</text>

  <rect x="1010" y="636" width="176" height="2"
        fill="#39ff14" opacity="0.72"/>
</svg>
```

## Avoid in this skill
- ❌ SVG filter color remapping such as `feColorMatrix` or blend modes to create the duotone dynamically; PowerPoint translation will not reliably preserve a true pixel-level duotone.
- ❌ `mask`-based photo treatments; use a preprocessed duotone image plus editable SVG overlays instead.
- ❌ Low-contrast text placed over bright highlight regions without a dark vignette or shadow.
- ❌ Natural-color photographs under neon overlays; the effect should read as a true two-color image, not a tinted photo.

## Composition notes
- Use a preprocessed duotone photo as the base: shadows mapped to violet/magenta and highlights mapped to electric green, yellow, cyan, or brand accent color.
- Reserve one side of the image for type by adding a dark gradient vignette; this keeps the photograph full-bleed while protecting headline readability.
- Keep typography oversized, bold, and minimal; the image texture provides energy, so the text should be simple and high contrast.
- Repeat the duotone colors in small UI-like accents, badges, lines, or labels to make the whole slide feel intentionally branded.