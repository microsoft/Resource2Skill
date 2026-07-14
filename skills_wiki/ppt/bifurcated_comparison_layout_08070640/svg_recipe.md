# SVG Recipe — Two-Column Comparison Layout

## Visual mechanism
A symmetrical pair of premium “comparison cards” divides the slide into two equally weighted arguments, using contrasting header colors, iconography, and numbered evidence rows to make the opposition instantly readable. Subtle shadows, gradients, and a central divider add executive polish while preserving full editability in PowerPoint.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm white background
- 2× large rounded `<rect>` for the left and right comparison cards
- 2× rounded/header `<rect>` for strongly colored column headers
- 6× light rounded `<rect>` for individual list item rows
- 6× `<circle>` for numbered item badges
- 1× `<line>` for the center divider
- 10× `<path>` for decorative trend/risk icons and small glyph details
- 12× small `<rect>` for chart bars inside the header icons
- Multiple `<text>` elements with explicit `width=` for title, subtitle, headers, numbers, item titles, and item descriptions
- 2× `<linearGradient>` for premium header fills
- 1× `<filter id="cardShadow">` applied to the card rectangles
- 1× `<filter id="softGlow">` applied to header icon backplates

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3157D4"/>
      <stop offset="55%" stop-color="#4A69BD"/>
      <stop offset="100%" stop-color="#7EA2FF"/>
    </linearGradient>
    <linearGradient id="darkHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1F2937"/>
      <stop offset="65%" stop-color="#333333"/>
      <stop offset="100%" stop-color="#5B6472"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8FAFC"/>
  <path d="M0,92 C180,34 315,62 456,22 C622,-25 795,28 955,18 C1110,8 1198,36 1280,6 L1280,0 L0,0 Z" fill="#EEF3FF"/>
  <path d="M1030,650 C1100,610 1162,612 1280,570 L1280,720 L980,720 C992,690 1005,666 1030,650 Z" fill="#F1F5F9"/>

  <text x="88" y="74" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="700" fill="#111827">Strategic Decision Comparison</text>
  <text x="90" y="112" width="710" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#64748B">Evaluate upside potential and execution constraints side by side.</text>

  <line x1="640" y1="162" x2="640" y2="650" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="8 10"/>

  <rect x="78" y="154" width="540" height="492" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="662" y="154" width="540" height="492" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <rect x="78" y="154" width="540" height="116" rx="28" fill="url(#blueHeader)"/>
  <rect x="78" y="236" width="540" height="34" fill="url(#blueHeader)"/>
  <rect x="662" y="154" width="540" height="116" rx="28" fill="url(#darkHeader)"/>
  <rect x="662" y="236" width="540" height="34" fill="url(#darkHeader)"/>

  <circle cx="135" cy="211" r="36" fill="#FFFFFF" opacity="0.16" filter="url(#softGlow)"/>
  <rect x="114" y="214" width="8" height="18" rx="3" fill="#FFFFFF"/>
  <rect x="128" y="203" width="8" height="29" rx="3" fill="#FFFFFF"/>
  <rect x="142" y="192" width="8" height="40" rx="3" fill="#FFFFFF"/>
  <rect x="156" y="180" width="8" height="52" rx="3" fill="#FFFFFF"/>
  <path d="M112 195 L137 185 L154 169 L166 174" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="192" y="203" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Rewards</text>
  <text x="192" y="234" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DBEAFE">Value creation levers that strengthen the case</text>

  <circle cx="719" cy="211" r="36" fill="#FFFFFF" opacity="0.14" filter="url(#softGlow)"/>
  <path d="M719 176 L749 189 L744 219 C740 239 729 250 719 256 C709 250 698 239 694 219 L689 189 Z" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"/>
  <path d="M704 211 L716 223 L736 198" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="776" y="203" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Risks</text>
  <text x="776" y="234" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Constraints that may reduce certainty or speed</text>

  <rect x="112" y="306" width="472" height="86" rx="18" fill="#F6F8FC"/>
  <circle cx="145" cy="349" r="18" fill="#4A69BD"/>
  <text x="139" y="356" width="16" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">1</text>
  <text x="178" y="337" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F2937">Accelerated market entry</text>
  <text x="178" y="365" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Captures demand while competitors are still validating the opportunity.</text>

  <rect x="112" y="414" width="472" height="86" rx="18" fill="#F6F8FC"/>
  <circle cx="145" cy="457" r="18" fill="#4A69BD"/>
  <text x="139" y="464" width="16" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">2</text>
  <text x="178" y="445" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F2937">Higher customer lifetime value</text>
  <text x="178" y="473" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Bundled services increase retention and expand account penetration.</text>

  <rect x="112" y="522" width="472" height="86" rx="18" fill="#F6F8FC"/>
  <circle cx="145" cy="565" r="18" fill="#4A69BD"/>
  <text x="139" y="572" width="16" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">3</text>
  <text x="178" y="553" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F2937">Clear operational focus</text>
  <text x="178" y="581" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Creates a shared roadmap for product, sales, and delivery teams.</text>

  <rect x="696" y="306" width="472" height="86" rx="18" fill="#F6F8FC"/>
  <circle cx="729" cy="349" r="18" fill="#333333"/>
  <text x="723" y="356" width="16" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">1</text>
  <text x="762" y="337" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F2937">Execution complexity</text>
  <text x="762" y="365" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Requires cross-functional coordination across systems, process, and policy.</text>

  <rect x="696" y="414" width="472" height="86" rx="18" fill="#F6F8FC"/>
  <circle cx="729" cy="457" r="18" fill="#333333"/>
  <text x="723" y="464" width="16" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">2</text>
  <text x="762" y="445" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F2937">Near-term margin pressure</text>
  <text x="762" y="473" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Investment period may precede measurable revenue contribution.</text>

  <rect x="696" y="522" width="472" height="86" rx="18" fill="#F6F8FC"/>
  <circle cx="729" cy="565" r="18" fill="#333333"/>
  <text x="723" y="572" width="16" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">3</text>
  <text x="762" y="553" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1F2937">Adoption uncertainty</text>
  <text x="762" y="581" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#64748B">Customers may require education before the value proposition is obvious.</text>
</svg>
```

## Avoid in this skill
- ❌ Using one continuous bullet list; it removes the side-by-side comparison logic.
- ❌ Making one column visually larger than the other unless the intent is to bias the recommendation.
- ❌ Low-contrast header colors with white text; the headers must act as instant category labels.
- ❌ `marker-end` arrows for the trend icons; draw arrow-like paths directly instead.
- ❌ Text without explicit `width=` attributes, because PowerPoint rendering may clip or overflow.

## Composition notes
- Keep the two cards equal width and aligned to the same baseline; symmetry is the credibility signal.
- Reserve the top 15–18% of each card for bold colored headers and icons, then use stacked rows below.
- Use a generous central gutter or dashed divider so the viewer reads the two sides as separate but related.
- Color rhythm should be restrained: one strong positive color, one serious neutral/dark color, and light gray content surfaces.