# SVG Recipe — Pictogram Stacked Bar Chart

## Visual mechanism
Replace horizontal bar segments with repeated thematic icons, so the “length” of each bar is read as a count of pictograms rather than a flat rectangle. A dark photo backdrop plus glowing accent-colored icons turns a normal category chart into an executive infographic.

## SVG primitives needed
- 1× `<image>` for the full-bleed contextual background photo.
- 3× `<rect>` for dark tint overlays, left hero gradient wash, and the translucent chart panel.
- 1× `<linearGradient>` for the asymmetric background tint.
- 1× `<radialGradient>` for the cyan glow behind the chart.
- 2× `<filter>` definitions: one soft panel shadow and one subtle pictogram glow.
- 5× `<line>` for faint horizontal row guides.
- 1× `<line>` for the vertical chart baseline.
- 36× `<path>` for repeated editable T-shirt pictograms, including one half-width pictogram approximation for a partial unit.
- 15× `<text>` for title, subtitle, KPI callout, category labels, value labels, axis note, and legend.
- Optional 1× `<path>` decorative curve/accent to connect the hero narrative to the chart area.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgTint" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#101626" stop-opacity="0.96"/>
      <stop offset="42%" stop-color="#202943" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#222A40" stop-opacity="0.70"/>
    </linearGradient>
    <radialGradient id="cyanAura" cx="68%" cy="52%" r="48%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.28"/>
      <stop offset="52%" stop-color="#00E5FF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="iconGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
  </defs>

  <image href="https://images.unsplash.com/photo-1445205170230-053b83016050?w=1600&amp;q=80" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgTint)"/>
  <rect x="430" y="0" width="850" height="720" fill="url(#cyanAura)"/>
  <rect x="470" y="112" width="720" height="486" rx="34" fill="#0D1424" opacity="0.54" filter="url(#panelShadow)"/>

  <text x="72" y="92" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#8CEEFF" letter-spacing="3">RETAIL PERFORMANCE</text>
  <text x="72" y="158" width="365" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF">NEXT 品牌服飾</text>
  <text x="72" y="204" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#CAD5E8">2019 Q3 各品類營收業績</text>
  <text x="72" y="292" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="800" fill="#00E5FF">7.1K</text>
  <text x="76" y="328" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#DDE7F6">Total revenue units represented by pictograms</text>
  <path d="M72 382 C150 356, 252 380, 336 338" fill="none" stroke="#00E5FF" stroke-width="3" stroke-opacity="0.55" stroke-dasharray="8 10"/>

  <text x="520" y="78" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Category revenue as stacked icons</text>
  <text x="520" y="107" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#AEBAD0">Each shirt pictogram represents 200 units; the half icon indicates a proportional remainder.</text>

  <line x1="520" y1="190" x2="1135" y2="190" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="520" y1="270" x2="1135" y2="270" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="520" y1="350" x2="1135" y2="350" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="520" y1="430" x2="1135" y2="430" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="520" y1="510" x2="1135" y2="510" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="520" y1="158" x2="520" y2="540" stroke="#00E5FF" stroke-opacity="0.45" stroke-width="2"/>

  <text x="494" y="205" width="160" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E7EEF8">內衣 Innerwear</text>
  <text x="494" y="285" width="160" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E7EEF8">褲子 Pants</text>
  <text x="494" y="365" width="160" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E7EEF8">洋裝 Dress</text>
  <text x="494" y="445" width="160" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E7EEF8">上衣 Top</text>
  <text x="494" y="525" width="160" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E7EEF8">外套 Jacket</text>

  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(540 174)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(578 174)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(616 174)" fill="#00E5FF" filter="url(#iconGlow)"/>

  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(540 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(578 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(616 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(654 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(692 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(730 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(768 254)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H17 V31 H9 V14 L5 17 L1 10 Z" transform="translate(806 254)" fill="#00E5FF" opacity="0.78" filter="url(#iconGlow)"/>

  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(540 334)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(578 334)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(616 334)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(654 334)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(692 334)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(730 334)" fill="#00E5FF" filter="url(#iconGlow)"/>

  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(540 414)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(578 414)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(616 414)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(654 414)" fill="#00E5FF" filter="url(#iconGlow)"/>

  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(540 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(578 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(616 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(654 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(692 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(730 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(768 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(806 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(844 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(882 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(920 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(958 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(996 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(1034 494)" fill="#00E5FF" filter="url(#iconGlow)"/>
  <path d="M10 3 H22 L31 10 L27 17 L23 14 V31 H9 V14 L5 17 L1 10 Z" transform="translate(1072 494)" fill="#00E5FF" filter="url(#iconGlow)"/>

  <text x="676" y="205" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#00E5FF">600</text>
  <text x="850" y="285" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#00E5FF">1,500</text>
  <text x="776" y="365" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#00E5FF">1,200</text>
  <text x="706" y="445" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#00E5FF">800</text>
  <text x="1142" y="525" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#00E5FF">3,000</text>
  <text x="520" y="586" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#92A0B8">Scale: 1 pictogram = 200 revenue units</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to repeat the icon, even though it is tempting; duplicate the editable `<path>` pictogram instances directly.
- ❌ Do not use `<pattern>` fills for the pictogram bar; pattern fills are not reliably translated into editable PowerPoint shapes.
- ❌ Do not apply `clip-path` to icon paths for partial pictograms; clipping non-image shapes is ignored. Draw a simplified partial icon path instead, or use a pre-cropped `<image>` only if the icon is intentionally raster.
- ❌ Do not build this as a native SVG chart with hidden data bindings; the mechanism is manual visual encoding with icons, labels, and guides.
- ❌ Do not put filters on `<line>` grid rules; keep shadows/glows on rectangles, text, or pictogram paths.

## Composition notes
- Keep the left 30–35% as a narrative hero area with title, timeframe, and one headline metric; reserve the right 65–70% for the pictogram rows.
- Use a single high-energy accent color for all icons and value labels so the eye connects quantities instantly.
- Leave enough horizontal spacing between pictograms that each icon is legible, but keep spacing tight enough that the row still reads as a continuous bar.
- A dark photo background works best when heavily tinted; the chart panel should be translucent, not opaque, to preserve the premium editorial feel.