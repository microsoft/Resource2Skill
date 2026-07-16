# SVG Recipe — Infographic KPI Modular Dashboard

## Visual mechanism
A dark, photo-tinted executive header with a bright angled ribbon establishes the theme, while the lower canvas converts KPIs into four equal geometric modules with circular badges, icon anchors, and oversized percentage typography. The design works by making every metric feel like a standalone “tile” rather than a row in a table.

## SVG primitives needed
- 1× `<image>` for the moody urban/corporate header photo, clipped to the header area.
- 1× `<clipPath>` with rounded `<rect>` for the header image crop.
- 3× `<linearGradient>` for header tint, cyan ribbon depth, and soft page background.
- 1× `<filter id="softShadow">` applied to cards, ribbon, and KPI circles.
- 1× `<filter id="cyanGlow">` applied to the ribbon accent for a premium neon edge.
- 1× large `<rect>` for the slide background.
- 1× clipped `<image>` plus 1× translucent `<rect>` overlay for the dark photographic header.
- 4× `<path>` for angled ribbon/chevron header shapes and decorative diagonal shards.
- 4× `<rect>` for white KPI cards with subtle shadows.
- 4× `<circle>` for colored KPI icon badges.
- 4× `<circle>` for pale outer halo rings behind KPI badges.
- 10–14× `<path>` / `<line>` primitives for simple editable white icons inside the KPI circles.
- Multiple `<text width="...">` elements for title, eyebrow, KPI values, labels, and captions.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="headerClip">
      <rect x="0" y="0" width="1280" height="235" rx="0"/>
    </clipPath>

    <linearGradient id="pageBg" x1="0" y1="235" x2="0" y2="720">
      <stop offset="0" stop-color="#F8FAFC"/>
      <stop offset="1" stop-color="#EEF3F7"/>
    </linearGradient>

    <linearGradient id="headerTint" x1="0" y1="0" x2="1280" y2="235">
      <stop offset="0" stop-color="#17232B" stop-opacity="0.92"/>
      <stop offset="0.55" stop-color="#223139" stop-opacity="0.82"/>
      <stop offset="1" stop-color="#101820" stop-opacity="0.95"/>
    </linearGradient>

    <linearGradient id="cyanRibbon" x1="160" y1="88" x2="1120" y2="160">
      <stop offset="0" stop-color="#00D4FF"/>
      <stop offset="0.48" stop-color="#00AEEF"/>
      <stop offset="1" stop-color="#008FD1"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>

  <image x="0" y="0" width="1280" height="235" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#headerClip)"
         href="https://images.example.com/1920x420/dark-night-city-skyline-corporate-buildings.jpg"/>
  <rect x="0" y="0" width="1280" height="235" fill="url(#headerTint)"/>

  <path d="M0,196 L290,160 L520,235 L0,235 Z" fill="#00AEEF" opacity="0.14"/>
  <path d="M970,0 L1280,0 L1280,92 L1040,132 Z" fill="#00D4FF" opacity="0.13"/>
  <path d="M196,82 H1016 L1102,124 L1016,166 H196 L156,124 Z"
        fill="url(#cyanRibbon)" filter="url(#softShadow)"/>
  <path d="M196,172 H1016 L1068,198 H248 Z" fill="#006C96" opacity="0.42"/>
  <path d="M176,78 H214 L170,124 L214,170 H176 L132,124 Z" fill="#53E5FF" opacity="0.72" filter="url(#cyanGlow)"/>
  <path d="M1066,78 H1104 L1148,124 L1104,170 H1066 L1110,124 Z" fill="#53E5FF" opacity="0.72" filter="url(#cyanGlow)"/>

  <text x="242" y="53" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600"
        letter-spacing="2" fill="#A7DFF2">QUARTERLY PERFORMANCE DASHBOARD</text>
  <text x="245" y="137" width="790" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700"
        text-anchor="middle" fill="#FFFFFF" transform="translate(395 0)">Main Product Sales Overview</text>
  <text x="454" y="201" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        text-anchor="middle" fill="#B8C8D1">Four headline metrics distilled into executive-ready modules</text>

  <path d="M72,283 C160,244 235,257 292,304 C217,314 142,330 70,367 Z" fill="#00AEEF" opacity="0.045"/>
  <path d="M1046,630 C1108,560 1188,552 1268,610 L1280,720 L1038,720 Z" fill="#800080" opacity="0.045"/>

  <rect x="70" y="278" width="250" height="350" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="370" y="278" width="250" height="350" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="670" y="278" width="250" height="350" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="970" y="278" width="250" height="350" rx="28" fill="#FFFFFF" filter="url(#softShadow)"/>

  <circle cx="195" cy="350" r="82" fill="#009688" opacity="0.12"/>
  <circle cx="495" cy="350" r="82" fill="#F4A460" opacity="0.14"/>
  <circle cx="795" cy="350" r="82" fill="#800080" opacity="0.12"/>
  <circle cx="1095" cy="350" r="82" fill="#9ACD32" opacity="0.15"/>

  <circle cx="195" cy="350" r="62" fill="#009688" filter="url(#softShadow)"/>
  <circle cx="495" cy="350" r="62" fill="#F4A460" filter="url(#softShadow)"/>
  <circle cx="795" cy="350" r="62" fill="#800080" filter="url(#softShadow)"/>
  <circle cx="1095" cy="350" r="62" fill="#9ACD32" filter="url(#softShadow)"/>

  <path d="M168,337 H222 V376 H168 Z M176,326 H214 L222,337 H168 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <line x1="181" y1="354" x2="209" y2="354" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>

  <path d="M465,374 L465,335 M493,374 L493,317 M521,374 L521,347" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <path d="M462,332 L493,316 L522,338" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M795,313 C776,313 764,327 764,343 C764,354 770,361 778,368 L778,378 H812 L812,368 C821,361 826,353 826,343 C826,327 814,313 795,313 Z"
        fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <line x1="780" y1="392" x2="810" y2="392" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <line x1="785" y1="405" x2="805" y2="405" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>

  <circle cx="1095" cy="350" r="35" fill="none" stroke="#FFFFFF" stroke-width="7"/>
  <circle cx="1095" cy="350" r="17" fill="none" stroke="#FFFFFF" stroke-width="7"/>
  <line x1="1095" y1="306" x2="1095" y2="323" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
  <line x1="1095" y1="377" x2="1095" y2="394" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
  <line x1="1051" y1="350" x2="1068" y2="350" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
  <line x1="1122" y1="350" x2="1139" y2="350" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>

  <text x="85" y="478" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        text-anchor="middle" fill="#263238" transform="translate(110 0)">55%</text>
  <text x="385" y="478" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        text-anchor="middle" fill="#263238" transform="translate(110 0)">70%</text>
  <text x="685" y="478" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        text-anchor="middle" fill="#263238" transform="translate(110 0)">40%</text>
  <text x="985" y="478" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800"
        text-anchor="middle" fill="#263238" transform="translate(110 0)">60%</text>

  <text x="85" y="525" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        text-anchor="middle" fill="#009688" transform="translate(110 0)">Product A</text>
  <text x="385" y="525" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        text-anchor="middle" fill="#F4A460" transform="translate(110 0)">Product B</text>
  <text x="685" y="525" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        text-anchor="middle" fill="#800080" transform="translate(110 0)">Product C</text>
  <text x="985" y="525" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        text-anchor="middle" fill="#7DAA25" transform="translate(110 0)">Product D</text>

  <text x="105" y="566" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        text-anchor="middle" fill="#7A8790" transform="translate(90 0)">Unit sales contribution across retail channels</text>
  <text x="405" y="566" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        text-anchor="middle" fill="#7A8790" transform="translate(90 0)">Fastest growth rate in the current quarter</text>
  <text x="705" y="566" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        text-anchor="middle" fill="#7A8790" transform="translate(90 0)">Innovation pipeline share in active launches</text>
  <text x="1005" y="566" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        text-anchor="middle" fill="#7A8790" transform="translate(90 0)">Strategic target completion for FY roadmap</text>

  <rect x="116" y="601" width="158" height="6" rx="3" fill="#009688"/>
  <rect x="416" y="601" width="158" height="6" rx="3" fill="#F4A460"/>
  <rect x="716" y="601" width="158" height="6" rx="3" fill="#800080"/>
  <rect x="1016" y="601" width="158" height="6" rx="3" fill="#9ACD32"/>
</svg>
```

## Avoid in this skill
- ❌ Don’t build the dashboard as a literal table with gridlines; the effect depends on separated, poster-like KPI modules.
- ❌ Don’t use `<marker-end>` for arrows or connector embellishments; if arrows are needed, use native `<line>` plus separate triangle `<path>` heads.
- ❌ Don’t apply `filter` to `<line>` elements for icon shadows; filters on lines may be dropped, so keep shadows on circles, cards, paths, or rectangles.
- ❌ Don’t clip non-image elements; use `clipPath` only on the header photo or other `<image>` crops.
- ❌ Don’t overcrowd each card with secondary numbers. One dominant KPI, one label, one short explanation is the visual limit.

## Composition notes
- Keep the header to roughly the top 30–33% of the slide; it provides mood and contrast but should not compete with the KPI modules.
- Use four equal columns with generous gutters so each metric reads as an independent module.
- The KPI number should be the largest text on the slide after the title; supporting text should be muted gray and short.
- Repeat the same module structure, but vary badge colors to create a rhythmic left-to-right infographic sequence.