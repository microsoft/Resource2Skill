# SVG Recipe — Cinematic Minimalist Title Card

## Visual mechanism
A pure-black, nearly empty slide uses small, muted-gray typography placed at the optical center to create a dramatic cinematic pause. Subtle vignette, restrained letterbox bands, and barely visible hairline rules add premium film-title polish without distracting from the phrase.

## SVG primitives needed
- 3× `<rect>` for the black base, soft vignette overlay, and subtle top/bottom letterbox bands
- 2× `<line>` for faint horizontal subtitle framing rules
- 2× `<path>` for near-invisible cinematic corner registration marks
- 3× `<text>` for the main title, subtitle/credit, and tiny classification line
- 1× `<radialGradient>` for the barely perceptible center glow on the black background
- 1× `<linearGradient>` for restrained gray title shading
- 1× `<filter id="textBloom">` with `feGaussianBlur`/`feMerge` applied to the main title for a soft projector-like bloom

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="blackVignette" cx="50%" cy="48%" r="72%">
      <stop offset="0%" stop-color="#0b0b0b"/>
      <stop offset="48%" stop-color="#050505"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="mutedTitle" x1="0" y1="260" x2="0" y2="420" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#b7b7b7"/>
      <stop offset="56%" stop-color="#979797"/>
      <stop offset="100%" stop-color="#7e7e7e"/>
    </linearGradient>

    <filter id="textBloom" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="1.2" result="blur"/>
      <feFlood flood-color="#9a9a9a" flood-opacity="0.24" result="glowColor"/>
      <feComposite in="glowColor" in2="blur" operator="in" result="softGlow"/>
      <feMerge>
        <feMergeNode in="softGlow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- absolute black field -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <!-- almost invisible optical center lift; keeps the slide from feeling like a flat void -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#blackVignette)"/>

  <!-- subtle cinematic letterbox weight -->
  <rect x="0" y="0" width="1280" height="76" fill="#000000" opacity="0.92"/>
  <rect x="0" y="644" width="1280" height="76" fill="#000000" opacity="0.92"/>

  <!-- tiny top classification line: optional, gives a premium title-sequence feel -->
  <text x="640" y="118"
        width="720"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="400"
        letter-spacing="5"
        fill="#5f5f5f"
        opacity="0.72">
    SECTION 03
  </text>

  <!-- main phrase: small relative to the canvas, with generous line spacing -->
  <text x="640" y="292"
        width="900"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44"
        font-weight="400"
        letter-spacing="1.2"
        fill="url(#mutedTitle)"
        filter="url(#textBloom)">
    <tspan x="640" dy="0">The Quiet Moment</tspan>
    <tspan x="640" dy="62">Before Everything Changes</tspan>
  </text>

  <!-- restrained subtitle with macro-whitespace below title -->
  <line x1="452" y1="518" x2="548" y2="518" stroke="#3f3f3f" stroke-width="1" opacity="0.62"/>
  <line x1="732" y1="518" x2="828" y2="518" stroke="#3f3f3f" stroke-width="1" opacity="0.62"/>

  <text x="640" y="525"
        width="600"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19"
        font-weight="400"
        letter-spacing="0.8"
        fill="#b1b1b1"
        opacity="0.84">
    A Strategy Briefing
  </text>

  <!-- barely-there corner registration marks; decorative, not functional -->
  <path d="M104 104 L104 132 M104 104 L132 104"
        fill="none"
        stroke="#2a2a2a"
        stroke-width="1"
        opacity="0.48"/>
  <path d="M1176 616 L1176 588 M1176 616 L1148 616"
        fill="none"
        stroke="#2a2a2a"
        stroke-width="1"
        opacity="0.48"/>
</svg>
```

## Avoid in this skill
- ❌ Pure white text on pure black; it feels harsh and less cinematic than muted gray.
- ❌ Large logos, icons, photos, or decorative grids; the effect depends on near-total negative space.
- ❌ Crowding the title with multiple subtitles, dates, or speaker names.
- ❌ Heavy drop shadows or neon glows; any glow should be nearly imperceptible.
- ❌ Overusing all-caps for the main title unless the phrase is very short.

## Composition notes
- Keep the main title within the central 30–35% of slide height; the black space is the design.
- Place secondary text far below the title, not directly underneath it, to create cinematic pacing.
- Use muted grays between `#7e7e7e` and `#b7b7b7`; avoid saturated brand colors.
- If using a fade transition in PowerPoint, make it slow enough to feel intentional, around 1.5–2 seconds.