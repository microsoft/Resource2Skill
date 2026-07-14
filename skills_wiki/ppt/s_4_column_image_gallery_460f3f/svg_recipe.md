# SVG Recipe — 4-Column Image Gallery

## Visual mechanism
A premium gallery row uses four equal portrait crops as the dominant visual rhythm, with generous gutters and a short headline above. Each image sits in a rounded vertical card with soft shadow, subtle border, and a small accent tag so the grid feels intentional rather than like four raw photos.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<path>` for soft abstract background blobs that add color without competing with the photos
- 4× `<clipPath>` each containing a rounded `<rect>` to crop portrait images to card shape
- 4× `<rect>` for soft shadow card bases using a blur/offset filter
- 4× `<image>` for the portrait-oriented gallery items, each clipped to a rounded rectangle
- 4× `<rect>` for thin rounded card borders over the images
- 4× `<rect>` for small translucent label pills at the bottom of each image
- 5× `<text>` for the headline and four short image labels; every text element has explicit `width`
- 1× `<filter id="cardShadow">` applied to card base rectangles
- 2× `<linearGradient>` fills for the background and accent styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF7EC"/>
      <stop offset="0.52" stop-color="#F7FBFF"/>
      <stop offset="1" stop-color="#EEF2FF"/>
    </linearGradient>

    <linearGradient id="warmAccent" x1="80" y1="185" x2="1200" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF7A59"/>
      <stop offset="0.45" stop-color="#FFB84D"/>
      <stop offset="1" stop-color="#6C63FF"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipPortrait1">
      <rect x="80" y="214" width="262" height="350" rx="30" ry="30"/>
    </clipPath>
    <clipPath id="clipPortrait2">
      <rect x="366" y="214" width="262" height="350" rx="30" ry="30"/>
    </clipPath>
    <clipPath id="clipPortrait3">
      <rect x="652" y="214" width="262" height="350" rx="30" ry="30"/>
    </clipPath>
    <clipPath id="clipPortrait4">
      <rect x="938" y="214" width="262" height="350" rx="30" ry="30"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40,88 C92,10 238,18 318,112 C397,204 300,315 144,310 C21,307 -61,228 -40,88 Z"
        fill="#FFE0C2" opacity="0.55"/>
  <path d="M1038,42 C1163,-10 1296,31 1341,139 C1388,251 1297,350 1167,328 C1050,309 970,212 990,126 C998,91 1012,62 1038,42 Z"
        fill="#D9E4FF" opacity="0.78"/>

  <text x="80" y="92" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700" fill="#1E2432">
    Four perspectives, <tspan fill="#FF7A59">one visual story</tspan>
  </text>
  <text x="82" y="134" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#667085">
    A clean portrait gallery shell for teams, products, campaigns, or before/after comparisons.
  </text>

  <rect x="80" y="214" width="262" height="350" rx="30" ry="30" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.9"/>
  <image x="80" y="214" width="262" height="350" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portrait-gallery/team-lead-in-sunlit-studio.jpg"
         clip-path="url(#clipPortrait1)"/>
  <rect x="80" y="214" width="262" height="350" rx="30" ry="30" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.9"/>
  <rect x="106" y="505" width="142" height="36" rx="18" ry="18" fill="#111827" opacity="0.72"/>
  <text x="124" y="529" width="112" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#FFFFFF">01 / Strategy</text>

  <rect x="366" y="214" width="262" height="350" rx="30" ry="30" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.9"/>
  <image x="366" y="214" width="262" height="350" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portrait-gallery/designer-holding-product-prototype.jpg"
         clip-path="url(#clipPortrait2)"/>
  <rect x="366" y="214" width="262" height="350" rx="30" ry="30" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.9"/>
  <rect x="392" y="505" width="132" height="36" rx="18" ry="18" fill="#111827" opacity="0.72"/>
  <text x="410" y="529" width="102" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#FFFFFF">02 / Design</text>

  <rect x="652" y="214" width="262" height="350" rx="30" ry="30" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.9"/>
  <image x="652" y="214" width="262" height="350" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portrait-gallery/product-detail-on-bold-color-backdrop.jpg"
         clip-path="url(#clipPortrait3)"/>
  <rect x="652" y="214" width="262" height="350" rx="30" ry="30" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.9"/>
  <rect x="678" y="505" width="132" height="36" rx="18" ry="18" fill="#111827" opacity="0.72"/>
  <text x="696" y="529" width="102" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#FFFFFF">03 / Build</text>

  <rect x="938" y="214" width="262" height="350" rx="30" ry="30" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.9"/>
  <image x="938" y="214" width="262" height="350" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portrait-gallery/customer-celebrating-launch-moment.jpg"
         clip-path="url(#clipPortrait4)"/>
  <rect x="938" y="214" width="262" height="350" rx="30" ry="30" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.9"/>
  <rect x="964" y="505" width="144" height="36" rx="18" ry="18" fill="#111827" opacity="0.72"/>
  <text x="982" y="529" width="114" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#FFFFFF">04 / Launch</text>

  <rect x="80" y="594" width="1120" height="5" rx="2.5" fill="url(#warmAccent)" opacity="0.85"/>
  <circle cx="80" cy="596.5" r="7" fill="#FF7A59"/>
  <circle cx="1200" cy="596.5" r="7" fill="#6C63FF"/>
</svg>
```

## Avoid in this skill
- ❌ Placing four uncropped images directly on the slide; inconsistent source aspect ratios will make the gallery feel messy.
- ❌ Applying `clip-path` to rectangles or groups; for this workflow, apply clipping only to `<image>` elements.
- ❌ Using `<pattern>` fills for photo placeholders; they will not translate reliably and do not communicate real image intent.
- ❌ Overloading the gallery with long captions; this layout works best when the images remain the main content.

## Composition notes
- Keep the headline in the upper-left 15–20% of the slide and let the image row own the center.
- Use equal card widths, equal gutters, and a shared baseline; the strength of the technique is the repeated portrait rhythm.
- Favor rounded image crops, soft shadows, and thin white borders to create a premium editorial look.
- If labels are needed, keep them short and place them inside translucent pills over the lower image area.