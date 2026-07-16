# SVG Recipe — Proportional Shape Picture Fill

## Visual mechanism
Place an `<image>` behind a vector-shaped clipping window and set `preserveAspectRatio="xMidYMid slice"` so the photo covers the shape without stretching. Add a matching editable outline shape on top to make the masked image feel like a deliberate PowerPoint picture-fill object.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× `<linearGradient>` for the premium dark backdrop, card fill, and accent strokes
- 1× `<radialGradient>` for a soft ambient glow
- 2× `<filter>` definitions: one soft shadow for cards/shapes, one blur glow for background accents
- 4× `<clipPath>` definitions: circle portrait crop, rounded-rectangle crop, hexagon crop, organic blob crop
- 4× `<image>` elements clipped to those shapes, each using `preserveAspectRatio="xMidYMid slice"`
- 4× matching outline shapes (`<circle>`, `<rect>`, `<path>`) layered above the clipped images
- 4× translucent `<rect>` card panels behind each picture-fill example
- Multiple `<text>` elements with explicit `width` attributes for title, labels, and explanatory callouts
- 3× decorative `<circle>`/`<path>` elements for depth, color rhythm, and keynote-style polish

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="55%" stop-color="#101B2E"/>
      <stop offset="100%" stop-color="#182A45"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="accentStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6EE7F9"/>
      <stop offset="50%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#FDE68A"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#55D6FF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#55D6FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <clipPath id="portraitCircle">
      <circle cx="228" cy="354" r="118"/>
    </clipPath>

    <clipPath id="roundedFeature">
      <rect x="398" y="236" width="260" height="236" rx="42"/>
    </clipPath>

    <clipPath id="hexCrop">
      <path d="M840 228 L948 290 L948 414 L840 476 L732 414 L732 290 Z"/>
    </clipPath>

    <clipPath id="organicBlob">
      <path d="M1056 233 C1126 221 1190 272 1198 344 C1206 418 1156 471 1083 482 C1004 494 946 451 940 374 C934 299 982 244 1056 233 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1090" cy="122" r="230" fill="url(#ambientGlow)" filter="url(#blurGlow)"/>
  <circle cx="84" cy="650" r="190" fill="#A78BFA" opacity="0.13" filter="url(#blurGlow)"/>
  <path d="M885 98 C972 52 1100 64 1171 141" fill="none" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2" stroke-dasharray="10 12"/>

  <text x="72" y="78" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">
    Proportional Shape Picture Fill
  </text>
  <text x="74" y="122" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#BFD0E8">
    Photos are clipped into editable vector silhouettes while preserving their natural aspect ratio — no squeezed faces, no distorted products.
  </text>

  <rect x="80" y="190" width="296" height="372" rx="34" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.12" filter="url(#shadow)"/>
  <rect x="382" y="190" width="292" height="372" rx="34" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.12" filter="url(#shadow)"/>
  <rect x="694" y="190" width="292" height="372" rx="34" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.12" filter="url(#shadow)"/>
  <rect x="1000" y="190" width="214" height="372" rx="34" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.12" filter="url(#shadow)"/>

  <image x="110" y="236" width="236" height="236"
         href="https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=900"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#portraitCircle)"/>
  <circle cx="228" cy="354" r="118" fill="none" stroke="url(#accentStroke)" stroke-width="6"/>
  <circle cx="228" cy="354" r="128" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.5"/>

  <image x="398" y="236" width="260" height="236"
         href="https://images.unsplash.com/photo-1518005020951-eccb494ad742?w=1000"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#roundedFeature)"/>
  <rect x="398" y="236" width="260" height="236" rx="42" fill="none" stroke="url(#accentStroke)" stroke-width="6"/>
  <rect x="410" y="248" width="236" height="212" rx="32" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.5"/>

  <image x="722" y="220" width="236" height="264"
         href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1000"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#hexCrop)"/>
  <path d="M840 228 L948 290 L948 414 L840 476 L732 414 L732 290 Z" fill="none" stroke="url(#accentStroke)" stroke-width="6"/>
  <path d="M840 246 L932 299 L932 405 L840 458 L748 405 L748 299 Z" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.5"/>

  <image x="930" y="218" width="280" height="276"
         href="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1000"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#organicBlob)"/>
  <path d="M1056 233 C1126 221 1190 272 1198 344 C1206 418 1156 471 1083 482 C1004 494 946 451 940 374 C934 299 982 244 1056 233 Z"
        fill="none" stroke="url(#accentStroke)" stroke-width="6"/>
  <path d="M1058 252 C1118 243 1173 286 1179 348 C1186 407 1144 449 1081 460 C1016 471 963 435 958 372 C953 310 996 262 1058 252 Z"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.5"/>

  <text x="120" y="604" width="216" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Circle portrait</text>
  <text x="120" y="632" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#BFD0E8">Ideal for leaders, authors, and org charts.</text>

  <text x="414" y="604" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Rounded feature</text>
  <text x="414" y="632" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#BFD0E8">A photo card that still behaves like a shape.</text>

  <text x="730" y="604" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Hexagon crop</text>
  <text x="730" y="632" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#BFD0E8">Useful for data, portfolio, and ecosystem slides.</text>

  <text x="1026" y="604" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Blob mask</text>
  <text x="1026" y="632" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#BFD0E8">Organic crop for human-centered stories.</text>

  <rect x="72" y="668" width="1136" height="1" fill="#FFFFFF" opacity="0.15"/>
  <text x="78" y="694" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8EA4C4">
    Implementation key: same image box as the target shape + clip-path + preserveAspectRatio=&quot;xMidYMid slice&quot;.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<rect>`, `<circle>`, or `<path>` instead of directly to the `<image>`; non-image clipping is not reliably translated.
- ❌ Using `<pattern>` image fills to simulate a picture fill; pattern fills are dropped by the translator.
- ❌ Stretching images with `preserveAspectRatio="none"`; this defeats the entire proportional-fill technique.
- ❌ Using `<mask>` for the crop shape; masks are a hard-fail pattern in this workflow.
- ❌ Relying on a single flattened screenshot of the entire composition; keep the photo, outline, and labels separately editable.

## Composition notes
- Keep each image’s SVG `x/y/width/height` aligned to the intended clipping shape’s bounding box; then use `preserveAspectRatio="xMidYMid slice"` to mimic PowerPoint’s non-distorted cover crop.
- Add a duplicate outline shape above the clipped image so the crop reads as a premium designed object and remains visually editable.
- Use generous spacing around photo-fill shapes; the technique looks best when each masked photo has breathing room and a clear label.
- For executive slides, pair the photo crops with restrained gradients, thin accent strokes, and soft shadows rather than heavy borders.