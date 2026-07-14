# SVG Recipe — Left Hero Right Align Title

## Visual mechanism
A premium split cover layout: a large cinematic hero image anchors the left half, while sparse right-aligned typography occupies the open right side. Subtle gradients, a rounded image crop, and restrained accent lines create a polished executive-keynote feel without crowding the slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 1× `<rect>` behind the hero image for a soft elevated card shadow
- 1× `<image>` for the left hero visual, clipped to a rounded rectangle
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 2× `<linearGradient>` for background depth and photo-edge fade accents
- 1× `<radialGradient>` for a soft ambient glow behind the title area
- 1× `<filter id="cardShadow">` applied to the hero card backing
- 1× `<filter id="softGlow">` applied to decorative accent shapes
- 3× `<path>` for premium abstract accents and diagonal visual energy
- 3× `<line>` for thin editorial divider/accent rules
- 4× `<text>` blocks with explicit `width` for kicker, headline, subtitle, and footer metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070B14"/>
      <stop offset="52%" stop-color="#101827"/>
      <stop offset="100%" stop-color="#05070D"/>
    </linearGradient>

    <linearGradient id="photoFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#05070D" stop-opacity="0.58"/>
    </linearGradient>

    <radialGradient id="titleGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#3A86FF" stop-opacity="0.34"/>
      <stop offset="54%" stop-color="#1D3557" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="accentStroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7DD3FC" stop-opacity="0"/>
      <stop offset="48%" stop-color="#7DD3FC" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#A78BFA" stop-opacity="0.25"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="64" y="58" width="620" height="604" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDepth)"/>

  <ellipse cx="1002" cy="352" rx="315" ry="248" fill="url(#titleGlow)"/>

  <path d="M788 89 C936 34 1098 61 1215 148 C1127 122 1027 132 930 183 C857 221 805 254 734 250 C736 185 752 126 788 89 Z"
        fill="#2563EB" opacity="0.12" filter="url(#softGlow)"/>

  <path d="M1118 582 C1034 621 923 630 835 598 C900 569 944 526 996 481 C1040 442 1101 432 1194 456 C1182 510 1157 560 1118 582 Z"
        fill="#8B5CF6" opacity="0.13" filter="url(#softGlow)"/>

  <rect x="64" y="58" width="620" height="604" rx="34" ry="34"
        fill="#000000" opacity="0.38" filter="url(#cardShadow)"/>

  <image x="64" y="58" width="620" height="604"
         href="https://images.example.com/hero-photo-premium-electric-vehicle-studio-lighting.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>

  <rect x="64" y="58" width="620" height="604" rx="34" ry="34"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.4"/>

  <rect x="64" y="58" width="620" height="604" rx="34" ry="34"
        fill="url(#photoFade)" opacity="0.95"/>

  <path d="M660 72 L732 72 C746 72 757 83 757 97 L757 625 C757 639 746 650 732 650 L660 650"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="1.2"/>

  <line x1="798" y1="221" x2="1180" y2="221"
        stroke="url(#accentStroke)" stroke-width="2"/>

  <line x1="1040" y1="579" x2="1180" y2="579"
        stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>

  <line x1="1122" y1="598" x2="1180" y2="598"
        stroke="#7DD3FC" stroke-opacity="0.65" stroke-width="2"/>

  <text x="1180" y="180" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="3.2"
        fill="#7DD3FC" text-anchor="end">
    PRODUCT VISION 2026
  </text>

  <text x="1180" y="305" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66" font-weight="700" letter-spacing="-2.4"
        fill="#F8FAFC" text-anchor="end">
    <tspan x="1180" dy="0">Designed for</tspan>
    <tspan x="1180" dy="74">the next move</tspan>
  </text>

  <text x="1180" y="457" width="475"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#CBD5E1" text-anchor="end">
    <tspan x="1180" dy="0">A focused launch narrative with a cinematic</tspan>
    <tspan x="1180" dy="32">visual anchor and confident editorial spacing.</tspan>
  </text>

  <text x="1180" y="644" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="500" letter-spacing="1.5"
        fill="#94A3B8" text-anchor="end">
    SECTION 01  ·  MARKET INTRODUCTION
  </text>
</svg>
```

## Avoid in this skill
- ❌ Center-aligning the title; the visual identity depends on a crisp right rag aligned to the slide edge.
- ❌ Filling the right side with bullets or dense body copy; this layout works best as a cover or section divider.
- ❌ Using an un-cropped rectangular photo edge-to-edge; the rounded hero card and shadow are what make the image feel premium.
- ❌ Applying `clip-path` to overlay rectangles or decorative shapes; keep clipping on the `<image>` only for reliable PPT translation.
- ❌ Putting filters on `<line>` accents; use filters only on rectangles, paths, ellipses, circles, or text.

## Composition notes
- Keep the hero image to roughly the left 50–55% of the slide, with generous top/bottom margins and a refined rounded crop.
- Place all key typography in the rightmost 35–40% of the canvas, using `text-anchor="end"` and consistent `x` positions.
- Use one bright accent color sparingly: a kicker, one or two thin rules, and subtle glow are enough.
- Preserve negative space around the headline; the title should feel calm, expensive, and intentional.