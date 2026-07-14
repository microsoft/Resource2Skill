# SVG Recipe — Donut Split Highlight

## Visual mechanism
A large left-side donut graphic anchors the slide, with split-color arc segments and a diagonal accent ribbon slicing through it. The right side stays clean and text-forward, balancing the bold circular motif with a headline and concise bullet list.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and subtle right-side text panel wash
- 4× `<path>` for organic background blobs, donut arc strokes, and the diagonal accent ribbon
- 1× `<image>` clipped into a circle for the donut center photo/texture
- 1× `<clipPath>` with `<circle>` for the circular image crop
- 2× `<linearGradient>` for background and accent ribbon fills
- 1× `<radialGradient>` for the soft donut-center glow
- 2× `<filter>` using blur/offset for premium shadows and glow
- 6× `<circle>` for donut base ring, bullet icons, and small decorative dots
- 7× `<text>` elements with explicit `width` for headline, ribbon label, and bullet copy
- Optional `<tspan>` inside headline text for inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF4FF"/>
    </linearGradient>

    <linearGradient id="ribbonGrad" x1="150" y1="405" x2="550" y2="405">
      <stop offset="0%" stop-color="#FFB000"/>
      <stop offset="52%" stop-color="#FF6B35"/>
      <stop offset="100%" stop-color="#E83E8C"/>
    </linearGradient>

    <linearGradient id="arcBlue" x1="180" y1="180" x2="540" y2="540">
      <stop offset="0%" stop-color="#1E88E5"/>
      <stop offset="100%" stop-color="#173B8F"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#EAF2FF"/>
      <stop offset="100%" stop-color="#D7E5FF"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.07  0 0 0 0 0.13  0 0 0 0 0.24  0 0 0 0.20 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="warmGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="centerPhotoClip">
      <circle cx="356" cy="360" r="112"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <path d="M-70,95 C55,10 170,50 225,150 C286,262 176,330 55,304 C-45,282 -118,210 -70,95 Z"
        fill="#DDEBFF" opacity="0.75"/>
  <path d="M1018,620 C1100,540 1220,548 1314,630 L1314,760 L982,760 C944,706 960,674 1018,620 Z"
        fill="#F6D7E7" opacity="0.55"/>

  <rect x="650" y="82" width="530" height="556" rx="44" fill="#FFFFFF" opacity="0.58"/>

  <circle cx="356" cy="360" r="207" fill="none" stroke="#E4ECF8" stroke-width="66"/>
  <circle cx="356" cy="360" r="114" fill="url(#centerGlow)" filter="url(#softShadow)"/>

  <path d="M495,263 A170,170 0 1,1 209,275"
        fill="none" stroke="url(#arcBlue)" stroke-width="62" stroke-linecap="round" filter="url(#softShadow)"/>
  <path d="M234,242 A170,170 0 0,1 497,265"
        fill="none" stroke="#FFB000" stroke-width="62" stroke-linecap="round" filter="url(#warmGlow)"/>

  <image href="https://images.example.com/premium-circular-photo-of-team-collaboration.jpg"
         x="244" y="248" width="224" height="224" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#centerPhotoClip)"/>

  <circle cx="356" cy="360" r="116" fill="none" stroke="#FFFFFF" stroke-width="8"/>
  <circle cx="206" cy="195" r="13" fill="#FF6B35"/>
  <circle cx="510" cy="448" r="9" fill="#1E88E5"/>
  <circle cx="535" cy="218" r="6" fill="#FFB000"/>

  <path d="M178,409 L508,349 Q530,345 536,366 L547,411 Q552,433 529,437 L199,497 Q177,501 171,480 L160,434 Q155,414 178,409 Z"
        fill="url(#ribbonGrad)" filter="url(#softShadow)"/>

  <text x="218" y="443" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#FFFFFF" transform="rotate(-10 218 443)">
    MARKET SIGNAL
  </text>

  <text x="700" y="182" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="750" fill="#16233F">
    Donut Split <tspan fill="#FF6B35">Highlight</tspan>
  </text>

  <text x="704" y="252" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="400" fill="#58657A">
    Use the circular split as a visual anchor, then let the right panel carry the executive message.
  </text>

  <circle cx="724" cy="338" r="17" fill="#EAF2FF" stroke="#1E88E5" stroke-width="2"/>
  <text x="718" y="346" width="20" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800" fill="#1E88E5">1</text>
  <text x="760" y="347" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#22304A">Frame the left donut as the core idea</text>

  <circle cx="724" cy="410" r="17" fill="#FFF4DA" stroke="#FFB000" stroke-width="2"/>
  <text x="718" y="418" width="20" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800" fill="#D88A00">2</text>
  <text x="760" y="419" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#22304A">Let the diagonal ribbon create momentum</text>

  <circle cx="724" cy="482" r="17" fill="#FFEAF4" stroke="#E83E8C" stroke-width="2"/>
  <text x="718" y="490" width="20" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800" fill="#E83E8C">3</text>
  <text x="760" y="491" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#22304A">Keep supporting points short and high contrast</text>

  <line x1="700" y1="555" x2="1110" y2="555" stroke="#D8E2F2" stroke-width="2" stroke-dasharray="8 10"/>
  <text x="704" y="594" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#7A869A">
    Best for section openers, comparison setups, or a single strategic takeaway.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a true SVG `<mask>` to cut the donut hole; build the ring with stroked circles/paths instead.
- ❌ Applying `filter` to `<line>` elements for dividers or connectors; shadows/glows should be on paths, rects, circles, or text.
- ❌ Using `skewX`, `skewY`, or matrix transforms for the ribbon; draw the angled ribbon directly as a `<path>`.
- ❌ Clipping the donut arcs or ribbon with `clip-path`; clipping should only be used on the center `<image>`.

## Composition notes
- Keep the donut center around x=350 and give it roughly 40–45% of slide width; it should feel oversized and intentional.
- Place headline and bullets in the right 45% of the canvas with generous line spacing and a soft panel or negative space behind them.
- Let the accent ribbon cross the lower-middle of the donut and point toward the text area to visually connect both halves.
- Use one cool arc color, one warm arc color, and repeat those colors in bullet icons for a cohesive rhythm.