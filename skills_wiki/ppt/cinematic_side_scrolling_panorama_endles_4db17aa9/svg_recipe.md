# SVG Recipe — Cinematic Side-Scrolling Panorama (Endless Runner Aesthetic)

## Visual mechanism
A horizontal parallax world is built from stacked cinematic bands: deep gradient sky, distant city, soft hills, reflective water, and a high-contrast road. A stylized runner anchored on the lower-right focal point turns the landscape into a paused frame from a side-scrolling animation.

## SVG primitives needed
- 1× `<rect>` for the full-slide sky gradient background
- 1× `<circle>` for a soft moon / atmospheric focal accent
- 20–40× `<circle>` for stars, some with glow
- 3–5× `<ellipse>` with blur filter for distant cloud masses
- 12–20× `<rect>` for skyline buildings
- 30–60× small `<rect>` for warm lit windows
- 3× large `<ellipse>` for layered green hills
- 1× `<rect>` for the water band using a vertical gradient
- 8–14× `<line>` for subtle horizontal water ripples
- 1× `<rect>` for the foreground road
- 6–10× `<line>` for road borders and lane dashes
- 10–14× `<path>` / `<circle>` for the runner’s body, limbs, shoe shapes, scarf, and motion streaks
- 2× `<text>` with explicit `width` for cinematic title and subtitle
- 3× `<linearGradient>` for sky, water, and road surfaces
- 1× `<radialGradient>` for moon/star glow
- 2× `<filter>` using `feGaussianBlur` and `feOffset+feGaussianBlur+feMerge` for clouds, subject shadow, and readable text glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="460">
      <stop offset="0%" stop-color="#07152f"/>
      <stop offset="48%" stop-color="#102f59"/>
      <stop offset="100%" stop-color="#2c75a5"/>
    </linearGradient>
    <linearGradient id="waterGrad" x1="0" y1="462" x2="0" y2="566">
      <stop offset="0%" stop-color="#123d73"/>
      <stop offset="100%" stop-color="#071d3f"/>
    </linearGradient>
    <linearGradient id="roadGrad" x1="0" y1="568" x2="0" y2="720">
      <stop offset="0%" stop-color="#34363d"/>
      <stop offset="100%" stop-color="#1f2025"/>
    </linearGradient>
    <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="45%" stop-color="#ccecff" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#ccecff" stop-opacity="0"/>
    </radialGradient>
    <filter id="cloudBlur" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textGlow" x="-10%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#skyGrad)"/>
  <circle cx="1060" cy="118" r="74" fill="url(#moonGlow)"/>
  <circle cx="1040" cy="112" r="24" fill="#eefaff" opacity="0.9"/>

  <circle cx="90" cy="62" r="1.7" fill="#ffffff" opacity="0.85"/>
  <circle cx="182" cy="144" r="1.2" fill="#ffffff" opacity="0.55"/>
  <circle cx="258" cy="82" r="1.5" fill="#ffffff" opacity="0.75"/>
  <circle cx="356" cy="42" r="1.1" fill="#ffffff" opacity="0.6"/>
  <circle cx="476" cy="122" r="1.8" fill="#ffffff" opacity="0.8"/>
  <circle cx="612" cy="72" r="1.3" fill="#ffffff" opacity="0.62"/>
  <circle cx="744" cy="158" r="1.5" fill="#ffffff" opacity="0.7"/>
  <circle cx="892" cy="48" r="1.2" fill="#ffffff" opacity="0.55"/>
  <circle cx="1188" cy="84" r="1.6" fill="#ffffff" opacity="0.75"/>
  <circle cx="1230" cy="182" r="1.1" fill="#ffffff" opacity="0.6"/>

  <ellipse cx="730" cy="118" rx="170" ry="34" fill="#ffffff" opacity="0.22" filter="url(#cloudBlur)"/>
  <ellipse cx="1030" cy="196" rx="220" ry="42" fill="#ffffff" opacity="0.18" filter="url(#cloudBlur)"/>
  <ellipse cx="380" cy="210" rx="145" ry="30" fill="#ffffff" opacity="0.16" filter="url(#cloudBlur)"/>

  <rect x="0" y="356" width="1280" height="110" fill="#1b3b5f" opacity="0.35"/>
  <rect x="42" y="286" width="48" height="180" fill="#667889" opacity="0.82"/>
  <rect x="116" y="322" width="68" height="144" fill="#7a8790" opacity="0.76"/>
  <rect x="214" y="260" width="54" height="206" fill="#596b7d" opacity="0.82"/>
  <rect x="308" y="335" width="92" height="131" fill="#7d8990" opacity="0.68"/>
  <rect x="438" y="288" width="62" height="178" fill="#637587" opacity="0.78"/>
  <rect x="535" y="318" width="78" height="148" fill="#72818d" opacity="0.72"/>
  <rect x="670" y="274" width="58" height="192" fill="#5e7182" opacity="0.78"/>
  <rect x="770" y="330" width="104" height="136" fill="#78858f" opacity="0.66"/>
  <rect x="922" y="296" width="72" height="170" fill="#637586" opacity="0.76"/>
  <rect x="1035" y="340" width="86" height="126" fill="#7b8790" opacity="0.65"/>
  <rect x="1162" y="282" width="58" height="184" fill="#607384" opacity="0.76"/>

  <rect x="54" y="314" width="7" height="12" fill="#ffe89a" opacity="0.85"/>
  <rect x="74" y="354" width="7" height="12" fill="#ffe89a" opacity="0.65"/>
  <rect x="132" y="346" width="8" height="12" fill="#ffe89a" opacity="0.75"/>
  <rect x="238" y="294" width="7" height="12" fill="#ffe89a" opacity="0.72"/>
  <rect x="352" y="366" width="8" height="12" fill="#ffe89a" opacity="0.65"/>
  <rect x="462" y="324" width="7" height="12" fill="#ffe89a" opacity="0.8"/>
  <rect x="558" y="352" width="8" height="12" fill="#ffe89a" opacity="0.74"/>
  <rect x="690" y="310" width="7" height="12" fill="#ffe89a" opacity="0.78"/>
  <rect x="806" y="358" width="8" height="12" fill="#ffe89a" opacity="0.64"/>
  <rect x="954" y="332" width="7" height="12" fill="#ffe89a" opacity="0.76"/>
  <rect x="1068" y="374" width="8" height="12" fill="#ffe89a" opacity="0.65"/>
  <rect x="1184" y="318" width="7" height="12" fill="#ffe89a" opacity="0.78"/>

  <ellipse cx="185" cy="492" rx="420" ry="145" fill="#15502f"/>
  <ellipse cx="620" cy="482" rx="520" ry="155" fill="#236f3d"/>
  <ellipse cx="1110" cy="498" rx="470" ry="138" fill="#2e8b57"/>

  <rect x="0" y="462" width="1280" height="106" fill="url(#waterGrad)"/>
  <line x1="58" y1="486" x2="194" y2="486" stroke="#ffffff" stroke-width="2" opacity="0.2"/>
  <line x1="260" y1="512" x2="410" y2="512" stroke="#ffffff" stroke-width="2" opacity="0.18"/>
  <line x1="512" y1="482" x2="642" y2="482" stroke="#ffffff" stroke-width="2" opacity="0.18"/>
  <line x1="730" y1="534" x2="906" y2="534" stroke="#ffffff" stroke-width="2" opacity="0.16"/>
  <line x1="982" y1="504" x2="1160" y2="504" stroke="#ffffff" stroke-width="2" opacity="0.18"/>
  <line x1="110" y1="548" x2="302" y2="548" stroke="#ffffff" stroke-width="2" opacity="0.12"/>

  <rect x="0" y="568" width="1280" height="152" fill="url(#roadGrad)"/>
  <line x1="0" y1="574" x2="1280" y2="574" stroke="#ffffff" stroke-width="5" opacity="0.9"/>
  <line x1="0" y1="684" x2="1280" y2="684" stroke="#ffffff" stroke-width="3" opacity="0.35"/>
  <line x1="72" y1="632" x2="190" y2="632" stroke="#ffffff" stroke-width="6" opacity="0.88"/>
  <line x1="310" y1="632" x2="428" y2="632" stroke="#ffffff" stroke-width="6" opacity="0.88"/>
  <line x1="548" y1="632" x2="666" y2="632" stroke="#ffffff" stroke-width="6" opacity="0.88"/>
  <line x1="786" y1="632" x2="904" y2="632" stroke="#ffffff" stroke-width="6" opacity="0.88"/>
  <line x1="1024" y1="632" x2="1142" y2="632" stroke="#ffffff" stroke-width="6" opacity="0.88"/>

  <path d="M889 606 C838 594, 796 595, 750 608" fill="none" stroke="#79d8ff" stroke-width="5" opacity="0.28"/>
  <path d="M900 632 C842 626, 806 630, 764 646" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.18"/>
  <ellipse cx="981" cy="679" rx="96" ry="15" fill="#000000" opacity="0.34" filter="url(#softShadow)"/>

  <path d="M987 514 C1010 526, 1025 545, 1022 570 C1002 574, 981 562, 966 543 Z" fill="#ffcf43"/>
  <circle cx="982" cy="489" r="22" fill="#ffd45c"/>
  <path d="M963 486 C978 467, 1000 464, 1014 479 C1000 477, 988 482, 980 497 Z" fill="#12243d"/>
  <path d="M970 536 C946 552, 926 558, 903 553" fill="none" stroke="#f6f7fb" stroke-width="13" stroke-linecap="round"/>
  <path d="M1015 548 C1044 551, 1065 542, 1088 522" fill="none" stroke="#f6f7fb" stroke-width="13" stroke-linecap="round"/>
  <path d="M1008 570 C992 599, 974 622, 942 646" fill="none" stroke="#111827" stroke-width="15" stroke-linecap="round"/>
  <path d="M1020 568 C1044 594, 1064 620, 1100 633" fill="none" stroke="#111827" stroke-width="15" stroke-linecap="round"/>
  <path d="M930 652 C948 642, 964 643, 978 653 C960 663, 940 665, 922 660 Z" fill="#ffffff"/>
  <path d="M1094 637 C1112 630, 1129 634, 1142 646 C1123 654, 1104 652, 1088 646 Z" fill="#ffffff"/>
  <path d="M1010 518 C1048 506, 1074 492, 1102 466 C1092 500, 1070 523, 1033 535 Z" fill="#ff4d63" opacity="0.96"/>

  <text x="88" y="136" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#ffffff" filter="url(#textGlow)">一個人的奔跑，始終找不到終點</text>
  <text x="92" y="184" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#d8efff" opacity="0.86">A cinematic progress metaphor: layered scenery, forward momentum, and one clear focal character.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` to create the side-scroll; PowerPoint translation will hard-fail. Represent motion with layered streaks, repeated road dashes, and parallax bands instead.
- ❌ Do not apply `filter` to `<line>` elements for glowing road stripes or ripples; use opacity and stroke width, or convert the glow element to a `<path>`.
- ❌ Do not use `marker-end` for motion arrows; if you need arrows, draw arrowheads manually as paths.
- ❌ Do not clip or mask non-image scenery layers. For this style, use direct vector paths, ellipses, and rectangles rather than masks.
- ❌ Avoid over-randomized star or window placement if the slide needs to look executive; keep the randomness visually balanced and sparse.

## Composition notes
- Keep the top 55–60% as cinematic negative space for title copy; the scene should feel expansive, not crowded.
- Place the runner near the lower-right third so the viewer reads the empty road and landscape as “distance already traveled.”
- Use horizontal bands with different contrast levels: dim sky, muted skyline, saturated hills, dark water, crisp road.
- Add 2–3 motion streaks behind the runner, but keep them subtle so they imply speed without becoming comic-book effects.