# SVG Recipe — Off-Canvas Geometric Masking

## Visual mechanism
Oversized rectangles are rotated and pushed beyond the slide boundaries so the canvas edge naturally “clips” them into sharp diagonal wedges. The result is a crisp, modern cover/closing slide built from simple editable geometry rather than hand-drawn polygons.

## SVG primitives needed
- 1× `<rect>` for the full black letterbox background.
- 1× `<rect>` for the central orange presentation field.
- 6× oversized rotated `<rect>` elements for off-canvas diagonal geometric masks and layered color facets.
- 2× `<linearGradient>` fills for premium depth on the orange field and angled slabs.
- 1× `<filter id="softShadow">` applied to the small label badge and logo card.
- 4× small `<rect>` elements for the editable PowerPoint-style icon and closing badge.
- 3× `<path>` elements for simple editable icon linework.
- 1× `<line>` for the subtitle underline.
- 5× `<text>` elements with explicit `width` for title, subtitle, badge, logo letter, and footer metadata.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="orangeField" x1="0" y1="60" x2="1280" y2="660" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D85B35"/>
      <stop offset="0.55" stop-color="#CE512F"/>
      <stop offset="1" stop-color="#B94127"/>
    </linearGradient>

    <linearGradient id="darkFacet" x1="0" y1="720" x2="480" y2="180" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8F2E1E"/>
      <stop offset="1" stop-color="#B94628"/>
    </linearGradient>

    <linearGradient id="lightFacet" x1="0" y1="720" x2="620" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F07A44"/>
      <stop offset="1" stop-color="#D85B35"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Letterbox stage -->
  <rect x="0" y="0" width="1280" height="720" fill="#050505"/>

  <!-- Main color field -->
  <rect x="0" y="64" width="1280" height="592" fill="url(#orangeField)"/>

  <!-- Off-canvas rotated rectangles: the slide boundary clips them into diagonals -->
  <rect x="-220" y="125" width="250" height="900" fill="url(#darkFacet)" opacity="0.72"
        transform="rotate(29 0 720)"/>
  <rect x="30" y="110" width="205" height="900" fill="url(#lightFacet)" opacity="0.55"
        transform="rotate(29 0 720)"/>
  <rect x="235" y="110" width="72" height="900" fill="#FFFFFF" opacity="0.10"
        transform="rotate(29 0 720)"/>

  <rect x="1040" y="-270" width="220" height="780" fill="#A13A25" opacity="0.34"
        transform="rotate(29 1280 64)"/>
  <rect x="1180" y="-280" width="90" height="780" fill="#FFFFFF" opacity="0.09"
        transform="rotate(29 1280 64)"/>
  <rect x="920" y="-330" width="86" height="760" fill="#EA7041" opacity="0.32"
        transform="rotate(29 1280 64)"/>

  <!-- Editable PPT-style icon in the upper-left -->
  <rect x="55" y="104" width="74" height="74" rx="5" fill="none" stroke="#FFFFFF" stroke-width="3"
        opacity="0.82" filter="url(#softShadow)"/>
  <rect x="88" y="96" width="70" height="68" rx="5" fill="none" stroke="#FFFFFF" stroke-width="2"
        opacity="0.58"/>
  <path d="M126 111 C144 111 152 121 152 137 C152 154 140 162 124 158"
        fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.65"/>
  <path d="M128 119 L143 119 L143 151 L128 151 Z"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.58"/>
  <path d="M105 132 L121 132 C133 132 139 139 139 148 C139 158 132 164 120 164 L105 164 Z"
        fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.85"/>
  <text x="73" y="159" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="48"
        fill="#FFFFFF" opacity="0.95">P</text>

  <!-- Small closing badge -->
  <rect x="938" y="145" width="198" height="42" rx="21" fill="#FFFFFF" opacity="0.16"/>
  <rect x="948" y="153" width="178" height="26" rx="13" fill="#FFFFFF" opacity="0.18"/>
  <text x="1037" y="173" width="178" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600"
        letter-spacing="2" fill="#FFFFFF">CLOSING SLIDE</text>

  <!-- Main title block -->
  <text x="640" y="304" width="980" text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI" font-size="48" font-weight="700"
        letter-spacing="3" fill="#FFFFFF">
    用形状制作简洁PPT封面
  </text>

  <text x="640" y="414" width="620" text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI" font-size="44" font-weight="300"
        fill="#FFFFFF" opacity="0.94">
    PPT基础教学
  </text>

  <line x1="473" y1="438" x2="807" y2="438" stroke="#FFFFFF" stroke-width="3" opacity="0.92"/>

  <text x="640" y="528" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="400"
        letter-spacing="1" fill="#FFFFFF" opacity="0.76">
    让矩形越界，让画布完成裁切
  </text>

  <text x="1110" y="618" width="250" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#FFFFFF" opacity="0.68">
    THANK YOU · Q&amp;A
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to crop the angled blocks; let the slide/viewBox boundary clip the oversized rectangles naturally.
- ❌ Do not draw every diagonal as a custom polygon unless the edge must be irregular; rotated rectangles remain easier to edit in PowerPoint.
- ❌ Do not apply `clip-path` to the rectangles; PPT-Master only preserves clipping reliably for `<image>`.
- ❌ Do not use `<use>` to duplicate facets or icons; duplicate the actual editable primitives instead.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the diagonal effect; use `rotate(angle cx cy)`.

## Composition notes
- Keep the most aggressive off-canvas geometry on one corner, usually bottom-left, and balance it with title text in the central or upper-right region.
- Let shapes bleed far outside the 1280×720 canvas; the visible crop should feel intentional, not barely clipped.
- Use two to three related tones for the rotated blocks so the geometry reads as layered depth rather than random decoration.
- Preserve generous negative space around the title; the diagonal edges should frame the message, not compete with it.