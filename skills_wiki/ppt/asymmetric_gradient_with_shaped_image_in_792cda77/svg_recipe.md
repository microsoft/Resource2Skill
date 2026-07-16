# SVG Recipe — Asymmetric Gradient with Shaped Image Inset

## Visual mechanism
A full-slide diagonal green gradient creates the energetic brand field, while a tall black-and-white photo is clipped into an oversized vertical oval that breaks the left edge of the canvas. Large white serif typography sits in the open right-hand space, balanced by a small rounded subtitle label and a thin vertical accent bar.

## SVG primitives needed
- 1× `<rect>` for the full-slide diagonal gradient background
- 2× `<linearGradient>` for the main green field and the subtle CTA/button highlight
- 1× `<clipPath>` with `<ellipse>` for the shaped photo inset
- 1× `<image>` for the black-and-white portrait / product / workplace photo clipped into the oval
- 1× `<filter id="ovalShadow">` using `feOffset + feGaussianBlur + feMerge` for depth behind the shaped image
- 1× `<ellipse>` behind the image as a soft editable shadow carrier
- 1× thin `<rect>` for the off-white vertical accent bar
- 2× translucent `<path>` elements for premium diagonal motion accents in the gradient field
- 1× rounded `<rect>` for the subtitle/company label pill
- 4× `<text>` elements for eyebrow text, main title, label text, and small footer metadata
- 1× `<line>` for a minimalist divider near the title block

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="brandGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8EC63F"/>
      <stop offset="0.38" stop-color="#35A853"/>
      <stop offset="0.72" stop-color="#056B3F"/>
      <stop offset="1" stop-color="#014D2E"/>
    </linearGradient>

    <linearGradient id="pillGradient" x1="745" y1="505" x2="1040" y2="565" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.12"/>
    </linearGradient>

    <filter id="ovalShadow" x="-30%" y="-20%" width="160%" height="150%">
      <feOffset dx="18" dy="20" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitOval">
      <ellipse cx="235" cy="360" rx="255" ry="335"/>
    </clipPath>
  </defs>

  <!-- Base brand gradient -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#brandGradient)"/>

  <!-- Subtle diagonal light fields for premium depth -->
  <path d="M650 -80 C820 30 960 90 1330 60 L1330 210 C1010 235 800 175 610 40 Z"
        fill="#FFFFFF" opacity="0.08"/>
  <path d="M720 760 C920 610 1050 540 1330 520 L1330 720 L720 720 Z"
        fill="#001E16" opacity="0.18"/>

  <!-- Left vertical accent bar -->
  <rect x="36" y="0" width="8" height="720" fill="#F3F2E8" opacity="0.95"/>

  <!-- Editable oval shadow, slightly offset from image -->
  <ellipse cx="248" cy="370" rx="255" ry="335"
           fill="#002415" opacity="0.32" filter="url(#ovalShadow)"/>

  <!-- Oversized clipped black-and-white image inset -->
  <image x="-90" y="20" width="620" height="680"
         href="https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&amp;fit=crop&amp;w=900&amp;h=1200&amp;q=85&amp;sat=-100"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#portraitOval)"/>

  <!-- Slight green glass overlay to integrate photo with brand palette -->
  <ellipse cx="235" cy="360" rx="255" ry="335"
           fill="#013B27" opacity="0.10"/>

  <!-- Small upper-right brand lockup -->
  <circle cx="1114" cy="70" r="7" fill="#FFFFFF" opacity="0.95"/>
  <circle cx="1138" cy="70" r="7" fill="#FFFFFF" opacity="0.55"/>
  <text x="1160" y="78" width="92"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#FFFFFF" opacity="0.88"
        letter-spacing="1.4">NOVA LABS</text>

  <!-- Eyebrow text -->
  <text x="705" y="190" width="380"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#E9F8DE"
        letter-spacing="4">PRODUCT STRATEGY 2026</text>

  <!-- Minimal divider -->
  <line x1="705" y1="218" x2="805" y2="218"
        stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>

  <!-- Main title -->
  <text x="700" y="300" width="500"
        font-family="Georgia, Cambria, 'Times New Roman', serif"
        font-size="64" font-weight="700" fill="#FFFFFF">
    <tspan x="700" dy="0">New Software</tspan>
    <tspan x="700" dy="76">Development</tspan>
  </text>

  <!-- Supporting subtitle -->
  <text x="705" y="445" width="445"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#F1FFE8" opacity="0.86">
    Building scalable platforms for a faster, smarter enterprise operating model.
  </text>

  <!-- Rounded label / button -->
  <rect x="705" y="510" width="305" height="54" rx="27"
        fill="url(#pillGradient)" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="1"/>
  <text x="735" y="544" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#FFFFFF"
        letter-spacing="0.6">YOUR COMPANY NAME</text>

  <!-- Bottom metadata -->
  <text x="705" y="640" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#FFFFFF" opacity="0.62">
    Executive keynote deck  ·  Confidential draft
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the photo crop; use `<clipPath>` directly on the `<image>` instead.
- ❌ Do not apply `clip-path` to a `<g>`, `<rect>`, or `<ellipse>` expecting it to translate; for this technique, clip only the `<image>`.
- ❌ Do not rely on SVG/CSS grayscale filters for the image. Use a black-and-white source image or preprocessed photo asset.
- ❌ Do not center the oval photo fully inside the slide; the premium effect depends on the image breaking the left edge.
- ❌ Do not overcrowd the gradient side with charts or many text blocks; the right side should remain a clean title field.

## Composition notes
- Keep the slide asymmetric: roughly 35% photo area on the left and 65% gradient/text field on the right.
- Place the title in the visual center-right, not the geometric center; this preserves negative space and lets the oval image act as an anchor.
- Use a monochrome or desaturated photo so it does not compete with the saturated green gradient.
- Maintain a simple color rhythm: white typography, off-white accent line, and green gradient as the dominant brand expression.