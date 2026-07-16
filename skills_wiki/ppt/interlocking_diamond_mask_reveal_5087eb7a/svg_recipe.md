# SVG Recipe — Interlocking Diamond Mask Reveal

## Visual mechanism
A dark full-slide overlay is visually “punched open” by repeating the same background photo inside clipped rounded diamonds, creating an interlocking geometric reveal lattice. A larger central gradient diamond sits on top as the focal plate, with soft shadow, thin outline echoes, and bold centered title text.

## SVG primitives needed
- 1× `<image>` for the full-slide mountain / landscape background base
- 1× `<rect>` for the dark slate full-slide mask layer
- 17× `<clipPath>` each containing a rotated rounded `<rect>` to define diamond reveal windows
- 17× clipped `<image>` instances using the same full-slide photo, one per diamond reveal window
- 1× `<linearGradient>` for the purple-to-pink central focal diamond
- 1× `<filter id="softShadow">` applied to the focal diamond
- 1× `<filter id="photoDim">` optionally applied to the base photo for atmospheric darkening
- 1× rotated rounded `<rect>` for the central gradient diamond
- 2× rotated rounded `<rect>` outlines for translucent diamond echo rings
- 1× `<text>` with nested `<tspan>` for the centered title
- 4× decorative `<line>` elements for faint diagonal lattice accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroGrad" x1="470" y1="230" x2="810" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8A2387" stop-opacity="0.92"/>
      <stop offset="55%" stop-color="#C43A8A" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#E94057" stop-opacity="0.90"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="photoDim">
      <feGaussianBlur stdDeviation="0.25"/>
    </filter>

    <!-- Rounded-square diamond reveal clips. Same photo is repeated under each clip. -->
    <clipPath id="d0"><rect x="530" y="250" width="220" height="220" rx="36" transform="rotate(45 640 360)"/></clipPath>

    <clipPath id="d1"><rect x="278" y="250" width="220" height="220" rx="36" transform="rotate(45 388 360)"/></clipPath>
    <clipPath id="d2"><rect x="782" y="250" width="220" height="220" rx="36" transform="rotate(45 892 360)"/></clipPath>
    <clipPath id="d3"><rect x="26" y="250" width="220" height="220" rx="36" transform="rotate(45 136 360)"/></clipPath>
    <clipPath id="d4"><rect x="1034" y="250" width="220" height="220" rx="36" transform="rotate(45 1144 360)"/></clipPath>

    <clipPath id="d5"><rect x="152" y="124" width="220" height="220" rx="36" transform="rotate(45 262 234)"/></clipPath>
    <clipPath id="d6"><rect x="404" y="124" width="220" height="220" rx="36" transform="rotate(45 514 234)"/></clipPath>
    <clipPath id="d7"><rect x="656" y="124" width="220" height="220" rx="36" transform="rotate(45 766 234)"/></clipPath>
    <clipPath id="d8"><rect x="908" y="124" width="220" height="220" rx="36" transform="rotate(45 1018 234)"/></clipPath>
    <clipPath id="d9"><rect x="1160" y="124" width="220" height="220" rx="36" transform="rotate(45 1270 234)"/></clipPath>

    <clipPath id="d10"><rect x="152" y="376" width="220" height="220" rx="36" transform="rotate(45 262 486)"/></clipPath>
    <clipPath id="d11"><rect x="404" y="376" width="220" height="220" rx="36" transform="rotate(45 514 486)"/></clipPath>
    <clipPath id="d12"><rect x="656" y="376" width="220" height="220" rx="36" transform="rotate(45 766 486)"/></clipPath>
    <clipPath id="d13"><rect x="908" y="376" width="220" height="220" rx="36" transform="rotate(45 1018 486)"/></clipPath>
    <clipPath id="d14"><rect x="1160" y="376" width="220" height="220" rx="36" transform="rotate(45 1270 486)"/></clipPath>

    <clipPath id="d15"><rect x="-100" y="-2" width="220" height="220" rx="36" transform="rotate(45 10 108)"/></clipPath>
    <clipPath id="d16"><rect x="116" y="-78" width="220" height="220" rx="36" transform="rotate(45 226 32)"/></clipPath>
  </defs>

  <!-- Base photo gives subtle continuity under the mask edges. -->
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.42" filter="url(#photoDim)"/>

  <!-- Full-slide dark mask. The apparent holes are recreated by clipped photo tiles above it. -->
  <rect x="0" y="0" width="1280" height="720" fill="#20242D"/>

  <!-- Repeated full-slide photo clipped to rounded diamond windows. -->
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d15)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d16)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d5)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d6)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d7)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d8)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d9)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d3)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d1)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d0)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d2)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d4)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d10)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d11)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d12)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d13)"/>
  <image href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;q=85" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#d14)"/>

  <!-- Thin glass-like echo outlines behind the central focal diamond. -->
  <rect x="440" y="160" width="400" height="400" rx="66" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.42" transform="rotate(45 640 360)"/>
  <rect x="474" y="194" width="332" height="332" rx="54" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity="0.30" transform="rotate(45 640 360)"/>

  <!-- Subtle diagonal accents reinforce the interlocking geometry. -->
  <line x1="348" y1="76" x2="580" y2="308" stroke="#FFFFFF" stroke-width="1" opacity="0.22"/>
  <line x1="932" y1="76" x2="700" y2="308" stroke="#FFFFFF" stroke-width="1" opacity="0.22"/>
  <line x1="348" y1="644" x2="580" y2="412" stroke="#FFFFFF" stroke-width="1" opacity="0.18"/>
  <line x1="932" y1="644" x2="700" y2="412" stroke="#FFFFFF" stroke-width="1" opacity="0.18"/>

  <!-- Central gradient diamond covers the center reveal and becomes the message plate. -->
  <rect x="495" y="215" width="290" height="290" rx="48"
        fill="url(#heroGrad)" stroke="#FFFFFF" stroke-width="2.6" stroke-opacity="0.82"
        transform="rotate(45 640 360)" filter="url(#softShadow)"/>

  <text x="510" y="337" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="55" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="3">
    <tspan x="640" dy="0">THANK</tspan>
    <tspan x="640" dy="68">YOU</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to punch holes in the dark overlay; mask attributes on shapes are not reliable for this translation path.
- ❌ Do not rely on `<use>` to repeat the same diamond clip or photo tile; duplicate the clipped `<image>` elements explicitly.
- ❌ Do not apply `clip-path` to the dark overlay `<rect>`; clip paths should be applied to `<image>` elements for this technique.
- ❌ Do not use `<pattern>` fills for the photo lattice; repeat full-slide images with individual clip paths instead.
- ❌ Do not put `filter` on `<line>` accents; line filters are dropped.

## Composition notes
- Keep the center diamond exactly on the slide midpoint, then stagger surrounding diamond centers by one diamond diagonal horizontally and half that distance vertically.
- Let the dark mask dominate 35–50% of the surface so the background photo feels curated rather than busy.
- Use a high-contrast scenic or architectural image; the lattice works best when different photo regions appear in each diamond.
- Reserve the central diamond for the title only; avoid extra subtitles inside it unless the diamond is enlarged.