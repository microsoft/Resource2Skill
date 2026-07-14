# SVG Recipe — Interactive Portfolio Showcase

## Visual mechanism
A single “application stage” or monitor frame anchors the slide while colorful navigation pills imply non-linear movement between portfolio examples. The current example appears inside the screen, with a magnifying-glass overlay using a clipped, enlarged duplicate image to spotlight one detail.

## SVG primitives needed
- 1× full-slide `<rect>` for the soft presentation background
- 2× decorative `<path>` blobs for premium depth and motion
- 6× `<linearGradient>` / `<radialGradient>` definitions for background, buttons, screen shine, and lens glow
- 2× `<filter>` definitions for soft card shadows and lens glow
- 1× large rounded `<rect>` for the monitor body
- 1× rounded `<rect>` for the inner screen bezel
- 1× `<image>` clipped to a rounded-rectangle screen area for the selected portfolio example
- 1× enlarged duplicate `<image>` clipped to a circular lens for the zoomed detail
- 1× `<circle>` for the magnifier rim and 1× `<path>` for the handle
- 4× rounded `<rect>` navigation buttons, plus small active-state accent shapes
- Multiple `<text>` labels with explicit `width` attributes for title, section labels, button text, and annotations
- 3× small `<circle>` elements for monitor window controls
- 2× `<rect>` / `<path>` elements for monitor stand and base

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F0F8FF"/>
      <stop offset="58%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EAF3FF"/>
    </linearGradient>
    <radialGradient id="blueBlob" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#B9D8FF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#B9D8FF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="monitorGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#DDE7F2"/>
    </linearGradient>
    <linearGradient id="screenShine" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#0B1F35" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="activeBtn" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF7A59"/>
      <stop offset="100%" stop-color="#E74C3C"/>
    </linearGradient>
    <linearGradient id="lensTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#DFF2FF" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="lensGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>

    <clipPath id="screenClip">
      <rect x="286" y="154" width="726" height="408" rx="16"/>
    </clipPath>
    <clipPath id="lensClip">
      <circle cx="874" cy="430" r="88"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-80 95 C110 20 205 75 310 10 C365 -24 430 -14 485 28 C380 96 336 160 218 155 C90 150 14 201 -80 255 Z" fill="url(#blueBlob)"/>
  <path d="M1014 625 C1110 560 1168 512 1298 535 L1298 740 L940 740 C940 690 970 654 1014 625 Z" fill="#F9D7A7" opacity="0.32"/>

  <text x="70" y="66" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#5D6D7E" letter-spacing="2">INTERACTIVE PORTFOLIO</text>
  <text x="70" y="112" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#17202A">Choose a case study, keep the stage consistent</text>
  <text x="72" y="145" width="515" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#657786">Use slide triggers or hyperlinks in PowerPoint to swap the image shown inside the monitor.</text>

  <rect x="70" y="208" width="210" height="64" rx="18" fill="url(#activeBtn)" filter="url(#softShadow)"/>
  <path d="M268 232 L292 240 L268 248 Z" fill="#E74C3C"/>
  <text x="96" y="246" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">01  Donation CTA</text>
  <text x="96" y="265" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFE9E4">active showcase</text>

  <rect x="70" y="292" width="210" height="58" rx="17" fill="#F1C40F"/>
  <text x="96" y="327" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#2C3E50">02  Product Story</text>

  <rect x="70" y="368" width="210" height="58" rx="17" fill="#2ECC71"/>
  <text x="96" y="403" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#FFFFFF">03  Impact Report</text>

  <rect x="70" y="444" width="210" height="58" rx="17" fill="#3498DB"/>
  <text x="96" y="479" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#FFFFFF">04  Mobile Flow</text>

  <rect x="316" y="118" width="736" height="482" rx="34" fill="#C9D6E3" opacity="0.65" filter="url(#softShadow)"/>
  <rect x="300" y="102" width="736" height="482" rx="34" fill="url(#monitorGrad)" stroke="#B8C7D6" stroke-width="2"/>
  <rect x="286" y="154" width="726" height="408" rx="16" fill="#FFFFFF" stroke="#AEBCCD" stroke-width="4"/>
  <circle cx="335" cy="128" r="7" fill="#E74C3C"/>
  <circle cx="359" cy="128" r="7" fill="#F1C40F"/>
  <circle cx="383" cy="128" r="7" fill="#2ECC71"/>
  <text x="425" y="134" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#7B8A9A">case-study-preview.app / donation-cta</text>

  <image x="286" y="154" width="726" height="408" clip-path="url(#screenClip)" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portfolio-nonprofit-fundraising-infographic.png"/>
  <rect x="286" y="154" width="726" height="408" rx="16" fill="url(#screenShine)" pointer-events="none"/>

  <rect x="606" y="600" width="124" height="48" rx="12" fill="#CCD8E4"/>
  <path d="M520 654 C585 638 758 638 824 654 C838 658 838 678 820 681 L524 681 C506 678 506 658 520 654 Z" fill="#B8C7D6"/>
  <rect x="550" y="650" width="244" height="12" rx="6" fill="#E8EEF5"/>

  <circle cx="874" cy="430" r="99" fill="#FFFFFF" opacity="0.78" filter="url(#lensGlow)"/>
  <image x="258" y="-60" width="1110" height="624" clip-path="url(#lensClip)" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portfolio-nonprofit-fundraising-infographic.png"/>
  <circle cx="874" cy="430" r="88" fill="url(#lensTint)" stroke="#2C3E50" stroke-width="8"/>
  <circle cx="874" cy="430" r="72" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>
  <path d="M936 492 L1027 583" stroke="#2C3E50" stroke-width="18" stroke-linecap="round"/>
  <path d="M936 492 L1027 583" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.42"/>

  <rect x="915" y="86" width="250" height="76" rx="20" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <text x="940" y="116" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#E67E22">MAGNIFIED DETAIL</text>
  <text x="940" y="142" width="198" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#5D6D7E">Duplicate the screen image, enlarge it, then clip it to the circular lens.</text>

  <text x="1045" y="622" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#5D6D7E">Presenter cue:</text>
  <text x="1045" y="646" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7B8A9A">Assign each colored tab a PowerPoint hyperlink or trigger target.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<a>` links for navigation; add PowerPoint hyperlinks/triggers after translation instead.
- ❌ Do not use `<mask>` for the magnifying glass; use `<clipPath>` only on the duplicate `<image>`.
- ❌ Do not clip grouped SVG shapes to create the zoom lens; clipping non-image elements may be ignored by the translator.
- ❌ Do not use `<use>` to duplicate buttons or monitor controls; copy the actual shapes so PowerPoint keeps them editable.
- ❌ Do not rely on `marker-end` for arrows or pointers; if needed, draw arrowheads manually with small paths.

## Composition notes
- Keep the monitor as the dominant focal object, occupying roughly 55–65% of slide width and centered slightly right.
- Place navigation buttons in a stable left rail or bottom dock; use one active color and softer inactive colors to imply state.
- Use the magnifier over the most commercially important part of the example: CTA, KPI, testimonial, product detail, or UI action.
- Preserve generous pale negative space around the monitor so the slide feels like an interactive product demo, not a dense dashboard.