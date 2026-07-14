# SVG Recipe — Organic Pop-out Character Spotlight

## Visual mechanism
A transparent-background portrait is layered twice around a warm organic blob: one copy sits behind the blob, while a second clipped copy appears only above the blob’s top edge, creating a polished “person popping out of color” effect. Soft blurred circles and generous negative space keep the biography layout modern, approachable, and premium.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm cream background
- 3× `<circle>` with blur filters for soft bokeh accent spots
- 1× `<path>` for the large organic orange blob behind the character
- 1× `<image>` behind the blob for the portrait base layer
- 1× `<image>` clipped by an organic `<clipPath>` for the pop-out upper portrait layer
- 1× `<filter id="blobShadow">` applied to the blob for grounded depth
- 1× `<filter id="softBlur">` applied to bokeh circles
- 1× `<filter id="portraitShadow">` applied to the upper portrait image for subtle separation
- 1× `<linearGradient>` for the blob fill
- 1× `<clipPath>` with a custom `<path>` applied only to the top portrait image
- Multiple `<text>` elements with explicit `width` for name, credential, bullets, and paragraphs
- 1× rounded `<rect>` accent badge behind the credential
- 4× small `<circle>` bullet dots for scannable profile details
- 2× decorative `<path>` strokes for subtle organic line accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blobGrad" x1="690" y1="180" x2="1120" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFD85A"/>
      <stop offset="0.55" stop-color="#FFC000"/>
      <stop offset="1" stop-color="#F5A900"/>
    </linearGradient>

    <filter id="softBlur" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="blobShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="portraitShadow" x="-30%" y="-20%" width="160%" height="150%">
      <feOffset dx="-10" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Region above the blob's front edge. Apply only to the portrait image. -->
    <clipPath id="upperPortraitClip">
      <path d="M650,0 L1280,0 L1280,404
               C1190,372 1114,374 1048,397
               C974,423 914,430 846,396
               C780,363 724,349 650,380 Z"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFF8E3"/>

  <!-- Soft atmospheric bokeh -->
  <circle cx="18" cy="16" r="118" fill="#FFC000" opacity="0.18" filter="url(#softBlur)"/>
  <circle cx="330" cy="-22" r="84" fill="#FFC000" opacity="0.13" filter="url(#softBlur)"/>
  <circle cx="1186" cy="670" r="132" fill="#FFC000" opacity="0.12" filter="url(#softBlur)"/>

  <!-- Left text column -->
  <text x="108" y="154" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700" fill="#333333">李玉婷</text>

  <rect x="110" y="183" width="88" height="34" rx="17" fill="#FFC000"/>
  <text x="136" y="207" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">MBA</text>

  <text x="110" y="268" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#333333">商业战略与组织增长顾问</text>

  <circle cx="122" cy="320" r="5.5" fill="#FFC000"/>
  <text x="145" y="328" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#595959">知名企业的高管，拥有跨行业管理经验</text>

  <circle cx="122" cy="363" r="5.5" fill="#FFC000"/>
  <text x="145" y="371" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#595959">毕业于北京大学经济学专业</text>

  <circle cx="122" cy="406" r="5.5" fill="#FFC000"/>
  <text x="145" y="414" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#595959">曾在国际投资银行负责战略项目</text>

  <circle cx="122" cy="449" r="5.5" fill="#FFC000"/>
  <text x="145" y="457" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#595959">2010 年成为商务经理并带领团队扩张</text>

  <text x="110" y="527" width="505" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    <tspan x="110" dy="0">拥有丰富的商业经验和管理能力。在公司的发展过程中，</tspan>
    <tspan x="110" dy="31">始终坚持以客户为中心的理念，不断推动产品与服务创新。</tspan>
  </text>

  <text x="110" y="622" width="505" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#777777">
    <tspan x="110" dy="0">积极参与社会责任活动，喜欢旅行、阅读和健身，</tspan>
    <tspan x="110" dy="29">保持健康、开放且持续学习的生活态度。</tspan>
  </text>

  <!-- Decorative organic line accents -->
  <path d="M68,612 C42,584 42,546 72,527 C94,512 128,520 139,548"
        fill="none" stroke="#FFC000" stroke-width="3" stroke-linecap="round" opacity="0.35"/>
  <path d="M584,122 C620,94 668,106 682,146"
        fill="none" stroke="#FFC000" stroke-width="4" stroke-linecap="round" opacity="0.28"/>

  <!-- Portrait base layer: sits behind the blob -->
  <image x="760" y="78" width="360" height="590"
         href="https://images.example.com/transparent-png-confident-businesswoman-standing.png"
         opacity="0.98"/>

  <!-- Organic blob layer: covers lower portrait and creates the color plinth -->
  <path filter="url(#blobShadow)"
        d="M745,390
           C730,308 792,236 889,215
           C974,197 1051,218 1108,279
           C1170,346 1185,438 1142,526
           C1104,604 1017,654 925,637
           C838,621 760,586 731,511
           C714,466 720,424 745,390 Z"
        fill="url(#blobGrad)"/>

  <!-- Pop-out portrait layer: only the upper body appears in front of the blob -->
  <image x="760" y="78" width="360" height="590"
         href="https://images.example.com/transparent-png-confident-businesswoman-standing.png"
         clip-path="url(#upperPortraitClip)"
         filter="url(#portraitShadow)"/>

  <!-- Small foreground highlights on the blob -->
  <ellipse cx="1090" cy="313" rx="19" ry="10" fill="#FFFFFF" opacity="0.30" transform="rotate(-22 1090 313)"/>
  <circle cx="783" cy="510" r="10" fill="#FFFFFF" opacity="0.22"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to cut the portrait around the blob; duplicate the transparent PNG and use `clipPath` on the top `<image>` instead.
- ❌ Applying `clip-path` to the blob or other vector shapes; clipping is reliable here only on the `<image>` portrait layer.
- ❌ Building the organic shape from many circles or rectangles; use one custom `<path>` so the blob stays fluid and premium.
- ❌ Using a rectangular portrait crop; the effect depends on a transparent-background person PNG.
- ❌ Overloading both columns with equal visual weight; the right portrait/blob must remain the primary focal point.

## Composition notes
- Keep the person-and-blob cluster on the right 40–45% of the slide, with the head rising above the blob to create the strongest pop-out illusion.
- Reserve the left 50% for biography text with generous line spacing and clear hierarchy: large name, small credential badge, bullets, then paragraphs.
- Use one dominant accent color repeatedly: blob, credential badge, bullet dots, and small decorative strokes.
- Let bokeh circles sit partially off-canvas and heavily blurred so they add atmosphere without competing with the portrait.