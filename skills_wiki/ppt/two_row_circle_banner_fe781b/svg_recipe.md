# SVG Recipe — Two Row Circle Banner

## Visual mechanism
Two stacked feature rows use oversized circular labels that overlap long rounded rectangular banners, creating a strong left-to-right reading path. The circles carry the row identity, while the banners provide richer explanatory copy with soft shadows, accent strips, and generous whitespace.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for large soft decorative background blobs
- 2× `<rect>` for the main rounded content banners
- 2× `<rect>` for thin colored accent rails on the right edge of each banner
- 2× `<circle>` for prominent overlapping row labels
- 2× `<circle>` for subtle outer halo rings behind the labels
- 1× `<line>` for the dashed vertical rhythm connector between row circles
- 10× `<text>` for slide heading, subtitle, circle numerals, circle labels, banner headings, body copy, and small metadata tags
- 4× `<linearGradient>` for background, banner fills, and circle label fills
- 1× `<radialGradient>` for decorative glow
- 2× `<filter>` using blur/offset/merge for soft card shadows and circle glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="52%" stop-color="#EEF5FF"/>
      <stop offset="100%" stop-color="#F9FBFD"/>
    </linearGradient>

    <linearGradient id="bannerOne" x1="270" y1="0" x2="1110" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="68%" stop-color="#F9FCFF"/>
      <stop offset="100%" stop-color="#EAF4FF"/>
    </linearGradient>

    <linearGradient id="bannerTwo" x1="270" y1="0" x2="1110" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="68%" stop-color="#FFFDF8"/>
      <stop offset="100%" stop-color="#FFF2DA"/>
    </linearGradient>

    <linearGradient id="circleBlue" x1="222" y1="158" x2="410" y2="342">
      <stop offset="0%" stop-color="#39B8FF"/>
      <stop offset="55%" stop-color="#2276F2"/>
      <stop offset="100%" stop-color="#164ACB"/>
    </linearGradient>

    <linearGradient id="circleOrange" x1="222" y1="370" x2="410" y2="554">
      <stop offset="0%" stop-color="#FFD36A"/>
      <stop offset="55%" stop-color="#FF8A34"/>
      <stop offset="100%" stop-color="#E85B1A"/>
    </linearGradient>

    <radialGradient id="cornerGlow" cx="70%" cy="18%" r="65%">
      <stop offset="0%" stop-color="#B7DCFF" stop-opacity="0.7"/>
      <stop offset="58%" stop-color="#DCEEFF" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="circleGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cornerGlow)"/>

  <path d="M-90,565 C90,495 180,610 335,555 C500,496 592,615 734,575 C865,538 940,575 1040,642 L1040,805 L-90,805 Z"
        fill="#DCEBFF" opacity="0.42"/>
  <path d="M917,-88 C1015,-24 1100,-12 1196,50 C1296,114 1330,218 1292,306 C1251,401 1138,392 1039,340 C943,288 854,274 818,180 C779,78 824,-22 917,-88 Z"
        fill="#FFE7C7" opacity="0.48"/>

  <text x="120" y="78" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#172033">Two strategic moves</text>
  <text x="122" y="114" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#6B7484">Use the circular labels as anchors, then let each banner explain the outcome in one clean scan.</text>

  <line x1="278" y1="272" x2="278" y2="442" stroke="#9BB3D4" stroke-width="3"
        stroke-dasharray="9 12" opacity="0.65"/>

  <circle cx="278" cy="246" r="106" fill="#D9EAFF" opacity="0.55"/>
  <rect x="286" y="168" width="832" height="156" rx="34" fill="url(#bannerOne)" filter="url(#cardShadow)"/>
  <rect x="1088" y="196" width="10" height="100" rx="5" fill="#247CFF"/>
  <circle cx="278" cy="246" r="88" fill="url(#circleBlue)" filter="url(#circleGlow)"/>
  <circle cx="278" cy="246" r="72" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.38"/>

  <text x="236" y="234" width="84" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF">01</text>
  <text x="220" y="267" width="116" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="1.6" fill="#DDF0FF">ALIGN</text>

  <text x="372" y="218" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="700" fill="#16243A">Clarify the operating model</text>
  <text x="374" y="256" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#5C6677">Define ownership, decision rights, and the few metrics that matter before scaling the program across teams.</text>
  <text x="922" y="248" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#247CFF">FOUNDATION</text>

  <circle cx="278" cy="458" r="106" fill="#FFE9C7" opacity="0.58"/>
  <rect x="286" y="380" width="832" height="156" rx="34" fill="url(#bannerTwo)" filter="url(#cardShadow)"/>
  <rect x="1088" y="408" width="10" height="100" rx="5" fill="#FF8A34"/>
  <circle cx="278" cy="458" r="88" fill="url(#circleOrange)" filter="url(#circleGlow)"/>
  <circle cx="278" cy="458" r="72" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.42"/>

  <text x="236" y="446" width="84" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF">02</text>
  <text x="220" y="479" width="116" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="1.6" fill="#FFF2DA">SCALE</text>

  <text x="372" y="430" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="700" fill="#16243A">Launch repeatable execution loops</text>
  <text x="374" y="468" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#5C6677">Package the playbook into rituals, templates, and review cadences so progress compounds without adding complexity.</text>
  <text x="922" y="460" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#F07822">MOMENTUM</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to duplicate the two rows; duplicate the row shapes directly so PowerPoint keeps everything editable.
- ❌ Do not apply `filter` to the dashed connector `<line>`; line filters are dropped, so keep the connector flat.
- ❌ Do not clip non-image shapes to make the overlapping circles; simply layer the circle above the rounded banner.
- ❌ Do not rely on skewed rectangles or matrix transforms for angled banner ends; use straight rounded rectangles or explicit `<path>` geometry if angled ends are required.
- ❌ Do not omit `width` on text elements, especially banner body copy, because PowerPoint will otherwise crop or reflow unpredictably.

## Composition notes
- Keep the two rows centered vertically, with the circle center sitting slightly left of the banner’s left edge so the overlap feels intentional and dimensional.
- Reserve the right half of each banner for breathing room, small status tags, or accent rails; avoid filling it with dense paragraphs.
- Use one cool row and one warm row to make the two features instantly distinguishable while preserving a shared white-card system.
- Let the background remain quiet: soft blobs and glows should support the circle-banner structure, not compete with the row labels.