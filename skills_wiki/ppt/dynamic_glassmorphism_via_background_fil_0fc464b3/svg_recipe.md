# SVG Recipe — Dynamic Glassmorphism via Background Fill Injection

## Visual mechanism
Create “real” frosted glass by stacking a sharp full-slide image over a blurred version of the same image, then placing clipped copies of the blurred image exactly inside the glass cards. The cards read as movable blur windows, enhanced with translucent fills, gradient edge lighting, soft shadows, and glowing typography.

## SVG primitives needed
- 1× full-slide `<image>` for the blurred background base.
- 1× full-slide `<image>` for the sharp foreground image that hides the blur.
- 3× clipped `<image>` repeats of the blurred background, one per glass panel, aligned to the slide coordinates.
- 3× `<clipPath>` with rounded `<rect>` geometry for panel-shaped blur windows.
- 3× translucent rounded `<rect>` overlays for the glass surface tint.
- 3× rounded `<rect>` strokes using a gradient for bright-to-transparent glass edges.
- 3× smaller highlight `<rect>` overlays for top-edge sheen.
- 3× decorative `<path>` glow streaks over the hero image.
- 3× simple icon constructions using `<circle>`, `<line>`, and `<path>` inside the cards.
- 1× `<linearGradient>` for the title color.
- 1× `<linearGradient>` for glass edge lighting.
- 1× `<linearGradient>` for global vignette/scrim.
- 1× `<filter id="panelShadow">` applied to glass rectangles.
- 1× `<filter id="softGlow">` applied to glow paths and text.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="titleGrad" x1="320" y1="110" x2="960" y2="190" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.55" stop-color="#dfefff"/>
      <stop offset="1" stop-color="#ffffff"/>
    </linearGradient>

    <linearGradient id="glassStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="0.28" stop-color="#ffffff" stop-opacity="0.36"/>
      <stop offset="0.62" stop-color="#b9ddff" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="topVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#03101d" stop-opacity="0.72"/>
      <stop offset="0.45" stop-color="#03101d" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#03101d" stop-opacity="0.52"/>
    </linearGradient>

    <linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset in="SourceAlpha" dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="panelClip1"><rect x="155" y="320" width="270" height="310" rx="34" ry="34"/></clipPath>
    <clipPath id="panelClip2"><rect x="505" y="320" width="270" height="310" rx="34" ry="34"/></clipPath>
    <clipPath id="panelClip3"><rect x="855" y="320" width="270" height="310" rx="34" ry="34"/></clipPath>
  </defs>

  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&amp;fit=crop&amp;w=1920&amp;q=80&amp;blur=90&amp;sat=-20"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&amp;fit=crop&amp;w=1920&amp;q=88"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#topVignette)"/>

  <path d="M60 180 C230 90, 340 120, 470 68 C620 8, 770 70, 920 36 C1050 8, 1160 38, 1240 88"
        fill="none" stroke="#bde9ff" stroke-opacity="0.28" stroke-width="8" filter="url(#softGlow)"/>
  <path d="M170 520 C330 450, 450 500, 590 440 C760 365, 930 430, 1110 350"
        fill="none" stroke="#fff6b0" stroke-opacity="0.18" stroke-width="10" filter="url(#softGlow)"/>
  <path d="M920 130 C1000 98, 1120 112, 1210 74"
        fill="none" stroke="#ffffff" stroke-opacity="0.35" stroke-width="5" filter="url(#softGlow)"/>

  <text x="640" y="144" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="68" font-weight="800"
        letter-spacing="3" fill="url(#titleGrad)" filter="url(#softGlow)">ANIMATED GLASS</text>
  <text x="784" y="210" width="360" text-anchor="middle"
        font-family="Segoe Script, Segoe UI, Microsoft YaHei, sans-serif" font-size="54"
        fill="#ffdc32" filter="url(#softGlow)">Effect</text>
  <text x="640" y="252" width="650" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#ffffff" opacity="0.84">background-aligned blur windows for premium morph-ready slides</text>

  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&amp;fit=crop&amp;w=1920&amp;q=80&amp;blur=90&amp;sat=-20"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#panelClip1)"/>
  <rect x="155" y="320" width="270" height="310" rx="34" ry="34" fill="#ffffff" opacity="0.16" filter="url(#panelShadow)"/>
  <rect x="155" y="320" width="270" height="310" rx="34" ry="34" fill="none" stroke="url(#glassStroke)" stroke-width="3"/>
  <rect x="178" y="342" width="224" height="58" rx="22" ry="22" fill="url(#shineGrad)" opacity="0.55"/>
  <circle cx="290" cy="408" r="38" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.88"/>
  <line x1="290" y1="370" x2="290" y2="446" stroke="#ffffff" stroke-width="4" opacity="0.88"/>
  <line x1="252" y1="408" x2="328" y2="408" stroke="#ffffff" stroke-width="4" opacity="0.88"/>
  <text x="190" y="504" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
        fill="#ffffff" filter="url(#softGlow)">LIVE BLUR</text>
  <text x="190" y="540" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#ffffff" opacity="0.78">the card reveals the softened environment beneath</text>

  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&amp;fit=crop&amp;w=1920&amp;q=80&amp;blur=90&amp;sat=-20"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#panelClip2)"/>
  <rect x="505" y="320" width="270" height="310" rx="34" ry="34" fill="#ffffff" opacity="0.17" filter="url(#panelShadow)"/>
  <rect x="505" y="320" width="270" height="310" rx="34" ry="34" fill="none" stroke="url(#glassStroke)" stroke-width="3"/>
  <rect x="528" y="342" width="224" height="58" rx="22" ry="22" fill="url(#shineGrad)" opacity="0.55"/>
  <path d="M640 366 L681 438 L599 438 Z" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round" opacity="0.9"/>
  <circle cx="640" cy="414" r="11" fill="#ffdc32" opacity="0.95"/>
  <text x="540" y="504" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
        fill="#ffffff" filter="url(#softGlow)">MORPH READY</text>
  <text x="540" y="540" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#ffffff" opacity="0.78">move the window and the blur stays visually registered</text>

  <image href="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&amp;fit=crop&amp;w=1920&amp;q=80&amp;blur=90&amp;sat=-20"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#panelClip3)"/>
  <rect x="855" y="320" width="270" height="310" rx="34" ry="34" fill="#ffffff" opacity="0.16" filter="url(#panelShadow)"/>
  <rect x="855" y="320" width="270" height="310" rx="34" ry="34" fill="none" stroke="url(#glassStroke)" stroke-width="3"/>
  <rect x="878" y="342" width="224" height="58" rx="22" ry="22" fill="url(#shineGrad)" opacity="0.55"/>
  <path d="M958 440 C958 392, 990 372, 990 372 C990 372, 1022 392, 1022 440 Z"
        fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round" opacity="0.9"/>
  <circle cx="990" cy="408" r="12" fill="#ffdc32" opacity="0.95"/>
  <text x="890" y="504" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
        fill="#ffffff" filter="url(#softGlow)">DEEP EDGE</text>
  <text x="890" y="540" width="200" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#ffffff" opacity="0.78">gradient outlines and highlights imply thick glass</text>
</svg>
```

## Avoid in this skill
- ❌ CSS `backdrop-filter: blur(...)`; it will not translate into editable PowerPoint glass.
- ❌ A single transparent rectangle over a photo; transparency alone does not create frosted glass.
- ❌ Applying `clip-path` to `<rect>` or `<g>` for the glass surface; use clip paths only on the blurred `<image>` copies.
- ❌ Moving a grouped clipped image without recalculating its crop/clip position on the next Morph slide; the blur must remain aligned to the slide background.
- ❌ SVG `<mask>` or `<foreignObject>` for blur windows; these can hard-fail or be ignored.

## Composition notes
- Keep the hero title in the upper third, with glass cards occupying the lower two-thirds so the image still feels cinematic.
- Use the same blurred image dimensions and x/y origin as the sharp foreground; the clipped blur copies must align perfectly with the full-slide photo.
- Make glass panels large enough for the blur to be legible, but leave generous gaps between cards so the sharp background remains visible.
- Use white, pale blue, and warm gold accents sparingly; the premium effect comes from edge lighting and depth, not heavy color.