# SVG Recipe — Retro Parallax Typography

## Visual mechanism
Stack the same large script word three times with small diagonal offsets: a deep brown base shadow, a striped middle shadow, and a top black fill with a thick white outline. The result reads as vintage screen-printed 3D lettering without converting text to paths.

## SVG primitives needed
- 1× `<rect>` for the warm cream slide background
- 2× `<rect>` for subtle retro underline/accent bars
- 4× `<circle>` for light decorative print-registration dots
- 1× `<linearGradient>` for the paper-like background tint
- 1× `<linearGradient>` for the horizontal stripe fill on the middle text layer
- 5× `<text>` for the typography stack: brown shadow, striped shadow, main outlined word, highlight/cutout overlay, and small label text

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="paperWarmth" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FBF7F1"/>
      <stop offset="100%" stop-color="#F4E8DD"/>
    </linearGradient>

    <linearGradient id="stripeShadow" x1="0" y1="0" x2="0" y2="14" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
      <stop offset="0%" stop-color="#1A1A1A"/>
      <stop offset="38%" stop-color="#1A1A1A"/>
      <stop offset="39%" stop-color="#F9F4F0"/>
      <stop offset="70%" stop-color="#F9F4F0"/>
      <stop offset="71%" stop-color="#1A1A1A"/>
      <stop offset="100%" stop-color="#1A1A1A"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWarmth)"/>

  <circle cx="114" cy="148" r="10" fill="#8E5D4B" opacity="0.18"/>
  <circle cx="148" cy="148" r="10" fill="#1A1A1A" opacity="0.12"/>
  <circle cx="1110" cy="562" r="13" fill="#8E5D4B" opacity="0.16"/>
  <circle cx="1152" cy="562" r="13" fill="#1A1A1A" opacity="0.10"/>

  <rect x="104" y="475" width="355" height="16" rx="0" ry="0" fill="#8E5D4B" opacity="0.18"/>
  <rect x="820" y="220" width="250" height="12" rx="0" ry="0" fill="#1A1A1A" opacity="0.08"/>

  <g id="retro-parallax-type">
    <text
      x="164" y="388" width="980"
      font-family="Brush Script MT, Segoe Script, Segoe UI, Microsoft YaHei"
      font-size="164"
      font-style="italic"
      font-weight="700"
      letter-spacing="-4"
      fill="#8E5D4B">Parallax</text>

    <text
      x="146" y="370" width="980"
      font-family="Brush Script MT, Segoe Script, Segoe UI, Microsoft YaHei"
      font-size="164"
      font-style="italic"
      font-weight="700"
      letter-spacing="-4"
      fill="url(#stripeShadow)">Parallax</text>

    <text
      x="128" y="352" width="980"
      font-family="Brush Script MT, Segoe Script, Segoe UI, Microsoft YaHei"
      font-size="164"
      font-style="italic"
      font-weight="700"
      letter-spacing="-4"
      fill="#1A1A1A"
      stroke="#FFFFFF"
      stroke-width="15"
      stroke-linejoin="round"
      paint-order="stroke fill">Parallax</text>

    <text
      x="120" y="343" width="980"
      font-family="Brush Script MT, Segoe Script, Segoe UI, Microsoft YaHei"
      font-size="164"
      font-style="italic"
      font-weight="700"
      letter-spacing="-4"
      fill="none"
      stroke="#F9F4F0"
      stroke-width="4"
      stroke-linejoin="round"
      opacity="0.9">Parallax</text>
  </g>

  <text
    x="438" y="548" width="405"
    font-family="Segoe UI, Microsoft YaHei"
    font-size="22"
    font-weight="700"
    letter-spacing="5"
    text-anchor="middle"
    fill="#8E5D4B">SCREEN PRINT EDITION</text>
</svg>
```

## Avoid in this skill
- ❌ Converting the word into `<path>` glyph outlines; keep it as editable `<text>`.
- ❌ Using `<filter>` drop shadows on the text stack, because the text subtree may rasterize in PPT conversion.
- ❌ Using `<mask>`, `<clipPath>`, or `<pattern>` to create stripes; use a simple repeated `<linearGradient>` fill instead.
- ❌ Applying skew/rotate transforms for the slant; use an italic/script font and offset layers instead.
- ❌ Placing the marker/stripe/outline logic on a parent group and expecting inheritance to translate perfectly; put critical fill, stroke, and width properties directly on each text layer.

## Composition notes
- Keep the main word centered horizontally and occupying roughly 65–75% of the slide width; this effect needs scale to read well.
- Use small diagonal offsets, usually 16–36 px, so the parallax depth is visible but does not detach from the main word.
- The color rhythm should be simple: cream background, brown rear shadow, black/cream striped middle, black top fill, white outline.
- Leave generous negative space above and below the word; the typography stack is the hero, while accents should stay faint and secondary.