# SVG Recipe — Precision Fragmented Ring Infographic

## Visual mechanism
A thick donut ring is split into mathematically precise arc fragments with clean negative-space gaps, turning a “parts of a whole” idea into four editable, premium-looking geometric containers. Satellite labels orbit the ring at the centroid of each segment, while a central hub anchors the message.

## SVG primitives needed
- 1× `<rect>` for the deep navy slide background
- 4× `<path>` for the editable annular ring fragments with exact angular gaps
- 4× `<linearGradient>` for vivid segment fills with subtle depth
- 1× `<radialGradient>` for the soft central glow behind the ring
- 1× `<filter id="softShadow">` applied to ring fragments and cards
- 1× `<filter id="glow">` applied to decorative glow ellipses
- 4× `<line>` for thin leader connectors from ring to labels
- 8× `<circle>` for connector anchor dots and central detail accents
- 4× `<rect>` for rounded satellite text cards
- 1× `<circle>` for the central hub
- Multiple `<text>` elements with explicit `width` attributes for editable title, center label, and card copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="centerAura" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.24"/>
      <stop offset="52%" stop-color="#6366f1" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="segTeal" x1="560" y1="240" x2="790" y2="420">
      <stop offset="0%" stop-color="#5eead4"/>
      <stop offset="100%" stop-color="#14b8a6"/>
    </linearGradient>
    <linearGradient id="segBlue" x1="790" y1="370" x2="620" y2="560">
      <stop offset="0%" stop-color="#7dd3fc"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <linearGradient id="segIndigo" x1="660" y1="560" x2="480" y2="380">
      <stop offset="0%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#4f46e5"/>
    </linearGradient>
    <linearGradient id="segPurple" x1="490" y1="370" x2="650" y2="230">
      <stop offset="0%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#9333ea"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="20"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0f172a"/>

  <ellipse cx="640" cy="390" rx="245" ry="245" fill="url(#centerAura)" filter="url(#glow)"/>
  <ellipse cx="260" cy="160" rx="160" ry="70" fill="#1e3a8a" opacity="0.16" filter="url(#glow)"/>
  <ellipse cx="1045" cy="590" rx="180" ry="80" fill="#7e22ce" opacity="0.14" filter="url(#glow)"/>

  <text x="80" y="72" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#f8fafc" letter-spacing="1.6">
    CORE STRATEGY PILLARS
  </text>
  <text x="82" y="110" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#94a3b8">
    Four precision fragments show how the operating model converts focus into measurable execution.
  </text>

  <!-- Fragmented donut ring: center 640,390; outer radius 152; inner radius 92; 8° gaps -->
  <path filter="url(#softShadow)" fill="url(#segTeal)"
        d="M 650.6 238.4
           A 152 152 0 0 1 791.6 379.4
           L 731.8 383.6
           A 92 92 0 0 0 646.4 298.2
           Z"/>
  <path filter="url(#softShadow)" fill="url(#segBlue)"
        d="M 791.6 400.6
           A 152 152 0 0 1 650.6 541.6
           L 646.4 481.8
           A 92 92 0 0 0 731.8 396.4
           Z"/>
  <path filter="url(#softShadow)" fill="url(#segIndigo)"
        d="M 629.4 541.6
           A 152 152 0 0 1 488.4 400.6
           L 548.2 396.4
           A 92 92 0 0 0 633.6 481.8
           Z"/>
  <path filter="url(#softShadow)" fill="url(#segPurple)"
        d="M 488.4 379.4
           A 152 152 0 0 1 629.4 238.4
           L 633.6 298.2
           A 92 92 0 0 0 548.2 383.6
           Z"/>

  <circle cx="640" cy="390" r="72" fill="#111827" stroke="#334155" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="640" cy="390" r="48" fill="#172033" stroke="#38bdf8" stroke-opacity="0.45" stroke-width="1.5"/>
  <text x="574" y="374" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#94a3b8" letter-spacing="1.2">
    OPERATING
  </text>
  <text x="574" y="402" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#ffffff">
    MODEL
  </text>
  <text x="574" y="426" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748b">
    2026 focus system
  </text>

  <!-- Leader lines and anchor dots -->
  <line x1="735" y1="295" x2="865" y2="205" stroke="#2dd4bf" stroke-width="1.6" opacity="0.75"/>
  <circle cx="735" cy="295" r="4" fill="#2dd4bf"/>
  <circle cx="865" cy="205" r="4" fill="#2dd4bf"/>

  <line x1="735" y1="485" x2="870" y2="555" stroke="#38bdf8" stroke-width="1.6" opacity="0.75"/>
  <circle cx="735" cy="485" r="4" fill="#38bdf8"/>
  <circle cx="870" cy="555" r="4" fill="#38bdf8"/>

  <line x1="545" y1="485" x2="410" y2="555" stroke="#6366f1" stroke-width="1.6" opacity="0.75"/>
  <circle cx="545" cy="485" r="4" fill="#6366f1"/>
  <circle cx="410" cy="555" r="4" fill="#6366f1"/>

  <line x1="545" y1="295" x2="410" y2="205" stroke="#a855f7" stroke-width="1.6" opacity="0.75"/>
  <circle cx="545" cy="295" r="4" fill="#a855f7"/>
  <circle cx="410" cy="205" r="4" fill="#a855f7"/>

  <!-- Satellite cards -->
  <rect x="865" y="150" width="270" height="110" rx="22" fill="#111827" stroke="#2dd4bf" stroke-opacity="0.42" filter="url(#softShadow)"/>
  <text x="895" y="190" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#f8fafc">Market Signal</text>
  <text x="895" y="221" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94a3b8">Track the category shifts that shape demand, pricing, and timing.</text>

  <rect x="870" y="515" width="270" height="110" rx="22" fill="#111827" stroke="#38bdf8" stroke-opacity="0.42" filter="url(#softShadow)"/>
  <text x="900" y="555" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#f8fafc">Product Velocity</text>
  <text x="900" y="586" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94a3b8">Compress cycle time with modular decisions and sharper release gates.</text>

  <rect x="140" y="515" width="270" height="110" rx="22" fill="#111827" stroke="#6366f1" stroke-opacity="0.42" filter="url(#softShadow)"/>
  <text x="170" y="555" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#f8fafc">Scale Engine</text>
  <text x="170" y="586" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94a3b8">Turn repeatable plays into operating leverage across channels.</text>

  <rect x="140" y="150" width="270" height="110" rx="22" fill="#111827" stroke="#a855f7" stroke-opacity="0.42" filter="url(#softShadow)"/>
  <text x="170" y="190" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#f8fafc">Talent System</text>
  <text x="170" y="221" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#94a3b8">Align roles, rituals, and incentives around the strategic cadence.</text>
</svg>
```

## Avoid in this skill
- ❌ Using a raster donut image for the ring; it will not remain editable as individual PowerPoint shapes.
- ❌ Drawing the ring as thick stroked arcs with rounded caps if you need crisp fragment-cut geometry; use filled annular `<path>` sectors instead.
- ❌ Using `<mask>` or `clip-path` on the ring paths to punch gaps; define the gaps directly in the path coordinates.
- ❌ Putting `filter` on `<line>` leader connectors; shadows on lines are dropped by the translator.
- ❌ Using `<use>` to repeat cards or dots; duplicate the native elements explicitly.

## Composition notes
- Keep the fragmented ring centered and sized around 300–340 px diameter so the negative-space gaps remain visible from the back of a room.
- Place satellite cards at the four diagonal quadrants, aligned to the visual centroid of each arc fragment rather than to the slide edges.
- Use a dark, quiet background so the categorical segment colors carry the hierarchy.
- Leave generous empty space between the ring and labels; the leader lines should feel precise, not crowded.