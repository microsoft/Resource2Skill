# SVG Recipe — Curved Split Cover

## Visual mechanism
A full-bleed hero image occupies the visual side of the slide, while a large off-canvas ellipse and matching rectangular panel carve a smooth curved split for the title content. The oversized curve feels more premium than a straight divider and creates motion toward the headline.

## SVG primitives needed
- 1× `<image>` for the hero photo, clipped to the left side of the slide
- 1× `<clipPath>` with `<rect>` applied to the hero image crop
- 3× `<rect>` for the background wash, right-side title panel, and small label pill
- 2× `<ellipse>` for the main curved split panel and soft decorative color field
- 3× `<circle>` for small accent dots and logo mark
- 2× `<path>` for the curved accent stroke and abstract brand flourish
- 5× `<text>` for eyebrow label, headline, subtitle, date, and logo text
- 2× `<linearGradient>` for warm panel fill and accent fills
- 1× `<radialGradient>` for subtle photo-edge glow
- 1× `<filter id="softShadow">` applied to the curved panel/accent shapes for depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelWarm" x1="650" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF7EA"/>
      <stop offset="0.58" stop-color="#FFE7C2"/>
      <stop offset="1" stop-color="#FFD49B"/>
    </linearGradient>

    <linearGradient id="coralAccent" x1="0" y1="0" x2="240" y2="180" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF7A59"/>
      <stop offset="1" stop-color="#F2B447"/>
    </linearGradient>

    <radialGradient id="photoGlow" cx="45%" cy="44%" r="65%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.72" stop-color="#231A12" stop-opacity="0"/>
      <stop offset="1" stop-color="#231A12" stop-opacity="0.28"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-14" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroCrop">
      <rect x="0" y="0" width="835" height="720"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFF3DF"/>

  <image
    href="https://images.example.com/hero-photo-warm-team-collaboration-studio.jpg"
    x="-28" y="0" width="900" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroCrop)"/>

  <rect x="0" y="0" width="835" height="720" fill="url(#photoGlow)"/>

  <ellipse
    cx="760" cy="358" rx="338" ry="502"
    fill="url(#panelWarm)"
    filter="url(#softShadow)"/>

  <rect x="760" y="0" width="520" height="720" fill="url(#panelWarm)"/>

  <ellipse
    cx="1128" cy="92" rx="190" ry="150"
    fill="#FFFFFF"
    opacity="0.28"/>

  <path
    d="M700 88 C624 192 616 304 687 405 C751 496 742 599 674 681"
    fill="none"
    stroke="#F5A25D"
    stroke-width="5"
    stroke-linecap="round"
    opacity="0.75"/>

  <path
    d="M1045 558 C1092 526 1160 536 1198 586 C1154 637 1078 645 1031 600 C1018 587 1027 570 1045 558 Z"
    fill="url(#coralAccent)"
    opacity="0.88"
    filter="url(#softShadow)"/>

  <circle cx="1135" cy="188" r="9" fill="#FF7A59"/>
  <circle cx="1178" cy="224" r="5" fill="#F2B447"/>
  <circle cx="1092" cy="250" r="4" fill="#2F6F73" opacity="0.75"/>

  <circle cx="850" cy="82" r="18" fill="#2F6F73"/>
  <text x="878" y="90" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700"
        fill="#253335">NOVA SUMMIT</text>

  <rect x="828" y="170" width="214" height="38" rx="19" fill="#FFFFFF" opacity="0.78"/>
  <text x="852" y="195" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        letter-spacing="1.8"
        fill="#B45E34">2026 STRATEGY</text>

  <text x="828" y="294" width="370"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800"
        fill="#263238">
    <tspan x="828" dy="0">Designing</tspan>
    <tspan x="828" dy="68">Growth with</tspan>
    <tspan x="828" dy="68" fill="#E26D45">Momentum</tspan>
  </text>

  <text x="832" y="530" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#5E5B55">
    <tspan x="832" dy="0">A practical keynote on building</tspan>
    <tspan x="832" dy="31">brand systems, customer trust,</tspan>
    <tspan x="832" dy="31">and resilient market advantage.</tspan>
  </text>

  <line x1="832" y1="638" x2="1040" y2="638" stroke="#D68A48" stroke-width="2" opacity="0.7"/>
  <text x="832" y="674" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        fill="#354044">June 18 · Executive Briefing</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to cut the curved divider; instead, overlay an editable ellipse and matching rect in the panel color.
- ❌ Applying `clip-path` to the ellipse or text panel; keep clipping only on the `<image>`.
- ❌ Building the split from many small rectangles or circles; one oversized ellipse gives a smoother, more editable PowerPoint shape.
- ❌ Putting filter effects on divider lines; use shadow on the ellipse or decorative paths, not on `<line>` elements.

## Composition notes
- Keep the hero image dominant on the left 55–65% of the canvas; the curve should intrude into the photo enough to feel intentional.
- Place headline content inside the clean right-side panel, with generous margins from the curved edge.
- Use warm panel colors when the image is busy; the curve acts as both visual separation and a calm reading zone.
- Add only a few small accent shapes near the title so the cover feels designed without competing with the hero photo.