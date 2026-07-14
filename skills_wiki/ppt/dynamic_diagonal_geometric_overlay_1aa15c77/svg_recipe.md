# SVG Recipe — Dynamic Diagonal Geometric Overlay

## Visual mechanism
A full-bleed photographic background is partially covered by large, semi-transparent diagonal geometric planes anchored to one corner. The layered navy/teal/light-blue shapes create a high-contrast editorial canvas for bold text and data while preserving motion and photographic context.

## SVG primitives needed
- 1× `<image>` for the full-bleed contextual hero photo
- 1× `<rect>` for a subtle global darkening tint over the photo
- 5× `<path>` for layered diagonal triangle/trapezoid overlays
- 1× `<linearGradient>` for the main dark overlay depth
- 2× `<linearGradient>` for accent geometric planes
- 1× `<filter id="softShadow">` applied to the main text panel/accent card
- 2× `<text>` blocks for headline and subtitle, each with explicit `width`
- 1× `<text>` block for the large metric, with nested `<tspan>` styling and explicit `width`
- 3× `<rect>` for small editable data bars inside the overlay
- 4× `<line>` elements for fine diagonal motion accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyPlane" x1="0" y1="720" x2="760" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.96"/>
      <stop offset="58%" stop-color="#22313f" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#22313f" stop-opacity="0.58"/>
    </linearGradient>

    <linearGradient id="tealPlane" x1="0" y1="720" x2="640" y2="330" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00a896" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="#00d4b8" stop-opacity="0.64"/>
    </linearGradient>

    <linearGradient id="bluePlane" x1="0" y1="720" x2="420" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7bc0e3" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.30"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed background photo -->
  <image href="https://images.example.com/hero-photo-modern-office-strategy-team.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Global photo toning so the overlays feel integrated -->
  <rect x="0" y="0" width="1280" height="720" fill="#0f172a" opacity="0.24"/>

  <!-- Fine diagonal motion accents in the open photo area -->
  <line x1="845" y1="42" x2="1190" y2="278" stroke="#ffffff" stroke-width="2" opacity="0.18"/>
  <line x1="895" y1="74" x2="1240" y2="310" stroke="#7bc0e3" stroke-width="3" opacity="0.22"/>
  <line x1="965" y1="560" x2="1230" y2="720" stroke="#ffffff" stroke-width="2" opacity="0.15"/>
  <line x1="1012" y1="522" x2="1280" y2="684" stroke="#00d4b8" stroke-width="3" opacity="0.18"/>

  <!-- Main layered diagonal overlay stack, anchored bottom-left -->
  <path d="M 0 58 L 888 720 L 0 720 Z"
        fill="url(#navyPlane)" filter="url(#softShadow)"/>

  <path d="M 0 310 L 720 720 L 0 720 Z"
        fill="url(#tealPlane)" opacity="0.92"/>

  <path d="M 0 518 L 430 720 L 0 720 Z"
        fill="url(#bluePlane)" opacity="0.86"/>

  <!-- Thin translucent architectural facets for depth -->
  <path d="M 0 186 L 198 330 L 0 428 Z"
        fill="#ffffff" opacity="0.10"/>

  <path d="M 506 690 L 910 720 L 728 585 Z"
        fill="#00a896" opacity="0.20"/>

  <!-- Text hierarchy placed where the dark overlay is thickest -->
  <text x="82" y="336" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3"
        fill="#7bc0e3">
    MARKET ENTRY PLAN
  </text>

  <text x="80" y="410" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800"
        fill="#ffffff">
    <tspan x="80" dy="0">Product Launch</tspan>
    <tspan x="80" dy="62">Go-To-Market Strategy</tspan>
  </text>

  <text x="84" y="546" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#dbeafe" opacity="0.95">
    A focused roadmap for accelerating awareness, adoption, and first-quarter revenue impact.
  </text>

  <!-- Big metric/data callout integrated into the diagonal overlay -->
  <text x="82" y="642" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        fill="#ffffff">
    <tspan font-size="58" font-weight="800">87</tspan>
    <tspan font-size="28" font-weight="700">%</tspan>
    <tspan x="84" dy="28" font-size="15" font-weight="600" fill="#bfdbfe" letter-spacing="1.2">LAUNCH READINESS</tspan>
  </text>

  <rect x="342" y="607" width="210" height="10" rx="5" fill="#ffffff" opacity="0.20"/>
  <rect x="342" y="607" width="176" height="10" rx="5" fill="#ffffff" opacity="0.86"/>
  <rect x="342" y="635" width="132" height="8" rx="4" fill="#7bc0e3" opacity="0.80"/>
</svg>
```

## Avoid in this skill
- ❌ Using a plain rectangular black overlay; the diagonal geometry is the whole premium visual mechanism.
- ❌ `<mask>` or `mask="url(...)"` to reveal the photo through the planes; use semi-transparent editable `<path>` shapes instead.
- ❌ `<polygon>` for the overlay planes if your translator only guarantees editable `<path>` support; write triangles/trapezoids as `d="M ... L ... Z"`.
- ❌ Applying filters to `<line>` motion accents; filters on lines may be dropped.
- ❌ Making the overlay too transparent over a busy photo; keep the main navy plane around 0.8–0.95 opacity where text sits.

## Composition notes
- Anchor the largest dark plane to the bottom-left or top-right and let its diagonal edge cut across roughly 45–55% of the slide.
- Place title, subtitle, and metric inside the thickest/darkest part of the overlay; keep the opposite side mostly photographic negative space.
- Use a corporate triad: dark navy for readability, teal for brand energy, and pale blue/white for secondary facets.
- Let small lines or facets echo the main diagonal angle so the slide feels intentional rather than simply “text on a photo.”