# SVG Recipe — Consulting-Grade Structural Consistency & Hero Reveal

## Visual mechanism
A premium consulting deck alternates between a cinematic full-bleed hero image with a translucent geometric title mask and rigorously consistent content slides using a locked header bar, thin accent rule, restrained palette, and flat data visuals. The emotional photo creates the reveal; the repeated header grid creates executive-grade continuity.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero background photo
- 1× `<clipPath>` with `<rect>` for a rounded mini content-card image crop
- 2× `<path>` for the translucent slanted hero mask and angular accent wedge
- 8× `<rect>` for header system, accent rules, data-card panels, chart bars, and KPI tiles
- 3× `<circle>` for minimalist status dots / icon accents
- 2× `<line>` for simple axis/grid references
- Multiple `<text>` with explicit `width` for title, subtitle, section labels, KPI values, and chart labels
- 1× `<linearGradient>` for subtle hero darkening / depth
- 1× `<filter id="cardShadow">` for soft editable PowerPoint-style panel shadows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroDim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101820" stop-opacity="0.10"/>
      <stop offset="55%" stop-color="#101820" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#101820" stop-opacity="0.55"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="roundedPhotoCrop">
      <rect x="825" y="188" width="300" height="152" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <!-- Full-bleed Apple-style hero background -->
  <image href="https://images.example.com/full-bleed-night-city-financial-district.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#heroDim)"/>

  <!-- Semi-transparent geometric title mask -->
  <path d="M0,0 L555,0 L470,720 L0,720 Z"
        fill="#FFFFFF" opacity="0.86"/>
  <path d="M470,0 L570,0 L485,720 L410,720 Z"
        fill="#ED7D31" opacity="0.82"/>

  <!-- Hero title block -->
  <text x="70" y="126" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="2.5"
        fill="#ED7D31">Q4 EXECUTIVE BRIEFING</text>

  <text x="70" y="208" width="385"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="700"
        fill="#404040">Market Analysis &amp; Strategy</text>

  <text x="70" y="338" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="400"
        fill="#595959">Structural consistency system for high-density decision slides</text>

  <line x1="70" y1="405" x2="214" y2="405" stroke="#ED7D31" stroke-width="5"/>
  <text x="70" y="444" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#404040">Prepared for Board Strategy Committee</text>

  <!-- Bain-style content slide preview, showing the locked system -->
  <rect x="640" y="92" width="560" height="510" rx="24" ry="24"
        fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="640" y="92" width="560" height="86" rx="24" ry="24"
        fill="#F2F2F2"/>
  <rect x="640" y="164" width="560" height="14" fill="#F2F2F2"/>
  <rect x="640" y="178" width="560" height="5" fill="#2E75B6"/>

  <text x="680" y="132" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700"
        fill="#404040">Regional growth remains concentrated in two segments</text>
  <text x="680" y="160" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#737373">Illustrative content slide: fixed header, fixed accent rule, flat data</text>

  <!-- Cropped image teaser inside content card -->
  <image href="https://images.example.com/cropped-office-team-reviewing-dashboard.jpg"
         x="825" y="188" width="300" height="152"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#roundedPhotoCrop)"/>
  <rect x="680" y="198" width="112" height="82" rx="10" fill="#F2F2F2"/>
  <text x="700" y="229" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#404040">2-color</text>
  <text x="700" y="253" width="78"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#737373">palette only</text>
  <circle cx="710" cy="270" r="5" fill="#2E75B6"/>
  <circle cx="730" cy="270" r="5" fill="#ED7D31"/>
  <circle cx="750" cy="270" r="5" fill="#404040"/>

  <!-- Flat chart module -->
  <rect x="680" y="370" width="420" height="150" rx="14" fill="#FAFAFA" stroke="#E6E6E6"/>
  <text x="704" y="404" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#404040">Revenue index by segment</text>
  <line x1="720" y1="492" x2="1055" y2="492" stroke="#D9D9D9" stroke-width="1"/>
  <line x1="720" y1="430" x2="720" y2="492" stroke="#D9D9D9" stroke-width="1"/>

  <rect x="748" y="456" width="42" height="36" fill="#2E75B6"/>
  <rect x="810" y="438" width="42" height="54" fill="#2E75B6"/>
  <rect x="872" y="418" width="42" height="74" fill="#ED7D31"/>
  <rect x="934" y="446" width="42" height="46" fill="#2E75B6"/>
  <rect x="996" y="406" width="42" height="86" fill="#ED7D31"/>

  <text x="744" y="516" width="55"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#737373">Core</text>
  <text x="810" y="516" width="55"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#737373">SMB</text>
  <text x="866" y="516" width="62"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#737373">Cloud</text>
  <text x="930" y="516" width="58"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#737373">Gov</text>
  <text x="992" y="516" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#737373">Partner</text>

  <!-- Small consistency annotation -->
  <rect x="680" y="544" width="420" height="34" rx="17" fill="#404040" opacity="0.92"/>
  <text x="704" y="567" width="380"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#FFFFFF">Header position and accent rule remain identical on every content slide</text>
</svg>
```

## Avoid in this skill
- ❌ Random multicolor chart palettes; limit data emphasis to one brand color plus one accent color.
- ❌ Default PowerPoint 3D charts, bevels, heavy outlines, or decorative gradients inside charts.
- ❌ Moving slide titles between pages; the header bar, title baseline, and accent rule must stay locked.
- ❌ Applying `clip-path` to rectangles or text for masks; use translucent paths for overlays and clip only images.
- ❌ Using a plain opaque title box over the hero photo; the premium look depends on controlled transparency and geometry.

## Composition notes
- Reserve the cover’s left 40–50% for the translucent geometric title mask; keep the hero image visible and emotionally dominant on the remaining side.
- For content slides, dedicate the top ~15% of the canvas to a full-width light-grey header and a thin brand accent rule.
- Keep data visuals flat, sparse, and aligned to a modular grid below the header; use orange or blue only for the key message.
- Maintain large negative space around titles and chart modules so the deck feels deliberate rather than assembled from mismatched sources.