# SVG Recipe — Corporate Color Block & Masonry Hero Slide

## Visual mechanism
A premium asymmetric title slide pairs oversized corporate typography on the left with a tightly packed masonry photo collage on the right. Subtle geometric background marks, floating plum/coral color blocks, and shadowed photo cards create depth while preserving a clean executive keynote feel.

## SVG primitives needed
- 1× `<rect>` for the off-white full-slide background
- 1× `<path>` for the subtle repeated plus-sign geometric background texture
- 5× `<rect>` for soft floating accent blocks behind text and images
- 6× `<rect>` for white shadow-card bases behind the masonry images
- 6× `<image>` clipped into rectangular masonry tiles
- 6× `<clipPath>` with `<rect rx="...">` for rounded photo crops
- 1× `<linearGradient>` for the large pale title block
- 1× `<radialGradient>` for a faint coral glow accent
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` for photo-card depth
- 1× `<filter id="softGlow">` with `feGaussianBlur` for ambient accent glow
- 1× `<line>` for the thin text divider
- 4× `<text>` elements with explicit `width` attributes for title, subtitle, eyebrow, and caption

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="titleBlockGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2F2F2"/>
      <stop offset="100%" stop-color="#E7E7E7"/>
    </linearGradient>

    <radialGradient id="coralGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F4988C" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#F4988C" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="135%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.16  0 0 0 0 0.12  0 0 0 0 0.14  0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>

    <clipPath id="clipMain" clipPathUnits="userSpaceOnUse">
      <rect x="626" y="86" width="318" height="512" rx="10"/>
    </clipPath>
    <clipPath id="clipTop" clipPathUnits="userSpaceOnUse">
      <rect x="972" y="76" width="230" height="174" rx="10"/>
    </clipPath>
    <clipPath id="clipMid" clipPathUnits="userSpaceOnUse">
      <rect x="972" y="278" width="188" height="158" rx="10"/>
    </clipPath>
    <clipPath id="clipBottom" clipPathUnits="userSpaceOnUse">
      <rect x="942" y="466" width="260" height="142" rx="10"/>
    </clipPath>
    <clipPath id="clipSmallA" clipPathUnits="userSpaceOnUse">
      <rect x="558" y="492" width="180" height="116" rx="10"/>
    </clipPath>
    <clipPath id="clipSmallB" clipPathUnits="userSpaceOnUse">
      <rect x="760" y="616" width="178" height="74" rx="10"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F5F5"/>

  <path opacity="0.58" stroke="#E1E1E1" stroke-width="1.2" stroke-linecap="round" fill="none"
    d="M40 46h10M45 41v10 M120 46h10M125 41v10 M200 46h10M205 41v10 M280 46h10M285 41v10 M360 46h10M365 41v10 M440 46h10M445 41v10 M520 46h10M525 41v10 M600 46h10M605 41v10 M680 46h10M685 41v10 M760 46h10M765 41v10 M840 46h10M845 41v10 M920 46h10M925 41v10 M1000 46h10M1005 41v10 M1080 46h10M1085 41v10 M1160 46h10M1165 41v10
       M40 126h10M45 121v10 M120 126h10M125 121v10 M200 126h10M205 121v10 M280 126h10M285 121v10 M360 126h10M365 121v10 M440 126h10M445 121v10 M520 126h10M525 121v10 M600 126h10M605 121v10 M680 126h10M685 121v10 M760 126h10M765 121v10 M840 126h10M845 121v10 M920 126h10M925 121v10 M1000 126h10M1005 121v10 M1080 126h10M1085 121v10 M1160 126h10M1165 121v10
       M40 206h10M45 201v10 M120 206h10M125 201v10 M200 206h10M205 201v10 M280 206h10M285 201v10 M360 206h10M365 201v10 M440 206h10M445 201v10 M520 206h10M525 201v10 M600 206h10M605 201v10 M680 206h10M685 201v10 M760 206h10M765 201v10 M840 206h10M845 201v10 M920 206h10M925 201v10 M1000 206h10M1005 201v10 M1080 206h10M1085 201v10 M1160 206h10M1165 201v10
       M40 286h10M45 281v10 M120 286h10M125 281v10 M200 286h10M205 281v10 M280 286h10M285 281v10 M360 286h10M365 281v10 M440 286h10M445 281v10 M520 286h10M525 281v10 M600 286h10M605 281v10 M680 286h10M685 281v10 M760 286h10M765 281v10 M840 286h10M845 281v10 M920 286h10M925 281v10 M1000 286h10M1005 281v10 M1080 286h10M1085 281v10 M1160 286h10M1165 281v10
       M40 366h10M45 361v10 M120 366h10M125 361v10 M200 366h10M205 361v10 M280 366h10M285 361v10 M360 366h10M365 361v10 M440 366h10M445 361v10 M520 366h10M525 361v10 M600 366h10M605 361v10 M680 366h10M685 361v10 M760 366h10M765 361v10 M840 366h10M845 361v10 M920 366h10M925 361v10 M1000 366h10M1005 361v10 M1080 366h10M1085 361v10 M1160 366h10M1165 361v10
       M40 446h10M45 441v10 M120 446h10M125 441v10 M200 446h10M205 441v10 M280 446h10M285 441v10 M360 446h10M365 441v10 M440 446h10M445 441v10 M520 446h10M525 441v10 M600 446h10M605 441v10 M680 446h10M685 441v10 M760 446h10M765 441v10 M840 446h10M845 441v10 M920 446h10M925 441v10 M1000 446h10M1005 441v10 M1080 446h10M1085 441v10 M1160 446h10M1165 441v10"/>

  <ellipse cx="236" cy="178" rx="170" ry="120" fill="url(#coralGlow)" filter="url(#softGlow)" opacity="0.9"/>
  <rect x="78" y="282" width="432" height="112" rx="0" fill="url(#titleBlockGrad)"/>
  <rect x="92" y="132" width="118" height="12" fill="#F4988C"/>
  <rect x="586" y="52" width="144" height="144" fill="#59324C"/>
  <rect x="1098" y="560" width="112" height="112" fill="#59324C"/>
  <rect x="516" y="478" width="98" height="98" fill="#F4988C" opacity="0.82"/>

  <rect x="626" y="86" width="318" height="512" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="972" y="76" width="230" height="174" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="972" y="278" width="188" height="158" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="942" y="466" width="260" height="142" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="558" y="492" width="180" height="116" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="760" y="616" width="178" height="74" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <image x="626" y="86" width="318" height="512" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMain)"
    href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=900&amp;q=80"/>
  <image x="972" y="76" width="230" height="174" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipTop)"
    href="https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&amp;fit=crop&amp;w=700&amp;q=80"/>
  <image x="972" y="278" width="188" height="158" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipMid)"
    href="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&amp;fit=crop&amp;w=700&amp;q=80"/>
  <image x="942" y="466" width="260" height="142" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipBottom)"
    href="https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&amp;fit=crop&amp;w=800&amp;q=80"/>
  <image x="558" y="492" width="180" height="116" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipSmallA)"
    href="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&amp;fit=crop&amp;w=700&amp;q=80"/>
  <image x="760" y="616" width="178" height="74" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipSmallB)"
    href="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&amp;fit=crop&amp;w=700&amp;q=80"/>

  <text x="84" y="118" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" letter-spacing="2.8" fill="#59324C">
    PRODUCT STRATEGY REVIEW
  </text>

  <text x="78" y="250" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#282828">
    <tspan x="78" y="250" fill="#F4988C">New Product</tspan>
    <tspan x="78" y="348" fill="#282828">Evaluation</tspan>
  </text>

  <line x1="82" y1="438" x2="298" y2="438" stroke="#282828" stroke-width="2" opacity="0.72"/>

  <text x="82" y="486" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="400" fill="#282828">
    Your Company Name
  </text>

  <text x="82" y="532" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6A6A6A">
    Market readiness, customer insight, and launch priorities for the next growth cycle.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<pattern>` for the background texture; PPT translation may drop pattern fills. Use a faint repeated `<path>` or individual editable marks instead.
- ❌ Do not clip `<rect>` overlays or gradient shapes; clipping is reliable only on `<image>` elements.
- ❌ Do not use `<use>` to repeat plus signs or photo frames; duplicate path segments directly.
- ❌ Do not apply filters to `<line>` elements; use filters only on cards, paths, text, circles, ellipses, or rectangles.
- ❌ Do not make the masonry grid perfectly even; the premium look comes from controlled asymmetry and overlapping accent blocks.

## Composition notes
- Keep the left 40–45% of the canvas mostly open for oversized title typography and a short subtitle.
- Let the masonry collage occupy the right 55%, with one dominant tall image and several smaller supporting crops.
- Place plum blocks partially behind the photo grid to create depth; use coral sparingly as a warm brand accent.
- The background texture should be barely visible: it should enrich the white space, not compete with text or images.