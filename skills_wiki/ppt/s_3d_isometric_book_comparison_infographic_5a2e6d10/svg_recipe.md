# SVG Recipe — 3D Isometric Book Comparison Infographic

## Visual mechanism
A central open-book form is built from four sloped polygons: pale “back pages” behind two saturated cover planes. Large rotated letters and horizontally branched callouts make the book feel like a pseudo-3D comparison object rather than a flat two-column table.

## SVG primitives needed
- 4× main `<path>` polygons for left pages, right pages, left cover, and right cover
- 1× blurred `<ellipse>` shadow under the book for table-top depth
- 6–10× thin `<path>` or `<line>` details for page seams, cover highlights, and spine crease
- 4× `<line>` connector strokes from book to callout blocks
- 4× small `<circle>` icon badges for callout anchors
- 8–12× simple `<path>` icon glyphs inside badges
- 10–16× `<text>` elements with explicit `width` for title, labels, giant A/B letters, and callout copy
- 3–5× `<linearGradient>` fills for cover shading, page shading, and background atmosphere
- 1× `<filter id="softShadow">` applied to the book shadow or decorative cards
- Optional 2–4× decorative translucent `<path>` blobs for premium keynote background depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#F7FBFF"/>
      <stop offset="0.55" stop-color="#F2FAF8"/>
      <stop offset="1" stop-color="#EEF4FF"/>
    </linearGradient>
    <linearGradient id="leftCoverGrad" x1="380" y1="240" x2="650" y2="580">
      <stop offset="0" stop-color="#28D6B2"/>
      <stop offset="0.58" stop-color="#1ABC9C"/>
      <stop offset="1" stop-color="#13A98B"/>
    </linearGradient>
    <linearGradient id="rightCoverGrad" x1="640" y1="250" x2="900" y2="570">
      <stop offset="0" stop-color="#20B997"/>
      <stop offset="0.62" stop-color="#169F85"/>
      <stop offset="1" stop-color="#0F806F"/>
    </linearGradient>
    <linearGradient id="leftPageGrad" x1="385" y1="220" x2="650" y2="292">
      <stop offset="0" stop-color="#DDF8F2"/>
      <stop offset="1" stop-color="#A3E4D7"/>
    </linearGradient>
    <linearGradient id="rightPageGrad" x1="895" y1="220" x2="640" y2="292">
      <stop offset="0" stop-color="#C9F1E9"/>
      <stop offset="1" stop-color="#76D7C4"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M84 110 C180 48 285 56 352 126 C260 146 198 198 156 278 C98 236 60 176 84 110 Z" fill="#DFF7F1" opacity="0.5"/>
  <path d="M1078 90 C1172 104 1228 176 1226 260 C1152 220 1078 218 1002 254 C1012 180 1030 124 1078 90 Z" fill="#DCE8FF" opacity="0.55"/>
  <text x="80" y="66" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#172B4D">Old Way vs. New Way</text>
  <text x="80" y="100" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6B778C">A premium isometric book comparison for strategic choices, methods, or product directions.</text>

  <ellipse cx="640" cy="588" rx="315" ry="42" fill="#103A4A" opacity="0.16" filter="url(#softShadow)"/>

  <!-- Back page planes -->
  <path d="M384 240 L403 221 L639 269 L639 288 Z" fill="url(#leftPageGrad)" stroke="#8FD8CB" stroke-width="1.5"/>
  <path d="M896 240 L876 221 L639 269 L639 288 Z" fill="url(#rightPageGrad)" stroke="#6DCCBB" stroke-width="1.5"/>
  <path d="M422 233 L639 276" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>
  <path d="M858 233 L639 276" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.65"/>

  <!-- Front cover planes -->
  <path d="M384 240 L639 288 L639 576 L384 528 Z" fill="url(#leftCoverGrad)" stroke="#0F9D83" stroke-width="2"/>
  <path d="M639 288 L896 240 L896 528 L639 576 Z" fill="url(#rightCoverGrad)" stroke="#0E7F70" stroke-width="2"/>
  <path d="M639 288 L639 576" fill="none" stroke="#0B6F63" stroke-width="4" opacity="0.5"/>
  <path d="M405 262 L620 303 L620 551 L405 512 Z" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.18"/>
  <path d="M661 303 L875 263 L875 512 L661 552 Z" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.14"/>

  <!-- Perspective letters -->
  <text x="462" y="438" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="900" fill="#FFFFFF" opacity="0.96" transform="rotate(11 527 420)">A</text>
  <text x="698" y="438" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="122" font-weight="900" fill="#FFFFFF" opacity="0.96" transform="rotate(-11 763 420)">B</text>
  <text x="448" y="506" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#EFFFFB" transform="rotate(11 528 494)">CURRENT MODEL</text>
  <text x="674" y="506" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#EFFFFB" transform="rotate(-11 764 494)">TARGET MODEL</text>

  <!-- Connector lines -->
  <line x1="412" y1="318" x2="250" y2="255" stroke="#A7B3C2" stroke-width="2"/>
  <line x1="408" y1="462" x2="248" y2="520" stroke="#A7B3C2" stroke-width="2"/>
  <line x1="868" y1="318" x2="1030" y2="255" stroke="#A7B3C2" stroke-width="2"/>
  <line x1="872" y1="462" x2="1032" y2="520" stroke="#A7B3C2" stroke-width="2"/>

  <!-- Left top callout -->
  <rect x="76" y="206" width="282" height="104" rx="22" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <circle cx="118" cy="256" r="25" fill="#1ABC9C"/>
  <path d="M108 255 L118 243 L130 255 L118 267 Z" fill="#FFFFFF"/>
  <text x="158" y="244" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#172B4D">Legacy Process</text>
  <text x="158" y="270" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B778C">Sequential handoffs and hidden decision points slow learning.</text>

  <!-- Left bottom callout -->
  <rect x="76" y="472" width="282" height="104" rx="22" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <circle cx="118" cy="522" r="25" fill="#1ABC9C"/>
  <path d="M105 524 C113 512 122 512 131 524 M112 533 L124 533" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="158" y="510" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#172B4D">Team Impact</text>
  <text x="158" y="536" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B778C">Creates dependency queues and uneven ownership across roles.</text>

  <!-- Right top callout -->
  <rect x="922" y="206" width="282" height="104" rx="22" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <circle cx="1162" cy="256" r="25" fill="#169F85"/>
  <path d="M1150 258 L1158 266 L1175 246" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="952" y="244" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#172B4D">Modern System</text>
  <text x="952" y="270" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B778C">Parallel experiments reveal evidence while momentum stays high.</text>

  <!-- Right bottom callout -->
  <rect x="922" y="472" width="282" height="104" rx="22" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <circle cx="1162" cy="522" r="25" fill="#169F85"/>
  <path d="M1152 532 L1152 514 L1172 506 L1172 524 Z M1152 514 L1162 522 L1172 506" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round"/>
  <text x="952" y="510" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#172B4D">Decision Quality</text>
  <text x="952" y="536" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B778C">Clear feedback loops make tradeoffs visible and comparable.</text>

  <text x="460" y="646" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A869A" text-anchor="middle">Use one accent hue, then darken one cover and lighten the back pages to sell the 3D illusion.</text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` to fake perspective; use hand-drawn polygon coordinates instead.
- ❌ `<path marker-end="...">` for connector arrows; use plain `<line>` connectors or separate small arrowhead `<path>` triangles.
- ❌ Applying `filter` to `<line>` connectors; shadows may silently drop, so shadow cards or book planes instead.
- ❌ Clipping or masking the book polygons; build each visible plane as its own editable `<path>`.
- ❌ Flat rectangles for the book covers; the entire effect depends on sloped quadrilateral geometry.

## Composition notes
- Keep the book centered and large enough to occupy roughly the middle third of the slide; it is the visual anchor.
- Leave wide left and right gutters for callout cards, using connector lines to tether them to the cover edges.
- Rotate the A/B letters approximately `+11°` and `-11°` to match the page slope; this is the key perspective trick.
- Use one accent color family: light tints for back pages, saturated color for the left cover, and a darker shade for the right cover.