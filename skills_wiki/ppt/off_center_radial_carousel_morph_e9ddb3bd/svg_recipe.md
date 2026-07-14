# SVG Recipe — Radial Carousel Showcase

## Visual mechanism
A large off-canvas circular track acts like a Ferris wheel, with product cards anchored to its circumference and one item enlarged at the horizontal “focus” point. Duplicate the slide and rotate the carousel group around the same off-screen pivot, then apply PowerPoint Morph to create the smooth radial carousel motion.

## SVG primitives needed
- 1× `<image>` for the full-bleed contextual background photo
- 3× `<rect>` for darkening overlay, vignette wash, and text-side panel tint
- 1× large `<circle>` for the off-screen carousel guide ring
- 5× `<circle>` for product plate bases and focus halos
- 5× `<image>` for clipped product / portfolio / team item visuals
- 5× `<clipPath>` with `<circle>` for circular item image crops
- 3× `<path>` for premium decorative glints, focus arc accent, and soft organic background glow
- 2× `<filter>` for editable soft shadows and subtle glow on shapes/text
- 3× gradients: dark vignette, gold accent, and translucent glass highlight
- Multiple `<text>` elements with explicit `width` for title, subtitle, item copy, and carousel index

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#050505" stop-opacity="0.92"/>
      <stop offset="45%" stop-color="#11100D" stop-opacity="0.68"/>
      <stop offset="100%" stop-color="#050505" stop-opacity="0.38"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8E6A0"/>
      <stop offset="48%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#8B6F1B"/>
    </linearGradient>
    <radialGradient id="glassGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="warmGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="clipFocus" clipPathUnits="userSpaceOnUse">
      <circle cx="460" cy="360" r="103"/>
    </clipPath>
    <clipPath id="clipTop" clipPathUnits="userSpaceOnUse">
      <circle cx="376" cy="22" r="72"/>
    </clipPath>
    <clipPath id="clipBottom" clipPathUnits="userSpaceOnUse">
      <circle cx="376" cy="698" r="72"/>
    </clipPath>
    <clipPath id="clipUpperGhost" clipPathUnits="userSpaceOnUse">
      <circle cx="143" cy="-243" r="58"/>
    </clipPath>
    <clipPath id="clipLowerGhost" clipPathUnits="userSpaceOnUse">
      <circle cx="143" cy="963" r="58"/>
    </clipPath>
  </defs>

  <image href="https://images.example.com/restaurant-chef-dark-kitchen-full-bleed.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgShade)"/>
  <rect x="620" y="0" width="660" height="720" fill="#050505" opacity="0.24"/>
  <path d="M724 84 C920 18 1122 64 1248 192 L1248 0 L724 0 Z" fill="url(#glassGlow)" opacity="0.55"/>
  <path d="M858 610 C1000 548 1158 560 1280 654 L1280 720 L800 720 C802 678 824 636 858 610 Z" fill="#D4AF37" opacity="0.10"/>

  <!-- Rotate this whole group around (-260,360) on duplicate slides: rotate(0), rotate(-28), rotate(-56)... -->
  <g id="carouselWheel" transform="rotate(0 -260 360)">
    <circle cx="-260" cy="360" r="720" fill="none" stroke="#FFFFFF" stroke-width="34" opacity="0.14"/>
    <circle cx="-260" cy="360" r="720" fill="none" stroke="#D4AF37" stroke-width="4" stroke-dasharray="18 28" opacity="0.45"/>
    <path d="M438 280 C486 296 518 326 536 360 C518 394 486 424 438 440" fill="none" stroke="url(#gold)" stroke-width="7" stroke-linecap="round" opacity="0.95"/>

    <g opacity="0.36">
      <circle cx="143" cy="-243" r="78" fill="#F4F0E8" filter="url(#softShadow)"/>
      <circle cx="143" cy="-243" r="61" fill="#FFFFFF" opacity="0.92"/>
      <image href="https://images.example.com/top-view-dessert-berry-tart.png" x="85" y="-301" width="116" height="116" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipUpperGhost)"/>
    </g>

    <g opacity="0.78">
      <circle cx="376" cy="22" r="94" fill="#F4F0E8" filter="url(#softShadow)"/>
      <circle cx="376" cy="22" r="76" fill="#FFFFFF" opacity="0.95"/>
      <image href="https://images.example.com/top-view-spicy-pumpkin-soup.png" x="304" y="-50" width="144" height="144" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipTop)"/>
    </g>

    <circle cx="460" cy="360" r="148" fill="#D4AF37" opacity="0.22" filter="url(#warmGlow)"/>
    <circle cx="460" cy="360" r="132" fill="#F8F5EC" filter="url(#softShadow)"/>
    <circle cx="460" cy="360" r="111" fill="#FFFFFF"/>
    <image href="https://images.example.com/top-view-signature-ramen-bowl.png" x="357" y="257" width="206" height="206" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipFocus)"/>
    <circle cx="460" cy="360" r="132" fill="none" stroke="url(#gold)" stroke-width="5"/>

    <g opacity="0.78">
      <circle cx="376" cy="698" r="94" fill="#F4F0E8" filter="url(#softShadow)"/>
      <circle cx="376" cy="698" r="76" fill="#FFFFFF" opacity="0.95"/>
      <image href="https://images.example.com/top-view-roasted-herb-potatoes.png" x="304" y="626" width="144" height="144" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipBottom)"/>
    </g>

    <g opacity="0.36">
      <circle cx="143" cy="963" r="78" fill="#F4F0E8" filter="url(#softShadow)"/>
      <circle cx="143" cy="963" r="61" fill="#FFFFFF" opacity="0.92"/>
      <image href="https://images.example.com/top-view-matcha-cheesecake.png" x="85" y="905" width="116" height="116" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipLowerGhost)"/>
    </g>
  </g>

  <text x="690" y="126" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" letter-spacing="3" fill="#D4AF37">CHEF’S ROTATING SELECTION</text>
  <text x="690" y="206" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="700" fill="#FFFFFF">
    Signature<tspan x="690" dy="68" fill="url(#gold)">Ramen</tspan>
  </text>
  <text x="692" y="356" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="23" fill="#F2EFE7" opacity="0.94">
    Rich pork broth, slow-braised chashu, marinated egg, spring onion, and hand-pulled noodles presented as the hero item of the carousel.
  </text>
  <line x1="692" y1="456" x2="880" y2="456" stroke="#D4AF37" stroke-width="3"/>
  <text x="692" y="502" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF" opacity="0.72">
    Duplicate this slide, rotate the wheel group by equal angle steps, then apply Morph for a premium rotating showcase.
  </text>
  <text x="1102" y="632" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#D4AF37" text-anchor="end">01 / 05</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the carousel; create separate slide states and rely on PowerPoint Morph.
- ❌ Do not use `<use>` to repeat carousel items; duplicate each native group explicitly so the PPT shapes remain editable.
- ❌ Do not apply `clip-path` to groups or circles; only apply circular clips directly to `<image>` elements.
- ❌ Do not use `marker-end` on curved paths for motion arrows; if arrows are needed, use editable `<line>` arrows instead.
- ❌ Do not rotate each item independently unless intentional; Morph works best when the full wheel group rotates around one consistent off-canvas pivot.

## Composition notes
- Place the wheel center far off the left edge; only the right side of the circle should enter the slide, creating a graceful vertical arc.
- Keep the active item near the horizontal midpoint-left, enlarged and haloed; reserve the right half for headline, description, and index.
- Use semi-transparent whites for the track and warm gold for the active arc so the carousel feels premium rather than mechanical.
- For Morph slides, preserve identical element IDs/order and only change the `rotate(angle -260 360)` value plus the active text content.