# SVG Recipe — Neumorphic Soft UI Styling

## Visual mechanism
Neumorphic Soft UI uses same-color surfaces and dual offset blurs: a white glow up-left and a cool gray shadow down-right, making cards feel gently extruded from the background. Keep contrast low, corners highly rounded, and reserve accent color for content rather than container borders.

## SVG primitives needed
- 1× `<rect>` for the full soft-gray canvas background.
- 3× large rounded `<rect>` layers for the hero title pill: white blurred shadow, gray blurred shadow, and top surface.
- 9× rounded `<rect>` layers for three raised dashboard cards using the same dual-shadow stack.
- 9× `<circle>` layers for three raised circular icon buttons.
- 3× `<path>` icon glyphs drawn with accent strokes inside the icon buttons.
- 8× `<text>` elements with explicit `width` attributes for title, eyebrow, metric values, and labels.
- 2× `<filter>` definitions using `feGaussianBlur` for large and medium soft shadows.
- 1× `<linearGradient>` for a very subtle surface highlight on raised objects.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="surfaceGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f8fb"/>
      <stop offset="48%" stop-color="#eef0f5"/>
      <stop offset="100%" stop-color="#e7ebf2"/>
    </linearGradient>

    <filter id="blurLarge" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>

    <filter id="blurMedium" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>

  <!-- base field -->
  <rect x="0" y="0" width="1280" height="720" fill="#eef0f5"/>

  <!-- soft ambient decoration -->
  <circle cx="1088" cy="126" r="168" fill="#ffffff" opacity="0.22" filter="url(#blurLarge)"/>
  <circle cx="164" cy="610" r="190" fill="#dce2ec" opacity="0.24" filter="url(#blurLarge)"/>

  <!-- small raised breadcrumb pill -->
  <rect x="477" y="118" width="326" height="46" rx="23" fill="#ffffff" opacity="0.9" filter="url(#blurMedium)"/>
  <rect x="493" y="134" width="326" height="46" rx="23" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <rect x="485" y="126" width="326" height="46" rx="23" fill="url(#surfaceGrad)"/>
  <text x="648" y="156" width="326" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700"
        letter-spacing="3" fill="#85c1b8">SOFT UI SYSTEM</text>

  <!-- hero neumorphic title pill -->
  <rect x="250" y="190" width="780" height="170" rx="85" fill="#ffffff" opacity="0.96" filter="url(#blurLarge)"/>
  <rect x="290" y="230" width="780" height="170" rx="85" fill="#c8cdd7" opacity="0.78" filter="url(#blurLarge)"/>
  <rect x="270" y="210" width="780" height="170" rx="85" fill="url(#surfaceGrad)"/>

  <text x="640" y="286" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="60" font-weight="800"
        letter-spacing="8" fill="#7fb0c2">
    <tspan x="640" dy="0">NEUMORPHIC</tspan>
    <tspan x="640" dy="76">PRESENTATION</tspan>
  </text>

  <!-- card 1 -->
  <rect x="147" y="438" width="286" height="150" rx="40" fill="#ffffff" opacity="0.9" filter="url(#blurMedium)"/>
  <rect x="175" y="466" width="286" height="150" rx="40" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <rect x="161" y="452" width="286" height="150" rx="40" fill="#eef0f5"/>

  <circle cx="223" cy="518" r="36" fill="#ffffff" opacity="0.92" filter="url(#blurMedium)"/>
  <circle cx="241" cy="536" r="36" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <circle cx="232" cy="527" r="36" fill="url(#surfaceGrad)"/>
  <path d="M213 531 L222 519 L232 536 L246 508 L257 523"
        fill="none" stroke="#85c1b8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="294" y="516" width="126" font-family="Segoe UI, Microsoft YaHei"
        font-size="38" font-weight="800" fill="#85c1b8">42%</text>
  <text x="294" y="552" width="136" font-family="Segoe UI, Microsoft YaHei"
        font-size="15" font-weight="600" letter-spacing="1.6" fill="#7a8599">LESS NOISE</text>

  <!-- card 2 -->
  <rect x="497" y="438" width="286" height="150" rx="40" fill="#ffffff" opacity="0.9" filter="url(#blurMedium)"/>
  <rect x="525" y="466" width="286" height="150" rx="40" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <rect x="511" y="452" width="286" height="150" rx="40" fill="#eef0f5"/>

  <circle cx="573" cy="518" r="36" fill="#ffffff" opacity="0.92" filter="url(#blurMedium)"/>
  <circle cx="591" cy="536" r="36" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <circle cx="582" cy="527" r="36" fill="url(#surfaceGrad)"/>
  <path d="M558 533 C558 522 566 516 576 518 C580 507 597 507 603 519 C612 520 619 526 619 535 C619 544 612 550 602 550 L569 550 C562 550 558 543 558 533 Z"
        fill="none" stroke="#85c1b8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="644" y="516" width="126" font-family="Segoe UI, Microsoft YaHei"
        font-size="38" font-weight="800" fill="#85c1b8">3.8×</text>
  <text x="644" y="552" width="136" font-family="Segoe UI, Microsoft YaHei"
        font-size="15" font-weight="600" letter-spacing="1.6" fill="#7a8599">APP FEEL</text>

  <!-- card 3 -->
  <rect x="847" y="438" width="286" height="150" rx="40" fill="#ffffff" opacity="0.9" filter="url(#blurMedium)"/>
  <rect x="875" y="466" width="286" height="150" rx="40" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <rect x="861" y="452" width="286" height="150" rx="40" fill="#eef0f5"/>

  <circle cx="923" cy="518" r="36" fill="#ffffff" opacity="0.92" filter="url(#blurMedium)"/>
  <circle cx="941" cy="536" r="36" fill="#c8cdd7" opacity="0.72" filter="url(#blurMedium)"/>
  <circle cx="932" cy="527" r="36" fill="url(#surfaceGrad)"/>
  <path d="M932 500 L954 510 L950 532 C947 546 940 554 932 558 C924 554 917 546 914 532 L910 510 Z M921 529 L929 537 L945 519"
        fill="none" stroke="#85c1b8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="994" y="516" width="126" font-family="Segoe UI, Microsoft YaHei"
        font-size="38" font-weight="800" fill="#85c1b8">98</text>
  <text x="994" y="552" width="136" font-family="Segoe UI, Microsoft YaHei"
        font-size="15" font-weight="600" letter-spacing="1.6" fill="#7a8599">TRUST SCORE</text>
</svg>
```

## Avoid in this skill
- ❌ Hard black borders around cards; neumorphism depends on shadow contrast, not outlines.
- ❌ Pure white canvas with dark shadows; use a tinted gray background so both white and gray shadows are visible.
- ❌ Tiny corner radii; squared cards make the effect feel like flat dashboard boxes instead of soft molded surfaces.
- ❌ Applying only one drop shadow to the top surface; the premium tactile effect requires both a top-left highlight and bottom-right shadow.
- ❌ Overcrowding the slide; blurred shadows need breathing room or they merge into visual mud.

## Composition notes
- Keep the background and object fills nearly identical: `#eef0f5` is the base, with only subtle gradient variation on raised surfaces.
- Place the largest neumorphic object near the center with generous margins; the soft shadow halo is part of its footprint.
- Use accent color sparingly for title text, icons, and metric values; containers should remain quiet and low contrast.
- Maintain symmetrical spacing and large rounded corners so the slide reads as a premium app interface rather than a conventional chart layout.