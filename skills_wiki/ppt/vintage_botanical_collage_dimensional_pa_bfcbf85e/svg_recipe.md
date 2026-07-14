# SVG Recipe — Vintage Botanical Collage & Dimensional Papercraft Aesthetic

## Visual mechanism
Build a slide that feels like a layered handmade keepsake card: a muted wallpaper base, metallic concentric frames, a raised cream sentiment plaque, and botanical “die-cut sticker” clusters that overlap the geometry with soft dimensional shadows.

## SVG primitives needed
- 1× `<rect>` for the full-canvas pastel paper background
- 14–20× thin translucent `<line>` elements for hand-built wallpaper striping, avoiding unsupported pattern fills
- 3× `<rect>` for concentric gold-foil frames and the raised central plaque
- 8× `<path>` for ornate corner flourishes and delicate botanical stems
- 18–28× `<ellipse>` / `<circle>` for roses, petals, berries, and soft dot texture
- 8–12× `<path>` for leaf silhouettes and loose papercraft botanical shapes
- 3× `<linearGradient>` for sage paper, cream plaque, and metallic gold stroke/fill effects
- 2× `<filter>` using `feOffset + feGaussianBlur + feMerge` for plaque and sticker shadows
- 3× `<text>` elements with explicit `width` attributes for editable sentiment typography

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sagePaper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#eef3ec"/>
      <stop offset="55%" stop-color="#dfe9df"/>
      <stop offset="100%" stop-color="#f4efe3"/>
    </linearGradient>
    <linearGradient id="creamPaper" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fffdf2"/>
      <stop offset="100%" stop-color="#f4ecd8"/>
    </linearGradient>
    <linearGradient id="foilGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7e8a4"/>
      <stop offset="28%" stop-color="#c99b2e"/>
      <stop offset="58%" stop-color="#fff2b8"/>
      <stop offset="100%" stop-color="#b98722"/>
    </linearGradient>
    <filter id="plaqueShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="8" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.16  0 0 0 0 0.13  0 0 0 0 0.08  0 0 0 0.28 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="stickerShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="7" dy="9" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.18  0 0 0 0 0.12  0 0 0 0 0.09  0 0 0 0.30 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#sagePaper)"/>
  <line x1="80" y1="0" x2="80" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="160" y1="0" x2="160" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <line x1="240" y1="0" x2="240" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="320" y1="0" x2="320" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <line x1="400" y1="0" x2="400" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="480" y1="0" x2="480" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <line x1="560" y1="0" x2="560" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="640" y1="0" x2="640" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <line x1="720" y1="0" x2="720" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="800" y1="0" x2="800" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <line x1="880" y1="0" x2="880" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="960" y1="0" x2="960" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <line x1="1040" y1="0" x2="1040" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.28"/>
  <line x1="1120" y1="0" x2="1120" y2="720" stroke="#ffffff" stroke-width="3" opacity="0.22"/>
  <circle cx="132" cy="118" r="3" fill="#ffffff" opacity="0.30"/>
  <circle cx="1092" cy="608" r="3" fill="#ffffff" opacity="0.25"/>
  <circle cx="1036" cy="126" r="2.5" fill="#ffffff" opacity="0.25"/>
  <circle cx="205" cy="570" r="2.5" fill="#ffffff" opacity="0.30"/>

  <rect x="82" y="70" width="1116" height="580" rx="18" fill="none" stroke="url(#foilGold)" stroke-width="5"/>
  <rect x="108" y="96" width="1064" height="528" rx="14" fill="none" stroke="url(#foilGold)" stroke-width="1.8" opacity="0.95"/>
  <rect x="140" y="128" width="1000" height="464" rx="10" fill="none" stroke="url(#foilGold)" stroke-width="1.2" opacity="0.7"/>

  <path d="M98 90 C130 88,132 128,104 128 C76 128,78 92,111 101" fill="none" stroke="url(#foilGold)" stroke-width="2.4"/>
  <path d="M1182 90 C1150 88,1148 128,1176 128 C1204 128,1202 92,1169 101" fill="none" stroke="url(#foilGold)" stroke-width="2.4"/>
  <path d="M98 630 C130 632,132 592,104 592 C76 592,78 628,111 619" fill="none" stroke="url(#foilGold)" stroke-width="2.4"/>
  <path d="M1182 630 C1150 632,1148 592,1176 592 C1204 592,1202 628,1169 619" fill="none" stroke="url(#foilGold)" stroke-width="2.4"/>

  <rect x="415" y="210" width="450" height="300" rx="38" fill="url(#creamPaper)" stroke="url(#foilGold)" stroke-width="4" filter="url(#plaqueShadow)"/>
  <rect x="435" y="230" width="410" height="260" rx="28" fill="none" stroke="url(#foilGold)" stroke-width="1.5" opacity="0.9"/>

  <path d="M350 455 C310 405,322 350,384 330" fill="none" stroke="#6f8e6c" stroke-width="5" stroke-linecap="round" filter="url(#stickerShadow)"/>
  <path d="M373 344 C330 319,331 279,390 289 C411 303,405 332,373 344Z" fill="#8cab7e" opacity="0.95" filter="url(#stickerShadow)"/>
  <path d="M326 420 C278 397,277 354,339 363 C365 381,359 409,326 420Z" fill="#9bb58c" opacity="0.95" filter="url(#stickerShadow)"/>
  <ellipse cx="382" cy="438" rx="42" ry="34" fill="#d97997" transform="rotate(-18 382 438)" filter="url(#stickerShadow)"/>
  <ellipse cx="350" cy="437" rx="34" ry="26" fill="#efabc0" transform="rotate(18 350 437)" filter="url(#stickerShadow)"/>
  <ellipse cx="376" cy="405" rx="32" ry="24" fill="#e990aa" transform="rotate(48 376 405)" filter="url(#stickerShadow)"/>
  <circle cx="371" cy="430" r="18" fill="#f7d7b6" filter="url(#stickerShadow)"/>
  <circle cx="306" cy="464" r="10" fill="#b94e6d" filter="url(#stickerShadow)"/>
  <circle cx="332" cy="486" r="7" fill="#d76f86" filter="url(#stickerShadow)"/>

  <path d="M900 247 C955 278,968 352,916 386" fill="none" stroke="#6f8e6c" stroke-width="5" stroke-linecap="round" filter="url(#stickerShadow)"/>
  <path d="M920 262 C967 240,995 270,953 307 C923 312,908 290,920 262Z" fill="#8cab7e" opacity="0.95" filter="url(#stickerShadow)"/>
  <path d="M945 350 C992 335,1015 371,966 399 C936 398,925 371,945 350Z" fill="#9bb58c" opacity="0.95" filter="url(#stickerShadow)"/>
  <ellipse cx="894" cy="281" rx="38" ry="31" fill="#d97997" transform="rotate(22 894 281)" filter="url(#stickerShadow)"/>
  <ellipse cx="928" cy="283" rx="30" ry="24" fill="#efabc0" transform="rotate(-20 928 283)" filter="url(#stickerShadow)"/>
  <ellipse cx="905" cy="316" rx="32" ry="24" fill="#e990aa" transform="rotate(-50 905 316)" filter="url(#stickerShadow)"/>
  <circle cx="906" cy="294" r="16" fill="#f7d7b6" filter="url(#stickerShadow)"/>
  <circle cx="974" cy="246" r="8" fill="#b94e6d" filter="url(#stickerShadow)"/>
  <circle cx="1000" cy="276" r="6" fill="#d76f86" filter="url(#stickerShadow)"/>

  <text x="640" y="302" width="360" text-anchor="middle" font-family="Georgia, 'Times New Roman', Microsoft YaHei, serif" font-size="54" font-style="italic" fill="#7a5a39">Follow</text>
  <text x="640" y="358" width="320" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" letter-spacing="7" fill="#9a8455">— YOUR —</text>
  <text x="640" y="438" width="390" text-anchor="middle" font-family="Georgia, 'Times New Roman', Microsoft YaHei, serif" font-size="78" font-weight="700" letter-spacing="3" fill="#3f4938">HEART</text>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` for wallpaper; build stripes, dots, or damask-like details manually with editable lines/circles/paths.
- ❌ One flattened raster image of the whole collage; it destroys editability and prevents recoloring of frames, flowers, and text.
- ❌ Filtered `<line>` shadows for stems; filters on lines may be dropped, so use filtered `<path>` strokes for botanical stems.
- ❌ `clip-path` on flowers, plaques, or frames; clipping is reliable for images only, not arbitrary shapes.
- ❌ Perfectly symmetrical floral placement; the aesthetic depends on organic overlap that breaks the rigid frame.

## Composition notes
- Keep the central plaque around 35–45% of slide width so the ornate frame and botanical clusters have room to breathe.
- Use gold sparingly but repeatedly: outer frame, inner plaque stroke, corner flourishes, and small accent lines.
- Let florals overlap the plaque and frame edges to create the illusion of foam-mounted paper stickers.
- Maintain a soft vintage palette: sage, cream, dusty rose, muted berry, and warm metallic gold.