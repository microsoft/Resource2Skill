# SVG Recipe — Organic Grid Reveal Sequence

## Visual mechanism
A calm sage-green canvas uses botanical blobs, dotted textures, and a spacious 2×2 agenda grid to soften a structured list. The reveal is achieved by duplicating the slide/SVG state and adding one item group at a time, so each numbered agenda point appears sequentially without relying on unsupported SVG animation.

## SVG primitives needed
- 1× `<rect>` for the full-slide sage background
- 4× `<path>` for large organic corner blobs and botanical accent shapes
- 2× `<linearGradient>` for dimensional blob fills
- 1× `<filter id="softShadow">` applied to blob/card-like elements for subtle depth
- 1× `<filter id="badgeGlow">` applied to number badges for a soft raised effect
- 31× `<circle>` for numbered badges and dotted botanical texture clusters
- 8× `<line>` for simple botanical leaf/stem accents
- 13× `<text>` for title, badge numbers, item titles, and item descriptions
- 4× grouped agenda item clusters; duplicate slides and progressively include groups `reveal-01` through `reveal-04`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sageBlob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#789077"/>
      <stop offset="100%" stop-color="#4e6655"/>
    </linearGradient>
    <linearGradient id="forestBlob" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#2f3e33"/>
      <stop offset="100%" stop-color="#506552"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="badgeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#d4d9cd"/>

  <path d="M1102,-28 C1188,-52 1276,4 1308,92 C1338,176 1294,278 1208,320 C1126,360 1040,336 1004,286 C966,234 1002,166 1054,126 C1108,84 1070,4 1102,-28 Z"
        fill="url(#sageBlob)" opacity="0.95" filter="url(#softShadow)"/>
  <path d="M1138,96 C1204,112 1264,166 1276,238 C1288,310 1234,378 1156,394 C1088,408 1016,376 1000,318 C982,256 1030,204 1078,176 C1122,150 1092,86 1138,96 Z"
        fill="#314238" opacity="0.82"/>
  <path d="M-88,612 C-40,534 58,518 126,560 C188,598 202,676 154,736 L-88,736 Z"
        fill="url(#forestBlob)" opacity="0.98"/>
  <path d="M-42,330 C38,302 94,350 86,418 C78,486 10,516 -56,492 Z"
        fill="#2f3e33" opacity="0.95"/>

  <g stroke="#263228" stroke-width="3" stroke-linecap="round" opacity="0.92">
    <line x1="30" y1="196" x2="98" y2="122"/>
    <line x1="36" y1="208" x2="104" y2="160"/>
    <line x1="40" y1="220" x2="120" y2="194"/>
    <line x1="34" y1="232" x2="116" y2="230"/>
    <line x1="26" y1="244" x2="100" y2="266"/>
    <line x1="1206" y1="0" x2="1238" y2="62" stroke="#eef0e6" stroke-width="2"/>
    <line x1="1246" y1="20" x2="1218" y2="92" stroke="#eef0e6" stroke-width="2"/>
    <line x1="1270" y1="48" x2="1216" y2="126" stroke="#eef0e6" stroke-width="2"/>
  </g>

  <g fill="#1d251f" opacity="0.95">
    <circle cx="1016" cy="58" r="4"/><circle cx="1046" cy="40" r="4"/><circle cx="1076" cy="32" r="4"/>
    <circle cx="996" cy="90" r="4"/><circle cx="1026" cy="76" r="4"/><circle cx="1058" cy="62" r="4"/>
    <circle cx="982" cy="124" r="4"/><circle cx="1010" cy="110" r="4"/><circle cx="1040" cy="94" r="4"/>
    <circle cx="82" cy="640" r="4"/><circle cx="110" cy="622" r="4"/><circle cx="138" cy="606" r="4"/>
    <circle cx="62" cy="676" r="4"/><circle cx="92" cy="658" r="4"/><circle cx="122" cy="642" r="4"/>
    <circle cx="42" cy="706" r="4"/><circle cx="72" cy="690" r="4"/><circle cx="104" cy="674" r="4"/>
  </g>

  <text x="70" y="92" width="620" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#1f2b24">
    Table of contents
  </text>

  <g id="reveal-01">
    <circle cx="154" cy="300" r="54" fill="#72886f" filter="url(#badgeGlow)"/>
    <text x="117" y="319" width="75" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#ffffff">01</text>
    <text x="242" y="280" width="300" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2f3b33">Experience</text>
    <text x="244" y="318" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#101813">
      <tspan x="244" dy="0">Map the proof points and</tspan><tspan x="244" dy="24">context behind the story</tspan>
    </text>
  </g>

  <g id="reveal-02">
    <circle cx="704" cy="300" r="54" fill="#72886f" filter="url(#badgeGlow)"/>
    <text x="667" y="319" width="78" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#ffffff">02</text>
    <text x="790" y="280" width="300" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2f3b33">Education</text>
    <text x="792" y="318" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#101813">
      <tspan x="792" dy="0">Introduce the framework</tspan><tspan x="792" dy="24">that shapes the discussion</tspan>
    </text>
  </g>

  <g id="reveal-03">
    <circle cx="154" cy="510" r="54" fill="#72886f" filter="url(#badgeGlow)"/>
    <text x="117" y="529" width="78" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#ffffff">03</text>
    <text x="242" y="490" width="300" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2f3b33">Skills</text>
    <text x="244" y="528" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#101813">
      <tspan x="244" dy="0">Highlight the capabilities</tspan><tspan x="244" dy="24">that unlock the next step</tspan>
    </text>
  </g>

  <g id="reveal-04">
    <circle cx="704" cy="510" r="54" fill="#72886f" filter="url(#badgeGlow)"/>
    <text x="667" y="529" width="78" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="43" font-weight="700" fill="#ffffff">04</text>
    <text x="790" y="490" width="360" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2f3b33">Interests / Hobbies</text>
    <text x="792" y="528" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#101813">
      <tspan x="792" dy="0">Close with a human detail</tspan><tspan x="792" dy="24">or optional exploration path</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` / `<animateTransform>` for the reveal; create sequential slides instead.
- ❌ `<mask>` or clipping non-image shapes for botanical blobs; use editable `<path>` shapes directly.
- ❌ `<use>` or `<symbol>` for repeated dots/badges; duplicate native circles so PowerPoint keeps them editable.
- ❌ Dense grid lines or boxes around every item; the organic layout works because the grid is implied by spacing.
- ❌ Applying filters to `<line>` botanical accents; filters on lines are dropped by the translator.

## Composition notes
- Keep the title anchored in the upper-left, occupying roughly the first 45% of the slide width; leave the upper-right for organic blobs and dot texture.
- Use a generous 2×2 grid: badge at left, title/description at right, with at least 90 px between columns and 140 px between rows.
- For the reveal sequence, generate 5 slide states: background/title only, then add `reveal-01`, then `reveal-02`, `reveal-03`, and `reveal-04`.
- Maintain a muted sage palette with high-contrast dark forest text; reserve white only for badge numerals so the numbering becomes the visual pacing cue.