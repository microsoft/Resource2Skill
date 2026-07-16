# SVG Recipe — Interactive Hyperlinked Table of Contents

## Visual mechanism
A standard agenda becomes a polished navigation hub: each section is presented as an individual underlined link card with a generous invisible hit area, clear hierarchy, and slide/section numbering. The right side stays mostly open, anchored by soft gradient geometry and a “navigation” motif to signal that the slide is interactive rather than merely informational.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for the pale blue left content panel
- 6× `<rect>` for clickable link-card backgrounds
- 6× transparent `<rect>` hit areas inside hyperlink wrappers
- 6× `<text>` for section numbers
- 6× `<text>` for linked agenda titles
- 6× `<text>` for short section descriptors
- 6× `<path>` for small chevron affordances at the end of each link row
- 1× `<text>` for the main title
- 1× `<text>` for the subtitle / instruction line
- 1× `<text>` for the right-side callout label
- 1× `<text>` for the right-side callout body
- 1× `<line>` for the title accent rule
- 3× `<circle>` for decorative navigation nodes
- 2× `<path>` for soft organic gradient blobs on the right
- 1× `<path>` for the curved route line connecting navigation nodes
- 1× `<linearGradient>` for the panel / card accents
- 2× `<radialGradient>` for the soft cyan / blue decorative blobs
- 1× `<filter id="softShadow">` applied to link cards and the right callout
- 1× `<filter id="glow">` applied to decorative circles / blobs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4FAFF"/>
      <stop offset="100%" stop-color="#EAF5FF"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7FBFF"/>
    </linearGradient>

    <radialGradient id="cyanBlob" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#00B0F0" stop-opacity="0.55"/>
      <stop offset="70%" stop-color="#00B0F0" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#00B0F0" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="blueBlob" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#0070C0" stop-opacity="0.35"/>
      <stop offset="75%" stop-color="#0070C0" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#0070C0" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <path d="M880 70 C1010 15 1180 65 1238 185 C1300 314 1198 470 1050 445 C900 419 790 545 725 425 C653 292 736 132 880 70 Z"
        fill="url(#cyanBlob)" filter="url(#glow)"/>
  <path d="M1010 390 C1135 342 1266 430 1288 556 C1306 660 1206 746 1068 720 C942 696 846 642 864 538 C878 459 929 421 1010 390 Z"
        fill="url(#blueBlob)"/>

  <rect x="64" y="50" width="690" height="620" rx="34" fill="url(#panelGrad)"/>
  <line x1="108" y1="146" x2="310" y2="146" stroke="#00B0F0" stroke-width="5" stroke-linecap="round"/>

  <text x="108" y="112" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#0070C0">
    Table of Contents
  </text>
  <text x="108" y="176" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#516170">
    Click any section to jump directly to that part of the deck.
  </text>

  <a href="#slide-executive-summary">
    <rect x="96" y="220" width="604" height="58" rx="18" fill="url(#cardGrad)" filter="url(#softShadow)"/>
    <rect x="96" y="220" width="604" height="58" rx="18" fill="#FFFFFF" opacity="0.01"/>
    <text x="126" y="257" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#00A4E4">01</text>
    <text x="184" y="252" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" text-decoration="underline" fill="#333333">Executive Summary</text>
    <text x="454" y="253" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C7883">strategy snapshot</text>
    <path d="M658 240 L672 249 L658 258" fill="none" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </a>

  <a href="#slide-market-opportunity">
    <rect x="126" y="292" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
    <rect x="126" y="292" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.01"/>
    <text x="156" y="326" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#0070C0">02</text>
    <text x="214" y="323" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="21" text-decoration="underline" fill="#404040">Market Opportunity</text>
    <text x="492" y="324" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C7883">where we win</text>
    <path d="M658 311 L672 320 L658 329" fill="none" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </a>

  <a href="#slide-product-roadmap">
    <rect x="126" y="360" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
    <rect x="126" y="360" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.01"/>
    <text x="156" y="394" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#0070C0">03</text>
    <text x="214" y="391" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="21" text-decoration="underline" fill="#404040">Product Roadmap</text>
    <text x="492" y="392" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C7883">next releases</text>
    <path d="M658 379 L672 388 L658 397" fill="none" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </a>

  <a href="#slide-go-to-market">
    <rect x="126" y="428" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
    <rect x="126" y="428" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.01"/>
    <text x="156" y="462" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#0070C0">04</text>
    <text x="214" y="459" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="21" text-decoration="underline" fill="#404040">Go-to-Market Plan</text>
    <text x="492" y="460" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C7883">launch motion</text>
    <path d="M658 447 L672 456 L658 465" fill="none" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </a>

  <a href="#slide-financial-model">
    <rect x="126" y="496" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.96" filter="url(#softShadow)"/>
    <rect x="126" y="496" width="574" height="54" rx="17" fill="#FFFFFF" opacity="0.01"/>
    <text x="156" y="530" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#0070C0">05</text>
    <text x="214" y="527" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="21" text-decoration="underline" fill="#404040">Financial Model</text>
    <text x="492" y="528" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C7883">unit economics</text>
    <path d="M658 515 L672 524 L658 533" fill="none" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </a>

  <a href="#slide-qa">
    <rect x="96" y="574" width="604" height="58" rx="18" fill="#F2FBFF" filter="url(#softShadow)"/>
    <rect x="96" y="574" width="604" height="58" rx="18" fill="#FFFFFF" opacity="0.01"/>
    <text x="126" y="611" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#00A4E4">06</text>
    <text x="184" y="606" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" text-decoration="underline" fill="#333333">Q&amp;A / Appendix</text>
    <text x="454" y="607" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6C7883">supporting detail</text>
    <path d="M658 594 L672 603 L658 612" fill="none" stroke="#00B0F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </a>

  <path d="M934 206 C1012 244 1068 315 1050 398 C1034 474 964 515 892 548"
        fill="none" stroke="#9EDDF6" stroke-width="5" stroke-linecap="round" stroke-dasharray="3 16"/>
  <circle cx="922" cy="202" r="16" fill="#00B0F0" filter="url(#glow)"/>
  <circle cx="1053" cy="394" r="22" fill="#0070C0" opacity="0.92" filter="url(#glow)"/>
  <circle cx="892" cy="548" r="13" fill="#00B0F0" opacity="0.86" filter="url(#glow)"/>

  <rect x="835" y="242" width="330" height="178" rx="28" fill="#FFFFFF" opacity="0.88" filter="url(#softShadow)"/>
  <text x="872" y="296" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#0070C0">
    Non-linear review
  </text>
  <text x="872" y="338" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#4E5B66">
    Use this slide as the deck’s home base. Return here during Q&amp;A and jump to the section your audience needs.
  </text>
  <path d="M1094 372 L1114 386 L1094 400" fill="none" stroke="#00B0F0" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the entire agenda as one large `<text>` block; each link item needs its own text and hit-area shape so it can receive a distinct hyperlink target.
- ❌ Do not rely only on underlined text as the clickable area; add a nearly transparent `<rect>` over each row to create a forgiving click target in PowerPoint.
- ❌ Do not use `marker-end` for the chevrons; draw chevrons as small editable `<path>` strokes.
- ❌ Do not use `<foreignObject>` or HTML lists for indentation; create hierarchy with explicit x-positions, font weights, and separate SVG text objects.
- ❌ Do not place `clip-path` on text or card shapes; if image thumbnails are added later, apply clips only to `<image>` elements.

## Composition notes
- Keep the navigation list on the left 55–60% of the slide; reserve the right side for a light visual metaphor so the slide feels like a hub, not a dense menu.
- Use larger, bolder cards for primary entry points and slightly indented smaller cards for secondary sections.
- Preserve generous vertical spacing between rows; clickable agendas feel more premium when they are easy to target.
- Use one accent color rhythm consistently: section numbers, underlines, chevrons, and decorative nodes should share the same cyan/blue family.