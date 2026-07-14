# SVG Recipe — Minimalist Rule of Thirds Data Storytelling Layout

## Visual mechanism
A full-height photographic anchor occupies the left third of the slide, while the right two-thirds remain quiet and spacious for one decisive headline and a stripped-down horizontal bar chart. The viewer’s eye moves from emotional context to quantitative proof without axes, legends, or visual clutter.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background.
- 1× `<clipPath>` with a `<rect>` for cropping the left-third hero image.
- 1× `<image>` for the full-bleed left visual anchor.
- 2× `<linearGradient>` for the subtle photo overlay and accent fade.
- 1× `<filter id="softShadow">` applied to the insight card.
- 1× `<rect>` for a translucent overlay on the photo.
- 1× `<line>` for the subtle vertical rule-of-thirds divider.
- 6× `<text>` blocks for eyebrow, headline, subtitle, chart title, takeaway, and footer note.
- 4× `<rect>` for pale chart tracks.
- 4× `<rect>` for teal filled data bars.
- 4× `<text>` for category labels.
- 4× `<text>` for percent labels.
- 1× `<rect>` for the minimalist insight card.
- 1× `<path>` for a small decorative accent mark inside the insight card.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="leftThirdCrop">
      <rect x="0" y="0" width="426" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="photoShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#092F2F" stop-opacity="0.26"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.24"/>
    </linearGradient>

    <linearGradient id="tealBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#38B2AC"/>
      <stop offset="100%" stop-color="#5EEAD4"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F9FB"/>

  <image
    href="https://images.example.com/photo-customer-using-mobile-app-cropped-hands-no-face.jpg"
    x="0" y="0" width="426" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#leftThirdCrop)"/>

  <rect x="0" y="0" width="426" height="720" fill="url(#photoShade)" opacity="0.95"/>
  <line x1="426" y1="0" x2="426" y2="720" stroke="#E5E7EB" stroke-width="1"/>

  <text x="560" y="104" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.4"
        fill="#38B2AC">CUSTOMER EXPERIENCE SURVEY</text>

  <text x="558" y="178" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700"
        fill="#1F2937">Availability drives retention.</text>

  <text x="560" y="222" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#6B7280">Users are most likely to stay when the service feels always-on, fast, and easy to reach.</text>

  <text x="560" y="314" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700"
        fill="#374151">Top factors influencing renewal</text>

  <text x="560" y="372" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600"
        fill="#374151">Availability</text>
  <rect x="742" y="350" width="360" height="24" rx="12" fill="#E8EEF2"/>
  <rect x="742" y="350" width="328" height="24" rx="12" fill="url(#tealBar)"/>
  <text x="1085" y="371" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700"
        fill="#1F2937">91%</text>

  <text x="560" y="426" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600"
        fill="#374151">Response time</text>
  <rect x="742" y="404" width="360" height="24" rx="12" fill="#E8EEF2"/>
  <rect x="742" y="404" width="281" height="24" rx="12" fill="url(#tealBar)"/>
  <text x="1038" y="425" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700"
        fill="#1F2937">78%</text>

  <text x="560" y="480" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600"
        fill="#374151">Ease of use</text>
  <rect x="742" y="458" width="360" height="24" rx="12" fill="#E8EEF2"/>
  <rect x="742" y="458" width="252" height="24" rx="12" fill="url(#tealBar)"/>
  <text x="1009" y="479" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700"
        fill="#1F2937">70%</text>

  <text x="560" y="534" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600"
        fill="#374151">Price clarity</text>
  <rect x="742" y="512" width="360" height="24" rx="12" fill="#E8EEF2"/>
  <rect x="742" y="512" width="194" height="24" rx="12" fill="url(#tealBar)"/>
  <text x="951" y="533" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700"
        fill="#1F2937">54%</text>

  <rect x="560" y="586" width="560" height="78" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M590 623 C600 606, 617 603, 632 615 C646 627, 666 623, 678 605"
        fill="none" stroke="#38B2AC" stroke-width="5" stroke-linecap="round"/>
  <text x="708" y="625" width="365"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700"
        fill="#1F2937">Prioritize uptime messaging in the renewal journey.</text>
  <text x="708" y="649" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="400"
        fill="#6B7280">n=2,418 active customers · Q4 pulse survey</text>
</svg>
```

## Avoid in this skill
- ❌ Dense chart furniture: axes, gridlines, legends, tick marks, and borders defeat the minimalist data-storytelling effect.
- ❌ Placing text immediately beside the photo edge; preserve a breathing gap between the left third and the right-side content.
- ❌ Using many accent colors; the method works best with one data color and restrained neutrals.
- ❌ Cropping a face awkwardly in the left-third image; use an intentional photo crop, ideally hands, product use, workspace detail, or a non-identifying customer moment.
- ❌ Building the bar chart as an embedded screenshot; use native SVG rectangles and text so the resulting PowerPoint remains editable.

## Composition notes
- Keep the photo locked to the left 33% of the canvas; the visual weight belongs there, but the data story lives on the right.
- Start right-side content around x=550–570 to create deliberate white space after the one-third divider.
- Place the headline in the upper third and the chart in the middle third; reserve the lower third for a single takeaway or source note.
- Use teal only for the data bars and small navigation accents so the quantitative proof becomes the focal rhythm.