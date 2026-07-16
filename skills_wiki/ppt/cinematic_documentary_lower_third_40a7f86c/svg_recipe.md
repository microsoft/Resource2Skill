# SVG Recipe — Cinematic Documentary Lower-Third

## Visual mechanism
A serious full-bleed monochrome documentary photo is darkened with cinematic overlays, then interrupted by a saturated teal lower-third ribbon that carries the key takeaway. The result feels like a broadcast title card: historical, authoritative background plus crisp modern UI typography.

## SVG primitives needed
- 1× `<image>` for the full-bleed pre-grayscale documentary / archival background photo
- 4× `<rect>` for darkening overlays, letterbox bars, and subtle readability gradients
- 2× `<linearGradient>` for the left-side text fade and teal ribbon sheen
- 1× `<radialGradient>` for the vignette-style dark edge treatment
- 1× `<filter id="ribbonShadow">` using `feOffset + feGaussianBlur + feMerge` for the lower-third depth
- 1× `<filter id="softGlow">` using `feGaussianBlur` for faint glow behind white typography
- 3× `<path>` for the angled ribbon end, icon play triangle, and decorative documentary tick marks
- 2× `<circle>` for the lower-third broadcast logo / anchor badge
- 2× `<line>` for crisp UI divider rules
- 4× `<text>` elements with explicit `width` for headline, eyebrow label, lower-third title, and subtitle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftReadability" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.72"/>
      <stop offset="48%" stop-color="#000000" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="tealRibbon" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00C2A8"/>
      <stop offset="62%" stop-color="#00B89F"/>
      <stop offset="100%" stop-color="#008F84"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="52%" cy="44%" r="78%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="66%" stop-color="#000000" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <filter id="ribbonShadow" x="-10%" y="-30%" width="120%" height="180%">
      <feOffset dx="0" dy="7" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-5%" y="-10%" width="110%" height="130%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
  </defs>

  <image
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    href="https://images.example.com/preprocessed-grayscale-archival-command-room-photo.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.36"/>
  <rect x="0" y="0" width="760" height="720" fill="url(#leftReadability)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <rect x="0" y="0" width="1280" height="48" fill="#000000" opacity="0.42"/>
  <rect x="0" y="672" width="1280" height="48" fill="#000000" opacity="0.48"/>

  <text x="72" y="118" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700"
        letter-spacing="3.2"
        fill="#00C2A8">
    STRATEGY ARCHIVE / FIELD NOTE 07
  </text>

  <line x1="72" y1="137" x2="270" y2="137" stroke="#00C2A8" stroke-width="3"/>
  <line x1="284" y1="137" x2="360" y2="137" stroke="#FFFFFF" stroke-width="1" opacity="0.55"/>

  <text x="70" y="210" width="880"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800"
        fill="#FFFFFF"
        filter="url(#softGlow)">
    “THE SUPREME ART OF WAR IS TO SUBDUE THE ENEMY WITHOUT FIGHTING.”
  </text>

  <text x="72" y="338" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="400"
        fill="#D7D7D7">
    A documentary-style frame for quotes, executive findings, historical context, or decisive narrative moments.
  </text>

  <path d="M0 558 L1042 558 L1108 624 L1042 690 L0 690 Z"
        fill="url(#tealRibbon)"
        filter="url(#ribbonShadow)"/>

  <rect x="0" y="558" width="1280" height="2" fill="#FFFFFF" opacity="0.72"/>
  <rect x="0" y="688" width="1044" height="2" fill="#004C48" opacity="0.45"/>

  <circle cx="86" cy="624" r="48" fill="#071B1B" opacity="0.92"/>
  <circle cx="86" cy="624" r="36" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.88"/>
  <path d="M76 602 L76 646 L111 624 Z" fill="#00C2A8"/>

  <text x="154" y="604" width="720"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800"
        letter-spacing="2.4"
        fill="#06312F">
    KEY TAKEAWAY
  </text>

  <text x="154" y="648" width="780"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="700"
        fill="#FFFFFF">
    Applying historical strategy to modern business negotiations
  </text>

  <path d="M978 582 L990 582 M1002 582 L1014 582 M1026 582 L1038 582"
        stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.62" fill="none"/>
  <path d="M1002 668 L1014 668 M1026 668 L1038 668 M1050 668 L1062 668"
        stroke="#06312F" stroke-width="3" stroke-linecap="round" opacity="0.45" fill="none"/>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG grayscale filters for the background photo; use a pre-desaturated image asset or a grayscale-rendered photo URL.
- ❌ Do not place the lower-third text directly on the photo without the teal ribbon; the visual mechanism depends on the broadcast-style color block.
- ❌ Do not use `clip-path` on rectangles or paths for the angled ribbon; draw the ribbon end directly as a `<path>`.
- ❌ Do not use `marker-end` for any decorative arrows or UI ticks; use simple `<line>` or `<path>` strokes instead.
- ❌ Do not over-color the background image; keep the photo monochrome so the teal accent remains the only saturated element.

## Composition notes
- Keep the background image full-bleed and visually dramatic, but darken it enough that white headline text remains readable.
- Place the main quote in the upper-left or center-left third; reserve the bottom 20–24% of the slide for the lower-third system.
- Let the teal ribbon extend from the left edge to roughly 82–88% of the slide width, ending asymmetrically with an angled cut.
- Use one saturated accent only, typically cyan/teal `#00C2A8`; all other tones should be black, white, gray, or near-black.