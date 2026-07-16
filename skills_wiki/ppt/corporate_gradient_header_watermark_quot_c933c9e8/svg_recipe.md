# SVG Recipe — Corporate Gradient Header & Watermark Quote Frame

## Visual mechanism
A restrained corporate quote slide is anchored by a full-width teal gradient header, while oversized pale serif quotation marks act as watermark framing devices around a centered italic statement. The design feels editorial and branded without relying on heavy illustration.

## SVG primitives needed
- 1× `<rect>` for the light gray slide background
- 1× `<rect>` for the full-width gradient header bar
- 1× `<rect>` for a thin header-bottom divider
- 1× `<rect>` for the subtle central quote card
- 2× `<rect>` for small teal accent blocks on the quote card edges
- 3× `<path>` for soft header highlight ribbons and decorative quote-area accents
- 7× `<text>` for header label, section label, two watermark quote marks, quote body, author, and author role
- 1× `<line>` for the fine attribution rule
- 2× `<linearGradient>` for the header and accent fills
- 1× `<filter id="cardShadow">` applied to the quote card for soft elevation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGradient" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8FDFD6"/>
      <stop offset="45%" stop-color="#55BDB5"/>
      <stop offset="100%" stop-color="#2B9991"/>
    </linearGradient>

    <linearGradient id="accentGradient" x1="300" y1="0" x2="980" y2="140" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.24"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Base canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#F2F2F2"/>

  <!-- Branded gradient header -->
  <rect x="0" y="0" width="1280" height="84" fill="url(#headerGradient)"/>
  <path d="M0,0 L560,0 C500,42 360,74 180,84 L0,84 Z" fill="url(#accentGradient)"/>
  <path d="M720,0 L1280,0 L1280,84 C1070,72 890,40 720,0 Z" fill="#FFFFFF" opacity="0.12"/>
  <rect x="0" y="84" width="1280" height="3" fill="#23877F"/>

  <!-- Header typography -->
  <text x="72" y="52" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3" fill="#FFFFFF">
    INSIGHT FRAME
  </text>
  <text x="1180" y="52" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="2" fill="#EAFBFA">
    BRAND TEMPLATE / QUOTE
  </text>

  <!-- Quote card -->
  <rect x="190" y="150" width="900" height="450" rx="24" fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.94"/>
  <rect x="190" y="222" width="8" height="172" rx="4" fill="#2B9991"/>
  <rect x="1082" y="356" width="8" height="172" rx="4" fill="#8FDFD6"/>

  <!-- Large watermark quotation marks -->
  <text x="232" y="330" width="260" font-family="Georgia, 'Times New Roman', serif"
        font-size="230" font-weight="700" fill="#D7D7D7" opacity="0.72">
    “
  </text>
  <text x="996" y="560" width="260" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif"
        font-size="230" font-weight="700" fill="#D7D7D7" opacity="0.72">
    ”
  </text>

  <!-- Decorative accents behind quote text -->
  <path d="M342,246 C430,214 520,212 610,242" fill="none" stroke="#8FDFD6" stroke-width="5" opacity="0.35"/>
  <path d="M684,520 C764,552 860,548 942,508" fill="none" stroke="#2B9991" stroke-width="5" opacity="0.20"/>

  <!-- Main quote -->
  <text x="640" y="294" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-style="italic" font-weight="400" fill="#505050">
    <tspan x="640" dy="0">A great option to have in your</tspan>
    <tspan x="640" dy="48">presentation toolkit is a custom layout.</tspan>
    <tspan x="640" dy="48">It saves you time when you need</tspan>
    <tspan x="640" dy="48">to put together a slide deck in a hurry.</tspan>
  </text>

  <!-- Attribution -->
  <line x1="560" y1="514" x2="720" y2="514" stroke="#2B9991" stroke-width="3"/>
  <text x="640" y="552" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#3F3F3F">
    — Presentation Bootcamp
  </text>
  <text x="640" y="582" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="1.8" fill="#8A8A8A">
    CUSTOM LAYOUT SYSTEM
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<image>` for the gradient header; create it as a native `<linearGradient>` so it remains editable.
- ❌ Putting the oversized quotation marks inline with the quote body; they should be separate watermark text objects.
- ❌ Using `<mask>` or clipped non-image elements for faded quote marks; use pale fills and opacity instead.
- ❌ Omitting `width` on `<text>` elements, which can cause PowerPoint text boxes to render unpredictably.
- ❌ Overdecorating the center area; the quote must remain the dominant visual object.

## Composition notes
- Keep the header to roughly 10–12% of slide height so it brands the slide without competing with the quote.
- Place the quote card slightly below center, leaving generous negative space between the header and the statement.
- Use pale gray watermark marks at very large size; they should frame the text, not reduce legibility.
- Maintain a tight color rhythm: teal gradient in the header, small teal accents near the quote, and neutral gray typography.