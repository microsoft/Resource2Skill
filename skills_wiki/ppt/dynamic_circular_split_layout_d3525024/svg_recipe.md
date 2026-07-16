# SVG Recipe — Dynamic Circular Split Layout

## Visual mechanism
An off-center circular photo is layered over a larger gradient circle so only a bold crescent of color remains visible, creating motion and depth. Structured typography and rounded content blocks occupy the opposite side, balancing organic geometry with clean executive-slide information design.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× large `<circle>` for the oversized gradient framing disc
- 1× `<image>` clipped by a circular `<clipPath>` for the hero photo
- 1× `<path>` for a soft decorative swoosh that reinforces circular motion
- 10× rounded `<rect>` for summary pills, section headers, and content cards
- 6× `<circle>` / `<ellipse>` for small decorative dots and logo-like accents
- 1× `<linearGradient>` for teal-to-blue circular energy
- 2× `<linearGradient>` for green pills and pale blue cards
- 1× `<filter id="shadow">` applied to cards and the photo cluster
- Multiple `<text>` elements with explicit `width` for title, subtitles, labels, and agenda/specification copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealBlue" x1="0" y1="120" x2="360" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00D2B5"/>
      <stop offset="58%" stop-color="#11C779"/>
      <stop offset="100%" stop-color="#0066CC"/>
    </linearGradient>
    <linearGradient id="pillGreen" x1="0" y1="0" x2="230" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#22D488"/>
      <stop offset="100%" stop-color="#00B96E"/>
    </linearGradient>
    <linearGradient id="cardBlue" x1="0" y1="0" x2="0" y2="160" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#EBFAFF"/>
      <stop offset="100%" stop-color="#CDEFFF"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="9"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.10  0 0 0 0 0.16  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoClip">
      <circle cx="185" cy="410" r="148"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="42" y="57" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="600" fill="#1E2832">
    New product summary and specification details
  </text>
  <text x="43" y="80" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#7B8791">
    This slide demonstrates an editable circular split layout with masked imagery, gradient framing, and structured content blocks.
  </text>

  <circle cx="64" cy="365" r="218" fill="url(#tealBlue)" filter="url(#glow)"/>
  <circle cx="71" cy="367" r="160" fill="#FFFFFF"/>
  <path d="M-22,572 C58,618 142,624 217,582 C282,546 337,486 375,409 C327,522 250,612 151,651 C84,677 18,665 -44,629 Z"
        fill="#0066CC" opacity="0.92"/>

  <image href="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=900&auto=format&fit=crop"
         x="37" y="262" width="296" height="296" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoClip)" filter="url(#shadow)"/>
  <circle cx="185" cy="410" r="148" fill="none" stroke="#FFFFFF" stroke-width="7"/>

  <circle cx="31" cy="610" r="11" fill="#0095D9"/>
  <circle cx="117" cy="608" r="5" fill="#20D083"/>
  <ellipse cx="388" cy="126" rx="58" ry="8" fill="#CFF7EE" opacity="0.75"/>

  <circle cx="1046" cy="52" r="12" fill="#2DBFEA"/>
  <circle cx="1072" cy="52" r="12" fill="#2DBFEA"/>
  <circle cx="1059" cy="34" r="12" fill="#2DBFEA"/>
  <text x="1090" y="47" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#1796C8">Slide</text>
  <text x="1090" y="72" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#1796C8">Team</text>

  <line x1="360" y1="103" x2="1186" y2="103" stroke="#D9EEF2" stroke-width="2"/>
  <rect x="560" y="92" width="282" height="24" rx="12" fill="#E8F7F2"/>
  <text x="668" y="109" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2E8B6C">Summary</text>

  <rect x="365" y="142" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <rect x="552" y="142" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <rect x="739" y="142" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <rect x="926" y="142" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <text x="407" y="160" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Processor</text>
  <text x="401" y="177" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">8-core B570</text>
  <text x="591" y="160" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Camera</text>
  <text x="577" y="177" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">108MP ultra-wide</text>
  <text x="781" y="160" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Battery</text>
  <text x="781" y="177" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">4300 mAh</text>
  <text x="971" y="160" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Storage</text>
  <text x="970" y="177" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">128 GB</text>

  <rect x="365" y="222" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <rect x="552" y="222" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <rect x="739" y="222" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <rect x="926" y="222" width="166" height="46" rx="23" fill="url(#pillGreen)"/>
  <text x="395" y="240" width="115" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Launch date</text>
  <text x="405" y="257" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">25 Oct 2026</text>
  <text x="597" y="240" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Display</text>
  <text x="588" y="257" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">6.5 in retina</text>
  <text x="786" y="240" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">RAM</text>
  <text x="792" y="257" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">8 GB</text>
  <text x="976" y="240" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">AI</text>
  <text x="949" y="257" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#EFFFFA">Local engine</text>

  <line x1="360" y1="318" x2="1186" y2="318" stroke="#D9EEF2" stroke-width="2"/>
  <rect x="548" y="306" width="300" height="24" rx="12" fill="#EAF4FF"/>
  <text x="665" y="323" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3576AD">Specifications</text>

  <rect x="374" y="357" width="170" height="205" rx="12" fill="url(#cardBlue)" filter="url(#shadow)"/>
  <rect x="591" y="357" width="170" height="205" rx="12" fill="url(#cardBlue)" filter="url(#shadow)"/>
  <rect x="808" y="357" width="170" height="205" rx="12" fill="url(#cardBlue)" filter="url(#shadow)"/>
  <rect x="1025" y="357" width="170" height="205" rx="12" fill="url(#cardBlue)" filter="url(#shadow)"/>

  <rect x="391" y="342" width="136" height="30" rx="15" fill="#12A8E8"/>
  <rect x="608" y="342" width="136" height="30" rx="15" fill="#12A8E8"/>
  <rect x="825" y="342" width="136" height="30" rx="15" fill="#12A8E8"/>
  <rect x="1042" y="342" width="136" height="30" rx="15" fill="#12A8E8"/>
  <text x="428" y="362" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">General</text>
  <text x="651" y="362" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">Design</text>
  <text x="858" y="362" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">Display</text>
  <text x="1078" y="362" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">Camera</text>

  <text x="397" y="395" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#425466">
    Dual SIM ready<tspan x="397" dy="18">Android 13 OS</tspan><tspan x="397" dy="18">5G network support</tspan><tspan x="397" dy="18">Fingerprint unlock</tspan><tspan x="397" dy="18">NFC payments</tspan>
  </text>
  <text x="614" y="395" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#425466">
    Glass front<tspan x="614" dy="18">Aluminum frame</tspan><tspan x="614" dy="18">Matte finish</tspan><tspan x="614" dy="18">IP68 protection</tspan><tspan x="614" dy="18">192 g weight</tspan>
  </text>
  <text x="831" y="395" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#425466">
    120 Hz refresh<tspan x="831" dy="18">OLED panel</tspan><tspan x="831" dy="18">HDR contrast</tspan><tspan x="831" dy="18">Peak 1800 nits</tspan><tspan x="831" dy="18">Always-on mode</tspan>
  </text>
  <text x="1048" y="395" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#425466">
    Triple lens array<tspan x="1048" dy="18">108MP main</tspan><tspan x="1048" dy="18">12MP ultra-wide</tspan><tspan x="1048" dy="18">Optical zoom</tspan><tspan x="1048" dy="18">Night capture</tspan>
  </text>

  <text x="392" y="646" width="735" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#9AA5AD">
    Source: Product launch planning deck. All elements are editable PowerPoint shapes after SVG translation.
  </text>
  <circle cx="1208" cy="662" r="12" fill="#12A8E8"/>
  <text x="1204" y="667" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#FFFFFF">i</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to create the crescent; instead, layer a large gradient circle behind a clipped circular image.
- ❌ Do not apply `clip-path` to circles, paths, or rectangles; only clip the `<image>` for reliable PowerPoint translation.
- ❌ Do not use `<pattern>` fills for the card backgrounds; use editable gradients and solid fills.
- ❌ Do not put shadows on `<line>` elements; keep filters on rectangles, circles, paths, text, or the clipped image.
- ❌ Do not overfill the circular side with text; the circle cluster should read as a visual anchor, not a second content panel.

## Composition notes
- Keep the circular image cluster bleeding toward one slide edge, with the gradient circle offset behind it to form a visible crescent.
- Reserve the opposite 55–65% of the canvas for structured text, pills, lists, or specification cards.
- Use white space as the separator between the organic photo cluster and the linear content system.
- Repeat teal, green, and blue accents across pills, dividers, and headers so the circular frame feels integrated rather than decorative.