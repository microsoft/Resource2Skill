# SVG Recipe — Interactive Morph Showcase

## Visual mechanism
A non-linear showcase is built from multiple nearly identical slides: the clicked card expands into the hero state while sibling cards shrink and fade, so PowerPoint Morph animates size, position, and emphasis changes smoothly. In SVG, each slide state should keep the same core objects and IDs, changing only geometry, opacity, fills, and text content between states.

## SVG primitives needed
- 1× `<rect>` full-slide background using a radial/linear gradient for soft keynote depth
- 3× shadowed `<rect>` card backplates for photo-card elevation
- 3× `<image>` portrait photos clipped into rounded rectangles
- 3× `<clipPath>` with rounded `<rect>` crops, one per photo card
- 3× translucent `<path>` bottom bands over photos for role labels
- 3× rotated `<text>` role labels on top of the photo bands
- 1× left-side title group using multiple `<text>` elements with explicit widths
- 1× active-member detail block with role, name, description, and contact-style metadata
- 2× decorative organic `<path>` blobs for premium visual atmosphere
- 1× home/navigation `<path>` icon in accent orange
- 1× `<filter id="softShadow">` applied to card rectangles and the active detail panel
- 1× `<filter id="orangeGlow">` applied to the active accent shape/card halo
- Several small `<circle>` indicators for interactive state/navigation affordance

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="38%" cy="32%" r="78%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F3F3F1"/>
      <stop offset="100%" stop-color="#E5E2DE"/>
    </radialGradient>

    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF8A35"/>
      <stop offset="100%" stop-color="#E85D1F"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="orangeGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>

    <clipPath id="clipCardA" clipPathUnits="userSpaceOnUse">
      <rect x="626" y="156" width="188" height="430" rx="34"/>
    </clipPath>
    <clipPath id="clipCardB" clipPathUnits="userSpaceOnUse">
      <rect x="832" y="104" width="272" height="520" rx="38"/>
    </clipPath>
    <clipPath id="clipCardC" clipPathUnits="userSpaceOnUse">
      <rect x="1122" y="156" width="188" height="430" rx="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <path d="M-55,122 C75,34 192,58 244,150 C304,256 179,337 58,312 C-48,291 -135,216 -55,122 Z"
        fill="#F06E23" opacity="0.09"/>
  <path d="M1068,648 C1118,548 1244,520 1328,574 C1408,626 1378,754 1264,785 C1155,815 1014,759 1068,648 Z"
        fill="#F06E23" opacity="0.12"/>

  <text x="86" y="112" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="66" font-weight="300" fill="#3E3E3E">Meet</text>
  <text x="88" y="164" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" letter-spacing="4" fill="#F06E23">OUR TEAM</text>
  <line x1="88" y1="190" x2="256" y2="190" stroke="#F06E23" stroke-width="5" stroke-linecap="round"/>

  <rect x="82" y="232" width="438" height="318" rx="30" fill="#FFFFFF" opacity="0.82" filter="url(#softShadow)"/>
  <text x="112" y="282" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="2.5" fill="#F06E23">FEATURED PROFILE</text>
  <text x="110" y="346" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="300" fill="#2D2D2D">Maya Chen</text>
  <text x="113" y="388" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#5F5F5F">Product Strategy Lead</text>
  <text x="114" y="438" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#7B7B7B">
    Turns customer signals into sharp product narratives, launch stories, and market-ready decision frameworks.
  </text>
  <text x="114" y="506" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#F06E23">Click another portrait to morph the spotlight.</text>

  <path d="M92,610 L116,590 L140,610 L140,642 L122,642 L122,622 L110,622 L110,642 L92,642 Z"
        fill="#F06E23"/>
  <text x="154" y="633" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#6B6B6B">Back to overview</text>

  <rect x="626" y="156" width="188" height="430" rx="34" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.9"/>
  <image x="626" y="156" width="188" height="430" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/team-portrait-engineering-director.jpg" clip-path="url(#clipCardA)" opacity="0.72"/>
  <rect x="626" y="156" width="188" height="430" rx="34" fill="#C9C9C9" opacity="0.42"/>
  <path d="M626,478 L814,478 L814,552 Q814,586 780,586 L660,586 Q626,586 626,552 Z" fill="#6B6B6B" opacity="0.62"/>
  <text x="666" y="552" width="156" transform="rotate(-90 666 552)"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">ENGINEERING</text>

  <rect x="822" y="94" width="292" height="540" rx="46" fill="#F06E23" opacity="0.22" filter="url(#orangeGlow)"/>
  <rect x="832" y="104" width="272" height="520" rx="38" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="832" y="104" width="272" height="520" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/team-portrait-product-strategist-orange-studio.jpg" clip-path="url(#clipCardB)"/>
  <path d="M832,496 L1104,496 L1104,586 Q1104,624 1066,624 L870,624 Q832,624 832,586 Z" fill="url(#orangeGrad)" opacity="0.82"/>
  <text x="890" y="590" width="220" transform="rotate(-90 890 590)"
        font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="900" letter-spacing="2" fill="#FFFFFF">PRODUCT</text>
  <text x="1004" y="568" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" opacity="0.9">ACTIVE</text>

  <rect x="1122" y="156" width="188" height="430" rx="34" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.9"/>
  <image x="1122" y="156" width="188" height="430" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/team-portrait-creative-director.jpg" clip-path="url(#clipCardC)" opacity="0.72"/>
  <rect x="1122" y="156" width="188" height="430" rx="34" fill="#C9C9C9" opacity="0.42"/>
  <path d="M1122,478 L1310,478 L1310,552 Q1310,586 1276,586 L1156,586 Q1122,586 1122,552 Z" fill="#6B6B6B" opacity="0.62"/>
  <text x="1162" y="552" width="156" transform="rotate(-90 1162 552)"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" letter-spacing="1.5" fill="#FFFFFF">CREATIVE</text>

  <circle cx="900" cy="672" r="6" fill="#B8B8B8"/>
  <circle cx="932" cy="672" r="8" fill="#F06E23"/>
  <circle cx="966" cy="672" r="6" fill="#B8B8B8"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the morph itself; create separate slides and let PowerPoint Morph handle motion.
- ❌ `<use>` / `<symbol>` for repeated cards; duplicate the actual editable shapes so Morph can match and interpolate them reliably.
- ❌ `clip-path` on groups or rectangles for card construction; only apply clipping to `<image>` and draw overlays as normal editable shapes.
- ❌ `filter` on `<line>` elements for glowing dividers; use shadow/glow filters on rectangles, paths, circles, or text instead.
- ❌ Relying on SVG hyperlinks for navigation; add PowerPoint hyperlinks to the resulting card shapes or transparent click zones after import.

## Composition notes
- Keep the left 40% of the slide for title, active profile copy, and home/navigation controls; keep the right 60% for the morphing card stage.
- On each destination slide, preserve the same card objects but change their x/y/width/height, opacity, and accent fills so Morph creates the expansion effect.
- The active card should be the only full-color, high-contrast portrait; inactive cards should be visually subdued with gray overlays and lower opacity.
- Use orange sparingly but consistently: subtitle, active glow, active photo band, home icon, and selected pagination dot.