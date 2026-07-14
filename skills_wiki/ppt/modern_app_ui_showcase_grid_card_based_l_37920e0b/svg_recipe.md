# SVG Recipe — Modern App UI Showcase (Grid & Card-Based Layout with Glassmorphism)

## Visual mechanism
A light app-like canvas is organized on a strict grid with elevated rounded cards, clipped photo thumbnails, and reusable list rows. A semi-transparent “sticky” navigation bar floats over the content to simulate glassmorphism, using soft shadows, translucent fills, and subtle background color blooms.

## SVG primitives needed
- 1× `<rect>` for the full-slide cool-gray background
- 3× blurred `<ellipse>` for soft ambient color blooms behind the UI
- 1× `<rect>` for the translucent glassmorphism header
- 6× `<rect>` for white/elevated card containers and reusable list rows
- 4× `<image>` clipped to rounded rectangles for the horizontal gallery cards
- 3× `<image>` clipped to small rounded rectangles for list thumbnails
- 7× `<clipPath>` using `<rect rx>` for editable rounded image crops
- 1× `<linearGradient>` for the premium app accent button
- 1× `<linearGradient>` for the large featured card overlay tint
- 2× `<filter>` definitions: one soft UI shadow and one ambient blur
- Multiple `<text>` elements with explicit `width` for nav labels, headings, captions, metadata, and list content
- 1× `<path>` for a simple editable app/logo mark in the header
- 2× `<line>` for subtle card separators and header baseline

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6B6B"/>
      <stop offset="100%" stop-color="#FF2D55"/>
    </linearGradient>
    <linearGradient id="photoTint" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.48"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .13 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="ambientBlur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="38"/>
    </filter>

    <clipPath id="clipHero"><rect x="72" y="176" width="354" height="224" rx="30"/></clipPath>
    <clipPath id="clipCardA"><rect x="458" y="176" width="222" height="224" rx="30"/></clipPath>
    <clipPath id="clipCardB"><rect x="712" y="176" width="222" height="224" rx="30"/></clipPath>
    <clipPath id="clipCardC"><rect x="966" y="176" width="222" height="224" rx="30"/></clipPath>
    <clipPath id="clipThumb1"><rect x="92" y="495" width="78" height="78" rx="20"/></clipPath>
    <clipPath id="clipThumb2"><rect x="488" y="495" width="78" height="78" rx="20"/></clipPath>
    <clipPath id="clipThumb3"><rect x="884" y="495" width="78" height="78" rx="20"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F5F7"/>
  <ellipse cx="188" cy="138" rx="160" ry="95" fill="#BFE9FF" opacity="0.36" filter="url(#ambientBlur)"/>
  <ellipse cx="1032" cy="190" rx="210" ry="112" fill="#FFD6E7" opacity="0.42" filter="url(#ambientBlur)"/>
  <ellipse cx="814" cy="610" rx="190" ry="84" fill="#D9D0FF" opacity="0.34" filter="url(#ambientBlur)"/>

  <text x="72" y="140" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#1D1D1F">Museum Art App</text>
  <text x="72" y="168" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#86868B">Explore contemporary collections, member events, and curated exhibition paths.</text>

  <rect x="72" y="176" width="354" height="224" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="72" y="176" width="354" height="224" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipHero)"
         href="https://images.example.com/hero-photo-modern-gallery-sculpture.jpg"/>
  <rect x="72" y="176" width="354" height="224" rx="30" fill="url(#photoTint)" opacity="0.88"/>
  <text x="98" y="348" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#FFFFFF">New Nordic Forms</text>
  <text x="98" y="375" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.86">Featured collection · 42 works</text>
  <rect x="332" y="336" width="58" height="36" rx="18" fill="#FFFFFF" opacity="0.92"/>
  <text x="348" y="359" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#1D1D1F">View</text>

  <rect x="458" y="176" width="222" height="224" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="458" y="176" width="222" height="148" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCardA)"
         href="https://images.example.com/card-photo-colorful-abstract-painting.jpg"/>
  <text x="480" y="355" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1D1D1F">Abstract Light</text>
  <text x="480" y="378" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86868B">Gallery 2 · Today</text>

  <rect x="712" y="176" width="222" height="224" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="712" y="176" width="222" height="148" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCardB)"
         href="https://images.example.com/card-photo-interactive-digital-installation.jpg"/>
  <text x="734" y="355" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1D1D1F">Digital Echoes</text>
  <text x="734" y="378" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86868B">Immersive room</text>

  <rect x="966" y="176" width="222" height="224" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="966" y="176" width="222" height="148" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipCardC)"
         href="https://images.example.com/card-photo-minimal-architecture-exhibit.jpg"/>
  <text x="988" y="355" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1D1D1F">Spatial Study</text>
  <text x="988" y="378" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86868B">Architecture wing</text>

  <text x="72" y="462" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#1D1D1F">Upcoming events</text>
  <text x="1040" y="462" width="148" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#FF2D55">See all events</text>

  <rect x="72" y="474" width="344" height="126" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="92" y="495" width="78" height="78" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb1)"
         href="https://images.example.com/thumb-curator-talk-art-audience.jpg"/>
  <text x="190" y="520" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1D1D1F">Curator Walkthrough</text>
  <text x="190" y="546" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86868B">Fri 18:00 · Main hall</text>
  <rect x="330" y="535" width="54" height="30" rx="15" fill="#FFF1F4"/>
  <text x="344" y="555" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FF2D55">RSVP</text>

  <rect x="468" y="474" width="344" height="126" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="488" y="495" width="78" height="78" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb2)"
         href="https://images.example.com/thumb-workshop-painting-tools-table.jpg"/>
  <text x="586" y="520" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1D1D1F">Color Lab Workshop</text>
  <text x="586" y="546" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86868B">Sat 11:30 · Studio B</text>
  <rect x="726" y="535" width="54" height="30" rx="15" fill="#F1F7FF"/>
  <text x="741" y="555" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2477FF">New</text>

  <rect x="864" y="474" width="344" height="126" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="884" y="495" width="78" height="78" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipThumb3)"
         href="https://images.example.com/thumb-evening-museum-cafe-lights.jpg"/>
  <text x="982" y="520" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1D1D1F">Member Preview Night</text>
  <text x="982" y="546" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86868B">Thu 19:00 · Atrium</text>
  <rect x="1122" y="535" width="54" height="30" rx="15" fill="url(#accentGrad)"/>
  <text x="1137" y="555" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Hot</text>

  <rect x="36" y="24" width="1208" height="78" rx="28" fill="#FFFFFF" opacity="0.76" stroke="#FFFFFF" stroke-width="1.2" filter="url(#softShadow)"/>
  <line x1="64" y1="102" x2="1216" y2="102" stroke="#FFFFFF" stroke-width="1" opacity="0.72"/>
  <path d="M86 54 C92 42,110 42,116 54 C123 68,112 82,101 86 C90 82,79 68,86 54 Z" fill="url(#accentGrad)"/>
  <text x="132" y="72" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#1D1D1F">Artspace</text>
  <text x="530" y="72" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#1D1D1F">Explore</text>
  <text x="625" y="72" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#86868B">Exhibitions</text>
  <text x="742" y="72" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#86868B">Tickets</text>
  <rect x="1066" y="44" width="136" height="38" rx="19" fill="#1D1D1F"/>
  <text x="1095" y="68" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Get the app</text>
</svg>
```

## Avoid in this skill
- ❌ Real blur-behind glass using `<mask>` or clipping non-image content; simulate glass with translucent white rectangles, strokes, and shadows instead
- ❌ Applying `clip-path` to card `<rect>` elements; use rounded `<rect>` directly for cards and reserve clip paths for `<image>` crops
- ❌ Overusing heavy dark shadows; modern UI elevation should be soft, low-opacity, and spacious
- ❌ Building the layout without a grid; arbitrary card positions break the app-dashboard illusion
- ❌ Tiny text without explicit `width`; PowerPoint text boxes need predictable widths for editable rendering

## Composition notes
- Keep the top 10–14% of the slide for the sticky glass header; let it slightly overlap the content below for an app-like feel.
- Use a 3- or 4-column grid with consistent gutters; align card edges, list rows, and section headings to the same x positions.
- Reserve the strongest imagery for the first large gallery card, then use smaller cards and list rows to create hierarchy.
- Maintain a cool-gray background, white cards, charcoal text, muted secondary labels, and one vivid accent color for buttons/status pills.