# SVG Recipe — Typographic Profile Lockup

## Visual mechanism
A magazine-style profile layout built from a hard right-aligned text edge: a huge colorful display name, a crisp biography block, and a vertical stacked uppercase subtitle that acts like a typographic divider. A large editorial portrait on the left balances the dense typography on the right, creating a premium asymmetrical introduction slide.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<linearGradient>` for a soft portrait-card backing fill
- 1× `<filter id="cardShadow">` for the portrait card shadow
- 1× `<clipPath>` with rounded `<rect>` for cropping the portrait image
- 1× `<image>` for the profile portrait
- 2× `<path>` for organic editorial accent blobs behind and near the portrait
- 2× `<rect>` for subtle vertical alignment rules / divider accents
- 1× `<text>` for the giant CJK display name
- 1× `<text>` with multiple `<tspan>` elements for the right-aligned biography
- 8× `<text>` for stacked vertical English/Pinyin letters
- 3× `<text>` for small metadata labels and section captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="portraitCardGrad" x1="190" y1="80" x2="510" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#fff4ef"/>
      <stop offset="0.55" stop-color="#f4f1f7"/>
      <stop offset="1" stop-color="#e8edf7"/>
    </linearGradient>

    <linearGradient id="coralFade" x1="95" y1="120" x2="450" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#EB4D4B" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#EB4D4B" stop-opacity="0.02"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.10  0 0 0 0 0.10  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitClip">
      <rect x="170" y="92" width="365" height="536" rx="38" ry="38"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <path d="M98,191 C124,91 263,45 374,92 C474,135 522,229 492,323 C461,422 363,480 250,451 C136,421 66,307 98,191 Z"
        fill="url(#coralFade)"/>
  <path d="M50,590 C138,526 213,548 272,604 C319,648 408,654 477,612 C430,701 266,733 154,697 C98,679 64,643 50,590 Z"
        fill="#F7DCD8" opacity="0.45"/>

  <rect x="146" y="70" width="413" height="580" rx="46" fill="url(#portraitCardGrad)" filter="url(#cardShadow)"/>
  <image x="170" y="92" width="365" height="536"
         href="https://images.example.com/editorial-profile-portrait-young-speaker-soft-studio-light.jpg"
         clip-path="url(#portraitClip)" preserveAspectRatio="xMidYMid slice"/>

  <rect x="132" y="112" width="6" height="118" rx="3" fill="#EB4D4B"/>
  <rect x="560" y="532" width="78" height="6" rx="3" fill="#EB4D4B" opacity="0.70"/>

  <text x="167" y="662" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        letter-spacing="2.2" fill="#8B8B8B">SPEAKER PROFILE · PRODUCT STRATEGY</text>

  <text x="925" y="174" width="410" text-anchor="end"
        font-family="Microsoft YaHei, Segoe UI" font-size="92" font-weight="800"
        letter-spacing="8" fill="#EB4D4B">小 美</text>

  <text x="925" y="222" width="420" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="3" fill="#B8B8B8">CREATIVE FACILITATOR</text>

  <text x="925" y="304" width="430" text-anchor="end"
        font-family="Microsoft YaHei, Segoe UI" font-size="22" fill="#303030">
    <tspan x="925" dy="0">秋叶大学职场学院高材生，原就读于</tspan>
    <tspan x="925" dy="36">湖北省武汉市绝对学霸高中；</tspan>
    <tspan x="925" dy="58">身具段子天赋，因言语出口成章、</tspan>
    <tspan x="925" dy="36">举手投足出梗，被高中同学誉为</tspan>
    <tspan x="925" dy="36">“新时代段子手”的姑娘；</tspan>
    <tspan x="925" dy="58">小破站业余UP主，创造过</tspan>
    <tspan x="925" dy="36">10W+阅读量的内容作品。</tspan>
  </text>

  <rect x="970" y="116" width="2" height="486" fill="#E6E6E6"/>

  <text x="1004" y="134" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">X</text>
  <text x="1004" y="189" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">I</text>
  <text x="1004" y="244" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">A</text>
  <text x="1004" y="299" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">O</text>
  <text x="1004" y="354" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">M</text>
  <text x="1004" y="409" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">E</text>
  <text x="1004" y="464" width="42" text-anchor="middle" font-family="Segoe UI" font-size="26" font-weight="700" fill="#B6B6B6">I</text>
  <text x="1004" y="541" width="42" text-anchor="middle" font-family="Segoe UI" font-size="15" font-weight="700" fill="#EB4D4B">01</text>

  <text x="925" y="646" width="420" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" letter-spacing="1.5"
        fill="#9A9A9A">HUMOR · LEARNING DESIGN · SOCIAL CONTENT</text>
</svg>
```

## Avoid in this skill
- ❌ Rotating a whole text box for the vertical subtitle; use upright stacked letters instead for the editorial “name spine” effect.
- ❌ Center-aligning the name and biography; the lockup depends on a sharp shared right edge.
- ❌ Using only small typography; the name should be oversized enough to become the main graphic element.
- ❌ Applying `clip-path` to decorative shapes; keep clipping only on the portrait `<image>` for reliable PowerPoint translation.
- ❌ Overloading the portrait side with captions or bullets; the left side should remain mostly visual and quiet.

## Composition notes
- Keep the portrait in the left 35–42% of the canvas; reserve the right 55–60% for the typographic system.
- Align the giant name, role label, biography, and footer metadata to the same right edge, then place the vertical English/Pinyin spine just outside that edge.
- Use one vivid accent color for the name and tiny rules; keep biography text charcoal and the vertical letters pale gray.
- Leave generous white space above and below the biography so the layout feels like an editorial profile, not a résumé page.