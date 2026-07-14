# SVG Recipe — Segmented Chevron Progression Timeline

## Visual mechanism
A sequence of bold, forward-pointing chevrons forms the main chronological spine, with each segment acting as a colored phase marker. Supporting cards beneath each chevron provide the phase title and short description while preserving a strong left-to-right momentum.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<circle>` for soft decorative background glows
- 5× `<path>` for the main segmented chevron blocks
- 5× `<path>` for subtle glossy highlight overlays inside the chevrons
- 5× `<line>` for vertical connectors from chevrons to detail cards
- 5× `<circle>` for connector nodes below the chevrons
- 5× `<rect>` for white rounded detail cards
- 1× `<linearGradient>` for the background wash
- 5× `<linearGradient>` for premium two-tone chevron fills
- 1× `<filter id="softShadow">` applied to chevrons and cards
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, phase labels, years, titles, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="gRed" x1="86" y1="255" x2="301" y2="367" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF5A6F"/>
      <stop offset="100%" stop-color="#D91F43"/>
    </linearGradient>
    <linearGradient id="gGreen" x1="307" y1="255" x2="522" y2="367" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#48E296"/>
      <stop offset="100%" stop-color="#16A765"/>
    </linearGradient>
    <linearGradient id="gBlue" x1="528" y1="255" x2="743" y2="367" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#5EC9FF"/>
      <stop offset="100%" stop-color="#2278D8"/>
    </linearGradient>
    <linearGradient id="gPurple" x1="749" y1="255" x2="964" y2="367" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#C084FC"/>
      <stop offset="100%" stop-color="#7C3AB8"/>
    </linearGradient>
    <linearGradient id="gOrange" x1="970" y1="255" x2="1185" y2="367" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFBE45"/>
      <stop offset="100%" stop-color="#F06418"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="180%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <circle cx="90" cy="620" r="190" fill="#E2364B" opacity="0.055"/>
  <circle cx="1195" cy="145" r="150" fill="#3498DB" opacity="0.07"/>

  <text x="120" y="82" width="1040" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#172033">
    5-Year Strategic Roadmap
  </text>
  <text x="290" y="126" width="700" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="500" fill="#667085">
    From foundation to global scale — a segmented chevron timeline for executive planning
  </text>
  <rect x="500" y="154" width="280" height="5" rx="2.5" fill="#172033" opacity="0.12"/>

  <path d="M86 255 L257 255 L301 311 L257 367 L86 367 L130 311 Z" fill="url(#gRed)" filter="url(#softShadow)"/>
  <path d="M307 255 L478 255 L522 311 L478 367 L307 367 L351 311 Z" fill="url(#gGreen)" filter="url(#softShadow)"/>
  <path d="M528 255 L699 255 L743 311 L699 367 L528 367 L572 311 Z" fill="url(#gBlue)" filter="url(#softShadow)"/>
  <path d="M749 255 L920 255 L964 311 L920 367 L749 367 L793 311 Z" fill="url(#gPurple)" filter="url(#softShadow)"/>
  <path d="M970 255 L1141 255 L1185 311 L1141 367 L970 367 L1014 311 Z" fill="url(#gOrange)" filter="url(#softShadow)"/>

  <path d="M101 267 L248 267 L282 311 L248 322 L111 322 L143 311 Z" fill="#FFFFFF" opacity="0.18"/>
  <path d="M322 267 L469 267 L503 311 L469 322 L332 322 L364 311 Z" fill="#FFFFFF" opacity="0.18"/>
  <path d="M543 267 L690 267 L724 311 L690 322 L553 322 L585 311 Z" fill="#FFFFFF" opacity="0.18"/>
  <path d="M764 267 L911 267 L945 311 L911 322 L774 322 L806 311 Z" fill="#FFFFFF" opacity="0.18"/>
  <path d="M985 267 L1132 267 L1166 311 L1132 322 L995 322 L1027 311 Z" fill="#FFFFFF" opacity="0.18"/>

  <text x="194" y="293" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.82">PHASE 01</text>
  <text x="194" y="331" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">2020</text>
  <text x="415" y="293" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.82">PHASE 02</text>
  <text x="415" y="331" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">2021</text>
  <text x="636" y="293" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.82">PHASE 03</text>
  <text x="636" y="331" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">2022</text>
  <text x="857" y="293" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.82">PHASE 04</text>
  <text x="857" y="331" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">2023</text>
  <text x="1078" y="293" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.82">PHASE 05</text>
  <text x="1078" y="331" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="800" fill="#FFFFFF">2024</text>

  <line x1="194" y1="367" x2="194" y2="415" stroke="#E2364B" stroke-width="2"/>
  <line x1="415" y1="367" x2="415" y2="415" stroke="#2ECC71" stroke-width="2"/>
  <line x1="636" y1="367" x2="636" y2="415" stroke="#3498DB" stroke-width="2"/>
  <line x1="857" y1="367" x2="857" y2="415" stroke="#9B59B6" stroke-width="2"/>
  <line x1="1078" y1="367" x2="1078" y2="415" stroke="#F39C12" stroke-width="2"/>

  <circle cx="194" cy="415" r="8" fill="#E2364B"/>
  <circle cx="415" cy="415" r="8" fill="#2ECC71"/>
  <circle cx="636" cy="415" r="8" fill="#3498DB"/>
  <circle cx="857" cy="415" r="8" fill="#9B59B6"/>
  <circle cx="1078" cy="415" r="8" fill="#F39C12"/>

  <rect x="92" y="438" width="204" height="132" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="313" y="438" width="204" height="132" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="534" y="438" width="204" height="132" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="755" y="438" width="204" height="132" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="976" y="438" width="204" height="132" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="194" y="468" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#E2364B">Foundation</text>
  <text x="112" y="500" width="164" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    <tspan x="112" dy="0">Establish core operating</tspan><tspan x="112" dy="20">model, funding, and the</tspan><tspan x="112" dy="20">initial leadership team.</tspan>
  </text>

  <text x="415" y="468" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#16A765">Alpha Launch</text>
  <text x="333" y="500" width="164" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    <tspan x="333" dy="0">Release a closed beta,</tspan><tspan x="333" dy="20">validate demand, and</tspan><tspan x="333" dy="20">prioritize feedback.</tspan>
  </text>

  <text x="636" y="468" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#2278D8">Market Entry</text>
  <text x="554" y="500" width="164" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    <tspan x="554" dy="0">Launch publicly with</tspan><tspan x="554" dy="20">targeted campaigns in</tspan><tspan x="554" dy="20">priority segments.</tspan>
  </text>

  <text x="857" y="468" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#7C3AB8">Scaling Up</text>
  <text x="775" y="500" width="164" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    <tspan x="775" dy="0">Expand capacity, add</tspan><tspan x="775" dy="20">automation, and grow</tspan><tspan x="775" dy="20">the customer base.</tspan>
  </text>

  <text x="1078" y="468" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#F06418">Global Reach</text>
  <text x="996" y="500" width="164" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    <tspan x="996" dy="0">Localize the offering,</tspan><tspan x="996" dy="20">open regional hubs,</tspan><tspan x="996" dy="20">and scale partnerships.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` arrows; the chevrons already imply direction and SVG arrow markers may not translate reliably.
- ❌ Building the chevrons with `<polygon>` if the translator target expects editable path geometry; use explicit `<path d="...">` shapes.
- ❌ Applying `clip-path` to chevron shapes for highlights; draw separate highlight paths instead.
- ❌ Overcrowding the chevron spine with full descriptions; keep only phase/year inside the shapes and put details below.

## Composition notes
- Keep the chevron spine around the upper-middle of the slide, roughly 35–45% down from the top.
- Use saturated categorical colors for the main sequence, then repeat those colors in smaller connector nodes and card headings.
- Let the white detail cards sit below the spine with generous spacing; this keeps the timeline readable rather than dense.
- For more than six phases, reduce card detail or split the roadmap across two slides instead of shrinking all typography.