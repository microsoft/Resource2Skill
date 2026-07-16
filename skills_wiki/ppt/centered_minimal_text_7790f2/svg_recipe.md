# SVG Recipe — Centered Minimal Text

## Visual mechanism
A restrained editorial slide where one centered headline carries the message, supported by a small accent subhead and generous negative space. Subtle gradient fields, soft blurred halos, and hairline dividers add premium depth without competing with the typography.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 2× `<circle>` for soft radial glow fields behind the centered text
- 2× `<path>` for faint organic corner atmosphere / editorial texture
- 3× `<line>` for the minimal accent rule system around the subhead
- 4× `<text>` for eyebrow label, main headline, subhead, and quiet body copy
- 3× `<linearGradient>` for background and metallic accent strokes
- 2× `<radialGradient>` for soft luminous color blooms
- 2× `<filter>` using `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for atmospheric glow and refined text shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="0.52" stop-color="#0B1020"/>
      <stop offset="1" stop-color="#050816"/>
    </linearGradient>

    <linearGradient id="accentGold" x1="470" y1="0" x2="810" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B88A3B" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#F2C46D" stop-opacity="1"/>
      <stop offset="1" stop-color="#B88A3B" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="coolLine" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#60A5FA" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#93C5FD" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#60A5FA" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="blueGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#2563EB" stop-opacity="0.45"/>
      <stop offset="0.55" stop-color="#2563EB" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#2563EB" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="goldGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#F59E0B" stop-opacity="0.28"/>
      <stop offset="0.6" stop-color="#F59E0B" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#F59E0B" stop-opacity="0"/>
    </radialGradient>

    <filter id="atmosphericBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <filter id="softTextShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <circle cx="370" cy="205" r="230" fill="url(#blueGlow)" filter="url(#atmosphericBlur)" opacity="0.75"/>
  <circle cx="890" cy="505" r="250" fill="url(#goldGlow)" filter="url(#atmosphericBlur)" opacity="0.7"/>

  <path d="M-40,88 C88,10 205,34 292,118 C372,196 350,305 246,330 C130,358 16,276 -40,210 Z"
        fill="#1D4ED8" opacity="0.075" filter="url(#atmosphericBlur)"/>
  <path d="M1045,610 C1110,520 1218,502 1328,554 L1328,760 L990,760 C960,704 982,660 1045,610 Z"
        fill="#F59E0B" opacity="0.08" filter="url(#atmosphericBlur)"/>

  <line x1="410" y1="263" x2="535" y2="263" stroke="url(#accentGold)" stroke-width="1.6"/>
  <line x1="745" y1="263" x2="870" y2="263" stroke="url(#accentGold)" stroke-width="1.6"/>
  <line x1="280" y1="575" x2="1000" y2="575" stroke="url(#coolLine)" stroke-width="1"/>

  <text x="640" y="270" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="3.5"
        fill="#F2C46D">
    SECTION FOUR
  </text>

  <text x="640" y="360" width="940" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="700" letter-spacing="-1.8"
        fill="#F8FAFC" filter="url(#softTextShadow)">
    <tspan x="640">CLARITY AT</tspan>
    <tspan x="640" dy="72">THE CENTER</tspan>
  </text>

  <text x="640" y="485" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="500" letter-spacing="0.1"
        fill="#CBD5E1">
    A quiet slide for decisive moments.
  </text>

  <text x="640" y="535" width="660" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="400" fill="#94A3B8">
    <tspan x="640">Use the space around the message as an asset:</tspan>
    <tspan x="640" dy="23">one idea, one emphasis, one memorable pause.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Adding dense supporting charts, icon rows, or multi-column content; this layout depends on silence and focus.
- ❌ Using `<foreignObject>` for paragraph wrapping; keep all copy as native `<text>` with explicit `width`.
- ❌ Applying `filter` to `<line>` elements; use unfiltered hairlines and reserve blur/shadow for shapes or text.
- ❌ Centering every element mechanically with no hierarchy; the headline should dominate, while the subhead and body stay restrained.
- ❌ Overusing bright accent colors; one warm accent is enough for a minimal executive divider.

## Composition notes
- Keep the primary headline in the central 45–50% of the slide height, with wide margins on all sides.
- Use the accent subhead as a small typographic “pin” above the title, not as a competing second headline.
- Decorative glows should sit behind the text and remain low-opacity; they create atmosphere, not content.
- Leave the lower third mostly open, with only a short supporting sentence or closing thought.