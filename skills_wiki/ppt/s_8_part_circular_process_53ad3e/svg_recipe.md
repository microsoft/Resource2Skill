# SVG Recipe — 8-Part Circular Process

## Visual mechanism
Create a segmented donut wheel made from eight editable annular wedge paths, with a central theme circle and eight numbered callout cards orbiting the diagram. Premium polish comes from gradient segment fills, subtle shadows, dashed connector lines, and a dark executive-style background.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 8× `<path>` for editable annular donut segments
- 1× `<circle>` for the center hub
- 8× `<circle>` for numbered badges placed on the ring
- 8× `<line>` for radial connector lines from the wheel to the callouts
- 8× `<rect>` for rounded callout cards
- 17× `<text>` for headline, subtitle, center label, segment numbers, and callout copy
- 8× `<linearGradient>` for distinct segment color fills
- 1× `<radialGradient>` for the dark background glow
- 1× `<filter id="softShadow">` for card, hub, and segment depth
- 1× `<filter id="textGlow">` for subtle center-label emphasis
- Optional decorative `<circle>` strokes for orbit rings and process rhythm

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="56%" cy="50%" r="68%">
      <stop offset="0%" stop-color="#173B5F"/>
      <stop offset="54%" stop-color="#0B1728"/>
      <stop offset="100%" stop-color="#050914"/>
    </radialGradient>

    <linearGradient id="seg1" x1="620" y1="170" x2="820" y2="270"><stop offset="0%" stop-color="#6EE7F9"/><stop offset="100%" stop-color="#2B7FFF"/></linearGradient>
    <linearGradient id="seg2" x1="790" y1="180" x2="940" y2="320"><stop offset="0%" stop-color="#7DD3FC"/><stop offset="100%" stop-color="#2563EB"/></linearGradient>
    <linearGradient id="seg3" x1="830" y1="310" x2="950" y2="480"><stop offset="0%" stop-color="#A78BFA"/><stop offset="100%" stop-color="#6D28D9"/></linearGradient>
    <linearGradient id="seg4" x1="800" y1="480" x2="900" y2="600"><stop offset="0%" stop-color="#F0ABFC"/><stop offset="100%" stop-color="#C026D3"/></linearGradient>
    <linearGradient id="seg5" x1="650" y1="510" x2="760" y2="610"><stop offset="0%" stop-color="#FDBA74"/><stop offset="100%" stop-color="#EA580C"/></linearGradient>
    <linearGradient id="seg6" x1="500" y1="470" x2="640" y2="590"><stop offset="0%" stop-color="#FDE047"/><stop offset="100%" stop-color="#CA8A04"/></linearGradient>
    <linearGradient id="seg7" x1="490" y1="300" x2="620" y2="450"><stop offset="0%" stop-color="#86EFAC"/><stop offset="100%" stop-color="#16A34A"/></linearGradient>
    <linearGradient id="seg8" x1="520" y1="170" x2="670" y2="310"><stop offset="0%" stop-color="#5EEAD4"/><stop offset="100%" stop-color="#0F766E"/></linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="720" cy="380" r="276" fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1.4" stroke-dasharray="6 10"/>
  <circle cx="720" cy="380" r="196" fill="none" stroke="#FFFFFF" stroke-opacity="0.06" stroke-width="1"/>

  <text x="72" y="86" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700" fill="#FFFFFF">
    Eight-part circular process
  </text>
  <text x="74" y="132" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#AFC3DA">
    Map the operating model as a continuous loop: eight distinct stages orbit one central strategic theme.
  </text>

  <path d="M644.8 173.2 A220 220 0 0 1 795.2 173.2 L761.0 267.2 A120 120 0 0 0 679.0 267.2 Z" fill="url(#seg1)" filter="url(#softShadow)"/>
  <path d="M813.0 180.7 A220 220 0 0 1 919.3 287.0 L828.8 329.3 A120 120 0 0 0 770.7 271.2 Z" fill="url(#seg2)" filter="url(#softShadow)"/>
  <path d="M926.8 304.8 A220 220 0 0 1 926.8 455.2 L832.8 421.0 A120 120 0 0 0 832.8 339.0 Z" fill="url(#seg3)" filter="url(#softShadow)"/>
  <path d="M919.3 473.0 A220 220 0 0 1 813.0 579.3 L770.7 488.8 A120 120 0 0 0 828.8 430.7 Z" fill="url(#seg4)" filter="url(#softShadow)"/>
  <path d="M795.2 586.8 A220 220 0 0 1 644.8 586.8 L679.0 492.8 A120 120 0 0 0 761.0 492.8 Z" fill="url(#seg5)" filter="url(#softShadow)"/>
  <path d="M627.0 579.3 A220 220 0 0 1 520.7 473.0 L611.2 430.7 A120 120 0 0 0 669.3 488.8 Z" fill="url(#seg6)" filter="url(#softShadow)"/>
  <path d="M513.2 455.2 A220 220 0 0 1 513.2 304.8 L607.2 339.0 A120 120 0 0 0 607.2 421.0 Z" fill="url(#seg7)" filter="url(#softShadow)"/>
  <path d="M520.7 287.0 A220 220 0 0 1 627.0 180.7 L669.3 271.2 A120 120 0 0 0 611.2 329.3 Z" fill="url(#seg8)" filter="url(#softShadow)"/>

  <circle cx="720" cy="380" r="104" fill="#07111F" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="720" cy="380" r="78" fill="#0E2239" stroke="#58D5FF" stroke-opacity="0.35" stroke-width="1.5"/>
  <text x="652" y="366" width="136" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF" filter="url(#textGlow)">
    CENTRAL THEME
  </text>
  <text x="660" y="392" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#9EC7E8">
    growth system
  </text>

  <line x1="720" y1="210" x2="720" y2="126" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="840" y1="260" x2="986" y2="176" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="890" y1="380" x2="1016" y2="380" stroke="#A78BFA" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="840" y1="500" x2="986" y2="584" stroke="#F0ABFC" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="720" y1="550" x2="720" y2="644" stroke="#FDBA74" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="600" y1="500" x2="454" y2="584" stroke="#FDE047" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="550" y1="380" x2="404" y2="380" stroke="#86EFAC" stroke-width="1.5" stroke-dasharray="4 5"/>
  <line x1="600" y1="260" x2="454" y2="176" stroke="#5EEAD4" stroke-width="1.5" stroke-dasharray="4 5"/>

  <rect x="620" y="72" width="200" height="74" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="988" y="128" width="218" height="82" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="1014" y="338" width="210" height="84" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="988" y="542" width="218" height="82" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="620" y="628" width="200" height="66" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="234" y="542" width="218" height="82" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="216" y="338" width="210" height="84" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="234" y="128" width="218" height="82" rx="18" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>

  <circle cx="720" cy="210" r="18" fill="#081322" stroke="#6EE7F9" stroke-width="2"/><text x="707" y="217" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">1</text>
  <circle cx="840" cy="260" r="18" fill="#081322" stroke="#7DD3FC" stroke-width="2"/><text x="827" y="267" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">2</text>
  <circle cx="890" cy="380" r="18" fill="#081322" stroke="#A78BFA" stroke-width="2"/><text x="877" y="387" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">3</text>
  <circle cx="840" cy="500" r="18" fill="#081322" stroke="#F0ABFC" stroke-width="2"/><text x="827" y="507" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">4</text>
  <circle cx="720" cy="550" r="18" fill="#081322" stroke="#FDBA74" stroke-width="2"/><text x="707" y="557" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">5</text>
  <circle cx="600" cy="500" r="18" fill="#081322" stroke="#FDE047" stroke-width="2"/><text x="587" y="507" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">6</text>
  <circle cx="550" cy="380" r="18" fill="#081322" stroke="#86EFAC" stroke-width="2"/><text x="537" y="387" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">7</text>
  <circle cx="600" cy="260" r="18" fill="#081322" stroke="#5EEAD4" stroke-width="2"/><text x="587" y="267" width="26" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">8</text>

  <text x="642" y="100" width="156" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Discover</text>
  <text x="642" y="122" width="156" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Surface signals and unmet needs.</text>
  <text x="1012" y="158" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Prioritize</text>
  <text x="1012" y="181" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Rank initiatives by value and urgency.</text>
  <text x="1038" y="368" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Design</text>
  <text x="1038" y="391" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Shape the solution and experience.</text>
  <text x="1012" y="572" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Launch</text>
  <text x="1012" y="595" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Activate pilots and market motions.</text>
  <text x="642" y="654" width="156" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Measure</text>
  <text x="642" y="676" width="156" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Track impact against success metrics.</text>
  <text x="258" y="572" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Optimize</text>
  <text x="258" y="595" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Tune costs, workflows, and quality.</text>
  <text x="240" y="368" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Scale</text>
  <text x="240" y="391" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Expand adoption across the system.</text>
  <text x="258" y="158" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Renew</text>
  <text x="258" y="181" width="168" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#BFD0E3">Feed learnings into the next cycle.</text>
</svg>
```

## Avoid in this skill
- ❌ Building the donut with `<mask>` or clipping non-image shapes; use explicit annular wedge `<path>` geometry instead.
- ❌ Using `<use>` to duplicate badges, cards, or segments; duplicate the editable shapes directly.
- ❌ Applying `marker-end` to connector paths; use plain `<line>` connectors or draw arrowheads manually as small paths if needed.
- ❌ Letting text auto-size implicitly; every `<text>` needs a `width` attribute for predictable PowerPoint rendering.
- ❌ Making all eight wedges the same color; the process becomes hard to scan and loses its segmented meaning.

## Composition notes
- Keep the wheel slightly right of center if the slide needs a headline block; keep it centered if the diagram is the entire story.
- Use 4–8 px angular gaps between wedge paths so each process step reads as a separate editable object.
- Place short labels outside the ring, not inside the segments, when copy exceeds 1–2 words.
- Use a restrained color rhythm: cool colors across the top/right, warm colors near the bottom, green/teal returning to the start to imply cycle completion.