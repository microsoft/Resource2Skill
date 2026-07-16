# SVG Recipe — Text-Behind-Scenery Reveal

## Visual mechanism
Layer a giant solid title between a full-bleed sky background and a transparent PNG foreground landscape, then place an exact hollow-outline duplicate of the title on top. In PowerPoint, make a second “start” slide with the title/scenery off-canvas and use Morph to create the cinematic reveal; the SVG represents the polished end-state.

## SVG primitives needed
- 2× `<image>` for the full-slide sky background and transparent foreground scenery PNG
- 2× `<text>` for the giant title: one solid white mid-layer, one white outline foreground duplicate
- 3× `<rect>` for atmospheric color grading overlays and bottom navigation pills
- 3× `<path>` for small bird silhouettes and subtle scenic atmosphere accents
- 1× `<linearGradient id="sunsetGrade">` for warm-to-purple cinematic color grading
- 1× `<radialGradient id="sunGlow">` for sunset glow behind the title
- 1× `<filter id="softShadow">` applied to UI pills and title for depth
- 1× `<filter id="hazeBlur">` applied to distant haze shapes
- 1× `<clipPath>` with rounded rect applied to the flag image button accent
- 1× `<image>` clipped inside the flag capsule accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sunsetGrade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f07a24" stop-opacity="0.72"/>
      <stop offset="42%" stop-color="#c94b4b" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#24143d" stop-opacity="0.72"/>
    </linearGradient>

    <radialGradient id="sunGlow" cx="42%" cy="42%" r="58%">
      <stop offset="0%" stop-color="#fff0b8" stop-opacity="0.55"/>
      <stop offset="36%" stop-color="#ff9b3d" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#2b1746" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="bottomFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#12091e" stop-opacity="0"/>
      <stop offset="72%" stop-color="#12091e" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#12091e" stop-opacity="0.68"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="hazeBlur" x="-10%" y="-20%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>

    <clipPath id="flagClip">
      <rect x="1006" y="598" width="58" height="36" rx="18"/>
    </clipPath>
  </defs>

  <!-- Background sky layer -->
  <image
    href="https://images.example.com/cinematic-amazon-sunset-sky-full-bleed.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Cinematic grading over the sky -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#sunsetGrade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#sunGlow)"/>

  <!-- Distant haze and birds, still behind the title -->
  <path d="M0,493 C150,455 260,482 384,458 C522,431 648,456 762,430 C918,394 1068,432 1280,392 L1280,720 L0,720 Z"
        fill="#ffffff" opacity="0.10" filter="url(#hazeBlur)"/>
  <path d="M918,128 C936,114 951,113 966,127 C950,122 936,123 918,128 Z" fill="#ffffff" opacity="0.62"/>
  <path d="M1002,164 C1018,151 1035,151 1052,165 C1034,160 1019,160 1002,164 Z" fill="#ffffff" opacity="0.46"/>

  <!-- Mid-ground solid title: this sits behind the transparent scenery -->
  <text x="640" y="382"
        width="1120"
        text-anchor="middle"
        font-family="Segoe UI, Arial Black, Microsoft YaHei, sans-serif"
        font-size="178"
        font-weight="900"
        letter-spacing="-8"
        fill="#ffffff"
        opacity="0.96"
        filter="url(#softShadow)">BRAZIL</text>

  <!-- Foreground scenery with transparent sky already cut out -->
  <image
    href="https://images.example.com/transparent-rio-mountains-rainforest-foreground.png"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Dark grounding fade over the lower landscape -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomFade)"/>

  <!-- Foreground hollow duplicate of the exact same title -->
  <text x="640" y="382"
        width="1120"
        text-anchor="middle"
        font-family="Segoe UI, Arial Black, Microsoft YaHei, sans-serif"
        font-size="178"
        font-weight="900"
        letter-spacing="-8"
        fill="none"
        stroke="#ffffff"
        stroke-width="3.2"
        stroke-linejoin="round"
        opacity="0.94">BRAZIL</text>

  <!-- Small UI/navigation elements for a polished hero-slide finish -->
  <rect x="84" y="588" width="196" height="54" rx="27" fill="#ffffff" opacity="0.92" filter="url(#softShadow)"/>
  <text x="122" y="623"
        width="128"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="700"
        fill="#3e3e46">Explore</text>

  <rect x="976" y="588" width="220" height="54" rx="27" fill="#ffffff" opacity="0.92" filter="url(#softShadow)"/>
  <image
    href="https://images.example.com/brazil-flag-small.png"
    x="1006" y="598" width="58" height="36"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#flagClip)"/>
  <text x="1078" y="623"
        width="96"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="700"
        fill="#3e3e46">Rio route</text>

  <!-- Final foreground glint on the title edge -->
  <path d="M297,250 C420,236 529,238 642,244 C764,251 879,246 1004,230"
        fill="none"
        stroke="#ffffff"
        stroke-width="2"
        stroke-linecap="round"
        opacity="0.22"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the reveal; create start/end slides and use PowerPoint Morph instead.
- ❌ Do not use `<mask>` to cut the scenery or title; use a pre-cut transparent PNG for the foreground landscape.
- ❌ Do not apply `clip-path` to text or paths for the hollow-title effect; use a duplicate `<text>` with `fill="none"` and `stroke`.
- ❌ Do not use `<textPath>` for the title; keep both title layers as identical standard `<text>` elements so Morph can align them cleanly.
- ❌ Do not put the scenery image behind both title layers; the key depth illusion requires `[sky] → [solid title] → [transparent scenery] → [outline title]`.

## Composition notes
- Keep the title enormous, centered, and spanning roughly 65–85% of the slide width; the landscape should visibly cross through the letter interiors.
- Use a sky image with strong gradients or sunset color, because the text must read clearly before the foreground scenery appears.
- The foreground PNG should contain only mountains, trees, skyline, or architecture with the sky removed; soft alpha edges make the reveal feel premium.
- For Morph, make slide 1 contain the same background sky, with the title/scenery/UI positioned just outside the canvas; slide 2 uses the final positions shown above.