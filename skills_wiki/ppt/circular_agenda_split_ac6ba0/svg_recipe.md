# SVG Recipe — Circular Agenda Split

## Visual mechanism
A bold cluster of overlapping circles anchors the left side, with one circle acting as a photo crop and surrounding circles creating playful motion. The right side stays calm and structured: a section-number pill, headline, and stacked agenda items aligned on a clean vertical rhythm.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<linearGradient>` for the warm circular field and cool accent circle
- 1× `<radialGradient>` for the image-ring glow / depth accent
- 1× `<filter id="softShadow">` applied to circles and cards for dimensional lift
- 1× `<clipPath>` with `<circle>` applied only to the hero `<image>`
- 1× `<image>` clipped into a circular hero photo
- 7× `<circle>` for overlapping circular agenda motif, image frame, accents, and numbered agenda bullets
- 1× `<path>` for an organic background swoosh behind the circle cluster
- 1× `<rect>` for the section-number pill
- 5× `<line>` for subtle agenda separators
- 12× `<text>` elements for kicker, title, section number, section title, agenda numbers, and agenda item labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#FFF7EC"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F7FF"/>
    </linearGradient>

    <linearGradient id="sunsetCircle" x1="80" y1="120" x2="520" y2="600">
      <stop offset="0%" stop-color="#FFB84D"/>
      <stop offset="48%" stop-color="#FF6B4A"/>
      <stop offset="100%" stop-color="#D9348C"/>
    </linearGradient>

    <linearGradient id="blueCircle" x1="120" y1="520" x2="480" y2="180">
      <stop offset="0%" stop-color="#1E63FF"/>
      <stop offset="100%" stop-color="#35D3FF"/>
    </linearGradient>

    <radialGradient id="photoHalo" cx="50%" cy="45%" r="62%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.18"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.08  0 0 0 0 0.10  0 0 0 0 0.16  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroCircleClip">
      <circle cx="330" cy="345" r="150"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-80,520 C70,420 115,210 255,150 C405,85 548,165 575,315 C603,475 480,630 290,682 C138,724 12,664 -80,620 Z"
        fill="#FCE7F3" opacity="0.72"/>

  <circle cx="255" cy="370" r="245" fill="url(#sunsetCircle)" filter="url(#softShadow)"/>
  <circle cx="165" cy="220" r="88" fill="#FFFFFF" opacity="0.32"/>
  <circle cx="485" cy="520" r="112" fill="url(#blueCircle)" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="500" cy="180" r="46" fill="#111827" opacity="0.08"/>
  <circle cx="105" cy="555" r="34" fill="#FFD166" opacity="0.95"/>

  <circle cx="330" cy="345" r="164" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero/diverse-team-strategy-workshop-square.jpg"
         x="180" y="195" width="300" height="300"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroCircleClip)"/>
  <circle cx="330" cy="345" r="150" fill="url(#photoHalo)" opacity="0.9"/>
  <circle cx="330" cy="345" r="151" fill="none" stroke="#FFFFFF" stroke-width="7"/>

  <text x="84" y="92" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="2.5" fill="#FFFFFF" opacity="0.95">
    STRATEGY WORKSHOP
  </text>

  <text x="78" y="590" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#FFFFFF">
    <tspan x="78" dy="0">Circular</tspan>
    <tspan x="78" dy="58">Agenda Split</tspan>
  </text>

  <rect x="680" y="78" width="118" height="44" rx="22" fill="#111827"/>
  <text x="708" y="107" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    03
  </text>

  <text x="680" y="172" width="465" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="800" fill="#111827">
    <tspan x="680" dy="0">Today’s</tspan>
    <tspan x="680" dy="56" fill="#FF6B4A">Operating Plan</tspan>
  </text>

  <text x="682" y="285" width="440" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#6B7280">
    Five focused conversations to move from ambition to accountable execution.
  </text>

  <line x1="682" y1="345" x2="1165" y2="345" stroke="#D8DEE9" stroke-width="1.4" stroke-dasharray="6 8"/>
  <circle cx="704" cy="382" r="19" fill="#FF6B4A"/>
  <text x="696" y="389" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" fill="#FFFFFF">1</text>
  <text x="744" y="389" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#111827">Market signals and strategic context</text>

  <line x1="682" y1="426" x2="1165" y2="426" stroke="#D8DEE9" stroke-width="1.4" stroke-dasharray="6 8"/>
  <circle cx="704" cy="463" r="19" fill="#2563EB"/>
  <text x="696" y="470" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" fill="#FFFFFF">2</text>
  <text x="744" y="470" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#111827">Customer journey friction points</text>

  <line x1="682" y1="507" x2="1165" y2="507" stroke="#D8DEE9" stroke-width="1.4" stroke-dasharray="6 8"/>
  <circle cx="704" cy="544" r="19" fill="#F59E0B"/>
  <text x="696" y="551" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" fill="#FFFFFF">3</text>
  <text x="744" y="551" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#111827">Portfolio choices and investment guardrails</text>

  <line x1="682" y1="588" x2="1165" y2="588" stroke="#D8DEE9" stroke-width="1.4" stroke-dasharray="6 8"/>
  <circle cx="704" cy="625" r="19" fill="#10B981"/>
  <text x="696" y="632" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" fill="#FFFFFF">4</text>
  <text x="744" y="632" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" fill="#111827">Next 90 days: owners, milestones, cadence</text>
</svg>
```

## Avoid in this skill
- ❌ Clipping the entire left circle cluster with `clip-path`; only apply clipping to the hero `<image>`.
- ❌ Using `<mask>` to blend the overlapping circles; use opacity, gradients, and layering instead.
- ❌ Building the agenda as a plain table grid; the visual identity comes from circular bullets and airy separators.
- ❌ Putting shadows on `<line>` separators; filters on lines are dropped, so keep lines flat.
- ❌ Overfilling the left circle area with text; reserve it for the title plus image-driven focal point.

## Composition notes
- Keep the circular motif within the left 45% of the slide, allowing it to bleed slightly off-canvas for energy.
- Place the agenda content in the right 50%, aligned to a strong vertical axis with generous row spacing.
- Use one warm dominant circle, one cool secondary circle, and small neutral accents to create color rhythm.
- The photo circle should be the visual anchor; agenda text should remain high-contrast, simple, and editorial.