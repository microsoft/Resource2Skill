# SVG Recipe — Depth-Layered Interlocking Title

## Visual mechanism
Create cinematic depth by placing massive typography between a full-bleed background image and an isolated foreground subject. The foreground object partially covers the title, using occlusion to make the words feel embedded inside the scene instead of floating on top.

## SVG primitives needed
- 1× `<image>` for the full-slide environmental background photo
- 1× `<image>` for the isolated transparent foreground subject, such as a tower, person, product, or monument
- 3× `<linearGradient>` for cinematic tinting, title contrast, and glass-building facets
- 1× `<radialGradient>` for atmospheric glow behind the title
- 2× `<filter>` with `feOffset`, `feGaussianBlur`, and `feMerge` for editable text shadow and foreground-object shadow
- 2× `<rect>` for full-slide tonal overlays and top/bottom cinematic shading
- 1× `<ellipse>` for soft atmospheric haze
- 3× `<text>` elements for chapter label, oversized interlocking title, and subtitle
- 5× `<path>` elements for editable foreground architecture facets and occluding geometry
- 20+× small `<rect>` elements for editable window highlights on the foreground building
- 1× `<line>` for a subtle editorial divider accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sceneTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111f" stop-opacity="0.58"/>
      <stop offset="45%" stop-color="#0b2340" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#02050a" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="70%" stop-color="#000000" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.62"/>
    </linearGradient>

    <linearGradient id="towerGlass" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#101722"/>
      <stop offset="38%" stop-color="#26374a"/>
      <stop offset="66%" stop-color="#111927"/>
      <stop offset="100%" stop-color="#05080d"/>
    </linearGradient>

    <linearGradient id="towerEdge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#8bd3ff" stop-opacity="0.05"/>
    </linearGradient>

    <radialGradient id="hazeGlow" cx="48%" cy="39%" r="48%">
      <stop offset="0%" stop-color="#b8dfff" stop-opacity="0.42"/>
      <stop offset="52%" stop-color="#5d8bb8" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <filter id="titleShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .48 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="objectShadow" x="-25%" y="-10%" width="150%" height="130%">
      <feOffset dx="-18" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .42 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- LAYER 1: full-bleed environment -->
  <image href="https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#sceneTint)"/>
  <ellipse cx="585" cy="270" rx="520" ry="270" fill="url(#hazeGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomFade)"/>

  <!-- LAYER 2: title sandwiched in the scene -->
  <text x="86" y="92" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4"
        fill="#d7ecff" opacity="0.9">URBAN GROWTH INDEX</text>

  <line x1="86" y1="112" x2="236" y2="112" stroke="#8bd3ff" stroke-width="3" opacity="0.75"/>

  <text x="146" y="382" width="900"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="188" font-weight="900" letter-spacing="-13"
        fill="#ffffff" opacity="0.96" filter="url(#titleShadow)">NYC</text>

  <text x="164" y="452" width="590"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="800" letter-spacing="8"
        fill="#ffffff" opacity="0.88">
    <tspan fill="#8bd3ff">2026</tspan><tspan fill="#ffffff"> PRESENTATION</tspan>
  </text>

  <!-- LAYER 3: foreground isolated subject, intentionally crossing the title -->
  <path d="M878 720 L902 148 L970 56 L1036 136 L1068 720 Z"
        fill="#05070c" opacity="0.58" filter="url(#objectShadow)"/>
  <path d="M914 720 L930 130 L974 56 L1012 720 Z"
        fill="url(#towerGlass)"/>
  <path d="M1012 720 L974 56 L1052 150 L1088 720 Z"
        fill="#0a101a"/>
  <path d="M930 130 L974 56 L1052 150 L1008 174 Z"
        fill="#31465a" opacity="0.9"/>
  <path d="M934 150 L956 112 L962 720 L930 720 Z"
        fill="url(#towerEdge)" opacity="0.42"/>

  <image href="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Empire_State_Building_transparent.png/400px-Empire_State_Building_transparent.png"
         x="780" y="-28" width="410" height="770" preserveAspectRatio="xMidYMid meet" opacity="0.92"/>

  <!-- Editable sparkle/window details on the occluding foreground layer -->
  <rect x="944" y="188" width="9" height="34" fill="#bfe9ff" opacity="0.45"/>
  <rect x="972" y="198" width="8" height="30" fill="#e7f8ff" opacity="0.30"/>
  <rect x="1000" y="214" width="8" height="38" fill="#86c8ef" opacity="0.38"/>
  <rect x="948" y="252" width="8" height="46" fill="#dff7ff" opacity="0.26"/>
  <rect x="978" y="264" width="8" height="40" fill="#7dbbe2" opacity="0.34"/>
  <rect x="1008" y="278" width="8" height="46" fill="#dff7ff" opacity="0.22"/>
  <rect x="950" y="332" width="8" height="54" fill="#bfe9ff" opacity="0.36"/>
  <rect x="981" y="342" width="8" height="52" fill="#ffffff" opacity="0.18"/>
  <rect x="1014" y="358" width="8" height="50" fill="#8bd3ff" opacity="0.32"/>
  <rect x="952" y="430" width="8" height="60" fill="#e7f8ff" opacity="0.30"/>
  <rect x="984" y="438" width="8" height="62" fill="#87cfff" opacity="0.26"/>
  <rect x="1020" y="454" width="8" height="58" fill="#dff7ff" opacity="0.20"/>
  <rect x="954" y="540" width="8" height="70" fill="#bfe9ff" opacity="0.24"/>
  <rect x="988" y="548" width="8" height="74" fill="#ffffff" opacity="0.16"/>
  <rect x="1025" y="564" width="8" height="70" fill="#8bd3ff" opacity="0.26"/>

  <!-- Foreground rim light that reinforces the cutout edge over the title -->
  <path d="M904 720 L918 162 L929 134 L920 720 Z"
        fill="#ffffff" opacity="0.16"/>
  <path d="M1082 720 L1048 154 L1058 166 L1098 720 Z"
        fill="#000000" opacity="0.34"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to hide parts of the title behind the foreground object; instead, stack the foreground subject above the text.
- ❌ Do not apply `clip-path` to the text or vector foreground shapes; clipping is only reliable on `<image>` elements.
- ❌ Do not flatten the title, foreground, and background into one screenshot; the depth effect depends on separately editable layers.
- ❌ Do not use subtle regular-weight typography; this technique needs very large, heavy text that visibly intersects the foreground object.
- ❌ Do not rely on SVG blend modes or CSS `mix-blend-mode`; use explicit opacity, gradients, and shadows instead.

## Composition notes
- Keep the title huge and centered, with at least one letter crossing into the foreground subject’s footprint so the occlusion is obvious.
- Place the foreground object off-center, usually on the right third, so it feels like a vertical architectural wall cutting into the type.
- Use a darker gradient overlay on the background to make white typography readable without destroying the photo.
- Preserve negative space on the left/top for small editorial labels; the main visual focus should be the title/foreground intersection.