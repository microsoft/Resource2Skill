# SVG Recipe — Geometric Glass-Shard Reveal

## Visual mechanism
A dark, typography-heavy slide is “broken open” by acute triangular image crops that reveal a cinematic photo on the right. Semi-transparent angular overlays and dark diagonal divider bars create the illusion of layered glass shards over a flat executive-keynote background.

## SVG primitives needed
- 1× `<rect>` for the full-slide midnight gradient background.
- 3× `<clipPath>` with `<path>` geometry for independent triangular photo shards.
- 3× `<image>` copies of the same hero photo, each clipped to a shard window.
- 1× large `<path>` for the dark chevron/negative-space panel that cuts into the image.
- 2× dark `<path>` diagonal bars for the “cracked glass” X-shaped seams.
- 5× translucent `<path>` overlays for pale glass-refraction facets.
- 1× oversized low-opacity `<text>` watermark icon for background texture.
- 4× main `<text>` elements for year, headline, script accent, and small caption.
- 1× `<circle>`, 2× `<rect>`, and 3× `<path>` elements for an editable orange PowerPoint-style badge.
- 3× `<linearGradient>` definitions for background, gold headline, and orange badge color.
- 2× `<filter>` definitions using `feOffset`, `feGaussianBlur`, and `feMerge` for heavy title/drop shadows and panel depth.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A2434"/>
      <stop offset="55%" stop-color="#0E1B27"/>
      <stop offset="100%" stop-color="#070A0F"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFD84A"/>
      <stop offset="58%" stop-color="#FFC400"/>
      <stop offset="100%" stop-color="#E3A400"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF7B45"/>
      <stop offset="100%" stop-color="#F04422"/>
    </linearGradient>

    <filter id="titleShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="7" dy="7" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="1.2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="paneShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="12" dy="0" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="liftShadow" x="-20%" y="-40%" width="150%" height="160%">
      <feOffset dx="0" dy="-5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="1.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="shardTop" clipPathUnits="userSpaceOnUse">
      <path d="M485 -20 L1285 -20 L960 270 L780 420 Z"/>
    </clipPath>
    <clipPath id="shardRight" clipPathUnits="userSpaceOnUse">
      <path d="M960 270 L1285 -20 L1285 740 L1170 740 L780 420 Z"/>
    </clipPath>
    <clipPath id="shardBottom" clipPathUnits="userSpaceOnUse">
      <path d="M600 740 L1170 740 L780 420 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="-6" y="360" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="330" font-weight="700" fill="#FFFFFF" opacity="0.055"
        transform="rotate(-20 220 260)">✈</text>

  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=1600&amp;auto=format&amp;fit=crop"
         x="430" y="-40" width="900" height="800" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#shardTop)" opacity="0.94"/>
  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=1600&amp;auto=format&amp;fit=crop"
         x="430" y="-40" width="900" height="800" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#shardRight)" opacity="0.88"/>
  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&amp;w=1600&amp;auto=format&amp;fit=crop"
         x="430" y="-40" width="900" height="800" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#shardBottom)" opacity="0.80"/>

  <path d="M0 0 L490 0 L760 420 L600 720 L0 720 Z" fill="#0A2130" filter="url(#paneShadow)"/>

  <path d="M560 0 L718 0 L935 300 L780 420 Z" fill="#E9FFFF" opacity="0.12"/>
  <path d="M835 0 L1035 0 L920 270 Z" fill="#D9FFFF" opacity="0.10"/>
  <path d="M1085 0 L1280 0 L1185 205 Z" fill="#BDEFFF" opacity="0.09"/>
  <path d="M795 424 L942 720 L720 720 Z" fill="#D7FFFF" opacity="0.13"/>
  <path d="M870 430 L1280 560 L1280 720 L1035 720 Z" fill="#B7F5FF" opacity="0.08"/>

  <path d="M1064 -20 L1090 -20 L781 421 L755 421 Z" fill="#081B27" opacity="0.96"/>
  <path d="M760 405 L785 397 L1192 740 L1154 740 Z" fill="#081B27" opacity="0.96"/>

  <text x="58" y="235" width="510" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="150" font-weight="900" letter-spacing="7" fill="#FFFFFF"
        filter="url(#titleShadow)">2024</text>
  <text x="52" y="392" width="600" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="145" font-weight="900" letter-spacing="-5" fill="url(#goldGrad)"
        filter="url(#titleShadow)">SLIDE</text>
  <text x="340" y="452" width="310" font-family="Segoe Script, Segoe UI, Microsoft YaHei, cursive"
        font-size="70" font-weight="700" fill="#FFFFFF" filter="url(#liftShadow)">design</text>
  <text x="64" y="96" width="440" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" letter-spacing="4" fill="#8FB7C8" opacity="0.85">
    GEOMETRIC GLASS-SHARD REVEAL
  </text>

  <circle cx="225" cy="572" r="170" fill="#FF7A3D" opacity="0.96"/>
  <path d="M225 402 A170 170 0 0 1 395 572 L225 572 Z" fill="#FFC28A" opacity="0.65"/>
  <path d="M225 572 L395 572 A170 170 0 0 1 225 742 Z" fill="#F25728" opacity="0.74"/>
  <path d="M55 572 A170 170 0 0 1 225 402 L225 572 Z" fill="#FF9A5C" opacity="0.40"/>

  <rect x="12" y="487" width="204" height="200" rx="16" fill="#8E2D16" opacity="0.35"/>
  <rect x="-6" y="467" width="214" height="205" rx="16" fill="url(#orangeGrad)" filter="url(#paneShadow)"/>
  <text x="56" y="626" width="110" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="154" font-weight="900" fill="#FFFFFF">P</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to reveal the photo; use multiple `<image>` elements with `clip-path` applied directly to each image.
- ❌ Do not apply `clip-path` to dark panels, glass overlays, or text; clipping is reliable here only on `<image>`.
- ❌ Do not use `<use>` for repeating shards or logo elements; duplicate the editable shapes explicitly.
- ❌ Do not build diagonal seams with `marker-end` arrows or filtered `<line>` elements; use filled `<path>` quadrilaterals for thick cracks.
- ❌ Do not flatten the entire shard composition into one PNG; keep text, panels, shards, and overlays editable.

## Composition notes
- Reserve the left 45–50% for massive typography and negative space; let the image shards dominate the right half.
- Make the dark chevron’s point land near the visual center-right so it acts as a leading line into the photo.
- Use only a few glass overlays, with low opacity, so the photo remains legible and cinematic rather than foggy.
- Keep the palette disciplined: midnight navy base, icy cyan shard highlights, white title text, and one warm accent color for emphasis.