# SVG Recipe — Architectural Earth-Tone Infographic Layout

## Visual mechanism
A calm, architectural infographic built from large earth-tone blocks, generous margins, and a technical radar chart that feels like a site-plan diagram. The slide balances a heavy sage text slab on the left with a beige analytical workspace on the right, using subtle grid lines, clipped imagery, and geometric data layers.

## SVG primitives needed
- 9× `<rect>` for the beige canvas, sage sidebar, radar panel, photo card, overlay wash, metric cards, and small accent bars
- 1× `<image>` clipped into a rounded architectural photo banner
- 1× `<clipPath>` with rounded `<rect>` for the photo crop
- 2× `<linearGradient>` for the photo overlay and radar data fill
- 1× `<filter id="softShadow">` applied to card rectangles for quiet editorial depth
- 18× `<line>` for the architectural background grid, radar axes, and small metric dividers
- 7× `<path>` for radar rings, filled radar area, benchmark outline, and decorative plan-like corner geometry
- 6× `<circle>` for radar vertex markers
- 20× `<text>` with explicit `width` attributes for titles, labels, axis names, values, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#555C49" stop-opacity="0.58"/>
      <stop offset="70%" stop-color="#989F88" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#EBE9E0" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="radarFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#989F88" stop-opacity="0.76"/>
      <stop offset="100%" stop-color="#555C49" stop-opacity="0.54"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.18  0 0 0 0 0.20  0 0 0 0 0.16  0 0 0 0.20 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoClip">
      <rect x="520" y="66" width="640" height="150" rx="22" ry="22"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#EBE9E0"/>

  <!-- subtle architectural grid -->
  <line x1="470" y1="0" x2="470" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="570" y1="0" x2="570" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="670" y1="0" x2="670" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="770" y1="0" x2="770" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="870" y1="0" x2="870" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="970" y1="0" x2="970" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="1070" y1="0" x2="1070" y2="720" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="430" y1="120" x2="1280" y2="120" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="430" y1="240" x2="1280" y2="240" stroke="#D6D2C4" stroke-width="1"/>
  <line x1="430" y1="600" x2="1280" y2="600" stroke="#D6D2C4" stroke-width="1"/>

  <!-- left editorial block -->
  <rect x="0" y="0" width="430" height="720" fill="#989F88"/>
  <rect x="68" y="72" width="72" height="6" fill="#FFFFFF" opacity="0.82"/>
  <text x="68" y="136" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="700" fill="#FFFFFF">
    <tspan x="68" dy="0">Site</tspan>
    <tspan x="68" dy="58">Performance</tspan>
    <tspan x="68" dy="58">Frame</tspan>
  </text>
  <text x="70" y="342" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#F7F6F0">
    Six-dimensional evaluation of a mixed-use architectural concept against strategic delivery criteria.
  </text>
  <text x="70" y="455" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#FFFFFF" opacity="0.86">Q3 MASTERPLAN REVIEW</text>
  <line x1="70" y1="484" x2="330" y2="484" stroke="#FFFFFF" stroke-width="1.4" opacity="0.55"/>
  <text x="70" y="528" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF">Earth-tone visual language signals stability, material honesty, and long-range planning.</text>

  <!-- clipped architectural photo banner -->
  <rect x="520" y="66" width="640" height="150" rx="22" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.72"/>
  <image x="520" y="66" width="640" height="150" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/architectural-concrete-courtyard-sage-landscape.jpg"
         clip-path="url(#photoClip)"/>
  <rect x="520" y="66" width="640" height="150" rx="22" fill="url(#photoWash)"/>
  <text x="552" y="112" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" letter-spacing="2" fill="#FFFFFF">CONCEPT OPTION B</text>
  <text x="552" y="158" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">Courtyard Massing Strategy</text>

  <!-- main radar panel -->
  <rect x="505" y="255" width="700" height="372" rx="0" fill="#F7F5EC" filter="url(#softShadow)"/>
  <rect x="505" y="255" width="700" height="8" fill="#555C49"/>
  <text x="540" y="310" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#555C49">Performance radar</text>
  <text x="540" y="338" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777767">Score normalized to 100; outer ring indicates best-fit strategic alignment.</text>

  <!-- radar rings -->
  <path d="M845 250 L949 310 L949 430 L845 490 L741 430 L741 310 Z" fill="none" stroke="#C9C4B4" stroke-width="1.4"/>
  <path d="M845 220 L975 295 L975 445 L845 520 L715 445 L715 295 Z" fill="none" stroke="#C9C4B4" stroke-width="1.2" stroke-dasharray="5 6"/>
  <path d="M845 195 L997 282.5 L997 457.5 L845 545 L693 457.5 L693 282.5 Z" fill="none" stroke="#AFA994" stroke-width="1.6"/>
  <path d="M845 282 L921 326 L921 414 L845 458 L769 414 L769 326 Z" fill="none" stroke="#DDD8C9" stroke-width="1"/>

  <!-- radar axes -->
  <line x1="845" y1="370" x2="845" y2="195" stroke="#B8B29F" stroke-width="1"/>
  <line x1="845" y1="370" x2="997" y2="282.5" stroke="#B8B29F" stroke-width="1"/>
  <line x1="845" y1="370" x2="997" y2="457.5" stroke="#B8B29F" stroke-width="1"/>
  <line x1="845" y1="370" x2="845" y2="545" stroke="#B8B29F" stroke-width="1"/>
  <line x1="845" y1="370" x2="693" y2="457.5" stroke="#B8B29F" stroke-width="1"/>
  <line x1="845" y1="370" x2="693" y2="282.5" stroke="#B8B29F" stroke-width="1"/>

  <!-- benchmark and current score -->
  <path d="M845 239 L954 307 L962 438 L845 501 L735 434 L722 299 Z" fill="none" stroke="#555C49" stroke-width="2" stroke-dasharray="7 7" opacity="0.62"/>
  <path d="M845 216 L939 316 L959 436 L845 533 L742 430 L762 322 Z" fill="url(#radarFill)" stroke="#555C49" stroke-width="3"/>
  <circle cx="845" cy="216" r="5.5" fill="#555C49"/>
  <circle cx="939" cy="316" r="5.5" fill="#555C49"/>
  <circle cx="959" cy="436" r="5.5" fill="#555C49"/>
  <circle cx="845" cy="533" r="5.5" fill="#555C49"/>
  <circle cx="742" cy="430" r="5.5" fill="#555C49"/>
  <circle cx="762" cy="322" r="5.5" fill="#555C49"/>

  <!-- axis labels -->
  <text x="786" y="181" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#555C49" text-anchor="middle">Sustainability</text>
  <text x="1005" y="286" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555C49">Cost control</text>
  <text x="1005" y="466" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555C49">Delivery speed</text>
  <text x="783" y="575" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#555C49" text-anchor="middle">Spatial quality</text>
  <text x="604" y="466" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555C49">Material fit</text>
  <text x="594" y="286" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555C49">Community</text>

  <!-- lower metric cards -->
  <rect x="540" y="650" width="182" height="44" fill="#989F88"/>
  <rect x="748" y="650" width="182" height="44" fill="#DDD8C9"/>
  <rect x="956" y="650" width="182" height="44" fill="#555C49"/>
  <text x="560" y="678" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">88 ESG score</text>
  <text x="768" y="678" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#555C49">14 mo. delivery</text>
  <text x="976" y="678" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">+23% amenity</text>

  <!-- decorative plan geometry -->
  <path d="M1162 318 L1188 318 L1188 344 L1175 344 L1175 382 L1148 382 L1148 356 L1162 356 Z" fill="none" stroke="#989F88" stroke-width="2" opacity="0.55"/>
  <path d="M566 573 C600 548 633 548 668 573" fill="none" stroke="#989F88" stroke-width="2" opacity="0.55"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the blueprint grid; use explicit low-opacity `<line>` elements instead so PowerPoint keeps them editable.
- ❌ Screenshot-only radar charts; build the radar from editable `<line>`, `<path>`, `<circle>`, and `<text>` elements.
- ❌ Rounded clipping on non-image shapes with `clip-path`; the translator only preserves clipping reliably for `<image>`.
- ❌ Heavy drop shadows or glossy gradients; this style should feel matte, grounded, and architectural.
- ❌ Busy full-slide photography behind data labels; keep imagery contained in a clipped banner or side panel.

## Composition notes
- Use a 33–40% width sage sidebar for title and narrative; keep the remaining beige area as the analytical workspace.
- Place the radar chart slightly right of center so axis labels have breathing room and do not collide with the text block.
- Keep the palette muted: beige background, sage primary block, dark olive typography, and off-white data cards.
- Add sparse architectural grid lines and plan-like path details only as texture; they should support the structure, not compete with the chart.