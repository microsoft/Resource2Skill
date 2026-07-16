# SVG Recipe — Multi-Layer Parallax Morph Reveal

## Visual mechanism
Build two near-identical slides with the same background image, hero title, and foreground silhouette layer, then change only their vertical positions so PowerPoint Morph creates a cinematic 2.5D parallax reveal. The distant photo moves slightly, the title exits quickly, and the dark organic foreground rises to become a readable content stage.

## SVG primitives needed
- 1× oversized `<image>` for the distant landscape/photo layer, positioned beyond the slide bounds so it can pan during Morph
- 1× `<rect>` with gradient fill for cinematic darkening and title legibility over the photo
- 1× large `<text>` hero title with shadow filter for the hook state / exiting title layer
- 1× organic `<path>` for the rising foreground landmass / reveal panel
- 3× small `<path>` silhouettes for pine/rock details along the foreground edge
- 1× `<linearGradient>` for the photo color grade overlay
- 1× `<linearGradient>` for the foreground panel depth
- 1× `<radialGradient>` for atmospheric glow behind the reveal content
- 1× `<filter id="softShadow">` applied to title, cards, and foreground elements
- 1× `<filter id="glow">` applied to accent circles / reveal highlights
- 3× `<rect>` for reveal content cards
- 3× `<circle>` for accent markers / metric bullets
- 6× `<text>` blocks for eyebrow, headline, body copy, and data labels, each with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoGrade" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#08111f" stop-opacity="0.15"/>
      <stop offset="0.48" stop-color="#0b1322" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#02060b" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="panelDepth" x1="0" y1="250" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172433" stop-opacity="0.94"/>
      <stop offset="0.45" stop-color="#0d141d" stop-opacity="0.98"/>
      <stop offset="1" stop-color="#05080d" stop-opacity="1"/>
    </linearGradient>

    <radialGradient id="cyanAura" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#26d9ff" stop-opacity="0.38"/>
      <stop offset="0.46" stop-color="#26d9ff" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#26d9ff" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>
  </defs>

  <!-- REVEAL STATE: for the HOOK state, move this same image down about 90px -->
  <image id="ParallaxBG"
         href="https://images.example.com/oversized-misty-mountain-valley-at-sunrise.jpg"
         x="-90" y="-135" width="1460" height="910" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#photoGrade)"/>

  <!-- In slide 1 this title sits near y=292; in slide 2 it morphs upward and mostly exits -->
  <text id="HeroTitle" x="0" y="-42" width="1280"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800" letter-spacing="10"
        text-anchor="middle" fill="#ffffff" opacity="0.96"
        filter="url(#softShadow)">EXPLORE</text>

  <!-- atmospheric glow that travels with the foreground reveal layer -->
  <ellipse cx="840" cy="418" rx="320" ry="150" fill="url(#cyanAura)" filter="url(#glow)" opacity="0.82"/>

  <!-- Rising organic foreground: in slide 1 set this group translate(0 380); in slide 2 translate(0 0) -->
  <g id="WavyOverlay" transform="translate(0 0)">
    <path d="M0,355
             C90,318 145,348 220,326
             C305,302 365,340 450,314
             C535,289 604,327 684,303
             C760,280 835,315 914,292
             C1008,264 1082,302 1162,276
             C1215,259 1250,271 1280,260
             L1280,720 L0,720 Z"
          fill="url(#panelDepth)" filter="url(#softShadow)"/>

    <path d="M58,348 L78,300 L96,348 Z
             M88,350 L112,286 L138,350 Z
             M133,346 L154,306 L174,346 Z
             M1018,295 L1042,244 L1068,295 Z
             M1062,292 L1090,224 L1120,292 Z
             M1110,290 L1134,250 L1158,290 Z"
          fill="#070b10" opacity="0.92"/>

    <path d="M0,376 C120,350 220,392 360,365
             C500,336 612,388 748,355
             C888,321 1008,366 1280,322
             L1280,720 L0,720 Z"
          fill="#070b10" opacity="0.46"/>

    <rect x="74" y="435" width="346" height="182" rx="30" fill="#101b27" opacity="0.88" filter="url(#softShadow)"/>
    <rect x="466" y="435" width="346" height="182" rx="30" fill="#101b27" opacity="0.78" filter="url(#softShadow)"/>
    <rect x="858" y="435" width="346" height="182" rx="30" fill="#101b27" opacity="0.78" filter="url(#softShadow)"/>

    <circle cx="116" cy="482" r="18" fill="#22d3ee" filter="url(#glow)"/>
    <circle cx="508" cy="482" r="18" fill="#7dd3fc" filter="url(#glow)"/>
    <circle cx="900" cy="482" r="18" fill="#a7f3d0" filter="url(#glow)"/>

    <text x="78" y="392" width="500"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="16" font-weight="700" letter-spacing="4"
          fill="#22d3ee">PARALLAX MORPH REVEAL</text>

    <text x="76" y="414" width="710"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="42" font-weight="750"
          fill="#ffffff">From atmosphere to evidence</text>

    <text x="76" y="654" width="690"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="400"
          fill="#b7c4d3">Layered motion shifts attention from cinematic imagery into concrete proof points without breaking visual continuity.</text>

    <text x="102" y="525" width="270"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="48" font-weight="800"
          fill="#ffffff">3.6×</text>
    <text x="104" y="563" width="270"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="19"
          fill="#9fb0c2">faster audience orientation</text>

    <text x="494" y="525" width="270"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="48" font-weight="800"
          fill="#ffffff">52%</text>
    <text x="496" y="563" width="270"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="19"
          fill="#9fb0c2">more space for reveal content</text>

    <text x="886" y="525" width="270"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="48" font-weight="800"
          fill="#ffffff">0.8s</text>
    <text x="888" y="563" width="270"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="19"
          fill="#9fb0c2">ideal Morph transition length</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; the motion should be created by duplicating slides and using PowerPoint Morph, not SVG animation.
- ❌ `<mask>` for the reveal panel; use a direct editable `<path>` silhouette instead.
- ❌ Clipping the foreground path; `clip-path` is reliable for `<image>` only, so keep organic landforms as editable paths.
- ❌ Straight horizontal reveal panels; the premium effect depends on an irregular organic edge that feels like foreground terrain.
- ❌ Moving every layer by the same distance; equal motion destroys the parallax depth illusion.

## Composition notes
- Use two slides with identical element IDs/names where possible: background, title, and foreground overlay should be matched objects for Morph.
- Slide 1 hook state: background lower, title centered, foreground group translated down off-canvas by roughly 350–420 px.
- Slide 2 reveal state: background pans up only 70–110 px, title moves far upward, foreground rises to cover the lower 55–65% of the slide.
- Keep the top half image-rich and atmospheric; reserve the dark foreground panel for high-contrast metrics, copy, and proof points.