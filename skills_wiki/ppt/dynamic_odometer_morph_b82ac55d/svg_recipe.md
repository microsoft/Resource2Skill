# SVG Recipe — Odometer Number Reveal

## Visual mechanism
A tall vertical strip of digits sits behind a narrow “viewing window”; between two PowerPoint slides, Morph interpolates each strip’s Y-position so the digits roll like a mechanical odometer. The mask is built from ordinary overlay rectangles around the window, keeping everything editable while hiding off-window numbers.

## SVG primitives needed
- 1× full-slide `<rect>` for the warm executive background gradient
- 2× decorative `<path>` blobs for subtle premium keynote atmosphere
- 1× dark `<rect>` behind the digit window for the odometer well
- 40× `<text>` digits arranged as four vertical number strips, one strip per digit column
- 4× matte `<rect>` overlays around the window to hide the off-window portions of the digit strips
- 2× rounded `<rect>` frames for the gold odometer bezel and inner glass highlight
- 2× `<text>` labels for headline and metric caption
- 3× static `<text>` symbols for currency, comma separator, and unit suffix
- 4× thin `<line>` separators for mechanical reel divisions
- 2× `<filter>` definitions: one soft shadow for the window well, one gold glow for the frame
- 3× `<linearGradient>` definitions for background, glass, and gold accent styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F38B72"/>
      <stop offset="0.42" stop-color="#C9502E"/>
      <stop offset="1" stop-color="#7C241E"/>
    </linearGradient>
    <linearGradient id="gold" x1="315" y1="260" x2="965" y2="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF1B8"/>
      <stop offset="0.45" stop-color="#E6B84D"/>
      <stop offset="1" stop-color="#9E6A18"/>
    </linearGradient>
    <linearGradient id="glass" x1="315" y1="276" x2="965" y2="444" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="0.52" stop-color="#FFFFFF" stop-opacity="0.03"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.24"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="goldGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M-60 112 C180 42 330 98 520 38 C690 -16 890 8 1048 90 C1180 158 1268 134 1348 80 L1348 -40 L-60 -40 Z" fill="#FFD4A8" opacity="0.12"/>
  <path d="M-80 660 C160 590 280 722 500 652 C720 580 836 632 1010 674 C1138 706 1240 672 1360 608 L1360 760 L-80 760 Z" fill="#5A1216" opacity="0.22"/>

  <rect x="315" y="276" width="650" height="168" rx="28" fill="#15151F" opacity="0.92" filter="url(#softShadow)"/>

  <text x="444" y="-754" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">0</text>
  <text x="444" y="-564" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">1</text>
  <text x="444" y="-374" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">2</text>
  <text x="444" y="-184" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">3</text>
  <text x="444" y="6" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">4</text>
  <text x="444" y="196" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">5</text>
  <text x="444" y="386" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">6</text>
  <text x="444" y="576" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">7</text>
  <text x="444" y="766" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">8</text>
  <text x="444" y="956" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">9</text>

  <text x="572" y="-944" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">0</text>
  <text x="572" y="-754" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">1</text>
  <text x="572" y="-564" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">2</text>
  <text x="572" y="-374" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">3</text>
  <text x="572" y="-184" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">4</text>
  <text x="572" y="6" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">5</text>
  <text x="572" y="196" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">6</text>
  <text x="572" y="386" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">7</text>
  <text x="572" y="576" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">8</text>
  <text x="572" y="766" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">9</text>

  <text x="702" y="-1134" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">0</text>
  <text x="702" y="-944" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">1</text>
  <text x="702" y="-754" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">2</text>
  <text x="702" y="-564" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">3</text>
  <text x="702" y="-374" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">4</text>
  <text x="702" y="-184" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">5</text>
  <text x="702" y="6" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">6</text>
  <text x="702" y="196" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">7</text>
  <text x="702" y="386" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">8</text>
  <text x="702" y="576" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">9</text>

  <text x="832" y="6" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">0</text>
  <text x="832" y="196" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">1</text>
  <text x="832" y="386" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">2</text>
  <text x="832" y="576" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">3</text>
  <text x="832" y="766" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">4</text>
  <text x="832" y="956" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">5</text>
  <text x="832" y="1146" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">6</text>
  <text x="832" y="1336" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">7</text>
  <text x="832" y="1526" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">8</text>
  <text x="832" y="1716" width="112" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="800" fill="#FFF2C7">9</text>

  <rect x="0" y="0" width="1280" height="276" fill="url(#bg)"/>
  <rect x="0" y="444" width="1280" height="276" fill="url(#bg)"/>
  <rect x="0" y="276" width="315" height="168" fill="url(#bg)"/>
  <rect x="965" y="276" width="315" height="168" fill="url(#bg)"/>

  <rect x="315" y="276" width="650" height="168" rx="28" fill="none" stroke="url(#gold)" stroke-width="7" filter="url(#goldGlow)"/>
  <rect x="330" y="291" width="620" height="138" rx="20" fill="url(#glass)" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="514" y1="296" x2="514" y2="424" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2"/>
  <line x1="638" y1="296" x2="638" y2="424" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2"/>
  <line x1="768" y1="296" x2="768" y2="424" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2"/>
  <line x1="890" y1="296" x2="890" y2="424" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2"/>

  <text x="640" y="168" width="900" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="700" fill="#FFF2D2" letter-spacing="10">让业绩数据更耀眼</text>
  <text x="640" y="228" width="720" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#FFE6A3" letter-spacing="4">FY2026 REVENUE REVEAL</text>
  <text x="358" y="386" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="700" fill="#FFE9B0">$</text>
  <text x="505" y="404" width="36" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#FFE9B0">,</text>
  <text x="915" y="386" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="700" fill="#FFE9B0">M</text>
  <text x="640" y="548" width="740" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="500" fill="#FFF1C8">Duplicate the slide, move each digit strip vertically, then apply PowerPoint Morph.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the rolling; the PowerPoint-native version should use two slides plus Morph.
- ❌ Do not use `<mask>` to cut a transparent window; build the matte from four ordinary overlay rectangles around the window.
- ❌ Do not apply `clip-path` to text groups; PPT-Master only preserves clipping reliably for images.
- ❌ Do not place all digits in one giant paragraph if you need precise column-by-column Morph control; use separate editable text objects or matched groups per digit column.
- ❌ Do not rely on filters on `<line>` separators; line filters are dropped, so keep glow/shadow on rects, paths, or text.

## Composition notes
- Keep the odometer window dead center and allocate roughly 55–60% of slide width to it; the reveal should feel ceremonial, not like a small dashboard widget.
- For Morph, create slide 1 with each strip positioned so `0` is centered; create slide 2 with the same strips shifted vertically so the target digits are centered.
- Use the overlay matte rectangles above the strips and below the headline; then redraw labels, frame, separators, and static punctuation on top.
- A warm dark background plus cream/gold numerals creates a gala-style metric reveal; navy/gold works equally well for finance and executive-review decks.