# SVG Recipe — Bold Section Divider

## Visual mechanism
A low-density section break built around one oversized, high-contrast headline, anchored by diagonal color slabs and playful geometric accents. The slide feels bold because the headline dominates the canvas while decorative shapes create motion without competing for attention.

## SVG primitives needed
- 1× `<rect>` for the full-bleed dark background
- 3× `<linearGradient>` for the background wash, accent slabs, and highlight fills
- 2× `<filter>` definitions for soft shadow and colored glow
- 3× large `<path>` shapes for diagonal section-divider bands and organic corner decoration
- 6× `<circle>` / `<ellipse>` for playful dot accents and orbital decorations
- 4× `<rect>` for small rotated color chips and underline bars
- 2× `<line>` for thin divider strokes
- 3× `<text>` elements for section label, oversized headline, and small kicker text
- Nested `<tspan>` inside the headline for inline color emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#08111F"/>
      <stop offset="55%" stop-color="#10172E"/>
      <stop offset="100%" stop-color="#1B1234"/>
    </linearGradient>

    <linearGradient id="hotBand" x1="210" y1="0" x2="1080" y2="720">
      <stop offset="0%" stop-color="#FF4D7D"/>
      <stop offset="52%" stop-color="#FFB000"/>
      <stop offset="100%" stop-color="#34D6FF"/>
    </linearGradient>

    <linearGradient id="coolBand" x1="0" y1="720" x2="1280" y2="0">
      <stop offset="0%" stop-color="#5B7CFF"/>
      <stop offset="48%" stop-color="#7D3CFF"/>
      <stop offset="100%" stop-color="#00E5B0"/>
    </linearGradient>

    <linearGradient id="titleFill" x1="170" y1="250" x2="980" y2="440">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="72%" stop-color="#F5F7FF"/>
      <stop offset="100%" stop-color="#CDE4FF"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80 578 C170 505 330 485 520 530 C740 582 902 558 1110 455 L1360 335 L1360 720 L-80 720 Z"
        fill="url(#coolBand)" opacity="0.34"/>
  <path d="M780 -70 L1360 -70 L1360 178 C1210 218 1074 283 946 373 C858 435 755 470 650 472 Z"
        fill="url(#hotBand)" opacity="0.9" filter="url(#softShadow)"/>
  <path d="M-70 110 C85 36 210 30 317 86 C430 146 472 255 596 281 C704 304 816 260 923 203 L976 278 C777 421 565 438 386 360 C232 293 116 280 -70 358 Z"
        fill="#FFFFFF" opacity="0.055"/>

  <circle cx="1088" cy="132" r="78" fill="#FFB000" opacity="0.95" filter="url(#accentGlow)"/>
  <circle cx="1088" cy="132" r="48" fill="#08111F" opacity="0.28"/>
  <ellipse cx="1128" cy="188" rx="122" ry="30" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.55" transform="rotate(-23 1128 188)"/>
  <circle cx="1192" cy="276" r="12" fill="#34D6FF"/>
  <circle cx="1018" cy="304" r="8" fill="#FFFFFF" opacity="0.85"/>
  <circle cx="114" cy="592" r="44" fill="#FF4D7D" opacity="0.9"/>
  <ellipse cx="170" cy="612" rx="96" ry="22" fill="none" stroke="#FFB000" stroke-width="4" opacity="0.75" transform="rotate(18 170 612)"/>

  <rect x="92" y="105" width="112" height="16" rx="8" fill="#34D6FF" transform="rotate(-12 92 105)"/>
  <rect x="1046" y="552" width="148" height="18" rx="9" fill="#FF4D7D" transform="rotate(-18 1046 552)"/>
  <rect x="978" y="606" width="78" height="12" rx="6" fill="#FFB000" transform="rotate(12 978 606)"/>
  <rect x="172" y="456" width="365" height="11" rx="5.5" fill="url(#hotBand)"/>

  <line x1="171" y1="205" x2="365" y2="205" stroke="#FFFFFF" stroke-width="2" opacity="0.28" stroke-dasharray="10 12"/>
  <line x1="854" y1="485" x2="1094" y2="485" stroke="#FFFFFF" stroke-width="2" opacity="0.22" stroke-dasharray="2 14"/>

  <text x="172" y="192" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="5" fill="#8BE9FF" opacity="0.95">
    SECTION 03
  </text>

  <text x="166" y="345" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="800" letter-spacing="-3" fill="url(#titleFill)">
    <tspan x="166" dy="0">Bold</tspan>
    <tspan fill="#FFB000"> New</tspan>
    <tspan x="166" dy="92">Direction</tspan>
  </text>

  <text x="176" y="523" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="500" fill="#D8E6FF" opacity="0.78">
    A confident transition slide for opening a new chapter.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense body copy or bullet lists; this divider should have one dominant message only
- ❌ Centering every element symmetrically; the drama comes from asymmetry and diagonal movement
- ❌ Thin, low-contrast headline typography; use heavy weight, large scale, and strong contrast
- ❌ Applying filters to `<line>` elements; keep shadows/glows on paths, circles, rectangles, or text
- ❌ Decorative elements that crowd the headline; accents should frame the title, not sit behind every word

## Composition notes
- Keep the headline in the left-center 60% of the canvas, with generous negative space around it.
- Use diagonal bands from opposite corners to create momentum and make the slide feel like a true section break.
- Restrict bright accents to 2–3 colors so the layout feels premium rather than chaotic.
- Let small dots, chips, and dashed lines echo the accent colors, but keep them secondary to the headline.