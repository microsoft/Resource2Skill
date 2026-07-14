# SVG Recipe — Modern KPI Card Dashboard

## Visual mechanism
A premium KPI dashboard is built from a disciplined grid of floating rounded cards, each containing one metric, a small trend signal, and a compact native SVG mini-chart. The depth comes from soft shadows and subtle gradients, while scanability comes from consistent padding, strong typography, and color-coded performance states.

## SVG primitives needed
- 1× `<rect>` for the slide background, plus several blurred decorative background blobs.
- 6× large rounded `<rect>` for KPI card containers with shadow filters.
- 6× small rounded `<rect>` for status pills, date chips, and compact labels.
- 6× `<circle>` / `<ellipse>` groups for icon badges, ring gauges, donut charts, and chart centers.
- Multiple `<path>` elements for sparkline charts, filled sparkline areas, donut wedges/arc strokes, trend arrows, and simple finance icons.
- Multiple `<text>` elements with explicit `width` attributes for slide title, card titles, KPI values, deltas, labels, and annotations.
- 1× `<filter id="cardShadow">` for card depth.
- 1× `<filter id="softGlow">` for atmospheric background glow.
- Multiple `<linearGradient>` and `<radialGradient>` definitions for premium card accents, KPI fills, sparkline areas, and background depth.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF4FF"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4F8CFF"/>
      <stop offset="100%" stop-color="#245BDB"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#37C98B"/>
      <stop offset="100%" stop-color="#159A68"/>
    </linearGradient>
    <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF7A7A"/>
      <stop offset="100%" stop-color="#E23B4B"/>
    </linearGradient>
    <linearGradient id="amberGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFC857"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>
    <linearGradient id="sparkBlue" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4F8CFF" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#4F8CFF" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="sparkGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2EB378" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#2EB378" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1030" cy="72" r="130" fill="#DCEBFF" filter="url(#softGlow)" opacity="0.65"/>
  <path d="M58,640 C170,565 275,650 388,590 C480,542 545,600 630,552 L630,720 L58,720 Z" fill="#E9F8F1" filter="url(#softGlow)" opacity="0.55"/>

  <text x="54" y="62" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">Chief Financial Officers KPI Dashboard</text>
  <text x="56" y="96" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">Q4 executive finance pulse · consolidated operating metrics</text>
  <rect x="1015" y="48" width="210" height="38" rx="19" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="1040" y="73" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#374151">Updated · Dec 2026</text>

  <!-- Card 1 -->
  <rect x="54" y="140" width="374" height="210" rx="22" fill="#FFFFFF" stroke="#E8EDF5" filter="url(#cardShadow)"/>
  <rect x="54" y="140" width="374" height="6" rx="3" fill="url(#greenGrad)"/>
  <circle cx="92" cy="184" r="20" fill="#E9F8F1"/>
  <path d="M82,190 L89,183 L96,187 L105,174" fill="none" stroke="#159A68" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="124" y="180" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">Net Revenue</text>
  <text x="74" y="244" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111827">$42.8M</text>
  <rect x="76" y="266" width="96" height="28" rx="14" fill="#E9F8F1"/>
  <text x="94" y="285" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#159A68">▲ 12.4%</text>
  <path d="M232,310 C250,272 272,292 292,254 C309,222 338,238 358,204" fill="none" stroke="#2EB378" stroke-width="5" stroke-linecap="round"/>
  <path d="M232,310 C250,272 272,292 292,254 C309,222 338,238 358,204 L358,322 L232,322 Z" fill="url(#sparkGreen)"/>

  <!-- Card 2 -->
  <rect x="453" y="140" width="374" height="210" rx="22" fill="#FFFFFF" stroke="#E8EDF5" filter="url(#cardShadow)"/>
  <rect x="453" y="140" width="374" height="6" rx="3" fill="url(#blueGrad)"/>
  <circle cx="491" cy="184" r="20" fill="#ECF3FF"/>
  <path d="M482,192 L482,178 L489,178 L489,192 M495,192 L495,171 L502,171 L502,192" fill="none" stroke="#245BDB" stroke-width="4" stroke-linecap="round"/>
  <text x="523" y="180" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">EBITDA Margin</text>
  <text x="474" y="244" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111827">28.6%</text>
  <text x="475" y="286" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Target: 25.0%</text>
  <circle cx="724" cy="245" r="54" fill="none" stroke="#EEF2F7" stroke-width="14"/>
  <circle cx="724" cy="245" r="54" fill="none" stroke="url(#blueGrad)" stroke-width="14" stroke-linecap="round" stroke-dasharray="308 340" transform="rotate(-90 724 245)"/>
  <text x="696" y="253" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#245BDB">89%</text>

  <!-- Card 3 -->
  <rect x="852" y="140" width="374" height="210" rx="22" fill="#FFFFFF" stroke="#E8EDF5" filter="url(#cardShadow)"/>
  <rect x="852" y="140" width="374" height="6" rx="3" fill="url(#amberGrad)"/>
  <circle cx="890" cy="184" r="20" fill="#FFF7E6"/>
  <path d="M880,184 C880,176 887,171 895,174 C902,177 904,184 899,190 C895,196 885,197 880,190" fill="none" stroke="#D97706" stroke-width="4" stroke-linecap="round"/>
  <text x="922" y="180" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">Cash Runway</text>
  <text x="873" y="244" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111827">18.2</text>
  <text x="1000" y="244" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#6B7280">months</text>
  <rect x="874" y="269" width="250" height="12" rx="6" fill="#EEF2F7"/>
  <rect x="874" y="269" width="202" height="12" rx="6" fill="url(#amberGrad)"/>
  <text x="874" y="307" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Liquidity coverage strong</text>

  <!-- Card 4 -->
  <rect x="54" y="385" width="374" height="210" rx="22" fill="#FFFFFF" stroke="#E8EDF5" filter="url(#cardShadow)"/>
  <rect x="54" y="385" width="374" height="6" rx="3" fill="url(#redGrad)"/>
  <circle cx="92" cy="429" r="20" fill="#FFF0F1"/>
  <path d="M82,424 L92,434 L104,418" fill="none" stroke="#E23B4B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="124" y="425" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">Accounts Payable Days</text>
  <text x="74" y="489" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111827">47</text>
  <rect x="76" y="512" width="104" height="28" rx="14" fill="#FFF0F1"/>
  <text x="94" y="531" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E23B4B">▲ +6 days</text>
  <path d="M230,550 C250,520 268,532 289,496 C310,462 335,475 360,430" fill="none" stroke="#E23B4B" stroke-width="5" stroke-linecap="round"/>
  <line x1="230" y1="558" x2="360" y2="558" stroke="#E5E7EB" stroke-width="2" stroke-dasharray="5 7"/>

  <!-- Card 5 -->
  <rect x="453" y="385" width="374" height="210" rx="22" fill="#FFFFFF" stroke="#E8EDF5" filter="url(#cardShadow)"/>
  <rect x="453" y="385" width="374" height="6" rx="3" fill="#7C3AED"/>
  <circle cx="491" cy="429" r="20" fill="#F3E8FF"/>
  <path d="M481,429 C486,418 497,418 502,429 C497,440 486,440 481,429 Z" fill="none" stroke="#7C3AED" stroke-width="4"/>
  <text x="523" y="425" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">Working Capital Mix</text>
  <circle cx="570" cy="504" r="60" fill="none" stroke="#EEF2F7" stroke-width="24"/>
  <circle cx="570" cy="504" r="60" fill="none" stroke="#4F8CFF" stroke-width="24" stroke-dasharray="151 377" transform="rotate(-90 570 504)"/>
  <circle cx="570" cy="504" r="60" fill="none" stroke="#2EB378" stroke-width="24" stroke-dasharray="113 377" stroke-dashoffset="-151" transform="rotate(-90 570 504)"/>
  <circle cx="570" cy="504" r="60" fill="none" stroke="#FFC857" stroke-width="24" stroke-dasharray="75 377" stroke-dashoffset="-264" transform="rotate(-90 570 504)"/>
  <circle cx="570" cy="504" r="34" fill="#FFFFFF"/>
  <text x="546" y="512" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#111827">100%</text>
  <rect x="668" y="466" width="12" height="12" rx="3" fill="#4F8CFF"/>
  <text x="688" y="477" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Receivables</text>
  <rect x="668" y="496" width="12" height="12" rx="3" fill="#2EB378"/>
  <text x="688" y="507" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Inventory</text>
  <rect x="668" y="526" width="12" height="12" rx="3" fill="#FFC857"/>
  <text x="688" y="537" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Payables</text>

  <!-- Card 6 -->
  <rect x="852" y="385" width="374" height="210" rx="22" fill="#FFFFFF" stroke="#E8EDF5" filter="url(#cardShadow)"/>
  <rect x="852" y="385" width="374" height="6" rx="3" fill="url(#greenGrad)"/>
  <circle cx="890" cy="429" r="20" fill="#E9F8F1"/>
  <path d="M880,431 L887,438 L902,418" fill="none" stroke="#159A68" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="922" y="425" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">Forecast Accuracy</text>
  <text x="873" y="489" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#111827">94.1%</text>
  <text x="874" y="530" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6B7280">Rolling 90-day model</text>
  <path d="M1040,548 L1062,522 L1085,531 L1107,493 L1130,508 L1158,458" fill="none" stroke="#111827" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1040,548 L1062,522 L1085,531 L1107,493 L1130,508 L1158,458 L1158,564 L1040,564 Z" fill="url(#sparkGreen)"/>
  <circle cx="1158" cy="458" r="6" fill="#2EB378"/>
</svg>
```

## Avoid in this skill
- ❌ Overusing default PowerPoint chart objects; the premium look comes from custom SVG mini-charts, gauges, arcs, and sparklines.
- ❌ Cards with heavy borders and no shadow; the technique depends on a light floating-card hierarchy.
- ❌ Inconsistent gutters or uneven internal padding; dashboards quickly look amateur when alignment drifts.
- ❌ Tiny dense tables inside cards; reserve each card for one primary metric plus one compact supporting signal.
- ❌ Applying filters to `<line>` elements; use filters on cards, paths, circles, or text instead.

## Composition notes
- Use a strict 3-column × 2-row card grid, with generous outer margins and consistent gutters so the dashboard feels executive rather than crowded.
- Keep every card’s hierarchy consistent: small title at top, oversized KPI value, then trend pill or mini-chart.
- Use color rhythm deliberately: green for positive, red for risk, amber for caution, blue/purple for neutral categorical information.
- Leave the top header clean and airy; the visual focus should land on the six floating KPI modules, not on decorative elements.