# SVG Recipe — Dynamic Wave Split-Screen Layout

## Visual mechanism
A clean white text field is split from a photographic hero area by a large organic S-curve. The photo is clipped to the right-side wave, while offset yellow and blue wavy layers underneath create a crisp, dimensional “paper overlap” edge.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<clipPath>` with a custom `<path>` for the right-side photo crop
- 1× `<image>` clipped by the wave path for the architectural / corporate hero photo
- 2× `<path>` for the offset yellow accent wave and the narrow blue wave divider
- 2× `<rect>` for the small logo badge and rounded CTA pill
- 2× `<line>` for subtle top and bottom horizontal rules
- 6× `<text>` for logo, title hierarchy, body copy, CTA, and small labels if needed
- 3× small icon groups using `<circle>`, `<rect>`, `<line>`, and `<path>` for footer service symbols
- 1× `<linearGradient>` for the CTA / logo blue treatment
- 1× `<filter id="softShadow">` applied to the logo badge and CTA pill for subtle elevation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoWaveClip">
      <path d="M1280 0 L1280 720 L760 720
               C730 610 704 520 728 410
               C752 300 817 190 812 0 Z"/>
    </clipPath>

    <linearGradient id="corpBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B8DCE"/>
      <stop offset="100%" stop-color="#0055A4"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Fine top rule -->
  <line x1="112" y1="37" x2="220" y2="37" stroke="#8BA6BD" stroke-width="1.2"/>

  <!-- Offset accent wave: shift left so it peeks out behind the photo -->
  <path d="M1280 0 L1280 720 L714 720
           C678 610 654 520 682 410
           C710 300 780 188 786 0 Z"
        fill="#FFC000"/>

  <!-- Blue divider wave, slightly wider than a hairline so it feels intentional -->
  <path d="M1280 0 L1280 720 L746 720
           C716 610 690 520 716 410
           C742 300 806 190 802 0
           L820 0
           C824 190 760 300 736 410
           C712 520 738 610 772 720
           L1280 720 L1280 0 Z"
        fill="#0078B8"/>

  <!-- Hero photo clipped to the same organic right-side geometry -->
  <image x="655" y="0" width="625" height="720"
         href="https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&amp;w=1400&amp;auto=format&amp;fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoWaveClip)"/>

  <!-- Logo badge -->
  <rect x="123" y="156" width="75" height="40" rx="7" fill="url(#corpBlue)" filter="url(#softShadow)"/>
  <text x="138" y="182" width="48"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#FFFFFF">LOGO</text>

  <!-- Main title block -->
  <text x="123" y="279" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800" fill="#FFC000">商务服务</text>

  <text x="123" y="356" width="540"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="800" fill="#0078B8">对接方案可行性报告</text>

  <!-- Body copy -->
  <text x="123" y="405" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="10.5" fill="#555555">
    <tspan x="123" dy="0">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce</tspan>
    <tspan x="123" dy="12">posuere, magna sed pulvinar ultricies, purus lectus malesuada libero, sit amet commodo magna eros</tspan>
    <tspan x="123" dy="12">quis urna.</tspan>
    <tspan x="123" dy="26">Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.</tspan>
    <tspan x="123" dy="26">Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin</tspan>
    <tspan x="123" dy="12">pharetra nonummy pede. Mauris et orci.</tspan>
  </text>

  <!-- CTA pill -->
  <rect x="123" y="512" width="124" height="31" rx="16" fill="url(#corpBlue)" filter="url(#softShadow)"/>
  <text x="161" y="535" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#FFFFFF">iSlide</text>

  <!-- Footer rule -->
  <line x1="123" y1="681" x2="577" y2="681" stroke="#9BB2C3" stroke-width="1"/>

  <!-- Footer icon 1: presentation -->
  <g transform="translate(131 651)" fill="none" stroke="#0078B8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <rect x="5" y="7" width="18" height="14" rx="1.5"/>
    <line x1="14" y1="21" x2="14" y2="29"/>
    <line x1="9" y1="29" x2="19" y2="29"/>
    <circle cx="2.5" cy="5" r="2.2" fill="#0078B8" stroke="none"/>
    <path d="M2.5 9 L2.5 22 M-1 14 L6 14"/>
  </g>

  <!-- Footer icon 2: clipboard -->
  <g transform="translate(174 650)" fill="none" stroke="#0078B8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <rect x="4" y="6" width="15" height="22" rx="2"/>
    <rect x="8" y="2" width="7" height="6" rx="1.3"/>
    <line x1="8" y1="13" x2="16" y2="13"/>
    <line x1="8" y1="18" x2="16" y2="18"/>
    <line x1="8" y1="23" x2="14" y2="23"/>
  </g>

  <!-- Footer icon 3: people / service -->
  <g transform="translate(213 651)" fill="none" stroke="#0078B8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="5" cy="5" r="3" fill="#0078B8" stroke="none"/>
    <path d="M5 10 L5 24 M1 15 L9 15 M2 29 L5 24 L8 29"/>
    <rect x="14" y="8" width="12" height="13" rx="1.5"/>
    <line x1="17" y1="13" x2="23" y2="13"/>
    <line x1="17" y1="17" x2="23" y2="17"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the yellow or blue accent `<path>` layers; only the `<image>` should be clipped.
- ❌ Using a rectangular photo crop with a wavy white shape placed on top; it will look less editable and can leave visible seams.
- ❌ Using `<mask>` to create the wave edge; masks are not reliable for this PPT translation target.
- ❌ Using `marker-end` for decorative arrows or dividers near the text; this layout should rely on clean lines and organic geometry.
- ❌ Overcrowding the left text column; the premium effect depends on generous white space.

## Composition notes
- Keep the left content column within roughly `x=120–590`; the wave should begin around the center-right so the title never collides with the image.
- The photo should occupy the full slide height and at least the right 45–50% of the canvas for a cinematic cover-slide feel.
- Let the yellow accent peek out more than the blue divider; yellow provides warmth and depth, while blue visually links the title and brand.
- Use a very small top rule and footer icon row to balance the heavy right-side image without adding clutter.