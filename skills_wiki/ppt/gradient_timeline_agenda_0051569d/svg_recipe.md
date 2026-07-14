# SVG Recipe — Gradient Timeline Agenda

## Visual mechanism
A slim vertical timeline anchors the slide, with evenly spaced numbered octagon markers progressing from light blue to deep navy. Each marker branches into a concise agenda block, making the sequence feel chronological, polished, and easy to follow.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 2× large translucent `<path>` shapes for subtle premium background atmosphere
- 1× `<line>` for the main vertical timeline with gradient stroke
- 5× short `<line>` connectors from markers to agenda text
- 2× `<circle>` for timeline end caps
- 5× `<path>` octagons for agenda markers
- 5× `<text>` marker numbers centered on octagons
- 1× `<text>` main title with nested `<tspan>` styling
- 1× `<text>` subtitle
- 10× `<text>` blocks for agenda item headings and descriptions
- 1× `<linearGradient id="timelineGrad">` for the vertical timeline
- 1× `<radialGradient id="auraBlue">` for subtle background glow
- 1× `<filter id="softShadow">` applied to octagon markers
- 1× `<filter id="titleGlow">` applied lightly to the main title

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="timelineGrad" x1="0" y1="160" x2="0" y2="635" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ADD8E6"/>
      <stop offset="45%" stop-color="#5D91BD"/>
      <stop offset="100%" stop-color="#1C335C"/>
    </linearGradient>

    <radialGradient id="auraBlue" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#DFF3FA" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#DFF3FA" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-20%" y="-60%" width="140%" height="220%">
      <feGaussianBlur stdDeviation="1.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <path d="M930 70 C1080 40 1210 110 1245 245 C1285 400 1140 455 1040 430 C920 400 875 305 895 210 C906 150 875 95 930 70 Z"
        fill="url(#auraBlue)" opacity="0.75"/>
  <path d="M-85 510 C50 455 150 520 160 635 C168 732 40 760 -65 705 C-175 647 -195 555 -85 510 Z"
        fill="#EEF7FB" opacity="0.8"/>

  <text x="90" y="72" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="700"
        fill="#2F3C51" letter-spacing="1.5" filter="url(#titleGlow)">
    BUSINESS <tspan fill="#4B83B5">AGENDA</tspan>
  </text>
  <text x="92" y="106" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16"
        fill="#7D8793" letter-spacing="2">
    EXECUTIVE OPERATING PLAN · Q3 PRIORITIES
  </text>

  <line x1="330" y1="166" x2="330" y2="626" stroke="url(#timelineGrad)" stroke-width="5" stroke-linecap="round"/>
  <circle cx="330" cy="158" r="8" fill="#ADD8E6"/>
  <circle cx="330" cy="634" r="8" fill="#1C335C"/>

  <line x1="370" y1="198" x2="435" y2="198" stroke="#C7D1DB" stroke-width="2"/>
  <line x1="370" y1="298" x2="435" y2="298" stroke="#C7D1DB" stroke-width="2"/>
  <line x1="370" y1="398" x2="435" y2="398" stroke="#C7D1DB" stroke-width="2"/>
  <line x1="370" y1="498" x2="435" y2="498" stroke="#C7D1DB" stroke-width="2"/>
  <line x1="370" y1="598" x2="435" y2="598" stroke="#C7D1DB" stroke-width="2"/>

  <path d="M330 158 L355 168 L370 193 L360 218 L335 233 L310 223 L295 198 L305 173 Z"
        fill="#ADD8E6" filter="url(#softShadow)"/>
  <path d="M330 258 L355 268 L370 293 L360 318 L335 333 L310 323 L295 298 L305 273 Z"
        fill="#82B8D2" filter="url(#softShadow)"/>
  <path d="M330 358 L355 368 L370 393 L360 418 L335 433 L310 423 L295 398 L305 373 Z"
        fill="#5D91BD" filter="url(#softShadow)"/>
  <path d="M330 458 L355 468 L370 493 L360 518 L335 533 L310 523 L295 498 L305 473 Z"
        fill="#3866A0" filter="url(#softShadow)"/>
  <path d="M330 558 L355 568 L370 593 L360 618 L335 633 L310 623 L295 598 L305 573 Z"
        fill="#1C335C" filter="url(#softShadow)"/>

  <text x="303" y="204" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700"
        fill="#FFFFFF" text-anchor="middle">01</text>
  <text x="303" y="304" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700"
        fill="#FFFFFF" text-anchor="middle">02</text>
  <text x="303" y="404" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700"
        fill="#FFFFFF" text-anchor="middle">03</text>
  <text x="303" y="504" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700"
        fill="#FFFFFF" text-anchor="middle">04</text>
  <text x="303" y="604" width="54" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700"
        fill="#FFFFFF" text-anchor="middle">05</text>

  <text x="455" y="187" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2F3C51">
    MARKET CONTEXT
  </text>
  <text x="455" y="214" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8088">
    Review category shifts, customer signals, and competitive movement shaping this quarter.
  </text>

  <text x="455" y="287" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2F3C51">
    GROWTH PRIORITIES
  </text>
  <text x="455" y="314" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8088">
    Align leadership around the few initiatives most likely to accelerate pipeline momentum.
  </text>

  <text x="455" y="387" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2F3C51">
    OPERATING MODEL
  </text>
  <text x="455" y="414" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8088">
    Define ownership, cadence, and decision rights for cross-functional execution.
  </text>

  <text x="455" y="487" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2F3C51">
    INVESTMENT CHOICES
  </text>
  <text x="455" y="514" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8088">
    Confirm budget tradeoffs and resource allocation against expected business impact.
  </text>

  <text x="455" y="587" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2F3C51">
    NEXT-STEP COMMITMENTS
  </text>
  <text x="455" y="614" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#7A8088">
    Close with accountable actions, deadlines, and the metrics used to track progress.
  </text>

  <rect x="1030" y="548" width="132" height="34" rx="17" fill="#EEF4F8"/>
  <text x="1052" y="571" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700"
        fill="#3866A0" letter-spacing="1">AGENDA</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<use>` or `<symbol>` to repeat the octagons; duplicate each octagon as its own editable `<path>` instead.
- ❌ Applying `filter` to the timeline `<line>` or connector `<line>` elements; shadows/glows should be reserved for marker paths or text.
- ❌ Relying on `marker-end` for connector arrows; this agenda style works best with clean straight connector lines.
- ❌ Putting `clip-path` on marker shapes or text; clipping is only reliable for `<image>` elements.
- ❌ Omitting `width` on `<text>` elements, which can cause PowerPoint text layout to render unpredictably.

## Composition notes
- Keep the timeline on the left third of the slide, around x=300–350, so the right two-thirds remain available for agenda content.
- Use evenly spaced vertical positions for markers; the visual rhythm is what makes the agenda feel structured and intentional.
- Let the marker gradient carry the progression: light at the top, dark at the bottom, with neutral gray text to avoid color overload.
- Preserve generous white space around the title and between agenda blocks; this layout should feel executive and calm, not like a dense checklist.