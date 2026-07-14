# SVG Recipe — App Window List

## Visual mechanism
Create a polished “application window” card floating on a soft background: a browser-like chrome frames a numbered content list on the left, while a portrait image card on the right adds human or product context. A bottom action bar anchors the composition with a call-to-action, status chips, or navigation controls.

## SVG primitives needed
- 1× large `<rect>` for the slide background
- 1× `<radialGradient>` and 1× `<linearGradient>` for atmospheric background and window surface
- 1× `<filter id="windowShadow">` for the main window elevation
- 1× `<filter id="softGlow">` for subtle colored accent glow
- 1× rounded `<rect>` for the main app window
- 1× rounded `<rect>` for the top browser chrome
- 3× small `<circle>` for window control dots
- 3× numbered badge `<circle>` elements for the list indices
- 3× list row `<rect>` elements for item cards
- 6× `<text>` elements for list titles and descriptions
- 1× `<clipPath>` with rounded `<rect>` applied to the side `<image>`
- 1× `<image>` for the optional portrait/product screenshot side visual
- 2× decorative `<path>` elements for abstract UI accents behind the side image
- 1× bottom action bar `<rect>`
- 1× CTA button `<rect>` plus `<text>`
- Several small `<rect>`, `<circle>`, and `<path>` elements for UI details, chips, icons, and navigation decoration

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="68%" cy="28%" r="76%">
      <stop offset="0%" stop-color="#DDF4FF"/>
      <stop offset="48%" stop-color="#F4F7FB"/>
      <stop offset="100%" stop-color="#E9EDF5"/>
    </radialGradient>

    <linearGradient id="windowFill" x1="180" y1="88" x2="1100" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F9FC"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="820" y1="120" x2="1060" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4F8CFF"/>
      <stop offset="55%" stop-color="#6B5CFF"/>
      <stop offset="100%" stop-color="#FF7AB6"/>
    </linearGradient>

    <filter id="windowShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="portraitClip">
      <rect x="838" y="190" width="250" height="318" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <path d="M897 112 C976 64 1112 83 1153 177 C1197 279 1104 328 1043 392 C969 470 962 566 850 548 C730 529 722 404 771 318 C811 247 816 162 897 112 Z"
        fill="url(#accentGrad)" opacity="0.16" filter="url(#softGlow)"/>
  <path d="M196 538 C252 476 356 492 394 548 C434 607 367 658 276 660 C191 662 149 591 196 538 Z"
        fill="#73D0FF" opacity="0.18" filter="url(#softGlow)"/>

  <rect x="132" y="76" width="1016" height="568" rx="34" fill="url(#windowFill)" filter="url(#windowShadow)"/>
  <rect x="132" y="76" width="1016" height="72" rx="34" fill="#F1F4F9"/>
  <rect x="132" y="120" width="1016" height="28" fill="#F1F4F9"/>

  <circle cx="178" cy="112" r="8" fill="#FF6B6B"/>
  <circle cx="204" cy="112" r="8" fill="#FFC857"/>
  <circle cx="230" cy="112" r="8" fill="#45D483"/>

  <rect x="280" y="96" width="382" height="32" rx="16" fill="#FFFFFF" stroke="#DDE4F0"/>
  <circle cx="304" cy="112" r="6" fill="#A8B4C5"/>
  <text x="324" y="117" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#778397">workspace.app / launch-plan</text>

  <text x="184" y="197" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" letter-spacing="2" fill="#5C6B82">IMPLEMENTATION QUEUE</text>
  <text x="184" y="238" width="555" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#172033">Three workstreams ready for review</text>

  <rect x="184" y="286" width="570" height="86" rx="22" fill="#FFFFFF" stroke="#E3E8F2"/>
  <circle cx="226" cy="329" r="22" fill="#EAF2FF"/>
  <text x="216" y="337" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#2F6BFF">1</text>
  <text x="270" y="319" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#1E293B">Map the customer journey</text>
  <text x="270" y="348" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66758A">Identify the five moments where product guidance changes conversion intent.</text>

  <rect x="184" y="388" width="570" height="86" rx="22" fill="#FFFFFF" stroke="#E3E8F2"/>
  <circle cx="226" cy="431" r="22" fill="#F0ECFF"/>
  <text x="216" y="439" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#6B5CFF">2</text>
  <text x="270" y="421" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#1E293B">Prioritize automation triggers</text>
  <text x="270" y="450" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66758A">Rank rules by business impact, signal quality, and effort to maintain.</text>

  <rect x="184" y="490" width="570" height="86" rx="22" fill="#FFFFFF" stroke="#E3E8F2"/>
  <circle cx="226" cy="533" r="22" fill="#FFEAF4"/>
  <text x="216" y="541" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#E7498A">3</text>
  <text x="270" y="523" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#1E293B">Publish the operating dashboard</text>
  <text x="270" y="552" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66758A">Give teams one shared surface for progress, risks, and next actions.</text>

  <rect x="806" y="166" width="314" height="384" rx="42" fill="#FFFFFF" stroke="#E3E8F2"/>
  <path d="M832 222 C860 174 942 156 1000 184 C1052 209 1074 270 1060 326 C1044 394 982 444 913 430 C847 416 798 377 800 311 C801 272 814 251 832 222 Z"
        fill="url(#accentGrad)" opacity="0.22"/>
  <image x="838" y="190" width="250" height="318" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/portrait-of-product-lead-using-tablet.jpg"
         clip-path="url(#portraitClip)"/>

  <rect x="860" y="472" width="206" height="48" rx="24" fill="#172033" opacity="0.88"/>
  <circle cx="890" cy="496" r="13" fill="#45D483"/>
  <text x="914" y="502" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Live review</text>

  <rect x="132" y="596" width="1016" height="48" rx="0" fill="#F8FAFD"/>
  <rect x="184" y="608" width="164" height="24" rx="12" fill="#EEF3FA"/>
  <circle cx="204" cy="620" r="5" fill="#4F8CFF"/>
  <text x="218" y="625" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#59687E">Sprint 04</text>

  <rect x="850" y="602" width="188" height="34" rx="17" fill="#246BFE"/>
  <text x="884" y="624" width="104" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Open action plan</text>
  <path d="M1006 613 L1017 619 L1006 625" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="1068" cy="619" r="4" fill="#C2CAD8"/>
  <circle cx="1084" cy="619" r="4" fill="#246BFE"/>
  <circle cx="1100" cy="619" r="4" fill="#C2CAD8"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<foreignObject>` to embed HTML-style app chrome; build the window with editable SVG rectangles, text, and paths.
- ❌ Do not apply `clip-path` to regular shape cards; use clipping only on the side `<image>` for the portrait/screenshot crop.
- ❌ Do not use `<use>` or `<symbol>` for repeated list rows; duplicate the row primitives directly so PowerPoint keeps them editable.
- ❌ Do not use `marker-end` for the CTA arrow; draw the arrowhead with a small editable `<path>`.
- ❌ Do not put shadows on `<line>` elements; use shadow filters only on rectangles, paths, circles, ellipses, or text.

## Composition notes
- Keep the main app window at roughly 80% slide width and centered, leaving soft negative space around it for a premium floating-card feel.
- Reserve the left 55–60% of the window for the numbered list; each row should have enough height for a title plus one concise supporting sentence.
- Use the right side for a portrait, product screenshot, or contextual image; overlap it with abstract gradient shapes to avoid a flat dashboard look.
- The bottom action bar should be quieter than the list: small status chip on the left, primary CTA on the right, and minimal navigation dots or metadata.