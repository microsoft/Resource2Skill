# SVG Recipe — Structured Data Clarity Formula

## Visual mechanism
A premium table is built by removing the grid cage and using alignment, whitespace, restrained color, and light horizontal rules as the real structure. A single header band, one highlighted row, right-aligned numbers, and subtle status pills guide attention without overwhelming the data.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 1× `<rect>` for the elevated table card container
- 1× `<rect>` with gradient fill for the header band
- 2–3× `<rect>` for very light zebra row washes and one strategic highlight row
- 6–8× `<line>` for horizontal dividers only, avoiding vertical grid lines
- 25–40× `<text>` for title, subtitle, headers, body cells, numeric values, and footnotes
- 6× `<rect>` for compact rounded status pills
- 6× `<path>` for small status glyphs inside pills
- 1× `<linearGradient>` for the executive-style header band
- 1× `<filter id="softShadow">` applied to the table card
- 1× `<filter id="softGlow">` applied to the highlighted insight label or row accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#EEF4F8"/>
    </linearGradient>
    <linearGradient id="headerBlue" x1="100" y1="160" x2="1180" y2="160" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#005B89"/>
      <stop offset="60%" stop-color="#0070C0"/>
      <stop offset="100%" stop-color="#0E9ED5"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="88" y="72" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#263238">
    Portfolio Operating Review
  </text>
  <text x="90" y="108" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#60717B">
    Subtractive table design: no vertical grid, right-aligned numbers, one purposeful highlight.
  </text>

  <rect x="80" y="136" width="1120" height="500" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="100" y="160" width="1080" height="58" rx="14" fill="url(#headerBlue)"/>
  <rect x="100" y="204" width="1080" height="14" fill="url(#headerBlue)"/>

  <rect x="100" y="346" width="1080" height="64" fill="#F8FBFD"/>
  <rect x="100" y="474" width="1080" height="64" fill="#F8FBFD"/>
  <rect x="100" y="410" width="1080" height="64" fill="#DCEAF7"/>
  <rect x="100" y="410" width="6" height="64" fill="#0070C0"/>

  <line x1="100" y1="218" x2="1180" y2="218" stroke="#D6E0E6" stroke-width="1.4"/>
  <line x1="100" y1="282" x2="1180" y2="282" stroke="#D6E0E6" stroke-width="1"/>
  <line x1="100" y1="346" x2="1180" y2="346" stroke="#D6E0E6" stroke-width="1"/>
  <line x1="100" y1="410" x2="1180" y2="410" stroke="#B7CDDF" stroke-width="1.4"/>
  <line x1="100" y1="474" x2="1180" y2="474" stroke="#B7CDDF" stroke-width="1.4"/>
  <line x1="100" y1="538" x2="1180" y2="538" stroke="#D6E0E6" stroke-width="1"/>
  <line x1="100" y1="602" x2="1180" y2="602" stroke="#D6E0E6" stroke-width="1"/>

  <text x="122" y="197" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Business Unit</text>
  <text x="380" y="197" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Owner</text>
  <text x="690" y="197" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Revenue</text>
  <text x="860" y="197" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Margin</text>
  <text x="1012" y="197" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">Status</text>

  <text x="122" y="257" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2F3B43">Urban Retail</text>
  <text x="380" y="257" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#4A5963">L. Chen</text>
  <text x="690" y="257" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#263238">$42.8M</text>
  <text x="860" y="257" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#263238">31.4%</text>
  <rect x="1010" y="236" width="104" height="28" rx="14" fill="#E6F4EC"/>
  <path d="M1028 249 l7 7 l14 -15" fill="none" stroke="#168A4A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1054" y="256" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#168A4A">ON PLAN</text>

  <text x="122" y="321" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2F3B43">Office Leasing</text>
  <text x="380" y="321" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#4A5963">A. Rivera</text>
  <text x="690" y="321" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#263238">$37.2M</text>
  <text x="860" y="321" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#263238">28.1%</text>
  <rect x="1010" y="300" width="104" height="28" rx="14" fill="#FFF3D6"/>
  <path d="M1036 306 l14 22 h-28 z" fill="#D58700"/>
  <text x="1054" y="320" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#9A6500">WATCH</text>

  <text x="122" y="385" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2F3B43">Mixed-use Assets</text>
  <text x="380" y="385" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#4A5963">M. Park</text>
  <text x="690" y="385" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#263238">$55.6M</text>
  <text x="860" y="385" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#263238">34.8%</text>
  <rect x="1010" y="364" width="104" height="28" rx="14" fill="#E6F4EC"/>
  <path d="M1028 377 l7 7 l14 -15" fill="none" stroke="#168A4A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1054" y="384" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#168A4A">ON PLAN</text>

  <text x="122" y="449" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#0A4D78">Premium Residences</text>
  <text x="380" y="449" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#0A4D78">S. Morgan</text>
  <text x="690" y="449" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#0A4D78">$68.9M</text>
  <text x="860" y="449" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#0A4D78">39.6%</text>
  <rect x="1010" y="428" width="104" height="28" rx="14" fill="#D7EBFF"/>
  <path d="M1024 442 c8 -12 20 -12 28 0 c-8 12 -20 12 -28 0 z" fill="#0070C0"/>
  <circle cx="1038" cy="442" r="4" fill="#FFFFFF"/>
  <text x="1054" y="448" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#0067A8">FOCUS</text>

  <text x="122" y="513" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2F3B43">Hospitality</text>
  <text x="380" y="513" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#4A5963">N. Gupta</text>
  <text x="690" y="513" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#263238">$24.7M</text>
  <text x="860" y="513" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#263238">22.0%</text>
  <rect x="1010" y="492" width="104" height="28" rx="14" fill="#FBE7E8"/>
  <path d="M1026 498 l24 24 M1050 498 l-24 24" stroke="#C33A3A" stroke-width="3" stroke-linecap="round"/>
  <text x="1054" y="512" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#A12B2B">AT RISK</text>

  <text x="122" y="577" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2F3B43">Data Centers</text>
  <text x="380" y="577" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#4A5963">T. Wilson</text>
  <text x="690" y="577" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#263238">$31.4M</text>
  <text x="860" y="577" width="110" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#263238">30.9%</text>
  <rect x="1010" y="556" width="104" height="28" rx="14" fill="#E6F4EC"/>
  <path d="M1028 569 l7 7 l14 -15" fill="none" stroke="#168A4A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1054" y="576" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#168A4A">ON PLAN</text>

  <rect x="104" y="621" width="280" height="2" rx="1" fill="#0070C0" filter="url(#softGlow)"/>
  <text x="100" y="662" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#75858E">
    Note: Numbers are right-aligned for rapid magnitude comparison; only the focus row receives color.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Building the table with full cell borders or vertical grid lines; it recreates the clutter this technique is meant to remove.
- ❌ Center-aligning all values; text should be left-aligned and numbers should be right-aligned.
- ❌ Using saturated fills on every row; reserve color for hierarchy and one key insight.
- ❌ Using SVG `<table>`, `<foreignObject>`, or HTML layout; use editable SVG rectangles, lines, and text instead.
- ❌ Applying filters to `<line>` dividers; use plain strokes for dividers and apply shadows only to rectangles, paths, or text.

## Composition notes
- Keep a generous title area above the table, then place the table card as the main visual object occupying roughly 80–85% of slide width.
- Use horizontal rhythm: header band, body rows, thin dividers, and no vertical rules.
- Create hierarchy through restrained contrast: dark title, blue header, gray body text, one pale-blue highlight row.
- Give numbers their own visual lane by right-aligning them consistently; this is the table’s main structural device.