# SVG Recipe — Vibrant Geometric Framed Overlay

## Visual mechanism
A cinematic full-bleed photo is pushed into the background with a deep navy tint, then locked inside the viewer’s attention by a thick neon geometric frame. A small overlapping badge cuts across the frame edge while bold centered typography creates the announcement moment.

## SVG primitives needed
- 1× `<image>` for the full-bleed atmospheric background photo.
- 2× full-slide `<rect>` overlays for dark tinting and vignette depth.
- 2× framed `<rect>` elements for the neon glow pass and crisp gradient stroke pass.
- 1× `<rect>` for the intersecting top badge.
- 4× `<path>` elements for diagonal geometric corner accents.
- 4× `<text>` elements for badge, oversized title, subtitle, and micro-footer copy.
- 2× `<linearGradient>` definitions for the hot-pink-to-cyan frame and dark cinematic tint.
- 1× `<radialGradient>` definition for the center-light / edge-dark vignette.
- 2× `<filter>` definitions: one neon glow applied to the frame, one soft shadow applied to badge/text blocks.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="frameGradient" x1="270" y1="130" x2="1010" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ff007f"/>
      <stop offset="42%" stop-color="#b000ff"/>
      <stop offset="100%" stop-color="#00f0ff"/>
    </linearGradient>

    <linearGradient id="darkWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#050711" stop-opacity="0.82"/>
      <stop offset="48%" stop-color="#0f1420" stop-opacity="0.74"/>
      <stop offset="100%" stop-color="#02040a" stop-opacity="0.9"/>
    </linearGradient>

    <radialGradient id="vignette" cx="50%" cy="48%" r="70%">
      <stop offset="0%" stop-color="#101827" stop-opacity="0.08"/>
      <stop offset="58%" stop-color="#050814" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <filter id="neonGlow" x="-15%" y="-20%" width="130%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="badgeShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.example.com/cinematic-city-night-abstract-lights.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M0,0 L235,0 L185,34 L0,34 Z" fill="#ff007f" opacity="0.72"/>
  <path d="M1280,720 L1040,720 L1090,686 L1280,686 Z" fill="#00f0ff" opacity="0.72"/>
  <path d="M1045,91 L1185,91 L1148,116 L1008,116 Z" fill="#ffffff" opacity="0.14"/>
  <path d="M95,612 L260,612 L219,640 L54,640 Z" fill="#ffffff" opacity="0.12"/>

  <rect x="264" y="138" width="752" height="444" rx="0"
        fill="none" stroke="url(#frameGradient)" stroke-width="24"
        opacity="0.7" filter="url(#neonGlow)"/>

  <rect x="264" y="138" width="752" height="444" rx="0"
        fill="none" stroke="url(#frameGradient)" stroke-width="14"/>

  <rect x="480" y="112" width="320" height="52" rx="2"
        fill="#ff007f" filter="url(#badgeShadow)"/>

  <text x="640" y="146" width="320" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3.2"
        fill="#ffffff">
    CREATIVE PORTFOLIO
  </text>

  <text x="640" y="322" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" letter-spacing="-2"
        fill="#ffffff" filter="url(#badgeShadow)">
    <tspan x="640" dy="0">PROJECT</tspan>
    <tspan x="640" dy="82">OVERVIEW</tspan>
  </text>

  <text x="640" y="472" width="610" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" line-height="1.35"
        fill="#dbe7f2" opacity="0.95">
    <tspan x="640" dy="0">We pursue relationships based on</tspan>
    <tspan x="640" dy="34">transparency and mutual trust.</tspan>
  </text>

  <text x="640" y="638" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="4"
        fill="#7eefff" opacity="0.82">
    STRATEGY  •  IDENTITY  •  DIGITAL EXPERIENCE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to darken the image; use semi-transparent overlay rectangles instead.
- ❌ Do not put `clip-path` on the frame or text; clipping is only reliable for `<image>` crops.
- ❌ Do not use `<pattern>` fills for the frame; use a real `<linearGradient>` stroke.
- ❌ Do not rely on a thin outline. The frame needs a thick stroke, usually 12–24 px, to feel intentional.
- ❌ Do not place dense body copy inside the frame; this layout is built for one big message and one short supporting line.

## Composition notes
- Keep the frame centered and large, occupying roughly 60–70% of the slide width and height.
- Use a dark, low-detail photo so the neon frame and white title remain the clear focal point.
- Let the badge overlap the top frame edge by about half its height to create an editorial “interlock.”
- Maintain a tight color rhythm: hot pink badge, cyan/pink gradient frame, white title, and only one muted secondary text color.