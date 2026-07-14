# SVG Recipe — Minimal Centered Text

## Visual mechanism
A restrained editorial slide built around a centered vertical text stack: tiny accent subhead, large headline, and optional supporting body copy. The premium feel comes from generous negative space, subtle background atmosphere, delicate hairlines, and precise typographic hierarchy.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm neutral background
- 2× `<path>` for soft abstract atmospheric color fields behind the text
- 1× `<radialGradient>` for a quiet center glow
- 2× `<linearGradient>` for background wash and accent strokes
- 1× `<filter id="softBlur">` applied to background paths for diffused ambience
- 1× `<filter id="textShadow">` applied to the main headline for a very subtle executive-keynote lift
- 4× `<line>` for thin editorial divider rules framing the text block
- 1× `<circle>` for a small centered accent mark
- 3× `<text>` blocks with explicit `width` attributes for subhead, headline, and body
- Multiple nested `<tspan>` elements for multiline headline/body and inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F7F3EC"/>
      <stop offset="52%" stop-color="#FBFAF7"/>
      <stop offset="100%" stop-color="#EEF2F6"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="48%" r="42%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="58%" stop-color="#FFFFFF" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="warmMist" x1="255" y1="120" x2="990" y2="570" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#D8B36A" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#D8B36A" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="coolMist" x1="1040" y1="95" x2="320" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#6E86A8" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#6E86A8" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ruleFade" x1="310" y1="0" x2="970" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1D2430" stop-opacity="0"/>
      <stop offset="18%" stop-color="#1D2430" stop-opacity="0.28"/>
      <stop offset="50%" stop-color="#1D2430" stop-opacity="0.45"/>
      <stop offset="82%" stop-color="#1D2430" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#1D2430" stop-opacity="0"/>
    </linearGradient>

    <filter id="softBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="textShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <path d="M184 118 C298 42 456 48 552 126 C646 202 606 312 506 350 C392 394 242 354 166 260 C116 198 124 158 184 118 Z"
        fill="url(#warmMist)" filter="url(#softBlur)" opacity="0.82"/>

  <path d="M1114 90 C1016 38 880 72 806 156 C732 240 770 344 878 382 C1010 428 1154 374 1204 270 C1236 204 1202 136 1114 90 Z"
        fill="url(#coolMist)" filter="url(#softBlur)" opacity="0.78"/>

  <line x1="322" y1="231" x2="958" y2="231" stroke="url(#ruleFade)" stroke-width="1.2"/>
  <line x1="322" y1="497" x2="958" y2="497" stroke="url(#ruleFade)" stroke-width="1.2"/>

  <line x1="603" y1="231" x2="624" y2="231" stroke="#A7813A" stroke-width="2.2"/>
  <line x1="656" y1="231" x2="677" y2="231" stroke="#A7813A" stroke-width="2.2"/>
  <circle cx="640" cy="231" r="3.8" fill="#A7813A"/>

  <text x="640" y="279" width="560"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="700"
        letter-spacing="4.5"
        fill="#A7813A">
    STRATEGIC INFLECTION
  </text>

  <text x="640" y="353" width="850"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58"
        font-weight="300"
        letter-spacing="-1.6"
        fill="#171B22"
        filter="url(#textShadow)">
    <tspan x="640" dy="0">The next advantage is</tspan>
    <tspan x="640" dy="66" font-weight="600">clarity at scale</tspan>
  </text>

  <text x="640" y="471" width="610"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="400"
        line-height="1.45"
        fill="#5B6470">
    <tspan x="640" dy="0">A minimal section divider gives the audience one idea to hold,</tspan>
    <tspan x="640" dy="28">with enough silence around it to make the message feel deliberate.</tspan>
  </text>

  <text x="640" y="566" width="520"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11"
        font-weight="600"
        letter-spacing="2.8"
        fill="#8C929B">
    01 / EXECUTIVE NARRATIVE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense grids, icon clusters, or decorative panels that compete with the centered statement
- ❌ Overusing shadows or glow on the typography; the effect should feel almost invisible
- ❌ `<textPath>` for curved quotes or arced subtitles, because it will not translate reliably
- ❌ Applying `filter` to `<line>` elements for rule shadows; keep divider rules flat and crisp
- ❌ Cropping or masking non-image shapes; if a decorative shape is needed, draw it directly with `<path>`

## Composition notes
- Keep the main text block within the central 45–55% of slide height; the slide should feel spacious above and below.
- Use one quiet accent color for eyebrow text, small dots, and short rule highlights; avoid adding a second accent.
- The headline should dominate, with the subhead acting as a label and the body copy no wider than about half the slide.
- Background atmosphere should be low contrast and never reduce text readability; keep the visual focus locked on the headline.