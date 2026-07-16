# SVG Recipe — Playful Hero Cover

## Visual mechanism
A calm left text column is counterbalanced by a large floating hero image on the right, cropped into a playful organic shape with a soft shadow. A top-hanging accent block and small geometric confetti add motion and personality without making the cover feel busy.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm background
- 1× `<rect>` for the top-hanging accent block
- 2× `<rect>` for small pill accents near the headline
- 1× `<image>` for the hero photo, clipped into an organic blob
- 1× `<clipPath>` with a `<path>` for the irregular hero-image crop
- 3× `<path>` for the hero blob frame, background organic color wash, and curved decorative stroke
- 8× `<circle>` for playful dots and floating accents
- 3× `<text>` blocks with explicit `width` for eyebrow, headline, and subhead
- 2× `<linearGradient>` fills for background and accent color depth
- 1× `<radialGradient>` for a soft color glow behind the hero
- 2× `<filter>` definitions for soft shadow and glow effects applied to shapes/text-safe elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWarm" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF7E8"/>
      <stop offset="48%" stop-color="#FFF2DD"/>
      <stop offset="100%" stop-color="#F8FBFF"/>
    </linearGradient>

    <linearGradient id="coralBlock" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FF8A68"/>
      <stop offset="100%" stop-color="#FF5A7A"/>
    </linearGradient>

    <radialGradient id="heroGlow" cx="50%" cy="50%" r="58%">
      <stop offset="0%" stop-color="#FFD36E" stop-opacity="0.55"/>
      <stop offset="65%" stop-color="#FFB2C8" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="heroBlobClip">
      <path d="M842 182
               C905 116 1032 112 1090 180
               C1146 246 1133 363 1190 424
               C1242 480 1189 607 1080 624
               C974 641 895 591 842 627
               C785 665 704 599 706 512
               C708 431 759 398 744 329
               C731 269 781 245 842 182 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWarm)"/>

  <circle cx="985" cy="370" r="285" fill="url(#heroGlow)" filter="url(#softGlow)"/>

  <path d="M-80 625
           C155 535 260 690 455 585
           C600 507 662 410 800 462"
        fill="none"
        stroke="#FFD36E"
        stroke-width="30"
        stroke-linecap="round"
        opacity="0.32"/>

  <rect x="762" y="-18" width="178" height="205" rx="34"
        fill="url(#coralBlock)" filter="url(#softShadow)"/>
  <circle cx="850" cy="72" r="18" fill="#FFFFFF" opacity="0.55"/>
  <rect x="806" y="126" width="88" height="12" rx="6" fill="#FFFFFF" opacity="0.42"/>

  <path d="M820 166
           C893 94 1035 101 1105 174
           C1174 246 1161 354 1212 415
           C1270 484 1210 633 1084 653
           C974 671 889 620 835 652
           C764 695 672 615 680 511
           C687 418 734 389 718 321
           C702 250 748 236 820 166 Z"
        fill="#FFFFFF"
        filter="url(#softShadow)"/>

  <image x="675" y="92" width="575" height="575"
         href="https://images.example.com/playful-hero-cover/bright-founder-portrait-with-colorful-background.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroBlobClip)"/>

  <path d="M842 182
           C905 116 1032 112 1090 180
           C1146 246 1133 363 1190 424
           C1242 480 1189 607 1080 624
           C974 641 895 591 842 627
           C785 665 704 599 706 512
           C708 431 759 398 744 329
           C731 269 781 245 842 182 Z"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="16"
        stroke-linejoin="round"/>

  <circle cx="1135" cy="145" r="13" fill="#2BC4A9"/>
  <circle cx="1182" cy="199" r="7" fill="#1E6BFF"/>
  <circle cx="679" cy="202" r="10" fill="#FFC247"/>
  <circle cx="732" cy="615" r="8" fill="#FF5A7A"/>
  <circle cx="1208" cy="565" r="16" fill="#FFD36E" opacity="0.86"/>
  <circle cx="608" cy="122" r="6" fill="#2BC4A9" opacity="0.75"/>

  <rect x="86" y="138" width="96" height="14" rx="7" fill="#FF5A7A"/>
  <rect x="194" y="138" width="46" height="14" rx="7" fill="#FFD36E"/>

  <text x="86" y="118" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700"
        letter-spacing="3"
        fill="#1E6BFF">NEW SECTION</text>

  <text x="82" y="246" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="68" font-weight="800"
        line-height="1.05"
        fill="#182033">
    <tspan x="82" dy="0">Make the</tspan>
    <tspan x="82" dy="76">launch feel</tspan>
    <tspan x="82" dy="76" fill="#FF5A7A">irresistible.</tspan>
  </text>

  <text x="88" y="500" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="400"
        fill="#596170">
    <tspan x="88" dy="0">A playful executive cover with</tspan>
    <tspan x="88" dy="36">a floating hero image, warm color,</tspan>
    <tspan x="88" dy="36">and confident left-aligned copy.</tspan>
  </text>

  <circle cx="96" cy="628" r="6" fill="#1E6BFF"/>
  <circle cx="124" cy="628" r="6" fill="#FF5A7A"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the irregular hero crop; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not clip decorative paths or groups; keep clipping only on the hero `<image>` for reliable PowerPoint translation.
- ❌ Avoid a rigid rectangular photo card unless the brand requires it; the organic crop is what makes the cover playful.
- ❌ Avoid adding too many small icons around the title, which can reduce the premium keynote feel.
- ❌ Do not use `<textPath>` for curved labels; keep all title and subtitle text as normal editable `<text>` with explicit `width`.

## Composition notes
- Keep the left 45% of the slide mostly open for large, high-contrast headline text.
- Let the hero image occupy the right 48–52% of the canvas and slightly overlap the vertical centerline for energy.
- Use the top-hanging accent block as a counterweight above the image, not as a content container.
- Repeat 2–3 accent colors from the hero area in tiny dots or pills near the text to unify the composition.