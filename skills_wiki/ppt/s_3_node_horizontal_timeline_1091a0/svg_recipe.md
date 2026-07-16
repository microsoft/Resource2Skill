# SVG Recipe — 3-Node Horizontal Timeline

## Visual mechanism
A clean horizontal spine carries three prominent milestone nodes, each dropping into a compact detail card below. Subtle gradients, glow rings, and faint technical background paths make the timeline feel premium while preserving the simple left-to-right sequence.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<path>` for a soft abstract background glow shape
- 6× `<path>` for faint technical/circuit accent lines and directional chevrons
- 1× `<line>` for the main horizontal timeline spine
- 3× `<line>` for vertical drop stems from nodes to cards
- 3× `<circle>` for outer node glow halos
- 3× `<circle>` for primary filled milestone nodes
- 3× `<circle>` for inner node highlights
- 3× `<rect>` for rounded detail cards
- 3× `<rect>` for small accent tabs on each card
- Multiple `<text>` elements with explicit `width` for kicker, headline, node numbers, stage labels, and supporting details
- 2× `<linearGradient>` for background and card fills
- 1× `<radialGradient>` for the abstract glow
- 2× `<filter>` definitions: one shadow for cards, one soft glow for node halos

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="55%" stop-color="#0D1930"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#16243C"/>
      <stop offset="100%" stop-color="#0E1728"/>
    </linearGradient>
    <linearGradient id="spineGrad" x1="210" y1="0" x2="1070" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#22C55E"/>
    </linearGradient>
    <radialGradient id="haloGrad" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="nodeGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-40,470 C150,360 250,450 420,330 C590,210 745,280 890,185 C1040,88 1160,120 1320,35 L1320,720 L-40,720 Z"
        fill="url(#haloGrad)" opacity="0.55"/>

  <path d="M88,142 H212 V184 H326" fill="none" stroke="#253A5C" stroke-width="2" opacity="0.45"/>
  <path d="M958,120 H1095 V168 H1190" fill="none" stroke="#253A5C" stroke-width="2" opacity="0.38"/>
  <path d="M135,600 H285 V560 H390" fill="none" stroke="#253A5C" stroke-width="2" opacity="0.34"/>
  <path d="M1030,585 H1138 V535 H1212" fill="none" stroke="#253A5C" stroke-width="2" opacity="0.3"/>

  <text x="80" y="78" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.4" fill="#38BDF8">THREE-STAGE ROADMAP</text>
  <text x="80" y="126" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#F8FAFC">From signal to scalable motion</text>
  <text x="82" y="158" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#94A3B8">A concise horizontal timeline for three distinct events, phases, or decision gates.</text>

  <line x1="210" y1="300" x2="1070" y2="300" stroke="url(#spineGrad)" stroke-width="6" stroke-linecap="round"/>
  <line x1="210" y1="300" x2="1070" y2="300" stroke="#E0F2FE" stroke-width="1.5" stroke-dasharray="4 18" opacity="0.75"/>

  <path d="M1085,300 L1065,288 L1065,312 Z" fill="#22C55E"/>
  <path d="M632,286 L650,300 L632,314" fill="none" stroke="#CBD5E1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
  <path d="M918,286 L936,300 L918,314" fill="none" stroke="#CBD5E1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>

  <line x1="260" y1="330" x2="260" y2="378" stroke="#38BDF8" stroke-width="2" stroke-dasharray="5 7" opacity="0.8"/>
  <line x1="640" y1="330" x2="640" y2="378" stroke="#A78BFA" stroke-width="2" stroke-dasharray="5 7" opacity="0.8"/>
  <line x1="1020" y1="330" x2="1020" y2="378" stroke="#22C55E" stroke-width="2" stroke-dasharray="5 7" opacity="0.8"/>

  <circle cx="260" cy="300" r="48" fill="#38BDF8" opacity="0.22" filter="url(#nodeGlow)"/>
  <circle cx="640" cy="300" r="48" fill="#A78BFA" opacity="0.22" filter="url(#nodeGlow)"/>
  <circle cx="1020" cy="300" r="48" fill="#22C55E" opacity="0.22" filter="url(#nodeGlow)"/>

  <circle cx="260" cy="300" r="31" fill="#0B1220" stroke="#38BDF8" stroke-width="5"/>
  <circle cx="640" cy="300" r="31" fill="#0B1220" stroke="#A78BFA" stroke-width="5"/>
  <circle cx="1020" cy="300" r="31" fill="#0B1220" stroke="#22C55E" stroke-width="5"/>

  <circle cx="260" cy="300" r="12" fill="#38BDF8"/>
  <circle cx="640" cy="300" r="12" fill="#A78BFA"/>
  <circle cx="1020" cy="300" r="12" fill="#22C55E"/>

  <text x="260" y="252" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#BAE6FD">Q1</text>
  <text x="640" y="252" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#DDD6FE">Q2</text>
  <text x="1020" y="252" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#BBF7D0">Q3</text>

  <rect x="140" y="378" width="240" height="176" rx="24" fill="url(#cardGrad)" stroke="#274568" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="520" y="378" width="240" height="176" rx="24" fill="url(#cardGrad)" stroke="#3D356B" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="900" y="378" width="240" height="176" rx="24" fill="url(#cardGrad)" stroke="#24563A" stroke-width="1.2" filter="url(#cardShadow)"/>

  <rect x="164" y="402" width="52" height="6" rx="3" fill="#38BDF8"/>
  <rect x="544" y="402" width="52" height="6" rx="3" fill="#A78BFA"/>
  <rect x="924" y="402" width="52" height="6" rx="3" fill="#22C55E"/>

  <text x="164" y="440" width="192" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#F8FAFC">Discover</text>
  <text x="164" y="474" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#CBD5E1">
    <tspan x="164" dy="0">Map customer signals,</tspan>
    <tspan x="164" dy="22">identify unmet needs,</tspan>
    <tspan x="164" dy="22">and define the brief.</tspan>
  </text>

  <text x="544" y="440" width="192" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#F8FAFC">Validate</text>
  <text x="544" y="474" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#CBD5E1">
    <tspan x="544" dy="0">Prototype the solution,</tspan>
    <tspan x="544" dy="22">test assumptions, and</tspan>
    <tspan x="544" dy="22">lock the operating model.</tspan>
  </text>

  <text x="924" y="440" width="192" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#F8FAFC">Scale</text>
  <text x="924" y="474" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#CBD5E1">
    <tspan x="924" dy="0">Launch the roadmap,</tspan>
    <tspan x="924" dy="22">measure adoption, and</tspan>
    <tspan x="924" dy="22">expand what works.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` for the timeline arrow; draw the arrowhead as a small `<path>` instead.
- ❌ Applying filters to `<line>` elements; use unfiltered lines for the spine/stems and filtered circles or rects for glow/shadow.
- ❌ Relying on automatic text wrapping; manually break supporting copy with `<tspan>` and always set `width` on every `<text>`.
- ❌ Overloading the slide with more than three cards or dense bullets; this layout works best as a low-density executive sequence.

## Composition notes
- Keep the main timeline spine around the vertical middle of the slide, with node labels above and detail cards dropping below.
- Use strong left-to-right color rhythm: cool blue for stage 1, violet for stage 2, green for stage 3.
- Reserve the top-left for the kicker, headline, and one-line context; avoid competing title blocks near the nodes.
- Let the card area occupy the lower third to half of the canvas, with generous gaps between cards so the sequence remains legible.