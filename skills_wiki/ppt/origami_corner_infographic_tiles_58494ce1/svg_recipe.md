# SVG Recipe — Origami Corner Infographic Tiles

## Visual mechanism
A square infographic card is made tactile by cutting off the top-left corner and placing a triangular “fold” back over it, creating a dog-eared paper illusion. The effect depends on precise polygon geometry, layered shadows, saturated color blocks, and a clean white content panel inside each tile.

## SVG primitives needed
- 4× `<path>` for the five-sided colored tile bases with the top-left corner removed
- 4× `<path>` for the triangular folded corners
- 4× `<line>` for subtle diagonal crease highlights on each fold
- 4× `<rect>` for the inset white content panels
- 4× small decorative `<path>` icons inside the cards
- 1× `<radialGradient>` for the premium light background
- 4× `<linearGradient>` fills for the saturated tile bases
- 4× `<linearGradient>` fills for the folded corner triangles
- 2× `<filter>` definitions for soft card shadows and lighter inner-panel shadows
- Multiple `<text>` elements with explicit `width` for step numbers, titles, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="38%" r="75%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="65%" stop-color="#f4f6f8"/>
      <stop offset="100%" stop-color="#e8ebef"/>
    </radialGradient>

    <linearGradient id="greenBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#88c55b"/>
      <stop offset="100%" stop-color="#5f9f36"/>
    </linearGradient>
    <linearGradient id="blueBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5b8be0"/>
      <stop offset="100%" stop-color="#315fae"/>
    </linearGradient>
    <linearGradient id="orangeBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f6a15c"/>
      <stop offset="100%" stop-color="#dd6a24"/>
    </linearGradient>
    <linearGradient id="purpleBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8956c5"/>
      <stop offset="100%" stop-color="#5d2b9a"/>
    </linearGradient>

    <linearGradient id="greenFold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#b7df95"/>
      <stop offset="100%" stop-color="#6dac42"/>
    </linearGradient>
    <linearGradient id="blueFold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a7c2f4"/>
      <stop offset="100%" stop-color="#416fc4"/>
    </linearGradient>
    <linearGradient id="orangeFold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffd0a6"/>
      <stop offset="100%" stop-color="#e47a32"/>
    </linearGradient>
    <linearGradient id="purpleFold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#c9a9eb"/>
      <stop offset="100%" stop-color="#7030a0"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-12%" y="-12%" width="124%" height="130%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="5"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .13 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <text x="90" y="74" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#202733">Origami Corner Infographic Tiles</text>
  <text x="90" y="108" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#667085">Use folded-corner cards to turn sequential information into tactile, premium-looking steps.</text>

  <g transform="translate(360 165)">
    <path d="M58 0 L240 0 L240 220 L0 220 L0 58 Z" fill="url(#greenBase)" filter="url(#cardShadow)"/>
    <rect x="18" y="76" width="204" height="126" rx="12" fill="#ffffff" filter="url(#panelShadow)"/>
    <path d="M0 58 L58 0 L58 58 Z" fill="url(#greenFold)" filter="url(#panelShadow)"/>
    <line x1="0" y1="58" x2="58" y2="0" stroke="#ffffff" stroke-width="2" opacity="0.52"/>
    <text x="78" y="51" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">01</text>
    <text x="32" y="112" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#27313f">DISCOVER</text>
    <text x="32" y="142" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#596273">Map the audience, surface the real problem, and define the decision context.</text>
    <path d="M172 160 C180 146 198 146 206 160 C198 174 180 174 172 160 Z M186 160 A6 6 0 1 0 198 160 A6 6 0 1 0 186 160" fill="none" stroke="#70ad47" stroke-width="3" stroke-linecap="round"/>
  </g>

  <g transform="translate(680 165)">
    <path d="M58 0 L240 0 L240 220 L0 220 L0 58 Z" fill="url(#blueBase)" filter="url(#cardShadow)"/>
    <rect x="18" y="76" width="204" height="126" rx="12" fill="#ffffff" filter="url(#panelShadow)"/>
    <path d="M0 58 L58 0 L58 58 Z" fill="url(#blueFold)" filter="url(#panelShadow)"/>
    <line x1="0" y1="58" x2="58" y2="0" stroke="#ffffff" stroke-width="2" opacity="0.52"/>
    <text x="78" y="51" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">02</text>
    <text x="32" y="112" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#27313f">DESIGN</text>
    <text x="32" y="142" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#596273">Shape the offer, simplify the story, and build the visual system around one idea.</text>
    <path d="M176 151 L203 151 L203 178 L176 178 Z M181 156 L198 173 M198 156 L181 173" fill="none" stroke="#4472c4" stroke-width="3" stroke-linecap="round"/>
  </g>

  <g transform="translate(360 425)">
    <path d="M58 0 L240 0 L240 220 L0 220 L0 58 Z" fill="url(#orangeBase)" filter="url(#cardShadow)"/>
    <rect x="18" y="76" width="204" height="126" rx="12" fill="#ffffff" filter="url(#panelShadow)"/>
    <path d="M0 58 L58 0 L58 58 Z" fill="url(#orangeFold)" filter="url(#panelShadow)"/>
    <line x1="0" y1="58" x2="58" y2="0" stroke="#ffffff" stroke-width="2" opacity="0.52"/>
    <text x="78" y="51" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">03</text>
    <text x="32" y="112" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#27313f">DELIVER</text>
    <text x="32" y="142" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#596273">Package the solution into a crisp sequence with clear proof, rhythm, and handoffs.</text>
    <path d="M174 176 L190 148 L207 176 Z M190 148 L190 166" fill="none" stroke="#ed7d31" stroke-width="3" stroke-linejoin="round"/>
  </g>

  <g transform="translate(680 425)">
    <path d="M58 0 L240 0 L240 220 L0 220 L0 58 Z" fill="url(#purpleBase)" filter="url(#cardShadow)"/>
    <rect x="18" y="76" width="204" height="126" rx="12" fill="#ffffff" filter="url(#panelShadow)"/>
    <path d="M0 58 L58 0 L58 58 Z" fill="url(#purpleFold)" filter="url(#panelShadow)"/>
    <line x1="0" y1="58" x2="58" y2="0" stroke="#ffffff" stroke-width="2" opacity="0.52"/>
    <text x="78" y="51" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">04</text>
    <text x="32" y="112" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#27313f">SCALE</text>
    <text x="32" y="142" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#596273">Turn the winning model into repeatable assets, rituals, and measurable momentum.</text>
    <path d="M174 169 C184 148 199 148 209 169 M181 169 L181 179 M202 169 L202 179 M174 179 L209 179" fill="none" stroke="#7030a0" stroke-width="3" stroke-linecap="round"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using a plain `<rect>` for the colored tile base; the cut corner must be a five-point `<path>` polygon.
- ❌ Applying `filter` to the diagonal `<line>` crease; line filters are dropped, so keep the crease unfiltered.
- ❌ Using `<mask>` to fake the folded corner; directly draw the base pentagon and fold triangle instead.
- ❌ Using `<use>` to duplicate the tile; repeat the editable shapes explicitly or group them with `transform`.
- ❌ Placing text too close to the fold; the folded corner consumes visual space and can make numbers feel cramped.

## Composition notes
- Keep tiles square or near-square, with the fold size around 22–28% of the tile width for a believable origami effect.
- Use generous gutters; the shadows need open space to read as physical depth rather than clutter.
- Put step numbers in the colored top band and main content in the white inset panel for strong hierarchy.
- Rotate color accents across tiles, but keep the fold direction consistent so the grid feels intentional and premium.