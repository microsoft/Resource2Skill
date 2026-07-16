# SVG Recipe — Dynamic Glassmorphism (Frosted Glass) Depth Panel

## Visual mechanism
Layer a vivid full-bleed photo with a pre-blurred, brightened duplicate clipped into a rounded rectangle, then add translucent white overlays, fine borders, glow, and shadow to make the rectangle read as frosted glass. A transparent foreground subject breaks across the panel edge to create premium depth and a “3D diorama” feel.

## SVG primitives needed
- 1× full-slide `<image>` for the sharp, colorful photographic background.
- 1× clipped `<image>` for the pre-blurred/brightened duplicate background inside the glass panel.
- 1× `<clipPath>` with rounded `<rect>` for the frosted panel crop.
- 2× `<rect>` for the glass wash and glass edge/stroke.
- 1× `<filter id="panelShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for the floating glass panel.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for ambient highlight blobs and decorative light.
- 3× `<circle>` / `<ellipse>` for blurred bokeh and atmospheric depth accents.
- 2× `<path>` for elegant light streaks/organic highlight shapes.
- 1× transparent foreground `<image>` for the frame-breaking subject.
- 3× `<text>` elements with explicit `width` for title, subtitle, and small eyebrow label.
- 1× `<line>` for a subtle premium divider accent.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="glassClip">
      <rect x="238" y="132" width="804" height="456" rx="54" ry="54"/>
    </clipPath>

    <linearGradient id="glassWash" x1="238" y1="132" x2="1042" y2="588" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.44"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#BFE7FF" stop-opacity="0.12"/>
    </linearGradient>

    <linearGradient id="edgeStroke" x1="238" y1="132" x2="1042" y2="588" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.58"/>
    </linearGradient>

    <radialGradient id="warmBokeh" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFE08A" stop-opacity="0.62"/>
      <stop offset="1" stop-color="#FF7AB6" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="24" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="24" in="offset" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <image
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
    href="https://images.example.com/vibrant-colorful-tropical-leaves-sharp-16x9.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="#06111F" opacity="0.18"/>

  <circle cx="1060" cy="104" r="170" fill="url(#warmBokeh)" filter="url(#softGlow)" opacity="0.72"/>
  <ellipse cx="170" cy="640" rx="210" ry="95" fill="#37D5FF" opacity="0.22" filter="url(#softGlow)"/>
  <circle cx="1010" cy="625" r="105" fill="#9F5CFF" opacity="0.20" filter="url(#softGlow)"/>

  <rect
    x="238" y="132" width="804" height="456" rx="54" ry="54"
    fill="#0B1F2E" opacity="0.35" filter="url(#panelShadow)"/>

  <image
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
    clip-path="url(#glassClip)" opacity="0.88"
    href="https://images.example.com/vibrant-colorful-tropical-leaves-preblurred-brightened-16x9.jpg"/>

  <rect
    x="238" y="132" width="804" height="456" rx="54" ry="54"
    fill="url(#glassWash)" opacity="0.92"/>

  <path
    d="M292 188 C410 120, 564 144, 680 220 C750 266, 850 262, 986 184"
    fill="none" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="2"/>

  <path
    d="M875 518 C930 486, 980 478, 1032 502 C994 552, 916 566, 862 544 C858 534, 864 524, 875 518 Z"
    fill="#FFFFFF" opacity="0.16" filter="url(#softGlow)"/>

  <rect
    x="239.5" y="133.5" width="801" height="453" rx="52" ry="52"
    fill="none" stroke="url(#edgeStroke)" stroke-width="2.5"/>

  <line x1="543" y1="455" x2="737" y2="455" stroke="#FFFFFF" stroke-width="1.3" stroke-opacity="0.56"/>

  <text
    x="640" y="248" width="610" text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, serif" font-size="18" font-weight="600"
    letter-spacing="7" fill="#FFFFFF" opacity="0.84">
    CREATIVE FIELD NOTES
  </text>

  <text
    x="640" y="356" width="720" text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, serif" font-size="72" font-weight="300"
    letter-spacing="13" fill="#FFFFFF">
    THE NATURE
  </text>

  <text
    x="640" y="506" width="620" text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400"
    letter-spacing="5" fill="#FFFFFF" opacity="0.88">
    Beauty in Every Breath
  </text>

  <image
    x="122" y="166" width="375" height="430" preserveAspectRatio="xMidYMid meet"
    href="https://images.example.com/transparent-png-colorful-bird-perched-wings-overlapping-panel.png"/>

  <path
    d="M268 556 C322 582, 402 596, 492 580"
    fill="none" stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="3"/>

  <text
    x="86" y="650" width="250"
    font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600"
    letter-spacing="3" fill="#FFFFFF" opacity="0.66">
    GLASS DEPTH / 01
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on CSS `backdrop-filter`; PPT translation will not dynamically blur pixels behind a shape.
- ❌ Do not place `clip-path` on the translucent glass `<rect>`; use rounded rectangle geometry directly, and reserve `clipPath` for the blurred `<image>`.
- ❌ Do not apply SVG filters to `<image>` for the blur step; use a pre-blurred/brightened duplicate image asset for reliable PowerPoint output.
- ❌ Do not use `<mask>` to create the rounded glass crop; use `<clipPath>` on the glass image instead.
- ❌ Do not make the panel too opaque; the effect should feel like luminous glass, not a flat white card.

## Composition notes
- Keep the glass panel centered and large: roughly 60–65% of slide width and height, with generous margins so the background still feels immersive.
- Place the subject so it crosses one panel edge; the overlap is what sells depth and prevents the layout from feeling like a flat UI card.
- Use a colorful, high-texture background, but add a subtle dark overlay outside the panel to preserve hierarchy.
- Typography should be sparse, centered, white, and widely tracked; the airy spacing reinforces the premium glassmorphism mood.