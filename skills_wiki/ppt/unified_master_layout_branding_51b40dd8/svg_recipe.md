# SVG Recipe — Unified Master Layout Branding

## Visual mechanism
A unified slide master creates a consistent branded wrapper: one modern font system, fixed logo placement, reusable footer metadata, and layout-specific hero assets reserved for title slides. The slide feels like an editable corporate template rather than a one-off design because the brand elements stay anchored while content changes inside predictable zones.

## SVG primitives needed
- 5× `<rect>` for background wash, master preview cards, footer fields, and the fixed logo badge
- 3× `<circle>` for PowerPoint-style brand icon geometry and decorative accent dots
- 4× `<path>` for the PowerPoint “P” tile, pie-disc overlay, subtle wave accent, and logo cookie/brand mark
- 1× `<image>` for a title-slide-only presenter/brand photo cropped on the right side
- 1× `<clipPath>` with a rounded `<rect>` applied to the hero image
- 1× `<linearGradient>` for the warm brand accent fill
- 1× `<radialGradient>` for the soft neutral slide background
- 1× `<filter id="softShadow">` applied to preview cards and brand marks
- 1× `<filter id="logoShadow">` applied to the fixed logo badge
- Multiple `<text>` elements using Segoe UI with explicit `width` attributes for all editable typography
- 4× `<line>` for master-layout divider rules and preview placeholders

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="paperGlow" cx="48%" cy="42%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="68%" stop-color="#f2f2f0"/>
      <stop offset="100%" stop-color="#dededb"/>
    </radialGradient>

    <linearGradient id="brandOrange" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff8a5c"/>
      <stop offset="52%" stop-color="#e45a2f"/>
      <stop offset="100%" stop-color="#b93418"/>
    </linearGradient>

    <linearGradient id="footerFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f7f7f7"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="logoShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="presenterCrop">
      <rect x="720" y="0" width="560" height="720" rx="0" ry="0"/>
    </clipPath>
  </defs>

  <!-- Master background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paperGlow)"/>
  <path d="M0,625 C220,580 360,655 560,620 C765,584 920,530 1280,592 L1280,720 L0,720 Z"
        fill="#ffffff" opacity="0.42"/>

  <!-- Layout-specific title-slide photo asset, excluded from content slides -->
  <image href="https://images.example.com/corporate-presenter-red-shirt-gesture-cropped-no-face.png"
         x="660" y="-18" width="670" height="760"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#presenterCrop)"
         opacity="0.96"/>

  <!-- Main title typography: master-controlled font -->
  <text x="36" y="138" width="710"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="700" fill="#000000" letter-spacing="-4">
    Slide Master
  </text>
  <text x="36" y="292" width="600"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="700" fill="#000000" letter-spacing="-3">
    Tutorial
  </text>

  <!-- Editable slide-master preview block -->
  <rect x="36" y="343" width="505" height="280" fill="#ffffff" stroke="#d9d9d9" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="36" y="343" width="505" height="64" fill="#ffffff" stroke="#d9d9d9" stroke-width="1"/>
  <text x="40" y="383" width="475"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="400" fill="#252525">
    Click to edit Master title style
  </text>

  <line x1="36" y1="409" x2="541" y2="409" stroke="#e3e3e3" stroke-width="1"/>
  <text x="39" y="430" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#111111">
    • Click to edit Master text styles
  </text>
  <text x="72" y="449" width="315"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#111111">
    • Second level
  </text>
  <text x="94" y="464" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#111111">
    • Third level
  </text>
  <text x="114" y="480" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9.5" fill="#111111">
    • Fourth level
  </text>
  <text x="140" y="494" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="8" fill="#111111">
    • Fifth level
  </text>

  <!-- PowerPoint-like brand training visual over the preview -->
  <circle cx="545" cy="484" r="122" fill="url(#brandOrange)" opacity="0.84"/>
  <path d="M545,484 L665,484 A122,122 0 0 1 421,484 Z" fill="#c63a18" opacity="0.55"/>
  <rect x="385" y="414" width="146" height="140" rx="10" fill="#c9391a" filter="url(#softShadow)"/>
  <rect x="396" y="406" width="126" height="146" rx="9" fill="#cf3d1c"/>
  <text x="416" y="526" width="95"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800" fill="#ffffff">
    P
  </text>

  <!-- Footer system: appears in same place on every slide -->
  <rect x="36" y="631" width="132" height="19" fill="url(#footerFade)" stroke="#d8d8d8" stroke-width="1"/>
  <rect x="189" y="631" width="199" height="19" fill="url(#footerFade)" stroke="#d8d8d8" stroke-width="1"/>
  <rect x="408" y="631" width="132" height="19" fill="url(#footerFade)" stroke="#d8d8d8" stroke-width="1"/>
  <text x="39" y="645" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="7.5" fill="#8a8a8a">
    9/2/2019
  </text>
  <text x="278" y="645" width="60"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="7.5" fill="#8a8a8a" text-anchor="middle">
    Footer
  </text>
  <text x="525" y="645" width="12"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="7.5" fill="#8a8a8a" text-anchor="end">
    18
  </text>

  <!-- Persistent anchored logo badge: bottom-right master branding -->
  <rect x="1040" y="624" width="202" height="58" rx="14" fill="#fff6eb" stroke="#d2691e" stroke-width="3" filter="url(#logoShadow)"/>
  <circle cx="1072" cy="653" r="22" fill="#d2691e"/>
  <circle cx="1064" cy="647" r="4" fill="#6d3410"/>
  <circle cx="1082" cy="657" r="4.2" fill="#6d3410"/>
  <circle cx="1070" cy="664" r="3.3" fill="#6d3410"/>
  <text x="1105" y="659" width="115"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#1f1f1f">
    BRAND LOGO
  </text>
  <text x="1042" y="699" width="198"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="10" fill="#777777" text-anchor="middle">
    fixed master position on every layout
  </text>
</svg>
```

## Avoid in this skill
- ❌ Letting logo position “float” per slide; it should use one fixed coordinate system, usually bottom-right.
- ❌ Mixing serif default fonts with modern sans-serif brand fonts; enforce one deck-wide type family.
- ❌ Placing title-slide-only assets, such as presenter photos, on every content slide.
- ❌ Using `<mask>` for photo fades or brand overlays; use clipped `<image>` crops, gradients, and editable shapes instead.
- ❌ Applying `clip-path` to text or shapes; in this workflow clipping should be reserved for images.

## Composition notes
- Keep the main content zone clear: title and body content should own the left two-thirds, while branded imagery may occupy the right edge on title layouts only.
- Anchor the logo in the same bottom-right position across all slide types, sized around 10–15% of slide width.
- Use neutral backgrounds with one restrained brand accent so the deck feels governed by a master system, not individually decorated.
- Footer fields, divider lines, and typography should be intentionally quiet; they support continuity without competing with slide content.