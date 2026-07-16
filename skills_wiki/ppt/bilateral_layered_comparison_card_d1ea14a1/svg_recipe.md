# SVG Recipe — Bilateral Layered Comparison Card

## Visual mechanism
A mirrored A/B comparison layout uses two rounded white base panels, layered horizontal pill tabs, and oversized circular hubs that overlap the tabs to create a premium stacked-card interface. The center “V/S” pivot remains open and calm, while each side uses a distinct gradient color system and soft shadows to imply depth.

## SVG primitives needed
- 1× `<rect>` for the full-slide cool gray background
- 2× decorative `<path>` shapes for subtle oversized background color washes
- 2× large rounded `<rect>` base panels with soft drop shadows
- 8× rounded `<rect>` pill tabs, four per side, stacked vertically and partially hidden under the hubs
- 4× `<circle>` elements for the two dark outer hub rings and two bright gradient-filled inner hubs
- 1× rounded `<rect>` for the center “V/S” badge
- 26× `<text>` elements for titles, tab numbers, tab labels, hub letters, center label, and footer note
- 4× gradients: background wash, blue tab/hub gradients, red tab/hub gradients, and center badge fill
- 3× `<filter>` effects: large soft card shadow, tab shadow, and hub glow/shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueTabGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5DADE2"/>
      <stop offset="55%" stop-color="#3498DB"/>
      <stop offset="100%" stop-color="#21618C"/>
    </linearGradient>
    <linearGradient id="redTabGrad" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="#F1948A"/>
      <stop offset="55%" stop-color="#EC7063"/>
      <stop offset="100%" stop-color="#922B21"/>
    </linearGradient>
    <radialGradient id="blueHubGrad" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#B9E6FF"/>
      <stop offset="45%" stop-color="#3498DB"/>
      <stop offset="100%" stop-color="#154360"/>
    </radialGradient>
    <radialGradient id="redHubGrad" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFD1CC"/>
      <stop offset="45%" stop-color="#E74C3C"/>
      <stop offset="100%" stop-color="#641E16"/>
    </radialGradient>
    <linearGradient id="vsGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EAF1F4"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feFlood flood-color="#23323A" flood-opacity="0.16" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="tabShadow" x="-15%" y="-30%" width="130%" height="170%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feFlood flood-color="#0B1B2B" flood-opacity="0.18" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="hubShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="15" result="blur"/>
      <feFlood flood-color="#06131A" flood-opacity="0.28" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F0F5F5"/>
  <path d="M-80,130 C110,20 250,45 365,155 C470,255 430,370 240,398 C80,421 -35,335 -80,130 Z" fill="#DDEFF8" opacity="0.55"/>
  <path d="M1360,585 C1175,705 1015,678 900,565 C795,462 840,345 1028,322 C1198,302 1308,395 1360,585 Z" fill="#F9DFDD" opacity="0.62"/>

  <rect x="632" y="112" width="16" height="496" rx="8" fill="#D9E3E7"/>
  <rect x="590" y="296" width="100" height="100" rx="30" fill="url(#vsGrad)" filter="url(#cardShadow)"/>
  <text x="640" y="356" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#263A45">V/S</text>
  <text x="640" y="405" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2" fill="#7C8B93">COMPARISON</text>

  <rect x="82" y="142" width="468" height="438" rx="42" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="730" y="142" width="468" height="438" rx="42" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <text x="130" y="210" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#154360">OPTION A</text>
  <text x="130" y="238" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7D8C95">Scalable, efficient, and built for adoption</text>
  <text x="902" y="210" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#922B21">OPTION B</text>
  <text x="1150" y="238" width="330" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7D8C95">Expressive, premium, and optimized for impact</text>

  <rect x="146" y="272" width="332" height="58" rx="29" fill="#5DADE2" filter="url(#tabShadow)"/>
  <rect x="122" y="346" width="356" height="58" rx="29" fill="#3498DB" filter="url(#tabShadow)"/>
  <rect x="146" y="420" width="332" height="58" rx="29" fill="#2874A6" filter="url(#tabShadow)"/>
  <rect x="122" y="494" width="356" height="58" rx="29" fill="url(#blueTabGrad)" filter="url(#tabShadow)"/>

  <text x="184" y="309" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">01</text>
  <text x="244" y="309" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Lower operating cost</text>
  <text x="160" y="383" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">02</text>
  <text x="220" y="383" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Fast rollout path</text>
  <text x="184" y="457" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">03</text>
  <text x="244" y="457" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Simple governance</text>
  <text x="160" y="531" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">04</text>
  <text x="220" y="531" width="225" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Broad team adoption</text>

  <rect x="802" y="272" width="332" height="58" rx="29" fill="#F1948A" filter="url(#tabShadow)"/>
  <rect x="802" y="346" width="356" height="58" rx="29" fill="#EC7063" filter="url(#tabShadow)"/>
  <rect x="802" y="420" width="332" height="58" rx="29" fill="#C0392B" filter="url(#tabShadow)"/>
  <rect x="802" y="494" width="356" height="58" rx="29" fill="url(#redTabGrad)" filter="url(#tabShadow)"/>

  <text x="1054" y="309" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">01</text>
  <text x="855" y="309" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Higher brand lift</text>
  <text x="1078" y="383" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">02</text>
  <text x="855" y="383" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Premium experience</text>
  <text x="1054" y="457" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">03</text>
  <text x="855" y="457" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Deeper analytics</text>
  <text x="1078" y="531" width="48" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">04</text>
  <text x="855" y="531" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Stronger differentiation</text>

  <circle cx="478" cy="412" r="114" fill="#154360" filter="url(#hubShadow)"/>
  <circle cx="478" cy="412" r="82" fill="url(#blueHubGrad)"/>
  <text x="478" y="397" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">SIDE</text>
  <text x="478" y="456" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="900" fill="#FFFFFF">A</text>

  <circle cx="802" cy="412" r="114" fill="#641E16" filter="url(#hubShadow)"/>
  <circle cx="802" cy="412" r="82" fill="url(#redHubGrad)"/>
  <text x="802" y="397" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#FFFFFF">SIDE</text>
  <text x="802" y="456" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="900" fill="#FFFFFF">B</text>

  <text x="640" y="650" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7C8B93">Use this card to compare products, plans, strategies, vendors, or competing operating models.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use actual cutout masks to make the tabs disappear behind the hub; simply layer tabs first and circles afterward.
- ❌ Do not place filters on `<line>` elements for the center divider; use a narrow rounded `<rect>` instead.
- ❌ Do not use `<use>` or `<symbol>` to duplicate the tab rows; duplicate the editable shapes directly.
- ❌ Do not overfill the center channel with labels or connectors; the negative space is what makes the bilateral comparison feel premium.
- ❌ Do not make both sides the same color family; the technique depends on immediate left/right semantic separation.

## Composition notes
- Keep the two base panels symmetrical, each about 36–38% of slide width, with a generous central channel for the “V/S” pivot.
- Draw order is essential: background washes → base cards → tabs → hub circles → text.
- Let each hub overlap the inner ends of the tabs by 70–100 px so the tabs feel anchored behind the circle.
- Use a cool blue family on one side and a warm red/pink family on the other; keep all body copy neutral gray to preserve hierarchy.