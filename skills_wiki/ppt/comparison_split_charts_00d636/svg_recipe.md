# SVG Recipe — Comparison Split Charts

## Visual mechanism
A premium two-up comparison slide: a strong editorial header anchors the page, a full-width horizontal rule separates narrative from analysis, and two equally weighted chart panels sit side-by-side under a subtle vertical split. Each chart has its own title, data story, and accent color so the audience can compare patterns without visual confusion.

## SVG primitives needed
- 1× full-canvas `<rect>` for the warm off-white background
- 2× blurred decorative `<path>` blobs for subtle executive-keynote depth behind the chart area
- 1× `<linearGradient>` for background accent blobs
- 2× rounded `<rect>` chart cards with soft shadow filters
- 1× full-width `<line>` or thin `<rect>` divider under the subtitle
- 1× vertical `<rect>` or `<line>` split divider between comparison panels
- Multiple `<text>` elements for headline, subtitle, panel titles, axis labels, data labels, and footer; every text element must include `width`
- Left chart: multiple `<rect>` bars, faint grid `<line>` elements, and small value callout labels
- Right chart: 1× filled `<path>` for the area under the line, 1× stroked `<path>` for the trend line, circles for data points, and labels
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` applied to chart cards
- 1× `<filter id="softGlow">` using `feGaussianBlur` applied to decorative paths only

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueBlob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D7E8FF"/>
      <stop offset="100%" stop-color="#F7FAFF"/>
    </linearGradient>
    <linearGradient id="amberBlob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE8B8"/>
      <stop offset="100%" stop-color="#FFF8EC"/>
    </linearGradient>
    <linearGradient id="areaFill" x1="0" y1="300" x2="0" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#F59E0B" stop-opacity="0.03"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8FAFC"/>
  <path d="M770 160 C910 90 1080 120 1145 240 C1210 360 1130 470 980 475 C840 480 720 405 700 295 C690 235 715 188 770 160 Z" fill="url(#blueBlob)" filter="url(#softGlow)" opacity="0.72"/>
  <path d="M92 500 C160 390 305 360 420 425 C535 490 540 630 410 675 C260 727 95 670 58 585 C45 552 58 525 92 500 Z" fill="url(#amberBlob)" filter="url(#softGlow)" opacity="0.62"/>

  <text x="72" y="76" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#0F172A">
    New Acquisition Channels Are Scaling Faster Than Legacy Spend
  </text>
  <text x="74" y="116" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#64748B">
    Side-by-side performance comparison across two growth models, normalized to indexed monthly output
  </text>
  <text x="1048" y="82" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2563EB" text-anchor="end">
    Q4 STRATEGY REVIEW
  </text>
  <rect x="72" y="150" width="1136" height="2" rx="1" fill="#CBD5E1"/>
  <rect x="72" y="151" width="312" height="2" rx="1" fill="#2563EB"/>

  <rect x="72" y="190" width="542" height="438" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="666" y="190" width="542" height="438" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="637" y="212" width="2" height="396" rx="1" fill="#DDE5EF"/>

  <text x="106" y="236" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#111827">
    Legacy paid media
  </text>
  <text x="106" y="262" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    Higher baseline, but rising cost pressure limits marginal gains
  </text>
  <rect x="478" y="221" width="96" height="28" rx="14" fill="#EFF6FF"/>
  <text x="526" y="240" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2563EB" text-anchor="middle">
    +12% YoY
  </text>

  <line x1="126" y1="548" x2="560" y2="548" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="126" y1="486" x2="560" y2="486" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="126" y1="424" x2="560" y2="424" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="126" y1="362" x2="560" y2="362" stroke="#E2E8F0" stroke-width="1"/>
  <text x="100" y="552" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">0</text>
  <text x="100" y="490" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">50</text>
  <text x="100" y="428" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">100</text>
  <text x="100" y="366" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8" text-anchor="end">150</text>

  <rect x="152" y="456" width="46" height="92" rx="8" fill="#BFDBFE"/>
  <rect x="224" y="428" width="46" height="120" rx="8" fill="#93C5FD"/>
  <rect x="296" y="394" width="46" height="154" rx="8" fill="#60A5FA"/>
  <rect x="368" y="374" width="46" height="174" rx="8" fill="#3B82F6"/>
  <rect x="440" y="352" width="46" height="196" rx="8" fill="#2563EB"/>
  <text x="175" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Jan</text>
  <text x="247" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Mar</text>
  <text x="319" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">May</text>
  <text x="391" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Jul</text>
  <text x="463" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Sep</text>
  <path d="M430 325 C470 302 516 304 548 334" fill="none" stroke="#2563EB" stroke-width="3" stroke-linecap="round"/>
  <text x="452" y="315" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1D4ED8">
    plateau risk
  </text>

  <text x="700" y="236" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#111827">
    Product-led referrals
  </text>
  <text x="700" y="262" width="405" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">
    Lower initial volume, but compounding behavior improves efficiency
  </text>
  <rect x="1072" y="221" width="96" height="28" rx="14" fill="#FFF7ED"/>
  <text x="1120" y="240" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#D97706" text-anchor="middle">
    +38% YoY
  </text>

  <line x1="720" y1="548" x2="1154" y2="548" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="720" y1="486" x2="1154" y2="486" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="720" y1="424" x2="1154" y2="424" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="720" y1="362" x2="1154" y2="362" stroke="#E2E8F0" stroke-width="1"/>
  <path d="M748 548 L748 510 C806 498 852 476 900 452 C946 429 990 395 1038 356 C1085 318 1126 286 1154 254 L1154 548 Z" fill="url(#areaFill)"/>
  <path d="M748 510 C806 498 852 476 900 452 C946 429 990 395 1038 356 C1085 318 1126 286 1154 254" fill="none" stroke="#F59E0B" stroke-width="4" stroke-linecap="round"/>
  <circle cx="748" cy="510" r="5" fill="#FFFFFF" stroke="#F59E0B" stroke-width="3"/>
  <circle cx="900" cy="452" r="5" fill="#FFFFFF" stroke="#F59E0B" stroke-width="3"/>
  <circle cx="1038" cy="356" r="5" fill="#FFFFFF" stroke="#F59E0B" stroke-width="3"/>
  <circle cx="1154" cy="254" r="6" fill="#F59E0B"/>
  <text x="748" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Jan</text>
  <text x="900" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">May</text>
  <text x="1038" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Sep</text>
  <text x="1154" y="574" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B" text-anchor="middle">Dec</text>
  <rect x="1012" y="300" width="118" height="38" rx="12" fill="#FFFBEB" stroke="#FCD34D"/>
  <text x="1071" y="324" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B45309" text-anchor="middle">
    compounding lift
  </text>

  <text x="72" y="672" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#94A3B8">
    Source: internal acquisition model; indexed output where Jan legacy baseline = 100
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using one shared chart color across both sides; the comparison needs distinct accent systems so the audience can track each story instantly.
- ❌ Overcrowding both charts with full axis tables, legends, and dense labels; this shell works best with one clear takeaway per side.
- ❌ Applying `filter` to grid `<line>` elements; shadows or glows on lines may be dropped, so keep filters on cards, paths, or text only.
- ❌ Using `marker-end` arrows on paths for callouts; if arrows are required, draw them as editable `<line>` elements with explicit endpoints or simple path chevrons.

## Composition notes
- Keep the header band to roughly the top 150 px; the horizontal divider creates a clean boundary between narrative and evidence.
- Use two equal-width cards with a narrow central split, leaving enough inner padding for axis labels and chart titles.
- Give each side its own accent color family, but keep gridlines, card backgrounds, and captions neutral for a consulting-style data-to-ink ratio.
- Place only one annotation per chart; callouts should explain the key contrast rather than label every data point.