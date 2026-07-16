# SVG Recipe — Rule of Thirds Data Highlight Composition

## Visual mechanism
A full-height photographic crop occupies exactly the left third of the slide, creating an immediate emotional anchor on the rule-of-thirds line. The right two-thirds remain mostly white space, with a large editorial headline and a custom horizontal bar chart where one key metric is highlighted in a vivid accent color.

## SVG primitives needed
- 1× `<image>` for the full-height left-third hero photo
- 1× `<clipPath>` with a rectangular crop to force the image into the exact one-third column
- 5× `<rect>` for horizontal data bar tracks
- 5× `<rect>` for filled data bars, with one highlighted accent bar and four muted bars
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a subtle vertical divider/accent at the one-third boundary
- 2× `<rect>` for small executive-summary callout cards
- 1× `<linearGradient>` for a dark-to-transparent photo overlay
- 1× `<linearGradient>` for the highlighted teal data bar
- 1× `<filter id="softShadow">` applied to the callout cards
- Multiple `<text>` elements with explicit `width` attributes for eyebrow, title, subtitle, labels, values, and callout copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="leftThirdCrop">
      <rect x="0" y="0" width="426.7" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="photoShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.15"/>
      <stop offset="68%" stop-color="#0F172A" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.36"/>
    </linearGradient>

    <linearGradient id="tealBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#51C4AB"/>
      <stop offset="100%" stop-color="#2AAE9A"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image
    href="https://images.example.com/editorial-photo-business-leader-looking-right-full-height.jpg"
    x="0" y="0" width="426.7" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#leftThirdCrop)"/>

  <rect x="0" y="0" width="426.7" height="720" fill="url(#photoShade)"/>
  <rect x="426.7" y="0" width="5" height="720" fill="#51C4AB"/>

  <text x="48" y="610" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" letter-spacing="2" fill="#FFFFFF" opacity="0.86">
    CUSTOMER PRIORITY STUDY
  </text>
  <text x="48" y="646" width="305" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="700" fill="#FFFFFF">
    What buyers need before they commit
  </text>

  <text x="520" y="76" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.2" fill="#51C4AB">
    EXECUTIVE SUMMARY
  </text>

  <text x="520" y="138" width="590" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700" fill="#282828">
    Availability is the strongest purchase driver
  </text>

  <text x="522" y="218" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#787878">
    Survey results show that customers prioritize product availability above price, support, and delivery speed.
  </text>

  <rect x="520" y="282" width="250" height="86" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="544" y="318" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="32" font-weight="800" fill="#51C4AB">92%</text>
  <text x="544" y="344" width="185" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#282828">rank availability first</text>

  <rect x="790" y="282" width="250" height="86" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="814" y="318" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="32" font-weight="800" fill="#282828">2.4×</text>
  <text x="814" y="344" width="188" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#787878">more decisive than price</text>

  <text x="520" y="424" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="1.8" fill="#A0A0A0">
    PURCHASE FACTORS
  </text>

  <text x="520" y="472" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#282828">Availability</text>
  <rect x="720" y="453" width="380" height="22" rx="11" fill="#ECECEC"/>
  <rect x="720" y="453" width="350" height="22" rx="11" fill="url(#tealBar)"/>
  <text x="1120" y="472" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#282828">92%</text>

  <text x="520" y="516" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#5E5E5E">Price</text>
  <rect x="720" y="497" width="380" height="22" rx="11" fill="#F0F0F0"/>
  <rect x="720" y="497" width="258" height="22" rx="11" fill="#DCDCDC"/>
  <text x="1120" y="516" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#787878">68%</text>

  <text x="520" y="560" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#5E5E5E">Support</text>
  <rect x="720" y="541" width="380" height="22" rx="11" fill="#F0F0F0"/>
  <rect x="720" y="541" width="205" height="22" rx="11" fill="#DCDCDC"/>
  <text x="1120" y="560" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#787878">54%</text>

  <text x="520" y="604" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#5E5E5E">Reviews</text>
  <rect x="720" y="585" width="380" height="22" rx="11" fill="#F0F0F0"/>
  <rect x="720" y="585" width="163" height="22" rx="11" fill="#DCDCDC"/>
  <text x="1120" y="604" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#787878">43%</text>

  <text x="520" y="648" width="175" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#5E5E5E">Shipping speed</text>
  <rect x="720" y="629" width="380" height="22" rx="11" fill="#F0F0F0"/>
  <rect x="720" y="629" width="118" height="22" rx="11" fill="#DCDCDC"/>
  <text x="1120" y="648" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#787878">31%</text>
</svg>
```

## Avoid in this skill
- ❌ Default Excel-style charts with axes, gridlines, legends, or heavy borders; the effect depends on a custom minimalist bar chart.
- ❌ Centering the photo or making it half the slide; the visual tension comes from the exact one-third / two-thirds split.
- ❌ Filling the right side with dense copy; keep the data area editorial, sparse, and instantly readable.
- ❌ Using `<mask>` for the photo fade; use a clipped image plus a transparent gradient overlay rectangle instead.
- ❌ Using chart arrows via `marker-end` on `<path>`; if directional annotations are needed, use `<line>` with marker attributes directly on the line.

## Composition notes
- Put the photographic subject on the left third and, ideally, choose an image where the person faces toward the data on the right.
- Keep the title and subtitle in the upper-right quadrant, leaving generous white space between the headline and the chart.
- Align chart labels, bar starts, and values to three clean vertical columns for a premium consulting-deck look.
- Use one vivid accent color only for the critical metric; all other bars should be pale gray so the highlight is understood immediately.