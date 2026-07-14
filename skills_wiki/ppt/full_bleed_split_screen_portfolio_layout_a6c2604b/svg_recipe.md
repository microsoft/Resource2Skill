# SVG Recipe — Full-Bleed Split-Screen Portfolio Layout

## Visual mechanism
Split the canvas into two hard-edged editorial zones: a solid-color typography panel and a full-bleed hero image panel. The contrast between quiet, structured text and immersive edge-to-edge imagery creates a premium portfolio or case-study opener.

## SVG primitives needed
- 1× `<rect>` for the full-slide base background
- 1× `<rect>` for the left solid typography panel
- 1× `<image>` for the right-side full-bleed hero artwork/photo
- 1× `<clipPath>` with `<rect>` to constrain the hero image to the right panel
- 1× `<linearGradient>` for a subtle image-side readability wash
- 1× `<rect>` with gradient fill for the image overlay wash
- 3× `<rect>` for accent details: coral title rule, vertical split seam, bottom metadata rule
- 1× `<filter id="panelShadow">` for a soft architectural shadow at the split
- Multiple `<text>` elements with explicit `width` for eyebrow, title, body copy, metadata, and image caption
- Optional `<path>` decorative monogram/portfolio mark in the panel for a bespoke editorial feel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroClip">
      <rect x="486" y="0" width="794" height="720"/>
    </clipPath>

    <linearGradient id="heroWash" x1="486" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.22"/>
      <stop offset="0.28" stop-color="#000000" stop-opacity="0.04"/>
      <stop offset="0.72" stop-color="#000000" stop-opacity="0.00"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.18"/>
    </linearGradient>

    <linearGradient id="panelDepth" x1="0" y1="0" x2="486" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#30343D"/>
      <stop offset="1" stop-color="#20242B"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-10%" width="160%" height="120%">
      <feOffset dx="10" dy="0" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="16" in="offset" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full canvas foundation -->
  <rect x="0" y="0" width="1280" height="720" fill="#111318"/>

  <!-- Right full-bleed portfolio image -->
  <image
    href="https://images.example.com/full-bleed-gallery-sculpture-balloon-dog-hero.jpg"
    x="426" y="-18" width="914" height="756"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroClip)"/>

  <!-- Subtle wash over image to make the split feel cinematic -->
  <rect x="486" y="0" width="794" height="720" fill="url(#heroWash)"/>

  <!-- Left typography block -->
  <rect x="0" y="0" width="486" height="720" fill="url(#panelDepth)" filter="url(#panelShadow)"/>

  <!-- Sharp editorial seam -->
  <rect x="482" y="0" width="4" height="720" fill="#FF6B6B"/>
  <rect x="486" y="0" width="1" height="720" fill="#0B0D10" opacity="0.45"/>

  <!-- Decorative portfolio mark -->
  <path d="M82 92 C105 62, 152 63, 174 94 C195 124, 179 166, 138 178 C103 188, 68 170, 61 138 C57 119, 65 104, 82 92 Z"
        fill="#FFFFFF" opacity="0.045"/>
  <path d="M100 116 L141 94 L179 119 L160 164 L112 163 Z"
        fill="none" stroke="#FF6B6B" stroke-width="3" opacity="0.55"/>

  <!-- Eyebrow -->
  <text x="70" y="118" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3"
        fill="#FF6B6B">PORTFOLIO STUDY</text>

  <!-- Accent rule -->
  <rect x="70" y="146" width="78" height="7" rx="3.5" fill="#FF6B6B"/>

  <!-- Title -->
  <text x="70" y="226" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800"
        fill="#FFFFFF">
    <tspan x="70" dy="0">Balloon</tspan>
    <tspan x="70" dy="68">Dog</tspan>
  </text>

  <!-- Body copy -->
  <text x="72" y="376" width="336"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#DDE1E8">
    <tspan x="72" dy="0">Mirror-polished stainless steel</tspan>
    <tspan x="72" dy="30">transforms a playful party object into</tspan>
    <tspan x="72" dy="30">a monumental study of surface, scale,</tspan>
    <tspan x="72" dy="30">and childhood spectacle.</tspan>
  </text>

  <!-- Secondary descriptor -->
  <text x="72" y="535" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500"
        fill="#AEB6C4">
    <tspan x="72" dy="0">Jeff Koons · 1994–2000</tspan>
    <tspan x="72" dy="24">Transparent color coating over steel</tspan>
  </text>

  <!-- Bottom metadata rhythm -->
  <rect x="70" y="624" width="338" height="1" fill="#FFFFFF" opacity="0.22"/>
  <text x="70" y="660" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2"
        fill="#FFFFFF" opacity="0.78">CASE 04</text>
  <text x="250" y="660" width="160"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2"
        text-anchor="end"
        fill="#FFFFFF" opacity="0.78">SCULPTURE</text>

  <!-- Image caption anchored inside the full-bleed side -->
  <rect x="1014" y="614" width="210" height="54" rx="8" fill="#111318" opacity="0.72"/>
  <text x="1034" y="647" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600"
        fill="#FFFFFF">Gallery installation view</text>
</svg>
```

## Avoid in this skill
- ❌ Floating text boxes on top of the photo without a structural panel; it weakens the split-screen concept.
- ❌ Using a centered image with margins on all sides; the image must bleed to the top, right, and bottom edges.
- ❌ Low-contrast body text on the dark panel; keep text white or pale gray with generous line spacing.
- ❌ Applying `clip-path` to rectangles or groups; only clip the `<image>` if you need a clean crop.
- ❌ Overloading the text panel with too many bullets, icons, or charts; this layout works best with editorial copy.

## Composition notes
- Use a 35/65 to 40/60 horizontal split; the text panel should feel intentional, not like a sidebar.
- Keep the title and body copy left-aligned with a generous inner margin of about 60–80 px.
- Let the hero image dominate the right side and bleed fully off the slide edges.
- Use one saturated accent color only, typically as a short title rule and/or a thin vertical seam between zones.