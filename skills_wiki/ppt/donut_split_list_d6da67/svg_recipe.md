# SVG Recipe — Donut Split List

## Visual mechanism
A bold segmented donut dominates the left half, acting as a visual index for four list items. The right half uses a highlighted headline and stacked bullet cards whose colored chips match the donut segments, creating a clear split-list relationship.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for soft abstract background blobs
- 4× `<path>` for thick donut wedges with gaps between segments
- 1× `<circle>` for the donut center hub
- 4× `<circle>` for small colored index dots on the donut
- 1× `<rect>` for the headline highlight pill
- 4× `<rect>` for rounded bullet cards
- 4× `<circle>` for numbered bullet chips
- 1× `<line>` for a subtle split divider / connector accent
- Multiple `<text>` elements with explicit `width` attributes for title, labels, numbers, and bullet copy
- 4× `<linearGradient>` for premium donut segment fills
- 1× `<radialGradient>` for the center hub
- 2× `<filter>` definitions: soft card shadow and gentle glow on the donut

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF4FF"/>
    </linearGradient>

    <linearGradient id="segBlue" x1="190" y1="150" x2="550" y2="470">
      <stop offset="0%" stop-color="#00B8FF"/>
      <stop offset="100%" stop-color="#246BFE"/>
    </linearGradient>
    <linearGradient id="segTeal" x1="520" y1="470" x2="180" y2="520">
      <stop offset="0%" stop-color="#2ED8B6"/>
      <stop offset="100%" stop-color="#00A789"/>
    </linearGradient>
    <linearGradient id="segAmber" x1="160" y1="470" x2="350" y2="150">
      <stop offset="0%" stop-color="#FFC857"/>
      <stop offset="100%" stop-color="#FF8A00"/>
    </linearGradient>
    <linearGradient id="segViolet" x1="360" y1="150" x2="560" y2="350">
      <stop offset="0%" stop-color="#B074FF"/>
      <stop offset="100%" stop-color="#6C3BFF"/>
    </linearGradient>

    <radialGradient id="hubGrad" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EAF0FF"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-60 145 C55 42 185 28 274 92 C363 156 332 267 210 306 C88 345 -28 290 -60 145 Z" fill="#DCEBFF" opacity="0.6"/>
  <path d="M1040 610 C1128 520 1258 512 1326 586 C1394 660 1320 757 1198 756 C1076 755 968 700 1040 610 Z" fill="#E8E0FF" opacity="0.55"/>

  <circle cx="350" cy="360" r="236" fill="#FFFFFF" opacity="0.82" filter="url(#shadow)"/>
  <circle cx="350" cy="360" r="216" fill="none" stroke="#DDE7F6" stroke-width="1.5"/>

  <path d="M350 150 A210 210 0 0 1 540 449 L470 416 A132 132 0 0 0 350 228 Z" fill="url(#segBlue)" filter="url(#softGlow)"/>
  <path d="M522 480 A210 210 0 0 1 178 480 L242 436 A132 132 0 0 0 458 436 Z" fill="url(#segTeal)" filter="url(#softGlow)"/>
  <path d="M160 449 A210 210 0 0 1 332 151 L339 228 A132 132 0 0 0 230 416 Z" fill="url(#segAmber)" filter="url(#softGlow)"/>
  <path d="M368 151 A210 210 0 0 1 559 342 L482 348 A132 132 0 0 0 362 228 Z" fill="url(#segViolet)" filter="url(#softGlow)"/>

  <circle cx="350" cy="360" r="116" fill="url(#hubGrad)" filter="url(#shadow)"/>
  <text x="290" y="344" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#65738A" text-anchor="middle">
    <tspan x="350">OPERATING</tspan>
  </text>
  <text x="284" y="397" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#172033" text-anchor="middle">
    <tspan x="350">04</tspan>
  </text>
  <text x="284" y="426" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#7B8798" text-anchor="middle">
    <tspan x="350">growth levers</tspan>
  </text>

  <circle cx="474" cy="246" r="18" fill="#FFFFFF"/>
  <circle cx="474" cy="246" r="10" fill="#246BFE"/>
  <circle cx="376" cy="545" r="18" fill="#FFFFFF"/>
  <circle cx="376" cy="545" r="10" fill="#00A789"/>
  <circle cx="183" cy="320" r="18" fill="#FFFFFF"/>
  <circle cx="183" cy="320" r="10" fill="#FF8A00"/>
  <circle cx="500" cy="360" r="18" fill="#FFFFFF"/>
  <circle cx="500" cy="360" r="10" fill="#6C3BFF"/>

  <line x1="610" y1="128" x2="610" y2="592" stroke="#D6E0EF" stroke-width="2" stroke-dasharray="8 12"/>

  <rect x="665" y="86" width="385" height="54" rx="27" fill="#FFE8A3"/>
  <text x="680" y="127" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" fill="#172033">
    Donut split list
  </text>
  <text x="680" y="174" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="500" fill="#667085">
    Use the circular index to make a short strategy list feel dimensional and memorable.
  </text>

  <rect x="675" y="225" width="465" height="78" rx="22" fill="#FFFFFF" filter="url(#shadow)"/>
  <rect x="675" y="225" width="8" height="78" rx="4" fill="#246BFE"/>
  <circle cx="720" cy="264" r="22" fill="#E6F2FF"/>
  <text x="706" y="272" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#246BFE" text-anchor="middle">1</text>
  <text x="760" y="257" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="750" fill="#1E293B">Acquire faster</text>
  <text x="760" y="283" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">Prioritize channels with compounding reach.</text>

  <rect x="700" y="326" width="465" height="78" rx="22" fill="#FFFFFF" filter="url(#shadow)"/>
  <rect x="700" y="326" width="8" height="78" rx="4" fill="#00A789"/>
  <circle cx="745" cy="365" r="22" fill="#E5FBF6"/>
  <text x="731" y="373" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#00A789" text-anchor="middle">2</text>
  <text x="785" y="358" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="750" fill="#1E293B">Activate deeper</text>
  <text x="785" y="384" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">Shorten the path from signup to first value.</text>

  <rect x="675" y="427" width="465" height="78" rx="22" fill="#FFFFFF" filter="url(#shadow)"/>
  <rect x="675" y="427" width="8" height="78" rx="4" fill="#FF8A00"/>
  <circle cx="720" cy="466" r="22" fill="#FFF2D8"/>
  <text x="706" y="474" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FF8A00" text-anchor="middle">3</text>
  <text x="760" y="459" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="750" fill="#1E293B">Retain longer</text>
  <text x="760" y="485" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">Build repeat loops around moments of trust.</text>

  <rect x="700" y="528" width="465" height="78" rx="22" fill="#FFFFFF" filter="url(#shadow)"/>
  <rect x="700" y="528" width="8" height="78" rx="4" fill="#6C3BFF"/>
  <circle cx="745" cy="567" r="22" fill="#F0EAFF"/>
  <text x="731" y="575" width="28" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#6C3BFF" text-anchor="middle">4</text>
  <text x="785" y="560" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="750" fill="#1E293B">Monetize smarter</text>
  <text x="785" y="586" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#64748B">Package value so expansion feels natural.</text>
</svg>
```

## Avoid in this skill
- ❌ Using a stroked circle with `stroke-dasharray` as the only donut construction; editable wedge paths give better control over gaps, gradients, and labels.
- ❌ Placing bullet text inside a single auto-sized text box; every `<text>` needs a fixed `width` so PowerPoint does not reflow unpredictably.
- ❌ Applying `filter` to connector `<line>` elements; shadows/glows on lines are dropped, so keep line accents flat.
- ❌ Using `<mask>` or clipping shapes to create the donut hole; instead draw wedge paths with inner arcs and place a center circle on top.

## Composition notes
- Keep the donut centered in the left 45% of the slide, large enough to feel like the primary visual anchor.
- Use matching colors between donut wedges and list chips so the viewer can scan from circle to bullet cards intuitively.
- Let the right side breathe: headline at the top, four low-density cards below, with staggered x-positions for motion.
- Use a pale background and white cards so the saturated donut segments carry the visual energy.