# SVG Recipe — Corporate Geometric Divider

## Visual mechanism
A deep corporate color field is split asymmetrically: the left half stays clean for bold section typography, while the right half gains depth from intersecting edge-bleeding triangles. Horizontal hatch strokes are manually drawn inside triangular zones to create an architectural, premium consulting texture without using non-translatable SVG patterns.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark corporate background
- 1× `<rect>` for the vertical white typography anchor
- 7× `<path>` for large overlapping geometric triangles and small accent triangles
- 40+× `<line>` for manually constructed horizontal hatch texture inside triangular areas
- 3× `<text>` for section label, main title, and footer/subtitle, each with explicit `width`
- 2× `<linearGradient>` for subtle background depth and premium accent fills
- 1× `<filter id="softShadow">` applied to select triangle paths for gentle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyDepth" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#203F55"/>
      <stop offset="0.55" stop-color="#24445A"/>
      <stop offset="1" stop-color="#142D41"/>
    </linearGradient>
    <linearGradient id="crimsonAccent" x1="760" y1="160" x2="1190" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F06A7E"/>
      <stop offset="1" stop-color="#C93D53"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-8" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#navyDepth)"/>

  <!-- right-side architectural geometry -->
  <path d="M680 720 L1280 140 L1280 720 Z" fill="#10283B" opacity="0.46" filter="url(#softShadow)"/>
  <path d="M875 720 L1245 370 L1280 720 Z" fill="#FFFFFF" opacity="0.055"/>
  <path d="M470 720 L820 720 L645 560 Z" fill="#10283B" opacity="0.64"/>
  <path d="M890 0 L1280 0 L1280 405 Z" fill="#19364B" opacity="0.48"/>
  <path d="M1004 418 L1130 295 L1130 552 Z" fill="url(#crimsonAccent)" opacity="0.95" filter="url(#softShadow)"/>
  <path d="M875 244 L920 202 L920 292 Z" fill="#E14A5F"/>
  <path d="M1098 628 L1152 578 L1186 666 Z" fill="#FFFFFF" opacity="0.28"/>

  <!-- manually calculated hatch lines for bottom-right triangle -->
  <line x1="696" y1="704" x2="1280" y2="704" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="713" y1="688" x2="1280" y2="688" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="729" y1="672" x2="1280" y2="672" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="746" y1="656" x2="1280" y2="656" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="762" y1="640" x2="1280" y2="640" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="779" y1="624" x2="1280" y2="624" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="796" y1="608" x2="1280" y2="608" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="812" y1="592" x2="1280" y2="592" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="829" y1="576" x2="1280" y2="576" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="845" y1="560" x2="1280" y2="560" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="862" y1="544" x2="1280" y2="544" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="878" y1="528" x2="1280" y2="528" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="895" y1="512" x2="1280" y2="512" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="911" y1="496" x2="1280" y2="496" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="928" y1="480" x2="1280" y2="480" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="944" y1="464" x2="1280" y2="464" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="961" y1="448" x2="1280" y2="448" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="978" y1="432" x2="1280" y2="432" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="994" y1="416" x2="1280" y2="416" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>
  <line x1="1011" y1="400" x2="1280" y2="400" stroke="#FFFFFF" stroke-width="2" opacity="0.13"/>

  <!-- manually calculated hatch lines for top-right triangle -->
  <line x1="909" y1="20" x2="1280" y2="20" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="925" y1="36" x2="1280" y2="36" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="940" y1="52" x2="1280" y2="52" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="956" y1="68" x2="1280" y2="68" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="971" y1="84" x2="1280" y2="84" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="986" y1="100" x2="1280" y2="100" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1002" y1="116" x2="1280" y2="116" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1017" y1="132" x2="1280" y2="132" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1032" y1="148" x2="1280" y2="148" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1048" y1="164" x2="1280" y2="164" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1063" y1="180" x2="1280" y2="180" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1078" y1="196" x2="1280" y2="196" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1094" y1="212" x2="1280" y2="212" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1109" y1="228" x2="1280" y2="228" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1125" y1="244" x2="1280" y2="244" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <line x1="1140" y1="260" x2="1280" y2="260" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>

  <!-- small floating accents -->
  <path d="M1160 130 L1188 105 L1217 143 Z" fill="#FFFFFF" opacity="0.22"/>
  <path d="M770 352 L796 328 L820 365 Z" fill="#FFFFFF" opacity="0.16"/>
  <line x1="742" y1="300" x2="822" y2="300" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="8 8" opacity="0.20"/>
  <line x1="1036" y1="236" x2="1132" y2="236" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="8 8" opacity="0.18"/>

  <!-- left typography block -->
  <rect x="116" y="224" width="8" height="238" rx="4" fill="#FFFFFF"/>
  <text x="150" y="218" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" letter-spacing="3" fill="#FFFFFF" opacity="0.78">
    SECTION 03
  </text>
  <text x="148" y="306" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="700" fill="#FFFFFF">
    <tspan x="148" dy="0">Our Proposed</tspan>
    <tspan x="148" dy="70">Approach</tspan>
    <tspan x="148" dy="70" fill="#F06A7E">&amp; Fees</tspan>
  </text>
  <text x="150" y="522" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="400" fill="#FFFFFF" opacity="0.76">
    www.YourCompany.com
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for hatching; they translate poorly, so draw hatch strokes manually as editable `<line>` elements.
- ❌ `clip-path` on lines or paths to crop stripes into triangles; clipping is only reliable on `<image>` elements.
- ❌ Mask-based triangle reveals; masks on shapes can hard-fail or be ignored.
- ❌ Centered decorative geometry; the premium divider effect depends on shapes bleeding from the right and bottom edges.
- ❌ Low-contrast text over the patterned area; reserve the left half as a calm typography zone.

## Composition notes
- Keep the left 45–50% of the slide mostly empty except for the anchor bar and text block.
- Let the largest triangles bleed off the right and bottom edges so the layout feels intentional rather than decorative.
- Use white hatch lines at very low opacity; the texture should be visible but never compete with the title.
- Add one vivid accent color triangle to create brand energy and prevent the navy field from feeling flat.