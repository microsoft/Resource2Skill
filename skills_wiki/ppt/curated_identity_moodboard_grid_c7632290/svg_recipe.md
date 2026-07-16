# SVG Recipe — Curated Identity Moodboard Grid

## Visual mechanism
An asymmetrical set of floating brand/application cards is arranged like a curated design-tool canvas, using generous gaps, rounded image crops, bold identity tiles, and soft diffused shadows. The result feels like a premium moodboard rather than a rigid gallery: one large visual anchor plus smaller staggered mockup and logo cards.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 8× `<rect>` for floating card bases, rounded identity tiles, logo plaques, and caption chips
- 4× `<image>` for hero/product/mockup photos clipped into rounded cards
- 4× `<clipPath>` using rounded `<rect>` crops for editable rounded photo cards
- 3× `<filter>` for soft UI-card shadows and subtle photo elevation
- 2× `<linearGradient>` for premium background and card highlight fills
- 1× `<radialGradient>` for a warm ambient glow behind the moodboard
- 8× `<text>` blocks with explicit `width` attributes for title, subtitles, labels, and bold identity copy
- 7× `<path>` elements for coffee-bean/brand illustration accents and a simple logo mark
- 2× `<circle>` / `<ellipse>` elements for icon construction and small decorative dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8f6f1"/>
      <stop offset="55%" stop-color="#f2efe8"/>
      <stop offset="100%" stop-color="#eee9df"/>
    </linearGradient>

    <radialGradient id="warmGlow" cx="72%" cy="38%" r="62%">
      <stop offset="0%" stop-color="#f2c27d" stop-opacity="0.30"/>
      <stop offset="55%" stop-color="#f2c27d" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#f2c27d" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="blueTile" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5b7cff"/>
      <stop offset="100%" stop-color="#3f65e8"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softPhotoShadow" x="-18%" y="-18%" width="136%" height="145%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="tinyGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>

    <clipPath id="heroCrop">
      <rect x="58" y="142" width="424" height="504" rx="34"/>
    </clipPath>
    <clipPath id="mugCrop">
      <rect x="802" y="438" width="218" height="176" rx="28"/>
    </clipPath>
    <clipPath id="bagCrop">
      <rect x="1014" y="310" width="170" height="160" rx="26"/>
    </clipPath>
    <clipPath id="beansCrop">
      <rect x="566" y="500" width="250" height="126" rx="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmGlow)"/>

  <text x="64" y="72" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800" fill="#1d1d1f">Mr. Li’s Coffee Workshop</text>
  <text x="66" y="112" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="500" fill="#77746e">Brand identity moodboard · logo system · merchandise applications</text>

  <rect x="58" y="142" width="424" height="504" rx="34" fill="#ffffff" filter="url(#softPhotoShadow)"/>
  <image x="58" y="142" width="424" height="504" clip-path="url(#heroCrop)"
         href="https://images.example.com/coffee-workshop-hands-holding-branded-mug-no-face.jpg"/>
  <rect x="86" y="566" width="178" height="44" rx="22" fill="#ffffff" opacity="0.92"/>
  <text x="108" y="594" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#2a211b">01 / Hero mockup</text>

  <rect x="520" y="46" width="594" height="168" rx="28" fill="#fff000" filter="url(#cardShadow)"/>
  <text x="558" y="160" width="530" font-family="Segoe UI, Microsoft YaHei" font-size="96" font-weight="900" fill="#050505">全球最強</text>

  <rect x="424" y="230" width="804" height="188" rx="26" fill="url(#blueTile)" filter="url(#cardShadow)"/>
  <text x="448" y="354" width="748" font-family="Segoe UI, Microsoft YaHei" font-size="92" font-weight="900" fill="#ffffff">設計AI智能體</text>

  <rect x="502" y="468" width="410" height="138" rx="24" fill="#050505" filter="url(#cardShadow)"/>
  <text x="530" y="562" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800" fill="#ffffff">Lovart</text>
  <path d="M838 523 C852 500 881 505 888 530 C894 552 873 569 852 561 C835 555 829 538 838 523 Z" fill="#ffffff"/>
  <circle cx="862" cy="533" r="15" fill="#050505"/>

  <rect x="944" y="442" width="220" height="220" rx="24" fill="#ffffff" filter="url(#cardShadow)"/>
  <circle cx="1054" cy="552" r="94" fill="#050505"/>
  <text x="982" y="587" width="138" font-family="Segoe UI, Microsoft YaHei" font-size="74" font-weight="900" fill="#ffffff">-L°</text>

  <rect x="802" y="438" width="218" height="176" rx="28" fill="#ffffff" filter="url(#softPhotoShadow)"/>
  <image x="802" y="438" width="218" height="176" clip-path="url(#mugCrop)"
         href="https://images.example.com/ceramic-coffee-mug-with-cat-logo-mockup.jpg"/>
  <text x="818" y="638" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7a736b">Ceramic cup application</text>

  <rect x="1014" y="310" width="170" height="160" rx="26" fill="#ffffff" filter="url(#softPhotoShadow)"/>
  <image x="1014" y="310" width="170" height="160" clip-path="url(#bagCrop)"
         href="https://images.example.com/kraft-coffee-bag-minimal-logo-label.jpg"/>
  <text x="1030" y="492" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7a736b">Packaging test</text>

  <rect x="566" y="500" width="250" height="126" rx="24" fill="#ffffff" filter="url(#softPhotoShadow)"/>
  <image x="566" y="500" width="250" height="126" clip-path="url(#beansCrop)"
         href="https://images.example.com/roasted-coffee-beans-on-table-closeup.jpg"/>

  <path d="M1148 38 C1184 54 1208 84 1202 126 C1198 158 1173 186 1137 199 C1166 158 1162 111 1148 38 Z" fill="none" stroke="#4d3a2a" stroke-width="3" opacity="0.72"/>
  <path d="M1178 62 C1158 98 1154 135 1162 178" fill="none" stroke="#4d3a2a" stroke-width="2" opacity="0.72"/>
  <path d="M1190 83 C1218 66 1242 54 1268 42" fill="none" stroke="#4d3a2a" stroke-width="2" opacity="0.55"/>
  <path d="M1162 100 C1136 84 1116 70 1096 58" fill="none" stroke="#4d3a2a" stroke-width="2" opacity="0.55"/>

  <path d="M742 646 C765 617 805 619 819 650 C791 658 765 661 742 646 Z" fill="#b8743d" stroke="#4d2c19" stroke-width="2"/>
  <path d="M821 636 C850 612 889 622 895 656 C867 660 840 655 821 636 Z" fill="#c98246" stroke="#4d2c19" stroke-width="2"/>
  <path d="M706 655 C725 631 760 637 770 666 C745 672 724 670 706 655 Z" fill="#a86738" stroke="#4d2c19" stroke-width="2"/>
  <ellipse cx="1182" cy="616" rx="6" ry="4" fill="#5b3a23" filter="url(#tinyGlow)"/>
  <ellipse cx="1218" cy="642" rx="8" ry="5" fill="#5b3a23"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the gallery as a rigid equal-size table; the technique depends on staggered masonry placement and visual hierarchy.
- ❌ Do not apply `clip-path` to regular `<rect>` or `<path>` card shapes; use it only on `<image>` elements for reliable PPT translation.
- ❌ Do not use SVG masks for photo fades or logo cutouts; use rounded image clipping, gradients, and editable paths instead.
- ❌ Do not overuse heavy black shadows; keep the shadows broad, soft, and low-contrast so the cards feel like floating UI panels.
- ❌ Do not leave image placeholders unstyled; every image should sit on a rounded white base or have a deliberate crop and shadow.

## Composition notes
- Anchor the slide with one large hero mockup on the left or center-left, occupying roughly one-third of the canvas.
- Cluster smaller identity tiles and application mockups on the right in a staggered stack, with 18–36 px of breathing room between cards.
- Use a restrained neutral background, then let one or two saturated brand-color cards provide the main rhythm.
- Keep captions tiny and understated; the primary drama should come from the floating cards, bold logo/type tiles, and polished product imagery.