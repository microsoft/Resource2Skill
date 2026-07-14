# SVG Recipe — Architectural Minimalist Chapter Title

## Visual mechanism
A full-bleed architectural/workshop photo is darkened with layered charcoal overlays and a subtle bottom gradient, then interrupted by oversized all-caps white typography. The premium feel comes from extreme scale contrast: a massive compressed title stack, a smaller technical subtitle, and a tiny geometric drafting accent.

## SVG primitives needed
- 1× `<image>` for the full-bleed architectural studio / blueprint background, preferably without visible faces
- 2× full-slide `<rect>` overlays for uniform dimming and bottom readability gradient
- 1× `<radialGradient>` vignette fill to darken slide edges
- 1× `<linearGradient>` bottom shadow fill for anchoring white typography
- 1× `<filter id="textShadow">` applied to large text for subtle cinematic separation
- 5× `<text>` elements for chapter code, subtitle, and massive title lines
- 4× small `<rect>` elements for rigid architectural accent rules and layout calibration marks
- Optional 3× faint `<line>` elements for blueprint-like structural rhythm

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bottomFade" x1="0" y1="300" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0f1114" stop-opacity="0"/>
      <stop offset="0.45" stop-color="#0f1114" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#0f1114" stop-opacity="0.76"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="50%" r="72%">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="0.62" stop-color="#000000" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.58"/>
    </radialGradient>

    <filter id="textShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softPhotoShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed contextual image: use a face-free architectural desk / blueprint / materials photo -->
  <image
    href="https://images.example.com/architecture-studio-blueprints-desk-hands-no-face.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Dark cinematic treatment -->
  <rect x="0" y="0" width="1280" height="720" fill="#0f1114" opacity="0.48"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomFade)"/>

  <!-- Subtle architectural guide geometry -->
  <line x1="98" y1="122" x2="1182" y2="122" stroke="#ffffff" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="98" y1="596" x2="1182" y2="596" stroke="#ffffff" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="100" y1="122" x2="100" y2="596" stroke="#ffffff" stroke-opacity="0.10" stroke-width="1"/>
  <rect x="100" y="108" width="54" height="4" fill="#ffffff" opacity="0.9"/>
  <rect x="100" y="130" width="18" height="18" fill="none" stroke="#ffffff" stroke-opacity="0.42" stroke-width="2"/>
  <rect x="123" y="130" width="18" height="18" fill="none" stroke="#ffffff" stroke-opacity="0.20" stroke-width="2"/>

  <!-- Small technical chapter label -->
  <text x="100" y="184" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        letter-spacing="4"
        fill="#d5d5d5" opacity="0.88">
    C H A P T E R&nbsp;&nbsp; 0 2
  </text>

  <text x="100" y="210" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600"
        letter-spacing="3"
        fill="#b9b9b9" opacity="0.72">
    S T R A T E G I C&nbsp;&nbsp; B R I E F I N G
  </text>

  <!-- Massive title block, weighted to the lower right like an editorial cover -->
  <text x="438" y="452" width="790"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800"
        letter-spacing="-4"
        fill="#ffffff"
        filter="url(#textShadow)">
    ARCHITECTURE
  </text>

  <text x="228" y="528" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="800"
        letter-spacing="-1"
        fill="#ffffff"
        filter="url(#textShadow)">
    PROCESS, PREP + ADVICE
  </text>

  <text x="862" y="552" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800"
        letter-spacing="-4"
        fill="#ffffff"
        filter="url(#textShadow)">
    CLIENT
  </text>

  <text x="442" y="653" width="790"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800"
        letter-spacing="-4"
        fill="#ffffff"
        filter="url(#textShadow)">
    PRESENTATION
  </text>

  <!-- Drafting-rule accent below the title block -->
  <rect x="442" y="674" width="188" height="5" fill="#ffffff" opacity="0.92"/>
  <rect x="640" y="674" width="46" height="5" fill="#ffffff" opacity="0.35"/>
</svg>
```

## Avoid in this skill
- ❌ Reproducing or emphasizing visible faces in the background photo; choose face-free architecture imagery, crop to hands/materials, or use a blurred/abstract workspace image
- ❌ Thin white text over an undimmed photo; the dark overlay and bottom gradient are essential for legibility
- ❌ Centered title layouts with equal margins; this style depends on strong asymmetric editorial weighting
- ❌ Decorative icons, rounded cards, or dashboard components that weaken the architectural minimalism
- ❌ Using `<mask>` or clipping non-image elements for the vignette; use gradient-filled rectangles instead

## Composition notes
- Keep the photo full-bleed, but suppress it until it reads as texture rather than content.
- Place the main title in the lower half, oversized enough that it nearly touches the right edge.
- Use one small left-side axis for chapter metadata and accent rules; this creates the “architectural drawing” discipline.
- Maintain a monochrome rhythm: white primary text, muted grey labels, charcoal overlays, and minimal accent geometry.