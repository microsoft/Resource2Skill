# SVG Recipe — 3D Isometric Typography Cubes

## Visual mechanism
Convert bold single-character typography into tactile cube-like blocks by layering a bright rounded-square front face over darker offset side/extrusion faces. Arrange the cubes in a loose isometric scatter so the words feel like physical building blocks tossed onto a dark stage.

## SVG primitives needed
- 1× `<image>` for a dark, cinematic background photo texture
- 2× `<rect>` for full-canvas color wash and translucent title/instruction panels
- 2× `<linearGradient>` for glossy title pill and cube face shading
- 1× `<radialGradient>` for warm spotlight behind the cubes
- 2× `<filter>` definitions: soft shadow for cubes/cards, subtle glow for yellow badges
- 6× cube groups, each using:
  - 1× `<path>` for top/extruded face
  - 1× `<path>` for side/extruded face
  - 1× `<rect rx>` for front rounded-square face
  - 1× `<text>` for the centered bold character
- 4× badge groups using `<path>` scallop/starburst shapes plus `<text>` numbers
- Multiple `<text>` elements with explicit `width` for title, steps, and captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pillGloss" x1="0" y1="40" x2="0" y2="170" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.45"/>
      <stop offset="0.45" stop-color="#444444" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#111111" stop-opacity="0.60"/>
    </linearGradient>
    <linearGradient id="cubeFace" x1="0" y1="0" x2="0" y2="150">
      <stop offset="0" stop-color="#FFD72A"/>
      <stop offset="1" stop-color="#FFC400"/>
    </linearGradient>
    <linearGradient id="goldSide" x1="0" y1="0" x2="120" y2="120">
      <stop offset="0" stop-color="#E7B42D"/>
      <stop offset="1" stop-color="#A96E08"/>
    </linearGradient>
    <radialGradient id="warmSpot" cx="68%" cy="55%" r="42%">
      <stop offset="0" stop-color="#FFD21C" stop-opacity="0.34"/>
      <stop offset="0.48" stop-color="#FFD21C" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <filter id="cubeShadow" x="-30%" y="-30%" width="170%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="badgeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#050505"/>
  <image href="https://images.example.com/macro-colored-pencils-on-black-background.jpg" x="0" y="0" width="1280" height="720" opacity="0.38"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.45"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmSpot)"/>

  <rect x="52" y="50" width="718" height="122" rx="58" fill="url(#pillGloss)" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="1.5"/>
  <text x="144" y="132" width="590" font-family="Microsoft YaHei, Segoe UI" font-size="54" font-weight="800" fill="#FFFFFF">翻轉吧！ 立方字</text>

  <g transform="translate(72 252)">
    <path d="M35,0 L45,12 L61,8 L65,25 L79,34 L70,48 L75,64 L58,67 L47,80 L34,70 L18,75 L14,58 L0,48 L9,34 L4,18 L21,15 Z" fill="#FFD21C" stroke="#FFFFFF" stroke-width="4" filter="url(#badgeGlow)"/>
    <text x="24" y="52" width="30" font-family="Segoe UI" font-size="30" font-weight="800" fill="#000000">1</text>
  </g>
  <text x="152" y="300" width="600" font-family="Microsoft YaHei, Segoe UI" font-size="34" fill="#FFFFFF">插入／圖案／圓角矩形</text>

  <g transform="translate(72 348)">
    <path d="M35,0 L45,12 L61,8 L65,25 L79,34 L70,48 L75,64 L58,67 L47,80 L34,70 L18,75 L14,58 L0,48 L9,34 L4,18 L21,15 Z" fill="#FFD21C" stroke="#FFFFFF" stroke-width="4"/>
    <text x="24" y="52" width="30" font-family="Segoe UI" font-size="30" font-weight="800" fill="#000000">2</text>
  </g>
  <text x="152" y="396" width="590" font-family="Microsoft YaHei, Segoe UI" font-size="34" fill="#FFFFFF">輸入文字，置中並加粗</text>

  <g transform="translate(72 444)">
    <path d="M35,0 L45,12 L61,8 L65,25 L79,34 L70,48 L75,64 L58,67 L47,80 L34,70 L18,75 L14,58 L0,48 L9,34 L4,18 L21,15 Z" fill="#FFD21C" stroke="#FFFFFF" stroke-width="4"/>
    <text x="24" y="52" width="30" font-family="Segoe UI" font-size="30" font-weight="800" fill="#000000">3</text>
  </g>
  <text x="152" y="490" width="650" font-family="Microsoft YaHei, Segoe UI" font-size="34" fill="#FFFFFF">建立右下方金色厚度面</text>

  <g transform="translate(72 540)">
    <path d="M35,0 L45,12 L61,8 L65,25 L79,34 L70,48 L75,64 L58,67 L47,80 L34,70 L18,75 L14,58 L0,48 L9,34 L4,18 L21,15 Z" fill="#FFD21C" stroke="#FFFFFF" stroke-width="4"/>
    <text x="24" y="52" width="30" font-family="Segoe UI" font-size="30" font-weight="800" fill="#000000">4</text>
  </g>
  <text x="152" y="588" width="570" font-family="Microsoft YaHei, Segoe UI" font-size="34" fill="#DDDDDD">旋轉、錯位，像積木散落</text>

  <rect x="780" y="272" width="412" height="374" rx="22" fill="#F2F2F2" filter="url(#cubeShadow)"/>
  <text x="815" y="326" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#777777">Editable SVG-built 3D typography blocks</text>

  <g transform="translate(918 388) rotate(-8)" filter="url(#cubeShadow)">
    <path d="M0,0 L42,-34 L162,-34 L120,0 Z" fill="#F7C84B"/>
    <path d="M120,0 L162,-34 L162,86 L120,120 Z" fill="url(#goldSide)"/>
    <rect x="0" y="0" width="120" height="120" rx="28" fill="url(#cubeFace)"/>
    <text x="22" y="84" width="82" font-family="Microsoft YaHei, Segoe UI" font-size="72" font-weight="900" fill="#000000">翻</text>
  </g>

  <g transform="translate(804 480) rotate(9) scale(0.82)" filter="url(#cubeShadow)">
    <path d="M0,0 L36,-30 L146,-30 L110,0 Z" fill="#F8CC54"/>
    <path d="M110,0 L146,-30 L146,80 L110,110 Z" fill="#B8790B"/>
    <rect x="0" y="0" width="110" height="110" rx="25" fill="url(#cubeFace)"/>
    <text x="20" y="78" width="78" font-family="Microsoft YaHei, Segoe UI" font-size="66" font-weight="900" fill="#000000">轉</text>
  </g>

  <g transform="translate(1046 488) rotate(13) scale(0.72)" filter="url(#cubeShadow)">
    <path d="M0,0 L34,-28 L134,-28 L100,0 Z" fill="#FAD45E"/>
    <path d="M100,0 L134,-28 L134,72 L100,100 Z" fill="#A96E08"/>
    <rect x="0" y="0" width="100" height="100" rx="23" fill="url(#cubeFace)"/>
    <text x="22" y="72" width="65" font-family="Microsoft YaHei, Segoe UI" font-size="60" font-weight="900" fill="#000000">吧</text>
  </g>

  <g transform="translate(872 210) rotate(-16) scale(0.74)" filter="url(#cubeShadow)">
    <path d="M0,0 L34,-28 L134,-28 L100,0 Z" fill="#F9D056"/>
    <path d="M100,0 L134,-28 L134,72 L100,100 Z" fill="#B8790B"/>
    <rect x="0" y="0" width="100" height="100" rx="22" fill="url(#cubeFace)"/>
    <text x="21" y="72" width="66" font-family="Microsoft YaHei, Segoe UI" font-size="60" font-weight="900" fill="#000000">立</text>
  </g>

  <g transform="translate(1036 234) rotate(7) scale(0.78)" filter="url(#cubeShadow)">
    <path d="M0,0 L36,-30 L146,-30 L110,0 Z" fill="#F8CC54"/>
    <path d="M110,0 L146,-30 L146,80 L110,110 Z" fill="#A96E08"/>
    <rect x="0" y="0" width="110" height="110" rx="25" fill="url(#cubeFace)"/>
    <text x="22" y="78" width="76" font-family="Microsoft YaHei, Segoe UI" font-size="66" font-weight="900" fill="#000000">方</text>
  </g>

  <g transform="translate(1112 364) rotate(-11) scale(0.66)" filter="url(#cubeShadow)">
    <path d="M0,0 L34,-28 L134,-28 L100,0 Z" fill="#FAD45E"/>
    <path d="M100,0 L134,-28 L134,72 L100,100 Z" fill="#B8790B"/>
    <rect x="0" y="0" width="100" height="100" rx="22" fill="url(#cubeFace)"/>
    <text x="20" y="72" width="68" font-family="Microsoft YaHei, Segoe UI" font-size="60" font-weight="900" fill="#000000">字</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using PowerPoint-only 3D extrusion assumptions in SVG; instead, draw visible top/side faces explicitly as editable paths.
- ❌ Applying `filter` to `<line>` for shadows; cube shadows should be on `<rect>`, `<path>`, or `<text>` only.
- ❌ Clipping cube faces with `clip-path` on shapes; only images should receive clip paths if used.
- ❌ Building cube geometry with `<use>` symbols; duplicate the path/rect/text structure for each cube so translation remains reliable.
- ❌ Tiny multi-line text inside cubes; the technique works best with one bold character or very short words.

## Composition notes
- Keep the cubes in the right half or center stage, with enough empty dark space around them so their shadows and extrusion read clearly.
- Use a saturated yellow face, darker gold side faces, and black typography for maximum “toy block” legibility.
- Vary rotation and scale slightly; too much alignment makes the cubes look like icons instead of physical blocks.
- Pair the playful 3D typography with a subdued background photo or dark gradient so the bright cube faces become the visual focus.