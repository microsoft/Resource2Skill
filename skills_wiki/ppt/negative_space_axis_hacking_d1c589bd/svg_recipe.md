# SVG Recipe — Negative Space Axis Hacking

## Visual mechanism
A positive-only column chart is visually “lifted” above the bottom of the plot, leaving an intentional negative-space band below the 0% baseline. That reserved band becomes a precise alignment zone for floating category icons, while a data table sits beneath as the real category/value label system.

## SVG primitives needed
- 1× `<image>` for the full-bleed fitness/photo background
- 2× `<rect>` overlays for dark purple tint and subtle bottom chart-panel depth
- 1× `<linearGradient>` for the atmospheric violet/blue wash
- 1× `<filter id="softShadow">` applied to chart bars, axis pill, and data table
- 1× `<filter id="glow">` applied to the title accent and icons
- 1× rounded `<rect>` for the vertical value-axis pill
- 1× `<line>` for the 0% baseline
- 14× triangular `<path>` bars for clustered male/female series
- 7× icon groups built from `<path>`, `<circle>`, and `<line>` primitives, positioned in the negative-space band
- 1× masking `<rect>` matching the background tint to imply hiding unwanted negative-axis labels
- Multiple `<line>` elements for the data-table grid
- Multiple `<text width="...">` elements for title, percentage ticks, category labels, legend, and values
- 1× annotation arrow made from a `<line>` plus a small `<path>` arrowhead

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="purpleWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8F88FF" stop-opacity="0.78"/>
      <stop offset="0.55" stop-color="#4B4DFF" stop-opacity="0.82"/>
      <stop offset="1" stop-color="#3E44F5" stop-opacity="0.94"/>
    </linearGradient>
    <linearGradient id="pinkBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FF496C"/>
      <stop offset="1" stop-color="#CF315F"/>
    </linearGradient>
    <linearGradient id="blackBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#07091D"/>
      <stop offset="1" stop-color="#000013"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <image href="https://images.example.com/fitness-stretching-workout-background-no-face.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#purpleWash)"/>
  <rect x="0" y="350" width="1280" height="370" fill="#3B40F6" opacity="0.34"/>

  <text x="20" y="82" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="800" fill="white" letter-spacing="2">PPT</text>
  <text x="215" y="44" width="380" font-family="Microsoft YaHei, Segoe UI" font-size="32" font-weight="800" fill="white">柱狀圖</text>
  <text x="215" y="86" width="520" font-family="Microsoft YaHei, Segoe UI" font-size="32" font-weight="800" fill="white">座標軸選項（範圍最大值最小值）</text>
  <text x="18" y="126" width="210" font-family="Microsoft YaHei, Segoe UI" font-size="30" font-weight="800" fill="white" letter-spacing="8">資訊圖表</text>
  <line x1="318" y1="94" x2="150" y2="197" stroke="white" stroke-width="1.5"/>
  <path d="M145 200 L153 190 L156 197 Z" fill="white"/>

  <rect x="83" y="141" width="57" height="376" rx="26" fill="#393FEF" opacity="0.72" filter="url(#softShadow)"/>
  <text x="94" y="172" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">70%</text>
  <text x="94" y="218" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">60%</text>
  <text x="94" y="264" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">50%</text>
  <text x="94" y="310" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">40%</text>
  <text x="94" y="356" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">30%</text>
  <text x="94" y="402" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">20%</text>
  <text x="94" y="449" width="44" font-family="Segoe UI" font-size="16" fill="#E8E8FF">10%</text>
  <text x="103" y="499" width="36" font-family="Segoe UI" font-size="16" fill="#FFFFFF">0%</text>

  <line x1="145" y1="493" x2="1227" y2="493" stroke="#E8E8FF" stroke-width="1.2"/>
  <rect x="68" y="504" width="90" height="77" fill="#474BF7" opacity="0.95"/>

  <g filter="url(#softShadow)">
    <path d="M167 493 L199 282 L232 493 Z" fill="url(#blackBar)"/>
    <path d="M216 493 L248 239 L281 493 Z" fill="url(#pinkBar)"/>
    <path d="M321 493 L354 204 L386 493 Z" fill="url(#blackBar)"/>
    <path d="M370 493 L402 318 L435 493 Z" fill="url(#pinkBar)"/>
    <path d="M477 493 L509 322 L542 493 Z" fill="url(#blackBar)"/>
    <path d="M526 493 L558 198 L591 493 Z" fill="url(#pinkBar)"/>
    <path d="M632 493 L664 361 L697 493 Z" fill="url(#blackBar)"/>
    <path d="M681 493 L713 160 L746 493 Z" fill="url(#pinkBar)"/>
    <path d="M785 493 L818 187 L850 493 Z" fill="url(#blackBar)"/>
    <path d="M835 493 L867 337 L899 493 Z" fill="url(#pinkBar)"/>
    <path d="M941 493 L974 128 L1006 493 Z" fill="url(#blackBar)"/>
    <path d="M991 493 L1023 391 L1055 493 Z" fill="url(#pinkBar)"/>
    <path d="M1093 493 L1126 335 L1158 493 Z" fill="url(#blackBar)"/>
    <path d="M1143 493 L1175 191 L1208 493 Z" fill="url(#pinkBar)"/>
  </g>

  <g stroke="white" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none" filter="url(#glow)">
    <g transform="translate(213 542) rotate(-8)"><circle cx="22" cy="-20" r="8" fill="white" stroke="none"/><path d="M17 -5 L-20 0 M17 -5 L-5 30 M17 -5 L39 17 M-5 30 L-27 42 M39 17 L27 35"/></g>
    <g transform="translate(369 548)"><circle cx="0" cy="21" r="15"/><circle cx="52" cy="21" r="15"/><path d="M0 21 L22 -8 L47 21 M22 -8 L22 -31 M-29 -28 L-7 -34 L-12 -21"/><path d="M-29 -28 L-26 -20"/></g>
    <g transform="translate(525 542)"><circle cx="-1" cy="-30" r="7" fill="white" stroke="none"/><path d="M0 -21 C-17 -7 -10 8 4 20 M4 20 L4 39 M4 20 L33 2 M-4 -25 L-10 -45 M-4 -25 L7 -45"/></g>
    <g transform="translate(682 543)"><circle cx="5" cy="-28" r="8" fill="white" stroke="none"/><path d="M5 -15 L-24 -23 M5 -15 L29 -38 L43 -22 L26 -8 M5 -15 L-19 25 M-19 25 L12 24"/></g>
    <g transform="translate(833 542)"><circle cx="0" cy="-39" r="9"/><circle cx="0" cy="-39" r="2" fill="white" stroke="none"/><path d="M0 -29 L0 16 M0 -4 L20 10 M0 16 L-14 37 M0 16 L16 35"/></g>
    <g transform="translate(982 534)"><circle cx="-2" cy="-43" r="6" fill="white" stroke="none"/><circle cx="23" cy="-55" r="5" fill="white" stroke="none"/><path d="M-9 -32 L-8 -15 L13 -7 L34 -22 M-8 -15 L-23 -1 M13 -7 L7 21 M7 21 L-17 24"/></g>
    <g transform="translate(1148 546)"><circle cx="7" cy="-11" r="8" fill="white" stroke="none"/><path d="M0 0 L-15 31 M0 0 L24 4 M-15 31 L-45 33 M24 4 L33 31 M-45 33 L-4 33"/></g>
  </g>

  <rect x="146" y="586" width="1081" height="101" fill="#5659FF" opacity="0.22" stroke="#B9BAFF" stroke-opacity="0.35" filter="url(#softShadow)"/>
  <line x1="146" y1="619" x2="1227" y2="619" stroke="#C8C8FF" stroke-opacity="0.45"/>
  <line x1="146" y1="653" x2="1227" y2="653" stroke="#C8C8FF" stroke-opacity="0.35"/>
  <line x1="88" y1="619" x2="146" y2="619" stroke="#C8C8FF" stroke-opacity="0.35"/>
  <line x1="88" y1="653" x2="146" y2="653" stroke="#C8C8FF" stroke-opacity="0.35"/>
  <line x1="88" y1="687" x2="1227" y2="687" stroke="#C8C8FF" stroke-opacity="0.35"/>
  <rect x="88" y="619" width="58" height="68" fill="#5659FF" opacity="0.16" stroke="#C8C8FF" stroke-opacity="0.35"/>
  <line x1="146" y1="586" x2="146" y2="687" stroke="#C8C8FF" stroke-opacity="0.35"/>
  <line x1="300" y1="586" x2="300" y2="687" stroke="#C8C8FF" stroke-opacity="0.23"/>
  <line x1="454" y1="586" x2="454" y2="687" stroke="#C8C8FF" stroke-opacity="0.23"/>
  <line x1="608" y1="586" x2="608" y2="687" stroke="#C8C8FF" stroke-opacity="0.23"/>
  <line x1="762" y1="586" x2="762" y2="687" stroke="#C8C8FF" stroke-opacity="0.23"/>
  <line x1="916" y1="586" x2="916" y2="687" stroke="#C8C8FF" stroke-opacity="0.23"/>
  <line x1="1070" y1="586" x2="1070" y2="687" stroke="#C8C8FF" stroke-opacity="0.23"/>

  <text x="207" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">跑步</text>
  <text x="361" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">單車</text>
  <text x="515" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">跳舞</text>
  <text x="669" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">瑜珈</text>
  <text x="823" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">重訓</text>
  <text x="978" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">球類</text>
  <text x="1132" y="608" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">伸展</text>
  <text x="94" y="640" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">▲ 男%</text>
  <text x="94" y="675" width="50" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#E7E7FF">▲ 女%</text>
  <text x="205" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">45%</text><text x="359" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">62%</text><text x="513" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">37%</text><text x="667" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">28%</text><text x="821" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">66%</text><text x="975" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">78%</text><text x="1130" y="641" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">34%</text>
  <text x="205" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">55%</text><text x="359" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">38%</text><text x="513" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">63%</text><text x="667" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">72%</text><text x="821" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">34%</text><text x="975" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">22%</text><text x="1130" y="675" width="55" font-family="Segoe UI" font-size="16" fill="#E7E7FF">66%</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to hide the negative tick labels; use a background-colored `<rect>` camouflage block instead.
- ❌ Do not rely on real chart axes generated from SVG; build the visual as editable bars, axis labels, icons, and table shapes.
- ❌ Do not put `marker-end` on a `<path>` for the annotation arrow; use a `<line>` plus a separate triangular `<path>` arrowhead.
- ❌ Do not clip the icons or bars with `clip-path`; keep the negative-space band clean and fully editable.

## Composition notes
- Reserve the lower 25–30% of the chart area as the “hacked” negative-space band: icons float there, table sits directly below.
- Keep the 0% baseline visually crisp; it is the hinge between quantitative bars above and qualitative icon labels below.
- Use a strong two-color rhythm for clustered series, such as neon pink versus near-black violet, so the bars remain readable over a photographic background.
- The masking rectangle should match the background/tint exactly and sit over the fake negative tick area, making the axis hack feel intentional rather than broken.