# SVG Recipe — Interactive Zoom Dashboard

## Visual mechanism
A dark executive “hub” slide presents a polished gallery of clickable section previews, each styled like a miniature slide with a label, status chip, and zoom affordance. The visual language implies non-linear navigation: the presenter can jump into any module and return to the dashboard.

## SVG primitives needed
- 1× `<rect>` for the full dark dashboard background
- 2× `<path>` for ambient curved glow bands behind the content
- 6× shadowed `<rect>` elements for thumbnail card bases
- 6× `<image>` elements clipped by rounded `<clipPath>` rectangles for slide-preview thumbnails
- 6× outlined `<rect>` elements for crisp clickable thumbnail borders
- 6× small `<circle>` or `<rect>` badges for section numbers / status chips
- 6× `<path>` icon glyphs for zoom/click affordances
- 8–12× `<text>` elements with explicit `width` for title, subtitle, labels, metrics, and navigation hints
- 2× `<linearGradient>` for background and card overlays
- 1× `<radialGradient>` for the central spotlight
- 2× `<filter>` definitions: soft shadow for cards and glow for active/accent elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="48%" stop-color="#101827"/>
      <stop offset="100%" stop-color="#05070D"/>
    </linearGradient>
    <radialGradient id="spotlight" cx="50%" cy="42%" r="65%">
      <stop offset="0%" stop-color="#2F80ED" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#2F80ED" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#2F80ED" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cardFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="68%" stop-color="#07111F" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#07111F" stop-opacity="0.82"/>
    </linearGradient>
    <linearGradient id="activeStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#58E6FF"/>
      <stop offset="50%" stop-color="#7C5CFF"/>
      <stop offset="100%" stop-color="#FFD166"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <clipPath id="clip1"><rect x="82" y="194" width="334" height="180" rx="22"/></clipPath>
    <clipPath id="clip2"><rect x="473" y="194" width="334" height="180" rx="22"/></clipPath>
    <clipPath id="clip3"><rect x="864" y="194" width="334" height="180" rx="22"/></clipPath>
    <clipPath id="clip4"><rect x="82" y="434" width="334" height="180" rx="22"/></clipPath>
    <clipPath id="clip5"><rect x="473" y="434" width="334" height="180" rx="22"/></clipPath>
    <clipPath id="clip6"><rect x="864" y="434" width="334" height="180" rx="22"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>
  <path d="M-80,172 C185,66 315,112 506,58 C724,-4 905,14 1365,-78 L1365,44 C984,116 789,100 585,160 C351,228 176,212 -80,300 Z"
        fill="#20D6FF" opacity="0.08" filter="url(#softGlow)"/>
  <path d="M-40,682 C214,550 392,666 604,570 C804,480 928,524 1322,404 L1322,720 L-40,720 Z"
        fill="#7C5CFF" opacity="0.10" filter="url(#softGlow)"/>

  <text x="70" y="66" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F5F7FB">Interactive Strategy Zoom Hub</text>
  <text x="72" y="100" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9AA7BD">Choose a module to zoom into the detailed slide, then return to this executive dashboard.</text>
  <rect x="1015" y="46" width="190" height="40" rx="20" fill="#FFFFFF" opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.18"/>
  <circle cx="1040" cy="66" r="6" fill="#3EF2C2"/>
  <text x="1055" y="72" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#DCE7F7">LIVE NAVIGATION</text>

  <line x1="86" y1="142" x2="1194" y2="142" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <text x="84" y="164" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#748196">SUMMARY ZOOM OBJECTS</text>
  <text x="1030" y="164" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#748196" text-anchor="end">CLICK ANY CARD TO ENTER</text>

  <rect x="76" y="188" width="346" height="234" rx="28" fill="#0D1726" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="82" y="194" width="334" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip1)"/>
  <rect x="82" y="194" width="334" height="180" rx="22" fill="url(#cardFade)"/>
  <rect x="82" y="194" width="334" height="180" rx="22" fill="none" stroke="url(#activeStroke)" stroke-width="2.5"/>
  <rect x="103" y="214" width="54" height="26" rx="13" fill="#07111F" opacity="0.78"/>
  <text x="119" y="233" width="25" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">01</text>
  <path d="M374,219 l15,0 l0,15 M389,219 l-23,23" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <text x="102" y="400" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F7FB">Company Overview</text>
  <text x="322" y="400" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#3EF2C2" text-anchor="end">4 slides</text>

  <rect x="467" y="188" width="346" height="234" rx="28" fill="#0D1726" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="473" y="194" width="334" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip2)"/>
  <rect x="473" y="194" width="334" height="180" rx="22" fill="url(#cardFade)"/>
  <rect x="473" y="194" width="334" height="180" rx="22" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>
  <rect x="494" y="214" width="54" height="26" rx="13" fill="#07111F" opacity="0.78"/>
  <text x="510" y="233" width="25" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">02</text>
  <path d="M765,219 l15,0 l0,15 M780,219 l-23,23" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <text x="493" y="400" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F7FB">Market Signals</text>
  <text x="713" y="400" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9AA7BD" text-anchor="end">6 slides</text>

  <rect x="858" y="188" width="346" height="234" rx="28" fill="#0D1726" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="864" y="194" width="334" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip3)"/>
  <rect x="864" y="194" width="334" height="180" rx="22" fill="url(#cardFade)"/>
  <rect x="864" y="194" width="334" height="180" rx="22" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>
  <rect x="885" y="214" width="54" height="26" rx="13" fill="#07111F" opacity="0.78"/>
  <text x="901" y="233" width="25" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">03</text>
  <path d="M1156,219 l15,0 l0,15 M1171,219 l-23,23" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <text x="884" y="400" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F7FB">Customer Journey</text>
  <text x="1104" y="400" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9AA7BD" text-anchor="end">5 slides</text>

  <rect x="76" y="428" width="346" height="234" rx="28" fill="#0D1726" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="82" y="434" width="334" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip4)"/>
  <rect x="82" y="434" width="334" height="180" rx="22" fill="url(#cardFade)"/>
  <rect x="82" y="434" width="334" height="180" rx="22" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>
  <rect x="103" y="454" width="54" height="26" rx="13" fill="#07111F" opacity="0.78"/>
  <text x="119" y="473" width="25" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">04</text>
  <path d="M374,459 l15,0 l0,15 M389,459 l-23,23" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <text x="102" y="640" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F7FB">Financial Model</text>
  <text x="322" y="640" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9AA7BD" text-anchor="end">7 slides</text>

  <rect x="467" y="428" width="346" height="234" rx="28" fill="#0D1726" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="473" y="434" width="334" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip5)"/>
  <rect x="473" y="434" width="334" height="180" rx="22" fill="url(#cardFade)"/>
  <rect x="473" y="434" width="334" height="180" rx="22" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>
  <rect x="494" y="454" width="54" height="26" rx="13" fill="#07111F" opacity="0.78"/>
  <text x="510" y="473" width="25" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">05</text>
  <path d="M765,459 l15,0 l0,15 M780,459 l-23,23" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <text x="493" y="640" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F7FB">Operating Plan</text>
  <text x="713" y="640" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9AA7BD" text-anchor="end">8 slides</text>

  <rect x="858" y="428" width="346" height="234" rx="28" fill="#0D1726" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=900&amp;q=80" x="864" y="434" width="334" height="180" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip6)"/>
  <rect x="864" y="434" width="334" height="180" rx="22" fill="url(#cardFade)"/>
  <rect x="864" y="434" width="334" height="180" rx="22" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>
  <rect x="885" y="454" width="54" height="26" rx="13" fill="#07111F" opacity="0.78"/>
  <text x="901" y="473" width="25" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">06</text>
  <path d="M1156,459 l15,0 l0,15 M1171,459 l-23,23" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
  <text x="884" y="640" width="215" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F7FB">Roadmap & Risks</text>
  <text x="1104" y="640" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9AA7BD" text-anchor="end">5 slides</text>
</svg>
```

## Avoid in this skill
- ❌ Relying on SVG alone to create the actual PowerPoint Summary Zoom relationship; the SVG should build the editable visual hub, while PowerPoint Zoom links / hyperlinks are assigned afterward.
- ❌ Using `<animate>` or `<animateTransform>` to fake the zoom transition; PowerPoint should handle the cinematic zoom behavior natively.
- ❌ Applying `clip-path` to card rectangles or groups; only clip the thumbnail `<image>` elements.
- ❌ Using `<use>` / `<symbol>` for repeated card components; duplicate the editable shapes directly so PPT-Master can translate them safely.
- ❌ Putting `filter` on `<line>` elements for connectors or dividers; use filters only on cards, paths, text, circles, rectangles, or ellipses.

## Composition notes
- Keep the title and navigation status in the top 15–18% of the slide; the dashboard grid should dominate the remaining area.
- Use a dark background with luminous blue/purple accents so thumbnail previews read as interactive objects.
- Make the first or current module visually “active” with a gradient stroke or glow; keep the other cards restrained with thin translucent borders.
- Leave consistent gutters between cards, and reserve a small bottom strip inside each card for labels, slide counts, or section metadata.