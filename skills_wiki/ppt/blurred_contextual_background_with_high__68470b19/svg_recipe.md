# SVG Recipe — Blurred Image Background with High-Contrast Text

## Visual mechanism
A contextual full-bleed photo is abstracted into a soft, cinematic color field with heavy blur, dark overlays, and vignette gradients. Large white typography sits centered above it, using a strong text shadow to guarantee legibility and keynote-style impact.

## SVG primitives needed
- 1× `<image>` for the full-slide blurred contextual background photo
- 1× `<rect>` for the dark contrast overlay across the entire slide
- 2× `<rect>` with gradient fills for top/bottom cinematic vignettes
- 3× `<circle>` with blur filters for soft ambient color blooms
- 1× `<filter id="textShadow">` using `feOffset + feGaussianBlur + feMerge` applied to title and subtitle text
- 1× `<filter id="colorBloom">` using `feGaussianBlur` applied to decorative glow circles
- 1× large centered `<text>` block with nested `<tspan>` lines for the hero title
- 1× small top-right `<text>` for minimalist brand/watermark
- 1× small centered `<text>` for supporting subtitle or section label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="topVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.70"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomVignette" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.78"/>
      <stop offset="52%" stop-color="#000000" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="centerLift" cx="50%" cy="48%" r="58%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.24"/>
    </radialGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feFlood flood-color="#000000" flood-opacity="0.68" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="colorBloom" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>
  </defs>

  <!-- Full-bleed contextual image: use an already blurred export for most reliable PPT rendering -->
  <image
    href="https://images.example.com/blurred-windows-desktop-workspace-1920x1080.jpg"
    x="-40" y="-30" width="1360" height="780"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Soft abstract color blooms reinforce the blurred-photo look -->
  <circle cx="210" cy="170" r="170" fill="#2D8CFF" opacity="0.34" filter="url(#colorBloom)"/>
  <circle cx="1035" cy="520" r="210" fill="#8A4DFF" opacity="0.30" filter="url(#colorBloom)"/>
  <circle cx="760" cy="105" r="145" fill="#00D6C9" opacity="0.22" filter="url(#colorBloom)"/>

  <!-- Contrast system: dimming layer + cinematic vignettes -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.38"/>
  <rect x="0" y="0" width="1280" height="300" fill="url(#topVignette)"/>
  <rect x="0" y="380" width="1280" height="340" fill="url(#bottomVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerLift)" opacity="0.9"/>

  <!-- Minimal watermark / brand in the extreme top-right -->
  <text x="1168" y="64" width="170"
        text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24"
        font-weight="800"
        letter-spacing="2.5"
        fill="#FFFFFF"
        opacity="0.92"
        filter="url(#textShadow)">INSIDER</text>

  <!-- Small section label -->
  <text x="640" y="198" width="760"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22"
        font-weight="700"
        letter-spacing="4"
        fill="#D8F1FF"
        opacity="0.92"
        filter="url(#textShadow)">WINDOWS PRODUCTIVITY GUIDE</text>

  <!-- Hero headline: high-contrast, large, centered, shadowed -->
  <text x="640" y="302" width="1080"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76"
        font-weight="800"
        fill="#FFFFFF"
        filter="url(#textShadow)">
    <tspan x="640" dy="0">How to Use Split</tspan>
    <tspan x="640" dy="88">Screen on Windows 10</tspan>
  </text>

  <!-- Supporting line with restrained opacity -->
  <text x="640" y="530" width="850"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26"
        font-weight="500"
        fill="#FFFFFF"
        opacity="0.82"
        filter="url(#textShadow)">A faster way to compare, reference, and work side by side</text>

  <!-- Subtle bottom hairline accent -->
  <rect x="440" y="596" width="400" height="4" rx="2" fill="#FFFFFF" opacity="0.34"/>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter="url(#blur)"` directly to the `<image>` if reliable PowerPoint editability is required; use a pre-blurred image asset instead.
- ❌ Placing white text over an undimmed photo; busy areas will destroy legibility.
- ❌ Thin or lightweight typography for the hero title; the effect depends on bold, high-contrast type.
- ❌ Using `<mask>` or clipping non-image elements for the vignette; use gradient-filled rectangles instead.
- ❌ Overcrowding the slide with charts, icons, or multiple text blocks; the background is atmospheric, not informational.

## Composition notes
- Keep the headline centered and wide, usually 75–85% of slide width, with generous line spacing.
- Use a 30–45% black overlay plus top/bottom vignettes to make white text consistently readable.
- The visual focus should be the title; branding stays small in the top-right and secondary text stays restrained.
- Choose a background image with strong thematic relevance but no critical details, because blur turns it into color and mood rather than content.