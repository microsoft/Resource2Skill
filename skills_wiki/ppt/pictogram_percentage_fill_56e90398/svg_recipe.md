# SVG Recipe — Pictogram Percentage Fill

## Visual mechanism
A meaningful icon acts as a “container” for a KPI: the full icon appears in a muted neutral color, while a second, lower slice of the same icon is overlaid in an accent color to show the percentage filled from bottom to top. The key is to make the colored slice a real editable `<path>` that represents the boolean intersection between the icon silhouette and a horizontal fill band.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× `<rect>` for premium KPI cards
- 3× `<path>` for the full neutral pictogram silhouettes
- 3× `<path>` for the colored lower-fill pictogram slices
- 3× `<line>` for subtle horizontal “liquid level” indicators
- 3× `<circle>` for small metric badges / accent dots
- 1× `<linearGradient>` for the background
- 1× `<linearGradient>` for card surfaces
- 3× `<linearGradient>` for icon fill colors
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` for soft card shadows
- Multiple `<text>` elements with explicit `width` attributes for title, labels, percentages, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0B1220"/>
      <stop offset="0.55" stop-color="#101D33"/>
      <stop offset="1" stop-color="#172A46"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="120" x2="0" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.98"/>
      <stop offset="1" stop-color="#EEF4FA" stop-opacity="0.96"/>
    </linearGradient>

    <linearGradient id="orangeFill" x1="0" y1="210" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFC27A"/>
      <stop offset="1" stop-color="#F57C28"/>
    </linearGradient>

    <linearGradient id="blueFill" x1="0" y1="210" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8FD3FF"/>
      <stop offset="1" stop-color="#2176D2"/>
    </linearGradient>

    <linearGradient id="greenFill" x1="0" y1="210" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#BDEB8C"/>
      <stop offset="1" stop-color="#5DAE36"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="16"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02  0 0 0 0 0.06  0 0 0 0 0.12  0 0 0 0.24 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="1110" cy="90" r="170" fill="#2B7CD3" opacity="0.18" filter="url(#softGlow)"/>
  <circle cx="165" cy="655" r="210" fill="#F57C28" opacity="0.12" filter="url(#softGlow)"/>

  <text x="80" y="78" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#FFFFFF">
    Pictogram Percentage Fill
  </text>
  <text x="82" y="118" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#AFC1D8">
    Three executive KPI icons use the same silhouette twice: neutral total underneath, colored lower slice on top.
  </text>

  <!-- Card 1 -->
  <rect x="90" y="170" width="330" height="430" rx="34" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
  <circle cx="132" cy="214" r="10" fill="#F57C28"/>
  <text x="150" y="221" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26364A">Customer Adoption</text>

  <g transform="translate(255 365)">
    <path d="M0,-150 C70,-55 105,0 105,70 C105,140 58,185 0,185 C-58,185 -105,140 -105,70 C-105,0 -70,-55 0,-150 Z"
          fill="#D9E1EA"/>
    <path d="M-43,-90 C-83,-32 -105,18 -105,70 C-105,140 -58,185 0,185 C58,185 105,140 105,70 C105,18 83,-32 43,-90 Z"
          fill="url(#orangeFill)"/>
    <line x1="-42" y1="-90" x2="42" y2="-90" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.88"/>
    <path d="M-32,-14 C-15,-42 4,-66 22,-88" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.22"/>
  </g>

  <text x="152" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#172A46" text-anchor="middle">82%</text>
  <text x="142" y="580" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#607086" text-anchor="middle">
    active users reached
  </text>

  <!-- Card 2 -->
  <rect x="475" y="170" width="330" height="430" rx="34" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
  <circle cx="517" cy="214" r="10" fill="#2176D2"/>
  <text x="535" y="221" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26364A">Cloud Migration</text>

  <g transform="translate(640 365)">
    <path d="M0,-150 C70,-55 105,0 105,70 C105,140 58,185 0,185 C-58,185 -105,140 -105,70 C-105,0 -70,-55 0,-150 Z"
          fill="#D9E1EA"/>
    <path d="M-76,-40 C-96,-5 -105,30 -105,70 C-105,140 -58,185 0,185 C58,185 105,140 105,70 C105,30 96,-5 76,-40 Z"
          fill="url(#blueFill)"/>
    <line x1="-76" y1="-40" x2="76" y2="-40" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.88"/>
    <path d="M-40,32 C-20,-2 12,-20 42,-32" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.20"/>
  </g>

  <text x="537" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#172A46" text-anchor="middle">67%</text>
  <text x="527" y="580" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#607086" text-anchor="middle">
    workloads transitioned
  </text>

  <!-- Card 3 -->
  <rect x="860" y="170" width="330" height="430" rx="34" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
  <circle cx="902" cy="214" r="10" fill="#5DAE36"/>
  <text x="920" y="221" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26364A">Efficiency Gain</text>

  <g transform="translate(1025 365)">
    <path d="M0,-150 C70,-55 105,0 105,70 C105,140 58,185 0,185 C-58,185 -105,140 -105,70 C-105,0 -70,-55 0,-150 Z"
          fill="#D9E1EA"/>
    <path d="M-101,30 C-104,43 -105,57 -105,70 C-105,140 -58,185 0,185 C58,185 105,140 105,70 C105,57 104,43 101,30 Z"
          fill="url(#greenFill)"/>
    <line x1="-100" y1="30" x2="100" y2="30" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.88"/>
    <path d="M-46,82 C-18,55 25,45 62,36" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" opacity="0.20"/>
  </g>

  <text x="922" y="548" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#172A46" text-anchor="middle">54%</text>
  <text x="912" y="580" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#607086" text-anchor="middle">
    process time reduced
  </text>

  <text x="80" y="668" width="1120" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8EA2BC">
    Implementation note: each colored area is a standalone editable path representing the lower percentage slice of the icon, not a masked rectangle.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not apply `clip-path` to a `<path>` icon; PPT-Master only preserves clipping reliably on `<image>`, and clipped editable shapes may be ignored.
- ❌ Do not use `<mask>` to reveal the lower fill band; masks are a hard-fail pattern for this pipeline.
- ❌ Do not use `<use href="#icon">` to duplicate the icon silhouette; repeat the actual `<path d="...">` instead.
- ❌ Do not fake the fill with a plain rectangle laid over the icon unless the icon is rectangular; the colored fill must conform to the pictogram silhouette.
- ❌ Do not rasterize the whole pictogram if editability matters; keep the neutral icon and colored fill as separate native paths.

## Composition notes
- Keep the pictogram large enough to read instantly; the icon should occupy roughly 45–55% of each card’s height.
- Place the percentage label directly below the icon so the filled shape and number reinforce each other.
- Use a muted neutral icon base, then reserve saturated color only for the filled portion and small accent badge.
- For comparison layouts, align all pictogram baselines and use identical icon dimensions so the fill heights are visually comparable.