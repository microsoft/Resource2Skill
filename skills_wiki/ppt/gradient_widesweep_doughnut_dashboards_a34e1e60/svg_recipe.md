# SVG Recipe — Modern KPI Doughnut Charts

## Visual mechanism
Thick rounded arcs sit on muted circular tracks, using neon gradients and subtle glow to turn percentages into premium “tech dashboard” hero metrics. Large centered numerals and restrained labels keep the KPI readable while the rings carry the emotional impact.

## SVG primitives needed
- 1× `<rect>` for the dark slide background
- 1× `<rect>` overlay with radial/linear gradient for subtle vignette depth
- 3× `<circle>` for full low-contrast doughnut tracks
- 6× `<path>` for glowing duplicate arcs plus crisp foreground KPI arcs
- 6× `<circle>` for glossy rounded cap highlights at arc endpoints
- 3× `<text>` for large percentage values inside the doughnuts
- 6× `<text>` for KPI labels and short explanatory copy
- 3× `<linearGradient>` for blue, violet, and hot orange/pink arc strokes
- 4× `<radialGradient>` for background light falloff and cap highlights
- 2× `<filter>` for soft shadows and colored glow
- Several decorative `<path>` flame shapes for an optional hero/emphasis accent on the highest KPI
- Small `<rect>`, `<circle>`, and `<text>` elements for logo/sidebar executive-keynote styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="28%" r="75%">
      <stop offset="0%" stop-color="#303033"/>
      <stop offset="55%" stop-color="#202022"/>
      <stop offset="100%" stop-color="#151516"/>
    </radialGradient>

    <linearGradient id="blueArc" x1="170" y1="410" x2="430" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00C8FF"/>
      <stop offset="48%" stop-color="#1265FF"/>
      <stop offset="100%" stop-color="#2530FF"/>
    </linearGradient>

    <linearGradient id="violetArc" x1="515" y1="420" x2="785" y2="635" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7A2CFF"/>
      <stop offset="45%" stop-color="#B000FF"/>
      <stop offset="100%" stop-color="#F000FF"/>
    </linearGradient>

    <linearGradient id="fireArc" x1="820" y1="610" x2="1170" y2="300" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF9A27"/>
      <stop offset="38%" stop-color="#FF4A45"/>
      <stop offset="68%" stop-color="#FF0877"/>
      <stop offset="100%" stop-color="#F90073"/>
    </linearGradient>

    <radialGradient id="blueCap" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#20E5FF"/>
      <stop offset="55%" stop-color="#1578FF"/>
      <stop offset="100%" stop-color="#252CFF"/>
    </radialGradient>

    <radialGradient id="violetCap" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#F23BFF"/>
      <stop offset="55%" stop-color="#B900FF"/>
      <stop offset="100%" stop-color="#752AFF"/>
    </radialGradient>

    <radialGradient id="fireCap" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FF4BD0"/>
      <stop offset="50%" stop-color="#FF0877"/>
      <stop offset="100%" stop-color="#E80065"/>
    </radialGradient>

    <radialGradient id="flameCore" cx="50%" cy="55%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="#FFF75A"/>
      <stop offset="72%" stop-color="#FF9B1E"/>
      <stop offset="100%" stop-color="#FF133D"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="neonGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.08"/>

  <rect x="0" y="210" width="57" height="300" fill="#111113" opacity="0.42"/>
  <text x="33" y="400" width="150" transform="rotate(-90 33 400)" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" letter-spacing="1.5" fill="#FFFFFF" text-anchor="middle">DOUGHNUT</text>

  <circle cx="97" cy="98" r="59" fill="#F15A24" opacity="0.95" filter="url(#softShadow)"/>
  <path d="M97 39 A59 59 0 0 1 156 98 L97 98 Z" fill="#FF7B54"/>
  <path d="M97 98 L156 98 A59 59 0 0 1 97 157 Z" fill="#E94B1C"/>
  <rect x="28" y="65" width="68" height="66" rx="4" fill="#E94716" filter="url(#softShadow)"/>
  <text x="62" y="114" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF" text-anchor="middle">P</text>

  <text x="202" y="137" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="112" font-weight="900" letter-spacing="2" fill="#FFFFFF" filter="url(#softShadow)">MODERN KPI</text>
  <text x="202" y="246" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="112" font-weight="900" letter-spacing="2" fill="#FFFFFF" filter="url(#softShadow)">DOUGHNUT</text>
  <text x="202" y="354" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="112" font-weight="900" letter-spacing="2" fill="#FFFFFF" filter="url(#softShadow)">CHARTS</text>

  <text x="1185" y="79" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="900" font-style="italic" fill="#FFFFFF">ONE</text>
  <text x="1187" y="97" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="900" font-style="italic" fill="#FFFFFF">SKILL</text>

  <circle cx="305" cy="535" r="115" fill="none" stroke="#2D2D31" stroke-width="68" opacity="0.78"/>
  <path d="M305 420 A115 115 0 1 0 373 628" fill="none" stroke="url(#blueArc)" stroke-width="68" stroke-linecap="round" opacity="0.58" filter="url(#neonGlow)"/>
  <path d="M305 420 A115 115 0 1 0 373 628" fill="none" stroke="url(#blueArc)" stroke-width="68" stroke-linecap="round"/>
  <circle cx="305" cy="420" r="37" fill="url(#blueCap)" opacity="0.98" filter="url(#neonGlow)"/>
  <circle cx="373" cy="628" r="36" fill="url(#blueCap)" opacity="0.92"/>
  <text x="305" y="552" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF" text-anchor="middle">60%</text>
  <text x="305" y="690" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="2" fill="#FFFFFF" text-anchor="middle">ADOPTION</text>

  <circle cx="640" cy="535" r="115" fill="none" stroke="#2D2D31" stroke-width="68" opacity="0.78"/>
  <path d="M640 420 A115 115 0 1 0 755 535" fill="none" stroke="url(#violetArc)" stroke-width="68" stroke-linecap="round" opacity="0.58" filter="url(#neonGlow)"/>
  <path d="M640 420 A115 115 0 1 0 755 535" fill="none" stroke="url(#violetArc)" stroke-width="68" stroke-linecap="round"/>
  <circle cx="640" cy="420" r="37" fill="url(#violetCap)" opacity="0.98" filter="url(#neonGlow)"/>
  <circle cx="755" cy="535" r="36" fill="url(#violetCap)" opacity="0.94"/>
  <text x="640" y="552" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFFFFF" text-anchor="middle">75%</text>
  <text x="640" y="690" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="2" fill="#FFFFFF" text-anchor="middle">RETENTION</text>

  <circle cx="1010" cy="455" r="165" fill="none" stroke="#2D2D31" stroke-width="78" opacity="0.78"/>
  <path d="M1160 385 A165 165 0 1 0 1090 311" fill="none" stroke="url(#fireArc)" stroke-width="78" stroke-linecap="round" opacity="0.55" filter="url(#neonGlow)"/>
  <path d="M1160 385 A165 165 0 1 0 1090 311" fill="none" stroke="url(#fireArc)" stroke-width="78" stroke-linecap="round"/>
  <circle cx="1160" cy="385" r="39" fill="url(#fireCap)" opacity="0.96" filter="url(#neonGlow)"/>
  <circle cx="1090" cy="311" r="39" fill="url(#fireCap)" opacity="0.96"/>
  <text x="1010" y="461" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="50" font-weight="800" fill="#FFFFFF" text-anchor="middle">90%</text>
  <text x="1010" y="676" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="2" fill="#FFFFFF" text-anchor="middle">TARGET HIT</text>

  <path d="M1019 336 C982 323 961 296 965 262 C970 219 1005 220 1013 183 C1038 201 1049 224 1045 249 C1061 244 1066 229 1064 213 C1091 238 1089 270 1076 292 C1097 288 1099 267 1098 246 C1133 285 1100 342 1019 336 Z" fill="#FF2D24" filter="url(#neonGlow)"/>
  <path d="M1020 329 C995 319 982 300 986 275 C990 246 1014 247 1019 221 C1037 239 1039 259 1030 276 C1044 274 1051 260 1050 248 C1070 270 1064 303 1020 329 Z" fill="#FF9A1E"/>
  <path d="M1019 330 C1002 319 999 300 1007 283 C1014 269 1025 258 1025 239 C1046 264 1052 296 1019 330 Z" fill="url(#flameCore)"/>
</svg>
```

## Avoid in this skill
- ❌ Don’t build the doughnut as filled pie-slice wedges; the modern look depends on thick stroked arcs with rounded caps.
- ❌ Don’t use `<animate>` or animated stroke-dashoffset to “draw” the chart; PPT-Master will not translate SVG animation.
- ❌ Don’t use `<mask>` to cut holes in circles; use `fill="none"` stroked circles/paths instead.
- ❌ Don’t put glow filters on `<line>` elements; use stroked `<path>` arcs for filtered glow.
- ❌ Don’t rely on `<pattern>` fills or `<textPath>` for labels; keep labels as normal editable `<text>` with explicit `width`.

## Composition notes
- Keep the highest-value KPI larger or farther right to create a hero hierarchy; smaller rings can sit below the title as supporting metrics.
- Use a dark charcoal background and low-contrast tracks so the gradient arcs appear luminous without clutter.
- Place percentage text exactly in the doughnut center; labels should sit below with generous negative space.
- Repeat stroke thickness, cap style, and typography across all rings; vary only gradient color and scale for visual rhythm.