# SVG Recipe — Algorithmic Dynamic Organization Chart

## Visual mechanism
An auto-balanced hierarchy is rendered as a mathematically spaced tree: every parent is centered above the total horizontal span of its children, while gray elbow connector buses route cleanly between levels. Rounded, shadowed color-coded nodes distinguish hierarchy levels and make the chart feel like a polished executive org map rather than a flat diagram.

## SVG primitives needed
- 1× `<rect>` for the soft slide background
- 2× `<path>` for subtle decorative background blobs / contour accents
- 16× `<rect>` for rounded employee node cards
- 8× `<path>` for orthogonal elbow connector buses between parents and children
- 34× `<text>` for slide title, subtitle, employee names, and roles
- 5× `<linearGradient>` for background and hierarchy-specific node fills
- 1× `<radialGradient>` for the ambient decorative glow
- 1× `<filter id="nodeShadow">` using `feOffset + feGaussianBlur + feMerge`, applied directly to node `<rect>` cards

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <linearGradient id="execGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#244D9A"/><stop offset="100%" stop-color="#102E69"/>
    </linearGradient>
    <linearGradient id="dirGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00A3A3"/><stop offset="100%" stop-color="#006D72"/>
    </linearGradient>
    <linearGradient id="mgrGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F28B25"/><stop offset="100%" stop-color="#C75C00"/>
    </linearGradient>
    <linearGradient id="staffGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7E57C2"/><stop offset="100%" stop-color="#3F7E44"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#B8E7FF" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#B8E7FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset in="SourceAlpha" dx="0" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M980 36 C1125 18 1210 84 1248 190 C1192 164 1114 162 1045 192 C983 219 930 212 896 165 C862 117 884 55 980 36 Z" fill="url(#glow)"/>
  <path d="M40 612 C142 546 226 566 301 636 C221 626 152 655 84 704 C55 702 33 683 24 656 C18 638 24 623 40 612 Z" fill="#DCE8F5" opacity="0.55"/>

  <text x="56" y="50" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#182233">Company Organization Chart</text>
  <text x="58" y="82" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">Auto-balanced tree layout: parent nodes are centered over the computed width of their child subtrees</text>

  <path d="M640 172 V204 M280 204 H1000 M280 204 V230 M640 204 V230 M1000 204 V230" fill="none" stroke="#B5C0CC" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M280 296 V330 M170 330 H355 M170 330 V360 M355 330 V360" fill="none" stroke="#B5C0CC" stroke-width="2" stroke-linecap="round"/>
  <path d="M640 296 V330 M540 330 H725 M540 330 V360 M725 330 V360" fill="none" stroke="#B5C0CC" stroke-width="2" stroke-linecap="round"/>
  <path d="M1000 296 V330 M910 330 H1095 M910 330 V360 M1095 330 V360" fill="none" stroke="#B5C0CC" stroke-width="2" stroke-linecap="round"/>
  <path d="M170 418 V455 M142.5 455 H292.5 M142.5 455 V495 M292.5 455 V495" fill="none" stroke="#CCD4DD" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M725 418 V455 H672.5 V495" fill="none" stroke="#CCD4DD" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M910 418 V455 M872.5 455 H1022.5 M872.5 455 V495 M1022.5 455 V495" fill="none" stroke="#CCD4DD" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M1095 418 V455 H1172.5 V495" fill="none" stroke="#CCD4DD" stroke-width="1.8" stroke-linecap="round"/>

  <rect x="530" y="98" width="220" height="74" rx="18" fill="url(#execGrad)" filter="url(#nodeShadow)"/>
  <text x="640" y="128" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Patti Fernandez</text>
  <text x="640" y="153" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D9E7FF">President</text>

  <rect x="185" y="230" width="190" height="66" rx="16" fill="url(#dirGrad)" filter="url(#nodeShadow)"/>
  <text x="280" y="257" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Kevin Stratvert</text>
  <text x="280" y="279" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#DDFBFB">VP Marketing</text>

  <rect x="545" y="230" width="190" height="66" rx="16" fill="url(#dirGrad)" filter="url(#nodeShadow)"/>
  <text x="640" y="257" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Miriam Graham</text>
  <text x="640" y="279" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#DDFBFB">VP Operations</text>

  <rect x="905" y="230" width="190" height="66" rx="16" fill="url(#dirGrad)" filter="url(#nodeShadow)"/>
  <text x="1000" y="257" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Lee Gu</text>
  <text x="1000" y="279" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#DDFBFB">VP Engineering</text>

  <rect x="85" y="360" width="170" height="58" rx="14" fill="url(#mgrGrad)" filter="url(#nodeShadow)"/>
  <text x="170" y="384" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="700" fill="#FFFFFF">Megan Bowen</text>
  <text x="170" y="404" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF1E2">Marketing Manager</text>

  <rect x="270" y="360" width="170" height="58" rx="14" fill="url(#mgrGrad)" filter="url(#nodeShadow)"/>
  <text x="355" y="384" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="700" fill="#FFFFFF">Alex Wilber</text>
  <text x="355" y="404" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF1E2">PR Lead</text>

  <rect x="455" y="360" width="170" height="58" rx="14" fill="url(#mgrGrad)" filter="url(#nodeShadow)"/>
  <text x="540" y="384" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="700" fill="#FFFFFF">Lidia Holloway</text>
  <text x="540" y="404" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF1E2">Logistics</text>

  <rect x="640" y="360" width="170" height="58" rx="14" fill="url(#mgrGrad)" filter="url(#nodeShadow)"/>
  <text x="725" y="384" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="700" fill="#FFFFFF">Diego Siciliani</text>
  <text x="725" y="404" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF1E2">HR Manager</text>

  <rect x="825" y="360" width="170" height="58" rx="14" fill="url(#mgrGrad)" filter="url(#nodeShadow)"/>
  <text x="910" y="384" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="700" fill="#FFFFFF">Grady Archie</text>
  <text x="910" y="404" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF1E2">Lead Developer</text>

  <rect x="1010" y="360" width="170" height="58" rx="14" fill="url(#mgrGrad)" filter="url(#nodeShadow)"/>
  <text x="1095" y="384" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="700" fill="#FFFFFF">Johanna Lorenz</text>
  <text x="1095" y="404" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFF1E2">QA Lead</text>

  <rect x="70" y="495" width="145" height="46" rx="12" fill="url(#staffGrad)" filter="url(#nodeShadow)"/>
  <text x="142.5" y="523" width="125" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" font-weight="700" fill="#FFFFFF">Campaigns Lead</text>
  <rect x="220" y="495" width="145" height="46" rx="12" fill="url(#staffGrad)" filter="url(#nodeShadow)"/>
  <text x="292.5" y="523" width="125" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" font-weight="700" fill="#FFFFFF">Design Lead</text>
  <rect x="600" y="495" width="145" height="46" rx="12" fill="url(#staffGrad)" filter="url(#nodeShadow)"/>
  <text x="672.5" y="523" width="125" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" font-weight="700" fill="#FFFFFF">Recruiting</text>
  <rect x="800" y="495" width="145" height="46" rx="12" fill="url(#staffGrad)" filter="url(#nodeShadow)"/>
  <text x="872.5" y="523" width="125" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" font-weight="700" fill="#FFFFFF">Frontend</text>
  <rect x="950" y="495" width="145" height="46" rx="12" fill="url(#staffGrad)" filter="url(#nodeShadow)"/>
  <text x="1022.5" y="523" width="125" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" font-weight="700" fill="#FFFFFF">Platform</text>
  <rect x="1100" y="495" width="145" height="46" rx="12" fill="url(#staffGrad)" filter="url(#nodeShadow)"/>
  <text x="1172.5" y="523" width="125" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" font-weight="700" fill="#FFFFFF">QA Ops</text>

  <text x="56" y="676" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7A8694">Layout hint: compute each subtree width first, then assign x positions from left to right so sibling groups never overlap.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to duplicate employees; emit each node as its own editable `<rect>` and `<text>`.
- ❌ Do not put `filter` on connector `<line>` or `<path>` strokes; keep connector buses flat and apply shadows only to node cards.
- ❌ Do not use `marker-end` for connector arrows; org charts read better with clean elbow buses, and markers may disappear.
- ❌ Do not rely on PowerPoint SmartArt-style auto layout after translation; calculate final SVG x/y positions before export.
- ❌ Do not clip non-image elements; if headshots are added, apply `clipPath` only to `<image>` avatars.

## Composition notes
- Reserve the top 90px for title and algorithm explanation; keep the tree itself centered in the remaining slide area.
- Use consistent vertical bands: executive, directors, managers, staff. Each band should have equal y spacing and enough room for connector elbows.
- Compute child group widths before drawing nodes; the visual quality comes from parents being centered over the full span of descendants.
- Keep connector color low-contrast gray so hierarchy color carries the emphasis, while shadows separate dense node clusters from the background.