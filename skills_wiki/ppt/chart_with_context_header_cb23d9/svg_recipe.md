# SVG Recipe — Chart with Context Header

## Visual mechanism
A strong editorial header creates the business context before the viewer enters a large, disciplined chart field. The slide uses a top title/subtitle/meta band, then a premium chart card with gridlines, highlighted trend, annotations, and a compact source footer.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<linearGradient>` for the slide background wash and chart area fill
- 1× `<filter id="cardShadow">` for the main chart card depth
- 1× `<filter id="softGlow">` applied to the highlighted trend path
- 1× large rounded `<rect>` for the chart card
- 3× small rounded `<rect>` metadata chips in the header
- Multiple `<line>` elements for chart gridlines, axes, and leader lines
- Multiple `<rect>` elements for vertical bars and the forecast region
- 2× `<path>` elements for the area fill and the main trend line
- Multiple `<circle>` elements for data points
- Multiple `<text>` elements with explicit `width` attributes for headline, subtitle, metadata, labels, callouts, and footer
- Optional dashed `<line>` elements for targets or forecast boundaries

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="58%" stop-color="#EEF4F8"/>
      <stop offset="100%" stop-color="#E8F0F6"/>
    </linearGradient>
    <linearGradient id="cardFill" x1="0" y1="150" x2="0" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FBFD"/>
    </linearGradient>
    <linearGradient id="areaBlue" x1="0" y1="250" x2="0" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1F77B4" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#1F77B4" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="72" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#15202B">
    Revenue mix is shifting faster than expected
  </text>
  <text x="74" y="93" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5C6B78">
    Enterprise subscriptions now account for most incremental growth despite slower SMB acquisition.
  </text>

  <rect x="922" y="38" width="94" height="30" rx="15" fill="#E7F1FB" stroke="#B9D7F1"/>
  <text x="946" y="59" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#1F5E93">Q4 FY25</text>
  <rect x="1028" y="38" width="90" height="30" rx="15" fill="#EEF7EF" stroke="#C9E5CE"/>
  <text x="1050" y="59" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#2D7A3E">Actuals</text>
  <rect x="1130" y="38" width="78" height="30" rx="15" fill="#FFF4DF" stroke="#F2D7A3"/>
  <text x="1151" y="59" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#9A6517">USD m</text>

  <line x1="72" y1="122" x2="1208" y2="122" stroke="#D9E2EA" stroke-width="1"/>

  <rect x="72" y="154" width="1136" height="478" rx="24" fill="url(#cardFill)" filter="url(#cardShadow)"/>
  <text x="104" y="197" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#1B2A38">
    Quarterly recurring revenue by segment
  </text>
  <text x="104" y="222" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8793">
    Bars show total recurring revenue; line shows enterprise share of incremental ARR.
  </text>

  <rect x="940" y="180" width="12" height="12" rx="2" fill="#9FC7E6"/>
  <text x="960" y="191" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#546371">Core ARR</text>
  <rect x="1046" y="180" width="12" height="12" rx="2" fill="#2F80ED"/>
  <text x="1066" y="191" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#546371">Enterprise mix</text>

  <line x1="142" y1="560" x2="1124" y2="560" stroke="#9AA8B5" stroke-width="1.2"/>
  <line x1="142" y1="476" x2="1124" y2="476" stroke="#E4EAF0" stroke-width="1"/>
  <line x1="142" y1="392" x2="1124" y2="392" stroke="#E4EAF0" stroke-width="1"/>
  <line x1="142" y1="308" x2="1124" y2="308" stroke="#E4EAF0" stroke-width="1"/>
  <line x1="142" y1="224" x2="1124" y2="224" stroke="#E4EAF0" stroke-width="1"/>
  <line x1="142" y1="280" x2="1124" y2="280" stroke="#F0A33A" stroke-width="1.4" stroke-dasharray="6 7"/>

  <text x="104" y="565" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7A8793">$0</text>
  <text x="98" y="481" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7A8793">$50</text>
  <text x="92" y="397" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7A8793">$100</text>
  <text x="92" y="313" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7A8793">$150</text>
  <text x="92" y="229" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7A8793">$200</text>

  <rect x="198" y="426" width="48" height="134" rx="6" fill="#BBD9EF"/>
  <rect x="316" y="404" width="48" height="156" rx="6" fill="#BBD9EF"/>
  <rect x="434" y="372" width="48" height="188" rx="6" fill="#BBD9EF"/>
  <rect x="552" y="342" width="48" height="218" rx="6" fill="#BBD9EF"/>
  <rect x="670" y="310" width="48" height="250" rx="6" fill="#BBD9EF"/>
  <rect x="788" y="270" width="48" height="290" rx="6" fill="#BBD9EF"/>
  <rect x="906" y="240" width="48" height="320" rx="6" fill="#BBD9EF"/>
  <rect x="1024" y="214" width="48" height="346" rx="6" fill="#BBD9EF"/>

  <rect x="984" y="224" width="140" height="336" fill="#F6EBD7" opacity="0.55"/>
  <line x1="984" y1="224" x2="984" y2="560" stroke="#D9A64E" stroke-width="1.4" stroke-dasharray="5 6"/>
  <text x="996" y="248" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#9A6517">Forecast window</text>

  <path d="M222 474 L340 442 L458 410 L576 370 L694 328 L812 292 L930 258 L1048 232 L1048 560 L222 560 Z" fill="url(#areaBlue)"/>
  <path d="M222 474 C278 454, 302 458, 340 442 C398 415, 414 428, 458 410 C518 385, 536 394, 576 370 C642 330, 652 348, 694 328 C754 294, 768 314, 812 292 C876 256, 890 274, 930 258 C990 230, 1008 244, 1048 232" fill="none" stroke="#2F80ED" stroke-width="4.5" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M222 474 C278 454, 302 458, 340 442 C398 415, 414 428, 458 410 C518 385, 536 394, 576 370 C642 330, 652 348, 694 328 C754 294, 768 314, 812 292 C876 256, 890 274, 930 258 C990 230, 1008 244, 1048 232" fill="none" stroke="#2F80ED" stroke-width="3" stroke-linecap="round"/>

  <circle cx="222" cy="474" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="340" cy="442" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="458" cy="410" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="576" cy="370" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="694" cy="328" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="812" cy="292" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="930" cy="258" r="5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="1048" cy="232" r="6" fill="#2F80ED" stroke="#FFFFFF" stroke-width="3"/>

  <text x="203" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q1'24</text>
  <text x="321" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q2'24</text>
  <text x="439" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q3'24</text>
  <text x="557" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q4'24</text>
  <text x="675" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q1'25</text>
  <text x="793" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q2'25</text>
  <text x="911" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q3'25</text>
  <text x="1029" y="590" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7A86">Q4'25</text>

  <line x1="875" y1="250" x2="792" y2="220" stroke="#8FA1B2" stroke-width="1.2"/>
  <rect x="642" y="190" width="146" height="46" rx="12" fill="#FFFFFF" stroke="#D9E2EA"/>
  <text x="660" y="210" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B2A38">Mix inflection</text>
  <text x="660" y="227" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#6D7A86">Enterprise +9 pts YoY</text>

  <text x="72" y="676" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7A8793">
    Source: Finance data mart, booked ARR only; excludes professional services and one-time implementation fees.
  </text>
  <text x="1068" y="676" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="11" text-anchor="end" fill="#7A8793">
    Confidential draft
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not let the chart compete with the header; avoid oversized legends or decorative shapes in the title band.
- ❌ Do not use `<foreignObject>` for tables or labels; build labels with native `<text>` so they remain editable.
- ❌ Do not apply filters to grid `<line>` elements; shadows and glows should be on cards, paths, or text only.
- ❌ Do not use `marker-end` for arrows in annotations; use simple leader lines or hand-drawn arrowheads with `<path>` if needed.
- ❌ Do not omit `width` on any `<text>` element, especially axis labels and footer notes.

## Composition notes
- Reserve the top 120–140 px for the contextual header: headline on the left, compact metadata chips on the right.
- Give the chart a dominant 70%+ slide footprint, preferably inside a softly elevated rounded card.
- Use restrained color rhythm: neutral grid and labels, one muted series color, and one vivid accent for the key trend.
- Keep footer/source text outside the chart card to preserve analytical credibility without cluttering the visualization.