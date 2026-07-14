# SVG Recipe — Bubble Bar Data Overlay

## Visual mechanism
Overlay a compact horizontal bar chart with size-encoded bubbles aligned to each row. Bars show absolute metrics such as revenue and profit, while the bubble column shows a ratio metric such as margin using both circle size and centered percentage labels.

## SVG primitives needed
- 1× full-slide `<rect>` for the executive-style background
- 1× large rounded `<rect>` for the chart card container
- 1× decorative `<path>` for a subtle background sweep behind the bubble zone
- 6× light rounded `<rect>` for total-value bars
- 6× dark rounded `<rect>` for component-value bars overlaid on the total bars
- 6× `<circle>` for size-encoded ratio bubbles
- 1× `<circle>` and 2× small `<rect>` for the legend
- 30+× `<text>` for title, subtitle, row labels, bar labels, bubble labels, and legend labels
- 4× `<linearGradient>` / `<radialGradient>` for background, bars, bubbles, and decorative depth
- 1× `<filter id="softShadow">` applied to the card and bubbles for premium depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="100%" stop-color="#EAF3FA"/>
    </linearGradient>
    <linearGradient id="revenueGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#CFE4F7"/>
      <stop offset="100%" stop-color="#9BC2E6"/>
    </linearGradient>
    <linearGradient id="profitGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1F5F9D"/>
      <stop offset="100%" stop-color="#2F75B5"/>
    </linearGradient>
    <radialGradient id="bubbleGrad" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#78D7F1"/>
      <stop offset="58%" stop-color="#4FB2DE"/>
      <stop offset="100%" stop-color="#238BB8"/>
    </radialGradient>
    <linearGradient id="sweepGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4FB2DE" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#2F75B5" stop-opacity="0.04"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05 0 0 0 0 0.13 0 0 0 0 0.22 0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M930,125 C1075,95 1190,165 1215,310 C1240,455 1155,595 990,620 C1075,505 1080,280 930,125 Z" fill="url(#sweepGrad)"/>
  <rect x="70" y="92" width="1140" height="560" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="100" y="63" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#18324A">Product performance: revenue, profit, margin</text>
  <text x="100" y="104" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#647789">Bubble size encodes profit margin; bars preserve absolute scale.</text>

  <rect x="240" y="128" width="16" height="16" rx="4" fill="url(#revenueGrad)"/>
  <text x="264" y="141" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#647789">Revenue</text>
  <rect x="365" y="128" width="16" height="16" rx="4" fill="url(#profitGrad)"/>
  <text x="389" y="141" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#647789">Profit</text>
  <circle cx="498" cy="136" r="9" fill="url(#bubbleGrad)"/>
  <text x="514" y="141" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#647789">Profit margin</text>

  <text x="100" y="160" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8A9BAD" letter-spacing="1">PRODUCT</text>
  <text x="240" y="160" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8A9BAD" letter-spacing="1">ABSOLUTE VALUE</text>
  <text x="970" y="160" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8A9BAD" text-anchor="middle" letter-spacing="1">MARGIN</text>

  <g transform="translate(0 0)">
    <text x="100" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263B50">Cloud Suite</text>
    <rect x="240" y="178" width="640" height="36" rx="18" fill="url(#revenueGrad)"/>
    <rect x="240" y="185" width="192" height="22" rx="11" fill="url(#profitGrad)"/>
    <text x="336" y="201" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">$360</text>
    <text x="895" y="201" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4D5D6C">$1,200</text>
    <circle cx="1010" cy="196" r="38" fill="url(#bubbleGrad)" filter="url(#softShadow)"/>
    <text x="1010" y="202" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">30%</text>
  </g>

  <g transform="translate(0 70)">
    <text x="100" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263B50">Security</text>
    <rect x="240" y="178" width="523" height="36" rx="18" fill="url(#revenueGrad)"/>
    <rect x="240" y="185" width="157" height="22" rx="11" fill="url(#profitGrad)"/>
    <text x="318" y="201" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">$294</text>
    <text x="778" y="201" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4D5D6C">$980</text>
    <circle cx="1010" cy="196" r="38" fill="url(#bubbleGrad)" filter="url(#softShadow)"/>
    <text x="1010" y="202" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">30%</text>
  </g>

  <g transform="translate(0 140)">
    <text x="100" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263B50">Analytics</text>
    <rect x="240" y="178" width="459" height="36" rx="18" fill="url(#revenueGrad)"/>
    <rect x="240" y="185" width="115" height="22" rx="11" fill="url(#profitGrad)"/>
    <text x="298" y="201" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">$215</text>
    <text x="714" y="201" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4D5D6C">$860</text>
    <circle cx="1010" cy="196" r="32" fill="url(#bubbleGrad)" filter="url(#softShadow)"/>
    <text x="1010" y="202" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">25%</text>
  </g>

  <g transform="translate(0 210)">
    <text x="100" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263B50">Payments</text>
    <rect x="240" y="178" width="384" height="36" rx="18" fill="url(#revenueGrad)"/>
    <rect x="240" y="185" width="134" height="22" rx="11" fill="url(#profitGrad)"/>
    <text x="307" y="201" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">$252</text>
    <text x="639" y="201" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4D5D6C">$720</text>
    <circle cx="1010" cy="196" r="44" fill="url(#bubbleGrad)" filter="url(#softShadow)"/>
    <text x="1010" y="202" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">35%</text>
  </g>

  <g transform="translate(0 280)">
    <text x="100" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263B50">IoT Platform</text>
    <rect x="240" y="178" width="299" height="36" rx="18" fill="url(#revenueGrad)"/>
    <rect x="240" y="185" width="51" height="22" rx="11" fill="url(#profitGrad)"/>
    <text x="266" y="201" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">$95</text>
    <text x="554" y="201" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4D5D6C">$560</text>
    <circle cx="1010" cy="196" r="24" fill="url(#bubbleGrad)" filter="url(#softShadow)"/>
    <text x="1010" y="202" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF" text-anchor="middle">17%</text>
  </g>

  <g transform="translate(0 350)">
    <text x="100" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263B50">Support</text>
    <rect x="240" y="178" width="224" height="36" rx="18" fill="url(#revenueGrad)"/>
    <rect x="240" y="185" width="67" height="22" rx="11" fill="url(#profitGrad)"/>
    <text x="274" y="201" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">$126</text>
    <text x="479" y="201" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4D5D6C">$420</text>
    <circle cx="1010" cy="196" r="38" fill="url(#bubbleGrad)" filter="url(#softShadow)"/>
    <text x="1010" y="202" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">30%</text>
  </g>

  <text x="100" y="622" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7C8C9B">Values in $K. Bubble radius is scaled by margin, not revenue.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build this as a native chart screenshot; draw bars, labels, and bubbles as editable SVG shapes.
- ❌ Do not add heavy axes or gridlines; the overlay works best when the bar lengths and bubbles are the visual anchors.
- ❌ Do not use `<marker-end>` arrows or callout arrows from paths; if annotation arrows are needed, use explicit `<line>` elements with arrow styling handled separately.
- ❌ Do not clip or mask bubbles; simple editable circles with gradient fill and shadow translate more reliably.
- ❌ Do not let bubble labels sit outside the circle unless the bubble is extremely small; centered percentage labels are the key decoding mechanism.

## Composition notes
- Reserve the left 15–18% of the slide for category labels, the center 50–55% for bars, and the right 15–20% for the bubble column.
- Keep all bubbles aligned on one vertical guide so the ratio metric reads as a separate but connected data layer.
- Use a low-contrast total bar and a saturated component bar; the bubble should use a distinct accent color so it does not compete with the bar hierarchy.
- Leave generous white space around the chart card and avoid dense numeric axes; executive audiences should read the pattern before the exact values.