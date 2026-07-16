# SVG Recipe — Vertical Kicker Metric

## Visual mechanism
A narrow vertical kicker column acts like a spine on the left, while an oversized central metric dominates the canvas with generous negative space. Soft gradient blobs, a slim accent rail, and restrained captioning make the slide feel minimal, bold, and keynote-ready.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and translucent metric stage panel
- 3× `<rect>` for the left vertical kicker rail, colored accent tabs, and small baseline block
- 3× `<path>` for organic gradient blobs and subtle decorative swooshes behind the number
- 3× `<circle>` for soft orbital accent dots around the metric
- 1× `<line>` for a fine divider between the vertical kicker and metric field
- 5× `<text>` for the rotated kicker, main metric, unit label, caption, and tiny context label
- 2× `<linearGradient>` for background and accent fills
- 1× `<radialGradient>` for the ambient metric halo
- 2× `<filter>` with blur/shadow applied to paths, rects, and text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#FAFBFF"/>
      <stop offset="0.56" stop-color="#F4F0FF"/>
      <stop offset="1" stop-color="#FFF7EA"/>
    </linearGradient>

    <linearGradient id="railGrad" x1="70" y1="90" x2="70" y2="630">
      <stop offset="0" stop-color="#6C3BFF"/>
      <stop offset="0.48" stop-color="#FF4FA3"/>
      <stop offset="1" stop-color="#FFB84D"/>
    </linearGradient>

    <linearGradient id="metricGrad" x1="350" y1="240" x2="900" y2="500">
      <stop offset="0" stop-color="#17132F"/>
      <stop offset="0.55" stop-color="#4D22D8"/>
      <stop offset="1" stop-color="#FF4FA3"/>
    </linearGradient>

    <radialGradient id="haloGrad" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="0.52" stop-color="#B9A7FF" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#FFB84D" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M770 115 C910 55 1075 95 1137 222 C1198 348 1120 516 950 548 C805 576 675 501 642 379 C610 259 655 164 770 115 Z"
        fill="url(#haloGrad)" filter="url(#glow)" opacity="0.86"/>

  <path d="M271 197 C386 101 555 118 622 226 C696 346 604 479 463 497 C321 515 203 443 195 331 C190 272 220 240 271 197 Z"
        fill="#FFFFFF" opacity="0.78" filter="url(#softShadow)"/>

  <path d="M777 168 C852 124 952 135 1004 198 C1055 260 1034 361 950 398 C866 435 763 401 731 326 C705 265 725 198 777 168 Z"
        fill="#FFE7F2" opacity="0.58"/>

  <rect x="64" y="88" width="78" height="544" rx="39" fill="#FFFFFF" opacity="0.78" filter="url(#softShadow)"/>
  <rect x="84" y="118" width="14" height="484" rx="7" fill="url(#railGrad)"/>
  <rect x="112" y="118" width="10" height="76" rx="5" fill="#17132F" opacity="0.92"/>
  <rect x="112" y="526" width="10" height="76" rx="5" fill="#17132F" opacity="0.18"/>

  <line x1="178" y1="116" x2="178" y2="604" stroke="#17132F" stroke-opacity="0.14" stroke-width="2"/>

  <circle cx="328" cy="190" r="9" fill="#FFB84D"/>
  <circle cx="982" cy="232" r="14" fill="#6C3BFF" opacity="0.22"/>
  <circle cx="1038" cy="474" r="7" fill="#FF4FA3" opacity="0.8"/>

  <path d="M862 492 C936 458 1009 455 1080 487" fill="none" stroke="#6C3BFF" stroke-width="8" stroke-linecap="round" opacity="0.15"/>
  <path d="M326 535 C405 596 544 604 638 543" fill="none" stroke="#FF4FA3" stroke-width="6" stroke-linecap="round" opacity="0.22"/>

  <g transform="translate(108 500) rotate(-90)">
    <text x="0" y="0" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="800" letter-spacing="6" fill="#17132F">
      REVENUE LIFT
    </text>
  </g>

  <text x="265" y="380" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="168" font-weight="900" letter-spacing="-9" fill="url(#metricGrad)" filter="url(#softShadow)">
    42%
  </text>

  <text x="782" y="305" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="800" fill="#17132F" opacity="0.76">
    YoY
  </text>

  <text x="280" y="452" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="600" fill="#17132F" opacity="0.78">
    Net expansion from enterprise accounts
  </text>

  <text x="284" y="506" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" fill="#17132F" opacity="0.58">
    <tspan font-weight="700">Q4 close:</tspan>
    <tspan> strongest conversion quarter since launch</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on CSS `writing-mode` for the vertical kicker; rotate a normal `<text>` group or stack individual letters instead.
- ❌ Do not place the kicker inside `<textPath>` around the rail; text paths are not reliably translated.
- ❌ Do not apply blur or shadow filters to `<line>` dividers; use filters only on rects, paths, circles/ellipses, or text.
- ❌ Do not fill the background with a `<pattern>` texture; use gradients, large paths, or translucent blobs instead.

## Composition notes
- Keep the vertical kicker rail within the left 12–15% of the slide; it should feel like a spine, not a sidebar.
- Place the metric slightly left of center so the percentage has room to breathe and the unit label can sit near the upper-right of the number.
- Use one vivid gradient family for the rail and metric, then keep captions in dark neutral colors with reduced opacity.
- Reserve the right side for ambient blobs and accent dots; the decorative elements should frame the metric without competing with it.