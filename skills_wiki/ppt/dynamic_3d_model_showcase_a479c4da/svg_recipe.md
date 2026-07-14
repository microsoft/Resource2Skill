# SVG Recipe — Dynamic 3D Model Showcase

## Visual mechanism
A premium “turntable” product reveal is simulated by placing a large pseudo-3D model in a spotlight, surrounded by orbit rings, motion ghosts, and specular highlights. Since SVG-to-PPT cannot preserve true 3D model animation, the slide should visually imply rotation and dimensionality while remaining fully editable.

## SVG primitives needed
- 2× `<rect>` for the dark stage background and translucent info plate
- 6× `<path>` for aurora glow shapes, 3D model body, edge trim, glass face, highlight streaks, and arrow/indicator accents
- 4× `<ellipse>` for floor shadow and tilted turntable orbit rings
- 5× `<circle>` for orbit nodes and small depth cues
- 1× `<image>` clipped into the model screen as a branded texture/UI surface
- 1× `<clipPath>` with a custom `<path>` for the screen image crop
- 3× `<linearGradient>` for the background, model body, and red metallic edge
- 2× `<radialGradient>` for spotlight and orbit node glow
- 2× `<filter>` using blur/shadow for premium depth
- 5× `<text>` blocks with explicit `width=` for title, subtitle, badges, and callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#08111F"/>
      <stop offset="0.48" stop-color="#111827"/>
      <stop offset="1" stop-color="#05070D"/>
    </linearGradient>
    <radialGradient id="spot" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#4FD1FF" stop-opacity="0.45"/>
      <stop offset="0.55" stop-color="#1D4ED8" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="phoneBody" x1="600" y1="80" x2="850" y2="620">
      <stop offset="0" stop-color="#2B3445"/>
      <stop offset="0.42" stop-color="#05070A"/>
      <stop offset="1" stop-color="#1A1D25"/>
    </linearGradient>
    <linearGradient id="edgeRed" x1="830" y1="120" x2="940" y2="590">
      <stop offset="0" stop-color="#FF7A66"/>
      <stop offset="0.5" stop-color="#D92132"/>
      <stop offset="1" stop-color="#6E0B18"/>
    </linearGradient>
    <linearGradient id="glass" x1="625" y1="120" x2="840" y2="585">
      <stop offset="0" stop-color="#1F2937"/>
      <stop offset="0.5" stop-color="#070B12"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFE66D"/>
      <stop offset="0.45" stop-color="#FFB000"/>
      <stop offset="1" stop-color="#FFB000" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .42 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neonBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <clipPath id="screenClip">
      <path d="M642 143 C680 122 803 143 826 177 L862 516 C866 552 845 578 807 586 L677 614 C641 621 617 602 613 566 L577 220 C573 184 601 157 642 143 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M760 44 C930 5 1130 88 1184 244 C1065 204 904 222 790 317 C711 382 610 327 602 234 C596 160 650 72 760 44 Z" fill="#2563EB" opacity="0.22" filter="url(#neonBlur)"/>
  <path d="M352 534 C502 450 688 482 794 617 C620 718 384 735 236 652 C251 610 289 570 352 534 Z" fill="#06B6D4" opacity="0.16" filter="url(#neonBlur)"/>
  <ellipse cx="735" cy="640" rx="305" ry="38" fill="#000000" opacity="0.42" filter="url(#softShadow)"/>
  <circle cx="738" cy="346" r="320" fill="url(#spot)" opacity="0.72"/>

  <path d="M505 225 C579 168 729 145 890 174" fill="none" stroke="#8FE7FF" stroke-width="2.2" stroke-opacity="0.38" stroke-dasharray="14 16"/>
  <ellipse cx="735" cy="360" rx="338" ry="92" fill="none" stroke="#56D6FF" stroke-width="2.5" stroke-opacity="0.42" transform="rotate(-12 735 360)"/>
  <ellipse cx="735" cy="360" rx="260" ry="68" fill="none" stroke="#FBBF24" stroke-width="1.6" stroke-opacity="0.35" stroke-dasharray="9 14" transform="rotate(-12 735 360)"/>
  <circle cx="1012" cy="300" r="22" fill="url(#nodeGlow)" opacity="0.85"/>
  <circle cx="477" cy="421" r="11" fill="#56D6FF" opacity="0.8"/>
  <circle cx="918" cy="422" r="6" fill="#FFFFFF" opacity="0.9"/>

  <path d="M476 186 C522 166 622 178 644 210 L678 531 C684 575 657 603 610 613 L557 625 C522 633 500 614 496 580 L456 236 C452 211 459 194 476 186 Z" fill="#1F2937" opacity="0.18"/>
  <path d="M901 143 C940 152 963 176 967 214 L1000 527 C1005 574 976 607 929 617 L886 626 C855 633 836 615 833 584 L794 205 C791 168 825 129 901 143 Z" fill="#E11D48" opacity="0.16"/>

  <g filter="url(#softShadow)">
    <path d="M670 92 C718 72 842 94 875 132 L914 511 C920 563 891 602 838 615 L699 648 C648 660 611 633 606 582 L566 194 C561 145 610 111 670 92 Z" fill="url(#edgeRed)"/>
    <path d="M628 105 C676 84 810 105 842 143 L881 516 C887 566 858 601 808 612 L674 642 C626 653 592 626 587 578 L548 205 C543 157 573 126 628 105 Z" fill="url(#phoneBody)"/>
    <path d="M642 143 C680 122 803 143 826 177 L862 516 C866 552 845 578 807 586 L677 614 C641 621 617 602 613 566 L577 220 C573 184 601 157 642 143 Z" fill="url(#glass)" stroke="#334155" stroke-width="2"/>
    <image href="https://images.example.com/branded-product-ui-yellow-black-dashboard-texture.png" x="574" y="125" width="300" height="505" preserveAspectRatio="xMidYMid slice" clip-path="url(#screenClip)" opacity="0.78"/>
    <path d="M632 151 C685 124 765 134 816 171 L854 512 C778 439 685 280 632 151 Z" fill="#FFFFFF" opacity="0.12"/>
    <path d="M606 249 C651 224 752 241 811 282" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.18"/>
    <path d="M890 192 L910 510 C913 555 888 586 844 599" fill="none" stroke="#FF9D7C" stroke-width="5" stroke-linecap="round" opacity="0.7"/>
    <circle cx="721" cy="604" r="13" fill="#0B0F19" stroke="#475569" stroke-width="2"/>
  </g>

  <rect x="74" y="78" width="420" height="505" rx="34" fill="#0B1020" opacity="0.58" stroke="#263247" stroke-width="1.5"/>
  <text x="106" y="132" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#67E8F9" letter-spacing="2.5">TURNABLE HERO MODEL</text>
  <text x="104" y="208" width="375" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#F8FAFC">
    Dynamic 3D<tspan x="104" dy="58">Product Reveal</tspan>
  </text>
  <text x="106" y="340" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#CBD5E1">
    Simulate continuous rotation with orbit trails, ghosted angles, metallic edges, and a branded surface texture.
  </text>
  <path d="M108 410 L206 410 C224 410 235 421 235 439 L235 439" fill="none" stroke="#FBBF24" stroke-width="3" stroke-linecap="round"/>
  <circle cx="245" cy="439" r="5" fill="#FBBF24"/>
  <text x="106" y="466" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#94A3B8">
    Best for launches, keynote openers, technical demos, and premium brand moments.
  </text>

  <text x="904" y="118" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E2E8F0">looping 360° impression</text>
  <text x="910" y="534" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#93C5FD">gloss + edge lighting create depth</text>
</svg>
```

## Avoid in this skill
- ❌ Real SVG animation with `<animate>` or `<animateTransform>`; PPT-Master will hard-fail these.
- ❌ Expecting an actual `.glb` 3D model to survive as a native editable PowerPoint object through SVG; use a rendered image or editable vector approximation instead.
- ❌ `transform="skewX(...)"` or matrix transforms for perspective; build perspective manually with custom `<path>` geometry.
- ❌ `clip-path` on vector shapes for screen glass or highlights; clipping is only reliable on `<image>`.
- ❌ `marker-end` arrows on paths; use small circles or explicit triangle/path arrowheads if direction is needed.

## Composition notes
- Place the pseudo-3D object large, around 50–70% of slide height, slightly right of center so text has a clear left-side runway.
- Use a dark, minimal background with one radial spotlight and one or two blurred color blooms to make the model feel staged.
- Orbit ellipses, ghost silhouettes, and glowing nodes should imply motion without competing with the product surface.
- Keep copy short and executive: one title, one explanatory sentence, and one small technical callout are enough.