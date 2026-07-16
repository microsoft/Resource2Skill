# SVG Recipe — Dynamic Curtain Reveal with 3D Depth Illusion

## Visual mechanism
Create a cinematic divider/title slide by stacking a full-bleed visual scene, oversized translucent typography, and a transparent cutout subject so the typography appears to pass behind the subject. Add two large gradient “curtain” panels above and below the slide, slightly visible at the edges, ready to be animated in PowerPoint as fly-in/fly-out reveal panels.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 1× `<image>` for the background hero photo clipped into a rounded card
- 1× `<clipPath>` with rounded `<rect>` for the hero photo crop
- 1× `<image>` for the transparent foreground cutout subject layered above the giant text
- 2× large `<text>` elements for oversized translucent depth typography behind the cutout
- 1× `<rect>` for the right-side content panel
- 1× `<path>` for an angled accent wedge separating image and content zones
- 1× `<rect>` for the title banner
- 4× `<text>` elements for title, subtitle, bullet copy, and small kicker label
- 2× large `<rect>` elements for top and bottom curtain panels
- 6× `<path>` elements for curtain folds, highlights, and edge shadows
- 3× `<linearGradient>` definitions for curtain fabric, title/banner accents, and dark overlay depth
- 1× `<radialGradient>` for a subtle spotlight glow behind the subject
- 2× `<filter>` definitions for soft shadows and glow applied to rectangles, paths, and text
- Several decorative `<circle>` elements for premium atmospheric bokeh and light depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="curtainGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#673AB7"/>
      <stop offset="45%" stop-color="#5B4DE1"/>
      <stop offset="100%" stop-color="#00BCD4"/>
    </linearGradient>

    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6D3BFF"/>
      <stop offset="100%" stop-color="#00D5E8"/>
    </linearGradient>

    <linearGradient id="darkFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#050B18" stop-opacity="0.15"/>
      <stop offset="65%" stop-color="#050B18" stop-opacity="0.80"/>
      <stop offset="100%" stop-color="#050B18" stop-opacity="1"/>
    </linearGradient>

    <radialGradient id="spotlight" cx="42%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#7EE7FF" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#1C4D86" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#06101F" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <rect x="42" y="54" width="640" height="612" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#06101F"/>
  <circle cx="430" cy="325" r="350" fill="url(#spotlight)"/>
  <circle cx="1070" cy="118" r="80" fill="#00BCD4" opacity="0.13" filter="url(#cyanGlow)"/>
  <circle cx="1135" cy="595" r="145" fill="#673AB7" opacity="0.18" filter="url(#cyanGlow)"/>
  <circle cx="755" cy="88" r="28" fill="#AEEFFF" opacity="0.20"/>

  <image href="https://images.example.com/hero-photo/business-leader-on-glass-stairs-dark-cinematic.jpg"
         x="42" y="54" width="640" height="612" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>

  <rect x="42" y="54" width="640" height="612" rx="34" ry="34" fill="none" stroke="#75E6FF" stroke-opacity="0.28" stroke-width="2"/>
  <rect x="42" y="54" width="640" height="612" rx="34" ry="34" fill="url(#darkFade)" opacity="0.55"/>

  <text x="70" y="284" width="590" font-family="Segoe UI, Microsoft YaHei" font-size="164" font-weight="800"
        letter-spacing="-8" fill="#BDEFFF" opacity="0.34" filter="url(#softShadow)">RISE</text>
  <text x="84" y="430" width="570" font-family="Segoe UI, Microsoft YaHei" font-size="118" font-weight="800"
        letter-spacing="-6" fill="#E6FAFF" opacity="0.18">ABOVE</text>

  <image href="https://images.example.com/transparent-png/executive-walking-up-stairs-cutout.png"
         x="104" y="76" width="520" height="610" preserveAspectRatio="xMidYMax meet"/>

  <path d="M650,0 L820,0 C760,150 760,294 824,430 C865,517 864,628 812,720 L650,720 Z"
        fill="#071528" opacity="0.92" filter="url(#softShadow)"/>

  <rect x="740" y="0" width="540" height="720" fill="#071528"/>
  <path d="M760,92 C900,44 1048,52 1198,92 L1198,98 C1045,78 904,78 760,120 Z"
        fill="#00BCD4" opacity="0.17"/>
  <path d="M780,610 C914,560 1058,562 1218,620 L1218,628 C1050,604 922,604 780,646 Z"
        fill="#673AB7" opacity="0.20"/>

  <text x="796" y="124" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="3" fill="#75E6FF">SECTION 02 / STRATEGIC MOMENTUM</text>

  <rect x="792" y="154" width="382" height="68" rx="14" fill="url(#titleGrad)" filter="url(#softShadow)"/>
  <text x="818" y="199" width="338" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800"
        fill="#FFFFFF">Business Strengths</text>

  <text x="796" y="286" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800"
        fill="#FFFFFF" letter-spacing="-2">Lead from a position of depth.</text>

  <text x="800" y="357" width="386" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#C9D7EA">
    <tspan x="800" dy="0">Use the reveal as a dramatic reset, then let the</tspan>
    <tspan x="800" dy="31">foreground subject break through oversized type</tspan>
    <tspan x="800" dy="31">to create a premium keynote-style focal point.</tspan>
  </text>

  <line x1="800" y1="478" x2="1168" y2="478" stroke="#75E6FF" stroke-opacity="0.35" stroke-width="2"/>
  <text x="800" y="526" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#FFFFFF">
    <tspan x="800" dy="0" font-weight="700" fill="#75E6FF">01</tspan>
    <tspan dx="18" font-weight="700">Layered hero photo</tspan>
    <tspan x="800" dy="38" font-weight="700" fill="#75E6FF">02</tspan>
    <tspan dx="18" font-weight="700">Oversized intersecting type</tspan>
    <tspan x="800" dy="38" font-weight="700" fill="#75E6FF">03</tspan>
    <tspan dx="18" font-weight="700">Animated gradient curtain panels</tspan>
  </text>

  <rect x="0" y="-300" width="1280" height="370" fill="url(#curtainGrad)" filter="url(#softShadow)"/>
  <path d="M0,52 C170,82 320,14 506,54 C680,92 858,34 1032,58 C1134,72 1210,62 1280,44 L1280,70 L0,70 Z"
        fill="#FFFFFF" opacity="0.13"/>
  <path d="M0,70 C170,96 360,70 512,90 C690,114 888,86 1044,98 C1140,106 1218,94 1280,86"
        fill="none" stroke="#02101C" stroke-opacity="0.35" stroke-width="8"/>
  <path d="M112,-300 C82,-210 94,-114 124,70 M356,-300 C326,-194 334,-80 378,70 M720,-300 C676,-184 688,-62 736,70 M1060,-300 C1022,-198 1034,-68 1082,70"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.11" stroke-width="10"/>

  <rect x="0" y="650" width="1280" height="370" fill="url(#curtainGrad)" filter="url(#softShadow)"/>
  <path d="M0,650 C170,626 336,676 506,646 C674,616 846,672 1028,642 C1132,626 1218,640 1280,660 L1280,650 Z"
        fill="#FFFFFF" opacity="0.12"/>
  <path d="M0,650 C180,622 362,654 518,632 C706,606 900,640 1052,624 C1152,614 1224,632 1280,642"
        fill="none" stroke="#02101C" stroke-opacity="0.38" stroke-width="8"/>
  <path d="M146,650 C106,752 116,894 156,1020 M442,650 C396,768 412,890 462,1020 M810,650 C764,760 780,886 828,1020 M1110,650 C1068,760 1082,894 1132,1020"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="10"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the curtain motion; export static editable curtain panels and apply PowerPoint Fly In / Fly Out animation manually.
- ❌ Do not use `<mask>` to fake the foreground cutout; use a real transparent PNG cutout image layered above the oversized text.
- ❌ Do not apply `clip-path` to text or shapes for the intersect effect; PowerPoint translation only preserves clipping reliably on `<image>`.
- ❌ Do not use `<use>` or `<symbol>` to repeat curtain folds; duplicate the editable `<path>` shapes directly.
- ❌ Do not put shadows on `<line>` elements; use filters on `<rect>`, `<path>`, `<circle>`, or `<text>` only.

## Composition notes
- Keep the hero image and depth illusion on the left 50–55% of the slide; reserve the right side for clean title and message hierarchy.
- Place the oversized typography between the background photo and the transparent cutout subject, using low opacity so it feels embedded in the scene.
- The curtain panels should sit slightly off-canvas at the top and bottom in the “revealed” state; for a closed state, move them to cover the upper and lower halves of the slide.
- Use the purple-to-cyan curtain gradient as a repeating color rhythm in the title banner, small accents, and atmospheric glow.