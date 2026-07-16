# SVG Recipe — Mosaic Grid Image Reveal

## Visual mechanism
A full-height photo block is fragmented into a rigid 6×6 mosaic grid, with selected cells covered in pure white to “remove” pieces and other cells washed with translucent white. The text area on the left stays clean and editorial, while the image grid steps into the whitespace like a digital reveal.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<image>` for the full-height right-side landscape/photo block
- 12× opaque white `<rect>` for fully hidden mosaic cells that reveal the slide background
- 6× translucent white `<rect>` for washed-out mosaic cells
- 11× `<line>` for crisp grid dividers across the photo block
- 3× `<path>` for a simple editable rural/nature line icon above the title
- 1× accent `<rect>` with rounded corners for the small underline bar
- 4× `<text>` elements for title, subtitle, English label, and paragraph copy
- 1× `<linearGradient>` for a subtle left-to-right image fade highlight, applied as a translucent overlay rectangle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="softPhotoWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="52%" stop-color="#FFFFFF" stop-opacity="0.00"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>
  </defs>

  <!-- clean editorial background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- left-side nature icon -->
  <path d="M100 199 C118 188, 132 188, 148 199 C132 199, 116 202, 100 199 Z"
        fill="none" stroke="#1E8F16" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M122 203 C132 191, 142 184, 154 181 M132 202 C126 194, 119 191, 111 191 M144 195 C146 185, 153 179, 163 177"
        fill="none" stroke="#1E8F16" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M121 169 C126 162, 134 163, 137 170 C140 159, 153 157, 158 166 C164 162, 172 166, 172 174 C172 181, 165 184, 158 181
           M142 180 L142 188 M153 184 L153 193"
        fill="none" stroke="#1E8F16" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- typography block -->
  <text x="97" y="292" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#333333">
    大力发展
  </text>
  <text x="97" y="362" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#1E8F16">
    特色乡村文化旅游
  </text>
  <text x="98" y="403" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#1E8F16">
    Featured rural cultural tourism
  </text>
  <text x="98" y="451" width="395" font-family="Segoe UI, Microsoft YaHei" font-size="16.5" font-weight="400" fill="#3F3F3F">
    <tspan x="98" dy="0">Pellentesque habitant morbi tristique senectus et</tspan>
    <tspan x="98" dy="20">netus et malesuada fames ac turpis egestas.</tspan>
    <tspan x="98" dy="20">Proin pharetra nonummy pede. Mauris et orci.</tspan>
  </text>
  <rect x="98" y="516" width="81" height="13" rx="6.5" fill="#1E8F16"/>

  <!-- base photo block: 6 columns x 6 rows; cell size 133 x 120, x starts at 482 -->
  <image x="482" y="0" width="798" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1400&amp;q=80"/>
  <rect x="482" y="0" width="798" height="720" fill="url(#softPhotoWash)" opacity="0.75"/>

  <!-- fully removed cells: cover photo with white, creating stepped mosaic edges and internal holes -->
  <rect x="482" y="0" width="133" height="120" fill="#FFFFFF"/>
  <rect x="1147" y="0" width="133" height="120" fill="#FFFFFF"/>
  <rect x="482" y="240" width="133" height="120" fill="#FFFFFF"/>
  <rect x="615" y="240" width="133" height="120" fill="#FFFFFF"/>
  <rect x="482" y="480" width="133" height="120" fill="#FFFFFF"/>
  <rect x="615" y="600" width="133" height="120" fill="#FFFFFF"/>
  <rect x="748" y="600" width="133" height="120" fill="#FFFFFF"/>
  <rect x="881" y="600" width="133" height="120" fill="#FFFFFF"/>
  <rect x="482" y="600" width="133" height="120" fill="#FFFFFF"/>
  <rect x="1147" y="480" width="133" height="120" fill="#FFFFFF"/>
  <rect x="615" y="120" width="133" height="120" fill="#FFFFFF" opacity="0.0"/>
  <rect x="1014" y="0" width="133" height="120" fill="#FFFFFF" opacity="0.0"/>

  <!-- washed cells: visible image remains, but becomes airy and pale -->
  <rect x="615" y="120" width="133" height="120" fill="#FFFFFF" opacity="0.47"/>
  <rect x="1014" y="120" width="133" height="120" fill="#FFFFFF" opacity="0.55"/>
  <rect x="881" y="360" width="133" height="120" fill="#FFFFFF" opacity="0.42"/>
  <rect x="1147" y="360" width="133" height="120" fill="#FFFFFF" opacity="0.52"/>
  <rect x="615" y="480" width="133" height="120" fill="#FFFFFF" opacity="0.60"/>
  <rect x="482" y="120" width="133" height="120" fill="#FFFFFF" opacity="0.08"/>

  <!-- crisp white grid lines -->
  <line x1="615" y1="0" x2="615" y2="720" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="748" y1="0" x2="748" y2="720" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="881" y1="0" x2="881" y2="720" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="1014" y1="0" x2="1014" y2="720" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="1147" y1="0" x2="1147" y2="720" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="482" y1="120" x2="1280" y2="120" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="482" y1="240" x2="1280" y2="240" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="482" y1="360" x2="1280" y2="360" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="482" y1="480" x2="1280" y2="480" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="482" y1="600" x2="1280" y2="600" stroke="#FFFFFF" stroke-width="1.4"/>
  <line x1="482" y1="720" x2="1280" y2="720" stroke="#FFFFFF" stroke-width="1.4"/>
</svg>
```

## Avoid in this skill
- ❌ Using SVG `<mask>` to cut out cells; instead, place opaque white rectangles above the image to simulate removed tiles.
- ❌ Building the mosaic from 36 individually cropped images unless each crop must be manually editable; one full image plus cell overlays is cleaner and more robust.
- ❌ Applying `clip-path` to rectangles for the missing cells; clipping non-image shapes will be ignored by the translator.
- ❌ Overly thick grid strokes; the premium look depends on thin, crisp pane dividers.
- ❌ Randomizing cell removal without regard to composition; keep the left edge stepped and the internal wash cells balanced.

## Composition notes
- Keep the left 38–42% of the slide mostly white, with the text block vertically centered and left aligned.
- Let the photo occupy the full slide height on the right; the missing cells should create an irregular stepped boundary where image meets whitespace.
- Use the photo’s dominant hue as the subtitle/accent color so the typography and image feel connected.
- Reserve the strongest image detail near the center-right; washed cells should soften the grid without hiding the hero scenery completely.