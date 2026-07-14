# SVG Recipe — Transparent Geometric Shard Overlay

## Visual mechanism
A full-bleed photo is fragmented by overlapping semi-transparent, sharp-angled polygons so the image shows through like tinted glass. A solid diagonal white block cuts across the lower slide to create a calm typography zone against the dynamic faceted top layer.

## SVG primitives needed
- 1× `<image>` for the full-bleed architectural/city background photo
- 1× translucent `<rect>` for subtle global photo darkening
- 10× `<path>` for cyan/navy geometric shards and angular white typography block
- 1× `<filter id="softShadow">` applied to the white diagonal block for separation from the photo
- 1× `<filter id="textGlow">` applied to white accent text inside the shards
- 4× `<line>` for fine diagonal facet seams and small data separators
- 3× `<rect>` for compact KPI/data cards in the white block
- 3× `<circle>` for small icon dots beside KPI values
- 8× `<text>` with explicit `width` attributes for headline, body, year, labels, and KPI values

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0D2A4E"/>
      <stop offset="100%" stop-color="#154376"/>
    </linearGradient>
    <linearGradient id="cyanShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00D2C2"/>
      <stop offset="100%" stop-color="#008EAF"/>
    </linearGradient>
    <linearGradient id="tealShard" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00B89F"/>
      <stop offset="100%" stop-color="#31E6D0"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-30%" width="120%" height="160%">
      <feOffset dx="0" dy="-8"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#101820"/>
  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/full-bleed-modern-glass-city-architecture-at-dusk.jpg"
         preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="#031A31" opacity="0.24"/>

  <!-- Transparent geometric shard overlay -->
  <path d="M0 42 L1140 330 L0 574 Z" fill="url(#navyShard)" opacity="0.78"/>
  <path d="M0 0 L650 0 L1152 330 L0 138 Z" fill="#154376" opacity="0.58"/>
  <path d="M570 0 L1280 0 L1280 382 L1090 336 Z" fill="#0B315A" opacity="0.64"/>
  <path d="M740 86 L1280 250 L1280 454 L1026 362 Z" fill="url(#cyanShard)" opacity="0.66"/>
  <path d="M122 188 L708 65 L978 320 L318 262 Z" fill="#00B89F" opacity="0.42"/>
  <path d="M370 270 L910 316 L632 462 L70 346 Z" fill="#092947" opacity="0.56"/>
  <path d="M0 430 L396 360 L640 454 L0 566 Z" fill="#00A8C8" opacity="0.36"/>
  <path d="M920 98 L1280 196 L1280 294 L1052 236 Z" fill="#ffffff" opacity="0.13"/>
  <path d="M210 0 L520 0 L356 118 L0 92 Z" fill="#ffffff" opacity="0.10"/>

  <!-- Thin facet seams, intentionally imperfect and diagonal -->
  <line x1="0" y1="138" x2="1152" y2="330" stroke="#FFFFFF" stroke-width="1.4" opacity="0.28"/>
  <line x1="122" y1="188" x2="978" y2="320" stroke="#FFFFFF" stroke-width="1.2" opacity="0.18"/>
  <line x1="640" y1="454" x2="1280" y2="250" stroke="#00E6D0" stroke-width="1.6" opacity="0.26"/>
  <line x1="570" y1="0" x2="1026" y2="362" stroke="#FFFFFF" stroke-width="1.1" opacity="0.20"/>

  <!-- White angular base block for readable content -->
  <path d="M0 515 L1280 404 L1280 720 L0 720 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M0 492 L1280 382 L1280 424 L0 535 Z" fill="#00B89F" opacity="0.92"/>
  <path d="M0 474 L1280 366 L1280 382 L0 492 Z" fill="#154376" opacity="0.98"/>

  <!-- Accent year inside the glass shards -->
  <text x="930" y="214" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="74"
        font-weight="700" fill="#FFFFFF" opacity="0.95" filter="url(#textGlow)">2026</text>
  <text x="937" y="252" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="600" letter-spacing="3" fill="#D8FFF8" opacity="0.88">MARKET OUTLOOK</text>

  <!-- Main typography in the white wedge -->
  <text x="76" y="574" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="46"
        font-weight="800" fill="#154376">Urban Intelligence Platform</text>
  <text x="78" y="617" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="19"
        font-weight="400" fill="#52606D">
    Converting fragmented city signals into confident portfolio decisions.
  </text>

  <!-- Compact KPI cards -->
  <rect x="742" y="548" width="150" height="86" rx="18" fill="#F3F7FA"/>
  <circle cx="770" cy="579" r="8" fill="#00B89F"/>
  <text x="790" y="584" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="700" fill="#154376">+18%</text>
  <text x="766" y="615" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        fill="#687887">YoY demand</text>

  <rect x="916" y="548" width="150" height="86" rx="18" fill="#F3F7FA"/>
  <circle cx="944" cy="579" r="8" fill="#154376"/>
  <text x="964" y="584" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="700" fill="#154376">42M</text>
  <text x="940" y="615" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        fill="#687887">signals read</text>

  <rect x="1090" y="548" width="150" height="86" rx="18" fill="#F3F7FA"/>
  <circle cx="1118" cy="579" r="8" fill="#00A8C8"/>
  <text x="1138" y="584" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        font-weight="700" fill="#154376">91%</text>
  <text x="1114" y="615" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        fill="#687887">model fit</text>

  <line x1="742" y1="664" x2="1240" y2="664" stroke="#D5DEE7" stroke-width="1"/>
  <text x="742" y="690" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        fill="#8A97A3">Semi-transparent polygons remain editable; replace the photo to retheme the entire cover.</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to create the shard effect; layer translucent polygon `<path>` elements instead.
- ❌ Applying `clip-path` to shard shapes; clipping is only safe on `<image>` elements.
- ❌ Building the facets with `<pattern>` fills; use real overlapping paths so each shard remains editable.
- ❌ Adding arrowheads with `marker-end` on diagonal seams; if arrows are needed, use separate `<line>` elements without inherited markers.
- ❌ Placing text directly over the busiest photo area without the white diagonal base block.

## Composition notes
- Keep the top 60–70% visually energetic with photo and translucent shards; reserve the bottom diagonal wedge for readable content.
- Use 2–3 brand colors only, then rely on opacity overlap to create richer intermediate tones.
- Let shards cross the full canvas edges so the geometry feels cropped and intentional, not like floating triangles.
- Put one large accent item, such as a year or short label, inside the colored shard field to connect the image area with the typography zone.