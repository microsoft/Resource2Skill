# SVG Recipe — Die-Cut Floating Pillar Infographic

## Visual mechanism
Four tall white die-cut “paper” pillars float over a sharp diagonal black/white background, with custom chevron cuts and interlocking colored hexagon caps. The contrast, shadows, and modular vertical layout turn a simple four-option comparison into a premium executive infographic.

## SVG primitives needed
- 1× `<rect>` for the white slide base.
- 1× `<path>` for the black diagonal background wedge.
- 4× `<ellipse>` for soft contact shadows under the floating pillars.
- 4× `<path>` for the white die-cut pillar bodies with top notch geometry and bottom chevron cutouts.
- 4× `<path>` for colored hexagonal option caps.
- 1× `<linearGradient>` for subtle white-to-light-gray pillar depth.
- 2× `<filter>` definitions: one larger floating shadow for pillars, one tighter shadow for colored caps/contact shadows.
- 17× `<text>` elements for title, option labels, section headings, and body copy; every text element includes an explicit `width` attribute.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pillarFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="72%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f2f2f2"/>
    </linearGradient>

    <filter id="liftShadow" x="-25%" y="-20%" width="150%" height="150%">
      <feOffset in="SourceAlpha" dx="9" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="capShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset in="SourceAlpha" dx="3" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <path d="M0 720 L1280 86 L1280 720 Z" fill="#000000"/>

  <text x="250" y="82" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#000000"
        letter-spacing="1.5">POWERPOINT INFOGRAPHIC</text>

  <ellipse cx="250" cy="620" rx="96" ry="18" fill="#000000" opacity="0.18" filter="url(#capShadow)"/>
  <ellipse cx="500" cy="620" rx="96" ry="18" fill="#000000" opacity="0.18" filter="url(#capShadow)"/>
  <ellipse cx="750" cy="620" rx="96" ry="18" fill="#000000" opacity="0.18" filter="url(#capShadow)"/>
  <ellipse cx="1000" cy="620" rx="96" ry="18" fill="#000000" opacity="0.18" filter="url(#capShadow)"/>

  <g transform="translate(165 168)">
    <path d="M0 42 L47 42 L63 12 L107 12 L123 42 L170 42 L170 405 L85 360 L0 405 Z"
          fill="url(#pillarFill)" filter="url(#liftShadow)"/>
    <path d="M21 0 L149 0 L170 31 L149 62 L21 62 L0 31 Z"
          fill="#0070C0" filter="url(#capShadow)"/>
    <text x="14" y="38" width="142" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#ffffff">OPTION A</text>
    <text x="22" y="122" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#0070C0">MARKET</text>
    <text x="22" y="148" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#0070C0">ENTRY</text>
    <text x="22" y="205" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#595959">
      <tspan x="22" dy="0">Launch a focused</tspan>
      <tspan x="22" dy="22">pilot program in</tspan>
      <tspan x="22" dy="22">one priority region</tspan>
      <tspan x="22" dy="22">before scaling.</tspan>
    </text>
  </g>

  <g transform="translate(415 168)">
    <path d="M0 42 L47 42 L63 12 L107 12 L123 42 L170 42 L170 405 L85 360 L0 405 Z"
          fill="url(#pillarFill)" filter="url(#liftShadow)"/>
    <path d="M21 0 L149 0 L170 31 L149 62 L21 62 L0 31 Z"
          fill="#00B050" filter="url(#capShadow)"/>
    <text x="14" y="38" width="142" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#ffffff">OPTION B</text>
    <text x="22" y="122" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#00B050">PRODUCT</text>
    <text x="22" y="148" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#00B050">DEPTH</text>
    <text x="22" y="205" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#595959">
      <tspan x="22" dy="0">Expand the core</tspan>
      <tspan x="22" dy="22">offer with premium</tspan>
      <tspan x="22" dy="22">features and higher</tspan>
      <tspan x="22" dy="22">retention value.</tspan>
    </text>
  </g>

  <g transform="translate(665 168)">
    <path d="M0 42 L47 42 L63 12 L107 12 L123 42 L170 42 L170 405 L85 360 L0 405 Z"
          fill="url(#pillarFill)" filter="url(#liftShadow)"/>
    <path d="M21 0 L149 0 L170 31 L149 62 L21 62 L0 31 Z"
          fill="#FF0000" filter="url(#capShadow)"/>
    <text x="14" y="38" width="142" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#ffffff">OPTION C</text>
    <text x="22" y="122" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FF0000">CHANNEL</text>
    <text x="22" y="148" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FF0000">SHIFT</text>
    <text x="22" y="205" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#595959">
      <tspan x="22" dy="0">Move investment</tspan>
      <tspan x="22" dy="22">toward digital-led</tspan>
      <tspan x="22" dy="22">acquisition and</tspan>
      <tspan x="22" dy="22">partner enablement.</tspan>
    </text>
  </g>

  <g transform="translate(915 168)">
    <path d="M0 42 L47 42 L63 12 L107 12 L123 42 L170 42 L170 405 L85 360 L0 405 Z"
          fill="url(#pillarFill)" filter="url(#liftShadow)"/>
    <path d="M21 0 L149 0 L170 31 L149 62 L21 62 L0 31 Z"
          fill="#7030A0" filter="url(#capShadow)"/>
    <text x="14" y="38" width="142" text-anchor="middle"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#ffffff">OPTION D</text>
    <text x="22" y="122" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#7030A0">STRATEGIC</text>
    <text x="22" y="148" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#7030A0">ALLIANCE</text>
    <text x="22" y="205" width="126"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#595959">
      <tspan x="22" dy="0">Co-develop a joint</tspan>
      <tspan x="22" dy="22">proposition with</tspan>
      <tspan x="22" dy="22">a complementary</tspan>
      <tspan x="22" dy="22">enterprise partner.</tspan>
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` or boolean-subtract effects to create the die-cuts; draw the pillar as a single custom `<path>` instead.
- ❌ Do not use `<use href="#pillar">` to duplicate pillars; repeat editable path geometry or use translated groups directly.
- ❌ Do not put `clip-path` on the pillar paths; clipping only translates reliably for `<image>` elements.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake perspective; keep the floating effect from shadows, layering, and diagonal background tension.
- ❌ Do not rely on filter effects on `<line>` elements; use filters on the pillar paths, cap paths, or ellipses only.

## Composition notes
- Keep the pillars in the middle 60% of the slide height, with generous top space for a centered executive title.
- Let the diagonal background pass behind the pillars so some white cards sit over white and others over black; this creates the premium floating contrast.
- Use one saturated accent color per pillar and repeat it in the header cap plus main heading for strong option identity.
- Keep body copy short: 3–5 compact lines per pillar, centered vertically below the title area, so the custom geometry remains the visual focus.