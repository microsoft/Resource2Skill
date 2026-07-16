# SVG Recipe — Continuous Flow Animated Diagram

## Visual mechanism
A dark technical schematic uses static glowing “pipes” as the structural diagram, then overlays transparent looping GIF strips of cyan chevrons to simulate uninterrupted data or energy flow. Opaque processor blocks sit above the animated strips so the motion appears to enter and exit components cleanly.

## SVG primitives needed
- 1× `<rect>` for the deep navy slide background
- 8–12× `<line>` for a subtle blueprint/grid texture
- 4× `<path>` for the main glowing circuit / flow routes
- 4× `<image>` for transparent looping arrow GIF strips placed directly over the routes
- 4× `<clipPath>` using rounded `<rect>` shapes to constrain GIF strips to pipe corridors
- 5× `<rect>` for opaque system/component blocks layered above the flow
- 5× `<circle>` or `<ellipse>` for node ports and pulse halos
- 3× `<linearGradient>` for background, node fills, and pipe highlights
- 2× `<filter>` with `feGaussianBlur` / `feOffset` / `feMerge` for neon glow and component shadows
- 8–12× `<text>` with explicit `width` attributes for title, labels, metrics, and callouts
- Optional editable `<path>` chevrons as a non-animated fallback or visual echo around the GIF flow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1220"/>
      <stop offset="55%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <linearGradient id="nodeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E3A5F"/>
      <stop offset="50%" stop-color="#17233A"/>
      <stop offset="100%" stop-color="#0B1220"/>
    </linearGradient>

    <linearGradient id="pipeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0891B2"/>
      <stop offset="45%" stop-color="#22D3EE"/>
      <stop offset="100%" stop-color="#67E8F9"/>
    </linearGradient>

    <filter id="neonGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipTopFlow">
      <rect x="260" y="224" width="700" height="56" rx="28"/>
    </clipPath>
    <clipPath id="clipMidFlow">
      <rect x="260" y="354" width="700" height="56" rx="28"/>
    </clipPath>
    <clipPath id="clipLeftVertical">
      <rect x="324" y="250" width="56" height="135" rx="28"/>
    </clipPath>
    <clipPath id="clipRightVertical">
      <rect x="902" y="250" width="56" height="135" rx="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <line x1="80" y1="120" x2="1200" y2="120" stroke="#1E293B" stroke-width="1"/>
  <line x1="80" y1="240" x2="1200" y2="240" stroke="#1E293B" stroke-width="1"/>
  <line x1="80" y1="360" x2="1200" y2="360" stroke="#1E293B" stroke-width="1"/>
  <line x1="80" y1="480" x2="1200" y2="480" stroke="#1E293B" stroke-width="1"/>
  <line x1="200" y1="90" x2="200" y2="620" stroke="#1E293B" stroke-width="1"/>
  <line x1="480" y1="90" x2="480" y2="620" stroke="#1E293B" stroke-width="1"/>
  <line x1="760" y1="90" x2="760" y2="620" stroke="#1E293B" stroke-width="1"/>
  <line x1="1040" y1="90" x2="1040" y2="620" stroke="#1E293B" stroke-width="1"/>

  <text x="74" y="72" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F8FAFC">Continuous Flow Animation Layer</text>
  <text x="76" y="108" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#94A3B8">Transparent looping GIF strips ride above static SVG pipes and below opaque component blocks.</text>

  <path d="M 214 252 L 1036 252" fill="none" stroke="#155E75" stroke-width="24" stroke-linecap="round" opacity="0.75"/>
  <path d="M 214 382 L 1036 382" fill="none" stroke="#155E75" stroke-width="24" stroke-linecap="round" opacity="0.75"/>
  <path d="M 352 252 C 352 294 352 336 352 382" fill="none" stroke="#155E75" stroke-width="24" stroke-linecap="round" opacity="0.75"/>
  <path d="M 930 252 C 930 294 930 336 930 382" fill="none" stroke="#155E75" stroke-width="24" stroke-linecap="round" opacity="0.75"/>

  <path d="M 214 252 L 1036 252" fill="none" stroke="url(#pipeGrad)" stroke-width="7" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M 214 382 L 1036 382" fill="none" stroke="url(#pipeGrad)" stroke-width="7" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M 352 252 C 352 294 352 336 352 382" fill="none" stroke="#22D3EE" stroke-width="7" stroke-linecap="round" filter="url(#neonGlow)"/>
  <path d="M 930 252 C 930 294 930 336 930 382" fill="none" stroke="#22D3EE" stroke-width="7" stroke-linecap="round" filter="url(#neonGlow)"/>

  <image x="260" y="224" width="700" height="56" clip-path="url(#clipTopFlow)"
         href="https://assets.example.com/flow/transparent-looping-cyan-chevron-strip-horizontal-700x56.gif"/>
  <image x="260" y="354" width="700" height="56" clip-path="url(#clipMidFlow)"
         href="https://assets.example.com/flow/transparent-looping-cyan-chevron-strip-horizontal-reverse-700x56.gif"/>
  <image x="324" y="250" width="56" height="135" clip-path="url(#clipLeftVertical)"
         href="https://assets.example.com/flow/transparent-looping-cyan-chevron-strip-vertical-down-56x135.gif"/>
  <image x="902" y="250" width="56" height="135" clip-path="url(#clipRightVertical)"
         href="https://assets.example.com/flow/transparent-looping-cyan-chevron-strip-vertical-up-56x135.gif"/>

  <circle cx="214" cy="252" r="22" fill="#22D3EE" opacity="0.12" filter="url(#neonGlow)"/>
  <circle cx="1036" cy="252" r="22" fill="#22D3EE" opacity="0.12" filter="url(#neonGlow)"/>
  <circle cx="214" cy="382" r="22" fill="#22D3EE" opacity="0.12" filter="url(#neonGlow)"/>
  <circle cx="1036" cy="382" r="22" fill="#22D3EE" opacity="0.12" filter="url(#neonGlow)"/>

  <rect x="104" y="198" width="210" height="108" rx="24" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="486" y="176" width="308" height="152" rx="28" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="966" y="198" width="210" height="108" rx="24" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="104" y="328" width="210" height="108" rx="24" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="966" y="328" width="210" height="108" rx="24" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="1.5" filter="url(#cardShadow)"/>

  <text x="134" y="236" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E0F2FE">SOURCE A</text>
  <text x="134" y="262" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">42 MW</text>
  <text x="518" y="226" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E0F2FE">REAL-TIME CONTROL CORE</text>
  <text x="518" y="260" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94A3B8">Routes, balances, and continuously monitors bidirectional throughput.</text>
  <text x="996" y="236" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E0F2FE">LOAD CLUSTER</text>
  <text x="996" y="262" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">87%</text>
  <text x="134" y="366" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E0F2FE">BUFFER</text>
  <text x="134" y="392" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">12 ms</text>
  <text x="996" y="366" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E0F2FE">SINK B</text>
  <text x="996" y="392" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">LIVE</text>

  <path d="M 612 474 L 642 492 L 612 510" fill="none" stroke="#22D3EE" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.6" filter="url(#neonGlow)"/>
  <path d="M 666 474 L 696 492 L 666 510" fill="none" stroke="#22D3EE" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.35" filter="url(#neonGlow)"/>
  <text x="424" y="560" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="15" text-anchor="middle" fill="#CBD5E1">Layer order: background → static pipes → animated GIF flow → opaque nodes</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` to create the movement; these hard-fail translation and should be replaced by transparent looping GIF strips embedded as `<image>`.
- ❌ Do not use `marker-end` arrowheads on `<path>` routes; if you need editable static arrows, draw chevrons manually with small `<path>` polygons or strokes.
- ❌ Do not place `filter` on `<line>` grid elements; use filters only on `<rect>`, `<circle>`, `<ellipse>`, `<path>`, or `<text>`.
- ❌ Do not apply `clip-path` to the glowing pipe `<path>` itself; clipping is reliable only on `<image>`, so clip the animated GIF strips instead.
- ❌ Do not let animated strips sit above component blocks; it destroys the illusion that flow emerges from inside the system.

## Composition notes
- Keep the animated GIF corridors exactly aligned to the underlying static pipe geometry; even a 2–3 px mismatch makes the flow feel detached.
- Use dark negative space and restrained grid lines so the neon flow remains the visual focus.
- Layer opaque node cards above the GIFs to hide strip seams and create clean “entry/exit” points.
- For seamless loops, design GIF strip widths as exact multiples of the chevron spacing, e.g. 700 px wide with 100 px spacing.