# SVG Recipe — Dynamic Split-Overlay Agenda Cascade

## Visual mechanism
A full-bleed photo is tamed by two translucent vertical overlays: a dark title sidebar and a bright content field. Numbered diamond markers sit exactly on the split seam, creating a zipper-like cascade that connects the left-side section label to the right-side agenda details.

## SVG primitives needed
- 1× `<image>` for the full-bleed photographic background.
- 2× `<rect>` for the dark left overlay and translucent white right overlay.
- 1× `<linearGradient>` for a subtle premium highlight wash over the content panel.
- 1× `<filter id="diamondShadow">` applied to diamond markers for depth.
- 1× `<filter id="softTextGlow">` applied to the vertical sidebar title for legibility.
- 1× `<rect>` for the narrow seam accent at the split.
- 5× `<path>` for rotated-square diamond agenda markers.
- 5× `<text>` for marker numbers.
- 5× `<text>` for agenda item titles.
- 5× `<text>` with nested `<tspan>` for agenda item descriptions.
- 5× `<path>` for subtle angled connector ticks extending from each diamond into the content panel.
- 1× rotated `<text>` for the large vertical sidebar title.
- 1× small `<text>` for sidebar subtitle/metadata.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="rightPanelWash" x1="336" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="0.55" stop-color="#F7FAFC" stop-opacity="0.90"/>
      <stop offset="1" stop-color="#E9EEF4" stop-opacity="0.86"/>
    </linearGradient>

    <linearGradient id="leftPanelDepth" x1="0" y1="0" x2="336" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111827" stop-opacity="0.96"/>
      <stop offset="0.55" stop-color="#20242B" stop-opacity="0.94"/>
      <stop offset="1" stop-color="#0B0F14" stop-opacity="0.96"/>
    </linearGradient>

    <filter id="diamondShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softTextGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1600&q=80"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="336" height="720" fill="url(#leftPanelDepth)"/>
  <rect x="336" y="0" width="944" height="720" fill="url(#rightPanelWash)"/>

  <rect x="332" y="0" width="8" height="720" fill="#FFFFFF" opacity="0.34"/>
  <rect x="340" y="0" width="2" height="720" fill="#111827" opacity="0.10"/>

  <text x="164" y="382" width="520"
        transform="rotate(-90 164 382)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="700" fill="#FFFFFF"
        text-anchor="middle" filter="url(#softTextGlow)" letter-spacing="2">
    MEETING <tspan font-weight="300">AGENDA</tspan>
  </text>

  <text x="42" y="662" width="245"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#CBD5E1" letter-spacing="1.5">
    STRATEGIC WORKSESSION · Q3
  </text>

  <path d="M336 84 L386 134 L336 184 L286 134 Z"
        fill="#4CAF50" stroke="#FFFFFF" stroke-width="5" filter="url(#diamondShadow)"/>
  <path d="M386 134 C420 134 438 119 458 105"
        fill="none" stroke="#4CAF50" stroke-width="4" stroke-linecap="round" opacity="0.75"/>
  <text x="336" y="146" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">01</text>
  <text x="470" y="118" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#4CAF50">Opening Context</text>
  <text x="470" y="154" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#4B5563">
    <tspan x="470" dy="0">Align on the decision frame, success measures, and the</tspan>
    <tspan x="470" dy="24">business questions that matter most for the session.</tspan>
  </text>

  <path d="M336 190 L386 240 L336 290 L286 240 Z"
        fill="#9C27B0" stroke="#FFFFFF" stroke-width="5" filter="url(#diamondShadow)"/>
  <path d="M386 240 C423 240 442 225 466 210"
        fill="none" stroke="#9C27B0" stroke-width="4" stroke-linecap="round" opacity="0.75"/>
  <text x="336" y="252" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">02</text>
  <text x="470" y="224" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#9C27B0">Market Signal Review</text>
  <text x="470" y="260" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#4B5563">
    <tspan x="470" dy="0">Scan demand shifts, competitive movement, customer</tspan>
    <tspan x="470" dy="24">sentiment, and the implications for near-term priorities.</tspan>
  </text>

  <path d="M336 296 L386 346 L336 396 L286 346 Z"
        fill="#C0A020" stroke="#FFFFFF" stroke-width="5" filter="url(#diamondShadow)"/>
  <path d="M386 346 C420 346 438 361 458 378"
        fill="none" stroke="#C0A020" stroke-width="4" stroke-linecap="round" opacity="0.75"/>
  <text x="336" y="358" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">03</text>
  <text x="470" y="330" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#C0A020">Operating Model Choices</text>
  <text x="470" y="366" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#4B5563">
    <tspan x="470" dy="0">Compare scenarios, resourcing tradeoffs, and the few</tspan>
    <tspan x="470" dy="24">capabilities that unlock disproportionate execution speed.</tspan>
  </text>

  <path d="M336 402 L386 452 L336 502 L286 452 Z"
        fill="#03A9F4" stroke="#FFFFFF" stroke-width="5" filter="url(#diamondShadow)"/>
  <path d="M386 452 C423 452 444 437 468 422"
        fill="none" stroke="#03A9F4" stroke-width="4" stroke-linecap="round" opacity="0.75"/>
  <text x="336" y="464" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">04</text>
  <text x="470" y="436" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#03A9F4">Investment Roadmap</text>
  <text x="470" y="472" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#4B5563">
    <tspan x="470" dy="0">Sequence bets by strategic value, implementation risk,</tspan>
    <tspan x="470" dy="24">and the evidence required before scaling commitments.</tspan>
  </text>

  <path d="M336 508 L386 558 L336 608 L286 558 Z"
        fill="#00BCD4" stroke="#FFFFFF" stroke-width="5" filter="url(#diamondShadow)"/>
  <path d="M386 558 C420 558 438 573 458 590"
        fill="none" stroke="#00BCD4" stroke-width="4" stroke-linecap="round" opacity="0.75"/>
  <text x="336" y="570" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="800" fill="#FFFFFF" text-anchor="middle">05</text>
  <text x="470" y="542" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" fill="#00BCD4">Decisions & Next Actions</text>
  <text x="470" y="578" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#4B5563">
    <tspan x="470" dy="0">Lock owners, timelines, dependencies, and the follow-up</tspan>
    <tspan x="470" dy="24">cadence that keeps momentum visible after the meeting.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the split-overlay treatment; use translucent `<rect>` panels over the photo instead.
- ❌ Do not use `<pattern>` fills for the panels; gradients and opacity translate more predictably.
- ❌ Do not place `clip-path` on rectangles or paths for the overlays; clipping is only reliable on `<image>`.
- ❌ Do not use `marker-end` on connector paths; if arrows are needed, draw them as explicit lines or small paths.
- ❌ Do not omit `width` on text elements, especially the rotated sidebar title and multi-line agenda descriptions.

## Composition notes
- Keep the split seam around 25–28% of slide width; this gives the sidebar authority while preserving enough room for readable agenda copy.
- Center every diamond on the seam so each marker overlaps both the dark and light panels equally.
- Use saturated marker colors sparingly: repeat each color only in its diamond, connector tick, and agenda heading.
- Leave the right panel airy; agenda descriptions should occupy the middle band, not touch the far-right edge.