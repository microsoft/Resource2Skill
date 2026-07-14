# SVG Recipe — Apple Glassmorphism Reveal

## Visual mechanism
A vibrant high-frequency photo background is duplicated as a pre-blurred image and clipped inside a translucent circle, creating a “frosted lens” that reveals softened color while keeping foreground text crisp. Specular white edges, soft shadows, and a clean white logo make the glass feel like a physical floating UI layer.

## SVG primitives needed
- 2× `<image>` for the leafy full-slide background and its server/pre-blurred duplicate clipped inside the glass lens
- 1× `<clipPath>` with `<circle>` for the circular frosted-glass crop
- 5× `<circle>` for the glass shadow, frosted wash, bevel rings, and edge accents
- 3× `<rect>` for background darkening overlays and the PowerPoint-style tile
- 4× `<path>` for the Apple-style logo, curved reveal arrow, orange presentation accent, and glass rim highlight
- 1× `<ellipse>` for a soft specular reflection across the glass
- 3× `<text>` for large headline typography and the editable “P” mark
- 2× `<linearGradient>` for vignette shading and orange presentation-card depth
- 1× `<radialGradient>` for the milky glass tint
- 2× `<filter>` using `feGaussianBlur`, `feOffset`, and `feMerge` for soft shadow and white glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000000" stop-opacity="0.66"/>
      <stop offset="0.35" stop-color="#00150a" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ppGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ff6a2d"/>
      <stop offset="0.55" stop-color="#ff4d22"/>
      <stop offset="1" stop-color="#df2717"/>
    </linearGradient>

    <radialGradient id="glassWash" cx="38%" cy="25%" r="72%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="0.42" stop-color="#ffffff" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#061b10" stop-opacity="0.20"/>
    </radialGradient>

    <linearGradient id="glassEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.92"/>
      <stop offset="0.45" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.34"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="whiteGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="9" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="glassCircleClip">
      <circle cx="650" cy="355" r="255"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#062414"/>
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&amp;fit=crop&amp;w=1280&amp;h=720&amp;q=90"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#001b0d" opacity="0.12"/>

  <text x="31" y="135" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="116" font-weight="900"
        letter-spacing="8" fill="#ffffff">GLASS</text>
  <text x="42" y="213" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="73" font-weight="900"
        letter-spacing="3" fill="#ffffff">EFFECT</text>

  <circle cx="650" cy="355" r="256" fill="#000000" opacity="0.16" filter="url(#softShadow)"/>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#glassCircleClip)" opacity="0.96"
         href="https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&amp;fit=crop&amp;w=1280&amp;h=720&amp;q=65&amp;blur=80"/>

  <circle cx="650" cy="355" r="255" fill="url(#glassWash)"/>
  <ellipse cx="570" cy="238" rx="175" ry="55" fill="#ffffff" opacity="0.10"
           transform="rotate(-18 570 238)"/>
  <circle cx="650" cy="355" r="255" fill="none" stroke="url(#glassEdge)" stroke-width="4"/>
  <circle cx="650" cy="355" r="238" fill="none" stroke="#ffffff" stroke-width="1.2" opacity="0.20"/>
  <path d="M424 218 C486 128 620 88 746 122 C819 142 873 183 910 240"
        fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.55"/>

  <path transform="translate(526 238) scale(3.05)"
        fill="#ffffff"
        d="M52 20c-7.8 0-14.2 4.7-18.2 4.7-4.3 0-10.9-4.4-18-4.3C5.7 20.6 0 29.4 0 40.6c0 17.9 13.9 41.1 25.2 40.7 5-.1 6.8-3.2 12.8-3.2 5.9 0 7.4 3.2 12.8 3.1 11.8-.2 23.4-21.1 23.5-21.8-.2-.1-13.8-5.4-13.9-21 0-13 10.7-18.9 11.2-19.2C65.6 10.5 56.5 20 52 20z M48.4 0c.4 5.6-1.6 11-5 15-3.5 4.2-9.3 7.5-14.8 7 0-5.4 2.1-10.9 5.4-14.7C37.6 3.2 43.9.3 48.4 0z"/>

  <path d="M1005 238 C1108 259 1172 338 1169 456 L1124 407
           C1091 352 1040 324 980 320 L980 372 L858 328 L980 241 L980 294
           C1047 296 1103 324 1140 382 C1123 314 1077 266 1005 250 Z"
        fill="#ffffff" opacity="0.97" filter="url(#whiteGlow)"/>

  <path d="M982 520 C1007 469 1058 437 1120 437 C1204 437 1272 505 1272 589
           L1272 720 L982 720 Z"
        fill="#ffb16f" opacity="0.96"/>
  <rect x="1133" y="620" width="170" height="100" fill="#ff5a27" opacity="0.96"/>
  <rect x="931" y="519" width="210" height="186" rx="19" fill="url(#ppGrad)" filter="url(#softShadow)"/>
  <rect x="944" y="532" width="184" height="160" rx="13" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.13"/>
  <text x="987" y="675" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="150" font-weight="800"
        fill="#ffffff">P</text>
</svg>
```

## Avoid in this skill
- ❌ Using an SVG `<filter>` blur directly on the full background image if the PowerPoint translator does not preserve image filters; use a pre-blurred duplicate image clipped to the glass shape instead.
- ❌ Applying `clip-path` to ordinary shapes for the glass tint or border; clipping is reliable for `<image>`, while editable shape overlays should be drawn directly.
- ❌ Building the curved arrow with `marker-end`; use a filled `<path>` arrow silhouette so the arrowhead remains editable and visible.
- ❌ Using `<mask>` to create the frosted region; masks are fragile in this pipeline and can hard-fail the slide.

## Composition notes
- Keep the glass lens large enough to feel premium, roughly 35–45% of slide height, but leave visible unblurred photo texture around it for contrast.
- Place bold white headline text in a darkened corner; the glass panel should be the central focal plane, not a full-slide overlay.
- Use a blurred duplicate image with identical crop parameters to the background so the lens appears spatially aligned.
- Add only a few high-opacity white elements—logo, arrow, headline—so the translucent greens and specular rim remain the visual rhythm.