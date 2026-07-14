# SVG Recipe — Comprehensive Capability Comparison Matrix

## Visual mechanism
A premium comparison matrix turns dense product capability data into a highly scannable executive table: a wide parameter column anchors each row while equal product columns use color-coded symbols, short labels, and alternating row bands to support fast horizontal comparison.

## SVG primitives needed
- 1× full-slide `<rect>` for the soft sage/teal background
- 3× decorative `<circle>` / `<path>` elements for subtle presentation-template atmosphere
- 1× rounded `<rect>` table card with shadow for the main matrix container
- 1× `<filter id="cardShadow">` applied to the matrix card
- 2× `<linearGradient>` definitions for background depth and header polish
- 5× header `<rect>` cells for the parameter and product columns
- 7× row-band `<rect>` elements for alternating comparison rows
- 8× vertical/horizontal `<line>` elements for clean table dividers
- Multiple `<text>` elements with explicit `width` for title, subtitle, headers, row labels, feature values, checkmarks, and crosses
- Optional small `<circle>` badges behind product-tier labels for premium visual hierarchy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5f7772"/>
      <stop offset="100%" stop-color="#e7ebe4"/>
    </linearGradient>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2d4b46"/>
      <stop offset="100%" stop-color="#527976"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="-18" cy="28" r="145" fill="none" stroke="#ffffff" stroke-width="42" opacity="0.72"/>
  <circle cx="198" cy="235" r="118" fill="#ffffff" opacity="0.08"/>
  <path d="M1018 0 L1280 0 L1280 720 L1038 720 C1008 570 1002 390 1018 0 Z" fill="#f5f7f0" opacity="0.58"/>

  <text x="72" y="68" width="760" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#ffffff">
    Product Capability Comparison
  </text>
  <text x="74" y="104" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#eaf1ee">
    Feature breakdown across service tiers, competitors, and buying criteria
  </text>
  <rect x="72" y="128" width="1136" height="2" fill="#ffffff" opacity="0.38"/>

  <rect x="72" y="158" width="1136" height="486" rx="24" fill="#ffffff" opacity="0.97" filter="url(#cardShadow)"/>
  <rect x="72" y="158" width="1136" height="64" rx="24" fill="url(#headerGrad)"/>
  <rect x="72" y="196" width="1136" height="26" fill="url(#headerGrad)"/>

  <rect x="72" y="222" width="1136" height="54" fill="#ffffff"/>
  <rect x="72" y="276" width="1136" height="54" fill="#f0f5f5"/>
  <rect x="72" y="330" width="1136" height="54" fill="#ffffff"/>
  <rect x="72" y="384" width="1136" height="54" fill="#f0f5f5"/>
  <rect x="72" y="438" width="1136" height="54" fill="#ffffff"/>
  <rect x="72" y="492" width="1136" height="54" fill="#f0f5f5"/>
  <rect x="72" y="546" width="1136" height="54" fill="#ffffff"/>

  <rect x="72" y="222" width="340" height="378" fill="#365a54" opacity="0.09"/>
  <line x1="412" y1="158" x2="412" y2="600" stroke="#d8e1df" stroke-width="2"/>
  <line x1="611" y1="158" x2="611" y2="600" stroke="#d8e1df" stroke-width="2"/>
  <line x1="810" y1="158" x2="810" y2="600" stroke="#d8e1df" stroke-width="2"/>
  <line x1="1009" y1="158" x2="1009" y2="600" stroke="#d8e1df" stroke-width="2"/>
  <line x1="72" y1="276" x2="1208" y2="276" stroke="#d8e1df" stroke-width="1.4"/>
  <line x1="72" y1="384" x2="1208" y2="384" stroke="#d8e1df" stroke-width="1.4"/>
  <line x1="72" y1="492" x2="1208" y2="492" stroke="#d8e1df" stroke-width="1.4"/>
  <line x1="72" y1="600" x2="1208" y2="600" stroke="#d8e1df" stroke-width="1.4"/>

  <text x="98" y="199" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Core Parameters</text>
  <text x="452" y="188" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#cfe8e3">BASIC</text>
  <text x="436" y="207" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Starter</text>
  <text x="646" y="188" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#cfe8e3">PRO</text>
  <text x="638" y="207" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Professional</text>
  <text x="846" y="188" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#cfe8e3">BUSINESS</text>
  <text x="839" y="207" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Business Plus</text>
  <text x="1048" y="188" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#cfe8e3">ENTERPRISE</text>
  <text x="1048" y="207" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#ffffff">Enterprise</text>

  <text x="98" y="256" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">Customizable user dashboard</text>
  <text x="98" y="310" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">Cloud storage capacity</text>
  <text x="98" y="364" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">Responsive mobile app access</text>
  <text x="98" y="418" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">Free monthly premium add-ons</text>
  <text x="98" y="472" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">Hosted & managed infrastructure</text>
  <text x="98" y="526" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">White-labeling / remove branding</text>
  <text x="98" y="580" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#2f3b3a">24/7 priority support SLAs</text>

  <text x="492" y="258" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="686" y="258" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="886" y="258" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="1086" y="258" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>

  <text x="468" y="311" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#323b3a">10 GB</text>
  <text x="664" y="311" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#323b3a">50 GB</text>
  <text x="850" y="311" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#00a859">Unlimited</text>
  <text x="1048" y="311" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#00a859">Unlimited</text>

  <text x="492" y="366" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="686" y="366" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="886" y="366" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="1086" y="366" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>

  <text x="492" y="420" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="686" y="420" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="886" y="420" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="1086" y="420" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>

  <text x="492" y="474" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="686" y="474" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="886" y="474" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>
  <text x="1086" y="474" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>

  <text x="492" y="528" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="686" y="528" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="886" y="528" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#e03a3e">✘</text>
  <text x="1086" y="528" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#00a859">✔</text>

  <text x="460" y="581" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#323b3a">Community</text>
  <text x="656" y="581" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#323b3a">Email only</text>
  <text x="840" y="581" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#323b3a">Phone + Email</text>
  <text x="1040" y="581" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#323b3a">Dedicated Rep</text>

  <rect x="72" y="620" width="1136" height="24" rx="0" fill="#2d4b46" opacity="0.08"/>
  <text x="92" y="637" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#527976">
    Decision guide: green indicates included capability; red indicates unavailable or requires custom contract.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using an actual SVG `<table>` or HTML inside `<foreignObject>`; PowerPoint translation will fail or become non-editable.
- ❌ Relying on `<mask>` for row effects; use direct filled rectangles and opacity instead.
- ❌ Applying `clip-path` to table cells or text; clipping is only reliable for images.
- ❌ Using tiny text-heavy cells; convert binary states to large Unicode symbols and keep specifications short.
- ❌ Building the grid from a single bitmap screenshot; it defeats the purpose of editable PowerPoint shapes.

## Composition notes
- Keep the title and subtitle in the upper 15–20% of the canvas; the matrix should dominate the lower three quarters.
- Allocate roughly 30% of table width to the parameter column and distribute the remaining width evenly across product or tier columns.
- Use a dark teal header and subtle cool-gray row banding so the eye can track horizontally without heavy borders.
- Reserve green and red exclusively for capability states; this makes symbolic typography instantly meaningful.