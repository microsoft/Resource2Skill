# SVG Recipe — Cinematic Picture-in-Picture Reveal

## Visual mechanism
Duplicate one epic full-bleed image into two layers: a darkened grayscale background for atmosphere, then a centered full-color crop revealed through a tall rectangular “cinema window.” A thin premium frame and staggered oversized title typography lock the viewer’s eye onto the focal strip.

## SVG primitives needed
- 2× `<image>` for the same scene: one preprocessed dark grayscale full-bleed background, one full-color duplicate clipped to the central window
- 1× `<clipPath>` with `<rect>` for the picture-in-picture reveal crop
- 5× `<rect>` for dark overlays, vignette wash, central backing shadow, frame, and subtle letterbox bars
- 1× `<filter id="softShadow">` for the central window depth
- 1× `<filter id="titleGlow">` for soft title glow
- 2× `<linearGradient>` for cinematic top/bottom darkening and frame highlight
- 1× `<radialGradient>` for center-to-edge vignette
- 4× large `<text>` elements for staggered Chinese title characters
- 2× smaller `<text>` elements for subtitle, eyebrow, or event metadata
- 4× `<line>` elements for fine editorial registration marks around the frame

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="centerReveal">
      <rect x="384" y="96" width="512" height="528" rx="0"/>
    </clipPath>

    <linearGradient id="letterboxGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.78"/>
      <stop offset="52%" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="goldFrame" x1="384" y1="96" x2="896" y2="624">
      <stop offset="0%" stop-color="#fff6c8"/>
      <stop offset="42%" stop-color="#cda44b"/>
      <stop offset="100%" stop-color="#fff0a8"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.68"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <!-- Full-bleed desaturated cinematic background: use a preprocessed dark grayscale version of the same source photo -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/epic-mountain-cityscape-dark-grayscale-16x9.jpg"/>

  <!-- Global mood grading -->
  <rect x="0" y="0" width="1280" height="720" fill="#07101a" opacity="0.34"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#letterboxGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <!-- Hidden depth plate behind the reveal window -->
  <rect x="372" y="84" width="536" height="552" fill="#000000" opacity="0.42" filter="url(#softShadow)"/>

  <!-- Full-color duplicate, clipped to exact center window so the scene aligns with the background -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#centerReveal)"
         href="https://images.example.com/epic-mountain-cityscape-full-color-16x9.jpg"/>

  <!-- Premium frame around the reveal -->
  <rect x="384" y="96" width="512" height="528" fill="none" stroke="url(#goldFrame)" stroke-width="2.5"/>
  <rect x="397" y="109" width="486" height="502" fill="none" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>

  <!-- Editorial registration marks; use lines, not marker paths -->
  <line x1="344" y1="96" x2="374" y2="96" stroke="#e9d18a" stroke-width="2"/>
  <line x1="906" y1="96" x2="936" y2="96" stroke="#e9d18a" stroke-width="2"/>
  <line x1="344" y1="624" x2="374" y2="624" stroke="#e9d18a" stroke-width="2"/>
  <line x1="906" y1="624" x2="936" y2="624" stroke="#e9d18a" stroke-width="2"/>

  <!-- Small cinematic eyebrow -->
  <text x="96" y="118" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        letter-spacing="4" fill="#d8c27a" opacity="0.95">ANNUAL STRATEGIC SUMMIT</text>
  <text x="96" y="146" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        letter-spacing="1.5" fill="#ffffff" opacity="0.62">2024 WORK REPORT · INDUSTRY OUTLOOK · GROWTH AGENDA</text>

  <!-- Soft glow duplicate behind title -->
  <text x="370" y="405" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#000000" opacity="0.45" filter="url(#titleGlow)">乘</text>
  <text x="506" y="458" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#000000" opacity="0.45" filter="url(#titleGlow)">势</text>
  <text x="642" y="458" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#000000" opacity="0.45" filter="url(#titleGlow)">而</text>
  <text x="778" y="405" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#000000" opacity="0.45" filter="url(#titleGlow)">上</text>

  <!-- Staggered calligraphy-style title, high-low-low-high -->
  <text x="362" y="398" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#fff7dd" stroke="#111111" stroke-width="3">乘</text>
  <text x="498" y="451" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#fff7dd" stroke="#111111" stroke-width="3">势</text>
  <text x="634" y="451" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#fff7dd" stroke="#111111" stroke-width="3">而</text>
  <text x="770" y="398" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="116"
        font-weight="700" fill="#fff7dd" stroke="#111111" stroke-width="3">上</text>

  <!-- Bottom subtitle block -->
  <text x="410" y="555" width="460" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="20" font-weight="600" letter-spacing="3" fill="#e9d18a">2024 年度工作汇报与战略部署</text>
  <text x="410" y="586" width="460" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="13" letter-spacing="2" fill="#ffffff" opacity="0.72">BUILDING MOMENTUM FOR THE NEXT GROWTH CYCLE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG `feColorMatrix` to grayscale the background; use a preprocessed grayscale image asset so PowerPoint keeps the look reliably.
- ❌ Do not use `<mask>` for the center reveal; use `clipPath` applied directly to the `<image>`.
- ❌ Do not clip text or rectangles; PPT-Master only preserves clipping reliably for images.
- ❌ Do not use `<textPath>` for cinematic title styling; create separate editable text boxes with manual staggered positions.
- ❌ Do not use `marker-end` on paths for registration marks; use simple `<line>` elements.

## Composition notes
- Keep the color window dead-center, about 40% of slide width and 70–75% of slide height; this creates the “picture-in-picture” reveal without feeling like a small thumbnail.
- Use grayscale/dark background to suppress image noise, then let the full-color crop carry all saturation and focal energy.
- Place the main title across the lower-middle of the window, overlapping slightly beyond the frame for a premium editorial feel.
- Maintain generous dark negative space at the left/right edges for eyebrow text, metadata, or logo placement.