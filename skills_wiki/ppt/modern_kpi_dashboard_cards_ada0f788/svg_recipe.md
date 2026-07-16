# SVG Recipe — Modern KPI Dashboard Cards

## Visual mechanism
A premium KPI dashboard is built from a row of tall, self-contained metric cards with alternating pale backgrounds, oversized numeric values, small contextual labels, and simple editable icon illustrations. Subtle accent stripes, soft shadows, and a small annotation note add executive polish while preserving the clean “chunked data” reading pattern.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 5× large rounded `<rect>` elements for KPI card containers
- 5× thin rounded `<rect>` elements for colored top accent bars
- 5× icon groups made from `<circle>`, `<rect>`, `<line>`, and `<path>` primitives for editable KPI symbols
- 15× `<text>` elements for title, subtitle, KPI values, labels, and deltas
- 1× rotated sticky-note `<rect>` plus supporting `<text>` and `<circle>` pin decoration
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to card rectangles
- 1× `<filter id="noteShadow">` applied to the sticky note
- 2× gradients: one background gradient and one radial pin gradient
- Several small decorative `<circle>` elements for subtle data-dot accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f3f5f8"/>
    </linearGradient>
    <radialGradient id="pinGrad" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#ff9a9a"/>
      <stop offset="100%" stop-color="#d72638"/>
    </radialGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="noteShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="90" cy="105" r="4" fill="#d72638" opacity="0.45"/>
  <circle cx="1135" cy="650" r="5" fill="#2d9cdb" opacity="0.25"/>
  <circle cx="1180" cy="615" r="3" fill="#d72638" opacity="0.3"/>

  <text x="70" y="66" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#252a31">
    Q3 Executive KPI Snapshot
  </text>
  <text x="72" y="102" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6b7280">
    Five operating indicators, normalized into a single-card dashboard for fast leadership review.
  </text>

  <g transform="rotate(4 1105 82)">
    <rect x="1012" y="38" width="178" height="96" rx="10" fill="#fff3b0" filter="url(#noteShadow)"/>
    <circle cx="1102" cy="38" r="10" fill="url(#pinGrad)"/>
    <text x="1032" y="74" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#5b4b00">Board readout</text>
    <text x="1032" y="99" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b5c12">Use icons as memory anchors.</text>
  </g>

  <g transform="translate(70 150)">
    <rect x="0" y="0" width="216" height="470" rx="24" fill="#ffffff" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="216" height="8" rx="4" fill="#d72638"/>
    <circle cx="88" cy="72" r="21" fill="#d72638"/>
    <circle cx="128" cy="72" r="21" fill="#32363f"/>
    <circle cx="108" cy="50" r="24" fill="#d72638"/>
    <path d="M52 137 C56 103 84 91 108 91 C132 91 160 103 164 137 Z" fill="#d72638"/>
    <path d="M34 144 C38 119 59 109 82 111 C68 120 62 131 61 144 Z" fill="#32363f"/>
    <path d="M155 144 C154 131 148 120 134 111 C157 109 178 119 182 144 Z" fill="#32363f"/>
    <text x="108" y="255" width="184" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#252a31">500</text>
    <text x="28" y="308" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#404040">New customers</text>
    <text x="28" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7a8089">per month</text>
    <text x="28" y="414" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0f9f6e">▲ 12% vs. plan</text>
  </g>

  <g transform="translate(300 150)">
    <rect x="0" y="0" width="216" height="470" rx="24" fill="#f5f6f8" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="216" height="8" rx="4" fill="#16a085"/>
    <path d="M48 84 H130 V135 H48 Z" fill="#32363f"/>
    <path d="M130 100 H163 L184 122 V135 H130 Z" fill="#16a085"/>
    <rect x="61" y="67" width="56" height="17" rx="4" fill="#16a085"/>
    <circle cx="76" cy="139" r="14" fill="#ffffff" stroke="#32363f" stroke-width="8"/>
    <circle cx="159" cy="139" r="14" fill="#ffffff" stroke="#32363f" stroke-width="8"/>
    <line x1="62" y1="116" x2="105" y2="116" stroke="#ffffff" stroke-width="5"/>
    <text x="108" y="255" width="184" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#252a31">95%</text>
    <text x="28" y="308" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#404040">On-time delivery</text>
    <text x="28" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7a8089">logistics SLA</text>
    <text x="28" y="414" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0f9f6e">▲ 4 pts QoQ</text>
  </g>

  <g transform="translate(530 150)">
    <rect x="0" y="0" width="216" height="470" rx="24" fill="#ffffff" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="216" height="8" rx="4" fill="#f2c94c"/>
    <path d="M72 140 H54 C47 140 42 135 42 128 V100 C42 93 47 88 54 88 H72 Z" fill="#32363f"/>
    <path d="M82 137 H142 C154 137 162 129 164 118 L171 86 C173 76 166 68 156 68 H128 L132 47 C134 36 125 28 116 34 L86 86 Z" fill="#f2c94c"/>
    <line x1="99" y1="94" x2="152" y2="94" stroke="#ffffff" stroke-width="5" opacity="0.8"/>
    <line x1="96" y1="113" x2="145" y2="113" stroke="#ffffff" stroke-width="5" opacity="0.8"/>
    <text x="108" y="255" width="184" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#252a31">90%</text>
    <text x="28" y="308" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#404040">Customer satisfaction</text>
    <text x="28" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7a8089">post-purchase CSAT</text>
    <text x="28" y="414" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#c47a00">● stable</text>
  </g>

  <g transform="translate(760 150)">
    <rect x="0" y="0" width="216" height="470" rx="24" fill="#f5f6f8" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="216" height="8" rx="4" fill="#34495e"/>
    <path d="M47 58 H169 L123 112 V146 L93 158 V112 Z" fill="#34495e"/>
    <path d="M66 76 H150 L134 95 H82 Z" fill="#ffffff" opacity="0.82"/>
    <circle cx="108" cy="58" r="18" fill="#d72638"/>
    <text x="108" y="255" width="184" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#252a31">30%</text>
    <text x="28" y="308" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#404040">Lead conversion</text>
    <text x="28" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7a8089">qualified to closed</text>
    <text x="28" y="414" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#d72638">▼ 2 pts target gap</text>
  </g>

  <g transform="translate(990 150)">
    <rect x="0" y="0" width="216" height="470" rx="24" fill="#ffffff" filter="url(#cardShadow)"/>
    <rect x="0" y="0" width="216" height="8" rx="4" fill="#d35400"/>
    <circle cx="108" cy="77" r="28" fill="#d35400"/>
    <path d="M61 153 C66 119 87 105 108 105 C129 105 150 119 155 153 Z" fill="#32363f"/>
    <path d="M152 70 C166 83 169 106 158 124" fill="none" stroke="#d35400" stroke-width="10" stroke-linecap="round"/>
    <path d="M158 124 L178 120 L165 104 Z" fill="#d35400"/>
    <path d="M64 112 C49 96 49 73 62 56" fill="none" stroke="#32363f" stroke-width="8" stroke-linecap="round"/>
    <path d="M62 56 L43 61 L56 75 Z" fill="#32363f"/>
    <text x="108" y="255" width="184" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800" fill="#252a31">80%</text>
    <text x="28" y="308" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#404040">Customer retention</text>
    <text x="28" y="336" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7a8089">rolling 12 months</text>
    <text x="28" y="414" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#0f9f6e">▲ 7% renewal lift</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Dense chart axes, gridlines, or micro-tables inside each card; they compete with the single KPI hierarchy.
- ❌ Using raster icon images when simple SVG paths can create fully editable native PowerPoint icons.
- ❌ Overly colorful card backgrounds; keep most cards white or very pale gray and reserve saturated color for accents.
- ❌ Applying shadows or filters to `<line>` elements; use filters on card `<rect>` elements only.
- ❌ Text without explicit `width` attributes, because PowerPoint text boxes may clip or wrap unpredictably.

## Composition notes
- Keep the card row as the dominant visual object, occupying roughly the middle 65–70% of the slide height.
- Use large numeric values centered vertically in each card; labels and trend notes should be secondary and aligned consistently.
- Alternate white and pale gray card fills to create separation without heavy borders.
- Reserve accent colors for top bars, icons, and delta indicators so the dashboard feels focused rather than noisy.