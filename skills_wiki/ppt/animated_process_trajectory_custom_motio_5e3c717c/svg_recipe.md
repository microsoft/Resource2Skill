# SVG Recipe — Animated Process Trajectory

## Visual mechanism
A bold keynote-style slide shows a visible motion trajectory as the “stage,” with anchor nodes and a glowing traveler implying movement along a custom path. The static SVG represents animation by combining a dashed route, sequential markers, ghosted traveler positions, and a highlighted active orb.

## SVG primitives needed
- 3× `<linearGradient>` for the pink background wash, PowerPoint logo color, and orange title accent
- 2× `<radialGradient>` for ambient glows and the traveler orb
- 2× `<filter>` for soft drop shadows and cyan/orange glow effects
- 8× `<rect>` for background panels, tilted cards, logo blocks, and rounded motion-path palette
- 12× `<path>` for the PowerPoint logo circle, tilted presentation sheets, dashed trajectory, and mini motion-path examples
- 18× `<circle>` for path nodes, ghost traveler positions, and decorative endpoint dots
- 8× `<line>` for straight motion examples and small connector ticks
- 9× `<text>` with explicit `width` for title, subtitle, and path labels
- 3× `<g>` groups with `translate(...)` / `rotate(...)` transforms for tilted composition and reusable layout zones

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgPink" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f0b2c8"/>
      <stop offset="55%" stop-color="#f7d5df"/>
      <stop offset="100%" stop-color="#e99ab9"/>
    </linearGradient>
    <linearGradient id="pptOrange" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f06b44"/>
      <stop offset="100%" stop-color="#c73219"/>
    </linearGradient>
    <linearGradient id="motionRed" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d8432e"/>
      <stop offset="100%" stop-color="#9f2518"/>
    </linearGradient>
    <radialGradient id="orbGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="28%" stop-color="#00d8ff"/>
      <stop offset="72%" stop-color="#00a7ff" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#00a7ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="ambient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgPink)"/>
  <ellipse cx="835" cy="150" rx="520" ry="210" fill="url(#ambient)" opacity="0.55"/>
  <ellipse cx="165" cy="500" rx="340" ry="160" fill="#d9f7ff" opacity="0.55" filter="url(#glow)"/>

  <g transform="translate(405 66) rotate(-5)">
    <rect x="-20" y="-55" width="850" height="300" fill="#ffffff" opacity="0.98"/>
    <text x="12" y="93" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="92" font-weight="900" fill="#050505" letter-spacing="-3">POWERPOINT</text>
    <text x="26" y="205" width="840" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="86" font-weight="900" fill="#c72f16" letter-spacing="-2">MOTION PATH</text>
  </g>

  <g transform="translate(78 118) rotate(-7)">
    <path d="M96 98 C112 28 190 -12 262 24 C336 62 360 150 310 214 C262 274 160 270 112 214 C88 187 82 139 96 98 Z" fill="url(#pptOrange)" opacity="0.95" filter="url(#shadow)"/>
    <rect x="40" y="72" width="188" height="176" rx="15" fill="#b9331e" opacity="0.38"/>
    <rect x="22" y="62" width="188" height="176" rx="15" fill="#c7361e" filter="url(#shadow)"/>
    <rect x="54" y="96" width="126" height="112" rx="8" fill="#d54828"/>
    <text x="78" y="183" width="105" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="88" font-weight="700" fill="#ffffff">P</text>
  </g>

  <g transform="translate(-42 382) rotate(12)">
    <rect x="0" y="0" width="520" height="248" fill="#ffffff" opacity="0.92" filter="url(#shadow)"/>
    <path d="M95 70 L140 42 L187 72 L141 102 Z" fill="#1399a0"/>
    <text x="126" y="94" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="800" fill="#ffffff">B</text>
    <text x="205" y="88" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" fill="#333333" letter-spacing="7">Bravo</text>
    <text x="72" y="178" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" fill="#111111">Creative Presentation</text>
    <line x1="195" y1="198" x2="308" y2="198" stroke="#199a9d" stroke-width="5"/>
    <text x="205" y="224" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#333333">Presented by Strategy Team</text>
  </g>

  <path d="M875 535 C870 605 905 625 1088 608 C1116 605 1083 686 1134 716" fill="none" stroke="url(#motionRed)" stroke-width="7" stroke-linecap="round" stroke-dasharray="26 16"/>
  <circle cx="875" cy="535" r="8" fill="#d8432e"/>
  <circle cx="1088" cy="608" r="8" fill="#c7361e"/>

  <g transform="translate(485 344) rotate(-6)">
    <rect x="-5" y="-5" width="750" height="180" rx="22" fill="#b7b7b7" opacity="0.45" filter="url(#shadow)"/>
    <rect x="0" y="0" width="740" height="170" rx="22" fill="#f1f1f1" stroke="#c9c9c9" stroke-width="5"/>
    
    <path d="M42 84 C78 126 128 124 162 74" fill="none" stroke="#222222" stroke-width="2.3"/>
    <circle cx="42" cy="84" r="11" fill="#d95057"/>
    <circle cx="162" cy="74" r="11" fill="#58a75b"/>
    <text x="72" y="145" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#111111">Arcs</text>

    <line x1="230" y1="55" x2="230" y2="126" stroke="#222222" stroke-width="2.4"/>
    <circle cx="230" cy="55" r="11" fill="#58a75b"/>
    <circle cx="230" cy="126" r="11" fill="#d95057"/>
    <text x="206" y="145" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#111111">Lines</text>

    <path d="M336 87 C357 52 390 52 410 87 C430 122 463 122 484 87 C463 52 430 52 410 87 C390 122 357 122 336 87 Z" fill="none" stroke="#222222" stroke-width="2.2"/>
    <circle cx="336" cy="87" r="11" fill="#58a75b"/>
    <text x="368" y="145" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#111111">Loops</text>

    <path d="M538 83 C538 45 567 19 603 23 C639 27 660 61 652 96 C644 132 608 150 575 136 C552 126 538 107 538 83 Z" fill="none" stroke="#222222" stroke-width="2.2"/>
    <circle cx="580" cy="25" r="11" fill="#58a75b"/>
    <text x="570" y="145" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#111111">Shapes</text>

    <path d="M675 46 L724 46 C746 46 752 66 752 89 L752 113" fill="none" stroke="#222222" stroke-width="2.2"/>
    <circle cx="675" cy="46" r="11" fill="#58a75b"/>
    <circle cx="752" cy="113" r="11" fill="#d95057"/>
    <text x="696" y="145" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#111111">Turns</text>
  </g>

  <path d="M145 650 C260 555 405 585 512 502 C625 415 708 460 808 409 C918 354 1012 392 1112 328" fill="none" stroke="#00bfff" stroke-width="4" stroke-linecap="round" stroke-dasharray="14 12" opacity="0.65"/>
  <circle cx="145" cy="650" r="11" fill="#00bfff" opacity="0.25"/>
  <circle cx="512" cy="502" r="11" fill="#00bfff" opacity="0.35"/>
  <circle cx="808" cy="409" r="11" fill="#00bfff" opacity="0.50"/>
  <circle cx="1112" cy="328" r="32" fill="url(#orbGlow)" filter="url(#glow)"/>
  <circle cx="1112" cy="328" r="8" fill="#ffffff"/>
  <text x="70" y="58" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600" fill="#7a1730" opacity="0.72">Sequential motion path storyboard</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateMotion>`; PPT-Master will not translate SVG animation, so represent motion with path, ghost positions, and an active traveler.
- ❌ Do not use `marker-end` on the curved trajectory path; arrowheads on paths may disappear. Use endpoint circles or separate `<line>` arrows if needed.
- ❌ Do not apply `filter` to `<line>` elements; place glows on circles, paths, or rectangles instead.
- ❌ Do not use `<textPath>` for labels following the route; keep labels as normal `<text width="...">` near each stage.
- ❌ Do not clip non-image objects; if using photo travelers or avatars, apply `clipPath` only to `<image>`.

## Composition notes
- Keep the upper third for a bold editorial title; the visible motion route should dominate the lower two-thirds.
- Use a tilted floating “motion palette” or stage card to make the trajectory feel like an interactive PowerPoint feature, not a flat diagram.
- The active traveler should be the brightest object on the slide; ghost dots along the path imply the animation’s previous positions.
- Combine warm red/orange title accents with cool cyan trajectory highlights for clear foreground/background separation.