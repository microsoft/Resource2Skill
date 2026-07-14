# SVG Recipe — Glassmorphism Focus Panel

## Visual mechanism
A full-bleed photographic background is duplicated, blurred, and clipped to a rounded rectangle so it appears like a frosted glass pane floating above the image. A translucent white tint, subtle border, shadow, and high-contrast typography make the panel feel premium while preserving the emotional context of the photo.

## SVG primitives needed
- 2× `<image>` for the full-slide background and the perfectly aligned blurred duplicate inside the glass panel
- 1× `<clipPath>` with rounded `<rect>` for cropping the duplicate background image to the glass panel shape
- 4× `<rect>` for the shadow catcher, frost tint, glass rim, and small label/CTA surfaces
- 2× `<filter>` for the strong glass blur and soft floating panel shadow
- 2× `<linearGradient>` for background darkening and the glass rim highlight
- 1× `<radialGradient>` for subtle atmospheric light bloom over the photo
- 3× `<path>` for decorative glass reflections and organic background light streaks
- 4× `<text>` with explicit `width` attributes for label, title, subtitle, and CTA copy
- 1× `<line>` for a simple divider/accent rule inside the panel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="glassClip">
      <rect x="760" y="92" width="430" height="536" rx="46" ry="46"/>
    </clipPath>

    <filter id="glassBlur" x="700" y="32" width="550" height="656" filterUnits="userSpaceOnUse">
      <feGaussianBlur stdDeviation="22" edgeMode="duplicate"/>
    </filter>

    <filter id="panelShadow" x="700" y="40" width="560" height="650" filterUnits="userSpaceOnUse">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="photoGrade" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#061b16" stop-opacity="0.08"/>
      <stop offset="0.52" stop-color="#08231c" stop-opacity="0.04"/>
      <stop offset="1" stop-color="#00130f" stop-opacity="0.42"/>
    </linearGradient>

    <linearGradient id="rimGradient" x1="760" y1="92" x2="1190" y2="628" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.78"/>
      <stop offset="0.38" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.36"/>
    </linearGradient>

    <radialGradient id="sunBloom" cx="260" cy="110" r="540" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffeaa0" stop-opacity="0.34"/>
      <stop offset="0.45" stop-color="#8be0b8" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;h=1080&amp;q=85"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#photoGrade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#sunBloom)"/>

  <path d="M-40 565 C190 500 330 665 545 595 C690 547 742 432 870 430"
        fill="none" stroke="#d8fff1" stroke-opacity="0.16" stroke-width="3"/>
  <path d="M80 90 C210 18 370 48 520 142 C660 230 760 205 890 160"
        fill="none" stroke="#ffffff" stroke-opacity="0.11" stroke-width="2"/>

  <rect x="760" y="92" width="430" height="536" rx="46" ry="46"
        fill="#031f19" opacity="0.24" filter="url(#panelShadow)"/>

  <image
    href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;h=1080&amp;q=85"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
    clip-path="url(#glassClip)" filter="url(#glassBlur)" opacity="1"/>

  <rect x="760" y="92" width="430" height="536" rx="46" ry="46"
        fill="#ffffff" opacity="0.18"/>
  <rect x="760" y="92" width="430" height="536" rx="46" ry="46"
        fill="none" stroke="url(#rimGradient)" stroke-width="1.6"/>

  <path d="M792 123 C873 105 996 103 1156 126"
        fill="none" stroke="#ffffff" stroke-opacity="0.46" stroke-width="2.4"/>
  <path d="M801 560 C910 602 1048 604 1158 552"
        fill="none" stroke="#ffffff" stroke-opacity="0.15" stroke-width="2"/>

  <rect x="810" y="146" width="144" height="34" rx="17" ry="17"
        fill="#ffffff" opacity="0.22"/>
  <text x="828" y="168" width="110"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="700" letter-spacing="1.6" fill="#eafff6">
    ECO FUTURE
  </text>

  <text x="810" y="270" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58"
        font-weight="800" fill="#ffd84d">
    <tspan x="810" dy="0">Save</tspan>
    <tspan x="810" dy="66" fill="#ffffff">Nature</tspan>
  </text>

  <line x1="812" y1="385" x2="915" y2="385"
        stroke="#ffd84d" stroke-width="4" stroke-linecap="round"/>

  <text x="812" y="432" width="320"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22"
        font-weight="500" fill="#f5fffb" opacity="0.94">
    <tspan x="812" dy="0">Protect our planet through</tspan>
    <tspan x="812" dy="32">restoration, clean energy,</tspan>
    <tspan x="812" dy="32">and everyday choices.</tspan>
  </text>

  <rect x="812" y="548" width="182" height="48" rx="24" ry="24"
        fill="#ffd84d" opacity="0.96"/>
  <text x="842" y="579" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16"
        font-weight="800" fill="#143024">
    START TODAY
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the “focus panel” motion; create separate PowerPoint slides and use Morph instead.
- ❌ Do not use `<mask>` to cut the glass panel; use a `<clipPath>` on the duplicate `<image>` and rounded `<rect>` overlays.
- ❌ Do not clip non-image elements; rounded `<rect>` shapes should be drawn directly at the same coordinates as the clipped image.
- ❌ Do not place text directly on the busy photo without the frosted panel; the glass surface is what makes the typography legible.
- ❌ Do not forget explicit `width` attributes on every `<text>` element, or PowerPoint text layout may differ.

## Composition notes
- Place the glass panel on the right third or right 40% of the slide; leave the left side open for the strongest photographic subject.
- Align the duplicate blurred image exactly with the full-slide background image; any offset breaks the illusion of refraction.
- Use white tint around 15–25% opacity, a 1–2 px translucent rim, and a soft dark shadow to create convincing depth.
- For Morph-style animation, duplicate the slide and move the panel/text group horizontally or vertically while keeping the background fixed.