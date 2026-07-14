# SVG Recipe — Vertical Image Strip Split

## Visual mechanism
A premium split composition: the left two-thirds carry a calm editorial message, while the right edge becomes a vertical gallery strip of four rounded square image crops. Subtle gradients, shadows, and small caption tabs make the image column feel like a curated profile carousel rather than a simple grid.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and right-side image rail
- 4× `<rect>` for photo-card shadow/backing plates
- 4× `<image>` clipped into rounded square crops for the vertical strip
- 4× `<clipPath>` with rounded `<rect>` crops applied only to images
- 1× `<path>` for the large organic editorial glow behind the text block
- 1× `<line>` for the vertical split divider
- 6× `<circle>` for small accent dots and bullet markers
- 7× `<text>` blocks with explicit `width` for label, headline, body, bullets, and image captions
- 2× `<linearGradient>` for the background and right rail
- 1× `<radialGradient>` for the soft editorial glow
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for card elevation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F5EF"/>
      <stop offset="58%" stop-color="#F1EEE6"/>
      <stop offset="100%" stop-color="#E7E0D3"/>
    </linearGradient>

    <linearGradient id="railFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.86"/>
      <stop offset="100%" stop-color="#E8DFD0" stop-opacity="0.92"/>
    </linearGradient>

    <radialGradient id="accentGlow" cx="40%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#D79B68" stop-opacity="0.35"/>
      <stop offset="52%" stop-color="#D79B68" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#D79B68" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipImg1">
      <rect x="1010" y="56" width="150" height="150" rx="24" ry="24"/>
    </clipPath>
    <clipPath id="clipImg2">
      <rect x="1010" y="211" width="150" height="150" rx="24" ry="24"/>
    </clipPath>
    <clipPath id="clipImg3">
      <rect x="1010" y="366" width="150" height="150" rx="24" ry="24"/>
    </clipPath>
    <clipPath id="clipImg4">
      <rect x="1010" y="521" width="150" height="150" rx="24" ry="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-80 80 C120 -70 385 8 500 165 C610 318 505 495 322 545 C145 594 -35 502 -60 328 C-78 206 -170 155 -80 80 Z"
        fill="url(#accentGlow)"/>

  <rect x="882" y="0" width="398" height="720" fill="url(#railFill)"/>
  <line x1="868" y1="70" x2="868" y2="650" stroke="#C9BBA6" stroke-width="1.6" stroke-dasharray="5 11"/>

  <circle cx="96" cy="90" r="5" fill="#B9784B"/>
  <circle cx="116" cy="90" r="5" fill="#D9C6A7"/>
  <text x="92" y="108" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        font-weight="700" letter-spacing="2.5" fill="#9B6A47">TEAM OPERATING MODEL</text>

  <text x="90" y="185" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="62"
        font-weight="700" fill="#1F2B2D">
    <tspan x="90" dy="0">From insight to</tspan>
    <tspan x="90" dy="72">field-ready teams</tspan>
  </text>

  <text x="94" y="360" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="23"
        font-weight="400" fill="#4E5C5E">
    <tspan x="94" dy="0">A compact profile layout for introducing four leaders,</tspan>
    <tspan x="94" dy="36">feature owners, client segments, or launch workstreams</tspan>
    <tspan x="94" dy="36">beside a strong editorial narrative.</tspan>
  </text>

  <circle cx="106" cy="513" r="6" fill="#B9784B"/>
  <text x="126" y="520" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="20"
        font-weight="600" fill="#263235">One message, four proof points</text>

  <circle cx="106" cy="562" r="6" fill="#B9784B"/>
  <text x="126" y="569" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="20"
        font-weight="600" fill="#263235">Ideal for people, products, regions, or pillars</text>

  <text x="902" y="54" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        font-weight="700" letter-spacing="2.2" fill="#8F6B4B">FIELD PROFILES</text>

  <rect x="1000" y="56" width="150" height="150" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="1010" y="56" width="150" height="150" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1494790108377-be9c29b29330"
         clip-path="url(#clipImg1)"/>
  <text x="902" y="128" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#263235">Strategy</text>
  <text x="902" y="153" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        font-weight="600" letter-spacing="1.4" fill="#A47B57">01</text>

  <rect x="1000" y="211" width="150" height="150" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="1010" y="211" width="150" height="150" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1500648767791-00dcc994a43e"
         clip-path="url(#clipImg2)"/>
  <text x="902" y="283" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#263235">Design</text>
  <text x="902" y="308" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        font-weight="600" letter-spacing="1.4" fill="#A47B57">02</text>

  <rect x="1000" y="366" width="150" height="150" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="1010" y="366" width="150" height="150" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1517841905240-472988babdf9"
         clip-path="url(#clipImg3)"/>
  <text x="902" y="438" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#263235">Delivery</text>
  <text x="902" y="463" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        font-weight="600" letter-spacing="1.4" fill="#A47B57">03</text>

  <rect x="1000" y="521" width="150" height="150" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="1010" y="521" width="150" height="150" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1527980965255-d3b416303d12"
         clip-path="url(#clipImg4)"/>
  <text x="902" y="593" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#263235">Scale</text>
  <text x="902" y="618" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        font-weight="600" letter-spacing="1.4" fill="#A47B57">04</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to caption overlays or decorative rectangles; use rounded `<rect>` geometry directly and reserve clipping for `<image>` only.
- ❌ Building the four-image column with `<use>` or symbols; duplicate the native shapes so PowerPoint keeps every card editable.
- ❌ Using `mask` to fade images at the rail edge; masks are not reliable in the PPT translation path.
- ❌ Placing long body copy inside the right strip; the rail should remain primarily visual and scannable.
- ❌ Putting shadows on `<line>` dividers; filters on lines are dropped, so use subtle stroke color instead.

## Composition notes
- Keep the left text area between `x=90` and `x=780`; this preserves a strong negative-space buffer before the image rail.
- Use the rightmost 30% of the canvas for the vertical strip, with four evenly spaced square crops and small caption labels to their left.
- Let the headline dominate the slide; the photo column should validate the message, not compete with it.
- Repeat one warm accent color across the label, bullets, image numbers, and soft glow to unify the split layout.