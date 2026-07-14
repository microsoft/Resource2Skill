# SVG Recipe — Frosted Glassmorphism Overlay (The Glass Effect)

## Visual mechanism
A translucent rounded pane appears to “frost” the scene behind it by placing a blurred duplicate crop of the same background inside the pane, then layering a milky white tint, luminous edge stroke, and soft shadow on top. Depth is reinforced by letting a foreground subject overlap the glass boundary so part of the composition feels in front of the pane and part feels behind it.

## SVG primitives needed
- 1× full-slide `<image>` for the vibrant background photo or abstract gradient scene
- 1× clipped `<image>` for the blurred duplicate background crop inside the glass pane
- 1× `<clipPath>` with rounded `<rect>` for the frosted crop shape
- 1× `<rect>` for the milky translucent glass tint
- 1× `<rect>` for the bright glass edge highlight stroke
- 1× `<linearGradient>` for subtle pane sheen
- 1× `<filter id="glassShadow">` using `feOffset + feGaussianBlur + feMerge` for soft lifted depth
- 1× `<filter id="softGlow">` using `feGaussianBlur` for accent glow behind foreground content
- 1× foreground `<image>` for an overlapping subject or product cutout
- 3× decorative `<circle>` or `<ellipse>` accent glows to make refraction visually obvious
- 4× `<text>` blocks with explicit `width` attributes for title, eyebrow, body copy, and UI label
- 2× `<line>` elements for thin UI separators or accent rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="glassClip">
      <rect x="438" y="92" width="690" height="536" rx="44" ry="44"/>
    </clipPath>

    <linearGradient id="paneSheen" x1="438" y1="92" x2="1128" y2="628" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="0.38" stop-color="#FFFFFF" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="titleGrad" x1="505" y1="170" x2="940" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.55" stop-color="#EAF7FF"/>
      <stop offset="1" stop-color="#BEEBFF"/>
    </linearGradient>

    <filter id="glassShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="24"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.04  0 0 0 0 0.10  0 0 0 0.42 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#08111F"/>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/abstract-neon-fluid-gradient-background-1280x720.jpg"/>

  <circle cx="130" cy="118" r="230" fill="#8238FF" opacity="0.35" filter="url(#softGlow)"/>
  <circle cx="1110" cy="540" r="270" fill="#00D5FF" opacity="0.30" filter="url(#softGlow)"/>
  <ellipse cx="655" cy="770" rx="390" ry="150" fill="#FF4EB8" opacity="0.22" filter="url(#softGlow)"/>

  <rect x="438" y="92" width="690" height="536" rx="44" ry="44"
        fill="#FFFFFF" opacity="0.01" filter="url(#glassShadow)"/>

  <!-- This image should be the same background, pre-blurred heavily or exported as a blurred duplicate crop. -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#glassClip)"
         href="https://images.example.com/abstract-neon-fluid-gradient-background-1280x720-blurred.jpg"/>

  <rect x="438" y="92" width="690" height="536" rx="44" ry="44"
        fill="url(#paneSheen)" opacity="0.92"/>

  <rect x="438" y="92" width="690" height="536" rx="44" ry="44"
        fill="#FFFFFF" opacity="0.14"/>

  <path d="M486 118 C620 96, 747 105, 884 118 C813 145, 615 150, 486 118 Z"
        fill="#FFFFFF" opacity="0.20"/>

  <rect x="439.5" y="93.5" width="687" height="533" rx="42" ry="42"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.58"/>

  <rect x="462" y="116" width="144" height="34" rx="17" fill="#FFFFFF" opacity="0.16"/>
  <circle cx="486" cy="133" r="5" fill="#86F6FF"/>
  <text x="502" y="139" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600"
        fill="#FFFFFF" opacity="0.88">PREMIUM UI SYSTEM</text>

  <text x="502" y="235" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="700"
        fill="url(#titleGrad)" letter-spacing="-2">Frosted Glass</text>
  <text x="504" y="304" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="700"
        fill="#FFFFFF" opacity="0.94" letter-spacing="-2">Overlay</text>

  <line x1="504" y1="344" x2="930" y2="344" stroke="#FFFFFF" stroke-width="1.5" opacity="0.28"/>

  <text x="506" y="390" width="454" font-family="Segoe UI, Microsoft YaHei" font-size="22"
        fill="#F4FBFF" opacity="0.86">
    Blur the exact background region, crop it to a rounded pane, then add a milky tint and bright edge to simulate refractive glass.
  </text>

  <rect x="506" y="474" width="212" height="56" rx="28" fill="#FFFFFF" opacity="0.18" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.38"/>
  <text x="542" y="510" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        fill="#FFFFFF">Explore effect</text>

  <line x1="756" y1="502" x2="930" y2="502" stroke="#FFFFFF" stroke-width="1.5" opacity="0.25"/>
  <text x="756" y="487" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600"
        fill="#D8F7FF" opacity="0.82">MORPH-FRIENDLY LAYERS</text>
  <text x="756" y="527" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#FFFFFF" opacity="0.72">Move pane, text, and subject across duplicate slides.</text>

  <circle cx="1018" cy="194" r="74" fill="#8BF6FF" opacity="0.16" filter="url(#softGlow)"/>
  <image x="876" y="248" width="344" height="344" preserveAspectRatio="xMidYMid meet"
         href="https://images.example.com/transparent-premium-wireless-headphones-overlapping-glass.png"/>

  <rect x="92" y="514" width="254" height="82" rx="28" fill="#07101D" opacity="0.46"/>
  <rect x="93" y="515" width="252" height="80" rx="27" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.18"/>
  <text x="122" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600"
        fill="#FFFFFF" opacity="0.84">Unblurred context</text>
  <text x="122" y="574" width="198" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        fill="#BBD6E8" opacity="0.78">The scene remains visible outside the pane.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on `filter="url(#blur)"` directly on a live `<image>` unless your pipeline confirms image filters translate; safest PowerPoint output uses a pre-blurred duplicate image cropped with `clipPath`.
- ❌ Do not use SVG `<mask>` to create the rounded glass crop; use `<clipPath>` on the blurred `<image>` instead.
- ❌ Do not clip the tint, border, or highlight shapes with `clip-path`; draw them as rounded `<rect>` elements with matching `x/y/width/height/rx`.
- ❌ Do not make the pane a flat semi-transparent white rectangle only; without the blurred duplicate background, the effect reads as a pale card rather than frosted glass.
- ❌ Do not place dense text directly over high-detail areas unless the milky tint opacity is strong enough for legibility.

## Composition notes
- Put the glass pane over the most colorful or high-contrast part of the background; the blur needs visible color variation to feel refractive.
- Reserve 50–60% of the slide for the pane, usually center-right, leaving one side of the original background exposed for contrast.
- Let a product, person, or abstract object overlap the pane edge to create depth; this is what makes the glass feel like a physical layer.
- Keep text white or pale cyan with generous line spacing; the pane should simplify the background, not become a busy UI dashboard.