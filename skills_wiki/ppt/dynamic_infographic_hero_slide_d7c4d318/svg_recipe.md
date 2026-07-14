# SVG Recipe — Dynamic Infographic Hero Slide

## Visual mechanism
A full-bleed atmospheric photo is darkened with a branded overlay, then interrupted by an oversized transparent hero cutout that breaks the slide frame. The right side becomes a polished infographic zone: translucent panels, compact timeline rows, icon-led achievements, and oversized editorial typography.

## SVG primitives needed
- 2× `<image>` for the full-bleed background photo and the transparent frame-breaking hero subject
- 4× clipped `<image>` elements for circular team/product/logo badges inside the timeline
- 12× `<rect>` for overlay masks, translucent information panels, stat cards, dividers, and accent bars
- 8× `<circle>` for badge frames, timeline nodes, and icon backplates
- 6× `<path>` for decorative diagonal ribbons, trophy/crown/bolt icons, and dynamic accent shapes
- 4× `<line>` for clean timeline connectors and panel separators
- 18× `<text>` with explicit `width` attributes for title, subtitle, labels, years, metrics, and captions
- 1× `<linearGradient>` for the dark-to-brand overlay wash
- 1× `<linearGradient>` for gold accent fills
- 1× `<filter id="softShadow">` applied to cards, panels, and the hero image
- 1× `<filter id="titleGlow">` applied to the main title for premium contrast
- 4× `<clipPath>` with circles applied only to `<image>` logo badges

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#090A12" stop-opacity="0.88"/>
      <stop offset="48%" stop-color="#241038" stop-opacity="0.68"/>
      <stop offset="100%" stop-color="#FDB927" stop-opacity="0.24"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE08A"/>
      <stop offset="55%" stop-color="#FDB927"/>
      <stop offset="100%" stop-color="#C98700"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="titleGlow" x="-15%" y="-25%" width="130%" height="160%">
      <feGaussianBlur stdDeviation="3" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="logoClip1" clipPathUnits="userSpaceOnUse"><circle cx="735" cy="252" r="22"/></clipPath>
    <clipPath id="logoClip2" clipPathUnits="userSpaceOnUse"><circle cx="735" cy="322" r="22"/></clipPath>
    <clipPath id="logoClip3" clipPathUnits="userSpaceOnUse"><circle cx="735" cy="392" r="22"/></clipPath>
    <clipPath id="logoClip4" clipPathUnits="userSpaceOnUse"><circle cx="735" cy="462" r="22"/></clipPath>
  </defs>

  <image href="https://images.example.com/arena-lights-crowd-background.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#05060B" opacity="0.18"/>

  <path d="M-80 620 C160 560 270 665 450 585 C565 535 640 568 720 540 L720 780 L-80 780 Z" fill="#000000" opacity="0.32"/>
  <path d="M870 -40 L1330 -40 L1195 220 L775 150 Z" fill="url(#goldGrad)" opacity="0.18"/>
  <path d="M1015 680 L1280 560 L1280 720 L960 720 Z" fill="#FFFFFF" opacity="0.08"/>

  <image href="https://images.example.com/transparent-png-athlete-hero-cutout.png" x="-78" y="62" width="650" height="735" preserveAspectRatio="xMidYMax meet" filter="url(#softShadow)"/>

  <rect x="48" y="52" width="118" height="6" rx="3" fill="url(#goldGrad)"/>
  <text x="48" y="118" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800" fill="#FFFFFF" letter-spacing="-2" filter="url(#titleGlow)">MAYA CHEN</text>
  <text x="52" y="158" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="600" fill="#FDB927" letter-spacing="3">PRODUCT VISIONARY · AI PLATFORM LEAD</text>
  <text x="52" y="198" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ECECF4" opacity="0.86">
    Turning complex technology into market-defining products with measurable adoption, revenue, and customer impact.
  </text>

  <rect x="575" y="94" width="310" height="538" rx="28" fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <rect x="914" y="94" width="300" height="538" rx="28" fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <rect x="596" y="118" width="72" height="5" rx="2.5" fill="url(#goldGrad)"/>
  <rect x="935" y="118" width="72" height="5" rx="2.5" fill="url(#goldGrad)"/>

  <text x="596" y="158" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#FFFFFF">CAREER ARC</text>
  <text x="935" y="158" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#FFFFFF">SIGNATURE WINS</text>

  <line x1="628" y1="252" x2="628" y2="462" stroke="#FDB927" stroke-width="3" opacity="0.75"/>
  <circle cx="628" cy="252" r="8" fill="#FDB927"/>
  <circle cx="628" cy="322" r="8" fill="#FDB927"/>
  <circle cx="628" cy="392" r="8" fill="#FDB927"/>
  <circle cx="628" cy="462" r="8" fill="#FDB927"/>

  <image href="https://images.example.com/logo-startup-or-team-alpha.png" x="713" y="230" width="44" height="44" clip-path="url(#logoClip1)"/>
  <image href="https://images.example.com/logo-cloud-platform-beta.png" x="713" y="300" width="44" height="44" clip-path="url(#logoClip2)"/>
  <image href="https://images.example.com/logo-enterprise-ai-gamma.png" x="713" y="370" width="44" height="44" clip-path="url(#logoClip3)"/>
  <image href="https://images.example.com/logo-global-lab-delta.png" x="713" y="440" width="44" height="44" clip-path="url(#logoClip4)"/>

  <text x="652" y="244" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FDB927">2016</text>
  <text x="770" y="244" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Founding PM</text>
  <text x="770" y="266" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9DAE8">0→1 analytics suite</text>

  <text x="652" y="314" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FDB927">2019</text>
  <text x="770" y="314" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Scale Lead</text>
  <text x="770" y="336" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9DAE8">15M monthly users</text>

  <text x="652" y="384" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FDB927">2022</text>
  <text x="770" y="384" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">AI Director</text>
  <text x="770" y="406" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9DAE8">$480M ARR line</text>

  <text x="652" y="454" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FDB927">2025</text>
  <text x="770" y="454" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Chief Product</text>
  <text x="770" y="476" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9DAE8">Global platform org</text>

  <rect x="596" y="530" width="248" height="72" rx="18" fill="#05060B" opacity="0.52"/>
  <text x="616" y="558" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="900" fill="#FFFFFF">42%</text>
  <text x="696" y="551" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FDB927">FASTER LAUNCH</text>
  <text x="696" y="572" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DADBEA">Average cycle-time reduction across portfolio</text>

  <rect x="936" y="198" width="246" height="84" rx="20" fill="#05060B" opacity="0.48"/>
  <rect x="936" y="306" width="246" height="84" rx="20" fill="#05060B" opacity="0.48"/>
  <rect x="936" y="414" width="246" height="84" rx="20" fill="#05060B" opacity="0.48"/>

  <circle cx="978" cy="240" r="23" fill="url(#goldGrad)"/>
  <path d="M968 232 L978 219 L988 232 L1002 229 L994 243 L998 258 L978 251 L958 258 L962 243 L954 229 Z" fill="#16100A"/>
  <text x="1018" y="235" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="900" fill="#FFFFFF">3×</text>
  <text x="1018" y="260" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#E8E8F2">Product of the Year</text>

  <circle cx="978" cy="348" r="23" fill="url(#goldGrad)"/>
  <path d="M964 361 L992 361 L988 341 C982 346 976 346 970 341 Z M968 337 L974 328 L978 339 L986 328 L991 337" fill="#16100A"/>
  <text x="1018" y="343" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="900" fill="#FFFFFF">$1.2B</text>
  <text x="1018" y="368" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#E8E8F2">Pipeline influenced</text>

  <circle cx="978" cy="456" r="23" fill="url(#goldGrad)"/>
  <path d="M982 431 L960 461 L976 459 L972 481 L998 448 L982 451 Z" fill="#16100A"/>
  <text x="1018" y="451" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="900" fill="#FFFFFF">89</text>
  <text x="1018" y="476" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#E8E8F2">NPS in beta cohorts</text>

  <line x1="936" y1="540" x2="1182" y2="540" stroke="#FFFFFF" stroke-width="1.5" opacity="0.24"/>
  <text x="936" y="580" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" opacity="0.9">Executive profile snapshot</text>
  <text x="936" y="604" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D8D9E7" opacity="0.78">Use this footer for a quote, source, keynote date, or short proof point.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to isolate the hero subject; use a pre-cut transparent PNG instead.
- ❌ Do not clip the hero image with a rectangle if the goal is frame-breaking impact; let it run off the slide edge.
- ❌ Do not apply `clip-path` to panels, paths, or text; clipping is reliable here only on `<image>`.
- ❌ Do not use `marker-end` for timeline arrows; use simple `<line>` connectors and circles instead.
- ❌ Do not overfill both sides with text; the hero image needs breathing room to feel cinematic.

## Composition notes
- Keep the hero cutout oversized, usually occupying 40–50% of the slide width and extending beyond the bottom or left edge.
- Reserve the right 50% for structured data panels; align all infographic rows to a strict vertical rhythm.
- Use one strong accent color repeatedly for title rules, timeline nodes, icon circles, and key numbers.
- Darken the background enough that white text and translucent panels remain legible, but keep some photographic texture visible for depth.