# SVG Recipe — 5-Column Profile Grid

## Visual mechanism
A five-column editorial roster uses equal-width vertical cards: each column leads with a square cropped portrait, then stacks role, name, and short descriptive copy. Warm gradient background, soft shadows, subtle accent tabs, and numeric labels keep the dense grid premium rather than spreadsheet-like.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm gradient background
- 2× `<path>` for large organic decorative blobs behind the grid
- 5× `<rect>` for raised profile cards with rounded corners and soft shadows
- 5× `<rect>` for small colored accent tabs at the top of each card
- 5× `<clipPath>` with rounded `<rect>` crops for square profile images
- 5× `<image>` for 1:1 profile photos clipped into rounded squares
- 5× `<rect>` for thin photo border overlays
- 5× `<circle>` for numbered profile badges
- 16× `<text>` blocks for title, subtitle, names, roles, descriptions, numbers, and footer
- 2× `<linearGradient>` for background and card accent fills
- 1× `<radialGradient>` for a soft spotlight wash
- 1× `<filter id="cardShadow">` for editable card shadows
- 1× `<filter id="softGlow">` for background glow shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWarm" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF6EA"/>
      <stop offset="0.48" stop-color="#F7E6D1"/>
      <stop offset="1" stop-color="#F2D3B4"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="212" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#C66A3D"/>
      <stop offset="1" stop-color="#E8A05F"/>
    </linearGradient>
    <radialGradient id="spotlight" cx="50%" cy="35%" r="70%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.82"/>
      <stop offset="0.62" stop-color="#FFFFFF" stop-opacity="0.2"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
    <clipPath id="photoClip1"><rect x="88" y="158" width="176" height="176" rx="22"/></clipPath>
    <clipPath id="photoClip2"><rect x="320" y="158" width="176" height="176" rx="22"/></clipPath>
    <clipPath id="photoClip3"><rect x="552" y="158" width="176" height="176" rx="22"/></clipPath>
    <clipPath id="photoClip4"><rect x="784" y="158" width="176" height="176" rx="22"/></clipPath>
    <clipPath id="photoClip5"><rect x="1016" y="158" width="176" height="176" rx="22"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWarm)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>
  <path d="M-70 170 C120 60 250 85 345 215 C420 318 315 420 135 390 C-5 368 -120 294 -70 170 Z" fill="#F7B37A" opacity="0.22" filter="url(#softGlow)"/>
  <path d="M990 48 C1138 -5 1288 28 1335 146 C1390 284 1248 376 1105 330 C1010 300 916 212 940 125 C948 88 968 61 990 48 Z" fill="#C66A3D" opacity="0.16" filter="url(#softGlow)"/>

  <text x="70" y="62" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2A211B">Leadership bench for the next growth chapter</text>
  <text x="72" y="92" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6E5A4B">Five complementary profiles, shown with equal visual weight for fast comparison.</text>
  <text x="1010" y="68" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#9B5C38" text-anchor="end">TEAM PROFILE GRID</text>

  <rect x="70" y="126" width="212" height="500" rx="30" fill="#FFFDF8" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="302" y="126" width="212" height="500" rx="30" fill="#FFFDF8" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="534" y="126" width="212" height="500" rx="30" fill="#FFFDF8" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="766" y="126" width="212" height="500" rx="30" fill="#FFFDF8" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="998" y="126" width="212" height="500" rx="30" fill="#FFFDF8" opacity="0.96" filter="url(#cardShadow)"/>

  <rect x="94" y="126" width="80" height="6" rx="3" fill="url(#accentGrad)"/>
  <rect x="326" y="126" width="80" height="6" rx="3" fill="#7C9A72"/>
  <rect x="558" y="126" width="80" height="6" rx="3" fill="#5B8DAA"/>
  <rect x="790" y="126" width="80" height="6" rx="3" fill="#A65F7A"/>
  <rect x="1022" y="126" width="80" height="6" rx="3" fill="#D59A38"/>

  <image x="88" y="158" width="176" height="176" href="https://images.example.com/profiles/strategic-operator-square-portrait.jpg" clip-path="url(#photoClip1)" preserveAspectRatio="xMidYMid slice"/>
  <image x="320" y="158" width="176" height="176" href="https://images.example.com/profiles/product-visionary-square-portrait.jpg" clip-path="url(#photoClip2)" preserveAspectRatio="xMidYMid slice"/>
  <image x="552" y="158" width="176" height="176" href="https://images.example.com/profiles/commercial-builder-square-portrait.jpg" clip-path="url(#photoClip3)" preserveAspectRatio="xMidYMid slice"/>
  <image x="784" y="158" width="176" height="176" href="https://images.example.com/profiles/data-leader-square-portrait.jpg" clip-path="url(#photoClip4)" preserveAspectRatio="xMidYMid slice"/>
  <image x="1016" y="158" width="176" height="176" href="https://images.example.com/profiles/culture-catalyst-square-portrait.jpg" clip-path="url(#photoClip5)" preserveAspectRatio="xMidYMid slice"/>

  <rect x="88" y="158" width="176" height="176" rx="22" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <rect x="320" y="158" width="176" height="176" rx="22" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <rect x="552" y="158" width="176" height="176" rx="22" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <rect x="784" y="158" width="176" height="176" rx="22" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <rect x="1016" y="158" width="176" height="176" rx="22" fill="none" stroke="#FFFFFF" stroke-width="5"/>

  <circle cx="238" cy="334" r="22" fill="#2A211B"/>
  <circle cx="470" cy="334" r="22" fill="#2A211B"/>
  <circle cx="702" cy="334" r="22" fill="#2A211B"/>
  <circle cx="934" cy="334" r="22" fill="#2A211B"/>
  <circle cx="1166" cy="334" r="22" fill="#2A211B"/>
  <text x="238" y="341" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">01</text>
  <text x="470" y="341" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">02</text>
  <text x="702" y="341" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">03</text>
  <text x="934" y="341" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">04</text>
  <text x="1166" y="341" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">05</text>

  <text x="94" y="374" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#C66A3D" letter-spacing="1.6">OPERATIONS</text>
  <text x="94" y="404" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#2A211B">Maya Chen</text>
  <text x="94" y="436" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6E5A4B">Scales delivery systems, converts ambiguity into operating cadence, and keeps cross-functional execution visible.</text>
  <text x="94" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#A77A5A">Best fit · Integration lead</text>

  <text x="326" y="374" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#7C9A72" letter-spacing="1.6">PRODUCT</text>
  <text x="326" y="404" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#2A211B">Jon Bell</text>
  <text x="326" y="436" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6E5A4B">Turns customer insight into crisp bets, prototypes quickly, and aligns roadmap tradeoffs with commercial proof.</text>
  <text x="326" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#7A8E70">Best fit · Venture studio</text>

  <text x="558" y="374" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#5B8DAA" letter-spacing="1.6">REVENUE</text>
  <text x="558" y="404" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#2A211B">Ari Patel</text>
  <text x="558" y="436" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6E5A4B">Builds repeatable pipeline motions, coaches enterprise teams, and packages value stories for strategic buyers.</text>
  <text x="558" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#67879A">Best fit · Market expansion</text>

  <text x="790" y="374" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#A65F7A" letter-spacing="1.6">INSIGHTS</text>
  <text x="790" y="404" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#2A211B">Lena Ortiz</text>
  <text x="790" y="436" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6E5A4B">Translates messy signal into executive decisions, from pricing models to cohort health and board-ready metrics.</text>
  <text x="790" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#956074">Best fit · Analytics spine</text>

  <text x="1022" y="374" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#D59A38" letter-spacing="1.6">CULTURE</text>
  <text x="1022" y="404" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#2A211B">Noah Reed</text>
  <text x="1022" y="436" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6E5A4B">Shapes leadership rituals, talent density, and decision norms so the organization can move faster without fragility.</text>
  <text x="1022" y="536" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#B38132">Best fit · Org acceleration</text>

  <line x1="70" y1="654" x2="1210" y2="654" stroke="#D7B99C" stroke-width="1" stroke-dasharray="4 8"/>
  <text x="70" y="684" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7A6454">Use this shell when all five people or entities require comparable prominence and enough room for individual narrative.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the photo crop by masking a rectangle or clipping non-image elements; use `<clipPath>` directly on each `<image>`.
- ❌ Do not rely on automatic text wrapping; every `<text>` needs a `width` and should be manually sized to fit the column.
- ❌ Do not overcrowd cards with long bios; five columns are already dense, so keep each description to 2–3 short lines.
- ❌ Do not use `<use>` for repeated cards or badges; duplicate the editable shapes explicitly.
- ❌ Do not apply filters to divider `<line>` elements; use shadows only on cards, paths, text, circles, or rects.

## Composition notes
- Keep the five cards equal width with narrow but consistent gutters; the visual strength comes from disciplined repetition.
- Reserve the top 100–120 px for title and context, then let portraits dominate the upper half of each card.
- Use one accent color per profile, but keep the card surfaces neutral so the slide remains editorial and warm.
- Place the footer below the grid as a light annotation, not a competing headline.