# SVG Recipe — Product Reveal Split

## Visual mechanism
A premium split-cover layout: a tall 9:16 product/hero image anchors the left side while oversized, high-contrast typography commands the right. Subtle gradients, a glowing divider, and restrained metadata create a cinematic “new product reveal” feel without crowding the slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 1× `<linearGradient>` for the background color wash
- 1× `<clipPath>` with rounded `<rect>` for the vertical hero image crop
- 1× `<image>` for the 9:16 product/hero visual on the left
- 2× `<rect>` for the hero card shadow base and glassy highlight overlay
- 1× `<filter id="heroShadow">` applied to the hero card base
- 1× `<filter id="softGlow">` applied to the vertical reveal divider
- 2× `<line>` for the split divider and small accent ticks
- 3× `<path>` for abstract product-reveal glow shards behind the headline
- 6× `<text>` elements for kicker, headline, subtitle, metadata, launch date, and small label text
- 1× `<radialGradient>` for the ambient glow behind the right-side headline
- 1× `<linearGradient>` for metallic accent strokes/fills

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#070A10"/>
      <stop offset="0.55" stop-color="#101827"/>
      <stop offset="1" stop-color="#05070B"/>
    </linearGradient>

    <radialGradient id="headlineGlow" cx="760" cy="318" r="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4DA3FF" stop-opacity="0.30"/>
      <stop offset="0.42" stop-color="#1E5EFF" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="accentMetal" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#EAF3FF"/>
      <stop offset="0.45" stop-color="#69B7FF"/>
      <stop offset="1" stop-color="#2147FF"/>
    </linearGradient>

    <filter id="heroShadow" x="-30%" y="-20%" width="160%" height="150%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="94" y="54" width="344" height="612" rx="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#headlineGlow)"/>

  <path d="M690 92 C815 38 985 58 1105 154 C1010 139 862 162 742 246 C704 208 681 157 690 92 Z"
        fill="#245BFF" opacity="0.12"/>
  <path d="M835 515 C940 468 1084 468 1192 548 C1077 546 955 579 864 650 C831 611 820 563 835 515 Z"
        fill="#66D9FF" opacity="0.10"/>
  <path d="M584 382 C670 304 776 285 890 316 C776 360 702 418 650 500 C614 472 589 431 584 382 Z"
        fill="#FFFFFF" opacity="0.045"/>

  <rect x="94" y="54" width="344" height="612" rx="34" fill="#030508" filter="url(#heroShadow)" opacity="0.92"/>
  <image x="94" y="54" width="344" height="612"
         href="https://images.example.com/vertical-hero-photo-premium-black-smartphone-on-blue-light.jpg"
         clip-path="url(#heroClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="94" y="54" width="344" height="612" rx="34" fill="none" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1.4"/>
  <rect x="114" y="74" width="304" height="96" rx="26" fill="#FFFFFF" opacity="0.08"/>
  <rect x="114" y="536" width="304" height="96" rx="26" fill="#02050A" opacity="0.36"/>

  <line x1="545" y1="86" x2="545" y2="634" stroke="url(#accentMetal)" stroke-width="2.5" opacity="0.82" filter="url(#softGlow)"/>
  <line x1="566" y1="118" x2="566" y2="210" stroke="#8FD2FF" stroke-width="1.2" opacity="0.45" stroke-dasharray="10 12"/>
  <line x1="566" y1="510" x2="566" y2="602" stroke="#8FD2FF" stroke-width="1.2" opacity="0.45" stroke-dasharray="10 12"/>

  <text x="620" y="116" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="4" fill="#8FD2FF">
    PRODUCT REVEAL
  </text>

  <text x="618" y="252" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="800" fill="#F5F8FF">
    <tspan x="618" dy="0">NOVA</tspan>
    <tspan x="618" dy="88">EDGE</tspan>
  </text>

  <text x="622" y="420" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="500" fill="#D5DFEF" opacity="0.92">
    <tspan x="622" dy="0">A thinner, brighter flagship platform</tspan>
    <tspan x="622" dy="36">built for the next mobile AI era.</tspan>
  </text>

  <text x="622" y="528" width="440" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="2.2" fill="#FFFFFF" opacity="0.58">
    ULTRA-LIGHT BODY · PRO CAMERA · ON-DEVICE AI
  </text>

  <rect x="622" y="574" width="226" height="54" rx="27" fill="#FFFFFF" opacity="0.09"/>
  <rect x="622" y="574" width="226" height="54" rx="27" fill="none" stroke="#8FD2FF" stroke-opacity="0.35" stroke-width="1.2"/>
  <text x="652" y="608" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#F8FBFF">
    Launching 09.24
  </text>

  <text x="1050" y="634" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2" fill="#B8C7DA" opacity="0.62">
    SERIES 01
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` for the photo fade; use a clipped image plus editable gradient/transparent rectangles instead.
- ❌ Do not clip non-image shapes for the hero card overlay; PowerPoint translation may ignore clip paths on shapes.
- ❌ Do not build the divider glow with a filtered `<line>` if strict fidelity is required; use a narrow `<rect>` with blur instead when glow must survive all translators.
- ❌ Do not overcrowd the right panel with bullets; this layout works because the headline has room to breathe.
- ❌ Do not use `<textPath>` or animated reveal effects; keep the reveal implied through split composition, glow, and scale.

## Composition notes
- Keep the hero image between 25–32% of slide width, with generous top/bottom margins so the 9:16 crop feels intentional and cinematic.
- Put the headline in the right-center third; use two stacked words or a short phrase under 50 characters for maximum impact.
- Use a thin luminous divider to separate image and message, but leave at least 55–70 px of breathing room between divider and text.
- Maintain a dark, minimal palette with one electric accent color repeated in the divider, kicker, and CTA/date pill.