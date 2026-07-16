# SVG Recipe — Bespoke Color Palette Theming

## Visual mechanism
Turn an abstract PowerPoint theme palette into a premium “brand system” slide: a central strip of named color tokens feeds a polished chart preview, proving that the custom accents drive charts, shapes, and UI elements consistently. The effect relies on disciplined color reuse, generous spacing, soft shadows, and one vivid data-visualization specimen.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 2× `<linearGradient>` for the background wash and primary hero card.
- 1× `<radialGradient>` for soft atmospheric color bloom.
- 1× `<filter id="softShadow">` applied to cards and chart containers.
- 1× `<filter id="glow">` applied to accent bloom shapes.
- 3× `<path>` for organic decorative blobs and a curved palette-flow connector.
- 2× large `<rect>` panels for the palette board and chart preview card.
- 12× small `<rect>` swatches for Text/Background and Accent color slots.
- 6× `<rect>` bars for a theme-colored bar chart.
- 4× `<path>` donut segments showing the same accent palette in a chart context.
- 1× `<line>` for the chart axis.
- Multiple `<text>` elements with explicit `width` attributes for labels, titles, captions, and HEX values.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7FAFC"/>
      <stop offset="0.55" stop-color="#EEF3F8"/>
      <stop offset="1" stop-color="#E8EEF6"/>
    </linearGradient>
    <linearGradient id="heroGrad" x1="72" y1="84" x2="494" y2="346" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#023047"/>
      <stop offset="1" stop-color="#219EBC"/>
    </linearGradient>
    <radialGradient id="orangeBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFB703" stop-opacity="0.75"/>
      <stop offset="1" stop-color="#FFB703" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M1005 20 C1125 -16 1256 54 1278 170 C1302 302 1162 332 1086 274 C1014 220 915 236 906 150 C898 80 942 40 1005 20 Z" fill="#BECAE6" opacity="0.45" filter="url(#glow)"/>
  <path d="M-44 520 C60 442 176 492 202 598 C228 704 102 748 -18 720 Z" fill="url(#orangeBloom)" opacity="0.75" filter="url(#glow)"/>
  <path d="M518 136 C590 84 684 92 734 154 C798 234 718 309 626 286 C544 266 466 270 454 212 C446 174 480 156 518 136 Z" fill="#219EBC" opacity="0.10"/>

  <rect x="72" y="76" width="422" height="568" rx="34" fill="url(#heroGrad)" filter="url(#softShadow)"/>
  <text x="112" y="136" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#BECAE6">CUSTOM THEME PALETTE</text>
  <text x="112" y="196" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#FFFFFF">Bespoke colors that travel everywhere</text>
  <text x="112" y="312" width="322" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E6F1F5">Define the six accents once, then let PowerPoint charts, shapes, and color pickers inherit the branded system.</text>

  <rect x="112" y="396" width="318" height="78" rx="18" fill="#FFFFFF" opacity="0.13"/>
  <circle cx="148" cy="435" r="13" fill="#FFB703"/>
  <circle cx="180" cy="435" r="13" fill="#FB8500"/>
  <circle cx="212" cy="435" r="13" fill="#4CAF50"/>
  <text x="246" y="428" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Theme-aware objects</text>
  <text x="246" y="450" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7EEF4">charts • icons • cards</text>

  <rect x="112" y="514" width="318" height="76" rx="18" fill="#023047" opacity="0.48"/>
  <text x="138" y="548" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Palette name</text>
  <text x="138" y="574" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFB703">Coolors Custom Palette</text>

  <rect x="536" y="76" width="308" height="568" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="572" y="128" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#023047">Theme slots</text>
  <text x="572" y="158" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#425466">12 native PowerPoint color roles</text>

  <rect x="572" y="196" width="92" height="62" rx="14" fill="#0B1220"/>
  <text x="680" y="218" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B1220">Dark 1</text>
  <text x="680" y="240" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#607080">#0B1220</text>

  <rect x="572" y="274" width="92" height="62" rx="14" fill="#FFFFFF" stroke="#D8E1EA"/>
  <text x="680" y="296" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B1220">Light 1</text>
  <text x="680" y="318" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#607080">#FFFFFF</text>

  <rect x="572" y="352" width="92" height="62" rx="14" fill="#425466"/>
  <text x="680" y="374" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B1220">Dark 2</text>
  <text x="680" y="396" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#607080">#425466</text>

  <rect x="572" y="430" width="92" height="62" rx="14" fill="#EEF3F8" stroke="#D8E1EA"/>
  <text x="680" y="452" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0B1220">Light 2</text>
  <text x="680" y="474" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#607080">#EEF3F8</text>

  <rect x="572" y="520" width="38" height="38" rx="10" fill="#BECAE6"/>
  <rect x="620" y="520" width="38" height="38" rx="10" fill="#219EBC"/>
  <rect x="668" y="520" width="38" height="38" rx="10" fill="#023047"/>
  <rect x="716" y="520" width="38" height="38" rx="10" fill="#FFB703"/>
  <rect x="764" y="520" width="38" height="38" rx="10" fill="#FB8500"/>
  <rect x="572" y="572" width="38" height="38" rx="10" fill="#4CAF50"/>
  <text x="620" y="596" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#023047">Accent 1–6</text>

  <path d="M846 360 C886 332 888 292 930 282" fill="none" stroke="#219EBC" stroke-width="5" stroke-linecap="round" opacity="0.55" stroke-dasharray="10 12"/>
  <rect x="888" y="76" width="320" height="568" rx="30" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="928" y="128" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#023047">Chart preview</text>
  <text x="928" y="158" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#425466">New charts pull from the accents automatically</text>

  <line x1="938" y1="434" x2="1158" y2="434" stroke="#C7D3DF" stroke-width="2"/>
  <rect x="948" y="318" width="24" height="116" rx="8" fill="#BECAE6"/>
  <rect x="988" y="270" width="24" height="164" rx="8" fill="#219EBC"/>
  <rect x="1028" y="232" width="24" height="202" rx="8" fill="#023047"/>
  <rect x="1068" y="292" width="24" height="142" rx="8" fill="#FFB703"/>
  <rect x="1108" y="248" width="24" height="186" rx="8" fill="#FB8500"/>
  <rect x="1148" y="340" width="24" height="94" rx="8" fill="#4CAF50"/>

  <path d="M1048 500 L1048 458 A42 42 0 0 1 1085 520 Z" fill="#219EBC"/>
  <path d="M1048 500 L1085 520 A42 42 0 0 1 1020 536 Z" fill="#FFB703"/>
  <path d="M1048 500 L1020 536 A42 42 0 0 1 1014 468 Z" fill="#FB8500"/>
  <path d="M1048 500 L1014 468 A42 42 0 0 1 1048 458 Z" fill="#023047"/>
  <circle cx="1048" cy="500" r="20" fill="#FFFFFF"/>

  <text x="936" y="488" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#425466">Accent-driven</text>
  <text x="936" y="510" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#607080">data palette</text>
  <text x="1104" y="504" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#023047">6</text>
  <text x="1104" y="530" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#607080">theme accents</text>

  <rect x="928" y="574" width="232" height="36" rx="18" fill="#EEF3F8"/>
  <circle cx="950" cy="592" r="7" fill="#4CAF50"/>
  <text x="968" y="598" width="164" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#023047">Reusable brand foundation</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<use>` to repeat swatches or chart bars; duplicate the actual `<rect>` elements so PPT-Master creates editable shapes.
- ❌ Relying on CSS variables or external stylesheets for theme colors; place final HEX values directly in SVG fills and strokes.
- ❌ Using `<pattern>` fills to imply a palette grid; patterns are not reliably translated.
- ❌ Applying `clip-path` to shape elements for decorative cards; clip paths should only be used on `<image>` elements.
- ❌ Making a “palette” slide from plain flat swatches only; show at least one downstream application such as a chart, card system, or UI preview.

## Composition notes
- Keep the left third for the strategic message, the center for the 12 theme slots, and the right third for a concrete chart/data preview.
- Use neutral background roles sparingly; let Accent 2 teal, Accent 4 yellow, and Accent 5 orange provide rhythm and visual energy.
- Give every swatch a label and HEX value so the slide reads like a usable brand specification, not just decoration.
- Use soft shadows and subtle atmospheric blobs to make the palette feel like a premium design system rather than a color-picker screenshot.