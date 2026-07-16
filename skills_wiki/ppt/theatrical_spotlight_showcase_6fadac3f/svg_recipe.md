# SVG Recipe — Theatrical Spotlight Showcase

## Visual mechanism
A dark purple “stage” is framed by a black overhead truss, with translucent spotlights converging onto a glowing floor oval. The featured subject sits center-stage, surrounded by theatrical beams, handwritten-style headline text, and supporting labels that feel like an announcement reveal.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep purple background
- 2× `<rect>` for top and bottom horizontal truss rails
- 16× `<line>` for zig-zag truss bracing and hanging cords
- 5× grouped spotlight fixtures, each built from `<rect>`, `<ellipse>`, and small `<path>` accents
- 5× `<path>` polygons for semi-transparent spotlight beams
- 2× `<ellipse>` for the stage floor and soft glow halo
- 1× `<image>` clipped to a rounded rectangle for the showcased employee/product/photo card
- 1× `<clipPath>` using rounded `<rect>` for the center photo crop
- 2× `<filter>` definitions: one soft glow for the floor/light beams, one shadow for photo and title depth
- 4× `<text>` elements with explicit `width` attributes for headline, role/name label, title, and small sponsor/logo caption
- 1× `<image>` for an optional organization logo block in the lower-left corner

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="stageGlow" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
      <stop offset="58%" stop-color="#f7f2ff" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#d8c4ff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="beamFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.58"/>
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.18"/>
    </linearGradient>
    <filter id="softGlow" x="-30%" y="-40%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
    <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="whiteTextGlow" x="-12%" y="-24%" width="124%" height="150%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoRoundCrop">
      <rect x="510" y="295" width="270" height="275" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#61188a"/>

  <!-- translucent theatrical beams, placed behind the subject -->
  <path d="M94 175 L140 196 L390 585 L335 600 Z" fill="url(#beamFade)" opacity="0.52"/>
  <path d="M388 188 L430 210 L500 586 L440 590 Z" fill="url(#beamFade)" opacity="0.55"/>
  <path d="M636 192 L684 192 L720 585 L560 585 Z" fill="url(#beamFade)" opacity="0.47"/>
  <path d="M895 188 L940 210 L835 590 L775 586 Z" fill="url(#beamFade)" opacity="0.55"/>
  <path d="M1186 175 L1140 196 L890 585 L945 600 Z" fill="url(#beamFade)" opacity="0.52"/>

  <!-- stage floor glow -->
  <ellipse cx="640" cy="586" rx="330" ry="74" fill="url(#stageGlow)" filter="url(#softGlow)" opacity="0.75"/>
  <ellipse cx="640" cy="580" rx="300" ry="64" fill="#ffffff" opacity="0.96"/>

  <!-- center photo card; use an approved portrait/product photo, avoiding unlicensed or sensitive face content -->
  <image href="https://images.example.com/approved-employee-or-product-center-stage-photo.jpg"
         x="510" y="295" width="270" height="275" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoRoundCrop)" filter="url(#dropShadow)"/>

  <!-- truss rails -->
  <rect x="44" y="27" width="1192" height="8" fill="#050505"/>
  <rect x="44" y="92" width="1192" height="8" fill="#050505"/>
  <rect x="44" y="27" width="8" height="73" fill="#050505"/>
  <rect x="1228" y="27" width="8" height="73" fill="#050505"/>

  <!-- truss zig-zag bracing -->
  <line x1="52" y1="35" x2="174" y2="96" stroke="#050505" stroke-width="7"/>
  <line x1="174" y1="96" x2="306" y2="35" stroke="#050505" stroke-width="7"/>
  <line x1="306" y1="35" x2="438" y2="96" stroke="#050505" stroke-width="7"/>
  <line x1="438" y1="96" x2="570" y2="35" stroke="#050505" stroke-width="7"/>
  <line x1="570" y1="35" x2="702" y2="96" stroke="#050505" stroke-width="7"/>
  <line x1="702" y1="96" x2="834" y2="35" stroke="#050505" stroke-width="7"/>
  <line x1="834" y1="35" x2="966" y2="96" stroke="#050505" stroke-width="7"/>
  <line x1="966" y1="96" x2="1098" y2="35" stroke="#050505" stroke-width="7"/>
  <line x1="1098" y1="35" x2="1228" y2="96" stroke="#050505" stroke-width="7"/>

  <!-- hanging cords -->
  <line x1="94" y1="98" x2="94" y2="146" stroke="#050505" stroke-width="7"/>
  <line x1="366" y1="98" x2="366" y2="145" stroke="#050505" stroke-width="7"/>
  <line x1="642" y1="98" x2="642" y2="146" stroke="#050505" stroke-width="7"/>
  <line x1="914" y1="98" x2="914" y2="145" stroke="#050505" stroke-width="7"/>
  <line x1="1189" y1="98" x2="1189" y2="146" stroke="#050505" stroke-width="7"/>

  <!-- spotlights -->
  <g transform="rotate(-46 94 170)">
    <rect x="61" y="132" width="66" height="88" rx="18" fill="#000000"/>
    <ellipse cx="94" cy="220" rx="33" ry="13" fill="#f8f8f2"/>
    <path d="M62 147 Q94 126 126 147" fill="#0b0b0b"/>
  </g>
  <g transform="rotate(-26 388 170)">
    <rect x="355" y="132" width="66" height="88" rx="18" fill="#000000"/>
    <ellipse cx="388" cy="220" rx="33" ry="13" fill="#f8f8f2"/>
    <path d="M356 147 Q388 126 420 147" fill="#0b0b0b"/>
  </g>
  <g>
    <rect x="612" y="132" width="60" height="88" rx="16" fill="#000000"/>
    <ellipse cx="642" cy="218" rx="31" ry="10" fill="#f8f8f2"/>
    <path d="M613 149 Q642 130 671 149" fill="#0b0b0b"/>
  </g>
  <g transform="rotate(26 914 170)">
    <rect x="881" y="132" width="66" height="88" rx="18" fill="#000000"/>
    <ellipse cx="914" cy="220" rx="33" ry="13" fill="#f8f8f2"/>
    <path d="M882 147 Q914 126 946 147" fill="#0b0b0b"/>
  </g>
  <g transform="rotate(46 1189 170)">
    <rect x="1156" y="132" width="66" height="88" rx="18" fill="#000000"/>
    <ellipse cx="1189" cy="220" rx="33" ry="13" fill="#d9d9d2"/>
    <path d="M1157 147 Q1189 126 1221 147" fill="#0b0b0b"/>
  </g>

  <!-- title/name with black fill and white glow stroke, mimicking hand-drawn stage lettering -->
  <text x="470" y="300" width="360" font-family="Segoe Print, Segoe UI, Microsoft YaHei" font-size="56"
        font-weight="700" fill="#000000" stroke="#ffffff" stroke-width="8" paint-order="stroke"
        filter="url(#whiteTextGlow)">Kelli Schwartz</text>

  <text x="390" y="605" width="520" font-family="Segoe Print, Segoe UI, Microsoft YaHei" font-size="43"
        font-weight="700" fill="#000000">Public Guardian – Conservator</text>

  <text x="1045" y="590" width="210" font-family="Segoe Print, Segoe UI, Microsoft YaHei" font-size="56"
        font-weight="700" fill="#ffffff">
    <tspan x="1045" dy="0">Employee</tspan>
    <tspan x="1045" dy="60">Spotlight</tspan>
  </text>

  <!-- optional sponsor/organization logo block -->
  <rect x="24" y="562" width="195" height="103" fill="#ffffff" opacity="0.96"/>
  <image href="https://images.example.com/organization-logo-transparent.png"
         x="58" y="524" width="78" height="78" preserveAspectRatio="xMidYMid meet"/>
  <text x="38" y="624" width="162" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#222222">Department of Health &amp; Human Services</text>
  <text x="39" y="646" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        fill="#5b5b5b">Recognition Program</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to cut the spotlight beams; use translucent `<path>` polygons instead.
- ❌ Applying `filter` to `<line>` truss elements; filters on lines are dropped, so keep truss lines flat black.
- ❌ Clipping non-image elements; only apply `clip-path` to the central `<image>`.
- ❌ Overfilling the stage with text; the theatrical effect depends on a single clear focal subject.
- ❌ Relying on `marker-end` for hanging fixtures or arrows; draw fixtures directly with rectangles, ellipses, and paths.

## Composition notes
- Keep the truss in the top 15% of the canvas; it should frame the scene without competing with the subject.
- The visual focus is the central photo/card and white floor oval; align all beams toward this stage area.
- Use deep purple or midnight blue backgrounds with white translucent beams for maximum contrast and drama.
- Place secondary branding in the lower-left corner and the showcase title in the lower-right to preserve the center-stage reveal.