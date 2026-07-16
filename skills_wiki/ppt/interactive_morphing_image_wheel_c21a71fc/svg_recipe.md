# SVG Recipe — Interactive Morphing Image Wheel

## Visual mechanism
A large photographic donut wheel is built from equal pie-slice image crops, with a clean central hub that names the active section. Across slides, the same wheel group is repositioned and rotated with PowerPoint Morph, turning the wheel into a spatial navigation device while the active content appears beside it.

## SVG primitives needed
- 1× `<rect>` for the clean slide background.
- 1× `<radialGradient>` for a subtle executive-keynote background glow.
- 1× `<linearGradient>` for accent typography and progress elements.
- 6× `<clipPath>` with `<path>` wedge geometry for cropping photos into pie slices.
- 6× `<image>` elements, each clipped to one wedge of the circular wheel.
- 6× `<path>` wedge overlays for subtle color tinting and slice borders.
- 6× `<line>` elements for crisp radial separators between image slices.
- 2× `<circle>` elements for the wheel shadow plate and white center hub.
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for premium depth.
- 1× `<filter id="hubGlow">` using `feGaussianBlur` for a soft central glow.
- Multiple `<text>` elements with explicit `width` attributes for section labels, hub text, title, body copy, and captions.
- 3× `<rect>` elements for the content panel, small metric cards, and progress indicator.
- 1× decorative `<path>` for a soft background accent curve.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="72%" cy="42%" r="58%">
      <stop offset="0%" stop-color="#F4F8FF"/>
      <stop offset="62%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F6F7FA"/>
    </radialGradient>

    <linearGradient id="blueAccent" x1="760" y1="130" x2="1160" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00AEEF"/>
      <stop offset="100%" stop-color="#5B4DFF"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="hubGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <!-- Six 60-degree wheel crops, centered at 0,0. Duplicate rather than <use>. -->
    <clipPath id="slice0" clipPathUnits="userSpaceOnUse">
      <path d="M0 0 L0 -330 A330 330 0 0 1 285.8 -165 Z"/>
    </clipPath>
    <clipPath id="slice1" clipPathUnits="userSpaceOnUse">
      <path d="M0 0 L285.8 -165 A330 330 0 0 1 285.8 165 Z"/>
    </clipPath>
    <clipPath id="slice2" clipPathUnits="userSpaceOnUse">
      <path d="M0 0 L285.8 165 A330 330 0 0 1 0 330 Z"/>
    </clipPath>
    <clipPath id="slice3" clipPathUnits="userSpaceOnUse">
      <path d="M0 0 L0 330 A330 330 0 0 1 -285.8 165 Z"/>
    </clipPath>
    <clipPath id="slice4" clipPathUnits="userSpaceOnUse">
      <path d="M0 0 L-285.8 165 A330 330 0 0 1 -285.8 -165 Z"/>
    </clipPath>
    <clipPath id="slice5" clipPathUnits="userSpaceOnUse">
      <path d="M0 0 L-285.8 -165 A330 330 0 0 1 0 -330 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <path d="M745 642 C860 560 930 606 1034 538 C1138 470 1130 332 1248 280 L1280 280 L1280 720 L745 720 Z"
        fill="#EAF2FF" opacity="0.75"/>

  <!-- Morph target state: detail slide. For overview slide, use translate(640 360) rotate(0) scale(.93). -->
  <g id="morphing_image_wheel_slices" transform="translate(250 360) rotate(-60)">
    <circle cx="0" cy="0" r="333" fill="#FFFFFF" filter="url(#softShadow)"/>

    <image href="https://images.example.com/photo-electric-vehicle-assembly-line-800x800.jpg"
           x="-330" y="-330" width="660" height="660" preserveAspectRatio="xMidYMid slice" clip-path="url(#slice0)"/>
    <image href="https://images.example.com/photo-keynote-audience-stage-lights-800x800.jpg"
           x="-330" y="-330" width="660" height="660" preserveAspectRatio="xMidYMid slice" clip-path="url(#slice1)"/>
    <image href="https://images.example.com/photo-chef-plating-modern-lunch-800x800.jpg"
           x="-330" y="-330" width="660" height="660" preserveAspectRatio="xMidYMid slice" clip-path="url(#slice2)"/>
    <image href="https://images.example.com/photo-mountain-hiking-trail-sunrise-800x800.jpg"
           x="-330" y="-330" width="660" height="660" preserveAspectRatio="xMidYMid slice" clip-path="url(#slice3)"/>
    <image href="https://images.example.com/photo-ocean-diving-blue-water-800x800.jpg"
           x="-330" y="-330" width="660" height="660" preserveAspectRatio="xMidYMid slice" clip-path="url(#slice4)"/>
    <image href="https://images.example.com/photo-premium-gear-texture-carbon-fiber-800x800.jpg"
           x="-330" y="-330" width="660" height="660" preserveAspectRatio="xMidYMid slice" clip-path="url(#slice5)"/>

    <path d="M0 0 L0 -330 A330 330 0 0 1 285.8 -165 Z" fill="#00AEEF" opacity="0.11"/>
    <path d="M0 0 L285.8 -165 A330 330 0 0 1 285.8 165 Z" fill="#5B4DFF" opacity="0.10"/>
    <path d="M0 0 L285.8 165 A330 330 0 0 1 0 330 Z" fill="#FFB000" opacity="0.09"/>
    <path d="M0 0 L0 330 A330 330 0 0 1 -285.8 165 Z" fill="#00B871" opacity="0.10"/>
    <path d="M0 0 L-285.8 165 A330 330 0 0 1 -285.8 -165 Z" fill="#0077FF" opacity="0.10"/>
    <path d="M0 0 L-285.8 -165 A330 330 0 0 1 0 -330 Z" fill="#FF4D6D" opacity="0.10"/>

    <line x1="0" y1="-330" x2="0" y2="-120" stroke="#FFFFFF" stroke-width="7"/>
    <line x1="285.8" y1="-165" x2="103.9" y2="-60" stroke="#FFFFFF" stroke-width="7"/>
    <line x1="285.8" y1="165" x2="103.9" y2="60" stroke="#FFFFFF" stroke-width="7"/>
    <line x1="0" y1="330" x2="0" y2="120" stroke="#FFFFFF" stroke-width="7"/>
    <line x1="-285.8" y1="165" x2="-103.9" y2="60" stroke="#FFFFFF" stroke-width="7"/>
    <line x1="-285.8" y1="-165" x2="-103.9" y2="-60" stroke="#FFFFFF" stroke-width="7"/>

    <text x="28" y="-240" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF" transform="rotate(60 28 -240)">JUNE</text>
    <text x="160" y="-8" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF" transform="rotate(120 160 -8)">KEYNOTE</text>
    <text x="42" y="247" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF" transform="rotate(180 42 247)">LUNCH</text>
    <text x="-210" y="246" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF" transform="rotate(240 -210 246)">HIKING</text>
    <text x="-292" y="-6" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF" transform="rotate(300 -292 -6)">DIVING</text>
    <text x="-160" y="-240" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">GEAR</text>
  </g>

  <g id="morphing_wheel_hub" transform="translate(250 360)">
    <circle cx="0" cy="0" r="142" fill="#FFFFFF" filter="url(#hubGlow)" opacity="0.75"/>
    <circle cx="0" cy="0" r="126" fill="#FFFFFF" stroke="#E9EDF5" stroke-width="2" filter="url(#softShadow)"/>
    <text x="-96" y="-18" width="192" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="2" fill="#8A94A6">SECTION 02</text>
    <text x="-98" y="27" width="196" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#151B26">ELECTRIC</text>
    <text x="-98" y="61" width="196" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#151B26">CARS</text>
  </g>

  <g id="content_reveal_panel">
    <text x="660" y="124" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="3" fill="url(#blueAccent)">INTERACTIVE AGENDA</text>
    <text x="660" y="184" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" fill="#101828">Electric mobility showcase</text>
    <text x="664" y="238" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#667085">Rotate the image wheel one slice per section. The audience always knows where they are in the story.</text>

    <rect x="662" y="294" width="418" height="118" rx="26" fill="#FFFFFF" stroke="#E7ECF3" filter="url(#softShadow)"/>
    <text x="694" y="339" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#667085">CURRENT STOP</text>
    <text x="694" y="378" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#101828">Prototype ride</text>
    <circle cx="1022" cy="353" r="30" fill="url(#blueAccent)"/>
    <text x="1003" y="363" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">02</text>

    <rect x="662" y="456" width="188" height="108" rx="24" fill="#F7FAFF" stroke="#E5EEF9"/>
    <text x="690" y="500" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#101828">6</text>
    <text x="690" y="532" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#667085">equal chapters</text>

    <rect x="886" y="456" width="188" height="108" rx="24" fill="#F7FAFF" stroke="#E5EEF9"/>
    <text x="914" y="500" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#101828">60°</text>
    <text x="914" y="532" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#667085">morph rotation</text>

    <rect x="662" y="615" width="418" height="8" rx="4" fill="#E5EAF2"/>
    <rect x="662" y="615" width="139" height="8" rx="4" fill="url(#blueAccent)"/>
    <text x="662" y="650" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#98A2B3">Slide 2 of 6 · keep the wheel object names identical across slides</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; build separate static slide states and let PowerPoint Morph interpolate them.
- ❌ `<mask>` for donut holes or image slices; use image `clipPath` crops plus a white center hub circle.
- ❌ `<textPath>` for curved wheel labels; it will not translate reliably, so use rotated straight text labels instead.
- ❌ `<use href="#slice">` to reuse wedge geometry; duplicate the wedge paths explicitly.
- ❌ Applying `clip-path` to tint rectangles or vector shapes; clipping is reliable here only on `<image>`.
- ❌ `marker-end` arrows or filter effects on `<line>` separators; keep separator lines plain white.

## Composition notes
- Keep the wheel diameter around 660 px: centered for the overview slide, then shifted left so it bleeds slightly off canvas for content slides.
- For Morph, preserve the same wheel slice objects between slides and change only `translate`, `rotate`, and optionally `scale`; rotate by `360 / number_of_sections`.
- The hub should remain upright and readable, even while the outer image wheel rotates; treat it as a separate object that moves with the wheel but does not rotate.
- Reserve the right 55–60% of the slide for large editorial typography, one focal card, and sparse metrics so the vivid image wheel remains the visual anchor.