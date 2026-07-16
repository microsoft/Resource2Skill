# SVG Recipe — Seamless Gradient Image Blend (全屏渐变蒙版融合排版)

## Visual mechanism
A full-bleed photo is placed edge-to-edge, then covered by a left-to-right transparent gradient overlay sampled from the photo’s dark tones, dissolving the image into a clean solid text zone. Large stacked typography sits in the opaque region while the subject remains visible on the right, creating a cinematic poster composition without hard image borders.

## SVG primitives needed
- 1× `<rect>` for the base dark cinematic background
- 1× `<image>` for the full-screen hero photo, positioned so the subject is on the right
- 2× `<linearGradient>` for the main horizontal blend and subtle top/bottom vignette
- 1× `<radialGradient>` for a soft focus glow behind the subject
- 3× `<rect>` overlays for the seamless gradient mask, vignette, and contrast wash
- 4× `<path>` for organic ink-like shadow shapes that help hide photo edges
- 1× `<filter id="softShadow">` applied to text for premium depth
- 1× `<filter id="goldGlow">` applied to accent text
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, and poster-style emphasis
- Nested `<tspan>` elements for line breaks and inline hierarchy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blendLeftToRight" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#11191F" stop-opacity="1"/>
      <stop offset="38%" stop-color="#11191F" stop-opacity="0.98"/>
      <stop offset="58%" stop-color="#11191F" stop-opacity="0.62"/>
      <stop offset="76%" stop-color="#11191F" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#11191F" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="verticalVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#05080B" stop-opacity="0.58"/>
      <stop offset="20%" stop-color="#05080B" stop-opacity="0"/>
      <stop offset="76%" stop-color="#05080B" stop-opacity="0"/>
      <stop offset="100%" stop-color="#05080B" stop-opacity="0.62"/>
    </linearGradient>

    <radialGradient id="subjectGlow" cx="73%" cy="44%" r="48%">
      <stop offset="0%" stop-color="#D7C4A1" stop-opacity="0.24"/>
      <stop offset="44%" stop-color="#344B54" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#05080B" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="5" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="150%">
      <feGaussianBlur stdDeviation="2.8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#11191F"/>

  <image
    x="0" y="0" width="1280" height="720"
    href="https://images.example.com/cinematic-wuxia-back-view-sword-hero-no-face.jpg"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#subjectGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#blendLeftToRight)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#verticalVignette)"/>

  <path d="M0,0 C142,20 226,90 315,170 C386,235 455,274 560,292 C438,338 337,330 244,298 C140,262 62,203 0,142 Z"
        fill="#0A1117" opacity="0.46"/>
  <path d="M0,720 C162,675 246,612 327,548 C420,475 510,450 610,470 C506,548 444,619 362,720 Z"
        fill="#071016" opacity="0.52"/>
  <path d="M468,0 C535,82 565,163 560,246 C552,362 490,428 405,474 C470,354 454,230 390,121 C360,70 330,32 300,0 Z"
        fill="#17242C" opacity="0.28"/>
  <path d="M888,0 C970,132 1018,283 1010,420 C1006,496 984,598 930,720 L1280,720 L1280,0 Z"
        fill="#05070A" opacity="0.18"/>

  <text x="78" y="132" width="420"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="34" font-weight="700" letter-spacing="5"
        fill="#D6B463" opacity="0.95" filter="url(#goldGlow)">
    武侠人物档案
  </text>

  <text x="76" y="236" width="640"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="88" font-weight="900"
        fill="#FFFFFF" filter="url(#softShadow)">
    这张PPT
  </text>

  <text x="78" y="294" width="530"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="4"
        fill="#AEB9BD">
    SEAMLESS GRADIENT IMAGE BLEND
  </text>

  <line x1="80" y1="326" x2="445" y2="326" stroke="#D6B463" stroke-width="3" opacity="0.88"/>
  <line x1="80" y1="340" x2="255" y2="340" stroke="#D6B463" stroke-width="1.5" opacity="0.42"/>

  <text x="78" y="456" width="820"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="96" font-weight="900"
        fill="#F4C56B" stroke="#102C48" stroke-width="8"
        paint-order="stroke fill"
        filter="url(#softShadow)">
    真养眼啊！
  </text>

  <text x="84" y="530" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#E7ECEF" opacity="0.92">
    <tspan x="84" dy="0">Use a dark gradient overlay instead of a hard crop.</tspan>
    <tspan x="84" dy="34">The left side becomes clean negative space,</tspan>
    <tspan x="84" dy="34">while the image breathes naturally on the right.</tspan>
  </text>

  <text x="84" y="654" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3"
        fill="#D6B463" opacity="0.85">
    FULL-BLEED PHOTO · ALPHA GRADIENT · CINEMATIC TYPE
  </text>

  <rect x="0" y="0" width="1280" height="6" fill="#071016" opacity="0.85"/>
  <rect x="0" y="714" width="1280" height="6" fill="#071016" opacity="0.85"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the blend; PPT translation may fail or ignore it. Use a semi-transparent gradient `<rect>` overlay instead.
- ❌ Do not paste the photo as a smaller rectangle with visible borders; the technique depends on a full-screen image with dissolved edges.
- ❌ Do not place dense text over the transparent/right side of the gradient where the photo remains high-detail.
- ❌ Do not use pure black-to-transparent if the image edge is blue, green, or brown; sample a nearby dark dominant color for the overlay.
- ❌ Do not rely on `clip-path` for non-image shapes; keep the blend as normal editable gradient rectangles.

## Composition notes
- Keep the left 38–45% nearly solid for typography; let the fade zone run through the middle third so the transition is invisible.
- Position the photo subject on the right third, leaving enough negative space on the left for oversized title text.
- Use a restrained palette: dark slate background, white primary type, and one warm gold accent to echo cinematic poster design.
- Add subtle top/bottom vignettes and organic dark paths to hide busy image edges and make the slide feel immersive.