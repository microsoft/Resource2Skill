# SVG Recipe — Pop-Art Duotone Aesthetic

## Visual mechanism
A high-contrast photo is reduced into a hot-pink/navy duotone field, then paired with stark white space and chunky editorial typography. The effect feels like a pop-art poster: flattened color, oversized cropped imagery, and bold translucent magenta blocks that unify the composition.

## SVG primitives needed
- 2× `<image>` for the duotone background texture and the cropped phone-screen photo
- 2× `<clipPath>` for angled full-bleed image cropping and rounded phone-screen cropping
- 7× `<rect>` for white panel, translucent color blocks, phone body, screen frame, logo mark, and small UI accents
- 4× `<path>` for angled white separator, phone highlight edge, logo swirl, and abstract decorative slashes
- 2× `<circle>` for phone home button details
- 4× `<linearGradient>` for duotone overlay, magenta block depth, phone metal edge, and soft background vignette
- 2× `<filter>` using blur/offset for phone shadow and soft card shadow
- 5× `<text>` with explicit `width` for logo, headline, footer, and small pop-art labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="duoWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff4bd2" stop-opacity="0.92"/>
      <stop offset="48%" stop-color="#f60083" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#25048f" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="blockGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f44ccc"/>
      <stop offset="55%" stop-color="#ba159f"/>
      <stop offset="100%" stop-color="#3b008f"/>
    </linearGradient>
    <linearGradient id="phoneMetal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="44%" stop-color="#f2f2f4"/>
      <stop offset="68%" stop-color="#bfc1c8"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <linearGradient id="whiteVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.35"/>
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <filter id="phoneShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="18" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="10" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="leftAngledCrop">
      <path d="M0,0 L765,0 L520,720 L0,720 Z"/>
    </clipPath>
    <clipPath id="phoneScreenClip">
      <rect x="360" y="58" width="372" height="520" rx="10" ry="10"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <image href="https://images.example.com/duotone-high-contrast-concert-texture-magenta-navy.jpg"
         x="-80" y="-40" width="850" height="820" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#leftAngledCrop)"/>
  <rect x="0" y="0" width="760" height="720" fill="url(#duoWash)" opacity="0.86"/>

  <path d="M648,-40 L795,-40 L540,760 L393,760 Z" fill="#ffffff" opacity="0.96" filter="url(#softShadow)"/>
  <path d="M686,-30 L734,-30 L478,750 L430,750 Z" fill="#eeeeef" opacity="0.55"/>

  <g transform="rotate(16 505 285)" filter="url(#phoneShadow)">
    <rect x="300" y="-58" width="470" height="700" rx="48" ry="48" fill="url(#phoneMetal)" stroke="#d4d4d8" stroke-width="6"/>
    <rect x="332" y="20" width="406" height="590" rx="22" ry="22" fill="#1c1230"/>
    <image href="https://images.example.com/preprocessed-duotone-portrait-or-fashion-shot-hot-pink-navy.png"
           x="332" y="20" width="406" height="590" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#phoneScreenClip)"/>
    <rect x="332" y="20" width="406" height="590" rx="22" ry="22" fill="url(#duoWash)" opacity="0.36"/>
    <rect x="456" y="-18" width="164" height="16" rx="8" fill="#d8d8dc"/>
    <circle cx="535" cy="610" r="34" fill="#f7f7f8" stroke="#c5c6cc" stroke-width="4"/>
    <circle cx="535" cy="610" r="26" fill="none" stroke="#9d9ea5" stroke-width="2"/>
    <path d="M758,40 C772,190 714,394 650,575" fill="none" stroke="#ffffff" stroke-width="6" opacity="0.8"/>
  </g>

  <rect x="0" y="76" width="445" height="344" fill="#f04bc9" opacity="0.88"/>
  <rect x="444" y="78" width="224" height="198" fill="#a90093" opacity="0.92"/>
  <rect x="0" y="300" width="445" height="120" fill="url(#blockGrad)" opacity="0.76"/>
  <path d="M24,635 C120,592 170,616 245,563 C315,513 382,518 466,482" fill="none" stroke="#ff42cf" stroke-width="26" opacity="0.42"/>
  <path d="M70,38 C185,18 260,42 344,12" fill="none" stroke="#6a1bd8" stroke-width="20" opacity="0.26"/>

  <rect x="735" y="0" width="545" height="720" fill="url(#whiteVignette)"/>
  <rect x="1080" y="56" width="38" height="38" rx="8" fill="#ffd400"/>
  <path d="M1089,75 C1089,63 1097,58 1108,58 C1120,58 1128,67 1128,79 C1128,91 1119,100 1106,100 C1096,100 1089,91 1089,75 Z
           M1098,77 C1098,86 1103,92 1110,92 C1117,92 1122,86 1122,78 C1122,69 1116,64 1109,64 C1102,64 1098,69 1098,77 Z"
        fill="#ffffff" opacity="0.95"/>
  <text x="1128" y="91" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="800" fill="#565158">Over</text>

  <text x="835" y="350" width="365" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800" fill="#948b91" text-anchor="middle">
    How to create a
  </text>
  <text x="835" y="408" width="365" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800" fill="#948b91" text-anchor="middle">
    duotone look
  </text>
  <text x="1028" y="665" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="500" fill="#575257">madewithOver.com</text>

  <text x="36" y="138" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#ffffff" opacity="0.38" letter-spacing="3">POP / DUOTONE</text>
  <text x="462" y="145" width="185" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#ffffff" opacity="0.34" letter-spacing="2">HOT PINK</text>
</svg>
```

## Avoid in this skill
- ❌ Relying on SVG color-matrix filters for true duotone remapping; preprocess the image or use a pre-duotoned asset because PowerPoint translation may not preserve advanced image filters.
- ❌ Applying `clip-path` to groups or rectangles for the angled crop; clip only the `<image>` and use editable paths/rectangles above it.
- ❌ Using blend modes, masks, or CSS `mix-blend-mode`; simulate the look with translucent magenta/navy overlays and gradients.
- ❌ Letting detailed multicolor photography compete with text; the photo should be high-contrast and visually flattened before placement.

## Composition notes
- Keep the duotone image dominant on the left 55–60% of the slide, with a clean white reading zone on the right.
- Use a diagonal white separator to make the composition feel kinetic and poster-like rather than a simple split screen.
- Add large translucent magenta blocks over the image to reinforce the two-color palette and hide distracting photo detail.
- Pair the active background with heavy, rounded, neutral typography in gray or white; avoid thin type over the duotone field.