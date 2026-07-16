# SVG Recipe — Seamless Gradient Image Blending (人物介绍渐变融合)

## Visual mechanism
A portrait photo is placed on one side of the slide, then its hard inner edge is covered by a wide alpha gradient whose solid end exactly matches the slide background. This makes the image “melt” into the canvas, creating clean negative space for oversized editorial typography.

## SVG primitives needed
- 1× `<rect>` for the full-slide background color that matches the photo edge.
- 1× `<image>` for the portrait photo, positioned flush to the left and cropped to full slide height.
- 1× `<clipPath>` with rounded `<rect>` for a controlled full-height portrait crop.
- 2× `<linearGradient>` for the horizontal image-to-background fade and subtle background wash.
- 2× `<radialGradient>` for soft decorative blue light spots.
- 3× `<circle>` for translucent atmosphere bubbles behind the content.
- 1× `<filter id="softBlur">` applied to decorative circles for diffused depth.
- 1× `<filter id="textGlow">` applied lightly to the headline for polished keynote emphasis.
- 4× `<rect>` for gradient overlays, subtitle chips, and small editorial accent bars.
- 3× `<text>` blocks with explicit `width` for label, main headline, and supporting caption.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoFadeToBg" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#D7EAF8" stop-opacity="0"/>
      <stop offset="42%" stop-color="#D7EAF8" stop-opacity="0.45"/>
      <stop offset="78%" stop-color="#D7EAF8" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#D7EAF8" stop-opacity="1"/>
    </linearGradient>

    <linearGradient id="canvasWash" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EEF8FF" stop-opacity="0.55"/>
      <stop offset="52%" stop-color="#D7EAF8" stop-opacity="0"/>
      <stop offset="100%" stop-color="#BFDDF7" stop-opacity="0.35"/>
    </linearGradient>

    <radialGradient id="bubbleBlue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#77BDF2" stop-opacity="0.30"/>
      <stop offset="72%" stop-color="#77BDF2" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#77BDF2" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="bubbleWhite" cx="42%" cy="38%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="textGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="blur"/>
      <feOffset dx="0" dy="2" result="offsetBlur"/>
      <feMerge>
        <feMergeNode in="offsetBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitCrop">
      <rect x="0" y="0" width="620" height="720" rx="0" ry="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#D7EAF8"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#canvasWash)"/>

  <circle cx="26" cy="126" r="78" fill="url(#bubbleBlue)" filter="url(#softBlur)"/>
  <circle cx="790" cy="5" r="56" fill="url(#bubbleBlue)" filter="url(#softBlur)"/>
  <circle cx="742" cy="774" r="104" fill="url(#bubbleBlue)" filter="url(#softBlur)"/>
  <circle cx="1135" cy="202" r="124" fill="url(#bubbleWhite)" opacity="0.35"/>

  <image
    x="0" y="0" width="640" height="720"
    href="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=900&auto=format&fit=crop"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#portraitCrop)"/>

  <rect x="280" y="0" width="450" height="720" fill="url(#photoFadeToBg)"/>
  <rect x="520" y="0" width="760" height="720" fill="#D7EAF8" opacity="0.18"/>

  <rect x="512" y="232" width="14" height="205" rx="7" fill="#1C92D2" opacity="0.92"/>
  <rect x="542" y="188" width="182" height="42" rx="21" fill="#FFFFFF" opacity="0.38"/>

  <text x="570" y="216" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700"
        letter-spacing="3"
        fill="#1C92D2">
    SPEAKER PROFILE
  </text>

  <text x="512" y="330" width="700"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="88" font-weight="800"
        fill="#178FD2"
        filter="url(#textGlow)">
    <tspan x="512" dy="0">PPT人物介绍</tspan>
    <tspan x="512" dy="110">做出大片质感</tspan>
  </text>

  <rect x="516" y="508" width="520" height="1.5" fill="#178FD2" opacity="0.28"/>
  <rect x="516" y="532" width="94" height="7" rx="3.5" fill="#178FD2" opacity="0.75"/>

  <text x="516" y="578" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="500"
        fill="#2C6F9F"
        opacity="0.88">
    让人物照片与背景色自然衔接，保留右侧大面积留白，形成高级演讲封面与人物介绍页。
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the fade; use a transparent-to-solid gradient rectangle over the photo edge instead.
- ❌ Do not leave a visible photo boundary; the gradient must be wide enough, usually 25–35% of the photo width.
- ❌ Do not mismatch the slide background and gradient stop color; even a small hue difference creates a visible seam.
- ❌ Do not place important text over the transparent part of the fade where the portrait still competes for attention.
- ❌ Do not use `clip-path` on normal shapes for this effect; clipping should only be applied to the `<image>` crop.

## Composition notes
- Keep the portrait on the left 40–50% of the slide, with the gradient beginning before the photo’s hard edge and extending deep into the canvas.
- Reserve the right 45–55% as clean negative space for large, heavy typography.
- Match the background color to the dominant edge color of the image, then use one saturated accent color for the title.
- Add very soft translucent circles or washes only behind the main content; they should enrich the atmosphere without revealing the blend boundary.