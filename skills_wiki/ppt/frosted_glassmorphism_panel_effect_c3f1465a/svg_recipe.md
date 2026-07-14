# SVG Recipe — Frosted Glassmorphism Panel Effect

## Visual mechanism
Place a sharp, full-bleed hero image behind the slide, then duplicate the same image in the exact same position, clipped to rounded card shapes and heavily blurred to simulate frosted glass. Add a translucent tint, a subtle border highlight, and soft shadow so the panels feel like physical glass floating above the background.

## SVG primitives needed
- 1× full-slide `<image>` for the sharp photographic background.
- 3× duplicate `<image>` elements for the blurred background crops inside the glass panels.
- 3× `<clipPath>` with rounded `<rect>` for panel-shaped image crops.
- 1× `<filter id="panelBlur">` with `feGaussianBlur` applied to the clipped duplicate images.
- 1× `<filter id="softShadow">` with `feOffset + feGaussianBlur + feMerge` applied to panel shadow rectangles.
- 3× shadow `<rect>` behind the panels.
- 3× translucent tint `<rect>` over each blurred crop.
- 3× stroked rounded `<rect>` for glass-edge borders.
- Several small `<rect>`, `<circle>`, and `<path>` elements for premium KPI/chart decoration inside the panels.
- Multiple `<linearGradient>` and `<radialGradient>` fills for glass shine, background darkening, and accent glows.
- Multiple editable `<text>` elements with explicit `width` attributes for headings, labels, and metrics.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="panelBlur" x="-8%" y="-8%" width="116%" height="116%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="slideShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F" stop-opacity="0.20"/>
      <stop offset="55%" stop-color="#07111F" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#07111F" stop-opacity="0.38"/>
    </linearGradient>

    <linearGradient id="glassTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#B8D8FF" stop-opacity="0.18"/>
    </linearGradient>

    <linearGradient id="edgeStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#7CC7FF" stop-opacity="0.38"/>
    </linearGradient>

    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#50E6FF" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#50E6FF" stop-opacity="0"/>
    </radialGradient>

    <clipPath id="clipCard1">
      <rect x="116" y="184" width="300" height="378" rx="34"/>
    </clipPath>
    <clipPath id="clipCard2">
      <rect x="490" y="140" width="300" height="442" rx="34"/>
    </clipPath>
    <clipPath id="clipCard3">
      <rect x="864" y="184" width="300" height="378" rx="34"/>
    </clipPath>
  </defs>

  <image href="https://images.example.com/hero-background-futuristic-city-office-data-dashboard.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#slideShade)"/>

  <circle cx="1115" cy="120" r="145" fill="url(#cyanGlow)"/>
  <circle cx="150" cy="620" r="190" fill="#7C3AED" opacity="0.16"/>
  <path d="M860 650 C960 590, 1070 620, 1185 545" fill="none" stroke="#9DEBFF" stroke-width="2" opacity="0.32"/>

  <text x="94" y="88" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#FFFFFF" opacity="0.82">
    GLASSMORPHISM ANALYTICS
  </text>
  <text x="92" y="136" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">
    Frosted panels over a live visual context
  </text>
  <text x="94" y="174" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#E8F5FF" opacity="0.80">
    Blur the background locally, keep the atmosphere globally.
  </text>

  <rect x="116" y="184" width="300" height="378" rx="34" fill="#07111F" opacity="0.24" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-background-futuristic-city-office-data-dashboard.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipCard1)" filter="url(#panelBlur)"/>
  <rect x="116" y="184" width="300" height="378" rx="34" fill="url(#glassTint)"/>
  <rect x="132" y="200" width="268" height="96" rx="24" fill="url(#shine)" opacity="0.48"/>
  <rect x="116" y="184" width="300" height="378" rx="34" fill="none" stroke="url(#edgeStroke)" stroke-width="1.4"/>
  <text x="146" y="244" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" opacity="0.76">SIGNAL QUALITY</text>
  <text x="146" y="314" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700" fill="#FFFFFF">97%</text>
  <text x="148" y="348" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#EAF8FF" opacity="0.82">clean data capture</text>
  <path d="M148 466 C182 418, 214 450, 246 406 C278 362, 318 394, 384 332" fill="none" stroke="#55E6FF" stroke-width="4" stroke-linecap="round"/>
  <circle cx="384" cy="332" r="7" fill="#FFFFFF"/>
  <rect x="148" y="500" width="70" height="8" rx="4" fill="#FFFFFF" opacity="0.72"/>
  <rect x="228" y="500" width="130" height="8" rx="4" fill="#FFFFFF" opacity="0.28"/>

  <rect x="490" y="140" width="300" height="442" rx="34" fill="#07111F" opacity="0.27" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-background-futuristic-city-office-data-dashboard.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipCard2)" filter="url(#panelBlur)"/>
  <rect x="490" y="140" width="300" height="442" rx="34" fill="url(#glassTint)"/>
  <rect x="506" y="156" width="268" height="118" rx="24" fill="url(#shine)" opacity="0.50"/>
  <rect x="490" y="140" width="300" height="442" rx="34" fill="none" stroke="url(#edgeStroke)" stroke-width="1.4"/>
  <text x="520" y="202" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" opacity="0.76">REVENUE MOMENTUM</text>
  <text x="520" y="278" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="700" fill="#FFFFFF">+37%</text>
  <text x="522" y="314" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#EAF8FF" opacity="0.84">quarter-over-quarter</text>
  <rect x="526" y="404" width="28" height="96" rx="10" fill="#FFFFFF" opacity="0.30"/>
  <rect x="568" y="356" width="28" height="144" rx="10" fill="#FFFFFF" opacity="0.46"/>
  <rect x="610" y="382" width="28" height="118" rx="10" fill="#FFFFFF" opacity="0.35"/>
  <rect x="652" y="318" width="28" height="182" rx="10" fill="#55E6FF" opacity="0.72"/>
  <rect x="694" y="284" width="28" height="216" rx="10" fill="#FFFFFF" opacity="0.68"/>
  <text x="520" y="540" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" opacity="0.76">blur + tint preserves contrast</text>

  <rect x="864" y="184" width="300" height="378" rx="34" fill="#07111F" opacity="0.24" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-background-futuristic-city-office-data-dashboard.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#clipCard3)" filter="url(#panelBlur)"/>
  <rect x="864" y="184" width="300" height="378" rx="34" fill="url(#glassTint)"/>
  <rect x="880" y="200" width="268" height="96" rx="24" fill="url(#shine)" opacity="0.48"/>
  <rect x="864" y="184" width="300" height="378" rx="34" fill="none" stroke="url(#edgeStroke)" stroke-width="1.4"/>
  <text x="894" y="244" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" opacity="0.76">DECISION LATENCY</text>
  <text x="894" y="314" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700" fill="#FFFFFF">1.8s</text>
  <text x="896" y="348" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#EAF8FF" opacity="0.82">average response time</text>
  <circle cx="1014" cy="438" r="56" fill="none" stroke="#FFFFFF" stroke-width="18" opacity="0.24"/>
  <path d="M1014 382 A56 56 0 1 1 970 472" fill="none" stroke="#55E6FF" stroke-width="18" stroke-linecap="round"/>
  <text x="962" y="448" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF" text-anchor="middle">84</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; it will not translate reliably to editable PowerPoint.
- ❌ Do not apply `clip-path` to `<rect>` or other shapes; for this workflow, clipping is only reliable on `<image>`.
- ❌ Do not use `<mask>` to create glass softness or transparency gradients; masks can hard-fail the slide.
- ❌ Do not rely on a flat semi-transparent rectangle alone; without the blurred duplicate image, the effect reads as dated overlay rather than frosted glass.
- ❌ Do not put filters on `<line>` elements; use `<path>` for glowing chart strokes instead.

## Composition notes
- Keep glass panels floating with generous outer margins; the sharp background must remain visible around them to sell the “glass over environment” illusion.
- Duplicate background images must use the exact same `x`, `y`, `width`, `height`, and `preserveAspectRatio` as the main background so the blurred crop aligns perfectly.
- Use a three-layer card stack: shadow rectangle behind, blurred clipped image in the middle, translucent tint and border on top.
- White text works best over darker or medium-toned hero imagery; if using a very bright background, switch the tint to darker navy and keep the glass border light.