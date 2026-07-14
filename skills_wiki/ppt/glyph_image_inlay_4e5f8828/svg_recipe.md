# SVG Recipe — Glyph Image Inlay

## Visual mechanism
Large, heavy individual glyphs act as visual “windows,” with each letter given its own image-like color treatment so the word becomes the main graphic object. In the safe SVG subset, use per-letter gradients to simulate photographic inlays; true bitmap-in-text masking should be avoided because it does not translate cleanly to editable PowerPoint shapes.

## SVG primitives needed
- 1× `<rect>` for the light neutral slide background
- 20–30× `<line>` for subtle diagonal background texture
- 5× `<linearGradient>` for distinct image-like fills, one per glyph
- 5× large `<text>` elements for the individual inlaid letters
- 5× small `<text>` elements for optional semantic labels under each glyph
- 1× subtitle `<text>` element for context below the hero word
- Optional 1× small eyebrow `<text>` element above the word for presentation context

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="brazilFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B7A3B"/>
      <stop offset="38%" stop-color="#F4D03F"/>
      <stop offset="68%" stop-color="#1F6FEB"/>
      <stop offset="100%" stop-color="#163B1F"/>
    </linearGradient>
    <linearGradient id="russiaFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4F7FA"/>
      <stop offset="34%" stop-color="#6787B7"/>
      <stop offset="66%" stop-color="#B02A37"/>
      <stop offset="100%" stop-color="#4E1F2B"/>
    </linearGradient>
    <linearGradient id="indiaFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F28C28"/>
      <stop offset="38%" stop-color="#FFF1C7"/>
      <stop offset="64%" stop-color="#2F8F4E"/>
      <stop offset="100%" stop-color="#165B36"/>
    </linearGradient>
    <linearGradient id="chinaFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D92323"/>
      <stop offset="42%" stop-color="#F7C948"/>
      <stop offset="72%" stop-color="#9B1C1C"/>
      <stop offset="100%" stop-color="#3D0B0B"/>
    </linearGradient>
    <linearGradient id="southAfricaFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1C7C54"/>
      <stop offset="30%" stop-color="#F5D547"/>
      <stop offset="58%" stop-color="#0A4C8A"/>
      <stop offset="82%" stop-color="#E76F51"/>
      <stop offset="100%" stop-color="#1C1C1C"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F5F5"/>

  <line x1="-640" y1="0" x2="80" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-580" y1="0" x2="140" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-520" y1="0" x2="200" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-460" y1="0" x2="260" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-400" y1="0" x2="320" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-340" y1="0" x2="380" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-280" y1="0" x2="440" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-220" y1="0" x2="500" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-160" y1="0" x2="560" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-100" y1="0" x2="620" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="-40" y1="0" x2="680" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="20" y1="0" x2="740" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="80" y1="0" x2="800" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="140" y1="0" x2="860" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="200" y1="0" x2="920" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="260" y1="0" x2="980" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="320" y1="0" x2="1040" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="380" y1="0" x2="1100" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="440" y1="0" x2="1160" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="500" y1="0" x2="1220" y2="720" stroke="#DCDCDC" stroke-width="2"/>
  <line x1="560" y1="0" x2="1280" y2="720" stroke="#DCDCDC" stroke-width="2"/>

  <text x="640" y="105" width="700" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="600"
        fill="#6A6A6A">MULTI-COUNTRY GROWTH PLATFORM</text>

  <text x="285" y="415" width="175" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="265" font-weight="900"
        fill="url(#brazilFill)" stroke="#FFFFFF" stroke-width="4">B</text>
  <text x="462" y="415" width="175" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="265" font-weight="900"
        fill="url(#russiaFill)" stroke="#FFFFFF" stroke-width="4">R</text>
  <text x="640" y="415" width="175" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="265" font-weight="900"
        fill="url(#indiaFill)" stroke="#FFFFFF" stroke-width="4">I</text>
  <text x="818" y="415" width="175" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="265" font-weight="900"
        fill="url(#chinaFill)" stroke="#FFFFFF" stroke-width="4">C</text>
  <text x="995" y="415" width="175" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="265" font-weight="900"
        fill="url(#southAfricaFill)" stroke="#FFFFFF" stroke-width="4">S</text>

  <text x="285" y="475" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#666666">Brazil</text>
  <text x="462" y="475" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#666666">Russia</text>
  <text x="640" y="475" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#666666">India</text>
  <text x="818" y="475" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#666666">China</text>
  <text x="995" y="475" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#666666">South Africa</text>

  <text x="640" y="570" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="400"
        fill="#595959">2023 金砖国家峰会 · Shared markets, distinct identities</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<image>` plus `<mask>` or `<clipPath>` to create real bitmap-filled letters; those are outside the safe subset and will not remain editable in PowerPoint.
- ❌ Do not convert letters to `<path>` outlines; the result may look accurate but becomes non-editable vector art rather than PowerPoint text.
- ❌ Do not put the whole word in one text frame if each glyph needs a different inlay; create one text element per character.
- ❌ Do not use thin fonts; the inlay needs very heavy letterforms to provide enough visual surface.
- ❌ Do not add filters to the glyph text; PPT-Master may rasterize filtered text subtrees.

## Composition notes
- Keep the glyph word as the hero object, centered and occupying roughly 70–80% of slide width.
- Use generous negative space above and below the word so the dense letter fills do not compete with other content.
- Give each letter a distinct fill palette to imply separate images or themes, but keep saturation balanced across the word.
- Use a pale textured background and dark gray subtitle so the focus stays on the inlaid typography.