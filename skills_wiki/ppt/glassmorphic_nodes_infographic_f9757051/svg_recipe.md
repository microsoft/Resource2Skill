# SVG Recipe — Glassmorphic Nodes Infographic

## Visual mechanism
A dark rounded stage holds four glowing radial-gradient nodes that appear to sit behind a translucent frosted-glass shield/hub. The illusion is made by layering neon nodes first, then placing a dark “knockout” shield over their inner halves, followed by a semi-transparent gradient shield with blur-glow accents, white stroke, and soft shadow.

## SVG primitives needed
- 1× full-slide `<rect>` for the deep navy background
- 1× large rounded `<rect>` for the elevated dark presentation card
- 4× glowing `<circle>` nodes with radial gradients and blur filters
- 1× `<path>` shield filled with background color to hide the inner halves of nodes
- 1× `<path>` shield with translucent glass gradient fill and white stroke
- 4× blurred `<ellipse>` highlights over the shield to simulate refracted color
- 4× `<line>` connectors from nodes to explanation labels
- 4× small icon groups made from `<path>`, `<circle>`, and `<line>`
- Multiple decorative `<path>`, `<circle>`, and `<rect>` accents for futuristic floating shapes
- 1× `<filter id="cardShadow">` for the large card shadow
- 1× `<filter id="nodeGlow">` for neon node glow
- 1× `<filter id="glassShadow">` for glass thickness/shadow
- Several `<linearGradient>` and `<radialGradient>` definitions for glass, nodes, and accents
- Multiple `<text>` elements with explicit `width` attributes for title, center label, numbers, and callout copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E0F2FE"/>
      <stop offset="45%" stop-color="#22D3EE"/>
      <stop offset="60%" stop-color="#FACC15"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
    <radialGradient id="cyanNode" cx="35%" cy="25%" r="75%">
      <stop offset="0%" stop-color="#67E8F9"/>
      <stop offset="55%" stop-color="#06B6D4"/>
      <stop offset="100%" stop-color="#0F766E"/>
    </radialGradient>
    <radialGradient id="tealNode" cx="35%" cy="25%" r="75%">
      <stop offset="0%" stop-color="#5EEAD4"/>
      <stop offset="58%" stop-color="#14B8A6"/>
      <stop offset="100%" stop-color="#115E59"/>
    </radialGradient>
    <linearGradient id="glassFill" x1="510" y1="205" x2="770" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#CBD5E1" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="100%" stop-color="#0F766E"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="nodeGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <filter id="glassShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softBlur" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8FAFC"/>
  <text x="38" y="58" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="900" font-style="italic" fill="url(#titleGrad)" stroke="#1D4ED8" stroke-width="2.2">4 STEP INFOGRAPHIC DESIGN</text>

  <rect x="145" y="82" width="990" height="556" rx="26" fill="#1E293B" filter="url(#cardShadow)"/>
  <rect x="145" y="82" width="990" height="556" rx="26" fill="none" stroke="#334155" stroke-width="1.4"/>

  <text x="154" y="126" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" letter-spacing="4" fill="#FFFFFF">
    <tspan x="154" dy="0">4 Step GLASSMORPHIC</tspan>
    <tspan x="236" dy="31">Infographic</tspan>
  </text>

  <circle cx="640" cy="228" r="76" fill="url(#cyanNode)" filter="url(#nodeGlow)"/>
  <circle cx="770" cy="360" r="76" fill="url(#tealNode)" filter="url(#nodeGlow)"/>
  <circle cx="640" cy="492" r="76" fill="url(#cyanNode)" filter="url(#nodeGlow)"/>
  <circle cx="510" cy="360" r="76" fill="url(#tealNode)" filter="url(#nodeGlow)"/>

  <line x1="566" y1="264" x2="414" y2="264" stroke="#94A3B8" stroke-width="1.4" stroke-opacity="0.45"/>
  <line x1="715" y1="256" x2="715" y2="148" stroke="#94A3B8" stroke-width="1.4" stroke-opacity="0.45"/>
  <line x1="714" y1="462" x2="820" y2="462" stroke="#94A3B8" stroke-width="1.4" stroke-opacity="0.45"/>
  <line x1="568" y1="486" x2="520" y2="548" stroke="#94A3B8" stroke-width="1.4" stroke-opacity="0.45"/>

  <path d="M640 208 C678 242 706 251 753 262 C767 265 771 276 770 292 C766 385 727 463 640 525 C553 463 514 385 510 292 C509 276 513 265 527 262 C574 251 602 242 640 208 Z" fill="#1E293B" opacity="0.88"/>
  <ellipse cx="586" cy="313" rx="48" ry="67" fill="#2DD4BF" opacity="0.56" filter="url(#softBlur)"/>
  <ellipse cx="695" cy="315" rx="48" ry="67" fill="#2DD4BF" opacity="0.54" filter="url(#softBlur)"/>
  <ellipse cx="640" cy="454" rx="58" ry="45" fill="#2DD4BF" opacity="0.50" filter="url(#softBlur)"/>
  <ellipse cx="640" cy="253" rx="54" ry="40" fill="#67E8F9" opacity="0.38" filter="url(#softBlur)"/>

  <path d="M640 208 C678 242 706 251 753 262 C767 265 771 276 770 292 C766 385 727 463 640 525 C553 463 514 385 510 292 C509 276 513 265 527 262 C574 251 602 242 640 208 Z"
        fill="url(#glassFill)" stroke="#E2E8F0" stroke-opacity="0.55" stroke-width="1.6" filter="url(#glassShadow)"/>
  <path d="M640 215 C675 247 705 257 748 267" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.35"/>
  <path d="M525 275 C518 348 542 430 640 510" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.22"/>

  <text x="623" y="277" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">01</text>
  <text x="715" y="368" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">02</text>
  <text x="622" y="479" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">03</text>
  <text x="529" y="365" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">04</text>
  <text x="598" y="358" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="900" letter-spacing="2" fill="#FFFFFF">
    <tspan x="598" dy="0">MAIN</tspan>
    <tspan x="587" dy="32">TITLE</tspan>
  </text>

  <circle cx="640" cy="178" r="15" fill="#F8FAFC" stroke="#0E7490" stroke-width="2"/>
  <path d="M633 178 L638 184 L648 171" fill="none" stroke="#0E7490" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M480 343 L480 375 M466 374 L494 374 M468 349 L492 349 M472 349 L472 369 M488 349 L488 369" stroke="#FFFFFF" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <path d="M794 352 C805 344 817 344 828 352 C817 361 805 361 794 352 Z" fill="none" stroke="#FFFFFF" stroke-width="2.2"/>
  <circle cx="811" cy="352" r="3.8" fill="#FFFFFF"/>
  <path d="M630 525 L667 541 L630 557 Z" fill="#FFFFFF"/>
  <circle cx="641" cy="541" r="4" fill="#1E293B"/>

  <text x="333" y="250" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" letter-spacing="6" fill="#FFFFFF">HEADING</text>
  <text x="310" y="270" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.92">
    <tspan x="310" dy="0">Some text goes here. Some</tspan><tspan x="314" dy="18">text goes here. Some text</tspan><tspan x="358" dy="18">goes here</tspan>
  </text>
  <text x="693" y="110" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" letter-spacing="6" fill="#FFFFFF">HEADING</text>
  <text x="665" y="129" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.92">
    <tspan x="665" dy="0">Some text goes here. Some</tspan><tspan x="673" dy="18">text goes here. Some text</tspan><tspan x="710" dy="18">goes here</tspan>
  </text>
  <text x="833" y="441" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" letter-spacing="6" fill="#FFFFFF">HEADING</text>
  <text x="810" y="462" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.92">
    <tspan x="810" dy="0">Some text goes here. Some</tspan><tspan x="816" dy="18">text goes here. Some text</tspan><tspan x="858" dy="18">goes here</tspan>
  </text>
  <text x="468" y="554" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" letter-spacing="6" fill="#FFFFFF">HEADING</text>
  <text x="440" y="575" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FFFFFF" opacity="0.92">
    <tspan x="440" dy="0">Some text goes here. Some</tspan><tspan x="446" dy="18">text goes here. Some text</tspan><tspan x="487" dy="18">goes here</tspan>
  </text>

  <rect x="246" y="265" width="49" height="10" rx="5" fill="url(#accentGrad)" transform="rotate(12 270 270)" filter="url(#nodeGlow)"/>
  <rect x="771" y="174" width="49" height="12" rx="6" fill="url(#accentGrad)" transform="rotate(-62 795 180)" filter="url(#nodeGlow)"/>
  <rect x="914" y="370" width="49" height="10" rx="5" fill="url(#accentGrad)" filter="url(#nodeGlow)"/>
  <rect x="594" y="598" width="49" height="11" rx="6" fill="url(#accentGrad)" transform="rotate(-78 618 603)" filter="url(#nodeGlow)"/>
  <circle cx="548" cy="109" r="9" fill="none" stroke="#22D3EE" stroke-width="7" opacity="0.9"/>
  <circle cx="245" cy="447" r="9" fill="none" stroke="#22D3EE" stroke-width="7" opacity="0.9"/>
  <circle cx="986" cy="235" r="14" fill="none" stroke="#22D3EE" stroke-width="12" opacity="0.9"/>
  <circle cx="795" cy="552" r="10" fill="none" stroke="#22D3EE" stroke-width="8" opacity="0.9"/>
  <path d="M453 166 L473 185 L445 191 Z" fill="url(#accentGrad)" opacity="0.95"/>
  <path d="M891 119 L906 139 L884 143 Z" fill="url(#accentGrad)" opacity="0.95"/>
  <path d="M949 534 L937 513 L962 516 Z" fill="url(#accentGrad)" opacity="0.95"/>
  <path d="M438 478 L450 497 L431 492 Z" fill="url(#accentGrad)" opacity="0.95"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to hide the inner halves of the glowing nodes; PPT translation may hard-fail. Use a same-color knockout shape layered above the nodes instead.
- ❌ Do not apply `clip-path` to circles, paths, or groups for the glass area; clipping is only reliable on `<image>` elements.
- ❌ Do not put `filter` on connector `<line>` elements; line filters are dropped. Keep glows on circles, paths, rects, ellipses, or text.
- ❌ Do not use `<use>` or `<symbol>` for repeated decorative accents; duplicate the editable primitives directly.
- ❌ Do not rely on true backdrop blur. Simulate frosted glass with translucent gradient fills, soft colored ellipses, semi-transparent strokes, and shadows.

## Composition notes
- Keep the glass hub centered and large enough to cover the inner thirds of all four nodes; this is what creates the “nodes behind glass” spatial illusion.
- Use a dark rounded card occupying roughly 75–80% of slide width, with generous margins so the glow and shadow feel premium rather than cramped.
- Place explanatory labels outside the hub in the four quadrants; keep body copy small, white, and low-density so the central glass object remains dominant.
- Repeat cyan/teal accents around the card to create rhythm, but vary scale and rotation so the futuristic decoration feels organic rather than like a grid.