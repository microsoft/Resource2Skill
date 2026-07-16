# SVG Recipe — Geometric Hero Cover

## Visual mechanism
A full-bleed hero photograph is partially veiled by oversized diagonal polygons, creating a sharp editorial “glass shard” text zone. Dark navy facets provide legibility while translucent accent triangles add depth, motion, and premium keynote drama.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph, clipped to the slide bounds
- 1× `<clipPath>` with a `<rect>` for safe full-slide image cropping
- 2× `<rect>` for global dimming/vignette overlays
- 6× `<path>` for large diagonal geometric panels and accent shards
- 4× `<linearGradient>` for dark panel depth, cool accent facets, warm highlight, and vignette
- 2× `<filter>` for soft panel shadow and accent glow
- 5× `<text>` elements with explicit `width` for eyebrow, headline, subtitle, metadata, and small label
- 1× `<line>` for a crisp editorial divider

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="slideClip">
      <rect x="0" y="0" width="1280" height="720"/>
    </clipPath>

    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.20"/>
      <stop offset="45%" stop-color="#020617" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.76"/>
    </linearGradient>

    <linearGradient id="darkFacet" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F" stop-opacity="0.94"/>
      <stop offset="55%" stop-color="#0B1D35" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.98"/>
    </linearGradient>

    <linearGradient id="blueFacet" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#39D5FF" stop-opacity="0.64"/>
      <stop offset="100%" stop-color="#2563EB" stop-opacity="0.16"/>
    </linearGradient>

    <linearGradient id="amberFacet" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.86"/>
      <stop offset="100%" stop-color="#F97316" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="facetShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-18" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <image href="https://images.example.com/hero-photo-modern-glass-building-at-dusk.jpg"
         x="0" y="0" width="1280" height="720"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#slideClip)"/>

  <rect x="0" y="0" width="1280" height="720" fill="#020617" opacity="0.22"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M520 0 L1280 0 L1280 720 L390 720 L610 370 Z"
        fill="url(#darkFacet)" filter="url(#facetShadow)"/>

  <path d="M720 0 L1280 0 L1280 210 L870 168 Z"
        fill="#0F2A47" opacity="0.72"/>

  <path d="M1040 720 L1280 720 L1280 380 L910 515 Z"
        fill="#030712" opacity="0.56"/>

  <path d="M660 70 L842 0 L1055 0 L756 240 Z"
        fill="url(#blueFacet)" opacity="0.70" filter="url(#accentGlow)"/>

  <path d="M1035 145 L1280 62 L1280 178 L1116 266 Z"
        fill="url(#amberFacet)" opacity="0.82"/>

  <path d="M430 720 L0 720 L0 592 L520 520 Z"
        fill="#07111F" opacity="0.58"/>

  <path d="M0 0 L245 0 L0 155 Z"
        fill="#38BDF8" opacity="0.18"/>

  <line x1="704" y1="220" x2="790" y2="220"
        stroke="#38BDF8" stroke-width="5" stroke-linecap="round"/>

  <text x="704" y="188" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4"
        fill="#7DD3FC">EXECUTIVE BRIEFING</text>

  <text x="704" y="286" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        fill="#FFFFFF">
    <tspan x="704" dy="0">Geometric</tspan>
    <tspan x="704" dy="68">Growth Strategy</tspan>
  </text>

  <text x="708" y="438" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#CBD5E1">
    <tspan x="708" dy="0">Building a sharper operating model</tspan>
    <tspan x="708" dy="34">for the next market cycle</tspan>
  </text>

  <text x="708" y="600" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600"
        fill="#93C5FD">Q4 LEADERSHIP OFFSITE</text>

  <text x="708" y="628" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        fill="#94A3B8">New York · October 2026</text>
</svg>
```

## Avoid in this skill
- ❌ Clipping the geometric overlay shapes; only apply `clip-path` to the hero `<image>` so the facets remain editable
- ❌ Using a plain rectangle as the only overlay; the technique depends on angled polygonal paths for drama
- ❌ Placing text directly on the photo without a dark facet behind it; contrast will vary by image
- ❌ Overusing many tiny triangles; keep the shard system bold and architectural rather than noisy

## Composition notes
- Put the main text inside the darkest diagonal facet, usually on the right half or lower-right third of the slide.
- Let the hero photo remain visible on the opposite side; the photograph should still read as a full-bleed cinematic background.
- Use one cool accent shard and one warm micro-highlight to create rhythm without competing with the headline.
- Keep the headline large, high-contrast, and left-aligned within the angled panel for a premium editorial cover feel.