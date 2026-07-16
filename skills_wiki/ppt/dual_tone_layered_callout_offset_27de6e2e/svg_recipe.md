# SVG Recipe — Dual-Tone Layered Callout Offset

## Visual mechanism
Two identical speech-bubble callout shapes are stacked with a small down-right offset: the rear layer is a darker tone with a soft shadow, while the front layer is a lighter tint that carries the message. The result is a tactile “sticker stack” highlight that makes a key data insight feel prominent without using complex 3D.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 6× `<line>` for faint chart-grid context behind the callout
- 7× `<circle>` for subtle data-dot decoration and color rhythm
- 2× identical `<path>` callout shapes, one dark offset back layer and one light front layer
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to the rear callout path
- 2× `<linearGradient>` fills for the soft background and front callout tint
- 5× `<text>` elements with explicit `width` attributes for title, callout copy, KPI emphasis, and caption labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFDFD"/>
      <stop offset="58%" stop-color="#FFF6F7"/>
      <stop offset="100%" stop-color="#F8EEF1"/>
    </linearGradient>

    <linearGradient id="frontRose" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E6ADB6"/>
      <stop offset="100%" stop-color="#D796A2"/>
    </linearGradient>

    <filter id="softShadow" x="-15%" y="-15%" width="140%" height="145%">
      <feOffset dx="10" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.12  0 0 0 0 0.04  0 0 0 0 0.06  0 0 0 0.30 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <line x1="180" y1="470" x2="1100" y2="470" stroke="#EBD7DC" stroke-width="2" stroke-dasharray="8 14"/>
  <line x1="180" y1="400" x2="1100" y2="400" stroke="#EBD7DC" stroke-width="2" stroke-dasharray="8 14"/>
  <line x1="180" y1="330" x2="1100" y2="330" stroke="#EBD7DC" stroke-width="2" stroke-dasharray="8 14"/>
  <line x1="180" y1="260" x2="1100" y2="260" stroke="#EBD7DC" stroke-width="2" stroke-dasharray="8 14"/>
  <line x1="230" y1="520" x2="1050" y2="520" stroke="#D7A7B0" stroke-width="3"/>
  <line x1="230" y1="520" x2="230" y2="225" stroke="#D7A7B0" stroke-width="3"/>

  <circle cx="326" cy="445" r="7" fill="#6D1930"/>
  <circle cx="438" cy="414" r="7" fill="#6D1930"/>
  <circle cx="552" cy="388" r="7" fill="#6D1930"/>
  <circle cx="668" cy="350" r="7" fill="#6D1930"/>
  <circle cx="786" cy="326" r="7" fill="#6D1930"/>
  <circle cx="902" cy="292" r="7" fill="#6D1930"/>
  <circle cx="1018" cy="276" r="7" fill="#6D1930"/>

  <text x="190" y="92" width="900" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#333033">
    Dual-tone callout for the decisive insight
  </text>

  <text x="193" y="126" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#7E6870">
    Use the offset layer to make one number or quote feel lifted from the chart.
  </text>

  <path d="M360 230 H860 Q888 230 888 258 V424 Q888 452 860 452 H515 L468 498 L478 452 H388 Q360 452 360 424 V258 Q360 230 388 230 Z"
        transform="translate(32 28)"
        fill="#69192D"
        filter="url(#softShadow)"/>

  <path d="M360 230 H860 Q888 230 888 258 V424 Q888 452 860 452 H515 L468 498 L478 452 H388 Q360 452 360 424 V258 Q360 230 388 230 Z"
        fill="url(#frontRose)"/>

  <text x="410" y="293" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700" fill="#321419">
    Key takeaway
  </text>

  <text x="410" y="342" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="700" fill="#321419">
    <tspan>Retention rose </tspan><tspan fill="#69192D">18%</tspan>
  </text>

  <text x="410" y="389" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" fill="#432129">
    after simplifying onboarding into three guided steps, turning a flat metric into an executive-ready headline.
  </text>

  <circle cx="840" cy="274" r="18" fill="#F5CDD4" opacity="0.78"/>
  <circle cx="876" cy="312" r="10" fill="#F9DCE1" opacity="0.9"/>
  <circle cx="815" cy="420" r="7" fill="#7C2639" opacity="0.5"/>

  <text x="395" y="585" width="490" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#705C64">
    The back layer should be offset just enough to be visible, not so far that it reads as a separate card.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` to duplicate the callout; repeat the same `<path d="...">` explicitly so both layers remain editable.
- ❌ Do not apply `filter` to connector `<line>` elements; keep the shadow only on the rear callout path.
- ❌ Do not use `clip-path` or masks for the callout layers; simple duplicated paths translate more reliably.
- ❌ Do not make the rear layer a translucent black shadow only; the technique depends on a visible dark monochrome shape offset from the lighter front shape.

## Composition notes
- Keep the dual-tone callout centered and large, roughly 45–55% of slide width, so it becomes the visual anchor.
- Offset the rear layer diagonally down-right by about 24–36 px on a 1280×720 canvas; smaller feels like a border, larger feels misaligned.
- Use one hue family: dark saturated rear layer, lighter front tint, and very dark text for contrast.
- Surround the callout with quiet chart/grid context or negative space so the layered card remains the focal point.